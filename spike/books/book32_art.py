"""Book 32 art: A Seed Grows All Year. The same little plant in the same spot, page by
page: snow, sprout, bud, bloom, seeds, snow again. Seasons change around it."""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
SPOT = "one small mound of brown soil on plain flat ground"

PAGES = {
    "p01_winter": f"{SPOT} under a smooth layer of white snow, small snowflakes falling, bare "
                  f"plain field around. {MARGIN} {NO_EXTRA}",
    "p02_sleep": f"A close view of {SPOT} in winter: under the thin snow one tiny brown seed "
                 f"visible half-buried in the soil, asleep. {MARGIN} {NO_EXTRA}",
    "p03_spring": f"{SPOT} with the snow gone, first green grass tips around it, soft spring "
                  f"light. {MARGIN} {NO_EXTRA}",
    "p04_wake": f"A close view of {SPOT} in spring: one small green sprout with two leaves "
                f"pushing up through the soil. {MARGIN} {NO_EXTRA}",
    "p05_water": f"{T} kneeling beside {SPOT}, pouring water from one small blue watering can "
                 f"onto the young sprout. {MARGIN} {NO_EXTRA}",
    "p06_grow": f"The young sprout on {SPOT} now has a straight stem and four leaves, growing "
                f"tall. {MARGIN} {NO_EXTRA}",
    "p07_sun": f"One big bright friendly sun with short rays shining down on {SPOT} and the "
               f"growing plant. {MARGIN} {NO_EXTRA}",
    "p08_rain": f"Soft straight rain falling on {SPOT} and the growing plant, small round "
                f"raindrops. {MARGIN} {NO_EXTRA}",
    "p09_summer": f"The plant on {SPOT} is now tall and green with one closed bud on top, full "
                  f"summer light. {MARGIN} {NO_EXTRA}",
    "p10_plant_big": f"The plant on {SPOT} stands tall with big leaves and one open red flower "
                     f"on top. {MARGIN} {NO_EXTRA}",
    "p11_grow_grow": f"{T} standing beside the tall flowering plant on {SPOT}, hand held flat "
                     f"above the head measuring how tall it is. {MARGIN} {NO_EXTRA}",
    "p12_autumn": f"The plant on {SPOT} with warm autumn light, leaves turning yellow, the "
                  f"flower now faded with a seed head. {MARGIN} {NO_EXTRA}",
    "p13_seeds": f"A close view of the dry seed head on {SPOT}: several small brown seeds "
                 f"clustering where the flower was. {MARGIN} {NO_EXTRA}",
    "p14_wind": f"The wind blowing hard: the dry plant on {SPOT} bent sideways, several small "
                f"seeds flying off in a curve, two curved wind lines. {MARGIN} {NO_EXTRA}",
    "p15_soil": f"Several small brown seeds lying on the brown soil of {SPOT}, half covered, "
                f"quiet end-of-year light. {MARGIN} {NO_EXTRA}",
    "p16_again": f"{SPOT} under a smooth fresh layer of white snow again, small snowflakes "
                 f"falling, the circle closed. {MARGIN} {NO_EXTRA}",
}
COVER = (f"A tall green flowering plant grows from {SPOT}, one small brown seed lying on the "
         f"soil in front, soft sun above. {MARGIN} {NO_EXTRA}")
