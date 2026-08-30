"""Tests for the family-embedding tree's verifiers.

The manifest must resolve at the snapshot and at HEAD and be exactly the
import closure of its roots; every refusal is exercised on a tampered
in-process copy (the JSON is never written); the write-root boundary is
tested on synthetic records and, when ``lake`` is on PATH, on a real clean
build.  No test here proves a theorem: the Lean statements are checked by
``verify_lean.py``, a manual receipt.
"""

from __future__ import annotations

import copy
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import verify_lean
import verify_pins

REPO = verify_pins.REPO
TREE = verify_pins.HERE


def tampered() -> dict[str, Any]:
    return copy.deepcopy(verify_pins.read_manifest())


class ManifestTests(unittest.TestCase):
    def test_manifest_resolves_and_is_the_import_closure(self) -> None:
        lines = verify_pins.verify()
        manifest = verify_pins.read_manifest()
        pin_lines = [line for line in lines if line.startswith("pin: ")]
        self.assertEqual(len(pin_lines), len(manifest["modules"]))
        self.assertEqual(len(pin_lines), 12)
        self.assertIn(
            "import closure of ['Derivation.PresentationNaturality']: 12 module(s), all pinned",
            lines,
        )
        self.assertEqual(
            lines[-1], "sealed prefixes clean: prompt paper code lean4/Derivation artifacts"
        )

    def test_manifest_follows_the_established_shape(self) -> None:
        manifest = verify_pins.read_manifest()
        self.assertEqual(manifest["schema"], verify_pins.SCHEMA)
        self.assertEqual(set(manifest["source_snapshot"]), {"commit", "tree"})
        self.assertIn("hash_basis", manifest)
        self.assertEqual(manifest["semantic_roots"], ["Derivation.PresentationNaturality"])
        for item in manifest["modules"]:
            self.assertEqual(set(item), {"module", "path", "sha256", "role"})
        roots = [m["module"] for m in manifest["modules"] if m["role"] == "semantic root"]
        self.assertEqual(roots, ["Derivation.PresentationNaturality"])

    def test_well_formed_but_nonexistent_snapshot_is_refused(self) -> None:
        manifest = tampered()
        manifest["source_snapshot"]["commit"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "0{40} does not resolve to a commit object"):
            verify_pins.verify(manifest)

    def test_head_snapshot_is_refused(self) -> None:
        manifest = tampered()
        manifest["source_snapshot"]["commit"] = "HEAD"
        with self.assertRaisesRegex(ValueError, "exact 40-digit lowercase hex id"):
            verify_pins.verify(manifest)

    def test_non_ancestor_snapshot_is_refused(self) -> None:
        with mock.patch.object(verify_pins, "_is_ancestor", return_value=False):
            with self.assertRaisesRegex(ValueError, "is not an ancestor of HEAD"):
                verify_pins.verify(verify_pins.read_manifest())

    def test_snapshot_tree_mismatch_is_refused(self) -> None:
        manifest = tampered()
        manifest["source_snapshot"]["tree"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "snapshot tree mismatch"):
            verify_pins.verify(manifest)

    def test_tampered_hash_is_refused_at_the_snapshot(self) -> None:
        manifest = tampered()
        manifest["modules"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash mismatch for .* at snapshot"):
            verify_pins.verify(manifest)

    def test_unpinned_closure_member_is_refused(self) -> None:
        manifest = tampered()
        manifest["modules"] = [
            m for m in manifest["modules"] if m["module"] != "Derivation.PrimDiff"
        ]
        with self.assertRaisesRegex(ValueError, r"unpinned \['Derivation\.PrimDiff'\]"):
            verify_pins.verify(manifest)

    def test_pinned_but_unreachable_module_is_refused(self) -> None:
        manifest = tampered()
        blob = verify_pins._git_bytes("show", "HEAD:lean4/Derivation/Composing.lean")
        manifest["modules"].append(
            {
                "module": "Derivation.Composing",
                "path": "lean4/Derivation/Composing.lean",
                "sha256": verify_pins._sha256(blob),
                "role": "transitive compilation input",
            }
        )
        with self.assertRaisesRegex(
            ValueError, r"pinned but unreachable \['Derivation\.Composing'\]"
        ):
            verify_pins.verify(manifest)

    def test_module_path_mismatch_is_refused(self) -> None:
        manifest = tampered()
        manifest["modules"][0]["path"] = "lean4/Derivation/PrimDiff.lean"
        with self.assertRaisesRegex(ValueError, "module/path mismatch"):
            verify_pins.verify(manifest)

    def test_import_closure_reads_the_supplied_blobs_only(self) -> None:
        blobs = {
            "Derivation.A": b"import Derivation.B\nimport Derivation.C\n",
            "Derivation.B": b"import Derivation.C\n",
            "Derivation.C": b"-- import Derivation.D in a comment line does not count\n",
        }
        closure = verify_pins.import_closure(["Derivation.A"], lambda m: blobs[m])
        self.assertEqual(set(closure), set(blobs))

    def test_sealed_prefix_check_refuses_ignored_bytecode_under_the_seal(self) -> None:
        record = "!! code/derivation/__pycache__/primdiff.cpython-314.pyc"
        self.assertEqual(verify_pins.sealed_prefix_violations(record + "\n"), [record])
        self.assertEqual(
            verify_pins.sealed_prefix_violations("?? research/family_embedding/x.py\n"), []
        )
        with self.assertRaisesRegex(ValueError, "malformed git status record"):
            verify_pins.sealed_prefix_violations("paper/x.md\n")


class LeanAuditTests(unittest.TestCase):
    def test_python_inventory_matches_the_report_source(self) -> None:
        source = (verify_lean.LEAN_ROOT / verify_lean.AXIOM_REPORT_SOURCE).read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            verify_lean.declared_report_inventory(source), verify_lean.AXIOM_REPORT_DECLARATIONS
        )
        self.assertEqual(len(verify_lean.AXIOM_REPORT_DECLARATIONS), 16)

    def test_every_listed_theorem_is_declared_in_the_source(self) -> None:
        source = "\n".join(
            path.read_text(encoding="utf-8") for path in verify_lean.research_lean_sources()
        )
        for name in verify_lean.AXIOM_REPORT_DECLARATIONS:
            self.assertTrue(name.startswith("FamilyEmbedding."), name)
            local = name[len("FamilyEmbedding."):]
            parts = local.split(".")
            candidates = [".".join(parts[i:]) for i in range(len(parts))]
            self.assertTrue(
                any(f"theorem {c} " in source for c in candidates), name
            )

    def test_disallowed_axiom_fails_even_when_the_name_is_listed(self) -> None:
        output = "'A.b' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
        with self.assertRaisesRegex(ValueError, r"disallowed axioms: \['Classical\.choice'\]"):
            verify_lean.check_axiom_reports(verify_lean.parse_axiom_report(output), ("A.b",))

    def test_parser_captures_primed_names_non_greedily(self) -> None:
        sample = "'A.primed'' does not depend on any axioms\n'A.b' depends on axioms: [propext]\n"
        self.assertEqual(
            verify_lean.parse_axiom_report(sample),
            {"A.primed'": frozenset(), "A.b": frozenset({"propext"})},
        )

    def test_forbidden_token_scan_names_the_token_and_passes_the_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            bad = Path(temporary) / "Bad.lean"
            bad.write_text("theorem t : True := by\n  " + "sor" + "ry\n", encoding="utf-8")
            self.assertEqual(
                verify_lean.scan_forbidden_tokens([bad]),
                ["Bad.lean: forbidden token '" + "sor" + "ry'"],
            )
        sources = verify_lean.research_lean_sources()
        self.assertEqual(
            sorted(path.name for path in sources),
            [
                "AxiomReport.lean",
                "FamilyEmbedding.lean",
                "lakefile.lean",
            ],
        )
        self.assertEqual(verify_lean.scan_forbidden_tokens(sources), [])

    def test_hom_is_the_subtype_of_arr_with_src_and_tgt(self) -> None:
        source = (verify_lean.LEAN_ROOT / "FamilyEmbedding.lean").read_text(encoding="utf-8")
        self.assertIn("{ f : F.Arr // F.src f = a ∧ F.tgt f = b }", source)
        self.assertNotIn("Hom a b := Empty", source)
        self.assertNotIn("Hom := fun _ _ => Empty", source)


