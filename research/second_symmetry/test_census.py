"""The census of the Lean package, and the frozen prediction it is scored
against.

A hand copy of `research/second_iso/test_census.py`, with this rung's
modules, counts and ledger rows, and with this rung's statement-shape
checks in place of rung four's.

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

LEAN = HERE / "lean" / "SecondSymmetry"
CENSUS = HERE / "FWDEF_CENSUS.json"
LOG = HERE / "receipts" / "lean_axioms.txt"
PREDICTIONS = HERE / "PREDICTIONS.md"
LEDGER = HERE / "CLAIM_LEDGER.md"

MODULES = (
    "Kernel.lean",
    "IsoKernel.lean",
    "Aut.lean",
    "Meet.lean",
    "Grow.lean",
    "Witness.lean",
)
RECONSTRUCTED = ("Kernel.lean", "IsoKernel.lean")
NATIVE = ("Aut.lean", "Meet.lean", "Grow.lean", "Witness.lean")
TEST_FILES = (
    "test_census.py",
    "test_forbidden.py",
    "test_pins.py",
    "test_reconstruction.py",
    "test_symmetry.py",
)
ADDING = ("inst", "rule", "req")
# A DEFINITION row may not carry a proof longer than this many lines.  The
# bound is on the class, not on the file: a long proof classed DEFINITION
# is the shape that hides content, which is why the exception list is
# separate and countable.
DEFINITION_PROOF_LINES = 12

# The scoring of the frozen FW-DEF prediction, computed by this file and
# dated in STATUS.md (2026-09-25).
PREDICTED_NAMES = 35
PREDICTED_CLASS_HITS = 27
PREDICTED_CLASS_MISSES = 8
UNPREDICTED_NATIVE = 12


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
    """The statement of a theorem, from its name to its `:=`, comments
    stripped and whitespace collapsed."""
    text = lean_audit.declaration_text((LEAN / module).read_text(encoding="utf-8"))
    body = text.split(f"theorem {name} ")[1].split(":=")[0]
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
            {"CONTENT": 6, "DEFINITION": 14, "RECONSTRUCTION": 17, "THIN": 27},
        )

    def test_no_definition_row_hides_a_long_proof(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        exceptions = payload["long_but_definitional"]
        lengths = proof_lengths()
        for name, row in payload["classes"].items():
            if row["class"] != "DEFINITION" or name in exceptions:
                continue
            self.assertLessEqual(lengths[name], DEFINITION_PROOF_LINES, name)
        self.assertEqual(sorted(exceptions), ["kinds_move_both_ways"])
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
        self.assertEqual(
            misses,
            [
                "inst_fixed_of_survives",
                "inst_meet",
                "inst_survives_of_fixed",
                "kinds_move_both_ways",
                "req_fixed_of_survives",
                "req_meet",
                "req_survives_of_fixed",
                "rule_meet",
            ],
        )

    def test_the_unpredicted_native_declarations_are_counted(self) -> None:
        native = {
            name
            for name, row in self.actual.items()
            if row["module"] not in RECONSTRUCTED
        }
        self.assertEqual(len(native - set(self.predicted)), UNPREDICTED_NATIVE)

    def test_every_miss_is_a_demotion(self) -> None:
        """All eight misses moved a target DOWN the order CONTENT, THIN,
        DEFINITION: the prediction over-rated the work, and never
        under-rated it."""
        order = {"DEFINITION": 0, "THIN": 1, "CONTENT": 2}
        for name, cls in self.predicted.items():
            actual = self.actual[name]["class"]
            if actual != cls:
                self.assertLess(order[actual], order[cls], name)


class StatementShapeTests(unittest.TestCase):
    """The frozen Lean-side predictions whose evidence is the statement
    text: what each theorem assumes, and what it does not."""

    def test_k1_the_fifteen_survival_theorems_exist(self) -> None:
        rows = census()
        for kind in ADDING:
            for suffix in (
                "fixed_of_survives", "survives_of_fixed", "descends_of_fixed",
                "meet", "meet_after",
            ):
                self.assertEqual(rows[f"{kind}_{suffix}"]["module"], "Meet.lean")

    def test_k1_no_survival_theorem_takes_a_decision(self) -> None:
        for kind in ADDING:
            for suffix in (
                "fixed_of_survives", "survives_of_fixed", "descends_of_fixed",
                "meet", "meet_after",
            ):
                stated = signature("Meet.lean", f"{kind}_{suffix}")
                self.assertNotIn("Decidable", stated, f"{kind}_{suffix}")

    def test_k1_only_the_descent_side_assumes_a_well_formed_regime(self) -> None:
        """Surviving into the regime after needs nothing of the regime
        before but the element's own bounds; descending from it needs the
        regime before well-formed, because an admitted element must be
        carried back inside the ranges."""
        for kind in ADDING:
            for suffix in ("fixed_of_survives", "survives_of_fixed", "meet"):
                self.assertNotIn(".wf", signature("Meet.lean", f"{kind}_{suffix}"))
            for suffix in ("descends_of_fixed", "meet_after"):
                self.assertIn("(hwf : r.wf)", signature("Meet.lean", f"{kind}_{suffix}"))

    def test_k1_the_meets_are_equivalences_with_fixing(self) -> None:
        self.assertIn(
            "Survives σ (addInst r e) ↔ instImage σ e = e", signature("Meet.lean", "inst_meet")
        )
        self.assertIn(
            "Survives σ (addRule r e) ↔ σ.fmap e = e", signature("Meet.lean", "rule_meet")
        )
        self.assertIn(
            "Survives σ (addReq r e) ↔ reqImage σ e = e", signature("Meet.lean", "req_meet")
        )
        self.assertIn(
            "(∃ σ : Iso r r, SameMaps τ σ) ↔ instImage τ e = e",
            signature("Meet.lean", "inst_meet_after"),
        )

    def test_k2_the_lifts_assume_only_well_formedness(self) -> None:
        for name, target in (("datum_lift", "addDatum r"), ("form_lift", "addForm r a")):
            stated = signature("Grow.lean", name)
            self.assertIn("(hwf : r.wf)", stated, name)
            self.assertIn(f"∃ τ : Iso ({target}) ({target})", stated, name)
            self.assertNotIn("Decidable", stated, name)

    def test_k4_the_witness_regimes_are_small_and_unary(self) -> None:
        text = (LEAN / "Witness.lean").read_text(encoding="utf-8")
        found = {
            name: (int(data), forms)
            for name, data, forms in re.findall(
                r"def (\w+R) : Regime := ⟨(\d+), \[([\d, ]*)\]", text
            )
        }
        self.assertEqual(
            sorted(found),
            ["instGainR", "instLossR", "reqGainR", "reqLossR", "ruleGainR", "ruleLossR"],
        )
        for name, (data, forms) in found.items():
            self.assertLessEqual(data, 3, name)
            arities = [f.strip() for f in forms.split(",") if f.strip()]
            self.assertLessEqual(len(arities), 2, name)
            self.assertTrue(all(a == "1" for a in arities), name)

    def test_k4_each_witness_is_closed_through_a_fixing_theorem(self) -> None:
        text = lean_audit.declaration_text((LEAN / "Witness.lean").read_text(encoding="utf-8"))
        for kind in ADDING:
            for side in ("loss", "gain"):
                body = text.split(f"theorem {kind}_{side} ")[1].split("theorem ")[0]
                self.assertIn(f"{kind}_fixed_of_survives", body, f"{kind}_{side}")

    def test_k5_no_theorem_counts_an_automorphism_set(self) -> None:
        text = native_text()
        for counting in ("card", "Finset", "Fintype", "List (Iso", "Array (Iso"):
            self.assertNotIn(counting, text, counting)

    def test_k6_every_event_keeps_the_regime_or_adds_one(self) -> None:
        self.assertIn("r' = r ∨ size r' = size r + 1", signature("Grow.lean", "size_step"))
        self.assertIn("r'' ≠ r", signature("Grow.lean", "no_return"))

    def test_k7_the_count_is_the_base_plus_the_changes(self) -> None:
        stated = signature("Grow.lean", "size_counts_changes")
        self.assertIn("replayE h b = some r → size r = size b + changes b h", stated)
        self.assertNotIn("Decidable", stated)

    def test_k8_no_theorem_carries_the_count_across_an_isomorphism(self) -> None:
        """Irreversibility up to the isomorphism is NOT proved here: no
        theorem statement mentions both an isomorphism and the element
        count."""
        text = native_text()
        for match in re.finditer(r"theorem (\w+)(.*?):=", text, re.S):
            stated = match.group(2)
            self.assertFalse(
                "Iso" in stated and "size" in stated, match.group(1)
            )

    def test_the_supply_row_is_at_the_level_of_a_definition(self) -> None:
        rows = census()
        self.assertEqual(rows["supply_keeps"]["class"], "DEFINITION")
        for name in ("stepE_inst", "stepE_rule", "stepE_req", "stepE_datum", "stepE_form"):
            self.assertEqual(rows[name]["class"], "DEFINITION", name)


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
    """Prediction K-18: exactly three rows of the challenge-five census are
    decided here -- symmetry along a history, invariants and
    irreversibility -- and each says that FORCED is conditional on an
    engine that does not exist yet.  K-8: irreversibility up to the
    isomorphism beyond the rectangle is OPEN."""

    def test_the_ledger_decides_exactly_three_census_rows(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        rows = re.findall(r"^\| CENSUS-([a-z]+) \|", text, re.M)
        self.assertEqual(rows, ["symmetry", "invariant", "irreversibility"])

    def test_every_census_row_carries_the_engine_condition(self) -> None:
        for name in ("symmetry", "invariant", "irreversibility"):
            self.assertIn("conditional on an engine", ledger_row(f"| CENSUS-{name}"), name)

    def test_the_symmetry_row_names_both_directions(self) -> None:
        row = ledger_row("| CENSUS-symmetry")
        self.assertIn("kinds_move_both_ways", row)
        self.assertIn("NEITHER", row)

    def test_the_class_level_return_is_open(self) -> None:
        row = ledger_row("| CENSUS-irreversibility")
        self.assertIn("no_return", row)
        self.assertIn("OPEN", row)

    def test_every_ledger_row_names_evidence_that_exists(self) -> None:
        """A ledger row's Lean evidence must be a theorem of this package,
        and its Python evidence a test that exists."""
        rows = census()
        text = LEDGER.read_text(encoding="utf-8")
        cited = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_']*)`", text))
        lean_cited = cited & set(rows)
        self.assertGreater(len(lean_cited), 15)
        for name in re.findall(r"`(test_[a-z0-9_]+)`", text):
            found = any(
                name in (HERE / module).read_text(encoding="utf-8")
                for module in TEST_FILES
            )
            self.assertTrue(found, name)


if __name__ == "__main__":
    unittest.main()
