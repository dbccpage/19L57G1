from __future__ import annotations

from hashlib import sha256
import unittest

from receipt_io import deterministic_json_bytes, strict_json_loads
from run_described_replay import (
    ReceiptEntry,
    render_output_injections,
    snapshot_failures,
)
from verify_pins import (
    PATH_POPULATION_COMMANDS,
    WRITE_ROOT,
    merge_path_populations,
    render_pin_injections,
    scope_failure_messages,
)


class PinVerifierInjectionTests(unittest.TestCase):
    def test_manifest_and_scope_injections_replay(self) -> None:
        payload = strict_json_loads(render_pin_injections(), source="pin injections")
        self.assertIsInstance(payload, dict)
        assert isinstance(payload, dict)
        self.assertEqual("PIN_VERIFIER_INJECTIONS_REPLAYED", payload["terminal"])
        self.assertEqual(29, payload["injection_count"])
        rows = payload["rows"]
        self.assertIsInstance(rows, list)
        assert isinstance(rows, list)
        self.assertTrue(all(isinstance(row, dict) and row["recovered"] for row in rows))

    def test_ignored_untracked_population_is_classified_without_tree_walk(self) -> None:
        self.assertIn(
            ("ls-files", "--others", "--ignored", "--exclude-standard", "-z"),
            PATH_POPULATION_COMMANDS,
        )
        paths = merge_path_populations(
            (
                (f"{WRITE_ROOT}.cache/inside",),
                ("research/described_replay_escape/.cache/outside",),
            )
        )
        self.assertEqual(
            [
                "paths outside write root changed: "
                "['research/described_replay_escape/.cache/outside']"
            ],
            scope_failure_messages(paths),
        )


class PythonReceiptInjectionTests(unittest.TestCase):
    def test_receipt_injections_replay(self) -> None:
        payload = strict_json_loads(
            render_output_injections(), source="Python receipt injections"
        )
        self.assertIsInstance(payload, dict)
        assert isinstance(payload, dict)
        self.assertEqual("PYTHON_RECEIPT_INJECTIONS_REPLAYED", payload["terminal"])
        self.assertEqual(12, payload["injection_count"])
        rows = payload["rows"]
        self.assertIsInstance(rows, list)
        assert isinstance(rows, list)
        self.assertTrue(all(isinstance(row, dict) and row["recovered"] for row in rows))

    def test_snapshot_checks_every_entry_and_hash_name(self) -> None:
        payload = deterministic_json_bytes({"value": 1})
        machine = deterministic_json_bytes(
            {"output_sha256": {"payload.json": sha256(payload).hexdigest()}}
        )
        rendered = {"machine_receipt.json": machine, "payload.json": payload}
        snapshot = {
            "extra.bin": ReceiptEntry("file", b"not JSON\n"),
            "extra": ReceiptEntry("directory", None),
            "machine_receipt.json": ReceiptEntry("file", machine),
            "payload.json": ReceiptEntry("file", payload),
        }
        failures = snapshot_failures(
            rendered,
            snapshot,
            all_names=("payload.json", "machine_receipt.json"),
            payload_names=("payload.json",),
        )
        self.assertEqual(2, len(failures))
        self.assertIn("extra.bin", failures[0])
        self.assertIn("extra (directory)", failures[1])


if __name__ == "__main__":
    unittest.main()
