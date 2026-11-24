import json
import tempfile
import unittest
from pathlib import Path

import long_story as L

REFRAIN = ["Тихо плывёт лодочка.", "Тихо течёт река."]


SUBJECTS = ["Пик", "Лодочка", "Луна", "Река", "Фонарик", "Цапля", "Мама", "Сова"]
PREDICATES = ["смотрит на воду", "плывёт по реке", "светит на камыши", "слушает тишину",
              "поёт тихую песню", "качается на волне"]
ADVERBS = ["тихо", "медленно", "спокойно", "мягко", "сонно", "плавно"]


def chapter(word_target=190):
    """A valid chapter body: unique short sentences, paragraphs of four, the refrain last."""
    sentences = ["Вечер. Над рекой встаёт луна.", "Вокруг темно и очень тихо.",
                 "Только луна смотрит в воду.", "Все уже легли и видят сны."]
    sentences += [f"{subject} {adverb} {predicate}."
                  for subject in SUBJECTS for predicate in PREDICATES for adverb in ADVERBS]
    lines, total, index = [], 0, 0
    while total < word_target - 12:
        block = sentences[index:index + 4]
        lines.extend(block)
        lines.append("")
        total += sum(len(L.words(line)) for line in block)
        index += 4
    lines += REFRAIN
    return lines


class ChapterRuleTests(unittest.TestCase):
    def test_a_valid_chapter_has_no_problems(self):
        lines = chapter()
        self.assertEqual(L.chapter_problems(lines, REFRAIN), [])
        self.assertGreaterEqual(sum(len(L.words(x)) for x in lines), L.CHAPTER_MIN)

    def test_a_short_chapter_is_reported_with_its_word_count(self):
        lines = ["Пик сидит в лодочке.", "Он смотрит на луну.", "", *REFRAIN]
        problems = L.chapter_problems(lines, REFRAIN)
        self.assertTrue(any("words, expected 180-220" in p for p in problems), problems)

    def test_a_long_chapter_is_reported(self):
        lines = chapter(word_target=400)
        self.assertTrue(any("words, expected" in p for p in L.chapter_problems(lines, REFRAIN)))

    def test_digits_are_reported(self):
        lines = chapter()
        lines[0] = "Вечер. Часы бьют 7 раз."
        self.assertTrue(any(p.startswith("digits") for p in L.chapter_problems(lines, REFRAIN)))

    def test_latin_letters_are_reported(self):
        lines = chapter()
        lines[0] = "Лодочка boat плывёт по реке."
        self.assertTrue(any(p.startswith("latin") for p in L.chapter_problems(lines, REFRAIN)))

    def test_a_line_without_a_sentence_end_is_reported(self):
        lines = chapter()
        lines[0] = "Вечер над тихой рекой"
        self.assertTrue(any("does not end a sentence" in p for p in L.chapter_problems(lines, REFRAIN)))

    def test_a_line_of_one_word_is_reported(self):
        lines = chapter()
        lines[0] = "Тихо."
        self.assertTrue(any("words in one line" in p for p in L.chapter_problems(lines, REFRAIN)))

    def test_a_missing_refrain_is_reported(self):
        lines = chapter()[:-2]
        problems = L.chapter_problems(lines, REFRAIN)
        self.assertTrue(any("refrain" in p for p in problems), problems)

    def test_a_changed_refrain_word_is_reported(self):
        lines = chapter()
        lines[-1] = "Тихо течёт вода."
        self.assertTrue(any("refrain" in p for p in L.chapter_problems(lines, REFRAIN)))

    def test_a_two_line_paragraph_is_reported(self):
        lines = chapter()
        lines.insert(2, "")
        self.assertTrue(any(p.startswith("paragraph of 2") for p in L.chapter_problems(lines, REFRAIN)))

    def test_a_repeated_sentence_is_reported(self):
        lines = chapter()
        lines[5] = lines[0]
        self.assertTrue(any(p.startswith("repeated line") for p in L.chapter_problems(lines, REFRAIN)))

    def test_the_refrain_may_repeat_across_a_chapter(self):
        lines = chapter()
        self.assertFalse(any(p.startswith("repeated line") for p in L.chapter_problems(lines, REFRAIN)))


