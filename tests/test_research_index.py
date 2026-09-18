"""The research-tree index in ``research/README.md`` is generated.

``ci/research_index.py`` derives the tree table and the hand-copy lists from
the git index and the workflow file.  These tests fail when the committed
README has drifted from the generator -- a tree added or removed, a tree
wired into or out of the research job, a verifier copied -- and check that
the generated table still parses the way
``research/estate_honesty/audit_estate.py`` reads it.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parent.parent
REGENERATE = "python ci/research_index.py --write"


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ri = _load("_research_index", REPO / "ci" / "research_index.py")
ae = _load(
    "_estate_audit", REPO / "research" / "estate_honesty" / "audit_estate.py"
)


def test_readme_matches_the_generator() -> None:
    problems = ri.problems(REPO)
    assert not problems, (
        f"research/README.md is stale. Run `{REGENERATE}` and commit the "
        "result.\n" + "\n".join(problems)
    )


def test_check_mode_exits_zero_on_the_committed_readme() -> None:
    result = subprocess.run(
        [sys.executable, "-B", "ci/research_index.py", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"`python ci/research_index.py --check` failed; run `{REGENERATE}`.\n"
        + result.stdout
        + result.stderr
    )


def test_generated_table_round_trips_through_the_estate_audit(
    tmp_path: Path,
) -> None:
    trees = ri.group_trees(ri.tracked_research_files(REPO))
    rows = ri.build_rows(REPO, trees)
    want = {row.name: row.status for row in rows}
    assert set(want.values()) <= {ri.WIRED, ri.LOCAL}
    readme = REPO / "research" / "README.md"
    block = ri.render_block(rows, ri.copy_holders(trees))
    generated = tmp_path / "README.md"
    generated.write_bytes(
        ri.splice(readme.read_bytes().decode("utf-8"), block).encode("utf-8")
    )
    assert ae.parse_readme_trees(generated) == want
    committed = ae.parse_readme_trees(readme)
    assert committed == want, (
        f"the committed table disagrees with the generator; run `{REGENERATE}`"
    )


def test_gate_11_match_is_a_whole_segment_on_a_non_comment_line() -> None:
    workflow = "\n".join([
        "name: probe",
        "jobs:",
        "  lean:",
        "    steps:",
        "      - run: python3 research/tree_a/verify_lean.py",
        "      # research/tree_b/verify_lean.py is named in a comment only",
        "  research:",
        "    steps:",
        "      # research/stem/NOTE.md is named in a comment only",
        "      - run: python research/stem_longer/verify_pins.py",
        "        working-directory: research/tree_a",
    ])
    research = ri.job_lines(workflow, "research")
    assert ri.mentions_tree(research, "tree_a")
    assert ri.mentions_tree(research, "stem_longer")
    assert not ri.mentions_tree(research, "stem")
    lean = ri.job_lines(workflow, "lean")
    assert ri.invokes_verify_lean(lean, "tree_a")
    assert not ri.invokes_verify_lean(lean, "tree_b")
    with pytest.raises(ValueError):
        ri.job_lines(workflow, "absent")


def test_dependents_read_lakefile_requires_and_json_paths(tmp_path: Path) -> None:
    files = {
        "research/tree_a/lean/lakefile.toml":
            '[[require]]\nname = "b"\npath = "../../tree_b/lean"\n',
        "research/tree_c/lean/lakefile.lean":
            '/- require x from "../../tree_a/lean" -/\n'
            '-- require y from "../../tree_a/lean"\n'
            'require z from "../../tree_b/lean"\n',
        "research/tree_d/pins.json":
            '{"a": "research/tree_c/x.lean", "b": "other/research/tree_a/y",'
            ' "c": "research/tree_d/own.py", "d": "research/unknown/z"}\n',
        "research/tree_b/lean/B.lean": "",
    }
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    trees = ri.group_trees(sorted(files))
    assert ri.dependents(tmp_path, trees) == {
        "tree_a": set(),
        "tree_b": {"tree_a", "tree_c"},
        "tree_c": {"tree_d"},
        "tree_d": set(),
    }


def test_splice_keeps_outside_text_and_refuses_bad_markers() -> None:
    text = f"head\r\n{ri.BEGIN}\r\nold\r\n{ri.END}\r\ntail\n"
    block = f"{ri.BEGIN}\nnew\n{ri.END}\n"
    assert ri.splice(text, block) == f"head\n{block}tail\n"
    for bad in ("no markers\n", f"{ri.END}\n{ri.BEGIN}\n", f"{ri.BEGIN}\n" * 2):
        with pytest.raises(ValueError):
            ri.splice(bad, block)
