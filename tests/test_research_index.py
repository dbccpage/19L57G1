"""The list of research trees in ``research/README.md`` is generated.

``ci/research_index.py`` derives the table of trees and their gate-11 status
from the git index.  These tests fail when a tree is added or removed, or
registered in or out of the workflow's research job, or given a different
maintenance status, without the README
being regenerated; they check that the estate audit reads the same rows and
differs from this reading of the workflow only where recorded; and they exercise the stale-report path on a scratch
repository.  The longer ``--show`` table is checked against facts measured
on 2026-09-18 and on a scratch repository.
"""

from __future__ import annotations

import importlib.util
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


ri = _load("_research_index", REPO / "ci" / "research_index.py")


def _estate_audit() -> ModuleType:
    # Loaded per test, not at collection: an edit inside that research tree
    # must not be able to break collection of the root suite.
    return _load("_estate_audit", REPO / "research" / "estate_honesty" / "audit_estate.py")


def test_readme_lists_every_tree_and_its_gate_11_status() -> None:
    found = ri.problems(REPO)
    assert not found, (
        f"research/README.md is stale. Run `{ri.REGENERATE}` and commit the result.\n"
        + "\n".join(found)
    )


def test_the_estate_audit_reads_the_same_rows_and_differs_only_as_recorded(
    tmp_path: Path,
) -> None:
    ae = _estate_audit()
    trees = ri.group_trees(ri.tracked_research_files(REPO))
    workflow = ri.workflow_text(REPO)
    wired = ri.wired_trees(workflow)
    want = {name: ri.WIRED if name in wired else ri.LOCAL for name in trees}
    assert ae.parse_readme_trees(REPO / ri.README_REL) == want
    # The audit reads a file; give it the same (index) text the generator read.
    copy = tmp_path / "verify.yml"
    copy.write_bytes(workflow.encode("utf-8"))
    audit_wired, _ = ae.check_verify_yml(copy)
    assert wired <= audit_wired
    assert (audit_wired - wired) & set(trees) == set(ri.KNOWN_AUDIT_DIFFERENCES)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=repo, check=True,
                   capture_output=True)


WORKFLOW = "\n".join([
    "name: probe",
    "jobs:",
    "  lean:",
    "    steps:",
    "      - run: python3 research/stem/verify_lean.py",
    "  research:",
    "    steps:",
    "      # research/umbrella/NOTE.md is named in a comment only: not run",
    "      - run: python research/stem_longer/verify_pins.py",
    "        working-directory: research/stem_longer",
    "",
])


def test_a_stale_readme_is_reported_by_name_and_regenerated(tmp_path: Path) -> None:
    files = {
        ".github/workflows/verify.yml": WORKFLOW,
        "research/stem/verify.py": "",
        "research/stem_longer/verify_pins.py": "",
        "research/umbrella/NOTE.md": "",
        "research/_template/run.py": "",
        "research/notes/idea.md": "",
        "research/README.md": f"head\n{ri.BEGIN}\n| `stem` | local receipt only |\n{ri.END}\ntail\n",
    }
    for rel, text in files.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_bytes(text.encode("utf-8"))
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")

    found = ri.problems(tmp_path)
    assert found[0].startswith("research/README.md is stale")
    assert "trees missing from the table: stem_longer, umbrella" in found

    current = (tmp_path / ri.README_REL).read_text(encoding="utf-8")
    regenerated = ri.expected_readme(tmp_path, current)
    assert regenerated == (
        f"head\n{ri.BEGIN}\n{ri.HEADER}\n{ri.RULE}\n"
        "| `stem` | local receipt only |  |\n"
        "| `stem_longer` | workflow (gate 11) |  |\n"
        "| `umbrella` | local receipt only |  |\n"
        f"{ri.END}\ntail\n"
    )
    (tmp_path / ri.README_REL).write_bytes(regenerated.encode("utf-8"))
    assert ri.problems(tmp_path) == []


def test_every_excluded_directory_exists() -> None:
    # An exclusion naming nothing would hide a future tree of that name.
    top = {p.split("/")[1] for p in ri.tracked_research_files(REPO) if p.count("/") >= 2}
    assert set(ri.NOT_TREES) <= top
    trees = set(ri.group_trees(ri.tracked_research_files(REPO)))
    assert set(ri.PARKED_TREES) <= trees
    assert not set(ri.PARKED_TREES) & ri.wired_trees(ri.workflow_text(REPO))


