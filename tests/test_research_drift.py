"""The research copy-drift lint: ``research/_scaffold/check_scaffold.py``.

The research trees keep hand copies of their verifiers on purpose; there is
no shared helper.  ``check_scaffold.py`` FAILS on the recurring correctness
defects: the substring coverage leak, and a quote-excluding name capture in
an axiom-report pattern, which drops a primed theorem name without a word.

The live-tree tests below are what give ``check_scaffold.py``'s errors teeth:
a new tree that copies an old, quote-blind parser fails the root suite, and
so does a pinned file whose bytes move.  The population test counts the
research Python files from the git index, independently of the walk the lint
does, so a file the walk cannot reach fails instead of vanishing from both
sides.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parent.parent


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cs = _load("_check_scaffold", REPO / "research" / "_scaffold" / "check_scaffold.py")

# The copies that carried a quote-excluding axiom-report capture when the
# check was added, measured at 827bf983 on 2026-09-18.  REPAIR_PENDING may
# lose entries as they are repaired; it may never gain one.
PENDING_AT_ADDITION = frozenset({
    "research/admission_sign_shadow/verify_frozen_compatibility.py",
    "research/admission_sign_shadow/verify_lean.py",
    "research/described_replay/verify_lean.py",
    "research/exchange_coefficients/verify.py",
    "research/higher_order_diagonalization/verify_lean.py",
    "research/iso_sound_lean/verify_lean.py",
    "research/seventh_constructor/verify_lean.py",
    "research/twin_pricing/verify_lean.py",
})

DEFECTIVE = "NO_AXIOMS = re.compile(r\"'([^']+)' does not depend on any axioms\")\n"
FIXED = "NO_AXIOMS = re.compile(r\"'(.+?)' does not depend on any axioms\")\n"


def _tracked(prefix: str = "research/") -> list[str]:
    proc = subprocess.run(["git", "ls-files", "-z", "--", prefix], cwd=REPO,
                          capture_output=True, check=True)
    return sorted(p.decode("utf-8") for p in proc.stdout.split(b"\0") if p)


def _write(path: Path, text: str | bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
    return path


# --- the reason for the literal check ---------------------------------------


def test_the_quote_excluding_capture_drops_a_primed_name_and_the_fixed_form_keeps_it() -> None:
    log = "'Tree.step'' does not depend on any axioms\n'Tree.plain' does not depend on any axioms\n"
    blind = re.findall(r"'([^']+)' does not depend on any axioms", log)
    fixed = re.findall(r"'(.+?)' does not depend on any axioms", log)
    assert blind == ["Tree.plain"]
    assert fixed == ["Tree.step'", "Tree.plain"]


# --- check_scaffold.py over the live tree -----------------------------------


def test_the_live_research_tree_carries_no_scaffold_error() -> None:
    errors, pinned = cs.axiom_capture_findings()
    errors = cs.coverage_errors() + errors
    assert not errors, "\n".join(errors)
    assert {line.split(":", 1)[0] for line in pinned} == (
        set(cs.FROZEN_EXCEPTIONS) | set(cs.REPAIR_PENDING))


def test_the_one_permanent_exception_is_the_frozen_boundary_seed_parser() -> None:
    assert set(cs.FROZEN_EXCEPTIONS) == {"research/boundary_seed/verify_lean.py"}


def test_repair_pending_only_shrinks() -> None:
    grown = set(cs.REPAIR_PENDING) - PENDING_AT_ADDITION
    assert not grown, f"REPAIR_PENDING gained entries it never had: {sorted(grown)}"
    assert not set(cs.REPAIR_PENDING) & set(cs.FROZEN_EXCEPTIONS)


def test_the_literal_scan_reaches_every_tracked_research_python_file() -> None:
    walked = {p.relative_to(REPO).as_posix() for p in cs.python_files()}
    indexed = {p for p in _tracked() if p.endswith(".py") and (REPO / p).is_file()}
    assert indexed, "no tracked research Python file at all; the census found nothing"
    assert indexed - walked == set(), f"tracked but not scanned: {sorted(indexed - walked)}"


# --- check_scaffold.py on fixtures ------------------------------------------


def _capture_errors(root: Path, frozen: dict[str, str] | None = None,
                    pending: dict[str, str] | None = None) -> tuple[list[str], list[str]]:
    result: tuple[list[str], list[str]] = cs.axiom_capture_findings(
        root, {} if frozen is None else frozen, {} if pending is None else pending)
    return result


def test_a_quote_excluding_capture_is_an_error_naming_file_and_line(tmp_path: Path) -> None:
    _write(tmp_path / "research" / "t" / "verify_lean.py", "import re\n" + DEFECTIVE)
    errors, pinned = _capture_errors(tmp_path)
    assert pinned == []
    assert len(errors) == 1
    assert errors[0].startswith("research/t/verify_lean.py:2: quote-excluding name capture")


def test_the_fixed_capture_is_clean(tmp_path: Path) -> None:
    _write(tmp_path / "research" / "t" / "verify_lean.py", "import re\n" + FIXED)
    assert _capture_errors(tmp_path) == ([], [])


@pytest.mark.parametrize("source", [
    # adjacent literals, joined as Python joins them
    'REPORT = (\n    r"\'(?P<name>[^\']+)\' "\n    r"(?:depends on axioms: x|does not depend on any axioms)"\n)\n',
    # a + chain of literals
    'REPORT = r"\'([^\']+)\' " + r"depends on axioms: x"\n',
    # the fixed parts of an f-string
    'P = "T"\nREPORT = rf"\'({P}[^\']+)\' does not depend on any axioms"\n',
    # escaped and leading-bracket members inside the class
    'REPORT = r"\'([^\\]\']+)\' does not depend on any axioms"\n',
    'REPORT = r"\'([^]\']+)\' does not depend on any axioms"\n',
    # the class with other members, and a star
    'REPORT = r"\'([^\'\\n]*)\' does not depend on any axioms"\n',
])
def test_every_literal_form_of_the_capture_is_seen(tmp_path: Path, source: str) -> None:
    _write(tmp_path / "research" / "t" / "verify.py", source)
    errors, _ = _capture_errors(tmp_path)
    assert len(errors) == 1 and "research/t/verify.py:" in errors[0], errors


@pytest.mark.parametrize("source", [
    # prose: a docstring and a comment naming the defective form
    '"""Not \'([^\']+)\': a primed name depends on axioms too."""\n',
    'def f() -> None:\n    """\'([^\']+)\' does not depend on any axioms"""\n',
    "# '([^']+)' does not depend on any axioms\nX = 1\n",
    # the axiom-list class excludes a bracket, not the quote
    'R = r"\'(.+?)\' depends on axioms: \\[([^\\]]*)\\]"\n',
    'R = r"\'(.+?)\' (?:depends on axioms: \\[([^]]*)\\]|does not depend on any axioms)"\n',
    # the class, but no axiom-report phrase
    'R = r"\'([^\']+)\'"\n',
])
def test_prose_and_other_patterns_are_not_errors(tmp_path: Path, source: str) -> None:
    _write(tmp_path / "research" / "t" / "verify.py", source)
    assert _capture_errors(tmp_path) == ([], [])


