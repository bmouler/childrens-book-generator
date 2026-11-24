"""Minimal xAI Grok Imagine client.

The client reads XAI_API_KEY from the environment. It never prints or stores the key.
Every image is cached on disk by a hash of (endpoint, model, prompt, refs, params), so a
re-run of the same book never pays twice and never changes pixels.
"""
from __future__ import annotations

import base64
import hashlib
from io import BytesIO
import json
import os
import pathlib
import time

import httpx
from PIL import Image

API = "https://api.x.ai/v1"
OUT = pathlib.Path(__file__).parent / "out"
CACHE = OUT / "cache"
UA = "childrens-book-generator"


def token() -> str:
    key = os.environ.get("XAI_API_KEY")
    if not key:
        raise RuntimeError("XAI_API_KEY is not set")
    return key


def _data_uri(path: pathlib.Path) -> str:
    mime = "image/png" if path.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def _matching_output(meta: pathlib.Path, expected: dict) -> dict | None:
    try:
        record = json.loads(meta.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if "provider" not in record and str(record.get("model", "")).startswith("grok-"):
        record["provider"] = "xai"
    for key, value in expected.items():
        if key == "ref_hashes" and key not in record:
            continue
        if record.get(key) != value:
            return None
    return record


def image(
    prompt: str,
    *,
    name: str,
    model: str = "grok-imagine-image-2.0",
    refs: list[pathlib.Path] | None = None,
    aspect_ratio: str = "3:2",
    resolution: str = "1k",
    quality: str | None = None,
    force: bool = False,
) -> pathlib.Path:
    """Generate (no refs) or edit-from-references (refs). Returns the saved image path.
    force=True ignores the cached picture and pays for a new one (a re-roll)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    refs = refs or []
    body: dict = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "response_format": "b64_json",
        "n": 1,
    }
    if quality and model == "grok-imagine-image-2.0":
        body["quality"] = quality
    endpoint = "images/generations"
    if refs:
        endpoint = "images/edits"
        body["images"] = [{"type": "image_url", "url": _data_uri(p)} for p in refs]

    # The reference hashes invalidate dependent pages when the character sheet changes.
    ref_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in refs]
    key = hashlib.sha256(
        json.dumps([endpoint, model, prompt, ref_hashes, aspect_ratio, resolution, quality], sort_keys=True).encode()
    ).hexdigest()[:20]
    dest = OUT / f"{name}.png"
    meta = OUT / f"{name}.json"
    cached = CACHE / f"{key}.png"
    cached_meta = CACHE / f"{key}.json"
    expected = {
        "name": name,
        "provider": "xai",
        "endpoint": endpoint,
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "quality": quality,
        "refs": [path.name for path in refs],
        "ref_hashes": ref_hashes,
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not force and dest.exists():
        record = _matching_output(meta, expected)
        if record is not None:
            record.update(expected)
            encoded = json.dumps(record, indent=2, ensure_ascii=False)
            meta.write_text(encoded)
            cached.write_bytes(dest.read_bytes())
            cached_meta.write_text(encoded)
            print(f"[output/xai] {name}")
            return dest
    if cached.exists() and not force:
        dest.write_bytes(cached.read_bytes())
        try:
            record = json.loads(cached_meta.read_text())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            with Image.open(cached) as cached_image:
                cached_size = cached_image.size
            record = {
                **expected,
                "size": cached_size,
                "seconds": None,
                "usage": None,
                "moderation": None,
                "cache_metadata": "reconstructed",
            }
        record.update(expected)
        encoded = json.dumps(record, indent=2, ensure_ascii=False)
        meta.write_text(encoded)
        cached_meta.write_text(encoded)
        print(f"[cache/xai] {name}")
        return dest

    t0 = time.time()
    r = httpx.post(
        f"{API}/{endpoint}",
        headers={"Authorization": f"Bearer {token()}", "User-Agent": UA, "Content-Type": "application/json"},
        json=body,
        timeout=240,
    )
    dt = time.time() - t0
    if r.status_code != 200:
        raise RuntimeError(f"{endpoint} {model} -> HTTP {r.status_code}: {r.text[:400]}")
    j = r.json()
    raw = base64.b64decode(j["data"][0]["b64_json"])
    im = Image.open(BytesIO(raw)).convert("RGB")
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(dest, "PNG")
    cached.write_bytes(dest.read_bytes())
    record = {
        **expected,
        "size": im.size,
        "seconds": round(dt, 1),
        "usage": j.get("usage"),
        "moderation": [d.get("respect_moderation") for d in j["data"]],
    }
    encoded = json.dumps(record, indent=2, ensure_ascii=False)
    meta.write_text(encoded)
    cached_meta.write_text(encoded)
    print(f"[api ] {name}: {im.size} in {dt:.1f}s usage={j.get('usage')}")
    return dest
