"""Tests for the presentation-compression mirror."""

from __future__ import annotations

from pathlib import Path

import run_compression
from derivation.compression import (
    MAX_FAMILY,
    MAX_M,
    MAX_N,
    Family,
    Fn,
    absolute_adequacy_iff_exhaustive,
    adequate,
    all_families,
    all_functions,
    class_bound_exhaustive,
    class_count,
    class_pos_exhaustive,
    countermodel_instances,
    descent_instance_count,
    descent_witnessed_exhaustive,
    digest_no_refine_exhaustive,
    digests,
    dup_no_refine_exhaustive,
    enlarge_refines_exhaustive,
    enlargements,
    factor_unique_on_image_exhaustive,
    factorization_iff_exhaustive,
    factors_on,
    fiber_constant,
    first_with_sig,
    injective_on,
    off_image_countermodel,
    p_quotient,
    partition_of,
    quotient_adequate_exhaustive,
    quotient_coarsest_exhaustive,
    quotient_exact_exhaustive,
    realized_sigs,
    separator_required_exhaustive,
    sig_determined,
    sig_eq,
    sig_iff_exhaustive,
    sig_list,
    split_characterization_exhaustive,
    split_count,
    splits_at,
    strict_split_increases_exhaustive,
    valid_factor_maps,
)

D3 = [0, 1, 2]
IND0: Fn = (1, 0, 0)
IND1: Fn = (0, 1, 0)
CONST: Fn = (0, 0, 0)


def test_bounds_declared() -> None:
    assert (MAX_N, MAX_M, MAX_FAMILY) == (3, 3, 2)


def test_enumerations() -> None:
    assert len(all_functions(2, 2)) == 4
    assert len(all_functions(3, 3)) == 27
    assert len(all_families(1, 1, 2)) == 3
    assert len(all_families(3, 3, 2)) == 1 + 27 + 729
    assert len(enlargements(1, 1, 1)) == 4


def test_sig_helpers() -> None:
    fam: Family = (IND0, IND1)
    assert sig_list(fam, 0) == (1, 0)
    assert sig_list((), 0) == ()
    assert sig_eq(fam, 1, 1)
    assert not sig_eq(fam, 0, 1)
    assert sig_eq((), 0, 2)
    assert sig_eq((CONST,), 0, 2)


def test_adequate_and_fiber_constant() -> None:
    merge_all: Fn = (0, 0, 0)
    assert adequate(D3, (), merge_all)
    assert not adequate(D3, (IND0,), merge_all)
    assert adequate(D3, (IND0,), (0, 1, 1))
    assert fiber_constant(D3, (0, 1, 1), IND0)
    assert not fiber_constant(D3, merge_all, IND0)


def test_factors_on_and_valid_maps() -> None:
    p: Fn = (0, 1, 1)
    assert factors_on(D3, p, IND0, 2)
    assert not factors_on(D3, (0, 0, 0), IND0, 2)
    gs = valid_factor_maps(D3, p, IND0, 2)
    assert gs == [{0: 1, 1: 0}]
    assert valid_factor_maps(D3, (0, 0, 0), IND0, 2) == []


def test_first_with_sig_and_quotient() -> None:
    fam: Family = (IND0,)
    assert first_with_sig(D3, fam, (1,)) == 0
    assert first_with_sig(D3, fam, (0,)) == 1
    # unrealized signature falls back to 0, mirroring ``getD 0``
    assert first_with_sig(D3, fam, (7,)) == 0
    assert p_quotient(D3, fam) == (0, 1, 1)
    assert p_quotient(D3, ()) == (0, 0, 0)
    assert p_quotient(D3, (IND0, IND1)) == (0, 1, 2)


def test_injective_on() -> None:
    assert injective_on(D3, (2, 1, 0))
    assert not injective_on(D3, (0, 0, 1))


def test_splits_and_sig_determined() -> None:
    assert splits_at(D3, (), (IND0,), 0)
    assert not splits_at(D3, (IND0,), (IND0,), 0)
    assert sig_determined(D3, (IND0,), IND0)
    assert sig_determined(D3, (IND0,), (0, 1, 1))
    assert not sig_determined(D3, (IND0,), IND1)


def test_realized_sigs_and_digests() -> None:
    fam: Family = (IND0,)
    assert realized_sigs(D3, fam) == [(1,), (0,)]
    assert realized_sigs(D3, ()) == [()]
    dgs = digests(D3, fam, 2)
    assert len(dgs) == 4  # 2 signatures, 2 values each
    for dg in dgs:
        assert dg[1] == dg[2]  # digests never separate a class
    assert digests(D3, (), 3) == [(0, 0, 0), (1, 1, 1), (2, 2, 2)]


def test_partition_and_class_count() -> None:
    assert partition_of(D3, ()) == [[0, 1, 2]]
    assert partition_of(D3, (IND0,)) == [[0], [1, 2]]
    assert partition_of(D3, (IND1,)) == [[0, 2], [1]]
    assert class_count(D3, ()) == 1
    assert class_count(D3, (IND0, IND1)) == 3


def test_off_image_countermodel() -> None:
    rep = off_image_countermodel()
    assert rep["g1_factors"] is True
    assert rep["g2_factors"] is True
    assert rep["agree_on_image"] is True
    assert rep["maps_differ"] is True


def test_countermodel_instances() -> None:
    rep = countermodel_instances()
    assert rep["both_split_at_zero"] is True
    assert rep["equal_cost"] is True
    assert rep["classes_differ"] is True
    assert rep["class_count_increases"] is True
    assert rep["classes_one"] == [[0], [1, 2]]
    assert rep["classes_two"] == [[0, 2], [1]]


def test_factorization_exhaustive_small() -> None:
    assert factorization_iff_exhaustive(2, 2)
    assert factor_unique_on_image_exhaustive(2, 2)


def test_quotient_exhaustive_small() -> None:
    assert sig_iff_exhaustive(2, 2, 2)
    assert quotient_exact_exhaustive(2, 2, 2)
    assert quotient_adequate_exhaustive(2, 2, 2)
    assert quotient_coarsest_exhaustive(2, 2, 2)


def test_descent_exhaustive_small() -> None:
    assert descent_witnessed_exhaustive(2, 2, 2)
    assert descent_instance_count(2, 2, 2) > 0


def test_enlargement_exhaustive_small() -> None:
    assert enlarge_refines_exhaustive(2, 2, 2)
    assert split_characterization_exhaustive(2, 2, 2)
    assert split_count(2, 2, 2) > 0


def test_absolute_adequacy_exhaustive_small() -> None:
    assert absolute_adequacy_iff_exhaustive(2, 2, 2)


def test_replay_exhaustive_small() -> None:
    assert dup_no_refine_exhaustive(2, 2, 2)
    assert digest_no_refine_exhaustive(2, 2, 2)
    assert separator_required_exhaustive(2, 2, 2)


def test_class_count_exhaustive_small() -> None:
    assert class_bound_exhaustive(2, 2, 2)
    assert class_pos_exhaustive(2, 2, 2)
    assert strict_split_increases_exhaustive(2, 2, 2)


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_compression.main(
        ["--artifacts", str(d1), "--max-n", "3"]) == 0
    assert run_compression.main(
        ["--artifacts", str(d2), "--max-n", "3"]) == 0
    assert (d1 / "compression.json").read_bytes() == \
        (d2 / "compression.json").read_bytes()
