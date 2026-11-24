"""Book 37: "The Five Senses Test!" — age 5, check, then look.

Eyes closed: touch it, smell it, listen. Then eyes open: were we right? The senses are the
tools, the guess is the test, and the check is the science.
"""

STORY = {
    "title": "The Five Senses Test!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_senses"}]},
    "pages": [
        {"art": "p01_five", "focus": ["five", "sense"],
         "clauses": [{"phrase": "five_senses"}]},
        {"art": "p02_close", "focus": ["close"],
         "clauses": [{"phrase": "close_eyes"}]},
        {"art": "p03_what",  # a recitation page
         "clauses": [{"phrase": "what_is_it"}]},
        {"art": "p04_touch", "focus": ["touch"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "touch", "obj": "teddy"}]},
        {"art": "p05_soft", "focus": ["soft"],
         "clauses": [{"pred": "soft", "subj": {"pron": "it_m"}}]},
        {"art": "p06_open", "focus": ["open"],
         "clauses": [{"phrase": "open_eyes"}]},
        {"art": "p07_teddy", "focus": ["teddy"],
         "clauses": [{"phrase": "its_teddy"}]},
        {"art": "p08_smell_cmd", "focus": ["smell"],
         "clauses": [{"imp": "smell"}]},
        {"art": "p09_smell_flower", "focus": ["flower"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "smell", "obj": "flower"}]},
        {"art": "p10_flower", "focus": ["flower"],
         "clauses": [{"phrase": "its_flower"}]},
        {"art": "p11_listen", "focus": ["listen"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "listen"}]},
        {"art": "p12_who", "focus": ["who"],
         "clauses": [{"subj": {"pron": "who"}, "verb": "bark", "end": "?"}]},
        {"art": "p13_dog", "focus": ["dog"],
         "clauses": [{"subj": "dog", "verb": "bark"}]},
        {"art": "p14_look_see", "focus": ["see"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "look"},
                     {"subj": {"pron": "we"}, "verb": "see"}]},
        {"art": "p15_eyes", "focus": ["eye"],
         "clauses": [{"subj": {"n": "eye", "num": "pl"}, "verb": "see"}]},
        {"art": "p16_ears", "focus": ["ear"],
         "clauses": [{"subj": {"n": "ear", "num": "pl"}, "verb": "listen"}]},
        {"art": "p17_hands", "focus": ["hand"],
         "clauses": [{"subj": {"n": "hand", "num": "pl"}, "verb": "touch"}]},
        {"art": "p18_nose", "focus": ["nose"],
         "clauses": [{"subj": "nose", "verb": "smell"}]},
        {"art": "p19_five_again", "focus": ["five"],
         "clauses": [{"phrase": "five_senses"}]},
        {"art": "p20_you_try",  # a recitation page
         "clauses": [{"phrase": "now_you_try"}]},
    ],
}
