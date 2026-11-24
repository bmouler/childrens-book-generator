#!/usr/bin/env python3
"""Print the stressed forms of a Russian word from the Russian Wiktionary, to settle a disputed stress mark.

usage: wiktionary_forms.py WORD [WORD ...] [--tables N]

Two stress engines can disagree, and a hand mark can be wrong. A dictionary settles it. Wiktionary's
declension and conjugation tables mark the stress with an acute accent. This script fetches the
rendered page of each LEMMA (not an inflected form: ask for `пруд`, not `прудом`) and prints the
first tables that carry a stress mark. Several tables mean the word has several senses. Read the
senses on the page before you choose. Two accents on one form mean both stresses are allowed.

On 5 Nov 2026 this found: пора́, прудо́м, далеко́, заходи́те, спе́ла in finished stories, and showed
that three hand choices for the new stories were wrong (у́шко, бо́ку, сжа́ла).

The site answers HTTP 429 when asked too fast, so the script waits between words and retries.
It needs the network and nothing but the standard library. Nothing leaves the machine but the word.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

API = "https://ru.wiktionary.org/w/api.php"
AGENT = "childrens-book-generator stress check (private, family use)"
ACUTE = "\u0301"
PAUSE_S = 2.5


class TableReader(HTMLParser):
    """The text of every outermost table, one string per row, cells joined by a space."""

    def __init__(self) -> None:
        super().__init__()
        self.tables: list[list[str]] = []
        self._rows: list[str] | None = None
        self._cells: list[str] = []
        self._cell: list[str] | None = None
        self._depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "table":
            self._depth += 1
            if self._depth == 1:
                self._rows, self._cells = [], []
        elif tag in ("td", "th") and self._depth == 1:
            self._cell = []
        elif tag == "br" and self._cell is not None:
            self._cell.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th") and self._depth == 1 and self._cell is not None:
            self._cells.append(re.sub(r"\s+", " ", "".join(self._cell)).strip())
            self._cell = None
        elif tag == "tr" and self._depth == 1 and self._rows is not None and self._cells:
            self._rows.append(" ".join(cell for cell in self._cells if cell))
            self._cells = []
        elif tag == "table":
            if self._depth == 1 and self._rows is not None:
                self.tables.append(self._rows)
                self._rows = None
            self._depth = max(0, self._depth - 1)

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)


def stressed_tables(html: str) -> list[list[str]]:
    """The tables whose text holds at least one acute accent: declension and conjugation tables."""
    reader = TableReader()
    reader.feed(html)
    return [rows for rows in reader.tables if any(ACUTE in row for row in rows)]


def fetch(word: str, attempts: int = 6) -> str:
    query = urllib.parse.urlencode({"action": "parse", "page": word, "prop": "text", "format": "json",
                                    "formatversion": "2", "redirects": "1"})
    request = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": AGENT})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=30) as answer:
                return json.load(answer)["parse"]["text"]
        except urllib.error.HTTPError as err:
            if err.code != 429 or attempt == attempts - 1:
                raise
            time.sleep(4 * (attempt + 1))
    raise RuntimeError("unreachable")


def main() -> None:
    ap = argparse.ArgumentParser(description="Print the stressed forms of Russian words from Wiktionary.")
    ap.add_argument("words", nargs="+", help="lemmas: the dictionary form of each word")
    ap.add_argument("--tables", type=int, default=1, help="how many stressed tables to print per word")
    args = ap.parse_args()
    for index, word in enumerate(args.words):
        if index:
            time.sleep(PAUSE_S)
        try:
            tables = stressed_tables(fetch(word))
        except (urllib.error.URLError, KeyError) as err:
            print(f"== {word}: {type(err).__name__} {err}")
            continue
        print(f"== {word}: {len(tables)} stressed tables")
        for rows in tables[:args.tables]:
            for row in rows:
                print("   " + row)
    sys.exit(0)


if __name__ == "__main__":
    main()
