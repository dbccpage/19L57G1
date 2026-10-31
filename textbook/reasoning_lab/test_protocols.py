"""Reject operational-protocol teaching errors and stale artifacts."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from textbook.reasoning_lab import protocols


class ProtocolRecords(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        for name in ('protocols.json','protocols.html'):
            shutil.copyfile(protocols.SOURCE/name,self.root/name)

    def inject(self,mutate):
        path=self.root/'protocols.json';data=json.loads(path.read_text(encoding='utf-8'))
        mutate(data);path.write_text(json.dumps(data),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'packet differs'):
            protocols.check_recorded(self.root)

    def test_target_update_does_not_refresh_record(self):
        self.inject(lambda d:d['histories']['3_0_1']['end'].update(r1=2))

    def test_coarse_record_agreement_does_not_equal_targets(self):
        self.inject(lambda d:d['histories']['2_2_4'].update(targets_match=True))

    def test_non_disturbing_does_not_mean_any_order(self):
        self.inject(lambda d:d['orders']['0_0_0'].update(commutes=True))

    def test_equal_diagnostics_do_not_restore_commutation(self):
        self.inject(lambda d:d['orders']['0_0_4'].update(commutes=True))

    def test_overlap_does_not_force_noncommutation(self):
        self.inject(lambda d:d['orders']['0_0_5'].update(commutes=False))

    def test_footprint_labels_are_not_behavior_proofs(self):
        self.inject(lambda d:d['scope_controls'].update(footprint_labels_alone_prove_commutation=True))

    def test_instrument_flag_does_not_prove_target_unchanged(self):
        self.inject(lambda d:d['scope_controls'].update(instrument_flag_alone_proves_target_unchanged=True))

    def test_zero_diagnostic_does_not_prove_target_unchanged(self):
        self.inject(lambda d:d['scope_controls'].update(zero_diagnostic_proves_target_unchanged=True))

    def test_formal_fields_are_not_declared_finite(self):
        self.inject(lambda d:d.update(formal_carrier='six bounded fields'))

    def test_model_preparations_are_not_observations(self):
        self.inject(lambda d:d.update(physical_observations=4))

    def test_agreement_change_does_not_change_remote_counts(self):
        self.inject(lambda d:d['ensembles']['0'].update(remote_counts_after={'1':'1'}))

    def test_protocol_desk_is_current(self):
        path=self.root/'protocols.html';path.write_text(path.read_text(encoding='utf-8')+'stale',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'desk differs'):
            protocols.check_recorded(self.root)

    def test_declared_bounded_population(self):
        self.assertEqual(protocols.check_population(),23328)

    def test_changed_practice_and_empty_list_scope(self):
        data=protocols.build_packet()
        self.assertEqual(data['practice']['stale']['end']['r1'],2)
        self.assertEqual(data['practice']['relay']['end']['r2'],1)
        self.assertEqual(data['practice']['counts']['remote_counts_after'],{'0':'1/3','2':'2/3'})
        empty=protocols.ensemble(lambda n:n,())
        self.assertEqual(empty['supplied_rows'],0)
        self.assertEqual(empty['remote_counts_before'],{})
        self.assertEqual(empty['physical_observations'],0)

    def test_actual_protocol_handlers(self):
        proc=subprocess.run(['node',str(protocols.SOURCE/'test_protocol_controls.mjs')],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)


if __name__=='__main__':unittest.main()
