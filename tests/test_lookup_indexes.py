"""The two lookup indexes under ``docs/index/`` are generated and current.

``ci/lookup_indexes.py`` derives ``docs/index/topics.md`` (runner stem ->
the files of its family) and ``docs/index/pins.md`` (path -> the research
trees that pin it).  These tests fail, naming the stale file, when either
is out of date; they check the tree-object expansion on a parked module,
the scope pins read from verifier syntax trees, the listing of pinned
paths outside the seal, and that a path in an unclassified manifest field
stops generation; and they exercise the stale-report path on a scratch
repository.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

REPO = Path(__file__).resolve().parent.parent


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


li = _load("_lookup_indexes", REPO / "ci" / "lookup_indexes.py")

# The nine manifests the audit named as pinning lean4/Derivation as one tree
# object.  Measured on 2026-09-18 there are thirteen; these nine are among them.
# 2026-09-25: seven of the nine (with alpha_engine and f_class_distinctness,
# which the audit did not name) now pin the files they consume instead, so
# they leave this set; represented_execution and setting_translation still pin
# the tree (docs/research_pin_scope.md says why).
AUDIT_NAMED_TREE_PINNERS = frozenset({
    "represented_execution", "setting_translation",
})
PARKED_MODULE = "lean4/Derivation/IsoCollapseCompat.lean"


def test_both_indexes_are_current() -> None:
    found = li.problems(REPO)
    assert not found, (
        f"a lookup index is stale. Run `{li.REGENERATE}` and commit the result.\n"
        + "\n".join(found)
    )


def _census() -> Any:
    census = li.collect_pins(REPO, li.tracked_files(REPO))
    assert census.problems == ()
    return census


def _tree_pinners_of(prefix: str) -> set[str]:
    """Trees whose pin file records ``prefix`` itself as a tree object, read
    straight from the JSON rather than through the generator's tables."""
    trees: set[str] = set()
    for rel in li.tracked_files(REPO):
        if not rel.startswith("research/") or not li.PIN_FILE_NAME.match(rel.rsplit("/", 1)[1]):
            continue
        data = json.loads((REPO / rel).read_text(encoding="utf-8-sig"))
        consumed = data.get("consumed_trees", {}) if isinstance(data, dict) else {}
        package = data.get("source_package", {}) if isinstance(data, dict) else {}
        if prefix in consumed or package.get("path") == prefix:
            trees.add(rel.split("/")[1])
    return trees


def _row(section: str, path: str) -> str:
    text = (REPO / li.PINS_REL).read_text(encoding="utf-8")
    body = text.split(f"## {section}\n", 1)[1].split("\n## ", 1)[0]
    return str(next(line for line in body.splitlines() if line.startswith(f"| `{path}` |")))


def test_a_parked_module_lists_every_tree_object_pin() -> None:
    assert "import Derivation.IsoCollapseCompat" in (
        (REPO / "lean4" / "ParkedAudit.lean").read_text(encoding="utf-8")
    ), "the probe module is no longer parked; pick another from lean4/ParkedAudit.lean"
    census = _census()
    holders = {p.tree for p in census.pins if p.path == PARKED_MODULE and p.kind == "tree"}
    assert holders == _tree_pinners_of("lean4/Derivation")
    assert AUDIT_NAMED_TREE_PINNERS <= holders
    scoped = {s.tree for s in census.scopes}
    row = _row("Sealed paths", PARKED_MODULE)
    for tree in holders:
        assert f"`{tree}` (tree)" in row
    assert row.startswith(f"| `{PARKED_MODULE}` | {len(holders | scoped)} | ")
    assert row.endswith(f"| all {len(census.scopes)} |")


def test_every_file_under_a_tree_pin_carries_it() -> None:
    census = _census()
    pinners = _tree_pinners_of("lean4/Derivation")
    under = [f for f in li.tracked_files(REPO) if f.startswith("lean4/Derivation/")]
    assert under
    for path in under:
        got = {p.tree for p in census.pins if p.path == path and p.kind == "tree"}
        assert got == pinners, path


def test_scope_pins_are_read_from_diff_calls_only() -> None:
    census = _census()
    scoped = {s.tree for s in census.scopes}
    # natural_sections diffs the sealed pathspecs between its snapshot and HEAD.
    assert "natural_sections" in scoped
    # second_stream holds a sealed-prefix tuple too, but only to police its own
    # commits' write scope: a sealed change elsewhere does not fail it.
    assert "second_stream" not in scoped
    assert "SEALED_PREFIXES" in (
        REPO / "research" / "second_stream" / "verify_pins.py").read_text(encoding="utf-8")


