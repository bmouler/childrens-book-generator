"""Book 14: "The Little House" (Теремок). The canonical tale, in modern Russian.

A little house stands in a field. The mouse runs past, asks "Who lives in the house?", hears no
answer and runs in. The frog, the hare, the fox and the wolf each arrive, ask, hear the roll of
the residents ("I am the mouse. ..."), answer "I am the frog" and are in. All live together. Then
the bear comes: the full roll call answers him, he asks "Let me live with you!" — but he is big
and the house is small. He climbs on the roof, the house falls apart, all run out. Then all build
a new house and live together: the canonical rebuild ending (the Tolstoy text), so the tale ends
safe. Dialogue pages are recitation pages: no word cards, bigger text.
Modernized words: теремок -> домик; мышка-норушка, лягушка-квакушка, зайчик-побегайчик,
лисичка-сестричка, волк-серый бочок -> мышь, лягушка, заяц, лиса, волк.
"""
HOUSE = {"n": "house", "art": "the"}
NEW_HOUSE = {"n": "house", "adj": ["new"], "art": "the"}
FIELD = {"n": "field"}

RESIDENTS = ["mouse", "frog", "hare", "fox", "wolf"]
MOVE = {"mouse": "run", "frog": "jump", "hare": "run", "fox": "walk", "wolf": "walk", "bear": "walk"}


def the(noun: str) -> dict:
    return {"n": noun, "art": "the"}


def who_lives() -> dict:
    """Who lives in the little house? — the tale's own question, always in the present."""
    return {"subj": {"pron": "who"}, "verb": "live", "pp": ("in", HOUSE), "tense": "pres", "end": "?"}


def arrival(animal: str, art: str) -> dict:
    """Someone goes past the house: the page carries the animal's card."""
    return {"art": art, "focus": [animal],
            "clauses": [{"subj": the(animal), "verb": MOVE[animal], "adv": "past"}]}


def dialogue(animal: str, residents: list, art: str) -> dict:
    """The door dialogue: the question, the roll call, And who are you?, I am the X. No cards."""
    clauses = [who_lives()]
    clauses += [{"subj": {"pron": "I"}, "be_np": the(r), "tense": "pres"} for r in residents]
    clauses += [{"phrase": "and_who_are_you"},
                {"subj": {"pron": "I"}, "be_np": the(animal), "tense": "pres"}]
    return {"art": art, "clauses": clauses}


def runs_in(animal: str, verb: str, art: str, focus: str) -> dict:
    """The newcomer goes into the house."""
    return {"art": art, "focus": [focus],
            "clauses": [{"subj": the(animal), "verb": verb, "pp_to": ("in", HOUSE)}]}


STORY = {
    "title": "The Little House",
    "tense": "past",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_teremok"}]},
    "pages": [
        {"art": "p02_house_small", "focus": ["house"],
         "clauses": [{"subj": {"n": "house"}, "verb": "stand", "pp": ("in", FIELD)}]},
        arrival("mouse", "p01_mouse_house"),
        {"art": "p01_mouse_house",  # the question to the empty house: a recitation page
         "clauses": [who_lives(), {"subj": {"pron": "nobody"}, "verb": "answer", "neg": True}]},
        {"art": "p03_mouse_lives", "focus": ["live"],  # she is in: the next dialogues prove it
         "clauses": [{"subj": the("mouse"), "verb": "live", "pp": ("in", HOUSE)}]},
        arrival("frog", "p04_frog_comes"),
        dialogue("frog", ["mouse"], "p04_frog_comes"),
        runs_in("frog", "jump", "p04b_frog_jumps", "jump"),
        arrival("hare", "p05_hare_comes"),
        dialogue("hare", ["mouse", "frog"], "p05_hare_comes"),
        arrival("fox", "p06_fox_comes"),
        dialogue("fox", ["mouse", "frog", "hare"], "p06_fox_comes"),
        arrival("wolf", "p07_wolf_comes"),
        dialogue("wolf", ["mouse", "frog", "hare", "fox"], "p07_wolf_comes"),
        {"art": "p08_all_live", "focus": ["live", "house"],
         "clauses": [{"subj": {"pron": "all"}, "verb": "live", "pp": ("in", HOUSE), "adv": "together"}]},
        arrival("bear", "p09_bear_comes"),
        {"art": "p09a_rollcall",  # the full roll call answers the bear: a recitation page
         "clauses": [who_lives()] +
                    [{"subj": {"pron": "I"}, "be_np": the(r), "tense": "pres"} for r in RESIDENTS]},
        {"art": "p09_bear_comes",  # the bear answers and asks his question: a recitation page
         "clauses": [{"phrase": "and_who_are_you"},
                     {"subj": {"pron": "I"}, "be_np": the("bear"), "tense": "pres"},
                     {"phrase": "let_me_live"}]},
        {"art": "p09b_bear_big", "focus": ["big", "small"],
         "clauses": [{"subj": the("bear"), "pred": "big"},
                     {"subj": HOUSE, "pred": "small", "end": "!"}]},
        {"art": "p10_bear_sits", "focus": ["roof"],
         "clauses": [{"subj": the("bear"), "verb": "climb", "pp_to": ("on", the("roof"))}]},
        {"art": "p11_house_breaks", "focus": ["fall_apart"],
         "clauses": [{"subj": HOUSE, "verb": "fall_apart", "end": "!"}]},
        {"art": "p12_all_run", "focus": ["run"],
         "clauses": [{"subj": {"pron": "all"}, "verb": "run", "pp": ("out_of", HOUSE)}]},
        {"art": "p13_all_build", "focus": ["build"],
         "clauses": [{"subj": {"pron": "all"}, "verb": "build", "obj": NEW_HOUSE}]},
        {"art": "p14_all_live_new", "focus": ["new"],
         "clauses": [{"subj": {"pron": "all"}, "verb": "live", "pp": ("in", NEW_HOUSE),
                      "adv": "together"}]},
        {"art": "p15_all_happy", "focus": ["be_happy"],
         "clauses": [{"subj": {"pron": "all"}, "verb": "be_happy", "end": "!"}]},
    ],
}
