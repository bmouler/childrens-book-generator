"""Book 2: "Hot or Cold?" Predict, then observe: ice, soup, the sun and snow. Ends with a command.

Values: science and objectivity. Safe tests only: the child touches ice and never touches a hot thing.
"""
WE = {"pron": "we"}
ICE = {"n": "ice", "art": ""}  # ice in general
THE_ICE = {"n": "ice", "art": "the"}  # this ice
SOUP = {"n": "soup", "art": ""}
THE_SOUP = {"n": "soup", "art": "the"}

STORY = {
    "title": "Hot or Cold?",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_hot_cold"}]},
    "pages": [
        {"art": "p01_see_ice", "focus": ["ice"], "clauses": [{"subj": WE, "verb": "see", "obj": ICE}]},
        {"art": "p02_ice_ask", "focus": ["hot", "cold"],
         "clauses": [{"q_or_adj": {"subj": THE_ICE, "adjs": ["hot", "cold"]}}]},
        {"art": "p03_ice_cold", "focus": ["cold"], "clauses": [{"subj": THE_ICE, "pred": "cold", "end": "!"}]},
        {"art": "p04_see_soup", "focus": ["soup"], "clauses": [{"subj": WE, "verb": "see", "obj": SOUP}]},
        {"art": "p05_soup_ask", "focus": ["hot", "cold"],
         "clauses": [{"q_or_adj": {"subj": THE_SOUP, "adjs": ["hot", "cold"]}}]},
        {"art": "p06_soup_hot", "focus": ["hot"], "clauses": [{"subj": THE_SOUP, "pred": "hot", "end": "!"}]},
        {"art": "p07_sun_hot", "focus": ["sun", "hot"],
         "clauses": [{"subj": {"n": "sun", "art": "the"}, "pred": "hot"}]},
        {"art": "p08_snow_cold", "focus": ["snow", "cold"],
         "clauses": [{"subj": {"n": "snow", "art": ""}, "pred": "cold"}]},
        {"art": "p09_ice_soup", "focus": ["cold", "hot"],
         "clauses": [{"subj": ICE, "pred": "cold"}, {"subj": SOUP, "pred": "hot"}]},
        {"art": "p10_touch_ice", "focus": ["touch", "ice"], "clauses": [{"imp": "touch", "obj": THE_ICE, "end": "!"}]},
    ],
}
