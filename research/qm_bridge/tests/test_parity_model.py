"""Tests of the parity model.  AuthorityEffect: None.

Each test re-runs a check of ``parity_model.py`` and asserts the outcome the
Lean module ``ResearchQmBridge.Parity`` proves.  A passing test proves
nothing beyond its bounds.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import parity_model as pm  # noqa: E402


def test_square_has_no_global_assignment() -> None:
    assert pm.global_count(3, 3, pm.SQUARE_TARGET) == 0


def test_dropping_any_context_leaves_sixteen() -> None:
    assert [pm.global_count(3, 3, pm.SQUARE_TARGET, skip=k) for k in range(6)] == [16] * 6


def test_even_sum_criterion_and_minimality_on_grids() -> None:
    assert pm.grid_failures(pm.GRID_MAX) == []


def test_context_indexed_witness() -> None:
    table = pm.context_indexed_witness()
    assert pm.context_indexed_meets(table)
    assert pm.broken_entries(table) == [(0, 2)]


def test_every_meeting_table_breaks_an_entry() -> None:
    assert pm.every_meeting_table_breaks()


def test_red_control_even_target_has_assignment() -> None:
    assert pm.global_count(3, 3, (0, 0, 0, 0, 0, 0)) == 2 ** 4
