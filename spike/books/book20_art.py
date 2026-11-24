"""Book 20 art prompts: Head and Shoulders. The page names match the `art` keys of book20.py.
The toddler points at each body part: the picture must show the touch, because the chant names it.
"""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
FLOOR = "on a plain soft-green floor"

PAGES = {
    "p01_head_shoulders": f"{T} standing {FLOOR}, facing the viewer, touching the top of the own "
                          f"head with one hand and the own shoulder with the other hand, smiling. "
                          f"{MARGIN} {NO_EXTRA}",
    "p02_knees_toes": f"{T} sitting {FLOOR} with legs stretched forward, touching one knee with "
                      f"one hand and the own toes with the other hand, smiling. {MARGIN} "
                      f"{NO_EXTRA}",
    "p03_eyes_ears": f"{T} standing {FLOOR}, facing the viewer, pointing at the own eye with one "
                     f"finger and touching the own ear with the other hand, smiling. {MARGIN} "
                     f"{NO_EXTRA}",
    "p04_mouth_nose": f"{T} standing {FLOOR}, facing the viewer, pointing at the own mouth with "
                      f"one finger and at the own nose with the other finger, smiling. {MARGIN} "
                      f"{NO_EXTRA}",
    "p05_chant": f"{T} standing {FLOOR}, facing the viewer, singing with the mouth open in a big "
                 f"smile and both arms stretched out to the sides. Three small round musical "
                 f"notes float in the air. {MARGIN} {NO_EXTRA}",
    "p06_touch_head": f"{T} standing {FLOOR}, facing the viewer, touching the top of the own head "
                      f"with both hands, with a proud smile. {MARGIN} {NO_EXTRA}",
    "p07_touch_toes": f"{T} standing {FLOOR}, bent forward with straight legs, touching the own "
                      f"toes with both hands, seen from the side, with a happy effort face. "
                      f"{MARGIN} {NO_EXTRA}",
    "p08_where_nose": f"{T} standing {FLOOR}, facing the viewer with a playful question face and "
                      f"raised eyebrows, covering the own nose completely with one flat hand. "
                      f"{MARGIN} {NO_EXTRA}",
    "p09_there_it_is": f"{T} standing {FLOOR}, facing the viewer, pointing at the own nose with "
                       f"one finger, laughing with eyes closed. {MARGIN} {NO_EXTRA}",
    "p10_chant_again": f"{T} marching {FLOOR} with high knees and swinging arms, singing with the "
                       f"mouth open in a big smile. Three small round musical notes float in the "
                       f"air. {MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} standing {FLOOR}, facing the viewer, touching the top of the own head with one "
         f"hand and pointing at the viewer with the other hand, with a big inviting smile. "
         f"{MARGIN} {NO_EXTRA}")
