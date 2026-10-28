"""Authoring failures that would misteach scope or quantifier order."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from run_lab import SOURCE, check_population, check_recorded
from build_results import render


class ReasoningRecords(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copyfile(SOURCE / 'recorded_lab.json', self.root / 'recorded_lab.json')
        shutil.copyfile(SOURCE / 'SOURCE_MAP.md', self.root / 'SOURCE_MAP.md')

    def inject(self, mutate):
        path = self.root / 'recorded_lab.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        mutate(data)
        path.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'differs from the recomputed examples'):
            check_recorded(self.root)

    def test_reverse_is_not_adopted_from_the_forward_direction(self):
        self.inject(lambda d: d['claims']['7_0_1_0_if'].update(holds=True))

    def test_empty_every_does_not_create_a_some_witness(self):
        self.inject(lambda d: d['claims']['0_0_1_0_if'].update(some_first=True))

    def test_pairwise_witnesses_do_not_become_a_common_witness(self):
        self.inject(lambda d: d['families']['7_5'].update(one_question_for_all=True))

    def test_removing_the_blocking_pair_does_not_make_a_recovery_function(self):
        self.inject(lambda d: d['recovery_blue_to_round']['7'].update(blocking_pairs=[]))

    def test_desk_is_current_and_self_contained(self):
        html = (SOURCE / 'results.html').read_text(encoding='utf-8')
        self.assertEqual(html, render(SOURCE))
        self.assertNotIn('__LAB_PACKET__', html)
        self.assertNotIn('fetch(', html)

    def test_source_map_does_not_enlarge_the_checked_population(self):
        path = self.root / 'SOURCE_MAP.md'
        path.write_text(path.read_text(encoding='utf-8').replace('| 147456 |', '| 999999 |'), encoding='utf-8')
        with patch('run_lab.SOURCE', self.root):
            with self.assertRaisesRegex(ValueError, 'population table differs'):
                check_population()


if __name__ == '__main__':
    unittest.main()
