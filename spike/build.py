"""Build books: page images, one PDF per book, a contact sheet per book.

usage: build.py [--text] [N ...]
  Build the named books, or every book that has all its pictures and stickers. --text builds the
  named books anyway. A missing picture becomes a code-drawn panel. A PDF goes to renders/ as
  "NN Title.pdf". The page images and a contact sheet go to renders/bookN/. renders/ is ignored by git:
  rebuild it any time from the art and the code. Two builds of one book give identical page images. The
  PDF differs only in its random document ID.
"""
import pathlib
import re
import sys

import img2pdf
from PIL import Image

import library
import render as R
import wordcard

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "renders"


def contact(pages: list[Image.Image], path: pathlib.Path, cols: int = 4, tw: int = 405, th: int = 540) -> None:
    rows = (len(pages) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 12) + 12), (190, 190, 190))
    for k, im in enumerate(pages):
        sheet.paste(im.resize((tw, th), Image.Resampling.LANCZOS), (12 + (k % cols) * (tw + 12), 12 + (k // cols) * (th + 12)))
    sheet.save(path)


def pdf_name(n: int, english_title: str) -> str:
    return f"{n:02d} {re.sub(r'[?!,.:]', '', english_title).replace('  ', ' ').strip()}.pdf"


def build(n: int, text_only: bool = False) -> list[str]:
    """Build book n. Returns what is missing (nothing was built), or an empty list."""
    compiled = library.compiled(n)
    book = wordcard.Book(n, compiled)
    gone = book.missing()
    if gone and not text_only:
        return gone
    pages = wordcard.WordCard(book).all_pages()
    folder = OUT / f"book{n}"
    folder.mkdir(parents=True, exist_ok=True)
    paths = []
    for k, im in enumerate(pages):
        assert im.size == (R.W, R.H), f"book {n} page {k} is {im.size}, not {(R.W, R.H)}"
        p = folder / f"{k:02d}.png"
        im.save(p, optimize=True)
        paths.append(str(p))
    title = f"{compiled['cover']['en']} / {compiled['cover']['ru']}"
    pdf = OUT / pdf_name(n, compiled["cover"]["en"])
    pdf.write_bytes(img2pdf.convert(paths, layout_fun=img2pdf.get_fixed_dpi_layout_fun((R.PPI, R.PPI)),
                                    title=title, nodate=True))
    contact(pages, folder / "contact.png")
    print(f"book {n:2d}  {len(pages)} pages  {pdf.stat().st_size / 1e6:5.1f} MB  {pdf.name}")
    return []


if __name__ == "__main__":
    args = sys.argv[1:]
    text_only = "--text" in args
    named = [int(a) for a in args if a != "--text"]
    if text_only and not named:
        raise SystemExit("usage: build.py --text N [N ...]")
    OUT.mkdir(exist_ok=True)
    skipped = {}
    for n in named or library.numbers():
        gone = build(n, text_only=text_only)
        if gone:
            skipped[n] = gone
    for n, gone in skipped.items():
        print(f"book {n:2d}  NOT BUILT, missing: {', '.join(gone)}")
    if named and skipped:
        raise SystemExit(1)
