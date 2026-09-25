"""The census of the Lean package, and the frozen prediction it is scored
against.

A hand copy of `research/second_index/test_census.py`, with this rung's
modules, counts and ledger rows, and with this rung's statement-shape
checks in place of rung three's.

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

LEAN = HERE / "lean" / "SecondIso"
CENSUS = HERE / "FWDEF_CENSUS.json"
LOG = HERE / "receipts" / "lean_axioms.txt"
PREDICTIONS = HERE / "PREDICTIONS.md"
LEDGER = HERE / "CLAIM_LEDGER.md"

MODULES = (
    "Kernel.lean",
    "IsoKernel.lean",
    "Inherited.lean",
    "IndexSlice.lean",
    "Transport.lean",
    "Trajectory.lean",
    "Check.lean",
    "Countermodel.lean",
)
RECONSTRUCTED = ("Kernel.lean", "IsoKernel.lean", "Inherited.lean", "IndexSlice.lean")
TEST_FILES = (
    "test_census.py",
    "test_forbidden.py",
    "test_iso_index.py",
    "test_pins.py",
    "test_reconstruction.py",
)
# A DEFINITION row may not carry a proof longer than this many lines.  The
# bound is on the class, not on the file: a long proof classed DEFINITION
# is the shape that hides content, which is why the exception list is
# separate and countable.
DEFINITION_PROOF_LINES = 12

# The scoring of the frozen FW-DEF prediction, computed by this file and
# dated in STATUS.md (2026-09-24).
PREDICTED_NAMES = 38
PREDICTED_CLASS_HITS = 31
PREDICTED_CLASS_MISSES = 7
UNPREDICTED_NATIVE = 11


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
        """A theorem reproduced under a pin is the sealed estate's or a
        sibling's result and is never counted as this rung's content."""
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
            {"CONTENT": 4, "DEFINITION": 15, "RECONSTRUCTION": 35, "THIN": 30},
        )

    def test_no_definition_row_hides_a_long_proof(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        exceptions = payload["long_but_definitional"]
        lengths = proof_lengths()
        for name, row in payload["classes"].items():
            if row["class"] != "DEFINITION" or name in exceptions:
                continue
            self.assertLessEqual(lengths[name], DEFINITION_PROOF_LINES, name)
        self.assertEqual(sorted(exceptions), ["iso_index"])
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
                "demandCheck_sound",
                "first_demand_matched_of_uniform",
                "honourCheck_sound",
                "matched_P",
                "matched_Q",
                "noDemandCheck_sound",
                "separable_of_unary_witness",
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
        """All seven misses moved a target DOWN the order CONTENT, THIN,
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

    def test_j1_separability_transports_with_no_decision(self) -> None:
        for name in ("separable_fwd", "separable_transport"):
            stated = signature("Transport.lean", name)
            self.assertNotIn("Decidable", stated, name)
            self.assertIn("(h : Iso r s)", stated, name)

    def test_j2_invariance_assumes_only_uniformity_and_the_isomorphism(self) -> None:
        stated = signature("Transport.lean", "hasDemand_iff_of_uniform")
        self.assertIn("(hu : Uniform S)", stated)
        self.assertIn("(h : Iso r s)", stated)
        self.assertIn("HasDemand S r ↔ HasDemand S s", stated)
        self.assertNotIn("Decidable", stated)
        self.assertNotIn(".wf", stated)

    def test_j4_no_theorem_derives_uniformity(self) -> None:
        """Necessity is NOT proved: no theorem of the package concludes
        that a stake is uniform, or is not, from invariance.  The only
        conclusions about uniformity are the three constant stakes' and
        the three refutations by exhibited label pairs."""
        concluding: list[str] = []
        for module in MODULES:
            text = lean_audit.declaration_text(
                (LEAN / module).read_text(encoding="utf-8")
            )
            for match in re.finditer(r"theorem (\w+)[^:]*?:\s*(?:¬\s*)?Uniform", text):
                concluding.append(match.group(1))
        self.assertEqual(
            sorted(concluding),
            [
                "chain_not_uniform",
                "parity_not_uniform",
                "residue_not_uniform",
                "uniform_allApart",
                "uniform_allSame",
                "uniform_freeStake",
            ],
        )

    def test_j5_the_regime_pairs_use_forms_of_arity_one(self) -> None:
        text = (LEAN / "Countermodel.lean").read_text(encoding="utf-8")
        found = {
            name: (int(data), forms)
            for name, data, forms in re.findall(
                r"def (pr\d|rr\d) : Regime := ⟨(\d+), \[([\d, ]*)\]", text
            )
        }
        self.assertEqual(sorted(found), ["pr0", "pr1", "rr0", "rr1"])
        for name, (data, forms) in found.items():
            self.assertEqual({f.strip() for f in forms.split(",")}, {"1"}, name)
            self.assertEqual(data, 3 if name.startswith("pr") else 4, name)

    def test_j6_matching_needs_no_decision_and_no_base_hypothesis(self) -> None:
        stated = signature("Trajectory.lean", "first_demand_matched_of_uniform")
        self.assertIn("(hu : Uniform S)", stated)
        self.assertIn("(hm : Matched base h base' h')", stated)
        self.assertNotIn("Decidable", stated)
        self.assertNotIn(".wf", stated)

    def test_j7_the_exhibited_first_counts(self) -> None:
        text = " ".join(
            lean_audit.declaration_text(
                (LEAN / "Countermodel.lean").read_text(encoding="utf-8")
            ).split()
        )
        for stated in (
            "theorem index_P2_parity : IsFirstDemand parity genesis P2 8",
            "theorem index_P2_chain : IsFirstDemand chain genesis P2 8",
            "theorem index_Q2_residue : IsFirstDemand residueThree genesis Q2 11",
            "theorem quiet_P1_parity : ∀ k, ¬ IsFirstDemand parity genesis P1 k",
            "theorem quiet_P1_chain : ∀ k, ¬ IsFirstDemand chain genesis P1 k",
            "theorem quiet_Q1_residue : ∀ k, ¬ IsFirstDemand residueThree genesis Q1 k",
            "theorem matched_P : Matched genesis P1 genesis P2",
            "theorem matched_Q : Matched genesis Q1 genesis Q2",
        ):
            self.assertIn(stated, text)
        receipt = json.loads(
            (HERE / "receipts" / "iso_index.json").read_text(encoding="utf-8")
        )
        exhibited = receipt["reports"]["exhibited"]
        self.assertEqual(exhibited["P"]["first_counts"]["parity"], {"P1": None, "P2": 8})
        self.assertEqual(exhibited["P"]["first_counts"]["chain"], {"P1": None, "P2": 8})
        self.assertEqual(
            exhibited["Q"]["first_counts"]["residue_three"], {"Q1": None, "Q2": 11}
        )

    def test_j9_the_supply_renaming_is_an_induction_and_no_more(self) -> None:
        rows = census()
        self.assertEqual(rows["first_demand_renameSupply"]["class"], "THIN")
        self.assertEqual(rows["stepE_renameSupply"]["class"], "DEFINITION")
        self.assertEqual(rows["replayE_renameSupply"]["class"], "THIN")

    def test_no_decision_procedure_for_separability_is_declared(self) -> None:
        """The sound checks are Boolean definitions that IMPLY the
        propositions they name, and are not instances deciding them: no
        instance of this package mentions separability, collapse or a
        demand."""
        for module in MODULES:
            text = lean_audit.declaration_text(
                (LEAN / module).read_text(encoding="utf-8")
            )
            for line in text.split("\n"):
                if re.match(r"^\s*instance\b", line):
                    self.assertNotIn("separable", line)
                    self.assertNotIn("collapsed", line)
                    self.assertNotIn("Demand", line)


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
    """Prediction J-21: exactly two rows of the challenge-five census are
    decided here, succession a second time and symmetry.  Prediction J-8:
    the lengths between the rectangle's bound and the exhibited witnesses
    are recorded OPEN."""

    def test_the_ledger_decides_exactly_two_census_rows(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        rows = re.findall(r"^\| CENSUS-([a-z]+) \|", text, re.M)
        self.assertEqual(rows, ["succession", "symmetry"])

    def test_the_succession_row_names_both_directions(self) -> None:
        row = ledger_row("| CENSUS-succession")
        self.assertIn("first_demand_matched_of_uniform", row)
        self.assertIn("first_count_not_trajectory_invariant", row)

    def test_the_symmetry_row_is_decided_as_definable(self) -> None:
        row = ledger_row("| CENSUS-symmetry")
        self.assertIn("DEFINABLE", row)
        self.assertIn("automorphisms", row)

    def test_the_shorter_witness_lengths_are_open(self) -> None:
        row = ledger_row("| ISO-SHORTEST")
        self.assertIn("OPEN", row)
        self.assertIn("five to seven", row)
        self.assertIn("five to ten", row)

    def test_necessity_of_uniformity_is_open(self) -> None:
        self.assertIn("OPEN", ledger_row("| ISO-NECESSITY"))

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
