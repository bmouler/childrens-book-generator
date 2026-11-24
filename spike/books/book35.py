"""Book 35: "What Is Water?" — age 5, three faces of one thing.

Water runs, freezes into ice, boils into steam, and the steam becomes water again.
Zero degrees one way, hot the other way: temperature is the dial, water is the same.
"""

W = {"n": "water", "art": "the"}

STORY = {
    "title": "What Is Water?",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_water"}]},
    "pages": [
        {"art": "p01_what",  # a recitation page
         "clauses": [{"phrase": "what_is_it"}]},
        {"art": "p02_we_see", "focus": ["water"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "see", "obj": W}]},
        {"art": "p03_we_touch", "focus": ["touch"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "touch", "obj": W}]},
        {"art": "p04_cold", "focus": ["cold"],
         "clauses": [{"pred": "cold", "subj": W}]},
        {"art": "p05_wet", "focus": ["wet"],
         "clauses": [{"pred": "wet", "subj": W}]},
        {"art": "p06_zero",  # a recitation page
         "clauses": [{"phrase": "zero_degrees"}]},
        {"art": "p07_becomes_ice", "focus": ["become", "ice"],
         "clauses": [{"subj": W, "verb": "become",
                      "instr": {"n": "ice", "art": "the"}}]},
        {"art": "p08_ice_cold", "focus": ["ice"],
         "clauses": [{"pred": "cold", "subj": {"n": "ice", "art": "the"}}]},
        {"art": "p09_ice_hard", "focus": ["hard"],
         "clauses": [{"pred": "hard", "subj": {"n": "ice", "art": "the"}}]},
        {"art": "p10_sun", "focus": ["sun"],
         "clauses": [{"subj": {"n": "sun", "art": "the"}, "verb": "shine"}]},
        {"art": "p11_melt", "focus": ["melt"],
         "clauses": [{"subj": {"n": "ice", "art": "the"}, "verb": "melt"}]},
        {"art": "p12_water_back", "focus": ["water"],
         "clauses": [{"phrase": "water_back"}]},
        {"art": "p13_hot", "focus": ["hot"],
         "clauses": [{"phrase": "hot_water"}]},
        {"art": "p14_boil", "focus": ["boil"],
         "clauses": [{"subj": W, "verb": "boil"}]},
        {"art": "p15_becomes_steam", "focus": ["steam"],
         "clauses": [{"subj": W, "verb": "become",
                      "instr": {"n": "steam", "art": ""}}]},
        {"art": "p16_steam_white", "focus": ["white"],
         "clauses": [{"pred": "white", "subj": {"n": "steam", "art": ""}}]},
        {"art": "p17_rise", "focus": ["rise"],
         "clauses": [{"subj": {"n": "steam", "art": ""}, "verb": "rise"}]},
        {"art": "p18_becomes_water", "focus": ["become"],
         "clauses": [{"subj": {"n": "steam", "art": ""}, "verb": "become",
                      "instr": W}]},
        {"art": "p19_all_water", "focus": ["water"],
         "clauses": [{"phrase": "it_all_water"}]},
        {"art": "p20_know",  # a recitation page
         "clauses": [{"phrase": "i_know"}]},
    ],
}
