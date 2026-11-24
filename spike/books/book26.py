"""Book 26: "Animal Babies!" — age 3, у кого кто.

The cat has a kitten, the dog has a puppy, the hen has a chick, the cow has a calf, the duck has
a duckling. Each baby gets one line of its own, and the book ends where it began, with the cat.
"""

STORY = {
    "title": "Animal Babies!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_babies"}]},
    "pages": [
        {"art": "p01_cat", "focus": ["kitten"],
         "clauses": [{"has": {"subj": "cat", "obj": "kitten"}}]},
        {"art": "p02_kitten", "focus": ["kitten", "soft"],
         "clauses": [{"pred": ["small", "soft"], "subj": "kitten"}]},
        {"art": "p03_dog", "focus": ["puppy"],
         "clauses": [{"has": {"subj": "dog", "obj": "puppy"}}]},
        {"art": "p04_puppy", "focus": ["puppy", "run"],
         "clauses": [{"subj": "puppy", "verb": "run"},
                     {"subj": "puppy", "verb": "jump"}]},
        {"art": "p05_hen", "focus": ["chick"],
         "clauses": [{"has": {"subj": "hen", "obj": "chick"}}]},
        {"art": "p06_chick", "focus": ["chick", "yellow"],
         "clauses": [{"pred": ["small", "yellow"], "subj": "chick"}]},
        {"art": "p07_cow", "focus": ["calf"],
         "clauses": [{"has": {"subj": "cow", "obj": "calf"}}]},
        {"art": "p08_calf", "focus": ["calf", "happy"],
         "clauses": [{"pred": ["big", "happy"], "subj": "calf"}]},
        {"art": "p09_duck", "focus": ["duckling"],
         "clauses": [{"has": {"subj": "duck", "obj": "duckling"}}]},
        {"art": "p10_duckling", "focus": ["duckling", "float"],
         "clauses": [{"subj": "duckling", "verb": "float"}]},
        {"art": "p11_play", "focus": ["play"],
         "clauses": [{"subj": ["kitten", "puppy"], "verb": "play"}]},
        {"art": "p12_sleep", "focus": ["sleep"],
         "clauses": [{"subj": {"n": "kitten", "num": "pl"}, "verb": "sleep"}]},
        {"art": "p13_look", "focus": ["look"],
         "clauses": [{"imp": "look", "pp": ("at", "kitten")}]},
        {"art": "p14_again", "focus": ["kitten"],
         "clauses": [{"has": {"subj": "cat", "obj": "kitten"}}]},
    ],
}