def test_splice_keeps_outside_text_and_refuses_bad_markers() -> None:
    text = f"head\r\n{ri.BEGIN}\r\nold\r\n{ri.END}\r\ntail\n"
    block = f"{ri.BEGIN}\nnew\n{ri.END}\n"
    assert ri.splice(text, block) == f"head\n{block}tail\n"
    for bad in ("no markers\n", f"{ri.END}\n{ri.BEGIN}\n", f"{ri.BEGIN}\n" * 2):
        with pytest.raises(ValueError):
            ri.splice(bad, block)


def test_show_prints_one_row_per_tree(capsys: pytest.CaptureFixture[str]) -> None:
    assert ri.main(["--show"]) == 0
    rows = [line for line in capsys.readouterr().out.splitlines() if line.startswith("| `")]
    assert len(rows) == len(ri.group_trees(ri.tracked_research_files(REPO)))


# --show columns.  The trees below are named bare, never as paths under
# research/: this file is itself read by the consumer column, and a path
# written here would make these tests a consumer of what they check.

@pytest.fixture(scope="module")
def show_rows() -> dict[str, dict[str, str]]:
    return ri.show_rows(REPO)


def test_show_lean_cell_names_every_verifier_that_calls_lake_or_lean(
    show_rows: dict[str, dict[str, str]],
) -> None:
    cell = show_rows["admission_sign_shadow"]["Lean"]
    # The checker segment itself, not the frozen mark, must name both.
    count, checkers, *marks = cell.split("; ")
    assert checkers == "local `verify_frozen_compatibility.py`, `verify_lean.py`", cell
    assert f"3 {ri.FROZEN_MARK} `{ri.FROZEN_VERIFIER}`" in marks, cell


# Trees whose Lean library compiles from a gitignored staging folder.  A bare
# `lake build` failed in each of them on 2026-09-18 (missing staged sources).
STAGING_TREES = frozenset({
    "diagonal_identity", "exchange_coefficients", "family_embedding",
    "natural_sections", "s9_obligations",
})


def test_show_marks_exactly_the_trees_that_build_from_staged_sources(
    show_rows: dict[str, dict[str, str]],
) -> None:
    marked = {name for name, row in show_rows.items() if ri.STAGED_BUILD_FAILS in row["Lean"]}
    assert marked == STAGING_TREES, (
        f"marked but not pinned: {sorted(marked - STAGING_TREES)}; "
        f"pinned but not marked: {sorted(STAGING_TREES - marked)}"
    )
    for name in STAGING_TREES:
        assert ri.STAGING_MARK in show_rows[name]["Lean"], name
    # This tree ignores a staging folder that no Lake library reads; its bare
    # `lake build` passed on 2026-09-18, so it must not carry the mark above.
    assert ri.STAGED_UNREAD in show_rows["observer_visibility"]["Lean"]


def test_show_marks_lean_files_without_a_lake_package(
    show_rows: dict[str, dict[str, str]],
) -> None:
    assert ri.NO_LAKE_PACKAGE in show_rows["symmetry_floor"]["Lean"]


def test_show_sees_executable_lake_or_lean_invokers(
    show_rows: dict[str, dict[str, str]],
) -> None:
    """Root verifiers that locate the binary as ``executable("lake"|"lean")``.

    The argv / ``which("lake")`` / ``lake.exe`` forms miss this family.
    """
    for name in ("oriented_boundary", "sign_tower", "symmetry_floor"):
        cell = show_rows[name]["Lean"]
        assert "`verify_lean.py`" in cell, (name, cell)
        assert ri.NO_LEAN_VERIFIER not in cell, (name, cell)


def test_show_counts_root_tests_as_consumers(show_rows: dict[str, dict[str, str]]) -> None:
    for name in ("boundary_seed", "side_free"):
        assert ri.ROOT_TESTS in show_rows[name]["required or named by"], name


