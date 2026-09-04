"""The FW-DEF census is total, and it is checked rather than asserted.

The frozen `PREDICTIONS.md` census named seventeen of this rung's targets.
An adversarial reading of the package before it was committed found that
the package carries far more theorems than that, and that the omissions
were disproportionately the trivia -- so a partial census flatters the
run.  `FWDEF_CENSUS.json` is the repair: it classifies EVERY theorem of
the package, and this file checks four things about it.

* Totality in both directions: every theorem of every module appears
  exactly once in the census, and the census names no theorem the package
  does not declare.
* The two reconstruction modules are classed RECONSTRUCTION throughout,
  and no module of this rung's own work is.
* Nothing classed DEFINITION has a long proof.  This is a crude bound and
  is stated as one: a short proof is not sufficient for being at the level
  of a definition, and the classification is the author's reading.  What
  the bound catches is the failure that matters -- a theorem with real work
  in it being filed as trivial to shrink the content count.
* The counts in the census match the counts `STATUS.md` reports, so the
  prose and the machine-readable file cannot drift apart.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import tempfile
import unittest
from unittest import mock

import verify_lean as lean_audit

HERE = pathlib.Path(__file__).resolve().parent
LEAN = HERE / "lean" / "SecondNoFirst"
CENSUS = HERE / "FWDEF_CENSUS.json"
RECONSTRUCTIONS = {"Kernel.lean", "Inherited.lean"}
REPORT_MODULE = "AxiomReport.lean"

# A proof at the level of a definition is short.  Twelve lines is generous
# on purpose: the bound exists to catch a long proof filed as trivial, not
# to decide the classification.
DEFINITION_LINE_BOUND = 12


def modules() -> list[pathlib.Path]:
    return [m for m in sorted(LEAN.rglob("*.lean")) if m.name != REPORT_MODULE]


def declared() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in modules():
        text = lean_audit.declaration_text(path.read_text("utf-8"))
        for name in lean_audit.THEOREM_DECL.findall(text):
            out[name] = path.name
    return out


def proof_lines() -> dict[str, int]:
    """Lines of proof per theorem, counted from the `:=` to the start of the
    next top-level declaration."""
    out: dict[str, int] = {}
    for path in modules():
        text = path.read_text("utf-8")
        parts = re.split(r"(?m)^(?=theorem |def |inductive |structure |/-- |/-! )", text)
        for part in parts:
            match = re.match(r"theorem ([A-Za-z_][\w'.]*)", part)
            if match is None:
                continue
            body = part.split(":=", 1)
            proof = body[1].strip() if len(body) > 1 else part
            out[match.group(1)] = proof.count("\n") + 1
    return out


class CensusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.census = json.loads(CENSUS.read_text(encoding="utf-8"))
        self.rows = self.census["classes"]

    def test_the_census_is_total_in_both_directions(self) -> None:
        found = declared()
        self.assertEqual(sorted(self.rows), sorted(found))

    def test_every_row_names_the_module_it_is_declared_in(self) -> None:
        found = declared()
        for name, row in self.rows.items():
            self.assertEqual(row["module"], found[name], name)

    def test_reconstructions_are_classed_as_such_and_nothing_else_is(
        self,
    ) -> None:
        for name, row in self.rows.items():
            if row["module"] in RECONSTRUCTIONS:
                self.assertEqual(row["class"], "RECONSTRUCTION", name)
            else:
                self.assertNotEqual(row["class"], "RECONSTRUCTION", name)

    def test_only_the_declared_classes_appear(self) -> None:
        allowed = {"RECONSTRUCTION", "DEFINITION", "THIN", "CONTENT"}
        self.assertEqual(
            {row["class"] for row in self.rows.values()} - allowed, set()
        )

    def test_nothing_classed_definitional_has_a_long_proof(self) -> None:
        """The crude bound.  A short proof does not make a theorem
        definitional; a long one makes the label implausible.

        One theorem is longer than the bound and is still at the level of a
        definition, because its length counts constructors rather than
        work.  It is EXCEPTED BY NAME, with its reason recorded in the
        census, rather than by raising the bound for everything: an
        exception that is listed can be counted and argued with, and a
        raised bound cannot."""
        lengths = proof_lines()
        excepted = self.census.get("long_but_definitional", {})
        offenders = [
            f"{name} ({lengths[name]} lines)"
            for name, row in self.rows.items()
            if row["class"] == "DEFINITION"
            and lengths.get(name, 0) > DEFINITION_LINE_BOUND
            and name not in excepted
        ]
        self.assertEqual(offenders, [])

    def test_every_exception_is_used_declared_and_definitional(self) -> None:
        """The exception list fails in both directions: an entry that is no
        longer over the bound, or is no longer classed definitional, or
        carries no reason, is a stale exception and is named."""
        lengths = proof_lines()
        excepted = self.census.get("long_but_definitional", {})
        self.assertLessEqual(len(excepted), 2)
        for name, reason in excepted.items():
            self.assertIn(name, self.rows, name)
            self.assertEqual(self.rows[name]["class"], "DEFINITION", name)
            self.assertGreater(lengths[name], DEFINITION_LINE_BOUND, name)
            self.assertGreater(len(reason), 80, name)

    def test_the_bound_would_catch_a_long_proof_filed_as_trivial(self) -> None:
        """NEGATIVE: the bound above is a check.  The longest CONTENT proof
        in the package exceeds the bound, so filing it as definitional
        would fail."""
        lengths = proof_lines()
        content = [
            lengths[name]
            for name, row in self.rows.items()
            if row["class"] == "CONTENT"
        ]
        self.assertGreater(max(content), DEFINITION_LINE_BOUND)

    def test_the_counts_are_consistent(self) -> None:
        counts: dict[str, int] = {}
        for row in self.rows.values():
            counts[row["class"]] = counts.get(row["class"], 0) + 1
        self.assertEqual(counts, self.census["counts"])
        self.assertEqual(sum(counts.values()), len(declared()))

    def test_the_status_prose_reports_the_same_counts(self) -> None:
        """The prose and the machine-readable census cannot drift."""
        status = (HERE / "STATUS.md").read_text(encoding="utf-8")
        counts = self.census["counts"]
        own = sum(v for k, v in counts.items() if k != "RECONSTRUCTION")
        for value in (
            counts["RECONSTRUCTION"],
            counts["DEFINITION"],
            counts["THIN"],
            counts["CONTENT"],
            own,
            sum(counts.values()),
        ):
            self.assertIn(str(value), status)

    def test_the_headline_conjunction_is_declared_definitional(self) -> None:
        """The finding the adversarial reading turned up, pinned so it
        cannot quietly be relabelled: the headline conjunction is an
        assembly of definitional facts and is classed as one."""
        self.assertEqual(self.rows["no_first_demand"]["class"], "DEFINITION")


class LeanVerifierTests(unittest.TestCase):
    def test_private_and_attributed_axioms_are_forbidden(self) -> None:
        """NEGATIVE: declaration modifiers may not hide a user axiom."""
        for text in (
            "private ax" + "iom hidden : False\n",
            "@[irreducible] protected ax" + "iom hidden : False\n",
        ):
            self.assertIsNotNone(lean_audit.LEADING_AXIOM.search(text))

    def test_attributed_theorem_is_in_the_axiom_population(self) -> None:
        text = "@[simp] theorem marked (n : Nat) : n = n := rfl\n"
        self.assertEqual(lean_audit.THEOREM_DECL.findall(text), ["marked"])

    def test_comment_line_that_begins_with_theorem_is_not_a_declaration(self) -> None:
        text = "/-- prose\ntheorem in this sentence is not Lean code -/\n"
        visible = lean_audit.declaration_text(text)
        self.assertEqual(lean_audit.THEOREM_DECL.findall(visible), [])

    def test_module_census_is_recursive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lean = pathlib.Path(tmp)
            nested = lean / "SecondNoFirst" / "Nested"
            nested.mkdir(parents=True)
            (nested / "Probe.lean").write_text("theorem probe : True := by trivial\n")
            report = lean / "SecondNoFirst" / "AxiomReport.lean"
            report.write_text("\n")
            with mock.patch.object(lean_audit, "LEAN", lean):
                self.assertEqual(
                    [path.name for path in lean_audit.modules()], ["Probe.lean"]
                )

    def test_failed_lake_clean_stops_before_build(self) -> None:
        failed = subprocess.CompletedProcess(
            args=["lake", "clean"], returncode=7, stdout="", stderr="probe failure"
        )
        with mock.patch.object(subprocess, "run", return_value=failed) as run:
            stage, code, log = lean_audit.build()
        self.assertEqual((stage, code), ("clean", 7))
        self.assertIn("probe failure", log)
        run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
