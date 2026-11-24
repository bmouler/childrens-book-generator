#!/usr/bin/env python3
"""Build one Russian story end to end: place the mode, improve the text, render, mix, gate.

The order is the point. The story gets its mode from stories/modes.json and the cue words must
agree, so a morning story can never take the night bed. The critic loop then edits the text. Only
after that does the renderer run, so a rejected line is never synthesized. The mix gets the bed the
mode names. Two measurements decide whether the result replaces the current file: the spread of the
part joins, and loudness. The new file stays in .next.m4a until both pass.

A line that starts with '# ' is a chapter heading. It is never read aloud and it is never a part.
A story with headings builds one chapter at a time under books-ru/STORY/chapters/NN/. A chapter whose
text and settings hashes are unchanged is reused without synthesis or transcription, so a failed
chapter costs nothing for the others. The chapters are then joined in order and the whole story is
mixed, measured and gated exactly like a story without headings. That story keeps the old path.

usage: story_build.py STORY [--mode auto|nighttime|morning] [--rounds 2] [--skip-critique]
       [--dry-run] [--workers 2] [--threads 8] [--max-unresolved 2] [--device auto|cuda|cpu]
       [--min-part-words N] [--chapters A-B]

Run this on the render machine in the bedtime env. narration/build_story.sh ships the
code and the text and pulls the result back. --chapters A-B builds only that chapter range for a
listen and never replaces the finished story. --device auto borrows the GPU once for the whole
render through gpu-run.sh --exec, so synthesis and every Whisper round share one window.
Set GPU_HOLD_SERVICE if a user service must be stopped and restored. --device cpu never touches the GPU.
"""
import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import f5_russian as F5
import story_modes as M
import story_values as V
from background_music import measure_loudnorm

HERE = Path(__file__).resolve().parent
BASE = Path.home() / "bedtime-audiobooks"
STORIES = BASE / "stories"
CONFIG = HERE / "config/russian-standard.json"
REGISTRY = STORIES / "modes.json"
MUSIC = BASE / "music"
LUFS_TOLERANCE = 0.7
PEAK_CEILING = -1.5


def run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    print("+", " ".join(command), flush=True)
    return subprocess.run(command, check=False, **kwargs)


def chapter_range(spec: str | None, count: int) -> set[int] | None:
    """'1-3' or '2' selects those chapter numbers. Chapters are numbered from 0."""
    if spec is None:
        return None
    try:
        first, _, last = spec.partition("-")
        chosen = set(range(int(first), int(last or first) + 1))
    except ValueError:
        sys.exit(f"--chapters wants A-B with numbers, not {spec!r}")
    unknown = chosen - set(range(count))
    if unknown:
        sys.exit(f"--chapters {spec}: the story has chapters 0 to {count - 1}")
    return chosen


def unresolved_limit(parts: int, explicit: int | None) -> int:
    """How many ASR-failing parts a build may keep. A 25-part story keeps 2. A long story keeps 2 percent,
    because the checker's misses scale with length: a final devoiced consonant or an unstressed vowel is
    heard as another letter in about one part in fifty, and that is the checker, not the voice."""
    if explicit is not None:
        return explicit
    return max(2, math.ceil(parts * 0.02))


def chapter_settings(cfg: dict, mode_name: str, form: str, min_part_words: int) -> dict:
    """Everything that changes a chapter's audio or its part boundaries.

    The device is absent on purpose. The part cache does not depend on it, so a chapter rendered on
    the CPU is reused on the GPU. The music is absent too: only the joined story is mixed.
    """
    gen, mode = cfg["generation"], cfg["modes"][mode_name]
    return {
        "config_sha256": M.sha256(CONFIG),
        "mode": mode_name,
        "form": form,
        "min_part_words": min_part_words,
        "pause_line_s": mode["pause_line_s"],
        "pause_paragraph_s": mode["pause_paragraph_s"],
        "part_edge_s": mode["part_edge_s"],
        "speed": gen["speed"],
        "seed_base": gen["seed_base"],
        "nfe_step": gen["nfe_step"],
        "cfg_strength": gen["cfg_strength"],
        "reference_sha256": cfg["reference"]["wav_sha256"],
        "revision": cfg["model"]["revision"],
        "checkpoint": cfg["model"]["checkpoint"],
    }


