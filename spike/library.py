"""The library: which books exist and their compiled text.

usage: library.py [N ...] [--digest]
  Print the English and Russian text of the books (all books by default), or with --digest the
  SHA-256 digest of each compiled book. The digest is the proof that the compiler is deterministic.
"""
import pathlib
import re
import sys

import bilingual as b
import books

HERE = pathlib.Path(__file__).parent


def numbers() -> list[int]:
    """Numbers of all books that have a story module."""
    found = (re.fullmatch(r"book(\d+)\.py", p.name) for p in (HERE / "books").iterdir())
    return sorted(int(m.group(1)) for m in found if m)


def compiled(n: int) -> dict:
    return b.compile_story(books.story(n).STORY)


if __name__ == "__main__":
    args = sys.argv[1:]
    wanted = [int(a) for a in args if a.isdigit()] or numbers()
    for n in wanted:
        book = compiled(n)
        if "--digest" in args:
            print(n, b.digest(book))
            continue
        print(f"== Book {n}: {book['cover']['en']} | {book['cover']['ru']}")
        for i, pg in enumerate(book["pages"], 1):
            print(f"p{i:02d}  {pg['en']:<40} | {pg['ru']}")
