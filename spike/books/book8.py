"""Book 8: "Animal Sounds". Listen, ask who makes the sound, then see the animal. Four animals.
Animals are real animals: they make sounds, they do not talk.
"""
WE = {"pron": "we"}
WHO = {"pron": "who"}


def asks(verb: str) -> dict:
    return {"subj": WHO, "verb": verb, "end": "?"}


def answers(animal: str, verb: str) -> dict:
    return {"subj": {"n": animal, "art": "the"}, "verb": verb, "end": "!"}


STORY = {
    "title": "Animal Sounds",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_animal_sounds"}]},
    "pages": [
        {"art": "p01_listen", "focus": ["listen"], "clauses": [{"subj": WE, "verb": "listen"}]},
        {"art": "p02_who_barks", "focus": ["who"], "clauses": [asks("bark")]},
        {"art": "p03_dog_barks", "focus": ["dog"], "clauses": [answers("dog", "bark")]},
        {"art": "p04_who_meows", "focus": ["who"], "clauses": [asks("meow")]},
        {"art": "p05_cat_meows", "focus": ["cat"], "clauses": [answers("cat", "meow")]},
        {"art": "p06_who_moos", "focus": ["who"], "clauses": [asks("moo")]},
        {"art": "p07_cow_moos", "focus": ["cow"], "clauses": [answers("cow", "moo")]},
        {"art": "p08_who_quacks", "focus": ["who"], "clauses": [asks("quack")]},
        {"art": "p09_duck_quacks", "focus": ["duck"], "clauses": [answers("duck", "quack")]},
        {"art": "p10_now_you", "focus": ["try"], "clauses": [{"phrase": "now_you_try"}]},
    ],
}
