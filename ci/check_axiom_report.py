"""Compare the freshly built axiom reports against the committed artifact.

Usage: python ci/check_axiom_report.py <lake-build-log>
"""

import pathlib
import re
import sys


def normalize(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        m = re.search(
            r"'(?P<name>.+?)' (?P<rest>(depends on axioms: "
            r"\[[^\]]*\]|does not depend on any axioms))",
            line,
        )
        if m:
            out.append(f"{m.group('name')}: {m.group('rest')}")
    return sorted(out)


def main() -> int:
    fresh = normalize(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    committed = normalize(
        pathlib.Path("artifacts/lean_axioms.txt").read_text(encoding="utf-8")
    )
    if not committed:
        print("FAIL: committed axiom report is empty")
        return 1
    if committed != fresh:
        print("FAIL: axiom reports differ between CI build and artifact")
        for line in sorted(set(committed) ^ set(fresh)):
            print(f"  delta: {line}")
        return 1
    print(f"axiom reports match ({len(committed)} theorems)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
