"""Book 9 art prompts: Weather. The page names match the `art` keys of book9.py."""

SUN = (
    "one big bright yellow sun without a face, a plain round yellow disc with a dark-navy outline and short "
    "triangular yellow rays"
)
SUN_IN = (
    "The sun and the tips of all its rays are well inside the picture, with a wide empty margin between them "
    "and the edges of the picture."
)
CLOUD = "one big white fluffy cloud with a dark-navy outline"
UMBRELLA = "one open bright red umbrella with a curved handle"
RAIN_CLOUD = "one gray-blue cloud with a dark-navy outline"
DROPS = "short straight blue raindrop lines"
CALM = "There are no bubbles, no sparkles, no stars, no birds and no extra decoration."
FLAKES = (
    "small light-blue six-pointed snowflakes. Every falling flake is a six-pointed snowflake shape, and there "
    "are no round dots, no balls and no bubbles in the air"
)
WINTER = (
    "Keep the same toddler face, the same light-blond hair showing under the front of the hat, the same "
    "blue-gray eyes and rosy cheeks and the same flat vector style from the reference picture, but dress the "
    "toddler in a warm red winter coat, a blue knitted hat, blue mittens, blue trousers and blue boots "
    "instead of the yellow t-shirt and blue shorts, with the same line weight."
)

PAGES = {
    "p01_look_sky": "Show the same toddler from the reference picture standing on plain flat ground, head tilted back, looking up at the sky with one hand held flat above the eyes to shade them. The background is a plain pale sky-blue. One small white cloud with a dark-navy outline floats high up in the upper part of the picture. There is only one cloud in the picture and there is no sun. " + CALM,
    "p02_sun_shines": f"Show the same toddler from the reference picture standing on plain flat ground, facing the viewer with a big happy smile. {SUN} shines in the upper right part of the picture. {SUN_IN} There is only one sun in the picture and there are no clouds. {CALM}",
    "p03_sun_warm": f"Show the same toddler from the reference picture standing on plain flat ground with both eyes closed and the face tilted up toward the sun, with a happy relaxed smile and both arms relaxed at the sides. {SUN} shines in the upper right part of the picture, with a few soft wavy orange glow lines around it. {SUN_IN} There is only one sun in the picture and there are no clouds. {CALM}",
    "p04_see_cloud": f"Show the same toddler from the reference picture standing on plain flat ground and pointing up with one arm at {CLOUD} high in a plain pale-blue sky. The toddler looks up at the cloud with curious wide eyes. There is only one cloud in the picture, there is no sun and there is no rain. {CALM}",
    "p05_rain_falls": f"Show the same toddler from the reference picture standing on plain flat ground, holding {UMBRELLA} over the head with both hands, smiling. High above the umbrella there is {RAIN_CLOUD}. {DROPS} fall from the cloud on both sides of the umbrella and bounce off the top of the umbrella. The toddler stays dry under the umbrella. There is only one umbrella and only one cloud in the picture, and there is no sun. {CALM}",
    "p06_grass_wet": "Show the same toddler from the reference picture crouching low on a small patch of green grass, touching the grass blades with one hand and looking at them with curious wide eyes. Small shiny blue water drops sit on the tips of the grass blades. One small flat blue puddle lies on the ground beside the toddler, outside the toddler's feet. There is only one puddle in the picture, there is no rain falling and there is no cloud and no sun. " + CALM,
    "p07_wind_blows": "Show the same toddler from the reference picture standing on plain flat ground, leaning a little into the wind with a happy surprised face. The wind blows from the left to the right: the toddler's light-blond hair and the yellow t-shirt blow sideways to the right. Exactly three green leaves and exactly four white curved wind lines with dark-navy outlines fly across the picture from left to right, all in the same direction. There are exactly three leaves in the picture. There is no tree, no sun, no cloud and no rain. " + CALM,
    "p08_snow_falls": f"Show the same toddler from the reference picture standing on plain flat white-blue snowy ground, holding one mittened hand up in front of the face with the palm up. One snowflake lies on the mitten and the toddler looks at it with a happy amazed face. Around the toddler fall {FLAKES}. There is no snowman, no tree and no sun.",
    "p09_snow_cold": "Show the same toddler from the reference picture standing on plain flat white-blue snowy ground, holding exactly one round white snowball in both mittens in front of the chest. The toddler shivers with raised shoulders and a happy face, and short light-blue shiver lines are drawn on both sides of the body. There is only one snowball in the picture. There is no snowman, no tree, no sun and no falling snow, and there are no round dots, no balls and no bubbles in the air.",
    "p10_look_sky": f"Show the same toddler from the reference picture standing on plain flat ground, smiling at the viewer and pointing up with one arm. In the upper left part of the picture there is {SUN}. In the upper right part of the picture there is one white cloud with a dark-navy outline, and a few short blue raindrop lines fall from the cloud. {SUN_IN} There is only one sun and only one cloud in the picture. There is no snow and there are no snowflakes. {CALM}",
}
COVER = (
    f"Show the same toddler from the reference picture standing on plain flat ground in the lower middle of the "
    f"picture, smiling at the viewer and holding {UMBRELLA} over the head with one hand. Above the toddler, in "
    f"one row from left to right, there are three things with clear empty space between them: on the left "
    f"{SUN}, in the middle one white cloud with a dark-navy outline with a few short blue raindrop lines falling "
    f"from it, and on the right exactly three small light-blue six-pointed snowflakes. {SUN_IN} There is only "
    f"one sun, one cloud and one umbrella in the picture. {CALM}"
)
KEEP_FOR = {"p08_snow_falls": WINTER, "p09_snow_cold": WINTER}
