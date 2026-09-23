"""Read the tree's pinned seed input. AuthorityEffect: None."""
import json
from pathlib import Path


def value() -> int:
    result = json.loads((Path(__file__).resolve().parent / "input.json").read_text(encoding="utf-8"))
    if not isinstance(result, int) or isinstance(result, bool):
        raise ValueError("input.json must contain an integer")
    return result
