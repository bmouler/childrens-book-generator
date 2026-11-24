"""Compile the sample story, stress the grammar, prove determinism and fail-closed behaviour."""
import contextlib
import sys

import bilingual as b

# Fixture only: proper-name protagonists exercise the NAMES path of the engine. No book uses a name.
b.NAMES.update({
    "fox": ("Fox", "лисёнок"),
    "rabbit": ("Rabbit", "зайчик"),
    "cat": ("Cat", "кошка"),
})


STORY = {
    "title": "Fox and the Yellow Ball",
    "tense": "pres",
    "pages": [
        {"art": "page1_fox_sees_ball", "clauses": [{"subj": "fox", "verb": "see", "obj": {"n": "ball", "adj": ["yellow"]}}]},
        {"art": "page2_fox_kicks_ball", "clauses": [{"subj": "fox", "verb": "kick", "obj": "ball"}]},
        {"art": None, "clauses": [{"subj": "rabbit", "verb": "see", "obj": "ball"}]},
        {"art": None, "clauses": [{"subj": "rabbit", "verb": "be_sad"}]},
        {"art": "page5_fox_gives_ball", "clauses": [{"subj": "fox", "verb": "give", "obj": "ball", "io": "rabbit"}]},
        {"art": "page6_play_together", "clauses": [{"subj": ["fox", "rabbit"], "verb": "play", "adv": "together"}]},
    ],
}

STRESS = [
    ({"subj": "fox", "verb": "see", "obj": "rabbit"}, "pres"),
    ({"subj": "cat", "verb": "see", "obj": {"n": "box", "adj": ["red"]}}, "pres"),
    ({"subj": "cat", "verb": "see", "obj": {"n": "ball", "adj": ["big", "red"]}}, "past"),
    ({"subj": "rabbit", "verb": "sit", "pp": ["under", "tree"]}, "pres"),
    ({"subj": "rabbit", "verb": "be", "pp": ["in", "box"]}, "pres"),
    ({"subj": "rabbit", "verb": "be", "pp": ["in", "box"]}, "past"),
    ({"subj": "fox", "verb": "kick", "obj": "ball"}, "past"),
    ({"subj": "rabbit", "verb": "give", "obj": "ball", "io": "fox"}, "past"),
    ({"subj": ["fox", "cat"], "verb": "play", "adv": "together"}, "pres"),
]


def run() -> dict:
    return b.compile_story(STORY)


_DEL = object()


@contextlib.contextmanager
def patched(table, key, value):
    """Temporarily set (or delete, with _DEL) one lexicon entry. Always restores it."""
    missing = object()
    old = table.get(key, missing)
    if value is _DEL:
        table.pop(key, None)
    else:
        table[key] = value
    try:
        yield
    finally:
        if old is missing:
            table.pop(key, None)
        else:
            table[key] = old


