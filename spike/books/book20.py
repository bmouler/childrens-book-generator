"""Book 20: "Head and Shoulders" — the body-parts chant (Голова и плечи, колени и пальчики).

Four pair pages, then the full chant. Then the game: touch the head, touch the toes, and the
peek-a-boo question "Where is the nose? — There it is!". The chant comes back at the end, because
repetition is the point of a chant.
"""


STORY = {
    "title": "Head and Shoulders",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_body"}]},
    "pages": [
        {"art": "p01_head_shoulders",  # the chant, pair by pair: recitation pages
         "clauses": [{"phrase": "head_shoulders"}]},
        {"art": "p02_knees_toes",
         "clauses": [{"phrase": "knees_toes"}]},
        {"art": "p03_eyes_ears",
         "clauses": [{"phrase": "eyes_ears"}]},
        {"art": "p04_mouth_nose",
         "clauses": [{"phrase": "mouth_nose"}]},
        {"art": "p05_chant",
         "clauses": [{"phrase": "chant_body"}]},
        {"art": "p06_touch_head", "focus": ["head"],
         "clauses": [{"imp": "touch", "obj": {"n": "head", "art": "the"}, "end": "!"}]},
        {"art": "p07_touch_toes", "focus": ["toe"],
         "clauses": [{"imp": "touch", "obj": {"n": "toe", "art": "the", "num": "pl"}, "end": "!"}]},
        {"art": "p08_where_nose", "focus": ["nose"],
         "clauses": [{"q_where": {"n": "nose", "art": "the"}}]},
        {"art": "p09_there_it_is",
         "clauses": [{"phrase": "there_it_is"}]},
        {"art": "p10_chant_again",
         "clauses": [{"phrase": "chant_body"}]},
    ],
}
