"""Python stages of the three local Lean verifiers added for oriented_boundary,
sign_tower, and symmetry_floor.  None of these tests runs lake or lean.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parent.parent

TREES = {
    "oriented_boundary": "research/oriented_boundary/verify_lean.py",
    "sign_tower": "research/sign_tower/verify_lean.py",
    "symmetry_floor": "research/symmetry_floor/verify_lean.py",
}


def _load(label: str, rel: str) -> ModuleType:
    path = REPO / rel
    spec = importlib.util.spec_from_file_location(f"verify_lean_{label}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


MODULES = {name: _load(name, rel) for name, rel in TREES.items()}


def _row(
    name: str = "M.t",
    axioms: list[str] | None = None,
    *,
    internal: bool = False,
    private: bool = False,
    last: str = "t",
    parent: str = "other",
    projection: bool = False,
) -> dict[str, object]:
    return {
        "name": name,
        "axioms": list(axioms or []),
        "internal": internal,
        "private": private,
        "last": last,
        "parent": parent,
        "projection": projection,
    }


@pytest.mark.parametrize("name", sorted(MODULES))
def test_primed_theorem_names_stay_whole(name: str) -> None:
    vl = MODULES[name]
    reports, failures = vl.parse_reports(
        "'Foo.bar'' depends on axioms: [propext]\n"
        "'Foo.none' does not depend on any axioms\n"
    )
    assert failures == []
    assert reports == {"Foo.bar'": ["propext"], "Foo.none": []}


@pytest.mark.parametrize("name", sorted(MODULES))
def test_unrecognised_report_shape_is_named(name: str) -> None:
    vl = MODULES[name]
    reports, failures = vl.parse_reports("'Foo.t' depends on axioms: not-a-list")
    assert reports == {}
    assert any("report shape was not recognised" in item for item in failures)


@pytest.mark.parametrize("name", sorted(MODULES))
def test_compare_names_a_missing_and_an_extra_authored_theorem(name: str, monkeypatch: pytest.MonkeyPatch) -> None:
    vl = MODULES[name]
    monkeypatch.setattr(vl, "EXPECTED_THEOREMS", frozenset({"M.kept", "M.missing"}))
    if hasattr(vl, "EXPECTED_AXIOMS"):
        monkeypatch.setattr(
            vl, "EXPECTED_AXIOMS", {"M.kept": [], "M.missing": []}
        )
    rows = [
        _row("M.kept"),
        _row("M.extra"),
        _row("M.gen.inj", last="inj", parent="constructor"),
    ]
    reports = {"M.kept": [], "M.extra": []}
    failures, kinds = vl.compare(rows, reports)
    assert kinds["authored"] == 2
    assert kinds["generated"] == 1
    assert "census theorem M.extra is not in EXPECTED_THEOREMS" in failures
    assert "expected theorem M.missing is not in the compiled census" in failures


@pytest.mark.parametrize("name", sorted(MODULES))
def test_stale_exemption_digest_fails_scan_tokens(name: str, monkeypatch: pytest.MonkeyPatch) -> None:
    vl = MODULES[name]
    relative = sorted(vl.EXPECTED_FILES)[0]
    monkeypatch.setattr(
        vl, "KNOWN_PROSE_LINES", {relative: frozenset({"0" * 64})}
    )
    failures = vl.scan_tokens()
    assert any("stale token exemption" in item for item in failures)


def test_sign_tower_inventory_names_equal_expected_theorems() -> None:
    vl = MODULES["sign_tower"]
    text = (REPO / "research/sign_tower/lean/Inventory.lean").read_text(encoding="utf-8")
    names = re.findall(r"^#print axioms (\S+)\s*$", text, re.MULTILINE)
    assert len(names) == 56
    assert set(names) == vl.EXPECTED_THEOREMS
    assert len(names) == len(set(names))


@pytest.mark.parametrize("name", ("oriented_boundary", "sign_tower"))
def test_lake_manifest_digest_folds_crlf(name: str, tmp_path: Path) -> None:
    vl = MODULES[name]
    lf = tmp_path / "lake-manifest.json"
    lf.write_bytes(b'{"packages": []}\n')
    crlf = tmp_path / "other" / "lake-manifest.json"
    crlf.parent.mkdir()
    crlf.write_bytes(b'{"packages": []}\r\n')
    assert vl.file_digest(lf) == vl.file_digest(crlf)
    notes_lf = tmp_path / "notes.md"
    notes_crlf = tmp_path / "notes-crlf.md"
    notes_lf.write_bytes(b"keep\n")
    notes_crlf.write_bytes(b"keep\r\n")
    assert vl.file_digest(notes_lf) != vl.file_digest(notes_crlf)
