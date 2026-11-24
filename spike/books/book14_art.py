"""Book 14 art prompts: The Little House (Теремок). The page names match the `art` keys of book14.py.
No toddler hero: the folk-tale cast gets its own character sheet, generated first into
out/book14/charsheet.png and used as the reference picture of every page.
"""

MS = "a tiny gray mouse with big round ears"
FR = "a small green frog with big round eyes on top of its head"
HARE = "a gray hare with long ears with pink insides, standing on its hind legs"
FOX = "an orange fox with white cheeks, a white chest and a bushy tail with a white tip"
WOLF = "a big gray wolf with a lighter gray muzzle, standing on four legs"
BEAR = "a big brown bear with round ears and a tan muzzle, standing on four legs"
HOUSE = ("a little wooden house with brown plank walls, a triangular dark-red roof, one blue window and "
         "a brown door, standing on a green meadow")
NO_EXTRA = "No other objects, no decoration."
MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."

CHARSHEET = (
    "Character reference picture for a folk-tale picture book. Show each of these characters once, "
    "full body, standing side by side in one row on a plain white background with generous space around "
    f"them: {MS}; {FR}; {HARE}; {FOX}; {WOLF}; {BEAR}; and {HOUSE}. Friendly faces, front view."
)
KEEP = (
    "Keep the same character designs from the reference picture: the same shapes, colours, "
    "line weight and flat vector style."
)

PAGES = {
    "p01_mouse_house": f"Show {MS} standing at the left side, looking at {HOUSE} at the right side, "
                       f"with curious wide eyes. {NO_EXTRA}",
    "p02_house_small": f"Show {HOUSE}, small in the middle of the large green meadow, with two tall round "
                       f"green trees far behind it. The house looks tiny. No animals. {NO_EXTRA}",
    "p03_mouse_lives": f"Show {HOUSE}. A tiny gray mouse with big round ears looks out of its blue window, "
                       f"smiling and waving one paw. {NO_EXTRA}",
    "p04_frog_comes": f"Show {FR} hopping toward {HOUSE}, with two small curved motion lines behind it. "
                      f"{NO_EXTRA}",
    "p04b_frog_jumps": f"Show {FR} in mid-air, hopping through the open brown door of {HOUSE}, with "
                       f"three curved motion lines behind it and a big happy smile. The tiny gray "
                       f"mouse with big round ears watches from the blue window. {MARGIN} {NO_EXTRA}",
    "p05_hare_comes": f"Show {HARE} walking toward {HOUSE}. {NO_EXTRA}",
    "p06_fox_comes": f"Show {FOX} walking toward {HOUSE}, tail held high. {NO_EXTRA}",
    "p07_wolf_comes": f"Show {WOLF} walking toward {HOUSE}. {NO_EXTRA}",
    "p08_all_live": f"Show {HOUSE}. The tiny gray mouse and the small green frog look out of its blue "
                    f"window together, and {HARE}, {FOX} and {WOLF} sit on the grass in front of its brown "
                    f"door. All five smile. There are exactly five animals, no people, no children, no boy. {NO_EXTRA}",
    "p09_bear_comes": f"Show {BEAR} walking toward {HOUSE}. The bear is much bigger than the house. "
                      f"{NO_EXTRA}",
    "p09a_rollcall": f"Show {HOUSE}. {MS}, {FR}, {HARE}, {FOX} and {WOLF} crowd at its blue window "
                     f"and brown door, all looking out, and {BEAR} stands in front of the house "
                     f"facing them, much bigger than the house. {MARGIN} {NO_EXTRA}",
    "p09b_bear_big": f"Show {BEAR} standing on its hind legs right beside {HOUSE}. The bear towers "
                     f"over the house, and the house's roof reaches only the bear's round belly. "
                     f"{MARGIN} {NO_EXTRA}",
    "p10_bear_sits": f"Show {BEAR} sitting on top of the roof of {HOUSE}. The house is much smaller than "
                     f"the bear and its walls tilt a little under him. The bear looks surprised. {NO_EXTRA}",
    "p11_house_breaks": f"Show {HOUSE} broken: its brown plank walls tilt outward, its triangular dark-red "
                        f"roof has slid off to one side onto the grass, and two zigzag crack lines run "
                        f"across the walls. In front stand {MS}, {FR}, {HARE}, {FOX} and {WOLF} with wide "
                        f"surprised eyes. The big brown bear sits beside the house, scratching the back of "
                        f"its head with one paw. {NO_EXTRA}",
    "p12_all_run": f"Show {MS}, {FR}, {HARE}, {FOX}, {WOLF} and {BEAR} running away from the broken "
                   f"little wooden house toward the right side, with three curved motion lines behind "
                   f"them. The broken house with its slid-off dark-red roof stands at the left side. "
                   f"{NO_EXTRA}",
    "p13_all_build": f"Show everyone building a new little wooden house on a green meadow: {BEAR} lifts "
                     f"the triangular dark-red roof from above, {HARE} and {WOLF} hold a brown plank "
                     f"wall upright, {FOX} holds the brown door, and {MS} and {FR} watch from the grass. "
                     f"The new house is whole. {NO_EXTRA}",
    "p14_all_live_new": f"Show a new little wooden house with brown plank walls, a triangular dark-red "
                        f"roof, one blue window and a brown door, standing on a green meadow. {MS} and "
                        f"{FR} look out of the blue window together, {HARE}, {FOX} and {WOLF} sit on "
                        f"the grass in front of the brown door, and {BEAR} stands beside the house. "
                        f"All six wave at the viewer and smile. {NO_EXTRA}",
    "p15_all_happy": f"Show {MS}, {FR}, {HARE}, {FOX}, {WOLF} and {BEAR} dancing for joy in front of "
                     f"a new little wooden house with brown plank walls, a triangular dark-red roof, "
                     f"one blue window and a brown door: the hare and the frog jump in the air, the "
                     f"others clap or wave, all six smile with closed happy eyes. {MARGIN} {NO_EXTRA}",
}
COVER = f"Show {HOUSE} with a tiny gray mouse with big round ears looking out of its blue window and " \
        f"waving one paw. {NO_EXTRA}"
KEEP_FOR = {**{name: KEEP for name in PAGES}, "cover": KEEP}
