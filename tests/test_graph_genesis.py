"""Tests for the graph-genesis mirror.

Mirrors ``lean4/Derivation/GraphGenesis.lean``: the field-invariance
battery, the internal fragment's carrier invariance, the proposal
record's obligations, transport over the full permutation group, the
retained equal-cost tie, and the Part-3 non-entailment witness.
"""

from __future__ import annotations

from pathlib import Path

import run_graph_genesis
from derivation.attachment_ladder import up_family
from derivation.graph_genesis import (
    ALL_KINDS,
    GRAPH_FIELDS,
    INTERNAL_KINDS,
    OBLIGATION_KEYS,
    OBSERVATION_FIELDS,
    SUPPLY_KINDS,
    arg_json,
    blind_pair,
    block_json,
    block_shape,
    carries_no_authority,
    changed_fields,
    declared_columns,
    event_battery,
    event_json,
    family_report,
    field_invariance_report,
    graph_stores_fixed,
    in_carrier_resolution,
    internal_alphabet,
    internal_fragment_report,
    is_funding,
    is_internal,
    is_response_event,
    mentions_only_existing,
    part3_report,
    proposal_obligations,
    proposal_report,
    record_field_names,
    refinable,
    sample_states,
    separated_pairs,
    supply_stages,
    tie_report,
    transport_report,
    up_proposal,
)
from derivation.primitive_passage import (
    GENESIS_P,
    PS,
    next_family_p,
    obst_p,
    preplay,
    pstep,
)


def test_event_classification_is_exact() -> None:
    """``IsInternal`` is true exactly on the four internal kinds and
    false on every supply and control kind."""
    internal = [("refineCol", (0,), 1), ("addCol", (0,)),
                ("declareObs",), ("refuse", 0, 1)]
    external = [("admitOcc", 3), ("assertWit", 0, 1),
                ("admitWit", 0, 1), ("protect", 0, 1),
                ("setBudget", 1), ("setLicense", True), ("halt",)]
    assert all(is_internal(e) for e in internal)
    assert not any(is_internal(e) for e in external)
    assert all(is_response_event(e) for e in internal)
    assert is_funding(("setBudget", 2))
    assert not is_funding(("halt",))
    assert is_response_event(("setBudget", 1))
    assert not is_response_event(("admitOcc", 3))
    assert set(ALL_KINDS) == {e[0] for e in internal + external}


def test_field_invariance_battery() -> None:
    rep = field_invariance_report()
    assert rep["refineCol_only_obs"] is True
    assert rep["addCol_only_obs"] is True
    assert rep["internal_events_fix_graph_stores"] is True
    assert rep["response_events_fix_graph_stores"] is True
    assert rep["graph_fields_move_only_under_supply"] is True
    # non-vacuity: the graph stores really do move, under supply only
    assert rep["every_supply_kind_moves_a_graph_store"] is True
    touched = rep["fields_touched_by_kind"]
    assert isinstance(touched, dict)
    assert touched["refineCol"] == ["budget", "obs"]
    assert touched["addCol"] == ["budget", "obs"]
    assert touched["admitOcc"] == ["occ"]
    assert touched["assertWit"] == ["asserted"]
    assert touched["admitWit"] == ["wit"]
    assert touched["protect"] == ["prot"]
    assert touched["refuse"] == ["refusals"]
    assert touched["declareObs"] == ["obs"]
    assert set(OBSERVATION_FIELDS) == {"obs", "budget"}
    # a firing structural response moves exactly obs and budget
    s = blind_pair()
    funded = pstep(s, ("setBudget", 1))
    assert changed_fields(funded, pstep(funded, ("addCol", (0,)))) \
        == ("obs", "budget")
    # and a supply event moves a graph store (the negative control)
    assert changed_fields(s, pstep(s, ("admitOcc", 9))) == ("occ",)
    assert not graph_stores_fixed(s, pstep(s, ("admitOcc", 9)))
    assert graph_stores_fixed(s, funded)


