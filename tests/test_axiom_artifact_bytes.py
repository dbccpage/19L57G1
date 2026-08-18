"""Byte-level discipline for ``artifacts/lean_axioms.txt``.

PR #20 rewrote this artifact wholesale from LF to CRLF.  Nothing caught it:
``.gitattributes`` marks ``artifacts/** -text`` so the CRLF bytes were
committed verbatim, ``ci/compare_artifacts.py`` only compares ``*.json`` and
``full/*.json.gz``, and the two receipts bind DIFFERENT byte domains --
``completion_receipt.axiom_report_sha256`` hashes the raw bytes while
``primitive_completion_receipt`` hashes the LF-canonicalized bytes.  The flip
therefore moved one recorded hash and not the other, and no gate compared them.

These tests bind the gap directly: the artifact is LF-only, and the raw and
canonical hashes coincide (which is true exactly when it is LF-only), so the
two receipts can never again describe different bytes.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AXIOMS = REPO / "artifacts" / "lean_axioms.txt"
COMPLETION_RECEIPT = REPO / "artifacts" / "completion_receipt.json"
PRIMITIVE_RECEIPT = REPO / "artifacts" / "primitive_completion_receipt.json"

# Non-greedy name capture: primed theorem names end in a quote and the
# blind [^']+ pattern cannot parse their reports (found live 2026-08-18).
REPORT = re.compile(
    r"'(?P<name>.+?)' (?:depends on axioms: \[[^\]]*\]|does not depend on any axioms)"
)
ALLOWED_AXIOMS = {"propext", "Quot.sound"}


def _raw() -> bytes:
    return AXIOMS.read_bytes()


def test_artifact_has_no_crlf() -> None:
    """No CR anywhere: the artifact is LF-only in the commit."""
    assert b"\r" not in _raw()


def test_artifact_ends_with_single_newline() -> None:
    raw = _raw()
    assert raw.endswith(b"\n")
    assert not raw.endswith(b"\n\n")


def test_raw_and_canonical_hashes_agree() -> None:
    """Raw bytes and LF-canonicalized bytes hash the same.

    This is the invariant the two receipts silently disagreed about.  It holds
    exactly when the file contains no CRLF, so it fails loudly on a reflip.
    """
    raw = _raw()
    canonical = raw.replace(b"\r\n", b"\n")
    assert hashlib.sha256(raw).hexdigest() == hashlib.sha256(canonical).hexdigest()


def test_both_receipts_bind_the_same_bytes() -> None:
    """Both recorded hashes equal the artifact's actual hash."""
    import json

    actual = hashlib.sha256(_raw()).hexdigest()
    completion = json.loads(COMPLETION_RECEIPT.read_text(encoding="utf-8"))
    primitive = json.loads(PRIMITIVE_RECEIPT.read_text(encoding="utf-8"))
    assert completion["axiom_report_sha256"] == actual
    assert primitive["axiom_report"]["sha256_canonical"] == actual


def test_theorem_counts_agree_with_the_artifact() -> None:
    import json

    lines = [
        ln for ln in AXIOMS.read_text(encoding="utf-8").splitlines()
        if REPORT.search(ln) is not None
    ]
    completion = json.loads(COMPLETION_RECEIPT.read_text(encoding="utf-8"))
    primitive = json.loads(PRIMITIVE_RECEIPT.read_text(encoding="utf-8"))
    assert completion["theorem_count"] == len(lines)
    assert primitive["axiom_report"]["theorem_count"] == len(lines)


def test_every_report_stays_within_the_allowed_axioms() -> None:
    for line in AXIOMS.read_text(encoding="utf-8").splitlines():
        if "depends on axioms:" not in line:
            continue
        inside = line.split("[", 1)[1].split("]", 1)[0]
        used = {tok.strip() for tok in inside.split(",") if tok.strip()}
        assert used <= ALLOWED_AXIOMS, f"unexpected axiom in: {line}"
