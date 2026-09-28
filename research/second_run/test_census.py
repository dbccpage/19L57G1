"""The census of the Lean package, and the frozen prediction it is scored
against.

A hand copy of the shape of `research/second_engine/test_census.py`, with
this tree's modules, counts, statement-shape checks and ledger rows.

Five things are checked here, none implying the others:

* the FW-DEF census is TOTAL over the package's theorem declarations, in
  both directions, read from the sources with the same parser the Lean
  audit uses;
* no row classed DEFINITION carries a long proof, so the class cannot
  absorb content;
* the frozen FW-DEF prediction of `PREDICTIONS.md` is scored MECHANICALLY
  against the committed census: the hit and miss counts are computed here
  and asserted at the values `STATUS.md` dates;
* the statement text of the theorems the frozen predictions R-1 and R-2
  name: what each assumes and what it does not;
* the committed axiom log covers every censused theorem and stays within
  the whitelist, and the ledger rows prediction R-23 names say what it
  says.

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

LEAN = HERE / "lean" / "SecondRun"
CENSUS = HERE / "FWDEF_CENSUS.json"
LOG = HERE / "receipts" / "lean_axioms.txt"
PREDICTIONS = HERE / "PREDICTIONS.md"
LEDGER = HERE / "CLAIM_LEDGER.md"

MODULES = ("Kernel.lean", "Run.lean")
RECONSTRUCTED = ("Kernel.lean",)
NATIVE = ("Run.lean",)
TEST_FILES = (
    "test_census.py",
    "test_forbidden.py",
    "test_fwd.py",
    "test_pins.py",
    "test_reconstruction.py",
)
DEFINITION_PROOF_LINES = 12

# The scoring of the frozen FW-DEF prediction, computed by this file and
# dated in STATUS.md (2026-09-28).
PREDICTED_NAMES = 13
PREDICTED_CLASS_HITS = 13
PREDICTED_CLASS_MISSES = 0
UNPREDICTED_NATIVE = 2
# Added after the prediction so that the structural refusal shape rests on
# a proof; recorded in STATUS.md as unpredicted work.
UNPREDICTED = ("collapsed_through", "not_separable_through")


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
    declaration to the next declaration, comments stripped."""
    lengths: dict[str, int] = {}
    for module in MODULES:
        text = lean_audit.declaration_text((LEAN / module).read_text(encoding="utf-8"))
        starts: list[tuple[int, str]] = []
        for match in lean_audit.THEOREM_DECL.finditer(text):
            line = text[: match.start()].count("\n")
            starts.append((line, lean_audit.canonical_identifier(match.group("name"))))
        lines = text.split("\n")
        for position, (line, name) in enumerate(starts):
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            body_lines = [
                row for row in lines[line:end]
                if row.strip() and not re.match(r"\s*(def|inductive|structure)\b", row)
            ]
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
        if line.startswith("The Lean objects"):
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

    def test_the_census_is_the_dated_one(self) -> None:
        """The counts STATUS.md dates.  A reclassification changes this
        line too, which is the point of writing it down."""
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["counts"],
            {"CONTENT": 1, "DEFINITION": 5, "RECONSTRUCTION": 17, "THIN": 9},
        )

    def test_no_definition_row_hides_a_long_proof(self) -> None:
        payload = json.loads(CENSUS.read_text(encoding="utf-8"))
        self.assertEqual(payload["long_but_definitional"], [])
        lengths = proof_lengths()
        for name, row in payload["classes"].items():
            if row["class"] == "DEFINITION":
                self.assertLessEqual(lengths[name], DEFINITION_PROOF_LINES, name)

    def test_the_length_reader_finds_the_longest_proof(self) -> None:
        """Not a vacuous bound: the package does carry native proofs longer
        than the DEFINITION limit, and they are classed otherwise."""
        lengths = proof_lengths()
        rows = census()
        native_long = [
            name
            for name, length in lengths.items()
            if length > DEFINITION_PROOF_LINES
            and rows[name]["module"] in NATIVE
            and rows[name]["class"] != "DEFINITION"
        ]
        self.assertIn("stepE_elems_le", native_long)


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
        hits = [n for n, cls in self.predicted.items() if self.actual[n]["class"] == cls]
        misses = sorted(set(self.predicted) - set(hits))
        self.assertEqual(len(hits), PREDICTED_CLASS_HITS)
        self.assertEqual(len(misses), PREDICTED_CLASS_MISSES)

    def test_the_unpredicted_native_declarations_are_counted(self) -> None:
        native = {n for n, row in self.actual.items() if row["module"] not in RECONSTRUCTED}
        self.assertEqual(len(native - set(self.predicted)), UNPREDICTED_NATIVE)
        self.assertEqual(sorted(native - set(self.predicted)), sorted(UNPREDICTED))
        note = json.loads(CENSUS.read_text(encoding="utf-8"))["note"]
        for name in UNPREDICTED:
            self.assertIn(name, note)

    def test_the_reconstructions_are_the_predicted_seventeen(self) -> None:
        text = PREDICTIONS.read_text(encoding="utf-8").replace("\r\n", "\n")
        section = text.split("Predicted RECONSTRUCTION")[1].split("Predicted DEFINITION")[0]
        named = set(re.findall(r"`([A-Za-z0-9_']+)`", section)) - {"Kernel.lean"}
        recon = {n for n, row in self.actual.items() if row["class"] == "RECONSTRUCTION"}
        self.assertEqual(named, recon)
        self.assertEqual(len(recon), 17)

    def test_the_scorer_can_say_missed(self) -> None:
        """NEGATIVE: a census that moved one row would be scored a miss."""
        moved = dict(self.actual)
        moved["no_return"] = {"class": "CONTENT", "module": "Run.lean"}
        hits = [n for n, cls in self.predicted.items() if moved[n]["class"] == cls]
        self.assertEqual(len(hits), PREDICTED_CLASS_HITS - 1)


