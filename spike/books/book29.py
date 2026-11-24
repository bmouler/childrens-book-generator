"""Book 29: "Which Is Heavier?" — age 4, comparatives.

Stone against feather, watermelon against apple, elephant against mouse. Then the two traps:
a big box that is light, a small stone that is heavy. Size does not say weight.
"""

STORY = {
    "title": "Which Is Heavier?",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_heavier"}]},
    "pages": [
        {"art": "p01_stone_feather", "focus": ["heavy"],
         "clauses": [{"q_which_comp": {"comp": "heavy", "subj": ["stone", "feather"]}}]},
        {"art": "p02_stone", "focus": ["stone"],
         "clauses": [{"pred": [{"comp": "heavy", "than": "feather"}], "subj": "stone"}]},
        {"art": "p03_feather", "focus": ["light"],
         "clauses": [{"pred": [{"comp": "light", "than": "stone"}], "subj": "feather"}]},
        {"art": "p04_hands", "focus": ["heavy", "light"],
         "clauses": [{"pred": "heavy", "subj": "stone"},
                     {"pred": "light", "subj": "feather"}]},
        {"art": "p05_melon_apple", "focus": ["apple"],
         "clauses": [{"q_which_comp": {"comp": "heavy", "subj": ["watermelon", "apple"]}}]},
        {"art": "p06_melon", "focus": ["watermelon"],
         "clauses": [{"pred": [{"comp": "heavy"}], "subj": "watermelon"}]},
        {"art": "p07_apple", "focus": ["small"],
         "clauses": [{"pred": [{"comp": "small", "than": "watermelon"}], "subj": "apple"}]},
        {"art": "p08_elephant_mouse", "focus": ["elephant"],
         "clauses": [{"q_which_comp": {"comp": "heavy", "subj": ["elephant", "mouse"]}}]},
        {"art": "p09_elephant", "focus": ["elephant"],
         "clauses": [{"pred": [{"comp": "heavy", "than": "mouse"}], "subj": "elephant"}]},
        {"art": "p10_big_too", "focus": ["big"],
         "clauses": [{"pred": [{"comp": "big"}], "subj": "elephant"}]},
        {"art": "p11_light_q", "focus": ["light"],
         "clauses": [{"q_which_comp": {"comp": "light", "subj": ["feather", "balloon"]}}]},
        {"art": "p12_feather", "focus": ["feather"],
         "clauses": [{"pred": [{"comp": "light"}], "subj": "feather"}]},
        {"art": "p13_balloon", "focus": ["balloon"],
         "clauses": [{"pred": ["light", "round"], "subj": "balloon"}]},
        {"art": "p14_box_trap", "focus": ["but", "light"],
         "clauses": [{"join": "but", "parts": [
             {"pred": "big", "subj": "box"},
             {"pred": "light", "subj": {"pron": "it_f"}}]}]},
        {"art": "p15_stone_trap", "focus": ["heavy"],
         "clauses": [{"join": "but", "parts": [
             {"pred": "small", "subj": "stone"},
             {"pred": "heavy", "subj": {"pron": "it_m"}}]}]},
        {"art": "p16_know",  # a recitation page
         "clauses": [{"phrase": "i_know"}]},
    ],
}