class StoryRuleTests(unittest.TestCase):
    def story(self, chapters=2):
        out = ["Лодочка плывёт домой", ""]
        for number in range(1, chapters + 1):
            out.append(f"# Глава {number}. Поворот реки")
            out.extend(chapter())
            out.append("")
        return "\n".join(out).rstrip() + "\n"

    def test_a_valid_story_passes(self):
        self.assertEqual(L.story_problems(self.story(), REFRAIN, 2, "nighttime"), [])

    def test_a_total_below_the_window_is_reported(self):
        text = self.story()
        total = L.body_words(text.splitlines()[1:])
        self.assertEqual(L.story_problems(text, REFRAIN, 2, "nighttime", total_min=total - 1,
                                          total_max=total + 1), [])
        problems = L.story_problems(text, REFRAIN, 2, "nighttime", total_min=total + 5, total_max=total + 9)
        self.assertTrue(any("body words, expected" in p for p in problems), problems)

    def test_the_fixed_line_restore_puts_back_headings_and_the_refrain(self):
        with tempfile.TemporaryDirectory() as folder:
            real = L.STORIES
            L.STORIES = Path(folder)
            try:
                headings = ["# Глава 1. Цапля", "# Глава 2. Бобры"]
                plain = ["Лодочка плывёт домой", ""]
                stressed = ["Л+одочка плывёт дом+ой", ""]
                for number, heading in enumerate(headings, 1):
                    plain += [heading, "Пик сидит в лодочке.", "",
                              "Тихо плывёт лодочка.", "Тихо течёт река.", ""]
                    stressed += [heading, "Пик с+идит в л+одочке.", "",
                                 "Т+ихо плывёт л+одочка.", "Т+ихо течёт рек+а.", ""]
                plain[2] = "# Глава один. Цапля"
                plain[6] = "Тихо течёт вода."
                stressed[6] = "Т+ихо течёт вод+а."
                (Path(folder) / "x.txt").write_text("\n".join(plain) + "\n", encoding="utf-8")
                (Path(folder) / "x.stressed.txt").write_text("\n".join(stressed) + "\n", encoding="utf-8")
                L.restore_fixed_lines("x", headings, REFRAIN)
                fixed_plain = (Path(folder) / "x.txt").read_text(encoding="utf-8").splitlines()
                fixed_stressed = (Path(folder) / "x.stressed.txt").read_text(encoding="utf-8").splitlines()
                self.assertEqual(fixed_plain[2], headings[0])
                self.assertEqual(fixed_plain[5:7], REFRAIN)
                self.assertEqual(fixed_stressed[5:7], ["Т+ихо плывёт л+одочка.", "Т+ихо течёт рек+а."])
                self.assertEqual(fixed_stressed[11:13], ["Т+ихо плывёт л+одочка.", "Т+ихо течёт рек+а."])
                self.assertEqual(fixed_stressed[2], "# Глав+а 1. Ц+апля")
                self.assertEqual(fixed_stressed[8], "# Глав+а 2. Бобр+ы")
                self.assertEqual(fixed_plain[8], headings[1])
            finally:
                L.STORIES = real

    def test_a_bad_heading_form_is_reported(self):
        text = self.story().replace("# Глава 1. Поворот реки", "Глава 1. Поворот реки", 1)
        self.assertTrue(L.story_problems(text, REFRAIN, 2, "nighttime"))

    def test_a_heading_with_a_word_instead_of_a_number_is_reported(self):
        text = self.story().replace("# Глава 2.", "# Глава два.", 1)
        problems = L.story_problems(text, REFRAIN, 2, "nighttime")
        self.assertTrue(any("bad heading" in p for p in problems), problems)

    def test_headings_out_of_order_are_reported(self):
        text = self.story().replace("# Глава 2.", "# Глава 3.", 1)
        self.assertTrue(any("out of order" in p for p in L.story_problems(text, REFRAIN, 2, "nighttime")))

    def test_a_missing_chapter_is_reported(self):
        self.assertTrue(any("numbered chapters" in p
                            for p in L.story_problems(self.story(), REFRAIN, 3, "nighttime")))

    def test_the_first_line_must_be_the_title(self):
        text = self.story().replace("Лодочка плывёт домой", "# Глава 1. Начало", 1)
        self.assertEqual(L.story_problems(text, REFRAIN, 2, "nighttime"), ["the first line must be the title"])

    def test_a_night_story_fails_the_morning_cue_check(self):
        problems = L.story_problems(self.story(), REFRAIN, 2, "morning")
        self.assertTrue(any("cue" in p for p in problems), problems)

    def test_an_opening_without_a_night_word_is_reported(self):
        lines = chapter()
        opening = ["Река несёт лодочку домой.", "Пик держит тёплый фонарик.",
                   "Фонарик качается и светит.", "Вода поёт под днищем."]
        text = "\n".join(["Лодочка плывёт домой", "", "# Глава 1. Поворот реки"]
                         + opening + [""] + lines[4:] + [""])
        problems = L.story_problems(text, REFRAIN, 1, "nighttime")
        self.assertTrue(any("first eight lines" in p for p in problems), problems)

    def test_chapter_word_counts_come_from_the_body_only(self):
        counts = L.chapter_word_counts(self.story())
        self.assertEqual(len(counts), 2)
        self.assertTrue(all(180 <= count <= 220 for _, count in counts), counts)

    def test_body_words_ignores_headings(self):
        text = self.story()
        self.assertEqual(L.body_words(text.splitlines()[1:]), sum(c for _, c in L.chapter_word_counts(text)))


