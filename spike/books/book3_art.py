"""Book 3 art prompts: Heavy or Light? The page names match the `art` keys of book3.py."""

S = "the same toddler from the reference picture"
F = "one large white feather with a light-gray outline and a faint light-blue tint"
ST = "one big smooth plain gray stone, round like a basketball and as big as the toddler's head"
ST2 = (
    "one big smooth plain gray river stone, a slightly lumpy flattened oval that is wider than it is tall, "
    "with a flat bottom, about as big as the toddler's head. It is clearly a heavy rock, not a ball"
)
NO_EXTRA = "No other objects, no bubbles, no sparkles, no decoration."

PAGES = {
    "p01_see_feather": f"Show {S} standing and holding {F} up between two fingers, looking at the feather with curious wide eyes. There is only one feather in the picture. {NO_EXTRA}",
    "p02_feather_ask": f"Show {S} standing and holding {F} in one hand, the index finger of the other hand touching his chin, head tilted, thinking. There is only one feather in the picture. {NO_EXTRA}",
    "p03_feather_light": f"Show {S} standing with one open palm held out flat in front of him. Just above the palm, not touching it, {F} drifts in the air, with exactly two small curved motion lines beside the feather. The toddler smiles and watches the feather. There is only one feather in the picture. {NO_EXTRA}",
    "p04_see_stone": f"Show {S} crouching on the ground next to {ST2}, which rests flat on the ground beside him. The toddler looks at the stone with curious wide eyes. There is only one stone in the picture. {NO_EXTRA}",
    "p05_stone_ask": f"Show {S} standing next to {ST2}, which rests flat on the ground and reaches up to his knees. The toddler bends forward and rests both hands on top of the stone, head tilted, curious. There is only one stone in the picture. {NO_EXTRA}",
    "p06_stone_heavy": f"Show {S} standing behind {ST2}, which rests flat on the ground in front of his feet. He bends his knees and grips the sides of the stone with both hands, pulling up hard. His cheeks are puffed and his eyes are squeezed shut. The bottom of the stone still touches the ground: the stone does not rise at all. There is only one stone in the picture. {NO_EXTRA}",
    "p07_balloon_light": f"Show {S} standing and holding the bottom end of a thin string in one raised hand. The string goes up to one round red balloon floating above his head. The top of the balloon is well below the top edge of the picture, with clear empty space above it. The toddler smiles and looks up at the balloon. There is only one balloon in the picture. {NO_EXTRA}",
    "p08_watermelon_heavy": f"Show {S} hugging one big round green watermelon with dark green stripes, which rests on the ground and is as big as the toddler's body. He strains to push it, cheeks puffed. There is only one watermelon in the picture and it is whole, not cut. {NO_EXTRA}",
    "p09_feathers_stones": f"Show {S} standing in the middle, smiling. On the left side, exactly three white feathers with light-gray outlines and a faint light-blue tint drift in the air at the height of his head. On the right side, exactly three big smooth plain gray stones, each round like a basketball, lie together in a low heap on the ground, two stones side by side on the ground and one stone resting on top of them. His left arm is raised with the index finger pointing up at the feathers. His right arm is stretched down with the index finger clearly pointing down at the stones. There are exactly three feathers and exactly three stones in the picture. {NO_EXTRA}",
    "p10_now_you": f"Show {S} standing and holding one open hand out toward the viewer in an inviting gesture. On the ground beside him lie {F} and one smooth plain gray stone the size of a melon. There is only one feather and only one stone in the picture. {NO_EXTRA}",
}
COVER = (
    f"Show {S} standing and smiling, holding {F} up in one hand. "
    f"Next to him, {ST} rests on the ground. There is only one feather and only one stone in the picture. {NO_EXTRA}"
)
