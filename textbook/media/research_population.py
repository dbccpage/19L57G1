"""Research population owned by the canonical source index.

AuthorityEffect: None. Presence of files is not validation of their claims.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

SOURCE_ROOT = Path(__file__).resolve().parents[2]
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from ci.research_index import group_trees, tracked_research_files  # noqa: E402


def research_trees(repo_root: Path) -> list[tuple[str, bool, bool]]:
    """Use tracked paths and the canonical exclusions, including markerless trees."""
    grouped = group_trees(tracked_research_files(repo_root))
    return [
        (name, "TREE_CONTRACT.json" in paths,
         any(path.endswith(".lean") and Path(path).name != "lakefile.lean" for path in paths))
        for name, paths in grouped.items()
    ]


def inventory_errors(repo_root: Path, text: str) -> list[str]:
    """Compare actual table rows with the canonical population, in both directions."""
    expected = {name for name, _, _ in research_trees(repo_root)}
    listed = set(re.findall(r"^\|\s*\[`research/([^/`]+)/`\]\(", text, re.MULTILINE))
    return ([f"missing research tree: {name}" for name in sorted(expected - listed)] +
            [f"unexpected research tree: {name}" for name in sorted(listed - expected)])
