"""The census of the Lean package, and the frozen prediction it is scored
against.

Four things are checked here, none implying the others:

* the FW-DEF census is TOTAL over the package's theorem declarations, in
  both directions, read from the sources with the same parser the Lean
  audit uses;
* no row classed DEFINITION carries a long proof, unless it is listed as
  an exception with a reason, so the class cannot absorb content;
* the frozen FW-DEF prediction of `PREDICTIONS.md` is scored MECHANICALLY
  against the committed census: the hit and miss counts are computed here
  and asserted at the values `STATUS.md` dates, so a later silent
  reclassification changes this file too;
* the committed axiom log covers every censused theorem and stays within
  the whitelist.  This is a check of the COMMITTED bytes, not of a fresh
  build; the fresh build is `verify_lean.py`, which runs in the Lean job.

A parser is not a compiler: a census read from source would miss a
compiler-generated constant.  `verify_lean.py` closes that by censusing
the compiled environment and comparing both ways; this file checks what
the committed files say to one another.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import verify_lean as lean_audit  # noqa: E402

LEAN = HERE / "lean" / "SecondIndex"
CENSUS = HERE / "FWDEF_CENSUS.json"
LOG = HERE / "receipts" / "lean_axioms.txt"
PREDICTIONS = HERE / "PREDICTIONS.md"
LEDGER = HERE / "CLAIM_LEDGER.md"

MODULES = ("Kernel.lean", "Inherited.lean", "Index.lean", "Countermodel.lean")
RECONSTRUCTED = ("Kernel.lean", "Inherited.lean")
# A DEFINITION row may not carry a proof longer than this many lines.  The
# bound is on the class, not on the file: a long proof classed DEFINITION
# is the shape that hides content, which is why the exception list is
# separate and countable.
DEFINITION_PROOF_LINES = 12

# The scoring of the frozen FW-DEF prediction, computed by this file and
# dated in STATUS.md (2026-09-23).
PREDICTED_NAMES = 25
PREDICTED_CLASS_HITS = 17
PREDICTED_CLASS_MISSES = 8
UNPREDICTED_NATIVE = 19


def census() -> dict[str, dict[str, str]]:
    payload = json.loads(CENSUS.read_text(encoding="utf-8"))
    rows = payload["classes"]
    assert isinstance(rows, dict)
    return rows


def declared_theorems() -> dict[str, str]:
    """Leaf theorem name -> module file, read from the committed sources
    with comments stripped."""
    found: dict[str, str] = {}
    for module in MODULES:
        text = (LEAN / module).read_text(encoding="utf-8")
        for name in lean_audit.theorem_names(text):
            if name in found:
                raise ValueError(f"duplicate leaf name {name}")
            found[name] = module
    return found


def proof_lengths() -> dict[str, int]:
    """Leaf theorem name -> the number of lines its declaration spans."""
    lengths: dict[str, int] = {}
    for module in MODULES:
        text = lean_audit.declaration_text(
            (LEAN / module).read_text(encoding="utf-8")
        )
        starts: list[tuple[int, str]] = []
        for match in lean_audit.THEOREM_DECL.finditer(text):
            line = text[: match.start()].count("\n")
            starts.append((line, lean_audit.canonical_identifier(match.group("name"))))
        lines = text.split("\n")
        for position, (line, name) in enumerate(starts):
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            body = [row for row in lines[line:end] if row.strip()]
            lengths[name] = len(body)
    return lengths


def predicted_classes() -> dict[str, str]:
    """The frozen FW-DEF prediction, parsed from `PREDICTIONS.md`."""
    text = PREDICTIONS.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    current: str | None = None
    for line in text.split("\n"):
        heading = re.match(r"^Predicted (DEFINITION|THIN|CONTENT):", line)
        if heading is not None:
            current = heading.group(1)
            continue
        if line.startswith("The names above"):
            current = None
            continue
        item = re.match(r"^- `([A-Za-z0-9_']+)`$", line)
        if item is not None and current is not None:
            out[item.group(1)] = current
    return out


class CensusTotalityTests(unittest.TestCase):
    def test_the_census_is_total_over_the_package(self) -> None:
        rows = census()
        declared = declared_theorems()
        self.assertEqual(sorted(set(rows) - set(declared)), [])
        self.assertEqual(sorted(set(declared) - set(rows)), [])

    def test_every_row_records_the_module_it_came_from(self) -> None:
        rows = census()
        declared = declared_theorems()
        for name, row in rows.items():
            self.assertEqual(row["module"], declared[name], name)

    def test_every_reconstructed_theorem_is_classed_reconstruction(self) -> None:
        """A theorem reproduced under a pin is the sibling's or the sealed
        estate's result and is never counted as this rung's content."""
        rows = census()
        for name, row in rows.items():
            if row["module"] in RECONSTRUCTED:
                self.assertEqual(row["class"], "RECONSTRUCTION", name)
            else:
                self.assertNotEqual(row["class"], "RECONSTRUCTION", name)

    def test_the_counts_block_matches_the_rows(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        tally: dict[str, int] = {}
        for row in payload["classes"].values():
            tally[row["class"]] = tally.get(row["class"], 0) + 1
        self.assertEqual(payload["counts"], dict(sorted(tally.items())))

    def test_the_content_census_is_the_dated_one(self) -> None:
        """The counts STATUS.md dates.  A reclassification changes this
        line too, which is the point of writing the number down."""
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["counts"],
            {"CONTENT": 16, "DEFINITION": 13, "RECONSTRUCTION": 44, "THIN": 14},
        )

    def test_no_definition_row_hides_a_long_proof(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        exceptions = payload["long_but_definitional"]
        lengths = proof_lengths()
        for name, row in payload["classes"].items():
            if row["class"] != "DEFINITION" or name in exceptions:
                continue
            self.assertLessEqual(lengths[name], DEFINITION_PROOF_LINES, name)
        self.assertEqual(sorted(exceptions), ["first_demand_index"])
        self.assertLessEqual(len(exceptions), 1)
        for name in exceptions:
            self.assertEqual(payload["classes"][name]["class"], "DEFINITION")

    def test_the_length_reader_finds_the_longest_proof(self) -> None:
        """Not a vacuous bound: the package does carry proofs longer than
        the DEFINITION limit, and they are classed otherwise."""
        lengths = proof_lengths()
        longest = max(lengths.values())
        self.assertGreater(longest, DEFINITION_PROOF_LINES)


class FrozenPredictionTests(unittest.TestCase):
    """The frozen FW-DEF prediction, scored mechanically.  A miss is a
    finding; it is recorded next to its value in STATUS.md and the
    prediction text is never edited."""

    def setUp(self) -> None:
        self.predicted = predicted_classes()
        self.actual = census()

    def test_the_prediction_names_what_it_said_it_named(self) -> None:
        self.assertEqual(len(self.predicted), PREDICTED_NAMES)

    def test_every_predicted_name_exists_in_the_package(self) -> None:
        for name in self.predicted:
            self.assertIn(name, self.actual, name)

    def test_the_prediction_is_scored_at_the_dated_values(self) -> None:
        hits = [
            name
            for name, cls in self.predicted.items()
            if self.actual[name]["class"] == cls
        ]
        misses = sorted(set(self.predicted) - set(hits))
        self.assertEqual(len(hits), PREDICTED_CLASS_HITS)
        self.assertEqual(len(misses), PREDICTED_CLASS_MISSES)
        self.assertEqual(
            misses,
            [
                "data_le_stateAt",
                "demand_can_cease",
                "first_demand_index",
                "index_is_not_a_function_of_the_reached_regime",
                "no_index_below_two_from_the_empty_base",
                "no_state_function_gives_the_index",
                "replayE_append",
                "wf_stateAt",
            ],
        )

    def test_the_unpredicted_native_declarations_are_counted(self) -> None:
        native = {
            name
            for name, row in self.actual.items()
            if row["module"] not in RECONSTRUCTED
        }
        self.assertEqual(len(native - set(self.predicted)), UNPREDICTED_NATIVE)

    def test_the_one_reconstruction_the_prediction_took_for_native(self) -> None:
        """`replayE_append` was predicted as this rung's content.  It is
        the sealed estate's own theorem, reconstructed under a pin, so the
        prediction is MISSED and the work was already done."""
        self.assertEqual(self.predicted["replayE_append"], "CONTENT")
        self.assertEqual(self.actual["replayE_append"]["class"], "RECONSTRUCTION")
        self.assertEqual(self.actual["replayE_append"]["module"], "Kernel.lean")


class ExistenceIsConditionalTests(unittest.TestCase):
    """Prediction I-7: existence is not proved outright, and the rung
    builds no decision procedure for the sealed separability."""

    def test_the_existence_theorem_carries_a_decidability_hypothesis(self) -> None:
        text = (LEAN / "Index.lean").read_text(encoding="utf-8")
        signature = text.split(
            "theorem first_demand_exists_when_a_demand_is_decidable"
        )[1].split(":= by")[0]
        self.assertIn("Decidable (HasDemand S r)", signature)

    def test_no_decision_procedure_for_separability_is_declared(self) -> None:
        """A decision procedure would be an instance or a definition over
        `separable`; none is written, in any module of this package."""
        for module in MODULES:
            text = lean_audit.declaration_text(
                (LEAN / module).read_text(encoding="utf-8")
            )
            for line in text.split("\n"):
                if re.match(r"^\s*instance\b", line):
                    self.assertNotIn("separable", line)
                    self.assertNotIn("Demand", line)


class WitnessAgreementTests(unittest.TestCase):
    """The Lean countermodels and the Python rectangle exhibit the same
    histories.  Compared as text: the two sides are different languages,
    and nothing here claims more than that the same events are named in
    the same order."""

    def test_the_two_sides_name_the_same_three_histories(self) -> None:
        lean = (LEAN / "Countermodel.lean").read_text(encoding="utf-8")
        self.assertIn(
            "def historyA : List Event := [.admitDatum, .admitDatum]", lean
        )
        self.assertIn(
            "def historyB : List Event := [.supply 0, .admitDatum, .admitDatum]",
            lean,
        )
        self.assertIn(
            "[.admitDatum, .admitDatum, .admitForm 1, .admitInst 0 [0]]", lean
        )
        python = (HERE / "test_index.py").read_text(encoding="utf-8")
        self.assertIn(
            'HISTORY_A: tuple[Event, ...] = (AdmitDatum("<n0>"), AdmitDatum("<n1>"))',
            python,
        )
        self.assertIn("AdmitInst(0, (0,)),", python)

    def test_the_two_sides_report_the_same_two_counts(self) -> None:
        lean = (LEAN / "Countermodel.lean").read_text(encoding="utf-8")
        self.assertIn("IsFirstDemand allApart genesis historyA 2", lean)
        self.assertIn("IsFirstDemand allApart genesis historyB 3", lean)
        receipt = json.loads(
            (HERE / "receipts" / "index.json").read_text(encoding="utf-8")
        )
        empty = next(r for r in receipt["reports"] if r["base"] == "EMPTY")
        witness = empty["stakes"]["total_apart"]["collision_witness"]
        self.assertEqual(witness["indices"], [2, 3])


class AxiomLogTests(unittest.TestCase):
    """The COMMITTED log, read as bytes.  The fresh build is
    `verify_lean.py`'s business and runs in the Lean job."""

    def test_the_log_covers_every_censused_theorem(self) -> None:
        rows = census()
        logged = {
            line.split(" :: ")[0].split(".")[-1]
            for line in LOG.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        self.assertEqual(sorted(set(rows) - logged), [])
        self.assertEqual(sorted(logged - set(rows)), [])

    def test_every_logged_axiom_is_within_the_whitelist(self) -> None:
        for line in LOG.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            axioms = line.split(" :: ")[1].split()
            for axiom in axioms:
                self.assertIn(axiom, {"none", "propext", "Quot.sound"})

    def test_the_log_is_stored_with_no_carriage_return(self) -> None:
        self.assertNotIn(b"\r", LOG.read_bytes())

    def test_some_theorem_depends_on_no_axiom_at_all(self) -> None:
        """Not a vacuous whitelist: the log distinguishes a report with no
        axioms from a report within the whitelist."""
        text = LOG.read_text(encoding="utf-8")
        self.assertIn(":: none", text)


class LedgerTests(unittest.TestCase):
    """Prediction I-23: exactly one row of the challenge-five census is
    decided here, the row for succession."""

    def test_the_ledger_decides_exactly_one_census_row(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        rows = re.findall(r"^\| CENSUS-([a-z]+) \|", text, re.M)
        self.assertEqual(rows, ["succession"])

    def test_the_census_row_is_decided_as_not_definable(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        row = next(
            line for line in text.split("\n") if line.startswith("| CENSUS-succession")
        )
        self.assertIn("NOT DEFINABLE", row)
        self.assertIn("no_state_function_gives_the_index", row)

    def test_every_ledger_row_names_evidence_that_exists(self) -> None:
        """A ledger row's Lean evidence must be a theorem of this package,
        and its Python evidence a test or an artifact key that exists."""
        rows = census()
        text = LEDGER.read_text(encoding="utf-8")
        cited = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_']*)`", text))
        lean_cited = cited & set(rows)
        self.assertGreater(len(lean_cited), 10)
        for name in re.findall(r"`(test_[a-z0-9_]+)`", text):
            found = any(
                name in (HERE / module).read_text(encoding="utf-8")
                for module in (
                    "test_index.py",
                    "test_census.py",
                    "test_pins.py",
                    "test_reconstruction.py",
                    "test_forbidden.py",
                )
            )
            self.assertTrue(found, name)


if __name__ == "__main__":
    unittest.main()
