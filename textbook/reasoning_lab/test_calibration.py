"""Calibration premise boundaries and stale teaching artifacts."""
from fractions import Fraction as F
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from textbook.reasoning_lab import calibration as c


class CalibrationPremises(unittest.TestCase):
    def test_native_unchecked_cases_remain_visible(self):
        self.assertEqual(c.native_limits()['raw_zero_standard_error'],'ZeroDivisionError')

    def test_wrong_positive_scale_is_not_a_conversion(self):
        q=c.quantity(6,c.STANDARDS[1])
        with self.assertRaisesRegex(ValueError,'Scale must match'):c.convert(q,c.STANDARDS[2],F(1,2))

    def test_zero_or_negative_standard_is_rejected(self):
        for base in (F(0),F(-1)):
            s=c.native.CalibrationStandard('bad',c.DIM.LENGTH,base)
            with self.assertRaisesRegex(ValueError,'positive standards'):c.quantity(1,s)

    def test_mismatched_kind_metadata_is_rejected(self):
        t=c.native.CalibrationStandard('T',c.DIM.DURATION,F(1))
        q=c.native.RelationalQuantity(F(1),c.DIM.LENGTH,t)
        with self.assertRaisesRegex(ValueError,'kind'):c.check_quantity(q)

    def test_mixed_standards_need_conversion_before_division(self):
        a=c.quantity(6,c.STANDARDS[1]);b=c.quantity(18,c.STANDARDS[0])
        self.assertEqual(c.ratio(a,b).unwrap(),F(2,3))
        self.assertNotEqual(a.value/b.value,F(2,3))

    def test_zero_numerator_and_zero_divisor_differ(self):
        zero=c.quantity(0,c.STANDARDS[1]);one=c.quantity(1,c.STANDARDS[1])
        self.assertEqual(c.ratio(zero,one).unwrap(),0)
        self.assertTrue(c.ratio(one,zero).is_err())

    def test_declared_population(self):
        self.assertEqual(c.check_population(),{'conversions':384,'same_kind_ratios':2304,'common_rescalings':9216,'cross_kind_refusals':6912})

    def test_actual_handlers(self):
        p=subprocess.run(['node',str(c.SOURCE/'test_calibration_controls.mjs')],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)


class CalibrationRecords(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.folder=Path(self.temp.name)
        for name in ('calibration.json','calibration.html'):shutil.copyfile(c.SOURCE/name,self.folder/name)

    def inject(self,mutate):
        p=self.folder/'calibration.json';d=json.loads(p.read_text(encoding='utf-8'));mutate(d);p.write_text(json.dumps(d),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'packet differs'):c.check_recorded(self.folder)

    def test_larger_unit_does_not_increase_number(self):
        self.inject(lambda d:d['conversions']['0_2'].update(answer='12'))

    def test_raw_numbers_do_not_give_mixed_unit_ratio(self):
        self.inject(lambda d:d['comparisons'][1].update(answer='1/3'))

    def test_ratio_agreement_does_not_fix_magnitude(self):
        self.inject(lambda d:d['comparisons'][5]['first'].update(magnitude='12'))

    def test_observation_count_is_zero(self):
        self.inject(lambda d:d.update(physical_observations=9))

    def test_stale_desk_rejected(self):
        p=self.folder/'calibration.html';p.write_text(p.read_text(encoding='utf-8')+'stale',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'desk differs'):c.check_recorded(self.folder)


if __name__=='__main__':unittest.main()
