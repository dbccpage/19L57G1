"""The census of the Lean package, and the frozen prediction it is scored
against.

A hand copy of the shape of `research/second_response/test_census.py`,
with this tree's modules, counts, statement-shape checks and ledger rows.

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
  the whitelist, and the ledger rows the frozen predictions C-20 and C-21
  name say what those predictions say.

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

LEAN = HERE / "lean" / "SecondEngine"
CENSUS = HERE / "FWDEF_CENSUS.json"
LOG = HERE / "receipts" / "lean_axioms.txt"
PREDICTIONS = HERE / "PREDICTIONS.md"
LEDGER = HERE / "CLAIM_LEDGER.md"

MODULES = (
    "Kernel.lean",
    "IsoKernel.lean",
    "Carry.lean",
    "Orbit.lean",
    "Stake.lean",
    "Genesis.lean",
    "Engine.lean",
    "Census.lean",
)
RECONSTRUCTED = ("Kernel.lean", "IsoKernel.lean")
NATIVE = ("Orbit.lean", "Stake.lean", "Genesis.lean", "Engine.lean", "Census.lean")
TEST_FILES = (
    "test_census.py",
    "test_engine.py",
    "test_forbidden.py",
    "test_pins.py",
    "test_reconstruction.py",
)
# A DEFINITION row may not carry a proof longer than this many lines.  The
# bound is on the class, not on the file: a long proof classed DEFINITION
# is the shape that hides content.
DEFINITION_PROOF_LINES = 12
LONG_BUT_DEFINITIONAL = ("e8_quiet_without_reqs",)

# The scoring of the frozen FW-DEF prediction, computed by this file and
# dated in STATUS.md (2026-09-25).
PREDICTED_NAMES = 50
PREDICTED_CLASS_HITS = 48
PREDICTED_CLASS_MISSES = 2
UNPREDICTED_NATIVE = 0
UNPREDICTED: tuple[str, ...] = ()
# The two misses, each (predicted, recorded), dated in STATUS.md.
MISSES: dict[str, tuple[str, str]] = {
    "oneOrbit_iso": ("CONTENT", "THIN"),
    "sortPair_swap": ("DEFINITION", "THIN"),
}

# The statements credited to rung nine, restated here.
CREDITED = (
    "map_inv",
    "plug_mapCtx",
    "plug_args_lt",
    "wfCtx_mapCtx",
    "derivable_fwd",
    "derivable_bwd",
    "derivable_mapCtx",
    "separable_iso",
    "collapsed_iso",
)


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
    """Leaf theorem name -> the number of non-blank lines from its
    declaration to the next theorem, comments stripped."""
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
            body_lines = [row for row in lines[line:end] if row.strip()]
            lengths[name] = len(body_lines)
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
    stated = text.split(f"theorem {name} ")[1].split(":=")[0]
    return " ".join(stated.split())


def body(module: str, name: str) -> str:
    """The declaration of a theorem up to the next theorem, comments
    stripped."""
    text = lean_audit.declaration_text((LEAN / module).read_text(encoding="utf-8"))
    return text.split(f"theorem {name} ")[1].split("theorem ")[0]


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
        and is never counted as this tree's content."""
        rows = census()
        for name, row in rows.items():
            if row["module"] in RECONSTRUCTED:
                self.assertEqual(row["class"], "RECONSTRUCTION", name)
            else:
                self.assertNotEqual(row["class"], "RECONSTRUCTION", name)

    def test_the_isomorphism_reconstruction_carries_no_theorem(self) -> None:
        self.assertEqual(
            lean_audit.theorem_names((LEAN / "IsoKernel.lean").read_text(encoding="utf-8")), []
        )

    def test_the_counts_block_matches_the_rows(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        tally: dict[str, int] = {}
        for row in payload["classes"].values():
            tally[row["class"]] = tally.get(row["class"], 0) + 1
        self.assertEqual(payload["counts"], dict(sorted(tally.items())))

    def test_the_content_census_is_the_dated_one(self) -> None:
        """The counts STATUS.md dates.  No row is CONTENT: a reclassification
        changes this line too, which is the point of writing it down."""
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["counts"],
            {"DEFINITION": 22, "RECONSTRUCTION": 17, "THIN": 28},
        )

    def test_no_definition_row_hides_a_long_proof(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        self.assertEqual(sorted(payload["long_but_definitional"]), sorted(LONG_BUT_DEFINITIONAL))
        lengths = proof_lengths()
        for name, row in payload["classes"].items():
            if row["class"] == "DEFINITION" and name not in LONG_BUT_DEFINITIONAL:
                self.assertLessEqual(lengths[name], DEFINITION_PROOF_LINES, name)
        for name in LONG_BUT_DEFINITIONAL:
            self.assertEqual(payload["classes"][name]["class"], "DEFINITION", name)
            self.assertGreater(lengths[name], DEFINITION_PROOF_LINES, name)

    def test_the_length_reader_finds_the_longest_proof(self) -> None:
        """Not a vacuous bound: the package does carry proofs longer than
        the DEFINITION limit, and they are classed otherwise."""
        lengths = proof_lengths()
        rows = census()
        native_long = [
            name
            for name, length in lengths.items()
            if length > DEFINITION_PROOF_LINES
            and rows[name]["module"] in NATIVE
            and rows[name]["class"] != "DEFINITION"
        ]
        self.assertTrue(native_long)


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
        unpredicted = sorted(native - set(self.predicted))
        self.assertEqual(len(unpredicted), UNPREDICTED_NATIVE)
        self.assertEqual(unpredicted, sorted(UNPREDICTED))

    def test_every_miss_is_the_dated_one(self) -> None:
        for name, cls in self.predicted.items():
            actual = self.actual[name]["class"]
            if actual != cls:
                self.assertEqual(MISSES.get(name), (cls, actual), name)
            else:
                self.assertNotIn(name, MISSES, name)

    def test_the_census_note_records_every_miss(self) -> None:
        note = json.loads(CENSUS.read_text(encoding="utf-8"))["note"]
        for name in MISSES:
            self.assertIn(name, note, name)
        self.assertIn("No theorem of this package is CONTENT", note)

    def test_the_reconstructions_are_the_predicted_seventeen(self) -> None:
        text = PREDICTIONS.read_text(encoding="utf-8").replace("\r\n", "\n")
        section = text.split("Predicted RECONSTRUCTION")[1].split("Predicted DEFINITION")[0]
        named = set(re.findall(r"`([A-Za-z0-9_']+)`", section)) - {"Kernel.lean", "IsoKernel.lean"}
        recon = {n for n, row in self.actual.items() if row["class"] == "RECONSTRUCTION"}
        self.assertEqual(named, recon)
        self.assertEqual(len(recon), 17)


class StatementShapeTests(unittest.TestCase):
    """The frozen Lean-side predictions whose evidence is the statement
    text: what each theorem assumes, and what it does not."""

    def test_c1_the_engine_statements(self) -> None:
        self.assertEqual(
            signature("Engine.lean", "fixpoint_of_halt"),
            "(e : Engine S D E) (hc : ∀ s h, ¬ e.Cont s h) {s s' : S} "
            "(hq : Quiet e s) : ¬ Step e s s'",
        )
        self.assertEqual(
            signature("Engine.lean", "step_at_demand_is_response"),
            "(e : Engine S D E) {s s' : S} {d₀ : D} (hd₀ : e.Demand s d₀) "
            "(hst : Step e s s') : ∃ d h, e.Demand s d ∧ e.Resp s d h ∧ e.apply s h = some s'",
        )
        self.assertEqual(
            signature("Engine.lean", "run_named"),
            "(e : Engine S D E) {s s' : S} {hs : List (List E)} "
            "(hr : Run e s s' hs) : ∀ h ∈ hs, ∃ t, Named e t h",
        )
        self.assertIn("(hg : e.Demand = stakeDemand E1) (r : Regime) : Quiet e (r, false)",
                      signature("Engine.lean", "e1_engine_quiet"))
        self.assertIn("¬ Step e (r, false) s'", signature("Engine.lean", "e1_halt_no_step"))

    def test_c2_the_observables_are_carried_with_admission_only(self) -> None:
        for name, predicate in (
            ("oneOrbit_iso", "OneOrbit"),
            ("reqMember_iso", "ReqMember"),
            ("separable_iso_iff", "separable"),
            ("collapsed_iso_iff", "collapsed"),
        ):
            self.assertEqual(
                signature("Orbit.lean", name),
                "{r s : Regime} (σ : Iso r s) {i j : Nat} (hi : i < r.data) (hj : j < r.data) : "
                f"{predicate} r i j ↔ {predicate} s (σ.dmap i) (σ.dmap j)",
                name,
            )

    def test_c3_every_mirrored_reading_is_carried(self) -> None:
        for name, reading in (("e1_carried", "E1"), ("e3_carried", "E3"),
                              ("e4_carried", "E4"), ("e8_carried", "E8")):
            self.assertEqual(signature("Stake.lean", name), f": Carried {reading}", name)
        self.assertEqual(
            signature("Stake.lean", "carried_flip"),
            "{ρ : Reading} (h : Carried ρ) : Carried ρ.flip",
        )
        self.assertEqual(
            signature("Stake.lean", "demand_carried"),
            "{ρ : Reading} (h : Carried ρ) {r s : Regime} (σ : Iso r s) {i j : Nat} "
            "(hi : i < r.data) (hj : j < r.data) : "
            "Demand ρ r i j ↔ Demand ρ s (σ.dmap i) (σ.dmap j)",
        )

    def test_c4_the_quiet_rules_and_the_flips(self) -> None:
        self.assertEqual(signature("Stake.lean", "e1_never_demands"),
                         "(r : Regime) (i j : Nat) : ¬ Demand E1 r i j")
        self.assertIn("(h : collapsed r i j ∨ separable r i j) : Demand E1.flip r i j",
                      signature("Stake.lean", "e1_flip_demands"))
        self.assertEqual(signature("Stake.lean", "e3_flip_eq_e4"), ": E3.flip = E4")
        self.assertEqual(signature("Stake.lean", "e4_flip_eq_e3"), ": E4.flip = E3")
        self.assertIn("rfl", body("Stake.lean", "e3_flip_eq_e4"))
        self.assertIn("(hr : r.reqs = [])", signature("Stake.lean", "e8_quiet_without_reqs"))

    def test_c5_the_genesis_of_reading_l(self) -> None:
        self.assertIn(
            "replayE [.supply 0, .supply 1, .supply 1, .supply 2, .admitDatum, .admitDatum] "
            "genesis = some genL",
            signature("Genesis.lean", "genL_replays"),
        )
        self.assertEqual(signature("Genesis.lean", "minima_differ_at_genL"),
                         ": Demand E4 genL 0 1 ∧ ¬ Demand E1 genL 0 1")
        self.assertEqual(signature("Genesis.lean", "e3_quiet_at_genL"), ": ¬ Demand E3 genL 0 1")
        self.assertEqual(signature("Genesis.lean", "e1_flip_demands_at_genL"),
                         ": Demand E1.flip genL 0 1")

    def test_c6_the_census_values(self) -> None:
        self.assertIn("classList.length = 144", signature("Census.lean", "class_size"))
        self.assertIn("literalList.length = 108", signature("Census.lean", "literal_size"))
        self.assertIn("6 ≤ e.count", signature("Census.lean", "count_ge_six"))
        self.assertIn("e.count == 6).length = 16", signature("Census.lean", "count_six_members"))
        self.assertIn("(h : e.literal = true) : 7 ≤ e.count",
                      signature("Census.lean", "literal_count_ge_seven"))
        self.assertIn("e.count == 7).length = 32",
                      signature("Census.lean", "literal_count_seven_members"))
        self.assertIn("e.count2 == 7).length = 16",
                      signature("Census.lean", "literal_count2_seven_members"))
        self.assertIn("e.count ≠ 1", signature("Census.lean", "no_one_declaration"))
        self.assertIn("¬ ∃ e : Decl, ∀ e' : Decl, ∀ c ∈ e.caps, c ∈ e'.caps",
                      signature("Census.lean", "no_initial"))
        self.assertIn("(hm : e₁.mu2 ≠ e₂.mu2)",
                      signature("Census.lean", "no_initial_of_two_measures"))

    def test_c7_no_tactic_known_to_reach_choice_is_used(self) -> None:
        """Rung nine found `omega` reaching `Classical.choice` on a
        conjunction or a goal that is not arithmetic.  This package uses
        no `omega` at all; the proof of the whitelist is `verify_lean.py`
        on a fresh build."""
        for module in MODULES:
            text = lean_audit.declaration_text((LEAN / module).read_text(encoding="utf-8"))
            self.assertNotIn("omega", text, module)
            self.assertNotIn("Classical", text, module)

    def test_the_credited_statements_say_whose_they_are(self) -> None:
        carry = (LEAN / "Carry.lean").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("RESTATED, not native.", carry)
        self.assertIn("rung nine's, from its\n`SecondProfile/Carry.lean`", carry)
        note = json.loads(CENSUS.read_text(encoding="utf-8"))["note"]
        for name in CREDITED:
            self.assertIn(name, note, name)
        self.assertIn("credited, not counted as new to the run", note)


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
            for axiom in line.split(" :: ")[1].split():
                self.assertIn(axiom, {"none", "propext", "Quot.sound"})

    def test_the_log_is_stored_with_no_carriage_return(self) -> None:
        self.assertNotIn(b"\r", LOG.read_bytes())

    def test_the_dated_axiom_tally(self) -> None:
        """Dated 2026-09-25 in STATUS.md and CLAIM_LEDGER.md."""
        tally: dict[str, int] = {}
        for line in LOG.read_text(encoding="utf-8").splitlines():
            if line.strip():
                key = line.split(" :: ")[1]
                tally[key] = tally.get(key, 0) + 1
        self.assertEqual(tally, {"none": 16, "propext": 32, "Quot.sound propext": 19})


class LedgerTests(unittest.TestCase):
    """Predictions C-20 to C-22 and the evidence the ledger names."""

    def test_the_required_questions_are_answered_with_their_classes(self) -> None:
        exists = ledger_row("| Q4-EXISTS")
        self.assertIn("DEFINITION", exists)
        unique = ledger_row("| Q4-UNIQUE")
        self.assertIn("COUNTERMODEL", unique)
        self.assertIn("minima_differ_at_genL", unique)
        initial = ledger_row("| Q4-INITIAL")
        self.assertIn("PROVED", initial)
        for name in ("no_initial", "no_initial_of_two_measures"):
            self.assertIn(name, initial)
        self.assertIn("inclusions of declarations", initial)
        self.assertIn("refused", initial)
        q10 = ledger_row("| Q10")
        self.assertIn("Q4-EXISTS", q10)

    def test_no_census_row_is_decided_here(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^\| CENSUS-(?!NONE )", text, re.M), [])
        row = ledger_row("| CENSUS-NONE")
        self.assertIn("No row of the challenge-five census", row)
        self.assertIn("second attempt", row)

    def test_the_input_count_is_recorded_not_reduced(self) -> None:
        row = ledger_row("| INPUT-COUNT")
        self.assertIn("RECORDED", row)
        self.assertIn("value two", row)
        self.assertIn("thirty-two", row)
        self.assertIn("G-2", row)

    def test_every_ledger_row_names_evidence_that_exists(self) -> None:
        """A ledger row's Lean evidence must be a theorem of this package,
        and its Python evidence a test that exists."""
        rows = census()
        text = LEDGER.read_text(encoding="utf-8")
        cited = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_'₀-₉]*)`", text))
        self.assertGreater(len(cited & set(rows)), 25)
        for name in re.findall(r"`(test_[a-z0-9_]+)`", text):
            found = any(
                name in (HERE / module).read_text(encoding="utf-8")
                for module in TEST_FILES
            )
            self.assertTrue(found, name)


if __name__ == "__main__":
    unittest.main()
