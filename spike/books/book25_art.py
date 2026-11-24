"""Book 25 art: In and Out! One cardboard box, one tote bag, the ball and the teddy bear.
Every picture keeps the same plain room corner."""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
FLOOR = "on a plain soft-green floor"
BOX = "one open brown cardboard box"

PAGES = {
    "p01_hide": f"{T} kneeling {FLOOR}, peeking into {BOX} where one small red ball lies inside, "
                f"one hand on the box rim. {MARGIN} {NO_EXTRA}",
    "p02_where": f"{T} kneeling {FLOOR} beside the closed side of {BOX}, palms up in a searching "
                 f"shrug, big questioning eyes. {MARGIN} {NO_EXTRA}",
    "p03_in_box": f"{T} kneeling {FLOOR}, pointing into {BOX} at the small red ball inside it. "
                  f"{MARGIN} {NO_EXTRA}",
    "p04_take_out": f"{T} kneeling {FLOOR}, lifting the small red ball up out of {BOX} with both "
                    f"hands, happy. {MARGIN} {NO_EXTRA}",
    "p05_play": f"{T} standing {FLOOR}, rolling the small red ball along the floor with one "
                f"hand, laughing. {MARGIN} {NO_EXTRA}",
    "p06_put_ball": f"{T} kneeling {FLOOR}, lowering the small red ball into {BOX} with one "
                    f"hand. {MARGIN} {NO_EXTRA}",
    "p07_under": f"{T} kneeling {FLOOR}, sliding one brown teddy bear under {BOX} so the bear "
                 f"peeks out from under the rim. {MARGIN} {NO_EXTRA}",
    "p08_where_teddy": f"{T} kneeling {FLOOR} beside {BOX}, hands on cheeks, searching face, the "
                       f"teddy bear just visible under the box. {MARGIN} {NO_EXTRA}",
    "p09_teddy_under": f"{T} kneeling {FLOOR}, lifting one side of {BOX} to reveal the brown "
                       f"teddy bear lying under it. {MARGIN} {NO_EXTRA}",
    "p10_take_teddy": f"{T} standing {FLOOR}, hugging the brown teddy bear happily after pulling "
                      f"it out, the box behind. {MARGIN} {NO_EXTRA}",
    "p11_bag": f"{T} kneeling {FLOOR} beside one soft yellow tote bag, the small red ball "
               f"peeking out of the open top. {MARGIN} {NO_EXTRA}",
    "p12_where_ball": f"{T} kneeling {FLOOR}, pointing at the lumpy yellow tote bag with a "
                      f"knowing smile, one finger on the chin. {MARGIN} {NO_EXTRA}",
    "p13_out_bag": f"{T} kneeling {FLOOR}, pulling the small red ball out of the yellow tote bag "
                   f"with both hands, delighted. {MARGIN} {NO_EXTRA}",
    "p14_end": f"{T} standing {FLOOR}, holding the small red ball up in one hand and the teddy "
               f"bear under the other arm, waving. {MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} kneeling {FLOOR} between {BOX} and the yellow tote bag, holding the small red "
         f"ball up with a big smile. {MARGIN} {NO_EXTRA}")
