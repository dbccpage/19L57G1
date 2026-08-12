"""Tests for the F5 composite-generator run."""

from __future__ import annotations

import json
from pathlib import Path

from derivation.generator import (
    ROUNDS,
    STRATEGIES,
    chain_rel,
    chain_tags,
    exclusion_check,
    lean_agreement,
    middle_pairs,
    obstructions,
    profile1,
    profile2,
    run_branch,
    view,
)

import run_generator


def test_chain_matches_lean_shape() -> None:
    assert chain_tags(4) == frozenset({1, 2, 3, 4})
    assert chain_rel(3) == ((0, 1), (1, 2), (2, 3))
    # Lean profile classes: seed, interior, tip.
    assert profile1(4, 0) == (False, False, True)
    assert profile1(4, 2) == (True, True, True)
    assert profile1(4, 4) == (True, True, False)


def test_depth1_obstructions_are_exactly_middle_pairs() -> None:
    for n in range(1, ROUNDS + 1):
        assert obstructions("none", n, {}) == middle_pairs(n)


def test_generation_never_dries_within_bound() -> None:
    """Mirror of the horizon-free Lean theorem, on the bounded prefix:
    from round 3 on, the bare composite has a live obstruction and
    (1, 2) is always one."""
    for n in range(3, ROUNDS + 1):
        obs = obstructions("none", n, {})
        assert obs and (1, 2) in obs
    assert obstructions("none", 2, {}) == []


def test_automark_presence_is_vacuous() -> None:
    for n in range(1, ROUNDS + 1):
        assert obstructions("automark_presence", n, {}) == obstructions(
            "none", n, {}
        )


def test_automark_valued_kills_generation() -> None:
    rep = run_branch("automark_valued")
    assert not rep.fired_ever()
    assert rep.classification() == "generation_dead"


def test_per_pair_repairs_but_imports_every_firing_round() -> None:
    rep = run_branch("per_pair_fresh_mark")
    assert rep.fired_ever()
    assert rep.repaired_every_round()
    assert rep.classification() == "repairs_by_recurring_imports"
    for r in rep.rounds:
        if r.obstructions_before > 0:
            assert r.imports_this_round > 0
            assert r.repairs == r.imports_this_round
    # The repair debt never dries within the bound: firing rounds keep
    # occurring to the horizon (the Lean outrun theorem, in bounds).
    firing = [r.round_no for r in rep.rounds if r.obstructions_before > 0]
    assert firing and firing[-1] == ROUNDS


def test_depth2_first_fires_at_five_and_stays_alive() -> None:
    rep = run_branch("depth2")
    assert rep.first_fire_round() == 5
    assert rep.classification() == "fires_unrepaired"
    assert rep.rounds[-1].obstructions_before > 0


def test_none_fires_unrepaired_from_three() -> None:
    rep = run_branch("none")
    assert rep.first_fire_round() == 3
    assert rep.classification() == "fires_unrepaired"


def test_exclusion_no_endogenous_cycle_in_class() -> None:
    ex = exclusion_check()
    assert ex["endogenous_cycle_found"] is False
    assert ex["endogenous_cycle_strategies"] == []
    table = ex["classification_table"]
    assert isinstance(table, dict)
    assert set(table) == set(STRATEGIES)
    assert table["none"] == "fires_unrepaired"
    assert table["automark_presence"] == "fires_unrepaired"
    assert table["depth2"] == "fires_unrepaired"
    assert table["per_pair_fresh_mark"] == "repairs_by_recurring_imports"
    assert table["automark_valued"] == "generation_dead"


def test_lean_agreement_all_hold() -> None:
    agree = lean_agreement()
    assert all(agree.values())
    assert profile2(4, 1) != profile2(4, 3)
    assert profile2(5, 2) == profile2(5, 3)


def test_view_components() -> None:
    marks = {2: frozenset({7})}
    v_marked = view("per_pair_fresh_mark", 4, 2, marks)
    v_unmarked = view("per_pair_fresh_mark", 4, 3, marks)
    assert v_marked != v_unmarked
    assert view("automark_valued", 4, 2, {}) != view(
        "automark_valued", 4, 3, {}
    )
    assert view("none", 4, 2, {}) == view("none", 4, 3, {})


def test_run_main(tmp_path: Path) -> None:
    out = tmp_path / "artifacts"
    assert run_generator.main(["--artifacts", str(out)]) == 0
    payload = json.loads(
        (out / "generator.json").read_text(encoding="utf-8")
    )
    assert payload["exclusion"]["endogenous_cycle_found"] is False
    assert all(payload["lean_agreement"].values())
    assert payload["bounds"]["rounds_per_branch"] == ROUNDS
    out2 = tmp_path / "artifacts2"
    run_generator.main(["--artifacts", str(out2)])
    assert (out / "generator.json").read_bytes() == (
        out2 / "generator.json"
    ).read_bytes()
