"""The sticker library: one flat icon per key word, as out/stickers/<name>.png (RGBA, transparent).

An icon is either cut from a generated sheet (out/stickers/sheets.json lists each sheet and its icon
names in grid order) or drawn by code (icons.py). A key word uses the sticker with its own name unless
ALIAS names another one: an adjective often shows the typical thing (heavy shows a stone).

usage: stickers.py cut     cut every sheet in sheets.json into the library
"""
from __future__ import annotations

import functools
import json
import pathlib

import numpy as np
from PIL import Image

import render as R

LIB = pathlib.Path(__file__).parent / "out" / "stickers"

ALIAS = {  # key word -> sticker name, when they differ
    # the older-kids books (23 to 37): a baby shows like its parent; a season shows its sign
    "kitten": "cat", "puppy": "dog", "calf": "cow", "duckling": "duck",
    "autumn": "leaf", "summer": "sun", "day": "sun", "smell": "nose", "open": "eye",
    "look": "eye", "see": "eye", "try": "hand",
    "water": "drop", "wet": "drop",
    "big": "elephant", "small": "mouse",
    "heavy": "stone", "light": "feather",
    "soft": "pillow", "hard": "stone",
    # folk tales (books 12 to 15): the verb shows a familiar thing
    "sow": "plant", "pull": "hand", "eat": "soup", "live": "house", "cry": "drop", "sit": "chair",
    "bark": "sound", "meow": "sound", "song": "sing", "be_happy": "happy",
}


def name_for(concept: str) -> str:
    return ALIAS.get(concept, concept)


def path(concept: str) -> pathlib.Path:
    return LIB / f"{name_for(concept)}.png"


def exists(concept: str) -> bool:
    return path(concept).exists()


@functools.lru_cache(maxsize=None)
def load(concept: str) -> Image.Image:
    p = path(concept)
    if not p.exists():
        raise FileNotFoundError(f"no sticker for the key word {concept!r}: {p.name} is not in {LIB}")
    return Image.open(p).convert("RGBA")


def cut_sheet(sheet: pathlib.Path, names: list[str], cols: int, rows: int) -> dict[str, Image.Image]:
    """Cut a sheet of icons on a plain background into RGBA icons with a clean transparent background."""
    im = Image.open(sheet).convert("RGB")
    out = {}
    for k, name in enumerate(names):
        cx, cy = k % cols, k // cols
        cell = im.crop((cx * im.width // cols, cy * im.height // rows,
                        (cx + 1) * im.width // cols, (cy + 1) * im.height // rows))
        alpha, colour = R.bg_alpha(cell)
        rgba = np.dstack([colour.round().astype(np.uint8), (alpha * 255).round().astype(np.uint8)])
        ys, xs = np.nonzero(alpha > 0.03)
        pad = 8
        box = (max(0, xs.min() - pad), max(0, ys.min() - pad),
               min(rgba.shape[1], xs.max() + 1 + pad), min(rgba.shape[0], ys.max() + 1 + pad))
        out[name] = Image.fromarray(rgba, "RGBA").crop(box)
    return out


def cut_all() -> list[str]:
    done = []
    for s in json.loads((LIB / "sheets.json").read_text()):
        for name, icon in cut_sheet(LIB / s["sheet"], s["names"], s["cols"], s["rows"]).items():
            icon.save(LIB / f"{name}.png", optimize=True)
            done.append(name)
    return done


if __name__ == "__main__":
    import sys

    if sys.argv[1:] != ["cut"]:
        raise SystemExit(__doc__)
    print("cut:", " ".join(cut_all()))
