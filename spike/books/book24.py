"""Book 24: "Guess First!" — age 3, the experiment loop begins.

Guess, put it in, look. The same three steps for every thing, so the loop itself is the lesson.
Future questions carry the guess: "Will it sink or float?"
"""

M = {"n": "water", "art": "the"}

STORY = {
    "title": "Guess First!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_guess_first"}]},
    "pages": [
        {"art": "p01_guess", "focus": ["guess"],
         "clauses": [{"imp": "guess"}]},
        {"art": "p02_ball_q", "focus": ["sink", "float"],
         "clauses": [{"q_or": {"subj": "ball", "verbs": ["sink", "float"]}}]},
        {"art": "p03_we_guess", "focus": ["first", "guess"],
         "clauses": [{"lead": "first", "subj": {"pron": "we"}, "verb": "guess"}]},
        {"art": "p04_put_ball", "focus": ["put"],
         "clauses": [{"imp": "put", "obj": "ball", "pp_to": ("in", M)}]},
        {"art": "p05_ball_floats", "focus": ["float"],
         "clauses": [{"subj": "ball", "verb": "float"}]},
        {"art": "p06_stone_q", "focus": ["stone", "sink"],
         "clauses": [{"q_or": {"subj": "stone", "verbs": ["sink", "float"]}}]},
        {"art": "p07_first",  # the loop again: a recitation page
         "clauses": [{"lead": "first", "subj": {"pron": "we"}, "verb": "guess"}]},
        {"art": "p08_put_stone", "focus": ["put"],
         "clauses": [{"imp": "put", "obj": "stone", "pp_to": ("in", M)}]},
        {"art": "p09_stone_sinks", "focus": ["sink"],
         "clauses": [{"subj": "stone", "verb": "sink"}]},
        {"art": "p10_melon_q", "focus": ["watermelon"],
         "clauses": [{"q_or": {"subj": "watermelon", "verbs": ["sink", "float"]}}]},
        {"art": "p11_melon_floats", "focus": ["but"],
         "clauses": [{"join": "but", "parts": [
             {"pred": "heavy", "subj": "watermelon"},
             {"subj": {"pron": "it_m"}, "verb": "float"}]}]},
        {"art": "p12_at_last", "focus": ["at_last", "see"],
         "clauses": [{"lead": "at_last", "subj": {"pron": "we"}, "verb": "see"}]},
        {"art": "p13_we_know",  # a recitation page
         "clauses": [{"phrase": "i_know"}]},
        {"art": "p14_guess_again", "focus": ["guess"],
         "clauses": [{"imp": "guess", "adv": "again"}]},
    ],
}
