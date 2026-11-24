#!/usr/bin/env python3
"""Render Russian narration, check every part with Whisper, and retry weak parts.

Run this script in the bedtime environment. It invokes f5_russian.py in the F5
environment, keeps the best deterministic seed for each part, and performs one
final assembly. The loop is bounded by --max-attempts.

usage: russian_quality_loop.py PARTS --out OUT.m4a [--mode nighttime|morning]
       [--music TRACK] [--max-attempts 3] [--workers 2]
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import audio_tools as A
import f5_russian as F5

HERE = Path(__file__).resolve().parent
HOME = Path.home()
BASE = HOME / "bedtime-audiobooks"
MODELS = {"small": "openai/whisper-small", "turbo": "openai/whisper-large-v3-turbo"}
RUSSIAN_WORD = re.compile(r"[А-Яа-яЁё+]+")
PLAIN_WORD = re.compile(r"[а-я]+")
VOWELS = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text: str) -> list[str]:
    return PLAIN_WORD.findall(text.lower().replace("ё", "е").replace("+", ""))


def edit_distance(left: list | str, right: list | str) -> int:
    if len(left) < len(right):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (a != b)))
        previous = current
    return previous[-1]


def transcript_score(expected: str, heard: str) -> dict:
    expected_words, heard_words = words(expected), words(heard)
    expected_chars, heard_chars = "".join(expected_words), "".join(heard_words)
    char_errors = edit_distance(expected_chars, heard_chars)
    return {
        "expected_words": expected_words,
        "heard_words": heard_words,
        "word_errors": edit_distance(expected_words, heard_words),
        "char_errors": char_errors,
        "expected_characters": len(expected_chars),
        "character_error_rate": round(char_errors / max(1, len(expected_chars)), 4),
    }


def score_rank(score: dict) -> tuple[int, int, int]:
    return (
        int(score["char_errors"]),
        int(score["word_errors"]),
        abs(len(score["expected_words"]) - len(score["heard_words"])),
    )


def stress_issues(text: str) -> list[str]:
    issues = []
    for line_number, line in enumerate(text.splitlines(), 1):
        for token in RUSSIAN_WORD.findall(line):
            letters = token.replace("+", "")
            marks = token.count("+")
            if marks and any(i + 1 == len(token) or token[i + 1] not in VOWELS for i, ch in enumerate(token) if ch == "+"):
                issues.append(f"line {line_number}: stress mark is not before a vowel in {token}")
                continue
            vowel_count = sum(ch in VOWELS for ch in letters)
            if "ё" in letters.lower():
                if marks:
                    issues.append(f"line {line_number}: word with ё must not have a stress mark: {token}")
            elif vowel_count >= 2 and marks != 1:
                issues.append(f"line {line_number}: expected one stress mark in {token}")
    return issues


def matching_plain_source(source: Path) -> Path | None:
    suffix = ".stressed.txt"
    if source.name.endswith(suffix):
        candidate = source.with_name(source.name[:-len(suffix)] + ".txt")
        if candidate.is_file():
            return candidate
    return None


def write_seeds(path: Path, seeds: list[int]) -> None:
    path.write_text(json.dumps(seeds) + "\n", encoding="utf-8")


def run_f5(
    args,
    source: Path,
    seeds_path: Path,
    chunk_manifest: Path | None,
    synthesize_only: bool,
) -> None:
    cmd = [
        str(Path(args.f5_python).expanduser()),
        str(HERE / "f5_russian.py"),
        str(source),
        "--out",
        str(Path(args.out).expanduser()),
        "--config",
        str(Path(args.config).expanduser()),
        "--work",
        str(Path(args.work).expanduser()),
        "--workers",
        str(args.workers),
        "--mode",
        args.mode,
        "--seeds",
        str(seeds_path),
        "--device",
        args.device,
        "--min-part-words",
        str(args.min_part_words),
        "--form",
        args.form,
    ]
    if args.reference:
        cmd += ["--reference", str(Path(args.reference).expanduser())]
    if args.trim_edges is not None:
        cmd += ["--trim-edges", str(args.trim_edges)]
    if chunk_manifest:
        cmd += ["--chunk-manifest", str(chunk_manifest)]
    if synthesize_only:
        cmd.append("--synthesize-only")
    elif args.music:
        cmd += ["--music", str(Path(args.music).expanduser())]
        if args.music_lufs is not None:
            cmd += ["--music-lufs", str(args.music_lufs)]
    subprocess.run(cmd, check=True)


def load_transcriber(model_name: str, threads: int, device: str = "cpu"):
    os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    import torch
    from transformers import pipeline  # pyright: ignore[reportMissingImports]

    torch.set_num_threads(threads)
    torch.set_num_interop_threads(1)
    if device == "cuda":
        return pipeline("automatic-speech-recognition", model=MODELS[model_name], device=0,
                        torch_dtype=torch.float16)
    return pipeline("automatic-speech-recognition", model=MODELS[model_name], device=-1)


def transcribe(transcriber, path: Path) -> str:
    audio, _ = A.decode(path, sr=16000)
    result = transcriber(
        audio.copy(),
        return_timestamps=False,
        generate_kwargs={"language": "russian", "task": "transcribe"},
    )
    return result["text"].strip()


def main() -> None:
    ap = argparse.ArgumentParser(description="Bounded ASR quality loop for Russian F5 narration.")
    ap.add_argument("parts", help="stress-marked .txt or parts .json")
    ap.add_argument("--out", required=True, help="final .m4a")
    ap.add_argument("--config", default=str(HERE / "config/russian-standard.json"))
    ap.add_argument("--reference", default=None)
    ap.add_argument("--work", default=None, help="cache folder; default: books-ru/<output name>")
    ap.add_argument("--f5-python", default=str(BASE / "f5-env/bin/python"))
    ap.add_argument("--mode", choices=("nighttime", "morning"), default="nighttime")
    ap.add_argument("--music", default=None, help="optional music file; it loops to the narration length")
    ap.add_argument("--music-lufs", type=float, default=None, help="override the mode's music loudness")
    ap.add_argument("--model", choices=sorted(MODELS), default="turbo")
    ap.add_argument("--max-attempts", type=int, default=3, help="total seeds per failing part, including the first")
    ap.add_argument("--max-char-errors", type=int, default=0, help="accepted ASR character edits per part")
    ap.add_argument("--workers", type=int, choices=(1, 2), default=2)
    ap.add_argument("--threads", type=int, default=8, help="Whisper CPU threads")
    ap.add_argument("--trim-edges", type=float, default=None)
    ap.add_argument("--allow-stress-issues", action="store_true", help="render despite strict stress validation errors")
    ap.add_argument("--require-pass", action="store_true", help="exit 2 when any part still fails after final assembly")
    ap.add_argument("--assume-baseline-pass", action="store_true",
                    help="with --baseline: a part that was never checked in the baseline counts as passing")
    ap.add_argument("--baseline", default=None,
                    help="earlier .quality.json; a part with the same text and the same seed keeps its score "
                         "and is not transcribed again")
    ap.add_argument("--device", choices=("auto", "cuda", "cpu"), default="auto",
                    help="device for synthesis and Whisper; auto uses CUDA when it is available and has VRAM free")
    ap.add_argument("--min-part-words", type=int, default=None,
                    help="join the sentences of a paragraph until a part has this many words (default: the mode's)")
    ap.add_argument("--form", choices=("prose", "verse"), default="prose", help="verse never joins sentence lines")
    args = ap.parse_args()

    if not 1 <= args.max_attempts <= 8:
        ap.error("--max-attempts must be from 1 to 8")
    if args.max_char_errors < 0:
        ap.error("--max-char-errors must not be negative")
    if args.music_lufs is not None and not args.music:
        ap.error("--music-lufs requires --music")

    source = Path(args.parts).expanduser().resolve()
    config_path = Path(args.config).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    args.out = str(out)
    args.config = str(config_path)
    args.work = str(Path(args.work).expanduser().resolve() if args.work else BASE / "books-ru" / out.stem)
    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)

    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    if args.mode not in cfg.get("modes", {}):
        sys.exit(f"mode {args.mode!r} is missing from {config_path}")
    mode = cfg["modes"][args.mode]
    args.min_part_words = args.min_part_words if args.min_part_words is not None else int(mode.get("min_part_words", 0))
    args.device, device_reason = F5.resolve_device(args.device)
    print(f"device: {args.device} for synthesis and Whisper ({device_reason})", flush=True)
    parts = F5.load_parts(source, float(mode["pause_line_s"]), float(mode["pause_paragraph_s"]),
                          args.min_part_words, args.form)
    if not parts:
        sys.exit(f"no text in {source}")

    stress = stress_issues("\n".join(part["text"] for part in parts))
    plain = matching_plain_source(source)
    if plain and source.read_text(encoding="utf-8").replace("+", "") != plain.read_text(encoding="utf-8"):
        stress.append(f"{source.name} without stress marks differs from {plain.name}")
    if stress:
        print("STRESS VALIDATION", file=sys.stderr)
        for issue in stress:
            print(f"  {issue}", file=sys.stderr)
        if not args.allow_stress_issues:
            sys.exit("fix the stress text or use --allow-stress-issues")

    seed_base = int(cfg["generation"]["seed_base"])
    original_seeds = [int(part["seed"]) if part["seed"] is not None else seed_base + i for i, part in enumerate(parts)]
    selected_seeds = original_seeds.copy()
    histories: list[list[dict[str, Any]]] = [[] for _ in parts]
    selected_scores: list[dict[str, Any] | None] = [None] * len(parts)
    selected_heard: list[str | None] = [None] * len(parts)
    started = time.monotonic()
    transcriber = None
    seed_stride = 1_000_003
    inherited = 0
    if args.baseline:
        baseline = json.loads(Path(args.baseline).expanduser().read_text(encoding="utf-8"))
        old_parts = baseline.get("parts", [])
        if len(old_parts) != len(parts):
            print(f"baseline has {len(old_parts)} parts, story has {len(parts)}; matching by text only",
                  file=sys.stderr)
        old_counts = Counter(p.get("text") for p in old_parts)
        new_counts = Counter(p["text"] for p in parts)
        by_text = {p["text"]: p for p in old_parts if old_counts[p.get("text")] == 1 and new_counts[p["text"]] == 1}
        if True:
            for i, part in enumerate(parts):
                old = by_text.get(part["text"])
                if old is None and i < len(old_parts) and old_parts[i].get("text") == part["text"]:
                    old = old_parts[i]
                if old is None:
                    continue
                if old.get("selected_seed") == original_seeds[i] or old["text"] == parts[i]["text"]:
                    # a part with the same text keeps its old seed too, so an earlier edit elsewhere in the
                    # story cannot change the audio or invalidate the score
                    original_seeds[i] = old["selected_seed"]
                    selected_seeds[i] = old["selected_seed"]
                    score = old.get("selected_score")
                    if score is None and args.assume_baseline_pass:
                        score = {"expected_words": [], "heard_words": [], "word_errors": 0, "char_errors": 0,
                                 "expected_characters": 0, "character_error_rate": 0.0, "unchecked": True}
                    selected_scores[i] = score
                    selected_heard[i] = old.get("selected_heard")
                    histories[i] = old.get("attempts", [])
                    inherited += 1
            print(f"baseline: {inherited} of {len(parts)} parts reused")
            if inherited < len(parts) and baseline.get("asr_model") != args.model:
                print(f"baseline used {baseline.get('asr_model')} but this run uses {args.model}", file=sys.stderr)

    transcribed = 0
    transcription_s = 0.0

    for attempt in range(1, args.max_attempts + 1):
        pending = [i for i in range(len(parts)) if selected_scores[i] is None] if attempt == 1 else [
            i for i, score in enumerate(selected_scores)
            if score is None or score["char_errors"] > args.max_char_errors
        ]
        if not pending:
            break
        candidate_seeds = selected_seeds.copy()
        if attempt > 1:
            for i in pending:
                candidate_seeds[i] = original_seeds[i] + (attempt - 1) * seed_stride

        seeds_path = work / f"quality-attempt-{attempt}.seeds.json"
        manifest_path = work / f"quality-attempt-{attempt}.chunks.json"
        write_seeds(seeds_path, candidate_seeds)
        run_f5(args, source, seeds_path, manifest_path, synthesize_only=True)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        chunks = {int(item["index"]): Path(item["path"]) for item in manifest["parts"]}
        if transcriber is None:
            transcriber = load_transcriber(args.model, args.threads, args.device)
            print(f"whisper device: {args.device} ({MODELS[args.model]}, "
                  f"{'float16' if args.device == 'cuda' else str(args.threads) + ' CPU threads'})", flush=True)

        for i in pending:
            t0 = time.monotonic()
            heard = transcribe(transcriber, chunks[i])
            elapsed = time.monotonic() - t0
            transcribed += 1
            transcription_s += elapsed
            score = transcript_score(parts[i]["text"], heard)
            record = {
                "attempt": attempt,
                "seed": candidate_seeds[i],
                "heard": heard,
                "transcribe_s": round(elapsed, 2),
                **score,
            }
            histories[i].append(record)
            current = selected_scores[i]
            if current is None or score_rank(score) < score_rank(current):
                selected_scores[i] = score
                selected_seeds[i] = candidate_seeds[i]
                selected_heard[i] = heard
            print(json.dumps({"index": i, **record, "selected": selected_seeds[i] == candidate_seeds[i]}, ensure_ascii=False), flush=True)

    final_seeds = work / "quality-selected.seeds.json"
    write_seeds(final_seeds, selected_seeds)
    run_f5(args, source, final_seeds, work / "quality-selected.chunks.json", synthesize_only=False)
    if transcribed:
        print(f"TRANSCRIPTION {args.device} | {transcribed} parts in {transcription_s:.1f} s | "
              f"{transcription_s / transcribed:.2f} s per part", flush=True)

    unresolved = [
        i for i, score in enumerate(selected_scores)
        if score is None or score["char_errors"] > args.max_char_errors
    ]
    report_path = out.with_suffix(".quality.json")
    report = {
        "schema": 1,
        "source": str(source),
        "source_sha256": file_sha256(source),
        "config": str(config_path),
        "config_sha256": file_sha256(config_path),
        "output": str(out),
        "output_sha256": file_sha256(out),
        "mode": args.mode,
        "seeds_file": str(final_seeds),
        "music": str(Path(args.music).expanduser().resolve()) if args.music else None,
        "asr_model": args.model,
        "asr_device": args.device,
        "min_part_words": args.min_part_words,
        "form": args.form,
        "transcribed_parts": transcribed,
        "transcription_s": round(transcription_s, 1),
        "baseline": str(Path(args.baseline).expanduser().resolve()) if args.baseline else None,
        "inherited_parts": inherited,
        "max_attempts": args.max_attempts,
        "max_char_errors": args.max_char_errors,
        "stress_issues": stress,
        "unresolved_parts": unresolved,
        "passed": not unresolved,
        "wall_s": round(time.monotonic() - started, 1),
        "parts": [
            {
                "index": i,
                "text": part["text"],
                "selected_seed": selected_seeds[i],
                "selected_heard": selected_heard[i],
                "selected_score": selected_scores[i],
                "attempts": histories[i],
            }
            for i, part in enumerate(parts)
        ],
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"QUALITY {'PASS' if not unresolved else 'REVIEW'} | {len(parts) - len(unresolved)}/{len(parts)} parts pass | {report_path}")
    if unresolved and args.require_pass:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