class StressTests(unittest.TestCase):
    def test_a_clean_pair_passes(self):
        plain = "Тихо плывёт лодочка.\nМышонок Пик смотрит на луну.\n"
        stressed = "Т+ихо плывёт л+одочка.\nМыш+онок Пик см+отрит на лун+у.\n"
        self.assertEqual(L.stress_problems(plain, stressed), [])

    def test_a_missing_mark_is_reported(self):
        problems = L.stress_problems("Мышонок спит.", "Мышонок спит.")
        self.assertTrue(any("expected one stress mark" in p for p in problems), problems)

    def test_a_mark_on_a_word_with_yo_is_reported(self):
        problems = L.stress_problems("Он плывёт.", "Он плыв+ёт.")
        self.assertTrue(any("with ё" in p for p in problems), problems)

    def test_two_marks_are_reported(self):
        problems = L.stress_problems("Лодочка плывёт.", "Л+од+очка плывёт.")
        self.assertTrue(any("expected one stress mark" in p for p in problems), problems)

    def test_a_mark_not_before_a_vowel_is_reported(self):
        problems = L.stress_problems("Мышонок спит.", "Мышонок+ спит.")
        self.assertTrue(any("not before a vowel" in p for p in problems), problems)

    def test_differing_texts_are_reported(self):
        problems = L.stress_problems("Мышонок спит.", "Мыш+онок гул+яет.")
        self.assertTrue(any("texts differ" in p for p in problems), problems)

    def test_differing_line_counts_are_reported(self):
        problems = L.stress_problems("Луна.\nЛуна.\n", "Лун+а.\n")
        self.assertTrue(any("line counts differ" in p for p in problems), problems)

    def test_hand_mark_fills_a_missing_word_and_keeps_the_case(self):
        table = L.correction_map()
        line, missing = L.hand_mark("Т+ихо плывёт Лодочка по реке.", table)
        self.assertIn("Л+одочка", line)
        self.assertIn("рек+е", line)
        self.assertEqual(missing, [])

    def test_hand_mark_reports_an_unknown_word(self):
        line, missing = L.hand_mark("Абракадабра с+ела.", {})
        self.assertEqual(missing, ["Абракадабра"])
        self.assertIn("Абракадабра", line)

    def test_hand_mark_never_marks_a_yo_word_or_a_one_vowel_word(self):
        line, missing = L.hand_mark("Он плывёт в дом.", L.correction_map())
        self.assertEqual(line, "Он плывёт в дом.")
        self.assertEqual(missing, [])

    def test_hand_mark_covers_this_weeks_misses(self):
        table = L.correction_map()
        line, missing = L.hand_mark("+Если они ст+али, Ого, лапкой вздохнул.", table)
        self.assertEqual(missing, [])
        for word in ("Ог+о", "л+апкой", "вздохн+ул"):
            self.assertIn(word, line)


