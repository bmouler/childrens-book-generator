#!/usr/bin/env python3
"""Check a Russian story before the build renders it: the values record, the content and the format.

usage: story_values.py check NAME [NAME ...] [--strict]     stories in stories/, plain or stressed text
       story_values.py check --all [--strict]
       story_values.py values                                the closed values list

Three groups of rules.

1. The values record. Every story has an entry in stories/modes.json with `values` (one to three
   keys from config/values.json, the main value first) and `shows` (one English sentence that
   names the action which shows the value). `allows_fear` is true only for a story about a fear.
2. The content lint, from config/content-lint.json. Religious words and obscene words always fail.
   Fear words fail unless the story allows fear. The lists are whole tokens or token starts, so
   «край» and «богатый» do not trip «рай» and «бог».
3. The format of a short prose story: the title and the blank line, only characters that F5 knows,
   no digits or Latin letters, 700 to 850 words counted three ways, and every line under 150
   characters. A verse story and a long story with headings skip the word count.

Rules that only a careful writer needs are warnings: a line under 20 characters, a line that does
not end a sentence, a line outside two to 24 words. `--strict` turns the warnings into failures.
A writer runs with `--strict`. The build does not. Two findings are notes and never fail: an
unmarked repeated line and a five-word span that repeats outside the refrain. A cumulative tale
repeats on purpose, so a person decides.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config"
STORIES = HERE / "stories"
REGISTRY = STORIES / "modes.json"

CYRILLIC = re.compile(r"[А-Яа-яЁё]+")
HYPHENATED = re.compile(r"[А-Яа-яЁё]+(?:-[А-Яа-яЁё]+)*")
LATIN = re.compile(r"[A-Za-z]")
DIGIT = re.compile(r"\d")
# Every one of these is in F5TTS_v1_Base/vocab.txt (checked 2026-11-05). "+" is the stress mark.
ALLOWED = set(
    "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    " !\"'(),-.:;?«»—…+"
)
SENTENCE_END = tuple(".!?…:»")
WORDS_MIN, WORDS_MAX = 700, 850
LINE_MIN, LINE_MAX = 20, 150
LINE_WORDS_MIN, LINE_WORDS_MAX = 2, 24  # the renderer's own per-line rule
MAX_VALUES = 3
SHOWS_MIN = 20
REFRAIN_REPEATS = 3  # a line that occurs this often is a refrain, not an accident
SPAN = 5
NOTE = "note: "  # a finding that is shown and never fails, even with --strict
DESCRIPTION_MAX = 90


def load_json(name: str) -> dict:
    return json.loads((CONFIG / name).read_text(encoding="utf-8"))


def load_values() -> dict:
    return load_json("values.json")["values"]


def fold(text: str) -> str:
    """Lower case, no stress mark, ё as е."""
    return text.replace("+", "").lower().replace("ё", "е")


def tokens(line: str) -> list[str]:
    return CYRILLIC.findall(fold(line))


class Rule:
    """One word list of the content lint."""

    def __init__(self, raw: dict) -> None:
        self.exact = {fold(word) for word in raw.get("exact", [])}
        self.prefix = tuple(fold(word) for word in raw.get("prefix", []))
        self.skip = {fold(word) for word in raw.get("except", [])}

    def hit(self, token: str) -> bool:
        if token in self.exact:
            return True
        if not self.prefix or token in self.skip:
            return False
        return token.startswith(self.prefix)


def load_lint() -> dict[str, Rule]:
    raw = load_json("content-lint.json")
    return {name: Rule(raw[name]) for name in ("religion", "fear", "obscene")}


def content_problems(text: str, allows_fear: bool = False, lint: dict[str, Rule] | None = None) -> list[str]:
    """Religious, obscene and (unless allowed) fear words, by line number. The title is line 1."""
    lint = lint or load_lint()
    problems = []
    for number, line in enumerate(text.splitlines(), 1):
        for token in tokens(line):
            if lint["religion"].hit(token):
                problems.append(f"line {number}: religious word «{token}»")
            elif lint["obscene"].hit(token):
                problems.append(f"line {number}: obscene word «{token}»")
            elif lint["fear"].hit(token) and not allows_fear:
                problems.append(f"line {number}: fear word «{token}». Only a story about a fear sets allows_fear")
    return problems


def registry_problems(story: str, entry: dict | None, values: dict) -> list[str]:
    """The values record of one story. An empty list means the record is complete and legal."""
    if entry is None:
        return [f"{story} has no entry in stories/modes.json"]
    problems = []
    chosen = entry.get("values")
    if not isinstance(chosen, list) or not chosen:
        problems.append("`values` must be a list of one to three keys")
    else:
        if len(chosen) > MAX_VALUES:
            problems.append(f"`values` has {len(chosen)} keys, the most is {MAX_VALUES}")
        unknown = [key for key in chosen if key not in values]
        if unknown:
            problems.append(f"unknown value {', '.join(map(repr, unknown))}. The list: {', '.join(values)}")
        if len(set(map(str, chosen))) != len(chosen):
            problems.append("`values` repeats a key")
    shows = entry.get("shows")
    if not isinstance(shows, str) or len(shows.strip()) < SHOWS_MIN:
        problems.append(f"`shows` must be one English sentence of at least {SHOWS_MIN} characters")
    elif CYRILLIC.search(shows):
        problems.append("`shows` is written in English")
    if "allows_fear" in entry and not isinstance(entry["allows_fear"], bool):
        problems.append("`allows_fear` must be true or false")
    if "min_words" in entry and not (isinstance(entry["min_words"], int) and 100 <= entry["min_words"] <= WORDS_MAX):
        problems.append(f"`min_words` must be a whole number from 100 to {WORDS_MAX}")
    description = entry.get("description")
    tail = {"nighttime": "Night.", "morning": "Morning."}.get(entry.get("mode"))
    if not isinstance(description, str) or not 20 <= len(description.strip()) <= DESCRIPTION_MAX \
            or CYRILLIC.search(description):
        problems.append(f"`description` is one English line of 20 to {DESCRIPTION_MAX} characters for the page")
    elif tail and not description.endswith(tail):
        problems.append(f"`description` ends with «{tail}»")
    return problems


def kind_of(entry: dict, text: str) -> str:
    if entry.get("form") == "verse":
        return "verse"
    if any(line.startswith("# ") for line in text.splitlines()):
        return "long"
    return "short"


def word_counts(lines: list[str]) -> tuple[int, int, int]:
    """Letters only, hyphen-joined and whitespace tokens that hold a letter."""
    body = [fold(line) for line in lines]
    letters = sum(len(CYRILLIC.findall(line)) for line in body)
    hyphen = sum(len(HYPHENATED.findall(line)) for line in body)
    spaced = sum(1 for line in body for chunk in line.split() if CYRILLIC.search(chunk))
    return letters, hyphen, spaced


def format_problems(text: str, kind: str, min_words: int = WORDS_MIN) -> tuple[list[str], list[str]]:
    """(errors, warnings) for the shape of the file."""
    errors: list[str] = []
    warnings: list[str] = []
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if not lines or not lines[0].strip() or lines[0].startswith("# "):
        return ["the first line must be the title"], warnings
    if len(lines) < 2 or lines[1].strip():
        errors.append("a blank line must follow the title")
    for number, line in enumerate(lines, 1):
        heading = kind == "long" and line.startswith("# ")
        stripped = line[2:] if heading else line
        if LATIN.search(stripped):
            errors.append(f"line {number}: Latin letters: {line}")
        if DIGIT.search(stripped) and not heading:
            errors.append(f"line {number}: digits. Spell the number out: {line}")
        bad = sorted({ch for ch in stripped if ch not in ALLOWED and not LATIN.match(ch) and not ch.isdigit()})
        if bad:
            errors.append(f"line {number}: characters F5 does not know {bad}: {line}")
        if len(line) > LINE_MAX:
            errors.append(f"line {number}: {len(line)} characters, the most is {LINE_MAX}")
    body = [line for line in lines[2:] if line.strip() and not line.startswith("# ")]
    counts = {}
    for line in body:
        counts[fold(" ".join(line.split()))] = counts.get(fold(" ".join(line.split())), 0) + 1
    refrains = {key for key, count in counts.items() if count >= REFRAIN_REPEATS}
    if kind == "short":
        total = word_counts(lines[2:])
        if not all(min_words <= count <= WORDS_MAX for count in total):
            errors.append(
                f"words (letters / hyphen-joined / spaced) {total[0]} / {total[1]} / {total[2]}, "
                f"each must be {min_words} to {WORDS_MAX}")
    for line in body:
        if kind != "verse" and len(line) < LINE_MIN and fold(" ".join(line.split())) not in refrains:
            warnings.append(f"under {LINE_MIN} characters, F5 may garble it: {line}")
        if kind == "short":
            if not line.rstrip().endswith(SENTENCE_END):
                warnings.append(f"does not end a sentence: {line}")
            n = len(CYRILLIC.findall(line))
            if not LINE_WORDS_MIN <= n <= LINE_WORDS_MAX:
                warnings.append(f"{n} words in one line, the renderer wants {LINE_WORDS_MIN} to {LINE_WORDS_MAX}: {line}")
    twice = sorted(key for key, count in counts.items() if count == 2)
    for key in twice:
        warnings.append(f"{NOTE}a line repeats twice, so it is neither a refrain nor new: {key}")
    warnings += [NOTE + item for item in span_repeats(body, refrains)]
    return errors, warnings


def span_repeats(body: list[str], refrains: set[str], span: int = SPAN, limit: int = 6) -> list[str]:
    """Five-word spans that occur twice outside the refrain lines. A model that loops writes these."""
    seen: dict[tuple[str, ...], int] = {}
    reported: list[str] = []
    for index, line in enumerate(body):
        if fold(" ".join(line.split())) in refrains:
            continue
        words = tokens(line)
        for start in range(len(words) - span + 1):
            gram = tuple(words[start:start + span])
            if gram in seen and seen[gram] != index:
                text = " ".join(gram)
                if text not in reported:
                    reported.append(text)
            seen.setdefault(gram, index)
    return [f"a {span}-word span repeats outside the refrain: «{text}»" for text in reported[:limit]]


def check_story(story: str, text: str, registry: dict, values: dict | None = None,
                lint: dict[str, Rule] | None = None) -> tuple[list[str], list[str]]:
    """(errors, warnings) for one story. `text` may be plain or stress marked."""
    values = values or load_values()
    entry = registry.get(story)
    errors = registry_problems(story, entry, values)
    if entry is None:
        return errors, []
    errors += content_problems(text, bool(entry.get("allows_fear", False)), lint)
    fmt_errors, warnings = format_problems(text, kind_of(entry, text), int(entry.get("min_words", WORDS_MIN)))
    return errors + fmt_errors, warnings


def story_text(story: str) -> str:
    stressed = STORIES / f"{story}.stressed.txt"
    plain = STORIES / f"{story}.txt"
    return (stressed if stressed.is_file() else plain).read_text(encoding="utf-8")


def report(name: str, errors: list[str], warnings: list[str], strict: bool) -> bool:
    """Print one story's findings. True when the story fails."""
    bad = errors + ([w for w in warnings if not w.startswith(NOTE)] if strict else [])
    print(f"{name}: {'FAIL' if bad else 'PASS'} ({len(errors)} errors, {len(warnings)} warnings and notes)")
    for item in errors:
        print(f"  error: {item}")
    for item in warnings:
        print(f"  warning: {item}")
    return bool(bad)


