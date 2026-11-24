"""Book 18: "The Little Spider" — Itsy Bitsy Spider (Паучок).

The little spider climbs up the pipe, the rain washes it out, the sun dries the rain, and the
spider climbs up again. The chant pages are recitation pages. The wash and dry beats are plain
past-tense clauses: the same "sun dries water" science as books 9 and 11.
"""


def the(noun: str) -> dict:
    return {"n": noun, "art": "the"}


STORY = {
    "title": "The Little Spider",
    "tense": "past",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_spider"}]},
    "pages": [
        {"art": "p01_climbs", "focus": ["spider"],
         "clauses": [{"subj": the("spider"), "verb": "climb", "adv": "up", "tense": "pres",
                      "end": "!"}]},
        {"art": "p02_up_pipe",  # the chant: a recitation page
         "clauses": [{"phrase": "up_the_pipe"}]},
        {"art": "p03_rain_came",
         "clauses": [{"phrase": "rain_came"}]},
        {"art": "p04_washes", "focus": ["rain"],
         "clauses": [{"subj": the("rain"), "verb": "wash_out", "obj": the("spider")}]},
        {"art": "p05_sun_out",
         "clauses": [{"phrase": "sun_comes_out"}]},
        {"art": "p06_dries", "focus": ["sun"],
         "clauses": [{"subj": the("sun"), "verb": "dry", "obj": the("rain")}]},
        {"art": "p07_up_again",
         "clauses": [{"phrase": "up_pipe_again"}]},
        {"art": "p08_in_sun", "focus": ["spider"],
         "clauses": [{"phrase": "spider_in_sun"}]},
    ],
}
