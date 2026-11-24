"""Structural checks of every book. Exit code 0 only when every check passes.

For each book: the story compiles, every page has one or two key words, the art module names the same
pictures as the story, the text fits the page at a readable size, and the compiled text has the same
digest in three separate processes. Then the pictures and stickers: a missing one is listed. With --art
a missing picture or sticker is also a failure.

usage: check_books.py [--art]
"""
import pathlib
import subprocess
import sys

import bilingual as b
import books
import library
import wordcard

HERE = pathlib.Path(__file__).parent
MIN_TEXT, MIN_CARD = 76, 56  # px at 229 PPI: 24 pt body text, 18 pt card text


def digests(n: int, runs: int = 3) -> set[str]:
    out = set()
    for _ in range(runs):
        r = subprocess.run([sys.executable, "library.py", str(n), "--digest"], cwd=HERE, capture_output=True, text=True)
        out.add(r.stdout.split()[-1] if r.returncode == 0 and r.stdout.split() else f"failed: {r.stderr.strip()[-200:]}")
    return out


def check(n: int) -> tuple[list[str], list[str], str]:
    """(failures, missing art and stickers, one summary line) for book n."""
    fails: list[str] = []
    try:
        compiled = library.compiled(n)
    except b.LexiconError as e:
        return [f"does not compile: {e}"], [], f"book {n:2d}  DOES NOT COMPILE"
    pages = compiled["pages"]
    cite = {c: (v[0], v[1]) for table in (b.NOUNS, b.NAMES, b.ADJS) for c, v in table.items()}
    for i, pg in enumerate(pages, 1):
        if len(pg.get("focus", [])) > 2:
            fails.append(f"page {i} has {len(pg.get('focus', []))} key words; "
                         "a page has room for two, or none on a recitation page")
        if pg.get("verse") and not pg.get("focus"):
            continue
        for (en_t, ru_t), pid in zip(wordcard.card_words(pg), pg.get("focus", [])):
            concept = next(x["concept"] for x in pg["pairs"] if x["id"] == pid)
            if concept in cite and (en_t, ru_t) != cite[concept]:
                fails.append(f"page {i}: the card for {concept!r} shows {en_t!r} / {ru_t!r}, "
                             f"not the dictionary form {cite[concept][0]!r} / {cite[concept][1]!r}")
    story_art = {pg["art"] for pg in pages if pg.get("art")}  # a chart page has no picture
    try:
        art = books.art(n)
        prompts = set(art.PAGES)
        if prompts != story_art:
            fails.append(f"art prompts and story differ: only in story {sorted(story_art - prompts)}, "
                         f"only in prompts {sorted(prompts - story_art)}")
        if not getattr(art, "COVER", ""):
            fails.append("the art module has no COVER prompt")
    except ModuleNotFoundError:
        fails.append("no art module")
    book = wordcard.Book(n, compiled)
    card = wordcard.WordCard(book)
    if card.size < MIN_TEXT:
        fails.append(f"body text is {card.size} px, under {MIN_TEXT}")
    if card.csize < MIN_CARD and any(pg.get("focus") for pg in pages):
        fails.append(f"card text is {card.csize} px, under {MIN_CARD}")
    for i, pg in enumerate(pages + [compiled["cover"]], 1):
        for pair in b._adjacent_concepts(pg):
            x, y = sorted(pair)
            if compiled["colors"][x] == compiled["colors"][y]:
                fails.append(f"{'cover' if i > len(pages) else f'page {i}'}: the words {x!r} and {y!r} sit side by side "
                             f"with one pill colour")
    seen = digests(n)
    if len(seen) != 1 or next(iter(seen)).startswith("failed"):
        fails.append(f"the compiled text is not the same in three processes: {seen}")
    gone = book.missing()
    line = (f"book {n:2d}  {compiled['cover']['en'][:28]:<28} {len(pages)} pages  text {card.size} px  "
            f"cards {card.csize} px  digest {next(iter(seen))[:8]}  "
            f"{'OK' if not fails else 'FAIL'}{'' if not gone else f'  ({len(gone)} pictures or stickers missing)'}")
    return fails, gone, line


if __name__ == "__main__":
    need_art = "--art" in sys.argv
    bad = 0
    for n in library.numbers():
        fails, gone, line = check(n)
        print(line)
        for f in fails:
            print(f"    FAIL {f}")
        bad += bool(fails) or (need_art and bool(gone))
    if bad:
        raise SystemExit(f"{bad} book(s) failed")
    print("all checks passed")
