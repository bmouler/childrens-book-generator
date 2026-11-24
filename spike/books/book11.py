"""Book 11: "Ice Melts". Ice is cold. It floats. In the sun it gets small, then it melts into water.
A sequel to Book 1 (sink or float) and Book 2 (hot or cold).
"""
WE = {"pron": "we"}
THE_ICE = {"n": "ice", "art": "the"}

STORY = {
    "title": "Ice Melts",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_ice_melts"}]},
    "pages": [
        {"art": "p01_see_ice", "focus": ["ice"], "clauses": [{"subj": WE, "verb": "see", "obj": {"n": "ice", "art": ""}}]},
        {"art": "p02_ice_cold", "focus": ["cold"], "clauses": [{"subj": THE_ICE, "pred": "cold"}]},
        {"art": "p03_ice_ask", "focus": ["sink", "float"],
         "clauses": [{"q_or": {"subj": THE_ICE, "verbs": ["sink", "float"]}}]},
        {"art": "p04_ice_floats", "focus": ["float"], "clauses": [{"subj": THE_ICE, "verb": "float", "end": "!"}]},
        {"art": "p05_sun_hot", "focus": ["sun", "hot"], "clauses": [{"subj": {"n": "sun", "art": "the"}, "pred": "hot"}]},
        {"art": "p06_wait", "focus": ["wait"], "clauses": [{"subj": WE, "verb": "wait"}]},
        {"art": "p07_ice_small", "focus": ["small"], "clauses": [{"subj": THE_ICE, "pred": "small"}]},
        {"art": "p08_ice_melts", "focus": ["melt"], "clauses": [{"subj": THE_ICE, "verb": "melt", "end": "!"}]},
        {"art": "p09_see_water", "focus": ["water"],
         "clauses": [{"subj": WE, "verb": "see", "obj": {"n": "water", "art": ""}}]},
        {"art": "p10_now_you", "focus": ["try"], "clauses": [{"phrase": "now_you_try"}]},
    ],
}
