"""Tests for the apartness/indistinguishability mirror."""

from __future__ import annotations

from pathlib import Path

import run_apartness
from derivation.apartness import (
    all_endofunctions,
    all_relations,
    equivalence_theorem_exhaustive,
    indist,
    indist_is_equivalence,
    insufficiency_countermodels,
    is_apart,
    is_cotrans,
    is_irrefl,
    is_symm,
    operation_censuses,
    orientation_separation,
    preserves_apart,
    preserves_oriented,
    sym_closure,
)


def test_equivalence_exhaustive_to_three() -> None:
    assert equivalence_theorem_exhaustive(3)


def test_apartness_laws_on_examples() -> None:
    s2 = frozenset({(0, 1), (1, 0)})
    assert is_apart(2, s2)
    assert indist_is_equivalence(2, s2)
    d2 = frozenset({(0, 1)})
    assert is_irrefl(2, d2) and not is_symm(2, d2)
    tri = frozenset({(0, 1), (1, 0)})
    assert is_symm(3, tri) and not is_cotrans(3, tri)
    bare = frozenset({(0, 0)})
    assert not is_irrefl(1, bare)
    assert not indist(bare, 0, 0)


def test_insufficiency_countermodels_all_hold() -> None:
    rep = insufficiency_countermodels()
    assert all(v is True for v in rep.values())


def test_orientation_separation() -> None:
    rep = orientation_separation()
    assert all(v is True for v in rep.values())
    assert sym_closure(frozenset({(0, 1)})) == frozenset(
        {(0, 1), (1, 0)})


def test_operation_censuses() -> None:
    rep = operation_censuses(4)
    assert rep["two_point_oriented_exactly_id"] is True
    assert rep["two_point_apart_exactly_id_and_swap"] is True
    assert rep["two_point_constants_preserve_neither"] is True
    assert rep["formula_checked"] is True
    per = rep["per_carrier"]
    assert isinstance(per, dict)
    assert per["2"]["oriented_preservers"] == 1
    assert per["2"]["apart_preservers"] == 2
    assert per["3"]["oriented_preservers"] == 3
    assert per["4"]["oriented_preservers"] == 16
    # spot negatives
    assert not preserves_oriented((1, 0), 0, 1)
    assert preserves_apart((1, 0), 0, 1)
    assert not preserves_apart((0, 0), 0, 1)
    assert len(all_endofunctions(3)) == 27
    assert len(all_relations(2)) == 16


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_apartness.main(
        ["--artifacts", str(d1), "--max-n", "3"]) == 0
    assert run_apartness.main(
        ["--artifacts", str(d2), "--max-n", "3"]) == 0
    assert (d1 / "apartness.json").read_bytes() == \
        (d2 / "apartness.json").read_bytes()
