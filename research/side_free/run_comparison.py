"""Write the price-list comparison: the receipt and the document it renders.

Deterministic: sorted keys, LF only, no timestamp, no environment value, and
byte-identical on regeneration.  ``--check`` compares without writing.

The reachability of the pinned commit is printed HERE and is deliberately not
written into the receipt: a record that carried it would not be the same file
in a clone that cannot reach that commit.  It is never silent -- the line
below says PASS or SKIPPED and gives the reason.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from comparison import (  # noqa: E402
    COMPARISON_DOC,
    COMPARISON_RECEIPT,
    Load,
    compare,
    declare_values,
    document,
    load_pinned,
    manifest,
    render,
    vendored_receipts,
)

HERE = pathlib.Path(__file__).resolve().parent
LIMIT = 1_000_000


def reachability() -> list[Load]:
    commit = str(manifest()["pinned_commit"])
    return [load_pinned(row, commit) for row in vendored_receipts()]


def report_reachability(loads: list[Load]) -> None:
    """Never silent: one line per pinned receipt, PASS or SKIPPED with why."""
    for load in loads:
        status = "PASS" if load.source == "the pinned commit" else "SKIPPED"
        print(f"pin challenge {load.challenge}: {status} -- {load.reason}")


def main(argv: list[str]) -> int:
    report_reachability(reachability())
    if "--declare" in argv:
        count = declare_values()
        print(
            f"declared {count} pinned values into pinned/BOUNDARY_PIN.json from "
            f"the vendored bytes.  This is a DELIBERATE snapshot: never run it "
            f"while an injection is live, or the injected value becomes the "
            f"baseline and gate C1 is destroyed"
        )
        return 0
    record = compare()
    if record["void"]:
        print("FAIL: the comparison is VOID and NO difference is reported")
        problems = record.get("problems")
        for problem in problems if isinstance(problems, list) else []:
            print(f"FAIL: {problem}")
        return 1
    payload = render(record)
    page = document(record)
    if len(payload) > LIMIT:
        print(
            f"FAIL: the receipt is {len(payload)} bytes, over the {LIMIT} byte "
            f"bound; split it into a summary plus a hashed archive"
        )
        return 1
    if "--check" in argv:
        for path, wanted in ((COMPARISON_RECEIPT, payload), (COMPARISON_DOC, page)):
            name = path.relative_to(HERE).as_posix()
            if not path.exists():
                print(f"FAIL: {name} is missing")
                return 1
            if path.read_bytes() != wanted:
                print(f"FAIL: {name} differs from a fresh computation")
                return 1
        print(
            f"comparison ok: {len(payload)} receipt bytes and {len(page)} "
            f"document bytes, byte-identical"
        )
        return 0
    COMPARISON_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    COMPARISON_RECEIPT.write_bytes(payload)
    COMPARISON_DOC.write_bytes(page)
    print(f"wrote receipts/comparison.json: {len(payload)} bytes")
    print(f"wrote COMPARISON.md: {len(page)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
