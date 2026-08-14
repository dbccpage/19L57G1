"""Tests for the contact-status artifact, its status branches, the
collision-cell mirror, and the enumeration probes."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

import run_primitive_contact
from run_primitive_contact import (
    COLLISION_CELLS,
    STATUS_HISTORY,
    _require,
    contact_report,
    enum_bool_observers,
    enum_descent_dictionary,
    enum_flagship_census,
    enum_settings_kernels,
    enum_value_fork,
)

REPO = Path(__file__).resolve().parent.parent

EXTERNAL_SHA = (
    "d9cdb350a53c513e3e211e72f17262be"
    "6ba85d7da6159f910388c7137e814a89")


def test_contact_processed_state() -> None:
    rep = contact_report(REPO)
    assert rep["package_present"] is True
    assert rep["manifest_present"] is True
    assert rep["status"] == "CONTACT_PROCESSED_LEAN_ONLY"
    history = rep["history"]
    assert isinstance(history, list)
    assert history == STATUS_HISTORY
    assert str(history[0]).startswith("CONTACT_INPUT_ABSENT")
    assert rep["prose_status"] == "PROSE_INPUT_ABSENT"
    # manifest binding: recorded hash of the committed manifest bytes
    manifest = (REPO / "contact" / "omega_primdiff"
                / "CONTACT_MANIFEST.json")
    want = hashlib.sha256(
        manifest.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    assert rep["manifest_sha256"] == want
    # the external hash comes from the manifest FIELD, never the file
    assert rep["external_file_sha256_per_manifest"] == EXTERNAL_SHA
    parsed = json.loads(manifest.read_text(encoding="utf-8"))
    assert parsed["files"][0]["sha256"] == EXTERNAL_SHA
    assert parsed["prose_supplied"] is False


def test_verdict_block() -> None:
    rep = contact_report(REPO)
    verdict = rep["verdict"]
    assert isinstance(verdict, dict)
    assert verdict["primary"] == \
        "CONTACT_INCOMPARABLE_WITH_COUNTERMODELS"
    terminals = verdict["terminals"]
    assert isinstance(terminals, list)
    codes = [t["code"] for t in terminals if isinstance(t, dict)]
    assert codes == [
        "CONTACT_INCOMPARABLE_WITH_COUNTERMODELS",
        "COMMON_PRIMITIVE_KERNEL_REPLACES_BOTH",
        "CONTACT_EQUIVALENT_UNDER_DECIDABLE_ZERO_PLUS_"
        "APARTNESS_ADMISSIONS",
    ]
    for t in terminals:
        assert isinstance(t, dict) and len(str(t["scope"])) > 100
    not_issued = verdict["not_issued"]
    assert isinstance(not_issued, list)
    dropped = {d["code"] for d in not_issued if isinstance(d, dict)}
    assert dropped == {"CONTACT_STRICTLY_STRONGER",
                       "NATIVE_STRICTLY_STRONGER",
                       "CONTACT_INPUT_ABSENT"}
    kernel = verdict["kernel"]
    assert isinstance(kernel, dict)
    assert kernel["structure"] == "ContactKernel.WitnessedDiff"


def test_equivalence_scope_splits_the_two_decidability_admissions(
) -> None:
    """Audit repair (2026-08-13): the equivalence terminal spends
    TWO different decidability admissions, one per direction; the
    scope must name each with its own theorems, and must record that
    the field-for-field premise is not reproducible in-repository."""
    rep = contact_report(REPO)
    verdict = rep["verdict"]
    assert isinstance(verdict, dict)
    terminals = verdict["terminals"]
    assert isinstance(terminals, list)
    scope = next(
        str(t["scope"]) for t in terminals if isinstance(t, dict)
        and str(t["code"]).startswith("CONTACT_EQUIVALENT"))
    assert "ASSERTED APARTNESS relation" in scope
    assert "isApart_repr" in scope and "apartObs_roundtrip" in scope
    assert "ZERO relation" in scope
    assert "obsApart_isApart" in scope
    assert "indist_obsApart_iff" in scope
    assert "NOT interchangeable" in scope
    assert "NOT reproducible from this repository" in scope
    assert "converse OPEN" in scope


def test_incomparable_scope_bounds_minimality_and_absence() -> None:
    """Audit repair (2026-08-13): only Bs=3 has proved carrier
    minimality, the crown is Prop-valued, and the supplied->native
    half is an absence claim rather than a countermodel."""
    rep = contact_report(REPO)
    verdict = rep["verdict"]
    assert isinstance(verdict, dict)
    terminals = verdict["terminals"]
    assert isinstance(terminals, list)
    scope = next(
        str(t["scope"]) for t in terminals if isinstance(t, dict)
        and t["code"] == "CONTACT_INCOMPARABLE_WITH_COUNTERMODELS")
    assert "exactly one reading - Bs at 3" in scope
    assert "bool_bs_repr" in scope
    assert "not a proved minimum" in scope
    assert "for Prop-valued observers" in scope
    assert "ABSENCE claim about the sealed corpus, NOT a refutation" \
        in scope
    assert "covers the native -> supplied direction only" in scope


def test_kernel_scope_states_grades_and_record_identity() -> None:
    """Audit repair (2026-08-13): the observer half of REPLACES is a
    record identity with a theorem, terminality is stated at its
    morphism grade, and value rigidity is sufficiency only."""
    rep = contact_report(REPO)
    verdict = rep["verdict"]
    assert isinstance(verdict, dict)
    terminals = verdict["terminals"]
    assert isinstance(terminals, list)
    scope = next(
        str(t["scope"]) for t in terminals if isinstance(t, dict)
        and t["code"] == "COMMON_PRIMITIVE_KERNEL_REPLACES_BOTH")
    assert "toDiffObs" in scope
    assert "DEFINITION not derivation" in scope
    assert "INDUCED-APARTNESS MORPHISM GRADE" in scope
    assert "necessity is not claimed" in scope
    assert "ENDPOINT DISTINCTNESS ONLY" in scope
    kernel = verdict["kernel"]
    assert isinstance(kernel, dict)
    assert "toDiffObs" in str(kernel["observer_side_identity"])


def test_status_branches(tmp_path: Path) -> None:
    rep = contact_report(tmp_path)
    assert rep["status"] == "CONTACT_INPUT_ABSENT"
    assert rep["package_present"] is False
    assert rep["manifest_sha256"] is None
    (tmp_path / "contact" / "omega_primdiff").mkdir(parents=True)
    rep2 = contact_report(tmp_path)
    assert rep2["status"] == "CONTACT_PRESENT_UNPROCESSED"
    analysis = tmp_path / "contact" / "analysis"
    analysis.mkdir()
    (analysis / "contact_countermodels.json").write_text(
        "{}", encoding="utf-8")
    rep3 = contact_report(tmp_path)
    assert rep3["status"] == "CONTACT_PROCESSED_LEAN_ONLY"


def test_collision_cells_mirror_lean_literal() -> None:
    assert len(COLLISION_CELLS) == 37
    text = (REPO / "lean4" / "Derivation"
            / "ContactKernel.lean").read_text(encoding="utf-8")
    block = text.split("def contactCells")[1]
    block = block.split("theorem contactCells_length")[0]
    strings = re.findall(r'"([^"]*)"', block)
    assert len(strings) == 3 * 37
    lean_rows = [tuple(strings[i:i + 3])
                 for i in range(0, len(strings), 3)]
    assert lean_rows == COLLISION_CELLS


def test_enum_bool_observers_pinned() -> None:
    assert enum_bool_observers() == {
        "delta_tables": 16,
        "zero_predicates": 4,
        "diag_zero_pairs": 24,
        "observer_law_pairs": 20,
        "witnessed_kernel_quadruples": 8,
        "oriented_complement_observers": 0,
    }


def test_enum_settings_kernels_pinned() -> None:
    assert enum_settings_kernels() == {
        "carriers": [1, 2, 3],
        "relation_counts": [2, 16, 512],
        "a_setting_counts": [0, 4, 192],
        "witnessed_kernel_counts_matching": [0, 4, 192],
        "representable_relation_counts": [1, 2, 5],
        "bell_numbers": [1, 2, 5],
        "witnessed_representable_counts": [0, 1, 3],
        "cotrans_equals_complement_transitivity": True,
    }


def test_enum_descent_dictionary_pinned() -> None:
    assert enum_descent_dictionary() == {
        "combinations": 64,
        "descend_count": 28,
        "fixed_domain_divergence_count": 36,
    }


def test_enum_flagship_and_value_fork_pinned() -> None:
    assert enum_flagship_census() == {"triples": 120}
    assert enum_value_fork() == {
        "value_type_size": 3,
        "tables": 81,
        "oriented_class_presentations": 2,
    }


def test_require_raises() -> None:
    with pytest.raises(ValueError):
        _require(False, "probe")
    _require(True, "probe")


def test_external_file_hash_when_present() -> None:
    """Manifest promise: verify the supplied file's hash when the
    external file is reachable; skip when absent (hosted CI), so
    artifact regeneration never depends on it."""
    candidates = [
        REPO / "docs_external_to_this_repo"
        / "primitive_difference.lean",
        REPO.parents[2] / "docs_external_to_this_repo"
        / "primitive_difference.lean",
    ]
    external = next((p for p in candidates if p.exists()), None)
    if external is None:
        pytest.skip("external contact file not present")
    got = hashlib.sha256(external.read_bytes()).hexdigest()
    assert got == EXTERNAL_SHA


# Native subject name: in the working denylist of 102, verified
# native at a5caee2, and the only working-denylist token permitted
# outside contact/analysis/.
_NATIVE_SUBJECT = "PrimitiveDifference"


def _identifier_token(name: str) -> re.Pattern[str]:
    return re.compile(r"(?<![\w])" + re.escape(name) + r"(?![\w])")


def _working_denylist() -> list[str]:
    payload = json.loads(
        (REPO / "contact" / "analysis" / "contact_countermodels.json")
        .read_text(encoding="utf-8"))
    block = payload["denylist"]
    assert isinstance(block, dict)
    full = block["full_census"]
    subtracted = block["subtracted_as_native_or_core"]
    assert isinstance(full, list)
    assert isinstance(subtracted, list)
    names = [n for n in full if isinstance(n, str)
             and n not in set(subtracted)]
    assert len(full) == 111
    assert len(names) == 102
    return names


def test_vocabulary_firewall_token_boundaries() -> None:
    """Negative: identifier-boundary matching catches a leak token
    and does not fire on a proper prefix or a glued suffix."""
    pat = _identifier_token("AaBbToken")
    assert pat.search("uses AaBbToken here")
    assert not pat.search("AaBbTokenMod")
    assert not pat.search("notAaBbToken")


def test_vocabulary_firewall_scan() -> None:
    """Working denylist identifiers must not appear as identifier
    tokens outside contact/analysis/. Census counts stay pinned in
    test_primitive_receipt; this test walks the tree."""
    if shutil.which("git") is None:
        pytest.skip("git unavailable")
    names = _working_denylist()
    patterns = [(n, _identifier_token(n)) for n in names
                if n != _NATIVE_SUBJECT]
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        capture_output=True, cwd=REPO, check=False)
    if proc.returncode != 0:
        pytest.skip("git ls-files failed")
    leaks: list[str] = []
    for raw in proc.stdout.split(b"\0"):
        if not raw:
            continue
        rel = raw.decode("utf-8", errors="replace").replace("\\", "/")
        if rel.startswith("contact/analysis/"):
            continue
        path = REPO / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for name, pat in patterns:
            if pat.search(text):
                leaks.append(f"{rel}:{name}")
    assert leaks == []


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_primitive_contact.main(["--artifacts", str(d1)]) == 0
    assert run_primitive_contact.main(["--artifacts", str(d2)]) == 0
    assert (d1 / "primitive_contact.json").read_bytes() == \
        (d2 / "primitive_contact.json").read_bytes()
