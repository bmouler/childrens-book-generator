#!/usr/bin/env python3
"""Score Russian stress markers against the hand-checked stories, and turn two markers into a review list.

usage: stress_check.py score ENGINE[,ENGINE ...] [STORY ...] [--house] [--errors N]
       stress_check.py vote  STORY [STORY ...] [--engines ruaccent,silero] [--house] [--write-stressed [--force]]
       stress_check.py suspects [STORY ...] [--engines ruaccent,silero] [--out FILE]

ENGINE is ruaccent, silero or udarenie. With no STORY, the gold is every stories/*.stressed.txt.
The gold is what a person fixed after RUAccent ran, so a score is agreement with the hand-checked
marks, not accuracy. A word that RUAccent got wrong and nobody caught still counts for RUAccent.

Protocol. The plain text of a gold line goes to the engine. Both sides drop the marks that the house
rule forbids: a word needs a mark only when it has two or more vowels and no ё. The marked vowel is
compared by its place among the vowels of the word, so е and ё spelling cannot cause a false miss.
A line whose words differ between the gold and the engine is counted as misaligned and not scored.

`score` with two engines also measures the review list: the words where the first two engines
disagree. It prints how much of the first engine's error the list holds and how long the list is.
`vote` writes that list for a new story, so a person checks the disagreements, not every word.

Run with Python 3.11. RUAccent needs huggingface_hub 0.25.x on this Mac:
  uv run --no-project --python 3.11 --with ruaccent --with silero-stress --with "huggingface_hub==0.25.2" \\
      python stress_check.py score ruaccent,silero
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import add_stress

HERE = Path(__file__).resolve().parent
STORIES = HERE / "stories"
VOWELS = add_stress.VOWELS
WORD = add_stress.WORD
ENGINES = ("ruaccent", "silero", "udarenie")


def plain(word: str) -> str:
    return word.replace("+", "")


def fold(word: str) -> str:
    return plain(word).lower().replace("ё", "е")


def needs_stress(word: str) -> bool:
    """The house rule: two or more vowels and no ё."""
    letters = plain(word)
    return sum(ch in VOWELS for ch in letters) >= 2 and "ё" not in letters.lower()


def stress_slot(word: str) -> int | None:
    """The stressed vowel, counted among the vowels of the word from zero. None without a mark."""
    where = word.find("+")
    if where < 0:
        return None
    return sum(ch in VOWELS for ch in plain(word[:where]))


@dataclass
class Result:
    line: int
    word: str
    gold: int | None
    cand: int | None

    @property
    def verdict(self) -> str:
        if self.gold is None:
            return "gold-unmarked"
        if self.cand is None:
            return "missing"
        return "ok" if self.gold == self.cand else "wrong"


def compare_line(number: int, gold: str, cand: str) -> list[Result] | None:
    """One Result per word that needs a mark, or None when the two lines hold different words."""
    left, right = WORD.findall(gold), WORD.findall(cand)
    if [fold(w) for w in left] != [fold(w) for w in right]:
        return None
    return [Result(number, plain(g), stress_slot(g), stress_slot(c)) for g, c in zip(left, right) if needs_stress(g)]


@dataclass
class Tally:
    needed: int = 0
    ok: int = 0
    wrong: int = 0
    missing: int = 0
    gold_unmarked: int = 0
    misaligned_lines: int = 0
    yo_words: int = 0
    errors: list[tuple[str, Result]] = field(default_factory=list)

    def add(self, story: str, results: list[Result] | None) -> None:
        if results is None:
            self.misaligned_lines += 1
            return
        for item in results:
            if item.verdict == "gold-unmarked":
                self.gold_unmarked += 1
                continue
            self.needed += 1
            if item.verdict == "ok":
                self.ok += 1
            else:
                self.wrong += item.verdict == "wrong"
                self.missing += item.verdict == "missing"
                self.errors.append((story, item))

    @property
    def agreement(self) -> float:
        return self.ok / self.needed if self.needed else 0.0

    @property
    def agreement_poly(self) -> float:
        total = self.needed + self.yo_words
        return (self.ok + self.yo_words) / total if total else 0.0


def gold_lines(story: str) -> list[tuple[int, str]]:
    """(line number, marked line) for every non-blank line of the hand-checked file."""
    path = STORIES / f"{story}.stressed.txt"
    return [(n, line) for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1) if line.strip()]


def strip_heading(line: str) -> tuple[str, str]:
    return ("# ", line[2:]) if line.startswith("# ") else ("", line)


# --------------------------------------------------------------------------- engines


class Engine:
    name = ""

    def mark(self, line: str) -> str:
        """The line with a + before each stressed vowel, in the spelling of the source, house rule applied."""
        raise NotImplementedError

    def finish(self, source: str, marked: str) -> str:
        result = add_stress.reconcile(source, marked.strip())
        return add_stress.tidy(result, False) if result is not None else source


class RuAccent(Engine):
    name = "ruaccent"

    def __init__(self, house: bool) -> None:
        from ruaccent import RUAccent
        custom = json.loads(add_stress.DEFAULT_DICTIONARY.read_text(encoding="utf-8")) if house else {}
        self.engine = RUAccent()
        self.engine.load(omograph_model_size="turbo3.1", use_dictionary=True, custom_dict=custom, device="CPU")

    def mark(self, line: str) -> str:
        return self.finish(line, add_stress.accent(self.engine, line))


class Silero(Engine):
    name = "silero"

    def __init__(self, house: bool) -> None:
        from silero_stress import load_accentor
        self.engine = load_accentor()

    def mark(self, line: str) -> str:
        return self.finish(line, self.engine(line, put_yo=False, stress_single_vowel=False))


class Udarenie(Engine):
    name = "udarenie"

    def __init__(self, house: bool) -> None:
        from udarenie import load_accentor
        user = str(add_stress.DEFAULT_DICTIONARY) if house else None
        self.engine = load_accentor(use_morph=True, user_dict=user, stress_monosyllabic=False, device="cpu")

    def mark(self, line: str) -> str:
        return self.finish(line, self.engine(line))


def make_engine(name: str, house: bool) -> Engine:
    if name not in ENGINES:
        sys.exit(f"unknown engine {name!r}. Choose from {', '.join(ENGINES)}")
    return {"ruaccent": RuAccent, "silero": Silero, "udarenie": Udarenie}[name](house)


def mark_lines(engine: Engine, lines: list[tuple[int, str]]) -> dict[int, str]:
    """Run the engine over the plain text of each gold line. A heading keeps its `# `."""
    out = {}
    for number, line in lines:
        prefix, body = strip_heading(line)
        out[number] = prefix + engine.mark(plain(body))
    return out


# --------------------------------------------------------------------------- score


def yo_count(gold_body: str) -> int:
    """Words with two or more vowels and ё. They need no mark, and the HANDOFF figure counts them as agreeing."""
    return sum(1 for w in WORD.findall(gold_body) if sum(ch in VOWELS for ch in plain(w)) >= 2 and "ё" in plain(w).lower())


def score_engine(story_lines: dict[str, list[tuple[int, str]]], marked: dict[str, dict[int, str]]) -> Tally:
    tally = Tally()
    for story, lines in story_lines.items():
        for number, gold in lines:
            body = strip_heading(gold)[1]
            results = compare_line(number, body, strip_heading(marked[story][number])[1])
            tally.add(story, results)
            if results is not None:
                tally.yo_words += yo_count(body)
    return tally


def disagreement_report(story_lines, first: dict[str, dict[int, str]], *others: dict[str, dict[int, str]]) -> dict:
    """How well the words where the first engine differs from ANY other engine find the first engine's errors."""
    needed = errors = flagged = caught = 0
    for story, lines in story_lines.items():
        for number, gold in lines:
            g = strip_heading(gold)[1]
            a = compare_line(number, g, strip_heading(first[story][number])[1])
            rest = [compare_line(number, g, strip_heading(other[story][number])[1]) for other in others]
            if a is None or any(r is None for r in rest):
                continue
            for index, x in enumerate(a):
                if x.verdict == "gold-unmarked":
                    continue
                needed += 1
                wrong = x.verdict != "ok"
                differ = any(r[index].cand != x.cand for r in rest if r is not None)
                errors += wrong
                flagged += differ
                caught += wrong and differ
    return {"needed": needed, "first_errors": errors, "flagged": flagged, "errors_in_flagged": caught,
            "list_share": flagged / needed if needed else 0.0, "recall": caught / errors if errors else 0.0,
            **fill_report(story_lines, first, others[0])}


