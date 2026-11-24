"""Book 36 art: Count Farther! Eleven to twenty, exact. Every counted picture names its
count in the prompt and must show exactly that many, evenly spread and easy to count."""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
FLOOR = "on a plain soft-green floor"
SKY = "in a clear light-blue sky"

PAGES = {
    "p01_count": f"{T} standing {FLOOR}, holding up both open hands with all fingers spread, "
                 f"ready to count on. {MARGIN} {NO_EXTRA}",
    "p02_eleven": f"Exactly eleven small white five-pointed stars spread evenly {SKY}. Count "
                  f"them: eleven, no more, no fewer. {MARGIN} {NO_EXTRA}",
    "p03_twelve": f"Twelve small wooden building blocks laid out flat in exactly two rows of "
                  f"six, every block separate on its own square, clear space between all blocks, "
                  f"no stacks, no child, no person. Count the rows: six and six make twelve. "
                  f"{MARGIN} {NO_EXTRA}",
    "p04_thirteen": f"Thirteen green leaves arranged in exactly two rows on plain flat pale "
                    f"ground: six leaves in the top row and seven in the bottom row, every leaf "
                    f"separate with clear space, no child, no person. Count the rows: six and "
                    f"seven make thirteen. {MARGIN} {NO_EXTRA}",
    "p05_fourteen": f"Fourteen red flowers with green stems arranged in exactly two rows of "
                    f"seven on plain flat green grass, every flower separate with clear space, no "
                    f"overlaps. Count the rows: seven and seven make fourteen. {MARGIN} "
                    f"{NO_EXTRA}",
    "p06_fifteen": f"Exactly fifteen red apples arranged in three neat rows of five {FLOOR}. "
                   f"{MARGIN} {NO_EXTRA}",
    "p07_sixteen": f"Exactly sixteen yellow ducks standing together on plain flat green grass "
                   f"by calm water. {MARGIN} {NO_EXTRA}",
    "p08_seventeen": f"Seventeen round grey stones arranged in exactly three rows: five stones "
                     f"in the first row, six in the second, six in the third, every stone "
                     f"separate with clear space, no child, no person. Count the rows: five and "
                     f"six and six make seventeen. {MARGIN} {NO_EXTRA}",
    "p09_eighteen": f"Eighteen soft white round clouds of different sizes arranged in exactly "
                    f"three rows: six clouds in the first row, six in the second, six in the "
                    f"third, every cloud separate, no child, no person. Count the rows: six and "
                    f"six and six make eighteen. {MARGIN} {NO_EXTRA}",
    "p10_nineteen": f"Nineteen separate round balloons in red, yellow, blue and green, arranged "
                    f"in four neat rows from top to bottom: four balloons in the first row, five "
                    f"in the second, five in the third, five in the fourth. Clear space between "
                    f"every balloon, no overlaps, no child, no person, {SKY}. Count the rows: "
                    f"four and five and five and five make nineteen. {MARGIN} {NO_EXTRA}",
    "p11_twenty": f"{T} standing {FLOOR}, holding up both open hands with all ten fingers "
                  f"spread and both bare feet forward, exactly ten fingers and ten toes "
                  f"visible. {MARGIN} {NO_EXTRA}",
    "p12_fives": f"{T} standing {FLOOR}, one open hand held up showing five fingers, the other "
                 f"hand pointing, counting by fives. {MARGIN} {NO_EXTRA}",
    "p13_fast": f"{T} standing {FLOOR}, counting fast with one hand flicking through the "
                f"fingers, quick motion lines at the hand. {MARGIN} {NO_EXTRA}",
    "p14_slowly": f"{T} standing {FLOOR}, counting slowly with one finger held up, calm face, "
                  f"one slow curving motion line. {MARGIN} {NO_EXTRA}",
    "p15_how_many": f"{T} standing outside on plain flat ground at night, hand above the eyes, "
                    f"looking up at a sky of many small white stars. {MARGIN} {NO_EXTRA}",
    "p16_twinkle": f"A deep-blue night sky full of small white twinkling five-pointed stars of "
                   f"different sizes. {MARGIN} {NO_EXTRA}",
    "p17_to_twenty": f"{T} standing {FLOOR}, both open hands up with all ten fingers spread and "
                     f"one bare foot forward, proud count-done smile. {MARGIN} {NO_EXTRA}",
    "p18_stars_many": f"{T} standing outside on plain flat ground at night, seen from behind, "
                      f"looking up at a whole sky of many white stars, too many to count. "
                      f"{MARGIN} {NO_EXTRA}",
    "p19_again": f"{T} standing {FLOOR}, both arms open wide in a big again-again invitation. "
                 f"{MARGIN} {NO_EXTRA}",
    "p20_end": f"{T} standing {FLOOR}, clapping above the head with a big happy count-done "
               f"grin. {MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} standing {FLOOR}, holding up both open hands with all ten fingers spread while "
         f"small white stars float above, counting on. {MARGIN} {NO_EXTRA}")
