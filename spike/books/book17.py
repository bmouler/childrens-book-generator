"""Book 17: "Rain, Go Away!" — the rain chant, then the payoff: puddles.

Russian: «Дождик, дождик, уходи! Приходи в другой день!», the chant every Russian child knows.
The chant pages are recitation pages. Then the sun comes out, the toddler jumps in puddles, and
the sun dries them: the same science as books 9 and 11, sung.
"""
WE = {"pron": "we"}


def the(noun: str, num: str | None = None) -> dict:
    spec = {"n": noun, "art": "the"}
    if num:
        spec["num"] = num
    return spec


STORY = {
    "title": "Rain, Go Away!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_rain_go"}]},
    "pages": [
        {"art": "p01_rain_falls", "focus": ["rain"],
         "clauses": [{"subj": the("rain"), "verb": "fall", "end": "!"}]},
        {"art": "p02_rain_go",  # the chant: a recitation page
         "clauses": [{"phrase": "rain_go_away"}]},
        {"art": "p03_come_later",
         "clauses": [{"phrase": "come_another_day"}]},
        {"art": "p04_want_play",
         "clauses": [{"phrase": "want_to_play"}]},
        {"art": "p05_sun_out",
         "clauses": [{"phrase": "sun_comes_out"}]},
        {"art": "p06_puddles", "focus": ["puddle"],
         "clauses": [{"imp": "look", "pp": ("at", the("puddle", "pl")), "end": "!"}]},
        {"art": "p07_jump", "focus": ["jump"],
         "clauses": [{"subj": WE, "verb": "jump", "pp": ("in", the("puddle", "pl")), "end": "!"}]},
        {"art": "p08_sun_dries", "focus": ["sun"],
         "clauses": [{"subj": the("sun"), "verb": "dry", "obj": the("puddle", "pl")}]},
        {"art": "p09_bye_rain",
         "clauses": [{"phrase": "bye_rain"}]},
    ],
}
