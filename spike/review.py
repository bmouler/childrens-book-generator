"""The Russian review sheet: every sentence and every word choice of every book, for the native speaker
who vets the Russian. Generated from the compiled books, so it can never drift from them.

usage: review.py        write docs/RUSSIAN_REVIEW.md
"""
from __future__ import annotations

import pathlib

import library
import lexicon as L

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
APPROVED_BOOKS = (1,)  # Book 1 was checked on 2026-10-13. The first build looked correct.
STILL_OPEN = [  # strings of an approved book that a reviewer has not seen yet
    ("Book 1 cover title", "Sink or Float?", "Тонет или плавает?"),
    ("Page counter on every page (the digits are the page and the total)", "3 out of 10", "3 из 10"),
]
CHECK_FIRST = [  # choices where Russian has several good options. The compiler follows the curator.
    ("Cover titles Hot or Cold? / Heavy or Light?", "Горячо или холодно? / Тяжёлый или лёгкий?",
     "The temperature title uses the game words горячо/холодно. The weight title uses the adjectives, like the sentences."),
    ("The sun is hot.", "Солнце горячее.", "Alternative: Солнце жаркое. I chose горячее, the same adjective as for soup."),
    ("The balloon is light.", "Шарик лёгкий.", "шарик is the usual word for a balloon. It also means a small ball."),
    ("The teddy bear is soft.", "Мишка мягкий.", "мишка for teddy bear. Alternative: плюшевый мишка."),
    ("Rain falls! / Snow falls!", "Дождь идёт! / Снег идёт!",
     "One English verb (falls), one Russian verb (идёт). Alternative for snow: падает."),
    ("We put the ball in the box.", "Мы кладём мячик в коробку.", "кладём (imperfective, present) for put."),
    ("We give water to the seed.", "Мы даём воду семечку.", "семечко is the diminutive. Alternative: семя, dative семени."),
    ("Touch the ice! / Look at the sky!", "Потрогай лёд! / Посмотри на небо!",
     "Commands to one child (ты), like Теперь попробуй ты! in Book 1."),
    ("Who barks? / Who meows?", "Кто лает? / Кто мяукает?", "кто with a verb in the present tense."),
    ("The cover of Book 8 and Book 9", "Голоса животных / Погода", "Titles without highlighted words."),
    ("The end of Kolobok", "И лиса съела Колобка.",
     "The canonical ending: the fox eats him. Say the word and I keep him safe instead."),
    ("The end of Teremok", "Все построили новый домик.",
     "The Tolstoy ending: the house falls apart, then everyone builds a new one together."),
    ("The Happy Song refrain (Book 16)", "Если весело, хлопни в ладоши!",
     "The full song says «Если весело живёшь, хлопни в ладоши». I kept the short chant so it tracks the English line."),
    ("The rain chant (Book 17)", "Дождик, дождик, уходи! Приходи в другой день!",
     "The canonical chant says «перестань» (stop). I chose уходи: it matches go away word for word."),
    ("The spider song (Book 18)", "Паучок лезет вверх. Дождь смыл паучка.",
     "Itsy Bitsy Spider has no single canonical Russian text. These lines follow the English beat by beat."),
    ("The star song (Book 19)", "Мерцай, мерцай, звёздочка!",
     "Twinkle Twinkle has many Russian translations. This one keeps the imperative, like the English."),
    ("Toes (Book 20)", "пальчики",
     "Russian has one word for fingers and toes. The toddler word пальчики covers both; the picture shows the toes."),
    ("The farm sounds (Book 21)", "му-му, хрю-хрю, кря-кря, гав-гав",
     "The same sound words as Book 8."),
    ("The numerals (Book 22)", "Один нос. Два глаза. Пять пальчиков. Восемь планет.",
     "Russian numerals govern case and gender: один/одно, два + genitive singular, пять/восемь/десять + genitive plural. Each line is aligned by hand."),
    ("Fingers and toes (Books 20 and 22)", "пальчики",
     "One word covers both. Book 20 points at the toes; Book 22 counts fingers on one hand, then toes on two feet."),
    ("Planet Earth (Book 22)", "Мы живём на планете Земле!",
     "Земля with a capital letter, like a name. «На планете Земле» is the standard wording."),
    ("The counting chant (Book 22)", "Один, два, три, четыре, пять!",
     "The chant goes to five. Eight and ten arrive with the planets and the toes."),
    ("The has-form (Book 26)", "У кошки есть котёнок. У собаки есть щенок.",
     "Russian says 'at the cat there is a kitten'. The possessor takes the genitive: у кошки."),
    ("The because-clause (Books 23, 34)", "Камень тонет, потому что он тяжёлый.",
     "The pronoun repeats the thing: он for камень, оно for перо, она for коробка. Each page names its gender."),
    ("In the sun / in the shadow (Book 28)", "Мы кладём лёд на солнце. Мы кладём лёд в тени.",
     "Russian says 'on the sun' (на солнце) for the sunny spot and 'in the shadow' (в тени) for the shade."),
    ("The comparatives (Book 29)", "Что тяжелее: камень или перо? Камень тяжелее пера.",
     "The comparative does not decline (тяжелее, легче, больше). 'Than' takes the genitive: тяжелее пера."),
    ("The turning Earth (Book 33)", "Земля вертится, поэтому бывает день и ночь.",
     "вертится spins on its axis. 'So' is поэтому; 'there is day and night' is бывает день и ночь."),
    ("The orange test (Book 34)", "Апельсин плавает, потому что кожура лёгкая. У кожуры есть воздух.",
     "кожура is the peel of a fruit. The reason the orange floats: the peel holds air."),
    ("Water becomes (Book 35)", "Вода становится льдом. Вода становится паром.",
     "становиться + instrumental: льдом, паром, водой. The thing it becomes takes that case."),
    ("Counting eleven to twenty (Book 36)", "Одиннадцать звёзд. Двенадцать кубиков. Двадцать пальчиков.",
     "Eleven to fourteen take the genitive plural like два; fifteen to twenty also take the genitive plural. Each line is aligned by hand."),
    ("The senses (Book 37)", "У нас пять чувств. Мы закрываем глаза.",
     "чувства for the five senses. Closing and opening the eyes: закрываем / открываем."),
]
MODERNIZED = [  # the canonical folk texts, in modern Russian: what changed and what stayed
    ("дед / баба / бабка / дедка", "дедушка / бабушка", "all four tales"),
    ("Жучка, the dog's folk name", "собака", "Репка"),
    ("репа", "репка", "the tale's own word; the cover already says Репка"),
    ("мышка, лисичка, зайчик, яичко, окошко", "мышь, лиса, заяц, яйцо, окно", "plain modern words"),
    ("теремок / теремочек", "домик", "the title of Book 14 stays Теремок: it is the name of the tale"),
    ("мышка-норушка, лягушка-квакушка, зайчик-побегайчик, лисичка-сестричка, волк-серый бочок",
     "plain animal names", "the folk epithets of Теремок"),
    ("по коробу поскребла, по сусеку помела / на сметане мешен, в масле спряжен, на окошке стужен",
     "dropped", "the pantry verse of Kolobok's song; the refrain every child sings is kept letter for letter"),
    ("кудахчет", "dropped", "the hen's words are quoted directly, not clucked"),
    ("тянет-потянет, жили-были, большая-пребольшая, хвостик", "kept as they are",
     "expressive, but modern: every child knows them"),
]
_WORDS = {"nomn": "nominative", "accs": "accusative", "datv": "dative", "gent": "genitive",
          "ablt": "instrumental", "loct": "prepositional", "sing": "singular", "plur": "plural",
          "pres": "present", "past": "past", "futr": "future", "1per": "1st person",
          "2per": "2nd person", "3per": "3rd person", "masc": "masculine", "femn": "feminine",
          "neut": "neuter", "impr": "command", "excl": "to the listener"}


