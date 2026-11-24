"""Book 4: "Big or Small?" An elephant and a mouse, asked and answered. Then a tree, a flower, and both
animals in one picture.
"""
WE = {"pron": "we"}

STORY = {
    "title": "Big or Small?",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_big_small"}]},
    "pages": [
        {"art": "p01_see_elephant", "focus": ["elephant"], "clauses": [{"subj": WE, "verb": "see", "obj": "elephant"}]},
        {"art": "p02_elephant_ask", "focus": ["big", "small"],
         "clauses": [{"q_or_adj": {"subj": "elephant", "adjs": ["big", "small"]}}]},
        {"art": "p03_elephant_big", "focus": ["big"], "clauses": [{"subj": "elephant", "pred": "big", "end": "!"}]},
        {"art": "p04_see_mouse", "focus": ["mouse"], "clauses": [{"subj": WE, "verb": "see", "obj": "mouse"}]},
        {"art": "p05_mouse_ask", "focus": ["big", "small"],
         "clauses": [{"q_or_adj": {"subj": "mouse", "adjs": ["big", "small"]}}]},
        {"art": "p06_mouse_small", "focus": ["small"], "clauses": [{"subj": "mouse", "pred": "small", "end": "!"}]},
        {"art": "p07_tree_big", "focus": ["tree", "big"],
         "clauses": [{"subj": {"n": "tree", "art": "the"}, "pred": "big"}]},
        {"art": "p08_flower_small", "focus": ["flower", "small"],
         "clauses": [{"subj": {"n": "flower", "art": "the"}, "pred": "small"}]},
        {"art": "p09_elephant_mouse", "focus": ["big", "small"],
         "clauses": [{"subj": "elephant", "pred": "big"}, {"subj": "mouse", "pred": "small"}]},
        {"art": "p10_now_you", "focus": ["try"], "clauses": [{"phrase": "now_you_try"}]},
    ],
}
