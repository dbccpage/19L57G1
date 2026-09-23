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


def _external_name() -> Path:
    """The external file's path as the contact manifest records it."""
    manifest = json.loads(
        (REPO / "contact" / "omega_primdiff" / "CONTACT_MANIFEST.json")
        .read_text(encoding="utf-8"))
    return Path(manifest["files"][0]["original_path"])


def _main_checkout(root: Path) -> Path | None:
    """The main worktree's root, read from git's common directory, so a
    linked worktree searches where the main checkout searches. None when
    git is unavailable or the common directory is not a checkout's
    .git."""
    if shutil.which("git") is None:
        return None
    proc = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        capture_output=True, cwd=root, check=False)
    if proc.returncode != 0:
        return None
    common = (root / proc.stdout.decode("utf-8").strip()).resolve()
    return common.parent if common.name == ".git" else None


def _external_candidates(
        root: Path, main: Path | None, name: Path) -> list[Path]:
    """Where the external contact file may sit. Each base, the checkout
    root and then the main checkout's root, contributes itself and its
    third ancestor when it has one; a base with fewer than three
    ancestors contributes itself only. Repeats keep their first place."""
    bases = [root] if main is None else [root, main]
    found = [b / name for base in bases
             for b in (base, *base.parents[2:3])]
    return list(dict.fromkeys(found))


def test_external_file_hash_when_present() -> None:
    """Manifest promise: verify the supplied file's hash when the
    external file is reachable; skip when absent (hosted CI), so
    artifact regeneration never depends on it."""
    candidates = _external_candidates(
        REPO, _main_checkout(REPO), _external_name())
    external = next((p for p in candidates if p.exists()), None)
    if external is None:
        pytest.skip("external contact file not present at: "
                    + "; ".join(str(p) for p in candidates))
    got = hashlib.sha256(external.read_bytes()).hexdigest()
    assert got == EXTERNAL_SHA


def test_external_candidates_tolerate_a_shallow_checkout() -> None:
    """A checkout with fewer than three ancestors has no third ancestor;
    the unguarded index raised IndexError there before the skip
    (2026-09-23). From three directories down, the candidates are the
    two the original list named."""
    name = Path("external") / "file.lean"
    anchor = Path(REPO.anchor)
    shallow = anchor / "wt" / "x"
    assert _external_candidates(shallow, None, name) == [shallow / name]
    three = anchor / "a" / "b" / "repo"
    assert _external_candidates(three, None, name) == [
        three / name, anchor / name]
    deep = anchor / "a" / "b" / "c" / "repo"
    assert _external_candidates(deep, None, name) == [
        deep / name, anchor / "a" / name]


def test_a_linked_worktree_searches_where_the_main_checkout_does() -> None:
    """Every checkout of one repository probes the main checkout's
    candidates, whatever its own depth; the main checkout adds nothing
    twice."""
    name = Path("external") / "file.lean"
    anchor = Path(REPO.anchor)
    main = anchor / "u" / "src" / "repos" / "repo"
    ancestor = anchor / "u" / name
    shallow = anchor / "wt" / "x"
    assert _external_candidates(shallow, main, name) == [
        shallow / name, main / name, ancestor]
    nested = main / ".claude" / "worktrees" / "y"
    assert _external_candidates(nested, main, name) == [
        nested / name, main / name, ancestor]
    assert _external_candidates(main, main, name) == [main / name, ancestor]


def test_main_checkout_is_read_from_the_git_common_directory(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """This checkout resolves to a root holding a .git directory, from
    the main checkout and from a linked worktree alike. A failed git
    call, or a common directory not named .git, gives None."""
    main = _main_checkout(REPO)
    if main is None:
        pytest.skip("git unavailable")
    assert (main / ".git").is_dir()

    def answer(code: int, out: bytes) -> object:
        def run(*args: object, **kwargs: object) -> object:
            return subprocess.CompletedProcess(args, code, out, b"")
        return run

    monkeypatch.setattr(subprocess, "run", answer(128, b""))
    assert _main_checkout(REPO) is None
    monkeypatch.setattr(subprocess, "run", answer(0, b"/srv/repo.git\n"))
    assert _main_checkout(REPO) is None


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
