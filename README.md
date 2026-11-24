# Children's book generator

[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-blue)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads/)
[![checks](https://github.com/bmouler/childrens-book-generator/actions/workflows/checks.yml/badge.svg)](https://github.com/bmouler/childrens-book-generator/actions/workflows/checks.yml)

This repository builds English and Russian picture books. It also builds audiobooks from a voice file you record.

The compiler turns a clause list into English and Russian that say the same thing. It does not call a model for the translation. The narration tools make speech from a short voice file.

This repository holds the code, the book sources, the stories and the docs. It does not hold an API key, a voice file, an audio file or a picture.

## Start with no key

You need Python 3.11 and [uv](https://docs.astral.sh/uv/). These commands do not call an API. They do not need a GPU.

```sh
git clone https://github.com/bmouler/childrens-book-generator.git
cd childrens-book-generator
cp .env.example .env
make check
make books
```

`make check` runs the narration unit tests. `make books` compiles every book. A missing picture is not a failure.

Print one book as text with this command:

```sh
make text BOOK=2
```

## Three paths

| Path | You need | First command |
|---|---|---|
| Books | Python 3.11 and uv | `make books` |
| Pictures | `OPENAI_API_KEY` or `XAI_API_KEY` | `make art BOOK=2` |
| Audiobooks | A GPU machine, your voice file, `NARRATION_HOST` | [narration/README.md](narration/README.md) |

Copy [.env.example](.env.example) to `.env`. Export the names you use. The clients read those variables. They do not print a key. They do not write a key to disk.

## License

Code, stories and documentation are [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). You can use them. You can share them. Do not sell them. Third-party pieces keep their own licenses. See [NOTICE.md](NOTICE.md).

## Picture books

A book is two files in `spike/books/`. `bookN.py` is the clause list. `bookN_art.py` holds the picture prompts. The lexicon is `spike/lexicon.py`. The engine is `spike/bilingual.py`.

```sh
cd spike
uv run --python 3.11 --group books python library.py 2
uv run --python 3.11 --group books python check_books.py
uv run --python 3.11 --group books python build.py 2
```

`build.py` writes a PDF to `../renders/` only when every picture for that book is present. That folder is ignored. Build it again at any time.

Pictures are not required for the text. You pay for each new picture. OpenAI is the default provider. xAI is the other provider.

```sh
make art BOOK=2
make art BOOK=2 PROVIDER=xai
```

The client pays only when no cache entry matches the full request. The flag `--force` always pays. Picture files go to `spike/out/`. Git ignores that folder.

A photo of a child is not required. If you use one as an art reference, keep it outside the repo. The default path is `~/.config/childrens-book-generator/hero_photo.png`. Set `HERO_PHOTO` to use another path. Remove its metadata before you send it to a provider.

Page size is 1620 x 2160 px, portrait 3:4. Design reasons are in [docs/DESIGN_PRINCIPLES.md](docs/DESIGN_PRINCIPLES.md). The Russian review sheet is [docs/RUSSIAN_REVIEW.md](docs/RUSSIAN_REVIEW.md).

Books 1 to 37 are in `spike/books/`. Books 38 to 43 are short verse books. Their Russian line is the lead line.

## Audiobooks

English uses Chatterbox. The output is one `.m4b` with chapter marks. Russian uses F5-TTS. The output is one `.m4a`. Night and morning each have a pause profile. Each profile can add a music bed.

```sh
export NARRATION_HOST=your-render-machine
export NARRATION_DEST=bedtime-audiobooks
```

The scripts have no default host. Set `NARRATION_PYTHON` to the Python on the render machine. The example path is `~/miniforge3/envs/bedtime/bin/python`.

Record the voice first. [narration/RECORDING_GUIDE.md](narration/RECORDING_GUIDE.md) has the steps. [narration/README.md](narration/README.md) has the render commands. [narration/RUSSIAN_STANDARD.md](narration/RUSSIAN_STANDARD.md) has the voice settings you fill in after you record.

A voice file stays on your disk. `.gitignore` blocks `narration/voice/`, `narration/samples/` and the audio extensions.

## Stories

`narration/stories/` holds 28 Russian stories as plain text and as stress-marked text. `stories/modes.json` names the mode and the value of each story. A story shows a value by what a character does. No line tells a child what to do.

The values list is `narration/config/values.json`. The word lint is `narration/config/content-lint.json`. Religious words fail the lint.

Until you record, the text critic uses an 8 second example for the reference sentence. The renderer does not use that example.

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
docs/                  design notes and the Russian review
Makefile               make check, make books, make text, make art
```

## Privacy

Do not commit a key, a voice file, a child photo, or a picture made from that photo. Do not put a home path, a LAN address, or a voice-file hash into a public fork. See [SECURITY.md](SECURITY.md).
