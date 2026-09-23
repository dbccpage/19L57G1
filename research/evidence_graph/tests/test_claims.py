from eg_claims import context_heading, ledger_entries
from eg_sources import load_snapshot


def test_substantive_headline_is_not_discarded_as_context() -> None:
    assert context_heading("## Claims")
    assert not context_heading("# Every carrier has a unique successor")
    assert not context_heading("## Coherent higher structure is established")


def test_ids_survive_summary_and_detailed_statement_occurrences() -> None:
    snapshot = load_snapshot()
    entries = ledger_entries(snapshot, "research/genesis_continuation/claims.md")
    assert sum(row.public_id == "GC-1" for row in entries) == 2
    assert any(row.public_id == "C01" for row in ledger_entries(snapshot, "research/g013_trace_calculus/CLAIMS.md"))
