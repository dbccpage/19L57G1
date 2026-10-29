"""Notice false lessons and stale same-record Wiki assets."""
from pathlib import Path
import tempfile
import unittest
from identification_lab_wiki import build_identification_lab, identification_lab_errors


class IdentificationWikiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.wiki = Path(self.temp.name)
        self.repo = Path(__file__).resolve().parents[2]
        (self.wiki / '_Sidebar.md').write_text('- [Boundary lab: reports, swaps, and declared prices](textbook_boundary_lab)\n', encoding='utf-8')
        (self.wiki / 'Home.md').write_text('> **Ask why an exchange fails:** Boundary lab\n', encoding='utf-8')
        self.assertEqual(build_identification_lab(self.repo, self.wiki, 'a' * 40), 12)
        self.assertEqual(identification_lab_errors(self.repo, self.wiki), [])

    def corrupt(self, name, content, message):
        p = self.wiki / name
        before = p.read_bytes()
        p.write_text(content, encoding='utf-8')
        self.assertTrue(any(message in e for e in identification_lab_errors(self.repo, self.wiki)))
        p.write_bytes(before)
        self.assertEqual(identification_lab_errors(self.repo, self.wiki), [])

    def test_invalid_record_is_refused(self):
        self.corrupt('media/identification_lab/recorded_lab.json', '{broken', 'stale same-record record')

    def test_false_figure_is_refused(self):
        self.corrupt('media/identification_lab/figures/02_three_additions.svg', '<svg/>', 'stale same-record figure')

    def test_false_price_in_lesson_is_refused(self):
        p = self.wiki / 'textbook_identification_lab_04_price_the_next_step.md'
        self.corrupt(p.name, p.read_text(encoding='utf-8').replace('**three**', '**one**'), 'stale same-record page')

    def test_missing_page_is_refused(self):
        (self.wiki / 'textbook_identification_lab_practice.md').unlink()
        self.assertTrue(any('missing same-record page' in e for e in identification_lab_errors(self.repo, self.wiki)))

    def test_prerequisites_and_answers_stay_on_wiki(self):
        text = (self.wiki / 'textbook_identification_lab.md').read_text(encoding='utf-8')
        for slug in ('first_steps', 'reasoning_lab', 'search_lab', 'map_lab', 'identification_lab_answers'):
            self.assertIn(f'](textbook_{slug})', text)
        self.assertNotIn('](../', text)


if __name__ == '__main__':
    unittest.main()
