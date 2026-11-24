"""Book 30 art: Sink or Float, the Big Test. The basin again, one thing per test, guess
faces first and results after. The chart page itself is drawn by code, not generated."""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
FLOOR = "on a plain soft-green floor"
BASIN = "one wide clear glass basin of pale blue water on the floor"

PAGES = {
    "p01_test": f"{T} kneeling {FLOOR} beside {BASIN} with one grey stone, one white feather and "
                 f"one red ball lined up on the floor, pointing at the basin. {MARGIN} "
                 f"{NO_EXTRA}",
    "p02_water": f"A close view of {BASIN} alone, calm pale blue water, no objects in it. "
                 f"{MARGIN} {NO_EXTRA}",
    "p03_guess": f"{T} kneeling {FLOOR} beside {BASIN}, finger on the chin, big thinking face. "
                 f"{MARGIN} {NO_EXTRA}",
    "p04_stone_q": f"{T} kneeling {FLOOR}, holding one round grey stone over {BASIN}, "
                   f"questioning face. {MARGIN} {NO_EXTRA}",
    "p05_stone_sinks": f"{T} kneeling {FLOOR} beside {BASIN}, pointing at one round grey stone "
                       f"on the basin bottom under the water. {MARGIN} {NO_EXTRA}",
    "p06_feather_q": f"{T} kneeling {FLOOR}, holding one white feather over {BASIN}, "
                     f"questioning face. {MARGIN} {NO_EXTRA}",
    "p07_feather_floats": f"{T} kneeling {FLOOR} beside {BASIN}, pointing at one white feather "
                          f"floating flat on the water. {MARGIN} {NO_EXTRA}",
    "p08_ball_q": f"{T} kneeling {FLOOR}, holding one small red ball over {BASIN}, questioning "
                  f"face. {MARGIN} {NO_EXTRA}",
    "p09_ball_floats": f"{T} kneeling {FLOOR} beside {BASIN}, clapping at the small red ball "
                       f"floating on the water. {MARGIN} {NO_EXTRA}",
    "p10_melon_q": f"{T} kneeling {FLOOR}, hugging one whole green watermelon over {BASIN}, "
                   f"effort and questioning face. {MARGIN} {NO_EXTRA}",
    "p11_melon_floats": f"{T} kneeling {FLOOR} beside {BASIN}, arms up in surprise at the whole "
                        f"green watermelon floating high on the water. {MARGIN} {NO_EXTRA}",
    "p12_apple_q": f"{T} kneeling {FLOOR}, holding one small red apple over {BASIN}, "
                   f"questioning face. {MARGIN} {NO_EXTRA}",
    "p13_apple_floats": f"{T} kneeling {FLOOR} beside {BASIN}, pointing at one red apple "
                        f"bobbing on the water. {MARGIN} {NO_EXTRA}",
    "p14_box_q": f"{T} kneeling {FLOOR}, holding one small brown cardboard box over {BASIN} with "
                 f"both hands, questioning face. {MARGIN} {NO_EXTRA}",
    "p15_box_floats": f"{T} kneeling {FLOOR} beside {BASIN}, pointing at one small brown "
                      f"cardboard box floating like a boat on the water. {MARGIN} {NO_EXTRA}",
    "p17_at_last": f"{T} standing {FLOOR} beside {BASIN}, both arms open wide in a proud "
                   f"finished-test pose. {MARGIN} {NO_EXTRA}",
    "p18_know": f"{T} standing {FLOOR}, one index finger raised high, bright knowing smile, "
                f"{BASIN} beside. {MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} kneeling {FLOOR} beside {BASIN}, a grey stone, a white feather and a red ball "
         f"lined up in front, finger on the chin. {MARGIN} {NO_EXTRA}")
