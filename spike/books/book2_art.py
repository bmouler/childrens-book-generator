"""Book 2 art prompts: Hot or Cold? The page names match the `art` keys of book2.py."""

ICE = (
    "one small white round plate with exactly three light-blue ice cubes on it, side by side in one row "
    "and not stacked, each cube with a small white shine mark"
)
ICE_END = "There are exactly three ice cubes and only one plate in the picture."
BOWL = "one white bowl of orange soup"
STEAM3 = "Exactly three wavy white steam lines with dark-navy outlines rise from the soup."
TABLE = "a small low wooden table"
CALM = "There are no bubbles, no sparkles and no snowflakes."
WINTER = (
    "Keep the same toddler face, hair and flat vector style from the reference picture, but dress the "
    "toddler in a warm red winter coat, a blue knitted hat and blue mittens instead of the yellow "
    "t-shirt and blue shorts, with the same line weight."
)

PAGES = {
    "p01_see_ice": f"Show the same toddler from the reference picture kneeling on the floor next to {ICE}, the plate on the floor in front of the toddler's knees. The toddler looks at the ice with curious wide eyes and a small gentle smile, hands resting on the knees. {ICE_END} {CALM}",
    "p02_ice_ask": f"Show the same toddler from the reference picture sitting cross-legged on the floor in front of {ICE}, with one finger raised to the chin and the head tilted in a curious thinking pose. {ICE_END} {CALM} There is no question mark.",
    "p03_ice_cold": f"Show the same toddler from the reference picture kneeling on the floor next to {ICE}, touching the top of one ice cube with one fingertip. The toddler has a surprised happy face and raised shoulders, as if feeling a little chill. Exactly three small light-blue snowflakes float above the ice. {ICE_END}",
    "p04_see_soup": f"Show the same toddler from the reference picture sitting on a small chair at {TABLE}, looking at {BOWL} that stands in the middle of the table, far from the toddler. {STEAM3} Both of the toddler's hands lie flat on the toddler's own knees, below the table top and far away from the bowl. The toddler does not touch the bowl. There is only one bowl, one table and one chair in the picture, and there is no spoon.",
    "p05_soup_ask": f"Show the same toddler from the reference picture sitting on a small chair at {TABLE}, leaning back a little with the head tilted in a curious thinking pose, looking at {BOWL} that stands in the middle of the table. {STEAM3} Both of the toddler's hands rest in the lap. There is only one bowl, one table and one chair in the picture, and there is no spoon. There is no question mark.",
    "p06_soup_hot": f"Show the same toddler from the reference picture sitting on a small chair at {TABLE}, leaning back away from {BOWL} that stands in the middle of the table. Thick steam rises from the soup: exactly five tall wavy white steam lines with dark-navy outlines. The toddler has big surprised eyes and holds one open hand up, palm out, like a stop sign, well away from the bowl. The toddler's hands do not touch the bowl. There is only one bowl, one table and one chair in the picture, and there is no spoon.",
    "p07_sun_hot": "Show the same toddler from the reference picture standing outdoors on plain flat sandy ground, wearing a floppy white sun hat as well as the yellow t-shirt and blue shorts, looking at the viewer with a smile. One big bright yellow sun without a face, with short triangular rays, shines in the upper right part of the picture, fully inside the picture with empty space between the sun and the picture edges. Wavy orange heat lines rise from the ground beside the toddler. There is only one sun in the picture and there are no clouds.",
    "p08_snow_cold": "Show the same toddler from the reference picture standing in the snow next to one small round white snowman with a carrot nose and two stick arms. The toddler shivers with a happy face. Light-blue snowflakes fall around them. The ground is plain white-blue snow.",
    "p09_ice_soup": f"Show the same toddler from the reference picture standing behind {TABLE}, facing the viewer and smiling, with both arms open wide. On the left half of the table is {ICE}. On the right half of the table is {BOWL}. {STEAM3} One of the toddler's open hands is held high above the ice and the other open hand is held high above the soup, with clear empty space between each hand and the food. The toddler touches neither the ice nor the bowl. {ICE_END} There is only one bowl and one table in the picture, and there is no spoon. {CALM}",
    "p10_touch_ice": f"Show the same toddler from the reference picture kneeling on the floor next to {ICE}, smiling at the viewer and holding one open hand out toward the viewer in an inviting gesture. {ICE_END} {CALM}",
}
COVER = (
    "Show the same toddler from the reference picture standing and smiling in the middle of the picture, "
    "facing the viewer. On the floor at the left side of the picture lies a small pile of exactly three "
    "light-blue ice cubes, each with a small white shine mark, and one small light-blue snowflake floats "
    f"above them. On the floor at the right side of the picture stands {BOWL}. {STEAM3} "
    "There are exactly three ice cubes, one snowflake and only one bowl in the picture, and there is no plate and no spoon."
)
KEEP_FOR = {"p08_snow_cold": WINTER}
