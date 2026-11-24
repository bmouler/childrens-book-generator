"""The Word-card page: the one page design of the books.

Every page is 1620 x 2160 px (render.W x render.H), portrait 3:4, the Paper Pro screen at 229 PPI.
From top to bottom: a square picture, one or two cards for the key words of the page (a sticker and
the word in English above Russian), the sentence in English above Russian, then the page counter
("3 out of 10" / "3 из 10") and one dot per page. Matching words share a colour pill.
Question pages show the answers as two cards: the child points at a guess.
"""
from __future__ import annotations

import pathlib

from PIL import Image

import render as R
import stickers
from lexicon import NAMES, NOUNS
from bilingual import card_text, compile_counter
from render import BLACK, NAVY, W, WHITE

ART = pathlib.Path(__file__).parent / "out"


def inset(box, dx, dy=None):
    dy = dx if dy is None else dy
    return (box[0] + dx, box[1] + dy, box[2] - dx, box[3] - dy)


def size_of(box):
    return box[2] - box[0], box[3] - box[1]


def card_words(pg: dict) -> list[tuple[str, str]]:
    """The (EN, RU) faces of the key-word cards of a page, in order. Always the citation forms."""
    pairs = {p["id"]: p for p in pg["pairs"]}
    return [card_text(pairs[pid]) for pid in pg.get("focus", ())]


def card_word(nid: str) -> tuple[str, str]:
    """The citation face of one noun or name, for the results chart."""
    return (NOUNS | NAMES)[nid][:2]

class Book:
    """A compiled story plus access to its pictures."""

    def __init__(self, n: int, compiled: dict):
        self.n = n
        self.pages = compiled["pages"]
        self.title = compiled["cover"]
        self.total = len(self.pages)
        self.dir = ART / f"book{n}"

    def art(self, name: str) -> Image.Image:
        return Image.open(self.dir / f"{name}.png").convert("RGB")

    def counter(self, i: int) -> dict:
        return compile_counter(i, self.total)

    def missing(self) -> list[str]:
        """Pictures and stickers that the book needs and the tree does not have."""
        art = [pg["art"] for pg in self.pages if pg.get("art")] + ["cover_flat"]
        gone = [f"book{self.n}/{a}.png" for a in art if not (self.dir / f"{a}.png").exists()]
        concepts = {p["concept"] for pg in self.pages for p in pg["pairs"]
                    if p["id"] in pg.get("focus", ())}
        return gone + [f"sticker {stickers.name_for(c)}" for c in sorted(concepts) if not stickers.exists(c)]