def fill_report(story_lines, first: dict[str, dict[int, str]], second: dict[str, dict[int, str]]) -> dict:
    """The draft that keeps the first engine's mark and takes the second engine's mark only where the first left none.

    Returns how many words that draft gets wrong, and how many of those the review list (words where the two
    engines differ, including every filled word) holds."""
    needed = wrong = caught = filled = filled_right = 0
    for story, lines in story_lines.items():
        for number, gold in lines:
            g = strip_heading(gold)[1]
            a = compare_line(number, g, strip_heading(first[story][number])[1])
            b = compare_line(number, g, strip_heading(second[story][number])[1])
            if a is None or b is None:
                continue
            for x, y in zip(a, b):
                if x.verdict == "gold-unmarked":
                    continue
                needed += 1
                merged = x.cand if x.cand is not None else y.cand
                bad = merged != x.gold
                wrong += bad
                caught += bad and x.cand != y.cand
                if x.cand is None:
                    filled += 1
                    filled_right += not bad
    return {"fill_words": filled, "fill_right": filled_right, "draft_errors": wrong, "draft_errors_in_list": caught,
            "draft_agreement": 1 - wrong / needed if needed else 0.0}


def run_score(args) -> None:
    names = [name.strip() for name in args.engine.split(",") if name.strip()]
    stories = args.stories or sorted(p.name[:-len(".stressed.txt")] for p in STORIES.glob("*.stressed.txt"))
    story_lines = {story: gold_lines(story) for story in stories}
    total_lines = sum(len(v) for v in story_lines.values())
    marked: dict[str, dict[str, dict[int, str]]] = {}
    for name in names:
        started = time.time()
        engine = make_engine(name, args.house)
        print(f"{name}: loaded in {time.time() - started:.1f} s, marking {total_lines} lines of {len(stories)} stories")
        started = time.time()
        marked[name] = {story: mark_lines(engine, lines) for story, lines in story_lines.items()}
        tally = score_engine(story_lines, marked[name])
        print(f"{name}{' + house corrections' if args.house else ''}: agreement {tally.ok}/{tally.needed} = "
              f"{100 * tally.agreement:.2f}% of the words that need a mark | wrong {tally.wrong} missing {tally.missing} | "
              f"gold unmarked {tally.gold_unmarked} | misaligned lines {tally.misaligned_lines} | {time.time() - started:.0f} s")
        print(f"  over every word with two vowels, as HANDOFF counts it: {tally.ok + tally.yo_words}/"
              f"{tally.needed + tally.yo_words} = {100 * tally.agreement_poly:.2f}%")
        for story in stories:
            single = score_engine({story: story_lines[story]}, {story: marked[name][story]})
            print(f"  {story:9s} {single.ok:4d}/{single.needed:<4d} {100 * single.agreement:6.2f}%")
        seen: dict[str, int] = {}
        for _, item in tally.errors:
            seen[item.word.lower()] = seen.get(item.word.lower(), 0) + 1
        print("  most missed words: " + ", ".join(f"{w} ({n})" for w, n in sorted(seen.items(), key=lambda kv: -kv[1])[:args.errors]))
    pairs = [(other, [other]) for other in names[1:]]
    if len(names) > 2:
        pairs.append(("any of " + " or ".join(names[1:]), names[1:]))
    for label, others in pairs:
        report = disagreement_report(story_lines, marked[names[0]], *(marked[o] for o in others))
        print(f"review list {names[0]} against {label}: {report['flagged']} of {report['needed']} words "
              f"({100 * report['list_share']:.1f}%) hold {report['errors_in_flagged']} of the {report['first_errors']} "
              f"{names[0]} errors ({100 * report['recall']:.1f}%)")
    if len(names) >= 2:
        report = disagreement_report(story_lines, marked[names[0]], marked[names[1]])
        print(f"draft = {names[0]} marks, {names[1]} fills the {report['fill_words']} words {names[0]} left unmarked "
              f"({report['fill_right']} of them right): agreement {100 * report['draft_agreement']:.2f}%, "
              f"{report['draft_errors']} errors left, {report['draft_errors_in_list']} of them in the review list")


