"""Tests for verify_pins and the shared scaffolding in common.

The pins must resolve and match at HEAD; every refusal is exercised by
tampering with the loaded pins in-process (the JSON is never written), and
the sealed-prefix refusal is exercised on a synthetic porcelain line so no
sealed path is ever touched (PROMPT.md step 35).
"""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

import common
import verify_lean
import verify_pins


class VerifyPinsTests(unittest.TestCase):
    def test_pins_resolve_and_match_at_head(self) -> None:
        lines = verify_pins.verify()
        self.assertTrue(lines[0].startswith("verification commit: "))
        pins = verify_pins.read_pins()
        pin_lines = [line for line in lines if line.startswith("pin: ")]
        self.assertEqual(len(pin_lines), len(pins["sealed_inputs"]))
        self.assertEqual(len(pin_lines), 5)
        self.assertIn(
            f"prompt: {common.PROMPT_PATH} {common.PROMPT_BLOB_ID}", lines
        )
        self.assertEqual(pins["snapshot_commit"], common.SNAPSHOT_COMMIT)
        self.assertEqual(pins["prompt"]["blob"], common.PROMPT_BLOB_ID)
        self.assertEqual(
            lines[-1],
            "sealed prefixes clean: prompt paper code lean4/Derivation artifacts",
        )

    def test_tampered_hash_is_refused(self) -> None:
        pins = copy.deepcopy(verify_pins.read_pins())
        pins["sealed_inputs"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(
            ValueError, r"hash mismatch for lean4/Derivation/PrimDiff\.lean"
        ):
            verify_pins.verify(pins)

    def test_head_snapshot_is_refused(self) -> None:
        pins = copy.deepcopy(verify_pins.read_pins())
        pins["snapshot_commit"] = "HEAD"
        with self.assertRaisesRegex(
            ValueError, "snapshot commit must be an exact 40-digit lowercase hex id"
        ):
            verify_pins.verify(pins)

    def test_prompt_blob_drift_is_refused(self) -> None:
        pins = copy.deepcopy(verify_pins.read_pins())
        pins["prompt"]["blob"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "prompt drift: research/s9_obligations/PROMPT.md"):
            verify_pins.verify(pins)

    def test_unsafe_pin_paths_are_refused(self) -> None:
        for raw in ("../paper/x.md", "/paper/x.md", "C:/paper/x.md", "paper\\x.md"):
            pins = copy.deepcopy(verify_pins.read_pins())
            pins["sealed_inputs"][0]["path"] = raw
            with self.assertRaisesRegex(ValueError, "unsafe path"):
                verify_pins.verify(pins)

    def test_unsealed_pin_path_is_refused(self) -> None:
        pins = copy.deepcopy(verify_pins.read_pins())
        pins["sealed_inputs"][0]["path"] = "research/s9_obligations/PROMPT.md"
        with self.assertRaisesRegex(ValueError, "not under a sealed prefix"):
            verify_pins.verify(pins)

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

    def test_sealed_prefix_check_passes_unsealed_and_empty_lines(self) -> None:
        self.assertEqual(verify_pins.sealed_prefix_violations(""), [])
        self.assertEqual(
            verify_pins.sealed_prefix_violations(
                "?? research/s9_obligations/foo.py\n?? lean4/ParkedAudit.lean\n\n"
            ),
            [],
        )

    def test_sealed_prefix_check_refuses_malformed_record(self) -> None:
        with self.assertRaisesRegex(ValueError, "malformed git status record"):
            verify_pins.sealed_prefix_violations("paper/x.md\n")


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

    def test_receipt_header_matches_the_pins(self) -> None:
        pins = verify_pins.read_pins()
        header = common.receipt_header()
        self.assertEqual(header["prompt_blob_id"], pins["prompt"]["blob"])
        self.assertEqual(header["prompt_path"], pins["prompt"]["path"])
        self.assertEqual(header["snapshot_commit"], pins["snapshot_commit"])

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
