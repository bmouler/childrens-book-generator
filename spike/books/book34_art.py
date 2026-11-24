"""Book 34 art: The Orange Test. One orange, one basin: floats whole, gets peeled, sinks.
The peel strip appears once the peeling starts."""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
FLOOR = "on a plain soft-green floor"
BASIN = "one wide clear glass basin of pale blue water on the floor"
ORANGE = "one whole round orange with a dimpled skin"

PAGES = {
    "p01_look": f"{T} kneeling {FLOOR}, holding {ORANGE} up in both hands, looking at it "
                f"closely. {MARGIN} {NO_EXTRA}",
    "p02_q": f"{T} kneeling {FLOOR}, holding {ORANGE} over {BASIN}, questioning face. {MARGIN} "
             f"{NO_EXTRA}",
    "p03_guess": f"{T} kneeling {FLOOR} beside {BASIN}, finger on the chin, thinking face. "
                 f"{MARGIN} {NO_EXTRA}",
    "p04_put": f"{T} kneeling {FLOOR}, lowering {ORANGE} into {BASIN} with both hands. {MARGIN} "
               f"{NO_EXTRA}",
    "p05_floats": f"{T} kneeling {FLOOR} beside {BASIN}, pointing at {ORANGE} floating high on "
                  f"the water. {MARGIN} {NO_EXTRA}",
    "p06_peel": f"{T} kneeling {FLOOR}, peeling {ORANGE}: one long strip of orange peel pulled "
                f"away in one hand, the fruit half bare in the other. {MARGIN} {NO_EXTRA}",
    "p07_q_again": f"{T} kneeling {FLOOR}, holding the bare peeled orange over {BASIN}, "
                   f"questioning face. {MARGIN} {NO_EXTRA}",
    "p08_then_guess": f"{T} kneeling {FLOOR} beside {BASIN} and the peel strip on the floor, "
                      f"finger on the chin again. {MARGIN} {NO_EXTRA}",
    "p09_put_again": f"{T} kneeling {FLOOR}, lowering the bare peeled orange into {BASIN} with "
                     f"one hand. {MARGIN} {NO_EXTRA}",
    "p10_sinks": f"A side view of {BASIN} with a bare peeled orange sunk deep under the pale "
                 f"blue water, well below the surface, clearly not floating. The toddler from "
                 f"the reference picture kneels behind the basin with hands on cheeks in "
                 f"surprise. {MARGIN} {NO_EXTRA}",
    "p11_peel_light": f"One long curled strip of orange peel lying alone {FLOOR}, soft light. "
                      f"{MARGIN} {NO_EXTRA}",
    "p12_because": f"{T} kneeling {FLOOR} beside {BASIN}: {ORANGE} floating in the water on one "
                   f"side and its peel strip held up in one hand on the other, comparing. "
                   f"{MARGIN} {NO_EXTRA}",
    "p13_air": f"Three small round pale-blue bubbles floating gently upward in soft light. "
               f"{MARGIN} {NO_EXTRA}",
    "p14_has_air": f"A close view of one strip of orange peel with three small pale-blue round "
                   f"bubbles held inside it. {MARGIN} {NO_EXTRA}",
    "p15_at_last": f"{T} standing {FLOOR} beside {BASIN} with the floating orange and the peel "
                   f"strip on the floor, arms open in a proud understood pose. {MARGIN} "
                   f"{NO_EXTRA}",
    "p16_know": f"{T} standing {FLOOR}, one index finger raised high, bright knowing smile. "
                f"{MARGIN} {NO_EXTRA}",
    "p17_you_try": f"{T} kneeling {FLOOR}, holding out {ORANGE} toward the viewer with both "
                   f"hands, inviting smile. {MARGIN} {NO_EXTRA}",
    "p18_eat": f"{T} sitting cross-legged {FLOOR}, happily biting into one juicy orange slice, "
               f"eyes closed. {MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} kneeling {FLOOR} beside {BASIN}, holding {ORANGE} over the water with both "
         f"hands, questioning face. {MARGIN} {NO_EXTRA}")
