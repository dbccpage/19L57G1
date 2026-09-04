"""The FW-DEF census is total, and it is checked rather than asserted.

The frozen `PREDICTIONS.md` census named seventeen of this rung's targets.
An adversarial reading of the package before it was committed found that
the package carries far more theorems than that, and that the omissions
were disproportionately the trivia -- so a partial census flatters the
run.  `FWDEF_CENSUS.json` is the repair: it classifies EVERY theorem of
the package, and this file checks four things about it.

* A fast source-side cross-check of totality.  The authoritative totality
  check is ``verify_lean.py``'s independent compiler-environment census,
  which is compared with this file and the fresh axiom reports in CI.
* The two reconstruction modules are classed RECONSTRUCTION throughout,
  and no module of this rung's own work is.
* Nothing classed DEFINITION has a long non-comment declaration span.  This
  conservative count includes the statement as well as the proof, and is a
  crude bound stated as one: a short proof is not sufficient for being at the level
  of a definition, and the classification is the author's reading.  What
  the bound catches is the failure that matters -- a theorem with real work
  in it being filed as trivial to shrink the content count.
* The counts in the census match the counts `STATUS.md` reports, so the
  prose and the machine-readable file cannot drift apart.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import tempfile
import unittest
from unittest import mock

import verify_lean as lean_audit

HERE = pathlib.Path(__file__).resolve().parent
LEAN = HERE / "lean" / "SecondNoFirst"
CENSUS = HERE / "FWDEF_CENSUS.json"
RECONSTRUCTIONS = {"Kernel.lean", "Inherited.lean"}

# A proof at the level of a definition is short.  Twelve lines is generous
# on purpose: the bound exists to catch a long proof filed as trivial, not
# to decide the classification.
DEFINITION_LINE_BOUND = 12


def modules() -> list[pathlib.Path]:
    return lean_audit.modules()


def declared() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in modules():
        for name in lean_audit.theorem_names(path.read_text("utf-8")):
            if name in out:
                raise ValueError(
                    f"theorem leaf {name!r} is not globally unique: "
                    f"{out[name]} and {path.name}"
                )
            out[name] = path.name
    return out


COMMAND_START = re.compile(
    rf"^[ \t]*(?:{lean_audit.DECL_PREFIX}"
    r"(?:theorem|lemma|def|abbrev|opaque|inductive|structure|class|instance|example)\b|"
    r"(?:namespace|section|end|open|export|variable|universe|attribute|set_option)\b|#)",
    re.MULTILINE,
)


def _indent_at(text: str, position: int) -> int:
    line = text[position : text.find("\n", position) if "\n" in text[position:] else None]
    return len(line) - len(line.lstrip(" \t"))


def _proof_separator(segment: str) -> int | None:
    """Find a declaration-level ``:=``, ignoring bracketed binder defaults."""
    depth = 0
    pairs = {"(": ")", "[": "]", "{": "}"}
    closers = set(pairs.values())
    for index, char in enumerate(segment[:-1]):
        if char in pairs:
            depth += 1
        elif char in closers:
            depth = max(0, depth - 1)
        elif char == ":" and segment[index + 1] == "=" and depth == 0:
            return index
    return None


def proof_lines_in_text(text: str) -> dict[str, int]:
    """Measure every theorem/lemma shape recognized by the shared parser.

    For a ``:=`` declaration the count starts at its proof separator.  Lean
    equation-clause declarations have no such separator, so their whole
    non-comment declaration span is counted conservatively.
    """
    visible = lean_audit.declaration_text(text)
    declarations = list(lean_audit.THEOREM_DECL.finditer(visible))
    names = lean_audit.theorem_names(text)
    commands = list(COMMAND_START.finditer(visible))
    out: dict[str, int] = {}
    for declaration, name in zip(declarations, names, strict=True):
        indent = _indent_at(visible, declaration.start())
        later = [
            command.start()
            for command in commands
            if command.start() > declaration.start()
            and _indent_at(visible, command.start()) <= indent
        ]
        end = min(later, default=len(text))
        span = visible[declaration.start() : end]
        separator = _proof_separator(span)
        measured = span[separator + 2 :] if separator is not None else span
        if name in out:
            raise ValueError(f"duplicate theorem leaf in proof-length census: {name}")
        out[name] = sum(bool(line.strip()) for line in measured.splitlines())
    return out


def proof_lines() -> dict[str, int]:
    """Conservative non-comment declaration spans across the package census."""
    out: dict[str, int] = {}
    for path in modules():
        for name, length in proof_lines_in_text(path.read_text("utf-8")).items():
            if name in out:
                raise ValueError(f"duplicate theorem leaf in proof-length census: {name}")
            out[name] = length
    return out


class CensusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.census = json.loads(CENSUS.read_text(encoding="utf-8"))
        self.rows = self.census["classes"]

    def test_the_census_is_total_in_both_directions(self) -> None:
        found = declared()
        self.assertEqual(sorted(self.rows), sorted(found))

    def test_every_row_names_the_module_it_is_declared_in(self) -> None:
        found = declared()
        for name, row in self.rows.items():
            self.assertEqual(row["module"], found[name], name)

    def test_reconstructions_are_classed_as_such_and_nothing_else_is(
        self,
    ) -> None:
        for name, row in self.rows.items():
            if row["module"] in RECONSTRUCTIONS:
                self.assertEqual(row["class"], "RECONSTRUCTION", name)
            else:
                self.assertNotEqual(row["class"], "RECONSTRUCTION", name)

    def test_only_the_declared_classes_appear(self) -> None:
        allowed = {"RECONSTRUCTION", "DEFINITION", "THIN", "CONTENT"}
        self.assertEqual(
            {row["class"] for row in self.rows.values()} - allowed, set()
        )

    def test_nothing_classed_definitional_has_a_long_proof(self) -> None:
        """The crude bound.  A short proof does not make a theorem
        definitional; a long one makes the label implausible.

        One theorem is longer than the bound and is still at the level of a
        definition, because its length counts constructors rather than
        work.  It is EXCEPTED BY NAME, with its reason recorded in the
        census, rather than by raising the bound for everything: an
        exception that is listed can be counted and argued with, and a
        raised bound cannot."""
        lengths = proof_lines()
        self.assertEqual(set(lengths), set(self.rows))
        excepted = self.census.get("long_but_definitional", {})
        offenders = [
            f"{name} ({lengths[name]} lines)"
            for name, row in self.rows.items()
            if row["class"] == "DEFINITION"
            and lengths[name] > DEFINITION_LINE_BOUND
            and name not in excepted
        ]
        self.assertEqual(offenders, [])

    def test_every_exception_is_used_declared_and_definitional(self) -> None:
        """The exception list fails in both directions: an entry that is no
        longer over the bound, or is no longer classed definitional, or
        carries no reason, is a stale exception and is named."""
        lengths = proof_lines()
        excepted = self.census.get("long_but_definitional", {})
        self.assertLessEqual(len(excepted), 2)
        for name, reason in excepted.items():
            self.assertIn(name, self.rows, name)
            self.assertEqual(self.rows[name]["class"], "DEFINITION", name)
            self.assertGreater(lengths[name], DEFINITION_LINE_BOUND, name)
            self.assertGreater(len(reason), 80, name)

    def test_the_bound_would_catch_a_long_proof_filed_as_trivial(self) -> None:
        """NEGATIVE: the bound above is a check.  The longest CONTENT proof
        in the package exceeds the bound, so filing it as definitional
        would fail."""
        lengths = proof_lines()
        content = [
            lengths[name]
            for name, row in self.rows.items()
            if row["class"] == "CONTENT"
        ]
        self.assertGreater(max(content), DEFINITION_LINE_BOUND)

    def test_attributed_unicode_lemma_cannot_escape_proof_length_census(self) -> None:
        body = "\n".join(
            f"  have h{index} : True := True.intro" for index in range(14)
        )
        source = (
            "@[simp] protected lemma «δemand proof» : True := by\n"
            f"{body}\n"
            "  exact h0\n"
        )
        lengths = proof_lines_in_text(source)
        self.assertEqual(set(lengths), {"δemand proof"})
        self.assertGreater(lengths["δemand proof"], DEFINITION_LINE_BOUND)

    def test_same_indent_comment_inside_proof_does_not_truncate_span(self) -> None:
        source = (
            "theorem commentProbe : True := by\n"
            "/-! a same-indent proof comment is whitespace -/\n"
            + "\n".join(
                f"  have h{index} : True := True.intro" for index in range(14)
            )
            + "\n  exact h0\n"
        )
        self.assertGreater(
            proof_lines_in_text(source)["commentProbe"], DEFINITION_LINE_BOUND
        )

    def test_the_counts_are_consistent(self) -> None:
        counts: dict[str, int] = {}
        for row in self.rows.values():
            counts[row["class"]] = counts.get(row["class"], 0) + 1
        self.assertEqual(counts, self.census["counts"])
        self.assertEqual(sum(counts.values()), len(declared()))

    def test_the_status_prose_reports_the_same_counts(self) -> None:
        """The prose and the machine-readable census cannot drift."""
        status = (HERE / "STATUS.md").read_text(encoding="utf-8")
        ledger = (HERE / "CLAIM_LEDGER.md").read_text(encoding="utf-8")
        receipt_lines = [
            line
            for line in (HERE / "receipts" / "lean_axioms.txt")
            .read_text(encoding="utf-8")
            .splitlines()
            if line
        ]
        counts = self.census["counts"]
        own = sum(v for k, v in counts.items() if k != "RECONSTRUCTION")
        rows = {
            name: int(value)
            for name, value in re.findall(
                r"^\| (RECONSTRUCTION|DEFINITION|THIN|CONTENT) \| (\d+) \|",
                status,
                re.MULTILINE,
            )
        }
        self.assertEqual(rows, counts)
        own_row = re.search(
            r"Of this rung's own (\d+) theorems, \*\*(\d+) are at the level"
            r" of a definition and\s+(\d+) are one-step\*\*, leaving (\d+)",
            status,
        )
        self.assertIsNotNone(own_row)
        assert own_row is not None
        self.assertEqual(
            tuple(int(value) for value in own_row.groups()),
            (own, counts["DEFINITION"], counts["THIN"], counts["CONTENT"]),
        )
        total = sum(counts.values())
        axiom_free = sum(line.endswith(" :: none") for line in receipt_lines)
        self.assertEqual(len(receipt_lines), total)
        self.assertIn(f"every one of the {total} theorems", status)
        reliance = re.search(
            r"Every one of the (\d+) theorems.*?; (\d+) report no axiom",
            ledger,
            re.DOTALL,
        )
        self.assertIsNotNone(reliance)
        assert reliance is not None
        self.assertEqual(
            tuple(int(value) for value in reliance.groups()),
            (total, axiom_free),
        )

    def test_the_headline_conjunction_is_declared_definitional(self) -> None:
        """The finding the adversarial reading turned up, pinned so it
        cannot quietly be relabelled: the headline conjunction is an
        assembly of definitional facts and is classed as one."""
        self.assertEqual(self.rows["no_first_demand"]["class"], "DEFINITION")


class LeanVerifierTests(unittest.TestCase):
    def test_private_and_attributed_axioms_are_forbidden(self) -> None:
        """NEGATIVE: declaration modifiers may not hide a user axiom."""
        for text in (
            "private ax" + "iom hidden : False\n",
            "@[irreducible] protected ax" + "iom hidden : False\n",
        ):
            self.assertIsNotNone(lean_audit.LEADING_AXIOM.search(text))

    def test_attributed_theorem_is_in_the_axiom_population(self) -> None:
        text = "@[simp] theorem marked (n : Nat) : n = n := rfl\n"
        self.assertEqual(lean_audit.theorem_names(text), ["marked"])

    def test_comment_line_that_begins_with_theorem_is_not_a_declaration(self) -> None:
        text = "/-- prose\ntheorem in this sentence is not Lean code -/\n"
        self.assertEqual(lean_audit.theorem_names(text), [])

    def test_source_and_compiler_parsers_handle_quoted_and_unicode_names(self) -> None:
        source = (
            "namespace SecondNoFirst.Probe\n"
            "theorem «hidden theorem» (P : Prop) : P ∨ ¬ P := Classical.em P\n"
            "theorem δemand₁ : True := by trivial\n"
            "#print axioms «hidden theorem»\n"
            "#print axioms δemand₁\n"
            "end SecondNoFirst.Probe\n"
        )
        self.assertEqual(
            lean_audit.theorem_names(source), ["hidden theorem", "δemand₁"]
        )
        report_log = (
            "'SecondNoFirst.Probe.«hidden theorem»' depends on axioms: "
            "[propext, Classical.choice, Quot.sound]\n"
            "'SecondNoFirst.Probe.δemand₁' does not depend on any axioms\n"
        )
        reports, free = lean_audit.parse(report_log)
        qualified = {
            "SecondNoFirst.Probe.«hidden theorem»",
            "SecondNoFirst.Probe.δemand₁",
        }
        self.assertEqual(set(reports), qualified)
        self.assertEqual(free, 1)
        self.assertIn(
            "Classical.choice",
            reports["SecondNoFirst.Probe.«hidden theorem»"],
        )
        census_log = "\n".join(
            (
                'MODULE_CENSUS\t{"module":"SecondNoFirst.Probe"}',
                'DECL_CENSUS\t{"name":"SecondNoFirst.Probe.«hidden theorem»",'
                '"leaf":"hidden theorem","module":"SecondNoFirst.Probe",'
                '"axioms":["Classical.choice","Quot.sound","propext"]}',
                'DECL_CENSUS\t{"name":"SecondNoFirst.Probe.δemand₁",'
                '"leaf":"δemand₁","module":"SecondNoFirst.Probe","axioms":[]}',
            )
        )
        found_modules, records = lean_audit.parse_compiler_census(census_log)
        self.assertEqual(found_modules, {"SecondNoFirst.Probe"})
        self.assertEqual(set(records), qualified)
        self.assertEqual(
            records["SecondNoFirst.Probe.«hidden theorem»"][0], "hidden theorem"
        )

    def test_module_census_is_recursive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lean = pathlib.Path(tmp)
            nested = lean / "SecondNoFirst" / "Nested"
            nested.mkdir(parents=True)
            (nested / "Probe.lean").write_text("theorem probe : True := by trivial\n")
            (nested / "lakefile.lean").write_text(
                "theorem nestedConfigName : True := by trivial\n"
            )
            report = lean / "SecondNoFirst" / "AxiomReport.lean"
            report.write_text("\n")
            with mock.patch.object(lean_audit, "LEAN", lean):
                self.assertEqual(
                    lean_audit.module_names(),
                    [
                        "SecondNoFirst.AxiomReport",
                        "SecondNoFirst.Nested.Probe",
                        "SecondNoFirst.Nested.lakefile",
                    ],
                )

    def test_duplicate_module_basenames_fail_fwdef_origin_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lean = pathlib.Path(tmp)
            for directory in ("A", "B"):
                target = lean / "SecondNoFirst" / directory
                target.mkdir(parents=True)
                (target / "Probe.lean").write_text(
                    "theorem probe : True := by trivial\n", encoding="utf-8"
                )
            with mock.patch.object(lean_audit, "LEAN", lean):
                with self.assertRaisesRegex(ValueError, "duplicate module basename"):
                    lean_audit.module_names()

    def test_compiler_leaf_collision_fails_fwdef_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fwdef = pathlib.Path(tmp) / "FWDEF_CENSUS.json"
            fwdef.write_text(
                json.dumps({"classes": {"same": {"module": "A.lean"}}}),
                encoding="utf-8",
            )
            records = {
                "SecondNoFirst.A.same": ("same", "SecondNoFirst.A", ()),
                "SecondNoFirst.B.same": ("same", "SecondNoFirst.B", ()),
            }
            with (
                mock.patch.object(lean_audit, "FWDEF", fwdef),
                mock.patch.object(
                    lean_audit,
                    "module_names",
                    return_value=["SecondNoFirst.A", "SecondNoFirst.B"],
                ),
                mock.patch.object(
                    lean_audit,
                    "modules",
                    return_value=[pathlib.Path("A.lean"), pathlib.Path("B.lean")],
                ),
            ):
                failures = lean_audit.fwdef_failures(records)
        self.assertTrue(
            any("share FW-DEF leaf key 'same'" in failure for failure in failures),
            failures,
        )

    def test_root_and_report_modules_cannot_escape_population(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lean = pathlib.Path(tmp)
            package = lean / "SecondNoFirst"
            package.mkdir()
            (lean / "SecondNoFirst.lean").write_text(
                "theorem «root theorem» : True := by trivial\n", encoding="utf-8"
            )
            (package / "AxiomReport.lean").write_text(
                "theorem reportTheorem : True := by trivial\n", encoding="utf-8"
            )
            with mock.patch.object(lean_audit, "LEAN", lean):
                self.assertEqual(
                    lean_audit.module_names(),
                    ["SecondNoFirst", "SecondNoFirst.AxiomReport"],
                )

    def test_private_theorem_source_shape_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "private theorem"):
            lean_audit.theorem_names(
                "private theorem hidden : True := by trivial\n"
            )

    def test_failed_lake_clean_stops_before_build(self) -> None:
        failed = subprocess.CompletedProcess(
            args=["lake", "clean"], returncode=7, stdout="", stderr="probe failure"
        )
        with mock.patch.object(subprocess, "run", return_value=failed) as run:
            stage, code, log = lean_audit.build()
        self.assertEqual((stage, code), ("clean", 7))
        self.assertIn("probe failure", log)
        run.assert_called_once()
        self.assertEqual(run.call_args.kwargs["encoding"], "utf-8")
        self.assertEqual(run.call_args.kwargs["errors"], "strict")

    def test_regen_refuses_a_disallowed_compiler_axiom(self) -> None:
        report_log = "'Probe' depends on axioms: [Classical.choice]\n"
        census_log = "\n".join(
            (
                'MODULE_CENSUS\t{"module":"SecondNoFirst"}',
                'DECL_CENSUS\t{"name":"Probe","leaf":"probe",'
                '"module":"SecondNoFirst","axioms":["Classical.choice"]}',
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            log = pathlib.Path(tmp) / "lean_axioms.txt"
            with mock.patch.multiple(
                lean_audit,
                token_scan=mock.DEFAULT,
                module_names=mock.DEFAULT,
                build=mock.DEFAULT,
                run_compiler_census=mock.DEFAULT,
                fwdef_failures=mock.DEFAULT,
                LOG=log,
            ) as patched:
                patched["token_scan"].return_value = []
                patched["module_names"].return_value = ["SecondNoFirst"]
                patched["build"].return_value = ("build", 0, report_log)
                patched["run_compiler_census"].return_value = (0, census_log)
                patched["fwdef_failures"].return_value = []
                self.assertEqual(lean_audit.audit(regen=True), 1)
            self.assertFalse(log.exists())


if __name__ == "__main__":
    unittest.main()
