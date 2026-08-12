"""Tests for the Frontier Run 006 protocol search."""

from __future__ import annotations

import json
from pathlib import Path

from derivation.refusal_frontier import (
    EMPTY_F,
    Proto,
    cost_a,
    cost_b,
    enumerate_protocols,
    minimum_table,
    normal_form_check,
    notion_matrix,
    notions,
    oriented_two,
    protocol_report,
    reachable_f,
    step_f,
    swap_first_two,
)

import run_refusal_frontier


def test_protocol_space_size_and_validity() -> None:
    protos = enumerate_protocols()
    assert len(protos) == 44
    assert all(p.valid() for p in protos)
    assert not Proto(1, "judgment", True, False, False, 1).valid()
    assert not Proto(3, "none", False, False, False, 1).valid()


def test_silent_protocol_is_inert() -> None:
    p = Proto(1, "none", False, False, False, 1)
    rep = protocol_report(p, 6)
    assert rep["max_carrier"] == 1
    mins = rep["min_events_to"]
    assert mins["two_carrier"] is None
    assert mins["separable_pair"] is None
    assert rep["dynamics"] == "fixpoint"


def test_tag_route_reaches_oriented_pair_at_two_events() -> None:
    p = Proto(1, "datum", True, False, False, 1)
    mins = protocol_report(p, 6)["min_events_to"]
    assert mins["two_carrier"] == 2
    assert mins["separable_pair"] == 2
    assert mins["oriented_pair"] == 2
    assert mins["witnessed_relation"] is None  # no relation rule


def test_relation_route_reaches_witnessed_irreflexive() -> None:
    p = Proto(1, "datum", False, False, True, 1)
    mins = protocol_report(p, 6)["min_events_to"]
    assert mins["witnessed_relation"] == 2
    assert mins["witnessed_irreflexive"] == 2
    assert mins["oriented_pair"] == 2


def test_judgment_protocol_two_states_only() -> None:
    p = Proto(2, "judgment", False, False, False, 1)
    rep = protocol_report(p, 6)
    assert rep["max_carrier"] == 1
    mins = rep["min_events_to"]
    assert mins["two_carrier"] is None
    assert mins["two_judgments"] == 3
    assert mins["two_result_constructors"] == 2


def test_reflection_grows_to_cap() -> None:
    p = Proto(1, "datum", True, True, True, 1)
    rep = protocol_report(p, 6)
    assert rep["dynamics"] == "growth_to_cap"
    assert rep["max_carrier"] == 4
    assert rep["two_event_classes"] is True


def test_refusal_links_are_born_irreflexive_in_class() -> None:
    """Structural fact of the class: a receipt is always fresh, so no
    refusal link is a self-edge — witnessed implies irreflexive-as-fact
    within this protocol space."""
    for p in enumerate_protocols():
        for s in reachable_f(p, 5):
            assert all(a != b for (a, b) in s.rel)


def test_swap_and_orientation() -> None:
    p = Proto(1, "datum", True, False, False, 1)
    s = step_f(
        p, step_f(p, EMPTY_F, ("present", "<>")), ("present", "<>")
    )
    assert len(s.data) == 2
    assert oriented_two(s)
    assert swap_first_two(s) != s
    q = Proto(1, "occurrence", False, False, False, 1)
    t = step_f(
        q, step_f(q, EMPTY_F, ("present", "<>")), ("present", "<>")
    )
    assert swap_first_two(t) == t
    assert not oriented_two(t)
    assert notions(t)["two_occurrences"]


def test_minimum_table_ties_and_disagreement() -> None:
    mt = minimum_table(5)
    a_sep = mt["A_total_imports"]["separable_pair"]
    assert isinstance(a_sep, dict)
    assert a_sep["cost"] == 2 and len(a_sep["tied_minima"]) == 2
    b_sep = mt["B_lex"]["separable_pair"]
    assert isinstance(b_sep, dict)
    assert len(b_sep["tied_minima"]) == 1
    assert b_sep["tied_minima"][0]["tagging"] is True
    a_two = mt["A_total_imports"]["two_carrier"]
    assert isinstance(a_two, dict)
    assert len(a_two["tied_minima"]) == 3  # token, occurrence, reify
    assert cost_a(Proto(1, "none", False, False, False, 1)) == 0
    assert cost_b(Proto(1, "none", False, False, False, 2)) == (1, 0, 0)


def test_witnessed_minimum_unique_under_both_orders() -> None:
    """The witnessed milestones have a single minimum protocol, and it
    is the same one under both cost orders: datum retention + the
    relation rule, no tag, singleton algebra, one token.  The multiple
    minima live only at the weaker milestones."""
    mt = minimum_table(5)
    for order in ("A_total_imports", "B_lex"):
        for milestone in ("witnessed_relation", "witnessed_irreflexive"):
            cell = mt[order][milestone]
            assert isinstance(cell, dict)
            ties = cell["tied_minima"]
            assert len(ties) == 1
            only = ties[0]
            assert only["retention"] == "datum"
            assert only["autorel"] is True
            assert only["tagging"] is False
            assert only["algebra"] == 1
            assert only["tokens"] == 1
            assert only["reflection"] is False


def test_normal_form_holds() -> None:
    nf = normal_form_check(5)
    assert nf["normal_form_holds_in_class"] is True
    assert nf["all_made_a_purchase"] is True
    assert nf["violations"] == []
    assert nf["witnessed_without_relation_rule"] == []
    assert nf["carrier2_without_reify_occurrence_or_second_token"] == []
    # Target-relative channel checks: carrier separability needs a tag
    # or a relation; result-outcome distinction needs the binary
    # algebra.  Zero exceptions in class.
    assert nf["separable_without_tag_or_relation"] == []
    assert nf["oriented_without_tag_or_relation"] == []
    assert nf["result_distinction_without_binary_algebra"] == []


def test_notion_matrix_declares_state_level_scope() -> None:
    m = notion_matrix(4)
    keys = m["state_level_notions"]
    assert isinstance(keys, list)
    assert len(keys) == 9  # nine state-level notions, 72 directed cells
    imp = m["implications"]
    assert isinstance(imp, dict)
    assert len(imp) == 81  # 9 x 9 including reflexive diagonal
    sep = m["separately_reported"]
    assert isinstance(sep, list)
    assert any("two_histories" in row for row in sep)
    assert any("oriented" in row for row in sep)


def test_notion_matrix_key_cells() -> None:
    m = notion_matrix(4)
    imp = m["implications"]
    assert isinstance(imp, dict)
    assert imp["witnessed_irreflexive->separable_pair"] is True
    assert imp["witnessed_relation->witnessed_irreflexive"] is True
    assert imp["two_carrier->separable_pair"] is False
    assert imp["separable_pair->two_result_constructors"] is False
    assert imp["two_result_constructors->two_carrier"] is False
    cms = m["countermodels"]
    assert isinstance(cms, dict)
    assert "two_carrier->separable_pair" in cms


def test_run_main(tmp_path: Path) -> None:
    out = tmp_path / "artifacts"
    assert run_refusal_frontier.main(
        ["--artifacts", str(out), "--max-events", "4"]
    ) == 0
    payload = json.loads(
        (out / "refusal_frontier.json").read_text(encoding="utf-8")
    )
    assert payload["protocol_space_size"] == 44
    assert payload["normal_form"]["normal_form_holds_in_class"] is True
    out2 = tmp_path / "artifacts2"
    run_refusal_frontier.main(
        ["--artifacts", str(out2), "--max-events", "4"]
    )
    assert (out / "refusal_frontier.json").read_bytes() == (
        out2 / "refusal_frontier.json"
    ).read_bytes()