def test_hidden_directories_and_caches_are_not_scanned(tmp_path: Path) -> None:
    _write(tmp_path / "research" / "t" / "lean" / ".lake" / "p" / "v.py", DEFECTIVE)
    _write(tmp_path / "research" / "t" / "__pycache__" / "v.py", DEFECTIVE)
    _write(tmp_path / "research" / "t" / "sub" / "deep" / "v.py", FIXED)
    walked = [p.relative_to(tmp_path).as_posix() for p in cs.python_files(tmp_path)]
    assert walked == ["research/t/sub/deep/v.py"]


def test_a_byte_order_mark_is_read_and_an_unparsable_file_is_named(tmp_path: Path) -> None:
    _write(tmp_path / "research" / "t" / "bom.py", b"\xef\xbb\xbf" + DEFECTIVE.encode())
    _write(tmp_path / "research" / "t" / "broken.py", "axioms = (\n")
    errors, _ = _capture_errors(tmp_path)
    assert errors[0] == ("research/t/broken.py: cannot be read as Python (SyntaxError), "
                         "so it cannot be checked")
    assert errors[1].startswith("research/t/bom.py:1: quote-excluding name capture")


def _pinned_fixture(tmp_path: Path) -> tuple[Path, str, str]:
    path = _write(tmp_path / "research" / "t" / "verify_lean.py", "import re\n" + DEFECTIVE)
    return path, "research/t/verify_lean.py", cs.digest(path)


