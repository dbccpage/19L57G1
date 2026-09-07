from __future__ import annotations

import pytest

from verify_lean import parse_reports


def test_report_parser_accepts_primed_theorem_names() -> None:
    assert parse_reports("'LocalReuse.cut\'' depends on axioms: [propext]",
                         "LOCAL_REUSE_THEOREM: LocalReuse.cut'") == {"LocalReuse.cut'": ["propext"]}


@pytest.mark.parametrize("log,census,reason", [
    ("", "", "empty"),
    ("", "LOCAL_REUSE_THEOREM: LocalReuse.cut", "missing"),
    ("'LocalReuse.other' does not depend on any axioms", "LOCAL_REUSE_THEOREM: LocalReuse.cut", "mismatch"),
    ("'LocalReuse.cut' depends on axioms: [Classical.choice]", "LOCAL_REUSE_THEOREM: LocalReuse.cut", "disallowed"),
    ("'LocalReuse.cut' does not depend on any axioms\n'LocalReuse.cut' does not depend on any axioms",
     "LOCAL_REUSE_THEOREM: LocalReuse.cut", "duplicate report"),
    ("'LocalReuse.cut' does not depend on any axioms",
     "LOCAL_REUSE_THEOREM: LocalReuse.cut\nLOCAL_REUSE_THEOREM: LocalReuse.cut", "duplicate environment"),
])
def test_incomplete_or_disallowed_proof_reports_fail(log: str, census: str, reason: str) -> None:
    with pytest.raises(ValueError, match=reason):
        parse_reports(log, census)
