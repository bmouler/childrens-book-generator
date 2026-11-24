"""Book 21 art prompts: On the Farm (У дедушки ферма). The page names match the `art` keys of
book21.py. A folk cast like books 12 to 15: a character sheet first, then every page.
"""

GP = "Grandpa, an old man with a round friendly face, a gray beard and mustache, a red shirt and brown pants"
COW = "a white cow with big black spots, small cream horns and a pink muzzle, standing on four legs"
PIG = "a round pink pig with a curly tail and a snout, standing on four short legs"
DUCK = "a yellow duck with an orange beak and orange feet"
DOG = "a friendly brown dog with floppy ears and a wagging tail, standing on four legs"
BARN = "a small red barn with a brown gambrel roof and a white door with a red cross"
MEADOW = "on a flat green meadow"
MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."

CHARSHEET = (
    "Character reference picture for a children's picture book. Show each of these characters once, "
    "full body, standing side by side in one row on a plain white background with generous space "
    f"around them: {GP}; {COW}; {PIG}; {DUCK}; {DOG}. Friendly faces, front view."
)
KEEP = (
    "Keep the same character designs from the reference picture: the same shapes, colours, "
    "line weight and flat vector style."
)


def singing(animal_desc: str) -> str:
    return (f"{animal_desc} with its mouth wide open, singing. Three short curved sound lines in "
            f"front of the mouth")


PAGES = {
    "p01_grandpa_farm": f"Show {GP} standing {MEADOW} in front of {BARN}, waving at the viewer "
                        f"with a big smile. {MARGIN} {NO_EXTRA}",
    "p02_cow_lives": f"Show {COW} {MEADOW} in front of {BARN}, looking at the viewer with a calm "
                     f"happy face. {MARGIN} {NO_EXTRA}",
    "p03_cow_says": f"Show {singing(COW)}. The cow stands {MEADOW}. {MARGIN} {NO_EXTRA}",
    "p04_pig_lives": f"Show {PIG} {MEADOW} beside one small brown mud puddle, looking at the "
                     f"viewer with a happy face. {MARGIN} {NO_EXTRA}",
    "p05_pig_says": f"Show {singing(PIG)}. The pig stands {MEADOW}. {MARGIN} {NO_EXTRA}",
    "p06_refrain": f"Show {COW} and {PIG} standing side by side {MEADOW}, both with mouths wide "
                   f"open singing, with three short curved sound lines in front of each mouth. "
                   f"{MARGIN} {NO_EXTRA}",
    "p07_duck_lives": f"Show {DUCK} floating on one small round blue pond {MEADOW}, looking at "
                      f"the viewer. {MARGIN} {NO_EXTRA}",
    "p08_duck_says": f"Show {singing(DUCK)}. The duck floats on one small round blue pond "
                     f"{MEADOW}. {MARGIN} {NO_EXTRA}",
    "p09_dog_lives": f"Show {DOG} {MEADOW} in front of {BARN}, sitting and wagging its tail, "
                     f"looking at the viewer. {MARGIN} {NO_EXTRA}",
    "p10_dog_says": f"Show {singing(DOG)}. The dog sits {MEADOW}. {MARGIN} {NO_EXTRA}",
    "p11_refrain": f"Show {DUCK} and {DOG} side by side {MEADOW}, both with mouths wide open "
                   f"singing, with three short curved sound lines in front of each mouth. "
                   f"{MARGIN} {NO_EXTRA}",
    "p12_finale": f"Show {GP} standing {MEADOW} in front of {BARN}, with {COW}, {PIG}, {DUCK} "
                  f"and {DOG} in a row beside him, all five with open mouths singing. Five small "
                  f"round musical notes float above them. {MARGIN} {NO_EXTRA}",
}
COVER = (f"Show {COW}, {PIG}, {DUCK} and {DOG} standing side by side in a row {MEADOW} in front "
         f"of {BARN}, all looking at the viewer with happy faces. {MARGIN} {NO_EXTRA}")
KEEP_FOR = {**{name: KEEP for name in PAGES}, "cover": KEEP}
