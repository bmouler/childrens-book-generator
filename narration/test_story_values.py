import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import story_values as V

VALUES = V.load_values()
LINT = V.load_lint()


def story(words_per_line: int, lines: int, hyphen_pairs: int = 0) -> str:
    """A title, a blank line and `lines` lines of plain Russian words. hyphen_pairs lines hold one cap-cap word."""
    body = []
    for n in range(lines):
        text = " ".join(["слово"] * words_per_line)
        if n < hyphen_pairs:
            text = text.replace("слово слово", "слово-слово", 1)
        body.append(text.capitalize() + ".")
    return "Название\n\n" + "\n".join(body) + "\n"


def entry(**extra):
    base = {"mode": "nighttime", "why": "the moon rises and the animals sleep", "values": ["calm"],
            "shows": "A mother cat lies beside her kitten until he sleeps.",
            "description": "A mother cat lies beside her kitten until he sleeps. Night."}
    base.update(extra)
    return base


class ContentTests(unittest.TestCase):
    def problems(self, text, allows_fear=False):
        return V.content_problems(text, allows_fear, LINT)

    def test_religious_words_fail_with_marks_and_yo(self):
        for line in ("Слава Богу, все дома.", "Бог+у молились все.", "Боже мой, какая луна.",
                     "Над крышей стоял ангел.", "У церкви горел свет.", "Христос воскрес.", "Ему сказали: «Ей-богу!»"):
            self.assertTrue(self.problems("Название\n\n" + line), line)

    def test_innocent_words_that_share_letters_pass(self):
        for line in ("На краю сарая лежал богатый урожай.", "Крестьянин вёл коня.", "Играй тихо, мышка.",
                     "Храбрый заяц шёл в адрес лисы.", "Святослав шёл домой.", "Кровать была мягкая."):
            self.assertEqual([], self.problems("Название\n\n" + line), line)

    def test_fear_words_need_the_flag(self):
        text = "Название\n\nМне немножко страшно, шепнул он."
        self.assertTrue(self.problems(text))
        self.assertEqual([], self.problems(text, allows_fear=True))

    def test_reassurance_is_not_fear(self):
        self.assertEqual([], self.problems("Название\n\n— Не бойся, — сказал паровозик."))

    def test_religion_still_fails_when_fear_is_allowed(self):
        self.assertTrue(self.problems("Название\n\nМолитва была страшная.", allows_fear=True))

    def test_obscene_stem_fails(self):
        self.assertTrue(self.problems("Название\n\nЭто " + "бля" + "дь."))

    def test_the_line_number_counts_the_title(self):
        self.assertIn("line 3:", self.problems("Название\n\nНа небе жил ангел.")[0])


class RegistryTests(unittest.TestCase):
    def problems(self, **extra):
        return V.registry_problems("s", entry(**extra), VALUES)

    def test_a_complete_record_passes(self):
        self.assertEqual([], self.problems())

    def test_a_missing_entry_fails(self):
        self.assertTrue(V.registry_problems("s", None, VALUES))

    def test_missing_values_empty_values_and_unknown_keys_fail(self):
        e = entry()
        del e["values"]
        self.assertTrue(V.registry_problems("s", e, VALUES))
        self.assertTrue(self.problems(values=[]))
        self.assertTrue(self.problems(values=["tradition"]))
        self.assertTrue(self.problems(values="calm"))

    def test_more_than_three_values_or_a_repeat_fails(self):
        self.assertTrue(self.problems(values=["calm", "comfort", "joy", "belonging"]))
        self.assertTrue(self.problems(values=["calm", "calm"]))

    def test_shows_must_be_a_real_english_sentence(self):
        self.assertTrue(self.problems(shows=""))
        self.assertTrue(self.problems(shows="short"))
        self.assertTrue(self.problems(shows="Мама лежит рядом с котёнком и мурлычет."))

    def test_the_flags_have_types(self):
        self.assertTrue(self.problems(allows_fear="yes"))
        self.assertTrue(self.problems(min_words=50))
        self.assertEqual([], self.problems(allows_fear=True, min_words=350))

    def test_the_description_is_one_english_line_ending_with_the_mode(self):
        self.assertTrue(self.problems(description=""))
        self.assertTrue(self.problems(description="Мама лежит рядом с котёнком. Night."))
        self.assertTrue(self.problems(description="A mother cat lies beside her kitten until he sleeps."))
        self.assertTrue(self.problems(description="A mother cat lies beside her kitten until he sleeps. Morning."))
        self.assertTrue(self.problems(description="A mother cat lies beside her kitten. " + "x" * 80 + " Night."))


