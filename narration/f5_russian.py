#!/usr/bin/env python3
"""Render Russian narration with F5-TTS from a reference clip you record.

usage: f5_russian.py PARTS --out OUT.m4a [--plan] [--config CFG] [--reference WAV]
                     [--mode nighttime|morning] [--music TRACK] [--seeds FILE] [--speed X | --match-seconds S]
                     [--workers N] [--trim-edges KEEP] [--threads N] [--nice N] [--work DIR]

PARTS is a .json list of {"text", "pause", "seed"} objects (pause and seed are optional) or a .txt
file with one part per line. A blank line in a .txt file ends a paragraph.
Mark word stress with "+" before the stressed vowel: мол+око. F5 guesses the stress of unmarked words.

F5 makes every part this long: (ref_frames / ref_bytes * part_bytes / speed) frames, minus one 10.7 ms
frame that the vocoder drops. So the speed in config/russian-standard.json sets the pace for every text.
--match-seconds picks the speed that gives a chosen total. --plan prints the length of every part and
stops. It loads no model.
--mode changes the default pauses and the optional music treatment. It does not change the voice, model,
reference, generation speed or loudness target. --music loops a supplied track and ducks only that track
under the narration.
--seeds FILE is a JSON list with one seed per part (null keeps the default). russian_quality_loop.py writes
it. The pauses still come from PARTS and --mode, so one set of chosen seeds can be assembled in any mode.

Run it on the render machine in the f5-env virtualenv (see README.md):
  ~/bedtime-audiobooks/f5-env/bin/python ~/bedtime-audiobooks/f5_russian.py PARTS.json --out OUT.m4a
Reruns resume. A part is cached under its text, reference, speed, steps, guidance and seed.
--workers N renders the parts in N parallel processes (every part has its own seed, so the audio is the same
as with one process), then assembles. Each worker uses --threads threads. Measured on 18 Oct 2026: two runs of
8 threads that shared the PC each took 1.3x the time of one run alone, so two workers give about 1.5x the speed.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOME = Path.home()
BASE = HOME / "bedtime-audiobooks"
ENV_BIN = HOME / "miniforge3/envs/bedtime/bin"
SR = 24000
HOP = 256


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_chapters(text: str) -> list[dict]:
    """Split a story into chapters at '# ' heading lines. A heading is never read aloud.

    The title line travels with the first chapter, so it is read once, as it is in a story without
    headings. Body before the first heading is chapter 0. A story with no headings gives one
    chapter whose text is the input unchanged.
    """
    lines = text.splitlines()
    if not any(line.startswith("# ") for line in lines):
        return [{"title": None, "text": text}]
    title = lines[0] if lines else ""
    sections: list[dict] = []
    current: dict = {"title": None, "lines": []}
    for line in lines[1:]:
        if line.startswith("# "):
            sections.append(current)
            current = {"title": line[2:].strip(), "lines": []}
            continue
        current["lines"].append(line)
    sections.append(current)
    chapters = []
    for section in sections:
        body = "\n".join(section["lines"]).strip("\n")
        if not body.strip():
            continue
        if not chapters:
            body = title + "\n\n" + body
        chapters.append({"title": section["title"], "text": body + "\n"})
    return chapters


def load_parts(path: Path, pause_line: float, pause_paragraph: float, min_part_words: int = 0, form: str = "prose"):
    """Turn a text or JSON source into parts. A '# ' line is a heading and is never a part.

    min_part_words joins the sentence lines of one paragraph until the part holds at least that
    many whitespace-separated words. It never crosses a paragraph boundary and never joins a verse
    story. The default 0 keeps one sentence per part.
    """
    if path.suffix.lower() == ".json":
        parts = []
        for item in json.loads(path.read_text(encoding="utf-8")):
            if isinstance(item, str):
                item = {"text": item}
            parts.append({"text": " ".join(item["text"].split()), "pause": float(item.get("pause", pause_line)),
                          "seed": item.get("seed")})
        return parts
    parts = []
    paragraph: list[str] = []

    def flush() -> None:
        nonlocal paragraph
        if not paragraph:
            return
        if min_part_words > 0 and form != "verse":
            group: list[str] = []
            for line in paragraph:
                group.append(line)
                if len(" ".join(group).split()) >= min_part_words:
                    parts.append({"text": " ".join(group), "pause": pause_line, "seed": None})
                    group = []
            if group:
                parts.append({"text": " ".join(group), "pause": pause_line, "seed": None})
        else:
            parts.extend({"text": line, "pause": pause_line, "seed": None} for line in paragraph)
        parts[-1]["pause"] = pause_paragraph
        paragraph = []

    for line in path.read_text(encoding="utf-8").splitlines():
        line = " ".join(line.split())
        if line.startswith("# "):
            flush()
            continue
        if not line:
            flush()
            continue
        paragraph.append(line)
    flush()
    return parts


def apply_seeds(parts, seeds):
    """Give part i the seed seeds[i]. None keeps the default seed. The quality loop writes such a list."""
    if not isinstance(seeds, list) or len(seeds) != len(parts):
        raise ValueError(f"need a JSON list with one seed per part ({len(parts)} parts)")
    for part, seed in zip(parts, seeds):
        if seed is not None:
            part["seed"] = int(seed)


MIN_CUDA_FREE_BYTES = 2 * 1024**3


def resolve_device(requested: str = "auto", fallback: str = "cpu") -> tuple[str, str]:
    """Pick 'cuda' or 'cpu', with the reason. auto takes CUDA when it works and has free VRAM.

    A broken driver or a full GPU must not stop a build, so auto falls back to the CPU.
    """
    if requested in ("cuda", "cpu"):
        return requested, "requested on the command line"
    try:
        import torch
        if not torch.cuda.is_available():
            return fallback, "torch.cuda.is_available() is False"
        free, _total = torch.cuda.mem_get_info()
        if free < MIN_CUDA_FREE_BYTES:
            return fallback, f"only {free / 2**30:.1f} GiB of VRAM is free"
        return "cuda", f"{free / 2**30:.1f} GiB of VRAM free"
    except Exception as err:
        return fallback, f"the CUDA check failed: {err}"


def main():
    ap = argparse.ArgumentParser(description="Render Russian narration with F5-TTS in the standard voice.")
    ap.add_argument("parts")
    ap.add_argument("--out", required=True, help="output .m4a")
    ap.add_argument("--config", default=str(HERE / "config/russian-standard.json"))
    ap.add_argument("--reference", default=None, help="reference WAV (default: voice/<wav_name> in the runtime folder)")
    ap.add_argument("--speed", type=float, default=None, help="override the manifest speed")
    ap.add_argument("--match-seconds", type=float, default=None, help="choose the speed that gives this total speech length")
    ap.add_argument("--threads", type=int, default=None)
    ap.add_argument("--nice", type=int, default=5, help="CPU niceness")
    ap.add_argument("--work", default=None, help="chunk cache folder (default: books-ru/<out name>)")
    ap.add_argument("--mode", choices=("nighttime", "morning"), default="nighttime",
                    help="presentation profile; nighttime keeps the approved pauses")
    ap.add_argument("--music", default=None, help="optional music file; it loops to the narration length")
    ap.add_argument("--music-lufs", type=float, default=None, help="override the mode's music loudness")
    ap.add_argument("--plan", action="store_true", help="print part lengths and the speed, then stop")
    ap.add_argument("--workers", type=int, default=1, help="render the parts in N parallel processes, then assemble")
    ap.add_argument("--shard", default=None, help=argparse.SUPPRESS)  # K/N: one worker of --workers, internal
    ap.add_argument("--trim-edges", type=float, default=None, metavar="KEEP",
                    help="trim the silence at both ends of every part to KEEP seconds (for example 0.15) before the pause is added. "
                         "Off by default: the approved sample keeps the model's own edges.")
    ap.add_argument("--synthesize-only", action="store_true",
                    help="fill the part cache without assembling the output")
    ap.add_argument("--chunk-manifest", default=None,
                    help="write the selected chunk paths as JSON (used by the quality loop)")
    ap.add_argument("--seeds", default=None, help="JSON list with one seed per part (null keeps the default)")
    ap.add_argument("--device", choices=("auto", "cuda", "cpu"), default="auto",
                    help="synthesis device; auto uses CUDA when it is available and has 2 GiB free")
    ap.add_argument("--min-part-words", type=int, default=None,
                    help="join the sentences of a paragraph until a part has this many words (default: the mode's)")
    ap.add_argument("--form", choices=("prose", "verse"), default="prose", help="verse never joins sentence lines")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    gen, ref_cfg, model_cfg, outc = cfg["generation"], cfg["reference"], cfg["model"], cfg["output"]
    if args.mode not in cfg.get("modes", {}):
        sys.exit(f"mode {args.mode!r} is missing from {args.config}")
    mode = cfg["modes"][args.mode]
    if args.music_lufs is not None and not args.music:
        sys.exit("--music-lufs requires --music")
    threads = args.threads or gen["threads"]
    os.environ.update({"HF_HUB_DISABLE_PROGRESS_BARS": "1", "HF_HUB_DISABLE_TELEMETRY": "1", "DO_NOT_TRACK": "1",
                       "WANDB_MODE": "disabled", "TOKENIZERS_PARALLELISM": "false",
                       "OMP_NUM_THREADS": str(threads), "MKL_NUM_THREADS": str(threads)})
    os.environ["PATH"] = f"{ENV_BIN}{os.pathsep}{os.environ.get('PATH', '')}"  # pydub looks for ffmpeg here
    if args.nice:
        os.nice(args.nice)

    src = Path(args.parts).expanduser()
    min_part_words = args.min_part_words if args.min_part_words is not None else int(mode.get("min_part_words", 0))
    parts = load_parts(src, mode["pause_line_s"], mode["pause_paragraph_s"], min_part_words, args.form)
    if not parts:
        sys.exit(f"no text in {src}")
    if args.seeds:
        try:
            apply_seeds(parts, json.loads(Path(args.seeds).expanduser().read_text(encoding="utf-8")))
        except ValueError as err:
            sys.exit(f"{args.seeds}: {err}")
    music = Path(args.music).expanduser().resolve() if args.music else None
    if music and not music.is_file():
        sys.exit(f"no music file: {music}")
    reference = Path(args.reference).expanduser() if args.reference else BASE / "voice" / ref_cfg["wav_name"]
    if not reference.exists():
        sys.exit(f"no reference: {reference}. Build it with prepare_reference.py and copy it there.")
    ref_sha = sha256(reference)
    expected = ref_cfg.get("wav_sha256") or ""
    if not args.reference and not expected:
        sys.exit(f"reference.wav_sha256 is empty. Paste {ref_sha} into config/russian-standard.json.")
    if not args.reference and ref_sha != expected:
        sys.exit(f"{reference} differs from the manifest (sha256 {ref_sha}). Run prepare_reference.py --verify.")

    import numpy as np
    import soundfile as sf
    import torch
    import torchaudio
    from f5_tts.infer.utils_infer import chunk_text, preprocess_ref_audio_text
    torch.set_num_threads(threads)
    torch.set_num_interop_threads(1)
    device, device_reason = resolve_device(args.device, str(gen.get("device", "cpu")))
    print(f"synthesis device: {device} ({device_reason})", flush=True)

    ref_audio, ref_text = preprocess_ref_audio_text(str(reference), ref_cfg["text"], show_info=lambda *a, **k: None)
    info = torchaudio.info(ref_audio)
    ref_secs = info.num_frames / info.sample_rate
    ref_frames = int(info.num_frames * SR / info.sample_rate) // HOP
    ref_bytes = len(ref_text.encode()) + (1 if len(ref_text[-1].encode()) == 1 else 0)  # F5 adds one more space

    raw_total = sum(ref_frames / ref_bytes * len(p["text"].encode()) for p in parts) * HOP / SR
    speed = round(raw_total / args.match_seconds, 3) if args.match_seconds else (args.speed or gen["speed"])
    max_chars = int(len(ref_text.encode()) / ref_secs * (22 - ref_secs) * speed)
    plan, split = [], 0
    for p in parts:
        nbytes = len(p["text"].encode())
        batches = len(chunk_text(p["text"], max_chars=max_chars))
        split += batches > 1
        plan.append((nbytes, (int(ref_frames / ref_bytes * nbytes / speed) - 1) * HOP / SR, batches))
    speech_s = sum(v[1] for v in plan)
    pause_s = sum(p["pause"] for p in parts)
    unmarked = sum("+" not in p["text"] for p in parts)
    print(f"reference {ref_secs:.2f} s processed, {ref_bytes} bytes | speed {speed} | {len(parts)} parts | "
          f"speech {speech_s:.1f} s + pauses {pause_s:.1f} s = {speech_s + pause_s:.1f} s")
    if args.plan:
        for i, (p, (nbytes, secs, batches)) in enumerate(zip(parts, plan)):
            print(f"  {i:3d}  {nbytes:4d} bytes  {secs:6.2f} s  pause {p['pause']:.2f}  batches {batches}  {p['text'][:60]}")
    if split:
        print(f"note: {split} part(s) exceed {max_chars} bytes. F5 splits them and joins with a 0.15 s cross-fade.")
    if unmarked:
        print(f"note: {unmarked} part(s) have no stress marks. F5 guesses the stress there.")
    if args.plan:
        return

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    work = Path(args.work).expanduser() if args.work else BASE / "books-ru" / out.stem
    work.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    shard = tuple(int(v) for v in args.shard.split("/")) if args.shard else None

    if args.workers > 1 and not shard:  # N processes fill the cache, then this one assembles from it
        base = [sys.executable, str(Path(__file__).resolve()), str(src), "--out", str(out), "--config", args.config,
                "--speed", str(speed), "--threads", str(threads), "--nice", "0", "--work", str(work),
                "--device", device, "--min-part-words", str(min_part_words), "--form", args.form]
        if args.reference:
            base += ["--reference", str(reference)]
        if args.seeds:
            base += ["--seeds", str(Path(args.seeds).expanduser())]
        procs = [subprocess.Popen(base + ["--shard", f"{k}/{args.workers}"]) for k in range(args.workers)]
        codes = [pr.wait() for pr in procs]
        if any(codes):
            sys.exit(f"a worker failed (exit codes {codes}). Run the same command again. It resumes from the cached parts.")

    from huggingface_hub import hf_hub_download
    from f5_tts.api import F5TTS

    def fetch(name):
        try:
            return hf_hub_download(model_cfg["checkpoint_repo"], name, revision=model_cfg["revision"], local_files_only=True)
        except Exception:
            return hf_hub_download(model_cfg["checkpoint_repo"], name, revision=model_cfg["revision"])

    held = {}

    def get_model():  # loaded on the first part that needs synthesis
        if "model" not in held:
            t0 = time.monotonic()
            held["model"] = F5TTS(model=model_cfg["f5_config"], ckpt_file=fetch(model_cfg["checkpoint"]),
                                  vocab_file=fetch(model_cfg["vocab"]), device=device)
            print(f"model loaded in {time.monotonic() - t0:.1f} s", flush=True)
        return held["model"]

    def cache_key(text, seed):
        blob = json.dumps([text, ref_sha, ref_cfg["text"], speed, gen["nfe_step"], gen["cfg_strength"], seed,
                           model_cfg["revision"], model_cfg["checkpoint"]], ensure_ascii=False)
        return hashlib.sha1(blob.encode()).hexdigest()[:12]

    def part_files():
        for i, p in enumerate(parts):
            seed = p["seed"] if p["seed"] is not None else gen["seed_base"] + i
            yield i, p, seed, work / f"{i:04d}-{cache_key(p['text'], seed)}.wav"

    elapsed = {}
    for i, p, seed, chunk in part_files():  # synthesis: every part, or this worker's share
        if shard and i % shard[1] != shard[0]:
            continue
        if chunk.exists():
            continue
        t0 = time.monotonic()
        wav, sr, spec = get_model().infer(ref_file=str(reference), ref_text=ref_cfg["text"], gen_text=p["text"],
                                          nfe_step=gen["nfe_step"], cfg_strength=gen["cfg_strength"], speed=speed,
                                          seed=seed, progress=None, show_info=lambda *a, **k: None)
        del spec
        if wav is None or sr != SR or not np.all(np.isfinite(wav)):
            raise RuntimeError(f"invalid synthesis output for part {i}")
        sf.write(chunk, wav, sr, subtype="FLOAT")
        elapsed[i] = round(time.monotonic() - t0, 1)
        print(json.dumps({"index": i, "seconds": round(len(wav) / SR, 3), "seed": seed, "elapsed_s": elapsed[i],
                          **({"shard": args.shard} if shard else {})}), flush=True)
    if shard:
        return
    if args.chunk_manifest:
        chunk_manifest = Path(args.chunk_manifest).expanduser()
        chunk_manifest.parent.mkdir(parents=True, exist_ok=True)
        chunk_manifest.write_text(json.dumps({
            "source": str(src.resolve()),
            "source_sha256": sha256(src),
            "config": cfg["name"],
            "reference_sha256": ref_sha,
            "speed": speed,
            "parts": [
                {
                    "index": i,
                    "text": p["text"],
                    "pause": p["pause"],
                    "seed": seed,
                    "path": str(chunk.resolve()),
                    "bytes": chunk.stat().st_size,
                }
                for i, p, seed, chunk in part_files()
            ],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.synthesize_only:
        print(f"DONE synthesis cache | {len(parts)} parts | {time.monotonic() - started:.0f} s wall")
        return

    def trim_edges(wav, keep):  # the model starts each part with 0.4 to 1.2 s of silence. Keep a little of it.
        frame = round(0.02 * SR)
        n = len(wav) // frame
        level = 20 * np.log10(np.maximum(np.sqrt(np.mean(wav[: n * frame].reshape(n, frame).astype(np.float64) ** 2, axis=1)), 1e-9))
        active = np.where(level > -45.0)[0]
        if len(active) == 0:
            return wav
        a = max(0, int(active[0]) * frame - round(keep * SR))
        b = min(len(wav), (int(active[-1]) + 1) * frame + round(keep * SR))
        out_wav = wav[a:b].copy()
        ramp = min(len(out_wav) // 2, round(0.005 * SR))
        out_wav[:ramp] *= np.linspace(0, 1, ramp, dtype=np.float32)
        out_wav[len(out_wav) - ramp:] *= np.linspace(1, 0, ramp, dtype=np.float32)
        return out_wav

    native = work / "complete-native.wav"
    report_parts = []
    with sf.SoundFile(native, "w", samplerate=SR, channels=1, subtype="FLOAT") as joined:  # streamed to disk
        for i, p, seed, chunk in part_files():
            wav, sr = sf.read(chunk, dtype="float32")
            if len(wav) < 2400 or float(np.max(np.abs(wav))) < 0.001:
                raise RuntimeError(f"empty or silent synthesis output for part {i}")
            raw_seconds = len(wav) / SR
            if args.trim_edges is not None:
                wav = trim_edges(wav, args.trim_edges)
            joined.write(wav)
            joined.write(np.zeros(round(p["pause"] * SR), dtype=np.float32))
            report_parts.append({"index": i, "seconds": round(raw_seconds, 3), "kept_seconds": round(len(wav) / SR, 3),
                                 "pause": p["pause"], "seed": seed, "elapsed_s": elapsed.get(i), "text": p["text"]})

    ffmpeg = str(ENV_BIN / "ffmpeg")
    ln = outc["loudnorm"]
    from background_music import loudnorm_filter, measure_loudnorm, mix_background
    native_levels = measure_loudnorm(ffmpeg, native, ln["i"], ln["tp"], ln["lra"])
    native_norm = loudnorm_filter(ln["i"], ln["tp"], ln["lra"], native_levels)
    encode_source = native
    output_levels = native_levels
    music_report = None
    if music:
        music_profile = dict(mode["music"])
        if args.music_lufs is not None:
            music_profile["integrated_lufs"] = args.music_lufs
        mixed = work / "complete-mixed.wav"
        duration_s = sf.info(native).frames / SR
        music_report = mix_background(
            ffmpeg, native, music, mixed, duration_s, native_norm, music_profile, outc["sample_rate"]
        )
        encode_source = mixed
        output_levels = measure_loudnorm(ffmpeg, mixed, ln["i"], ln["tp"], ln["lra"])
    output_norm = loudnorm_filter(ln["i"], ln["tp"], ln["lra"], output_levels)
    subprocess.run([ffmpeg, "-nostdin", "-v", "error", "-y", "-i", str(encode_source), "-af", output_norm,
                    "-ar", str(outc["sample_rate"]), "-ac", "1", "-c:a", "aac", "-b:a", outc["aac_bitrate"],
                    "-movflags", "+faststart", "-metadata", f"title={out.stem}", str(out)], check=True)
    wall = time.monotonic() - started
    trim_note = (
        f"part edges trimmed to {args.trim_edges} s; " if args.trim_edges is not None else ""
    )
    if music_report:
        processing = (
            trim_note
            + f"{args.mode} music loop normalized to {music_report['integrated_lufs']} LUFS and sidechain-ducked "
            + "by the narration; the narration received linear loudness gain only, with no denoising or time stretching"
        )
    elif args.trim_edges is None:
        processing = "loudness normalization only, no denoising and no time stretching"
    else:
        processing = f"silence at both ends of every part trimmed to {args.trim_edges} s, then loudness normalization"
    out.with_suffix(".json").write_text(json.dumps({
        "config": cfg["name"], "mode": args.mode, "reference_sha256": ref_sha, "speed": speed,
        "nfe_step": gen["nfe_step"], "cfg_strength": gen["cfg_strength"],
        "speech_s": round(sum(r["seconds"] for r in report_parts), 3), "wall_s": round(wall, 1),
        "native_levels": native_levels, "output_source_levels": output_levels, "music": music_report,
        "parts": report_parts, "trim_edges_s": args.trim_edges, "post_processing": processing,
    }, ensure_ascii=False, indent=2))
    print(f"DONE {out} | {sum(r['seconds'] for r in report_parts) / 60:.1f} min of speech | {wall:.0f} s wall")


if __name__ == "__main__":
    main()