class WordCard:
    key = "wordcard"
    ART_H = 1120
    CHIPS = (54, 1160, 1566, 1468)
    SENT = (54, 1494, 1566, 1916)
    PLAIN = (54, 1160, 1566, 1916)  # a page with no cards (a song, a chain, a dialogue) is all text
    VERSE = (54, 1000, 1566, 1916)  # a verse page takes more of the picture height for its lines
    VERSE_ART_H = 960
    FOOT = (60, 1942, 720, 2118)
    CHIP_W, CHIP_GAP, ICON, PAD = 740, 32, 214, 30
    CSIZE = 44  # counter text size

    def __init__(self, book: Book):
        self.b = book
        self.zone = inset(self.SENT, 26, 10)
        with_cards = [pg for pg in book.pages if pg.get("focus")]
        plain = [pg for pg in book.pages if not pg.get("focus") and not pg.get("verse")]
        sizes = [R.fit_size(with_cards, *size_of(self.zone))] if with_cards else []
        if plain:
            sizes.append(R.fit_size(plain, *size_of(inset(self.PLAIN, 26, 10))))
        verse = [pg for pg in book.pages if pg.get("verse")]
        if verse:
            sizes.append(R.fit_size(verse, *size_of(inset(self.VERSE, 26, 10))))
        self.size = min(sizes)
        self.tsize = R.fit_size([book.title], *size_of(self.zone), hi=150, bold=True)
        words = [w for pg in book.pages for face in card_words(pg) for w in face]
        room = self.CHIP_W - 3 * self.PAD - self.ICON
        self.csize = 62 if not words else next(
            s for s in range(96, 40, -2) if max(R.text_width(w, s) for w in words) + 2 * R.pad_for(s) <= room)

    def all_pages(self) -> list[Image.Image]:
        return [self.cover()] + [self.story(i) for i in range(1, self.b.total + 1)]

    def text(self, cv, page, box, size, **kw):
        R.draw_block(cv, page, R.colors_of(page), R.STORY_INK, box, size, **kw)

    def counter(self, cv, i, box):
        c = self.b.counter(i)
        R.draw_block(cv, c, R.colors_of(c), R.CHROME_INK, box, self.CSIZE, valign="middle")

    def _art(self, cv, name, height=None):
        h = self.ART_H if height is None else height
        cv.fit(self.b.art(name), (0, 0, W, h))
        cv.rect((0, h, W, h + 8), BLACK)

    def _chips(self, cv, pg):
        ids = pg["focus"]
        if len(ids) > 2:
            raise ValueError(f"a page has room for two key words, not {len(ids)}: {pg['en']!r}")
        pairs = {p["id"]: p for p in pg["pairs"]}
        x = (W - (len(ids) * self.CHIP_W + (len(ids) - 1) * self.CHIP_GAP)) / 2
        y0, y1 = self.CHIPS[1], self.CHIPS[3]
        for pid, (en_t, ru_t) in zip(ids, card_words(pg)):
            p = pairs[pid]
            box = (x, y0, x + self.CHIP_W, y1)
            cv.rrect(box, 44, fill=WHITE, outline=NAVY, width=8)
            cv.sticker(stickers.load(p["concept"]), (x + self.PAD, y0 + 30, x + self.PAD + self.ICON, y1 - 30))
            word = {"en_segs": [{"t": en_t, "pair": pid, "sp": False}],
                    "ru_segs": [{"t": ru_t, "pair": pid, "sp": False}], "pairs": [p]}
            self.text(cv, word, (x + 2 * self.PAD + self.ICON - 8, y0 + 8, x + self.CHIP_W - 14, y1 - 8), self.csize)
            x += self.CHIP_W + self.CHIP_GAP

    OK, OOPS = (46, 125, 50), (230, 126, 34)  # a tick when the guess held, a cross when it did not

    def _chart(self, cv, rows):
        """The results chart of an experiment book, drawn by code: what we guessed, what we saw.
        Each row is one thing: its sticker, the guessed word, the seen word, and the verdict."""
        cv.rect((0, 0, W, self.ART_H), WHITE)
        cv.rect((0, self.ART_H, W, self.ART_H + 8), BLACK)
        cols = (60, 640, 1110, 1560)
        for x0, x1, (en, ru) in zip(cols[1:], cols[2:], (("We guessed", "Мы угадали"), ("We saw", "Мы увидели"))):
            mid = (x0 + x1) / 2
            cv.text((mid - R.text_width(ru, 54, True) / 2, 36), ru, 54, NAVY, True)
            cv.text((mid - R.text_width(en, 38) / 2, 100), en, 38, NAVY)
        n = len(rows)
        top = 180
        gap = (self.ART_H - 190) / n
        for x in cols[1:]:
            cv.rect((x - 12, top - 14, x - 4, self.ART_H - 6), (225, 225, 225))
        for i, row in enumerate(rows):
            y = top + i * gap
            mid = y + gap / 2
            cv.sticker(stickers.load(row["n"]), (cols[0] + 8, y + 14, cols[0] + 8 + gap - 28, y + gap - 14))
            en, ru = card_word(row["n"])
            cv.text((cols[0] + gap - 16, mid - 46), en, 52, NAVY, True)
            cv.text((cols[0] + gap - 16, mid + 12), ru, 46, NAVY)
            for j, key in enumerate(("guess", "saw")):
                x = cols[1 + j]
                en_w, ru_w = row[key]
                cv.text((x + 70, mid - 46), en_w, 46, NAVY, True)
                cv.text((x + 70, mid + 12), ru_w, 52, NAVY)
            hit = row["guess"][0] == row["saw"][0]
            cx, cy, r = cols[2] + 330, mid, 42
            colour = self.OK if hit else self.OOPS
            cv.ellipse((cx - r, cy - r, cx + r, cy + r), outline=colour, width=10)
            if hit:
                for a, b in (((cx - 18, cy), (cx - 5, cy + 15)), ((cx - 5, cy + 15), (cx + 20, cy - 16))):
                    cv.line(a, b, colour, 12)
            else:
                for a, b in (((cx - 15, cy - 15), (cx + 15, cy + 15)),
                             ((cx - 15, cy + 15), (cx + 15, cy - 15))):
                    cv.line(a, b, colour, 12)

    def story(self, i):
        cv, pg = R.Canvas(), self.b.pages[i - 1]
        if pg.get("chart"):
            self._chart(cv, pg["chart"])
        else:
            self._art(cv, pg["art"], self.VERSE_ART_H if pg.get("verse") else None)
            if pg.get("focus"):
                self._chips(cv, pg)
                self.text(cv, pg, self.zone, self.size)
            elif pg.get("verse"):  # a verse page: no cards, its own lines, centered
                self.text(cv, pg, inset(self.VERSE, 26, 10), self.size, align="center")
            else:  # a recitation page: no cards, the text gets the card zone too
                self.text(cv, pg, inset(self.PLAIN, 26, 10), self.size, valign="middle")
        self.counter(cv, i, self.FOOT)
        R.draw_dots(cv, i, self.b.total, 1560, (self.FOOT[1] + self.FOOT[3]) / 2)
        return cv.done()

    def cover(self):
        cv = R.Canvas()
        self._art(cv, "cover_flat")
        self.text(cv, self.b.title, (54, self.CHIPS[1], 1566, self.SENT[3]), self.tsize, align="center", bold=True)
        return cv.done()
