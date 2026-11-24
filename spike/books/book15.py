"""Book 15: "The Speckled Hen" (Курочка Ряба). The canonical tale, in modern Russian.

Grandpa and Grandma live with their speckled hen. She lays an egg: not a plain one, a golden one.
Grandpa beats and beats, Grandma beats and beats — neither breaks it. The mouse runs past, waves
its little tail, and the egg falls and shatters. Grandpa and Grandma cry. The hen says: do not cry,
I will lay you an egg — not a golden one, a plain one. She does, and Grandpa and Grandma are happy.
Modernized words: дед да баба -> дедушка и бабушка, яичко -> яйцо, кудахчет -> сказала (the hen
simply speaks), мышка -> мышь. "Хвостик" stays: it is the tale's own little word, not an archaism.
"""
HEN = {"n": "hen", "art": "the"}
EGG = {"n": "egg", "art": "the"}
GRANDPARENTS = ["grandpa", "grandma"]

STORY = {
    "title": "The Speckled Hen",
    "tense": "past",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_hen"}]},
    "pages": [
        {"art": "p00_once",  # the opener: a recitation page, no cards
         "clauses": [{"phrase": "once_upon"}, {"phrase": "once_hen"}]},
        {"art": "p03_hen_lays", "focus": ["hen", "egg"],
         "clauses": [{"subj": HEN, "verb": "lay", "obj": {"n": "egg"}}]},
        {"art": "p04_egg_golden", "focus": ["golden"],
         "clauses": [{"phrase": "not_plain_golden"}]},
        {"art": "p05a_grandpa_beats", "focus": ["beat"],
         "clauses": [{"phrase": "beat_grandpa"}]},
        {"art": "p05b_grandma_beats", "focus": ["beat"],
         "clauses": [{"phrase": "beat_grandma"}]},
        {"art": "p06_mouse_runs", "focus": ["mouse"],
         "clauses": [{"subj": {"n": "mouse"}, "verb": "run", "adv": "past"}]},
        {"art": "p06_mouse_runs", "focus": ["tail"],  # the same moment, one beat later
         "clauses": [{"subj": {"n": "mouse", "art": "the"}, "verb": "wave",
                      "instr": {"n": "tail"}}]},
        {"art": "p07_egg_breaks", "focus": ["break"],
         "clauses": [{"subj": EGG, "verb": "tumble"}, {"subj": EGG, "verb": "break"}]},
        {"art": "p08b_grandparents_sad", "focus": ["cry"],
         "clauses": [{"subj": ["grandpa", "grandma"], "verb": "cry"}]},
        {"art": "p09b_hen_speaks",  # the hen's promise: a recitation page, no cards
         "clauses": [{"phrase": "dont_cry"}, {"phrase": "i_will_lay_plain"}]},
        {"art": "p09_hen_lays_again", "focus": ["egg"],
         "clauses": [{"subj": HEN, "verb": "lay", "obj": {"n": "egg"}}]},
        {"art": "p10_egg_white", "focus": ["white"],
         "clauses": [{"subj": EGG, "pred": "white", "end": "!"}]},
        {"art": "p11_all_happy", "focus": ["happy"],
         "clauses": [{"subj": GRANDPARENTS, "pred": "happy", "end": "!"}]},
    ],
}
