"""The census of the Lean package, and the frozen prediction it is scored
against.

A hand copy of `research/second_class/test_census.py`, with this
rung's modules, counts and ledger rows, and with this rung's
statement-shape checks in place of rung eight's.

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

LEAN = HERE / "lean" / "SecondProfile"
CENSUS = HERE / "FWDEF_CENSUS.json"
LOG = HERE / "receipts" / "lean_axioms.txt"
PREDICTIONS = HERE / "PREDICTIONS.md"
LEDGER = HERE / "CLAIM_LEDGER.md"

MODULES = (
    "Kernel.lean",
    "IsoKernel.lean",
    "Carry.lean",
    "Classes.lean",
    "Stage.lean",
    "Keep.lean",
)
RECONSTRUCTED = ("Kernel.lean", "IsoKernel.lean")
NATIVE = ("Carry.lean", "Classes.lean", "Stage.lean", "Keep.lean")
TEST_FILES = (
    "test_census.py",
    "test_forbidden.py",
    "test_pins.py",
    "test_reconstruction.py",
    "test_profile.py",
)
# A DEFINITION row may not carry a proof longer than this many lines.  The
# bound is on the class, not on the file: a long proof classed DEFINITION
# is the shape that hides content, which is why the exception list is
# separate and countable.
DEFINITION_PROOF_LINES = 12

# The scoring of the frozen FW-DEF prediction, computed by this file and
# dated in STATUS.md (2026-09-25).
PREDICTED_NAMES = 33
PREDICTED_CLASS_HITS = 29
PREDICTED_CLASS_MISSES = 4
UNPREDICTED_NATIVE = 0
UNPREDICTED: tuple[str, ...] = ()
# The four misses, each (predicted, recorded), dated in STATUS.md.  All
# four are demotions of an assembly of neighbours from CONTENT to THIN.
MISSES: dict[str, tuple[str, str]] = {
    "derivable_mapCtx": ("CONTENT", "THIN"),
    "collapsed_iso": ("CONTENT", "THIN"),
    "reps_iso": ("CONTENT", "THIN"),
    "replay_parts_le": ("CONTENT", "THIN"),
}

# The statement credited to an earlier rung, proved again here.
CREDITED = ("getD_append_lt",)


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
        """`IsoKernel.lean` reproduces definitions and a structure only;
        so every RECONSTRUCTION row comes from `Kernel.lean`."""
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
            {"CONTENT": 2, "DEFINITION": 10, "RECONSTRUCTION": 17, "THIN": 21},
        )

    def test_no_definition_row_hides_a_long_proof(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        exceptions = payload["long_but_definitional"]
        lengths = proof_lengths()
        for name, row in payload["classes"].items():
            if row["class"] != "DEFINITION" or name in exceptions:
                continue
            self.assertLessEqual(lengths[name], DEFINITION_PROOF_LINES, name)
        self.assertEqual(sorted(exceptions), ["two_classes_at_four"])
        for name in exceptions:
            self.assertEqual(payload["classes"][name]["class"], "DEFINITION")
            self.assertGreater(lengths[name], DEFINITION_PROOF_LINES, name)

    def test_the_long_definition_is_case_exhaustion(self) -> None:
        """The one exception closes a concrete regime by kernel computation
        and a split of the datum; it calls no lemma of this package but
        `collapsed_refl`, and inducts on nothing."""
        text = body("Stage.lean", "two_classes_at_four")
        self.assertIn("rcases", text)
        self.assertIn("decide", text)
        self.assertNotIn("induction", text)
        for name in census():
            if name not in ("two_classes_at_four", "collapsed_refl"):
                self.assertNotIn(name, text, name)

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
        """Every miss is the dated one, with its direction.  A later
        reclassification of any row fails here by name rather than passing
        as a new hit or a new miss."""
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

    def test_q1_observation_is_carried_with_admitted_data_only(self) -> None:
        self.assertEqual(
            signature("Carry.lean", "separable_iso"),
            "{r s : Regime} (σ : Iso r s) {d d' : Nat} (hd : d < r.data) "
            "(hd' : d' < r.data) (h : separable r d d') : "
            "separable s (σ.dmap d) (σ.dmap d')",
        )
        self.assertEqual(
            signature("Carry.lean", "collapsed_iso"),
            "{r s : Regime} (σ : Iso r s) {d d' : Nat} (hd : d < r.data) "
            "(hd' : d' < r.data) (h : collapsed r d d') : "
            "collapsed s (σ.dmap d) (σ.dmap d')",
        )
        for name in ("separable_iso", "collapsed_iso", "derivable_mapCtx", "wfCtx_mapCtx"):
            stated = signature("Carry.lean", name)
            self.assertNotIn(".wf", stated, name)
            self.assertNotIn("Nodup", stated, name)
            self.assertNotIn("Clean", stated, name)

    def test_q2_holding_two_and_representatives_need_no_hypothesis(self) -> None:
        self.assertEqual(signature("Classes.lean", "holdsTwo_iso"),
                         "{r s : Regime} (σ : Iso r s) : HoldsTwo r ↔ HoldsTwo s")
        self.assertEqual(
            signature("Classes.lean", "reps_iso"),
            "{r s : Regime} (σ : Iso r s) {l : List Nat} (h : Reps r l) : "
            "Reps s (l.map σ.dmap) ∧ (l.map σ.dmap).length = l.length",
        )

    def test_q3_collapse_is_reflexive_symmetric_and_transitive(self) -> None:
        rows = census()
        for name in ("collapsed_refl", "collapsed_symm", "collapsed_trans"):
            self.assertEqual(rows[name]["class"], "DEFINITION", name)
        self.assertIn(": collapsed r d d", signature("Classes.lean", "collapsed_refl"))
        self.assertIn(": collapsed r d' d", signature("Classes.lean", "collapsed_symm"))
        self.assertIn(": collapsed r d d''", signature("Classes.lean", "collapsed_trans"))

    def test_q4_the_bounds_and_their_witnesses(self) -> None:
        self.assertEqual(
            signature("Stage.lean", "holdsTwo_parts"),
            "{r : Regime} (h : HoldsTwo r) : "
            "2 ≤ r.data ∧ 1 ≤ r.forms.length ∧ 1 ≤ r.insts.length",
        )
        self.assertIn("parts r ≤ parts b + h.length",
                      signature("Stage.lean", "replay_parts_le"))
        for name, base, bound in (("twoness_needs_four", "genesis", "4"),
                                  ("twoness_needs_two_L", "R2L", "2"),
                                  ("twoness_needs_two_F", "R2F", "2")):
            stated = signature("Stage.lean", name)
            self.assertIn(f"(hr : replayE h {base} = some r) (ht : HoldsTwo r)", stated, name)
            self.assertIn(f": {bound} ≤ h.length", stated, name)
        self.assertIn("[.admitDatum, .admitDatum, .admitForm 1, .admitInst 0 [0]]",
                      signature("Stage.lean", "twoness_at_four"))
        for name, base in (("twoness_at_two_L", "R2L"), ("twoness_at_two_F", "R2F")):
            self.assertIn(f"[.admitForm 1, .admitInst 0 [0]] {base}",
                          signature("Stage.lean", name), name)
        for name in ("twoness_at_four", "twoness_at_two_L", "twoness_at_two_F",
                     "two_classes_at_four"):
            self.assertIn("decide", body("Stage.lean", name), name)
            self.assertEqual(census()[name]["class"], "DEFINITION", name)

    def test_q5_four_kinds_keep_separability_with_no_hypothesis(self) -> None:
        stated = signature("Keep.lean", "separable_step_keep")
        self.assertIn("(hi : ∀ f args, e ≠ .admitInst f args) (hr : ∀ f, e ≠ .admitRuleAll f)",
                      stated)
        self.assertIn("(h : stepE r e = some r') (hs : separable r d d') : separable r' d d'",
                      stated)
        for name in ("separable_step_keep", "holdsTwo_step_keep"):
            self.assertNotIn(".wf", signature("Keep.lean", name), name)

    def test_q6_two_kinds_can_end_it(self) -> None:
        for name, event in (("twoness_lost_by_inst", ".admitInst 0 [1]"),
                            ("twoness_lost_by_rule", ".admitRuleAll 0")):
            self.assertIn(
                f"r.wf ∧ HoldsTwo r ∧ stepE r ({event}) = some r' ∧ ¬ HoldsTwo r'",
                signature("Keep.lean", name), name,
            )

    def test_q7_no_omega_closes_a_conjunction_or_a_non_arithmetic_goal(self) -> None:
        """The first build found `omega`, closing a goal that is a
        conjunction or not arithmetic at all, reaching `Classical.choice`.
        Every `omega` of the package now stands alone on an arithmetic goal
        or inside `by omega` for one conjunct; this reads the text for the
        two shapes that were repaired."""
        for module in NATIVE:
            text = lean_audit.declaration_text((LEAN / module).read_text(encoding="utf-8"))
            self.assertNotIn("simp only [parts]\n    omega", text, module)
            self.assertNotIn("simp only [parts]\n      omega", text, module)
            self.assertNotIn("hd\n      omega", text, module)
            self.assertNotIn("hx\n        omega", text, module)

    def test_the_credited_statements_say_whose_they_are(self) -> None:
        keep = (LEAN / "Keep.lean").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("`getD_append_lt` repeats, as a statement, rung five's", keep)
        carry = (LEAN / "Carry.lean").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("`isoSymm` repeats rung eight's definition", carry)
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
            axioms = line.split(" :: ")[1].split()
            for axiom in axioms:
                self.assertIn(axiom, {"none", "propext", "Quot.sound"})

    def test_the_log_is_stored_with_no_carriage_return(self) -> None:
        self.assertNotIn(b"\r", LOG.read_bytes())

    def test_some_theorem_depends_on_no_axiom_at_all(self) -> None:
        """Not a vacuous whitelist: the log distinguishes a report with no
        axioms from a report within the whitelist."""
        self.assertIn(":: none", LOG.read_text(encoding="utf-8"))

    def test_the_dated_axiom_tally(self) -> None:
        """Dated 2026-09-25 in STATUS.md and CLAIM_LEDGER.md."""
        tally: dict[str, int] = {}
        for line in LOG.read_text(encoding="utf-8").splitlines():
            if line.strip():
                key = line.split(" :: ")[1]
                tally[key] = tally.get(key, 0) + 1
        self.assertEqual(tally, {"none": 3, "propext": 20, "Quot.sound propext": 27})


class LedgerTests(unittest.TestCase):
    """Predictions Q-15 and Q-16: the two-ness and observational-classes
    rows are decided here; each says FORCED is conditional on an engine
    that does not exist yet, and neither claims a Lean count."""

    ROWS = ["twoness", "classes"]

    def test_the_ledger_touches_exactly_two_census_rows(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        rows = re.findall(r"^\| CENSUS-([a-z]+) \|", text, re.M)
        self.assertEqual(rows, self.ROWS)

    def test_every_census_row_carries_the_engine_condition(self) -> None:
        for name in self.ROWS:
            self.assertIn("conditional on an engine", ledger_row(f"| CENSUS-{name}"), name)

    def test_the_twoness_row_names_its_evidence(self) -> None:
        row = ledger_row("| CENSUS-twoness")
        for name in ("holdsTwo_iso", "separable_iso", "holdsTwo_parts", "twoness_needs_four",
                     "twoness_needs_two_L", "twoness_needs_two_F", "twoness_at_four",
                     "separable_step_keep", "twoness_lost_by_inst", "twoness_lost_by_rule"):
            self.assertIn(name, row, name)
        self.assertIn("DEFINABLE", row)

    def test_the_classes_row_claims_no_lean_count(self) -> None:
        row = ledger_row("| CENSUS-classes")
        for name in ("collapsed_refl", "collapsed_symm", "collapsed_trans", "collapsed_iso",
                     "reps_iso"):
            self.assertIn(name, row, name)
        self.assertIn("OPEN", row)
        self.assertIn("X-1", row)
        self.assertIn("DEFINABLE", row)

    def test_every_ledger_row_names_evidence_that_exists(self) -> None:
        """A ledger row's Lean evidence must be a theorem of this package,
        and its Python evidence a test that exists."""
        rows = census()
        text = LEDGER.read_text(encoding="utf-8")
        cited = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_']*)`", text))
        lean_cited = cited & set(rows)
        self.assertGreater(len(lean_cited), 25)
        for name in re.findall(r"`(test_[a-z0-9_]+)`", text):
            found = any(
                name in (HERE / module).read_text(encoding="utf-8")
                for module in TEST_FILES
            )
            self.assertTrue(found, name)


if __name__ == "__main__":
    unittest.main()
