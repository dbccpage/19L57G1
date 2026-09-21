"""The new-tree contract rejects defects while leaving existing trees alone."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

REPO = Path(__file__).resolve().parents[1]
SCAFFOLD = REPO/"research/_scaffold"
SPEC = importlib.util.spec_from_file_location("new_tree_contract", REPO/"ci/check_new_research_trees.py")
assert SPEC and SPEC.loader
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, encoding="utf-8").strip()


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    (tmp_path/"research/legacy").mkdir(parents=True)
    (tmp_path/"research/legacy/README.md").write_text("unchanged legacy tree\n")
    (tmp_path/"lean4").mkdir()
    shutil.copyfile(REPO/"lean4/lean-toolchain", tmp_path/"lean4/lean-toolchain")
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "contract-test")
    git(tmp_path, "config", "user.email", "contract-test@example.invalid")
    git(tmp_path, "config", "core.autocrlf", "false")
    git(tmp_path, "add", "--", "research/legacy/README.md", "lean4/lean-toolchain")
    git(tmp_path, "commit", "-qm", "existing tree")
    scaffold = tmp_path/"research/_scaffold"
    scaffold.mkdir()
    (scaffold/"grandfathered.json").write_text(json.dumps({"schema": 1, "baseline": git(tmp_path, "rev-parse", "HEAD"), "trees": ["legacy"]}))
    shutil.copytree(SCAFFOLD/"new_tree_templates", scaffold/"new_tree_templates")
    result = subprocess.run([sys.executable, str(SCAFFOLD/"new_tree.py"), "probe", "--repo", str(tmp_path)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout+result.stderr
    assert contract.problems(tmp_path) == []
    return tmp_path


def test_current_repository_is_grandfathered_and_clean() -> None:
    assert contract.problems(REPO) == []


def test_missing_claim_file_fails_by_path_then_recovers(repository: Path) -> None:
    claim = repository/"research/probe/CLAIMS.md"
    original = claim.read_bytes()
    claim.unlink()
    assert any("research/probe/CLAIMS.md" in error for error in contract.problems(repository))
    claim.write_bytes(original)
    assert contract.problems(repository) == []
    assert (repository/"research/legacy/README.md").read_text() == "unchanged legacy tree\n"


@pytest.mark.parametrize("mutation, expected", [
    ("status", "invalid claim row or status"),
    ("claims_alias", "CLAIMS.md"),
    ("noop", "verify.py"),
    ("root_package", "one package under lean"),
    ("bare_inventory", "Lean modules must live under the unique tree root"),
    ("import_inventory", "do not import a census module"),
    ("import_bare_inventory", "do not import a census module"),
    ("scope", "printed declarations differ"),
    ("empty_pins", "nonempty unique list"),
])
def test_contract_mutations_are_named(repository: Path, mutation: str, expected: str) -> None:
    tree = repository/"research/probe"
    if mutation == "status":
        path = tree/"CLAIMS.md"
        path.write_text(path.read_text().replace("PROVED_THEOREM", "proved theorem"))
    elif mutation == "claims_alias":
        (tree/"CLAIM_LEDGER.md").write_text("second claim document\n")
    elif mutation == "noop":
        (tree/"verify.py").write_text("raise SystemExit(0)\n")
    elif mutation == "root_package":
        shutil.copyfile(tree/"lean/lakefile.toml", tree/"lakefile.toml")
    elif mutation == "bare_inventory":
        (tree/"lean/Inventory.lean").write_text("-- misplaced census\n")
    elif mutation in ("import_inventory", "import_bare_inventory"):
        path = tree/"lean/ResearchProbe.lean"
        imported = "ResearchProbe.AxiomReport" if mutation == "import_inventory" else "Inventory"
        path.write_text("import "+imported+"\n"+path.read_text())
    elif mutation == "scope":
        path = tree/"lean/ResearchProbe/AxiomReport.lean"
        path.write_text("import ResearchProbe\n")
    else:
        path = tree/"TREE_CONTRACT.json"
        data = json.loads(path.read_text())
        data["pin_files"] = []
        path.write_text(json.dumps(data))
    failures = contract.problems(repository)
    assert any(expected in failure for failure in failures), failures


def test_duplicate_roots_name_both_trees(repository: Path) -> None:
    shutil.copytree(repository/"research/probe", repository/"research/duplicate")
    failures = contract.problems(repository)
    assert any("ResearchProbe" in f and "duplicate" in f for f in failures)
    assert any("ResearchProbe" in f and "probe" in f for f in failures)


def test_new_tree_cannot_be_added_to_the_frozen_exception_list(repository: Path) -> None:
    path = repository/"research/_scaffold/grandfathered.json"
    data = json.loads(path.read_text())
    data["trees"].append("probe")
    path.write_text(json.dumps(data))
    assert any("tree list differs from its fixed baseline" in f for f in contract.problems(repository))


def test_primed_name_is_retained_by_the_copied_parser(repository: Path) -> None:
    path = repository/"research/probe/verify.py"
    spec = importlib.util.spec_from_file_location("probe_verifier", path)
    assert spec and spec.loader
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    assert verifier.NO_AXIOMS.findall("'ResearchProbe.identity'' does not depend on any axioms") == ["ResearchProbe.identity'"]
    assert verifier.WITH_AXIOMS.findall("'ResearchProbe.identity'' depends on axioms: [propext]") == [("ResearchProbe.identity'", "propext")]


def test_generator_refuses_existing_or_traversing_names(repository: Path) -> None:
    for name in ("probe", "../escape"):
        result = subprocess.run([sys.executable, str(SCAFFOLD/"new_tree.py"), name, "--repo", str(repository)], capture_output=True, text=True)
        assert result.returncode == 1
    assert contract.problems(repository) == []



def test_native_pins_use_the_existing_lookup_index_path_convention(repository: Path) -> None:
    spec = importlib.util.spec_from_file_location("new_tree_pin_lookup", REPO/"ci/lookup_indexes.py")
    assert spec and spec.loader
    lookup = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lookup
    spec.loader.exec_module(lookup)
    paths = ["research/probe/SOURCE_MANIFEST.json", "research/probe/input.json", "research/probe/verify.py"]
    census = lookup.collect_pins(repository, paths)
    assert not census.problems
    assert {pin.path for pin in census.pins} == {"research/probe/input.json"}
