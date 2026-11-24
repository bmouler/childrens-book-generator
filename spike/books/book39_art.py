"""Book 39 art: Rain and a Puddle. The page names match the `art` keys of book39.py.
A yellow duckling in a warm summer rain, dancing in a puddle.
"""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same duckling from the reference picture"
CHARSHEET = (
    "A character reference picture of one small duckling for a children's picture book: a round "
    "fluffy yellow duckling with a wide flat orange bill, big happy brown eyes and small orange "
    "webbed feet. Shown once, full body, friendly front view, centered on a plain white background "
    "with generous empty space on every side."
)
RAIN = "short thin blue rain lines falling from the top of the picture"
PUDDLE = "one flat light-blue puddle on plain flat green grass"
PAGES = {
    "p01_rain": f"{T} running out of a small house door onto plain flat green grass toward {PUDDLE}, "
                 f"bill open with joy, {RAIN}. {MARGIN} {NO_EXTRA}",
    "p02_splash": f"{T} standing in the middle of {PUDDLE} with one webbed foot lifted high, small "
                  f"blue splash drops flying up around the foot, bill wide open laughing. {MARGIN} "
                  f"{NO_EXTRA}",
    "p03_sun": f"{T} on plain flat green grass beside {PUDDLE}, spinning with happiness, wings out "
               f"wide, a big bright yellow sun with short triangular rays above, no rain. {MARGIN} "
               f"{NO_EXTRA}",
    "p04_quack": f"{T} standing in the puddle, bill wide open in a loud quack, both wings flapping "
                 f"high, three small curved sound lines beside the bill. {MARGIN} {NO_EXTRA}",
    "p05_mother": f"{T} standing beside one larger mother duck on plain flat green grass, both "
                  f"facing each other with open bills, the duckling lifting one wing. {MARGIN} "
                  f"{NO_EXTRA}",
    "p06_evening": f"{T} walking on plain flat green grass toward a small warm-lit house door in "
                   f"the evening, the sky a soft pink, one small star above the roof. {MARGIN} "
                   f"{NO_EXTRA}",
}
COVER = (f"{T} standing in the middle of {PUDDLE} with wings out, laughing, under {RAIN}. "
         f"{MARGIN} {NO_EXTRA}")