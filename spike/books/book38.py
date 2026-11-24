"""Book 38: "A Little Bit Scary" — the fear book.

Russian: «Мне немножко страшно». Rhymed quatrains, one emotion. A hare cub sits alone in a dark
burrow, hears a noise, looks with a torch and finds two animals who are more afraid than he is.
He takes them in, and the fear goes. Verse pages carry literal lines: `verse.en` / `verse.ru`, one
line each, and no key-word cards.
"""
STORY = {
    "title": "A Little Bit Scary",
    "cover": {"art": "cover", "verse": {
        "en": ["A Little Bit Scary"],
        "ru": ["Мне немножко страшно"],
    }},
    "pages": [
        {"art": "p01_burrow", "verse": {
            "en": ["I sit in my burrow and wait for trouble.",
                   "My ears are flat and I do not breathe.",
                   "Out in the bushes something rustles.",
                   "I am shaking all over with fear."],
            "ru": ["Сижу в норке, жду беды,",
                   "Ушки вжал и не дышу.",
                   "А в кустах шумят, шуршат —",
                   "Я от страха весь дрожу."],
        }},
        {"art": "p02_heart", "verse": {
            "en": ["My heart goes knock, knock, knock.",
                   "My paws are cold as ice.",
                   "What is that noise past the wall?",
                   "Someone is scratching at my door."],
            "ru": ["Сердце бьётся: тук-тук-тук,",
                   "Лапки холодны, как лёд.",
                   "Что за шум там, за стеной?",
                   "Кто-то в дверь мою скребёт."],
        }},
        {"art": "p03_torch", "verse": {
            "en": ["I pick up my little torch.",
                   "I come closer to the door.",
                   "I shine it and I look myself:",
                   "Oh! Visitors! Who is that?"],
            "ru": ["Я фонарик свой беру,",
                   "Подхожу к двери поближе.",
                   "Посвечу — и сам смотрю:",
                   "Ой, тут гости! Кто-то рыжий?"],
        }},
        {"art": "p04_two", "verse": {
            "en": ["It is a hedgehog and a mouse.",
                   "They cannot sleep so late at night.",
                   "Both are rolled up in a ball.",
                   "They are much more scared than me."],
            "ru": ["Это ёжик и мышонок,",
                   "Им не спится в поздний час.",
                   "Оба съёжились в комок —",
                   "Им страшнее в десять раз, в сто."],
        }},
        {"art": "p05_come_in", "verse": {
            "en": ["“Come in,” I whisper,",
                   "and I light them with my torch.",
                   "The burrow fills with warm yellow light:",
                   "fear is not scary when there are three."],
            "ru": ["— Заходите, — я шепчу,",
                   "И свечу им фонарём.",
                   "В норке тёплый жёлтый свет:",
                   "Страх не страшен нам втроём."],
        }},
        {"art": "p06_asleep", "verse": {
            "en": ["Together we lie down in a row.",
                   "Rain taps on the window.",
                   "The hedgehog sniffs, the mouse sleeps —",
                   "it is quiet and warm in the burrow."],
            "ru": ["Вместе мы легли спать в ряд.",
                   "Дождик капает в окно.",
                   "Ёжик сопит, мышка спит —",
                   "В норке тихо и тепло."],
        }},
    ],
}