"""Bind all published result prose byte-for-byte to a fresh computation."""

from __future__ import annotations

from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "code"))

from typed_translation.report import build_receipt, rendered_prose  # noqa: E402


def main() -> int:
    expected = rendered_prose(build_receipt())
    problems: list[str] = []
    for name, text in expected.items():
        path = HERE / name
        if not path.is_file():
            problems.append(f"{name} is missing")
        elif path.read_bytes() != text.encode("utf-8"):
            problems.append(f"{name} differs from the fresh receipt rendering")
    for problem in problems:
        print(f"FAIL: {problem}")
    if problems:
        return 1
    print(f"prose ok: {len(expected)} rendered documents match the fresh computation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