class FormatTests(unittest.TestCase):
    def errors(self, text, kind="short", min_words=700):
        return V.format_problems(text, kind, min_words)[0]

    def test_the_word_range_holds_at_both_ends(self):
        self.assertTrue(self.errors(story(10, 69) + "Слово " * 8 + "слово."))  # 699 words
        self.assertEqual([], self.errors(story(10, 70)))  # 700
        self.assertEqual([], self.errors(story(10, 85)))  # 850
        self.assertTrue(self.errors(story(10, 85) + "Слово."))  # 851

    def test_every_counting_method_must_pass(self):
        # 700 letters-only words, but 70 hyphen pairs make the hyphen-joined and spaced counts 630
        text = story(10, 70, hyphen_pairs=70)
        letters, hyphen, spaced = V.word_counts(text.split("\n")[2:])
        self.assertEqual((700, 630, 630), (letters, hyphen, spaced))
        self.assertTrue(self.errors(text))

    def test_verse_skips_the_word_count(self):
        self.assertEqual([], self.errors("Название\n\nЛуна над лесом.\nТихо, тихо.\n", kind="verse"))

    def test_a_lower_limit_for_a_shorter_story(self):
        self.assertEqual([], self.errors(story(10, 40), min_words=350))

    def test_latin_digits_and_unknown_characters_fail(self):
        base = "Название\n\nЛуна над лесом.\n"
        for bad in ("Луна над forest.", "Луна над лесом 3 раза.", "Луна над лесом\tтихо.", "Луна над лесом ß."):
            self.assertTrue(self.errors(base + bad + "\n", kind="verse"), bad)

    def test_a_heading_may_hold_a_digit_only_in_a_long_story(self):
        long = "Название\n\n# Глава 1. У камышей\nТихо течёт река.\n"
        self.assertEqual([], self.errors(long, kind="long"))
        self.assertTrue(self.errors(long, kind="short"))

    def test_title_and_blank_line(self):
        self.assertTrue(self.errors("# Глава\n\nТекст.\n", kind="verse"))
        self.assertTrue(self.errors("Название\nТекст сразу.\n", kind="verse"))

    def test_a_line_over_150_characters_fails(self):
        self.assertTrue(self.errors("Название\n\n" + "а" * 151 + ".\n", kind="verse"))

    def test_style_findings_are_warnings_not_errors(self):
        errors, warnings = V.format_problems("Название\n\nПора спать\nТихо.\n", "short", 1)
        self.assertEqual([], [e for e in errors if "words" not in e])
        self.assertTrue(any("does not end a sentence" in w for w in warnings))
        self.assertTrue(any("under 20" in w for w in warnings))

    def test_a_refrain_is_not_a_short_line_finding(self):
        text = "Название\n\n" + "Тихо, тихо.\nОна идёт по лесу и поёт тихую песню.\n" * 3
        _, warnings = V.format_problems(text, "short", 1)
        self.assertFalse(any("under 20" in w for w in warnings))

    def test_repeats_are_notes_and_a_refrain_is_exempt(self):
        text = ("Название\n\nМедведь лёг под тёплое одеяло и уснул.\nМышка нашла место под тёплым одеялом.\n"
                "Потом медведь лёг под тёплое одеяло и уснул.\n")
        _, warnings = V.format_problems(text, "short", 1)
        self.assertTrue(any(w.startswith(V.NOTE) and "span repeats" in w for w in warnings))
        refrain = "Название\n\n" + "Медведь лёг под тёплое одеяло и уснул.\n" * 3
        _, warnings = V.format_problems(refrain, "short", 1)
        self.assertFalse(any("span repeats" in w or "repeats twice" in w for w in warnings))


class FileCommandTests(unittest.TestCase):
    def run_file(self, text, **extra):
        with tempfile.TemporaryDirectory() as folder:
            text_path, entry_path = Path(folder) / "demo.txt", Path(folder) / "demo.entry.json"
            text_path.write_text(text, encoding="utf-8")
            entry_path.write_text(json.dumps(entry(form="verse", **extra), ensure_ascii=False), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = V.check_file(text_path, entry_path, strict=False, values=VALUES)
        return code, out.getvalue()

    def test_a_clean_draft_passes_and_names_its_mode(self):
        code, out = self.run_file("Спи, малыш\n\nНочь пришла в лесок.\nМама лежит рядом с ним.\n")
        self.assertEqual(0, code, out)
        self.assertIn("mode nighttime", out)

    def test_a_draft_with_a_religious_word_fails(self):
        code, out = self.run_file("Спи, малыш\n\nНочь пришла в лесок.\nНад ним стоит ангел.\n")
        self.assertEqual(1, code)
        self.assertIn("religious", out)

    def test_a_draft_that_reads_like_the_other_mode_fails(self):
        code, out = self.run_file("Утро\n\nВстало солнце, и все проснулись на рассвете.\nПора на завтрак.\n")
        self.assertEqual(1, code)
        self.assertIn("mode:", out)


class RegistryFileTests(unittest.TestCase):
    def test_every_story_passes_the_gate(self):
        registry = json.loads(V.REGISTRY.read_text(encoding="utf-8"))
        self.assertTrue(registry)
        for name in registry:
            errors, _ = V.check_story(name, V.story_text(name), registry, VALUES, LINT)
            self.assertEqual([], errors, name)

    def test_only_stories_about_a_fear_allow_fear(self):
        registry = json.loads(V.REGISTRY.read_text(encoding="utf-8"))
        for name, item in registry.items():
            if not item.get("allows_fear"):
                self.assertEqual([], [p for p in V.content_problems(V.story_text(name), False, LINT) if "fear" in p], name)

    def test_the_values_list_marks_nine_confirmed_values(self):
        self.assertEqual(9, sum(1 for item in VALUES.values() if item["confirmed"] == "2026-11-05"))


if __name__ == "__main__":
    unittest.main()
