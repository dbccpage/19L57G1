"""Independent checker custody and entry-point controls."""
from typing import Any

import pytest

from eg_inventory import declared_options, require_local_verifier


def test_subcommand_mention_is_not_an_own_option() -> None:
    source = 'STEPS = [("python", "another.py", "--check")]\np.add_argument("--report")\n'
    assert declared_options(source) == {"--report"}


def test_shared_helper_cannot_replace_tree_checker() -> None:
    tree: dict[str, Any] = {"name": "example", "verifier_commands": [
        {"argv": ["python", "verify.py", "--check"], "cwd": "research/example", "source": {"path": "research/example/verify.py"}}
    ]}
    assert require_local_verifier(tree, ["python", "verify.py", "--check"], "research/example")
    with pytest.raises(ValueError, match="INDEPENDENT_VERIFIER_SUBSTITUTED"):
        require_local_verifier(tree, ["python", "common.py", "--all"], "research")
    tree["verifier_commands"][0]["source"]["path"] = "research/common.py"
    with pytest.raises(ValueError, match="INDEPENDENT_VERIFIER_ORIGIN"):
        require_local_verifier(tree, ["python", "verify.py", "--check"], "research/example")
