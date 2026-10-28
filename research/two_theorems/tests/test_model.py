"""Tests of the finite model and of the tree's pins.  AuthorityEffect: None.

Every test here re-runs a check of ``model.py`` and asserts the outcome the
Lean library proves (or, for the capacity lists, the outcome the Lean file
decides).  A failing test means the model and the library disagree, or the
pins drifted; it never means a theorem is proved.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
TREE = HERE.parent
sys.path.insert(0, str(TREE))

import model  # noqa: E402

D3: model.Carrier = (0, 1, 2)
D4: model.Carrier = (0, 1, 2, 3)
POOL: list[model.Presentation] = [
    model.Table({x: x % 2 for x in D4}),
    model.Table({x: x // 2 for x in D4}),
    model.Table({x: 1 if x == 1 else 0 for x in D4}),
    model.Table({x: 0 for x in D4}),
]


# ---------------------------------------------------------------- pins


def test_lean_imports_match_pin() -> None:
    assert model.lean_imports() == model.consumed_modules()


def test_consumed_modules_exist() -> None:
    lean4 = TREE.parents[1] / "lean4"
    for module in model.consumed_modules():
        assert (lean4 / (module.replace(".", "/") + ".lean")).is_file(), module


def test_axiom_report_matches_contract() -> None:
    report = (TREE / "lean" / "ResearchTwoTheorems" / "AxiomReport.lean").read_text(encoding="utf-8")
    reported = re.findall(r"^#print axioms (\S+)$", report, re.M)
    contract = json.loads((TREE / "TREE_CONTRACT.json").read_text(encoding="utf-8"))
    assert reported == contract["axiom_declarations"]
    assert len(set(reported)) == len(reported)


# ---------------------------------------------------------------- Theorem I


@pytest.mark.parametrize("D, m", [(D3, 1), (D4, 1), (D4, 2)])
def test_resolution(D: model.Carrier, m: int) -> None:
    out = model.resolution_check(D, m)
    assert out["disagree"] == 0
    expected = sum(1 for p in model.all_presentations(D) if model.fibers(D, p) <= 2 ** m)
    assert out["bit_observer_sharp"] == expected
    assert out["presentations"] == len(D) ** len(D)


def test_verdict_ceiling() -> None:
    assert model.verdict_ceiling_check(D4, 2)
    assert model.information_le_resolution_check(D4, 2)


def test_fact_not_law() -> None:
    out = model.separation_fact_not_law()
    assert out == {"irreflexive_on_examples": True, "separates_0_1": True, "merges_0_2": True}


# ---------------------------------------------------------------- Theorem I(d)


@pytest.mark.parametrize("k, d", [(k, d) for k in (1, 2, 3, 4) for d in (0, 1, 2) if k ** (2 * d + 1) <= 1100])
def test_window_distinct_tight(k: int, d: int) -> None:
    assert model.tight(k, d)
    assert len(model.colouring_list(k, d)) == model.threshold(k, d) - 1


@pytest.mark.parametrize("k, d", [(2, 0), (3, 0), (2, 1)])
def test_forced_collision_at_threshold(k: int, d: int) -> None:
    assert model.forced_collision_exhaustive(k, d)


def test_lean_lists_are_the_construction() -> None:
    """The lists the Lean file decides on are the ones the construction gives."""
    text = (TREE / "lean" / "ResearchTwoTheorems" / "Capacity.lean").read_text(encoding="utf-8")
    found = re.findall(r"def list_(\d)_(\d) : List Nat :=\s*\[([^\]]*)\]", text)
    assert len(found) == 6
    for k_s, d_s, body in found:
        k, d = int(k_s), int(d_s)
        lean_list = [int(t) for t in body.replace("\n", " ").split(",") if t.strip()]
        assert lean_list == model.colouring_list(k, d), (k, d)


def test_encode_is_little_endian() -> None:
    assert model.encode(2, [1, 0, 1]) == 1 + 2 * (0 + 2 * 1)
    assert model.encode(3, []) == 0


# ---------------------------------------------------------------- Theorem II


def test_knowledge_checks() -> None:
    out = model.knowledge_checks(D4, POOL, 2)
    assert out["families"] == 11
    assert all(v == 0 for k, v in out.items() if k != "families"), out


def test_institution_exceeds_members() -> None:
    out = model.institution_exceeds_members(D4)
    assert out == {"information_joint": 4, "information_parity": 2, "information_half": 2,
                   "parity_knows_half": False, "half_knows_parity": False,
                   "joint_knows_identity": True}


def test_mutual_knowledge() -> None:
    assert model.mutual_knowledge_check(D3, 1, POOL[:3], 2) == 0


def test_panels() -> None:
    out = model.panel_checks(D3, 1, 2)
    assert out["neg_mismatch"] == 0
    assert out["pos_violation"] == 0
    assert out["pooled_not_unanimous"] > 0


def test_witness_of_ignorance() -> None:
    parity, half = POOL[0], POOL[1]
    assert model.witness_of_ignorance(D4, [parity], half) is not None
    assert model.witness_of_ignorance(D4, [parity, half], model.Table({x: x for x in D4})) is None


# ---------------------------------------------------------------- Diagonal


def test_diagonal() -> None:
    out = model.diagonal_checks(D4, 5)
    assert out == {"never_member": True, "known_by": [3, 4, 5], "unknown_by": [0, 1, 2]}


@pytest.mark.parametrize("size", [1, 2, 3])
def test_no_closed_self_evaluator(size: int) -> None:
    assert model.self_evaluator_check(size)


# ---------------------------------------------------------------- Correspondence


def test_correspondence() -> None:
    out = model.correspondence_checks(D3, POOL[:3], 2)
    assert out == {"constant_faithful": False, "constant_collapses_all": True,
                   "empty_actor_constant": True, "faithful_actor_mismatch": 0,
                   "sharp_pullback_mismatch": 0, "fiber_constant_violation": 0}


def test_faithful_examples() -> None:
    assert model.faithful(D3, model.Table({0: 5, 1: 7, 2: 9}))
    assert not model.faithful(D3, model.Table({0: 5, 1: 5, 2: 9}))


# ---------------------------------------------------------------- Regime bridge


def test_bridge() -> None:
    out = model.bridge_checks([model.R0, model.R0_RULE, model.R0_BOTH, model.R_BINARY, model.R_RULE_ONLY])
    assert out["mismatch"] == 0
    assert out["bound_violation"] == 0
    assert out["pairs"] == 4 + 4 + 4 + 9 + 9
    assert out["informations"] == [2, 1, 1, 3, 1]
    assert out["unadmitted_in_no_view"] is True
    assert out["unadmitted_separated_from_0"] is True


def test_recollapse_witness() -> None:
    out = model.recollapse_witness()
    assert out == {"views_before": [[0]], "views_after": [[0, 1]],
                   "separable_before": True, "separable_after": False, "lost_views": [[0]]}


def test_contexts_of_r0() -> None:
    assert model.all_ctxs(model.R0) == [(0, (None,))]
    assert len(model.all_ctxs(model.R_BINARY)) == 1 + (4 * 4 - 3 * 3)


def test_verdict_mono() -> None:
    assert model.verdict_mono_check(D3, 1)


# ---------------------------------------------------------------- summary


def test_run_all_serialises() -> None:
    json.dumps(model.run_all(), sort_keys=True)


# ---------------------------------------------------------------- 2026-10-28 reading

POOL4 = [model.Table({x: x % 2 for x in D4}), model.Table({x: x // 2 for x in D4}),
         model.Table({x: (x == 1) * 1 for x in D4}), model.Table({x: 0 for x in D4})]
POOL3 = [model.Table({x: x % 2 for x in D3}), model.Table({x: x // 2 for x in D3}),
         model.Table({x: (x == 1) * 1 for x in D3}), model.Table({x: 0 for x in D3})]


def test_extension_forced() -> None:
    r = model.extension_checks(D4, POOL4, 2)
    assert r["forced_cases"] > 0 and r["forced_violations"] == 0
    assert r["member_knows_what_family_does_not"] == 0
    assert r["finder_cases"] > 0 and r["finder_violations"] == 0


def test_observer_cannot_read_resolution() -> None:
    for D, m in ((D3, 1), (D4, 2)):
        r = model.cannot_read_checks(D, m)
        assert r["merged_pairs"] > 0 and r["failures"] == 0


def test_residuals() -> None:
    r = model.residual_checks(D4, POOL4, 2)
    assert r["cases"] > 0 and r["nil_iff_violations"] == 0 and r["antitone_violations"] == 0
    half, parity = POOL4[1], POOL4[0]
    assert model.residuals(D4, [half], model.Table({x: x for x in D4})) == [(0, 1), (1, 0), (2, 3), (3, 2)]
    assert model.residuals(D4, [half, parity], model.Table({x: x for x in D4})) == []


def test_nesting() -> None:
    r = model.nest_checks(D4, POOL4, 2)
    assert r["knows_violations"] == 0 and r["information_violations"] == 0
    assert r["collapse_cases"] > 0 and r["collapse_violations"] == 0


def test_finite_question_space() -> None:
    r = model.finite_question_space(D3, POOL3, 2)
    assert r["tables"] == 27 and r["representative_mismatch"] == 0
    assert r["know_or_witness_over_all_tables"] is True


def test_honesty() -> None:
    r = model.honesty_checks(D3, POOL3, 2)
    assert r["silence_honest"] and r["self_report_honest"] and r["members_honest"]
    assert r["mono_violations"] == 0 and r["carrier_violations"] == 0
    assert r["reports_do_not_certify"] is True and r["honest_here_not_there"] is True


def test_guess() -> None:
    r = model.guess_checks(D4)
    assert r["guess"] and (r["witness_x"], r["witness_y"]) == (0, 1)
    assert r["own_guess_invisible"] and r["visible_to_family"] and r["another_member_splits"]
    assert r["honest_for_family"] and r["shared_by_half_alone"]
