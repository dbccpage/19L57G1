"""Tests for scale dynamics, rectangular rank defect, and Markov cylinder consistency."""

from __future__ import annotations

import pytest
import sys
from pathlib import Path

PY_DIR = Path(__file__).resolve().parent.parent
if str(PY_DIR) not in sys.path:
    sys.path.insert(0, str(PY_DIR))

from scale_dynamics import (
    bond,
    rank_defect,
    stage_dimension,
    twin_hi,
    twin_lo,
    verify_kolmogorov_cylinder_consistency,
    verify_rectangular_rank_defect,
    verify_regime_reflection_no_alphabet_map,
    verify_twin_separation,
)


def test_bonding_map() -> None:
    assert bond((0, 1, 2)) == (0, 1)
    assert bond((5,)) == ()
    assert bond(()) == ()


def test_rectangular_rank_defect() -> None:
    # Alphabet size c = 2: Delta_n = 2^n * (2 - 1) = 2^n > 0
    res_c2 = verify_rectangular_rank_defect(c=2, max_n=5)
    assert res_c2["all_positive"] is True
    assert res_c2["defects"][0] == 1
    assert res_c2["defects"][1] == 2
    assert res_c2["defects"][2] == 4
    assert res_c2["defects"][3] == 8

    # Alphabet size c = 3: Delta_n = 3^n * 2 > 0
    res_c3 = verify_rectangular_rank_defect(c=3, max_n=4)
    assert res_c3["all_positive"] is True
    assert res_c3["defects"][0] == 2
    assert res_c3["defects"][1] == 6
    assert res_c3["defects"][2] == 18


def test_dyadic_twin_separation() -> None:
    # Dyadic twins differ at scale 1
    sep1 = verify_twin_separation(scale=1)
    assert sep1["twin_lo"] == (0,)
    assert sep1["twin_hi"] == (1,)
    assert sep1["separated"] is True

    sep2 = verify_twin_separation(scale=2)
    assert sep2["twin_lo"] == (0, 1)
    assert sep2["twin_hi"] == (1, 0)
    assert sep2["separated"] is True


def test_regime_reflection_no_alphabet_map() -> None:
    ref = verify_regime_reflection_no_alphabet_map()
    assert ref["has_alphabet_map"] is False
    assert ref["premise_decoupled"] is True
    assert "data" in ref["fields"]
    assert "forms" in ref["fields"]
    assert "insts" in ref["fields"]
    assert "rules" in ref["fields"]
    assert "reqs" in ref["fields"]


def test_kolmogorov_cylinder_consistency() -> None:
    # Branching ratio is identically 1.0 for all alphabet sizes c >= 2
    for c in [2, 3, 4, 5]:
        res = verify_kolmogorov_cylinder_consistency(c=c, prefix_length=3)
        assert res["is_consistent"] is True
        assert abs(res["branching_ratio"] - 1.0) < 1e-12
