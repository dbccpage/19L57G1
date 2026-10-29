"""Refuse false teaching claims without touching research receipts."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from xml.etree import ElementTree
from run_lab import SOURCE, check_recorded
from build_results import render


class GrowthRecords(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for name in ('recorded_lab.json','SOURCE_MAP.md'):
            shutil.copyfile(SOURCE/name,self.root/name)
        shutil.copytree(SOURCE/'figures',self.root/'figures')

    def inject(self, mutation):
        p=self.root/'recorded_lab.json'
        packet=json.loads(p.read_text(encoding='utf-8'))
        mutation(packet)
        p.write_text(json.dumps(packet),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'differs from recomputed'):
            check_recorded(self.root)

    def test_views_cannot_be_ignored_in_the_counting_claim(self):
        self.inject(lambda p:p['growth_cases']['15_3_total'].update(new_demands=[[4,i] for i in range(4)]))

    def test_growth_does_not_resolve_old_demands(self):
        self.inject(lambda p:p['growth_cases']['15_0_total'].update(after=[]))

    def test_empty_commitment_does_not_acquire_a_demand(self):
        self.inject(lambda p:p['growth_cases']['15_0_empty'].update(new_demands=[[4,0]]))

    def test_quiet_does_not_mean_closed_under_all_growth(self):
        self.inject(lambda p:p['growth_cases']['15_3_total'].update(reopens=False))

    def test_unused_service_capacity_cannot_be_saved(self):
        self.inject(lambda p:p['races']['bounded_8_1']['log'][3].update(backlog=2))

    def test_final_clear_does_not_mean_every_round_was_clear(self):
        self.inject(lambda p:p['races']['bounded_8_1'].update(max_backlog=0))

    def test_peak_is_not_a_general_threshold_formula(self):
        self.inject(lambda p:p['thresholds']['bounded_8'].update(least_final_clearing_rate=3))

    def test_population_cannot_be_enlarged_by_editing_prose(self):
        p=self.root/'SOURCE_MAP.md'
        p.write_text(p.read_text(encoding='utf-8').replace('| 845 |','| 999 |'),encoding='utf-8')
        with patch('run_lab.SOURCE',self.root):
            with self.assertRaisesRegex(ValueError,'population table differs'):
                check_recorded(self.root)

    def test_figure_cannot_erase_a_backlog(self):
        p=self.root/'figures/03_bounded_clears.svg'
        p.write_text(p.read_text(encoding='utf-8').replace('>3</text>','>99</text>'),encoding='utf-8')
        with patch('run_lab.SOURCE',self.root):
            with self.assertRaisesRegex(ValueError,'figure differs'):
                check_recorded(self.root)

    def test_standalone_desk_is_current_and_has_no_runtime_fetch(self):
        html=(SOURCE/'results.html').read_text(encoding='utf-8')
        self.assertEqual(html,render(SOURCE))
        self.assertNotIn('fetch(',html)
        self.assertNotIn('__LAB_PACKET__',html)

    def test_static_figures_have_explicit_readable_dimensions(self):
        paths=list((SOURCE/'figures').glob('*.svg'))
        self.assertEqual(len(paths),4)
        for p in paths:
            svg=ElementTree.fromstring(p.read_text(encoding='utf-8'))
            self.assertGreaterEqual(int(svg.attrib['width']),640)
            self.assertGreaterEqual(int(svg.attrib['height']),360)


if __name__=='__main__':
    unittest.main()
