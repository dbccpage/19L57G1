"""Tests for verify_pins and the shared scaffolding in common.

The manifest must resolve and match at the snapshot and at HEAD; every
refusal is exercised by tampering with the loaded manifest in-process (the
JSON is never written), and the sealed-prefix refusal is exercised on a
synthetic porcelain line so no sealed path is ever touched (PROMPT.md
step 35).  Two refusals a reviewer found missing are here by name: a
well-formed snapshot id that resolves to nothing, and a bytecode file
written under the seal.
"""

from __future__ import annotations

import copy
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import common
import verify_lean
import verify_pins


def tampered() -> dict[str, Any]:
    return copy.deepcopy(verify_pins.read_manifest())


class VerifyPinsTests(unittest.TestCase):
    def test_manifest_resolves_and_matches_at_snapshot_and_head(self) -> None:
        lines = verify_pins.verify()
        self.assertTrue(lines[0].startswith("verification commit: "))
        manifest = verify_pins.read_manifest()
        pin_lines = [line for line in lines if line.startswith("pin: ")]
        self.assertEqual(len(pin_lines), len(manifest["sources"]))
        self.assertEqual(len(pin_lines), 5)
        for line in pin_lines:
            self.assertTrue(line.endswith("(at snapshot and HEAD)"), line)
        self.assertIn(
            f"prompt: {common.PROMPT_PATH} {common.PROMPT_BLOB_ID} (at snapshot and HEAD)",
            lines,
        )
        snapshot = manifest["source_snapshot"]
        self.assertEqual(snapshot["commit"], common.SNAPSHOT_COMMIT)
        self.assertTrue(
            lines[1].startswith(
                f"snapshot commit: {snapshot['commit']} tree {snapshot['tree']} ("
            )
        )
        self.assertEqual(manifest["prompt"]["blob"], common.PROMPT_BLOB_ID)
        self.assertIn("sealed prefixes unchanged between snapshot and HEAD", lines)
        self.assertEqual(
            lines[-1],
            "sealed prefixes clean: prompt paper code lean4/Derivation artifacts",
        )

    def test_manifest_follows_the_established_shape(self) -> None:
        manifest = verify_pins.read_manifest()
        self.assertEqual(manifest["schema"], verify_pins.SCHEMA)
        self.assertEqual(set(manifest["source_snapshot"]), {"commit", "tree"})
        self.assertIn("hash_basis", manifest)
        for item in manifest["sources"]:
            self.assertEqual(set(item), {"path", "sha256", "role"})
        self.assertEqual(verify_pins.MANIFEST_PATH.name, "SOURCE_MANIFEST.json")

    def test_tampered_hash_is_refused(self) -> None:
        manifest = tampered()
        manifest["sources"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(
            ValueError, r"hash mismatch for lean4/Derivation/PrimDiff\.lean at snapshot"
        ):
            verify_pins.verify(manifest)

    def test_blob_that_moved_since_the_snapshot_is_refused(self) -> None:
        """A pin must hold at HEAD, not only at the snapshot it was taken at."""
        manifest = verify_pins.read_manifest()
        snapshot = manifest["source_snapshot"]["commit"]
        real = verify_pins._sha256_git_blob

        def moved_at_head(revision: str, relative: Any) -> str:
            if revision == snapshot:
                return real(revision, relative)
            return "0" * 64

        with mock.patch.object(verify_pins, "_sha256_git_blob", moved_at_head):
            with self.assertRaisesRegex(
                ValueError, r"hash mismatch for lean4/Derivation/PrimDiff\.lean at HEAD"
            ):
                verify_pins.verify(manifest)

    def test_head_snapshot_is_refused(self) -> None:
        manifest = tampered()
        manifest["source_snapshot"]["commit"] = "HEAD"
        with self.assertRaisesRegex(
            ValueError, "snapshot commit must be an exact 40-digit lowercase hex id"
        ):
            verify_pins.verify(manifest)

    def test_well_formed_but_nonexistent_snapshot_is_refused(self) -> None:
        """The reviewer's injection: forty zeroes passed the spelling check."""
        manifest = tampered()
        manifest["source_snapshot"]["commit"] = "0" * 40
        with self.assertRaisesRegex(
            ValueError, "snapshot commit 0{40} does not resolve to a commit object"
        ):
            verify_pins.verify(manifest)

    def test_snapshot_that_is_not_an_ancestor_is_refused(self) -> None:
        manifest = verify_pins.read_manifest()
        with mock.patch.object(verify_pins, "_is_ancestor", return_value=False):
            with self.assertRaisesRegex(ValueError, "is not an ancestor of HEAD"):
                verify_pins.verify(manifest)

    def test_snapshot_tree_mismatch_is_refused(self) -> None:
        manifest = tampered()
        manifest["source_snapshot"]["tree"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "snapshot tree mismatch"):
            verify_pins.verify(manifest)

    def test_sealed_path_moved_since_the_snapshot_is_refused(self) -> None:
        manifest = verify_pins.read_manifest()
        with mock.patch.object(
            verify_pins, "_sealed_diff", return_value=["paper/primitive_difference.md"]
        ):
            with self.assertRaisesRegex(
                ValueError, "tracked sealed paths differ between the snapshot and HEAD"
            ):
                verify_pins.verify(manifest)

    def test_prompt_blob_drift_is_refused(self) -> None:
        manifest = tampered()
        manifest["prompt"]["blob"] = "0" * 40
        with self.assertRaisesRegex(
            ValueError, "prompt drift: research/s9_obligations/PROMPT.md"
        ):
            verify_pins.verify(manifest)

    def test_unsafe_pin_paths_are_refused(self) -> None:
        for raw in ("../paper/x.md", "/paper/x.md", "C:/paper/x.md", "paper\\x.md"):
            manifest = tampered()
            manifest["sources"][0]["path"] = raw
            with self.assertRaisesRegex(ValueError, "unsafe path"):
                verify_pins.verify(manifest)

    def test_unsealed_pin_path_is_refused(self) -> None:
        manifest = tampered()
        manifest["sources"][0]["path"] = "research/s9_obligations/PROMPT.md"
        with self.assertRaisesRegex(ValueError, "not under a sealed prefix"):
            verify_pins.verify(manifest)

    def test_sealed_prefix_check_refuses_synthetic_paper_line(self) -> None:
        """Step 35's negative test: a porcelain line naming paper/x.md."""
        self.assertEqual(
            verify_pins.sealed_prefix_violations("?? paper/x.md\n"), ["?? paper/x.md"]
        )
        self.assertEqual(
            verify_pins.sealed_prefix_violations(" M lean4/Derivation/PrimDiff.lean\n"),
            [" M lean4/Derivation/PrimDiff.lean"],
        )
        self.assertEqual(
            verify_pins.sealed_prefix_violations(
                "R  paper/a.md -> research/s9_obligations/b.md\n"
            ),
            ["R  paper/a.md -> research/s9_obligations/b.md"],
        )
        self.assertEqual(
            verify_pins.sealed_prefix_violations('?? "artifacts/with space.json"\n'),
            ['?? "artifacts/with space.json"'],
        )

    def test_sealed_prefix_check_refuses_ignored_bytecode_under_the_seal(self) -> None:
        """The reviewer's write: a gitignored .pyc inside code/derivation/."""
        record = "!! code/derivation/__pycache__/primdiff.cpython-314.pyc"
        self.assertEqual(verify_pins.sealed_prefix_violations(record + "\n"), [record])

    def test_live_porcelain_asks_git_for_ignored_files(self) -> None:
        calls: list[tuple[str, ...]] = []

        def record(*args: str) -> bytes:
            calls.append(args)
            return b""

        with mock.patch.object(verify_pins, "_git_bytes", record):
            verify_pins._live_porcelain()
        self.assertEqual(len(calls), 1)
        self.assertIn("--ignored=matching", calls[0])
        self.assertIn("--untracked-files=all", calls[0])

    def test_sealed_prefix_check_passes_unsealed_and_empty_lines(self) -> None:
        self.assertEqual(verify_pins.sealed_prefix_violations(""), [])
        self.assertEqual(
            verify_pins.sealed_prefix_violations(
                "?? research/s9_obligations/foo.py\n?? lean4/ParkedAudit.lean\n"
                "!! research/s9_obligations/__pycache__/common.cpython-314.pyc\n\n"
            ),
            [],
        )

    def test_sealed_prefix_check_refuses_malformed_record(self) -> None:
        with self.assertRaisesRegex(ValueError, "malformed git status record"):
            verify_pins.sealed_prefix_violations("paper/x.md\n")


class BytecodeBoundaryTests(unittest.TestCase):
    """Importing common must stop the interpreter writing bytecode anywhere."""

    def test_common_sets_dont_write_bytecode_in_this_process(self) -> None:
        self.assertTrue(sys.dont_write_bytecode)

    def test_importing_common_first_leaves_no_pycache_behind(self) -> None:
        env = dict(os.environ)
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        with tempfile.TemporaryDirectory() as scratch:
            probe = Path(scratch) / "zzz_probe_module.py"
            probe.write_text("VALUE = 1\n", encoding="utf-8")
            code = (
                "import sys\n"
                f"sys.path.insert(0, {scratch!r})\n"
                "import common\n"
                "import zzz_probe_module\n"
                "print(sys.dont_write_bytecode, zzz_probe_module.VALUE)\n"
            )
            result = subprocess.run(
                [sys.executable, "-c", code],
                cwd=common.TREE,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "True 1")
            self.assertFalse((Path(scratch) / "__pycache__").exists())


class CommonHelperTests(unittest.TestCase):
    def test_receipt_bytes_follow_the_convention(self) -> None:
        payload = {"b": [2, 1], "a": "x", "c": {"z": 1, "y": None}}
        self.assertEqual(
            common.receipt_bytes(payload),
            b'{\n  "a": "x",\n  "b": [\n    2,\n    1\n  ],\n  "c": {\n    "y": null,\n    "z": 1\n  }\n}\n',
        )

    def test_write_receipt_replays_byte_identically_with_lf_only(self) -> None:
        payload = {"header": common.receipt_header(), "count": 3}
        with tempfile.TemporaryDirectory(dir=common.TREE) as scratch:
            first = common.write_receipt(Path(scratch) / "one" / "r.json", payload)
            second = common.write_receipt(Path(scratch) / "two" / "r.json", payload)
            one = first.read_bytes()
            self.assertEqual(one, second.read_bytes())
            self.assertNotIn(b"\r", one)
            self.assertTrue(one.endswith(b"}\n"))
            self.assertEqual(one, common.receipt_bytes(payload))

    def test_write_root_guard_refuses_paths_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "receipt.json"
            with self.assertRaisesRegex(ValueError, "refusing to write outside"):
                common.assert_inside_tree(target)
            with self.assertRaisesRegex(ValueError, "refusing to write outside"):
                common.write_receipt(target, {"never": "written"})
            self.assertFalse(target.exists())
        with self.assertRaisesRegex(ValueError, "refusing to write outside"):
            common.assert_inside_tree(common.REPO / "paper" / "x.md")
        with self.assertRaisesRegex(ValueError, "refusing to write outside"):
            common.assert_inside_tree(common.TREE.parent / "blind_restart" / "x.json")

    def test_write_root_guard_accepts_paths_inside_the_tree(self) -> None:
        inside = common.assert_inside_tree(common.TREE / "receipts" / "p1.json")
        self.assertTrue(inside.is_relative_to(common.TREE))

    def test_receipt_header_matches_the_manifest(self) -> None:
        manifest = verify_pins.read_manifest()
        header = common.receipt_header()
        self.assertEqual(header["prompt_blob_id"], manifest["prompt"]["blob"])
        self.assertEqual(header["prompt_path"], manifest["prompt"]["path"])
        self.assertEqual(
            header["snapshot_commit"], manifest["source_snapshot"]["commit"]
        )

    def test_render_relation_is_sorted_without_duplicates(self) -> None:
        self.assertEqual(
            common.render_relation(frozenset({(2, 1), (0, 1), (1, 1)})),
            [[0, 1], [1, 1], [2, 1]],
        )
        self.assertEqual(common.render_relation(((1, 0), (1, 0), (0, 0))), [[0, 0], [1, 0]])
        self.assertEqual(common.render_relation(()), [])


SAMPLE_REPORT = (
    "'S9Obligations.P1.transfer_cell' depends on axioms: [propext, Quot.sound]\n"
    "'S9Obligations.P1.primed'' does not depend on any axioms\n"
    "info: an unrelated line\n"
)


class VerifyLeanAuditTests(unittest.TestCase):
    """The audit half of verify_lean; no Lean toolchain is needed here."""

    def test_empty_inventory_passes_only_with_no_reports(self) -> None:
        self.assertEqual(verify_lean.check_axiom_reports({}, ()), [])
        with self.assertRaisesRegex(
            ValueError,
            r"missing \[\], unexpected \[\"S9Obligations\.P1\.primed'\", "
            r"'S9Obligations\.P1\.transfer_cell'\]",
        ):
            verify_lean.check_axiom_reports(
                verify_lean.parse_axiom_report(SAMPLE_REPORT), ()
            )

    def test_parser_captures_primed_names_non_greedily(self) -> None:
        self.assertEqual(
            verify_lean.parse_axiom_report(SAMPLE_REPORT),
            {
                "S9Obligations.P1.transfer_cell": frozenset({"propext", "Quot.sound"}),
                "S9Obligations.P1.primed'": frozenset(),
            },
        )
        with self.assertRaisesRegex(ValueError, "duplicate axiom report"):
            verify_lean.parse_axiom_report(SAMPLE_REPORT + SAMPLE_REPORT)

    def test_disallowed_axiom_fails_even_when_the_name_is_listed(self) -> None:
        output = "'A.b' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
        with self.assertRaisesRegex(
            ValueError, r"A\.b depends on disallowed axioms: \['Classical\.choice'\]"
        ):
            verify_lean.check_axiom_reports(verify_lean.parse_axiom_report(output), ("A.b",))

    def test_declared_inventory_matches_the_report_source(self) -> None:
        source = (verify_lean.LEAN_ROOT / verify_lean.AXIOM_REPORT_SOURCE).read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            verify_lean.declared_report_inventory(source),
            verify_lean.AXIOM_REPORT_DECLARATIONS,
        )

    def test_forbidden_token_scan_names_the_token_and_passes_the_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            bad = Path(temporary) / "Bad.lean"
            bad.write_text(
                "theorem t : True := by\n  " + "sor" + "ry\n" + "ax" + "iom zzz : True\n",
                encoding="utf-8",
            )
            self.assertEqual(
                verify_lean.scan_forbidden_tokens([bad]),
                [
                    "Bad.lean: forbidden token '" + "sor" + "ry'",
                    "Bad.lean: forbidden token '" + "ax" + "iom'",
                ],
            )
        # The research Lean source census, pinned by name: the root, the
        # report inventory, the lakefile, and the three part modules.  A
        # seventh file goes red here until it is registered, which is the
        # pin working (the empty package's three-name pin went red when the
        # first part module landed and stayed red until this repair).
        sources = verify_lean.research_lean_sources()
        self.assertEqual(
            sorted(path.name for path in sources),
            [
                "AxiomLattice.lean",
                "AxiomReport.lean",
                "MorphismClasses.lean",
                "S9Obligations.lean",
                "WitnessTypes.lean",
                "lakefile.lean",
            ],
        )
        self.assertEqual(verify_lean.scan_forbidden_tokens(sources), [])


if __name__ == "__main__":
    unittest.main()
