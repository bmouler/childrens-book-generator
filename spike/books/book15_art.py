"""Book 15 art prompts: The Speckled Hen (Курочка Ряба). The page names match the `art` keys of
book15.py. No toddler hero: the folk-tale cast gets its own character sheet, generated first into
out/book15/charsheet.png and used as the reference picture of every page.
"""

HEN = "a white hen with gray and black speckles on her wings, a red comb and a yellow beak"
GM = "Grandma, an old woman with gray hair in a bun, round glasses, a blue dress and a white apron"
MS = "a tiny gray mouse with big round ears"
GP = "Grandpa, an old man with a round friendly face, a gray beard and mustache, a red shirt and brown pants"
NEST = "a round brown straw nest on green grass"
GOLD = "one shiny golden egg"
NO_EXTRA = "No other objects, no decoration."
MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."

CHARSHEET = (
    "Character reference picture for a folk-tale picture book. Show each of these characters once, "
    "full body, standing side by side in one row on a plain white background with generous space around "
    f"them: {HEN}; {GM}; {MS}; and one shiny golden egg lying on the ground. Friendly faces, front view."
)
KEEP = (
    "Keep the same character designs from the reference picture: the same shapes, colours, "
    "line weight and flat vector style."
)

PAGES = {
    "p00_once": f"Show {GP} and {GM} standing side by side on green grass in front of a small wooden "
                f"house, with {HEN} pecking the grass beside them. All smile. {MARGIN} {NO_EXTRA}",
    "p03_hen_lays": f"Show {HEN} standing up from {NEST}. In the nest lies {GOLD}. {NO_EXTRA}",
    "p04_egg_golden": f"Show {GOLD} lying in {NEST}, centered and large. {NO_EXTRA}",
    "p05a_grandpa_beats": f"Show {GP} kneeling beside {NEST} with {GOLD} in it, raising one wooden "
                          f"spoon high above the egg, ready to tap it. The egg is whole and shiny. "
                          f"{MARGIN} {NO_EXTRA}",
    "p05b_grandma_beats": f"Show {GM} kneeling beside {NEST} with {GOLD} in it, raising one wooden "
                          f"spoon high above the egg, ready to tap it. The egg is whole and shiny. "
                          f"{MARGIN} {NO_EXTRA}",
    "p06_mouse_runs": f"Show {MS} running fast right past {NEST} with {GOLD} in it, with three curved "
                      f"motion lines behind the mouse. The egg tips at the edge of the nest. {NO_EXTRA}",
    "p07_egg_breaks": f"Show {GOLD} broken into two halves on green grass, with a zigzag crack on each "
                      f"half. {NO_EXTRA}",
    "p08b_grandparents_sad": f"Show {GM} and {GP} sitting side by side on green grass with drooping "
                             f"shoulders, looking down sadly, each with one big round blue tear drop "
                             f"on a cheek. {NO_EXTRA}",
    "p09b_hen_speaks": f"Show {HEN} standing tall on green grass in front of {GM} and {GP}, who sit "
                       f"side by side looking sad, each with one big round blue tear drop on a cheek. "
                       f"The hen spreads her wings a little and has her beak open, as if speaking. "
                       f"{MARGIN} {NO_EXTRA}",
    "p09_hen_lays_again": f"Show {HEN} standing up from {NEST}. In the nest lies one plain white egg. "
                          f"{NO_EXTRA}",
    "p10_egg_white": f"Show one plain white egg lying in {NEST}, centered and large. Next to the nest "
                     f"stands {HEN}, smiling with one wing raised high. {NO_EXTRA}",
    "p11_all_happy": f"Show {GM} and {GP} standing side by side on green grass behind {NEST} with one "
                     f"plain white egg in it. Both smile with wide happy eyes and wave at the viewer. "
                     f"Beside the nest stands {HEN}, smiling with both wings raised high. {NO_EXTRA}",
}
COVER = f"Show {HEN} standing beside {NEST} with {GOLD} in it, smiling at the viewer. No people, no children. {NO_EXTRA}"
KEEP_FOR = {**{name: KEEP for name in PAGES}, "cover": KEEP}