class WriteRootBoundaryTests(unittest.TestCase):
    def test_lakefile_declares_no_dependency_and_stages_the_closure(self) -> None:
        lakefile = (verify_lean.LEAN_ROOT / "lakefile.lean").read_text(encoding="utf-8")
        self.assertNotIn("require ", lakefile)
        self.assertIn('srcDir := "sealed"', lakefile)
        for item in verify_pins.read_manifest()["modules"]:
            self.assertIn("`" + item["module"], lakefile)
        manifest = (verify_lean.LEAN_ROOT / "lake-manifest.json").read_text(encoding="utf-8")
        self.assertIn('"packages": []', manifest)
        self.assertIn("sealed/", (verify_lean.LEAN_ROOT / ".gitignore").read_text(encoding="utf-8"))

    def test_staged_sources_are_the_pinned_snapshot_blobs(self) -> None:
        lines = verify_lean.stage_sealed_sources()
        manifest = verify_pins.read_manifest()
        self.assertEqual(len(lines), len(manifest["modules"]))
        for item in manifest["modules"]:
            target = verify_lean.STAGED_ROOT / (item["module"].replace(".", "/") + ".lean")
            self.assertTrue(target.is_relative_to(TREE))
            digest = hashlib.sha256(target.read_bytes()).hexdigest().upper()
            self.assertEqual(digest, item["sha256"], item["module"])
            self.assertNotIn(target, verify_lean.research_lean_sources())

    def test_staging_refuses_a_blob_that_does_not_match_the_pin(self) -> None:
        manifest = tampered()
        manifest["modules"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "manifest pins 0{64}"):
            verify_lean.stage_sealed_sources(manifest)

    def test_writes_outside_root_names_a_new_lean4_build_product(self) -> None:
        before = frozenset({"!! coverage.json", "!! lean4/.lake/build/old.olean"})
        after = before | {
            "!! lean4/.lake/build/lib/Derivation/PrimDiff.olean",
            "!! research/family_embedding/lean/.lake/build/lib/FamilyEmbedding.olean",
            "!! research/family_embedding/lean/sealed/Derivation/PrimDiff.lean",
        }
        self.assertEqual(
            verify_lean.writes_outside_root(before, after),
            ["!! lean4/.lake/build/lib/Derivation/PrimDiff.olean"],
        )
        self.assertEqual(verify_lean.writes_outside_root(after, after), [])

    def test_common_sets_dont_write_bytecode_in_this_process(self) -> None:
        self.assertTrue(sys.dont_write_bytecode)

    def test_clean_build_leaves_lean4_untouched_and_stays_inside_the_root(self) -> None:
        if shutil.which("lake") is None:
            self.skipTest("lake is not on PATH")
        sealed_cache = REPO / "lean4" / ".lake"
        had_sealed_cache = sealed_cache.exists()
        shutil.rmtree(verify_lean.LEAN_ROOT / ".lake", ignore_errors=True)
        shutil.rmtree(verify_lean.STAGED_ROOT, ignore_errors=True)
        before = verify_lean.repository_records()
        env = dict(os.environ)
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        result = subprocess.run(
            [sys.executable, str(TREE / "verify_lean.py")],
            cwd=REPO,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("write root respected", result.stdout)
        self.assertIn("declarations: 16 within", result.stdout)
        self.assertEqual(
            verify_lean.writes_outside_root(before, verify_lean.repository_records()), []
        )
        self.assertEqual(sealed_cache.exists(), had_sealed_cache)


if __name__ == "__main__":
    unittest.main()