def test_declared_columns_and_battery() -> None:
    # pre-observational: no declared columns to add
    assert declared_columns(PS(occ=(0, 1), obs=None)) \
        == ((), (0,), (1,), (0, 1))
    # a declared column outside the base universe is included
    wide = PS(occ=(0, 1), obs=((0, 1, 2),))
    assert declared_columns(wide)[-1] == (0, 1, 2)
    # an already-listed declared column is not duplicated
    assert declared_columns(PS(occ=(0, 1), obs=((0,),))) \
        == ((), (0,), (1,), (0, 1))
    battery = event_battery(PS(occ=(0, 1), obs=()))
    assert {e[0] for e in battery} == set(ALL_KINDS)
    # positions and tokens probe one past the carrier
    assert ("assertWit", 2, 2) in battery
    assert ("admitOcc", 3) in battery
    assert len(event_battery(GENESIS_P)) == len(
        event_battery(GENESIS_P, 1))


def test_internal_fragment_cannot_grow_carrier() -> None:
    rep = internal_fragment_report(2)
    assert rep["all_graph_stores_fixed"] is True
    assert isinstance(rep["traces_checked"], int)
    assert rep["traces_checked"] > 1000
    assert rep["max_trace_length"] == 2
    # every event of the enumerated alphabet is internal
    for _, s in sample_states():
        assert all(is_internal(e) for e in internal_alphabet(s))
    # a longer hand-built internal trace on the witness state
    s = blind_pair()
    trace = [("setBudget", 1), ("addCol", (0,))]
    del trace[0]  # keep the internal event only
    long_trace = [("declareObs",), ("refuse", 0, 1)] + trace * 3
    t = preplay(long_trace, s)
    assert graph_stores_fixed(s, t)
    assert t.refusals == ((0, 1),)


def test_family_shape_range_and_invariance() -> None:
    rep = family_report()
    assert rep["every_block_has_a_declared_shape"] is True
    assert rep["family_ranges_over_existing_carrier"] is True
    assert rep["family_blocks_are_response_events"] is True
    assert rep["family_blocks_fix_graph_stores"] is True
    shapes = rep["block_shapes"]
    assert isinstance(shapes, dict)
    assert shapes["other"] == 0
    assert shapes["repair"] >= 1        # the refinable sample
    assert shapes["funded_extension"] >= 1
    # the third shape exists only outside the family
    assert block_shape((("halt",),)) == "other"
    assert block_shape((("setBudget", 1), ("halt",))) == "other"
    assert block_shape((("refineCol", (0,), 2),)) == "repair"
    assert block_shape((("setBudget", 1), ("addCol", (0,)))) \
        == "funded_extension"
    # the range predicate, on each of its three branches
    s = refinable()
    assert mentions_only_existing(s, ("refineCol", (0,), 2))
    assert not mentions_only_existing(s, ("refineCol", (0,), 7))
    assert mentions_only_existing(s, ("addCol", (0, 1)))
    assert not mentions_only_existing(s, ("addCol", (0, 9)))
    assert mentions_only_existing(s, ("setBudget", 1))
    # the repair block really is emitted by the refinable state
    assert (("refineCol", (0,), 2),) in next_family_p(s)


def test_proposal_record_obligations() -> None:
    rep = proposal_report()
    assert rep["all_obligations_discharged"] is True
    assert rep["carries_no_authority_field"] is True
    assert rep["execution_is_separately_gated"] is True
    assert rep["record_fields"] == [
        "block", "embed", "retract", "new_pair", "parent_pos",
        "fresh_pos", "cost"]
    assert carries_no_authority()
    assert "licensed" not in record_field_names()
    s = refinable()
    rec = up_proposal(s, 1)
    assert rec.block[0] == ("admitOcc", 3)
    assert rec.new_pair == (1, 3)
    assert rec.parent_pos == 1
    assert rec.fresh_pos == 3
    assert rec.cost == 4
    checks = proposal_obligations(s, rec)
    for key in OBLIGATION_KEYS:
        assert checks[key] is True, key
    assert checks["complete_family_retained_alongside_named_branch"] \
        is True
    # The record names one branch.  Membership does not make it the
    # canonical or unique branch: a distinct parent-indexed proposal
    # remains in the same complete family.
    other = up_proposal(s, 2)
    assert rec.block != other.block
    assert list(rec.block) in up_family(s)
    assert list(other.block) in up_family(s)
    assert checks["separated_pairs_before"] == 4
    assert checks["separated_pairs_after"] == 6
    # the separated-pair set is empty exactly pre-observationally
    assert separated_pairs(None, 3) == set()
    assert separated_pairs(((0,),), 2) == {(0, 1), (1, 0)}
    # a proposal on a terminal state exists and executes to nothing
    halted = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
                prot=((0, 1),), obs=(), budget=2, halted=True)
    inert = up_proposal(halted, 0)
    assert preplay(list(inert.block), halted) == halted
    for key in OBLIGATION_KEYS:
        assert proposal_obligations(halted, inert)[key] is True, key


