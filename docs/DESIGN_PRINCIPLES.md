# Design principles and prior art

Research date: 2026-10-13. Each principle names its source and the design that applies it.
"Read" means I opened the page. "Excerpt" means I only saw the search-result excerpt.

## Principles

| # | Principle | Source | Where it shows up |
|---|---|---|---|
| 1 | One idea per page. Two or three focal elements at most. Bold simple shapes, thick outlines, high contrast, minimal background detail. | usillustrations.com "5 key rules", madegooddesigns.com (excerpts) | All books: one picture and one sentence per page. Flat art with navy outlines. |
| 2 | A master palette of 8 to 12 colours keeps a book coherent. | usillustrations.com, markwatsonbooks.com (excerpts) | Four pill colours, one per concept for the whole book. Art uses flat fills. |
| 3 | Keep text off the art. Use a light background under dark text. White space gives the eye a rest. | oldmatemedia.com, bookdesignmadesimple.com (excerpts) | The Word-card page: the picture on top, text on white below, never on the art. |
| 4 | Sans-serif type, 18 to 24 pt for ages 2 to 5, leading 120 to 145 percent, large x-height. Andika was designed for literacy and USAID lists it as a best-practice font. | fonts.com, visualstress.info, designyourway.net, colourmylearning.com (excerpts) | Andika everywhere. Body text is 88 to 100 px, which is 28 to 31 pt at 229 PPI. |
| 5 | Stack the two languages in the same order and place on every page. Do not rely on colour alone to tell them apart. | yourbookbound.com (read), bookdesigntemplates.com, Taylor and Francis 2023 (excerpts) | English above Russian on every page. Latin and Cyrillic look different, so the labels are gone. |
| 6 | Colour-coded vocabulary is common in bilingual books. It helps most when the two sentences do not have the same word order. | medium.com/@shahnorama, kelseykloss.com (excerpts) | Colour pills. Page 10 shows the crossing order: "you try" against "попробуй ты". |
| 7 | Toddlers learn more from realistic pictures. Photos worked at 18, 24 and 30 months. Colour line drawings worked at 24 and 30 months, not at 18. | bps.org.uk digest of Simcock and DeLoache 2006 (read) | The books use drawings. The study taught an action (building a rattle), not words. Your child is 24 months, so drawings are in range. A photo design was tried and dropped (history, commit 8defcb2). |
| 8 | Mix picture sizes (spot, half page, full page) to set the pace. | getyourbookillustrations.com (excerpt) | The Word-card page has three sizes on one page: a square picture, word cards, the sentence. |
| 9 | Colour e-ink wants strong contrast, a limited palette and no subtle gradients. Gallery 3 colours are muted. | goodereader.com, good-display.com (excerpts) | Flat art, solid fills, medium pill tints. The tints are estimates. I have not seen them on the device. |
| 10 | Page counter as "x out of y" with one dot per page. | Your request. The dots are my addition. | Every story page. Digits and "out of / из" are matched with neutral pills. |

## Prior art on GitHub

I found no repository that compiles English and Russian from one source, aligns the words and shows
colour pills. Stars were read with `gh` on the research date.

| Repository | Stars | What it does | Use for us |
|---|---|---|---|
| yihong0618/bilingual_book_maker | 9,878 | Makes bilingual EPUB books with AI translation | The opposite of our rule. Translation is not deterministic. Look at it when we build EPUB output. |
| GrammaticalFramework/gf-rgl | 70 | Grammar library with `src/english` and `src/russian` | Closest prior art for our compiler: one abstract tree, two languages. Consider it if the grammar outgrows about 300 lexicon entries. |
| simplenlg/simplenlg | 832 | Java realiser for English | English only. |
| HVision-NKU/StoryDiffusion | 6,474 | Consistent characters across images | Needs a local GPU. We use one derived character sheet as the OpenAI or xAI reference. |
| weaiw/storybook-generator-skill | 48 | Skill for consistent picture-book drafts | LLM text and art. No translation guarantee. |
| angrysky56/gemini_picturebook_generator | 42 | HTML and PDF picture books with Gemini | Same. |
| StarryGuli/bilingual-epub-toolkit | 12 | Merges two EPUBs into a tap-to-reveal bilingual EPUB | Idea for EPUB output. |
| jasonhibbs/blankbook | 3 | Fixed-layout ePub 3 template for picture books | Starting point for EPUB output. |
| tinygodsdev/bitext-word-alignment | n/a | Draws curved lines between matching words | An alternative to pills. |

## What I could not read

- The Taylor and Francis article on bilingual picturebook typography returned HTTP 403. I used the search summary.
- Most design sites are excerpts only. Open the sources before you rely on a number.
