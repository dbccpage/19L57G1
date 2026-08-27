"""
test_dynamics_menu.py — Tests for dynamics menu and collapse exhibit

<!-- AuthorityEffect: None -->
"""

import pytest
from derivation.model import EMPTY, AdmitDatum, AdmitForm, AdmitInst, replay
from dynamics_menu import (
    inspect_response_menu,
    is_pair_separated,
    five_atom_collapse_exhibit,
)


def test_genesis_quiescent_empty_menu():
    assert is_pair_separated(EMPTY, (0, 1)) is False
    res = inspect_response_menu(EMPTY, (0, 1))
    assert res.is_separated is False
    assert len(res.candidate_deltas) == 0


def test_unseparated_pair_exposes_tied_menu():
    # Challenge 3 base regime (2 data, 0 forms)
    base = replay([AdmitDatum("a"), AdmitDatum("ab")])
    pair = (0, 1)

    assert is_pair_separated(base, pair) is False

    # Under mu1, minimum valid responses are tied across multiple deltas
    menu = inspect_response_menu(base, pair, measure="mu1")
    assert menu.is_separated is False
    assert menu.is_tied is True
    assert len(menu.candidate_deltas) > 1
    # Check that cost is (2, -1)
    assert menu.attained_cost == (2, -1)


def test_separated_pair_returns_empty_menu():
    # Regime with datum 0 distinguished by unary form 0
    base = replay([
        AdmitDatum("a"),
        AdmitDatum("ab"),
        AdmitForm(arity=1),
        AdmitInst(form=0, args=(0,)),
    ])
    pair = (0, 1)

    assert is_pair_separated(base, pair) is True
    menu = inspect_response_menu(base, pair, measure="mu1")
    assert menu.is_separated is True
    assert len(menu.candidate_deltas) == 0


def test_five_atom_collapse_exhibit():
    exhibit = five_atom_collapse_exhibit()
    assert exhibit.atom_cost == 5
    assert exhibit.uncollapsed_holds is True
    assert exhibit.quotient_holds is False
    assert exhibit.law_failed_in_quotient is True
