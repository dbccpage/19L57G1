"""Replay, mutation, and countermodel tests for the represented-progress
kernel."""

from __future__ import annotations

import json
from pathlib import Path

from derivation.represented import (
    GENESIS,
    HEAD_A,
    HEAD_B,
    ORACLE_WORLD,
    PIGEON_HISTORY,
    SCHED_WORLD,
    TRUNC_WORLD,
    World,
    aug_ok,
    cert_neg,
    cert_pos,
    countermodel_report,
    hist_up_to,
    koenig_report,
    mark_ok,
    mutation_report,
    obstructed,
    obstructed_trunc,
    overwrite_first,
    productivity_report,
    progress_story,
    quiescent,
    repair_family,
    replay,
    sat,
    sep,
    step,
    step_gensym,
    step_head,
    step_oracle,
    step_sched,
    viol,
    wf,
    wit_valid,
)

import run_represented


def test_replay_determinism_and_composition() -> None:
    h = PIGEON_HISTORY
    assert replay(h) == replay(h)
    for cut in range(len(h) + 1):
        assert replay(h) == replay(h[cut:], replay(h[:cut]))


def test_genesis_inert_and_wf() -> None:
    assert replay([]) == GENESIS
    assert wf(GENESIS)
    for h in [PIGEON_HISTORY, hist_up_to(5)]:
        assert wf(replay(h))


def test_notes_are_transition_inert() -> None:
    w = replay(PIGEON_HISTORY)
    w_notes = replay(PIGEON_HISTORY + [("note", 7)])
    assert w_notes.notes != w.notes
    a = step(w, ("addView", (1,)))
    b = step(w_notes, ("addView", (1,)))
    assert a.views == b.views and a.reqs == b.reqs
    assert a.data == b.data and a.budget == b.budget


def test_pigeonhole_progress_story() -> None:
    story = progress_story()
    assert story["wf"] is True
    assert story["violated_1_2"] is True
    assert story["repair_family_1_2"] == []  # exhaustive failure
    assert story["obstructed_1_2"] is True
    assert story["augmentation_accepted"] is True
    assert story["discharged_after_augmentation"] is True
    assert story["old_reqs_preserved"] is True
    assert story["quiescent_after"] is True


def test_repair_family_retains_ties() -> None:
    w = World(data=(10, 20), views=((),), reqs=((0, 1),), budget=9)
    fam = repair_family(w, (0, 1))
    assert ((), 0) in fam and ((), 1) in fam  # both tied marks kept
    assert len(fam) == 2


def test_budget_and_license_are_load_bearing() -> None:
    w = replay(PIGEON_HISTORY)
    w0 = step(step(w, ("setBudget", 0)), ("addView", (1,)))
    assert w0.views == w.views  # no budget, no transition
    wl = step(
        step(w, ("setAugLicense", False)), ("addView", (1,))
    )
    assert wl.views == w.views  # no license, no transition
    assert step(w, ("addView", (1,))).views != w.views


def test_refusal_needs_certificate() -> None:
    w = replay(PIGEON_HISTORY)
    assert obstructed(w, (1, 2))
    w2 = step(w, ("refuse", 1, 2))
    assert (1, 2) in w2.refusals
    # a non-obstructed pair cannot be recorded as refused
    w3 = step(w, ("refuse", 0, 1))
    assert w3 == w


def test_productive_run_prefix_compatible() -> None:
    rep = productivity_report(10)
    assert rep["all_prefix_compatible"] is True
    assert rep["carriers_are_initial_segments"] is True
    assert rep["all_quiescent"] is True


def test_quiescent_worlds_stay_quiescent_without_require() -> None:
    w = replay(hist_up_to(4))
    assert quiescent(w)
    for e in [("admit", 99), ("mark", (1,), 0), ("addView", (0, 1)),
              ("note", 3), ("setBudget", 5)]:
        assert quiescent(step(w, e))


def test_countermodels_all_exhibited() -> None:
    rep = countermodel_report()
    assert rep["all_exhibited"] is True
    names = [r["name"] for r in rep["rows"]]  # type: ignore[index]
    assert names == [
        "unrecorded_scheduler",
        "unrecorded_fresh_name_source",
        "hidden_evaluator",
        "incomplete_search_false_obstruction",
        "destructive_rewrite_not_augmentation",
        "repetition_mislabeled_as_progress",
        "order_sensitive_semantics_splits_equivalents",
    ]


