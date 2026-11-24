"""Size probe: print the compiled text of a book and the biggest font each page fits at.
usage: probe_sizes.py N
"""
import sys

import render as R
import library
from wordcard import WordCard, inset, size_of

n = int(sys.argv[1])
pages = library.compiled(n)["pages"]
w_card, h_card = size_of(inset(WordCard.SENT, 26, 10))
w_plain, h_plain = size_of(inset(WordCard.PLAIN, 26, 10))
sizes = []
for i, pg in enumerate(pages, 1):
    w, h = (w_card, h_card) if pg.get("focus") else (w_plain, h_plain)
    size = next(s for s in range(100, 40, -2) if R.fits([pg], s, w, h))
    sizes.append(size)
    print(f"p{i:02} {size:3}px {'cards' if pg.get('focus') else 'plain'}  {pg['en']} | {pg['ru']}")
print(f"book {n}: {len(pages)} pages, text {min(sizes)} px")