def test_transport_over_full_permutation_group() -> None:
    rep = transport_report(3)
    assert rep["permutation_group_size"] == 6
    assert rep["checks"] == 18
    assert rep["act_up_comm_all_perms"] is True
    assert rep["transported_block_is_complete_member"] is True
    assert rep["cost_invariant_under_renaming"] is True
    assert rep["transported_obligations_discharged"] is True
    # a smaller carrier still transports over its full group
    small = transport_report(2)
    assert small["permutation_group_size"] == 2
    assert small["act_up_comm_all_perms"] is True


def test_equal_cost_tie_is_retained() -> None:
    rep = tie_report()
    assert rep["equal_cost"] is True
    assert rep["blocks_differ"] is True
    assert rep["both_complete_members"] is True
    assert rep["executions_non_isomorphic"] is True
    assert rep["family_size_equals_parent_count"] is True
    assert rep["cost"] == 4
    assert rep["left_edges"] == [[0, 1], [1, 2], [1, 3]]
    assert rep["right_edges"] == [[0, 1], [1, 2], [2, 3]]


def test_part3_obstruction_does_not_request_the_lift() -> None:
    rep = part3_report()
    conditions = rep["four_conditions"]
    assert isinstance(conditions, dict)
    assert conditions["retained"] is True
    assert conditions["protected"] is True
    assert conditions["observation_declared"] is True
    assert conditions["observer_zero_on_the_pair"] is True
    assert conditions["all_four"] is True
    assert rep["family_nonempty"] is True
    assert rep["complete_family"] == [
        [["setBudget", 1], ["addCol", [0]]],
        [["setBudget", 1], ["addCol", [1]]]]
    assert rep["every_response_resolves"] is True
    assert rep["every_response_fixes_graph_stores"] is True
    assert rep["no_response_grows_the_carrier"] is True
    assert rep["every_obstruction_resolved_in_carrier"] is True
    assert rep["obstructions_meeting_the_hypotheses"] == 2
    assert "not entailed by nextFamilyP" in str(rep["verdict"])
    # the witness resolves in carrier, decided directly
    s = blind_pair()
    t = preplay((("setBudget", 1), ("addCol", (0,))), s)
    assert obst_p(s, 0, 1) and not obst_p(t, 0, 1)
    assert t.occ == s.occ and t.wit == s.wit
    assert t.obs == ((0,),)
    # the terminal state fails the hypotheses and is not resolved
    halted = PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
                prot=((0, 1),), obs=(), budget=2, halted=True)
    row = in_carrier_resolution(halted, 0, 1)
    assert row["hypotheses_hold"] is False
    assert row["obstructed_after"] is True
    assert row["resolved_in_carrier"] is False
    assert row["graph_stores_fixed"] is True


def test_json_helpers() -> None:
    assert arg_json((0, 1)) == [0, 1]
    assert arg_json(3) == 3
    assert arg_json(True) is True
    assert event_json(("setLicense", False)) == ["setLicense", False]
    assert event_json(("halt",)) == ["halt"]
    assert block_json((("setBudget", 1), ("addCol", (2,)))) == [
        ["setBudget", 1], ["addCol", [2]]]


def test_declared_vocabulary() -> None:
    assert GRAPH_FIELDS == ("occ", "asserted", "wit", "prot")
    assert set(INTERNAL_KINDS) & set(SUPPLY_KINDS) == set()
    names = [n for n, _ in sample_states()]
    assert names == ["genesis", "pre_observational", "blind_pair",
                     "separated_pair", "refinable", "supply_stages",
                     "path3", "terminal"]
    # the mid-supply sample really has both supply events live
    s = supply_stages()
    assert pstep(s, ("admitWit", 0, 1)).wit == ((1, 2), (0, 1))
    assert pstep(s, ("protect", 1, 2)).prot == ((1, 2),)


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_graph_genesis.main(
        ["--artifacts", str(d1), "--trace-len", "1",
         "--carrier", "3", "--probe", "1"]) == 0
    assert run_graph_genesis.main(
        ["--artifacts", str(d2), "--trace-len", "1",
         "--carrier", "3", "--probe", "1"]) == 0
    assert (d1 / "graph_genesis.json").read_bytes() == \
        (d2 / "graph_genesis.json").read_bytes()
