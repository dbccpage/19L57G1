"""The census of the Lean package, and the frozen prediction it is scored
against.

A hand copy of `research/second_profile/test_census.py`, with this
rung's modules, counts and ledger rows, and with this rung's
statement-shape checks in place of rung nine's.

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

LEAN = HERE / "lean" / "SecondResponse"
CENSUS = HERE / "FWDEF_CENSUS.json"
LOG = HERE / "receipts" / "lean_axioms.txt"
PREDICTIONS = HERE / "PREDICTIONS.md"
LEDGER = HERE / "CLAIM_LEDGER.md"

MODULES = (
    "Kernel.lean",
    "IsoKernel.lean",
    "Carry.lean",
    "Exhaust.lean",
    "ExhaustStep.lean",
    "Move.lean",
)
RECONSTRUCTED = ("Kernel.lean", "IsoKernel.lean")
NATIVE = ("Carry.lean", "Exhaust.lean", "ExhaustStep.lean", "Move.lean")
TEST_FILES = (
    "test_census.py",
    "test_forbidden.py",
    "test_pins.py",
    "test_reconstruction.py",
    "test_response.py",
)
# A DEFINITION row may not carry a proof longer than this many lines.  The
# bound is on the class, not on the file: a long proof classed DEFINITION
# is the shape that hides content.
DEFINITION_PROOF_LINES = 12

# The scoring of the frozen FW-DEF prediction, computed by this file and
# dated in STATUS.md (2026-09-25).
PREDICTED_NAMES = 39
PREDICTED_CLASS_HITS = 37
PREDICTED_CLASS_MISSES = 2
UNPREDICTED_NATIVE = 0
UNPREDICTED: tuple[str, ...] = ()
# The two misses, each (predicted, recorded), dated in STATUS.md.  Both
# are demotions from THIN to DEFINITION.
MISSES: dict[str, tuple[str, str]] = {
    "holdsTwo_iff_distinguishes": ("THIN", "DEFINITION"),
    "mem_plug_of_hole": ("THIN", "DEFINITION"),
}

# The statements credited to earlier rungs, proved again here.
CREDITED = (
    "map_inv",
    "plug_mapCtx",
    "plug_args_lt",
    "wfCtx_mapCtx",
    "derivable_fwd",
    "derivable_bwd",
    "derivable_mapCtx",
    "separable_step_keep",
    "getD_append_lt",
    "step_wf",
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
    """The statement of a theorem, from its name to its `:=` or to its
    first equation, comments stripped and whitespace collapsed."""
    text = lean_audit.declaration_text((LEAN / module).read_text(encoding="utf-8"))
    stated = text.split(f"theorem {name} ")[1].split(":=")[0].split("\n  |")[0]
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
        and is never counted as this rung's content."""
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
        """The counts STATUS.md dates.  A reclassification changes this
        line too, which is the point of writing the number down."""
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["counts"],
            {"CONTENT": 8, "DEFINITION": 8, "RECONSTRUCTION": 17, "THIN": 23},
        )

    def test_no_definition_row_hides_a_long_proof(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        self.assertEqual(payload["long_but_definitional"], {})
        lengths = proof_lengths()
        for name, row in payload["classes"].items():
            if row["class"] == "DEFINITION":
                self.assertLessEqual(lengths[name], DEFINITION_PROOF_LINES, name)

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
        self.assertIn("No native theorem was added beyond the frozen prediction", note)


class StatementShapeTests(unittest.TestCase):
    """The frozen Lean-side predictions whose evidence is the statement
    text: what each theorem assumes, and what it does not."""

    def test_r1_exhaustion_is_carried_with_an_admitted_form_only(self) -> None:
        self.assertEqual(
            signature("Exhaust.lean", "exhausted_iso"),
            "{r s : Regime} (σ : Iso r s) {f : Nat} (hf : f < r.forms.length) : "
            "Exhausted r f ↔ Exhausted s (σ.fmap f)",
        )
        self.assertNotIn(".wf", signature("Carry.lean", "derivable_mapCtx"))
        self.assertNotIn(".wf", signature("Carry.lean", "wfCtx_mapCtx"))

    def test_r2_exhaustion_and_holding_two_need_no_hypothesis(self) -> None:
        self.assertEqual(
            signature("Exhaust.lean", "exhausted_iff_not_distinguishes"),
            "(r : Regime) (f : Nat) : Exhausted r f ↔ ¬ Distinguishes r f",
        )
        self.assertEqual(
            signature("Exhaust.lean", "holdsTwo_iff_distinguishes"),
            "(r : Regime) : HoldsTwo r ↔ ∃ f, Distinguishes r f",
        )
        self.assertEqual(signature("Exhaust.lean", "exhausted_of_rule"),
                         "{r : Regime} {f : Nat} (h : f ∈ r.rules) : Exhausted r f")
        self.assertEqual(
            signature("Exhaust.lean", "exhausted_of_no_inst"),
            "{r : Regime} {f : Nat} (h : ∀ p ∈ r.insts, p.1 ≠ f) : Exhausted r f",
        )
        self.assertEqual(signature("Exhaust.lean", "exhausted_of_le_one"),
                         "{r : Regime} (h : r.data ≤ 1) (f : Nat) : Exhausted r f")
        self.assertIn("(hwf : r.wf)", signature("ExhaustStep.lean", "fresh_form_exhausted"))

    def test_r3_the_keeping_kinds_and_the_four_exhibits(self) -> None:
        stated = signature("ExhaustStep.lean", "exhausted_step_keep")
        self.assertIn("(hd : e ≠ .admitDatum) (hi : ∀ g args, e ≠ .admitInst g args)", stated)
        self.assertNotIn(".wf", stated)
        stated = signature("ExhaustStep.lean", "distinguishes_step_keep")
        self.assertIn(
            "(hi : ∀ g args, e ≠ .admitInst g args) (hr : ∀ g, e ≠ .admitRuleAll g)", stated
        )
        self.assertNotIn(".wf", stated)
        for name, event, before, after in (
            ("exhaustion_begun_by_inst", ".admitInst 0 [1]", "Distinguishes r 0",
             "Exhausted r' 0"),
            ("exhaustion_begun_by_rule", ".admitRuleAll 0", "Distinguishes r 0",
             "Exhausted r' 0"),
            ("exhaustion_ended_by_datum", ".admitDatum", "Exhausted r 0",
             "Distinguishes r' 0"),
            ("exhaustion_ended_by_inst", ".admitInst 0 [0]", "Exhausted r 0",
             "Distinguishes r' 0"),
        ):
            stated = signature("ExhaustStep.lean", name)
            self.assertIn(f"r.wf ∧ {before} ∧", stated, name)
            self.assertIn(event, stated, name)
            self.assertIn(f"= some r' ∧ {after}", stated, name)

    def test_r4_the_first_stage_of_exhaustion(self) -> None:
        self.assertEqual(signature("Exhaust.lean", "no_exhausted_at_genesis"),
                         ": ¬ HasExhausted genesis")
        self.assertIn("replayE [.admitForm 1] genesis = some r ∧ HasExhausted r",
                      signature("Exhaust.lean", "exhaustion_at_one"))

    def test_r5_which_kinds_keep_a_pair_and_what_each_needs(self) -> None:
        stated = signature("Move.lean", "collapsed_step_keep")
        self.assertIn("(hwf : r.wf) (hi : ∀ f args, e ≠ .admitInst f args)", stated)
        self.assertIn("(hc : collapsed r d d') : collapsed r' d d'", stated)
        self.assertIn("hwf", body("Move.lean", "collapsed_step_keep").split(":=", 1)[1])
        self.assertNotIn(".wf", signature("ExhaustStep.lean", "separable_step_keep"))
        for name in ("separable_inst_unmentioned", "collapsed_inst_unmentioned"):
            stated = signature("Move.lean", name)
            self.assertIn("(hd : d ∉ args) (hd' : d' ∉ args)", stated, name)
            self.assertNotIn(".wf", stated, name)
        self.assertIn("(hwf : r.wf) (h : stepE r e = some r') : r'.wf",
                      signature("Move.lean", "step_wf"))

    def test_r6_a_moved_pair_is_mentioned(self) -> None:
        stated = signature("Move.lean", "separation_needs_mention")
        self.assertIn(
            "r.wf → replayE h r = some r' → collapsed r d d' → separable r' d d' →", stated
        )
        self.assertIn("∃ f args, Event.admitInst f args ∈ h ∧ (d ∈ args ∨ d' ∈ args)", stated)
        stated = signature("Move.lean", "collapse_needs_mention_or_rule")
        self.assertNotIn(".wf", stated)
        self.assertIn("∃ g, Event.admitRuleAll g ∈ h", stated)
        self.assertIn("(hr : ∀ g, Event.admitRuleAll g ∉ h)",
                      signature("Move.lean", "moved_pairs_meet_mentions"))
        self.assertIn(": ∃ f args, Event.admitInst f args ∈ h",
                      signature("Move.lean", "separation_needs_inst"))

    def test_r7_the_two_moving_exhibits(self) -> None:
        self.assertIn(
            "collapsed r 0 1 ∧ collapsed r 0 2 ∧ stepE r (.admitInst 0 [0]) = some r' ∧ "
            "separable r' 0 1 ∧ separable r' 0 2",
            signature("Move.lean", "one_inst_moves_two_pairs"),
        )
        self.assertIn(
            "collapsed r 0 1 ∧ separable r 0 2 ∧ stepE r (.admitInst 0 [0]) = some r' ∧ "
            "separable r' 0 1 ∧ collapsed r' 0 2",
            signature("Move.lean", "response_collapses_a_pair"),
        )

    def test_r8_every_omega_stands_alone_on_one_arithmetic_goal(self) -> None:
        """Rung nine found `omega` reaching `Classical.choice` on a
        conjunction or a non-arithmetic goal.  Every `omega` of this
        package sits inside `exact absurd h (by omega)`; this reads the
        text for that shape.  The proof of the whitelist is
        `verify_lean.py` on a fresh build."""
        seen = 0
        for module in NATIVE:
            text = lean_audit.declaration_text((LEAN / module).read_text(encoding="utf-8"))
            for line in text.split("\n"):
                if "omega" in line:
                    seen += 1
                    self.assertIn("exact absurd", line, module)
                    self.assertIn("(by omega)", line, module)
        self.assertGreater(seen, 0)

    def test_the_credited_statements_say_whose_they_are(self) -> None:
        step = (LEAN / "ExhaustStep.lean").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("`getD_append_lt` repeats, as a statement, rung five's", step)
        self.assertIn("`separable_step_keep`\nrepeats rung nine's statement", step)
        carry = (LEAN / "Carry.lean").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("RESTATED, not native.", carry)
        move = (LEAN / "Move.lean").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("(rung\n  three's `wf_step_any`, restated", move)
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

    def test_some_theorem_depends_on_no_axiom_at_all(self) -> None:
        self.assertIn(":: none", LOG.read_text(encoding="utf-8"))

    def test_the_dated_axiom_tally(self) -> None:
        """Dated 2026-09-25 in STATUS.md and CLAIM_LEDGER.md."""
        tally: dict[str, int] = {}
        for line in LOG.read_text(encoding="utf-8").splitlines():
            if line.strip():
                key = line.split(" :: ")[1]
                tally[key] = tally.get(key, 0) + 1
        self.assertEqual(tally, {"none": 3, "propext": 27, "Quot.sound propext": 26})


class LedgerTests(unittest.TestCase):
    """Predictions R-21 and R-22: the four remaining rows are decided here;
    each says FORCED is conditional on an engine that does not exist yet,
    and none claims a Lean statement about a minimum response."""

    ROWS = ["adjacency", "reach", "branching", "exhaustion"]

    def test_the_ledger_touches_exactly_four_census_rows(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        rows = re.findall(r"^\| CENSUS-([a-z]+) \|", text, re.M)
        self.assertEqual(rows, self.ROWS)

    def test_every_census_row_carries_the_engine_condition(self) -> None:
        for name in self.ROWS:
            self.assertIn("conditional on an engine", ledger_row(f"| CENSUS-{name}"), name)

    def test_the_exhaustion_row_is_definable_on_its_evidence(self) -> None:
        row = ledger_row("| CENSUS-exhaustion")
        for name in ("exhausted_iso", "exhausted_iff_not_distinguishes",
                     "holdsTwo_iff_distinguishes", "no_exhausted_at_genesis",
                     "exhaustion_at_one", "exhausted_step_keep", "distinguishes_step_keep",
                     "exhaustion_begun_by_inst", "exhaustion_begun_by_rule",
                     "exhaustion_ended_by_datum", "exhaustion_ended_by_inst"):
            self.assertIn(name, row, name)
        self.assertIn("DEFINABLE", row)

    def test_the_response_rows_are_useful_realizations(self) -> None:
        for name in ("adjacency", "reach", "branching"):
            row = ledger_row(f"| CENSUS-{name}")
            self.assertIn("USEFUL REALIZATION", row, name)
            self.assertNotIn("DEFINABLE", row, name)
            self.assertIn("sealed responder", row, name)
            self.assertIn("priced", row, name)
            self.assertIn("FINITE COMPUTATION", row, name)
        for name in ("adjacency", "reach"):
            row = ledger_row(f"| CENSUS-{name}")
            for theorem in ("separation_needs_mention", "collapse_needs_mention_or_rule"):
                self.assertIn(theorem, row, name)
        self.assertIn("no further declaration", ledger_row("| CENSUS-adjacency"))
        self.assertIn("no Lean statement", ledger_row("| CENSUS-branching"))

    def test_every_ledger_row_names_evidence_that_exists(self) -> None:
        """A ledger row's Lean evidence must be a theorem of this package,
        and its Python evidence a test that exists."""
        rows = census()
        text = LEDGER.read_text(encoding="utf-8")
        cited = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_']*)`", text))
        self.assertGreater(len(cited & set(rows)), 25)
        for name in re.findall(r"`(test_[a-z0-9_]+)`", text):
            found = any(
                name in (HERE / module).read_text(encoding="utf-8")
                for module in TEST_FILES
            )
            self.assertTrue(found, name)


if __name__ == "__main__":
    unittest.main()
