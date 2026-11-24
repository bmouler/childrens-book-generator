"""Sticker icons drawn by code: flat colours, thick navy outlines, a transparent background.

The same code gives the same pixels, and drawing costs nothing. An icon is a function that draws on a
512 x 512 canvas. Drawing is at 4x and reduced once, so the edges are anti-aliased. Each icon is cropped
to its content, like an icon cut from a generated sheet.

usage: icons.py [name ...]      draw the named icons (default: all) into out/stickers/<name>.png
       icons.py --sheet         also write a contact sheet to renders/icons.png
"""
from __future__ import annotations

import math
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import render as R
from stickers import LIB

N, SS, OW = 512, 4, 12  # canvas, supersampling, outline width (canvas units)
NAVY = R.NAVY
WHITE = (255, 255, 255)
RED = (237, 52, 56)
ORANGE = (255, 150, 40)
YELLOW = (255, 208, 52)
GREEN = (74, 178, 96)
DGREEN = (40, 128, 66)
BLUE = (46, 142, 236)
LBLUE = (170, 214, 250)
ICE = (190, 226, 250)
GRAY = (176, 178, 184)
DGRAY = (110, 114, 124)
BROWN = (150, 98, 58)
WOOD = (226, 184, 128)
TAN = (240, 208, 156)
SKIN = (255, 198, 152)
PINK = (250, 150, 160)
STEAM = (150, 176, 208)