# --------------------------------------------------------------------------- vote


def fill_line(first_line: str, second_line: str) -> str:
    """The first line, with the second line's mark on every word that needs a mark and has none."""
    first, second = list(WORD.finditer(first_line)), WORD.findall(second_line)
    if len(first) != len(second):
        return first_line
    out, last = [], 0
    for match, other in zip(first, second):
        word = match.group(0)
        out.append(first_line[last:match.start()])
        take = needs_stress(word) and stress_slot(word) is None and stress_slot(other) is not None
        out.append(other if take else word)
        last = match.end()
    out.append(first_line[last:])
    return "".join(out)


def vote_rows(lines: list[tuple[int, str]], outputs: list[dict[int, str]]) -> tuple[list[tuple], dict[int, str]]:
    """The words a person must check, and the draft lines. The draft is the first engine's text, with the second
    engine's mark on each word the first left unmarked.

    why: unmarked (neither engine marked it, mark it by hand), filled (only the second engine marked it),
    differs (both marked it, on different vowels). A word that only the first engine marked is not listed."""
    rows, merged = [], {}
    for number, line in lines:
        prefix, body = strip_heading(line)
        words = WORD.findall(body)
        marks = [WORD.findall(strip_heading(out[number])[1]) for out in outputs]
        if all(len(m) == len(words) for m in marks):
            for index, word in enumerate(words):
                if not needs_stress(word):
                    continue
                first, second = (stress_slot(m[index]) for m in marks)
                if first is None and second is None:
                    why = "unmarked"
                elif first is None:
                    why = "filled"
                elif second is not None and first != second:
                    why = "differs"
                else:
                    continue
                rows.append((number, word, [m[index] for m in marks], why, line))
        merged[number] = prefix + fill_line(strip_heading(outputs[0][number])[1], strip_heading(outputs[1][number])[1])
    return rows, merged


