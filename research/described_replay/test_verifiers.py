from __future__ import annotations

import gzip
from hashlib import sha256
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

import run_described_replay
from receipt_io import (
    GZIP_MTIME,
    deterministic_gzip_bytes,
    deterministic_json_bytes,
    strict_gzip_payload,
    strict_json_loads,
    write_gzip_atomic,
)
from run_described_replay import (
    GZIP_PAYLOAD_NAMES,
    ReceiptEntry,
    render_output_injections,
    snapshot_failures,
    stored_name,
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


HERE = Path(__file__).resolve().parent
_PROBE = deterministic_json_bytes({"value": "gzip probe"})


def _set_header_byte(data: bytes, offset: int, value: int) -> bytes:
    return data[:offset] + bytes((value,)) + data[offset + 1 :]


class GzipReceiptTests(unittest.TestCase):
    """The storage of the two large payloads as ``.gz`` members.

    Each refusal below is an in-memory injection retained as a negative test:
    it names the defect the strict reader or the snapshot check exists to
    catch, and the unmodified member passes beside it.
    """

    def test_the_two_large_payloads_are_the_gzip_names(self) -> None:
        self.assertEqual(("class_replay.json", "diagonal.json"), GZIP_PAYLOAD_NAMES)
        self.assertEqual("class_replay.json.gz", stored_name("class_replay.json"))
        self.assertEqual("register.json", stored_name("register.json"))
        self.assertEqual(
            sorted(
                f"{name}.gz" if name in GZIP_PAYLOAD_NAMES else name
                for name in run_described_replay.ALL_NAMES
            ),
            sorted(run_described_replay.STORED_NAMES),
        )

    def test_writer_is_deterministic_nameless_and_zero_mtime(self) -> None:
        first = deterministic_gzip_bytes(_PROBE)
        self.assertEqual(first, deterministic_gzip_bytes(_PROBE))
        magic, method, flags, mtime = struct.unpack("<2sBBI", first[:8])
        self.assertEqual((b"\x1f\x8b", 8, 0, GZIP_MTIME), (magic, method, flags, mtime))
        self.assertEqual(_PROBE, strict_gzip_payload(first))
        self.assertEqual(_PROBE, gzip.decompress(first))

    def test_writer_refuses_bad_payloads_and_non_gz_targets(self) -> None:
        with self.assertRaisesRegex(ValueError, "LF-only"):
            deterministic_gzip_bytes(b"{}\r\n")
        with self.assertRaisesRegex(ValueError, "exactly one LF"):
            deterministic_gzip_bytes(b"{}")
        with self.assertRaisesRegex(ValueError, "must end in .gz"):
            write_gzip_atomic(HERE / ".pytest_tmp" / "probe.json", _PROBE)

    def test_strict_reader_refuses_each_named_defect(self) -> None:
        good = deterministic_gzip_bytes(_PROBE)
        named_flag = _set_header_byte(good, 3, 0x08)
        cases = (
            ("truncated header", good[:9], "gzip member is truncated"),
            ("wrong magic", b"PK" + good[2:], "not a gzip member"),
            ("wrong method", _set_header_byte(good, 2, 7), "gzip method is not deflate"),
            ("file-name flag", named_flag, "gzip header flags must be zero"),
            (
                "nonzero mtime",
                good[:4] + struct.pack("<I", 1) + good[8:],
                "gzip modification time must be zero",
            ),
            ("truncated member", good[:-1], "gzip member is truncated"),
            ("trailing byte", good + b"\0", "bytes follow the gzip member"),
            ("second member", good + good, "bytes follow the gzip member"),
            (
                "checksum mismatch",
                good[:-8] + bytes((good[-8] ^ 0xFF,)) + good[-7:],
                "incorrect data check",
            ),
            ("uncompressed JSON", _PROBE, "not a gzip member"),
        )
        for label, data, diagnostic in cases:
            with self.subTest(label):
                with self.assertRaisesRegex(ValueError, diagnostic):
                    strict_gzip_payload(data, source="probe.json.gz")

    def _snapshot_case(
        self, stored: dict[str, bytes]
    ) -> list[str]:
        machine = deterministic_json_bytes(
            {"output_sha256": {"payload.json": sha256(_PROBE).hexdigest()}}
        )
        rendered = {"machine_receipt.json": machine, "payload.json": _PROBE}
        snapshot = {
            "machine_receipt.json": ReceiptEntry("file", machine),
            **{name: ReceiptEntry("file", data) for name, data in stored.items()},
        }
        return snapshot_failures(
            rendered,
            snapshot,
            all_names=("payload.json", "machine_receipt.json"),
            payload_names=("payload.json",),
            gzip_names=("payload.json",),
        )

    def test_snapshot_compares_decompressed_bytes_only(self) -> None:
        self.assertEqual(
            [], self._snapshot_case({"payload.json.gz": deterministic_gzip_bytes(_PROBE)})
        )
        # Another compressed stream of the same bytes, as another zlib build
        # or level would write, passes: the stored gzip bytes are never compared.
        other_stream = gzip.compress(_PROBE, compresslevel=1, mtime=0)
        self.assertNotEqual(deterministic_gzip_bytes(_PROBE), other_stream)
        self.assertEqual([], self._snapshot_case({"payload.json.gz": other_stream}))

    def test_snapshot_names_each_gzip_defect(self) -> None:
        changed = deterministic_json_bytes({"value": "changed"})
        good = deterministic_gzip_bytes(_PROBE)
        cases = (
            (
                "decompressed payload drift",
                {"payload.json.gz": deterministic_gzip_bytes(changed)},
                [
                    "Python receipt differs: payload.json.gz",
                    "machine receipt output hash map differs",
                ],
            ),
            (
                "uncompressed file under the payload name",
                {"payload.json": _PROBE},
                [
                    "Python receipt census differs: "
                    "got=['machine_receipt.json', 'payload.json'] "
                    "wanted=['machine_receipt.json', 'payload.json.gz']"
                ],
            ),
            (
                "uncompressed bytes under the gzip name",
                {"payload.json.gz": _PROBE},
                ["invalid payload.json.gz: not a gzip member"],
            ),
            (
                "bytes after the member",
                {"payload.json.gz": good + b"\n"},
                ["invalid payload.json.gz: bytes follow the gzip member"],
            ),
            (
                "gzip of invalid JSON",
                {"payload.json.gz": deterministic_gzip_bytes(b"{\n")},
                [
                    "invalid payload.json.gz: Expecting property name enclosed in "
                    "double quotes: line 2 column 1 (char 2)",
                    "machine receipt output hash map differs",
                ],
            ),
        )
        for label, stored, expected in cases:
            with self.subTest(label):
                self.assertEqual(expected, self._snapshot_case(stored))

    def test_write_keeps_an_equal_member_and_rewrites_a_changed_one(self) -> None:
        scratch_root = HERE / ".pytest_tmp"
        scratch_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch_root) as raw:
            receipts = Path(raw)
            # Small stand-in payloads under the real names keep this test
            # cheap; the committed payloads are checked by the runner and by
            # test_committed_receipts_match_the_rendering.
            rendered = {
                name: deterministic_json_bytes({"payload": name})
                for name in run_described_replay.PAYLOAD_NAMES
            }
            rendered["machine_receipt.json"] = deterministic_json_bytes(
                {
                    "output_sha256": {
                        name: sha256(rendered[name]).hexdigest()
                        for name in run_described_replay.PAYLOAD_NAMES
                    }
                }
            )
            other_stream = gzip.compress(
                rendered["diagonal.json"], compresslevel=1, mtime=0
            )
            (receipts / "diagonal.json.gz").write_bytes(other_stream)
            (receipts / "class_replay.json.gz").write_bytes(
                deterministic_gzip_bytes(deterministic_json_bytes({"stale": True}))
            )
            with mock.patch.object(run_described_replay, "RECEIPTS", receipts):
                run_described_replay.write_outputs(rendered)
                self.assertEqual(
                    [],
                    snapshot_failures(
                        rendered, run_described_replay.receipt_snapshot(receipts)
                    ),
                )
            self.assertEqual(other_stream, (receipts / "diagonal.json.gz").read_bytes())
            self.assertEqual(
                rendered["class_replay.json"],
                strict_gzip_payload((receipts / "class_replay.json.gz").read_bytes()),
            )
            self.assertEqual(
                sorted(run_described_replay.STORED_NAMES),
                sorted(path.name for path in receipts.iterdir()),
            )


if __name__ == "__main__":
    unittest.main()
