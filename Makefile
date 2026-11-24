# Zero-key checks, then the optional picture call.
# `make help` lists the targets.

UV := uv run --python 3.11
BOOK ?= 2
PROVIDER ?= openai

.PHONY: help check books text pdf art

help:
	@echo "make check          narration unit tests. No key. No GPU."
	@echo "make books          compile every book. A missing picture is not a failure."
	@echo "make text BOOK=2    print one book in English and Russian."
	@echo "make pdf BOOK=2     write a PDF with code-drawn panels. No key. No pictures."

check:
	$(UV) --group checks python -m unittest discover -s narration -p "test_*.py"

books:
	cd spike && $(UV) --group books python check_books.py

text:
	cd spike && $(UV) --group books python library.py $(BOOK)

pdf:
	cd spike && $(UV) --group books python build.py --text $(BOOK)

art:
	cd spike && $(UV) --group pictures python gen_art.py --provider $(PROVIDER) book $(BOOK) all
