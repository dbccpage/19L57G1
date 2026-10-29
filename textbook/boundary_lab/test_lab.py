"""Defect-sensitive checks for teaching records; AuthorityEffect: None."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from xml.etree import ElementTree
from run_lab import SOURCE, check_recorded
from build_results import render


class BoundaryRecords(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('recorded_lab.json', 'SOURCE_MAP.md'):
            shutil.copyfile(SOURCE / name, self.root / name)
        shutil.copytree(SOURCE / 'figures', self.root / 'figures')

    def inject(self, mutate):
        p = self.root / 'recorded_lab.json'
        packet = json.loads(p.read_text(encoding='utf-8'))
        mutate(packet)
        p.write_text(json.dumps(packet), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'differs from recomputed'):
            check_recorded(self.root)

    def test_empty_reports_do_not_block_a_swap(self):
        self.inject(lambda p: p['report_cases']['0'].update(swap_preserves_all=False))

    def test_unequal_answer_is_not_erased(self):
        self.inject(lambda p: p['report_cases']['4'].update(breaking_witnesses=[]))

    def test_names_are_admitted_in_O_not_U(self):
        self.inject(lambda p: p['boundary_cases']['U_'].update(names=[True, True]))

    def test_restricting_permission_is_not_a_new_label(self):
        self.inject(lambda p: p['control_menu']['100'].update(labels=['a', 'b']))

    def test_equal_labels_still_allow_exchange(self):
        self.inject(lambda p: p['control_menu']['010'].update(automorphisms=[[0, 1]], satisfies=True))

    def test_bundles_are_not_single_step_candidates(self):
        self.inject(lambda p: p['control_menu']['111'].update(eligible=True))

    def test_primary_does_not_replace_the_secondary_question(self):
        self.inject(lambda p: p['secondary_minimum'].update(minimum=1))

    def test_changed_label_example_uses_all_marks(self):
        packet = json.loads((SOURCE / 'recorded_lab.json').read_text(encoding='utf-8'))
        row = packet['transfer_cases']['aab_11_arity']
        self.assertEqual(row['automorphisms'], [[0, 1, 2], [1, 0, 2]])
        self.assertEqual(row['separated_pairs'], [[0, 2], [1, 2]])

    def test_population_and_figure_drift_are_rejected(self):
        p = self.root / 'SOURCE_MAP.md'
        p.write_text(p.read_text(encoding='utf-8').replace('| Report subsets | 16 |',
                                                       '| Report subsets | 17 |'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'population table differs'):
            check_recorded(self.root)
        shutil.copyfile(SOURCE / 'SOURCE_MAP.md', p)
        p = self.root / 'figures/03_fixed_menu.svg'
        p.write_text(p.read_text(encoding='utf-8').replace('>1</text>', '>99</text>'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'figure differs'):
            check_recorded(self.root)

    def test_bundle_and_figures_are_readable_standalone_assets(self):
        html = (SOURCE / 'results.html').read_text(encoding='utf-8')
        self.assertEqual(html, render(SOURCE))
        self.assertNotIn('fetch(', html)
        self.assertNotIn('__DESK_SCRIPT__', html)
        self.assertNotIn('__LAB_PACKET__', html)
        for p in (SOURCE / 'figures').glob('*.svg'):
            root = ElementTree.fromstring(p.read_text(encoding='utf-8'))
            self.assertEqual(root.attrib['width'], '900')
            self.assertIn('viewBox', root.attrib)
            self.assertTrue(root.find('{http://www.w3.org/2000/svg}title').text)

    def test_actual_javascript_looks_up_all_recorded_settings(self):
        node = shutil.which('node')
        self.assertIsNotNone(node, 'Node is needed to check the desk')
        subprocess.run([node, str(SOURCE / 'test_desk.cjs')], check=True)


if __name__ == '__main__':
    unittest.main()
