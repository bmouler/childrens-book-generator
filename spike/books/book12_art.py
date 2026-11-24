"""Book 12 art prompts: The Turnip (Репка). The page names match the `art` keys of book12.py.
No toddler hero: the folk-tale cast gets its own character sheet, generated first into
out/book12/charsheet.png and used as the reference picture of every page.
"""

GP = "Grandpa, an old man with a round friendly face, a gray beard and mustache, a red shirt and brown pants"
GM = "Grandma, an old woman with gray hair in a bun, round glasses, a blue dress and a white apron"
GD = "the granddaughter, a little girl with brown hair in two braids, wearing a red dress"
DOG = "a small brown dog with floppy ears"
CAT = "a small orange cat with a striped tail"
MOUSE = "a tiny gray mouse with big round ears"
TURNIP = "one huge round yellow turnip with big green leaves on top, sitting in the brown soil of a garden bed"
NO_EXTRA = "No other objects, no decoration."
MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."

CHARSHEET = (
    "Character reference picture for a folk-tale picture book. Show each of these characters once, "
    "full body, standing side by side in one row on a plain white background with generous space around "
    f"them: {GP}; {GM}; {GD}; {DOG}; {CAT}; {MOUSE}; and a huge round yellow turnip with big green "
    "leaves. Friendly smiling faces, front view."
)
KEEP = (
    "Keep the same character designs from the reference picture: the same shapes, colours, "
    "line weight and flat vector style."
)

PAGES = {
    "p01_once": f"Show {GP} and {GM} standing side by side in front of a small wooden house with a "
                f"brown garden bed beside it. Both wave at the viewer and smile. {MARGIN} {NO_EXTRA}",
    "p01_grandpa_plants": f"Show {GP} kneeling in a garden bed of brown soil. He places one small yellow "
                          f"turnip root with tiny green leaves into the soil with both hands. There is only "
                          f"one small turnip root in the picture. {NO_EXTRA}",
    "p03_turnip_big": f"Show {TURNIP}. The turnip is very big but sits in the middle of the picture "
                      f"with empty pale sky all around its leaves. No people. {MARGIN} {NO_EXTRA}",
    "p04_grandpa_pulls": f"Show {GP} standing behind {TURNIP}, gripping its green leaves with both hands "
                         f"and leaning far back, pulling hard. His cheeks are puffed. The turnip stays in "
                         f"the soil. {NO_EXTRA}",
    "p05_grandma_comes": f"Show {GP} gripping the green leaves of {TURNIP} and {GM} standing behind Grandpa, "
                         f"holding his waist with both hands. Both lean back and pull. The turnip stays in "
                         f"the soil. {NO_EXTRA}",
    "p06_granddaughter_comes": f"Show {GP} gripping the green leaves of {TURNIP}, {GM} holding Grandpa's "
                               f"waist, and {GD} holding Grandma's waist at the end of the line. All three "
                               f"lean back and pull. The turnip stays in the soil. {NO_EXTRA}",
    "p07_dog_comes": f"Show {GP} gripping the green leaves of {TURNIP}, {GM} holding Grandpa's waist, "
                     f"and {GD} holding Grandma's waist at the end of the line. All three lean back and "
                     f"pull. Beside the line stands {DOG}, barking at the turnip with its mouth open "
                     f"and two curved sound lines by its mouth. The turnip stays in the soil. "
                     f"{MARGIN} {NO_EXTRA}",
    "p08_cat_comes": f"Show {GP} gripping the green leaves of {TURNIP}, {GM} holding Grandpa's waist, "
                     f"{GD} holding Grandma's waist, and {DOG} holding the granddaughter's dress hem "
                     f"gently in its mouth at the end of the line. All lean back and pull. Beside the "
                     f"dog sits {CAT}, meowing up at the line with its mouth open and two curved sound "
                     f"lines by its mouth. The turnip stays in the soil. {MARGIN} {NO_EXTRA}",
    "p09_mouse_comes": f"Show {GP} gripping the green leaves of {TURNIP}, {GM} holding Grandpa's waist, "
                       f"{GD} holding Grandma's waist, {DOG} holding the dress hem, and {CAT} holding "
                       f"onto the dog's back with its front paws. All lean back and pull. At the end of "
                       f"the line stands {MOUSE}, looking up at the cat, much smaller than everyone. "
                       f"The turnip stays in the soil. {MARGIN} {NO_EXTRA}",
    "chain_dog": f"Show {GP} gripping the green leaves of {TURNIP}, {GM} holding Grandpa's waist, {GD} "
                 f"holding Grandma's waist, and {DOG} holding the granddaughter's dress hem gently in "
                 f"its mouth at the end of the line. All four lean back and pull. The turnip stays in "
                 f"the soil. No cat. {MARGIN} {NO_EXTRA}",
    "chain_cat": f"Show {GP} gripping the green leaves of {TURNIP}, {GM} holding Grandpa's waist, {GD} "
                 f"holding Grandma's waist, {DOG} holding the granddaughter's dress hem gently in its "
                 f"mouth, and {CAT} holding onto the dog's back with its front paws at the end of the "
                 f"line. All five lean back and pull. The turnip stays in the soil. No mouse. "
                 f"{MARGIN} {NO_EXTRA}",
    "chain_mouse": f"Show {GP} gripping the green leaves of {TURNIP}, {GM} holding Grandpa's waist, "
                   f"{GD} holding Grandma's waist, {DOG} holding the dress hem, {CAT} holding the "
                   f"dog's back, and {MOUSE} holding onto the cat's back with its tiny front paws at "
                   f"the very end. All seven lean back and pull hard with puffed cheeks. The turnip "
                   f"stays deep in the soil and does not move. {MARGIN} {NO_EXTRA}",
    "p11_turnip_tumbles": f"Show {TURNIP} flying up high out of the soil, and {GP}, {GM}, {GD}, {DOG}, "
                          f"{CAT} and {MOUSE} fallen backward in one happy heap on the grass, arms and "
                          f"legs up in the air, all laughing. {MARGIN} {NO_EXTRA}",
    "p12_all_eat": f"Show {GP}, {GM}, {GD}, {DOG}, {CAT} and {MOUSE} sitting in a circle on green grass "
                   f"around one big round wooden bowl filled with yellow turnip slices. Each one holds "
                   f"a slice and eats it happily. Exactly six characters, no other people, no boy. "
                   f"{MARGIN} {NO_EXTRA}",
}
COVER = f"Show {GP} standing next to {TURNIP}, resting one hand on the turnip and waving at the viewer " \
        f"with the other hand. Both smile. {NO_EXTRA}"
KEEP_FOR = {**{name: KEEP for name in PAGES}, "cover": KEEP}