def loop_command(args, source: Path, out: Path, work: Path, mode_name: str, edge_s: float,
                 form: str, min_part_words: int, bed: Path | None) -> list[str]:
    command = [
        sys.executable, str(HERE / "russian_quality_loop.py"), str(source),
        "--out", str(out), "--work", str(work), "--mode", mode_name,
        "--trim-edges", str(edge_s), "--workers", str(args.workers), "--threads", str(args.threads),
        "--f5-python", args.python, "--require-pass", "--device", args.device,
        "--min-part-words", str(min_part_words), "--form", form,
    ]
    if bed is not None:
        command += ["--music", str(bed)]
    return command


def render_chapters(args, cfg, placed, chapters, work, staged, bed, form, min_part_words, wanted):
    """Build each chapter, then join the selected chunks and assemble the whole story once."""
    mode = cfg["modes"][placed["mode"]]
    settings = chapter_settings(cfg, placed["mode"], form, min_part_words)
    settings_sha = hashlib.sha256(json.dumps(settings, sort_keys=True).encode()).hexdigest()
    reports = []
    for index, chapter in enumerate(chapters):
        if wanted is not None and index not in wanted:
            continue
        cdir = work / "chapters" / f"{index:02d}"
        cdir.mkdir(parents=True, exist_ok=True)
        ctext = cdir / "text.stressed.txt"
        render = cdir / "render.m4a"
        quality_path = render.with_suffix(".quality.json")
        manifest_path = cdir / "quality-selected.chunks.json"
        meta_path = cdir / "chapter.json"
        text_sha = hashlib.sha256(chapter["text"].encode()).hexdigest()
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
        label = chapter["title"] or "opening"
        cached = (
            meta.get("text_sha256") == text_sha
            and meta.get("settings_sha256") == settings_sha
            and quality_path.is_file()
            and manifest_path.is_file()
            and all(Path(p["path"]).is_file() for p in json.loads(manifest_path.read_text(encoding="utf-8"))["parts"])
        )
        if cached:
            print(f"chapter {index:02d} ({label}): reused, text and settings unchanged", flush=True)
        else:
            if not meta:
                reason = "new chapter"
            elif meta.get("text_sha256") != text_sha:
                reason = "text changed"
            else:
                reason = "settings changed or chunks missing"
            print(f"chapter {index:02d} ({label}): building, {reason}", flush=True)
            ctext.write_text(chapter["text"], encoding="utf-8")
            command = loop_command(args, ctext, render, cdir, placed["mode"], mode["part_edge_s"],
                                   form, min_part_words, None)
            if quality_path.is_file():
                command += ["--baseline", str(quality_path)]
            if run(command).returncode not in (0, 2):
                sys.exit(f"chapter {index:02d} failed. The other chapters keep their results. "
                         "Run the same command again to resume.")
            meta = {"index": index, "title": chapter["title"], "text_sha256": text_sha,
                    "settings_sha256": settings_sha, "settings": settings,
                    "parts": len(json.loads(quality_path.read_text(encoding="utf-8"))["parts"])}
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reports.append((index, cdir, json.loads(quality_path.read_text(encoding="utf-8"))))

    # One part list for the whole story. Each chapter ends on the paragraph pause, so joining the
    # lists puts exactly that pause between chapters. The selected chunks are linked into the story
    # cache under their whole-story index, which is what the assembler and the seam gate read.
    combined, seeds, quality_parts, unresolved = [], [], [], []
    inherited, wall = 0, 0.0
    for index, cdir, report in reports:
        parts = F5.load_parts(cdir / "text.stressed.txt", mode["pause_line_s"], mode["pause_paragraph_s"],
                              min_part_words, form)
        chapter_seeds = json.loads((cdir / "quality-selected.seeds.json").read_text(encoding="utf-8"))
        manifest = json.loads((cdir / "quality-selected.chunks.json").read_text(encoding="utf-8"))
        chunks = {int(p["index"]): Path(p["path"]) for p in manifest["parts"]}
        inherited += int(report.get("inherited_parts", 0))
        wall += float(report.get("wall_s", 0.0))
        for local, part in enumerate(parts):
            combined.append({"text": part["text"], "pause": part["pause"], "seed": chapter_seeds[local]})
            seeds.append(chapter_seeds[local])
            source = chunks[local]
            target = work / f"{len(combined) - 1:04d}-{source.name.split('-', 1)[1]}"
            if not target.exists():
                try:
                    os.link(source, target)
                except OSError:
                    shutil.copy2(source, target)
            entry = dict(report["parts"][local])
            entry["index"] = len(quality_parts)
            entry["chapter"] = index
            if local in report["unresolved_parts"]:
                unresolved.append(len(quality_parts))
            quality_parts.append(entry)
    parts_path = work / "parts.combined.json"
    parts_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seeds_path = work / "quality-selected.seeds.json"
    seeds_path.write_text(json.dumps(seeds) + "\n", encoding="utf-8")

    command = [
        str(Path(args.python).expanduser()), str(HERE / "f5_russian.py"), str(parts_path),
        "--out", str(staged), "--config", str(CONFIG), "--work", str(work), "--mode", placed["mode"],
        "--music", str(bed), "--trim-edges", str(mode["part_edge_s"]), "--seeds", str(seeds_path),
        "--device", args.device, "--min-part-words", str(min_part_words), "--form", form,
    ]
    if run(command).returncode:
        sys.exit("the final assembly failed")
    quality = {
        "schema": 1,
        "source": str(STORIES / f"{args.story}.stressed.txt"),
        "output": str(staged),
        "mode": placed["mode"],
        "asr_model": reports[0][2].get("asr_model"),
        "asr_device": reports[0][2].get("asr_device"),
        "transcription_s": round(sum(float(report[2].get("transcription_s", 0.0)) for report in reports), 1),
        "min_part_words": min_part_words,
        "form": form,
        "chapters": [{"index": index, "title": chapters[index]["title"], "dir": str(cdir),
                      "passed": report["passed"]} for index, cdir, report in reports],
        "inherited_parts": inherited,
        "unresolved_parts": unresolved,
        "passed": not unresolved,
        "wall_s": round(wall, 1),
        "parts": quality_parts,
    }
    quality_path = staged.with_suffix(".quality.json")
    quality_path.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return parts_path


