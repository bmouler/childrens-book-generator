"""Book 34: "The Orange Test!" — age 5, one fruit, two answers.

The orange floats. Guess again, take the peel off, and it sinks. Why? The peel is light,
the peel has air, and air is light. A real experiment with a real surprise, and then you eat it.
"""

W = {"n": "water", "art": "the"}

STORY = {
    "title": "The Orange Test!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_orange_test"}]},
    "pages": [
        {"art": "p01_look", "focus": ["orange"],
         "clauses": [{"imp": "look", "pp": ("at", {"n": "orange", "art": "the"})}]},
        {"art": "p02_q", "focus": ["float"],
         "clauses": [{"q_or": {"subj": "orange", "verbs": ["sink", "float"]}}]},
        {"art": "p03_guess", "focus": ["first", "guess"],
         "clauses": [{"lead": "first", "subj": {"pron": "we"}, "verb": "guess"}]},
        {"art": "p04_put", "focus": ["put"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "put", "obj": "orange",
                      "pp_to": ("in", W)}]},
        {"art": "p05_floats", "focus": ["float"],
         "clauses": [{"subj": "orange", "verb": "float"}]},
        {"art": "p06_peel", "focus": ["peel_off"],
         "clauses": [{"imp": "peel_off", "obj": "orange"}]},
        {"art": "p07_q_again", "focus": ["sink", "float"],
         "clauses": [{"q_or": {"subj": {"pron": "it_m"}, "verbs": ["sink", "float"]}}]},
        {"art": "p08_then_guess", "focus": ["then"],
         "clauses": [{"lead": "then", "subj": {"pron": "we"}, "verb": "guess",
                      "adv": "again"}]},
        {"art": "p09_put_again", "focus": ["orange"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "put", "obj": "orange",
                      "pp_to": ("in", W), "adv": "again"}]},
        {"art": "p10_sinks", "focus": ["sink"],
         "clauses": [{"subj": {"pron": "it_m"}, "verb": "sink"}]},
        {"art": "p11_peel_light", "focus": ["peel", "light"],
         "clauses": [{"pred": "light", "subj": {"n": "peel", "art": "the"}}]},
        {"art": "p12_because",  # the payoff line runs full width: a recitation page
         "clauses": [{"join": "because", "parts": [
             {"subj": "orange", "verb": "float"},
             {"pred": "light", "subj": {"n": "peel", "art": "the"}}]}]},
        {"art": "p13_air", "focus": ["air"],
         "clauses": [{"pred": "light", "subj": {"n": "air", "art": ""}}]},
        {"art": "p14_has_air", "focus": ["air"],
         "clauses": [{"has": {"subj": {"n": "peel", "art": "the"},
                              "obj": {"n": "air", "art": ""}}}]},
        {"art": "p15_at_last", "focus": ["at_last", "see"],
         "clauses": [{"lead": "at_last", "subj": {"pron": "we"}, "verb": "see"}]},
        {"art": "p16_know",  # a recitation page
         "clauses": [{"phrase": "i_know"}]},
        {"art": "p17_you_try",  # a recitation page
         "clauses": [{"phrase": "now_you_try"}]},
        {"art": "p18_eat", "focus": ["eat"],
         "clauses": [{"imp": "eat", "obj": "orange"}]},
    ],
}
