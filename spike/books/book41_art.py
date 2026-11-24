"""Book 41 art: Grr! The Fox Cub Is Angry. The page names match the `art` keys of book41.py.
A fox cub's block tower falls, he stamps and growls, he breathes out, and he builds again.
"""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same fox cub from the reference picture"
CHARSHEET = (
    "A character reference picture of one small fox cub for a children's picture book: a small "
    "orange fox with a white chest, a white muzzle tip, big pointed ears with dark tips, a large "
    "bushy tail with a white tip and big dark eyes. Shown once, full body, friendly front view, "
    "centered on a plain white background with generous empty space on every side."
)
TOWER = "one tall tower of eight large flat coloured toy blocks"
PAGES = {
    "p01_tower": f"{T} kneeling on a plain pale floor placing the top block on {TOWER} with both "
                  f"front paws, tongue out in concentration. {MARGIN} {NO_EXTRA}",
    "p02_grr": f"{T} standing beside a fallen pile of coloured blocks, one paw stamped down, fur "
               f"bristling, tail stiff and up, mouth open in a growl. {MARGIN} {NO_EXTRA}",
    "p03_run": f"{T} running across the plain pale floor kicking one block away, blocks scattered "
               f"around, tail high, mouth open. {MARGIN} {NO_EXTRA}",
    "p04_breathe": f"{T} sitting on the floor beside one larger mother fox with a gentle face, the "
                   f"cub's chest puffed out with a big breath, eyes closed. {MARGIN} {NO_EXTRA}",
    "p05_calm": f"{T} sitting quietly on the floor with shoulders down and eyes half closed, the "
                f"blocks lying in a pile in front of him, tail loose on the floor. {MARGIN} {NO_EXTRA}",
    "p06_build": f"{T} kneeling and placing a block on a new short tower of three blocks, a calm "
                 f"small smile on the face. {MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} standing with a bristling tail beside a fallen pile of coloured blocks, mouth open "
         f"in a growl. {MARGIN} {NO_EXTRA}")