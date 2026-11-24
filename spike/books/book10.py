"""Book 10: "A Seed Grows". Put a seed in soil, give water, wait, watch it grow. A real sequence of care
and time: a seed, a sprout, a plant, a flower.
"""
WE = {"pron": "we"}
THE_SEED = {"n": "seed", "art": "the"}
THE_PLANT = {"n": "plant", "art": "the"}
WATER = {"n": "water", "art": ""}

STORY = {
    "title": "A Seed Grows",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_seed_grows"}]},
    "pages": [
        {"art": "p01_see_seed", "focus": ["seed"], "clauses": [{"subj": WE, "verb": "see", "obj": "seed"}]},
        {"art": "p02_seed_soil", "focus": ["seed", "soil"],
         "clauses": [{"subj": WE, "verb": "put", "obj": THE_SEED, "pp_to": ["in", {"n": "soil", "art": "the"}]}]},
        {"art": "p03_water_seed", "focus": ["water", "seed"],
         "clauses": [{"subj": WE, "verb": "give", "obj": WATER, "io": THE_SEED}]},
        {"art": "p04_sun_warm", "focus": ["sun", "warm"],
         "clauses": [{"subj": {"n": "sun", "art": "the"}, "pred": "warm"}]},
        {"art": "p05_wait", "focus": ["wait"], "clauses": [{"subj": WE, "verb": "wait"}]},
        {"art": "p06_seed_grows", "focus": ["grow"], "clauses": [{"subj": THE_SEED, "verb": "grow", "end": "!"}]},
        {"art": "p07_water_plant", "focus": ["water", "plant"],
         "clauses": [{"subj": WE, "verb": "give", "obj": WATER, "io": THE_PLANT}]},
        {"art": "p08_plant_grows", "focus": ["plant", "grow"],
         "clauses": [{"subj": THE_PLANT, "verb": "grow", "end": "!"}]},
        {"art": "p09_see_flower", "focus": ["flower"],
         "clauses": [{"subj": WE, "verb": "see", "obj": "flower", "end": "!"}]},
        {"art": "p10_now_you", "focus": ["try"], "clauses": [{"phrase": "now_you_try"}]},
    ],
}
