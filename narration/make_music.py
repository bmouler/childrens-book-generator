#!/usr/bin/env python3
"""Generate the ambient music beds for the narration: one to fall asleep to, one to wake up to.

usage: make_music.py {night,morning} OUT.wav [--seconds 600] [--seed N] [--rate 32000]

numpy and scipy synthesize every note from sine partials. There is no sample, no model and no network.
The same seed gives the same file, and the file carries no licence. Pass the result to --music of
f5_russian.py or russian_quality_loop.py. Make a bed longer than the story, because the mixer repeats a
shorter file with a hard cut at the seam.

night    D major. Four chords of 24 s cross-fade into one another. Soft bell notes fall at random. Long
         reverb. No beat and no sudden sound. Meant for the nighttime mode.
morning  G major, 78 BPM. A soft plucked arpeggio and a bass note play over a warm pad. Short reverb.
         The level swells over the first 2.5 minutes. Meant for the morning mode.

Only a listener can judge music. To change the sound, edit the chords, the levels and the reverb below.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

import audio_tools as A

RATE = 32000
SEED = 20261019
FADE_IN_S = 1.5
FADE_OUT_S = 4.0
PEAK = 0.7  # -3 dBFS

# Night. D major add9, B minor 9, G major 7, A sus2 add6. MIDI note numbers. The lowest note is B1 (62 Hz).
NIGHT_CHORDS = (
    (38, 45, 50, 54, 57, 64),
    (35, 42, 47, 50, 57, 61),
    (43, 50, 54, 59, 62, 66),
    (45, 52, 57, 59, 64, 66),
)
NIGHT_BELLS = (62, 64, 66, 69, 71, 74, 76, 78, 81, 83)  # D major pentatonic, D4 to B5
NIGHT_CHORD_S = 24.0
NIGHT_CROSS_S = 8.0

# Morning. Each chord gets pad notes, two bass notes and four arpeggio tones.
MORNING_CHORDS = {
    "G": {"pad": (43, 50, 55, 59, 62), "bass": (43, 50), "arp": (67, 71, 74, 79)},
    "D/F#": {"pad": (42, 50, 57, 62, 66), "bass": (42, 50), "arp": (66, 69, 74, 78)},
    "Em7": {"pad": (40, 47, 52, 55, 62), "bass": (40, 47), "arp": (64, 67, 71, 74)},
    "Cmaj7": {"pad": (36, 43, 48, 52, 59), "bass": (36, 43), "arp": (64, 67, 71, 76)},
    "Bm7": {"pad": (35, 42, 47, 50, 57, 62), "bass": (47, 54), "arp": (66, 71, 74, 78)},
    "D6/9": {"pad": (38, 45, 50, 54, 59, 64), "bass": (38, 45), "arp": (66, 69, 74, 81)},
}
MORNING_PROGRESSION = ("G", "D/F#", "Em7", "Cmaj7", "G", "Bm7", "Cmaj7", "D6/9")
MORNING_PATTERNS = ((0, 1, 2, 3, 2, 1, 2, 1), (0, 2, 1, 3, 2, 3, 1, 2), (0, 1, 2, 1, 3, 2, 1, 2))
MORNING_BPM = 78.0
MORNING_SWELL_S = 150.0

# A struck tone is a list of (frequency ratio, weight, decay relative to the fundamental).
BELL = ((1.0, 1.0, 1.0), (2.0, 0.30, 0.5), (3.0, 0.08, 0.3), (4.2, 0.03, 0.15))
PLUCK = ((1.0, 1.0, 1.0), (2.0, 0.34, 0.5), (5.4, 0.16, 0.15))
BASS = ((1.0, 1.0, 1.0), (2.0, 0.25, 0.5))


def hz(midi: float) -> float:
    return 440.0 * 2.0 ** ((midi - 69.0) / 12.0)


def ramp(n: int) -> np.ndarray:
    """A raised-cosine rise from 0 to 1 over n samples."""
    return 0.5 - 0.5 * np.cos(np.pi * np.arange(n) / max(1, n - 1))


def place(buf: np.ndarray, start_s: float, sig: np.ndarray, rate: int) -> None:
    """Add sig to buf at start_s. The part before the start or after the end of buf is dropped."""
    i = int(round(start_s * rate))
    skip = max(0, -i)
    end = min(len(sig), len(buf) - i)
    if end > skip:
        buf[i + skip:i + end] += sig[skip:end]


def pad(freq: float, dur_s: float, rate: int, rng: np.random.Generator, attack_s: float, release_s: float,
        amp: float) -> np.ndarray:
    """A warm sustained tone: three detuned voices with four partials, a slow rise and fall, a slow tremolo."""
    partials = (1.0, 0.42, 0.2, 0.09)
    cents = (-3.5, 0.0, 3.5)
    n = int(round((dur_s + release_s) * rate))
    t = np.arange(n) / rate
    sig = np.zeros(n)
    for c in cents:
        f = freq * 2.0 ** (c / 1200.0)
        for k, w in enumerate(partials, start=1):
            if f * k < 0.45 * rate:
                sig += w * np.sin(2.0 * np.pi * f * k * t + rng.uniform(0.0, 2.0 * np.pi))
    env = np.ones(n)
    na, nr = min(n, int(attack_s * rate)), min(n, int(release_s * rate))
    env[:na] = ramp(na)
    env[n - nr:] *= ramp(nr)[::-1]
    trem = 1.0 + 0.07 * np.sin(2.0 * np.pi * rng.uniform(0.05, 0.13) * t + rng.uniform(0.0, 2.0 * np.pi))
    return amp / len(cents) * sig * env * trem


def struck(freq: float, rate: int, rng: np.random.Generator, t60_s: float, partials, attack_s: float = 0.003,
           inharmonic: float = 0.0006) -> np.ndarray:
    """A bell, a pluck or a bass note: partials that die away exponentially. The fundamental falls 60 dB in t60_s."""
    n = int(rate * t60_s)
    t = np.arange(n) / rate
    sig = np.zeros(n)
    for ratio, weight, rel in partials:
        f = freq * ratio * (1.0 + inharmonic * ratio * ratio)
        if f < 0.45 * rate:
            tau = t60_s * rel / 6.9078
            sig += weight * np.sin(2.0 * np.pi * f * t + rng.uniform(0.0, 2.0 * np.pi)) * np.exp(-t / tau)
    na = max(1, int(attack_s * rate))
    sig[:na] *= ramp(na)
    return sig


def tilt(midi: int) -> float:
    """Low notes play softer, so that the bass does not swamp the bed."""
    return float(np.clip((midi - 30) / 30.0, 0.25, 1.0))


def reverb_ir(rate: int, rt60_s: float, rng: np.random.Generator, predelay_s: float = 0.02,
              bright_ratio: float = 0.5) -> np.ndarray:
    """A synthetic room: decaying noise, where the highs die away faster than the lows. Unit energy."""
    import scipy.signal as sps
    n = int(rate * rt60_s * 1.15)
    t = np.arange(n) / rate
    noise = rng.standard_normal(n)
    low = sps.sosfilt(sps.butter(2, 2200, "low", fs=rate, output="sos"), noise)
    high = noise - low
    ir = low * 10.0 ** (-3.0 * t / rt60_s) + high * 10.0 ** (-3.0 * t / (rt60_s * bright_ratio))
    ir[: int(predelay_s * rate)] = 0.0
    ir = sps.sosfilt(sps.butter(2, 90, "high", fs=rate, output="sos"), ir)
    return ir / np.sqrt(np.sum(ir ** 2))


def wash(layer: np.ndarray, ir: np.ndarray, wet: float) -> np.ndarray:
    import scipy.signal as sps
    return (1.0 - wet) * layer + wet * sps.oaconvolve(layer, ir, mode="full")[: len(layer)].astype(np.float32)


def compose_night(seconds: float, rate: int, rng: np.random.Generator) -> np.ndarray:
    n = int(round((seconds + 12.0) * rate))
    pads, bells = np.zeros(n, dtype=np.float32), np.zeros(n, dtype=np.float32)
    for c in range(int(math.ceil(seconds / NIGHT_CHORD_S)) + 1):
        for midi in NIGHT_CHORDS[c % len(NIGHT_CHORDS)]:
            start = max(0.0, c * NIGHT_CHORD_S - NIGHT_CROSS_S / 2) + (float(rng.uniform(0.0, 1.5)) if c else 0.0)
            place(pads, start, pad(hz(midi), NIGHT_CHORD_S, rate, rng, NIGHT_CROSS_S, NIGHT_CROSS_S, 0.5 * tilt(midi)), rate)
    t, idx = 5.0, int(rng.integers(3, 7))
    while t < seconds + 4.0:
        idx = int(np.clip(idx + rng.choice((-2, -1, 1, 2), p=(0.2, 0.3, 0.3, 0.2)), 0, len(NIGHT_BELLS) - 1))
        amp = float(rng.uniform(0.25, 0.55))
        place(bells, t, amp * struck(hz(NIGHT_BELLS[idx]), rate, rng, 5.5, BELL), rate)
        if idx >= 2 and rng.random() < 0.18:  # a soft echo a third lower
            place(bells, t + float(rng.uniform(0.35, 0.6)), 0.6 * amp * struck(hz(NIGHT_BELLS[idx - 2]), rate, rng, 5.5, BELL), rate)
        t += float(np.clip(rng.exponential(5.0), 2.2, 13.0))
    ir = reverb_ir(rate, 6.5, rng)
    return wash(pads, ir, 0.55) + wash(bells, ir, 0.85)


def compose_morning(seconds: float, rate: int, rng: np.random.Generator) -> np.ndarray:
    beat = 60.0 / MORNING_BPM
    bar, eighth = 4 * beat, beat / 2
    n = int(round((seconds + 6.0) * rate))
    pads, plucks, basses = (np.zeros(n, dtype=np.float32) for _ in range(3))
    for b in range(int(math.ceil(seconds / bar)) + 1):
        chord = MORNING_CHORDS[MORNING_PROGRESSION[b % len(MORNING_PROGRESSION)]]
        t0 = b * bar
        for midi in chord["pad"]:
            place(pads, max(0.0, t0 - 0.5), pad(hz(midi), bar, rate, rng, 1.0, 1.4, 0.3 * tilt(midi)), rate)
        root, fifth = chord["bass"]
        place(basses, t0, 0.5 * struck(hz(root), rate, rng, 2.2, BASS, attack_s=0.02), rate)
        place(basses, t0 + 2 * beat, 0.32 * struck(hz(fifth), rate, rng, 1.8, BASS, attack_s=0.02), rate)
        pattern = MORNING_PATTERNS[int(rng.integers(0, len(MORNING_PATTERNS)))]
        for k, tone in enumerate(pattern):
            if k % 2 == 1 and rng.random() < 0.18:  # a rest on some off-beats keeps the line from sounding mechanical
                continue
            accent = 1.0 if k % 4 == 0 else (0.8 if k % 2 == 0 else 0.62)
            amp = accent * float(rng.uniform(0.85, 1.0))
            place(plucks, t0 + k * eighth + float(rng.normal(0.0, 0.006)),
                  amp * struck(hz(chord["arp"][tone]), rate, rng, 1.4, PLUCK), rate)
    ir = reverb_ir(rate, 2.2, rng, bright_ratio=0.6)
    mix = wash(pads, ir, 0.3) + 1.3 * wash(plucks, ir, 0.3) + wash(basses, ir, 0.1)
    s = np.clip(np.arange(n) / rate / MORNING_SWELL_S, 0.0, 1.0)
    return mix * (0.3 + 0.7 * s * s * (3.0 - 2.0 * s)).astype(np.float32)


def shape(sig: np.ndarray, rate: int, seconds: float, high_cut_hz: float) -> np.ndarray:
    """Cut the rumble and the hiss, fade the ends and set the peak to -3 dBFS."""
    import scipy.signal as sps
    sig = sps.sosfilt(sps.butter(2, 35, "high", fs=rate, output="sos"), sig)
    sig = sps.sosfilt(sps.butter(2, min(high_cut_hz, 0.45 * rate), "low", fs=rate, output="sos"), sig)[: int(round(seconds * rate))]
    n_in, n_out = min(len(sig) // 2, int(FADE_IN_S * rate)), min(len(sig) // 2, int(FADE_OUT_S * rate))
    sig[:n_in] *= ramp(n_in)
    sig[len(sig) - n_out:] *= ramp(n_out)[::-1]
    return (sig * (PEAK / float(np.max(np.abs(sig))))).astype(np.float32)


def compose(mode: str, seconds: float, rate: int = RATE, seed: int = SEED) -> np.ndarray:
    """The bed as mono float32 samples in [-0.7, 0.7]. The same arguments always give the same samples."""
    rng = np.random.default_rng(seed)
    if mode == "night":
        return shape(compose_night(seconds, rate, rng), rate, seconds, 6000.0)
    if mode == "morning":
        return shape(compose_morning(seconds, rate, rng), rate, seconds, 9000.0)
    raise ValueError(f"mode must be night or morning, not {mode!r}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate an ambient music bed for the narration.")
    ap.add_argument("mode", choices=("night", "morning"))
    ap.add_argument("out", help="output .wav (16-bit mono)")
    ap.add_argument("--seconds", type=float, default=600.0, help="length of the bed (default 600). Longer than the story.")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--rate", type=int, default=RATE)
    args = ap.parse_args()
    if args.seconds < 10:
        ap.error("--seconds must be at least 10")

    sig = compose(args.mode, args.seconds, args.rate, args.seed)
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    A.write_wav16(out, sig, args.rate, args.rate)
    print(json.dumps({
        "mode": args.mode, "out": str(out), "seconds": round(len(sig) / args.rate, 3), "rate": args.rate,
        "seed": args.seed, "peak_dbfs": round(A.db(np.max(np.abs(sig))), 2), "rms_dbfs": round(A.rms_db(sig), 2),
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
