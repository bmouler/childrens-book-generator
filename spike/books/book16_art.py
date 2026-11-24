"""Book 16 art prompts: Clap! Stomp! Hooray! The page names match the `art` keys of book16.py.
The toddler from the hero sheet does every action: the song is about the child's own body moving.
"""

MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."
NO_EXTRA = "No other objects, no decoration."
T = "Show the same toddler from the reference picture"

PAGES = {
    "p01_happy_clap": f"{T} standing on a plain soft-green floor, facing the viewer with a big happy "
                      f"smile, holding both open hands up in front of the chest, ready to clap. "
                      f"{MARGIN} {NO_EXTRA}",
    "p02_clap": f"{T} standing on a plain soft-green floor, clapping both hands together in front of "
                f"the chest, eyes closed in a delighted smile. Three small curved motion lines around "
                f"the hands. {MARGIN} {NO_EXTRA}",
    "p03_happy_stomp": f"{T} standing on a plain soft-green floor, facing the viewer with a big happy "
                       f"smile, one foot lifted high with a bent knee, ready to stomp. {MARGIN} "
                       f"{NO_EXTRA}",
    "p04_stomp": f"{T} standing on a plain soft-green floor, stomping one foot down hard, arms bent "
                 f"and pumping, mouth open in a laugh. Three small curved motion lines under the "
                 f"stomping foot. {MARGIN} {NO_EXTRA}",
    "p05_happy_hooray": f"{T} standing on a plain soft-green floor, facing the viewer with a huge "
                        f"open-mouth smile, one hand cupped beside the open mouth as if calling out. "
                        f"{MARGIN} {NO_EXTRA}",
    "p06_hooray": f"{T} jumping in the air on a plain soft-green floor, both arms thrown up in a V, "
                  f"mouth wide open in a cheer, feet off the ground. {MARGIN} {NO_EXTRA}",
    "p07_happy_all": f"{T} standing on a plain soft-green floor, facing the viewer with a big smile, "
                     f"wiggling the whole body: hands mid-clap and one foot mid-stomp at the same "
                     f"time. {MARGIN} {NO_EXTRA}",
    "p08_all_three": f"{T} in the middle of a plain soft-green floor, clapping both hands above the "
                     f"head while one foot stomps, mouth open shouting happily. Three small curved "
                     f"motion lines around the hands and under the foot. {MARGIN} {NO_EXTRA}",
}
COVER = (f"{T} standing in the middle of the picture on a plain soft-green floor, clapping both "
         f"hands with a huge happy smile, facing the viewer. {MARGIN} {NO_EXTRA}")
