"""Book 30: "Sink or Float: The Big Test!" — age 4, eight things and a results chart.

Guess first, then try, then the chart: what we guessed against what we saw. A cross is not a
failure. A cross is news. That is the whole scientific method, at age four.
"""

W = {"n": "water", "art": "the"}
S = ("sink", "тонет")
F = ("float", "плавает")

STORY = {
    "title": "Sink or Float: The Big Test!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_big_test"}]},
    "pages": [
        {"art": "p01_test",  # the frame: a recitation page
         "clauses": [{"phrase": "title_big_test"}]},
        {"art": "p02_water", "focus": ["water"],
         "clauses": [{"imp": "look", "pp": ("at", W)}]},
        {"art": "p03_guess", "focus": ["first", "guess"],
         "clauses": [{"lead": "first", "subj": {"pron": "we"}, "verb": "guess"}]},
        {"art": "p04_stone_q", "focus": ["stone", "sink"],
         "clauses": [{"q_or": {"subj": "stone", "verbs": ["sink", "float"]}}]},
        {"art": "p05_stone_sinks", "focus": ["sink"],
         "clauses": [{"subj": "stone", "verb": "sink"}]},
        {"art": "p06_feather_q", "focus": ["feather"],
         "clauses": [{"q_or": {"subj": "feather", "verbs": ["sink", "float"]}}]},
        {"art": "p07_feather_floats", "focus": ["float"],
         "clauses": [{"subj": "feather", "verb": "float"}]},
        {"art": "p08_ball_q", "focus": ["ball"],
         "clauses": [{"q_or": {"subj": "ball", "verbs": ["sink", "float"]}}]},
        {"art": "p09_ball_floats", "focus": ["float"],
         "clauses": [{"subj": "ball", "verb": "float"}]},
        {"art": "p10_melon_q", "focus": ["watermelon"],
         "clauses": [{"q_or": {"subj": "watermelon", "verbs": ["sink", "float"]}}]},
        {"art": "p11_melon_floats", "focus": ["but"],
         "clauses": [{"join": "but", "parts": [
             {"pred": "heavy", "subj": "watermelon"},
             {"subj": {"pron": "it_m"}, "verb": "float"}]}]},
        {"art": "p12_apple_q", "focus": ["apple"],
         "clauses": [{"q_or": {"subj": "apple", "verbs": ["sink", "float"]}}]},
        {"art": "p13_apple_floats", "focus": ["apple"],
         "clauses": [{"subj": "apple", "verb": "float"}]},
        {"art": "p14_box_q", "focus": ["box"],
         "clauses": [{"q_or": {"subj": "box", "verbs": ["sink", "float"]}}]},
        {"art": "p15_box_floats", "focus": ["box"],
         "clauses": [{"subj": "box", "verb": "float"}]},
        {"chart": [  # the results chart, drawn by code
            {"n": "stone", "guess": S, "saw": S},
            {"n": "feather", "guess": F, "saw": F},
            {"n": "ball", "guess": S, "saw": F},
            {"n": "watermelon", "guess": S, "saw": F},
            {"n": "apple", "guess": S, "saw": F},
            {"n": "box", "guess": F, "saw": F},
         ],
         "clauses": [{"phrase": "chart_look"}]},
        {"art": "p17_at_last", "focus": ["at_last", "see"],
         "clauses": [{"lead": "at_last", "subj": {"pron": "we"}, "verb": "see"}]},
        {"art": "p18_know",  # a recitation page
         "clauses": [{"phrase": "i_know"}]},
    ],
}
