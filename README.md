# Children's book generator

Bilingual English and Russian picture books, and audiobooks in a voice you record yourself.

The compiler turns a clause list into matching English and Russian. It does not call a model for the translation. The narration tools clone a voice from a short recording and render a story to one audio file.

This repository holds the code, the book sources, the stories and the docs. It does not hold API keys, voice recordings, rendered audio or pictures.

## License

Code, stories and documentation are [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). You may use them and share them. You may not sell them. Third-party pieces keep their own licenses. See [NOTICE.md](NOTICE.md).

## What you need

- Python 3.11 and [uv](https://docs.astral.sh/uv/)
- `OPENAI_API_KEY` or `XAI_API_KEY` if you generate pictures
- A machine with a GPU, or a patient CPU, if you render speech
- Your own voice recording. The repository has no voice file.

```sh
cp .env.example .env
export OPENAI_API_KEY=your-key
export XAI_API_KEY=your-key
```

The clients read those variables. They never print the key and they never store it.

## Picture books

A book is two files in `spike/books/`. `bookN.py` is the clause list. `bookN_art.py` holds the picture prompts. The lexicon is `spike/lexicon.py`. The engine is `spike/bilingual.py`.

```sh
cd spike
U="uv run --no-project --python 3.11 --with pymorphy3 --with pymorphy3-dicts-ru --with pillow --with numpy --with scipy --with img2pdf python"
$U library.py 2
$U check_books.py
$U build.py 2
```

`build.py` writes a PDF to `../renders/`. That folder is ignored. Rebuild it any time.

Pictures are optional and they cost money. OpenAI is the default provider. xAI is the other.

```sh
A="uv run --no-project --python 3.11 --with httpx --with pillow python"
$A gen_art.py --provider openai book 4 all
$A gen_art.py --provider xai book 4 p03
```

The client pays only when no cache entry matches the full request. `--force` always pays. Generated files land in `spike/out/`, which is ignored.

A photo of a child is not required. If you use one as an art reference, keep it outside the repo. The default path is `~/.config/childrens-book-generator/hero_photo.png`. Set `HERO_PHOTO` to use another path. Strip its metadata before you send it to a provider.

Page size is 1620 x 2160 px, portrait 3:4. Design reasons are in [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md). The Russian review sheet is [docs/RUSSIAN_REVIEW.md](docs/RUSSIAN_REVIEW.md).

Books 1 to 37 are in `spike/books/`. Books 38 to 43 are short verse books. Their Russian line is the lead line.

## Audiobooks

English uses Chatterbox and writes one `.m4b` with chapter marks. Russian uses F5-TTS and writes one `.m4a`. Night and morning each have a pause profile and an optional music bed.

```sh
export NARRATION_HOST=your-render-machine
export NARRATION_DEST=bedtime-audiobooks
```

The scripts have no default host. Record the voice first. [narration/RECORDING_GUIDE.md](narration/RECORDING_GUIDE.md) has the steps. [narration/README.md](narration/README.md) has the render commands. [narration/RUSSIAN_STANDARD.md](narration/RUSSIAN_STANDARD.md) has the voice settings you fill in after you record.

A voice file stays on your disk. `.gitignore` blocks `narration/voice/`, `narration/samples/` and the audio extensions.

## Stories

`narration/stories/` holds 28 Russian stories as plain text and as stress-marked text. `stories/modes.json` names the mode and the value of each story. A story shows a value by what a character does. No line tells a child what to do.

The values list is `narration/config/values.json`. The word lint is `narration/config/content-lint.json`. Religious words fail the lint.

## Layout

```
spike/                 picture-book compiler, lexicon, book sources, fonts
spike/gen_art.py       picture generation. Reads OPENAI_API_KEY or XAI_API_KEY.
narration/             audiobook tools and the Russian stories
narration/bedtime.py   English book to .m4b
narration/f5_russian.py
                       Russian text to .m4a
narration/build_story.sh
                       ship one story to NARRATION_HOST, build it, pull the audio back
docs/                  design notes, Russian review, recording guide pointer
```

## Privacy

Do not commit a key, a voice recording, a child's photo, or a picture made from that photo. Do not put a home path, a LAN address, or a voice-file hash into a public fork.
