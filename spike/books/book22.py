"""Book 22: "Count With Me!" — numbers on the body, then numbers in space.

One nose, two eyes, two ears, five fingers, ten toes — then the same counting looks up: one sun,
eight planets, our Earth, and more stars than we can count. Numerals are fixed phrases because
Russian numerals govern the noun's case (два глаза, пять пальчиков, восемь планет). The chant
"one, two, three, four, five!" sits in the middle, and the book ends where it began: считай со
мной опять!
"""


STORY = {
    "title": "Count With Me!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_count"}]},
    "pages": [
        {"art": "p01_lets_count", "focus": ["count"],
         "clauses": [{"phrase": "lets_count"}]},
        {"art": "p02_one_nose", "focus": ["one", "nose"],
         "clauses": [{"phrase": "one_nose"}]},
        {"art": "p03_two_eyes", "focus": ["two", "eye"],
         "clauses": [{"phrase": "two_eyes"}]},
        {"art": "p04_two_ears", "focus": ["ear"],
         "clauses": [{"phrase": "two_ears"}]},
        {"art": "p05_five_fingers", "focus": ["five", "finger"],
         "clauses": [{"phrase": "five_fingers"}]},
        {"art": "p06_ten_toes", "focus": ["ten", "toe"],
         "clauses": [{"phrase": "ten_toes"}]},
        {"art": "p07_count_chant",  # the chant: a recitation page, no cards
         "clauses": [{"phrase": "count_chant"}]},
        {"art": "p08_one_sun", "focus": ["sun"],
         "clauses": [{"phrase": "one_sun"}]},
        {"art": "p09_eight_planets", "focus": ["eight", "planet"],
         "clauses": [{"phrase": "eight_planets"}]},
        {"art": "p10_earth", "focus": ["earth"],
         "clauses": [{"phrase": "on_earth"}]},
        {"art": "p11_many_stars", "focus": ["star"],
         "clauses": [{"phrase": "many_stars"}]},
        {"art": "p12_count_again",  # the bookend: a recitation page
         "clauses": [{"phrase": "count_again"}]},
    ],
}