def run_vote(args) -> None:
    names = [name.strip() for name in args.engines.split(",") if name.strip()]
    if len(names) != 2:
        sys.exit("vote wants exactly two engines")
    engines = [make_engine(name, args.house) for name in names]
    for story in args.stories:
        plain_path, stressed_path = STORIES / f"{story}.txt", STORIES / f"{story}.stressed.txt"
        original = plain_path.read_text(encoding="utf-8").splitlines()
        lines = [(n, plain(line)) for n, line in enumerate(original, 1) if line.strip()]
        rows, merged = vote_rows(lines, [mark_lines(e, lines) for e in engines])
        total = sum(1 for _, text in lines for w in WORD.findall(strip_heading(text)[1]) if needs_stress(w))
        counts = {why: sum(1 for r in rows if r[3] == why) for why in ("unmarked", "filled", "differs")}
        review = STORIES / f"{story}.stress-review.md"
        body = [f"# Stress review: {story}", "",
                f"Draft: {names[0]} marks, and {names[1]} marks where {names[0]} left none. "
                f"{len(rows)} of {total} words need a look: {counts['unmarked']} unmarked, {counts['filled']} filled, "
                f"{counts['differs']} where the engines differ. Every other word has a mark that both engines accept or that "
                f"only {names[0]} gave. Read the rows, fix the draft by hand, then run `stress_check.py suspects`.", "",
                "| line | word | why | " + " | ".join(names) + " | the line |", "|---:|---|---|" + "---|" * len(names) + "---|"]
        for number, word, marked, why, text in rows:
            body.append(f"| {number} | {word} | {why} | " + " | ".join(marked) + f" | {text} |")
        review.write_text("\n".join(body) + "\n", encoding="utf-8")
        print(f"{story}: {len(rows)} of {total} words to check ({counts['unmarked']} unmarked, {counts['filled']} filled, "
              f"{counts['differs']} differ) -> {review.name}")
        if args.write_stressed:
            if stressed_path.exists() and not args.force:
                print(f"  {stressed_path.name} exists, not overwritten. Use --force")
                continue
            stressed_path.write_text("\n".join(merged.get(n, line) for n, line in enumerate(original, 1)) + "\n", encoding="utf-8")
            print(f"  draft -> {stressed_path.name}")


