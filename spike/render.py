"""Page primitives for the reMarkable Paper Pro.

One page size for every page of every design. Shapes and text are drawn at 2x and reduced once at
the end, so curves are anti-aliased. Bilingual text has English above Russian, with matched words
shown as colour pills. The colour of a pill comes from the compiler (one colour per concept).
"""
from __future__ import annotations

import functools
import pathlib

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

from bilingual import PALETTE

HERE = pathlib.Path(__file__).parent
FONT_R = str(HERE / "fonts/Andika-Regular.ttf")
FONT_B = str(HERE / "fonts/Andika-Bold.ttf")

W, H = 1620, 2160  # THE page size: Paper Pro 11.8 in, 2160x1620 native, portrait 3:4
PPI = 229
S = 2  # supersampling factor

NAVY = (14, 30, 72)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Pill fill and text colour. The tints are estimates for Gallery 3 (not measured on the device).
STORY_INK = {
    "red": ((255, 150, 150), BLACK), "blue": ((150, 190, 255), BLACK),
    "green": ((150, 222, 150), BLACK), "yellow": ((255, 226, 110), BLACK),
}
# Page furniture (the "3 out of 10" counter) uses neutral tints, so it never looks like story words.
CHROME_INK = {"n": ((206, 192, 240), BLACK), "of": ((214, 214, 214), BLACK), "total": ((232, 212, 170), BLACK)}
LANG_GAP = 0.2  # extra space between the English and the Russian line, in line pitches
UP, DOWN = 0.86, 0.26  # Andika glyph extent above and below the baseline in em (measured: 0.80 / 0.24)


# ------------------------------------------------------------------------------- fonts and metrics
@functools.lru_cache(maxsize=None)
def font(size: float, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_B if bold else FONT_R, round(size * S))


def text_width(s: str, size: float, bold: bool = False) -> float:
    return font(size, bold).getlength(s) / S


def pill_h(size: float) -> float:
    """Height of a highlight pill: the glyph extent plus the padding."""
    return (UP + DOWN) * size + pad_for(size)


