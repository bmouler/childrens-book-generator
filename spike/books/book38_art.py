"""Book 38 art: A Little Bit Scary. The page names match the `art` keys of book38.py.
A hare cub in a burrow at night, afraid of a sound, then brave with a torch.
"""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same hare cub from the reference picture"
CHARSHEET = (
    "A character reference picture of one small hare cub for a children's picture book: a soft gray "
    "hare with very long upright ears with pink inside, big worried brown eyes, a round face and a "
    "small pink nose, standing on two short legs. He wears nothing. Shown once, full body, friendly "
    "front view, centered on a plain white background with generous empty space on every side."
)
PAGES = {
    "p01_burrow": f"{T} sitting on the floor of a small round dark earth burrow at night, ears "
                  f"pressed flat to the head, eyes wide, the body low. One dark arch of the entrance "
                  f"behind him. {MARGIN} {NO_EXTRA}",
    "p02_heart": f"{T} standing in the dark burrow with both front paws pressed to the chest, eyes "
                 f"very wide, two small lines around the chest like a fast heartbeat. {MARGIN} {NO_EXTRA}",
    "p03_torch": f"{T} standing in the dark burrow and holding one small yellow torch in one front "
                 f"paw, a wide yellow light beam from the torch falling on the dark arch of the "
                 f"entrance. {MARGIN} {NO_EXTRA}",
    "p04_two": f"{T} standing in the burrow doorway and looking at one small brown hedgehog rolled "
               f"into a ball and one tiny gray mouse standing beside it, both outside on the dark "
               f"ground. {MARGIN} {NO_EXTRA}",
    "p05_come_in": f"{T} inside the warm yellow-lit burrow, one front paw raised in a welcoming "
                   f"wave, the same hedgehog and gray mouse standing beside him in the doorway. "
                   f"{MARGIN} {NO_EXTRA}",
    "p06_asleep": f"{T} lying asleep on soft dry moss in the burrow beside the sleeping tiny gray "
                  f"mouse, the hedgehog curled asleep at their feet, all lit by a soft warm yellow "
                  f"light. {MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} standing in the doorway of a dark round burrow at night, holding one small yellow "
         f"torch that lights his worried face, his long ears upright. {MARGIN} {NO_EXTRA}")