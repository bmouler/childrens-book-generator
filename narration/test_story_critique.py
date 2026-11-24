import json
import unittest
from pathlib import Path

import story_critique_loop as C

HERE = Path(__file__).resolve().parent
PER_BYTE = 0.055  # about the measured rate for one UTF-8 letter at speed 0.788


class AskTests(unittest.TestCase):
    def setUp(self):
        self.real = C.chat
        self.calls = 0

    def tearDown(self):
        C.chat = self.real

    def test_retries_a_timeout_and_returns_the_next_answer(self):
        def chat(*args, **kwargs):
            self.calls += 1
            if self.calls == 1:
                raise TimeoutError("timed out")
            return '{"patches": []}'
        C.chat = chat
        self.assertEqual(C.ask("e", "m", [], 5, 0.2), '{"patches": []}')
        self.assertEqual(self.calls, 2)

    def test_retries_an_empty_answer(self):
        def chat(*args, **kwargs):
            self.calls += 1
            return "  " if self.calls < 3 else "ok"
        C.chat = chat
        self.assertEqual(C.ask("e", "m", [], 5, 0.2), "ok")
        self.assertEqual(self.calls, 3)

    def test_gives_up_after_three_tries(self):
        def chat(*args, **kwargs):
            self.calls += 1
            raise TimeoutError("timed out")
        C.chat = chat
        with self.assertRaises(RuntimeError):
            C.ask("e", "m", [], 5, 0.2)
        self.assertEqual(self.calls, 3)


class ParseTests(unittest.TestCase):
    def test_plain_object(self):
        self.assertEqual({"a": 1}, C.parse_json_block('{"a": 1}'))

    def test_fenced_object(self):
        self.assertEqual({"a": 2}, C.parse_json_block('```json\n{"a": 2}\n```'))

    def test_object_after_prose(self):
        self.assertEqual({"patches": []}, C.parse_json_block('Вот ответ:\n{"patches": []}\nГотово.'))

    def test_nothing_returns_empty(self):
        self.assertEqual({}, C.parse_json_block("без json"))


class LineRuleTests(unittest.TestCase):
    def test_good_line(self):
        self.assertEqual([], C.line_problems("Медвеж+онок леж+ал на м+ягком мху.", PER_BYTE))

    def test_unmarked_polysyllable(self):
        self.assertTrue(any("stress" in p for p in C.line_problems("Медвежонок лежал.", PER_BYTE)))

    def test_latin_and_digits(self):
        self.assertIn("latin letters", C.line_problems("Медвеж+онок леж+ал ok.", PER_BYTE))
        self.assertIn("digits", C.line_problems("Медвеж+онок леж+ал 3 р+аза.", PER_BYTE))

    def test_one_word(self):
        self.assertTrue(any("words" in p for p in C.line_problems("Спи.", PER_BYTE)))

    def test_too_short_in_seconds(self):
        self.assertTrue(any(" s" in p for p in C.line_problems("Топ-топ.", PER_BYTE)))

    def test_very_long_line(self):
        line = "Медв+ежонок " * 24
        self.assertTrue(any(" s" in p for p in C.line_problems(line, PER_BYTE)))


class ApplyTests(unittest.TestCase):
    def test_patch_replaces_and_reports(self):
        lines = ["Заголовок", "Медвеж+онок леж+ал на м+ягком мху.", "Он не спал."]
        ok, why = C.apply_patch(lines, 1, "Медвеж+онок леж+ал на м+ягком м+уху.", PER_BYTE)
        self.assertTrue(ok)
        self.assertEqual("ok", why)
        self.assertEqual("Медвеж+онок леж+ал на м+ягком м+уху.", lines[1])

    def test_rejected_patch_leaves_the_line(self):
        lines = ["Заголовок", "Медвеж+онок леж+ал.", "Он не спал."]
        before = lines[1]
        ok, why = C.apply_patch(lines, 1, "Медвежонок лежал.", PER_BYTE)
        self.assertFalse(ok)
        self.assertIn("stress", why)
        self.assertEqual(before, lines[1])

    def test_unchanged_and_out_of_range(self):
        lines = ["Заголовок", "Медвеж+онок леж+ал."]
        self.assertEqual((False, "unchanged"), C.apply_patch(lines, 1, "Медвеж+онок  леж+ал.", PER_BYTE))
        self.assertEqual((False, "line is outside the story"), C.apply_patch(lines, 9, "Он спит.", PER_BYTE))


