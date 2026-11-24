"""Book 27: "On Purpose!" — age 3, the same act, done two ways.

Now we clap: fast, then slowly. Loud, then quiet. Up, then down. The adverb is the star,
and every fourth page resets the game with "Now we...".
"""

STORY = {
    "title": "On Purpose!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_on_purpose"}]},
    "pages": [
        {"art": "p01_clap", "focus": ["now", "clap"],
         "clauses": [{"lead": "now", "subj": {"pron": "we"}, "verb": "clap"}]},
        {"art": "p02_fast", "focus": ["fast"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "clap", "adv": "fast"}]},
        {"art": "p03_slow", "focus": ["slow"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "clap", "adv": "slow"}]},
        {"art": "p04_stomp", "focus": ["now", "stomp"],
         "clauses": [{"lead": "now", "subj": {"pron": "we"}, "verb": "stomp"}]},
        {"art": "p05_stomp_fast", "focus": ["fast"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "stomp", "adv": "fast"}]},
        {"art": "p06_sing", "focus": ["now", "sing"],
         "clauses": [{"lead": "now", "subj": {"pron": "we"}, "verb": "sing"}]},
        {"art": "p07_quiet", "focus": ["quietly"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "sing", "adv": "quietly"}]},
        {"art": "p08_loud", "focus": ["loudly"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "sing", "adv": "loudly"}]},
        {"art": "p09_jump", "focus": ["now", "jump"],
         "clauses": [{"lead": "now", "subj": {"pron": "we"}, "verb": "jump"}]},
        {"art": "p10_up", "focus": ["up"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "jump", "adv": "up"}]},
        {"art": "p11_down", "focus": ["down"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "jump", "adv": "down"}]},
        {"art": "p12_count", "focus": ["now", "count"],
         "clauses": [{"lead": "now", "subj": {"pron": "we"}, "verb": "count"}]},
        {"art": "p13_count_two",  # fast, then slowly: a recitation page
         "clauses": [{"subj": {"pron": "we"}, "verb": "count", "adv": "fast"},
                     {"subj": {"pron": "we"}, "verb": "count", "adv": "slow"}]},
        {"art": "p14_clap_again", "focus": ["clap"],
         "clauses": [{"imp": "clap", "adv": "again"}]},
    ],
}
