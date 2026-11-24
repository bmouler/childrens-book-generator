#!/usr/bin/env python3
"""Make the square cover picture of every Nursery story, 512 px, into narration/covers/NAME.png.

A story that is a book (38 to 43) takes the book's cover picture from spike/out/bookN/cover_flat.png.
The nine older stories have no book, so this script asks the same image model for one picture each in
the library's flat style (spike/styles.STYLE_FLAT), with no reference picture. The pictures are cached by
prompt in spike/out/cache like every other picture. The build installs a cover when the file exists.

usage: make_covers.py [NAME ...]      all stories in stories/modes.json when no name is given
"""
import json
import pathlib
import sys

from PIL import Image

HERE = pathlib.Path(__file__).parent
SPIKE = HERE.parent / "spike"
sys.path.insert(0, str(SPIKE))

import openai_image  # noqa: E402
import styles  # noqa: E402

COVERS = HERE / "covers"
SIZE = 512
BOOK = {"strah": 38, "dozhd": 39, "sharik": 40, "zlost": 41, "chto-eto": 42, "kotenok": 43}
SCENE = {
    "luchik": "One soft pale full moon above a dark blue night forest of simple round trees, and one thin "
              "pale beam of moonlight reaching down to one small gray hare asleep in the grass.",
    "palchiki": "One small orange fox cub lying in a bed under a blue blanket at night, holding up one front "
                "paw and looking at its toes with sleepy half-closed eyes.",
    "poezd": "One small blue night train with three warm yellow lit windows rolling across a dark blue field "
             "under one crescent moon and three stars.",
    "odeyalo": "One small brown bear cub asleep under one big patchwork blanket of red, blue, green and "
               "yellow squares, with one pale moon half hidden behind one small cloud above.",
    "solnce": "One tiny gray mouse standing on top of one round green hill, looking at one big bright yellow "
              "sun with short triangular rays rising behind the hill, with soft pale mist below.",
    "tramvay": "One small red tram with yellow lit windows on an empty gray street at dawn, with a soft pink "
               "and pale blue sky and one streetlamp.",
    "hleb": "One small boy in a yellow t-shirt and blue shorts carrying one big round warm loaf of bread with "
            "both arms on a quiet street at dawn, with one small bakery with a lit window behind him.",
    "utka": "One brown mother duck walking in a line with seven small yellow ducklings behind her toward one "
            "flat light-blue pond on plain flat green grass at first light.",
    "lodochka": "One small wooden boat with one glowing paper lantern on its bow drifting on a dark blue "
                "night river, one tiny gray mouse sitting in the boat, one round pale moon above and simple "
                "reeds at the bank.",
    "petuh": "One red and orange rooster asleep on top of one wooden fence with its head tucked down, and one "
             "small brown sparrow on the fence beside it with its beak open, under a pale dawn sky.",
    "moloko": "One small boy in blue pyjamas with yellow stars and one gray-haired grandfather kneeling "
              "together on one green rug, wiping a small white puddle with one yellow cloth, one blue cup "
              "beside them and one gray cat watching, in a warm room at night with one small lamp.",
    "prosti": "One small brown bear cub and one small orange squirrel cub asleep side by side inside one little "
              "round hut of twigs and green moss with one yellow maple leaf on top, under one old dark green "
              "spruce, with one pine cone at the door and three stars above.",
    "spasibo": "One gray father hare sitting in the round doorway of one burrow under one small bush with two "
               "small gray baby hares beside him, one in a red scarf and one in a blue scarf, looking at one big "
               "pale yellow moon rising over a dark field at dusk.",
    "koridor": "One small girl in pale pajamas walking barefoot down a dark blue hallway past one round glowing "
               "yellow moon-shaped night light on the wall, with one grandmother standing in a lit kitchen "
               "doorway behind her.",
    "sad": "One small boy in yellow rubber boots holding one small yellow watering can over a row of tiny "
           "green sprouts in a quiet garden at dusk, with one upside-down orange clay flowerpot nearby and "
           "one pale moon above.",
    "ulitka": "One small brown snail with a striped shell climbing one big wet green leaf in a garden at dusk, "
              "with one small shiny green beetle sitting on a blade of grass beside her and one round pale moon "
              "rising above an old tree stump.",
    "lopatka": "One small girl in a blue jacket and one small boy in a green jacket kneeling in a sandbox beside "
               "one sand castle with a yellow leaf flag, the boy holding one red spade, under a pale morning "
               "sun.",
    "korzinka": "One small gray badger with white face stripes, one small yellow duckling and one small gray "
                "rabbit pushing one little wooden cart with a basket of red and yellow apples up a green hill by "
                "a pond at first light.",
    "sapozhok": "One small girl with two braids sitting on a hall floor pulling on one red rubber boot with a "
                "white daisy by its loop, and one sunny window with a puddle-lit yard behind her.",
    "mozhno": "One small orange fox cub lying in green grass with dew drops, gently holding one flat paw above "
              "one small gray hedgehog with soft prickles, with white daisies around them under a pale morning "
              "sky.",
    "yagoda": "One small brown bear cub with a red berry-stained nose standing in a sunny green glade beside "
              "one big brown father bear, with one round wooden bowl of red raspberries in the grass between "
              "them.",
    "zaika": "One small white toy hare hanging by its ears from a low clothesline with one green and one "
             "yellow clothes peg in the sun, with one small girl and one smaller boy sitting on a wooden bench "
             "below it.",
}
MARGIN = "Every part of the scene stays at least 8 percent of the picture size away from the edges."


def picture(name: str) -> pathlib.Path:
    if name in BOOK:
        return SPIKE / "out" / f"book{BOOK[name]}" / "cover_flat.png"
    prompt = f"{SCENE[name]} One scene, the main subject centered and large. {MARGIN} {styles.STYLE_FLAT}"
    return openai_image.image(prompt, name=f"covers/{name}", refs=[])


def main() -> None:
    names = sys.argv[1:] or list(json.loads((HERE / "stories/modes.json").read_text(encoding="utf-8")))
    COVERS.mkdir(exist_ok=True)
    for name in names:
        if name not in BOOK and name not in SCENE:
            print(f"{name}: no scene and no book, skipped")
            continue
        src = picture(name)
        im = Image.open(src).convert("RGB")
        side = min(im.size)
        box = ((im.width - side) // 2, (im.height - side) // 2, (im.width + side) // 2, (im.height + side) // 2)
        im.crop(box).resize((SIZE, SIZE), Image.Resampling.LANCZOS).save(COVERS / f"{name}.png", optimize=True)
        print(f"{name}: {COVERS / f'{name}.png'} from {src.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
