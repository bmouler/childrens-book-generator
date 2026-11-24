"""Book 18 art prompts: The Little Spider (Паучок). The page names match the `art` keys of
book18.py. No toddler hero: the spider gets its own character sheet, generated first into
out/book18/charsheet.png and used as the reference picture of every page.
"""

SPIDER = ("a small round dark-gray spider the size of a child's fist, with a friendly smiling face, "
          "two big white eyes and eight thin bent legs")
SUN = "one big bright yellow sun with short triangular rays and a small friendly smile"
CLOUD = "one soft blue-gray rain cloud with a round friendly shape"
PIPE = ("one straight white waterspout pipe running down the side of a simple light-beige house "
        "wall, vertical, with a small opening at the bottom")
MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."

CHARSHEET = (
    "Character reference picture for a children's picture book. Show each of these characters once, "
    "full body, side by side in one row on a plain white background with generous space around "
    f"them: {SPIDER}; {SUN}; {CLOUD}. Friendly faces, front view."
)
KEEP = (
    "Keep the same character designs from the reference picture: the same shapes, colours, "
    "line weight and flat vector style."
)

PAGES = {
    "p01_climbs": f"Show {SPIDER} climbing {PIPE}, halfway up, facing up. The spider's legs grip "
                  f"the pipe. {MARGIN} {NO_EXTRA}",
    "p02_up_pipe": f"Show {SPIDER} near the top of {PIPE}, climbing up with three short curved "
                   f"motion lines behind it. {MARGIN} {NO_EXTRA}",
    "p03_rain_came": f"Show {CLOUD} above {PIPE}, with five short slanted blue raindrops falling "
                     f"from the cloud onto the pipe. The spider sits on the pipe, looking up with "
                     f"worried wide eyes. {MARGIN} {NO_EXTRA}",
    "p04_washes": f"Show a stream of light-blue water gushing from the bottom opening of {PIPE}, "
                  f"with {SPIDER} tumbling inside the stream with wide surprised eyes, legs spread. "
                  f"{MARGIN} {NO_EXTRA}",
    "p05_sun_out": f"Show {SUN} emerging from behind {CLOUD}, which drifts away with no raindrops. "
                   f"Below them is {PIPE}, wet with two small light-blue drips. The spider is not "
                   f"in the picture. {MARGIN} {NO_EXTRA}",
    "p06_dries": f"Show {SUN} shining on a small light-blue puddle at the bottom of {PIPE}. Three "
                 f"wavy white steam lines rise from the puddle. The spider is not in the picture. "
                 f"{MARGIN} {NO_EXTRA}",
    "p07_up_again": f"Show {SPIDER} climbing {PIPE} again, halfway up, with three short curved "
                    f"motion lines behind it and a determined happy face. {MARGIN} {NO_EXTRA}",
    "p08_in_sun": f"Show {SPIDER} sitting on a warm dry light-beige spot at the bottom of {PIPE}, "
                  f"basking with closed happy eyes, with {SUN} above. {MARGIN} {NO_EXTRA}",
}
COVER = (f"Show {SPIDER} sitting on {PIPE} halfway up, smiling at the viewer, with {SUN} in the "
         f"upper part of the picture. {MARGIN} {NO_EXTRA}")
KEEP_FOR = {**{name: KEEP for name in PAGES}, "cover": KEEP}
