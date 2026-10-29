"""Reject concrete false matching, price, and scope records."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from xml.etree import ElementTree
from run_lab import SOURCE, check_recorded


class IdentificationRecords(unittest.TestCase):
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

    def test_request_alone_is_not_an_answer(self):
        self.inject(lambda p: p['probes']['g00_release_01_mu1'].update(minimum=0))

    def test_rule_does_change_the_third_profile(self):
        self.inject(lambda p: p['paths']['uniform']['first']['diagnostics'].update(third_party_changed=[]))

    def test_two_holes_receive_the_same_datum(self):
        self.inject(lambda p: p['roots']['g05']['released']['answers'][2].__setitem__(0, True))

    def test_non_target_changes_do_not_mean_equal_profiles(self):
        self.inject(lambda p: p['paths']['uniform']['first']['after'].update(collapsed_pairs=[[0, 1], [0, 2]]))

    def test_kept_promises_can_block_a_never_required_pair(self):
        self.inject(lambda p: p['probes']['g05_keep_01_mu1'].update(minimum=1))

    def test_validity_does_not_enforce_the_search_budget(self):
        self.inject(lambda p: p['larger_reply'].update(within_two_item_bound=True))

    def test_separation_pruning_is_not_used_for_matching(self):
        self.inject(lambda p: p['probes']['g05_release_01_mu1'].update(minimum_without_rules=1))

    def test_first_tie_does_not_imply_a_future_tie(self):
        self.inject(lambda p: p['paths']['focused'].update(least_total_items_along_this_choice=2))

    def test_practice_keeps_all_ties_and_protects_z(self):
        p = json.loads((SOURCE / 'recorded_lab.json').read_text(encoding='utf-8'))['practice']
        self.assertEqual(len(p['probe']['responses']), 4)
        self.assertEqual(len(p['promised_probe']['responses']), 3)
        for reply in p['promised_probe']['responses']:
            self.assertEqual(reply['after']['collapsed_pairs'], [[0, 1]])
            self.assertEqual(reply['after']['regime']['reqs'], [[0, 2], [1, 2]])

    def test_changed_practice_count_is_rejected(self):
        self.inject(lambda p: p['practice']['probe'].update(minimum=1))

    def test_population_and_figure_drift_are_rejected(self):
        p = self.root / 'SOURCE_MAP.md'
        p.write_text(p.read_text(encoding='utf-8').replace('| Root pair/setting/measure probes | 24 |',
                                                        '| Root pair/setting/measure probes | 25 |'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'population table differs'):
            check_recorded(self.root)
        shutil.copyfile(SOURCE / 'SOURCE_MAP.md', p)
        p = self.root / 'figures/03_next_step.svg'
        p.write_text('<svg/>', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'figure differs'):
            check_recorded(self.root)

    def test_static_figures_have_accessible_titles(self):
        self.assertEqual(len(list((SOURCE / 'figures').glob('*.svg'))), 4)
        for p in (SOURCE / 'figures').glob('*.svg'):
            root = ElementTree.fromstring(p.read_text(encoding='utf-8'))
            self.assertEqual(root.attrib['width'], '900')
            self.assertIn('viewBox', root.attrib)
            self.assertTrue(root.find('{http://www.w3.org/2000/svg}title').text)


if __name__ == '__main__':
    unittest.main()