def test_a_pinned_capture_at_its_pinned_bytes_is_reported_not_failed(tmp_path: Path) -> None:
    _, rel, sha = _pinned_fixture(tmp_path)
    assert _capture_errors(tmp_path, pending={rel: sha}) == (
        [], [f"{rel}:2: DEFECT, repair pending"])
    assert _capture_errors(tmp_path, frozen={rel: sha}) == (
        [], [f"{rel}:2: frozen by verify_freeze.py; the one permanent exception"])


def test_a_crlf_checkout_keeps_the_pinned_digest(tmp_path: Path) -> None:
    path, rel, sha = _pinned_fixture(tmp_path)
    path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    assert _capture_errors(tmp_path, pending={rel: sha})[0] == []


def test_a_pinned_file_edited_but_still_defective_is_an_error(tmp_path: Path) -> None:
    path, rel, sha = _pinned_fixture(tmp_path)
    path.write_bytes(path.read_bytes() + b"# edited\n")
    errors, pinned = _capture_errors(tmp_path, pending={rel: sha})
    assert pinned == []
    assert len(errors) == 1
    assert errors[0].startswith(f"{rel}: named in REPAIR_PENDING but its bytes moved")
    assert "still carries the capture at line(s) 2; repair it" in errors[0]


def test_a_repaired_pinned_file_must_leave_the_list(tmp_path: Path) -> None:
    path, rel, sha = _pinned_fixture(tmp_path)
    path.write_text("import re\n" + FIXED, encoding="utf-8")
    errors, _ = _capture_errors(tmp_path, pending={rel: sha})
    assert len(errors) == 1
    assert errors[0].endswith("it no longer carries the capture; drop the entry")


def test_a_pinned_file_that_is_gone_or_never_carried_the_capture_is_an_error(
    tmp_path: Path,
) -> None:
    clean = _write(tmp_path / "research" / "t" / "clean.py", FIXED)
    errors, _ = _capture_errors(
        tmp_path,
        frozen={"research/t/gone.py": "0" * 64},
        pending={"research/t/clean.py": cs.digest(clean)},
    )
    assert errors == [
        "research/t/gone.py: named in FROZEN_EXCEPTIONS but absent; drop the entry",
        "research/t/clean.py: named in REPAIR_PENDING but its pinned bytes carry no capture; "
        "drop the entry",
    ]


def test_double_scan_counts_calls_not_comments(tmp_path: Path) -> None:
    once = ("def receipt_bytes() -> None:\n    failures = verify_sources()\n"
            "    # a second verify_sources() here would be redundant\n")
    twice = once + "    again = verify_sources()\n"
    _write(tmp_path / "research" / "a" / "run.py", once)
    _write(tmp_path / "research" / "b" / "run.py", twice)
    _write(tmp_path / "research" / "c" / "run.py", "def (\n")
    assert cs.run_warnings(tmp_path) == [
        "research/b/run.py: 2 verify_sources() calls (double custody scan)",
        "research/c/run.py: cannot be read as Python (SyntaxError); custody scans not counted",
    ]


def test_the_substring_coverage_leak_is_an_error(tmp_path: Path) -> None:
    _write(tmp_path / "research" / "a" / "check_coverage.py", "OMIT_PARTS = ()\n")
    _write(tmp_path / "research" / "b" / "check_coverage.py", "OMIT_DIRS = ()\ndef _directories(): ...\n")
    _write(tmp_path / "research" / "_scaffold" / "check_coverage.py", "OMIT_PARTS = ()\n")
    assert cs.coverage_errors(tmp_path) == [
        "research/a/check_coverage.py: substring COVERAGE_LEAK (OMIT_PARTS)"]


def test_main_exits_one_on_an_error_and_zero_otherwise(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(cs, "FROZEN_EXCEPTIONS", {})
    monkeypatch.setattr(cs, "REPAIR_PENDING", {})
    path = _write(tmp_path / "research" / "t" / "verify_lean.py", DEFECTIVE)
    assert cs.main(tmp_path) == 1
    assert "research/t/verify_lean.py:1: quote-excluding" in capsys.readouterr().out
    path.write_text(FIXED, encoding="utf-8")
    assert cs.main(tmp_path) == 0
    assert "scaffold clean of correctness drift; 0 pinned" in capsys.readouterr().out
