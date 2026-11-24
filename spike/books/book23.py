"""Book 23: "Why Does It Sink?" — age 3, cause joins the facts.

Every sink-or-float fact from Book 1 gets its because: heavy things sink, light things float.
The watermelon breaks the rule (heavy, but it floats) and the book closes on the loop:
look at the water again.
"""

M = {"n": "water", "art": "the"}  # water is a mass noun: it takes an explicit article

STORY = {
    "title": "Why Does It Sink?",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_why_sink"}]},
    "pages": [
        {"art": "p01_water", "focus": ["water"],
         "clauses": [{"imp": "look", "pp": ("at", M)}]},
        {"art": "p02_stone", "focus": ["because", "heavy"],
         "clauses": [{"join": "because", "parts": [
             {"subj": "stone", "verb": "sink"},
             {"pred": "heavy", "subj": {"pron": "it_m"}}]}]},
        {"art": "p03_feather", "focus": ["feather", "light"],
         "clauses": [{"join": "because", "parts": [
             {"subj": "feather", "verb": "float"},
             {"pred": "light", "subj": {"pron": "it_n"}}]}]},
        {"art": "p04_ball_q", "focus": ["why"],
         "clauses": [{"q_why": {"subj": "ball", "verb": "float"}}]},
        {"art": "p05_ball_a", "focus": ["because", "light"],
         "clauses": [{"lead": "because", "pred": "light", "subj": {"pron": "it_m"}}]},
        {"art": "p06_stone_q", "focus": ["why", "stone"],
         "clauses": [{"q_why": {"subj": "stone", "verb": "sink"}}]},
        {"art": "p07_stone_a", "focus": ["heavy"],
         "clauses": [{"lead": "because", "pred": "heavy", "subj": {"pron": "it_m"}}]},
        {"art": "p08_melon", "focus": ["but", "float"],
         "clauses": [{"join": "but", "parts": [
             {"pred": "heavy", "subj": "watermelon"},
             {"subj": {"pron": "it_m"}, "verb": "float"}]}]},
        {"art": "p09_melon_q", "focus": ["why"],
         "clauses": [{"q_why": {"subj": "watermelon", "verb": "float"}}]},
        {"art": "p10_melon_a", "focus": ["big"],
         "clauses": [{"lead": "because", "pred": "big", "subj": {"pron": "it_m"}}]},
        {"art": "p11_we_look", "focus": ["look", "see"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "look"},
                     {"subj": {"pron": "we"}, "verb": "see"}]},
        {"art": "p12_we_know", "focus": ["know"],
         "clauses": [{"phrase": "i_know"}]},
        {"art": "p13_you_try",  # a recitation page: no cards
         "clauses": [{"phrase": "now_you_try"}]},
        {"art": "p14_again", "focus": ["water"],
         "clauses": [{"imp": "look", "pp": ("at", M), "adv": "again"}]},
    ],
}