def _plain(slot: str) -> str:
    toks = [t for t in slot.replace("/", "+").split("+") if t != "VERB"]
    return ", ".join(_WORDS.get(t, t) for t in sorted(toks, key=lambda t: t not in ("pres", "past", "futr")))


def _lexicon_row(concept: str) -> tuple[str, str]:
    if concept in L.NAMES:
        return L.NAMES[concept][0], L.NAMES[concept][1]
    for table in (L.NOUNS, L.ADJS, L.PRONOUNS, L.PREPS, L.ADVS):
        if concept in table:
            return table[concept][0], table[concept][1]
    if concept in L.VERBS:
        v = L.VERBS[concept]
        lemmas = {v.get(k) for k in ("ru_pres", "ru_past", "ru_futr", "ru_impr")} - {None}
        return v["en"]["pres_pl"], " / ".join(sorted(lemmas))
    if concept in L.PHRASES:
        ph = L.PHRASES[concept]
        return _join(ph["en"]), _join(ph["ru"])
    return concept, "?"


def _join(side: list) -> str:
    out = ""
    for t, _ in side:
        out += t if t in {".", "!", "?", ","} or not out else " " + t
    return out


def write(path: pathlib.Path) -> None:
    numbers = library.numbers()
    compiled = {n: library.compiled(n) for n in numbers}
    approved = {row for n in APPROVED_BOOKS for row in compiled[n]["audit"]}
    forms: dict[str, dict[tuple[str, str], set[int]]] = {}
    for n in numbers:
        for concept, slot, form in compiled[n]["audit"]:
            forms.setdefault(concept, {}).setdefault((slot, form), set()).add(n)
    lines = ["# Russian review sheet", "",
             "Book 1 was checked on 2026-10-13. The first build looked correct. "
             "Book 1 below is that approved text. Books 2 to 37 are new: please check every row.", "",
             "## Please check first: choices where Russian has several good options", "",
             "| Where | Russian | Note |", "|---|---|---|"]
    lines += [f"| {w} | {r} | {note} |" for w, r, note in CHECK_FIRST]
    lines += ["", "## Strings of Book 1 that you have not seen yet", "", "| Where | English | Russian |", "|---|---|---|"]
    lines += [f"| {w} | {e} | {r} |" for w, e, r in STILL_OPEN]
    lines += ["", "## Folk tales: the old words and the modern words", "",
              "Books 12 to 15 follow the canonical texts. Only old words moved to modern Russian.", "",
              "| Old | Modern | Where and why |", "|---|---|---|"]
    lines += [f"| {old} | {new} | {note} |" for old, new, note in MODERNIZED]
    for n in numbers:
        book = compiled[n]
        status = "approved" if n in APPROVED_BOOKS else "new, please check"
        lines += ["", f"## Book {n}: {book['cover']['en']} / {book['cover']['ru']} ({status})", "",
                  "| Page | English | Russian |", "|---|---|---|"]
        lines += [f"| {i} | {pg['en']} | {pg['ru']} |" for i, pg in enumerate(book["pages"], 1)]
    lines += ["", "## Word choices of all books", "",
              "A row marked new is a form that Book 1 did not use. The slot says which form of the word the sentence needs.", "",
              "| Concept | English | Russian lemma | Form used | Books | Status |", "|---|---|---|---|---|---|"]
    for concept in sorted(forms):
        en, ru = _lexicon_row(concept)
        for (slot, form), used in sorted(forms[concept].items()):
            status = "approved" if (concept, slot, form) in approved else "new"
            lines.append(f"| {concept} | {en} | {ru} | {form} ({_plain(slot)}) | {', '.join(map(str, sorted(used)))} | {status} |")
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    DOCS.mkdir(exist_ok=True)
    write(DOCS / "RUSSIAN_REVIEW.md")
    print("wrote docs/RUSSIAN_REVIEW.md")
