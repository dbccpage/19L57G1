"""Unit tests for footprint.py: Footprint, Bernstein interference, and DependencyGraph."""

from __future__ import annotations

from carrier import State3
from footprint import (
    FP_L1,
    FP_L2,
    FP_M,
    FP_READ_L1_WRITE_M,
    FP_READ_M_WRITE_L1,
    FP_READ_M_WRITE_L2,
    DependencyGraph,
    Footprint,
    Locus,
    interferes,
    is_disjoint,
    locus_interferes,
)


def test_footprint_creation_and_properties() -> None:
    fp = Footprint.from_loci(reads=[Locus.L1, Locus.M], writes=[Locus.L2])
    assert fp.r1 is True
    assert fp.r2 is False
    assert fp.rm is True
    assert fp.w1 is False
    assert fp.w2 is True
    assert fp.wm is False

    assert fp.reads == {Locus.L1, Locus.M}
    assert fp.writes == {Locus.L2}


def test_locus_interference_bernstein_truth_table() -> None:
    # Read-Read never interferes
    assert locus_interferes(w_a=False, r_a=True, w_b=False, r_b=True) is False
    # None-None never interferes
    assert locus_interferes(w_a=False, r_a=False, w_b=False, r_b=False) is False

    # Write-Read interferes (RAW / WAR)
    assert locus_interferes(w_a=True, r_a=False, w_b=False, r_b=True) is True
    assert locus_interferes(w_a=False, r_a=True, w_b=True, r_b=False) is True

    # Write-Write interferes (WAW)
    assert locus_interferes(w_a=True, r_a=False, w_b=True, r_b=False) is True
    assert locus_interferes(w_a=True, r_a=True, w_b=True, r_b=True) is True


def test_canonical_footprints_disjointness() -> None:
    # Local moves at distinct loci are mutually disjoint
    assert is_disjoint(FP_L1, FP_L2) is True
    assert is_disjoint(FP_L1, FP_M) is True
    assert is_disjoint(FP_L2, FP_M) is True

    assert interferes(FP_L1, FP_L2) is False
    assert interferes(FP_L1, FP_M) is False
    assert interferes(FP_L2, FP_M) is False


def test_interference_symmetry() -> None:
    all_fps = [
        FP_L1,
        FP_L2,
        FP_M,
        FP_READ_M_WRITE_L1,
        FP_READ_M_WRITE_L2,
        FP_READ_L1_WRITE_M,
    ]
    for fp1 in all_fps:
        for fp2 in all_fps:
            assert interferes(fp1, fp2) == interferes(fp2, fp1)
            assert is_disjoint(fp1, fp2) == is_disjoint(fp2, fp1)


def test_coupling_interference() -> None:
    # FP_READ_M_WRITE_L1 reads M and writes L1
    # FP_M writes M. Thus they interfere on M (RAW/WAR)!
    assert interferes(FP_READ_M_WRITE_L1, FP_M) is True
    assert is_disjoint(FP_READ_M_WRITE_L1, FP_M) is False

    # FP_READ_M_WRITE_L1 and FP_L2:
    # FP_READ_M_WRITE_L1: reads M, writes L1
    # FP_L2: reads L2, writes L2
    # Mutually disjoint!
    assert is_disjoint(FP_READ_M_WRITE_L1, FP_L2) is True


def test_dependency_graph_construction() -> None:
    from footprint import OperationRecord

    ops = [
        OperationRecord("opL1", FP_L1, lambda s: s),
        OperationRecord("opL2", FP_L2, lambda s: s),
        OperationRecord("opM", FP_M, lambda s: s),
        OperationRecord("opReadMWriteL1", FP_READ_M_WRITE_L1, lambda s: s),
        OperationRecord("opWrite1L1", FP_L1, lambda s: s),
    ]

    graph = DependencyGraph(ops)

    # Independent pairs:
    assert not graph.has_edge("opL1", "opL2")
    assert not graph.has_edge("opL1", "opM")
    assert not graph.has_edge("opL2", "opM")
    assert not graph.has_edge("opReadMWriteL1", "opL2")

    # Dependent pairs:
    assert graph.has_edge("opL1", "opWrite1L1")  # WAW on L1
    assert graph.has_edge("opReadMWriteL1", "opM")  # WAR on M
    assert graph.has_edge("opReadMWriteL1", "opL1")  # WAW on L1

    indep = graph.independent_pairs()
    assert ("opL1", "opL2") in indep
    assert ("opL1", "opM") in indep
    assert ("opL2", "opM") in indep

    interf = graph.interfering_pairs()
    assert ("opL1", "opWrite1L1") in interf
    assert ("opM", "opReadMWriteL1") in interf or ("opReadMWriteL1", "opM") in interf
