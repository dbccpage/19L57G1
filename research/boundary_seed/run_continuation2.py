"""Write the deterministic stage-2 receipt, with explicit replay available."""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "code"))
from boundary.continuation2 import build, render  # noqa: E402


def main() -> int:
    out = HERE / "receipts" / "continuation2.json"
    data = render(build())
    if out.exists() and out.read_bytes() == data:
        print(f"unchanged: {out.relative_to(HERE)} ({len(data)} bytes)")
        return 0
    out.write_bytes(data)
    print(f"wrote: {out.relative_to(HERE)} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
