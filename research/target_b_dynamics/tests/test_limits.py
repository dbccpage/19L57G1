"""Tests for limits.py: Inverse systems, bonding maps, and thread spaces."""

import pytest

from limits import (
    LimitsError,
    bond,
    compatible,
    ebond,
    ecompatible,
    eof_seq,
    eto_seq,
    even_family,
    eventual,
    eventually_compatible,
    of_seq,
    restrict_even,
    roundtrip_of_to_seq,
    roundtrip_to_of_seq,
    shift_not_local_witness,
    to_seq,
    twin_hi,
    twin_lo,
    twins_differ_at_scale_one,
)


def test_bonding_basic() -> None:
    assert bond((0, 1, 2)) == (0, 1)
    assert bond((5,)) == ()
    assert bond(()) == ()


def test_compatible_family() -> None:
    # A genuine prefix thread
    family = ((), (0,), (0, 1), (0, 1, 2), (0, 1, 2, 0))
    assert compatible(family) is True


def test_incompatible_family() -> None:
    # Scale 2 has (0, 2), while scale 3 has (0, 1, 0)
    family = ((), (0,), (0, 2), (0, 1, 0))
    assert compatible(family) is False


def test_eventual_agreement_not_compatible() -> None:
    # eventual(4) reads: scale 0: (), scale 1: (1,), scale 2: (0, 0), scale 3: (0, 0, 0)
    fam = eventual(4)
    assert compatible(fam) is False
    # But it agrees after scale 2
    assert eventually_compatible(fam, after=2) is True


def test_sequence_thread_roundtrip() -> None:
    # Sequence: alternating 0 and 1
    seq = lambda i: i % 2
    assert roundtrip_to_of_seq(seq, upto=20) is True

    thread = of_seq(seq, upto=15)
    assert roundtrip_of_to_seq(thread) is True


def test_to_seq_out_of_bounds() -> None:
    family = ((), (0,), (0, 1))
    with pytest.raises(LimitsError):
        to_seq(family, 5)


def test_even_subsystem_rescaling() -> None:
    seq = lambda i: (i * 3) % 7
    thread = of_seq(seq, upto=10)
    ev_fam = restrict_even(thread)
    assert ecompatible(ev_fam) is True

    # Reconstruct sequence from even thread
    for i in range(5):
        assert eto_seq(ev_fam, i) == seq(i)


def test_shift_not_local() -> None:
    w1, w2, s1, s2 = shift_not_local_witness()
    assert w1[:2] == w2[:2]
    assert s1 != s2


def test_dyadic_twin_separation() -> None:
    assert twins_differ_at_scale_one() is True
    assert twin_lo(0) == 0
    assert twin_hi(0) == 1
    assert twin_lo(1) == 1
    assert twin_hi(1) == 0