class Pen:
    def __init__(self):
        self.im = Image.new("RGBA", (N * SS, N * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    @staticmethod
    def _s(pts):
        return [(x * SS, y * SS) for x, y in pts]

    def fill(self, pts, color):
        self.d.polygon(self._s(pts), fill=color)

    def stroke(self, pts, w=OW, color=NAVY, closed=False):
        P = self._s(list(pts) + ([pts[0]] if closed else []))
        self.d.line(P, fill=color, width=round(w * SS), joint="curve")
        r = w * SS / 2
        for x, y in (P[:-1] if closed else P):  # round joins and caps
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=color)

    def shape(self, pts, color, w=OW):
        """A filled shape with a navy outline."""
        self.fill(pts, color)
        self.stroke(pts, w, NAVY, closed=True)

    def blob(self, shapes, color):
        """The union of shapes as one silhouette with one outline (no seams inside)."""
        for pts in shapes:
            self.stroke(pts, 2 * OW, NAVY, closed=True)
        for pts in shapes:
            self.fill(pts, color)

    def oline(self, pts, w, color):
        """A thick line with a navy outline and round ends."""
        self.stroke(pts, w + 2 * OW, NAVY)
        self.stroke(pts, w, color)

    def image(self) -> Image.Image:
        im = self.im.resize((N, N), Image.Resampling.LANCZOS)
        a = np.asarray(im)[..., 3]
        ys, xs = np.nonzero(a > 8)
        pad = 8
        return im.crop((max(0, xs.min() - pad), max(0, ys.min() - pad),
                        min(N, xs.max() + 1 + pad), min(N, ys.max() + 1 + pad)))


# ---------------------------------------------------------------------------------------- geometry
def ell(cx, cy, rx, ry=None, rot=0.0, n=96):
    ry = rx if ry is None else ry
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out


def rrect(x0, y0, x1, y1, r, n=10):
    out = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def bez(p0, p1, p2, p3, n=28):
    out = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def wave(x, y_from, y_to, amp, cycles, n=48):
    return [(x + amp * math.sin(2 * math.pi * cycles * k / n), y_from + (y_to - y_from) * k / n) for k in range(n + 1)]


def teardrop(cx, cy, r):
    """A drop with its point up. (cx, cy) is the centre of the round part."""
    left = bez((cx, cy - 1.55 * r), (cx - 0.2 * r, cy - 0.85 * r), (cx - r, cy - 0.7 * r), (cx - r, cy))
    arc = [(cx - r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    right = bez((cx + r, cy), (cx + r, cy - 0.7 * r), (cx + 0.2 * r, cy - 0.85 * r), (cx, cy - 1.55 * r))
    return left + arc + right


# ---------------------------------------------------------------------------------------- pieces
def ball(p, cx, cy, r, color=RED):
    p.shape(ell(cx, cy, r), color)
    p.fill(ell(cx - 0.35 * r, cy - 0.38 * r, 0.2 * r, 0.3 * r, rot=35), (255, 255, 255, 110))


def cloud_shapes(cx, cy, k=1.0):
    return [ell(cx - 80 * k, cy + 20 * k, 70 * k), ell(cx, cy - 20 * k, 90 * k), ell(cx + 90 * k, cy + 20 * k, 66 * k),
            rrect(cx - 130 * k, cy + 20 * k, cx + 140 * k, cy + 86 * k, 33 * k)]


def thermo(p, level, color):
    p.shape(rrect(222, 50, 290, 350, 34), WHITE)
    p.shape(ell(256, 402, 66), color)
    p.fill(rrect(232, 330, 280, 400, 10), color)
    p.fill(rrect(240, level, 272, 400, 14), color)
    for y in (100, 150, 200, 250, 300):
        p.stroke([(312, y), (350, y)], 10)


def pot(p, cx=256, top=330):
    p.shape([(cx - 130, top), (cx + 130, top), (cx + 100, 460), (cx - 100, 460)], (214, 110, 60))
    p.shape(rrect(cx - 150, top - 40, cx + 150, top + 20, 18), (230, 130, 74))


def leaf_shape(cx, cy, length, width, rot):
    return ell(cx, cy, length, width, rot=rot)


def table_top(p, y=170):
    p.shape(rrect(60, y, 452, y + 60, 20), WOOD)
    p.shape(rrect(95, y + 55, 140, 440, 10), BROWN)
    p.shape(rrect(372, y + 55, 417, 440, 10), BROWN)


def open_box(p, ball_in=False):
    """A cardboard box seen from the front and a little above, flaps open."""
    p.shape([(100, 215), (150, 150), (362, 150), (412, 215)], (170, 120, 70))  # dark opening
    p.shape([(100, 215), (50, 150), (110, 110), (150, 150)], WOOD)  # left flap
    p.shape([(412, 215), (462, 150), (402, 110), (362, 150)], WOOD)  # right flap
    if ball_in:
        ball(p, 256, 170, 84)
    p.shape(rrect(100, 215, 412, 440, 14), TAN)
    p.stroke([(100, 250), (412, 250)], 8)


# ---------------------------------------------------------------------------------------- icons
def ice(p):
    p.shape([(110, 150), (170, 90), (420, 90), (360, 150)], (226, 243, 254))
    p.shape([(360, 150), (420, 90), (420, 340), (360, 400)], (150, 200, 240))
    p.shape(rrect(110, 150, 360, 400, 26), ICE)
    p.stroke([(145, 195), (145, 255)], 16, WHITE)
    p.stroke([(145, 290), (145, 300)], 16, WHITE)
    p.stroke([(190, 182), (255, 182)], 16, WHITE)


def cold(p):
    thermo(p, 275, BLUE)


def warm(p):
    thermo(p, 190, ORANGE)


def hot(p):
    thermo(p, 100, RED)


def soup(p):
    p.shape(rrect(196, 405, 316, 450, 14), WHITE)
    bowl = [(66, 250)] + [(256 - 190 * math.cos(math.radians(a)), 250 + 172 * math.sin(math.radians(a))) for a in range(0, 181, 6)]
    p.shape(bowl, WHITE)
    p.shape(ell(256, 250, 190, 52), ORANGE)
    for x in (190, 256, 322):
        p.stroke(wave(x, 190, 62, 14, 1.5), 14, STEAM)


def sun(p):
    cx = cy = 256
    for k in range(8):
        a = math.radians(45 * k)
        a1, a2 = a - math.radians(13), a + math.radians(13)
        p.shape([(cx + 132 * math.cos(a1), cy + 132 * math.sin(a1)), (cx + 205 * math.cos(a), cy + 205 * math.sin(a)),
                 (cx + 132 * math.cos(a2), cy + 132 * math.sin(a2))], (255, 170, 30), 10)
    p.shape(ell(cx, cy, 100), YELLOW)


def snow(p):
    cx = cy = 256
    segs = []
    for k in range(6):
        a = math.radians(60 * k - 90)
        d = (math.cos(a), math.sin(a))
        segs.append([(cx, cy), (cx + 190 * d[0], cy + 190 * d[1])])
        for f in (0.5, 0.75):
            bx, by = cx + 190 * f * d[0], cy + 190 * f * d[1]
            for s in (-1, 1):
                b = a + s * math.radians(50)
                segs.append([(bx, by), (bx + 62 * math.cos(b), by + 62 * math.sin(b))])
    for s in segs:
        p.stroke(s, 20 + 2 * OW, NAVY)
    for s in segs:
        p.stroke(s, 20, ICE)


def touch(p):
    p.shape(rrect(150, 300, 392, 475, 70), SKIN)
    for cx, cy, rx, ry in ((310, 307, 32, 44), (348, 317, 29, 40), (382, 335, 25, 36)):
        p.shape(ell(cx, cy, rx, ry), SKIN)
    p.shape(rrect(205, 105, 277, 345, 36), SKIN)
    p.fill(rrect(212, 307, 270, 365, 4), SKIN)
    p.shape(ell(160, 390, 40, 66, rot=-22), SKIN)
    c = (241, 105)
    for a in (-35, 0, 35):  # a touch spark above the fingertip
        r0, r1 = 50, 88
        p.stroke([(c[0] + r0 * math.sin(math.radians(a)), c[1] - r0 * math.cos(math.radians(a))),
                  (c[0] + r1 * math.sin(math.radians(a)), c[1] - r1 * math.cos(math.radians(a)))], 10)


def feather(p):
    left = bez((120, 450), (80, 260), (230, 90), (410, 62))
    right = bez((410, 62), (420, 220), (300, 380), (120, 450))
    p.shape(left + right[1:], (232, 242, 254))
    p.stroke(bez((110, 475), (190, 330), (290, 190), (400, 76)), 10)
    for f in (0.28, 0.46, 0.64, 0.8):
        x = 110 + (400 - 110) * f
        y = 475 + (76 - 475) * f
        p.stroke([(x, y), (x - 60, y - 22)], 7)
        p.stroke([(x, y), (x + 18, y + 60)], 7)


def balloon(p):
    p.stroke(wave(256, 372, 480, 14, 1.2, 30), 8)
    p.shape([(236, 392), (276, 392), (256, 348)], RED, 8)
    p.shape(ell(256, 205, 128, 155), RED)
    p.fill(ell(200, 140, 24, 44, rot=25), (255, 150, 150))


def watermelon(p):
    p.shape(ell(256, 256, 190), GREEN)
    for rx in (40, 100, 150):
        p.stroke(ell(256, 256, rx, 188, n=120)[10:-10], 18, DGREEN)
    p.stroke(ell(256, 256, 190, 190, n=120), OW)
    p.shape(rrect(240, 40, 272, 82, 8), BROWN, 8)


def elephant(p):
    p.shape(rrect(222, 330, 278, 448, 18), DGRAY)
    p.shape(rrect(372, 330, 428, 448, 18), DGRAY)
    p.shape(rrect(172, 330, 230, 452, 18), GRAY)
    p.shape(rrect(330, 330, 388, 452, 18), GRAY)
    p.shape(ell(290, 270, 160, 112), GRAY)
    p.stroke(bez((445, 240), (472, 270), (472, 320), (452, 352)), 10)
    p.oline([(95, 280), (62, 350), (70, 425), (112, 450)], 48, GRAY)
    p.shape(ell(140, 232, 96), GRAY)
    p.shape(ell(196, 245, 60, 84, rot=-8), (206, 208, 216))
    p.fill(ell(118, 205, 11), NAVY)


def mouse(p):
    p.stroke(bez((390, 360), (460, 380), (470, 290), (440, 250)), 11)
    p.shape(ell(275, 345, 125, 86), GRAY)
    p.shape(ell(150, 330, 72, 58), GRAY)
    p.shape(ell(172, 255, 46), GRAY)
    p.fill(ell(172, 255, 26), PINK)
    p.shape(ell(86, 345, 16), PINK, 8)
    p.fill(ell(140, 316, 11), NAVY)
    p.stroke([(100, 360), (40, 345)], 6)
    p.stroke([(100, 372), (44, 385)], 6)


def tree(p):
    p.shape(rrect(224, 290, 290, 455, 10), BROWN)
    p.blob([ell(256, 175, 112), ell(170, 255, 84), ell(342, 255, 84), ell(256, 270, 90)], GREEN)


def flower(p):
    p.oline([(256, 230), (256, 460)], 18, GREEN)
    p.shape(ell(330, 385, 62, 26, rot=-35), GREEN)
    petals = [ell(256 + 84 * math.cos(math.radians(60 * k)), 165 + 84 * math.sin(math.radians(60 * k)), 62) for k in range(6)]
    p.blob(petals, RED)
    p.shape(ell(256, 165, 48), YELLOW)


def pillow(p):
    p.shape(rrect(66, 110, 446, 402, 100), (240, 246, 255))
    for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):  # creases in the corners
        x, y = 256 + sx * 150, 256 + sy * 105
        p.stroke(bez((x, y), (x + sx * 20, y + sy * 8), (x + sx * 36, y + sy * 8), (x + sx * 52, y + sy * 26)), 7)
    p.stroke(bez((170, 245), (210, 225), (300, 225), (342, 245)), 6, (150, 170, 200))  # soft folds
    p.stroke(bez((190, 290), (230, 270), (290, 270), (322, 290)), 6, (150, 170, 200))


def block(p):
    p.shape([(256, 66), (434, 160), (256, 254), (78, 160)], (240, 208, 152))
    p.shape([(78, 160), (256, 254), (256, 452), (78, 358)], (222, 178, 118))
    p.shape([(256, 254), (434, 160), (434, 358), (256, 452)], (196, 150, 96))


def teddy(p):
    p.shape(ell(150, 118, 46), BROWN)
    p.shape(ell(362, 118, 46), BROWN)
    p.fill(ell(150, 118, 24), TAN)
    p.fill(ell(362, 118, 24), TAN)
    p.shape(ell(256, 385, 112, 96), BROWN)
    p.shape(ell(158, 365, 38, 66, rot=-20), BROWN)
    p.shape(ell(354, 365, 38, 66, rot=20), BROWN)
    p.shape(ell(256, 395, 62, 60), TAN, 8)
    p.shape(ell(195, 462, 52, 30), BROWN)
    p.shape(ell(317, 462, 52, 30), BROWN)
    p.shape(ell(256, 195, 112, 104), BROWN)
    p.shape(ell(256, 232, 50, 38), TAN, 9)
    p.fill(ell(256, 216, 19, 13), NAVY)
    p.fill(ell(212, 176, 11), NAVY)
    p.fill(ell(300, 176, 11), NAVY)
    p.stroke(bez((256, 230), (256, 248), (240, 255), (228, 248)), 7)
    p.stroke(bez((256, 230), (256, 248), (272, 255), (284, 248)), 7)


def table(p):
    table_top(p)


def chair(p):
    p.shape(rrect(350, 285, 395, 445, 10), BROWN)
    p.shape(rrect(130, 285, 175, 445, 10), BROWN)
    p.shape(rrect(130, 70, 178, 300, 14), BROWN)
    p.shape(rrect(130, 230, 395, 290, 20), WOOD)


def where(p):
    p.oline([(300, 300), (425, 425)], 50, BROWN)
    p.shape(ell(215, 215, 128), (214, 238, 255))
    p.stroke(bez((135, 190), (150, 150), (185, 125), (225, 118)), 12, WHITE)


def in_(p):
    open_box(p, ball_in=True)


def on(p):
    p.shape(rrect(100, 290, 412, 450, 14), TAN)
    p.shape([(100, 290), (140, 250), (372, 250), (412, 290)], WOOD)
    ball(p, 256, 190, 84)


def under(p):
    p.shape(rrect(70, 80, 442, 140, 20), WOOD)
    p.shape(rrect(100, 135, 145, 440, 10), BROWN)
    p.shape(rrect(367, 135, 412, 440, 10), BROWN)
    ball(p, 256, 355, 72)


def box(p):
    open_box(p)


def _swatch(color):
    def draw(p):
        p.shape(ell(256, 256, 178), color)
        p.fill(ell(190, 190, 34, 52, rot=35), (255, 255, 255, 90))
    return draw


def sea(p):
    p.shape(rrect(50, 120, 462, 400, 50), BLUE)
    for y, x0, x1 in ((205, 100, 300), (285, 190, 410), (355, 100, 280)):
        p.stroke([(x, y + 12 * math.sin((x - x0) / 28)) for x in range(x0, x1 + 1, 6)], 12, WHITE)


def listen(p):
    p.shape(ell(290, 250, 108, 170, rot=6), SKIN)
    p.stroke(bez((255, 345), (215, 290), (225, 175), (300, 170)), 12)
    p.stroke(bez((300, 170), (350, 170), (362, 235), (320, 275)), 12)
    p.shape(ell(318, 300, 20, 28), (240, 170, 130), 9)
    for r in (280, 330, 380):  # sound arriving from the left
        p.stroke([(420 - r * math.cos(math.radians(a)), 250 + r * math.sin(math.radians(a))) for a in range(-20, 21, 4)], 11)


def who(p):
    p.shape([(300, 330), (330, 440), (225, 330)], WHITE)
    p.shape(rrect(60, 80, 452, 340, 70), WHITE)
    p.fill([(236, 332), (322, 332), (312, 346), (242, 346)], WHITE)
    for x in (160, 256, 352):
        p.fill(ell(x, 210, 24), NAVY)


def dog(p):
    p.shape(ell(125, 270, 55, 105, rot=14), BROWN)
    p.shape(ell(387, 270, 55, 105, rot=-14), BROWN)
    p.shape(ell(256, 262, 128, 120), (236, 204, 156))
    p.shape(ell(256, 335, 70, 52), WHITE)
    p.fill(ell(195, 215, 38, 44), BROWN)
    p.fill(ell(210, 245, 13), NAVY)
    p.fill(ell(302, 245, 13), NAVY)
    p.shape(ell(256, 312, 28, 18), NAVY, 8)
    p.shape(rrect(244, 350, 268, 392, 12), PINK, 8)
    p.stroke(bez((256, 330), (256, 352), (236, 362), (220, 354)), 8)
    p.stroke(bez((256, 330), (256, 352), (276, 362), (292, 354)), 8)


def cat(p):
    p.shape([(128, 230), (140, 80), (245, 165)], ORANGE)
    p.shape([(384, 230), (372, 80), (267, 165)], ORANGE)
    p.fill([(152, 190), (158, 125), (205, 163)], PINK)
    p.fill([(360, 190), (354, 125), (307, 163)], PINK)
    p.shape(ell(256, 285, 134, 116), ORANGE)
    for x in (226, 256, 286):
        p.stroke([(x, 185), (x, 215)], 9, (200, 100, 20))
    for x in (200, 312):
        p.shape(ell(x, 272, 24, 30), WHITE, 8)
        p.fill(ell(x, 272, 9, 22), NAVY)
    p.shape([(240, 312), (272, 312), (256, 330)], PINK, 7)
    p.stroke(bez((256, 330), (256, 352), (238, 358), (226, 350)), 7)
    p.stroke(bez((256, 330), (256, 352), (274, 358), (286, 350)), 7)
    for dy in (-12, 8):
        p.stroke([(150, 330 + dy), (60, 320 + dy * 2)], 6)
        p.stroke([(362, 330 + dy), (452, 320 + dy * 2)], 6)


def cow(p):
    p.shape([(165, 150), (120, 70), (205, 110)], (240, 230, 200), 9)
    p.shape([(347, 150), (392, 70), (307, 110)], (240, 230, 200), 9)
    p.shape(ell(100, 210, 58, 28, rot=-18), WHITE)
    p.shape(ell(412, 210, 58, 28, rot=18), WHITE)
    p.shape(ell(256, 245, 114, 135), WHITE)
    p.fill(ell(190, 190, 52, 58), (50, 50, 60))
    p.shape(ell(256, 345, 88, 58), PINK)
    p.fill(ell(228, 350, 11, 15), NAVY)
    p.fill(ell(284, 350, 11, 15), NAVY)
    p.fill(ell(208, 240, 13), NAVY)
    p.fill(ell(304, 240, 13), NAVY)


def duck(p):
    p.shape([(105, 310), (60, 250), (140, 285)], YELLOW)
    p.shape(ell(245, 335, 152, 98), YELLOW)
    p.shape(ell(335, 205, 74), YELLOW)
    p.shape(rrect(385, 195, 462, 238, 20), ORANGE)
    p.fill(ell(350, 188, 11), NAVY)
    p.stroke(bez((170, 330), (210, 275), (285, 285), (305, 345)), 10, (225, 160, 30))
    p.shape(rrect(205, 430, 235, 462, 8), ORANGE, 8)
    p.shape(rrect(275, 430, 305, 462, 8), ORANGE, 8)


def sky(p):
    p.shape(rrect(60, 70, 452, 440, 50), (140, 200, 250))
    p.blob(cloud_shapes(256, 250, 0.8), WHITE)


def cloud(p):
    p.blob(cloud_shapes(256, 250, 1.1), (236, 244, 252))


def rain(p):
    p.blob(cloud_shapes(256, 175, 1.0), (176, 194, 218))
    for x, y in ((150, 345), (256, 385), (362, 345)):
        p.shape(teardrop(x, y, 30), BLUE, 9)


def wind(p):
    p.oline(bez((60, 170), (190, 170), (330, 170), (380, 170))[:] + bez((380, 170), (440, 170), (450, 100), (395, 95))[1:], 16, ICE)
    p.oline(bez((60, 260), (200, 260), (340, 260), (400, 260)) + bez((400, 260), (470, 260), (475, 340), (415, 340))[1:], 16, ICE)
    p.oline(bez((60, 350), (150, 350), (230, 350), (280, 350)) + bez((280, 350), (330, 350), (340, 410), (295, 412))[1:], 16, ICE)


def grass(p):
    for x, lean, h in ((130, -40, 250), (190, -10, 330), (256, 10, 390), (322, 30, 320), (382, 50, 240)):
        blade = bez((x - 22, 452), (x - 16, 452 - h * 0.5), (x + lean * 0.4, 452 - h * 0.8), (x + lean, 452 - h))
        back = bez((x + lean, 452 - h), (x + lean * 0.4 + 12, 452 - h * 0.7), (x + 24, 452 - h * 0.4), (x + 24, 452))
        p.shape(blade + back[1:], GREEN, 10)


def seed(p):
    shape = bez((256, 60), (390, 150), (390, 330), (256, 455)) + bez((256, 455), (122, 330), (122, 150), (256, 60))[1:]
    p.shape(shape, (176, 122, 70))
    for dx in (-40, 0, 40):
        p.stroke(bez((256 + dx * 0.4, 130), (256 + dx * 1.4, 220), (256 + dx * 1.4, 320), (256 + dx * 0.6, 400)), 10, (230, 196, 150))


def soil(p):
    mound = [(60, 420)] + [(256 - 196 * math.cos(math.radians(a)), 420 - 250 * math.sin(math.radians(a))) for a in range(0, 181, 6)]
    p.shape(mound, (110, 72, 44))
    for x, y in ((170, 340), (270, 300), (340, 370), (220, 390)):
        p.fill(ell(x, y, 16, 11), (150, 108, 70))


def wait(p):
    p.shape(ell(150, 80, 48), (255, 190, 60), 9)
    p.shape(ell(362, 80, 48), (255, 190, 60), 9)
    p.shape(ell(256, 285, 175), WHITE)
    p.stroke([(256, 285), (256, 175)], 16)
    p.stroke([(256, 285), (340, 330)], 16)
    for k in range(12):
        a = math.radians(30 * k)
        p.stroke([(256 + 140 * math.sin(a), 285 - 140 * math.cos(a)), (256 + 156 * math.sin(a), 285 - 156 * math.cos(a))], 9)
    p.stroke(ell(256, 285, 175, 175, n=120), OW)


def grow(p):
    soil_mound = [(100, 450)] + [(256 - 156 * math.cos(math.radians(a)), 450 - 90 * math.sin(math.radians(a))) for a in range(0, 181, 8)]
    p.shape(soil_mound, (110, 72, 44))
    p.oline([(256, 380), (256, 250), (250, 190)], 18, GREEN)
    p.shape(ell(180, 200, 80, 38, rot=-30), GREEN)
    p.shape(ell(330, 170, 80, 38, rot=30), GREEN)


def plant(p):
    p.oline([(256, 340), (256, 200)], 16, GREEN)
    p.shape(ell(170, 215, 78, 34, rot=-35), GREEN)
    p.shape(ell(342, 190, 78, 34, rot=35), GREEN)
    p.shape(ell(256, 120, 40, 70, rot=0), GREEN)
    pot(p)


def melt(p):
    p.shape(ell(256, 395, 190, 62), BLUE)
    p.shape(ell(256, 385, 150, 40), (130, 190, 245), 9)
    p.shape([(190, 190), (230, 140), (350, 140), (320, 190)], (226, 243, 254))
    p.shape(rrect(190, 190, 320, 330, 24), ICE)
    p.stroke([(215, 225), (215, 260)], 13, WHITE)
    p.shape(teardrop(372, 285, 24), BLUE, 9)


def egg(p):
    p.shape(ell(256, 272, 140, 172), WHITE)
    p.fill(ell(198, 192, 30, 44, rot=20), (218, 230, 244))


def golden(p):  # the golden egg of Курочка Ряба
    p.shape(ell(256, 272, 140, 172), YELLOW)
    p.fill(ell(198, 192, 30, 44, rot=20), (255, 238, 150))


def speckled(p):  # a speckled egg
    p.shape(ell(256, 272, 140, 172), WHITE)
    for x, y, r in ((198, 205, 18), (298, 245, 22), (218, 330, 16), (312, 350, 14), (255, 278, 12)):
        p.fill(ell(x, y, r), BROWN)


def kolobok(p):  # the bun with his simple face
    p.shape(ell(256, 256, 185), TAN)
    p.fill(ell(150, 285, 22, 14), PINK)
    p.fill(ell(362, 285, 22, 14), PINK)
    p.fill(ell(185, 225, 16), NAVY)
    p.fill(ell(327, 225, 16), NAVY)
    p.stroke(bez((190, 295), (225, 345), (290, 345), (322, 295)), 10)


def round_(p):
    p.shape(ell(256, 256, 175), LBLUE)


def roll(p):  # a rolling bun: motion lines to the left
    for y in (170, 250, 330):
        p.stroke(bez((40, y), (90, y - 14), (130, y + 14), (165, y)), 10, STEAM)
    p.shape(ell(320, 256, 150), TAN)


def happy(p):  # a smiling face
    p.shape(ell(256, 256, 180), YELLOW)
    p.fill(ell(190, 215, 17), NAVY)
    p.fill(ell(322, 215, 17), NAVY)
    p.stroke(bez((170, 300), (220, 375), (292, 375), (342, 300)), 12)


def house(p):  # a little wooden house, as in Теремок
    p.shape([(120, 250), (392, 250), (392, 460), (120, 460)], WOOD)
    p.shape([(85, 255), (256, 90), (427, 255)], (196, 96, 60))
    p.shape(rrect(222, 320, 290, 460, 10), BROWN)
    p.shape(rrect(315, 290, 370, 360, 8), LBLUE)
    p.stroke([(315, 325), (370, 325)], 8)
    p.stroke([(342, 290), (342, 360)], 8)


def frog(p):
    p.blob([ell(256, 290, 165, 130), ell(170, 140, 52), ell(342, 140, 52)], GREEN)
    p.fill(ell(170, 140, 24), WHITE)
    p.fill(ell(342, 140, 24), WHITE)
    p.fill(ell(170, 140, 11), NAVY)
    p.fill(ell(342, 140, 11), NAVY)
    p.stroke(bez((165, 320), (220, 370), (292, 370), (347, 320)), 10)


def hen(p):
    p.blob([ell(90, 220, 30, 70, rot=-35), ell(80, 270, 30, 75), ell(95, 320, 28, 65, rot=35)], WHITE)
    p.oline([(250, 430), (250, 470)], 8, ORANGE)
    p.oline([(300, 430), (300, 470)], 8, ORANGE)
    p.blob([ell(250, 300, 150, 120), ell(360, 175, 62)], WHITE)
    for cx in (335, 365, 395):
        p.shape(ell(cx, 108, 20), RED)
    p.shape([(410, 165), (465, 185), (410, 205)], ORANGE)
    p.fill(ell(375, 168, 10), NAVY)


def hare(p):
    p.shape(ell(185, 120, 40, 110, rot=-10), GRAY)
    p.shape(ell(327, 120, 40, 110, rot=10), GRAY)
    p.fill(ell(185, 125, 17, 72, rot=-10), PINK)
    p.fill(ell(327, 125, 17, 72, rot=10), PINK)
    p.shape(ell(256, 320, 145, 118), GRAY)
    p.fill(ell(212, 300, 13), NAVY)
    p.fill(ell(300, 300, 13), NAVY)
    p.fill(ell(256, 340, 15, 11), PINK)
    p.shape(rrect(238, 352, 254, 388, 4), WHITE, 8)
    p.shape(rrect(258, 352, 274, 388, 4), WHITE, 8)


def wolf(p):
    p.shape([(150, 190), (120, 60), (235, 130)], DGRAY)
    p.shape([(362, 190), (392, 60), (277, 130)], DGRAY)
    p.shape(ell(256, 300, 145, 125), DGRAY)
    p.shape(ell(256, 372, 78, 52), (205, 208, 215))
    p.fill(ell(256, 348, 16, 12), NAVY)
    p.fill(ell(208, 275, 13), NAVY)
    p.fill(ell(304, 275, 13), NAVY)


def bear(p):
    p.shape(ell(140, 135, 52), BROWN)
    p.shape(ell(372, 135, 52), BROWN)
    p.fill(ell(140, 135, 22), TAN)
    p.fill(ell(372, 135, 22), TAN)
    p.shape(ell(256, 300, 155, 130), BROWN)
    p.shape(ell(256, 365, 75, 55), TAN)
    p.fill(ell(256, 345, 16, 12), NAVY)
    p.fill(ell(208, 280, 13), NAVY)
    p.fill(ell(304, 280, 13), NAVY)


def fox(p):
    p.shape([(140, 180), (115, 55), (240, 120)], ORANGE)
    p.shape([(372, 180), (397, 55), (272, 120)], ORANGE)
    p.shape([(120, 200), (392, 200), (256, 420)], ORANGE)
    p.fill(ell(205, 310, 50, 36), WHITE)
    p.fill(ell(307, 310, 50, 36), WHITE)
    p.fill(ell(256, 392, 15, 12), NAVY)
    p.fill(ell(200, 255, 13), NAVY)
    p.fill(ell(312, 255, 13), NAVY)


def grandma(p):
    p.shape(ell(256, 100, 42), (225, 228, 234))
    p.blob([ell(140, 220, 40, 70), ell(372, 220, 40, 70)], (225, 228, 234))
    p.shape(ell(256, 265, 145, 125), SKIN)
    p.stroke(ell(200, 255, 40), 8)
    p.stroke(ell(312, 255, 40), 8)
    p.stroke([(240, 255), (272, 255)], 8)
    p.fill(ell(200, 255, 10), NAVY)
    p.fill(ell(312, 255, 10), NAVY)
    p.stroke(bez((210, 335), (240, 365), (272, 365), (302, 335)), 9)


def granddaughter(p):
    p.shape(ell(120, 330, 34, 80), BROWN)
    p.shape(ell(392, 330, 34, 80), BROWN)
    p.shape(ell(256, 225, 148, 115), BROWN)
    p.shape(ell(256, 285, 128, 105), SKIN)
    p.fill(ell(180, 320, 20, 13), PINK)
    p.fill(ell(332, 320, 20, 13), PINK)
    p.fill(ell(215, 275, 12), NAVY)
    p.fill(ell(297, 275, 12), NAVY)
    p.stroke(bez((215, 342), (240, 368), (272, 368), (297, 342)), 9)


def turnip(p):
    p.blob([ell(256, 95, 26, 70), ell(190, 120, 24, 62, rot=-25), ell(322, 120, 24, 62, rot=25)], GREEN)
    p.blob([ell(256, 315, 140, 120), ell(256, 440, 26, 36)], (255, 200, 70))


def break_(p):  # a cracked circle: the egg cracks, the house cracks
    p.shape(ell(256, 256, 175), LBLUE)
    p.stroke([(256, 90), (220, 170), (280, 240), (225, 320), (265, 400)], 10)

def grandpa(p):  # bald, gray side hair and a gray beard
    p.blob([ell(140, 235, 32, 55), ell(372, 235, 32, 55)], (225, 228, 234))
    p.shape(ell(256, 265, 145, 125), SKIN)
    p.shape(ell(256, 375, 95, 62), (225, 228, 234))
    p.fill(ell(215, 250, 12), NAVY)
    p.fill(ell(297, 250, 12), NAVY)
    p.stroke([(190, 222), (240, 216)], 10, (225, 228, 234))
    p.stroke([(272, 216), (322, 222)], 10, (225, 228, 234))


def hungry(p):  # eyes squeezed shut, mouth open, one drool drop
    p.shape(ell(256, 256, 175), YELLOW)
    p.stroke(bez((160, 200), (185, 220), (205, 220), (225, 200)), 10)
    p.stroke(bez((287, 200), (307, 220), (327, 220), (352, 200)), 10)
    p.fill(ell(256, 330, 48, 58), NAVY)
    p.shape(teardrop(316, 420, 16), LBLUE, 8)


def run(p):  # two shoes mid-stride, motion lines behind
    for y in (140, 215, 290):
        p.stroke(bez((30, y), (90, y - 8), (130, y + 8), (170, y)), 10, STEAM)
    p.oline([(365, 120), (400, 62)], 14, BLUE)
    p.oline([(330, 320), (365, 262)], 14, BLUE)
    p.shape(ell(340, 160, 95, 42, rot=-18), BROWN)
    p.shape(ell(300, 372, 100, 44, rot=8), BROWN)


def build(p):  # a mallet
    p.shape(rrect(150, 90, 362, 175, 18), DGRAY)
    p.shape(rrect(240, 175, 278, 440, 12), WOOD)


def tumble(p):  # an egg dropping, speed lines above
    for x in (196, 256, 316):
        p.stroke([(x, 60), (x, 170)], 10, STEAM)
    p.shape(ell(256, 330, 115, 135), WHITE)
    p.fill(ell(212, 268, 24, 34, rot=15), (218, 230, 244))

def sound(p):  # a mouth dot with three sound arcs opening to the right
    p.fill(ell(105, 256, 52), NAVY)
    for r in (105, 165, 225):
        arc = [(105 + r * math.cos(math.radians(a)), 256 + r * math.sin(math.radians(a)))
               for a in range(-55, 56, 5)]
        p.stroke(arc, 13)


def sing(p):  # a musical note: a yellow head, a navy stem and a flag
    p.shape(ell(190, 385, 100, 68, rot=-18), YELLOW)
    p.shape(rrect(258, 110, 292, 372, 10), NAVY)
    p.stroke(bez((292, 122), (372, 140), (398, 195), (368, 250)), 24)


def clever(p):  # a light bulb with rays: a clever idea
    for a in (-150, -110, -70, -30, 30, 70, 110, 150):
        p.stroke([(256 + 148 * math.cos(math.radians(a)), 220 - 148 * math.sin(math.radians(a))),
                  (256 + 190 * math.cos(math.radians(a)), 220 - 190 * math.sin(math.radians(a)))],
                 11, (255, 190, 60))
    p.shape(ell(256, 220, 128, 138), YELLOW)
    p.shape(rrect(202, 340, 310, 372, 10), DGRAY)
    p.shape(rrect(212, 382, 300, 414, 10), DGRAY)


def jump(p):  # a hop: an up-and-over arc with an arrowhead at the landing
    p.stroke(bez((96, 396), (170, 130), (330, 130), (404, 372)), 13, STEAM)
    p.stroke([(404, 372), (352, 340)], 16)
    p.stroke([(404, 372), (368, 428)], 16)

def bake(p):  # a bun on a baking tray, steam rising: Grandma bakes Kolobok
    for x in (216, 256, 296):
        p.stroke(wave(x, 96, 168, 8, 1.2), 8, STEAM)
    p.shape(ell(256, 268, 92, 78), TAN)  # the bun
    p.shape(rrect(104, 320, 408, 392, 18), DGRAY)  # the tray
    p.shape(rrect(84, 392, 428, 424, 12), GRAY)


def window(p):  # a four-pane window with sky behind
    p.shape(rrect(116, 116, 396, 396, 14), LBLUE)
    p.stroke([(256, 116), (256, 396)], 16)
    p.stroke([(116, 256), (396, 256)], 16)
    p.shape(ell(186, 186, 30), WHITE)  # the sun behind the glass


def nose(p):  # a button nose: a soft triangle with two nostrils
    p.shape([(150, 150), (362, 150), (256, 356)], SKIN)
    p.fill(ell(216, 300, 15, 11), NAVY)
    p.fill(ell(296, 300, 15, 11), NAVY)


def beat(p):  # a hammer coming down, motion lines: Дедушка бил-бил
    for a in (200, 230, 260):
        p.stroke([(90 + 40 * math.cos(math.radians(a)), 330 - 40 * math.sin(math.radians(a))),
                  (30 + 40 * math.cos(math.radians(a)), 330 - 40 * math.sin(math.radians(a)))], 9, STEAM)
    p.shape(rrect(196, 128, 268, 380, 12), WOOD)  # the handle
    p.shape(rrect(120, 88, 344, 176, 16), DGRAY)  # the head


def tail(p):  # a little curved tail with a tuft: мышь махнула хвостиком
    p.stroke(bez((120, 392), (140, 200), (300, 210), (360, 130)), 20, GRAY)
    p.fill(ell(360, 130, 30), DGRAY)
    p.stroke(ell(360, 130, 30), OW)


def roof(p):  # a gable roof with a chimney: the bear climbs on the roof
    p.shape(rrect(340, 140, 396, 240, 8), BROWN)  # the chimney
    p.shape([(96, 316), (256, 132), (416, 316)], RED)  # the roof
    p.stroke([(150, 316), (150, 380)], 16, NAVY)  # the eaves
    p.stroke([(362, 316), (362, 380)], 16, NAVY)


def fall_apart(p):  # a house cracked in two: домик развалился
    p.shape([(120, 120), (252, 120), (216, 256), (268, 300), (200, 392), (120, 392)], WOOD)
    p.shape([(260, 120), (392, 120), (392, 392), (220, 392), (288, 300), (232, 256)], WOOD)


def new_(p):  # a fresh sparkle: a brand-new house
    p.shape([(256, 116), (296, 216), (396, 256), (296, 296), (256, 396), (216, 296), (116, 256),
             (216, 216)], YELLOW)
    p.fill(ell(382, 150, 20), ORANGE)
    p.fill(ell(140, 370, 14), ORANGE)



def clap(p):  # two hands clap in the middle, motion arcs above: Хлоп-хлоп!
    p.shape(ell(196, 300, 60, 90, rot=-28), SKIN)
    p.shape(ell(316, 300, 60, 90, rot=28), SKIN)
    p.fill(ell(238, 360, 18, 30, rot=-40), SKIN)  # thumbs
    p.fill(ell(274, 360, 18, 30, rot=40), SKIN)
    for a in (-50, -25, 0, 25, 50):
        p.stroke([(256 + 120 * math.cos(math.radians(a + 90)), 190 - 120 * math.sin(math.radians(a + 90))),
                  (256 + 165 * math.cos(math.radians(a + 90)), 190 - 165 * math.sin(math.radians(a + 90)))],
                 10, STEAM)


def stomp(p):  # a boot comes down, motion lines under it: Топ-топ!
    p.shape(rrect(206, 110, 306, 260, 18), BROWN)  # the leg of the boot
    p.shape(rrect(150, 240, 370, 330, 26), BROWN)  # the foot
    for x in (180, 256, 332):
        p.stroke([(x, 372), (x, 420)], 12, STEAM)
    p.stroke([(110, 452), (402, 452)], 12)


def puddle(p):  # a rain puddle with two ripples
    p.shape(ell(256, 320, 185, 62), LBLUE)
    p.stroke(bez((196, 312), (220, 296), (292, 296), (316, 312)), 9, BLUE)
    p.stroke(bez((170, 332), (205, 352), (307, 352), (342, 332)), 9, BLUE)
    for x in (206, 256, 306):  # last raindrops falling in
        p.stroke([(x, 130), (x, 175)], 10, BLUE)


def spider(p):  # Паучок: a round grey body, a little head and eight bent legs
    for side in (-1, 1):
        for dy, lift in ((-40, -70), (-10, -30), (20, 10), (50, 50)):
            x0 = 256 + side * 88
            p.stroke(bez((x0, 300 + dy), (x0 + side * 55, 300 + dy + lift),
                         (x0 + side * 95, 300 + dy + lift), (x0 + side * 115, 300 + dy + 60)), 9, DGRAY)
    p.shape(ell(256, 310, 105, 90), DGRAY)
    p.shape(ell(256, 195, 52), DGRAY)
    for x in (236, 276):
        p.fill(ell(x, 188, 12), WHITE)
        p.fill(ell(x, 190, 6), NAVY)


def sleep(p):  # three Z's floating up and to the right: спать
    for x, y, s in ((130, 360, 62), (232, 262, 84), (352, 148, 108)):
        p.stroke([(x, y), (x + s, y), (x, y + s * 0.72), (x + s, y + s * 0.72)], 15, NAVY)


def star(p):  # a five-pointed star
    pts = []
    for i in range(10):
        r = 165 if i % 2 == 0 else 70
        a = math.radians(-90 + i * 36)
        pts.append((256 + r * math.cos(a), 266 + r * math.sin(a)))
    p.shape(pts, YELLOW)


def head(p):  # a child's head with a tuft of hair
    p.shape(ell(256, 275, 140), SKIN)
    p.blob([ell(200, 148, 46, 30, rot=-18), ell(256, 132, 52, 32), ell(312, 148, 46, 30, rot=18)], BROWN)
    p.fill(ell(200, 262, 14), NAVY)
    p.fill(ell(312, 262, 14), NAVY)
    p.stroke(bez((205, 330), (235, 368), (277, 368), (307, 330)), 10)


def toe(p):  # five toes in a row, the big one first: пальчики
    for x, y, r in ((118, 262, 46), (196, 280, 40), (268, 294, 35), (334, 304, 30), (394, 312, 26)):
        p.shape(ell(x, y, r, r + 8), SKIN)


def farm(p):  # a red barn with a white cross door
    p.shape([(96, 236), (170, 128), (342, 128), (416, 236)], (196, 96, 60))  # the gambrel roof
    p.shape(rrect(120, 232, 392, 442, 8), RED)
    p.shape(rrect(228, 160, 284, 216, 8), WHITE)  # the hayloft window
    p.shape(rrect(214, 300, 298, 442, 6), WHITE)  # the door
    p.stroke([(214, 300), (298, 442)], 10, RED)
    p.stroke([(298, 300), (214, 442)], 10, RED)


def moo(p):  # the cow's word: a speech bubble with two slow waves
    p.shape([(176, 306), (150, 402), (238, 330)], WHITE)  # the bubble tail
    p.shape(rrect(92, 116, 420, 336, 60), WHITE)
    p.stroke(wave(216, 168, 286, 10, 1.2), 10, BROWN)
    p.stroke(wave(296, 168, 286, 10, 1.2), 10, BROWN)


def oink(p):  # the pig's word: a curly pink tail
    pts = []
    for i in range(61):
        a = i / 60 * 4.2 * math.pi
        r = 26 + i / 60 * 130
        pts.append((256 + r * math.cos(a), 266 + r * 0.85 * math.sin(a)))
    p.oline(pts, 10, PINK)


def quack(p):  # the duck's word: an open beak with sound dashes
    p.shape([(84, 216), (290, 250), (84, 284)], ORANGE)
    p.shape([(84, 284), (268, 322), (84, 344)], (230, 120, 25))
    for r in (330, 372, 414):
        p.stroke([(r, 236), (r + 18, 222)], 10, STEAM)
        p.stroke([(r, 300), (r + 18, 314)], 10, STEAM)


def pig(p):  # a pig face with a snout
    p.shape([(150, 205), (118, 92), (238, 152)], PINK)
    p.shape([(362, 205), (394, 92), (274, 152)], PINK)
    p.shape(ell(256, 290, 148, 128), PINK)
    p.fill(ell(198, 262, 13), NAVY)
    p.fill(ell(314, 262, 13), NAVY)
    p.shape(ell(256, 330, 62, 44), (255, 196, 200))
    p.fill(ell(236, 330, 10, 14), NAVY)
    p.fill(ell(276, 330, 10, 14), NAVY)


def one(p):  # the digit 1
    p.stroke([(208, 176), (268, 132), (268, 384)], 30)
    p.stroke([(196, 384), (340, 384)], 30)


def two(p):  # the digit 2
    p.stroke(bez((168, 200), (170, 108), (344, 108), (342, 214)), 30)
    p.stroke(bez((342, 214), (322, 300), (212, 332), (172, 384)), 30)
    p.stroke([(172, 384), (352, 384)], 30)


def five(p):  # the digit 5
    p.stroke([(344, 128), (196, 128), (184, 248)], 30)
    p.stroke(bez((184, 248), (236, 206), (362, 226), (356, 322)), 30)
    p.stroke(bez((356, 322), (350, 404), (224, 420), (168, 364)), 30)


def eight(p):  # the digit 8: two stacked rings
    p.stroke(ell(256, 192, 84, 74), 26, closed=True)
    p.stroke(ell(256, 346, 98, 84), 26, closed=True)


def ten(p):  # the digits 1 and 0
    p.stroke([(128, 190), (172, 160), (172, 372)], 28)
    p.stroke([(116, 372), (228, 372)], 28)
    p.stroke(ell(342, 266, 78, 106), 28, closed=True)


def planet(p):  # a ringed planet
    p.shape(ell(256, 246, 118), ORANGE)
    p.fill(ell(216, 210, 26, 18), (230, 120, 20))
    p.fill(ell(296, 286, 30, 20), (230, 120, 20))
    p.stroke(ell(256, 258, 205, 56, rot=-12), 18, TAN)


def earth(p):  # planet Earth: blue oceans, green land
    p.shape(ell(256, 256, 165), BLUE)
    p.fill(ell(196, 196, 58, 42, rot=-18), GREEN)
    p.fill(ell(310, 300, 52, 38, rot=14), GREEN)
    p.fill(ell(222, 332, 32, 24, rot=28), GREEN)


def ear(p):  # an ear with its inner curl: ухо
    p.shape(ell(256, 268, 118, 150), SKIN)
    p.stroke(bez((300, 190), (222, 220), (220, 300), (286, 330)), 13, (240, 170, 130))
    p.fill(ell(268, 352, 26, 34), (240, 170, 130))


def finger(p):  # one pointing finger: пальчик
    p.shape(rrect(216, 108, 296, 400, 40), SKIN)
    p.shape(ell(256, 158, 26, 34), (255, 228, 200), 7)  # the nail
    for a in (-40, 0, 40):  # it points up: three short marks
        p.stroke([(256 + 120 * math.cos(math.radians(a + 90)), 90 - 120 * math.sin(math.radians(a + 90)) * 0.4),
                  (256 + 165 * math.cos(math.radians(a + 90)), 90 - 165 * math.sin(math.radians(a + 90)) * 0.4)],
                 9, STEAM)


def count(p):  # one, two, three: three ascending dots with an arrow
    for (x, y, c) in ((140, 380, GREEN), (256, 300, YELLOW), (372, 220, RED)):
        p.shape(ell(x, y, 52), c)
    p.stroke(bez((120, 420), (220, 240), (300, 190), (400, 140)), 11, STEAM)


ICONS = {
    "ice": ice, "cold": cold, "warm": warm, "hot": hot, "soup": soup, "sun": sun, "snow": snow, "touch": touch,
    "feather": feather, "balloon": balloon, "watermelon": watermelon, "elephant": elephant, "mouse": mouse,
    "tree": tree, "flower": flower, "pillow": pillow, "block": block, "teddy": teddy, "table": table,
    "chair": chair, "where": where, "in": in_, "on": on, "under": under, "box": box,
    "red": _swatch((237, 52, 56)), "blue": _swatch((46, 120, 230)), "yellow": _swatch((255, 214, 40)),
    "green": _swatch((70, 176, 90)),
    "sea": sea, "listen": listen, "who": who, "dog": dog, "cat": cat, "cow": cow, "duck": duck, "sky": sky,
    "cloud": cloud, "rain": rain, "wind": wind, "grass": grass, "seed": seed, "soil": soil, "wait": wait,
    "grow": grow, "plant": plant, "melt": melt,
    "egg": egg, "golden": golden, "speckled": speckled, "kolobok": kolobok, "round": round_,
    "roll": roll, "happy": happy, "house": house, "frog": frog, "hen": hen, "hare": hare,
    "wolf": wolf, "bear": bear, "fox": fox, "grandma": grandma, "granddaughter": granddaughter,
    "turnip": turnip, "break": break_, "white": _swatch(WHITE),
    "grandpa": grandpa, "hungry": hungry, "run": run, "build": build, "tumble": tumble,
    "sound": sound, "sing": sing, "clever": clever, "jump": jump,
    "bake": bake, "window": window, "nose": nose, "beat": beat, "tail": tail, "roof": roof,
    "fall_apart": fall_apart, "new": new_,
    "clap": clap, "stomp": stomp, "puddle": puddle, "spider": spider, "sleep": sleep,
    "star": star, "head": head, "toe": toe, "farm": farm, "moo": moo, "oink": oink,
    "quack": quack, "pig": pig,
    "one": one, "two": two, "five": five, "eight": eight, "ten": ten, "planet": planet,
    "earth": earth, "ear": ear, "finger": finger, "count": count,
}


def draw(name: str) -> Image.Image:
    pen = Pen()
    ICONS[name](pen)
    return pen.image()


def sheet(names: list[str], path: pathlib.Path, cols: int = 8, cell: int = 150) -> None:
    rows = (len(names) + cols - 1) // cols
    im = Image.new("RGB", (cols * cell, rows * (cell + 18)), (255, 255, 255))
    d = ImageDraw.Draw(im)
    font = ImageFont.load_default()
    for k, name in enumerate(names):
        icon = Image.open(LIB / f"{name}.png").convert("RGBA")
        s = min((cell - 20) / icon.width, (cell - 20) / icon.height)
        icon = icon.resize((round(icon.width * s), round(icon.height * s)), Image.Resampling.LANCZOS)
        x, y = (k % cols) * cell, (k // cols) * (cell + 18)
        im.paste(icon, (x + (cell - icon.width) // 2, y + 14 + (cell - icon.height) // 2), icon)
        d.text((x + 4, y + 2), name, fill=(0, 0, 0), font=font)
    path.parent.mkdir(exist_ok=True)
    im.save(path)


def eleven(p):
    _two_digits(p, 1, 1)


def twelve(p):
    _two_digits(p, 1, 2)


def thirteen(p):
    _two_digits(p, 1, 3)


def fourteen(p):
    _two_digits(p, 1, 4)


def fifteen(p):
    _two_digits(p, 1, 5)


def sixteen(p):
    _two_digits(p, 1, 6)


def seventeen(p):
    _two_digits(p, 1, 7)


def eighteen(p):
    _two_digits(p, 1, 8)


def nineteen(p):
    _two_digits(p, 1, 9)


def twenty(p):
    _two_digits(p, 2, 0)


def because(p):  # one thing points to the next: dot, arrow, dot
    p.fill(ell(120, 300, 42), YELLOW)
    p.stroke(ell(120, 300, 42), 10, closed=True)
    p.fill(ell(396, 300, 42), GREEN)
    p.stroke(ell(396, 300, 42), 10, closed=True)
    p.oline([(176, 300), (336, 300)], 16, NAVY)
    p.fill([(316, 268), (366, 300), (316, 332)], NAVY)


def so_(p):  # a bold onward arrow: therefore
    p.oline([(110, 256), (330, 256)], 26, NAVY)
    p.fill([(300, 196), (412, 256), (300, 316)], NAVY)


def but(p):  # the path turns: a hooked arrow
    p.stroke(bez((120, 380), (110, 160), (330, 140), (352, 300)), 22)
    p.fill([(320, 272), (392, 322), (312, 344)], NAVY)


def why(p):  # a big asking hook with a spark
    p.stroke(bez((160, 190), (160, 90), (370, 90), (370, 210)), 30)
    p.stroke(bez((370, 210), (300, 280), (276, 300), (276, 340)), 30)
    p.fill(ell(276, 400, 26), NAVY)
    for dx, dy in ((60, -70), (96, -20), (40, 30)):
        p.fill(ell(400 + dx * 0.6, 120 + dy, 12), ORANGE)


def which(p):  # a question over two choices
    p.stroke(bez((256, 140), (256, 84), (368, 84), (368, 160)), 24)
    p.stroke(bez((368, 160), (330, 200), (298, 216), (298, 252)), 24)
    p.fill(ell(298, 296, 20), NAVY)
    p.fill(ell(150, 380, 40), YELLOW)
    p.stroke(ell(150, 380, 40), 10, closed=True)
    p.fill(ell(370, 380, 40), GREEN)
    p.stroke(ell(370, 380, 40), 10, closed=True)


def first(p):  # a starter flag on the first dot
    p.fill(ell(170, 360, 56), GREEN)
    p.stroke(ell(170, 360, 56), 12, closed=True)
    p.oline([(170, 360), (170, 96)], 14, NAVY)
    p.fill([(170, 96), (342, 142), (170, 192)], RED)
    p.stroke([(170, 96), (342, 142), (170, 192)], 10, closed=True)


def then(p):  # one, two: the steps in order
    p.fill(ell(140, 320, 54), GREEN)
    p.stroke(ell(140, 320, 54), 12, closed=True)
    p.fill(ell(400, 320, 54), RED)
    p.stroke(ell(400, 320, 54), 12, closed=True)
    p.oline([(208, 320), (330, 320)], 16, NAVY)
    p.fill([(310, 288), (368, 320), (310, 352)], NAVY)


def next_(p):  # dots three and four: the march goes on
    for i, (x, c) in enumerate(((110, GREEN), (230, YELLOW), (350, ORANGE))):
        p.fill(ell(x, 290, 42), c)
        p.stroke(ell(x, 290, 42), 11, closed=True)
    p.oline([(410, 400), (150, 400)], 16, NAVY)
    p.fill([(128, 372), (76, 400), (128, 428)], NAVY)


def at_last(p):  # the flag at the finish line
    p.oline([(96, 380), (400, 380)], 16, NAVY)
    p.fill(ell(140, 380, 48), GREEN)
    p.stroke(ell(140, 380, 48), 12, closed=True)
    p.fill([(400, 380), (400, 116), (438, 116), (438, 380)], NAVY)
    p.fill([(160, 110), (330, 152), (160, 198)], RED)
    p.stroke([(160, 110), (330, 152), (160, 198)], 10, closed=True)
    p.oline([(160, 380), (160, 110)], 14, NAVY)
    p.fill(ell(330, 300, 30), YELLOW)


def now(p):  # a clock face: this moment
    p.stroke(ell(256, 266, 150), 16, closed=True)
    for a in range(0, 360, 90):
        import math as _m
        x = 256 + 118 * _m.cos(_m.radians(a))
        y = 266 + 118 * _m.sin(_m.radians(a))
        p.fill(ell(x, y, 16), NAVY)
    p.oline([(256, 266), (256, 156)], 16, NAVY)
    p.oline([(256, 266), (346, 320)], 20, RED)
    p.fill(ell(256, 266, 18), NAVY)


def guess(p):  # two covered cards and a question
    p.stroke(rrect(120, 180, 260, 340, 18), 12, closed=True)
    p.stroke(rrect(250, 220, 390, 380, 18), 12, closed=True)
    p.fill(ell(256, 120, 22), NAVY)
    p.stroke(bez((300, 66), (380, 60), (382, 112), (350, 130)), 14)


def know(p):  # a bulb that lights: now we know
    p.stroke(ell(256, 210, 92, 104), 12, closed=True)
    p.fill(ell(256, 210, 64, 74), YELLOW)
    p.stroke([(226, 330), (286, 330)], 14)
    p.stroke([(232, 366), (280, 366)], 14)
    for a in (-60, -20, 20, 60):
        import math as _m
        x = 256 + 140 * _m.cos(_m.radians(a - 90))
        y = 210 + 140 * _m.sin(_m.radians(a - 90))
        p.oline([(256 + 108 * _m.cos(_m.radians(a - 90)), 210 + 108 * _m.sin(_m.radians(a - 90))),
                 (x, y)], 10, ORANGE)


def make(p):  # parts go in, a thing comes out
    p.fill(ell(130, 300, 36), YELLOW)
    p.stroke(ell(130, 300, 36), 10, closed=True)
    p.oline([(180, 300), (300, 300)], 14, NAVY)
    p.fill([(280, 272), (332, 300), (280, 328)], NAVY)
    p.shape(ell(400, 300, 58), RED)


def become(p):  # a drop turns into an ice cube
    p.shape(teardrop(120, 300, 52), BLUE)
    p.oline([(190, 300), (300, 300)], 14, NAVY)
    p.fill([(280, 272), (332, 300), (280, 328)], NAVY)
    p.shape(rrect(340, 240, 440, 360, 22), ICE)
    p.stroke([(356, 300), (424, 300)], 8, WHITE)


def give(p):  # two hands pass a round thing across
    p.oline([(96, 330), (216, 300), (236, 336)], 22, SKIN)
    p.oline([(416, 330), (296, 300), (276, 336)], 22, SKIN)
    p.shape(ell(256, 250, 44), ORANGE)


def take(p):  # a hand lifts the thing out of the box
    open_box(p)
    p.oline([(300, 60), (266, 150)], 22, SKIN)
    p.shape(ell(256, 190, 40), RED)


def put(p):  # a hand lowers the thing into the box
    open_box(p)
    p.oline([(300, 60), (266, 130)], 22, SKIN)
    p.shape(ell(256, 176, 40), RED)


def play(p):  # a ball and a spark: a game is on
    ball(p, 236, 266, 110)
    for dx, dy in ((120, -60), (150, 40), (-40, -130)):
        p.fill(ell(256 + dx, 266 + dy, 14), YELLOW)


def hide(p):  # two eyes peek from inside the box
    open_box(p, ball_in=False)
    p.fill(ell(210, 330, 26, 30), WHITE)
    p.fill(ell(302, 330, 26, 30), WHITE)
    p.fill(ell(210, 330, 11, 14), NAVY)
    p.fill(ell(302, 330, 11, 14), NAVY)


def leave(p):  # a door and an arrow out
    p.stroke(rrect(150, 120, 330, 400, 14), 14, closed=True)
    p.fill(ell(296, 266, 12), NAVY)
    p.oline([(200, 440), (200, 470)], 0.1, WHITE)  # no-op keeps the API busy
    p.oline([(350, 266), (430, 266)], 16, GREEN)
    p.fill([(410, 238), (462, 266), (410, 294)], GREEN)


def rise(p):  # curls climb: steam rises
    for i, x in enumerate((180, 280, 380)):
        p.stroke(bez((x, 400), (x - 50, 320), (x + 50, 260), (x, 160 + i * 10)), 16, STEAM)
    p.oline([(180, 150), (380, 120)], 12, NAVY)


def set_(p):  # the sun goes down below the line
    p.stroke([(96, 340), (416, 340)], 14, NAVY)
    p.shape(ell(256, 340, 120), YELLOW)
    for a in (-70, -40, -10, 20, 50, 80):
        import math as _m
        x0 = 256 + 150 * _m.cos(_m.radians(a))
        y0 = 340 - 150 * _m.sin(_m.radians(a))
        x1 = 256 + 190 * _m.cos(_m.radians(a))
        y1 = 340 - 190 * _m.sin(_m.radians(a))
        p.oline([(x0, y0), (x1, y1)], 10, ORANGE)


def turn(p):  # a round arrow: it goes around
    p.stroke(bez((150, 330), (110, 170), (330, 120), (380, 280)), 24)
    p.fill([(352, 252), (416, 300), (344, 326)], NAVY)


def boil(p):  # a pot with bubbles
    pot(p)
    for (x, y, r) in ((190, 220, 18), (256, 190, 22), (322, 220, 18)):
        p.stroke(ell(x, y, r), 9, STEAM, closed=True)


def wake(p):  # an eye opens to the sun
    p.stroke(bez((120, 330), (180, 210), (340, 210), (400, 330)), 16)
    p.fill(ell(256, 292, 60, 54), WHITE)
    p.fill(ell(256, 292, 26, 30), NAVY)
    p.shape(ell(256, 96, 44), YELLOW)


def close_(p):  # a shut eye: lashes down
    p.stroke(bez((120, 266), (190, 330), (322, 330), (392, 266)), 18)
    for t in (0.2, 0.5, 0.8):
        x = 140 + 232 * t
        y = 322 + 26 * _sin_bump(t)
        p.oline([(x, y), (x - 8, y + 34)], 8, NAVY)


def _sin_bump(t):
    import math as _m
    return _m.sin(_m.pi * t)


def long(p):  # a line that runs to both edges
    p.oline([(90, 256), (422, 256)], 20, BLUE)
    p.fill([(60, 226), (110, 256), (60, 286)], NAVY)
    p.fill([(402, 226), (452, 256), (402, 286)], NAVY)


def short(p):  # the same idea, small
    p.oline([(196, 256), (316, 256)], 20, BLUE)
    p.fill([(172, 232), (208, 256), (172, 280)], NAVY)
    p.fill([(304, 232), (340, 256), (304, 280)], NAVY)


def fast(p):  # three chevrons: speed
    for i in range(3):
        x = 130 + i * 96
        p.stroke([(x, 190), (x + 60, 256), (x, 322)], 20)


def slow(p):  # one chevron: not fast
    p.stroke([(180, 200), (270, 256), (180, 312)], 20)


def quietly(p):  # a small note under a hush curve
    p.fill(ell(200, 330, 34, 26), NAVY)
    p.oline([(232, 330), (232, 180)], 12, NAVY)
    p.stroke(bez((150, 130), (256, 86), (362, 130), (380, 170)), 12, STEAM)


def loudly(p):  # a big note with rays
    p.fill(ell(210, 350, 46, 36), NAVY)
    p.oline([(252, 350), (252, 140)], 18, NAVY)
    for a in (-30, 30, 90):
        import math as _m
        x0 = 300 + 40 * _m.cos(_m.radians(a - 90))
        y0 = 260 + 40 * _m.sin(_m.radians(a - 90))
        x1 = 300 + 90 * _m.cos(_m.radians(a - 90))
        y1 = 260 + 90 * _m.sin(_m.radians(a - 90))
        p.oline([(x0, y0), (x1, y1)], 10, ORANGE)


def shadow_st(p):  # a grey twin on the ground
    p.stroke([(70, 380), (442, 380)], 12, NAVY)
    p.fill(ell(180, 388, 96, 22), GRAY)
    p.fill(ell(196, 240, 34, 40), SKIN)
    p.stroke(ell(196, 240, 34, 40), 10, closed=True)
    p.fill([(166, 290), (226, 290), (240, 378), (152, 378)], BLUE)
    p.stroke([(166, 290), (226, 290), (240, 378), (152, 378)], 10, closed=True)
    p.oline([(256, 300), (330, 250)], 12, SKIN)
    p.shape(ell(370, 240, 30), YELLOW)


def night_st(p):  # a moon and one star
    p.stroke(bez((300, 120), (180, 150), (180, 300), (300, 360)), 20, YELLOW)
    p.fill(ell(256, 200, 40, 10), (255, 208, 52))
    p.fill([(400, 140), (416, 180), (458, 184), (426, 212), (438, 252), (400, 230),
            (362, 252), (374, 212), (342, 184), (384, 180)], YELLOW)


def moon(p):  # a filled crescent: outer arc out, inner arc home
    import math as _m
    outer = [(256 + 120 * _m.cos(_m.radians(a)), 256 + 120 * _m.sin(_m.radians(a)))
             for a in range(-80, 100, 8)]
    inner = [(236 + 96 * _m.cos(_m.radians(a)), 256 + 96 * _m.sin(_m.radians(a)))
             for a in range(90, -70, -8)]
    pts = outer + inner
    p.fill(pts, YELLOW)
    p.stroke(pts, 12, closed=True)


def morning(p):  # the sun comes up over the line
    p.stroke([(96, 330), (416, 330)], 14, NAVY)
    p.shape(ell(256, 330, 110), YELLOW)
    for a in (-60, -30, 0, 30, 60):
        import math as _m
        x0 = 256 + 140 * _m.cos(_m.radians(a))
        y0 = 330 - 140 * _m.sin(_m.radians(a))
        x1 = 256 + 180 * _m.cos(_m.radians(a))
        y1 = 330 - 180 * _m.sin(_m.radians(a))
        p.oline([(x0, y0), (x1, y1)], 10, ORANGE)


def winter(p):  # a snowflake
    import math as _m
    for a in range(0, 180, 60):
        x1 = 256 + 150 * _m.cos(_m.radians(a))
        y1 = 256 + 150 * _m.sin(_m.radians(a))
        x0 = 256 - 150 * _m.cos(_m.radians(a))
        y0 = 256 - 150 * _m.sin(_m.radians(a))
        p.oline([(x0, y0), (x1, y1)], 12, ICE)
    p.fill(ell(256, 256, 20), WHITE)


def spring(p):  # a sprout in the soil with a bud on top
    p.oline([(256, 420), (256, 240)], 16, DGREEN)
    p.fill(bez((256, 260), (180, 240), (150, 180), (216, 176)), GREEN)
    p.stroke(bez((256, 260), (180, 240), (150, 180), (216, 176)), 12, closed=True)
    p.fill(bez((256, 260), (330, 240), (360, 180), (296, 176)), GREEN)
    p.stroke(bez((256, 260), (330, 240), (360, 180), (296, 176)), 12, closed=True)
    p.oline([(120, 420), (392, 420)], 16, BROWN)
    p.fill(ell(256, 190, 30, 34), PINK)
    p.stroke(ell(256, 190, 30, 34), 10, closed=True)


def summer(p):  # the high sun
    p.shape(ell(256, 240, 90), YELLOW)
    for a in range(0, 360, 45):
        import math as _m
        x0 = 256 + 116 * _m.cos(_m.radians(a))
        y0 = 240 + 116 * _m.sin(_m.radians(a))
        x1 = 256 + 160 * _m.cos(_m.radians(a))
        y1 = 240 + 160 * _m.sin(_m.radians(a))
        p.oline([(x0, y0), (x1, y1)], 10, ORANGE)


def steam_st(p):  # three soft curls
    for i, x in enumerate((170, 270, 370)):
        p.stroke(bez((x - 40, 400), (x + 40, 330), (x - 40, 260), (x + 20, 160)), 20, STEAM)


def air(p):  # three bubbles of nothing you can see
    for (x, y, r) in ((180, 340, 40), (300, 260, 56), (390, 150, 30)):
        p.stroke(ell(x, y, r, r * 0.92), 12, LBLUE, closed=True)


def bag(p):  # a soft tote
    p.shape(rrect(130, 200, 382, 420, 26), YELLOW)
    p.stroke(bez((200, 210), (210, 120), (302, 120), (312, 210)), 16, closed=False)


def apple_st(p):  # an apple with one leaf
    p.fill(ell(230, 300, 100, 96), RED)
    p.stroke(ell(230, 300, 100, 96), 12, closed=True)
    p.oline([(236, 200), (246, 130)], 14, BROWN)
    p.fill(bez((250, 150), (310, 110), (350, 140), (330, 186)), GREEN)


def orange_st(p):  # an orange with a star navel
    p.fill(ell(256, 290, 110, 104), ORANGE)
    p.stroke(ell(256, 290, 110, 104), 12, closed=True)
    for (dx, dy) in ((-40, -30), (30, -46), (52, 26), (-14, 44), (-58, 10)):
        p.fill(ell(256 + dx, 290 + dy, 5), (200, 90, 10))
    p.fill(ell(256, 290, 22, 8), (255, 210, 120))


def peel_st(p):  # one curled strip of peel
    p.stroke(bez((130, 400), (160, 240), (300, 200), (370, 260)), 26, ORANGE)
    p.stroke(bez((370, 260), (380, 340), (300, 380), (230, 350)), 18, ORANGE)


def peel_off(p):  # the orange and its strip
    p.stroke(ell(200, 300, 96, 90), 12, ORANGE, closed=True)
    p.fill(ell(200, 300, 82, 76), ORANGE)
    p.stroke(bez((300, 380), (330, 240), (430, 220), (450, 290)), 20, ORANGE)


def sense(p):  # five dots, one for each sense
    import math as _m
    pts = [(256 + 120 * _m.sin(_m.radians(a)), 260 - 120 * _m.cos(_m.radians(a)))
           for a in range(0, 360, 72)]
    cols = (RED, YELLOW, GREEN, BLUE, ORANGE)
    for (x, y), c in zip(pts, cols):
        p.fill(ell(x, y, 34), c)
        p.stroke(ell(x, y, 34), 10, closed=True)
    p.oline([(256, 260 - 60), (256, 260 + 60)], 12, NAVY)


def hand_st(p):  # an open hand: the five tools
    p.fill(rrect(190, 230, 322, 420, 30), SKIN)
    p.stroke(rrect(190, 230, 322, 420, 30), 11, closed=True)
    for i in range(4):
        x = 196 + i * 34
        p.fill(rrect(x - 11, 120 + abs(i - 1.5) * 16, x + 11, 250, 11), SKIN)
        p.stroke(rrect(x - 11, 120 + abs(i - 1.5) * 16, x + 11, 250, 11), 9, closed=True)
    p.fill(rrect(120, 250, 200, 310, 22), SKIN)
    p.stroke(rrect(120, 250, 200, 310, 22), 9, closed=True)


def chick(p):  # a round yellow chick
    p.fill(ell(256, 300, 110, 100), YELLOW)
    p.stroke(ell(256, 300, 110, 100), 11, closed=True)
    p.fill(ell(216, 270, 12, 14), NAVY)
    p.fill(ell(296, 270, 12, 14), NAVY)
    p.fill(ell(256, 306, 14, 10), ORANGE)
    p.oline([(256, 396), (256, 436)], 10, ORANGE)
    p.oline([(226, 396), (226, 436)], 10, ORANGE)


def up(p):  # one bold arrow, tip up
    p.oline([(256, 420), (256, 130)], 24, NAVY)
    p.fill([(196, 190), (256, 84), (316, 190)], NAVY)


def down(p):  # one bold arrow, tip down
    p.oline([(256, 100), (256, 390)], 24, NAVY)
    p.fill([(196, 330), (256, 436), (316, 330)], NAVY)


def quiet(p):  # one finger on the lips: hush
    p.stroke(bez((130, 300), (200, 360), (320, 360), (390, 300)), 18)
    p.fill(rrect(228, 150, 284, 330, 24), SKIN)
    p.stroke(rrect(228, 150, 284, 330, 24), 10, closed=True)
    p.fill(ell(256, 130, 34, 40), SKIN)
    p.stroke(ell(256, 130, 34, 40), 10, closed=True)


def out_of(p):  # the arrow leaves the box
    open_box(p)
    p.oline([(300, 240), (400, 130)], 18, GREEN)
    p.fill([(382, 96), (446, 84), (424, 148)], GREEN)


def _dig(p, ch, cx, cy, h, sw):  # one digit, drawn from strokes in a tall box
    w = 0.62 * h  # the digit's width span
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = cy - h / 2, cy + h / 2
    yq = cy - h / 4  # the upper quarter line

    def L(pts):
        p.stroke(pts, sw)

    if ch == "0":
        p.stroke(ell(cx, cy, w * 0.42, h * 0.46), sw, closed=True)
    elif ch == "1":
        L([(x0 + 0.16 * w, y1 - 0.22 * h), (cx - 0.04 * w, y0 + 0.18 * h)])
        L([(cx + 0.08 * w, y0), (cx + 0.08 * w, y1)])
        L([(x0 + 0.08 * w, y1), (x1 - 0.1 * w, y1)])
    elif ch == "2":
        p.stroke(bez((x0 + 0.12 * w, yq + 0.1 * h), (x0, y0 + 0.06 * h), (x1, y0 + 0.04 * h),
                     (x1 - 0.06 * w, yq)), sw)
        p.stroke(bez((x1 - 0.06 * w, yq), (x1 - 0.2 * w, cy + 0.12 * h), (x0 + 0.2 * w, cy + 0.2 * h),
                     (x0 + 0.08 * w, y1)), sw)
        L([(x0 + 0.08 * w, y1), (x1 - 0.08 * w, y1)])
    elif ch == "3":
        p.stroke(bez((x0 + 0.1 * w, y0 + 0.1 * h), (x1 - 0.1 * w, y0), (x1 - 0.06 * w, yq + 0.08 * h),
                     (cx + 0.02 * w, cy - 0.04 * h)), sw)
        p.stroke(bez((cx + 0.02 * w, cy - 0.04 * h), (x1 + 0.1 * w, cy + 0.14 * h),
                     (x1 - 0.16 * w, y1 - 0.04 * h), (x0 + 0.12 * w, y1 - 0.06 * h)), sw)
    elif ch == "4":
        L([(x0, yq + 0.12 * h), (x1 - 0.36 * w, y1 - 0.06 * h)])
        L([(x1 - 0.36 * w, y1 - 0.06 * h), (x1 - 0.04 * w, y1 - 0.06 * h)])
        L([(x1 - 0.04 * w, y1), (x1 - 0.04 * w, y0)])
        L([(x1 - 0.42 * w, cy + 0.1 * h), (x1 - 0.02 * w, cy + 0.1 * h)])
    elif ch == "5":
        L([(x0 + 0.1 * w, y0), (x1 - 0.14 * w, y0)])
        L([(x1 - 0.14 * w, y0), (x1 - 0.18 * w, yq)])
        p.stroke(bez((x1 - 0.18 * w, yq), (x1 + 0.14 * w, cy - 0.1 * h), (x1 - 0.1 * w, y1),
                     (x0 + 0.1 * w, y1 - 0.04 * h)), sw)
    elif ch == "6":
        p.stroke(bez((x1 - 0.2 * w, y0 + 0.08 * h), (x0 + 0.06 * w, y0 + 0.2 * h),
                     (x0 + 0.04 * w, cy), (cx, y1 - 0.06 * h)), sw)
        p.stroke(ell(cx + 0.06 * w, cy + 0.22 * h, 0.36 * w, 0.26 * h), sw, closed=True)
    elif ch == "7":
        L([(x0 + 0.06 * w, y0), (x1 - 0.06 * w, y0)])
        L([(x1 - 0.06 * w, y0), (cx - 0.08 * w, y1)])
    elif ch == "8":
        p.stroke(ell(cx, yq, 0.3 * w, 0.23 * h), sw * 0.9, closed=True)
        p.stroke(ell(cx, cy + h * 0.27, 0.38 * w, 0.24 * h), sw * 0.9, closed=True)
    elif ch == "9":
        p.stroke(ell(cx - 0.04 * w, yq, 0.34 * w, 0.24 * h), sw * 0.9, closed=True)
        p.stroke(bez((cx + 0.3 * w, yq), (x1 + 0.06 * w, cy + 0.1 * h), (x1 - 0.1 * w, y1),
                     (x0 + 0.14 * w, y1 - 0.02 * h)), sw)


def _two_digits(p, tens, ones):  # the number stickers of book 36: two digits side by side
    _dig(p, str(tens), 168, 266, 240, 34)
    _dig(p, str(ones), 356, 266, 240, 34)


ICONS.update({  # the older-kids books (23 to 37)
    "eleven": eleven, "twelve": twelve, "thirteen": thirteen, "fourteen": fourteen,
    "fifteen": fifteen, "sixteen": sixteen, "seventeen": seventeen, "eighteen": eighteen,
    "nineteen": nineteen, "twenty": twenty,
    "because": because, "so": so_, "but": but, "why": why, "which": which,
    "first": first, "then": then, "next": next_, "at_last": at_last, "now": now,
    "guess": guess, "know": know, "make": make, "become": become, "give": give,
    "take": take, "put": put, "play": play, "hide": hide, "leave": leave,
    "rise": rise, "set": set_, "turn": turn, "boil": boil, "wake": wake, "close": close_,
    "long": long, "short": short, "fast": fast, "slow": slow,
    "quietly": quietly, "loudly": loudly,
    "shadow": shadow_st, "night": night_st, "moon": moon, "morning": morning,
    "winter": winter, "spring": spring, "steam": steam_st, "air": air,
    "bag": bag, "apple": apple_st, "orange": orange_st, "peel": peel_st, "peel_off": peel_off,
    "sense": sense, "hand": hand_st, "chick": chick, "out_of": out_of,
    "up": up, "down": down, "quiet": quiet,
})



if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    names = args or list(ICONS)
    unknown = [n for n in names if n not in ICONS]
    if unknown:
        raise SystemExit(f"no icon drawn by code for {unknown}. Icons: {' '.join(ICONS)}")
    LIB.mkdir(parents=True, exist_ok=True)
    for name in names:
        draw(name).save(LIB / f"{name}.png", optimize=True)
    print("drew:", " ".join(names))
    if "--sheet" in sys.argv:
        sheet(names, pathlib.Path(__file__).resolve().parent.parent / "renders" / "icons.png")


# -------------------------------------------------------------------------------- the older-kids icons