def suspect_words(story_lines, first: dict[str, dict[int, str]], second: dict[str, dict[int, str]]) -> list[dict]:
    """Gold marks that two engines both contradict, with the same stressed vowel. A person should check these:
    a hand mark or a critic patch may be wrong, or both engines may share one error."""
    found = []
    for story, lines in story_lines.items():
        for number, gold in lines:
            g = strip_heading(gold)[1]
            left = WORD.findall(strip_heading(first[story][number])[1])
            right = WORD.findall(strip_heading(second[story][number])[1])
            words = WORD.findall(g)
            if not len(left) == len(right) == len(words):
                continue
            for gw, lw, rw in zip(words, left, right):
                if not needs_stress(gw):
                    continue
                gold_slot, slot = stress_slot(gw), stress_slot(lw)
                if gold_slot is not None and slot is not None and slot == stress_slot(rw) != gold_slot:
                    found.append({"story": story, "line": number, "gold": gw, "engines": lw, "text": g})
    return found


def run_suspects(args) -> None:
    stories = args.stories or sorted(p.name[:-len(".stressed.txt")] for p in STORIES.glob("*.stressed.txt"))
    story_lines = {story: gold_lines(story) for story in stories}
    names = [name.strip() for name in args.engines.split(",") if name.strip()]
    if len(names) != 2:
        sys.exit("suspects wants exactly two engines")
    marked = [{story: mark_lines(make_engine(name, args.house), lines) for story, lines in story_lines.items()} for name in names]
    found = suspect_words(story_lines, marked[0], marked[1])
    groups: dict[tuple[str, str, str], list[dict]] = {}
    for item in found:
        groups.setdefault((item["gold"].lower(), item["gold"], item["engines"]), []).append(item)
    rows = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0][0]))
    out = [f"# Gold stress marks that {names[0]} and {names[1]} both contradict", "",
           f"{len(found)} word uses, {len(rows)} distinct words, in {len(stories)} stories. The engines agree with each other and differ from the "
           "hand-checked mark. Check each one by ear and by dictionary before you change anything.", "",
           "| word as marked now | both engines say | uses | first place | the line |", "|---|---|---:|---|---|"]
    for (_, gold_form, engine_form), items in rows:
        first = items[0]
        out.append(f"| {gold_form} | {engine_form} | {len(items)} | {first['story']}:{first['line']} | {first['text']} |")
    text = "\n".join(out) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"{len(found)} word uses, {len(rows)} distinct words -> {args.out}")
    else:
        print(text)


def main() -> None:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    sub = ap.add_subparsers(dest="command", required=True)
    score = sub.add_parser("score")
    score.add_argument("engine", help="one engine, or two separated by a comma for the review list measure")
    score.add_argument("stories", nargs="*")
    score.add_argument("--house", action="store_true", help="apply config/russian-stress-corrections.json")
    score.add_argument("--errors", type=int, default=25, help="how many most-missed words to print")
    vote = sub.add_parser("vote", help="mark new stories with two engines and list the words to check")
    vote.add_argument("stories", nargs="+", help="story names in stories/ (the plain NAME.txt)")
    vote.add_argument("--engines", default="ruaccent,silero")
    vote.add_argument("--house", action="store_true", help="apply the house corrections to ruaccent")
    vote.add_argument("--write-stressed", action="store_true", help="write the draft to stories/NAME.stressed.txt")
    vote.add_argument("--force", action="store_true", help="overwrite an existing NAME.stressed.txt")
    suspects = sub.add_parser("suspects", help="hand-checked marks that two engines both contradict")
    suspects.add_argument("stories", nargs="*")
    suspects.add_argument("--engines", default="ruaccent,silero")
    suspects.add_argument("--house", action="store_true", help="apply the house corrections to ruaccent")
    suspects.add_argument("--out", default=None, help="write the table to this file")
    args = ap.parse_args()
    {"score": run_score, "vote": run_vote, "suspects": run_suspects}[args.command](args)


if __name__ == "__main__":
    main()
