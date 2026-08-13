"""Tests for the trace-algebra mirror.

Every law is tested together with the countermodel that bounds it: the
frame conditions with the pairs that do not commute, the rewrite system
with the equation it cannot derive, replay equivalence with its
unscoped countermodel, and the internal-trace theorems with the budget
write the internal generator does emit.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import run_trace_algebra
from derivation.primitive_passage import GENESIS_P, PS, preplay, pstep
from derivation.trace_algebra import (
    BUDGET_INSENSITIVE,
    LICENSE_INSENSITIVE,
    OCC_INSENSITIVE,
    REWRITE_ALPHABET,
    TRecord,
    aligned,
    build_trace,
    comm_states,
    commutation_report,
    cons_nf,
    end_state,
    erase_trace,
    frame_report,
    funded_state,
    identity_report,
    internal_report,
    legal_trace,
    list_battery,
    make_record,
    named_states,
    nf,
    no_redex,
    normal_forms,
    obstructed_state,
    one_occurrence_state,
    post_of,
    refine_state,
    rewrite_report,
    rw_reducts,
    scoping_report,
    step_by_normal_form,
    trace_report,
    wf_record,
)
from derivation.transition_alphabet import (
    EVENT_BATTERY,
    accepted,
    enumerate_states,
)

HALT: tuple[object, ...] = ("halt",)
A: tuple[object, ...] = ("admitOcc", 0)
B: tuple[object, ...] = ("setBudget", 1)


def test_post_of_and_step_normal_form() -> None:
    for s in named_states():
        for e in EVENT_BATTERY:
            assert step_by_normal_form(s, e) == pstep(s, e)
    # the two observation events have no post-state before declaration
    assert post_of(GENESIS_P, ("refineCol", (), 0)) == GENESIS_P
    assert post_of(GENESIS_P, ("addCol", (0,))) == GENESIS_P
    assert post_of(GENESIS_P, ("declareObs",)).obs == ()
    assert post_of(GENESIS_P, ("assertWit", 0, 1)).asserted == ((0, 1),)
    assert post_of(GENESIS_P, ("admitWit", 0, 1)).wit == ((0, 1),)
    assert post_of(GENESIS_P, ("protect", 0, 1)).prot == ((0, 1),)
    assert post_of(GENESIS_P, ("refuse", 0, 1)).refusals == ((0, 1),)
    assert post_of(GENESIS_P, ("setLicense", False)).licensed is False
    assert post_of(GENESIS_P, ("setBudget", 2)).budget == 2
    assert post_of(GENESIS_P, HALT).halted is True
    assert post_of(refine_state(), ("refineCol", (), 0)).obs == ((0,),)
    assert post_of(funded_state(), ("addCol", (0,))).obs == ((0,),)


def test_identity_laws_hold_everywhere() -> None:
    rep = identity_report()
    assert rep["step_normal_form_failures"] == 0
    assert rep["idempotence_failures"] == 0
    assert rep["inertness_criterion_failures"] == 0
    assert rep["terminal_absorption_failures"] == 0
    assert rep["every_event_idempotent"] is True


def test_typed_records_and_legal_traces() -> None:
    rep = trace_report()
    assert rep["legal_trace"] is True
    assert rep["replay_erases"] is True
    assert rep["raw_history_same_end_state"] is True
    assert rep["refused_attempts"] == 2
    tr = build_trace(GENESIS_P, (("admitOcc", 0), ("admitOcc", 0)))
    assert len(tr) == 1
    assert wf_record(tr[0])
    assert legal_trace(GENESIS_P, tr)
    assert end_state(GENESIS_P, ()) == GENESIS_P
    assert erase_trace(tr) == [("admitOcc", 0)]
    # a record whose fields are not the computed ones is not well formed
    bad = replace(tr[0], cls="writeBudget")
    assert not wf_record(bad)
    assert not legal_trace(GENESIS_P, (bad,))
    # a record chain that does not start where it claims is not aligned
    assert not aligned(PS(occ=(9,)), tr)
    detached = TRecord(pre=GENESIS_P, ev=A, guard="occurrenceFresh",
                       post=GENESIS_P, cls="supplyOccurrence",
                       spend="unchanged")
    assert not aligned(GENESIS_P, (detached,))
    assert not wf_record(detached)
    # an unaccepted attempt is not a record
    assert build_trace(GENESIS_P, (("protect", 0, 1),)) == ()
    assert make_record(GENESIS_P, A).cls == "supplyOccurrence"


def test_commutation_matrix_and_countermodels() -> None:
    rep = commutation_report()
    failing = rep["non_commuting_pairs"]
    commuting = rep["commuting_pairs"]
    assert isinstance(failing, list) and isinstance(commuting, list)
    assert len(failing) > 0 and len(commuting) > 0
    assert rep["unordered_pairs"] == len(failing) + len(commuting)
    # the declared frame pairs really do commute, everywhere
    funded = funded_state()
    assert (pstep(pstep(funded, ("setBudget", 1)), ("setLicense", False))
            == pstep(pstep(funded, ("setLicense", False)),
                     ("setBudget", 1)))
    # …and the five countermodels
    assert (pstep(pstep(funded, ("setLicense", False)), ("addCol", (0,)))
            != pstep(pstep(funded, ("addCol", (0,))),
                     ("setLicense", False)))
    assert (pstep(pstep(funded, ("setBudget", 0)), ("addCol", (0,)))
            != pstep(pstep(funded, ("addCol", (0,))), ("setBudget", 0)))
    assert (pstep(pstep(GENESIS_P, HALT), ("setLicense", False))
            != pstep(pstep(GENESIS_P, ("setLicense", False)), HALT))
    one = one_occurrence_state()
    assert (pstep(pstep(one, ("admitOcc", 6)), ("admitWit", 0, 1))
            != pstep(pstep(one, ("admitWit", 0, 1)), ("admitOcc", 6)))
    two = PS(occ=(0, 1))
    left = pstep(pstep(two, ("assertWit", 0, 1)), ("assertWit", 1, 0))
    right = pstep(pstep(two, ("assertWit", 1, 0)), ("assertWit", 0, 1))
    assert left != right
    # presentation differs, membership does not: never conflated
    assert set(left.asserted) == set(right.asserted)


def test_frames_are_sound_and_tight() -> None:
    rep = frame_report()
    assert rep["frames_violated"] == 0
    assert rep["frames_verified"] == (
        len(LICENSE_INSENSITIVE) + len(BUDGET_INSENSITIVE)
        + len(OCC_INSENSITIVE))
    failing = rep["excluded_and_really_failing"]
    framing = rep["excluded_but_actually_framing"]
    assert isinstance(failing, list) and isinstance(framing, list)
    assert "license:addCol" in failing
    assert "budget:refineCol" in failing
    assert "occurrence:admitWit" in failing
    # the terminal frames one-sidedly and is still excluded, with a reason
    assert sorted(framing) == ["budget:halt", "license:halt",
                               "occurrence:halt"]
    assert isinstance(rep["why_the_terminal_is_excluded"], str)
    assert len(list(comm_states())) > 0


def test_internal_traces_and_refusal_records() -> None:
    rep = internal_report()
    assert rep["internal_trace_preserves_occurrences"] is True
    assert rep["internal_trace_preserves_license"] is True
    assert rep["refusal_is_accepted"] is True
    assert rep["refusal_survives_every_event"] is True
    assert rep["refusal_survives_terminal"] is True
    obstructed = obstructed_state()
    refused = pstep(obstructed, ("refuse", 0, 1))
    assert refused.refusals == ((0, 1),)
    # no trace of internal events removes the record
    internal = [e for e in EVENT_BATTERY
                if e[0] not in ("admitOcc", "setBudget", "setLicense",
                                "halt")]
    assert (0, 1) in preplay(internal, refused).refusals


def test_replay_equivalence_is_scoped() -> None:
    rep = scoping_report()
    assert rep["equivalent_on_scope"] is True
    assert rep["equivalent_at_genesis"] is False
    assert preplay([A], PS(occ=(0,))) == PS(occ=(0,))
    assert preplay([A], GENESIS_P) != GENESIS_P


def test_rewrite_system_is_sound_terminating_confluent() -> None:
    rep = rewrite_report(2)
    assert rep["soundness_failures"] == 0
    assert rep["termination_failures"] == 0
    assert rep["confluence_failures"] == 0
    assert rep["normal_form_fixpoint_failures"] == 0
    assert rep["lists_checked"] == 1 + len(REWRITE_ALPHABET) \
        + len(REWRITE_ALPHABET) ** 2
    witness = rep["incompleteness_witness"]
    assert isinstance(witness, dict)
    assert witness["same_replay_everywhere"] is True
    assert witness["identified_by_rewriting"] is False


def test_normal_form_computation() -> None:
    assert nf([]) == []
    assert nf([A, A, A]) == [A]
    assert nf([HALT, A, B]) == [HALT]
    assert nf([A, B]) == [A, B]
    assert cons_nf(A, []) == [A]
    assert cons_nf(A, [A, B]) == [A, B]
    assert cons_nf(A, [B]) == [A, B]
    assert no_redex([])
    assert no_redex([A])
    assert no_redex([A, B])
    assert not no_redex([A, A])
    assert not no_redex([HALT, A])
    assert not no_redex([A, B, B])
    assert rw_reducts([]) == []
    assert rw_reducts([A]) == []
    assert rw_reducts([A, A]) == [[A]]
    assert rw_reducts([HALT, A]) == [[HALT]]
    assert rw_reducts([B, A, A]) == [[B, A]]
    # a list whose reduction graph rejoins: the same reduct twice
    assert normal_forms([A, A, A]) == [[A]]
    assert normal_forms([A]) == [[A]]
    assert len(list_battery(0)) == 1
    assert len(list_battery(1)) == 1 + len(REWRITE_ALPHABET)
    assert len(named_states()) == 12
    assert accepted(GENESIS_P, A)
    assert len(list(enumerate_states())) == 6144


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_trace_algebra.main(
        ["--artifacts", str(d1), "--max-len", "2"]) == 0
    assert run_trace_algebra.main(
        ["--artifacts", str(d2), "--max-len", "2"]) == 0
    assert (d1 / "trace_algebra.json").read_bytes() == \
        (d2 / "trace_algebra.json").read_bytes()
