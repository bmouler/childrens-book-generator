"""Book 11 art prompts: Ice Melts. The page names match the `art` keys of book11.py."""
import styles

T = styles.TUB
PLATE = "one small white round plate"
ICE = (
    f"{PLATE} with exactly three light-blue ice cubes on it, side by side in one row and not stacked, "
    "each cube with a small white shine mark"
)
ICE_END = "There are exactly three ice cubes and only one plate in the picture."
CUBE = "one light-blue ice cube with a small white shine mark"
TABLE = "a small low wooden table"
SUN = (
    "One big bright yellow sun without a face, with short triangular rays, shines in the upper right part "
    "of the picture, fully inside the picture with empty space between the sun and the picture edges. "
    "There is only one sun in the picture and there are no clouds."
)
CALM = "There are no bubbles, no sparkles and no snowflakes."
NO_TEXT = "There is no question mark and no text."

PAGES = {
    "p01_see_ice": f"Show the same toddler from the reference picture kneeling on the floor next to {ICE}, the plate on the floor in front of the toddler's knees. The toddler looks at the ice with curious wide eyes and a small gentle smile, hands resting on the knees. {ICE_END} {CALM}",
    "p02_ice_cold": f"Show the same toddler from the reference picture kneeling on the floor next to {ICE}, touching the top of one ice cube with one fingertip. The toddler has a surprised happy face and raised shoulders, as if feeling a little chill. Exactly three small light-blue snowflakes float above the ice. {ICE_END}",
    "p03_ice_ask": f"Show the same toddler from the reference picture standing on the floor outside the tub, next to it, holding {CUBE} between the fingers of one hand above {T}, about to drop it, head tilted with a curious expression. The ice cube is in the air above the water and does not touch the water yet. There is only one tub and exactly one ice cube in the picture, and there is no plate. {CALM} {NO_TEXT}",
    "p04_ice_floats": f"Show the same toddler from the reference picture standing on the floor outside the tub, next to it, smiling and pointing at {CUBE} floating in the water inside {T}. Draw the water line across the ice cube within the top tenth of the cube. About ninety percent of the cube is below the water line and visible through the clear water. Only a very thin top cap sticks out above the water. Do not show half of the cube above the water. The cube does not touch the bottom of the tub. There is only one tub and exactly one ice cube in the picture, and there is no plate. {CALM}",
    "p05_sun_hot": f"Show the same toddler from the reference picture standing outdoors on plain flat sandy ground next to {TABLE}, wearing a floppy white sun hat as well as the yellow t-shirt and blue shorts, looking at the viewer with a smile. On the table is {ICE}. {SUN} {ICE_END} There is only one table in the picture. {CALM}",
    "p06_wait": f"Show the same toddler from the reference picture sitting cross-legged on the floor next to {ICE}, the plate on the floor in front of the toddler, with the chin resting on one hand and a calm, patient face, watching the ice. {SUN} {ICE_END} {CALM}",
    "p07_ice_small": f"Show the same toddler from the reference picture kneeling on the floor and leaning close to {PLATE}, looking at it closely with wide curious eyes. On the plate is exactly one small light-blue ice cube with a small white shine mark, standing in a little flat puddle of light-blue water. There is exactly one ice cube and only one plate in the picture. {CALM}",
    "p08_ice_melts": f"Show the same toddler from the reference picture kneeling on the floor next to {PLATE}, pointing at it with an amazed face and an open mouth. On the plate is exactly one tiny rounded light-blue piece of ice, much smaller than before, melting in a big flat puddle of light-blue water that covers most of the plate. Exactly two small water drops drip from the edge of the plate. There is exactly one piece of ice and only one plate in the picture. {CALM}",
    "p09_see_water": f"Show the same toddler from the reference picture kneeling on the floor next to {PLATE}, looking at it with a calm interested face. On the plate is only a flat puddle of light-blue water, with no ice at all. There is no ice cube and only one plate in the picture. {CALM}",
    "p10_now_you": f"Show the same toddler from the reference picture kneeling on the floor next to {ICE}, smiling at the viewer and holding one open hand out toward the viewer in an inviting gesture. {ICE_END} {CALM}",
}
COVER = (
    f"Show the same toddler from the reference picture kneeling on the floor next to {PLATE}, smiling at "
    "the viewer. On the plate is exactly one half-melted light-blue ice cube with rounded corners and a "
    "small white shine mark, standing in a flat puddle of light-blue water. One big bright yellow sun "
    "without a face, with short triangular rays, shines in the upper right corner of the picture, fully "
    "inside the picture with empty space between the sun and the picture edges. There is exactly one ice "
    f"cube, only one plate and only one sun in the picture, and there are no clouds. {CALM}"
)
