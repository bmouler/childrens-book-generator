"""Book 5 art prompts: Soft or Hard? The page names match the `art` keys of book5.py."""

PILLOW = (
    "one big plain white fluffy pillow, a puffy rounded square with soft rounded corners and bulging "
    "sides, with no pattern, no buttons and no stitching"
)
CUBE = (
    "one plain light-wood toy cube with sharp straight edges, flat sides and crisp corners, its faces "
    "completely blank with no letters, no numbers, no pictures and no marks"
)
TEDDY = "one plain brown teddy bear with a lighter tan muzzle, small round black eyes and no clothes"
TABLE = (
    "one small plain light-wood table with a flat rectangular top, sharp straight edges and four "
    "straight legs"
)
BLANK = "No letters, numbers, pictures or marks appear on any block."

PAGES = {
    "p01_see_pillow": f"Show the same toddler from the reference picture sitting on the floor next to {PILLOW}, which lies on the floor at the toddler's side. The toddler looks at the pillow with curious wide eyes and a small gentle smile, hands resting in the lap. There is only one pillow in the picture.",
    "p02_pillow_ask": f"Show the same toddler from the reference picture sitting cross-legged on the floor with {PILLOW} lying on the floor in front of the toddler, with one finger raised to the chin and the head tilted in a curious thinking pose. There is only one pillow in the picture.",
    "p03_pillow_soft": f"Show the same toddler from the reference picture kneeling on the floor behind {PILLOW}, seen from the front. The toddler presses only the right hand, open and flat, down into the middle of the pillow top, and the left hand rests on the left knee. The hand sinks deep into the pillow: the top outline of the pillow dips down in a deep curved hollow under the hand, with a few curved fold lines around the hollow, and the pillow bulges up high on both sides of the hand. The toddler smiles with a happy face. There is only one pillow in the picture, and there are no sparkles, stars or motion lines.",
    "p04_see_block": f"Show the same toddler from the reference picture sitting on the floor next to {CUBE}, which stands on the floor at the toddler's side. The cube is about as big as the toddler's head. The toddler looks at the cube with curious wide eyes and a small gentle smile, hands resting in the lap. There is only one cube in the picture. {BLANK}",
    "p05_block_ask": f"Show the same toddler from the reference picture sitting on the floor and holding {CUBE} in both hands in front of the chest. The cube is about as big as the toddler's head. The toddler tilts the head with a curious thinking expression. There is only one cube in the picture. {BLANK}",
    "p06_block_hard": f"Show the same toddler from the reference picture kneeling on the floor in front of {CUBE}, which stands on the floor. The cube is about as big as the toddler's head. The toddler taps the top of the cube with the knuckles of one small fist and smiles. Exactly three short straight dark-navy impact lines fan out from the spot where the knuckles touch the cube. The cube keeps its sharp edges and does not bend. There is only one cube in the picture. {BLANK}",
    "p07_teddy_soft": f"Show the same toddler from the reference picture sitting on the floor and hugging {TEDDY} tightly against the chest with both arms. The toddler's eyes are closed in happy curved lines and the toddler smiles. There is only one teddy bear in the picture, and there are no hearts, sparkles or stars.",
    "p08_table_hard": f"Show the same toddler from the reference picture standing beside {TABLE}. The table top is at the height of the toddler's chest. The toddler taps the flat table top with the knuckles of one small fist and smiles. Exactly three short straight dark-navy impact lines fan out from the spot where the knuckles touch the table. Nothing stands on the table. There is only one table in the picture.",
    "p09_pillows_blocks": "Show the same toddler from the reference picture standing in the middle of the picture and smiling at the viewer, with one arm reaching out toward each side. On the floor on the left side stands a stack of exactly two plain white fluffy pillows, puffy rounded squares with soft rounded corners and no pattern, one pillow lying on top of the other. On the floor on the right side stands a stack of exactly three plain light-wood toy cubes with sharp straight edges and flat sides, all the same size, one cube on top of another in a single tower. Both stacks stand close to the toddler and well inside the picture, with a wide empty margin between each stack and the edge of the picture. The toddler does not touch the stacks. There are exactly two pillows and exactly three cubes in the picture. " + BLANK,
    "p10_touch_teddy": f"Show the same toddler from the reference picture sitting on the floor and holding one open hand out toward the viewer in an inviting gesture, smiling. {TEDDY[0].upper()}{TEDDY[1:]} sits upright on the floor in front of the toddler, a little to one side, so the toddler stays fully visible. There is only one teddy bear in the picture.",
}
COVER = (
    f"Show the same toddler from the reference picture standing and smiling at the viewer, hugging {TEDDY} "
    f"against the side with one arm. On the floor beside the toddler's feet stands {CUBE}. There is only "
    f"one teddy bear and only one cube in the picture. {BLANK}"
)