class StatementShapeTests(unittest.TestCase):
    """Predictions R-1 and R-2: what each theorem assumes."""

    def test_r1_the_step_statements(self) -> None:
        self.assertEqual(
            signature("Run.lean", "stepE_elems_le"),
            "{r r' : Regime} {e : Event} (h : stepE r e = some r') : elems r ≤ elems r'",
        )
        self.assertEqual(
            signature("Run.lean", "stepE_elems_lt_of_ne"),
            "{r r' : Regime} {e : Event} (h : stepE r e = some r') (hne : r' ≠ r) : elems r < elems r'",
        )
        self.assertEqual(
            signature("Run.lean", "estep_elems_le"),
            "{s t : EState} {e : EEvent} (h : estep s e = some t) : elems s.regime ≤ elems t.regime",
        )
        self.assertIn("(hne : t.regime ≠ s.regime)", signature("Run.lean", "estep_elems_lt_of_ne"))
        self.assertEqual(
            signature("Run.lean", "switch_switch"),
            "(s : EState) : (estep s .switch).bind (fun t => estep t .switch) = some s",
        )
        self.assertIn("t.regime = s.regime", signature("Run.lean", "switch_keeps_regime"))

    def test_r2_the_history_statements(self) -> None:
        self.assertEqual(
            signature("Run.lean", "ereplay_elems_le"),
            "(h : List EEvent) {s t : EState} (hr : ereplay h s = some t) : "
            "elems s.regime ≤ elems t.regime",
        )
        self.assertIn(
            "(he : elems t.regime = elems s.regime) : t.regime = s.regime",
            signature("Run.lean", "ereplay_regime_eq_of_elems_eq"),
        )
        self.assertEqual(
            signature("Run.lean", "no_return"),
            "(h₁ h₂ : List EEvent) {s t u : EState} (h1 : ereplay h₁ s = some t) "
            "(hne : t.regime ≠ s.regime) (h2 : ereplay h₂ t = some u) : u.regime ≠ s.regime",
        )
        self.assertEqual(
            signature("Run.lean", "cycle_regime_const"),
            "(h₁ h₂ : List EEvent) {s t : EState} (h1 : ereplay h₁ s = some t) "
            "(h2 : ereplay h₂ t = some s) : t.regime = s.regime",
        )

    def test_the_refusal_shape_statements(self) -> None:
        self.assertEqual(
            signature("Run.lean", "not_separable_through"),
            "{r : Regime} {a b c : Nat} (h1 : collapsed r a c) (h2 : collapsed r b c) : "
            "¬ separable r a b",
        )
        self.assertIn(": collapsed r a b", signature("Run.lean", "collapsed_through"))

    def test_the_package_imports_nothing_sealed(self) -> None:
        for path in sorted((HERE / "lean").rglob("*.lean")):
            if ".lake" in path.parts:
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.startswith("import "):
                    self.assertTrue(
                        line.split()[1].startswith(("SecondRun", "Lake")), f"{path}: {line}"
                    )


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
        """Dated 2026-09-28 in STATUS.md and CLAIM_LEDGER.md."""
        tally: dict[str, int] = {}
        for line in LOG.read_text(encoding="utf-8").splitlines():
            if line.strip():
                key = line.split(" :: ")[1]
                tally[key] = tally.get(key, 0) + 1
        self.assertEqual(tally, {"none": 2, "propext": 17, "Quot.sound propext": 13})


class LedgerTests(unittest.TestCase):
    """Prediction R-23 and the evidence the ledger names."""

    def test_the_input_count_is_bounded_not_reduced(self) -> None:
        row = ledger_row("| INPUT-COUNT")
        self.assertIn("FINITE COMPUTATION", row)
        self.assertIn("not a floor proof", row)
        self.assertIn("not a reduction", row)

    def test_every_ledger_row_names_evidence_that_exists(self) -> None:
        """A ledger row's Lean evidence must be a theorem of this package,
        and its Python evidence a test that exists."""
        rows = census()
        text = LEDGER.read_text(encoding="utf-8")
        cited = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_'₀-₉]*)`", text))
        self.assertGreaterEqual(len(cited & set(rows)), 8)
        for name in re.findall(r"`(test_[a-z0-9_]+)`", text):
            found = any(
                name in (HERE / module).read_text(encoding="utf-8") for module in TEST_FILES
            )
            self.assertTrue(found, name)


if __name__ == "__main__":
    unittest.main()
