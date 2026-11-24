"""Book 7: "Red, Yellow, Green, Blue!" Four colours. First one ball in four colours, then four things
that have those colours. Only the colour words are highlighted (pills: hues), each in its own colour.
"""
WE = {"pron": "we"}


def a_ball(colour: str) -> dict:
    return {"n": "ball", "adj": [colour], "art": "a"}


STORY = {
    "title": "Red, Yellow, Green, Blue!",
    "tense": "pres",
    "pills": "hues",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_colors"}]},
    "pages": [
        {"art": "p01_red_ball", "focus": ["red"], "clauses": [{"subj": WE, "verb": "see", "obj": a_ball("red")}]},
        {"art": "p02_blue_ball", "focus": ["blue"], "clauses": [{"subj": WE, "verb": "see", "obj": a_ball("blue")}]},
        {"art": "p03_yellow_ball", "focus": ["yellow"],
         "clauses": [{"subj": WE, "verb": "see", "obj": a_ball("yellow")}]},
        {"art": "p04_green_ball", "focus": ["green"], "clauses": [{"subj": WE, "verb": "see", "obj": a_ball("green")}]},
        {"art": "p05_apple_red", "focus": ["red"],
         "clauses": [{"subj": {"n": "apple", "art": "the"}, "pred": "red"}]},
        {"art": "p06_sun_yellow", "focus": ["yellow"],
         "clauses": [{"subj": {"n": "sun", "art": "the"}, "pred": "yellow"}]},
        {"art": "p07_leaf_green", "focus": ["green"],
         "clauses": [{"subj": {"n": "leaf", "art": "the"}, "pred": "green"}]},
        {"art": "p08_sea_blue", "focus": ["blue"],
         "clauses": [{"subj": {"n": "sea", "art": "the"}, "pred": "blue"}]},
        {"art": "p09_four_balls", "focus": ["red", "blue"], "clauses": [{"phrase": "title_colors"}]},
        {"art": "p10_now_you", "focus": ["try"], "clauses": [{"phrase": "now_you_try"}]},
    ],
}
