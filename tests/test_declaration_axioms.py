"""The declaration-level axiom census (``ci/check_declaration_axioms.py``).

These tests cover generation and output parsing only; none of them runs
Lean.  The census itself is a local tool, not a registered gate, and its
proof is the injection recorded with the change that added it: a definition
carrying ``Classical.choice`` that no theorem reaches, in a parked module,
failed the census by name while ``ci/check_lean_audit.py`` stayed clean on
the same build.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

REPO = Path(__file__).resolve().parent.parent


def _load() -> ModuleType:
    path = REPO / "ci" / "check_declaration_axioms.py"
    spec = importlib.util.spec_from_file_location("check_declaration_axioms", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_declaration_axioms"] = module
    spec.loader.exec_module(module)
    return module


cda = _load()

# Real lines, copied from a local census run over the built package.
REAL_LINES = [
    'DECLAX_MODULE {"constants":2,"module":"Derivation.Basic","scope":"sealed"}',
    'DECLAX_CONST {"axioms":[],"instance":false,"internal":false,'
    '"kind":"recursor","module":"Derivation.Basic","name":"Derivation.Item.rec"}',
    'DECLAX_CONST {"axioms":[],"instance":false,"internal":false,'
    '"kind":"definition","module":"Derivation.Basic",'
    '"name":"Derivation.Event.admitForm.noConfusion"}',
]


def _module(name: str, count: int, scope: str = "sealed") -> str:
    return "DECLAX_MODULE " + json.dumps(
        {"module": name, "scope": scope, "constants": count})


def _const(
    module: str,
    name: str,
    kind: str = "definition",
    axioms: tuple[str, ...] = (),
    internal: bool = False,
    instance: bool = False,
) -> str:
    return "DECLAX_CONST " + json.dumps({
        "module": module, "name": name, "kind": kind, "internal": internal,
        "instance": instance, "axioms": list(axioms)})


def _end(modules: int, constants: int) -> str:
    return "DECLAX_END " + json.dumps({"modules": modules, "constants": constants})


def _clean_run() -> list[str]:
    """A census over the root plus two pinned modules, witness included."""
    return [
        "info: some unrelated message Lean may print",
        _module("Derivation", 0),
        _module("Derivation.A", 3),
        _const("Derivation.A", "Derivation.a_def", axioms=("propext",)),
        _const("Derivation.A", "Derivation.a_thm", kind="theorem",
               axioms=("propext", "Quot.sound")),
        _const("Derivation.A", "Derivation.a_def._proof_1", kind="theorem",
               internal=True),
        _module("Derivation.B", 2),
        _const("Derivation.B", "Derivation.instB", instance=True),
        _const("Derivation.B", "Derivation.B.rec", kind="recursor"),
        _module("ParkedAudit", 2, scope="witness"),
        _const("ParkedAudit", "ParkedAudit.helper",
               axioms=("propext", "Classical.choice", "Quot.sound")),
        _const("ParkedAudit", "ParkedAudit.list"),
        _end(4, 7),
    ]


PIN = ["Derivation.A", "Derivation.B"]


def _evaluate(lines: list[str], pin: list[str] = PIN) -> Any:
    return cda.evaluate(cda.parse_output("\n".join(lines)), pin)


# -- the module pin ------------------------------------------------------


def test_committed_pin_parses_to_its_own_lines() -> None:
    text = (REPO / "artifacts" / "elaborated_modules.txt").read_text(encoding="utf-8")
    want = [line for line in text.splitlines() if line.strip()]
    assert cda.parse_pin(text) == want
    assert all(name.startswith("Derivation.") for name in want)


def test_pin_refuses_a_line_that_is_not_a_module_name() -> None:
    with pytest.raises(ValueError, match="pin line 2 is not a Derivation module"):
        cda.parse_pin("Derivation.Basic\n#eval 1\n")
    with pytest.raises(ValueError, match="pin line 1"):
        cda.parse_pin("Other.Module\n")


def test_pin_refuses_repeats_and_emptiness() -> None:
    with pytest.raises(ValueError, match="repeats module Derivation.Basic"):
        cda.parse_pin("Derivation.Basic\nDerivation.Basic\n")
    with pytest.raises(ValueError, match="names no modules"):
        cda.parse_pin("\n\n")


def test_pin_accepts_crlf() -> None:
    assert cda.parse_pin("Derivation.A\r\nDerivation.B\r\n") == PIN


# -- the generated census ------------------------------------------------


def test_render_imports_root_then_sorted_pin_then_witness() -> None:
    text = cda.render_census(["Derivation.B", "Derivation.A"])
    imports = [line for line in text.splitlines() if line.startswith("import Derivation")
               or line.startswith("import ParkedAudit")]
    assert imports == [
        "import Derivation",
        "import Derivation.A",
        "import Derivation.B",
        "import ParkedAudit",
    ]
    assert "@@" not in text
    assert "(`Derivation).isPrefixOf modName" in text
    assert "modName == `ParkedAudit" in text
    assert "Lean.collectAxioms name" in text
    assert "data.constNames" in text


def test_render_names_every_kind_the_parser_accepts() -> None:
    text = cda.render_census(PIN)
    for kind in cda.KINDS:
        assert f'=> "{kind}"' in text
    assert text.count("=> \"") == len(cda.KINDS)


def test_render_carries_no_forbidden_token() -> None:
    # The generated file is not scanned by ci/check_lean_audit.py (it lives
    # outside the repository), so it is held to the same list here.
    text = cda.render_census(PIN)
    for pattern in (r"\bsorry\b", r"\badmit\b", r"^\s*axiom\s", r"\bunsafe\b",
                    r"\bpartial\b"):
        assert not re.search(pattern, text, flags=re.M), pattern


def test_render_refuses_a_name_that_is_not_a_module() -> None:
    with pytest.raises(ValueError, match="not a Derivation module name"):
        cda.render_census(["Derivation.A\nimport Evil"])


# -- parsing and evaluation ----------------------------------------------


def test_real_lines_parse() -> None:
    out = cda.parse_output("\n".join(REAL_LINES))
    assert out.malformed == []
    assert out.modules == {"Derivation.Basic": ("sealed", 2)}
    assert [c.kind for c in out.constants] == ["recursor", "definition"]
    assert out.constants[0].name == "Derivation.Item.rec"
    assert out.constants[0].axioms == ()


def test_clean_run_summary_counts_by_kind_and_prints_witness() -> None:
    ev = _evaluate(_clean_run())
    assert ev.failures == []
    assert ev.summary == (
        "declaration axiom census clean: 3 Derivation modules, 5 constants "
        "(axiom 0, constructor 0, definition 2, inductive 0, opaque 0, "
        "quotient 0, recursor 1, theorem 2; 1 instances, 1 internal details), "
        "axioms within ['Quot.sound', 'propext']"
    )
    assert ev.witness == (
        "witness (informational, outside the census by module): ParkedAudit "
        "adds 2 constants, 1 outside ['Quot.sound', 'propext']: "
        "ParkedAudit.helper (definition) [propext, Classical.choice, Quot.sound]"
    )


def test_disallowed_axiom_in_a_derivation_module_fails_by_name() -> None:
    lines = _clean_run()
    lines[3] = _const("Derivation.A", "Derivation.a_def",
                      axioms=("Classical.choice", "propext"))
    ev = _evaluate(lines)
    assert ev.failures == [
        "Derivation.A: Derivation.a_def (definition) depends on disallowed "
        "axioms ['Classical.choice'] [all: Classical.choice, propext]"
    ]
    assert ev.summary.startswith("declaration axiom census FAILED: ")
    assert ev.summary.endswith("constants outside ['Quot.sound', 'propext']: 1")


def test_any_axiom_outside_the_whitelist_fails_not_only_choice() -> None:
    lines = _clean_run()
    lines[4] = _const("Derivation.A", "Derivation.a_thm", kind="theorem",
                      axioms=("sorryAx",))
    ev = _evaluate(lines)
    assert len(ev.failures) == 1
    assert "Derivation.a_thm (theorem)" in ev.failures[0]
    assert "['sorryAx']" in ev.failures[0]


def test_witness_axioms_never_fail() -> None:
    ev = _evaluate(_clean_run())
    assert ev.failures == []
    assert ev.witness is not None and "ParkedAudit.helper" in ev.witness


def test_witness_line_without_any_outside_constant() -> None:
    lines = _clean_run()
    lines[10] = _const("ParkedAudit", "ParkedAudit.helper")
    ev = _evaluate(lines)
    assert ev.failures == []
    assert ev.witness is not None
    assert ev.witness.endswith("adds 2 constants, 0 outside ['Quot.sound', 'propext']")


def test_missing_witness_module_fails() -> None:
    lines = [line for line in _clean_run() if "ParkedAudit" not in line]
    lines[-1] = _end(3, 5)
    ev = _evaluate(lines)
    assert ev.failures == ["ParkedAudit was not read -- the witness is missing"]
    assert ev.witness is None


def test_pinned_module_absent_from_output_fails_by_name() -> None:
    ev = _evaluate(_clean_run(), pin=[*PIN, "Derivation.C"])
    assert ev.failures == [
        "Derivation.C is in the pin (or is the root) but the census read no "
        "constants from it"
    ]


def test_module_read_but_not_pinned_fails_by_name() -> None:
    ev = _evaluate(_clean_run(), pin=["Derivation.A"])
    assert ev.failures == [
        "Derivation.B was read by the census but is not in "
        "artifacts/elaborated_modules.txt"
    ]


def test_truncated_module_fails() -> None:
    lines = _clean_run()
    del lines[4]
    lines[-1] = _end(4, 6)
    ev = _evaluate(lines)
    assert ev.failures == [
        "Derivation.A declares 3 constants but the census reported 2"
    ]


def test_missing_end_record_fails() -> None:
    ev = _evaluate(_clean_run()[:-1])
    assert ev.failures == [
        "census output has no end record -- the run was cut short"
    ]


def test_end_record_disagreeing_with_records_fails() -> None:
    lines = _clean_run()
    lines[-1] = _end(4, 99)
    ev = _evaluate(lines)
    assert len(ev.failures) == 1
    assert ev.failures[0].startswith("end record counts (4, 99) differ")


def test_unresolved_constant_fails_by_name() -> None:
    lines = _clean_run()
    lines[7] = "DECLAX_UNRESOLVED " + json.dumps(
        {"module": "Derivation.B", "name": "Derivation.instB"})
    ev = _evaluate(lines)
    assert ev.failures == [
        "Derivation.B: Derivation.instB is in constNames but cannot be resolved"
    ]


def test_malformed_records_fail_and_other_lines_are_ignored() -> None:
    lines = _clean_run()
    lines.insert(1, "DECLAX_CONST {not json")
    lines.insert(1, "warning: unrelated")
    ev = _evaluate(lines)
    assert len(ev.failures) == 1
    assert ev.failures[0].startswith("malformed census record (")
    assert "DECLAX_CONST {not json" in ev.failures[0]


@pytest.mark.parametrize(
    "line, reason",
    [
        (_const("Derivation.A", "x", kind="lemma"), "unknown kind 'lemma'"),
        ('DECLAX_CONST {"module":"Derivation.A","name":"x","kind":"theorem",'
         '"internal":false,"instance":false,"axioms":[1]}',
         "field 'axioms' is not a list of strings"),
        ('DECLAX_CONST {"module":"Derivation.A","name":"x","kind":"theorem",'
         '"internal":0,"instance":false,"axioms":[]}',
         "field 'internal' is not a boolean"),
        ('DECLAX_MODULE {"module":"Derivation.A","scope":"sealed","constants":true}',
         "field 'constants' is not an integer"),
        ('DECLAX_MODULE {"module":7,"scope":"sealed","constants":1}',
         "field 'module' is not a string"),
        ("DECLAX_END []", "record is not a JSON object"),
    ],
)
def test_ill_typed_records_are_malformed(line: str, reason: str) -> None:
    out = cda.parse_output(line)
    assert len(out.malformed) == 1
    assert out.malformed[0].startswith(reason)


def test_repeated_module_and_end_records_are_malformed() -> None:
    lines = _clean_run()
    lines.insert(2, _module("Derivation", 0))
    lines.append(_end(4, 7))
    out = cda.parse_output("\n".join(lines))
    assert [m.split(":")[0] for m in out.malformed] == [
        "module Derivation reported twice",
        "end record reported twice",
    ]


def test_constant_without_module_record_and_unknown_scope_fail() -> None:
    lines = _clean_run()
    lines.insert(-1, _const("Derivation.Z", "Derivation.z"))
    lines.insert(-1, _module("Stray", 0, scope="elsewhere"))
    lines[-1] = _end(5, 8)
    ev = _evaluate(lines)
    assert "Derivation.Z has constant records but no module record" in ev.failures
    assert "Stray carries unknown scope 'elsewhere'" in ev.failures


# -- where the census file is written ------------------------------------


def test_census_directory_inside_the_repository_is_refused(tmp_path: Path) -> None:
    inside = REPO / "lean4"
    with pytest.raises(ValueError, match="is inside"):
        cda.temp_dir_outside(inside, [REPO])
    cda.temp_dir_outside(tmp_path, [REPO])


# -- the command line, with Lean replaced by a canned runner -------------


def _package(tmp_path: Path) -> Path:
    lean = tmp_path / "lean4"
    lean.mkdir()
    (lean / "lakefile.toml").write_bytes(b'name = "derivation"\n')
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    (artifacts / "elaborated_modules.txt").write_bytes(b"Derivation.A\nDerivation.B\n")
    return lean


def _runner(code: int, lines: list[str]) -> Any:
    seen: list[str] = []

    def run(lean_dir: Path, census: str, timeout: int) -> tuple[int, str]:
        seen.append(census)
        return code, "\n".join(lines)

    run.seen = seen  # type: ignore[attr-defined]
    return run


def test_main_clean_exits_zero(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    lean = _package(tmp_path)
    raw = tmp_path / "raw.txt"
    run = _runner(0, _clean_run())
    assert cda.main(["--lean-dir", str(lean), "--raw-out", str(raw)], runner=run) == 0
    printed = capsys.readouterr().out.splitlines()
    assert printed[0].startswith("declaration axiom census clean: 3 Derivation modules")
    assert printed[1].startswith("witness (informational")
    assert "import Derivation.B" in run.seen[0]  # type: ignore[attr-defined]
    assert raw.read_text(encoding="utf-8").startswith("info: some unrelated")


def test_main_names_the_failing_constant(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    lean = _package(tmp_path)
    lines = _clean_run()
    lines[7] = _const("Derivation.B", "Derivation.instB", instance=True,
                      axioms=("Classical.choice",))
    assert cda.main(["--lean-dir", str(lean)], runner=_runner(0, lines)) == 1
    printed = capsys.readouterr().out.splitlines()
    assert printed[0] == (
        "FAIL: Derivation.B: Derivation.instB (definition) depends on "
        "disallowed axioms ['Classical.choice'] [all: Classical.choice]"
    )
    assert printed[1].startswith("declaration axiom census FAILED")


def test_main_reports_a_lean_failure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    lean = _package(tmp_path)
    run = _runner(1, ["error: unknown module prefix 'Derivation'"])
    assert cda.main(["--lean-dir", str(lean)], runner=run) == 1
    out = capsys.readouterr().out
    assert "FAIL: `lake env lean` exited 1" in out
    assert "unknown module prefix" in out


def test_main_reports_a_runner_that_cannot_start(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    lean = _package(tmp_path)

    def broken(lean_dir: Path, census: str, timeout: int) -> tuple[int, str]:
        raise RuntimeError("lake is not on PATH")

    assert cda.main(["--lean-dir", str(lean)], runner=broken) == 1
    assert "FAIL: census did not run: lake is not on PATH" in capsys.readouterr().out


def test_main_print_census_does_not_run_lean(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    lean = _package(tmp_path)
    run = _runner(0, [])
    assert cda.main(["--lean-dir", str(lean), "--print-census"], runner=run) == 0
    assert run.seen == []  # type: ignore[attr-defined]
    assert "import Derivation.A\nimport Derivation.B\nimport ParkedAudit" in (
        capsys.readouterr().out)


def test_main_refuses_a_missing_pin_and_a_non_package(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    lean = _package(tmp_path)
    missing = tmp_path / "absent.txt"
    run = _runner(0, _clean_run())
    assert cda.main(["--lean-dir", str(lean), "--pin", str(missing)], runner=run) == 1
    assert "FAIL: cannot read module pin" in capsys.readouterr().out
    (lean / "lakefile.toml").unlink()
    assert cda.main(["--lean-dir", str(lean)], runner=run) == 1
    assert "is not the Lean package (no lakefile.toml)" in capsys.readouterr().out
    assert run.seen == []  # type: ignore[attr-defined]