if __name__ == "__main__":
    if "--digest" in sys.argv:  # used by the cross-process determinism check
        print(b.digest(run()))
        raise SystemExit

    compiled = run()
    print("== STORY ==")
    for i, pg in enumerate(compiled["pages"], 1):
        print(f"p{i}  EN: {pg['en']:<34} RU: {pg['ru']}")
        print("     pairs:", "  ".join(f"{p['en']}={p['ru']}[c{p['color']}]" for p in pg["pairs"]))
    print("\nconcept colours:", compiled["colors"])

    print("\n== GRAMMAR STRESS (fresh discourse state each) ==")
    for cl, tense in STRESS:
        ctx = b.Ctx(tense, set(), set())
        en, ru = b.compile_clause(cl, ctx)
        print(f"[{tense:<4}] {b.text_of(en):<36} | {b.text_of(ru)}")

    print("\n== FAIL CLOSED (each case isolated, must be rejected for the stated reason) ==")
    LEAF_PL = ("лист", frozenset({"plur", "nomn"}))
    cases = [
        ("unknown word id", None, {"subj": "dragon", "verb": "see"}, "pres", "not in the lexicon"),
        ("perfective verb in present", (b.VERBS, "see", dict(b.VERBS["see"], ru_pres="увидеть")),
         {"subj": "fox", "verb": "see", "obj": "ball"}, "pres", "no form"),
        ("Russian word not in dictionary", (b.NOUNS, "blork", ("blork", "блорк", "blorks")),
         {"subj": "fox", "verb": "see", "obj": "blork"}, "pres", "not a known dictionary lemma"),
        ("several valid forms, no curator choice", (b.OVERRIDES, LEAF_PL, _DEL),
         {"subj": {"n": "leaf", "num": "pl"}, "verb": "float"}, "pres", "several valid forms"),
        ("plural not allowed for this noun", None,
         {"subj": {"n": "water", "num": "pl"}, "verb": "float"}, "pres", "no plural"),
        ("past tense, subject gender unknown", None,
         {"subj": {"pron": "I"}, "verb": "see", "obj": "ball"}, "past", "known gender"),
        ("first person with a third-person-only verb", None,
         {"subj": {"pron": "I"}, "verb": "be", "pp": ["in", "box"]}, "pres", "third-person"),
        ("future tense, no future lemma", None,
         {"q_or": {"subj": "ball", "verbs": ["kick"]}}, "pres", "no future-tense lemma"),
        ("mass noun without an explicit article", None,
         {"subj": {"pron": "we"}, "verb": "see", "obj": "ice"}, "pres", "mass or unique noun"),
        ("predicate adjective in the future tense", None,
         {"subj": {"n": "ball", "art": "the"}, "pred": "big"}, "futr", "present and past tense only"),
        ("command in the past tense", None,
         {"imp": "touch", "obj": "ball"}, "past", "present tense only"),
        ("predicate adjective with a pronoun subject", None,
         {"subj": {"pron": "we"}, "pred": "big"}, "pres", "not a pronoun"),
        ("predicate with three adjectives", None,
         {"subj": {"n": "ball", "art": "the"}, "pred": ["big", "red", "round"]}, "pres", "two joined"),
        ("command with a verb that has no command lemma", None,
         {"imp": "see", "obj": "ball"}, "pres", "no ru_impr lemma"),
        ("motion phrase with a preposition that has no direction case", None,
         {"subj": {"pron": "we"}, "verb": "look", "pp_to": ["at", {"n": "sky", "art": "the"}]}, "pres",
         "no direction case"),
        ("two prepositional phrases in one clause", None,
         {"subj": {"pron": "we"}, "verb": "put", "obj": "ball", "pp": ["in", "box"], "pp_to": ["on", "table"]},
         "pres", "one prepositional phrase"),
        ("verb with no past lemma, used in the past", None,
         {"subj": {"pron": "we"}, "verb": "listen"}, "past", "no ru_past lemma"),
        ("two valid plurals of цветок, no curator choice",
         (b.OVERRIDES, ("цветок", frozenset({"plur", "nomn"})), _DEL),
         {"subj": {"n": "flower", "num": "pl"}, "verb": "grow"}, "pres", "several valid forms"),
        ("two valid forms of ветер, no curator choice",
         (b.OVERRIDES, ("ветер", frozenset({"sing", "nomn"})), _DEL),
         {"subj": {"n": "wind", "art": "the"}, "verb": "blow"}, "pres", "several valid forms"),
    ]
    failed = 0
    for label, patch, cl, tense, expect in cases:
        try:
            with patched(*patch) if patch else contextlib.nullcontext():
                b.compile_clause(cl, b.Ctx(tense, set(), set()))
            print(f"{label}: NOT REJECTED  <-- bug")
            failed += 1
        except b.LexiconError as e:
            ok = expect in str(e)
            failed += not ok
            print(f"{label}: {'rejected' if ok else 'REJECTED FOR THE WRONG REASON'} -> {e}")
    if failed:
        raise SystemExit(f"{failed} fail-closed case(s) broken")

    print("\n== NEW CLAUSE FORMS (exact English and Russian) ==")
    WE = {"pron": "we"}

    def the(n: str) -> dict:
        return {"n": n, "art": "the"}

    forms = [
        ({"subj": the("ice"), "pred": "cold", "end": "!"}, "The ice is cold!", "Лёд холодный!"),
        ({"subj": {"n": "stone", "num": "pl"}, "pred": "heavy"}, "Stones are heavy.", "Камни тяжёлые."),
        ({"subj": the("feather"), "pred": "light"}, "The feather is light.", "Перо лёгкое."),
        ({"q_or_adj": {"subj": the("ice"), "adjs": ["hot", "cold"]}}, "Is the ice hot or cold?",
         "Лёд горячий или холодный?"),
        ({"q_or_adj": {"subj": the("mouse"), "adjs": ["big", "small"]}}, "Is the mouse big or small?",
         "Мышь большая или маленькая?"),
        ({"q_or_adj": {"subj": {"n": "stone", "num": "pl", "art": "the"}, "adjs": ["heavy", "light"]}},
         "Are the stones heavy or light?", "Камни тяжёлые или лёгкие?"),
        ({"q_where": the("ball")}, "Where is the ball?", "Где мячик?"),
        ({"q_where": {"n": "ball", "num": "pl", "art": "the"}}, "Where are the balls?", "Где мячики?"),
        ({"imp": "touch", "obj": the("ice"), "end": "!"}, "Touch the ice!", "Потрогай лёд!"),
        ({"imp": "look", "pp": ["at", the("sky")], "end": "!"}, "Look at the sky!", "Посмотри на небо!"),
        ({"subj": WE, "verb": "put", "obj": the("ball"), "pp_to": ["in", the("box")]},
         "We put the ball in the box.", "Мы кладём мячик в коробку."),
        ({"subj": WE, "verb": "put", "obj": the("ball"), "pp_to": ["on", the("table")]},
         "We put the ball on the table.", "Мы кладём мячик на стол."),
        ({"subj": WE, "verb": "put", "obj": the("ball"), "pp_to": ["under", the("chair")]},
         "We put the ball under the chair.", "Мы кладём мячик под стул."),
        ({"subj": the("ball"), "verb": "be", "pp": ["under", the("chair")]},
         "The ball is under the chair.", "Мячик под стулом."),
        ({"subj": {"pron": "who"}, "verb": "bark", "end": "?"}, "Who barks?", "Кто лает?"),
        ({"subj": the("wind"), "verb": "blow", "end": "!"}, "The wind blows!", "Ветер дует!"),
        ({"subj": {"n": "flower", "num": "pl"}, "verb": "grow"}, "Flowers grow.", "Цветы растут."),
        ({"subj": {"pron": "I"}, "be_np": {"n": "mouse"}}, "I am a mouse.", "Я мышь."),
        ({"subj": {"pron": "I"}, "be_np": the("bear"), "end": "!"}, "I am the bear!", "Я медведь!"),
        ({"subj": WE, "verb": "give", "obj": {"n": "water", "art": ""}, "io": the("seed")},
         "We give water to the seed.", "Мы даём воду семечку."),
        ({"subj": WE, "verb": "see", "obj": {"n": "ice", "art": ""}}, "We see ice.", "Мы видим лёд."),
        # the connective grammar of books 23 to 37
        ({"join": "because", "parts": [{"subj": the("stone"), "verb": "sink"},
                                       {"pred": "heavy", "subj": {"pron": "it_m"}}]},
         "The stone sinks because it is heavy.", "Камень тонет, потому что он тяжёлый."),
        ({"join": "so", "parts": [{"subj": the("wind"), "verb": "blow"},
                                  {"subj": the("leaf"), "verb": "tumble"}]},
         "The wind blows so the leaf falls.", "Ветер дует, поэтому лист падает."),
        ({"join": "but", "parts": [{"pred": "heavy", "subj": the("watermelon")},
                                   {"subj": {"pron": "it_m"}, "verb": "float"}]},
         "The watermelon is heavy but it floats.", "Арбуз тяжёлый, но он плавает."),
        ({"lead": "first", "subj": WE, "verb": "guess"}, "First we guess.", "Сначала мы угадываем."),
        ({"lead": "because", "pred": "light", "subj": {"pron": "it_n"}, "end": "!"},
         "Because it is light!", "Потому что оно лёгкое!"),
        ({"q_why": {"subj": the("stone"), "verb": "sink"}}, "Why does the stone sink?",
         "Почему камень тонет?"),
        ({"q_why": {"subj": WE, "verb": "wait"}}, "Why do we wait?", "Почему мы ждём?"),
        ({"q_which_comp": {"comp": "heavy", "subj": [the("stone"), the("ball")]}},
         "Which is heavier: the stone or the ball?", "Что тяжелее: камень или мячик?"),
        ({"pred": [{"comp": "heavy", "than": the("ball")}], "subj": the("stone")},
         "The stone is heavier than the ball.", "Камень тяжелее мячика."),
        ({"pred": [{"comp": "light"}], "subj": the("feather")}, "The feather is lighter.",
         "Перо легче."),
        ({"has": {"subj": "dog", "obj": "puppy"}}, "A dog has a puppy.", "У собаки есть щенок."),
        ({"subj": WE, "verb": "take", "obj": the("ball"), "pp_from": the("box")},
         "We take the ball out of the box.", "Мы достаём мячик из коробки."),
        ({"subj": the("orange"), "verb": "float", "pp": ["with", {"n": "peel", "art": ""}]},
         "The orange floats with peel.", "Апельсин плавает с кожурой."),
        ({"subj": {"pron": "it_m"}, "verb": "sink", "pp": ["without", {"n": "peel", "art": ""}]},
         "It sinks without peel.", "Он тонет без кожуры."),
        ({"subj": the("water"), "verb": "become", "instr": the("ice")},
         "The water becomes ice.", "Вода становится льдом."),
        ({"subj": the("sun"), "verb": "make", "obj": "shadow"}, "The sun makes a shadow.",
         "Солнце делает тень."),
        ({"subj": WE, "verb": "touch", "obj": the("water")}, "We touch the water.",
         "Мы трогаем воду."),
        ({"subj": the("puddle"), "verb": "freeze"}, "The puddle freezes.", "Лужа замерзает."),
        ({"subj": "puddle", "verb": "freeze"}, "A puddle freezes.", "Лужа замерзает."),
    ]
    wrong = 0
    for cl, want_en, want_ru in forms:
        en, ru = b.compile_clause(cl, b.Ctx("pres", set(), set()))
        got = (b.text_of(en), b.text_of(ru))
        ok = got == (want_en, want_ru)
        wrong += not ok
        print(f"{'ok ' if ok else 'BAD'} {got[0]:<36} | {got[1]}" + ("" if ok else f"    expected {want_en} | {want_ru}"))
    if wrong:
        raise SystemExit(f"{wrong} clause form(s) wrong")

    print("\n== PAST TENSE (exact English and Russian) ==")
    past_forms = [
        ({"subj": the("stone"), "pred": "heavy"}, "The stone was heavy.", "Камень был тяжёлый."),
        ({"subj": the("turnip"), "pred": "big"}, "The turnip was big.", "Репка была большая."),
        ({"subj": the("egg"), "pred": "golden"}, "The egg was golden.", "Яйцо было золотое."),
        ({"subj": {"n": "stone", "num": "pl"}, "pred": "heavy"}, "Stones were heavy.",
         "Камни были тяжёлые."),
        ({"subj": "grandpa", "verb": "sow", "obj": {"n": "turnip"}},
         "Grandpa planted a turnip.", "Дедушка посадил репку."),
        ({"subj": the("turnip"), "verb": "grow"}, "The turnip grew.", "Репка выросла."),
        ({"subj": {"pron": "all"}, "verb": "eat", "obj": the("turnip")}, "All ate the turnip.",
         "Все съели репку."),
        ({"subj": the("ball"), "verb": "be", "pp": ["under", the("chair")]},
         "The ball was under the chair.", "Мячик был под стулом."),
        ({"subj": ["grandma", "grandpa"], "verb": "be_sad"}, "Grandma and Grandpa were sad.",
         "Бабушка и Дедушка грустили."),
        ({"subj": "grandma", "verb": "bake", "obj": {"n": "kolobok"}},
         "Grandma baked Kolobok.", "Бабушка испекла Колобка."),
        ({"subj": the("turnip"), "pred": ["big", "round"]}, "The turnip was big and round.",
         "Репка была большая и круглая."),
        ({"subj": the("ice"), "pred": ["cold", "wet"]}, "The ice was cold and wet.",
         "Лёд был холодный и мокрый."),
        ({"subj": "kolobok", "verb": "sing"}, "Kolobok sang.", "Колобок пел."),
        ({"subj": "kolobok", "verb": "sing", "obj": {"n": "song"}}, "Kolobok sang a song.",
         "Колобок пел песню."),
        ({"subj": the("hen"), "pred": "clever", "end": "!"}, "The hen was clever!", "Курочка была хитрая!"),
        ({"subj": {"n": "frog"}, "verb": "jump", "pp_to": ["in", the("house")], "end": "!"},
         "A frog jumped in the house!", "Лягушка прыгнула в домик!"),
        ({"subj": {"n": "dog"}, "verb": "bark", "end": "!"}, "A dog barked!", "Собака залаяла!"),
        ({"subj": {"n": "cat"}, "verb": "meow", "end": "!"}, "Cat meowed!", "Кошка замяукала!"),
        ({"subj": {"pron": "all"}, "verb": "be_happy", "end": "!"}, "All were happy!", "Все радовались!"),
        ({"subj": ["grandma", "grandpa"], "pred": "happy", "end": "!"},
         "Grandma and Grandpa were happy!", "Бабушка и Дедушка были счастливые!"),
        ({"chain": ["grandma", "grandpa", the("turnip")]}, "Grandma held Grandpa, and Grandpa the turnip.",
         "Бабушка за Дедушку, Дедушка за репку."),
        ({"chain": [the("mouse"), the("dog"), the("wolf")]}, "The mouse held the dog, and the dog the wolf.",
         "Мышь за собаку, собака за волка."),
        ({"subj": {"pron": "nobody"}, "verb": "answer", "neg": True}, "Nobody answered.",
         "Никто не ответил."),
        ({"subj": the("wolf"), "verb": "eat", "obj": the("turnip"), "neg": True},
         "The wolf did not eat the turnip.", "Волк не съел репку."),
        ({"subj": the("mouse"), "verb": "wave", "instr": the("tail")}, "The mouse waved its tail.",
         "Мышь махнула хвостиком."),
    ]
    for cl, want_en, want_ru in past_forms:
        en, ru = b.compile_clause(cl, b.Ctx("past", set(), set()))
        got = (b.text_of(en), b.text_of(ru))
        ok = got == (want_en, want_ru)
        wrong += not ok
        print(f"{'ok ' if ok else 'BAD'} {got[0]:<36} | {got[1]}" + ("" if ok else f"    expected {want_en} | {want_ru}"))
    if wrong:
        raise SystemExit(f"{wrong} past-tense form(s) wrong")

    print("\n== SONG LINES (exact English and Russian) ==")
    song_forms = [
        ({"phrase": "happy_clap"}, "If you are happy, clap your hands!", "Если весело, хлопни в ладоши!"),
        ({"phrase": "happy_stomp"}, "If you are happy, stomp your feet!", "Если весело, топни ножкой!"),
        ({"phrase": "title_happy_song"}, "Clap! Stomp! Hooray!", "Хлоп! Топ! Ура!"),
        ({"phrase": "rain_go_away"}, "Rain, rain, go away!", "Дождик, дождик, уходи!"),
        ({"phrase": "come_another_day"}, "Come again another day!", "Приходи в другой день!"),
        ({"phrase": "up_the_pipe"}, "Up, up, up the pipe!", "Вверх, вверх, по трубе!"),
        ({"phrase": "twinkle_star"}, "Twinkle, twinkle, little star!", "Мерцай, мерцай, звёздочка!"),
        ({"phrase": "sleep_star"}, "Sleep, little star!", "Спи, звёздочка!"),
        ({"phrase": "chant_body"}, "Head, shoulders, knees and toes!", "Голова, плечи, колени и пальчики!"),
        ({"phrase": "says_cow"}, "The cow says: moo-moo!", "Корова говорит: му-му!"),
        ({"phrase": "says_pig"}, "The pig says: oink-oink!", "Свинья говорит: хрю-хрю!"),
        ({"phrase": "says_duck"}, "The duck says: quack-quack!", "Утка говорит: кря-кря!"),
        ({"phrase": "says_dog"}, "The dog says: woof-woof!", "Собака говорит: гав-гав!"),
        ({"phrase": "refrain_farm_1"}, "Moo-moo here, oink-oink there!", "Му-му тут, хрю-хрю там!"),
        ({"phrase": "farm_finale"}, "All the animals sing together!", "Все поют вместе!"),
        ({"subj": the("sun"), "verb": "dry", "obj": {"n": "puddle", "num": "pl", "art": "the"}},
         "The sun dries the puddles.", "Солнце сушит лужи."),
        ({"subj": the("rain"), "verb": "wash_out", "obj": the("spider")},
         "The rain washes out the spider.", "Дождь смывает паучка."),
        ({"imp": "touch", "obj": {"n": "toe", "art": "the", "num": "pl"}, "end": "!"},
         "Touch the toes!", "Потрогай пальчики!"),
        ({"subj": the("spider"), "verb": "climb", "adv": "up", "end": "!"},
         "The spider climbs up!", "Паучок лезет вверх!"),
        ({"phrase": "one_nose"}, "One nose!", "Один нос!"),
        ({"phrase": "five_fingers"}, "Five fingers on one hand!", "Пять пальчиков на одной руке!"),
        ({"phrase": "ten_toes"}, "Ten toes on two feet!", "Десять пальчиков на двух ногах!"),
        ({"phrase": "count_chant"}, "One, two, three, four, five!", "Один, два, три, четыре, пять!"),
        ({"phrase": "eight_planets"}, "Eight planets go around the sun!", "Восемь планет вокруг солнца!"),
        ({"phrase": "on_earth"}, "We live on planet Earth!", "Мы живём на планете Земле!"),
        ({"phrase": "count_again"}, "Count with me again!", "Считай со мной опять!"),
    ]
    for cl, want_en, want_ru in song_forms:
        en, ru = b.compile_clause(cl, b.Ctx("pres", set(), set()))
        got = (b.text_of(en), b.text_of(ru))
        ok = got == (want_en, want_ru)
        wrong += not ok
        print(f"{'ok ' if ok else 'BAD'} {got[0]:<36} | {got[1]}" + ("" if ok else f"    expected {want_en} | {want_ru}"))
    if wrong:
        raise SystemExit(f"{wrong} song line(s) wrong")

    print("\n== PAGE FURNITURE AND PAGE STRUCTURE ==")

    def rejected(fn, expect) -> bool:
        try:
            fn()
        except b.LexiconError as e:
            return expect in str(e)
        return False

    counter = b.compile_counter(3, 10)
    two = b.compile_story({"pages": [{"clauses": [{"subj": "fox", "verb": "see", "obj": "ball"},
                                                  {"subj": "rabbit", "verb": "see", "obj": "ball"}]}]})["pages"][0]
    ids = [p["id"] for p in two["pairs"]]
    used = {s["pair"] for s in two["en_segs"] + two["ru_segs"] if s["pair"] is not None}
    hue_story = {"pills": "hues", "pages": [
        {"clauses": [{"subj": {"pron": "we"}, "verb": "see", "obj": {"n": "ball", "adj": ["red"], "art": "a"}}],
         "focus": ["red"]},
        {"clauses": [{"phrase": "now_you_try"}], "focus": ["try"]}]}
    hue_pages = b.compile_story(hue_story)["pages"]
    hue_ok = ([p["concept"] for p in hue_pages[0]["pairs"]] == ["red"]
              and all(s["pair"] is None for s in hue_pages[0]["en_segs"] if s["t"] in ("We", "see", "a", "ball"))
              and [p["concept"] for p in hue_pages[1]["pairs"]] == ["try"])

    def duplicate_id():
        with patched(b.NOUNS, "red", ("red", "красный", None)):
            b.check_lexicon()

    # Forced temperature colours (hot red, cold blue) plus a first page "We see ice." leave the greedy
    # pass with no free colour for "ice": it used to give ice the colour of hot, side by side on one page.
    ice_story = {"pages": [
        {"clauses": [{"subj": {"pron": "we"}, "verb": "see", "obj": {"n": "ice", "art": ""}}]},
        {"clauses": [{"q_or_adj": {"subj": {"n": "ice", "art": "the"}, "adjs": ["hot", "cold"]}}]},
        {"clauses": [{"subj": {"n": "ice", "art": ""}, "pred": "cold"}, {"subj": {"n": "soup", "art": ""}, "pred": "hot"}]},
    ]}
    shades = b.compile_story(ice_story)["colors"]
    shades_ok = (shades["ice"] not in (shades["hot"], shades["cold"])
                 and shades["soup"] not in (shades["hot"], shades["cold"]) and shades["ice"] != shades["soup"])

    # Cards teach the word, so a card face is the lexicon citation form, never the case, number or
    # gender the sentence happened to need ("лиса", not "лису"). Verb cards keep the sentence form.
    card_pg = b.compile_story({"pages": [{"clauses": [
        {"subj": "fox", "verb": "see", "obj": {"n": "turnip"}},
        {"subj": {"n": "sun", "art": "the"}, "pred": "warm"}]}]})["pages"][0]
    card_pairs = {p["concept"]: p for p in card_pg["pairs"]}

    win = b.compile_clause({"phrase": "pull_win"}, b.Ctx("past", set(), set()))
    win_ok = (b.text_of(win[0]), b.text_of(win[1])) == ("They pulled and pulled, and pulled the turnip out!",
                                                        "Тянут-потянут — вытянули репку!")
    song = b.compile_clause({"phrase": "song_hare"}, b.Ctx("past", set(), set()))
    song_ok = b.text_of(song[1]) == "Я колобок! Я от дедушки ушёл, я от бабушки ушёл, и от тебя, заяц, уйду!"

    checks = [
        ("counter says 3 out of 10 / 3 из 10", (counter["en"], counter["ru"]) == ("3 out of 10", "3 из 10")),
        ("counter pairs match digit to digit and out of to из",
         [(p["concept"], p["en"], p["ru"]) for p in counter["pairs"]] == [("n", "3", "3"), ("of", "out of", "из"), ("total", "10", "10")]),
        ("page 0 of 10 is rejected", rejected(lambda: b.compile_counter(0, 10), "outside")),
        ("page 11 of 10 is rejected", rejected(lambda: b.compile_counter(11, 10), "outside")),
        ("two clauses on one page keep unique pair ids", len(ids) == len(set(ids)) and used <= set(ids)),
        ("a key word that is not on the page is rejected", rejected(
            lambda: b.compile_story({"pages": [{"clauses": [{"subj": "fox", "verb": "see", "obj": "ball"}], "focus": ["leaf"]}]}),
            "not a highlighted word")),
        ("a cover word that no page uses is rejected", rejected(
            lambda: b.compile_story({**STORY, "cover": {"clauses": [{"phrase": "title_sink_float"}]}}),
            "which no story page uses")),
        ("a colours book highlights only colour words and the key words of a page", hue_ok),
        ("a pills mode that does not exist is rejected", rejected(
            lambda: b.compile_story({**STORY, "pills": "some"}), "pills must be")),
        ("a concept id in two lexicon tables is rejected", rejected(duplicate_id, "is in both")),
        ("words of one sentence get different pill colours when four colours are enough", shades_ok),
        ("a noun card shows the citation form (репка), not the case form of the sentence (репку)",
         card_pairs["turnip"]["ru"] == "репку" and b.card_text(card_pairs["turnip"]) == ("turnip", "репка")),
        ("an adjective card shows the masculine citation form (тёплый), not the sentence gender (тёплое)",
         card_pairs["warm"]["ru"] == "тёплое" and b.card_text(card_pairs["warm"]) == ("warm", "тёплый")),
        ("a verb card keeps the sentence form in both languages",
         b.card_text(card_pairs["see"]) == (card_pairs["see"]["en"], card_pairs["see"]["ru"])),
        ("the grasp chain is refused in the present tense", rejected(
            lambda: b.compile_clause({"chain": ["grandma", "grandpa"]}, b.Ctx("pres", set(), set())),
            "past tense only")),
        ("'be' with a noun complement is refused in the past tense", rejected(
            lambda: b.compile_clause({"subj": {"pron": "I"}, "be_np": {"n": "mouse"}}, b.Ctx("past", set(), set())),
            "present tense only")),
        ("negation of a 'be' verb is refused", rejected(
            lambda: b.compile_clause({"subj": the("stone"), "verb": "be", "neg": True}, b.Ctx("past", set(), set())),
            "'be' verbs")),
        ("the winning refrain is the canonical Тянут-потянут — вытянули репку", win_ok),
        ("Kolobok's song to the hare is the canonical modern refrain, letter for letter", song_ok),
    ]
    broken = 0
    for label, ok in checks:
        print(f"{label}: {'ok' if ok else 'BROKEN'}")
        broken += not ok
    if broken:
        raise SystemExit(f"{broken} page check(s) broken")

    print("\n== REVIEW AUDIT (every Russian form the story used) ==")
    for concept, grams, form in compiled["audit"]:
        print(f"  {concept:<8} {grams:<22} {form}")
    print("\ndigest:", b.digest(compiled))
