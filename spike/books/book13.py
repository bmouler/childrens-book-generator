"""Book 13: "Kolobok" (Колобок). The canonical tale, in modern Russian.

Grandpa is hungry and asks for a bun; Grandma bakes Kolobok and sets him on the window to cool.
He jumps down and rolls away. The hare, the wolf and the bear each want to eat him, and each gets
the song (Я от дедушки ушёл, ...) — the modern refrain every child sings; the old pantry verses
(по коробу поскребла, на сметане мешен) are dropped. The clever fox asks for the song once more,
Kolobok sits on her nose, sings again, and the tale ends as it always ends: the fox eats him.
Meet and song pages are recitation pages: no word cards, bigger text.
Modernized words: дед/баба -> дедушка/бабушка, окошко -> окно, and the song skips the pantry verses.
"""
K = {"n": "kolobok"}


def the(noun: str) -> dict:
    return {"n": noun, "art": "the"}


def triple(animal, art_met, art_threat, art_song):
    """One hungry animal: they meet (recitation), it threatens (Я тебя съем!), Kolobok sings."""
    return [
        {"art": art_met,  # Колобок покатился по дороге и встретил ...: a recitation page
         "clauses": [{"subj": K, "verb": "roll", "pp": ("along", the("road"))},
                     {"subj": K, "verb": "meet", "obj": the(animal)}]},
        {"art": art_threat, "focus": [animal, "eat"],
         "clauses": [{"phrase": "i_will_eat_you"}, {"subj": the(animal), "verb": "say"}]},
        {"art": art_song,  # the song: a recitation page, no cards
         "clauses": [{"phrase": f"song_{animal}"}]},
    ]


STORY = {
    "title": "Kolobok",
    "tense": "past",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_kolobok"}]},
    "pages": [
        {"art": "p00_once", "focus": ["grandpa", "grandma"],
         "clauses": [{"phrase": "once_upon"}]},
        {"art": "p01a_grandpa_hungry", "focus": ["hungry"],
         "clauses": [{"subj": {"n": "grandpa"}, "pred": "hungry"},
                     {"phrase": "bake_one"}]},
        {"art": "p01_grandma_bakes", "focus": ["bake"],
         "clauses": [{"subj": {"n": "grandma"}, "verb": "bake", "obj": K}]},
        {"art": "p02_window", "focus": ["window"],
         "clauses": [{"subj": {"n": "grandma"}, "verb": "put", "obj": K, "pp_to": ("on", the("window"))}]},
        {"art": "p02_window",  # he cools on the window: the same picture, a recitation page
         "clauses": [{"subj": K, "verb": "cool"}]},
        {"art": "p03_kolobok_rolls",  # the escape: a recitation page, no cards
         "clauses": [{"subj": K, "verb": "jump", "pp": ("from", the("window"))},
                     {"subj": K, "verb": "roll"}]},
        *triple("hare", "p05_meets_hare", "p05b_hare_hungry", "song_hare"),
        *triple("wolf", "p06_meets_wolf", "p06b_wolf_hungry", "song_wolf"),
        *triple("bear", "p07_meets_bear", "p07b_bear_hungry", "song_bear"),
        {"art": "p08c_fox_clever", "focus": ["fox", "clever"],
         "clauses": [{"subj": K, "verb": "meet", "obj": the("fox")},
                     {"subj": the("fox"), "pred": "clever", "end": "!"}]},
        {"art": "p08_meets_fox", "focus": ["song"],
         "clauses": [{"imp": "sing", "obj": {"n": "song"}, "tense": "pres", "end": "!"},
                     {"subj": the("fox"), "verb": "say"},
                     {"subj": K, "verb": "sing"}]},
        {"art": "p08d_kolobok_sits", "focus": ["nose"],
         "clauses": [{"subj": K, "verb": "sit", "pp_to": ("on", the("nose"))}]},
        {"art": "p08d_kolobok_sits", "focus": ["sing"],  # he sings on her nose: the same picture
         "clauses": [{"subj": K, "verb": "sing", "adv": "again"}]},
        {"art": "p09_fox_eats", "focus": ["eat"],  # the canonical ending
         "clauses": [{"subj": the("fox"), "verb": "eat", "obj": K}]},
    ],
}
