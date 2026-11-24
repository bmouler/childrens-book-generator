"""Book 13 art prompts: Kolobok (Колобок). The page names match the `art` keys of book13.py.
No toddler hero: the folk-tale cast gets its own character sheet, generated first into
out/book13/charsheet.png and used as the reference picture of every page.
"""

KO = ("Kolobok, a round yellow bun the size of a child's head, with two small black dot eyes, "
      "pink cheeks and a small happy smile")
GP = "Grandpa, an old man with a round friendly face, a gray beard and mustache, a red shirt and brown pants"
GM = "Grandma, an old woman with gray hair in a bun, round glasses, a blue dress and a white apron"
HARE = "a gray hare with long ears with pink insides, standing on its hind legs"
WOLF = "a big gray wolf with a lighter gray muzzle, standing on four legs"
BEAR = "a big brown bear with round ears and a tan muzzle, standing on four legs"
FOX = "an orange fox with white cheeks, a white chest and a bushy tail with a white tip"
PATH = "on a simple forest path with green grass and two round green trees"
NO_EXTRA = "No other objects, no decoration."
MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NOTES = "Three small round musical notes float in the air above Kolobok."

CHARSHEET = (
    "Character reference picture for a folk-tale picture book. Show each of these characters once, "
    "full body, standing side by side in one row on a plain white background with generous space around "
    f"them: {KO}; {GM}; {HARE}; {WOLF}; {BEAR}; {FOX}. Friendly faces, front view."
)
KEEP = (
    "Keep the same character designs from the reference picture: the same shapes, colours, "
    "line weight and flat vector style."
)

PAGES = {
    "p00_once": f"Show {GP} and {GM} standing side by side in front of a small wooden house with a "
                f"blue window. Both wave at the viewer and smile. Kolobok is not in the picture. "
                f"{MARGIN} {NO_EXTRA}",
    "p01a_grandpa_hungry": "Show Grandpa, an old man with a round friendly face, a gray beard and "
                           "mustache, a red shirt and brown pants, standing at an empty wooden table, "
                           f"holding his round belly with both hands and looking down at it sadly. "
                           f"{MARGIN} {NO_EXTRA}",
    "p01_grandma_bakes": f"Show {GM} standing at a wooden table, holding a round baking tray in both "
                         f"hands. {KO} sits on the tray, smiling. {NO_EXTRA}",
    "p02_window": f"Show {KO} sitting on the wooden windowsill of a small wooden house with an open "
                  f"blue window, smiling at the viewer. {MARGIN} {NO_EXTRA}",
    "p03_kolobok_rolls": f"Show {KO} rolling {PATH}, with three curved motion lines behind him. "
                         f"He smiles. {NO_EXTRA}",
    "p05_meets_hare": f"Show {KO} {PATH}, facing {HARE}. The hare tilts its head and looks at Kolobok "
                      f"with curious eyes. {NO_EXTRA}",
    "p05b_hare_hungry": f"Show {KO} in the middle of a simple forest path with green grass and two "
                        f"round green trees, singing with his mouth open in a big smile. {NOTES} At the "
                        f"side, a gray hare with long ears with pink insides sits up and licks its "
                        f"lips, watching Kolobok. {MARGIN} {NO_EXTRA}",
    "song_hare": f"Show {KO} {PATH}, singing with his mouth open in a big smile. {NOTES} Beside him "
                 f"{HARE} sits on the grass and listens, tilting its head. {MARGIN} {NO_EXTRA}",
    "p06_meets_wolf": f"Show {KO} {PATH}, facing {WOLF}. The wolf looks at Kolobok with curious eyes. "
                      f"{NO_EXTRA}",
    "p06b_wolf_hungry": f"Show {KO} in the middle of a simple forest path with green grass and two "
                        f"round green trees, singing with his mouth open in a big smile. {NOTES} At the "
                        f"side, {WOLF} licks its lips, watching Kolobok. {MARGIN} {NO_EXTRA}",
    "song_wolf": f"Show {KO} {PATH}, singing with his mouth open in a big smile. {NOTES} Beside him "
                 f"{WOLF} sits on the grass and listens, its ears up. {MARGIN} {NO_EXTRA}",
    "p07_meets_bear": f"Show {KO} {PATH}, facing {BEAR}. The bear looks down at Kolobok with curious "
                      f"eyes. {NO_EXTRA}",
    "p07b_bear_hungry": f"Show {KO} in the middle of a simple forest path with green grass and two "
                        f"round green trees, singing with his mouth open in a big smile. {NOTES} At the "
                        f"side, {BEAR} licks its lips, watching Kolobok. {MARGIN} {NO_EXTRA}",
    "song_bear": f"Show {KO} {PATH}, singing with his mouth open in a big smile. {NOTES} Beside him "
                 f"{BEAR} sits on the grass and listens, tilting its huge head. {MARGIN} {NO_EXTRA}",
    "p08_meets_fox": f"Show {KO} {PATH}, facing {FOX}. The fox smiles with half-closed eyes. {NO_EXTRA}",
    "p08c_fox_clever": f"Show {FOX} sitting {PATH}, tapping the side of her head with one front paw, "
                       f"with a sly half-closed grin. Kolobok is not in the picture. {MARGIN} "
                       f"{NO_EXTRA}",
    "p08d_kolobok_sits": f"Show {FOX} sitting {PATH}, head tilted up. {KO} sits balanced on the tip of "
                         f"the fox's nose, looking down with nervous wide eyes. The fox grins with "
                         f"half-closed eyes. {NO_EXTRA}",
    "p09_fox_eats": f"Show {FOX} sitting {PATH}, tossing {KO} high into the air above her open smiling "
                    f"mouth with one front paw. Kolobok is in the air with wide surprised eyes. {NO_EXTRA}",
}
COVER = f"Show {KO} {PATH}, smiling at the viewer, centered and large. {NO_EXTRA}"
KEEP_FOR = {**{name: KEEP for name in PAGES}, "cover": KEEP}
