"""Book 5: "Soft or Hard?" A pillow and a block, asked and answered. Then a teddy bear, a table, the two
rules in the plural, and a command to touch.
"""
WE = {"pron": "we"}
PILLOW_PL = {"n": "pillow", "num": "pl"}
BLOCK_PL = {"n": "block", "num": "pl"}

STORY = {
    "title": "Soft or Hard?",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_soft_hard"}]},
    "pages": [
        {"art": "p01_see_pillow", "focus": ["pillow"], "clauses": [{"subj": WE, "verb": "see", "obj": "pillow"}]},
        {"art": "p02_pillow_ask", "focus": ["soft", "hard"],
         "clauses": [{"q_or_adj": {"subj": "pillow", "adjs": ["soft", "hard"]}}]},
        {"art": "p03_pillow_soft", "focus": ["soft"], "clauses": [{"subj": "pillow", "pred": "soft", "end": "!"}]},
        {"art": "p04_see_block", "focus": ["block"], "clauses": [{"subj": WE, "verb": "see", "obj": "block"}]},
        {"art": "p05_block_ask", "focus": ["soft", "hard"],
         "clauses": [{"q_or_adj": {"subj": "block", "adjs": ["soft", "hard"]}}]},
        {"art": "p06_block_hard", "focus": ["hard"], "clauses": [{"subj": "block", "pred": "hard", "end": "!"}]},
        {"art": "p07_teddy_soft", "focus": ["teddy", "soft"],
         "clauses": [{"subj": {"n": "teddy", "art": "the"}, "pred": "soft"}]},
        {"art": "p08_table_hard", "focus": ["table", "hard"],
         "clauses": [{"subj": {"n": "table", "art": "the"}, "pred": "hard"}]},
        {"art": "p09_pillows_blocks", "focus": ["soft", "hard"],
         "clauses": [{"subj": PILLOW_PL, "pred": "soft"}, {"subj": BLOCK_PL, "pred": "hard"}]},
        {"art": "p10_touch_teddy", "focus": ["touch", "teddy"],
         "clauses": [{"imp": "touch", "obj": {"n": "teddy", "art": "the"}, "end": "!"}]},
    ],
}