def test_show_counts_a_sibling_path_built_in_python(
    show_rows: dict[str, dict[str, str]],
) -> None:
    owners = show_rows["p209a_wigner_phase_space"]["required or named by"]
    assert "`p209d_nonclassical_horizons`" in owners, owners


# Every file name the claims column has met.  A new naming convention fails
# here by name; a new tree using one of these names does not.
CLAIM_DOCUMENT_NAMES = frozenset({
    "CLAIMS.md", "CLAIM_LEDGER.md", "RECONCILED_CLAIMS_LEDGER.md", "claim_ledger.md",
    "claims.md",
})


def test_claim_document_names_are_pinned() -> None:
    holders: dict[str, list[str]] = {}
    for name, files in ri.group_trees(ri.tracked_research_files(REPO)).items():
        for document in ri.claim_documents(files):
            holders.setdefault(document, []).append(name)
    new = {d: holders[d] for d in sorted(set(holders) - CLAIM_DOCUMENT_NAMES)}
    gone = sorted(CLAIM_DOCUMENT_NAMES - set(holders))
    assert not new and not gone, (
        f"claim documents under an unpinned name: {new}; pinned names no tree uses: {gone}"
    )


SCRATCH_WORKFLOW = "\n".join([
    "name: probe",
    "jobs:",
    "  lean:",
    "    steps:",
    "      - run: python3 research/zq_front/verify_lean.py",
    "  research:",
    "    steps:",
    "      - run: echo nothing",
    "",
])

SCRATCH_FILES = {
    ".github/workflows/verify.yml": SCRATCH_WORKFLOW,
    "research/README.md": f"{ri.BEGIN}\n{ri.END}\n",
    # A staged library: lakefile.lean requires a sibling tree and compiles
    # from a folder the tree's .gitignore ignores.
    "research/zq_front/CLAIMS.md": "",
    "research/zq_front/verify_lean.py": 'import subprocess\nsubprocess.run(["lake", "build"])\n',
    "research/zq_front/verify_extra.py": 'import shutil\nshutil.which("lean")\n',
    "research/zq_front/verify_pins.py": "print('lake and lean are only words here')\n",
    "research/zq_front/lean/.gitignore": "sealed/\n",
    "research/zq_front/lean/lakefile.lean": (
        'import Lake\nopen Lake DSL\npackage zq_front\n'
        'require zq_back from "../../zq_back/lean"\n'
        'lean_lib Snap where\n  srcDir := "sealed"\n'
    ),
    "research/zq_front/lean/Front.lean": "import Snap.Core\n",
    # Two lakefiles, an ignored staging folder no library reads, and an
    # import of the sealed package with no require and no staging.
    "research/zq_back/Ledger.md": "",
    "research/zq_back/.gitignore": "/pinned/\n",
    "research/zq_back/lakefile.toml": 'name = "zq_back"\n',
    "research/zq_back/lean/lakefile.toml": 'name = "zq_back_lean"\n',
    "research/zq_back/lean/Back.lean": "import Derivation.Core -- sealed\nimport Lean\n",
    # Lean sources with no Lake package at all.
    "research/zq_loose/Loose.lean": "theorem t : True := trivial\n",
    # Python consumers.
    "research/zq_user/tool.py": (
        "from pathlib import Path\n"
        "HERE = Path(__file__).resolve().parent\n"
        'SIBLING = HERE.parent / "zq_loose" / "Loose.lean"\n'
        'UP = "../zq_front/x"\n'
        'SELF = "research/zq_user/x"\n'
    ),
    "research/zq_user/doc_only.py": (
        '"""Only a docstring names research/zq_back/ here."""\n'
        "# and a comment: research/zq_back/x\n"
        "def f() -> None:\n"
        '    """research/zq_back/ again."""\n'
    ),
    "research/zq_bad/broken.py": 'def broken(:\n    return "research/zq_back/x"\n',
    "research/zq_top.py": 'from pathlib import Path\nP = Path("r") / "research" / "zq_back"\n',
    "research/notes/n.py": 'P = "research/zq_back/x"\n',
    "tests/test_zq.py": 'P = "research/zq_front/verify_lean.py"\n',
    "ci/zq_tool.py": 'import os\nP = os.path.join("r", "research", "zq_loose")\n',
}