class ResumeTests(unittest.TestCase):
    def records(self):
        return [
            {"stage": "plan", "ok": True, "plan": {"chapters": []}},
            {"stage": "draft", "chapter": 1, "event": "request", "messages": []},
            {"stage": "draft", "chapter": 1, "ok": True, "lines": ["Пик спит."], "facts": ["Пик в лодочке."]},
            {"stage": "draft", "chapter": 2, "event": "check", "ok": False, "problems": ["short"]},
            {"stage": "draft", "chapter": 2, "ok": True, "lines": ["Луна спит."], "facts": []},
        ]

    def test_drafted_chapters_come_from_accepted_records_only(self):
        drafts = L.drafted_chapters(self.records(), set())
        self.assertEqual(sorted(drafts), [1, 2])
        self.assertEqual(drafts[1]["facts"], ["Пик в лодочке."])

    def test_a_failed_attempt_does_not_mark_a_chapter_drafted(self):
        records = [{"stage": "draft", "chapter": 3, "event": "check", "ok": False}]
        self.assertEqual(L.drafted_chapters(records, set()), {})

    def test_redo_drops_a_chapter(self):
        self.assertEqual(sorted(L.drafted_chapters(self.records(), {2})), [1])

    def test_the_latest_accepted_draft_wins(self):
        records = self.records() + [{"stage": "draft", "chapter": 1, "ok": True, "lines": ["Новый текст."]}]
        self.assertEqual(L.drafted_chapters(records, set())[1]["lines"], ["Новый текст."])

    def test_the_plan_is_resumed_from_the_log(self):
        self.assertEqual(L.saved_plan(self.records()), {"chapters": []})

    def test_the_journal_round_trips_and_survives_a_torn_last_line(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "story.writer.jsonl"
            log = L.Log(path)
            for record in self.records():
                log.write(record)
            log.close()
            with path.open("a", encoding="utf-8") as handle:
                handle.write('{"stage": "draft", "chapter": 3, "ok": tr')
            records = L.load_log(path)
            self.assertEqual(len(records), len(self.records()))
            self.assertEqual(sorted(L.drafted_chapters(records, set())), [1, 2])
            self.assertTrue(all("ts" in record for record in records))

    def test_assemble_resumed_chapters_gives_the_contract_layout(self):
        drafts = {n: {"lines": chapter(), "title": "Поворот", "facts": []} for n in (1, 2)}
        text = L.assemble("Лодочка плывёт домой", {"chapters": []}, drafts)
        self.assertEqual(L.story_problems(text, REFRAIN, 2, "nighttime"), [])
        self.assertTrue(text.splitlines()[2].startswith("# Глава 1. "))

    def test_chapter_lines_adds_a_missing_refrain_and_drops_headings(self):
        data = {"paragraphs": [["Пик сидит в лодочке.", "Он смотрит на луну.", "Река поёт."]]}
        lines = L.chapter_lines(data, REFRAIN)
        self.assertEqual(lines[-2:], REFRAIN)
        self.assertEqual(lines[-3], "")

    def test_chapter_lines_replaces_a_wrong_refrain(self):
        data = {"text": "# Глава 1. Поворот\nПик сидит в лодочке.\n\nТихо плывёт лодочка.\nТихо течёт вода."}
        lines = L.chapter_lines(data, REFRAIN)
        self.assertEqual(lines[-2:], REFRAIN)
        self.assertNotIn("Тихо течёт вода.", lines)
        self.assertFalse(any(line.startswith("# ") for line in lines))


class PromptTests(unittest.TestCase):
    def test_the_chapter_prompt_carries_the_window_and_the_refrain(self):
        brief = json.loads((Path(L.BRIEFS) / "lodochka.json").read_text(encoding="utf-8"))
        plan = {"cast": [{"name": "Пик", "kind": "мышонок", "trait": "сонный", "speech": "шёпотом"}],
                "recurring": ["фонарик"], "chapters": [{"title": "Цапля", "beat": "Цапля спит.",
                                                       "quieter": "Цапля закрывает глаза.", "cast": ["Пик"]}]}
        messages = L.chapter_prompt(brief, plan, 1, 180, 220, ["Пик в лодочке."], ["Пик зевнул."], [])
        text = messages[-1]["content"]
        self.assertIn("от 180 до 220 слов", text)
        self.assertIn("Тихо течёт река.", text)
        self.assertIn("Пик в лодочке.", text)
        self.assertIn("Пик зевнул.", text)
        self.assertIn("вечер, ночь, луна, спать", text)

    def test_the_plan_prompt_lists_every_bend(self):
        brief = json.loads((Path(L.BRIEFS) / "lodochka.json").read_text(encoding="utf-8"))
        text = L.plan_prompt(brief, 11)[-1]["content"]
        self.assertEqual(len(brief["bends"]), 11)
        for beat in brief["bends"]:
            self.assertIn(beat, text)


if __name__ == "__main__":
    unittest.main()
