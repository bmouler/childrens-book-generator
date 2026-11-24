"""The curated lexicon: every word, phrase and Russian form the books may use.

A person reviews each entry once, then it is frozen. (The real version is YAML in git, about 300
entries.) bilingual.py is the engine that reads these tables. Rules:
  - A concept id is unique across all tables, because an id names a pill colour and a sticker.
  - A Russian lemma must be a dictionary word. The engine refuses guesses and ambiguous forms.
  - A noun without an English plural (None) is a mass or unique noun. A story must give it an
    explicit article, 'the' or ''.
"""

NAMES = {  # proper-name protagonists: id -> (EN, RU lemma). The tale elders and Kolobok act as names:
    # no article and a capital letter in both languages, in any position.
    "grandpa": ("Grandpa", "дедушка"),
    "grandma": ("Grandma", "бабушка"),
    "kolobok": ("Kolobok", "колобок"),
    "earth": ("Earth", "земля"),  # the planet's name: capital and no article, like a protagonist.
}

NOUNS = {  # id -> (EN singular, RU lemma, EN plural or None)
    "ball": ("ball", "мячик", "balls"),
    "box": ("box", "коробка", "boxes"),
    "tree": ("tree", "дерево", "trees"),
    "water": ("water", "вода", None),
    "stone": ("stone", "камень", "stones"),
    "leaf": ("leaf", "лист", "leaves"),
    "ice": ("ice", "лёд", None),
    "soup": ("soup", "суп", None),
    "sun": ("sun", "солнце", None),
    "snow": ("snow", "снег", None),
    "feather": ("feather", "перо", "feathers"),
    "balloon": ("balloon", "шарик", "balloons"),
    "watermelon": ("watermelon", "арбуз", "watermelons"),
    "elephant": ("elephant", "слон", "elephants"),
    "mouse": ("mouse", "мышь", "mice"),
    "flower": ("flower", "цветок", "flowers"),
    "pillow": ("pillow", "подушка", "pillows"),
    "block": ("block", "кубик", "blocks"),
    "teddy": ("teddy bear", "мишка", "teddy bears"),
    "table": ("table", "стол", "tables"),
    "chair": ("chair", "стул", "chairs"),
    "apple": ("apple", "яблоко", "apples"),
    "sea": ("sea", "море", None),
    "sky": ("sky", "небо", None),
    "cloud": ("cloud", "облако", "clouds"),
    "rain": ("rain", "дождь", None),
    "wind": ("wind", "ветер", None),
    "grass": ("grass", "трава", None),
    "dog": ("dog", "собака", "dogs"),
    "cat": ("cat", "кошка", "cats"),
    "cow": ("cow", "корова", "cows"),
    "duck": ("duck", "утка", "ducks"),
    "seed": ("seed", "семечко", "seeds"),
    "soil": ("soil", "земля", None),
    "plant": ("plant", "растение", "plants"),
    # folk-tale cast and props (books 12 to 15)
    "turnip": ("turnip", "репка", "turnips"),  # репка, the tale's own word (репа is the field word)
    "granddaughter": ("granddaughter", "внучка", "granddaughters"),
    "song": ("song", "песня", "songs"),
    "hare": ("hare", "заяц", "hares"),
    "wolf": ("wolf", "волк", "wolves"),
    "bear": ("bear", "медведь", "bears"),
    "fox": ("fox", "лиса", "foxes"),
    "frog": ("frog", "лягушка", "frogs"),
    "house": ("house", "домик", "houses"),  # a little house, as in Теремок
    "hen": ("hen", "курочка", "hens"),
    "egg": ("egg", "яйцо", "eggs"),
    # more props for the canonical tale texts
    "field": ("field", "поле", "fields"),
    "window": ("window", "окно", "windows"),
    "road": ("road", "дорога", "roads"),
    "nose": ("nose", "нос", "noses"),
    "tail": ("tail", "хвостик", "tails"),  # the tale says хвостик; хвост is the plain modern word
    "roof": ("roof", "крыша", "roofs"),
    # song and rhyme books (16 to 21)
    "day": ("day", "день", "days"),
    "puddle": ("puddle", "лужа", "puddles"),
    "spider": ("spider", "паучок", "spiders"),
    "pipe": ("pipe", "труба", "pipes"),
    "star": ("star", "звёздочка", "stars"),
    "head": ("head", "голова", "heads"),
    "shoulder": ("shoulder", "плечо", "shoulders"),
    "knee": ("knee", "колено", "knees"),
    "toe": ("toe", "пальчик", "toes"),  # пальчик: for a toddler, пальчики covers fingers and toes
    "eye": ("eye", "глаз", "eyes"),
    "ear": ("ear", "ухо", "ears"),
    "mouth": ("mouth", "рот", "mouths"),
    "farm": ("farm", "ферма", "farms"),
    "pig": ("pig", "свинья", "pigs"),
    # the counting book (22)
    "finger": ("finger", "пальчик", "fingers"),  # same word as the toes of book 20: пальчики
    "planet": ("planet", "планета", "planets"),
    # the older-kids books (23 to 37)
    "kitten": ("kitten", "котёнок", "kittens"),
    "puppy": ("puppy", "щенок", "puppies"),
    "chick": ("chick", "цыплёнок", "chicks"),
    "calf": ("calf", "телёнок", "calves"),
    "shadow": ("shadow", "тень", "shadows"),
    "orange": ("orange", "апельсин", "oranges"),
    "peel": ("peel", "кожура", None),  # the orange's skin: a mass noun here
    "winter": ("winter", "зима", "winters"),
    "spring": ("spring", "весна", "springs"),
    "summer": ("summer", "лето", "summers"),
    "autumn": ("autumn", "осень", "autumns"),
    "night": ("night", "ночь", "nights"),
    "moon": ("moon", "луна", "moons"),
    "morning": ("morning", "утро", "mornings"),
    "bag": ("bag", "сумка", "bags"),
    "duckling": ("duckling", "утёнок", "ducklings"),
    "air": ("air", "воздух", None),
    "steam": ("steam", "пар", None),
    "hand": ("hand", "рука", "hands"),
    "sense": ("sense", "чувство", "senses"),
}
ADJS = {  # id -> (EN, RU lemma, hue). A word with a hue is always highlighted in that colour: the four
    # colour words, and the temperatures (hot is red, warm is yellow, cold is blue).
    "yellow": ("yellow", "жёлтый", "yellow"),
    "red": ("red", "красный", "red"),
    "green": ("green", "зелёный", "green"),
    "blue": ("blue", "синий", "blue"),
    "big": ("big", "большой", None),
    "small": ("small", "маленький", None),
    "hot": ("hot", "горячий", "red"),
    "cold": ("cold", "холодный", "blue"),
    "warm": ("warm", "тёплый", "yellow"),
    "heavy": ("heavy", "тяжёлый", None),
    "light": ("light", "лёгкий", None),
    "soft": ("soft", "мягкий", None),
    "hard": ("hard", "твёрдый", None),
    "wet": ("wet", "мокрый", None),
    "round": ("round", "круглый", None),
    "golden": ("golden", "золотой", None),
    "white": ("white", "белый", None),
    "happy": ("happy", "счастливый", None),
    "speckled": ("speckled", "рябой", None),
    "hungry": ("hungry", "голодный", None),
    "clever": ("clever", "хитрый", None),
    "new": ("new", "новый", None),
    "plain": ("plain", "простой", None),
    "bright": ("bright", "яркий", None),
    "long": ("long", "длинный", None),
    "short": ("short", "короткий", None),
    "quiet": ("quiet", "тихий", None),
}
ADVS = {  # id -> (EN, RU)
    "together": ("together", "вместе"),
    "where": ("where", "где"),
    "past": ("past", "мимо"),  # runs past = бежит мимо
    "again": ("again", "снова"),
    "up": ("up", "вверх"),
    "down": ("down", "вниз"),
    "fast": ("fast", "быстро"),
    "slow": ("slowly", "медленно"),
    "quietly": ("quiet", "тихо"),
    "loudly": ("loud", "громко"),
}
PREPS = {  # id -> (EN word, RU preposition, RU case that marks where something is)
    "in": ("in", "в", "loct"),
    "under": ("under", "под", "ablt"),
    "on": ("on", "на", "loct"),
    "at": ("at", "на", "accs"),  # look at = смотреть на + accusative
    "from": ("from", "с", "gent"),  # jumps from the window = прыгает с окна
    "out_of": ("out of", "из", "gent"),  # runs out of the house = бежит из домика
    "along": ("along", "по", "datv"),  # rolls along the road = катится по дороге
    "with": ("with", "с", "ablt"),  # with peel = с кожурой
    "without": ("without", "без", "gent"),  # without peel = без кожуры
    "after": ("after", "за", "ablt"),  # runs after me = бежит за мной
}
PREP_DIR = {  # RU case after the same preposition when something MOVES there: put it in the box
    "in": "accs",
    "under": "accs",
    "on": "accs",
}
PRONOUNS = {  # id -> (EN, RU, person, number, optional gender for verb agreement). Nominative only.
    "I": ("I", "я", 1, "sing"),
    "we": ("we", "мы", 1, "plur"),
    "you": ("you", "ты", 2, "sing"),
    "who": ("who", "кто", 3, "sing", "masc"),  # кто takes masculine agreement: Кто лает?
    "all": ("all", "все", 3, "plur"),
    "nobody": ("nobody", "никто", 3, "sing", "masc"),  # Никто не ответил
    "it_m": ("it", "он", 3, "sing", "masc"),  # the stone... it is heavy = камень... он тяжёлый
    "it_f": ("it", "она", 3, "sing", "femn"),  # the box... it is big = коробка... она большая
    "it_n": ("it", "оно", 3, "sing", "neut"),  # the feather... it is light = перо... оно лёгкое
}
CONN = {  # words that frame or join clauses. A lead word starts a sentence and both sides capitalise
    # it; a join word sits between two clauses after a comma. These are the grammar words we teach.
    "because": ("because", "потому что"),
    "so": ("so", "поэтому"),
    "but": ("but", "но"),
    "first": ("first", "сначала"),
    "then": ("then", "потом"),
    "next": ("next", "дальше"),
    "at_last": ("at last", "наконец"),
    "now": ("now", "теперь"),
    "why": ("why", "почему"),
    "which": ("which", "что"),
    "once_more": ("again", "опять"),
}
COMPS = {  # comparative forms of the adjectives (id = the ADJS id, so the pill colour and the sticker
    # are shared). Russian comparatives do not decline, so one form serves every slot.
    "heavy": ("heavier", "тяжелее"),
    "light": ("lighter", "легче"),
    "big": ("bigger", "больше"),
    "small": ("smaller", "меньше"),
    "long": ("longer", "длиннее"),
    "short": ("shorter", "короче"),
    "hot": ("hotter", "горячее"),
    "cold": ("colder", "холоднее"),
    "fast": ("faster", "быстрее"),
    "slow": ("slower", "медленнее"),
}
PHRASES = {  # fixed, curator-written, hand-aligned: (text, concept) per side. Word order may differ.
    "now_you_try": dict(
        en=[("Now", "now"), ("you", "you"), ("try", "try"), ("!", None)],
        ru=[("Теперь", "now"), ("попробуй", "try"), ("ты", "you"), ("!", None)],
    ),
    # Cover titles. A word with no concept ("or") has no highlight. A cover may use only concepts that
    # a page of the same book also uses.
    "title_sink_float": dict(
        en=[("Sink", "sink"), ("or", None), ("Float", "float"), ("?", None)],
        ru=[("Тонет", "sink"), ("или", None), ("плавает", "float"), ("?", None)],
    ),
    "title_hot_cold": dict(
        en=[("Hot", "hot"), ("or", None), ("Cold", "cold"), ("?", None)],
        ru=[("Горячо", "hot"), ("или", None), ("холодно", "cold"), ("?", None)],
    ),
    "title_heavy_light": dict(
        en=[("Heavy", "heavy"), ("or", None), ("Light", "light"), ("?", None)],
        ru=[("Тяжёлый", "heavy"), ("или", None), ("лёгкий", "light"), ("?", None)],
    ),
    "title_big_small": dict(
        en=[("Big", "big"), ("or", None), ("Small", "small"), ("?", None)],
        ru=[("Большой", "big"), ("или", None), ("маленький", "small"), ("?", None)],
    ),
    "title_soft_hard": dict(
        en=[("Soft", "soft"), ("or", None), ("Hard", "hard"), ("?", None)],
        ru=[("Мягкий", "soft"), ("или", None), ("твёрдый", "hard"), ("?", None)],
    ),
    "title_where_ball": dict(
        en=[("Where", "where"), ("Is", None), ("the", None), ("Ball", "ball"), ("?", None)],
        ru=[("Где", "where"), ("мячик", "ball"), ("?", None)],
    ),
    "title_colors": dict(
        en=[("Red", "red"), (",", None), ("Yellow", "yellow"), (",", None), ("Green", "green"), (",", None),
            ("Blue", "blue"), ("!", None)],
        ru=[("Красный", "red"), (",", None), ("жёлтый", "yellow"), (",", None), ("зелёный", "green"), (",", None),
            ("синий", "blue"), ("!", None)],
    ),
    "title_animal_sounds": dict(
        en=[("Animal", None), ("Sounds", None)],
        ru=[("Голоса", None), ("животных", None)],
    ),
    "title_weather": dict(
        en=[("Weather", None)],
        ru=[("Погода", None)],
    ),
    "title_seed_grows": dict(
        en=[("A", None), ("Seed", "seed"), ("Grows", "grow")],
        ru=[("Семечко", "seed"), ("растёт", "grow")],
    ),
    "title_ice_melts": dict(
        en=[("Ice", "ice"), ("Melts", "melt")],
        ru=[("Лёд", "ice"), ("тает", "melt")],
    ),
    # Folk-tale covers. "Kolobok" is a name, so both sides carry it. "Теремок" is the little house.
    "title_repka": dict(
        en=[("The", None), ("Turnip", "turnip")],
        ru=[("Репка", "turnip")],
    ),
    "title_kolobok": dict(
        en=[("Kolobok", "kolobok")],
        ru=[("Колобок", "kolobok")],
    ),
    "title_teremok": dict(
        en=[("The", None), ("Little", None), ("House", "house")],  # Теремок carries "little" in itself
        ru=[("Теремок", "house")],
    ),
    "title_hen": dict(
        en=[("The", None), ("Speckled", "speckled"), ("Hen", "hen")],
        ru=[("Курочка", "hen"), ("Ряба", "speckled")],
    ),
    # Lines of the canonical folk tales (books 12 to 15), in modern Russian. Word order may differ
    # between the languages; the curator aligns the pairs by hand.
    "once_upon": dict(  # Жили-были дед да баба -> modern дедушка и бабушка
        en=[("Once", None), ("upon", None), ("a", None), ("time", None), (",", None), ("there", None),
            ("lived", "live"), ("Grandpa", "grandpa"), ("and", None), ("Grandma", "grandma"), (".", None)],
        ru=[("Жили", "live"), ("-", None), ("были", "live"), ("дедушка", "grandpa"), ("и", None),
            ("бабушка", "grandma"), (".", None)],
    ),
    "once_hen": dict(  # И была у них курочка Ряба
        en=[("And", None), ("a", None), ("speckled", "speckled"), ("hen", "hen"), ("lived", "live"),
            ("with", None), ("them", None), (".", None)],
        ru=[("Жила", "live"), ("-", None), ("была", "live"), ("курочка", "hen"), ("Ряба", "speckled"),
            (".", None)],
    ),
    "repka_big": dict(  # Выросла репка большая-пребольшая: kept, it is expressive but not archaic
        en=[("The", None), ("turnip", "turnip"), ("grew", "grow"), ("big", "big"), (",", None),
            ("very", None), ("big", "big"), ("!", None)],
        ru=[("Выросла", "grow"), ("репка", "turnip"), ("большая", "big"), ("-", None),
            ("пребольшая", "big"), ("!", None)],
    ),
    "pull_fail_one": dict(  # one puller: Тянет-потянет, вытянуть не может
        en=[("He", None), ("pulls", "pull"), ("and", None), ("pulls", "pull"), (",", None),
            ("but", None), ("he", None), ("cannot", None), ("pull", "pull_out"), ("it", None),
            ("out", None), (".", None)],
        ru=[("Тянет", "pull"), ("-", None), ("потянет", "pull"), (",", None), ("вытянуть", "pull_out"),
            ("не", None), ("может", None), (".", None)],
    ),
    "pull_fail": dict(  # many pullers: Тянут-потянут, вытянуть не могут
        en=[("They", None), ("pull", "pull"), ("and", None), ("pull", "pull"), (",", None),
            ("but", None), ("they", None), ("cannot", None), ("pull", "pull_out"), ("it", None),
            ("out", None), (".", None)],
        ru=[("Тянут", "pull"), ("-", None), ("потянут", "pull"), (",", None), ("вытянуть", "pull_out"),
            ("не", None), ("могут", None), (".", None)],
    ),
    "pull_win": dict(  # the last time: тянут-потянут — вытянули репку!
        en=[("They", None), ("pulled", "pull"), ("and", None), ("pulled", "pull"), (",", None),
            ("and", None), ("pulled", "pull_out"), ("the", None), ("turnip", "turnip"), ("out", None),
            ("!", None)],
        ru=[("Тянут", "pull"), ("-", None), ("потянут", "pull"), ("—", None), ("вытянули", "pull_out"),
            ("репку", "turnip"), ("!", None)],
    ),
    "bake_one": dict(  # Испеки, баба, колобок -> modern: the request to bake, without the pantry words
        en=[("Bake", "bake"), ("a", None), ("bun", "kolobok"), ("!", None)],
        ru=[("Испеки", "bake"), ("колобок", "kolobok"), ("!", None)],
    ),
    "i_will_eat_you": dict(  # Колобок, колобок, я тебя съем!
        en=[("I", "I"), ("will", None), ("eat", "eat"), ("you", "you"), ("!", None)],
        ru=[("Я", "I"), ("тебя", "you"), ("съем", "eat"), ("!", None)],
    ),
    "song_hare": dict(  # the modern refrain every child sings; the pantry verses are dropped
        en=[("I", None), ("am", None), ("Kolobok", "kolobok"), ("!", None), ("I", None),
            ("left", "leave"), ("Grandpa", "grandpa"), (",", None), ("I", None), ("left", "leave"),
            ("Grandma", "grandma"), (",", None), ("and", None), ("I", None), ("will", None),
            ("leave", "leave"), ("you", "you"), (",", None), ("hare", "hare"), ("!", None)],
        ru=[("Я", None), ("колобок", "kolobok"), ("!", None), ("Я", None), ("от", None),
            ("дедушки", "grandpa"), ("ушёл", "leave"), (",", None), ("я", None), ("от", None),
            ("бабушки", "grandma"), ("ушёл", "leave"), (",", None), ("и", None), ("от", None),
            ("тебя", "you"), (",", None), ("заяц", "hare"), (",", None), ("уйду", "leave"), ("!", None)],
    ),
    "song_wolf": dict(
        en=[("I", None), ("am", None), ("Kolobok", "kolobok"), ("!", None), ("I", None),
            ("left", "leave"), ("Grandpa", "grandpa"), (",", None), ("I", None), ("left", "leave"),
            ("Grandma", "grandma"), (",", None), ("I", None), ("left", "leave"), ("the", None),
            ("hare", "hare"), (",", None), ("and", None), ("I", None), ("will", None),
            ("leave", "leave"), ("you", "you"), (",", None), ("wolf", "wolf"), ("!", None)],
        ru=[("Я", None), ("колобок", "kolobok"), ("!", None), ("Я", None), ("от", None),
            ("дедушки", "grandpa"), ("ушёл", "leave"), (",", None), ("я", None), ("от", None),
            ("бабушки", "grandma"), ("ушёл", "leave"), (",", None), ("я", None), ("от", None),
            ("зайца", "hare"), ("ушёл", "leave"), (",", None), ("и", None), ("от", None),
            ("тебя", "you"), (",", None), ("волк", "wolf"), (",", None), ("уйду", "leave"), ("!", None)],
    ),
    "song_bear": dict(
        en=[("I", None), ("am", None), ("Kolobok", "kolobok"), ("!", None), ("I", None),
            ("left", "leave"), ("Grandpa", "grandpa"), (",", None), ("I", None), ("left", "leave"),
            ("Grandma", "grandma"), (",", None), ("I", None), ("left", "leave"), ("the", None),
            ("hare", "hare"), (",", None), ("I", None), ("left", "leave"), ("the", None),
            ("wolf", "wolf"), (",", None), ("and", None), ("I", None), ("will", None),
            ("leave", "leave"), ("you", "you"), (",", None), ("bear", "bear"), ("!", None)],
        ru=[("Я", None), ("колобок", "kolobok"), ("!", None), ("Я", None), ("от", None),
            ("дедушки", "grandpa"), ("ушёл", "leave"), (",", None), ("я", None), ("от", None),
            ("бабушки", "grandma"), ("ушёл", "leave"), (",", None), ("я", None), ("от", None),
            ("зайца", "hare"), ("ушёл", "leave"), (",", None), ("я", None), ("от", None),
            ("волка", "wolf"), ("ушёл", "leave"), (",", None), ("и", None), ("от", None),
            ("тебя", "you"), (",", None), ("медведь", "bear"), (",", None), ("уйду", "leave"), ("!", None)],
    ),
    "and_who_are_you": dict(  # А ты кто?
        en=[("And", None), ("who", "who"), ("are", None), ("you", "you"), ("?", None)],
        ru=[("А", None), ("ты", "you"), ("кто", "who"), ("?", None)],
    ),
    "live_with_us": dict(  # the welcome of the house
        en=[("Come", None), ("and", None), ("live", "live"), ("with", None), ("us", "we"), ("!", None)],
        ru=[("Живи", "live"), ("с", None), ("нами", "we"), ("!", None)],
    ),
    "let_me_live": dict(  # the bear asks: Пустите меня к себе жить
        en=[("Let", None), ("me", "I"), ("live", "live"), ("with", None), ("you", "you"), ("!", None)],
        ru=[("Пустите", None), ("меня", "I"), ("жить", "live"), ("с", None), ("вами", "you"),
            ("!", None)],
    ),
    "not_plain_golden": dict(  # яичко не простое — золотое
        en=[("The", None), ("egg", "egg"), ("is", None), ("not", None), ("a", None),
            ("plain", "plain"), ("one", None), (",", None), ("it", None), ("is", None),
            ("golden", "golden"), ("!", None)],
        ru=[("Яйцо", "egg"), ("не", None), ("простое", "plain"), ("—", None), ("золотое", "golden"),
            ("!", None)],
    ),
    "beat_grandpa": dict(  # Дед бил-бил — не разбил
        en=[("Grandpa", "grandpa"), ("beat", "beat"), ("and", None), ("beat", "beat"), (",", None),
            ("but", None), ("he", None), ("did", None), ("not", None), ("break", "break"), ("it", None),
            (".", None)],
        ru=[("Дедушка", "grandpa"), ("бил", "beat"), ("-", None), ("бил", "beat"), ("—", None),
            ("не", None), ("разбил", "break"), (".", None)],
    ),
    "beat_grandma": dict(  # Баба била-била — не разбила
        en=[("Grandma", "grandma"), ("beat", "beat"), ("and", None), ("beat", "beat"), (",", None),
            ("but", None), ("she", None), ("did", None), ("not", None), ("break", "break"),
            ("it", None), (".", None)],
        ru=[("Бабушка", "grandma"), ("била", "beat"), ("-", None), ("била", "beat"), ("—", None),
            ("не", None), ("разбила", "break"), (".", None)],
    ),
    "dont_cry": dict(  # Не плачь, дед, не плачь, баба
        en=[("Do", None), ("not", None), ("cry", "cry"), (",", None), ("Grandpa", "grandpa"),
            ("and", None), ("Grandma", "grandma"), ("!", None)],
        ru=[("Не", None), ("плачьте", "cry"), (",", None), ("дедушка", "grandpa"), ("и", None),
            ("бабушка", "grandma"), ("!", None)],
    ),
    "i_will_lay_plain": dict(  # Снесу я вам яичко другое, не золотое — простое
        en=[("I", None), ("will", None), ("lay", "lay"), ("you", None), ("an", None), ("egg", "egg"),
            ("—", None), ("not", None), ("a", None), ("golden", "golden"), ("one", None), (",", None),
            ("a", None), ("plain", "plain"), ("one", None), ("!", None)],
        ru=[("Я", None), ("снесу", "lay"), ("вам", None), ("яйцо", "egg"), ("—", None), ("не", None),
            ("золотое", "golden"), (",", None), ("а", None), ("простое", "plain"), ("!", None)],
    ),
    # Song and rhyme lines (books 16 to 21). Sound words (хлоп, му-му) carry no concept: they are
    # not words to learn, they are the fun of the song.
    "title_happy_song": dict(
        en=[("Clap", "clap"), ("!", None), ("Stomp", "stomp"), ("!", None), ("Hooray", None), ("!", None)],
        ru=[("Хлоп", "clap"), ("!", None), ("Топ", "stomp"), ("!", None), ("Ура", None), ("!", None)],
    ),
    "happy_clap": dict(  # Если весело живёшь, хлопни в ладоши
        en=[("If", None), ("you", None), ("are", None), ("happy", "happy"), (",", None),
            ("clap", "clap"), ("your", None), ("hands", None), ("!", None)],
        ru=[("Если", None), ("весело", "happy"), (",", None), ("хлопни", "clap"), ("в", None),
            ("ладоши", None), ("!", None)],
    ),
    "happy_stomp": dict(
        en=[("If", None), ("you", None), ("are", None), ("happy", "happy"), (",", None),
            ("stomp", "stomp"), ("your", None), ("feet", None), ("!", None)],
        ru=[("Если", None), ("весело", "happy"), (",", None), ("топни", "stomp"), ("ножкой", None),
            ("!", None)],
    ),
    "happy_hooray": dict(
        en=[("If", None), ("you", None), ("are", None), ("happy", "happy"), (",", None),
            ("say", "say"), ("Hooray", None), ("!", None)],
        ru=[("Если", None), ("весело", "happy"), (",", None), ("скажи", "say"), ("Ура", None),
            ("!", None)],
    ),
    "clap_go": dict(
        en=[("Clap", "clap"), (",", None), ("clap", "clap"), (",", None), ("clap", "clap"), ("!", None)],
        ru=[("Хлоп", "clap"), (",", None), ("хлоп", "clap"), (",", None), ("хлоп", "clap"), ("!", None)],
    ),
    "stomp_go": dict(
        en=[("Stomp", "stomp"), (",", None), ("stomp", "stomp"), (",", None), ("stomp", "stomp"),
            ("!", None)],
        ru=[("Топ", "stomp"), (",", None), ("топ", "stomp"), (",", None), ("топ", "stomp"), ("!", None)],
    ),
    "hooray_go": dict(
        en=[("Hooray", None), ("!", None), ("Hooray", None), ("!", None)],
        ru=[("Ура", None), ("!", None), ("Ура", None), ("!", None)],
    ),
    "happy_all": dict(
        en=[("If", None), ("you", None), ("are", None), ("happy", "happy"), (",", None),
            ("do", None), ("it", None), ("all", None), ("!", None)],
        ru=[("Если", None), ("весело", "happy"), (",", None), ("делай", None), ("всё", None),
            ("!", None)],
    ),
    "title_rain_go": dict(
        en=[("Rain", "rain"), (",", None), ("Go", "leave"), ("Away", None), ("!", None)],
        ru=[("Дождик", "rain"), (",", None), ("уходи", "leave"), ("!", None)],
    ),
    "rain_go_away": dict(  # Дождик, дождик, перестань -> уходи matches "go away" word for word
        en=[("Rain", "rain"), (",", None), ("rain", "rain"), (",", None), ("go", "leave"),
            ("away", None), ("!", None)],
        ru=[("Дождик", "rain"), (",", None), ("дождик", "rain"), (",", None), ("уходи", "leave"),
            ("!", None)],
    ),
    "come_another_day": dict(
        en=[("Come", "come"), ("again", None), ("another", None), ("day", "day"), ("!", None)],
        ru=[("Приходи", "come"), ("в", None), ("другой", None), ("день", "day"), ("!", None)],
    ),
    "want_to_play": dict(
        en=[("We", "we"), ("want", None), ("to", None), ("play", "play"), ("!", None)],
        ru=[("Мы", "we"), ("хотим", None), ("играть", "play"), ("!", None)],
    ),
    "sun_comes_out": dict(
        en=[("The", None), ("sun", "sun"), ("comes", "come"), ("out", None), ("!", None)],
        ru=[("Вышло", "come"), ("солнце", "sun"), ("!", None)],
    ),
    "bye_rain": dict(
        en=[("Bye", None), ("-", None), ("bye", None), (",", None), ("rain", "rain"), ("!", None)],
        ru=[("Пока", None), (",", None), ("дождик", "rain"), ("!", None)],
    ),
    "title_spider": dict(
        en=[("The", None), ("Little", None), ("Spider", "spider")],
        ru=[("Паучок", "spider")],
    ),
    "up_the_pipe": dict(  # the waterspout chant
        en=[("Up", None), (",", None), ("up", None), (",", None), ("up", None), ("the", None),
            ("pipe", "pipe"), ("!", None)],
        ru=[("Вверх", None), (",", None), ("вверх", None), (",", None), ("по", None),
            ("трубе", "pipe"), ("!", None)],
    ),
    "rain_came": dict(
        en=[("Down", None), ("came", "fall"), ("the", None), ("rain", "rain"), ("!", None)],
        ru=[("Пошёл", "fall"), ("дождик", "rain"), ("!", None)],
    ),
    "up_pipe_again": dict(
        en=[("Up", None), (",", None), ("up", None), (",", None), ("up", None), ("the", None),
            ("pipe", "pipe"), ("again", None), ("!", None)],
        ru=[("Вверх", None), (",", None), ("вверх", None), (",", None), ("по", None),
            ("трубе", "pipe"), ("опять", None), ("!", None)],
    ),
    "spider_in_sun": dict(
        en=[("The", None), ("spider", "spider"), ("sits", "sit"), ("in", None), ("the", None),
            ("sun", "sun"), ("!", None)],
        ru=[("Паучок", "spider"), ("сидит", "sit"), ("на", None), ("солнышке", "sun"), ("!", None)],
    ),
    "title_star": dict(
        en=[("Little", None), ("Star", "star")],
        ru=[("Звёздочка", "star")],
    ),
    "twinkle_star": dict(
        en=[("Twinkle", "twinkle"), (",", None), ("twinkle", "twinkle"), (",", None),
            ("little", None), ("star", "star"), ("!", None)],
        ru=[("Мерцай", "twinkle"), (",", None), ("мерцай", "twinkle"), (",", None),
            ("звёздочка", "star"), ("!", None)],
    ),
    "high_in_sky": dict(
        en=[("High", None), ("above", None), ("us", None), ("in", None), ("the", None),
            ("sky", "sky"), ("!", None)],
        ru=[("Высоко", None), ("в", None), ("небе", "sky"), ("!", None)],
    ),
    "star_wants_sleep": dict(
        en=[("The", None), ("star", "star"), ("wants", None), ("to", None), ("sleep", "sleep"),
            ("!", None)],
        ru=[("Звёздочка", "star"), ("хочет", None), ("спать", "sleep"), ("!", None)],
    ),
    "sleep_star": dict(
        en=[("Sleep", "sleep"), (",", None), ("little", None), ("star", "star"), ("!", None)],
        ru=[("Спи", "sleep"), (",", None), ("звёздочка", "star"), ("!", None)],
    ),
    "good_night": dict(
        en=[("Good", None), ("night", None), ("!", None)],
        ru=[("Спокойной", None), ("ночи", None), ("!", None)],
    ),
    "we_sleep_too": dict(
        en=[("We", "we"), ("sleep", "sleep"), ("too", None), ("!", None)],
        ru=[("Мы", "we"), ("тоже", None), ("спим", "sleep"), ("!", None)],
    ),
    "title_body": dict(
        en=[("Head", "head"), ("and", None), ("Shoulders", "shoulder")],
        ru=[("Голова", "head"), ("и", None), ("плечи", "shoulder")],
    ),
    "head_shoulders": dict(
        en=[("Head", "head"), ("and", None), ("shoulders", "shoulder"), ("!", None)],
        ru=[("Голова", "head"), ("и", None), ("плечи", "shoulder"), ("!", None)],
    ),
    "knees_toes": dict(
        en=[("Knees", "knee"), ("and", None), ("toes", "toe"), ("!", None)],
        ru=[("Колени", "knee"), ("и", None), ("пальчики", "toe"), ("!", None)],
    ),
    "eyes_ears": dict(
        en=[("Eyes", "eye"), ("and", None), ("ears", "ear"), ("!", None)],
        ru=[("Глаза", "eye"), ("и", None), ("уши", "ear"), ("!", None)],
    ),
    "mouth_nose": dict(
        en=[("Mouth", "mouth"), ("and", None), ("nose", "nose"), ("!", None)],
        ru=[("Рот", "mouth"), ("и", None), ("нос", "nose"), ("!", None)],
    ),
    "chant_body": dict(  # the full chant of Head, Shoulders, Knees and Toes
        en=[("Head", "head"), (",", None), ("shoulders", "shoulder"), (",", None),
            ("knees", "knee"), ("and", None), ("toes", "toe"), ("!", None)],
        ru=[("Голова", "head"), (",", None), ("плечи", "shoulder"), (",", None),
            ("колени", "knee"), ("и", None), ("пальчики", "toe"), ("!", None)],
    ),
    "there_it_is": dict(
        en=[("There", None), ("it", None), ("is", None), ("!", None)],
        ru=[("Вот", None), ("он", None), ("!", None)],
    ),
    "title_farm": dict(
        en=[("On", None), ("the", None), ("Farm", "farm")],
        ru=[("На", None), ("ферме", "farm")],
    ),
    "grandpa_farm": dict(  # У дедушки есть ферма
        en=[("Grandpa", "grandpa"), ("has", None), ("a", None), ("farm", "farm"), ("!", None)],
        ru=[("У", None), ("дедушки", "grandpa"), ("есть", None), ("ферма", "farm"), ("!", None)],
    ),
    "says_cow": dict(
        en=[("The", None), ("cow", "cow"), ("says", "say"), (":", None), ("moo", "moo"), ("-", None),
            ("moo", "moo"), ("!", None)],
        ru=[("Корова", "cow"), ("говорит", "say"), (":", None), ("му", "moo"), ("-", None),
            ("му", "moo"), ("!", None)],
    ),
    "says_pig": dict(
        en=[("The", None), ("pig", "pig"), ("says", "say"), (":", None), ("oink", "oink"), ("-", None),
            ("oink", "oink"), ("!", None)],
        ru=[("Свинья", "pig"), ("говорит", "say"), (":", None), ("хрю", "oink"), ("-", None),
            ("хрю", "oink"), ("!", None)],
    ),
    "says_duck": dict(
        en=[("The", None), ("duck", "duck"), ("says", "say"), (":", None), ("quack", "quack"),
            ("-", None), ("quack", "quack"), ("!", None)],
        ru=[("Утка", "duck"), ("говорит", "say"), (":", None), ("кря", "quack"), ("-", None),
            ("кря", "quack"), ("!", None)],
    ),
    "says_dog": dict(
        en=[("The", None), ("dog", "dog"), ("says", "say"), (":", None), ("woof", "bark"), ("-", None),
            ("woof", "bark"), ("!", None)],
        ru=[("Собака", "dog"), ("говорит", "say"), (":", None), ("гав", "bark"), ("-", None),
            ("гав", "bark"), ("!", None)],
    ),
    "refrain_farm_1": dict(  # Moo-moo here, oink-oink there
        en=[("Moo", None), ("-", None), ("moo", None), ("here", None), (",", None), ("oink", None),
            ("-", None), ("oink", None), ("there", None), ("!", None)],
        ru=[("Му", None), ("-", None), ("му", None), ("тут", None), (",", None), ("хрю", None),
            ("-", None), ("хрю", None), ("там", None), ("!", None)],
    ),
    "refrain_farm_2": dict(
        en=[("Quack", None), ("-", None), ("quack", None), ("here", None), (",", None),
            ("woof", None), ("-", None), ("woof", None), ("there", None), ("!", None)],
        ru=[("Кря", None), ("-", None), ("кря", None), ("тут", None), (",", None), ("гав", None),
            ("-", None), ("гав", None), ("там", None), ("!", None)],
    ),
    "farm_finale": dict(
        en=[("All", None), ("the", None), ("animals", None), ("sing", "sing"),
            ("together", "together"), ("!", None)],
        ru=[("Все", None), ("поют", "sing"), ("вместе", "together"), ("!", None)],
    ),
    # The counting book (22). Numerals live in phrases only: Russian numerals govern the noun's
    # case (два глаза, пять пальчиков, восемь планет), and the curator aligns each pair by hand.
    "title_count": dict(
        en=[("Count", "count"), ("With", None), ("Me", None), ("!", None)],
        ru=[("Считай", "count"), ("со", None), ("мной", None), ("!", None)],
    ),
    "lets_count": dict(
        en=[("Let", None), ("us", None), ("count", "count"), ("!", None)],
        ru=[("Давай", None), ("считать", "count"), ("!", None)],
    ),
    "one_nose": dict(
        en=[("One", "one"), ("nose", "nose"), ("!", None)],
        ru=[("Один", "one"), ("нос", "nose"), ("!", None)],
    ),
    "two_eyes": dict(
        en=[("Two", "two"), ("eyes", "eye"), ("!", None)],
        ru=[("Два", "two"), ("глаза", "eye"), ("!", None)],
    ),
    "two_ears": dict(
        en=[("Two", "two"), ("ears", "ear"), ("listen", "listen"), ("!", None)],
        ru=[("Два", "two"), ("уха", "ear"), ("слушают", "listen"), ("!", None)],
    ),
    "five_fingers": dict(
        en=[("Five", "five"), ("fingers", "finger"), ("on", None), ("one", "one"),
            ("hand", None), ("!", None)],
        ru=[("Пять", "five"), ("пальчиков", "finger"), ("на", None), ("одной", "one"),
            ("руке", None), ("!", None)],
    ),
    "ten_toes": dict(
        en=[("Ten", "ten"), ("toes", "toe"), ("on", None), ("two", "two"), ("feet", None),
            ("!", None)],
        ru=[("Десять", "ten"), ("пальчиков", "toe"), ("на", None), ("двух", "two"),
            ("ногах", None), ("!", None)],
    ),
    "count_chant": dict(  # the counting chant, one to five
        en=[("One", "one"), (",", None), ("two", "two"), (",", None), ("three", "three"),
            (",", None), ("four", "four"), (",", None), ("five", "five"), ("!", None)],
        ru=[("Один", "one"), (",", None), ("два", "two"), (",", None), ("три", "three"),
            (",", None), ("четыре", "four"), (",", None), ("пять", "five"), ("!", None)],
    ),
    "one_sun": dict(
        en=[("One", "one"), ("sun", "sun"), ("in", None), ("the", None), ("sky", "sky"), ("!", None)],
        ru=[("Одно", "one"), ("солнце", "sun"), ("в", None), ("небе", "sky"), ("!", None)],
    ),
    "eight_planets": dict(
        en=[("Eight", "eight"), ("planets", "planet"), ("go", None), ("around", None),
            ("the", None), ("sun", "sun"), ("!", None)],
        ru=[("Восемь", "eight"), ("планет", "planet"), ("вокруг", None), ("солнца", "sun"),
            ("!", None)],
    ),
    "on_earth": dict(
        en=[("We", "we"), ("live", "live"), ("on", None), ("planet", "planet"),
            ("Earth", "earth"), ("!", None)],
        ru=[("Мы", "we"), ("живём", "live"), ("на", None), ("планете", "planet"),
            ("Земле", "earth"), ("!", None)],
    ),
    "many_stars": dict(
        en=[("And", None), ("so", None), ("many", None), ("stars", "star"), ("!", None)],
        ru=[("И", None), ("очень", None), ("много", None), ("звёзд", "star"), ("!", None)],
    ),
    "count_again": dict(
        en=[("Count", "count"), ("with", None), ("me", None), ("again", "again"), ("!", None)],
        ru=[("Считай", "count"), ("со", None), ("мной", None), ("опять", "again"), ("!", None)],
    ),
    # the older-kids books (23 to 37): cover titles first
    "title_why_sink": dict(
        en=[("Why", None), ("does", None), ("it", None), ("sink", "sink"), ("?", None)],
        ru=[("Почему", None), ("оно", None), ("тонет", "sink"), ("?", None)],
    ),
    "title_guess_first": dict(
        en=[("Guess", "guess"), ("first", "first"), ("!", None)],
        ru=[("Сначала", "first"), ("угадай", "guess"), ("!", None)],
    ),
    "title_in_out": dict(
        en=[("In", "in"), ("and", None), ("out", None), ("!", None)],
        ru=[("Внутри", "in"), ("и", None), ("снаружи", None), ("!", None)],
    ),
    "title_babies": dict(
        en=[("Animal", None), ("babies", None), ("!", None)],
        ru=[("Детки", None), ("животных", None), ("!", None)],
    ),
    "title_on_purpose": dict(
        en=[("On", None), ("purpose", None), ("!", None)],
        ru=[("Нарочно", None), ("!", None)],
    ),
    "title_melting_race": dict(
        en=[("The", None), ("melting", "melt"), ("race", None), ("!", None)],
        ru=[("Гонка", None), ("таяния", "melt"), ("!", None)],
    ),
    "title_heavier": dict(
        en=[("Which", None), ("is", None), ("heavier", "heavy"), ("?", None)],
        ru=[("Что", None), ("тяжелее", "heavy"), ("?", None)],
    ),
    "title_big_test": dict(
        en=[("Sink", "sink"), ("or", None), ("float", "float"), (":", None), ("the", None),
            ("big", None), ("test", None), ("!", None)],
        ru=[("Тонет", "sink"), ("или", None), ("плавает", "float"), (":", None), ("большой", None),
            ("тест", None), ("!", None)],
    ),
    "title_shadows": dict(
        en=[("Shadows", "shadow"), ("!", None)],
        ru=[("Тени", "shadow"), ("!", None)],
    ),
    "title_seed_year": dict(
        en=[("A", None), ("seed", "seed"), ("grows", "grow"), ("all", None), ("year", None),
            ("long", None), ("!", None)],
        ru=[("Семечко", "seed"), ("растёт", "grow"), ("весь", None), ("год", None), ("!", None)],
    ),
    "title_day_night": dict(
        en=[("Day", "day"), ("and", None), ("night", "night"), ("!", None)],
        ru=[("День", "day"), ("и", None), ("ночь", "night"), ("!", None)],
    ),
    "title_orange_test": dict(
        en=[("The", None), ("orange", "orange"), ("test", None), ("!", None)],
        ru=[("Тест", None), ("с", None), ("апельсином", "orange"), ("!", None)],
    ),
    "title_water": dict(
        en=[("What", None), ("is", None), ("water", "water"), ("?", None)],
        ru=[("Что", None), ("такое", None), ("вода", "water"), ("?", None)],
    ),
    "title_count_farther": dict(
        en=[("Count", "count"), ("farther", None), ("!", None)],
        ru=[("Считаем", "count"), ("дальше", None), ("!", None)],
    ),
    "title_senses": dict(
        en=[("The", None), ("five", "five"), ("senses", None), ("test", None), ("!", None)],
        ru=[("Тест", None), ("пяти", "five"), ("чувств", None), ("!", None)],
    ),
    # numerals eleven to twenty: fixed phrases, like one to ten in book 22
    "eleven": dict(en=[("Eleven", "eleven")], ru=[("Одиннадцать", "eleven")]),
    "twelve": dict(en=[("Twelve", "twelve")], ru=[("Двенадцать", "twelve")]),
    "thirteen": dict(en=[("Thirteen", "thirteen")], ru=[("Тринадцать", "thirteen")]),
    "fourteen": dict(en=[("Fourteen", "fourteen")], ru=[("Четырнадцать", "fourteen")]),
    "fifteen": dict(en=[("Fifteen", "fifteen")], ru=[("Пятнадцать", "fifteen")]),
    "sixteen": dict(en=[("Sixteen", "sixteen")], ru=[("Шестнадцать", "sixteen")]),
    "seventeen": dict(en=[("Seventeen", "seventeen")], ru=[("Семнадцать", "seventeen")]),
    "eighteen": dict(en=[("Eighteen", "eighteen")], ru=[("Восемнадцать", "eighteen")]),
    "nineteen": dict(en=[("Nineteen", "nineteen")], ru=[("Девятнадцать", "nineteen")]),
    "twenty": dict(en=[("Twenty", "twenty")], ru=[("Двадцать", "twenty")]),
    "fives_chant": dict(
        en=[("Five", "five"), (",", None), ("ten", "ten"), (",", None), ("fifteen", "fifteen"),
            (",", None), ("twenty", "twenty"), ("!", None)],
        ru=[("Пять", "five"), (",", None), ("десять", "ten"), (",", None), ("пятнадцать", "fifteen"),
            (",", None), ("двадцать", "twenty"), ("!", None)],
    ),
    # the seasons open their pages: It is winter. / Зима.
    "it_winter": dict(en=[("It", None), ("is", None), ("winter", "winter"), (".", None)],
                      ru=[("Зима", "winter"), (".", None)]),
    "it_spring": dict(en=[("It", None), ("is", None), ("spring", "spring"), (".", None)],
                      ru=[("Весна", "spring"), (".", None)]),
    "it_summer": dict(en=[("It", None), ("is", None), ("summer", "summer"), (".", None)],
                      ru=[("Лето", "summer"), (".", None)]),
    "it_autumn": dict(en=[("It", None), ("is", None), ("autumn", "autumn"), (".", None)],
                      ru=[("Осень", "autumn"), (".", None)]),
    "day_and_night": dict(  # ... there is day and night = ... бывает день и ночь
        en=[("there", None), ("is", None), ("day", "day"), ("and", None), ("night", "night"),
            (".", None)],
        ru=[("бывает", None), ("день", "day"), ("и", None), ("ночь", "night"), (".", None)],
    ),
    "shadow_runs": dict(  # the shadow runs after me = тень бежит за мной
        en=[("The", None), ("shadow", "shadow"), ("runs", "run"), ("after", None),
            ("me", "me"), (".", None)],
        ru=[("Тень", "shadow"), ("бежит", "run"), ("за", None), ("мной", "me"), (".", None)],
    ),
    "no_shadow": dict(  # a cloud comes: no shadow! = приходит облако: нет тени!
        en=[("No", None), ("shadow", "shadow"), ("!", None)],
        ru=[("Нет", None), ("тени", "shadow"), ("!", None)],
    ),
    "chart_look": dict(  # the results chart page: Look: our guesses and what we saw
        en=[("Look", "look"), (":", None), ("our", None), ("guesses", "guess"),
            ("and", None), ("what", None), ("we", None), ("saw", "see"), ("!", None)],
        ru=[("Смотри", "look"), (":", None), ("мы", None), ("угадали", "guess"),
            ("и", None), ("что", None), ("мы", None), ("увидели", "see"), ("!", None)],
    ),
    "close_eyes": dict(  # the blindfold test: we close our eyes = мы закрываем глаза
        en=[("We", "we"), ("close", "close"), ("our", None), ("eyes", "eye"), (".", None)],
        ru=[("Мы", "we"), ("закрываем", "close"), ("глаза", "eye"), (".", None)],
    ),
    "open_eyes": dict(
        en=[("We", "we"), ("open", "open"), ("our", None), ("eyes", "eye"), ("!", None)],
        ru=[("Мы", "we"), ("открываем", "open"), ("глаза", "eye"), ("!", None)],
    ),
    "what_is_it": dict(
        en=[("What", None), ("is", None), ("it", None), ("?", None)],
        ru=[("Что", None), ("это", None), ("?", None)],
    ),
    "zero_degrees": dict(  # zero degrees: water becomes ice = ноль градусов: вода становится льдом
        en=[("Zero", None), ("degrees", None), ("!", None)],
        ru=[("Ноль", None), ("градусов", None), ("!", None)],
    ),
    "water_back": dict(  # the ice melts: the water comes back = лёд тает: вода возвращается
        en=[("The", None), ("water", "water"), ("comes", "come"), ("back", None), ("!", None)],
        ru=[("Вода", "water"), ("возвращается", "come"), ("!", None)],
    ),
    "hot_water": dict(  # hot water: the sun makes steam? no: boiling for the states of water
        en=[("Hot", "hot"), ("water", "water"), ("!", None)],
        ru=[("Горячая", "hot"), ("вода", "water"), ("!", None)],
    ),
    # books 23 to 37: page phrases
    "in_the_sun": dict(  # we put the ice in the sun = мы кладём лёд на солнце (на = in the sunlight)
        en=[("We", "we"), ("put", "put"), ("the", None), ("ice", "ice"), ("in", None),
            ("sun", "sun"), (".", None)],
        ru=[("Мы", "we"), ("кладём", "put"), ("лёд", "ice"), ("на", None),
            ("солнце", "sun"), (".", None)],
    ),
    "it_day": dict(en=[("It", None), ("is", None), ("day", "day"), (".", None)],
                   ru=[("День", "day"), (".", None)]),
    "it_night": dict(en=[("It", None), ("is", None), ("night", "night"), (".", None)],
                     ru=[("Ночь", "night"), (".", None)]),
    "it_morning": dict(en=[("It", None), ("is", None), ("morning", "morning"), (".", None)],
                       ru=[("Утро", "morning"), (".", None)]),
    "day_again": dict(en=[("It", None), ("is", None), ("day", "day"), ("again", "once_more"),
                          (".", None)],
                      ru=[("Опять", "once_more"), ("день", "day"), (".", None)]),
    "winter_again": dict(en=[("It", None), ("is", None), ("winter", "winter"), ("again", "once_more"),
                             (".", None)],
                         ru=[("Опять", "once_more"), ("зима", "winter"), (".", None)]),
    "shadow_back": dict(en=[("The", None), ("shadow", "shadow"), ("comes", "come"), ("back", None),
                            ("!", None)],
                        ru=[("Тень", "shadow"), ("возвращается", "come"), ("!", None)]),
    "it_all_water": dict(en=[("It", None), ("is", None), ("all", None), ("water", "water"),
                             ("!", None)],
                         ru=[("Это", None), ("всё", None), ("вода", "water"), ("!", None)]),
    "how_many_stars": dict(en=[("How", None), ("many", None), ("stars", "star"), ("?", None)],
                           ru=[("Сколько", None), ("звёзд", "star"), ("?", None)]),
    "count_twenty": dict(en=[("We", "we"), ("count", "count"), ("to", None), ("twenty", "twenty"),
                             ("!", None)],
                         ru=[("Мы", "we"), ("считаем", "count"), ("до", None), ("двадцати", "twenty"),
                             ("!", None)]),
    "five_senses": dict(en=[("We", None), ("have", None), ("five", "five"), ("senses", "sense"),
                            ("!", None)],
                        ru=[("У", None), ("нас", None), ("пять", "five"), ("чувств", "sense"),
                            ("!", None)]),
    "its_teddy": dict(en=[("It", None), ("is", None), ("the", None), ("teddy", "teddy"),
                          ("bear", None), ("!", None)],
                      ru=[("Это", None), ("мишка", "teddy"), ("!", None)]),
    "its_flower": dict(en=[("It", None), ("is", None), ("the", None), ("flower", "flower"),
                           ("!", None)],
                       ru=[("Это", None), ("цветок", "flower"), ("!", None)]),
    "eleven_stars": dict(en=[("Eleven", "eleven"), ("stars", "star"), ("!", None)],
                         ru=[("Одиннадцать", "eleven"), ("звёзд", "star"), ("!", None)]),
    "twelve_blocks": dict(en=[("Twelve", "twelve"), ("blocks", "block"), ("!", None)],
                          ru=[("Двенадцать", "twelve"), ("кубиков", "block"), ("!", None)]),
    "thirteen_leaves": dict(en=[("Thirteen", "thirteen"), ("leaves", "leaf"), ("!", None)],
                            ru=[("Тринадцать", "thirteen"), ("листьев", "leaf"), ("!", None)]),
    "fourteen_flowers": dict(en=[("Fourteen", "fourteen"), ("flowers", "flower"), ("!", None)],
                             ru=[("Четырнадцать", "fourteen"), ("цветов", "flower"), ("!", None)]),
    "fifteen_apples": dict(en=[("Fifteen", "fifteen"), ("apples", "apple"), ("!", None)],
                           ru=[("Пятнадцать", "fifteen"), ("яблок", "apple"), ("!", None)]),
    "sixteen_ducks": dict(en=[("Sixteen", "sixteen"), ("ducks", "duck"), ("!", None)],
                          ru=[("Шестнадцать", "sixteen"), ("уток", "duck"), ("!", None)]),
    "seventeen_stones": dict(en=[("Seventeen", "seventeen"), ("stones", "stone"), ("!", None)],
                             ru=[("Семнадцать", "seventeen"), ("камней", "stone"), ("!", None)]),
    "eighteen_clouds": dict(en=[("Eighteen", "eighteen"), ("clouds", "cloud"), ("!", None)],
                            ru=[("Восемнадцать", "eighteen"), ("облаков", "cloud"), ("!", None)]),
    "nineteen_balloons": dict(en=[("Nineteen", "nineteen"), ("balloons", "balloon"), ("!", None)],
                              ru=[("Девятнадцать", "nineteen"), ("шариков", "balloon"), ("!", None)]),
    "twenty_fingers": dict(en=[("Twenty", "twenty"), ("fingers", "finger"), ("on", None),
                               ("hands", "hand"), ("and", None), ("feet", "toe"), ("!", None)],
                           ru=[("Двадцать", "twenty"), ("пальчиков", "finger"), ("на", None),
                               ("руках", "hand"), ("и", None), ("ногах", "toe"), ("!", None)]),
    "i_know": dict(
        en=[("Now", None), ("we", "we"), ("know", "know"), ("!", None)],
        ru=[("Теперь", None), ("мы", "we"), ("знаем", "know"), ("!", None)],
    ),
}
OVERRIDES = {  # (RU lemma, grammemes) -> the one form the curator chose among several valid ones
    ("лист", frozenset({"plur", "nomn"})): "листья",  # leaves, not листы (sheets)
    ("цветок", frozenset({"plur", "nomn"})): "цветы",  # flowers, not цветки (botanical parts)
    ("цветок", frozenset({"plur", "accs"})): "цветы",
    ("ветер", frozenset({"sing", "nomn"})): "ветер",  # not the poetic ветр
}
CHROME = {  # page furniture, not story text. Curator-written and hand-aligned like PHRASES.
    "counter": dict(
        en=[("{n}", "n"), ("out of", "of"), ("{total}", "total")],
        ru=[("{n}", "n"), ("из", "of"), ("{total}", "total")],
    ),
}