def test_pinned_paths_outside_the_seal_are_listed_not_dropped() -> None:
    # 2026-09-19: sign_slice withdrew its consultation-only pins. Keep both
    # document and data examples, using their remaining actual pinners.
    # 2026-09-21: admission_sign_shadow dropped its CLAUDE.md pin (author
    # ruling); balance_carrier still pins the file.
    for path, tree in (
        ("CLAUDE.md", "balance_carrier"),
        ("contact/analysis/contact_countermodels.json", "sign_slice"),
    ):
        assert f"`{tree}` (file)" in _row("Other pinned paths", path)
        assert not li.is_sealed(path)


def test_the_root_lean_file_is_sealed_by_ruling() -> None:
    """``lean4/`` is carved to ``lean4/Derivation/`` plus the root file.

    2026-09-21: the author ruled on 2026-09-18 that ``lean4/Derivation.lean``
    is inside the seal.  This test used to assert the opposite; that
    assertion is withdrawn.  The rule names one exact file, so other
    top-level files and look-alike names stay outside.
    """
    assert li.is_sealed("lean4/Derivation/IsoCollapseCompat.lean")
    assert li.is_sealed("lean4/Derivation/Basic.lean")
    assert li.is_sealed("lean4/Derivation.lean")
    assert not li.is_sealed("lean4/ParkedAudit.lean")
    assert not li.is_sealed("lean4/lakefile.toml")
    assert not li.is_sealed("lean4/Derivation.lean.orig")
    row = _row("Sealed paths", "lean4/Derivation.lean")
    # 2026-09-24: 14, not 13, since g010_primitive_removal pins the import
    # closure of the Derivation root that its Lake package builds.
    assert row.startswith("| `lean4/Derivation.lean` | 14 |")
    assert row.endswith("| none |")


def test_every_field_rule_matches_some_pin_file() -> None:
    # A rule that names no field would hide a future field of that name.
    shapes: set[tuple[str, ...]] = set()
    not_trees = li._load_research_index().NOT_TREES
    for rel in li.pin_files(li.tracked_files(REPO), not_trees):
        data = json.loads((REPO / rel).read_text(encoding="utf-8-sig"))
        shapes.update(shape for shape, _ in li._strings(data))
    for rule in (*li.PIN_FIELDS, *li.NOT_PIN_FIELDS):
        assert any(li._matches(rule, shape) for shape in shapes), rule


def test_a_topic_row_reports_a_case_difference() -> None:
    text = (REPO / li.TOPICS_REL).read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if line.startswith("| `primdiff` |"))
    assert "`PrimDiff.lean` (case differs)" in row and row.endswith("| 5 of 5 |")


def test_outputs_lie_outside_the_seal_and_sealed_writes_are_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for rel in li.OUTPUTS:
        assert not li.is_sealed(rel)
    monkeypatch.setattr(li, "expected", lambda repo: {"paper/zzz_probe.md": "x\n"})
    with pytest.raises(ValueError, match="sealed"):
        li.write(tmp_path)
    assert not (tmp_path / "paper").exists()


def test_who_pins_prices_a_change() -> None:
    lines = li.who_pins(REPO, [PARKED_MODULE, "no/such/path.py"])
    assert lines[0].startswith(f"{PARKED_MODULE}: ")
    assert lines[1] == "no/such/path.py: pinned by no tree"
    assert lines[-1].startswith("distinct trees pinning the paths given: ")


# --- scratch repository ------------------------------------------------------


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=repo, check=True,
                   capture_output=True)


SCOPE_VERIFIER = "\n".join([
    'SEALED = ("code", "lean4/Derivation")',
    "def moved(git, snap):",
    '    return git("diff", "--name-only", snap, "HEAD", "--", *SEALED)',
    "",
])
STATUS_ONLY_VERIFIER = "\n".join([
    'SEALED = ("code", "lean4/Derivation")',
    "def dirty(git):",
    '    return git("status", "--porcelain", "--", *SEALED)',
    "",
])


