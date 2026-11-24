#!/usr/bin/env python3
"""Read a whole Russian story as an editor would, with the local DeepSeek model, and list what is wrong.

usage: story_logic_review.py NAME_OR_FILE [NAME_OR_FILE ...] [--out-dir DIR] [--timeout S]

The critic loop (story_critique_loop.py) fixes stress marks and line breaks. It never reads the story as a
whole, so it let three errors through in the 16 finished stories: a boy in the bakery before he woke up,
the wrong word «Оно одеяло», and «кто-то рыжий» for a hedgehog and a mouse. This pass asks for one kind of
finding: a line that contradicts an earlier line, a wrong word, a fact that does not fit, a line that teaches
a lesson in words, anything frightening, anything religious.

The model must quote the line it blames. Every quote is checked against the text. A finding with a quote
that is not in the named line is rejected, and the report counts how many. Only a person decides what is
a real error. The model is a second pair of eyes, not a judge.

The endpoint is the same tunnel as the critic: http://127.0.0.1:18888/v1, model deepseek-v4.1-flash.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
STORIES = HERE / "stories"
ENDPOINT = "http://127.0.0.1:18888/v1"
MODEL = "deepseek-v4.1-flash"
KINDS = ("continuity", "grammar", "fact", "lesson", "fear", "religion")

SYSTEM = (
    "You are a careful editor of Russian bedtime and morning stories for children of two to five years. "
    "You read the whole story, then report only real defects. You never praise and never rewrite the story."
)

TASK = """Read the story below. Each line starts with its number. Find defects of these kinds only.

continuity: a line contradicts an earlier line, or a character, animal or thing is somewhere before it has arrived, is awake when it was asleep, holds something it put down, or is counted wrongly.
grammar: a wrong word, a wrong case, gender or number, or a sentence that is not Russian.
fact: a colour, sound, body part or habit that does not fit the animal or thing that is named.
lesson: a line in which the narrator or a character says what a child must or should do, or states a moral.
fear: anything that frightens a two-year-old: danger, a chase, a predator, being lost, a scary dark.
religion: anything religious.

Rules.
- Report a defect only when you can quote it. `quote` is copied exactly, letter for letter, from the line you name, 3 to 12 words.
- Prefer no finding to a weak finding. Do not report style, rhythm, repetition or taste.
- A refrain that repeats on purpose is not a defect.
- Fairy-tale logic is allowed: animals talk, a moon smiles. Judge consistency inside the story.
- Order the findings by line number. At most 12.

Answer with one JSON object and nothing else:
{"problems": [{"line": 14, "quote": "...", "kind": "continuity", "why": "one short English sentence"}]}
Use {"problems": []} when you find nothing.

STORY
"""


def numbered(text: str) -> str:
    return "\n".join(f"{n}: {line}" for n, line in enumerate(text.splitlines(), 1))


def parse_findings(raw: str) -> list[dict]:
    """The `problems` list of the first JSON object in the answer. An unreadable answer gives an empty list."""
    cleaned = re.sub(r"```(?:json)?", "", raw).strip()
    decoder = json.JSONDecoder()
    for start in (i for i, ch in enumerate(cleaned) if ch == "{"):
        try:
            data, _ = decoder.raw_decode(cleaned[start:])
        except json.JSONDecodeError:
            continue
        found = data.get("problems") if isinstance(data, dict) else None
        return [item for item in found if isinstance(item, dict)] if isinstance(found, list) else []
    return []


def verify(findings: list[dict], lines: list[str]) -> tuple[list[dict], list[dict]]:
    """(accepted, rejected). A finding is accepted when its quote is in the line it names, ignoring stress marks."""
    accepted, rejected = [], []
    for item in findings:
        number, quote, kind = item.get("line"), str(item.get("quote", "")).strip(), item.get("kind")
        ok = (isinstance(number, int) and 1 <= number <= len(lines) and quote
              and quote.replace("+", "") in lines[number - 1].replace("+", "") and kind in KINDS)
        (accepted if ok else rejected).append(item)
    accepted.sort(key=lambda item: item["line"])
    return accepted, rejected


def chat(prompt: str, endpoint: str, model: str, timeout: float) -> str:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
        "temperature": 0.2,
        "top_p": 0.9,
        "max_tokens": 32768,
        "reasoning_effort": "high",
        "chat_template_kwargs": {"enable_thinking": True},
    }, ensure_ascii=False).encode()
    request = urllib.request.Request(f"{endpoint.rstrip('/')}/chat/completions", data=body,
                                     headers={"content-type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as answer:
        payload = json.loads(answer.read().decode())
    return payload["choices"][0]["message"]["content"] or ""


def review(text: str, ask: Callable[[str], str]) -> dict:
    """Review one story. `ask` takes the prompt and returns the model's answer."""
    lines = text.splitlines()
    raw = ask(TASK + numbered(text))
    accepted, rejected = verify(parse_findings(raw), lines)
    return {"accepted": accepted, "rejected": rejected, "raw": raw}


def load(name: str) -> tuple[str, str, Path]:
    """(label, text, the story's own folder). NAME is a story in stories/, or a path to a text file."""
    path = Path(name)
    if path.is_file():
        return path.stem.split(".")[0], path.read_text(encoding="utf-8"), path.parent
    plain = STORIES / f"{name}.txt"
    return name, plain.read_text(encoding="utf-8"), STORIES


def main() -> None:
    ap = argparse.ArgumentParser(description="Read a story as an editor and list what is wrong.")
    ap.add_argument("stories", nargs="+")
    ap.add_argument("--endpoint", default=ENDPOINT)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--timeout", type=float, default=1800.0)
    ap.add_argument("--out-dir", default=None, help="write NAME.logic.json here (default: the story's folder)")
    args = ap.parse_args()
    for name in args.stories:
        label, text, folder = load(name)
        result = review(text, lambda prompt: chat(prompt, args.endpoint, args.model, args.timeout))
        out = Path(args.out_dir) if args.out_dir else folder
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{label}.logic.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        lines = text.splitlines()
        print(f"{label}: {len(result['accepted'])} findings, {len(result['rejected'])} rejected (quote not in the line)")
        for item in result["accepted"]:
            print(f"  line {item['line']} [{item['kind']}] {item['quote']}  <- {item.get('why', '')}")
            print(f"      {lines[item['line'] - 1]}")


if __name__ == "__main__":
    sys.exit(main())
