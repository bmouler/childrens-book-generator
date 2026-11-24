"""Book 28: "The Melting Race!" — age 4, an experiment with two ice cubes.

One cube in the sun, one in the shadow of the box. First we guess, then we wait, at last we
see. The sun wins the race, because the sun is hot and the shadow is cold.
"""

W = {"n": "water", "art": "the"}

STORY = {
    "title": "The Melting Race!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_melting_race"}]},
    "pages": [
        {"art": "p01_ice", "focus": ["ice"],
         "clauses": [{"imp": "look", "pp": ("at", {"n": "ice", "art": "the"})}]},
        {"art": "p02_sun", "focus": ["put"],
         "clauses": [{"phrase": "in_the_sun"}]},
        {"art": "p03_shade", "focus": ["shadow"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "put", "obj": {"n": "ice", "art": "the"},
                      "pp": ("in", "shadow")}]},
        {"art": "p04_guess", "focus": ["first", "guess"],
         "clauses": [{"lead": "first", "subj": {"pron": "we"}, "verb": "guess"}]},
        {"art": "p05_sun_hot", "focus": ["hot"],
         "clauses": [{"pred": "hot", "subj": {"n": "sun", "art": "the"}}]},
        {"art": "p06_shadow_cold", "focus": ["cold"],
         "clauses": [{"pred": "cold", "subj": "shadow"}]},
        {"art": "p07_wait", "focus": ["then", "wait"],
         "clauses": [{"lead": "then", "subj": {"pron": "we"}, "verb": "wait"}]},
        {"art": "p08_wait_wait",  # and wait, and wait: a recitation page
         "clauses": [{"subj": {"pron": "we"}, "verb": "wait"},
                     {"subj": {"pron": "we"}, "verb": "wait"}]},
        {"art": "p09_so", "focus": ["melt", "so"],
         "clauses": [{"join": "so", "parts": [
             {"subj": {"n": "sun", "art": "the"}, "verb": "shine"},
             {"subj": {"n": "ice", "art": "the"}, "verb": "melt"}]}]},
        {"art": "p10_shade_slow", "focus": ["slow"],
         "clauses": [{"subj": {"n": "ice", "art": "the"}, "verb": "melt",
                      "pp": ("in", "shadow"), "adv": "slow"}]},
        {"art": "p11_water_back", "focus": ["water"],
         "clauses": [{"phrase": "water_back"}]},
        {"art": "p12_see", "focus": ["at_last", "see"],
         "clauses": [{"lead": "at_last", "subj": {"pron": "we"}, "verb": "see"}]},
        {"art": "p13_know",  # a recitation page
         "clauses": [{"phrase": "i_know"}]},
        {"art": "p14_touch", "focus": ["touch"],
         "clauses": [{"imp": "touch", "obj": W}]},
        {"art": "p15_cold", "focus": ["cold"],
         "clauses": [{"pred": "cold", "subj": W}]},
        {"art": "p16_end",  # the loop, in one breath: a recitation page
         "clauses": [{"lead": "first", "subj": {"pron": "we"}, "verb": "guess"},
                     {"lead": "at_last", "subj": {"pron": "we"}, "verb": "know"}]},
    ],
}
