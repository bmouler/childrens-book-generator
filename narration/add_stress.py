#!/usr/bin/env python3
"""Mark word stress in Russian text with RUAccent. A "+" goes before the stressed vowel: мол+око.

usage: add_stress.py IN.txt OUT.txt [--dictionary WORDS.json] [--model turbo3.1] [--keep-monosyllables]

Each line is a sentence or a part. Lines stay in place and blank lines stay blank. A line that already has
a "+" is kept as written, so hand marks win. The built-in `config/russian-stress-corrections.json` fixes
recurring unambiguous errors. WORDS.json adds or overrides entries for names and rare words: {"сигги": "с+игги"}.

The spoken words never change. RUAccent also restores ё, and it gets that wrong (небе became нёбе, все became
всё). This script puts the spelling of your text back. When RUAccent had put ё there, the vowel gets the stress
mark instead. A line whose letters differ in any other way is left unmarked, and the script says so.
The approved hand-marked texts carry no mark on a one-vowel word and none before ё, so this script removes
those marks. --keep-monosyllables keeps the marks on one-vowel words.

Run it on the render machine in the ruaccent-env virtualenv (see README.md):
  ~/bedtime-audiobooks/ruaccent-env/bin/python ~/bedtime-audiobooks/add_stress.py story.txt story.stressed.txt

RUAccent is a model. Read its result before you render. It can be wrong on a homograph (замок, плачу).
"""
import argparse
import json
import re
import sys
from pathlib import Path

VOWELS = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")
WORD = re.compile(r"[А-Яа-яЁё+]+")
HERE = Path(__file__).resolve().parent
DEFAULT_DICTIONARY = HERE / "config/russian-stress-corrections.json"


def reconcile(source: str, marked: str):
    """The marked line in the spelling of the source. None when the letters differ beyond ё and е."""
    out, j = [], 0
    for ch in marked:
        if ch == "+":
            out.append(ch)
            continue
        if j >= len(source):
            return None
        s = source[j]
        j += 1
        if ch == s:
            out.append(ch)
        elif ch in "ёЁ" and s in "еЕ":
            out.append(s if out and out[-1] == "+" else "+" + s)  # RUAccent stressed this vowel
        else:
            return None
    return "".join(out) if j == len(source) else None


def accent(accentizer, line: str) -> str:
    """Mark one line. RUAccent fails on some single words with a missing ONNX input, so fall back to
    one call per word and keep the working marks. A word that still fails stays unmarked."""
    try:
        return accentizer.process_all(line)
    except Exception:
        pieces = []
        for token in line.split(" "):
            try:
                pieces.append(accentizer.process_all(token))
            except Exception:
                pieces.append(token)
        return " ".join(pieces)


def tidy(line: str, keep_monosyllables: bool) -> str:
    def fix(match):
        word = match.group(0)
        if not keep_monosyllables and sum(c in VOWELS for c in word) < 2:
            word = word.replace("+", "")
        return re.sub(r"\+(?=[ёЁ])", "", word)
    return WORD.sub(fix, line)


def main():
    ap = argparse.ArgumentParser(description="Mark Russian word stress with RUAccent.")
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--dictionary", default=None,
                    help="extra JSON word map; entries override config/russian-stress-corrections.json")
    ap.add_argument("--model", default="turbo3.1", help="RUAccent homograph model")
    ap.add_argument("--keep-monosyllables", action="store_true", help="keep marks on one-vowel words")
    args = ap.parse_args()

    from ruaccent import RUAccent
    custom = json.loads(DEFAULT_DICTIONARY.read_text(encoding="utf-8"))
    if args.dictionary:
        custom.update(json.loads(Path(args.dictionary).read_text(encoding="utf-8")))
    accentizer = RUAccent()
    accentizer.load(omograph_model_size=args.model, use_dictionary=True, custom_dict=custom, device="CPU")

    lines_out, kept, unmarked = [], 0, 0
    for n, line in enumerate(Path(args.src).read_text(encoding="utf-8").splitlines(), 1):
        source = line.strip()
        if not source or "+" in source:
            lines_out.append(line)
            kept += bool(source)
            continue
        result = reconcile(source, accent(accentizer, source).strip())
        if result is None:
            print(f"line {n}: RUAccent changed the letters, left unmarked: {source}", file=sys.stderr)
            lines_out.append(line)
            unmarked += 1
            continue
        lines_out.append(tidy(result, args.keep_monosyllables))
    Path(args.dst).write_text("\n".join(lines_out) + "\n", encoding="utf-8")
    text = "\n".join(lines_out)
    print(f"{sum(1 for v in lines_out if v.strip())} lines, {text.count('+')} stress marks, "
          f"{kept} hand-marked lines kept, {unmarked} lines left unmarked -> {args.dst}")


if __name__ == "__main__":
    main()
