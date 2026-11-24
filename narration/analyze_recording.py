#!/usr/bin/env python3
"""Measure a voice recording before it becomes a TTS reference.

usage: analyze_recording.py RECORDING [--window S E] [--json]

Prints the level, the noise floor, the pauses, the speech runs and the speech-to-noise gap per band.
Use it to judge a new recording and to choose the clip window for prepare_reference.py.
Reference points from 18 Oct 2026: the rejected recording had a gap of about 12 dB between speech and
pauses. The accepted one has 24.6 dB raw and 30.5 dB after the 70 Hz high-pass.

  uv run --no-project --python 3.11 --with numpy --with scipy python narration/analyze_recording.py REC.wav
"""
import argparse
import json
from pathlib import Path

import numpy as np

import audio_tools as A

BANDS = [(0, 60), (60, 130), (130, 300), (300, 1000), (1000, 2000), (2000, 4000), (4000, 6000), (6000, 8000), (8000, 12000)]


def band_power(sig, sr, nfft=1024):
    n = (len(sig) // nfft) * nfft
    frames = sig[:n].reshape(-1, nfft) * np.hanning(nfft)
    p = (np.abs(np.fft.rfft(frames, axis=1)) ** 2).mean(axis=0) / (np.hanning(nfft) ** 2).sum()
    return np.fft.rfftfreq(nfft, 1 / sr), p


def main():
    ap = argparse.ArgumentParser(description="Measure a voice recording.")
    ap.add_argument("recording")
    ap.add_argument("--window", type=float, nargs=2, metavar=("S", "E"), help="also report this window, seconds")
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    args = ap.parse_args()

    path = Path(args.recording).expanduser()
    x, sr = A.decode(path)
    fdb, frame, hop = A.frame_levels(x, sr)
    runs, floor = A.quiet_runs(fdb)
    hop_s = hop / sr

    pauses = []
    for a, b in runs:
        seg = x[int(a * hop): int(b * hop + frame)]
        pauses.append({"start_s": round(a * hop_s, 2), "end_s": round((b * hop + frame) / sr, 2),
                       "rms_dbfs": round(A.rms_db(seg), 1)})
    edges = [0.0] + [v for p in pauses for v in (p["start_s"], p["end_s"])] + [len(x) / sr]
    speech_runs = []
    for i in range(0, len(edges), 2):
        s0, s1 = edges[i], edges[i + 1]
        if s1 - s0 > 0.2:
            seg = x[int(s0 * sr): int(s1 * sr)]
            speech_runs.append({"start_s": round(s0, 2), "end_s": round(s1, 2), "rms_dbfs": round(A.rms_db(seg), 1),
                                "peak_dbfs": round(A.db(np.max(np.abs(seg))), 1)})

    # Noise and speech sample sets. Loud frames: within 10 dB of the 90th percentile.
    x_hp = A.hpf(x, sr, 70.0)
    noise = A.noise_samples(x, runs, sr, frame, hop)
    noise_hp = A.noise_samples(x_hp, runs, sr, frame, hop)
    loud_idx = np.where(fdb > np.percentile(fdb, 90) - 10)[0]
    speech = np.concatenate([x[i * hop: i * hop + frame] for i in loud_idx])
    speech_hp = np.concatenate([x_hp[i * hop: i * hop + frame] for i in loud_idx])

    nyquist = sr / 2
    fn, pn = band_power(noise, sr)
    _, ps = band_power(speech, sr)
    bands = []
    for lo, hi in BANDS:
        if lo >= nyquist:
            continue
        sel = (fn >= lo) & (fn < min(hi, nyquist))
        n_db, s_db = 10 * np.log10(pn[sel].sum() + 1e-20), 10 * np.log10(ps[sel].sum() + 1e-20)
        bands.append({"band_hz": f"{lo}-{min(hi, int(nyquist))}", "noise_db": round(float(n_db), 1),
                      "speech_db": round(float(s_db), 1), "gap_db": round(float(s_db - n_db), 1)})
    f2, p2 = band_power(noise, sr, 4096)
    pdb = 10 * np.log10(p2 + 1e-20)
    tones = []
    for i in range(8, len(pdb) - 8):
        if pdb[i] == pdb[i - 6: i + 7].max():
            over = pdb[i] - np.median(pdb[max(0, i - 60): i + 60])
            if over > 8:
                tones.append({"hz": round(float(f2[i]), 1), "db_over_local_median": round(float(over), 1)})
    tones = sorted(tones, key=lambda t: -t["db_over_local_median"])[:5]

    gap_raw = A.rms_db(speech) - A.rms_db(noise)
    gap_hp = A.rms_db(speech_hp) - A.rms_db(noise_hp)
    report = {
        "file": str(path), "sample_rate": sr, "bandwidth_hz": int(nyquist), "duration_s": round(len(x) / sr, 2),
        "peak_dbfs": round(A.db(np.max(np.abs(x))), 2), "clipped_samples": int(np.count_nonzero(np.abs(x) >= 0.999)),
        "dc_offset": float(np.mean(x)), "overall_rms_dbfs": round(A.rms_db(x), 2),
        "frame_rms_percentiles_dbfs": {str(k): round(float(np.percentile(fdb, k)), 1) for k in (1, 5, 10, 25, 50, 75, 90, 99)},
        "noise_floor_p5_dbfs": round(floor, 1),
        "lead_in_s": pauses[0]["end_s"] if pauses and pauses[0]["start_s"] <= 0.02 else 0.0,
        "pause_rms_dbfs_raw": round(A.rms_db(noise), 1), "pause_rms_dbfs_after_hpf70": round(A.rms_db(noise_hp), 1),
        "speech_rms_dbfs": round(A.rms_db(speech), 1),
        "speech_to_pause_gap_db_raw": round(gap_raw, 1), "speech_to_pause_gap_db_after_hpf70": round(gap_hp, 1),
        "bands": bands, "tonal_peaks_in_pauses": tones, "pauses": pauses, "speech_runs": speech_runs,
    }
    if args.window:
        s0, s1 = args.window
        seg = x[int(s0 * sr): int(s1 * sr)]
        report["window"] = {"start_s": s0, "end_s": s1, "rms_dbfs": round(A.rms_db(seg), 1),
                            "peak_dbfs": round(A.db(np.max(np.abs(seg))), 1)}
    notes = []
    if sr < 24000:
        notes.append(f"sample rate {sr} Hz: nothing above {int(nyquist)} Hz. A voice cloned from it has no air above that")
    if report["clipped_samples"]:
        notes.append(f"{report['clipped_samples']} clipped samples")
    if report["lead_in_s"] < 3:
        notes.append(f"lead-in {report['lead_in_s']} s: the recording guide asks for 10 s of room sound")
    if gap_hp < 20:
        notes.append(f"gap {gap_hp:.1f} dB after the high-pass: expect audible noise in the clone")
    report["notes"] = notes

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    print(f"{path.name}: {report['duration_s']} s, {sr} Hz mono, bandwidth {report['bandwidth_hz']} Hz")
    print(f"peak {report['peak_dbfs']} dBFS, clipped {report['clipped_samples']}, overall RMS {report['overall_rms_dbfs']} dBFS, "
          f"lead-in {report['lead_in_s']} s")
    print("frame RMS percentiles (dBFS):", report["frame_rms_percentiles_dbfs"])
    print(f"noise floor p5 {report['noise_floor_p5_dbfs']} dBFS | pauses {report['pause_rms_dbfs_raw']} dBFS raw, "
          f"{report['pause_rms_dbfs_after_hpf70']} dBFS after the 70 Hz high-pass | speech {report['speech_rms_dbfs']} dBFS")
    print(f"speech-to-pause gap: {report['speech_to_pause_gap_db_raw']} dB raw, {report['speech_to_pause_gap_db_after_hpf70']} dB after the high-pass")
    print("band (Hz)        noise dB  speech dB  gap dB")
    for b in bands:
        print(f"{b['band_hz']:>12s}   {b['noise_db']:8.1f}  {b['speech_db']:9.1f}  {b['gap_db']:6.1f}")
    if tones:
        print("tonal peaks in the pauses:", tones)
    print(f"pauses >= 0.3 s: {len(pauses)}   speech runs: {len(speech_runs)}")
    for r in speech_runs:
        print(f"  speech {r['start_s']:6.2f}-{r['end_s']:6.2f} s  RMS {r['rms_dbfs']:6.1f}  peak {r['peak_dbfs']:6.1f}")
    if args.window:
        print("window:", report["window"])
    for n in notes:
        print("note:", n)


if __name__ == "__main__":
    main()
