import unittest

import stress_check as S


def compare(gold: str, cand: str) -> list[S.Result]:
    results = S.compare_line(1, gold, cand)
    assert results is not None, "the two lines hold different words"
    return results


class WordRuleTests(unittest.TestCase):
    def test_stress_slot_counts_vowels_not_letters(self):
        self.assertEqual(1, S.stress_slot("зап+олз"))
        self.assertEqual(0, S.stress_slot("+очень"))
        self.assertEqual(1, S.stress_slot("Пот+ом"))
        self.assertEqual(2, S.stress_slot("нарис+ова"))
        self.assertIsNone(S.stress_slot("мимо"))

    def test_the_house_rule_for_which_words_need_a_mark(self):
        self.assertTrue(S.needs_stress("мимо"))
        self.assertFalse(S.needs_stress("лисёнок"))  # ё carries the stress
        self.assertFalse(S.needs_stress("кот"))  # one vowel
        self.assertFalse(S.needs_stress("ёж"))


class CompareTests(unittest.TestCase):
    def test_a_wrong_position_is_wrong_and_a_match_is_ok(self):
        results = compare("Пот+ом он+и шли м+имо.", "П+отом он+и шл+и м+имо.")
        self.assertEqual(["потом", "они", "мимо"], [r.word.lower() for r in results])
        self.assertEqual(["wrong", "ok", "ok"], [r.verdict for r in results])

    def test_a_missing_mark_is_missing_and_a_gold_word_without_a_mark_is_not_scored(self):
        results = compare("Пот+ом они", "Потом они")
        self.assertEqual(["missing", "gold-unmarked"], [r.verdict for r in results])

    def test_lines_with_different_words_are_not_scored(self):
        self.assertIsNone(S.compare_line(1, "Мама спит.", "Мама спит крепко."))
        self.assertIsNone(S.compare_line(1, "Мама спит.", "Папа спит."))

    def test_e_and_yo_spelling_does_not_break_the_alignment(self):
        self.assertEqual(["ok"], [r.verdict for r in compare("Лисёнок нор+у", "Лисенок нор+у")])

    def test_hyphenated_words_are_two_words_on_both_sides(self):
        self.assertEqual(["ok", "ok"], [r.verdict for r in compare("М+ама-лис+а", "М+ама-лис+а")])


class TallyTests(unittest.TestCase):
    def test_counts_and_the_two_agreement_measures(self):
        tally = S.Tally()
        tally.add("s", S.compare_line(1, "Пот+ом он+и мим+о", "П+отом он+и м+имо"))  # wrong, ok, wrong
        tally.add("s", S.compare_line(2, "Мама спит", "Папа спит"))  # not scored
        tally.add("s", S.compare_line(3, "Пот+ом", "Потом"))  # missing
        self.assertEqual((1, 2, 1, 1), (tally.ok, tally.wrong, tally.missing, tally.misaligned_lines))
        self.assertEqual(4, tally.needed)
        self.assertAlmostEqual(0.25, tally.agreement)
        tally.yo_words = 4
        self.assertAlmostEqual((1 + 4) / (4 + 4), tally.agreement_poly)


class FakeEngine(S.Engine):
    name = "fake"

    def __init__(self, table):
        self.table = table

    def mark(self, line):
        return self.finish(line, self.table.get(line, line))


class EngineTests(unittest.TestCase):
    def test_the_house_rule_removes_marks_on_one_vowel_words_and_before_yo(self):
        engine = FakeEngine({"Мама шла лисёнок": "М+ама шл+а лис+ёнок"})
        self.assertEqual("М+ама шла лисёнок", engine.mark("Мама шла лисёнок"))

    def test_a_marker_that_changes_letters_leaves_the_line_unmarked(self):
        engine = FakeEngine({"Мама спит": "М+ама спит крепко"})
        self.assertEqual("Мама спит", engine.mark("Мама спит"))


class ReviewListTests(unittest.TestCase):
    def test_recall_and_share_of_the_list(self):
        gold = {"s": [(1, "пот+ом нор+у мим+о")]}
        first = {"s": {1: "п+отом н+ору мим+о"}}   # wrong, wrong, ok
        second = {"s": {1: "пот+ом н+ору м+имо"}}  # differs from the first on the first and the third word
        report = S.disagreement_report(gold, first, second)
        self.assertEqual(3, report["needed"])
        self.assertEqual(2, report["first_errors"])
        self.assertEqual(2, report["flagged"])
        self.assertEqual(1, report["errors_in_flagged"])
        self.assertAlmostEqual(0.5, report["recall"])
        self.assertAlmostEqual(2 / 3, report["list_share"])


