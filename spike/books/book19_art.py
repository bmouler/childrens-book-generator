"""Book 19 art prompts: Little Star. The page names match the `art` keys of book19.py.
A bedtime book: soft night blue, one friendly star, and the toddler falling asleep at the end.
"""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
STAR = ("one small five-pointed yellow star with a friendly face: two black dot eyes, pink cheeks "
        "and a small smile")
WINDOW = "a large window of a child's bedroom, with a deep-blue night sky outside"

PAGES = {
    "p01_twinkle": f"{T} standing at {WINDOW}, smiling up at {STAR} in the night sky outside. "
                   f"Four tiny white sparkle marks twinkle around the star. {MARGIN} {NO_EXTRA}",
    "p02_high": f"Show a deep-blue night sky over the dark silhouette of one small house roof. "
                f"{STAR} shines high in the sky, far above the roof. The toddler is not in the "
                f"picture. {MARGIN} {NO_EXTRA}",
    "p03_small_bright": f"Show a deep-blue night sky with {STAR} in the middle, glowing with "
                        f"eight short bright rays around it. Nothing else is in the sky. {MARGIN} "
                        f"{NO_EXTRA}",
    "p04_many_stars": f"{T} standing at {WINDOW}, pointing up with one finger. The night sky "
                      f"outside is full of many small plain white five-pointed stars of different "
                      f"sizes, and {STAR} among them. {MARGIN} {NO_EXTRA}",
    "p05_wants_sleep": f"Show {STAR} in a deep-blue night sky, with sleepy half-closed eyes and a "
                       f"small yawn. Its yellow glow is softer. {MARGIN} {NO_EXTRA}",
    "p06_sleep_star": f"Show {STAR} lying on one small soft white cloud in a deep-blue night sky, "
                      f"sleeping with closed eyes. Three small light-blue Z letters float above "
                      f"the star. {MARGIN} {NO_EXTRA}",
    "p07_good_night": f"Show a calm deep-blue night sky with {STAR} sleeping on one small soft "
                      f"white cloud and one small pale-yellow crescent moon beside it. {MARGIN} "
                      f"{NO_EXTRA}",
    "p08_we_sleep": f"{T} asleep in a small bed with a light-blue blanket, eyes closed and a "
                    f"peaceful smile. Through {WINDOW} behind the bed, {STAR} shines softly. "
                    f"{MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} standing at {WINDOW}, waving one hand at {STAR} in the night sky outside. The star "
         f"smiles back. {MARGIN} {NO_EXTRA}")
