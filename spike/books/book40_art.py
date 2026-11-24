"""Book 40 art: Where the Balloon Flew. The page names match the `art` keys of book40.py.
A bear cub loses a red balloon, cries, and is comforted.
"""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same bear cub from the reference picture"
CHARSHEET = (
    "A character reference picture of one small bear cub for a children's picture book: a round "
    "soft brown bear cub with small round ears, a light tan muzzle, big dark eyes and a short "
    "stubby tail. Shown once, full body, friendly front view, centered on a plain white background "
    "with generous empty space on every side."
)
BALLOON = "one round red balloon on a long thin string"
PAGES = {
    "p01_balloon": f"{T} walking on plain flat green grass holding {BALLOON} tight in one paw, "
                   f"looking up at it with a smile. {MARGIN} {NO_EXTRA}",
    "p02_sky": f"{T} standing on plain flat green grass with the empty paw raised to the empty "
               f"string, looking straight up at a tiny red balloon dot high in a pale blue sky. "
               f"{MARGIN} {NO_EXTRA}",
    "p03_heavy": f"{T} standing on plain flat green grass with head lowered and both arms hanging "
                 f"down, mouth turned down, one string end in the paw. {MARGIN} {NO_EXTRA}",
    "p04_mother": f"{T} sitting on plain flat green grass beside one larger mother bear who strokes "
                  f"his back, the cub's head resting against her side, one big tear at the eye. "
                  f"{MARGIN} {NO_EXTRA}",
    "p05_dry": f"{T} standing on plain flat green grass wiping one eye with a paw, a small smile "
               f"already on the face, one dry tear line left on the cheek. {MARGIN} {NO_EXTRA}",
    "p06_again": f"{T} standing on plain flat green grass holding a spare {BALLOON}, smiling at the "
                 f"viewer, one small red balloon dot still high in the sky. {MARGIN} {NO_EXTRA}",
}
COVER = f"{T} on plain flat green grass watching {BALLOON} float up out of reach. {MARGIN} {NO_EXTRA}"