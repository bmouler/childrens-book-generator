"""Book 22 art prompts: Count With Me! The page names match the `art` keys of book22.py.
The body pages show exactly the counted body parts. The space pages keep the counts exact:
one sun, exactly eight planets, one Earth, and too many stars to count.
"""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
FLOOR = "on a plain soft-green floor"
SUN = "one big bright yellow sun with short triangular rays and a small friendly smile"

PAGES = {
    "p01_lets_count": f"{T} standing {FLOOR}, facing the viewer with a big smile, holding up both "
                      f"open hands with all fingers spread, ready to count. {MARGIN} {NO_EXTRA}",
    "p02_one_nose": f"A close-up of the toddler from the reference picture, head and shoulders "
                    f"only, facing the viewer, touching the tip of the own nose with one finger, "
                    f"smiling. {MARGIN} {NO_EXTRA}",
    "p03_two_eyes": f"A close-up of the toddler from the reference picture, head and shoulders "
                    f"only, pointing at the own two eyes with the two index fingers, with wide "
                    f"happy eyes. {MARGIN} {NO_EXTRA}",
    "p04_two_ears": f"A close-up of the toddler from the reference picture, head and shoulders "
                    f"only, touching the own two ears with both hands, listening with a curious "
                    f"smile. {MARGIN} {NO_EXTRA}",
    "p05_five_fingers": f"{T} standing {FLOOR}, holding one open hand up toward the viewer with "
                        f"all five fingers spread wide, looking at the own hand and counting. The "
                        f"other hand rests at the side. Exactly five fingers on the raised hand. "
                        f"{MARGIN} {NO_EXTRA}",
    "p06_ten_toes": f"{T} sitting {FLOOR} with bare feet stretched forward toward the viewer, "
                    f"leaning on both hands behind, looking down at the own ten toes and wiggling "
                    f"them, laughing. Both bare feet are fully visible with exactly ten toes. "
                    f"{MARGIN} {NO_EXTRA}",
    "p07_count_chant": f"{T} standing {FLOOR}, facing the viewer, chanting with the mouth open "
                       f"and folding down fingers one by one on one raised hand. {MARGIN} "
                       f"{NO_EXTRA}",
    "p08_one_sun": f"{T} standing outdoors on plain flat green grass, pointing up at {SUN} in a "
                   f"clear light-blue sky. There is exactly one sun and there are no clouds. "
                   f"{MARGIN} {NO_EXTRA}",
    "p09_eight_planets": f"Show a deep-blue space scene (the whole background is deep night blue, not white), with with {SUN} in the middle and exactly "
                         f"eight small round planets around it in a loose ring, each a different "
                         f"colour and size. The toddler from the reference picture floats at the "
                         f"side in a small white astronaut suit, pointing at the planets. There "
                         f"are exactly eight planets. {MARGIN} {NO_EXTRA}",
    "p10_earth": f"Show one planet Earth in deep-blue space: a round blue planet with green land "
                 f"shapes and small white cloud swirls. The toddler from the reference picture "
                 f"floats beside it in a small white astronaut suit, waving at the viewer. There "
                 f"is exactly one planet in the picture. {MARGIN} {NO_EXTRA}",
    "p11_many_stars": f"{T} standing outdoors on plain flat ground at night, seen from behind, "
                      f"looking up at a deep-blue night sky completely full of many small white "
                      f"five-pointed stars of different sizes, too many to count. {MARGIN} "
                      f"{NO_EXTRA}",
    "p12_count_again": f"{T} standing {FLOOR}, facing the viewer with a big inviting smile, "
                       f"holding up both open hands with all ten fingers spread. {MARGIN} "
                       f"{NO_EXTRA}",
}
COVER = (f"{T} standing {FLOOR}, facing the viewer, holding up one open hand with five fingers "
         f"spread and pointing at the fingers with the other index finger, counting with a happy "
         f"smile. {MARGIN} {NO_EXTRA}")
