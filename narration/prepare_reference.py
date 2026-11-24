#!/usr/bin/env python3
"""Build the Russian standard F5 reference clip from the original recording.

usage: prepare_reference.py RECORDING [--config config/russian-standard.json] [--out voice/reference-ru-standard.wav]
                            [--start S --end E] [--no-denoise] [--verify]

Steps: a 70 Hz high-pass on the whole recording, a Wiener denoise from the pause noise profile,
the clip window, one gain (RMS -20 dBFS, peak at most -1.5 dBFS), 24 kHz, 16-bit mono WAV.
--verify compares the SHA-256 of the result with the manifest and exits 1 on a mismatch.
--no-denoise builds the "natural" variant (high-pass only) for comparison.

The exact hash needs numpy 2.2.5 and scipy 1.16.3. Another version pair can move a few samples
by one step, so the hash differs.

  uv run --no-project --python 3.11 --with numpy==2.2.5 --with scipy==1.16.3 python narration/prepare_reference.py REC.wav --verify
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

import audio_tools as A

HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description="Build the Russian standard F5 reference clip.")
    ap.add_argument("recording")
    ap.add_argument("--config", default=str(HERE / "config/russian-standard.json"))
    ap.add_argument("--out", default=None, help="default: voice/<reference.wav_name> next to this script")
    ap.add_argument("--start", type=float, default=None, help="window start, seconds (default: manifest)")
    ap.add_argument("--end", type=float, default=None, help="window end, seconds (default: manifest)")
    ap.add_argument("--no-denoise", action="store_true", help="high-pass only")
    ap.add_argument("--verify", action="store_true", help="exit 1 if the result hash differs from the manifest")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    ref = cfg["reference"]
    rec = Path(args.recording).expanduser()
    if not rec.exists():
        sys.exit(f"no such file: {rec}")
    out = Path(args.out).expanduser() if args.out else HERE / "voice" / ref["wav_name"]
    out.parent.mkdir(parents=True, exist_ok=True)

    expected = ref["source_recording"].get("sha256") or ""
    got = sha256(rec)
    if expected and got != expected:
        print("warning: this recording is not the one in the manifest; the result will not match its hash")
    elif not expected:
        print(f"recording sha256: {got}")
        print("paste that value into reference.source_recording.sha256")
    x, sr = A.decode(rec)
    expected_sr = ref["source_recording"].get("sample_rate") or 0
    if expected_sr and sr != expected_sr:
        print(f"warning: sample rate {sr} Hz, the manifest recording has {expected_sr} Hz")

    fdb, frame, hop = A.frame_levels(x, sr)
    runs, _ = A.quiet_runs(fdb)
    x_hp = A.hpf(x, sr, ref["hpf"]["hz"], ref["hpf"]["order"])
    if args.no_denoise:
        x_clean, denoise = x_hp, "none"
    else:
        d = ref["denoise"]
        noise = A.noise_samples(x_hp, runs, sr, frame, hop)
        x_clean = A.wiener_dd(x_hp, sr, noise, d["floor_db"], d["alpha"], d["nfft"], d["noverlap"])
        denoise = f"wiener-dd floor {d['floor_db']} dB"
    start = args.start if args.start is not None else ref["window_s"][0]
    end = args.end if args.end is not None else ref["window_s"][1]
    if end <= start:
        sys.exit("set --start and --end, or set reference.window_s to a real window")
    seg, gain_db = A.clip_and_level(x_clean, sr, start, end, ref["level"]["target_rms_dbfs"], ref["level"]["peak_cap_dbfs"])
    A.write_wav16(out, seg, sr, ref["output_sample_rate"])

    cf, _, _ = A.frame_levels(seg, sr)
    low = np.percentile(cf, 10)
    speech = float(10 * np.log10(np.mean(10 ** (cf[cf > low + 14] / 10))))
    pause = float(10 * np.log10(np.mean(10 ** (cf[cf < low + 4] / 10))))
    digest = sha256(out)
    result = {
        "out": str(out), "window_s": [start, end], "seconds": round(len(seg) / sr, 3), "denoise": denoise,
        "gain_db": round(gain_db, 2), "rms_dbfs": round(A.rms_db(seg), 2), "peak_dbfs": round(A.db(np.max(np.abs(seg))), 2),
        "speech_to_pause_db": round(speech - pause, 1), "sha256": digest,
    }
    print(json.dumps(result, indent=2))
    if args.verify:
        expected_wav = ref.get("wav_sha256") or ""
        if not expected_wav:
            print(f"wav_sha256: {digest}")
            print("paste that value into reference.wav_sha256")
            sys.exit(0)
        ok = digest == expected_wav
        print("VERIFY", "OK: identical to the standard reference" if ok else f"MISMATCH: manifest has {expected_wav}")
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
