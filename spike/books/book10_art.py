"""Book 10 art prompts: A Seed Grows. The page names match the `art` keys of book10.py."""

POT = (
    "one round terracotta flower pot with a wide rim, filled to the top with dark-brown soil, "
    "standing on the plain ground"
)
CAN = "one small blue watering can"
SEED = "one big brown seed shaped like a pointed oval with light stripes, like a sunflower seed"
ONE_POT = "There is only one flower pot in the picture."
NO_PLANT = "The soil is bare: there is no plant, no sprout and no leaf in the pot."
CALM = "There are no bubbles, no sparkles, no insects and no extra decoration."

PAGES = {
    "p01_see_seed": f"Show the same toddler from the reference picture standing and holding out one open hand, palm up, with {SEED} lying on the palm. The toddler looks down at the seed with curious wide eyes. The seed is big enough to see clearly. There is only one seed in the picture, and there is no pot and no plant. {CALM}",
    "p02_seed_soil": f"Show the same toddler from the reference picture kneeling on the ground outside the pot, next to {POT}. The toddler presses {SEED} into the soil with one finger, half of the seed still visible above the soil. {NO_PLANT} {ONE_POT} There is only one seed in the picture. {CALM}",
    "p03_water_seed": f"Show the same toddler from the reference picture standing outside the pot, next to {POT}. The toddler holds {CAN} tilted over the pot, and exactly five small blue water drops fall from the spout onto the soil. {NO_PLANT} {ONE_POT} There is only one watering can in the picture. {CALM}",
    "p04_sun_warm": f"Show {POT} in the sunshine, with the same toddler from the reference picture sitting on the ground outside the pot, next to it, smiling. One big yellow sun without a face, with short triangular rays, shines above them in the upper part of the picture, fully inside the picture with empty space around it. {NO_PLANT} {ONE_POT} There is only one sun in the picture and there are no clouds. {CALM}",
    "p05_wait": f"Show the same toddler from the reference picture sitting cross-legged on the ground outside the pot, next to {POT}, with the chin resting on one hand, looking at the soil with a calm, patient face. {NO_PLANT} {ONE_POT} There is no clock. {CALM}",
    "p06_seed_grows": f"Show the same toddler from the reference picture kneeling on the ground outside the pot, next to {POT}. Out of the soil comes one tiny green sprout with exactly two small round leaves. The toddler points at the sprout with one finger and has a delighted open-mouthed smile. The sprout has exactly two leaves and no flower. {ONE_POT} {CALM}",
    "p07_water_plant": f"Show the same toddler from the reference picture standing outside the pot, next to {POT}. In the pot grows one small green plant with exactly four leaves and no flower. The toddler holds {CAN} tilted over the soil. Exactly five separate small blue water drops form one vertical line from the spout to the soil. Count the drops from top to bottom: first, second, third, fourth and fifth. Every drop is fully visible, with empty space between adjacent drops. {ONE_POT} There is only one watering can and one plant in the picture. {CALM}",
    "p08_plant_grows": f"Show the same toddler from the reference picture standing outside the pot, next to {POT}. In the pot grows one taller green plant, about as tall as the toddler's chest, with exactly six leaves arranged as three clearly separated pairs: one low pair, one middle pair and one high pair. One closed green flower bud grows at the top. Do not draw four leaves. The toddler stretches both arms up high with an amazed face. The bud is closed and there is no open flower. {ONE_POT} There is only one plant in the picture. {CALM}",
    "p09_see_flower": f"Show the same toddler from the reference picture standing outside the pot, next to {POT}. In the pot grows one tall green plant with exactly six leaves arranged as three clearly separated pairs: one low pair, one middle pair and one high pair. Exactly one big red flower is in full bloom at the top. Do not draw four leaves. The toddler smiles at the flower with both hands clasped together under the chin. {ONE_POT} There is only one flower and one plant in the picture. {CALM}",
    "p10_now_you": f"Show the same toddler from the reference picture standing behind {POT}, which stands on the ground in front of the toddler. The toddler smiles at the viewer, holds one open hand out toward the viewer in an inviting gesture, and holds {SEED} between the fingers of the other hand. {NO_PLANT} {ONE_POT} There is only one seed in the picture. {CALM}",
}
COVER = (
    f"Show the same toddler from the reference picture standing and smiling at the viewer, next to {POT}. "
    "In the pot grows one tall green plant with exactly three horizontal pairs of leaves. The lower pair has "
    "one leaf on the left and one on the right. The middle pair has one leaf on the left and one on the right. "
    "The upper pair has one leaf on the left and one on the right. These are exactly six visible leaves in total. "
    "Exactly one big red flower is in full bloom at the top. "
    f"On the ground on the other side of the toddler stands {CAN}. {ONE_POT} "
    f"There is only one flower and only one watering can in the picture. {CALM}"
)