def values_gate(story: str, text: str, registry: dict, when: str) -> None:
    """Stop before any audio exists when the values record or the content breaks a rule."""
    errors, warnings = V.check_story(story, text, registry)
    if errors:
        sys.exit(f"VALUES {when}: " + " | ".join(errors[:8]))
    notes = sum(1 for item in warnings if item.startswith(V.NOTE))
    print(f"values {', '.join(registry[story]['values'])} | content clean {when} | "
          f"{len(warnings) - notes} warnings, {notes} notes")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build and gate one Russian story.")
    ap.add_argument("story")
    ap.add_argument("--mode", default="auto", help="auto follows stories/modes.json")
    ap.add_argument("--rounds", type=int, default=1, help="critic passes")
    ap.add_argument("--skip-critique", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="critique only, no render, no install")
    ap.add_argument("--workers", type=int, choices=(1, 2), default=2)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--max-unresolved", type=int, default=None,
                    help="accepted ASR-failing parts. Default: 2, or 2 percent of the parts when that is more")
    ap.add_argument("--assume-baseline-pass", action="store_true",
                    help="trust a baseline that was never ASR-checked (seeded from an old manifest)")
    ap.add_argument("--accept-bed", action="store_true", help="allow a bed whose hash differs from the config")
    ap.add_argument("--python", default=str(BASE / "f5-env/bin/python"))
    ap.add_argument("--device", choices=("auto", "cuda", "cpu"), default="auto",
                    help="auto borrows the GPU once for the render; cpu never touches it")
    ap.add_argument("--min-part-words", type=int, default=None,
                    help="join the sentences of a paragraph until a part has this many words "
                         "(default: the story's modes.json entry, then the mode's)")
    ap.add_argument("--chapters", default=None, metavar="A-B",
                    help="build only this chapter range for a listen; the finished story is not replaced")
    ap.add_argument("--in-gpu-window", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    story = args.story
    stressed = STORIES / f"{story}.stressed.txt"
    if not stressed.is_file():
        sys.exit(f"no story: {stressed}")
    registry = M.load_registry(REGISTRY)
    try:
        placed = M.resolve(story, stressed.read_text(encoding="utf-8"), registry,
                           None if args.mode == "auto" else args.mode)
        if args.accept_bed:
            mode = cfg["modes"][placed["mode"]]
            bed = MUSIC / mode["bed"]
            if not bed.is_file():
                sys.exit(f"missing bed {bed}")
        else:
            bed = M.bed_for(placed["mode"], cfg["modes"][placed["mode"]], MUSIC)
    except M.ModeError as err:
        sys.exit(f"MODE {err}")

    entry = registry.get(story, {})
    form = entry.get("form", "prose")
    if form not in ("prose", "verse"):
        sys.exit(f"{story}: form must be prose or verse, not {form!r}")
    min_part_words = args.min_part_words
    if min_part_words is None:
        min_part_words = int(entry.get("min_part_words", cfg["modes"][placed["mode"]].get("min_part_words", 0)))
    print(f"mode {placed['mode']} ({placed['source']}): {placed['why']}")
    print(f"cues {placed['cues']} | bed {bed.name} | form {form} | min_part_words {min_part_words}")
    values_gate(story, stressed.read_text(encoding="utf-8"), registry, "before critique")

    if not args.skip_critique:
        result = run([sys.executable, str(HERE / "story_critique_loop.py"), story, "--mode", placed["mode"],
                      "--rounds", str(args.rounds)] + (["--dry-run"] if args.dry_run else []))
        if result.returncode:
            sys.exit("critique loop failed")
        if args.dry_run:
            return
        try:  # the edits must not have turned the story into another mode
            again = M.resolve(story, stressed.read_text(encoding="utf-8"), M.load_registry(REGISTRY),
                              None if args.mode == "auto" else args.mode)
        except M.ModeError as err:
            sys.exit(f"MODE after critique: {err}")
        if again["mode"] != placed["mode"]:
            sys.exit(f"critique changed the mode from {placed['mode']} to {again['mode']}")
        values_gate(story, stressed.read_text(encoding="utf-8"), M.load_registry(REGISTRY), "after critique")

    if args.device != "cpu" and not args.in_gpu_window:
        # One window for the whole render. gemma stops once, synthesis and every transcription round
        # run inside it, and the EXIT trap in gpu-run.sh starts gemma again on any exit. The critique
        # above already ran, so the re-exec skips it.
        command = [str(HERE / "gpu-run.sh"), "--exec", sys.executable, str(Path(__file__).resolve()),
                   *sys.argv[1:], "--in-gpu-window", "--skip-critique"]
        raise SystemExit(run(command).returncode)

    work = BASE / "books-ru" / story
    work.mkdir(parents=True, exist_ok=True)
    text = stressed.read_text(encoding="utf-8")
    chapters = F5.split_chapters(text)
    chaptered = not (len(chapters) == 1 and chapters[0]["text"] == text)
    wanted = chapter_range(args.chapters, len(chapters))
    if wanted is not None and not chaptered:
        sys.exit("--chapters needs a story with '# ' headings")

    final = BASE / "books-ru" / f"{story}.m4a"
    staged = work / f"{story}.next.m4a"
    if wanted is not None:
        final = BASE / "books-ru" / f"{story}.chapters-{args.chapters}.m4a"
        staged = work / f"{story}.chapters-{args.chapters}.next.m4a"
    baseline = BASE / "books-ru" / f"{story}.quality.json"
    seeds = work / "quality-selected.seeds.json"
    started = time.monotonic()

    if chaptered:
        parts_source = render_chapters(args, cfg, placed, chapters, work, staged, bed, form,
                                       min_part_words, wanted)
    else:
        parts_source = stressed
        command = loop_command(args, stressed, staged, work, placed["mode"],
                               cfg["modes"][placed["mode"]]["part_edge_s"], form, min_part_words, bed)
        if baseline.is_file():
            command += ["--baseline", str(baseline)]
            if args.assume_baseline_pass:
                command.append("--assume-baseline-pass")
        if run(command).returncode not in (0, 2):
            sys.exit("render failed")
    quality_path = staged.with_suffix(".quality.json")
    quality = json.loads(quality_path.read_text(encoding="utf-8"))
    unresolved = quality["unresolved_parts"]
    print(f"ASR: {len(quality['parts']) - len(unresolved)}/{len(quality['parts'])} parts pass, "
          f"{quality['inherited_parts']} reused from the baseline")

    seams_path = work / "seams.next.json"
    gate = cfg["modes"][placed["mode"]]["seam"]
    seam = run([sys.executable, str(HERE / "measure_seams.py"), str(work), str(parts_source),
                "--mode", placed["mode"], "--seeds", str(seeds), "--out", str(seams_path),
                "--cap", str(cfg["modes"][placed["mode"]]["part_edge_s"]),
                "--min-part-words", str(min_part_words), "--form", form,
                "--max-p90", str(gate["max_p90_s"]), "--max-gap", str(gate["max_gap_s"])])
    failures = []
    max_unresolved = unresolved_limit(len(quality["parts"]), args.max_unresolved)
    if len(unresolved) > max_unresolved:
        failures.append(f"{len(unresolved)} unresolved parts (limit {max_unresolved})")
    if seam.returncode:
        failures.append("seam spread over the gate")

    pinned_ffmpeg = Path.home() / "miniforge3/envs/bedtime/bin/ffmpeg"
    ffmpeg = str(pinned_ffmpeg) if pinned_ffmpeg.is_file() else (shutil.which("ffmpeg") or str(pinned_ffmpeg))
    levels = measure_loudnorm(ffmpeg, staged,
                              cfg["output"]["loudnorm"]["i"], cfg["output"]["loudnorm"]["tp"],
                              cfg["output"]["loudnorm"]["lra"])
    lufs, peak = float(levels["input_i"]), float(levels["input_tp"])
    if abs(lufs + 18) > LUFS_TOLERANCE:
        failures.append(f"loudness {lufs} LUFS")
    if peak > PEAK_CEILING:
        failures.append(f"peak {peak} dBTP")

    report = {
        "story": story,
        "mode": placed["mode"],
        "why": placed["why"],
        "mode_source": placed["source"],
        "cues": placed["cues"],
        "bed": str(bed),
        "bed_sha256": M.sha256(bed),
        "edge_s": cfg["modes"][placed["mode"]]["part_edge_s"],
        "form": form,
        "min_part_words": min_part_words,
        "device": quality.get("asr_device"),
        "chapters": quality.get("chapters"),
        "lufs": lufs,
        "true_peak": peak,
        "unresolved_parts": unresolved,
        "seams": json.loads(seams_path.read_text(encoding="utf-8")) if seams_path.is_file() else None,
        "quality": str(quality_path),
        "staged": str(staged),
        "wall_s": round(time.monotonic() - started, 1),
        "failures": failures,
    }
    report_name = f"{story}.build.json" if wanted is None else f"{story}.chapters-{args.chapters}.build.json"
    (work / report_name).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if wanted is not None:
        shutil.move(staged, final)
        shutil.move(quality_path, final.with_suffix(".quality.json"))
        shutil.move(seams_path, work / f"seams.chapters-{args.chapters}.json")
        print(f"BUILD SUBSET | {final} | chapters {args.chapters} of {len(chapters)} | "
              f"{lufs} LUFS {peak} dBTP | {final.name} does not replace {story}.m4a")
        if failures:
            print("SUBSET NOTES | " + "; ".join(failures))
        return
    if failures:
        print("BUILD FAIL | " + "; ".join(failures))
        print(f"kept {final.name}, staged file at {staged}")
        raise SystemExit(1)

    shutil.move(staged, final)
    shutil.move(quality_path, BASE / "books-ru" / f"{story}.quality.json")
    shutil.move(seams_path, work / "seams.json")
    report["staged"] = str(final)
    report["output_sha256"] = M.sha256(final)
    (work / f"{story}.build.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"BUILD PASS | {final.name} | mode {placed['mode']} | {lufs} LUFS {peak} dBTP | "
          f"seam p90 {report['seams']['gap_p90_s']} s")


if __name__ == "__main__":
    main()