class JoinTests(unittest.TestCase):
    LINES = [
        "Лунный зайчик",
        "Над больш+им тёмным л+есом поднял+ась лун+а.",
        "Зв+али ег+о Л+учик.",
        "К+аждый в+ечер он обход+ил лес.",
        "Он жел+ал всем спок+ойной н+очи.",
    ]
    NAMES = {"лучи", "кажд"}

    def test_lowercase_name_with_a_stress_mark_rejected(self):
        lines = self.LINES.copy()
        ok, why = C.apply_patch(lines, 2, "Зв+али ег+о л+учик.", PER_BYTE, names=self.NAMES)
        self.assertFalse(ok)
        self.assertIn("name written in lowercase", why)

    def test_lowercase_name_rejected(self):
        lines = self.LINES.copy()
        ok, why = C.apply_patch(lines, 2, "Зв+али ег+о луч+ик.", PER_BYTE, names=self.NAMES)
        self.assertFalse(ok)
        self.assertIn("name written in lowercase", why)

    def test_sentence_start_lowered_rejected(self):
        lines = self.LINES.copy()
        ok, why = C.apply_patch(lines, 1, "над больш+им тёмным л+есом поднял+ась лун+а.", PER_BYTE, names=self.NAMES)
        self.assertFalse(ok)
        self.assertIn("lowercase", why)

    def test_body_lowered_inside_a_sentence_is_allowed(self):
        lines = ["Заголовок", "Он л+ег", "Сп+ал весь день и всю ночь и не просн+улся ни р+азу.", "Пот+ом встал."]
        ok, _ = C.apply_patch(lines, 2, "сп+ал весь день и всю ночь и не просн+улся ни р+азу.", PER_BYTE, names=set())
        self.assertTrue(ok)

    def test_full_stop_dropped_before_a_capital_is_rejected(self):
        lines = self.LINES.copy()
        ok, why = C.apply_patch(lines, 2, "Зв+али ег+о Л+учик,", PER_BYTE, names=self.NAMES)
        self.assertFalse(ok)
        self.assertIn("full stop", why)

    def test_quote_starting_line_counts_as_a_sentence_start(self):
        lines = ["Заголовок", "Он игр+ал и пр+ыгал.", "«Ты кто?» — спрос+или зайч+ата."]
        ok, why = C.apply_patch(lines, 1, "Он игр+ал и пр+ыгал", PER_BYTE, names=set())
        self.assertFalse(ok)
        self.assertIn("full stop", why)

    def test_full_stop_added_before_lowercase_is_rejected(self):
        lines = ["Заголовок", "Он л+ег,", "и ср+азу усн+ул.", "Утро."]
        ok, why = C.apply_patch(lines, 1, "Он л+ег.", PER_BYTE, names=set())
        self.assertFalse(ok)
        self.assertIn("full stop", why)

    def test_seam_pair_may_lowercase_and_continue(self):
        lines = ["Заголовок", "Он л+ег на м+ягкую трав+у", "ср+азу усн+ул.", "Утро."]
        ok, _ = C.apply_patch(lines, 1, "Он л+ег на м+ягкую трав+у и", PER_BYTE, check_join=False, names=set())
        self.assertTrue(ok)
        ok, _ = C.apply_patch(lines, 2, "уж+е не встал ни р+азу.", PER_BYTE, check_join=False, names=set())
        self.assertTrue(ok)


class NameTests(unittest.TestCase):
    def test_names_come_from_mid_line_capitals_only(self):
        lines = ["Лунный зайчик", "Звали его Лучик.", "Мишутка жил в берлоге под сосной."]
        self.assertEqual({"лучи"}, C.name_tokens(lines))

    def test_sentence_initial_common_word_is_not_a_name(self):
        self.assertEqual(set(), C.name_tokens(["Заголовок", "Над лесом поднялась луна."]))


class EstimateTests(unittest.TestCase):
    def test_rate_grows_with_the_text(self):
        cfg = json.loads((HERE / "config/russian-standard.json").read_text(encoding="utf-8"))
        rate = C.seconds_per_byte(cfg)
        self.assertGreater(rate, 0)
        self.assertGreater(C.estimate_seconds("Он " * 30, rate), C.estimate_seconds("Он", rate))

    def test_seam_pairs_flags_the_extremes(self):
        lines = ["Заголовок", "Топ-топ.", "Медв+ежонок " * 24, "Он л+ег и закр+ыл гл+аза, и ему ст+ало т+епло."]
        flagged = C.seam_pairs(lines, 0.06)
        self.assertIn(1, flagged)
        self.assertIn(2, flagged)
        self.assertNotIn(3, flagged)

    def test_no_seam_across_a_paragraph_break(self):
        lines = ["Заголовок", "Он спит.", "", "Медв+ежонок " * 24]
        self.assertNotIn(1, C.seam_pairs(lines, 0.06))

    def test_no_seam_on_a_refrain(self):
        lines = ["Заголовок", "Пор+а спать.", "Он л+ег.", "Пор+а спать.", "Он встал.",
                 "Пор+а спать.", "Он сел."]
        flagged = C.seam_pairs(lines, 0.06)
        for index in (1, 3, 5):
            self.assertNotIn(index, flagged)


if __name__ == "__main__":
    unittest.main()