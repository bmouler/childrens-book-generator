"""Book 6: "Where Is the Ball?" In, on, under. The same ball, three places, asked and answered. Then the
child puts the ball in the same three places.
"""
WE = {"pron": "we"}
THE_BALL = {"n": "ball", "art": "the"}
THE_BOX = {"n": "box", "art": "the"}
THE_TABLE = {"n": "table", "art": "the"}
THE_CHAIR = {"n": "chair", "art": "the"}

STORY = {
    "title": "Where Is the Ball?",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_where_ball"}]},
    "pages": [
        {"art": "p01_where_1", "focus": ["where", "ball"], "clauses": [{"q_where": THE_BALL}]},
        {"art": "p02_ball_in_box", "focus": ["in", "box"],
         "clauses": [{"subj": THE_BALL, "verb": "be", "pp": ["in", THE_BOX]}]},
        {"art": "p03_where_2", "focus": ["where"], "clauses": [{"q_where": THE_BALL}]},
        {"art": "p04_ball_on_table", "focus": ["on", "table"],
         "clauses": [{"subj": THE_BALL, "verb": "be", "pp": ["on", THE_TABLE]}]},
        {"art": "p05_where_3", "focus": ["where"], "clauses": [{"q_where": THE_BALL}]},
        {"art": "p06_ball_under_chair", "focus": ["under", "chair"],
         "clauses": [{"subj": THE_BALL, "verb": "be", "pp": ["under", THE_CHAIR]}]},
        {"art": "p07_put_in", "focus": ["in"],
         "clauses": [{"subj": WE, "verb": "put", "obj": THE_BALL, "pp_to": ["in", THE_BOX]}]},
        {"art": "p08_put_on", "focus": ["on"],
         "clauses": [{"subj": WE, "verb": "put", "obj": THE_BALL, "pp_to": ["on", THE_TABLE]}]},
        {"art": "p09_put_under", "focus": ["under"],
         "clauses": [{"subj": WE, "verb": "put", "obj": THE_BALL, "pp_to": ["under", THE_CHAIR]}]},
        {"art": "p10_now_you", "focus": ["try"], "clauses": [{"phrase": "now_you_try"}]},
    ],
}