def _en(pres_sg, past, pres_pl=None, past_pl=None):
    return {"pres_sg": pres_sg, "past_sg": past, "pres_pl": pres_pl or pres_sg, "past_pl": past_pl or past}


VERBS = {  # a key is the aspect-correct Russian lemma the curator chose for that use. A missing key is refused.
    # ru_pres = present tense, ru_past = past, ru_futr = future ("will ..."), ru_impr = command to one child
    "see": dict(en=_en("sees", "saw", "see"), ru_pres="видеть", ru_past="увидеть", ru_futr="увидеть"),
    "look": dict(en=_en("looks", "looked", "look"), ru_pres="смотреть", ru_past="посмотреть",
                 ru_futr="посмотреть", ru_impr="посмотреть"),
    "kick": dict(en=_en("kicks", "kicked", "kick"), ru_pres="пинать", ru_past="пнуть"),
    "give": dict(en=_en("gives", "gave", "give"), ru_pres="давать", ru_past="дать", io="to"),
    "play": dict(en=_en("plays", "played", "play"), ru_pres="играть", ru_past="играть"),
    "sit": dict(en=_en("sits", "sat", "sit"), ru_pres="сидеть", ru_past="сесть"),  # sat down: сел
    "sink": dict(en=_en("sinks", "sank", "sink"), ru_pres="тонуть", ru_past="утонуть", ru_futr="утонуть"),
    "float": dict(en=_en("floats", "floated", "float"), ru_pres="плавать", ru_past="плавать",
                  ru_futr="поплыть"),
    "be_sad": dict(en=_en("is sad", "was sad", "are sad", "were sad"), ru_pres="грустить",
                   ru_past="грустить", third_only=True),
    "be_happy": dict(en=_en("is happy", "was happy", "are happy", "were happy"), ru_pres="радоваться",
                     ru_past="радоваться", third_only=True),
    # copula: English "is/was", Russian present tense has no verb at all
    "be": dict(en=_en("is", "was", "are", "were"), ru_pres=None, ru_past="быть", third_only=True),
    "touch": dict(en=_en("touches", "touched", "touch"), ru_pres="трогать", ru_impr="потрогать"),
    "listen": dict(en=_en("listens", "listened", "listen"), ru_pres="слушать"),
    "wait": dict(en=_en("waits", "waited", "wait"), ru_pres="ждать"),
    "put": dict(en=_en("puts", "put", "put"), ru_pres="класть", ru_past="положить",
                ru_impr="положить"),
    "bark": dict(en=_en("barks", "barked", "bark"), ru_pres="лаять", ru_past="залаять"),
    "meow": dict(en=_en("meows", "meowed", "meow"), ru_pres="мяукать", ru_past="замяукать"),
    "moo": dict(en=_en("moos", "mooed", "moo"), ru_pres="мычать"),
    "quack": dict(en=_en("quacks", "quacked", "quack"), ru_pres="крякать"),
    "shine": dict(en=_en("shines", "shone", "shine"), ru_pres="светить"),
    "fall": dict(en=_en("falls", "fell", "fall"), ru_pres="идти"),  # rain and snow "go" in Russian
    "blow": dict(en=_en("blows", "blew", "blow"), ru_pres="дуть"),
    "grow": dict(en=_en("grows", "grew", "grow"), ru_pres="расти", ru_past="вырасти"),
    "melt": dict(en=_en("melts", "melted", "melt"), ru_pres="таять"),
    # folk-tale verbs (books 12 to 15). "plant" is a noun in the lexicon, so to plant takes the id "sow".
    "sow": dict(en=_en("plants", "planted", "plant"), ru_pres="сажать", ru_past="посадить",
                ru_futr="посадить"),
    "pull": dict(en=_en("pulls", "pulled", "pull"), ru_pres="тянуть", ru_past="тянуть",
                 ru_futr="потянуть"),
    "come": dict(en=_en("comes", "came", "come"), ru_pres="приходить", ru_past="прийти", ru_futr="прийти"),
    "eat": dict(en=_en("eats", "ate", "eat"), ru_pres="есть", ru_past="съесть", ru_futr="съесть",
                ru_impr="съесть"),
    "bake": dict(en=_en("bakes", "baked", "bake"), ru_pres="печь", ru_past="испечь", ru_futr="испечь",
                 ru_impr="испечь"),
    "roll": dict(en=_en("rolls", "rolled", "roll"), ru_pres="катиться", ru_past="покатиться"),
    "meet": dict(en=_en("meets", "met", "meet"), ru_pres="встречать", ru_past="встретить",
                 ru_futr="встретить"),
    "live": dict(en=_en("lives", "lived", "live"), ru_pres="жить", ru_past="жить"),
    "break": dict(en=_en("breaks", "broke", "break"), ru_pres="разбиваться", ru_past="разбиться"),  # an egg shatters
    "walk": dict(en=_en("walks", "walked", "walk"), ru_pres="идти", ru_past="идти"),  # идёт, шёл: a tale arrival
    "run": dict(en=_en("runs", "ran", "run"), ru_pres="бегать", ru_past="побежать"),
    "cry": dict(en=_en("cries", "cried", "cry"), ru_pres="плакать", ru_past="заплакать",
                ru_futr="заплакать"),
    "lay": dict(en=_en("lays", "laid", "lay"), ru_pres="нести", ru_past="снести", ru_futr="снести"),
    "build": dict(en=_en("builds", "built", "build"), ru_pres="строить", ru_past="построить",
                  ru_futr="построить"),
    # "fall" is rain and snow (идти); this one is a thing dropping (падать)
    "tumble": dict(en=_en("falls", "fell", "fall"), ru_pres="падать", ru_past="упасть",
                   ru_futr="упасть"),
    # more fun for the folk tales: Kolobok's song, the frog's hop, the happy ending
    "sing": dict(en=_en("sings", "sang", "sing"), ru_pres="петь", ru_past="петь", ru_impr="спеть"),
    "jump": dict(en=_en("jumps", "jumped", "jump"), ru_pres="прыгать", ru_past="прыгнуть"),
    # the canonical tale texts (books 12 to 15)
    "call": dict(en=_en("calls", "called", "call"), ru_pres="звать", ru_past="позвать"),
    "hold": dict(en=_en("holds", "held", "hold"), ru_pres="держаться", ru_past="держаться"),
    "pull_out": dict(en=_en("pulls out", "pulled out", "pull out"), ru_pres="вытягивать",
                     ru_past="вытянуть"),
    "leave": dict(en=_en("leaves", "left", "leave"), ru_pres="уходить", ru_past="уйти",
                  ru_futr="уйти"),
    "say": dict(en=_en("says", "said", "say"), ru_pres="говорить", ru_past="сказать"),
    "answer": dict(en=_en("answers", "answered", "answer"), ru_pres="отвечать", ru_past="ответить"),
    "cool": dict(en=_en("cools", "cooled", "cool"), ru_pres="остывать", ru_past="остыть"),
    "stand": dict(en=_en("stands", "stood", "stand"), ru_pres="стоять", ru_past="стоять"),
    "climb": dict(en=_en("climbs", "climbed", "climb"), ru_pres="лезть", ru_past="полезть"),
    "fall_apart": dict(en=_en("falls apart", "fell apart", "fall apart"), ru_pres="разваливаться",
                       ru_past="развалиться"),
    "wave": dict(en=_en("waves", "waved", "wave"), ru_pres="махать", ru_past="махнуть"),
    "beat": dict(en=_en("beats", "beat", "beat"), ru_pres="бить", ru_past="бить"),
    # song and rhyme books (16 to 21)
    "clap": dict(en=_en("claps", "clapped", "clap"), ru_pres="хлопать", ru_past="хлопнуть",
                 ru_impr="хлопнуть"),
    "stomp": dict(en=_en("stomps", "stomped", "stomp"), ru_pres="топать", ru_past="топнуть",
                  ru_impr="топнуть"),
    "wash_out": dict(en=_en("washes out", "washed out", "wash out"), ru_pres="смывать",
                     ru_past="смыть"),
    "dry": dict(en=_en("dries", "dried", "dry"), ru_pres="сушить", ru_past="высушить"),
    "twinkle": dict(en=_en("twinkles", "twinkled", "twinkle"), ru_pres="мерцать", ru_impr="мерцать"),
    "sleep": dict(en=_en("sleeps", "slept", "sleep"), ru_pres="спать", ru_impr="спать"),
    "oink": dict(en=_en("oinks", "oinked", "oink"), ru_pres="хрюкать", ru_past="хрюкнуть"),
    "count": dict(en=_en("counts", "counted", "count"), ru_pres="считать", ru_past="считать",
                  ru_impr="считать"),
    # the older-kids books (23 to 37)
    "guess": dict(en=_en("guesses", "guessed", "guess"), ru_pres="угадывать", ru_past="угадать",
                  ru_futr="угадать", ru_impr="угадать"),
    "peel_off": dict(en=_en("peels", "peeled", "peel"), ru_pres="чистить", ru_impr="почистить"),
    "rise": dict(en=_en("rises", "rose", "rise"), ru_pres="подниматься", third_only=True),
    "make": dict(en=_en("makes", "made", "make"), ru_pres="делать", ru_past="сделать"),
    "become": dict(en=_en("becomes", "became", "become"), ru_pres="становиться",
                   ru_past="стать", instr_join=""),
    "turn": dict(en=_en("turns", "turned", "turn"), ru_pres="вертеться", third_only=True),
    "take": dict(en=_en("takes", "took", "take"), ru_pres="доставать", ru_past="достать"),
    "close": dict(en=_en("closes", "closed", "close"), ru_pres="закрывать", ru_past="закрыть"),
    "open": dict(en=_en("opens", "opened", "open"), ru_pres="открывать", ru_past="открыть"),
    "smell": dict(en=_en("smells", "smelled", "smell"), ru_pres="нюхать", ru_impr="понюхать"),
    "know": dict(en=_en("knows", "knew", "know"), ru_pres="знать"),
    "wake": dict(en=_en("wakes", "woke", "wake"), ru_pres="просыпаться"),
    "freeze": dict(en=_en("freezes", "froze", "freeze"), ru_pres="замерзать", third_only=True),
    "boil": dict(en=_en("boils", "boiled", "boil"), ru_pres="кипеть", third_only=True),
    "hide": dict(en=_en("hides", "hid", "hide"), ru_pres="прятаться", ru_past="спрятаться",
                 third_only=True),
    "set": dict(en=_en("sets", "set", "set"), ru_pres="садиться", third_only=True),
}
