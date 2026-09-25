"""The census of the Lean package, and the frozen prediction it is scored
against.

A hand copy of `research/second_duration/test_census.py`, with this
rung's modules, counts and ledger rows, and with this rung's
statement-shape checks in place of rung seven's.

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

LEAN = HERE / "lean" / "SecondClass"
CENSUS = HERE / "FWDEF_CENSUS.json"
LOG = HERE / "receipts" / "lean_axioms.txt"
PREDICTIONS = HERE / "PREDICTIONS.md"
LEDGER = HERE / "CLAIM_LEDGER.md"

MODULES = (
    "Kernel.lean",
    "IsoKernel.lean",
    "Rounds.lean",
    "Count.lean",
    "Clean.lean",
    "Recur.lean",
    "Counter.lean",
)
RECONSTRUCTED = ("Kernel.lean", "IsoKernel.lean")
NATIVE = ("Rounds.lean", "Count.lean", "Clean.lean", "Recur.lean", "Counter.lean")
TEST_FILES = (
    "test_census.py",
    "test_forbidden.py",
    "test_pins.py",
    "test_reconstruction.py",
    "test_class.py",
)
# A DEFINITION row may not carry a proof longer than this many lines.  The
# bound is on the class, not on the file: a long proof classed DEFINITION
# is the shape that hides content, which is why the exception list is
# separate and countable.
DEFINITION_PROOF_LINES = 12

# The scoring of the frozen FW-DEF prediction, computed by this file and
# dated in STATUS.md (2026-09-25).
PREDICTED_NAMES = 40
PREDICTED_CLASS_HITS = 40
PREDICTED_CLASS_MISSES = 0
UNPREDICTED_NATIVE = 1
UNPREDICTED = ("range_nodup",)
# No miss, dated in STATUS.md.
MISSES: dict[str, tuple[str, str]] = {}

# The statements credited to earlier rungs, proved again here.
CREDITED = (
    "replayE_cons",
    "insertNew_grows",
    "changes_counted",
    "step_parts",
    "growths_counted",
    "rest_counted",
    "getD_append_lt",
)
COUNTERMODELS = (
    "insts_need_nodup",
    "insts_need_wf",
    "rules_need_nodup",
    "rules_need_wf",
    "reqs_need_nodup",
    "reqs_need_wf",
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
            {"CONTENT": 5, "DEFINITION": 14, "RECONSTRUCTION": 17, "THIN": 22},
        )

    def test_no_definition_row_hides_a_long_proof(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        exceptions = payload["long_but_definitional"]
        lengths = proof_lengths()
        for name, row in payload["classes"].items():
            if row["class"] != "DEFINITION" or name in exceptions:
                continue
            self.assertLessEqual(lengths[name], DEFINITION_PROOF_LINES, name)
        self.assertEqual(sorted(exceptions), ["sortPair_map"])
        for name in exceptions:
            self.assertEqual(payload["classes"][name]["class"], "DEFINITION")
            self.assertGreater(lengths[name], DEFINITION_PROOF_LINES, name)

    def test_the_long_definition_is_case_exhaustion(self) -> None:
        """The one exception closes every case by rewriting conditionals;
        it calls no lemma of this package and inducts on nothing."""
        text = body("Count.lean", "sortPair_map")
        self.assertIn("by_cases", text)
        self.assertNotIn("induction", text)
        for name in census():
            if name != "sortPair_map":
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
        """No miss at the dated values.  A later reclassification of any
        row fails here by name rather than passing as a new hit or a new
        miss."""
        for name, cls in self.predicted.items():
            actual = self.actual[name]["class"]
            if actual != cls:
                self.assertEqual(MISSES.get(name), (cls, actual), name)
            else:
                self.assertNotIn(name, MISSES, name)

    def test_the_census_note_records_the_unpredicted_theorem(self) -> None:
        note = json.loads(CENSUS.read_text(encoding="utf-8"))["note"]
        for name in UNPREDICTED:
            self.assertIn(name, note, name)
        self.assertIn("recorded as unpredicted native work", note)


class StatementShapeTests(unittest.TestCase):
    """The frozen Lean-side predictions whose evidence is the statement
    text: what each theorem assumes, and what it does not."""

    def test_p1_data_and_forms_need_no_hypothesis(self) -> None:
        self.assertEqual(signature("Count.lean", "iso_data"),
                         "{r s : Regime} (σ : Iso r s) : r.data = s.data")
        self.assertEqual(signature("Count.lean", "iso_forms"),
                         "{r s : Regime} (σ : Iso r s) : r.forms.length = s.forms.length")

    def test_p2_the_three_lists_need_hypotheses_on_the_source_only(self) -> None:
        for name, field in (("insts_le", "insts"), ("rules_le", "rules"), ("reqs_le", "reqs")):
            stated = signature("Count.lean", name)
            self.assertIn(f"(hwf : r.wf) (hnd : r.{field}.Nodup) (σ : Iso r s)", stated, name)
            self.assertIn(f"r.{field}.length ≤ s.{field}.length", stated, name)
            self.assertNotIn("s.wf", stated, name)
            self.assertNotIn(f"s.{field}.Nodup", stated, name)
        both = signature("Count.lean", "components_iso")
        self.assertIn("(hr : Clean r) (hs : Clean s) (σ : Iso r s)", both)
        self.assertIn("r.reqs.length = s.reqs.length", both)
        self.assertIn("size r = size s", signature("Count.lean", "size_iso"))

    def test_p3_six_countermodels_one_hypothesis_broken_each(self) -> None:
        rows = census()
        for name in COUNTERMODELS:
            stated = signature("Counter.lean", name)
            field = name.split("_")[0]
            if name.endswith("_nodup"):
                self.assertIn("r.wf ∧ s.wf ∧ Dupfree s ∧ Nonempty (Iso r s)", stated, name)
            else:
                self.assertIn("Dupfree r ∧ Dupfree s ∧ s.wf ∧ Nonempty (Iso r s)", stated, name)
            self.assertIn(f"r.{field}.length ≠ s.{field}.length", stated, name)
            self.assertIn("decide", body("Counter.lean", name), name)
            self.assertEqual(rows[name]["class"], "DEFINITION", name)

    def test_p4_cleanness_is_kept_by_every_event(self) -> None:
        self.assertEqual(
            signature("Clean.lean", "clean_step"),
            "{r r' : Regime} {e : Event} (hc : Clean r) (h : stepE r e = some r') : Clean r'",
        )
        self.assertIn("Clean b → replayE h b = some r → Clean r",
                      signature("Clean.lean", "clean_replay"))
        for name, base in (("genesis_clean", "genesis"), ("R2L_clean", "R2L"),
                           ("R2F_clean", "R2F")):
            self.assertEqual(signature("Clean.lean", name), f": Clean {base}", name)

    def test_p5_no_return_and_stutter_need_only_a_clean_base(self) -> None:
        back = signature("Recur.lean", "no_return_class")
        self.assertIn("(hb : Clean b) (hs : stepE b e = some b') (hch : b' ≠ b)", back)
        self.assertIn("(σ : Iso r b) : False", back)
        stutter = signature("Recur.lean", "recurrence_is_stutter")
        self.assertIn("(hb : Clean b)", stutter)
        self.assertIn("(σ : Iso r₂ r₁) : r₂ = r₁ ∧ changes r₁ h₂ = 0", stutter)
        for stated in (back, stutter):
            self.assertEqual(stated.count("Clean"), 1)
            self.assertNotIn(".wf", stated)
            self.assertNotIn("Nodup", stated)

    def test_p6_the_counts_are_carried_by_the_class(self) -> None:
        stated = signature("Recur.lean", "counts_of_class")
        self.assertIn("(hb : Clean b)", stated)
        self.assertIn("changes b h = changes b h' ∧ growths b h = growths b h' ∧ "
                      "rest b h = rest b h'", stated)
        genesis = signature("Recur.lean", "counts_of_class_genesis")
        self.assertNotIn("Clean", genesis)
        self.assertIn("replayE h genesis = some r", genesis)

    def test_p7_across_bases_the_count_moves(self) -> None:
        stated = signature("Counter.lean", "counts_not_of_class")
        self.assertIn("Nonempty (Iso r₁ r₂) ∧ changes b₁ h₁ = 0 ∧ changes b₂ h₂ = 3", stated)
        text = body("Counter.lean", "counts_not_of_class")
        self.assertIn("[.admitDatum, .admitDatum, .impose 0 1]", text)
        self.assertIn("R2L, genesis", text)
        self.assertEqual(census()["counts_not_of_class"]["class"], "DEFINITION")

    def test_p8_the_classical_lemmas_are_not_used(self) -> None:
        """The library's counting, removal and range lemmas that reach
        `Classical.choice` are named nowhere in the package's code."""
        text = "\n".join(
            lean_audit.declaration_text((LEAN / m).read_text(encoding="utf-8"))
            for m in NATIVE
        )
        for name in ("length_le_of_subset", "length_erase_of_mem", "mem_erase_of_ne",
                     "List.nodup_range", "pairwise_lt_range", "classical"):
            self.assertNotIn(name, text, name)

    def test_the_credited_statements_say_whose_they_are(self) -> None:
        text = (LEAN / "Rounds.lean").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("Credited statements, proved again here", text)
        clean = (LEAN / "Clean.lean").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertIn("`getD_append_lt` repeats, as a statement, rung five's", clean)
        note = json.loads(CENSUS.read_text(encoding="utf-8"))["note"]
        for name in CREDITED:
            self.assertIn(name, note, name)
        self.assertIn("are credited, not counted as new to the run", note)


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
        self.assertEqual(tally, {"none": 3, "propext": 18, "Quot.sound propext": 37})


