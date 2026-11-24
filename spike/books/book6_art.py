"""Book 6 art prompts: Where Is the Ball? The page names match the `art` keys of book6.py."""

BOX = "one open brown cardboard box with its four flaps folded open, seen slightly from above"
TABLE = "one small plain wooden table with four straight legs and a bare flat top"
CHAIR = "one small plain wooden chair with four straight legs and a straight back"
BALL = "one plain bright red rubber ball with no pattern"
SET = (
    f"On the floor to the left of the toddler stands {BOX}, and the box is empty. To the right of the "
    f"toddler stand {TABLE} and, next to the table, {CHAIR}. The table top is empty and the chair seat is empty."
)
NO_BALL = (
    "There is no ball anywhere in the picture, and there are no question marks. There is only one box, "
    "one table and one chair in the picture."
)
ONE_EACH = "There is only one ball, one box, one table and one chair in the picture."
MARGIN = (
    "The whole group fits well inside the picture, with a wide empty margin on every side, and nothing "
    "touches or crosses the edge of the picture."
)
COMPACT = (
    "Draw the whole group small and close together in the middle of the picture, so that it fills only "
    "the middle 70 percent of the picture width. A wide strip of plain empty background stays on the left "
    "side and on the right side, and nothing touches or crosses the edge of the picture."
)

PAGES = {
    "p01_where_1": f"Show the same toddler from the reference picture standing in the middle of the picture with both palms turned up and both shoulders raised, looking around with a puzzled face. {SET} {NO_BALL} {MARGIN}",
    "p02_ball_in_box": f"Show the same toddler from the reference picture standing outside the box, next to it, smiling and pointing at {BOX}. Inside the box sits {BALL}: only the top half of the ball shows above the rim of the box. To the right of the toddler stand {TABLE} and, next to the table, {CHAIR}. {ONE_EACH} {MARGIN}",
    "p03_where_2": f"Show the same toddler from the reference picture standing in the middle of the picture, holding one hand flat above the eyes to shade them and looking to the side with a searching face. {SET} {NO_BALL} {MARGIN}",
    "p04_ball_on_table": f"Show the same toddler from the reference picture standing next to {TABLE}, smiling and pointing at {BALL} that sits on top of the table, in the middle of the bare table top. Next to the table stands {CHAIR}, and on the floor behind the toddler stands {BOX}, and the box is empty. {ONE_EACH} {MARGIN}",
    "p05_where_3": f"Show the same toddler from the reference picture standing in the middle of the picture, bending forward with both hands on the knees and looking down at the floor with a puzzled face. {SET} {NO_BALL} {MARGIN}",
    "p06_ball_under_chair": f"Show the same toddler from the reference picture crouching on the floor next to {CHAIR}, smiling and pointing at {BALL} that lies on the floor under the chair, between the four chair legs, clearly below the seat. The chair seat is empty. Further back, {TABLE} stands on the floor, and next to the table {BOX} stands on the floor, and the box is empty. {ONE_EACH} {MARGIN}",
    "p07_put_in": f"Show the same toddler from the reference picture standing outside the box, next to it, holding {BALL} in both hands just above the open top of {BOX} and lowering the ball into the box. The box is empty. Behind them stand {TABLE} and {CHAIR}. {ONE_EACH} {MARGIN}",
    "p08_put_on": f"Show the same toddler from the reference picture standing on tiptoes next to {TABLE}, reaching up and setting {BALL} down onto the middle of the table top with one hand. Next to the table stands {CHAIR}, and on the floor behind the toddler stands {BOX}, and the box is empty. {ONE_EACH} {MARGIN}",
    "p09_put_under": f"Show the same toddler from the reference picture kneeling on the floor in front of {CHAIR}, pushing {BALL} with one hand so it rolls along the floor under the chair, between the four chair legs, below the seat. The chair seat is empty. Further back, {TABLE} stands on the floor, and next to the table {BOX} stands on the floor, and the box is empty. {ONE_EACH} {MARGIN}",
    "p10_now_you": f"Show the same toddler from the reference picture standing in front, holding one open hand out toward the viewer in an inviting gesture and holding {BALL} in the other hand. Behind the toddler, in one row from left to right, stand {BOX}, {TABLE} and {CHAIR}. The box is empty, the table top is empty and the chair seat is empty. {ONE_EACH} {MARGIN}",
}
COVER = (
    f"Show the same toddler from the reference picture standing in the middle of the picture and smiling, "
    f"holding {BALL} up high in one hand. On the floor to the left of the toddler stands {BOX}, and the "
    f"box is empty. To the right of the toddler stand {TABLE} and, next to the table, {CHAIR}. The table "
    f"top is empty and the chair seat is empty. {ONE_EACH} {COMPACT}"
)
