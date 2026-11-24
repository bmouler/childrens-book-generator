# Zero-key checks, then the optional picture call.
# `make help` lists the targets.

UV := uv run --python 3.11
BOOK ?= 2
PROVIDER ?= openai

.PHONY: help check books text art

help:
	@echo "make check          narration unit tests. No key. No GPU."
	@echo "make books          compile every book. A missing picture is not a failure."
	@echo "make text BOOK=2    print one book in English and Russian."
	@echo "make art BOOK=2     make pictures. Needs OPENAI_API_KEY, or PROVIDER=xai."

check:
	$(UV) --group checks python -m unittest discover -s narration -p "test_*.py"

books:
	cd spike && $(UV) --group books python check_books.py

text:
	cd spike && $(UV) --group books python library.py $(BOOK)

art:
	cd spike && $(UV) --group pictures python gen_art.py --provider $(PROVIDER) book $(BOOK) all
