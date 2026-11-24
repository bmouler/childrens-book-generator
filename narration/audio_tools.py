"""Shared audio helpers for the narration tools. numpy and scipy do the work. ffmpeg decodes.

The numbers here define the Russian standard reference. Change them and the reference changes:
`prepare_reference.py --verify` then reports a hash mismatch.
"""
import os
import shutil
import subprocess
import wave
from math import gcd
from pathlib import Path

import numpy as np

HOME = Path.home()
_BIN_DIRS = ("/opt/homebrew/bin", str(HOME / "miniforge3/envs/bedtime/bin"), "/usr/local/bin", "/usr/bin")


def _bin(name: str) -> str:
    """ffmpeg or ffprobe: environment override, then PATH, then the known install folders."""
    found = os.environ.get(name.upper()) or shutil.which(name)
    if found:
        return found
    for d in _BIN_DIRS:
        if (Path(d) / name).exists():
            return str(Path(d) / name)
    raise FileNotFoundError(f"{name} not found; set {name.upper()}")


def db(v) -> float:
    return float(20 * np.log10(max(float(v), 1e-12)))


def rms_db(x) -> float:
    return db(np.sqrt(np.mean(np.square(np.asarray(x, dtype=np.float64)))))


def decode(path, sr=None, start=0.0, duration=None):
    """Mono float32 samples and their rate. sr=None keeps the file's own rate."""
    path = str(path)
    if sr is None:
        out = subprocess.run([_bin("ffprobe"), "-v", "error", "-select_streams", "a:0", "-show_entries",
                              "stream=sample_rate", "-of", "csv=p=0", path],
                             capture_output=True, text=True, check=True).stdout.strip()
        sr = int(out)
    cmd = [_bin("ffmpeg"), "-nostdin", "-v", "error"]
    if start:
        cmd += ["-ss", str(start)]
    cmd += ["-i", path]
    if duration is not None:
        cmd += ["-t", str(duration)]
    cmd += ["-ac", "1", "-ar", str(sr), "-f", "f32le", "pipe:1"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32), sr


def frame_levels(x, sr, frame_s=0.025, hop_s=0.010):
    """RMS level in dBFS of every 25 ms frame at a 10 ms hop. Returns (levels, frame, hop) in samples."""
    frame, hop = round(sr * frame_s), round(sr * hop_s)
    fr = np.lib.stride_tricks.sliding_window_view(x, frame)[::hop]
    fdb = 20 * np.log10(np.maximum(np.sqrt(np.mean(fr.astype(np.float64) ** 2, axis=1)), 1e-12))
    return fdb, frame, hop


def find_runs(mask, min_len):
    """(start, end) frame ranges where mask is true for at least min_len frames."""
    out, start = [], None
    for i, m in enumerate(mask):
        if m and start is None:
            start = i
        if (not m) and start is not None:
            if i - start >= min_len:
                out.append((start, i))
            start = None
    if start is not None and len(mask) - start >= min_len:
        out.append((start, len(mask)))
    return out


def quiet_runs(fdb, hop_s=0.010, margin_db=8.0, min_s=0.3):
    """Pauses: runs of at least min_s whose 50 ms smoothed level sits within margin_db of the 5th percentile."""
    floor = float(np.percentile(fdb, 5))
    smooth = np.convolve(fdb, np.ones(5) / 5, mode="same")
    return find_runs(smooth < floor + margin_db, round(min_s / hop_s)), floor


def noise_samples(sig, runs, sr, frame, hop):
    """The pause interiors, 60 ms away from the speech edges, joined. The noise profile for the denoiser."""
    parts = [sig[int(a * hop + 0.06 * sr): int(b * hop + frame - 0.06 * sr)]
             for a, b in runs if (b - a) * hop > 0.3 * sr]
    return np.concatenate(parts)


def hpf(sig, sr, f_hz=70.0, order=4):
    import scipy.signal as sps
    sos = sps.butter(order, f_hz, btype="highpass", fs=sr, output="sos")
    return sps.sosfilt(sos, sig).astype(np.float32)


def wiener_dd(sig, sr, noise_sig, g_floor_db=-9.0, alpha=0.95, nfft=512, nover=384):
    """Wiener filter with decision-directed a priori SNR. The noise profile is the mean pause spectrum.
    The gain never drops below g_floor_db, so the room tone stays natural."""
    import scipy.signal as sps
    _, _, X = sps.stft(sig, fs=sr, window="hann", nperseg=nfft, noverlap=nover)
    _, _, N = sps.stft(noise_sig, fs=sr, window="hann", nperseg=nfft, noverlap=nover)
    npsd = np.mean(np.abs(N) ** 2, axis=1)
    npsd = np.convolve(npsd, np.ones(5) / 5, mode="same") + 1e-14
    P = np.abs(X) ** 2
    gmin = 10 ** (g_floor_db / 20)
    G = np.ones_like(P)
    g_prev = np.ones(P.shape[0])
    gam_prev = np.ones(P.shape[0])
    for i in range(P.shape[1]):
        gam = P[:, i] / npsd
        xi = alpha * (g_prev ** 2) * gam_prev + (1 - alpha) * np.maximum(gam - 1.0, 0.0)
        g = np.clip(xi / (1.0 + xi), gmin, 1.0)
        G[:, i] = g
        g_prev = g
        gam_prev = gam
    G = sps.convolve2d(G, np.ones((3, 1)) / 3, mode="same", boundary="symm")  # no isolated bins
    _, y = sps.istft(X * G, fs=sr, window="hann", nperseg=nfft, noverlap=nover)
    y = y[:len(sig)]
    return np.pad(y, (0, len(sig) - len(y))).astype(np.float32)


def clip_and_level(sig, sr, start, end, target_rms_db=-20.0, peak_cap_db=-1.5):
    """Cut [start, end] seconds and apply one gain: RMS to the target, never past the peak cap."""
    seg = sig[int(start * sr):int(end * sr)].astype(np.float64)
    gain_db = min(target_rms_db - rms_db(seg), peak_cap_db - db(np.max(np.abs(seg))))
    return (seg * 10 ** (gain_db / 20)).astype(np.float32), gain_db


def write_wav16(path, sig, sr_in, sr_out=24000):
    """Resample by an exact rational factor and write 16-bit mono PCM."""
    import scipy.signal as sps
    g = gcd(sr_in, sr_out)
    up = sps.resample_poly(sig, sr_out // g, sr_in // g).astype(np.float32) if sr_in != sr_out else sig
    pcm16 = np.clip(np.round(up * 32767.0), -32768, 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr_out)
        w.writeframes(pcm16.tobytes())
    return up