def test_show_columns_on_a_scratch_repository(tmp_path: Path) -> None:
    for rel, text in SCRATCH_FILES.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_bytes(text.encode("utf-8"))
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")

    rows = ri.show_rows(tmp_path)
    assert list(rows) == ["zq_back", "zq_bad", "zq_front", "zq_loose", "zq_user"]
    assert rows["zq_front"]["Lean"] == (
        "1; workflow Lean job `verify_lean.py`, local `verify_extra.py`; "
        f"{ri.STAGING_MARK} (`lean/sealed`, gitignored); {ri.STAGED_BUILD_FAILS}"
    )
    assert rows["zq_back"]["Lean"] == (
        "1; no root verifier invokes lake or lean; "
        "2 lakefiles: `lakefile.toml`, `lean/lakefile.toml`; "
        f"{ri.STAGING_MARK} (`pinned`, gitignored) {ri.STAGED_UNREAD}; "
        "1 file imports Derivation.* with no lean4 require and no staging"
    )
    assert rows["zq_loose"]["Lean"] == (
        f"1; {ri.NO_LEAN_VERIFIER}; {ri.NO_LAKE_PACKAGE}"
    )
    assert rows["zq_user"]["Lean"] == "none"
    assert [rows[n]["claims"] for n in ("zq_front", "zq_back", "zq_user")] == [
        "`CLAIMS.md`", "`Ledger.md`", "none",
    ]
    owners = {name: row["required or named by"] for name, row in rows.items()}
    assert owners == {
        # lakefile.lean require; unparseable Python; top-level and excluded
        # directories.  The docstrings and comment in doc_only.py do not count.
        "zq_back": "`zq_bad`, `zq_front`, notes (not a tree), research top level",
        "zq_bad": "none",
        "zq_front": "`zq_user`, root tests",
        "zq_loose": "`zq_user`, ci",
        "zq_user": "none",
    }
    lines = ri.show(tmp_path).splitlines()
    assert lines[0] == "| " + " | ".join(ri.SHOW_COLUMNS) + " |"
    assert len(lines) == 2 + len(rows)


def test_staging_mark_needs_an_import_without_a_tracked_source(tmp_path: Path) -> None:
    files = {
        ".github/workflows/verify.yml": SCRATCH_WORKFLOW,
        "research/zq_front/lean/.gitignore": "sealed/\n",
        "research/zq_front/lean/lakefile.lean": 'lean_lib Snap where\n  srcDir := "sealed"\n',
        "research/zq_front/lean/Front.lean": "import Front.Part\n",
        "research/zq_front/lean/Front/Part.lean": "",
    }
    for rel, text in files.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_bytes(text.encode("utf-8"))
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    cell = ri.show_rows(tmp_path)["zq_front"]["Lean"]
    assert cell.endswith(f"(`lean/sealed`, gitignored); {ri.STAGED_UNIMPORTED}"), cell



def test_parked_status_drift_is_reported_and_gate_registration_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    for rel, text in {
        ".github/workflows/verify.yml": WORKFLOW,
        "research/stem/verify.py": "",
        "research/README.md": f"{ri.BEGIN}\n{ri.END}\n",
    }.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text, encoding="utf-8")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "--", ".github/workflows/verify.yml",
         "research/stem/verify.py", "research/README.md")
    monkeypatch.setattr(ri, "PARKED_TREES", {"stem": "reviewed in this fixture"})
    page = tmp_path / ri.README_REL
    expected = ri.expected_readme(tmp_path, page.read_text(encoding="utf-8"))
    page.write_text(expected, encoding="utf-8")
    assert not ri.problems(tmp_path)
    assert ri.show_rows(tmp_path)["stem"]["status"] == "parked"
    page.write_text(expected.replace("| parked |", "|  |"), encoding="utf-8")
    diagnostic = "\n".join(ri.problems(tmp_path))
    assert "research/README.md is stale" in diagnostic and "stem" in diagnostic
    page.write_text(expected, encoding="utf-8")
    assert not ri.problems(tmp_path)
    with pytest.raises(ValueError, match="parked trees are registered in gate 11: stem"):
        ri.render_block(["stem"], {"stem"})
