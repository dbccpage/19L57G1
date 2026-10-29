"""Detect false numerical, domain, and information claims."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from xml.etree import ElementTree
from run_lab import SOURCE, check_recorded


class NumberRecords(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('recorded_lab.json', 'SOURCE_MAP.md'):
            shutil.copyfile(SOURCE/name, self.root/name)
        shutil.copytree(SOURCE/'figures', self.root/'figures')

    def inject(self, mutate):
        p = self.root/'recorded_lab.json'
        data = json.loads(p.read_text(encoding='utf-8'))
        mutate(data)
        p.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'differs from recomputed'):
            check_recorded(self.root)

    def test_equal_proportions_do_not_preserve_total(self):
        self.inject(lambda p: p['shares_example'].update(totals=[5, 5]))

    def test_zero_total_has_no_fractional_share(self):
        self.inject(lambda p: p['proportion_cases'][0].update(positive_share_match=True))

    def test_zero_box_does_not_test_the_general_invariance(self):
        self.inject(lambda p: p['bounded_descent'].update(zero_box=False))

    def test_sign_loss_does_not_determine_combined_reading(self):
        self.inject(lambda p: next(r for r in p['signed_cases'] if r['inputs']==[1, -1]).update(readout=4))

    def test_vertical_input_has_a_middle_reading(self):
        self.inject(lambda p: p['coordinate_instance'][1].update(readout=4))

    def test_information_is_class_count_not_input_count(self):
        self.inject(lambda p: p['domain_cases'][-1].update(information_before=3))

    def test_domain_restriction_can_change_determination(self):
        self.inject(lambda p: p['domain_cases'][1].update(knows=False))

    def test_reversal_can_pair_two_different_positions(self):
        self.inject(lambda p: p['loops'][3].update(maximum_distinct=4))

    def test_five_positions_do_not_force_five_readings(self):
        self.inject(lambda p: p['loops'][4].update(groups=[[0], [1], [2], [3], [4]]))

    def test_doubling_coordinates_scales_squares_by_four(self):
        self.inject(lambda p: p['practice_coordinates'][0].update(readout=8))

    def test_population_and_figure_drift_are_detected(self):
        p = self.root/'SOURCE_MAP.md'
        p.write_text(p.read_text(encoding='utf-8').replace('| Coordinate input pairs | 2401 |',
                                                        '| Coordinate input pairs | 2402 |'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'population table differs'):
            check_recorded(self.root)
        shutil.copyfile(SOURCE/'SOURCE_MAP.md', p)
        (self.root/'figures/02_coordinate_readings.svg').write_text('<svg/>', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'figure differs'):
            check_recorded(self.root)

    def test_all_figures_have_accessible_titles(self):
        files = list((SOURCE/'figures').glob('*.svg'))
        self.assertEqual(len(files), 5)
        for p in files:
            root = ElementTree.fromstring(p.read_text(encoding='utf-8'))
            self.assertEqual(root.attrib['width'], '900')
            self.assertIn('viewBox', root.attrib)
            self.assertTrue(root.find('{http://www.w3.org/2000/svg}title').text)


if __name__ == '__main__':
    unittest.main()
