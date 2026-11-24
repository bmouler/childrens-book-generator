"""Book 42 art: What Is That? The page names match the `art` keys of book42.py.
A squirrel cub finds a round piece of glass and sees himself in it.
"""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same squirrel cub from the reference picture"
CHARSHEET = (
    "A character reference picture of one small squirrel cub for a children's picture book: a small "
    "red-brown squirrel with a white belly, a very big curved fluffy tail, small tufted ears and big "
    "round dark eyes. Shown once, full body, friendly front view, centered on a plain white "
    "background with generous empty space on every side."
)
GLASS = "one small round clear glass disc like a mirror"
PAGES = {
    "p01_freeze": f"{T} standing still on a big brown tree branch high above the ground, head "
                   f"lowered, looking down over the edge at plain flat green grass below. "
                   f"{MARGIN} {NO_EXTRA}",
    "p02_peek": f"{T} hanging head-down on the tree trunk, neck stretched out and eyes very round, "
                f"looking at {GLASS} lying on the grass below. {MARGIN} {NO_EXTRA}",
    "p03_glass": f"{T} sitting on plain flat green grass holding {GLASS} up in both front paws, "
                 f"eyes wide, the small reflection of a squirrel's face visible in the glass. "
                 f"{MARGIN} {NO_EXTRA}",
    "p04_self": f"{T} sitting on the grass and looking straight into {GLASS} close to his face, "
                f"eyes wide, the glass showing a clear small squirrel face looking back. {MARGIN} "
                f"{NO_EXTRA}",
    "p05_laugh": f"{T} sitting on the grass and laughing with one paw over the mouth, {GLASS} held "
                 f"in the other paw, tail curled up beside him. {MARGIN} {NO_EXTRA}",
    "p06_mother": f"{T} sitting beside one larger mother squirrel on the grass, both looking down "
                  f"into {GLASS} together, tails touching. {MARGIN} {NO_EXTRA}",
}
COVER = f"{T} sitting on plain flat green grass holding {GLASS} to the eye with a wide astonished look. {MARGIN} {NO_EXTRA}"