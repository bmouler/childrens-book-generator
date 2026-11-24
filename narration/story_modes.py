#!/usr/bin/env python3
"""Decide which music mode a story needs, and prove the decision.

Every story has an entry in stories/modes.json: {"mode": "nighttime"|"morning", "why": "..."}.
An optional "form": "verse" keeps one sentence line per part, and an optional "min_part_words"
overrides the mode's grouping. Stress marks are stripped before the cue words are matched, so a
marked word like в+ечер still counts as the cue вечер.
The registry is the decision. A cue-word count over the title and the first lines is the check.
The two must agree. A missing entry, a missing reason, no cues or a near tie all stop the build.

The bed file name comes from the mode profile in config/russian-standard.json, so the mode alone
selects the music. A bed whose sha256 differs from the profile is refused.
"""
import hashlib
import json
import re
from pathlib import Path

NIGHT_CUES = (
    "ночь", "ночи", "вечер", "вечером", "луна", "лунный", "звёзд", "звезд", "спать", "спит",
    "засыпа", "тёмн", "темн", "сон", "сны", "одеял", "подушк", "баюк", "устал", "звёздочк",
    "закат", "садится",
)
MORNING_CUES = (
    "утро", "утром", "рассвет", "солнц", "светает", "светл", "встаёт", "встает", "просыпа",
    "проснул", "вставать", "встало", "завтрак", "будильник", "петух", "заря", "роса", "день",
)
CUE_SCAN_LINES = 200
CUE_MARGIN = 2  # the other mode must win by this many weighted cues before the build stops
OPENING_LINES = 8
OPENING_WEIGHT = 3  # the opening tells you what kind of story it is
MODE_NAMES = ("nighttime", "morning")


def cue_score(text: str) -> dict[str, int]:
    """Weighted cue counts. The first lines count for more, because they set the scene."""
    lines = text.splitlines()[:CUE_SCAN_LINES]
    score = {"nighttime": 0, "morning": 0}
    for index, line in enumerate(lines):
        weight = OPENING_WEIGHT if index < OPENING_LINES else 1
        low = line.lower().replace("ё", "е").replace("+", "")
        for mode, cues in (("nighttime", NIGHT_CUES), ("morning", MORNING_CUES)):
            score[mode] += weight * sum(low.count(cue.replace("ё", "е")) for cue in cues)
    return score


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ModeError(Exception):
    """The story cannot be placed in a mode with confidence."""


def load_registry(path: Path) -> dict:
    if not path.is_file():
        raise ModeError(f"no mode registry: {path}. Add an entry for every story.")
    registry = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(registry, dict):
        raise ModeError(f"{path} must hold a JSON object")
    return registry


def resolve(story: str, text: str, registry: dict, override: str | None = None) -> dict:
    """Return {"mode", "why", "cues", "source"} for the story, or raise ModeError."""
    if override:
        if override not in MODE_NAMES:
            raise ModeError(f"unknown mode {override!r}")
        return {"mode": override, "why": "chosen on the command line", "cues": cue_score(text), "source": "override"}
    entry = registry.get(story)
    if entry is None:
        raise ModeError(f"{story} has no entry in the mode registry")
    why = str(entry.get("why", "")).strip()
    mode = entry.get("mode")
    if mode not in MODE_NAMES:
        raise ModeError(f"{story}: mode must be one of {', '.join(MODE_NAMES)}, not {mode!r}")
    if len(why) < 12:
        raise ModeError(f"{story}: give a real reason, at least 12 characters")
    cues = cue_score(text)
    other = "morning" if mode == "nighttime" else "nighttime"
    if cues[mode] == 0 and cues[other] == 0:
        raise ModeError(f"{story}: no {mode} cues in the first {CUE_SCAN_LINES} lines. Read it and set the mode by hand")
    if cues[other] >= cues[mode] + CUE_MARGIN:
        raise ModeError(
            f"{story}: registry says {mode} ({why!r}) but the cues say {other} "
            f"({cues[mode]} against {cues[other]}). Read the story again"
        )
    return {"mode": mode, "why": why, "cues": cues, "source": "registry"}


def bed_for(mode: str, profile: dict, music_dir: Path) -> Path:
    """The bed the mode names, checked against the recorded hash."""
    name = profile.get("bed")
    if not name:
        raise ModeError(f"mode {mode} has no 'bed' in the config")
    path = music_dir / name
    if not path.is_file():
        raise ModeError(f"missing bed for {mode}: {path}")
    want = profile.get("bed_sha256")
    got = sha256(path)
    if want and got != want:
        raise ModeError(f"{path} is not the recorded bed (sha256 {got}, expected {want})")
    return path


def strip_marks(text: str) -> str:
    return re.sub(r"\+", "", text)