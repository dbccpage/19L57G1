"""Exact historical exceptions must not become a live isolation carve."""
import importlib.util
from pathlib import Path
import unittest
from unittest import mock

_path = Path(__file__).resolve().parents[1] / "research/side_free/tests/test_isolation.py"
_spec = importlib.util.spec_from_file_location("_side_free_isolation", _path)
assert _spec is not None and _spec.loader is not None
sf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sf)


class HistoricalIsolationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.commit = next(iter(sf.HISTORICAL_LEDGER))
        cls.path = f"{sf.REL}/CLAIM_LEDGER.md"
        cls.data = sf.git_bytes(["show", f"{cls.commit}:{cls.path}"])
        cls.patterns = sf.patterns_for(cls.path, [sf.ACKNOWLEDGED_TREE])

    def test_exact_snapshots_are_acknowledged(self):
        for commit in sf.HISTORICAL_LEDGER:
            data = sf.git_bytes(["show", f"{commit}:{self.path}"])
            self.assertEqual(sf.historical_problems(data, commit, self.path, self.patterns), ([], True))

    def test_another_commit_is_not_covered(self):
        problems, accepted = sf.historical_problems(self.data, "0" * 40, self.path, self.patterns)
        self.assertTrue(problems)
        self.assertFalse(accepted)

    def test_another_path_is_not_covered(self):
        problems, accepted = sf.historical_problems(self.data, self.commit, "other.md", self.patterns)
        self.assertTrue(problems)
        self.assertFalse(accepted)

    def test_byte_change_is_refused_even_when_hits_are_unchanged(self):
        problems, accepted = sf.historical_problems(self.data + b"\n", self.commit, self.path, self.patterns)
        self.assertIn("bytes or complete hit list differ", problems[0])
        self.assertFalse(accepted)

    def test_missing_or_additional_hits_are_refused(self):
        for patterns in ([], self.patterns + [("extra", "SF-OPEN-A")]):
            problems, accepted = sf.historical_problems(self.data, self.commit, self.path, patterns)
            self.assertTrue(problems)
            self.assertFalse(accepted)

    def test_removing_the_exception_does_not_hide_the_breach(self):
        with mock.patch.object(sf, "HISTORICAL_LEDGER", {}):
            problems, accepted = sf.historical_problems(self.data, self.commit, self.path, self.patterns)
        self.assertTrue(problems)
        self.assertFalse(accepted)

    def test_current_tree_scan_still_refuses_the_exact_old_bytes(self):
        self.assertTrue(sf.scan_bytes(self.data, self.path, self.patterns))

    def test_undecodable_bytes_are_not_acknowledged(self):
        problems, accepted = sf.historical_problems(b"\xff", self.commit, self.path, self.patterns)
        self.assertTrue(problems)
        self.assertFalse(accepted)


if __name__ == "__main__":
    unittest.main()
