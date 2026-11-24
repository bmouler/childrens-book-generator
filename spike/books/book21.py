"""Book 21: "On the Farm" — Old MacDonald (У дедушки ферма).

Four animals live on Grandpa's farm, and each says its sound: the cow moos (му-му), the pig oinks
(хрю-хрю), the duck quacks (кря-кря) and the dog woofs (гав-гав). A sound refrain follows each
pair, and everyone sings together at the end. The sound words match book 8 exactly.
"""


def a(noun: str) -> dict:
    return {"n": noun}  # first mention: the engine picks "a"


def the(noun: str) -> dict:
    return {"n": noun, "art": "the"}


FARM = ("on", the("farm"))


def lives(page: str, animal: str) -> dict:
    """A cow lives on the farm. -> Корова живёт на ферме."""
    return {"art": page, "focus": [animal],
            "clauses": [{"subj": a(animal), "verb": "live", "pp": FARM}]}


def says(page: str, animal: str, sound_verb: str) -> dict:
    """The cow says: moo-moo! -> Корова говорит: му-му!"""
    return {"art": page, "focus": [sound_verb],
            "clauses": [{"phrase": f"says_{animal}"}]}


STORY = {
    "title": "On the Farm",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_farm"}]},
    "pages": [
        {"art": "p01_grandpa_farm", "focus": ["farm"],
         "clauses": [{"phrase": "grandpa_farm"}]},
        lives("p02_cow_lives", "cow"),
        says("p03_cow_says", "cow", "moo"),
        lives("p04_pig_lives", "pig"),
        says("p05_pig_says", "pig", "oink"),
        {"art": "p06_refrain",  # Moo-moo here, oink-oink there: a recitation page
         "clauses": [{"phrase": "refrain_farm_1"}]},
        lives("p07_duck_lives", "duck"),
        says("p08_duck_says", "duck", "quack"),
        lives("p09_dog_lives", "dog"),
        says("p10_dog_says", "dog", "bark"),
        {"art": "p11_refrain",
         "clauses": [{"phrase": "refrain_farm_2"}]},
        {"art": "p12_finale", "focus": ["sing"],
         "clauses": [{"phrase": "farm_finale"}]},
    ],
}
