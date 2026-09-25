"""The census of the Lean package, and the frozen prediction it is scored
against.

A hand copy of `research/second_succession/test_census.py`, with this
rung's modules, counts and ledger rows, and with this rung's
statement-shape checks in place of rung six's.

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

LEAN = HERE / "lean" / "SecondDuration"
CENSUS = HERE / "FWDEF_CENSUS.json"
LOG = HERE / "receipts" / "lean_axioms.txt"
PREDICTIONS = HERE / "PREDICTIONS.md"
LEDGER = HERE / "CLAIM_LEDGER.md"

MODULES = (
    "Kernel.lean",
    "Rounds.lean",
    "Gaps.lean",
)
RECONSTRUCTED = ("Kernel.lean",)
NATIVE = ("Rounds.lean", "Gaps.lean")
TEST_FILES = (
    "test_census.py",
    "test_forbidden.py",
    "test_pins.py",
    "test_reconstruction.py",
    "test_duration.py",
)
# A DEFINITION row may not carry a proof longer than this many lines.  The
# bound is on the class, not on the file: a long proof classed DEFINITION
# is the shape that hides content, which is why the exception list is
# separate and countable.
DEFINITION_PROOF_LINES = 12

# The scoring of the frozen FW-DEF prediction, computed by this file and
# dated in STATUS.md (2026-09-25).
PREDICTED_NAMES = 16
PREDICTED_CLASS_HITS = 13
PREDICTED_CLASS_MISSES = 3
UNPREDICTED_NATIVE = 0
# The three misses, by name and direction (predicted, actual), dated in
# STATUS.md.
MISSES = {
    "growths_counted": ("THIN", "CONTENT"),
    "naming_bounded": ("CONTENT", "THIN"),
    "naming_step": ("THIN", "CONTENT"),
}


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
            {"CONTENT": 3, "DEFINITION": 3, "RECONSTRUCTION": 17, "THIN": 10},
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
        self.assertEqual(misses, sorted(MISSES))

    def test_the_unpredicted_native_declarations_are_counted(self) -> None:
        native = {
            name
            for name, row in self.actual.items()
            if row["module"] not in RECONSTRUCTED
        }
        self.assertEqual(len(native - set(self.predicted)), UNPREDICTED_NATIVE)

    def test_every_miss_is_the_dated_one(self) -> None:
        """Three misses at the dated values, two promotions and one
        demotion, each named with its direction.  A later
        reclassification of any row fails here by name rather than
        passing as a new hit or a new miss."""
        for name, cls in self.predicted.items():
            actual = self.actual[name]["class"]
            if actual != cls:
                self.assertEqual(MISSES.get(name), (cls, actual), name)
            else:
                self.assertNotIn(name, MISSES, name)

    def test_the_census_note_records_the_misses(self) -> None:
        note = json.loads(CENSUS.read_text(encoding="utf-8"))["note"]
        for name in MISSES:
            self.assertIn(name, note, name)
        self.assertIn("recorded as misses in STATUS.md", note)


class StatementShapeTests(unittest.TestCase):
    """The frozen Lean-side predictions whose evidence is the statement
    text: what each theorem assumes, and what it does not."""

    def test_n1_growths_and_rest_rounds_are_read_off_base_and_regime(self) -> None:
        grown = signature("Rounds.lean", "growths_counted")
        self.assertIn("replayE h b = some r → r.data = b.data + growths b h", grown)
        rested = signature("Rounds.lean", "rest_counted")
        self.assertIn("replayE h b = some r → size r = size b + growths b h + rest b h", rested)
        for name in ("growths_counted", "rest_counted"):
            stated = signature("Rounds.lean", name)
            self.assertNotIn("Decidable", stated, name)
            self.assertNotIn(".wf", stated, name)
        for name, quantity in (("growths_given_base", "growths b h"), ("rest_given_base", "rest b h")):
            given = signature("Rounds.lean", name)
            self.assertIn("∃ F : Regime → Regime → Nat", given, name)
            self.assertIn(f"replayE h b = some r → {quantity} = F b r", given, name)

    def test_n2_a_segment_is_refused_given_the_base(self) -> None:
        refused = signature("Gaps.lean", "segment_not_given_base")
        self.assertTrue(refused.startswith(": ¬ ∃ F : Nat → Regime → Regime → Nat"), refused)
        self.assertIn("during n b h = F n b r", refused)
        split = signature("Gaps.lean", "lead_splits")
        self.assertIn("[.admitForm 1, .admitDatum] genesis", split)
        self.assertIn("[.admitDatum, .admitForm 1] genesis", split)

    def test_n3_a_duration_between_growths_is_refused_from_the_empty_regime(self) -> None:
        refused = signature("Gaps.lean", "gap_not_from_genesis")
        self.assertTrue(refused.startswith(": ¬ ∃ F : Regime → Nat"), refused)
        self.assertIn("replayE h genesis = some r → during 1 genesis h = F r", refused)
        split = signature("Gaps.lean", "gap_splits")
        self.assertIn("[.admitDatum, .admitForm 1, .admitDatum] genesis", split)
        self.assertIn("[.admitDatum, .admitDatum, .admitForm 1] genesis", split)

    def test_n2_n3_the_two_countermodels_are_kernel_computations(self) -> None:
        text = lean_audit.declaration_text(
            (LEAN / "Gaps.lean").read_text(encoding="utf-8")
        )
        rows = census()
        for name in ("lead_splits", "gap_splits"):
            body = text.split(f"theorem {name} ")[1].split("theorem ")[0]
            self.assertIn("decide", body, name)
            self.assertIn("genesis", body, name)
            self.assertEqual(rows[name]["class"], "DEFINITION", name)

    def test_n4_the_lower_bound_needs_no_well_formed_base(self) -> None:
        bound = signature("Rounds.lean", "naming_bounded")
        self.assertIn(
            "replayE h b = some r → naming t r ≤ naming t b + after t b h", bound
        )
        self.assertNotIn(".wf", bound)
        below = signature("Rounds.lean", "after_le_rest")
        self.assertIn("after t b h ≤ rest b h", below)
        self.assertNotIn("replayE", below)

    def test_n5_the_tail_is_forced_when_everything_names_late(self) -> None:
        forced = signature("Gaps.lean", "tail_forced")
        self.assertIn("(hb : naming t b = 0)", forced)
        self.assertIn("(hn : naming t r = rest b h)", forced)
        self.assertIn("after t b h = rest b h", forced)
        pinned = signature("Gaps.lean", "pinned_by_requirement")
        self.assertIn("replayE h genesis = some ⟨2, [], [], [], [(0, 1)]⟩", pinned)
        self.assertIn("rest genesis h = 1 ∧ after 1 genesis h = 1", pinned)

    def test_n6_no_theorem_mentions_the_isomorphism_or_attainment(self) -> None:
        """That the vectors reached are exactly the envelope, and anything
        taken up to the isomorphism, are NOT proved here: no native module
        names the sealed isomorphism, a bijection, a class key, or the
        envelope."""
        text = native_text()
        for word in ("Iso", "iso", "bijection", "canonical", "envelope", "Envelope"):
            self.assertNotIn(word, text, word)

    def test_the_definition_rows_are_at_the_level_of_a_definition(self) -> None:
        rows = census()
        for name in ("replayE_cons", "lead_splits", "gap_splits"):
            self.assertEqual(rows[name]["class"], "DEFINITION", name)

    def test_the_two_restated_lemmas_credit_rung_six(self) -> None:
        """`replayE_cons` and `insertNew_grows` repeat rung six's lemmas;
        the module that proves them says so, and so does the census
        note."""
        text = (LEAN / "Rounds.lean").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("`replayE_cons` and `insertNew_grows` repeat, as statements, rung six's", text)
        note = json.loads(CENSUS.read_text(encoding="utf-8"))["note"]
        self.assertIn("replayE_cons and insertNew_grows repeat, as statements, rung six's", note)


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
    """Prediction N-15: exactly one row of the challenge-five census is
    decided here -- duration, under the CHANGING reading -- and it says
    that FORCED is conditional on an engine that does not exist yet, that
    the durations between growths are not definable, and that attainment
    of the envelope and the class-level question are OPEN beyond the
    rectangle.  N-6: neither is claimed."""

    def test_the_ledger_decides_exactly_one_census_row(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        rows = re.findall(r"^\| CENSUS-([a-z]+) \|", text, re.M)
        self.assertEqual(rows, ["duration"])

    def test_the_census_row_carries_the_engine_condition(self) -> None:
        self.assertIn("conditional on an engine", ledger_row("| CENSUS-duration"))

    def test_the_census_row_names_its_evidence(self) -> None:
        row = ledger_row("| CENSUS-duration")
        for name in (
            "gap_not_from_genesis", "segment_not_given_base", "growths_given_base",
            "rest_given_base", "naming_bounded", "tail_forced",
        ):
            self.assertIn(name, row, name)
        self.assertIn("CHANGING", row)

    def test_the_durations_between_growths_are_not_definable(self) -> None:
        row = ledger_row("| CENSUS-duration")
        self.assertIn("NOT DEFINABLE", row)
        self.assertNotIn("between growths DEFINABLE", row)

    def test_attainment_and_the_class_level_question_are_open(self) -> None:
        row = ledger_row("| CENSUS-duration")
        self.assertIn("OPEN", row)
        self.assertIn("V-1", row)
        self.assertIn("Z-1", row)

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
