"""Minimal OpenAI image client with prompt-and-reference-byte caching.

The client reads OPENAI_API_KEY. It never prints or stores the key. Each cache
entry is provider-specific, so OpenAI generation cannot replace an xAI cache
entry with the same prompt.
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

API = "https://api.openai.com/v1"
OUT = pathlib.Path(__file__).parent / "out"
CACHE = OUT / "cache"
UA = "childrens-book-generator-spike"

_SIZES = {
    ("1:1", "1k"): "1024x1024",
    ("1:1", "2k"): "2048x2048",
    ("3:2", "1k"): "1536x1024",
    ("3:2", "2k"): "3072x2048",
    ("2:3", "1k"): "1024x1536",
    ("2:3", "2k"): "2048x3072",
}


def token() -> str:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return key


def _data_uri(path: pathlib.Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def _estimated_cost(usage: dict | None) -> float | None:
    """Estimate standard-tier cost from the published GPT Image 2.5 rates."""
    if not usage:
        return None
    details = usage.get("input_tokens_details") or {}
    image_input = details.get("image_tokens")
    text_input = details.get("text_tokens")
    output = usage.get("output_tokens")
    if not isinstance(image_input, int) or not isinstance(text_input, int) or not isinstance(output, int):
        return None
    return round((image_input * 8 + text_input * 5 + output * 30) / 1_000_000, 6)

def _matching_output(meta: pathlib.Path, expected: dict) -> dict | None:
    try:
        record = json.loads(meta.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
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
    model: str = "gpt-image-2.5-sunburst-2026-09-08",
    refs: list[pathlib.Path] | None = None,
    aspect_ratio: str = "1:1",
    resolution: str = "2k",
    quality: str = "medium",
    force: bool = False,
) -> pathlib.Path:
    """Generate or edit an image and return its output path.

    force=True ignores the OpenAI cache and pays for a new image.
    """
    refs = refs or []
    try:
        size = _SIZES[(aspect_ratio, resolution)]
    except KeyError as exc:
        raise ValueError(f"unsupported OpenAI size: {aspect_ratio} at {resolution}") from exc

    endpoint = "images/edits" if refs else "images/generations"
    body: dict = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "output_format": "png",
        "background": "opaque",
        "n": 1,
    }
    if refs:
        body["images"] = [{"image_url": _data_uri(path)} for path in refs]

    CACHE.mkdir(parents=True, exist_ok=True)
    ref_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in refs]
    key = hashlib.sha256(
        json.dumps(
            ["openai", endpoint, model, prompt, ref_hashes, size, quality],
            sort_keys=True,
        ).encode()
    ).hexdigest()[:20]
    dest = OUT / f"{name}.png"
    meta = OUT / f"{name}.json"
    cached = CACHE / f"openai-{key}.png"
    cached_meta = CACHE / f"openai-{key}.json"
    expected = {
        "name": name,
        "provider": "openai",
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
            print(f"[output/openai] {name}")
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
                "estimated_cost_usd": None,
                "request_id": None,
                "cache_metadata": "reconstructed",
            }
        record.update(expected)
        encoded = json.dumps(record, indent=2, ensure_ascii=False)
        meta.write_text(encoded)
        cached_meta.write_text(encoded)
        print(f"[cache/openai] {name}")
        return dest

    started = time.time()
    response = httpx.post(
        f"{API}/{endpoint}",
        headers={
            "Authorization": f"Bearer {token()}",
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
        json=body,
        timeout=600,
    )
    seconds = time.time() - started
    if response.status_code != 200:
        raise RuntimeError(
            f"{endpoint} {model} -> HTTP {response.status_code}: {response.text[:400]}"
        )

    payload = response.json()
    raw = base64.b64decode(payload["data"][0]["b64_json"])
    rendered = Image.open(BytesIO(raw)).convert("RGB")
    rendered.save(dest, "PNG")
    cached.write_bytes(dest.read_bytes())

    usage = payload.get("usage")
    cost = _estimated_cost(usage)
    record = {
        **expected,
        "size": rendered.size,
        "seconds": round(seconds, 1),
        "usage": usage,
        "estimated_cost_usd": cost,
        "request_id": response.headers.get("x-request-id"),
    }
    encoded = json.dumps(record, indent=2, ensure_ascii=False)
    meta.write_text(encoded)
    cached_meta.write_text(encoded)
    cost_text = f" cost≈${cost:.4f}" if cost is not None else ""
    print(f"[api/openai] {name}: {rendered.size} in {seconds:.1f}s{cost_text}")
    return dest