def test_scheduler_and_oracle_details() -> None:
    assert step_sched(True, SCHED_WORLD, ("mark", (), 0)) != step_sched(
        False, SCHED_WORLD, ("mark", (), 0)
    )
    assert not mark_ok(ORACLE_WORLD, (0,), 1)  # kernel rejects
    assert step_oracle(True, ORACLE_WORLD, ("mark", (0,), 1)) != (
        step_oracle(False, ORACLE_WORLD, ("mark", (0,), 1))
    )


def test_incomplete_search_vs_exhaustive() -> None:
    assert obstructed_trunc(1, TRUNC_WORLD, (1, 2))
    assert not obstructed(TRUNC_WORLD, (1, 2))
    assert repair_family(TRUNC_WORLD, (1, 2))


def test_destructive_rewrite_rejected_by_kernel() -> None:
    w = ORACLE_WORLD
    assert sat(w, (0, 1))
    assert not sat(overwrite_first(w, ()), (0, 1))
    # the kernel's augmentation cannot express an overwrite: append-only
    assert not aug_ok(w, (0,))  # already present
    w2 = step(w, ("addView", (1,)))
    assert sat(w2, (0, 1))  # conservativity


def test_order_sensitivity_splits_equivalents() -> None:
    assert set(HEAD_A.views) == set(HEAD_B.views)
    a = sat(step_head(HEAD_A, ("mark", (), 1)), (0, 1))
    b = sat(step_head(HEAD_B, ("mark", (), 1)), (0, 1))
    assert a != b


def test_gensym_hidden_source() -> None:
    base = replay(hist_up_to(1))
    a = step_gensym(0, base, ("admit", 99))
    b = step_gensym(99, base, ("admit", 99))
    assert a.data != b.data


def test_koenig_witnesses_without_infinite_history() -> None:
    rep = koenig_report(12)
    assert rep["witness_at_every_length"] is True
    assert rep["sampled_infinite_sources_refuted"] is True
    assert wit_valid([4] * 4)
    assert not wit_valid([4] * 5)


def test_certification_scope_and_relativity() -> None:
    rep = certification = certification_report_helper()
    assert rep["panel_certifies_equivalent"] is True
    assert rep["outside_column_separates"] is True
    assert rep["certification_is_panel_relative"] is True
    assert certification is rep
    assert cert_pos([((0,),)], 0, 1)
    assert not cert_pos([], 0, 1)
    assert cert_neg([((0, 1),)], 0, 1)
    assert sep((0,), 0, 1)


def certification_report_helper() -> dict[str, object]:
    from derivation.represented import certification_report

    return certification_report()


def test_mutation_detection() -> None:
    rep = mutation_report()
    assert rep["replay_deterministic"] is True
    assert rep["every_single_event_mutation_detected"] is True
    assert rep["mutations_checked"] == len(PIGEON_HISTORY)


def test_violation_only_from_require() -> None:
    w = replay(hist_up_to(3))
    assert quiescent(w)
    violations_before = [r for r in w.reqs if viol(w, r)]
    assert violations_before == []
    w2 = step(w, ("require", 0, 3))
    assert not viol(w2, (0, 3))  # already separated by (3,)
    w3 = step(step(w, ("admit", 99)), ("require", 0, 4))
    assert viol(w3, (0, 4))  # a new violation, from a require event


def test_run_main(tmp_path: Path) -> None:
    out = tmp_path / "artifacts"
    assert run_represented.main(["--artifacts", str(out)]) == 0
    payload = json.loads(
        (out / "represented.json").read_text(encoding="utf-8")
    )
    assert payload["progress_story"]["obstructed_1_2"] is True
    assert payload["countermodels"]["all_exhibited"] is True
    assert payload["productivity"]["all_prefix_compatible"] is True
    assert payload["mutation"][
        "every_single_event_mutation_detected"] is True
    out2 = tmp_path / "artifacts2"
    run_represented.main(["--artifacts", str(out2)])
    assert (out / "represented.json").read_bytes() == (
        out2 / "represented.json"
    ).read_bytes()
