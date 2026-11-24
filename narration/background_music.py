#!/usr/bin/env python3
"""Mix a narration file with a looped music bed.

The caller supplies a normalized narration filter and a mode-specific music profile.
Only the music is compressed. The narration remains the sidechain key and is never
compressed by this module. profile["tail_s"] keeps the bed playing after the last word. The bed
rises to its own level there and fades out, so the sound does not stop at once.
"""
import hashlib
import json
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def measure_loudnorm(ffmpeg: str, source: Path, target_i: float, target_tp: float, target_lra: float) -> dict:
    probe = subprocess.run(
        [
            ffmpeg,
            "-nostdin",
            "-hide_banner",
            "-i",
            str(source),
            "-af",
            f"loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}:print_format=json",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stderr
    start, end = probe.rfind("{"), probe.rfind("}")
    if start < 0 or end < start:
        raise RuntimeError(f"ffmpeg did not report loudness for {source}")
    return json.loads(probe[start:end + 1])


def loudnorm_filter(target_i: float, target_tp: float, target_lra: float, measured: dict) -> str:
    return (
        f"loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}:linear=true"
        f":measured_I={measured['input_i']}:measured_TP={measured['input_tp']}"
        f":measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}"
        f":offset={measured['target_offset']}"
    )


def mix_background(
    ffmpeg: str,
    narration: Path,
    music: Path,
    output: Path,
    duration_s: float,
    narration_filter: str,
    profile: dict,
    sample_rate: int,
) -> dict:
    """Write a float WAV mix and return the music settings used."""
    if duration_s <= 0:
        raise ValueError("narration duration must be positive")
    if not music.is_file():
        raise FileNotFoundError(f"no music file: {music}")

    target_i = float(profile["integrated_lufs"])
    target_tp = float(profile.get("true_peak_db", -8.0))
    target_lra = float(profile.get("lra", 11.0))
    measured = measure_loudnorm(ffmpeg, music, target_i, target_tp, target_lra)
    music_filter = loudnorm_filter(target_i, target_tp, target_lra, measured)

    tail = max(0.0, float(profile.get("tail_s", 0.0)))
    total_s = duration_s + tail
    fade_in = min(float(profile["fade_in_s"]), total_s / 3)
    fade_out = min(float(profile["fade_out_s"]), total_s / 3)
    fade_out_start = max(0.0, total_s - fade_out)
    threshold = float(profile["duck_threshold"])
    ratio = float(profile["duck_ratio"])
    attack = float(profile["duck_attack_ms"])
    release = float(profile["duck_release_ms"])

    pad = f",apad=pad_dur={tail:.6f}" if tail > 0 else ""  # apad without a duration pads forever
    filters = (
        f"[0:a]{narration_filter},aresample={sample_rate},"
        f"aformat=sample_fmts=fltp:channel_layouts=mono{pad},asplit=2[voice][key];"
        f"[1:a]{music_filter},aresample={sample_rate},"
        "aformat=sample_fmts=fltp:channel_layouts=mono,"
        f"atrim=end={total_s:.6f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d={fade_in:.6f},"
        f"afade=t=out:st={fade_out_start:.6f}:d={fade_out:.6f}[bed];"
        f"[bed][key]sidechaincompress=threshold={threshold}:ratio={ratio}:"
        f"attack={attack}:release={release}[ducked];"
        "[voice][ducked]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mix]"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-nostdin",
            "-v",
            "error",
            "-y",
            "-i",
            str(narration),
            "-stream_loop",
            "-1",
            "-i",
            str(music),
            "-filter_complex",
            filters,
            "-map",
            "[mix]",
            "-ar",
            str(sample_rate),
            "-ac",
            "1",
            "-c:a",
            "pcm_f32le",
            str(output),
        ],
        check=True,
    )
    return {
        "source": str(music),
        "sha256": sha256(music),
        "integrated_lufs": target_i,
        "true_peak_db": target_tp,
        "tail_s": round(tail, 3),
        "fade_in_s": round(fade_in, 3),
        "fade_out_s": round(fade_out, 3),
        "duck_threshold": threshold,
        "duck_ratio": ratio,
        "duck_attack_ms": attack,
        "duck_release_ms": release,
        "source_levels": measured,
    }
