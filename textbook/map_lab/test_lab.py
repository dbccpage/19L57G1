"""Reject misleading finite map/lookup teaching records."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from xml.etree import ElementTree

from run_lab import SOURCE, check_recorded
from build_results import render


class MapRecords(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('recorded_lab.json','SOURCE_MAP.md'):
            shutil.copyfile(SOURCE/name, self.root/name)
        shutil.copytree(SOURCE/'figures', self.root/'figures')

    def inject(self, mutation):
        path=self.root/'recorded_lab.json'
        data=json.loads(path.read_text(encoding='utf-8'))
        mutation(data)
        path.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'differs from the source-backed computations'):
            check_recorded(self.root)

    def test_shortened_domain_is_not_reindexed_as_original_positions(self):
        self.inject(lambda p:p['cases']['10_1_0_0'].update(presentation=[1,3]))

    def test_new_representative_does_not_restore_the_blocked_target(self):
        self.inject(lambda p:p['cases']['15_1_1_1'].update(recoverable=True))

    def test_paired_answer_cannot_use_only_the_successful_component(self):
        self.inject(lambda p:p['cases']['15_1_2_0'].update(recoverable=True))

    def test_unused_labels_prevent_a_false_global_uniqueness_count(self):
        self.inject(lambda p:p['cases']['15_1_0_0'].update(full_lookup_count=1))

    def test_empty_domain_does_not_supply_a_class(self):
        self.inject(lambda p:p['cases']['0_0_0_0'].update(groups=[{'representative':0,'members':[]}]))

    def test_population_table_is_not_enlarged(self):
        path=self.root/'SOURCE_MAP.md'
        path.write_text(path.read_text(encoding='utf-8').replace('| 512 |','| 999 |'),encoding='utf-8')
        with patch('run_lab.SOURCE',self.root):
            with self.assertRaisesRegex(ValueError,'population table differs'):
                check_recorded(self.root)

    def test_figure_conflicts_cannot_be_silently_drawn_as_solid_lookup_arrows(self):
        path=self.root/'figures/02_block_triangle.svg'
        path.write_text(path.read_text(encoding='utf-8').replace('stroke-dasharray="9 6"','stroke-dasharray="none"'),encoding='utf-8')
        with patch('run_lab.SOURCE',self.root):
            with self.assertRaisesRegex(ValueError,'figure differs'):
                check_recorded(self.root)

    def test_figures_declare_intrinsic_dimensions(self):
        paths=list((SOURCE/'figures').glob('*.svg'))
        self.assertEqual(len(paths),5)
        for path in paths:
            root=ElementTree.fromstring(path.read_text(encoding='utf-8'))
            self.assertGreaterEqual(int(root.attrib['width']),640)
            self.assertGreaterEqual(int(root.attrib['height']),640)

    def test_complete_lookup_examples_obey_each_selected_task(self):
        data=json.loads((SOURCE/'recorded_lab.json').read_text(encoding='utf-8'))
        for row in data['cases'].values():
            for g in row['full_lookup_examples']:
                self.assertEqual(len(g),4)
                self.assertTrue(all(g[row['presentation'][i]]==row['requested'][i] for i in row['domain']))

    def test_single_file_desk_is_current(self):
        text=(SOURCE/'results.html').read_text(encoding='utf-8')
        self.assertEqual(text,render(SOURCE))
        self.assertNotIn('fetch(',text)
        self.assertNotIn('__LAB_PACKET__',text)


if __name__=='__main__':
    unittest.main()
