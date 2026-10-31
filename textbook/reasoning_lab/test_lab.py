"""Authoring failures that would misteach scope or quantifier order."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from run_lab import SOURCE, check_population, check_recorded
from build_results import render
from textbook.reasoning_lab import evidence


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

    def test_fictional_records_cannot_be_published_as_measurements(self):
        self.inject(lambda d: d['evidence'].update(physical_observations_recorded=12))

    def test_repeat_disagreement_is_retained_in_the_packet(self):
        self.inject(lambda d: d['evidence'].update(repeat_conflicts=[]))


class EvidenceScope(unittest.TestCase):
    @unittest.skipUnless(shutil.which('node'), 'Node is needed for the event-handler unit check')
    def test_actual_evidence_event_handlers(self):
        proc = subprocess.run(['node', str(SOURCE / 'test_evidence_controls.mjs')],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_partial_answers_match_independent_boolean_completions(self):
        self.assertEqual(evidence.check_evidence_population(), {
            'partial_answer_pairs': 9, 'scoped_comparisons': 72,
            'fictional_logs': 12, 'physical_observations_recorded': 0})

    def test_question_mark_cannot_become_no(self):
        with patch.dict(evidence.CODES, {'?': False}):
            with self.assertRaises(AssertionError):
                evidence.check_evidence_population()

    def test_scope_and_protocol_cannot_be_silently_repaired(self):
        original = evidence.classify
        def widened(row):
            return original({**row, 'card': 'K', 'protocol': 'P1', 'condition': 'front-desk'})
        with patch.object(evidence, 'classify', widened):
            with self.assertRaises(AssertionError):
                evidence.check_evidence_population()

    def test_dropping_the_counterexample_is_not_a_passing_update(self):
        rows = [r for r in evidence.supplied_records() if r['id'] != 'new-N']
        with patch.object(evidence, 'supplied_records', lambda: rows):
            with self.assertRaises(AssertionError):
                evidence.build_evidence_packet()

    def test_repeats_are_compared_without_mutating_or_averaging_rows(self):
        rows = evidence.supplied_records()
        before = json.loads(json.dumps(rows))
        self.assertEqual(evidence.repeat_conflicts(rows), [
            {'records': ['new-N', 'repeat-N'], 'changed': ['crease']}])
        self.assertEqual(rows, before)

    def test_bad_codes_and_origin_fail_closed(self):
        for updates in ({'origin': 'measured'}, {'dot': False}, {'crease': ''}, {'dot': 'unknown'}):
            with self.subTest(updates=updates), self.assertRaises(ValueError):
                evidence.classify({**evidence.supplied_records()[0], **updates})


if __name__ == '__main__':
    unittest.main()
