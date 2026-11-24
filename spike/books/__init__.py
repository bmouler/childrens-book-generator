"""One story module and one art module per book.

books/bookN.py       the story: a clause list over the curated lexicon, the key words of each page,
                     the cover title. The compiler turns it into English and Russian.
books/bookN_art.py   the art prompts: what the picture of each page shows. The page names match the
                     `art` keys of bookN.py.
"""
import importlib


def story(n: int):
    return importlib.import_module(f"books.book{n}")


def art(n: int):
    return importlib.import_module(f"books.book{n}_art")
