#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

import add_stress
import f5_russian as F5
import russian_quality_loop as Q


class TranscriptScoreTests(unittest.TestCase):
    def test_ignores_stress_yo_and_token_boundaries(self):
        score = Q.transcript_score("Т+у-ту, ёжик!", "Туту ежик")
        self.assertEqual(score["char_errors"], 0)

    def test_counts_missing_phrase(self):
        score = Q.transcript_score("Засыпают плечики, тихо, тихо.", "Засыпают плечики.")
        self.assertGreater(score["char_errors"], 0)
        self.assertEqual(score["word_errors"], 2)

    def test_rank_prefers_fewer_character_errors(self):
        expected = "Тогда ёжик пришёл."
        weak = Q.transcript_score(expected, "Тогда ижик пришёл.")
        exact = Q.transcript_score(expected, "Тогда ежик пришел.")
        self.assertLess(Q.score_rank(exact), Q.score_rank(weak))


class AccentFallbackTests(unittest.TestCase):
    class Fake:
        def process_all(self, text):
            if "Тимка" in text:
                raise ValueError("Required inputs (['token_type_ids']) are missing")
            return text.replace("воды", "вод+ы")

    def test_falls_back_to_words_and_keeps_the_working_marks(self):
        self.assertEqual(add_stress.accent(self.Fake(), "Тимка стоит у воды."), "Тимка стоит у вод+ы.")

    def test_keeps_a_clean_line_from_the_model(self):
        self.assertEqual(add_stress.accent(self.Fake(), "стоит у воды"), "стоит у вод+ы")


class StressValidationTests(unittest.TestCase):
    def test_accepts_valid_marks_and_legacy_monosyllable_marks(self):
        self.assertEqual(Q.stress_issues("С+онные п+альчики. Ёжик кт+о спит."), [])

    def test_reports_missing_and_misplaced_marks(self):
        issues = Q.stress_issues("Сонные пал+ьчики.")
        self.assertEqual(len(issues), 2)
        self.assertIn("expected one stress mark", issues[0])
        self.assertIn("not before a vowel", issues[1])

    def test_finds_matching_plain_story(self):
        with tempfile.TemporaryDirectory() as tmp:
            plain = Path(tmp) / "story.txt"
            marked = Path(tmp) / "story.stressed.txt"
            plain.write_text("Сон.\n", encoding="utf-8")
            marked.write_text("Сон.\n", encoding="utf-8")
            self.assertEqual(Q.matching_plain_source(marked), plain)


class SeedTests(unittest.TestCase):
    def test_overrides_only_the_given_parts(self):
        parts = [{"text": "а", "seed": None}, {"text": "б", "seed": None}, {"text": "в", "seed": 5}]
        F5.apply_seeds(parts, [None, 7, None])
        self.assertEqual([part["seed"] for part in parts], [None, 7, 5])

    def test_rejects_a_list_of_the_wrong_length(self):
        with self.assertRaises(ValueError):
            F5.apply_seeds([{"seed": None}], [1, 2])


