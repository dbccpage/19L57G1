"""Reject teaching records that conflate membership, closure, and cancellation."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from xml.etree import ElementTree
from unittest.mock import patch

from run_lab import SOURCE, check_recorded, walk_case
from build_results import render


class PathRecords(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('recorded_lab.json', 'SOURCE_MAP.md'):
            shutil.copyfile(SOURCE / name, self.root / name)
        shutil.copytree(SOURCE / 'figures', self.root / 'figures')

    def inject(self, mutation):
        path = self.root / 'recorded_lab.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        mutation(data)
        path.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'differs from the recomputed source-backed cases'):
            check_recorded(self.root)

    def test_missing_edge_does_not_become_a_closed_walk(self):
        self.inject(lambda p: p['walk_cases']['27_1'].update(valid=True, kind='closed'))

    def test_no_face_request_does_not_fill_an_outline(self):
        self.inject(lambda p: p['face_cases']['31_0_1'].update(admitted_faces=[[0, 1, 2]]))

    def test_zero_shared_coefficient_does_not_delete_the_edge(self):
        self.inject(lambda p: p['face_cases']['31_3_1']['after']['1'].remove([0, 2]))

    def test_reversing_one_face_does_not_leave_shared_coefficient_zero(self):
        self.inject(lambda p: p['face_cases']['31_3_-1']['edge_coefficients'][2].update(coefficient=0))

    def test_all_positive_deletion_does_not_inherit_signed_cancellation(self):
        self.inject(lambda p: p['comparisons']['triangle_all_positive'][0].update(coefficient=0))

    def test_population_table_cannot_enlarge_the_checked_case_count(self):
        path = self.root / 'SOURCE_MAP.md'
        path.write_text(path.read_text(encoding='utf-8').replace('| 256 |', '| 999 |'), encoding='utf-8')
        with patch('run_lab.SOURCE', self.root):
            with self.assertRaisesRegex(ValueError, 'population table differs'):
                check_recorded(self.root)

    def test_walk_input_domain_is_declared(self):
        for bad in ((), (-1, 0), (0, 4), (False, 1)):
            with self.assertRaises(ValueError):
                walk_case(31, bad)

    def test_shared_edge_figure_cannot_silently_change_the_coefficient(self):
        path = self.root / 'figures/04_two_faces.svg'
        path.write_text(path.read_text(encoding='utf-8').replace('boundary coefficient: 0.', 'boundary coefficient: 99.'), encoding='utf-8')
        with patch('run_lab.SOURCE', self.root):
            with self.assertRaisesRegex(ValueError, 'figure differs'):
                check_recorded(self.root)

    def test_standalone_desk_is_current(self):
        html = (SOURCE / 'results.html').read_text(encoding='utf-8')
        self.assertEqual(html, render(SOURCE))
        self.assertNotIn('fetch(', html)
        self.assertNotIn('__LAB_PACKET__', html)

    def test_figures_have_readable_intrinsic_dimensions(self):
        figures = list((SOURCE / 'figures').glob('*.svg'))
        self.assertEqual(len(figures), 5)
        for path in figures:
            root = ElementTree.fromstring(path.read_text(encoding='utf-8'))
            self.assertGreaterEqual(int(root.attrib['width']), 440)
            self.assertGreaterEqual(int(root.attrib['height']), 430)


if __name__ == '__main__':
    unittest.main()
