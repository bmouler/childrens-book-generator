"""Book 7 art prompts: Red, Yellow, Green, Blue! The page names match the `art` keys of book7.py."""

PLAIN = "plain smooth solid-colour {c} ball with no stripes, no pattern, no shine spots and no second colour"
NO_EXTRA = "Do not draw any bubbles, sparkles, stars or other decoration."
FOUR = (
    "exactly four balls of the same size: one pure bright red ball, one pure bright yellow ball, "
    "one pure bright green ball and one pure bright blue ball. Each ball is a single plain solid colour "
    "with a thick dark-navy outline and no pattern. There are exactly four balls in the picture and no other toys"
)


def _ball(c: str) -> str:
    return (
        f"Show the same toddler from the reference picture standing and smiling at the viewer, holding one big "
        f"{PLAIN.format(c=c)} in front of the chest with both hands. The ball is pure bright {c} and clearly "
        f"bigger than the toddler's head. There is only one ball in the picture. {NO_EXTRA}"
    )


PAGES = {
    "p01_red_ball": _ball("red"),
    "p02_blue_ball": _ball("blue").replace("pure bright blue and", "pure bright primary blue, not teal and not purple, and"),
    "p03_yellow_ball": f"Show the same toddler from the reference picture standing and smiling at the viewer, holding one big {PLAIN.format(c='yellow')} high above the head with both arms raised, so the ball sits against the plain pale background and not in front of the yellow t-shirt. The ball is pure bright lemon yellow with a thick dark-navy outline and is clearly bigger than the toddler's head. The whole ball stays inside the picture with a wide margin above it. There is only one ball in the picture. {NO_EXTRA}",
    "p04_green_ball": _ball("green"),
    "p05_apple_red": f"Show the same toddler from the reference picture standing and smiling at the viewer, holding one round pure bright red apple up in one hand. The apple has one short brown stem and exactly one small green leaf on top. The apple is red all over with no yellow or green patches. There is only one apple in the picture. {NO_EXTRA}",
    "p06_sun_yellow": f"Show the same toddler from the reference picture standing outdoors on a plain strip of pale ground, smiling and looking at the viewer, not at the sun. One big pure bright yellow round sun with a thick dark-navy outline and short triangular yellow rays shines in the upper right part of the picture. The sun and all its rays stay well inside the picture, with a wide empty margin between the rays and the top and right edges. There is only one sun in the picture. No clouds. {NO_EXTRA}",
    "p07_leaf_green": f"Show the same toddler from the reference picture standing and smiling at the viewer, holding up one big pure bright green leaf by its short stem in one raised hand. The leaf is about as big as the toddler's head, a simple oval leaf shape with one darker green centre line. There is only one leaf in the picture. {NO_EXTRA}",
    "p08_sea_blue": f"Show the same toddler from the reference picture standing barefoot on a strip of pale sand in the lower part of the picture, smiling at the viewer. Behind the toddler a wide pure bright blue sea fills the upper half of the picture, with a few simple white wave lines. The sea is bright primary blue, not teal and not green. Above the sea is a plain pale sky. No boats, no birds, no shells. {NO_EXTRA}",
    "p09_four_balls": f"Show the same toddler from the reference picture standing and cheering with both arms raised high and a big smile. On the ground a short distance in front of the toddler, not touching the feet, with the whole feet visible, sit {FOUR}, in one straight row from left to right in this order: red, yellow, green, blue. {NO_EXTRA}",
    "p10_now_you": f"Show the same toddler from the reference picture standing just left of the centre of the picture, smiling and holding one open hand out toward the viewer in an inviting gesture. On the ground to the right of the toddler, close to the feet, sit {FOUR}, small, each about as big as the toddler's head, in a short row from left to right: red, yellow, green, blue. The toddler and the balls together are centred in the picture, with a wide empty margin between the blue ball and the right edge. {NO_EXTRA}",
}
COVER = (
    f"Show the same toddler from the reference picture standing and smiling at the viewer in the middle of the "
    f"picture. Above the toddler's head, {FOUR}, float in a gentle arc from left to right in this order: red, "
    f"yellow, green, blue. The arc of balls starts well below the top edge of the picture, with a wide empty margin above it, and the toddler is a little smaller to leave room. {NO_EXTRA}"
)
