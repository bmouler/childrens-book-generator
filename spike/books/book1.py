"""Book 1: "Sink or Float?" as a clause list over the curated lexicon (what the LLM will write).

Values: science and objectivity. Predict, test, observe. No talking animals, no moral.
Hero: "we" (the child and the reader), so the text is gender-neutral.
"""
WE = {"pron": "we"}
STONE_PL = {"n": "stone", "num": "pl"}
LEAF_PL = {"n": "leaf", "num": "pl"}

STORY = {
    "title": "Sink or Float?",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_sink_float"}]},
    "pages": [  # focus = the key words of the page: the word-card designs show them large, with a sticker
        {"art": "p01_look_water", "focus": ["look"], "clauses": [{"subj": WE, "verb": "look", "pp": ["at", {"n": "water", "art": "the"}]}]},
        {"art": "p02_see_ball", "focus": ["ball"], "clauses": [{"subj": WE, "verb": "see", "obj": "ball"}]},
        {"art": "p03_ball_ask", "focus": ["sink", "float"], "clauses": [{"q_or": {"subj": "ball", "verbs": ["sink", "float"]}}]},
        {"art": "p04_ball_floats", "focus": ["float"], "clauses": [{"subj": "ball", "verb": "float", "end": "!"}]},
        {"art": "p05_see_stone", "focus": ["stone"], "clauses": [{"subj": WE, "verb": "see", "obj": "stone"}]},
        {"art": "p06_stone_ask", "focus": ["sink", "float"], "clauses": [{"q_or": {"subj": "stone", "verbs": ["sink", "float"]}}]},
        {"art": "p07_stone_sinks", "focus": ["sink"], "clauses": [{"subj": "stone", "verb": "sink", "end": "!"}]},
        {"art": "p08_stones_sink", "focus": ["sink"], "clauses": [{"subj": STONE_PL, "verb": "sink"}]},
        {"art": "p09_leaves_float", "focus": ["float"], "clauses": [{"subj": LEAF_PL, "verb": "float"}]},
        {"art": "p10_now_you", "focus": ["try"], "clauses": [{"phrase": "now_you_try"}]},
    ],
}
