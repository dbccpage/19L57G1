"""Reject stale numerical teaching pages and assets."""
from pathlib import Path
import tempfile
import unittest
from number_lab_wiki import build_number_lab, number_lab_errors


class NumberWikiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.wiki = Path(self.temp.name)
        self.repo = Path(__file__).resolve().parents[2]
        (self.wiki/'_Sidebar.md').write_text('- [Same-record lab: equal profiles, distinct positions](textbook_identification_lab)\n', encoding='utf-8')
        (self.wiki/'Home.md').write_text('> **Match answers without merging things:** Same-record lab\n', encoding='utf-8')
        self.assertEqual(build_number_lab(self.repo, self.wiki, 'a'*40), 14)
        self.assertEqual(number_lab_errors(self.repo, self.wiki), [])

    def corrupt(self, name, text, message):
        p = self.wiki/name; original = p.read_bytes()
        p.write_text(text, encoding='utf-8')
        self.assertTrue(any(message in e for e in number_lab_errors(self.repo, self.wiki)))
        p.write_bytes(original)
        self.assertEqual(number_lab_errors(self.repo, self.wiki), [])

    def test_false_reading_is_rejected(self):
        p = self.wiki/'textbook_number_lab_05_two_coordinates.md'
        self.corrupt(p.name, p.read_text(encoding='utf-8').replace('with weight 2.', 'with weight 9.'), 'stale number-lab page')

    def test_invalid_json_is_rejected(self):
        self.corrupt('media/number_lab/recorded_lab.json', '{bad', 'stale number-lab record')

    def test_missing_figure_is_rejected(self):
        self.corrupt('media/number_lab/figures/02_coordinate_readings.svg', '<svg/>', 'stale number-lab figure')

    def test_missing_page_is_rejected(self):
        (self.wiki/'textbook_number_lab_practice.md').unlink()
        self.assertTrue(any('missing number-lab page' in e for e in number_lab_errors(self.repo, self.wiki)))

    def test_prerequisites_unit_and_answers_reach_wiki(self):
        body = (self.wiki/'textbook_number_lab.md').read_text(encoding='utf-8')
        for slug in ('first_steps', 'reasoning_lab', 'map_lab', 'u64_a_profile_without_division', 'number_lab_answers'):
            self.assertIn(f'](textbook_{slug})', body)
        self.assertNotIn('](../', body)


if __name__ == '__main__':
    unittest.main()
