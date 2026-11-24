"""Book 26 art: Animal Babies! Mother and baby of each farm animal on plain grass.
One mother, exactly one baby per picture."""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
GRASS = "standing close together on plain flat green grass"

PAGES = {
    "p01_cat": f"One calm mother cat {GRASS} with exactly one small grey kitten beside her, the "
               f"kitten looking up at her. {MARGIN} {NO_EXTRA}",
    "p02_kitten": f"One small fluffy grey kitten sitting alone on plain flat green grass, "
                  f"looking at the viewer with big eyes. {MARGIN} {NO_EXTRA}",
    "p03_dog": f"One friendly mother dog {GRASS} with exactly one small puppy beside her, the "
               f"puppy's tail mid-wag. {MARGIN} {NO_EXTRA}",
    "p04_puppy": f"One small brown puppy alone on plain flat green grass, mid-jump with ears up, "
                 f"joyful. {MARGIN} {NO_EXTRA}",
    "p05_hen": f"One mother hen {GRASS} with exactly one small yellow chick beside her. "
               f"{MARGIN} {NO_EXTRA}",
    "p06_chick": f"One small round yellow chick standing alone on plain flat green grass, beak "
                 f"open in a tiny cheep. {MARGIN} {NO_EXTRA}",
    "p07_cow": f"One mother cow {GRASS} with exactly one calf beside her, the calf nuzzling her "
               f"side. {MARGIN} {NO_EXTRA}",
    "p08_calf": f"One brown-and-white calf alone on plain flat green grass, tail up, playful "
                f"buck. {MARGIN} {NO_EXTRA}",
    "p09_duck": f"One mother duck {GRASS} with exactly one small duckling beside her. {MARGIN} "
                f"{NO_EXTRA}",
    "p10_duckling": f"One small yellow duckling swimming alone on calm flat blue water, little "
                    f"ripple rings around it. {MARGIN} {NO_EXTRA}",
    "p11_play": f"One small grey kitten and one small brown puppy chasing each other on plain "
                f"flat green grass, both mid-run. {MARGIN} {NO_EXTRA}",
    "p12_sleep": f"Exactly three small grey kittens curled asleep together on plain flat green "
                 f"grass, eyes closed. {MARGIN} {NO_EXTRA}",
    "p13_look": f"The same toddler from the reference picture kneeling on plain flat green "
                f"grass, gently petting one small grey kitten. {MARGIN} {NO_EXTRA}",
    "p14_again": f"One mother cat lying on her side on plain flat green grass, exactly one "
                 f"small grey kitten snuggled against her, both eyes closed. {MARGIN} {NO_EXTRA}",
}
COVER = ("One mother cat and exactly one small grey kitten sitting close together on plain flat "
         "green grass, the kitten looking up. MARGIN NO_EXTRA".replace("MARGIN", MARGIN).replace(
             "NO_EXTRA", NO_EXTRA))
