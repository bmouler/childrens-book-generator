"""Book 4 art prompts: Big or Small? The page names match the `art` keys of book4.py."""

ELEPHANT = (
    "one huge gray adult elephant, not a baby elephant, with realistic elephant proportions, standing on "
    "four thick legs and seen from the side in profile so that only one of its eyes is visible, with large "
    "flat ears, a long trunk that hangs down, no tusks and a friendly simple face"
)
ELEPHANT_SCALE = (
    "Draw the sizes true to life, like a real small child next to a real adult elephant. The toddler is "
    "drawn much smaller than in the reference picture: the whole toddler is shorter than one elephant leg, "
    "and the top of the toddler's head reaches only up to the elephant's knee. The elephant's belly is high "
    "above the toddler's head."
)
MOUSE = "one tiny gray mouse with round pink ears, a pink nose, small black eyes and a thin pink tail"
MOUSE_SCALE = "The mouse is much smaller than the toddler's hand: it is only about as long as the toddler's thumb."
MOUSE_PALM = (
    "The mouse covers only the middle of the palm, and the toddler's fingers reach well beyond the mouse."
)
MOUSE_GROUND = "The mouse is drawn very small, true to life: its body is shorter than the toddler's foot."
ONLY = "There is only one elephant and only one mouse in the picture, and no other animal."

PAGES = {
    "p01_see_elephant": f"Show the same toddler from the reference picture standing on plain flat ground beside {ELEPHANT}. {ELEPHANT_SCALE} The toddler stands outside the elephant, next to its front legs, and looks up at the elephant's face with curious wide eyes. The whole elephant fits inside the picture with empty space above its back. There is only one elephant in the picture, and no other animal.",
    "p02_elephant_ask": f"Show the same toddler from the reference picture standing on plain flat ground beside {ELEPHANT}. {ELEPHANT_SCALE} The toddler looks up at the elephant with the head tilted in a curious thinking pose and one finger at the chin. The whole elephant fits inside the picture with empty space above its back. There is only one elephant in the picture, and no other animal.",
    "p03_elephant_big": f"Show {ELEPHANT}, filling most of the picture and towering over the same toddler from the reference picture. {ELEPHANT_SCALE} The toddler stands on plain flat ground next to the elephant's front feet, at the same distance from the viewer as the elephant, facing the viewer, smiling, with both arms stretched wide out to the sides. The whole elephant fits inside the picture with a thin margin of empty space around it. There is only one elephant in the picture, and no other animal.",
    "p04_see_mouse": f"Show the same toddler from the reference picture kneeling on a plain floor and looking down with curious wide eyes at {MOUSE} that sits on the floor in front of the toddler's knees. {MOUSE_SCALE} The toddler's hands rest on the knees. There is only one mouse in the picture, and no other animal.",
    "p05_mouse_ask": f"Show the same toddler from the reference picture sitting on a plain floor and holding one open hand, palm up, in front of the chest. {MOUSE} sits on the open palm. {MOUSE_SCALE} {MOUSE_PALM} The toddler looks at the mouse with the head tilted and a curious face. There is only one mouse in the picture, and no other animal.",
    "p06_mouse_small": f"Show the same toddler from the reference picture sitting on a plain floor and smiling. One hand is held open, palm up, and {MOUSE} sits on that palm. {MOUSE_SCALE} {MOUSE_PALM} The other hand is raised beside the face in a pinch gesture: the thumb and the index finger point toward each other and almost touch, with a tiny gap between their tips, and the other fingers are curled. No finger points up. There is only one mouse in the picture, and no other animal.",
    "p07_tree_big": "Show one very tall tree with a thick brown trunk and a big round green crown, filling the picture from the ground nearly to the top. The same toddler from the reference picture stands on plain flat ground at the base of the trunk, looking up. The toddler is tiny next to the tree: the top of the toddler's head reaches only a short way up the trunk. The whole tree fits inside the picture with a thin margin of empty space around it. There is only one tree in the picture.",
    "p08_flower_small": "Show the same toddler from the reference picture crouching on plain flat ground beside one small red flower with five round petals on a thin green stem with two small leaves. The flower grows from the ground and is only as tall as the toddler's ankle, and the red flower head is smaller than the toddler's hand. The toddler looks at the flower with a gentle smile and does not pick it. There is only one flower in the picture and no grass.",
    "p09_elephant_mouse": f"Show three things side by side on plain flat ground. On the left stands {ELEPHANT}, its head and trunk turned to the right, filling the left two thirds of the picture from near the bottom to near the top. Right of the elephant stands the same toddler from the reference picture, outside the elephant and next to its trunk, smiling at the viewer, with one arm stretched toward the elephant and the other arm pointing down toward the mouse. On the right, on the ground near the toddler's feet, sits {MOUSE}. {ELEPHANT_SCALE} {MOUSE_GROUND} {ONLY}",
    "p10_now_you": "Show the same toddler from the reference picture standing on plain flat ground, smiling and holding one open hand out toward the viewer in an inviting gesture. On the ground next to the toddler lie exactly two plain red balls with no pattern: one big red ball as tall as the toddler's knee and one small red ball the size of an orange. The big ball is at least three times as wide as the small ball. There are exactly two balls in the picture.",
}
COVER = (
    f"Show three things side by side on plain flat ground. On the left stands {ELEPHANT}, its head and trunk "
    f"turned to the right, filling the left two thirds of the picture from near the bottom to near the top. "
    f"Right of the elephant stands the same toddler from the reference picture, outside the elephant and "
    f"next to its trunk, smiling at the viewer with both hands at the sides. On the right, on the ground "
    f"near the toddler's feet, sits {MOUSE}. {ELEPHANT_SCALE} {MOUSE_GROUND} {ONLY}"
)
