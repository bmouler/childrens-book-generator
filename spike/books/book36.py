"""Book 36: "Count Farther!" — age 5, eleven to twenty.

Book 22 counted to ten on the body. This one keeps going: eleven stars, twelve blocks,
thirteen leaves... twenty fingers on hands and feet. Then counting by fives, fast and slowly.
"""

STORY = {
    "title": "Count Farther!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_count_farther"}]},
    "pages": [
        {"art": "p01_count", "focus": ["count"],
         "clauses": [{"phrase": "lets_count"}]},
        {"art": "p02_eleven", "focus": ["eleven", "star"],
         "clauses": [{"phrase": "eleven_stars"}]},
        {"art": "p03_twelve", "focus": ["twelve", "block"],
         "clauses": [{"phrase": "twelve_blocks"}]},
        {"art": "p04_thirteen", "focus": ["thirteen", "leaf"],
         "clauses": [{"phrase": "thirteen_leaves"}]},
        {"art": "p05_fourteen", "focus": ["fourteen", "flower"],
         "clauses": [{"phrase": "fourteen_flowers"}]},
        {"art": "p06_fifteen", "focus": ["fifteen", "apple"],
         "clauses": [{"phrase": "fifteen_apples"}]},
        {"art": "p07_sixteen", "focus": ["sixteen", "duck"],
         "clauses": [{"phrase": "sixteen_ducks"}]},
        {"art": "p08_seventeen", "focus": ["seventeen", "stone"],
         "clauses": [{"phrase": "seventeen_stones"}]},
        {"art": "p09_eighteen", "focus": ["eighteen", "cloud"],
         "clauses": [{"phrase": "eighteen_clouds"}]},
        {"art": "p10_nineteen", "focus": ["nineteen", "balloon"],
         "clauses": [{"phrase": "nineteen_balloons"}]},
        {"art": "p11_twenty", "focus": ["twenty", "finger"],
         "clauses": [{"phrase": "twenty_fingers"}]},
        {"art": "p12_fives",  # by fives: a recitation page
         "clauses": [{"phrase": "fives_chant"}]},
        {"art": "p13_fast", "focus": ["count", "fast"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "count", "adv": "fast"}]},
        {"art": "p14_slowly", "focus": ["slow"],
         "clauses": [{"subj": {"pron": "we"}, "verb": "count", "adv": "slow"}]},
        {"art": "p15_how_many", "focus": ["star"],
         "clauses": [{"phrase": "how_many_stars"}]},
        {"art": "p16_twinkle", "focus": ["star"],
         "clauses": [{"subj": {"n": "star", "num": "pl"}, "verb": "twinkle"}]},
        {"art": "p17_to_twenty", "focus": ["twenty"],
         "clauses": [{"phrase": "count_twenty"}]},
        {"art": "p18_stars_many", "focus": ["star"],
         "clauses": [{"phrase": "many_stars"}]},
        {"art": "p19_again",  # a recitation page
         "clauses": [{"phrase": "count_again"}]},
        {"art": "p20_end",  # a recitation page: one more time, bigger
         "clauses": [{"subj": {"pron": "we"}, "verb": "count"},
                     {"subj": {"pron": "we"}, "verb": "count"}]},
    ],
}
