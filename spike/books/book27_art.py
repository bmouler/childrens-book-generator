"""Book 27 art: On Purpose! The toddler does one action per page, fast or slow shown by
motion lines: many short lines for fast, one long line for slow."""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"
FLOOR = "on a plain soft-green floor"

PAGES = {
    "p01_clap": f"{T} standing {FLOOR}, hands coming together in a clap, mouth open in a song. "
                f"{MARGIN} {NO_EXTRA}",
    "p02_fast": f"{T} standing {FLOOR}, clapping with many short motion lines between the hands, "
                f"energetic face. {MARGIN} {NO_EXTRA}",
    "p03_slow": f"{T} standing {FLOOR}, hands far apart mid-slow-clap with one long curving "
                f"motion line, calm face. {MARGIN} {NO_EXTRA}",
    "p04_stomp": f"{T} standing {FLOOR}, one foot raised ready to stomp, arms out for balance. "
                 f"{MARGIN} {NO_EXTRA}",
    "p05_stomp_fast": f"{T} standing {FLOOR}, one foot coming down with many short motion lines "
                      f"under it, dust puff. {MARGIN} {NO_EXTRA}",
    "p06_sing": f"{T} standing {FLOOR}, both hands on the chest, mouth open wide in song, eyes "
                f"closed happily. {MARGIN} {NO_EXTRA}",
    "p07_quiet": f"{T} standing {FLOOR}, one finger held to the lips, singing a tiny quiet note "
                 f"shown as one small music squiggle. {MARGIN} {NO_EXTRA}",
    "p08_loud": f"{T} standing {FLOOR}, arms wide, mouth open very wide, big bold music notes "
                f"bursting out. {MARGIN} {NO_EXTRA}",
    "p09_jump": f"{T} standing {FLOOR}, knees bent ready to jump, arms swung back. {MARGIN} "
                f"{NO_EXTRA}",
    "p10_up": f"{T} mid-air high above {FLOOR}, arms up, hair up, small motion lines under the "
              f"feet. {MARGIN} {NO_EXTRA}",
    "p11_down": f"{T} landing {FLOOR} in a small crouch, arms forward for balance, one motion "
                f"line above the head. {MARGIN} {NO_EXTRA}",
    "p12_count": f"{T} standing {FLOOR}, holding up one open hand with fingers spread, pointing "
                 f"at the fingers with the other hand. {MARGIN} {NO_EXTRA}",
    "p13_count_two": f"{T} standing {FLOOR}, counting on the fingers of one open hand, one side "
                     f"of the face quick and the other calm, two small arrows circling the "
                     f"hands. {MARGIN} {NO_EXTRA}",
    "p14_clap_again": f"{T} standing {FLOOR}, clapping above the head with a big grin. "
                      f"{MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} standing {FLOOR}, one hand mid-clap and the other on the hip, cheeky purposeful "
         f"smile. {MARGIN} {NO_EXTRA}")