def _scratch(tmp_path: Path, extra: dict[str, str] | None = None) -> Path:
    files = {
        "code/run_alpha.py": 'from derivation.alpha import go\nOUT = "alpha.json"\n',
        "code/derivation/alpha.py": "def go() -> None: ...\n",
        "tests/test_alpha.py": "import run_alpha\n",
        "lean4/Derivation/Alpha.lean": "-- alpha\n",
        "lean4/Derivation/Beta.lean": "-- beta\n",
        "artifacts/alpha.json": "{}\n",
        "research/one/SOURCE_MANIFEST.json": json.dumps(
            {"sources": [{"path": "lean4/Derivation/Alpha.lean", "sha256": "0" * 64}]}),
        "research/two/SOURCE_MANIFEST.json": json.dumps(
            {"consumed_trees": {"lean4/Derivation": "0" * 40},
             "tree_census": {"lean4/Derivation": ["lean4/Derivation/Alpha.lean"]},
             "pins": {"CLAUDE.md": "0" * 64}}),
        "research/three/verify_pins.py": SCOPE_VERIFIER,
        "research/four/verify_pins.py": STATUS_ONLY_VERIFIER,
        "CLAUDE.md": "contract\n",
    }
    files.update(extra or {})
    for rel, text in files.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_bytes(text.encode("utf-8"))
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    return tmp_path


def test_a_stale_index_is_reported_by_name_and_regenerated(tmp_path: Path) -> None:
    repo = _scratch(tmp_path)
    found = li.problems(repo)
    assert f"{li.TOPICS_REL} is missing; generate it with: {li.REGENERATE}" in found
    assert f"{li.PINS_REL} is missing; generate it with: {li.REGENERATE}" in found
    li.write(repo)
    assert li.problems(repo) == []

    pins = (repo / li.PINS_REL).read_text(encoding="utf-8")
    assert "| `lean4/Derivation/Alpha.lean` | 3 | `one` (file), `two` (tree) | all 1 |" in pins
    assert "| `lean4/Derivation/Beta.lean` | 2 | `two` (tree) | all 1 |" in pins
    assert "| `code/run_alpha.py` | 1 | none | all 1 |" in pins
    assert "| `CLAUDE.md` | 1 | `two` (file) | none |" in pins
    assert "| `research/three/verify_pins.py` | `code` `lean4/Derivation` | 4 |" in pins
    assert "research/four/verify_pins.py" not in pins
    topics = (repo / li.TOPICS_REL).read_text(encoding="utf-8")
    assert ("| `alpha` | `alpha.py` | `run_alpha.py` | `test_alpha.py` | `Alpha.lean` "
            "| `alpha.json` | 5 of 5 |") in topics
    assert "| `alpha` | `derivation.alpha` | `test_alpha.py` | `alpha.json` |" in topics

    # A new pin makes the pin index stale, and only it.
    manifest = repo / "research" / "one" / "SOURCE_MANIFEST.json"
    manifest.write_bytes(json.dumps({"sources": [
        {"path": "lean4/Derivation/Alpha.lean", "sha256": "0" * 64},
        {"path": "lean4/Derivation/Beta.lean", "sha256": "0" * 64},
    ]}).encode("utf-8"))
    found = li.problems(repo)
    assert found[0] == f"{li.PINS_REL} is stale; regenerate it with: {li.REGENERATE}"
    assert not any(line.startswith(li.TOPICS_REL) for line in found)
    assert "+| `lean4/Derivation/Beta.lean` | 3 | `one` (file), `two` (tree) | all 1 |" in found

    # A hand edit of the topic index is stale too.
    li.write(repo)
    topic_file = repo / li.TOPICS_REL
    topic_file.write_bytes(topic_file.read_bytes().replace(b"5 of 5", b"4 of 5"))
    found = li.problems(repo)
    assert found[0] == f"{li.TOPICS_REL} is stale; regenerate it with: {li.REGENERATE}"
    li.write(repo)
    assert li.problems(repo) == []

    # Line endings are not staleness.
    for rel in li.OUTPUTS:
        target = repo / rel
        target.write_bytes(target.read_bytes().replace(b"\n", b"\r\n"))
    assert li.problems(repo) == []


def test_a_path_in_an_unclassified_field_stops_generation(tmp_path: Path) -> None:
    repo = _scratch(tmp_path, {
        "research/five/SOURCE_MANIFEST.json": json.dumps(
            {"extra_pins": {"code/derivation/alpha.py": "0" * 64}}),
    })
    found = li.problems(repo)
    assert len(found) == 1
    assert "research/five/SOURCE_MANIFEST.json: field /extra_pins/<key> names the path " \
        "'code/derivation/alpha.py'" in found[0]
    assert "neither PIN_FIELDS nor NOT_PIN_FIELDS" in found[0]
