"""Prompt byte-identity gate.

Pinned to the repository-canonical bytes (what any clone checks out;
``prompt/**`` carries ``-text`` so no smudge filter applies).
``prompt/prompt.md`` is byte-identical to the original input in both the
working tree and the repository.  ``prompt/seed_prompt.md`` was
line-ending-normalized once at the original staging; the original
working-tree hash is recorded alongside for the paper's provenance table.
"""

import hashlib
import sys

ACCEPTED = {
    # repository-canonical bytes only: this file's byte-identity mandate
    # holds in both the working tree and the repository
    "prompt/prompt.md": {
        "a613a1965e4f02fee00df4d42041fceeca176abcfaa9202c3e769021305940b5",
    },
    # original supplied bytes (CRLF) and repository-canonical bytes (LF;
    # normalized once at the original staging, before prompt/** -text)
    "prompt/seed_prompt.md": {
        "ee3ba0583fea2a11f1294538c912c542b3faee5316355dc226efb92ef64646ab",
        "4ea4682e1da25363f9c7c1e9234b4b248f980097ae92d6f7dc1e8e8dd9bd4388",
    },
}


def main() -> int:
    ok = True
    for path, wanted in ACCEPTED.items():
        got = hashlib.sha256(open(path, "rb").read()).hexdigest()
        status = "ok" if got in wanted else "MISMATCH"
        if got not in wanted:
            ok = False
        print(f"{status}: {path} sha256={got}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
