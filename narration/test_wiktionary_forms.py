import unittest

import wiktionary_forms as W

PAGE = """
<table class="wikitable"><tr><th>падеж</th><th>ед. ч.</th><th>мн. ч.</th></tr>
<tr><td>Им.</td><td>у́шко</td><td>у́шки</td></tr>
<tr><td>Р.</td><td>у́шка</td><td>у́шек</td></tr></table>
<table><tr><td>no stress mark here</td></tr></table>
<table><tr><td>Им.</td><td>нача́лся́<br>начали́сь</td></tr>
<tr><td><table><tr><td>nested table is part of this cell</td></tr></table></td><td>x</td></tr></table>
"""


class TableReaderTests(unittest.TestCase):
    def test_only_tables_with_a_stress_mark_are_kept(self):
        tables = W.stressed_tables(PAGE)
        self.assertEqual(2, len(tables))
        self.assertEqual(["падеж ед. ч. мн. ч.", "Им. у́шко у́шки", "Р. у́шка у́шек"], tables[0])

    def test_a_line_break_inside_a_cell_becomes_a_space_and_a_nested_table_stays_inside(self):
        second = W.stressed_tables(PAGE)[1]
        self.assertEqual("Им. нача́лся́ начали́сь", second[0])
        self.assertEqual(2, len(second))

    def test_a_page_without_accents_gives_nothing(self):
        self.assertEqual([], W.stressed_tables("<table><tr><td>слово</td></tr></table>"))


if __name__ == "__main__":
    unittest.main()
