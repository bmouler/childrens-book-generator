"""Generate book art with OpenAI or xAI.

usage:
  gen_art.py [--provider openai|xai] hero
      Redraw the character sheet from the photo at $HERO_PHOTO (default
      ~/.config/childrens-book-generator/hero_photo.png). The photo never enters the repo.
  gen_art.py [--provider openai|xai] book N [all | cover | <page name start> ...] [--force]
      Make the pictures of book N from books/bookN_art.py. `all` (the default) makes every page and the
      cover. A page name start such as p03 makes only that page. --force ignores that provider's cache
      and pays for a new picture. Pictures go to out/bookN/<page>.png and out/bookN/cover_flat.png.
      An art module with a CHARSHEET prompt (folk tales, no toddler hero) first makes
      out/bookN/charsheet.png and uses it as the reference picture of every page.
Every picture is cached by provider, model, prompt and reference bytes. $GEN_WORKERS sets the number of
requests in flight (default 2). $IMAGE_PROVIDER sets the default provider (default openai).
"""
import argparse
import concurrent.futures as cf
import os
import pathlib

import books
import openai_image
import styles
import xai
from xai import OUT

PROVIDERS = {
    "openai": (openai_image, "gpt-image-2.5-sunburst-2026-09-08"),
    "xai": (xai, "grok-imagine-image-2.0"),
}
HERO = OUT / "hero_sheet.png"
HERO_PHOTO = pathlib.Path(os.environ.get("HERO_PHOTO", "~/.config/childrens-book-generator/hero_photo.png")).expanduser()


def img(prompt, name, refs=None, ratio="1:1", force=False, provider="openai"):
    client, model = PROVIDERS[provider]
    return client.image(prompt, name=name, model=model, refs=refs, aspect_ratio=ratio,
                        resolution="2k", quality="medium", force=force)


def book_jobs(n: int, picks: list[str]) -> list[tuple]:
    """(prompt, name, refs, ratio) for the chosen pictures of book n."""
    mod = books.art(n)
    keep_for = getattr(mod, "KEEP_FOR", {})
    refs = [OUT / f"book{n}/charsheet.png"] if getattr(mod, "CHARSHEET", None) else [HERO]
    whole = not picks or picks == ["all"]
    jobs = []
    for name, action in mod.PAGES.items():
        if whole or any(name.startswith(p) for p in picks):
            jobs.append((styles.scene_flat(action, keep_for.get(name, styles.KEEP)), f"book{n}/{name}", refs, "1:1"))
    if whole or "cover" in picks:
        jobs.append((styles.scene_flat(mod.COVER, keep_for.get("cover", styles.KEEP)), f"book{n}/cover_flat", refs, "1:1"))
    unknown = [p for p in picks if p not in ("all", "cover") and not any(k.startswith(p) for k in mod.PAGES)]
    if unknown:
        raise SystemExit(f"book {n} has no page that starts with {unknown}. Pages: {', '.join(mod.PAGES)}")
    return jobs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=PROVIDERS, default=os.environ.get("IMAGE_PROVIDER", "openai"))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("command", choices=("hero", "book"))
    parser.add_argument("rest", nargs="*")
    args = parser.parse_args()

    if args.command == "hero":
        if args.rest:
            parser.error("hero takes no positional arguments")
        if not HERO_PHOTO.exists():
            raise SystemExit(f"no hero photo at {HERO_PHOTO}. Put one there or set HERO_PHOTO.")
        jobs = [(styles.sheet_from_photo(), "hero_sheet", [HERO_PHOTO], "1:1")]
    else:
        if not args.rest:
            parser.error("book requires its number")
        try:
            number = int(args.rest[0])
        except ValueError:
            parser.error(f"book number must be an integer, not {args.rest[0]!r}")
        if not HERO.exists():
            raise SystemExit(f"{HERO} is missing: run `gen_art.py hero` first")
        if getattr(books.art(number), "CHARSHEET", None):  # a folk-tale cast sheet, not the toddler
            img(f"{books.art(number).CHARSHEET} {styles.STYLE_FLAT}", name=f"book{number}/charsheet",
                refs=[], ratio="1:1", force=args.force, provider=args.provider)
        jobs = book_jobs(number, args.rest[1:])

    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("GEN_WORKERS", "2"))) as pool:
        futures = [
            pool.submit(img, prompt, name, refs, ratio, args.force, args.provider)
            for prompt, name, refs, ratio in jobs
        ]
        for future in futures:
            future.result()
    print(f"done: {len(jobs)} picture(s) via {args.provider}")
