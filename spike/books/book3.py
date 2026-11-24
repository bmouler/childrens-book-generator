"""Book 3: "Heavy or Light?" A feather and a stone, asked and answered. Then a balloon, a watermelon,
and the two rules in the plural.
"""
WE = {"pron": "we"}
FEATHER_PL = {"n": "feather", "num": "pl"}
STONE_PL = {"n": "stone", "num": "pl"}

STORY = {
    "title": "Heavy or Light?",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_heavy_light"}]},
    "pages": [
        {"art": "p01_see_feather", "focus": ["feather"], "clauses": [{"subj": WE, "verb": "see", "obj": "feather"}]},
        {"art": "p02_feather_ask", "focus": ["heavy", "light"],
         "clauses": [{"q_or_adj": {"subj": "feather", "adjs": ["heavy", "light"]}}]},
        {"art": "p03_feather_light", "focus": ["light"], "clauses": [{"subj": "feather", "pred": "light", "end": "!"}]},
        {"art": "p04_see_stone", "focus": ["stone"], "clauses": [{"subj": WE, "verb": "see", "obj": "stone"}]},
        {"art": "p05_stone_ask", "focus": ["heavy", "light"],
         "clauses": [{"q_or_adj": {"subj": "stone", "adjs": ["heavy", "light"]}}]},
        {"art": "p06_stone_heavy", "focus": ["heavy"], "clauses": [{"subj": "stone", "pred": "heavy", "end": "!"}]},
        {"art": "p07_balloon_light", "focus": ["balloon", "light"],
         "clauses": [{"subj": {"n": "balloon", "art": "the"}, "pred": "light"}]},
        {"art": "p08_watermelon_heavy", "focus": ["watermelon", "heavy"],
         "clauses": [{"subj": {"n": "watermelon", "art": "the"}, "pred": "heavy"}]},
        {"art": "p09_feathers_stones", "focus": ["light", "heavy"],
         "clauses": [{"subj": FEATHER_PL, "pred": "light"}, {"subj": STONE_PL, "pred": "heavy"}]},
        {"art": "p10_now_you", "focus": ["try"], "clauses": [{"phrase": "now_you_try"}]},
    ],
}
