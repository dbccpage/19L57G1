"""The Wiki checker must notice stale boundary teaching assets."""
import json
from pathlib import Path
import tempfile
import unittest
from boundary_lab_wiki import build_boundary_lab, boundary_lab_errors


class BoundaryWikiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.wiki = Path(self.temp.name)
        self.repo = Path(__file__).resolve().parents[2]
        (self.wiki / '_Sidebar.md').write_text('- [Growth lab: commitments, demands, and service](textbook_growth_lab)\n', encoding='utf-8')
        (self.wiki / 'Home.md').write_text('> **See why a settled task can reopen:** Growth lab\n', encoding='utf-8')
        self.assertEqual(build_boundary_lab(self.repo, self.wiki, 'a' * 40), 12)
        self.assertEqual(boundary_lab_errors(self.repo, self.wiki), [])

    def corrupt(self, name, content, message):
        p = self.wiki / name
        before = p.read_bytes()
        p.write_text(content, encoding='utf-8')
        self.assertTrue(any(message in e for e in boundary_lab_errors(self.repo, self.wiki)))
        p.write_bytes(before)
        self.assertEqual(boundary_lab_errors(self.repo, self.wiki), [])

    def test_false_record_is_refused(self):
        p = self.wiki / 'media/boundary_lab/recorded_lab.json'
        data = json.loads(p.read_text(encoding='utf-8'))
        data['control_menu']['010']['satisfies'] = True
        self.corrupt('media/boundary_lab/recorded_lab.json', json.dumps(data), 'stale boundary-lab record')

    def test_unbundled_desk_is_refused(self):
        self.corrupt('media/boundary_lab/results.html', '<html>missing desk</html>', 'stale boundary-lab desk')

    def test_false_figure_is_refused(self):
        self.corrupt('media/boundary_lab/figures/03_fixed_menu.svg', '<svg/>', 'stale boundary-lab figure')

    def test_new_route_links_reach_wiki_lessons(self):
        text = (self.wiki / 'textbook_boundary_lab.md').read_text(encoding='utf-8')
        self.assertIn('](textbook_boundary_lab_practice)', text)
        self.assertIn('](textbook_u37_an_inventory_is_not_a_derivation)', text)
        self.assertNotIn('](../', text)


if __name__ == '__main__':
    unittest.main()
