"""Write the Challenge 2 receipt.  Deterministic: sorted keys, LF, no
timestamp, no environment value."""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "code"))

from boundary.challenge2 import build  # noqa: E402


def render() -> bytes:
    return (json.dumps(build(), indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    out = HERE / "receipts" / "challenge2.json"
    out.parent.mkdir(exist_ok=True)
    data = render()
    if out.exists() and out.read_bytes() == data:
        print(f"unchanged: {out.relative_to(HERE)} ({len(data)} bytes)")
        return 0
    out.write_bytes(data)
    print(f"wrote: {out.relative_to(HERE)} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
