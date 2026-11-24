"""Book 12: "The Turnip" (Репка). The canonical tale, in modern Russian.

Grandpa plants a turnip; it grows big, very big (большая-пребольшая). He pulls and cannot pull it
out. He calls Grandma, Grandma calls the granddaughter, she calls the dog, the dog calls the cat,
the cat calls the mouse. Every helper gets a call page, a grasp-chain page (Бабушка за дедушку, ...)
and the refrain page (Тянут-потянут, вытянуть не могут). The two longest chains break across two
pages at the middle link, so the text stays at the 76 px floor. At the mouse the chain wins:
вытянули репку! Then all eat. Chain and refrain pages are recitation pages: no word cards.
Modernized words: дед/бабка -> дедушка/бабушка, Жучка -> собака, мышка -> мышь, репа -> репка.
"""
TURNIP = {"n": "turnip", "art": "the"}
SOIL = {"n": "soil", "art": "the"}


def the(noun: str) -> dict:
    return {"n": noun, "art": "the"}


GIRL, DOG, CAT, MOUSE = the("granddaughter"), the("dog"), the("cat"), the("mouse")

# The chain of graspers, from the newest helper back to the turnip. The two longest chains break
# into two pages at the middle link; the middle noun repeats, so each page reads as a full breath.
PLANS = [  # (newcomer, caller, chain pages)
    ("grandma", "grandpa", [["grandma", "grandpa", TURNIP]]),
    ("granddaughter", "grandma", [[GIRL, "grandma", "grandpa", TURNIP]]),
    ("dog", "granddaughter", [[DOG, GIRL, "grandma", "grandpa", TURNIP]]),
    ("cat", "dog", [[CAT, DOG, GIRL], [GIRL, "grandma", "grandpa", TURNIP]]),
    ("mouse", "cat", [[MOUSE, CAT, DOG], [DOG, GIRL, "grandma", "grandpa", TURNIP]]),
]


def spec(noun: str):
    """A name takes no article; a tale animal or the granddaughter is 'the ...' from the start."""
    return noun if noun in ("grandpa", "grandma") else the(noun)


def pages():
    out = [
        {"art": "p01_once", "focus": ["grandpa", "grandma"],
         "clauses": [{"phrase": "once_upon"}]},
        {"art": "p01_grandpa_plants", "focus": ["sow", "turnip"],
         "clauses": [{"subj": {"n": "grandpa"}, "verb": "sow", "obj": {"n": "turnip"},
                      "pp_to": ("in", SOIL)}]},
        {"art": "p03_turnip_big", "focus": ["big"],
         "clauses": [{"phrase": "repka_big"}]},
        {"art": "p04_grandpa_pulls", "focus": ["pull"],
         "clauses": [{"subj": {"n": "grandpa"}, "verb": "pull", "obj": TURNIP}]},
        {"art": "p04_grandpa_pulls",  # the refrain over the same picture
         "clauses": [{"phrase": "pull_fail_one"}]},
    ]
    # The pull-line picture of a helper step: the first two steps already have one (the old "comes"
    # pictures show the line pulling); the dog, cat and mouse steps get new pictures without the
    # not-yet-called animal in them.
    line_art = {"grandma": "p05_grandma_comes", "granddaughter": "p06_granddaughter_comes",
                "dog": "chain_dog", "cat": "chain_cat", "mouse": "chain_mouse"}
    for i, (newcomer, caller, chains) in enumerate(PLANS):
        last = newcomer == "mouse"  # with the mouse the chain wins: the refrain is the triumph
        out.append({"art": f"p0{5 + i}_{newcomer}_comes", "focus": [newcomer],
                    "clauses": [{"subj": spec(caller), "verb": "call", "obj": spec(newcomer)}]})
        for chain in chains:  # recitation pages: the cumulative chain, no cards
            out.append({"art": line_art[newcomer], "clauses": [{"chain": chain}]})
        out.append({"art": "p11_turnip_tumbles" if last else line_art[newcomer],
                    "clauses": [{"phrase": "pull_win" if last else "pull_fail"}]})
    out.append({"art": "p12_all_eat", "focus": ["eat"],
                "clauses": [{"subj": {"pron": "all"}, "verb": "eat", "obj": TURNIP}]})
    return out


STORY = {
    "title": "The Turnip",
    "tense": "past",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_repka"}]},
    "pages": pages(),
}
