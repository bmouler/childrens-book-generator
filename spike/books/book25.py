"""Book 25: "In and Out!" — age 3, where things sit and where they go.

The ball hides in the box, the box hides the teddy bear, the bag hides the ball.
In, under, out of: the prepositions carry the pills, because place words are the lesson.
"""

STORY = {
    "title": "In and Out!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_in_out"}]},
    "pages": [
        {"art": "p01_hide", "focus": ["ball"],
         "clauses": [{"subj": "ball", "verb": "hide", "pp": ("in", "box")}]},
        {"art": "p02_where", "focus": ["where"],
         "clauses": [{"q_where": "ball"}]},
        {"art": "p03_in_box", "focus": ["in"],
         "clauses": [{"subj": "ball", "verb": "be", "pp": ("in", "box")}]},
        {"art": "p04_take_out", "focus": ["out_of"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "take", "obj": "ball",
                      "pp_from": "box"}]},
        {"art": "p05_play", "focus": ["now", "play"],
         "clauses": [{"lead": "now", "subj": {"pron": "we"}, "verb": "play"}]},
        {"art": "p06_put_ball", "focus": ["put"],
         "clauses": [{"imp": "put", "obj": "ball", "pp_to": ("in", "box")}]},
        {"art": "p07_under", "focus": ["under"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "put", "obj": "teddy",
                      "pp_to": ("under", "box")}]},
        {"art": "p08_where_teddy", "focus": ["teddy"],
         "clauses": [{"q_where": "teddy"}]},
        {"art": "p09_teddy_under", "focus": ["under"],
         "clauses": [{"subj": "teddy", "verb": "be", "pp": ("under", "box")}]},
        {"art": "p10_take_teddy", "focus": ["take"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "take", "obj": "teddy",
                      "pp_from": "box"}]},
        {"art": "p11_bag", "focus": ["bag"],
         "clauses": [{"subj": "ball", "verb": "be", "pp": ("in", "bag")}]},
        {"art": "p12_where_ball", "focus": ["where", "ball"],
         "clauses": [{"q_where": "ball"}]},
        {"art": "p13_out_bag", "focus": ["out_of"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "take", "obj": "ball",
                      "pp_from": "bag"}]},
        {"art": "p14_end",  # a recitation page: the title says it all
         "clauses": [{"phrase": "title_in_out"}]},
    ],
}