class LedgerTests(unittest.TestCase):
    """Prediction P-14: the recurrence row is decided here, and the
    irreversibility, succession and duration rows gain their class-level
    statements; every row says FORCED is conditional on an engine that
    does not exist yet, and every class-level statement carries its
    clean-base scope."""

    ROWS = ["recurrence", "irreversibility", "succession", "duration"]

    def test_the_ledger_touches_exactly_four_census_rows(self) -> None:
        text = LEDGER.read_text(encoding="utf-8")
        rows = re.findall(r"^\| CENSUS-([a-z]+) \|", text, re.M)
        self.assertEqual(rows, self.ROWS)

    def test_every_census_row_carries_the_engine_condition(self) -> None:
        for name in self.ROWS:
            self.assertIn("conditional on an engine", ledger_row(f"| CENSUS-{name}"), name)

    def test_every_census_row_carries_the_clean_base_scope(self) -> None:
        for name in self.ROWS:
            self.assertIn("clean base", ledger_row(f"| CENSUS-{name}"), name)

    def test_the_recurrence_row_names_its_evidence(self) -> None:
        row = ledger_row("| CENSUS-recurrence")
        for name in ("recurrence_is_stutter", "no_return_class", "clean_replay",
                     "size_iso", "genesis_clean", "R2L_clean", "R2F_clean"):
            self.assertIn(name, row, name)
        self.assertIn("stutter", row)

    def test_the_across_bases_countermodel_is_in_the_counting_rows(self) -> None:
        for name in ("succession", "duration"):
            row = ledger_row(f"| CENSUS-{name}")
            self.assertIn("counts_of_class", row, name)
            self.assertIn("counts_not_of_class", row, name)

    def test_every_ledger_row_names_evidence_that_exists(self) -> None:
        """A ledger row's Lean evidence must be a theorem of this package,
        and its Python evidence a test that exists."""
        rows = census()
        text = LEDGER.read_text(encoding="utf-8")
        cited = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_']*)`", text))
        lean_cited = cited & set(rows)
        self.assertGreater(len(lean_cited), 30)
        for name in re.findall(r"`(test_[a-z0-9_]+)`", text):
            found = any(
                name in (HERE / module).read_text(encoding="utf-8")
                for module in TEST_FILES
            )
            self.assertTrue(found, name)


if __name__ == "__main__":
    unittest.main()
