"""Book 24 art: Guess First! The experiment loop, three beats per thing: the guess face,
the hand putting it in, the answer in the water."""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
FLOOR = "on a plain soft-green floor"
BASIN = "one wide clear glass basin of pale blue water on the floor"

PAGES = {
    "p01_guess": f"{T} kneeling {FLOOR} beside {BASIN}, hands on cheeks, making a big guessing "
                 f"face with round eyes. {MARGIN} {NO_EXTRA}",
    "p02_ball_q": f"{T} kneeling {FLOOR}, holding one small red ball above {BASIN} with both "
                  f"hands, questioning face. {MARGIN} {NO_EXTRA}",
    "p03_we_guess": f"{T} kneeling {FLOOR} beside {BASIN}, one finger on the chin, thinking "
                    f"hard with a small question-mark face. {MARGIN} {NO_EXTRA}",
    "p04_put_ball": f"{T} kneeling {FLOOR}, lowering one small red ball into {BASIN} with one "
                    f"hand, water splashing softly. {MARGIN} {NO_EXTRA}",
    "p05_ball_floats": f"{T} kneeling {FLOOR} beside {BASIN}, clapping at one small red ball "
                       f"floating on the water surface. {MARGIN} {NO_EXTRA}",
    "p06_stone_q": f"{T} kneeling {FLOOR}, holding one round grey stone above {BASIN} with both "
                   f"hands, questioning face. {MARGIN} {NO_EXTRA}",
    "p07_first": f"{T} kneeling {FLOOR} beside {BASIN}, holding up one index finger first, then "
                 f"resting the other hand on the chin, thinking. {MARGIN} {NO_EXTRA}",
    "p08_put_stone": f"{T} kneeling {FLOOR}, lowering one round grey stone into {BASIN} with one "
                     f"hand. {MARGIN} {NO_EXTRA}",
    "p09_stone_sinks": f"{T} kneeling {FLOOR} beside {BASIN}, pointing at one round grey stone "
                       f"on the basin bottom under the water. {MARGIN} {NO_EXTRA}",
    "p10_melon_q": f"{T} kneeling {FLOOR}, hugging one whole green watermelon above {BASIN} with "
                   f"effort, questioning face. {MARGIN} {NO_EXTRA}",
    "p11_melon_floats": f"{T} kneeling {FLOOR} beside {BASIN}, arms up in happy surprise at one "
                        f"whole green watermelon floating on the water surface. {MARGIN} "
                        f"{NO_EXTRA}",
    "p12_at_last": f"{T} kneeling {FLOOR} beside {BASIN}, pointing at the floating watermelon "
                   f"with one hand and nodding, satisfied smile. {MARGIN} {NO_EXTRA}",
    "p13_we_know": f"{T} standing {FLOOR}, one index finger raised high, proud smile, {BASIN} "
                   f"beside with the floating watermelon. {MARGIN} {NO_EXTRA}",
    "p14_guess_again": f"{T} kneeling {FLOOR} beside {BASIN}, holding up one yellow feather with "
                       f"a playful guessing smile. {MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} kneeling {FLOOR} beside {BASIN}, holding a red ball over the water with one hand "
         f"and a finger on the chin with the other, big guessing face. {MARGIN} {NO_EXTRA}")
