"""Book 28 art: The Melting Race! Two ice cubes: one on a sunny patch, one in the shade of
the box. The sun patch cube shrinks page by page; the shaded one keeps its shape."""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
FLOOR = "on a plain soft-green floor"
SUN = "one big bright yellow sun with short triangular rays and a small friendly smile"
BOX = "one open brown cardboard box"

PAGES = {
    "p01_ice": f"{T} kneeling {FLOOR}, holding one clear blue-white ice cube in both cupped "
                f"hands, looking at it closely. {MARGIN} {NO_EXTRA}",
    "p02_sun": f"{T} kneeling {FLOOR}, placing one clear ice cube down on a bright warm patch of "
               f"light, {SUN} shining above. {MARGIN} {NO_EXTRA}",
    "p03_shade": f"{T} kneeling {FLOOR}, placing a second clear ice cube in the cool shadow cast "
                 f"by {BOX}, no sun on that side. {MARGIN} {NO_EXTRA}",
    "p04_guess": f"{T} kneeling {FLOOR} between the sunny ice cube and the shaded one, one "
                 f"finger on the chin, thinking face. {MARGIN} {NO_EXTRA}",
    "p05_sun_hot": f"A close view of the sunny patch {FLOOR}: one clear ice cube on warm bright "
                   f"grass with {SUN} above it. {MARGIN} {NO_EXTRA}",
    "p06_shadow_cold": f"A close view of the cool shadow under {BOX}: one clear ice cube on the "
                       f"shadowed grass, calm and blue-grey light. {MARGIN} {NO_EXTRA}",
    "p07_wait": f"{T} sitting {FLOOR} between the two ice cubes, hands folded in the lap, "
                f"patient waiting face. {MARGIN} {NO_EXTRA}",
    "p08_wait_wait": f"{T} lying on the tummy {FLOOR}, chin on hands, watching the two ice cubes "
                     f"with sleepy patience. {MARGIN} {NO_EXTRA}",
    "p09_so": f"The sunny ice cube is now half melted into a wide puddle while {SUN} beams on "
              f"it, the toddler from the reference picture pointing at it beside. {MARGIN} "
              f"{NO_EXTRA}",
    "p10_shade_slow": f"In the cool shadow of {BOX}, the second ice cube still stands whole and "
                      f"tall with only a tiny puddle, the toddler pointing at it. {MARGIN} "
                      f"{NO_EXTRA}",
    "p11_water_back": f"{T} kneeling {FLOOR}, touching a wide clear puddle of water where the "
                      f"sunny ice cube was, small splash. {MARGIN} {NO_EXTRA}",
    "p12_see": f"{T} standing {FLOOR} between the wide puddle and the still-whole shaded cube, "
               f"arms out in a proud see moment. {MARGIN} {NO_EXTRA}",
    "p13_know": f"{T} standing {FLOOR}, one index finger raised high, bright knowing smile, the "
                f"two patches behind. {MARGIN} {NO_EXTRA}",
    "p14_touch": f"{T} kneeling {FLOOR}, dipping one finger into the wide clear puddle, curious "
                 f"face. {MARGIN} {NO_EXTRA}",
    "p15_cold": f"{T} kneeling {FLOOR} by the puddle, hugging own shoulders with a small brr "
                f"face, breath puff. {MARGIN} {NO_EXTRA}",
    "p16_end": f"{T} standing {FLOOR} with one finger up and {SUN} above, calm closing smile. "
               f"{MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} kneeling {FLOOR} between one ice cube in bright sun and one in the shadow of "
         f"{BOX}, finger on the chin, guessing face. {MARGIN} {NO_EXTRA}")
