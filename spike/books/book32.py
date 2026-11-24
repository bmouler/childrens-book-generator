"""Book 32: "A Seed Grows All Year Long!" — age 4, one year, four seasons.

Winter sleeps, spring wakes and drinks, summer grows tall, autumn makes new seeds.
The wind carries them, they sleep in the soil, and then: опять зима. The circle closes.
"""

STORY = {
    "title": "A Seed Grows All Year Long!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_seed_year"}]},
    "pages": [
        {"art": "p01_winter", "focus": ["winter"],
         "clauses": [{"phrase": "it_winter"}]},
        {"art": "p02_sleep", "focus": ["seed", "sleep"],
         "clauses": [{"subj": "seed", "verb": "sleep"}]},
        {"art": "p03_spring", "focus": ["spring"],
         "clauses": [{"phrase": "it_spring"}]},
        {"art": "p04_wake", "focus": ["wake"],
         "clauses": [{"subj": "seed", "verb": "wake"}]},
        {"art": "p05_water", "focus": ["give"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "give",
                      "obj": {"n": "water", "art": ""}, "io": "seed"}]},
        {"art": "p06_grow", "focus": ["grow"],
         "clauses": [{"subj": "seed", "verb": "grow"}]},
        {"art": "p07_sun", "focus": ["sun"],
         "clauses": [{"subj": {"n": "sun", "art": "the"}, "verb": "shine"}]},
        {"art": "p08_rain", "focus": ["rain"],
         "clauses": [{"subj": {"n": "rain", "art": "the"}, "verb": "fall"}]},
        {"art": "p09_summer", "focus": ["summer"],
         "clauses": [{"phrase": "it_summer"}]},
        {"art": "p10_plant_big", "focus": ["plant"],
         "clauses": [{"pred": "big", "subj": "plant"}]},
        {"art": "p11_grow_grow",  # and grows, and grows: a recitation page
         "clauses": [{"subj": "plant", "verb": "grow"},
                     {"subj": "plant", "verb": "grow"}]},
        {"art": "p12_autumn", "focus": ["autumn"],
         "clauses": [{"phrase": "it_autumn"}]},
        {"art": "p13_seeds", "focus": ["flower"],
         "clauses": [{"subj": "flower", "verb": "make",
                      "obj": {"n": "seed", "num": "pl"}}]},
        {"art": "p14_wind", "focus": ["wind"],
         "clauses": [{"subj": {"n": "wind", "art": "the"}, "verb": "blow"}]},
        {"art": "p15_soil", "focus": ["soil"],
         "clauses": [{"subj": {"n": "seed", "num": "pl"}, "verb": "sleep",
                      "pp": ("in", {"n": "soil", "art": "the"})}]},
        {"art": "p16_again", "focus": ["winter"],
         "clauses": [{"phrase": "winter_again"}]},
    ],
}
