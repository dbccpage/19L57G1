"""Check the supplied evidence's byte identity and explicit limits."""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import unittest

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]


class ReconciliationTests(unittest.TestCase):
    def test_report_and_both_seed_byte_representations_are_named(self) -> None:
        prose = (HERE / "BLIND_RECONCILIATION.md").read_text(encoding="utf-8")
        report = (HERE / "BLIND_RUN_REPORT_20260916.md").read_bytes()
        seed = subprocess.check_output(
            ["git", "show", "HEAD:research/oriented_boundary/SEED.md"], cwd=REPO
        )
        self.assertNotIn(b"\r", seed)
        for blob in (report, seed, seed.replace(b"\n", b"\r\n")):
            self.assertIn(hashlib.sha256(blob).hexdigest(), prose)

    def test_source_pin_withdraws_independent_confirmation(self) -> None:
        pin = json.loads((HERE / "SOURCE_PIN.json").read_text(encoding="utf-8"))
        self.assertIn("independent-confirmation claim", pin["note"])
        self.assertIn("is withdrawn", pin["note"])
        self.assertIn("independence is not certified", pin["note"])
        self.assertFalse(pin["consumes_sealed_files"])

    def test_reconciliation_keeps_provenance_and_cost_boundaries(self) -> None:
        prose = (HERE / "BLIND_RECONCILIATION.md").read_text(encoding="utf-8")
        self.assertIn("raw prompts, transcripts, execution", prose)
        self.assertIn("shared-directory concern", prose)
        self.assertIn("zero-cost observing", prose)
        self.assertIn("not a zero-admission oriented object", prose)
        self.assertIn("no cost-preserving", prose)


if __name__ == "__main__":
    unittest.main()