def pad_for(size: float) -> float:
    return max(5, size // 6)


def line_pitch(size: float) -> float:
    return pill_h(size) + max(8, size * 0.10)


def colors_of(page: dict) -> dict:
    """pair id -> ink key. Story pairs hold a palette index, chrome pairs hold their own key."""
    return {p["id"]: (PALETTE[p["color"]] if isinstance(p["color"], int) else p["color"]) for p in page["pairs"]}


def line_width(segs: list, size: float, bold: bool = False) -> float:
    sp = text_width(" ", size, bold)
    return sum(text_width(s["t"], size, bold) + (sp if s["sp"] and i else 0) for i, s in enumerate(segs))


def wrap(segs: list, size: float, max_w: float, bold: bool = False) -> list[list]:
    """Greedy line breaking at word gaps. Punctuation stays with the word before it, so the break
    check looks ahead through glued segments: a word that fits only without its punctuation does
    not fit. (The old check missed the glued tail, so `fits` refused some good sizes at random.)"""
    lines: list[list] = []
    cur: list = []
    for i, s in enumerate(segs):
        if cur and s["sp"]:
            tail = [s]
            j = i + 1
            while j < len(segs) and not segs[j]["sp"]:
                tail.append(segs[j])
                j += 1
            if line_width(cur + tail, size, bold) > max_w:
                lines.append(cur)
                cur = []
        cur.append(s)
    if cur:
        lines.append(cur)
    return lines


def block_height(n_en: int, n_ru: int, size: float) -> float:
    p = line_pitch(size)
    return (n_en + n_ru) * p + (p * LANG_GAP if n_en and n_ru else 0)


def lines_of(pg: dict, size: float, avail: float, bold: bool = False) -> tuple[list, list]:
    """The English and Russian lines of a page. Verse keeps its own lines, prose is rewrapped."""
    if pg.get("en_lines"):
        return pg["en_lines"], pg["ru_lines"]
    return wrap(pg["en_segs"], size, avail, bold), wrap(pg["ru_segs"], size, avail, bold)


def fits(pages: list, size: float, box_w: float, box_h: float, bold: bool = False) -> bool:
    avail = box_w - 2 * pad_for(size)
    for pg in pages:
        en, ru = lines_of(pg, size, avail, bold)
        if any(line_width(ln, size, bold) > avail + 0.5 for ln in en + ru):
            return False
        if block_height(len(en), len(ru), size) > box_h:
            return False
    return True


def fit_size(pages: list, box_w: float, box_h: float, hi: int = 100, lo: int = 44, bold: bool = False) -> int:
    """The largest even size at which every page fits the box. One size for the whole book."""
    for size in range(hi, lo - 1, -2):
        if fits(pages, size, box_w, box_h, bold):
            return size
    raise ValueError(f"the text does not fit a {box_w}x{box_h} px box even at {lo} px")


# ------------------------------------------------------------------------------------------ canvas
class Canvas:
    """A page at 2x. Coordinates are page pixels (1620 x 2160). `done()` returns the final page."""

    def __init__(self, bg=WHITE):
        self.im = Image.new("RGB", (W * S, H * S), bg)
        self.d = ImageDraw.Draw(self.im)

    @staticmethod
    def _b(box) -> list[int]:
        return [round(v * S) for v in box]

    def rect(self, box, fill) -> None:
        self.d.rectangle(self._b(box), fill=fill)

    def rrect(self, box, r, fill=None, outline=None, width=0) -> None:
        self.d.rounded_rectangle(self._b(box), radius=round(r * S), fill=fill, outline=outline, width=round(width * S))

    def ellipse(self, box, fill=None, outline=None, width=0) -> None:
        self.d.ellipse(self._b(box), fill=fill, outline=outline, width=round(width * S))

    def line(self, a, b, fill, width) -> None:
        self.d.line((a[0] * S, a[1] * S, b[0] * S, b[1] * S), fill=fill, width=round(width * S))

    def text(self, xy, s: str, size: float, fill, bold: bool = False) -> None:
        self.d.text((xy[0] * S, xy[1] * S), s, font=font(size, bold), fill=fill, anchor="ls")

    def _paste(self, im: Image.Image, box, radius: float) -> None:
        x0, y0 = round(box[0] * S), round(box[1] * S)
        mask = None
        if radius:
            mask = Image.new("L", im.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=round(radius * S), fill=255)
        self.im.paste(im, (x0, y0), mask)

    def fit(self, img: Image.Image, box, radius: float = 0) -> None:
        """Contain the art in the box, extending plain edges (flat art on a plain background)."""
        w, h = round((box[2] - box[0]) * S), round((box[3] - box[1]) * S)
        self._paste(fit_art(img, w, h), box, radius)

    def sticker(self, rgba: Image.Image, box) -> None:
        """Scale an RGBA sticker to fit inside the box, centred."""
        bw, bh = (box[2] - box[0]) * S, (box[3] - box[1]) * S
        s = min(bw / rgba.width, bh / rgba.height)
        im = rgba.resize((round(rgba.width * s), round(rgba.height * s)), Image.Resampling.LANCZOS)
        x = round(box[0] * S + (bw - im.width) / 2)
        y = round(box[1] * S + (bh - im.height) / 2)
        self.im.paste(im, (x, y), im)

    def done(self) -> Image.Image:
        return self.im.resize((W, H), Image.Resampling.LANCZOS)


# ------------------------------------------------------------------------------------------- text
def draw_line(cv: Canvas, segs: list, colors: dict, ink: dict, x0: float, base: float, size: float,
              bold: bool = False) -> None:
    sp = text_width(" ", size, bold)
    up, down = UP * size, DOWN * size
    pad = pad_for(size)
    x, placed = x0, []
    for i, s in enumerate(segs):
        if i and s["sp"]:
            x += sp
        w = text_width(s["t"], size, bold)
        placed.append((s, x, w))
        x += w
    groups: list[list] = []  # neighbouring words of one pair share one pill. Punctuation joins the word before it.
    for s, sx, w in placed:
        if s["pair"] is None:
            if groups and not s["sp"] and abs(groups[-1][2] - sx) < 0.5:
                groups[-1][2] = sx + w
            continue
        if groups and groups[-1][0] == s["pair"] and abs(groups[-1][2] + sp - sx) < 1.5:
            groups[-1][2] = sx + w
        else:
            groups.append([s["pair"], sx, sx + w])
    text_col: dict[int, tuple] = {}
    for pid, gx0, gx1 in groups:
        fill, tcol = ink[colors[pid]]
        cv.rrect([gx0 - pad, base - up - pad / 2, gx1 + pad, base + down + pad / 2], max(6, pill_h(size) / 4), fill=fill)
        for s, _, _ in placed:
            if s["pair"] == pid:
                text_col[id(s)] = tcol
    for s, sx, _ in placed:
        cv.text((sx, base), s["t"], size, text_col.get(id(s), BLACK), bold)


def draw_block(cv: Canvas, page: dict, colors: dict, ink: dict, box, size: float, align: str = "left",
               valign: str = "middle", bold: bool = False) -> None:
    """English lines, then Russian lines, inside the box."""
    x0, y0, x1, y1 = box
    pad = pad_for(size)
    avail = (x1 - x0) - 2 * pad
    en, ru = lines_of(page, size, avail, bold)
    pitch = line_pitch(size)
    total = block_height(len(en), len(ru), size)
    y = y0 + (y1 - y0 - total) / 2 if valign == "middle" else y0
    for lines in (en, ru):
        for ln in lines:
            w = line_width(ln, size, bold)
            x = x0 + pad if align == "left" else x0 + (x1 - x0 - w) / 2
            draw_line(cv, ln, colors, ink, x, y + pad / 2 + UP * size, size, bold)
            y += pitch
        y += pitch * LANG_GAP


def draw_dots(cv: Canvas, n: int, total: int, x_right: float, y_mid: float, r: float = 15, gap: float = 14) -> None:
    """One dot per page. Dots up to this page are filled."""
    step = 2 * r + gap
    x = x_right - (total * step - gap)
    for i in range(total):
        box = [x + i * step, y_mid - r, x + i * step + 2 * r, y_mid + r]
        if i < n:
            cv.ellipse(box, fill=NAVY)
        else:
            cv.ellipse(box, fill=WHITE, outline=NAVY, width=4)


# --------------------------------------------------------------------------------------------- art
def fit_art(img: Image.Image, w: int, h: int) -> Image.Image:
    """Contain the art in w x h and extend the leftover axis by replicating the edge pixels.
    Works for flat art on a plain background. Edges are averaged over 4 px so noise never
    turns into streaks."""
    rs = Image.Resampling
    img = img.convert("RGB")
    s = min(w / img.width, h / img.height)
    nw, nh = round(img.width * s), round(img.height * s)
    r = img.resize((nw, nh), rs.LANCZOS)
    cv = Image.new("RGB", (w, h))
    ox, oy = (w - nw) // 2, (h - nh) // 2
    cv.paste(r, (ox, oy))
    if ox > 0:
        left = r.crop((0, 0, 4, nh)).resize((1, nh), rs.BOX).resize((ox, nh), rs.NEAREST)
        right = r.crop((nw - 4, 0, nw, nh)).resize((1, nh), rs.BOX).resize((w - ox - nw, nh), rs.NEAREST)
        cv.paste(left, (0, oy))
        cv.paste(right, (ox + nw, oy))
    if oy > 0:
        top = cv.crop((0, oy, w, oy + 4)).resize((w, 1), rs.BOX).resize((w, oy), rs.NEAREST)
        bot = cv.crop((0, oy + nh - 4, w, oy + nh)).resize((w, 1), rs.BOX).resize((w, h - oy - nh), rs.NEAREST)
        cv.paste(top, (0, 0))
        cv.paste(bot, (0, oy + nh))
    return cv


def bg_alpha(img: Image.Image, tol: int = 24, ring: int = 2) -> tuple[np.ndarray, np.ndarray]:
    """Split an icon from its plain background. Returns (alpha 0..1, colour).

    Alpha is 0 on background, 1 on the artwork. Only background that touches the border counts, so the
    white of an eye stays white. A thin ring of anti-aliased pixels next to the background gets partial
    alpha and the outline colour, so a new background leaves no light halo."""
    a = np.asarray(img.convert("RGB")).astype(np.int16)
    corners = np.concatenate([a[:6, :6].reshape(-1, 3), a[:6, -6:].reshape(-1, 3),
                              a[-6:, :6].reshape(-1, 3), a[-6:, -6:].reshape(-1, 3)])
    ref = np.median(corners, axis=0)
    near = np.abs(a - ref).max(axis=2) <= tol
    lab = ndimage.label(near)[0]  # type: ignore[index]
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, border[border > 0])
    edge = ndimage.binary_dilation(bg, iterations=ring) & ~bg
    alpha = np.where(bg, 0.0, 1.0)
    dist = np.linalg.norm(a - ref, axis=2)
    alpha[edge] = np.clip(dist[edge] / np.linalg.norm(np.array(NAVY) - ref), 0, 1)
    colour = a.astype(np.float64)
    colour[edge] = NAVY
    return alpha, colour
