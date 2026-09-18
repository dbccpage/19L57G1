"""The list of research trees in ``research/README.md`` is generated.

``ci/research_index.py`` derives the table of trees and their gate-11 status
from the git index.  These tests fail when a tree is added or removed, or
registered in or out of the workflow's research job, without the README
being regenerated; they check that the estate audit reads the same wiring
from the workflow; and they exercise the stale-report path on a scratch
repository.
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


def test_the_estate_audit_reads_the_same_rows_and_the_same_wiring() -> None:
    ae = _estate_audit()
    trees = ri.group_trees(ri.tracked_research_files(REPO))
    wired = ri.wired_trees(ri.workflow_text(REPO))
    want = {name: ri.WIRED if name in wired else ri.LOCAL for name in trees}
    assert ae.parse_readme_trees(REPO / ri.README_REL) == want
    audit_wired, _ = ae.check_verify_yml(REPO / ri.WORKFLOW_REL)
    assert audit_wired & set(trees) == wired & set(trees)


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
    "      # research/umbrella/NOTE.md registers the rungs below",
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
        "| `stem` | local receipt only |\n"
        "| `stem_longer` | workflow (gate 11) |\n"
        "| `umbrella` | workflow (gate 11) |\n"
        f"{ri.END}\ntail\n"
    )
    (tmp_path / ri.README_REL).write_bytes(regenerated.encode("utf-8"))
    assert ri.problems(tmp_path) == []


def test_every_excluded_directory_exists() -> None:
    # An exclusion naming nothing would hide a future tree of that name.
    top = {p.split("/")[1] for p in ri.tracked_research_files(REPO) if p.count("/") >= 2}
    assert set(ri.NOT_TREES) <= top


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
