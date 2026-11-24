import json
import unittest

import story_logic_review as R

TEXT = "Хлеб\n\nТимоша смотрит на них и тихо ахает.\nМурка пьёт молоко.\nОн+о оде+яло любил."


class ParseTests(unittest.TestCase):
    def test_a_fenced_answer_with_chatter_around_it_still_parses(self):
        raw = 'Here is my answer:\n```json\n{"problems": [{"line": 3, "quote": "Тимоша смотрит", "kind": "continuity", "why": "x"}]}\n```\nDone.'
        self.assertEqual(1, len(R.parse_findings(raw)))

    def test_an_answer_that_is_not_json_gives_no_findings(self):
        self.assertEqual([], R.parse_findings("I found nothing wrong."))
        self.assertEqual([], R.parse_findings('{"problems": "none"}'))
        self.assertEqual([], R.parse_findings('{"problems": [1, "a"]}'))

    def test_braces_inside_a_quote_do_not_break_the_object(self):
        raw = '{"problems": [{"line": 4, "quote": "оде+яло", "kind": "grammar", "why": "a } brace"}]}'
        self.assertEqual(4, R.parse_findings(raw)[0]["line"])


class VerifyTests(unittest.TestCase):
    lines: list[str] = TEXT.splitlines()

    def finding(self, **change):
        base = {"line": 3, "quote": "Тимоша смотрит на них", "kind": "continuity", "why": "x"}
        base.update(change)
        return base

    def test_a_quote_that_is_in_the_named_line_is_accepted(self):
        accepted, rejected = R.verify([self.finding()], self.lines)
        self.assertEqual((1, 0), (len(accepted), len(rejected)))

    def test_a_quote_in_another_line_is_rejected(self):
        accepted, rejected = R.verify([self.finding(line=4)], self.lines)
        self.assertEqual((0, 1), (len(accepted), len(rejected)))

    def test_stress_marks_do_not_hide_a_quote(self):
        accepted, _ = R.verify([self.finding(line=5, quote="Оно одеяло", kind="grammar")], self.lines)
        self.assertEqual(1, len(accepted))

    def test_bad_line_numbers_kinds_and_empty_quotes_are_rejected(self):
        bad = [self.finding(line=0), self.finding(line=99), self.finding(line="3"), self.finding(kind="style"),
               self.finding(quote=""), self.finding(line=None)]
        accepted, rejected = R.verify(bad, self.lines)
        self.assertEqual((0, 6), (len(accepted), len(rejected)))

    def test_findings_come_back_in_line_order(self):
        first = self.finding(line=4, quote="Мурка пьёт")
        accepted, _ = R.verify([first, self.finding()], self.lines)
        self.assertEqual([3, 4], [item["line"] for item in accepted])


class ReviewTests(unittest.TestCase):
    def test_the_prompt_numbers_every_line_and_the_report_counts_rejections(self):
        seen = []

        def ask(prompt):
            seen.append(prompt)
            return json.dumps({"problems": [
                {"line": 3, "quote": "Тимоша смотрит", "kind": "continuity", "why": "x"},
                {"line": 3, "quote": "не в тексте", "kind": "continuity", "why": "x"}]})

        result = R.review(TEXT, ask)
        self.assertIn("3: Тимоша смотрит на них", seen[0])
        self.assertIn("1: Хлеб", seen[0])
        self.assertEqual((1, 1), (len(result["accepted"]), len(result["rejected"])))


if __name__ == "__main__":
    unittest.main()
