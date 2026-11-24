import tempfile
import unittest
from pathlib import Path

import story_modes as M

NIGHT = "Лунный зайчик\nНад лесом поднялась луна.\nВсе звери легли спать в тёмном лесу."
MORNING = "Утренний петух\nВстало солнце, запел петух.\nПора вставать и завтракать, уже утро."


class CueTests(unittest.TestCase):
    def test_night_text_scores_night(self):
        cues = M.cue_score(NIGHT)
        self.assertGreater(cues["nighttime"], cues["morning"])

    def test_morning_text_scores_morning(self):
        cues = M.cue_score(MORNING)
        self.assertGreater(cues["morning"], cues["nighttime"])

    def test_stress_marks_do_not_hide_cues(self):
        stressed = "Л+унный з+айчик\nНад л+есом подн+ялась лун+а.\nВс+е зв+ери л+егли сп+ать в т+ёмном л+есу."
        self.assertEqual(M.cue_score(stressed), M.cue_score(M.strip_marks(stressed)))
        self.assertGreater(M.cue_score("В+ечер. Т+ихий в+ечер.")["nighttime"], 0)


class ResolveTests(unittest.TestCase):
    def registry(self, **entry):
        return {"s": {"mode": "nighttime", "why": "the moon rises and the animals sleep", **entry}}

    def test_registry_entry_is_used(self):
        got = M.resolve("s", NIGHT, self.registry())
        self.assertEqual("nighttime", got["mode"])
        self.assertEqual("registry", got["source"])

    def test_missing_entry_fails(self):
        with self.assertRaises(M.ModeError):
            M.resolve("s", NIGHT, {})

    def test_short_reason_fails(self):
        with self.assertRaises(M.ModeError):
            M.resolve("s", NIGHT, {"s": {"mode": "nighttime", "why": "night"}})

    def test_registry_against_the_cues_fails(self):
        with self.assertRaises(M.ModeError):
            M.resolve("s", MORNING, self.registry())

    def test_no_cues_anywhere_fails(self):
        with self.assertRaises(M.ModeError):
            M.resolve("s", "Заголовок\nПросто строка без примет.", self.registry())

    def test_narrow_margin_still_passes(self):
        text = "Заголовок\nВстало солнце, и петух запел."
        got = M.resolve("s", text, {"s": {"mode": "morning", "why": "the sun comes up and the rooster sings"}})
        self.assertEqual("morning", got["mode"])

    def test_override_skips_the_registry(self):
        got = M.resolve("s", MORNING, {}, override="morning")
        self.assertEqual("morning", got["mode"])
        self.assertEqual("override", got["source"])

    def test_morning_mode_matches_morning_cues(self):
        got = M.resolve("s", MORNING, {"s": {"mode": "morning", "why": "the sun comes up and the rooster sings"}})
        self.assertEqual("morning", got["mode"])


class BedTests(unittest.TestCase):
    def test_missing_bed_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(M.ModeError):
                M.bed_for("nighttime", {"bed": "night-bed.wav"}, Path(folder))

    def test_changed_bed_fails_and_matches(self):
        with tempfile.TemporaryDirectory() as folder:
            bed = Path(folder) / "night-bed.wav"
            bed.write_bytes(b"x")
            self.assertEqual(bed, M.bed_for("nighttime", {"bed": "night-bed.wav", "bed_sha256": M.sha256(bed)}, Path(folder)))
            with self.assertRaises(M.ModeError):
                M.bed_for("nighttime", {"bed": "night-bed.wav", "bed_sha256": "0" * 64}, Path(folder))


class RegistryFileTests(unittest.TestCase):
    def test_every_story_has_a_checked_entry(self):
        here = Path(__file__).resolve().parent
        registry = M.load_registry(here / "stories/modes.json")
        stories = sorted(p.name.replace(".stressed.txt", "") for p in (here / "stories").glob("*.stressed.txt"))
        self.assertTrue(stories)
        for story in stories:
            text = (here / "stories" / f"{story}.stressed.txt").read_text(encoding="utf-8")
            got = M.resolve(story, text, registry)
            self.assertIn(got["mode"], M.MODE_NAMES)

    def test_stories_and_their_plain_twins_agree(self):
        here = Path(__file__).resolve().parent
        for stressed in (here / "stories").glob("*.stressed.txt"):
            plain = stressed.with_name(stressed.name.replace(".stressed.txt", ".txt"))
            self.assertEqual(M.strip_marks(stressed.read_text(encoding="utf-8")),
                             plain.read_text(encoding="utf-8"), stressed.name)


if __name__ == "__main__":
    unittest.main()