"""Book 19: "Little Star" — Twinkle, Twinkle, Little Star (Мерцай, мерцай, звёздочка), as a
bedtime book.

The star twinkles high in the sky, it is small and bright, then it gets sleepy — and so do we.
The last page sends the child to sleep with the star: a book for the bedtime slot, when naps and
night sleep consolidate new words.
"""


def the(noun: str) -> dict:
    return {"n": noun, "art": "the"}


STORY = {
    "title": "Little Star",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_star"}]},
    "pages": [
        {"art": "p01_twinkle",  # the song: a recitation page
         "clauses": [{"phrase": "twinkle_star"}]},
        {"art": "p02_high",
         "clauses": [{"phrase": "high_in_sky"}]},
        {"art": "p03_small_bright", "focus": ["star"],
         "clauses": [{"subj": the("star"), "pred": ["small", "bright"], "end": "!"}]},
        {"art": "p04_many_stars", "focus": ["star"],
         "clauses": [{"imp": "look", "pp": ("at", {"n": "star", "num": "pl"}), "end": "!"}]},
        {"art": "p05_wants_sleep",
         "clauses": [{"phrase": "star_wants_sleep"}]},
        {"art": "p06_sleep_star",
         "clauses": [{"phrase": "sleep_star"}]},
        {"art": "p07_good_night",
         "clauses": [{"phrase": "good_night"}]},
        {"art": "p08_we_sleep", "focus": ["sleep"],
         "clauses": [{"phrase": "we_sleep_too"}]},
    ],
}
