import unittest

import bedtime


def chapters(text: str) -> list[dict]:
    """Each [CHAPTER] block of the metadata as a dict."""
    out = []
    for block in text.split("[CHAPTER]")[1:]:
        out.append(dict(line.split("=", 1) for line in block.strip().splitlines()))
    return out


class ChapterMetadataTests(unittest.TestCase):
    def test_each_chapter_ends_where_the_next_starts_and_the_last_ends_with_the_book(self):
        text = bedtime.chapter_metadata("Book", [("One", 0.0), ("Two", 60.5), ("Three", 100.0)], 130.25)
        got = chapters(text)
        self.assertEqual([("0", "60500"), ("60500", "100000"), ("100000", "130250")],
                         [(c["START"], c["END"]) for c in got])

    def test_no_chapter_is_one_second_long(self):
        got = chapters(bedtime.chapter_metadata("Book", [("One", 0.0), ("Two", 600.0)], 1200.0))
        self.assertEqual([600000, 600000], [int(c["END"]) - int(c["START"]) for c in got])

    def test_one_chapter_runs_to_the_end(self):
        got = chapters(bedtime.chapter_metadata("Book", [("Only", 0.0)], 42.0))
        self.assertEqual("42000", got[0]["END"])

    def test_ffmpeg_special_characters_in_a_title_are_escaped(self):
        text = bedtime.chapter_metadata("A=B", [("Chapter #1; part=2\\", 0.0)], 10.0)
        self.assertIn("title=A\\=B", text)
        self.assertIn("title=Chapter \\#1\\; part\\=2\\\\", text)
        self.assertTrue(text.startswith(";FFMETADATA1\n"))

    def test_a_newline_in_a_title_cannot_start_a_new_metadata_line(self):
        text = bedtime.chapter_metadata("Book", [("Line one\nline two", 0.0)], 10.0)
        self.assertEqual(1, text.count("[CHAPTER]"))
        self.assertIn("Line one\\\nline two", text)


if __name__ == "__main__":
    unittest.main()