def check_file(text_path: Path, entry_path: Path, strict: bool, values: dict) -> int:
    """A draft and its registry entry, both in files. The shared modes.json stays untouched."""
    import story_modes  # not at the top: it needs Python 3.10 and this module also runs on older ones
    name = text_path.name.split(".")[0]
    text = text_path.read_text(encoding="utf-8")
    registry = {name: json.loads(entry_path.read_text(encoding="utf-8"))}
    errors, warnings = check_story(name, text, registry, values)
    try:
        placed = story_modes.resolve(name, text, registry)
        print(f"mode {placed['mode']}, cues {placed['cues']}")
    except story_modes.ModeError as err:
        errors.append(f"mode: {err}")
    return 1 if report(name, errors, warnings, strict) else 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Check the values record, the content and the format of a story.")
    sub = ap.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("stories", nargs="*")
    check.add_argument("--all", action="store_true", help="every story in stories/modes.json")
    check.add_argument("--strict", action="store_true", help="warnings fail too")
    sub.add_parser("values")
    one = sub.add_parser("file", help="check a draft with its registry entry in a JSON file. modes.json is not read")
    one.add_argument("text")
    one.add_argument("entry")
    one.add_argument("--strict", action="store_true", help="warnings fail too")
    args = ap.parse_args()
    values = load_values()
    if args.command == "values":
        for key, item in values.items():
            mark = f"confirmed {item['confirmed']}" if item["confirmed"] else "from the finished stories"
            print(f"{key:11s} {item['name']} ({mark}): {item['means']}")
        return
    if args.command == "file":
        sys.exit(check_file(Path(args.text), Path(args.entry), args.strict, values))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    names = list(registry) if args.all else args.stories
    if not names:
        sys.exit("name a story or use --all")
    lint = load_lint()
    failed = 0
    for name in names:
        try:
            text = story_text(name)
        except FileNotFoundError:
            print(f"{name}: no text in stories/")
            failed += 1
            continue
        errors, warnings = check_story(name, text, registry, values, lint)
        failed += report(name, errors, warnings, args.strict)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
