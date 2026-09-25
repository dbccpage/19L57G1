"""The census of the Lean package, and the frozen prediction it is scored
against.

A hand copy of `research/second_symmetry/test_census.py`, with this
rung's modules, counts and ledger rows, and with this rung's
statement-shape checks in place of rung five's.

Five things are checked here, none implying the others:

* the FW-DEF census is TOTAL over the package's theorem declarations, in
  both directions, read from the sources with the same parser the Lean
  audit uses;
* no row classed DEFINITION carries a long proof, unless it is listed as
  an exception with a reason, so the class cannot absorb content;
* the frozen FW-DEF prediction of `PREDICTIONS.md` is scored MECHANICALLY
  against the committed census: the hit and miss counts are computed here
  and asserted at the values `STATUS.md` dates, so a later silent
  reclassification changes this file too;
* the statement text of the theorems the frozen Lean-side predictions
  name: what each assumes and what it does not;
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

LEAN = HERE / "lean" / "SecondSuccession"
CENSUS = HERE / "FWDEF_CENSUS.json"
LOG = HERE / "receipts" / "lean_axioms.txt"
PREDICTIONS = HERE / "PREDICTIONS.md"
LEDGER = HERE / "CLAIM_LEDGER.md"

MODULES = (
    "Kernel.lean",
    "Count.lean",
    "Readings.lean",
)
RECONSTRUCTED = ("Kernel.lean",)
NATIVE = ("Count.lean", "Readings.lean")
TEST_FILES = (
    "test_census.py",
    "test_forbidden.py",
    "test_pins.py",
    "test_reconstruction.py",
    "test_succession.py",
)
# A DEFINITION row may not carry a proof longer than this many lines.  The
# bound is on the class, not on the file: a long proof classed DEFINITION
# is the shape that hides content, which is why the exception list is
# separate and countable.
DEFINITION_PROOF_LINES = 12

# The scoring of the frozen FW-DEF prediction, computed by this file and
# dated in STATUS.md (2026-09-25).
PREDICTED_NAMES = 17
PREDICTED_CLASS_HITS = 17
PREDICTED_CLASS_MISSES = 0
UNPREDICTED_NATIVE = 0


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


def signature(module: str, name: str) -> str:
    """The statement of a theorem, from its name to its `:=` or to its
    first equation, comments stripped and whitespace collapsed."""
    text = lean_audit.declaration_text((LEAN / module).read_text(encoding="utf-8"))
    body = text.split(f"theorem {name} ")[1].split(":=")[0].split("\n  |")[0]
    return " ".join(body.split())


def native_text() -> str:
    return "\n".join(
        lean_audit.declaration_text((LEAN / module).read_text(encoding="utf-8"))
        for module in NATIVE
    )


def ledger_row(prefix: str) -> str:
    text = LEDGER.read_text(encoding="utf-8")
    return next(line for line in text.split("\n") if line.startswith(prefix))


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
        """A theorem reproduced under a pin is the sealed estate's result
        and is never counted as this rung's content."""
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
            {"CONTENT": 1, "DEFINITION": 6, "RECONSTRUCTION": 17, "THIN": 10},
        )

    def test_no_definition_row_hides_a_long_proof(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        exceptions = payload["long_but_definitional"]
        lengths = proof_lengths()
        for name, row in payload["classes"].items():
            if row["class"] != "DEFINITION" or name in exceptions:
                continue
            self.assertLessEqual(lengths[name], DEFINITION_PROOF_LINES, name)
        self.assertEqual(sorted(exceptions), [])
        for name in exceptions:
            self.assertEqual(payload["classes"][name]["class"], "DEFINITION")
            self.assertGreater(lengths[name], DEFINITION_PROOF_LINES, name)

    def test_the_length_reader_finds_the_longest_proof(self) -> None:
        """Not a vacuous bound: the package does carry proofs longer than
        the DEFINITION limit, and they are classed otherwise."""
        lengths = proof_lengths()
        self.assertGreater(max(lengths.values()), DEFINITION_PROOF_LINES)


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
        self.assertEqual(misses, [])

    def test_the_unpredicted_native_declarations_are_counted(self) -> None:
        native = {
            name
            for name, row in self.actual.items()
            if row["module"] not in RECONSTRUCTED
        }
        self.assertEqual(len(native - set(self.predicted)), UNPREDICTED_NATIVE)

    def test_every_miss_is_a_demotion(self) -> None:
        """There are no misses at the dated values.  The test is kept so
        that a later reclassification that PROMOTES a target fails here
        by name rather than passing as a new hit."""
        order = {"DEFINITION": 0, "THIN": 1, "CONTENT": 2}
        for name, cls in self.predicted.items():
            actual = self.actual[name]["class"]
            if actual != cls:
                self.assertLess(order[actual], order[cls], name)


class StatementShapeTests(unittest.TestCase):
    """The frozen Lean-side predictions whose evidence is the statement
    text: what each theorem assumes, and what it does not."""

    def test_m1_the_changing_count_is_read_off_base_and_regime(self) -> None:
        stated = signature("Count.lean", "changes_counted")
        self.assertIn("replayE h b = some r → size r = size b + changes b h", stated)
        self.assertNotIn("Decidable", stated)
        self.assertNotIn(".wf", stated)
        free = signature("Count.lean", "changes_path_free")
        self.assertIn("(hr : replayE h b = some r) (hr' : replayE h' b = some r)", free)
        self.assertIn("changes b h = changes b h'", free)
        given = signature("Count.lean", "changes_given_base")
        self.assertIn("∃ F : Regime → Regime → Nat", given)
        self.assertIn("replayE h b = some r → changes b h = F b r", given)

    def test_m2_from_the_empty_regime_no_base_is_named(self) -> None:
        stated = signature("Count.lean", "changes_from_genesis")
        self.assertIn("replayE h genesis = some r", stated)
        self.assertIn("changes genesis h = size r", stated)
        self.assertIn("size genesis = 0", signature("Count.lean", "size_genesis"))

    def test_m3_every_and_admitting_are_refuted_given_the_base(self) -> None:
        every = signature("Readings.lean", "every_not_given_base")
        self.assertTrue(every.startswith(": ¬ ∃ F : Regime → Regime → Nat"), every)
        self.assertIn("h.length = F b r", every)
        admitting = signature("Readings.lean", "admitting_not_given_base")
        self.assertTrue(admitting.startswith(": ¬ ∃ F : Regime → Regime → Nat"), admitting)
        self.assertIn("admitting h = F b r", admitting)

    def test_m3_the_two_countermodels_are_kernel_computations(self) -> None:
        text = lean_audit.declaration_text(
            (LEAN / "Readings.lean").read_text(encoding="utf-8")
        )
        rows = census()
        for name in ("every_splits", "admitting_splits"):
            body = text.split(f"theorem {name} ")[1].split("theorem ")[0]
            self.assertIn("decide", body, name)
            self.assertIn("genesis", body, name)
            self.assertEqual(rows[name]["class"], "DEFINITION", name)
        self.assertIn(
            "[.admitForm 1, .admitRuleAll 0, .admitRuleAll 0]",
            signature("Readings.lean", "admitting_splits"),
        )
        self.assertIn("[.supply 0]", signature("Readings.lean", "every_splits"))

    def test_m4_the_regime_alone_does_not_give_the_changing_count(self) -> None:
        stated = signature("Readings.lean", "changing_not_of_regime")
        self.assertTrue(stated.startswith(": ¬ ∃ F : Regime → Nat"), stated)
        self.assertIn("changes b h = F r", stated)
        matters = signature("Readings.lean", "base_matters")
        self.assertIn("= some R2L", matters)
        self.assertIn("= 3", matters)
        self.assertIn("changes R2L [] = 0", matters)

    def test_m5_the_three_counts_are_ordered_for_every_history(self) -> None:
        low = signature("Count.lean", "changes_le_admitting")
        self.assertIn("changes b h ≤ admitting h", low)
        self.assertNotIn("replayE", low)
        high = signature("Count.lean", "admitting_le_every")
        self.assertIn("admitting h ≤ h.length", high)
        self.assertNotIn("replayE", high)

    def test_m6_no_theorem_mentions_the_isomorphism(self) -> None:
        """That the count is a function of the class of a regime is NOT
        proved here: no native module names the sealed isomorphism, a
        bijection, or a class key."""
        text = native_text()
        for word in ("Iso", "iso", "bijection", "canonical"):
            self.assertNotIn(word, text, word)

    def test_the_definition_rows_are_at_the_level_of_a_definition(self) -> None:
        rows = census()
        for name in ("supply_uncounted", "replayE_cons", "size_genesis", "base_matters"):
            self.assertEqual(rows[name]["class"], "DEFINITION", name)

    def test_the_two_restated_theorems_credit_rung_five(self) -> None:
        """`step_grows` and `changes_counted` repeat rung five's
        statements; the module that proves them says so, and so does the
        census note."""
        text = (LEAN / "Count.lean").read_text(encoding="utf-8")
        self.assertIn("`size_counts_changes`", text)
        self.assertIn("(rung five's `size_step`)", text)
        note = json.loads(CENSUS.read_text(encoding="utf-8"))["note"]
        self.assertIn("rung five's size_step and size_counts_changes", note)


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
        self.assertIn(":: none", LOG.read_text(encoding="utf-8"))


class LedgerTests(unittest.TestCase):
    """Prediction M-14: exactly one row of the challenge-five census is
    decided here -- succession, under the three declared readings -- and
    it says that FORCED is conditional on an engine that does not exist
    yet, that the class-level question is OPEN beyond the rectangle, and
    that rungs three and four's readings stand.  M-6: the class-level
    question is OPEN."""

    def test_the_ledger_decides_exactly_one_census_row(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        rows = re.findall(r"^\| CENSUS-([a-z]+) \|", text, re.M)
        self.assertEqual(rows, ["succession"])

    def test_the_census_row_carries_the_engine_condition(self) -> None:
        self.assertIn("conditional on an engine", ledger_row("| CENSUS-succession"))

    def test_the_census_row_names_every_reading(self) -> None:
        row = ledger_row("| CENSUS-succession")
        for reading in ("EVERY", "ADMITTING", "CHANGING"):
            self.assertIn(reading, row, reading)
        for name in (
            "changes_given_base", "changes_from_genesis", "changing_not_of_regime",
            "every_not_given_base", "admitting_not_given_base",
        ):
            self.assertIn(name, row, name)

    def test_the_class_level_question_is_open(self) -> None:
        row = ledger_row("| CENSUS-succession")
        self.assertIn("OPEN", row)
        self.assertIn("Z-1", row)

    def test_the_earlier_readings_stand(self) -> None:
        row = ledger_row("| CENSUS-succession")
        self.assertIn("rung three's and rung four's readings stand", row.lower())
        self.assertNotIn("withdrawn", row.lower())
        self.assertNotIn("superseded", row.lower())

    def test_every_ledger_row_names_evidence_that_exists(self) -> None:
        """A ledger row's Lean evidence must be a theorem of this package,
        and its Python evidence a test that exists."""
        rows = census()
        text = LEDGER.read_text(encoding="utf-8")
        cited = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_']*)`", text))
        lean_cited = cited & set(rows)
        self.assertGreater(len(lean_cited), 12)
        for name in re.findall(r"`(test_[a-z0-9_]+)`", text):
            found = any(
                name in (HERE / module).read_text(encoding="utf-8")
                for module in TEST_FILES
            )
            self.assertTrue(found, name)


if __name__ == "__main__":
    unittest.main()