class FillTests(unittest.TestCase):
    def test_a_word_without_a_mark_takes_the_second_engines_mark(self):
        self.assertEqual("М+ама спит т+ихо.", S.fill_line("М+ама спит тихо.", "М+ама сп+ит т+ихо."))

    def test_a_mark_the_first_engine_gave_is_never_replaced(self):
        self.assertEqual("М+ама спит т+ихо.", S.fill_line("М+ама спит т+ихо.", "М+ама спит тих+о."))

    def test_a_one_vowel_word_stays_unmarked_and_punctuation_stays(self):
        self.assertEqual("«Спи», — сказ+ал.", S.fill_line("«Спи», — сказал.", "«Сп+и», — сказ+ал."))

    def test_lines_with_different_word_counts_are_left_alone(self):
        self.assertEqual("Мама спит тихо", S.fill_line("Мама спит тихо", "М+ама спит"))


class VoteTests(unittest.TestCase):
    def test_each_listed_word_says_why_and_the_draft_takes_the_fill(self):
        lines = [(1, "Потом они шли мимо")]
        first = {1: "П+отом они шли м+имо"}
        second = {1: "Пот+ом он+и шли м+имо"}
        rows, merged = S.vote_rows(lines, [first, second])
        self.assertEqual([("Потом", "differs"), ("они", "filled")], [(r[1], r[3]) for r in rows])
        self.assertEqual("П+отом он+и шли м+имо", merged[1])

    def test_a_word_that_neither_engine_marked_is_listed_as_unmarked(self):
        rows, merged = S.vote_rows([(1, "Теперь спит")], [{1: "Теперь спит"}, {1: "Теперь спит"}])
        self.assertEqual([("Теперь", "unmarked")], [(r[1], r[3]) for r in rows])
        self.assertEqual("Теперь спит", merged[1])

    def test_a_word_only_the_first_engine_marked_is_not_listed(self):
        rows, _ = S.vote_rows([(1, "Мама спит тихо")], [{1: "М+ама спит т+ихо"}, {1: "М+ама спит тихо"}])
        self.assertEqual([], rows)

    def test_agreement_lists_nothing_and_a_heading_keeps_its_prefix(self):
        rows, merged = S.vote_rows([(1, "# Глава")], [{1: "# Гл+ава"}, {1: "# Гл+ава"}])
        self.assertEqual([], rows)
        self.assertEqual("# Гл+ава", merged[1])


class SuspectTests(unittest.TestCase):
    def test_two_engines_that_agree_against_the_gold_make_a_suspect(self):
        gold = {"s": [(1, "На угл+у дворн+ик убир+ает")]}
        first = {"s": {1: "На угл+у дв+орник убир+ает"}}
        second = {"s": {1: "На угл+у дв+орник убир+ает"}}
        found = S.suspect_words(gold, first, second)
        self.assertEqual([("дворн+ик", "дв+орник")], [(f["gold"], f["engines"]) for f in found])

    def test_engines_that_disagree_with_each_other_make_no_suspect(self):
        gold = {"s": [(1, "дворн+ик")]}
        first = {"s": {1: "дв+орник"}}
        second = {"s": {1: "дворн+ик"}}
        self.assertEqual([], S.suspect_words(gold, first, second))

    def test_a_gold_mark_that_the_engines_confirm_is_not_a_suspect(self):
        gold = {"s": [(1, "пот+ом")]}
        same = {"s": {1: "пот+ом"}}
        self.assertEqual([], S.suspect_words(gold, same, same))


class GoldFileTests(unittest.TestCase):
    def test_every_hand_checked_story_agrees_with_itself_and_nothing_is_unmarked(self):
        stories = sorted(p.name[:-len(".stressed.txt")] for p in S.STORIES.glob("*.stressed.txt"))
        self.assertGreaterEqual(len(stories), 16)
        for story in stories:
            marked = {story: {n: line for n, line in S.gold_lines(story)}}
            tally = S.score_engine({story: S.gold_lines(story)}, marked)
            self.assertEqual(tally.needed, tally.ok, story)
            self.assertEqual(0, tally.gold_unmarked, story)
            self.assertEqual(0, tally.misaligned_lines, story)
            self.assertGreater(tally.needed, 0, story)


if __name__ == "__main__":
    unittest.main()
