#!/usr/bin/env python3
"""Measure the silence at every part join and gate on its spread.

The model puts 0.4 to 1.2 s of silence at the start of each part. Without a trim, that silence adds
to the planned pause, so the real gap is about twice the planned one and varies by half a second.
This reports the real gap and refuses a spread above the gate.

usage: measure_seams.py CHUNK_DIR PARTS [--out JSON] [--max-p90 1.5] [--max-gap 2.4] [--seeds FILE]
       [--silence-db -45] [--frame 0.02] [--cap 3.0]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf


def silent_run(path: Path, threshold: float, frame_s: float, from_end: bool, cap: float) -> float:
    """Length of the silent run at one end of the file, capped."""
    audio, rate = sf.read(path, dtype="float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    size = max(1, int(frame_s * rate))
    frames = len(audio) // size
    if not frames:
        return 0.0
    level = np.max(np.abs(audio[: frames * size]).reshape(frames, size), axis=1)
    silent = level < 10 ** (threshold / 20)
    if from_end:
        silent = silent[::-1]
    run = 0
    for value in silent:
        if not value:
            break
        run += 1
    return min(run * frame_s, cap)


def main() -> None:
    ap = argparse.ArgumentParser(description="Measure part join silence.")
    ap.add_argument("chunks")
    ap.add_argument("parts", help="stress .txt or parts .json, for the planned pauses")
    ap.add_argument("--out", default=None)
    ap.add_argument("--seeds", default=None)
    ap.add_argument("--silence-db", type=float, default=-45.0)
    ap.add_argument("--frame", type=float, default=0.02)
    ap.add_argument("--cap", type=float, default=3.0)
    ap.add_argument("--max-p90", type=float, default=1.5)
    ap.add_argument("--max-gap", type=float, default=2.4)
    ap.add_argument("--mode", choices=("nighttime", "morning"), default="nighttime")
    ap.add_argument("--config", default=str(Path(__file__).resolve().parent / "config/russian-standard.json"))
    ap.add_argument("--min-part-words", type=int, default=None, help="the grouping the render used")
    ap.add_argument("--form", choices=("prose", "verse"), default="prose")
    args = ap.parse_args()

    import f5_russian as F5

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    mode = cfg["modes"][args.mode]
    min_part_words = args.min_part_words if args.min_part_words is not None else int(mode.get("min_part_words", 0))
    parts = F5.load_parts(Path(args.parts), mode["pause_line_s"], mode["pause_paragraph_s"], min_part_words, args.form)
    directory = Path(args.chunks)
    chunks: dict[int, list[Path]] = {}
    for path in directory.glob("[0-9][0-9][0-9][0-9]-*.wav"):
        chunks.setdefault(int(path.name[:4]), []).append(path)
    seeds = json.loads(Path(args.seeds).read_text(encoding="utf-8")) if args.seeds else [None] * len(parts)

    def chosen(index: int) -> Path | None:
        found = chunks.get(index)
        if not found:
            return None
        return next((p for p in found if str(seeds[index]) in p.name), found[0])

    gaps, leads, trails = [], [], []
    for index in range(len(parts) - 1):
        first, second = chosen(index), chosen(index + 1)
        if not first or not second:
            continue
        lead = silent_run(second, args.silence_db, args.frame, False, args.cap)
        trail = silent_run(first, args.silence_db, args.frame, True, args.cap)
        leads.append(lead)
        trails.append(trail)
        gaps.append(trail + float(parts[index]["pause"]) + lead)
    if not gaps:
        sys.exit(f"no part joins measured in {directory}")

    gaps, leads, trails = np.array(gaps), np.array(leads), np.array(trails)
    result = {
        "chunks": str(directory.resolve()),
        "mode": args.mode,
        "joins": len(gaps),
        "planned_pause_s": round(sum(float(p["pause"]) for p in parts[:-1]) / len(gaps), 3),
        "lead_median_s": round(float(np.median(leads)), 3),
        "trail_median_s": round(float(np.median(trails)), 3),
        "edge_silence_median_s": round(float(np.median(leads + trails)), 3),
        "gap_median_s": round(float(np.median(gaps)), 3),
        "gap_p90_s": round(float(np.percentile(gaps, 90)), 3),
        "gap_max_s": round(float(gaps.max()), 3),
        "gap_stdev_s": round(float(gaps.std()), 3),
        "max_p90_s": args.max_p90,
        "max_gap_s": args.max_gap,
    }
    result["passed"] = result["gap_p90_s"] <= args.max_p90 and result["gap_max_s"] <= args.max_gap
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        f"SEAM {'PASS' if result['passed'] else 'FAIL'} | {result['joins']} joins | gap median "
        f"{result['gap_median_s']} s, p90 {result['gap_p90_s']} s, max {result['gap_max_s']} s "
        f"(gate p90 {args.max_p90}, max {args.max_gap})"
    )
    if not result["passed"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()