class PresentationModeTests(unittest.TestCase):
    def test_modes_change_only_default_text_pauses(self):
        config = json.loads((Path(__file__).parent / "config/russian-standard.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "parts.txt"
            source.write_text("П+ервая.\nВтор+ая.\n\nТр+етья.\n", encoding="utf-8")
            night = config["modes"]["nighttime"]
            morning = config["modes"]["morning"]
            night_parts = F5.load_parts(source, night["pause_line_s"], night["pause_paragraph_s"])
            morning_parts = F5.load_parts(source, morning["pause_line_s"], morning["pause_paragraph_s"])
        # pauses are calibrated so that, after the 0.15 s edge trim on both sides of a join, the real
        # gap matches the approved one: 1.2 s at night, 0.85 s in the morning
        self.assertEqual([part["pause"] for part in night_parts], [0.9, 1.1, 1.1])
        self.assertEqual([part["pause"] for part in morning_parts], [0.55, 0.75, 0.75])
        for parts in (night_parts, morning_parts):
            self.assertAlmostEqual(0.3 + parts[0]["pause"], 1.2 if parts is night_parts else 0.85, places=2)


class PartGroupingTests(unittest.TestCase):
    def parts(self, text, minimum=0, form="prose"):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "story.stressed.txt"
            source.write_text(text, encoding="utf-8")
            return F5.load_parts(source, 0.9, 1.1, minimum, form)

    def test_zero_keeps_one_sentence_per_part(self):
        text = "Назв+ание\n\nР+аз дв+а.\nТр+и чет+ыре.\n"
        self.assertEqual([p["text"] for p in self.parts(text)], ["Назв+ание", "Р+аз дв+а.", "Тр+и чет+ыре."])

    def test_joins_until_the_minimum_inside_one_paragraph(self):
        text = "Назв+ание\n\nР+аз дв+а.\nТр+и чет+ыре.\nП+ять шесть с+емь.\n"
        parts = self.parts(text, minimum=4)
        self.assertEqual([p["text"] for p in parts],
                         ["Назв+ание", "Р+аз дв+а. Тр+и чет+ыре.", "П+ять шесть с+емь."])
        self.assertEqual([p["pause"] for p in parts], [1.1, 0.9, 1.1])

    def test_never_crosses_a_paragraph_boundary(self):
        text = "Назв+ание\n\nР+аз дв+а.\n\nТр+и чет+ыре.\n"
        parts = self.parts(text, minimum=8)
        self.assertEqual([p["text"] for p in parts], ["Назв+ание", "Р+аз дв+а.", "Тр+и чет+ыре."])
        self.assertEqual([p["pause"] for p in parts], [1.1, 1.1, 1.1])

    def test_verse_never_joins(self):
        text = "Назв+ание\n\nР+аз дв+а.\nТр+и чет+ыре.\n"
        parts = self.parts(text, minimum=8, form="verse")
        self.assertEqual([p["text"] for p in parts], ["Назв+ание", "Р+аз дв+а.", "Тр+и чет+ыре."])

    def test_a_heading_is_not_a_part_and_ends_a_paragraph(self):
        text = "Назв+ание\n\nР+аз дв+а.\n# Глава\n\nТр+и чет+ыре.\n"
        parts = self.parts(text, minimum=8)
        self.assertEqual([p["text"] for p in parts], ["Назв+ание", "Р+аз дв+а.", "Тр+и чет+ыре."])
        self.assertEqual([p["pause"] for p in parts], [1.1, 1.1, 1.1])


class ChapterTests(unittest.TestCase):
    def test_no_headings_returns_the_input_unchanged(self):
        text = "Назв+ание\n\nР+аз дв+а.\n\nТр+и чет+ыре.\n"
        chapters = F5.split_chapters(text)
        self.assertEqual(len(chapters), 1)
        self.assertEqual(chapters[0]["text"], text)
        self.assertIsNone(chapters[0]["title"])

    def test_headings_split_and_the_title_travels_with_the_first_chapter(self):
        text = "Назв+ание\n\n# П+ервая\n\nР+аз дв+а.\n\n# Втор+ая\n\nТр+и чет+ыре.\n"
        chapters = F5.split_chapters(text)
        self.assertEqual([c["title"] for c in chapters], ["П+ервая", "Втор+ая"])
        self.assertTrue(chapters[0]["text"].startswith("Назв+ание\n\n"))
        self.assertNotIn("Назв+ание", chapters[1]["text"])
        self.assertNotIn("# ", "".join(c["text"] for c in chapters))

    def test_body_before_the_first_heading_is_chapter_zero(self):
        text = "Назв+ание\n\nВступл+ение.\n\n# П+ервая\n\nР+аз дв+а.\n"
        chapters = F5.split_chapters(text)
        self.assertEqual([c["title"] for c in chapters], [None, "П+ервая"])
        self.assertIn("Вступл+ение.", chapters[0]["text"])

    def test_joined_chapter_parts_equal_the_whole_story_parts(self):
        text = ("Назв+ание\n\nВступл+ение.\n\n# П+ервая\n\nР+аз дв+а.\nТр+и чет+ыре.\n\n"
                "# Втор+ая\n\nП+ять шесть.\n")
        with tempfile.TemporaryDirectory() as tmp:
            whole = Path(tmp) / "whole.stressed.txt"
            whole.write_text(text, encoding="utf-8")
            joined = []
            for number, chapter in enumerate(F5.split_chapters(text)):
                source = Path(tmp) / f"chapter-{number}.stressed.txt"
                source.write_text(chapter["text"], encoding="utf-8")
                joined.extend(F5.load_parts(source, 0.9, 1.1))
            self.assertEqual(joined, F5.load_parts(whole, 0.9, 1.1))

    def test_chapter_settings_track_the_text_rules_but_not_the_device(self):
        import story_build as B

        cfg = json.loads((Path(__file__).parent / "config/russian-standard.json").read_text(encoding="utf-8"))
        first = B.chapter_settings(cfg, "nighttime", "prose", 0)
        self.assertEqual(first, B.chapter_settings(cfg, "nighttime", "prose", 0))
        self.assertNotIn("device", first)
        self.assertNotIn("music", first)
        self.assertNotEqual(first, B.chapter_settings(cfg, "nighttime", "prose", 8))
        self.assertNotEqual(first, B.chapter_settings(cfg, "morning", "prose", 0))
        self.assertNotEqual(first, B.chapter_settings(cfg, "nighttime", "verse", 0))

    def test_chapter_range_selects_and_validates(self):
        import story_build as B

        self.assertIsNone(B.chapter_range(None, 3))
        self.assertEqual(B.chapter_range("1-2", 3), {1, 2})
        self.assertEqual(B.chapter_range("0", 3), {0})
        with self.assertRaises(SystemExit):
            B.chapter_range("2-5", 3)

    def test_unresolved_limit_scales_with_length(self):
        import story_build as B

        self.assertEqual(B.unresolved_limit(25, None), 2)
        self.assertEqual(B.unresolved_limit(100, None), 2)
        self.assertEqual(B.unresolved_limit(101, None), 3)
        self.assertEqual(B.unresolved_limit(267, None), 6)
        self.assertEqual(B.unresolved_limit(267, 1), 1)


if __name__ == "__main__":
    unittest.main()
