"""Book 17 art prompts: Rain, Go Away! The page names match the `art` keys of book17.py.
The toddler chants at the rain, then plays in the puddles when the sun comes out.
"""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
RAINCLOUD = ("one soft blue-gray rain cloud with a round friendly shape, with five short slanted "
             "blue raindrops falling from it")
PUDDLE = "one flat oval light-blue puddle on the ground"

PAGES = {
    "p01_rain_falls": f"{T} standing indoors at a large window, seen from the side, watching "
                      f"{RAINCLOUD} outside the window, with a small frown. {MARGIN} {NO_EXTRA}",
    "p02_rain_go": f"{T} standing indoors at a large window, facing the window, mouth open as if "
                   f"chanting, both palms pressed to the glass. Outside is {RAINCLOUD}. {MARGIN} "
                   f"{NO_EXTRA}",
    "p03_come_later": f"{T} standing indoors at a large window, waving one hand in a friendly "
                      f"goodbye wave toward {RAINCLOUD} outside. {MARGIN} {NO_EXTRA}",
    "p04_want_play": f"{T} standing indoors at a large window, hugging a red ball to the chest, "
                     f"looking out at {RAINCLOUD} with an eager hopeful face. {MARGIN} {NO_EXTRA}",
    "p05_sun_out": f"{T} standing outdoors on plain flat green grass, pointing up with one finger "
                   f"and smiling. One big bright yellow sun with short triangular rays emerges from "
                   f"behind one small white cloud that drifts away. {MARGIN} {NO_EXTRA}",
    "p06_puddles": f"{T} kneeling on plain flat green grass, looking down at three flat oval "
                   f"light-blue puddles in a row in front of the knees, with curious wide eyes. "
                   f"There are exactly three puddles. {MARGIN} {NO_EXTRA}",
    "p07_jump": f"{T} in mid-air above {PUDDLE}, knees tucked up, arms out wide, laughing. Small "
                f"light-blue splash drops fly up around the puddle. {MARGIN} {NO_EXTRA}",
    "p08_sun_dries": f"One big bright yellow sun with short triangular rays in the upper part of "
                     f"the picture shines on {PUDDLE} on plain flat green grass. Three wavy white "
                     f"steam lines rise from the puddle. The toddler is not in the picture. "
                     f"{MARGIN} {NO_EXTRA}",
    "p09_bye_rain": f"{T} standing outdoors on plain flat green grass under one big bright yellow "
                    f"sun, waving goodbye to one small blue-gray rain cloud drifting away at the "
                    f"side, with no raindrops. {MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} standing outdoors on plain flat green grass beside {PUDDLE}, smiling at the viewer. "
         f"One big bright yellow sun with short triangular rays is on one side of the sky and one "
         f"small blue-gray rain cloud with three raindrops is on the other side. {MARGIN} {NO_EXTRA}")
