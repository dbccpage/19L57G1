"""Shared apparatus for the S9-obligations research tree.

A receipt writer with the tree's byte convention, a write-root guard, the
pinned identifiers every receipt records, and a relation renderer.
Nothing here computes a result or decides a claim.  AuthorityEffect: None.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

TREE = Path(__file__).resolve().parent
REPO = TREE.parents[1]
TREE_RELATIVE = "research/s9_obligations"

# PROMPT.md step 1: the governing prompt's Git blob id and the snapshot
# commit, recorded in every receipt.  verify_pins.py checks both at HEAD.
PROMPT_PATH = "research/s9_obligations/PROMPT.md"
PROMPT_BLOB_ID = "1642e3f6ac746002678e4997f738e0fabd1248c9"
SNAPSHOT_COMMIT = "db1d2b225b577d5212780ff02700efd693c8e446"


def receipt_header() -> dict[str, str]:
    """The identifiers every receipt carries (PROMPT.md step 1)."""

    return {
        "prompt_path": PROMPT_PATH,
        "prompt_blob_id": PROMPT_BLOB_ID,
        "snapshot_commit": SNAPSHOT_COMMIT,
    }


def assert_inside_tree(path: str | Path) -> Path:
    """Resolve ``path`` and refuse it unless it lies under this tree.

    The write root is ``research/s9_obligations/`` (PROMPT.md step 2).
    Every part calls this before writing anything.
    """

    resolved = Path(path).resolve()
    if not resolved.is_relative_to(TREE):
        raise ValueError(f"refusing to write outside {TREE_RELATIVE}/: {path}")
    return resolved


def receipt_bytes(obj: object) -> bytes:
    """The receipt convention: indent 2, sorted keys, ASCII, one trailing LF."""

    return (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode(
        "ascii"
    )


def write_receipt(path: str | Path, obj: object) -> Path:
    """Write ``obj`` as a receipt at ``path`` (inside the tree), LF only."""

    target = assert_inside_tree(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(receipt_bytes(obj).decode("ascii"))
    return target


def render_relation(rel: Iterable[tuple[int, int]]) -> list[list[int]]:
    """Render a relation given as pairs as a sorted list without duplicates."""

    return [[x, y] for x, y in sorted(set(rel))]
