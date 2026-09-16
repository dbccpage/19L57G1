"""Tests for Overlapping Dyadic Interval Domain & Constructive Connectedness.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from research.endogenous_continuum.interval_domain import (
    MAX_COVER_SCALE,
    DyadicInterval,
    IntervalCover,
    IntervalRewriteSystem,
    analyze_cross_scale_cover,
    compute_cover_profile,
    create_interval_coarsening_map,
    create_interval_movegraph,
)


def test_dyadic_interval_endpoints_and_width() -> None:
    """Exact rational arithmetic for endpoints and widths across multiple scales."""
    # Scale 1: [0, 1] represented by index 0: [0/2, 2/2] = [0, 1], width = 1
    iv1 = DyadicInterval(scale=1, index=0)
    assert iv1.left_endpoint == Fraction(0, 2)
    assert iv1.right_endpoint == Fraction(2, 2)
    assert iv1.midpoint == Fraction(1, 2)
    assert iv1.width == Fraction(1, 1)

    # Scale 3, index 4: [4/8, 6/8] = [1/2, 3/4], width = 1/4
    iv3 = DyadicInterval(scale=3, index=4)
    assert iv3.left_endpoint == Fraction(1, 2)
    assert iv3.right_endpoint == Fraction(3, 4)
    assert iv3.midpoint == Fraction(5, 8)
    assert iv3.width == Fraction(1, 4)

    # Scale 10, index 1022: [1022/1024, 1024/1024] = [511/512, 1]
    iv10 = DyadicInterval(scale=10, index=1022)
    assert iv10.left_endpoint == Fraction(511, 512)
    assert iv10.right_endpoint == Fraction(1, 1)
    assert iv10.width == Fraction(1, 512)

    # Negative scale or index validation
    with pytest.raises(ValueError, match="scale must be non-negative"):
        DyadicInterval(scale=-1, index=0)
    with pytest.raises(ValueError, match="index must be non-negative"):
        DyadicInterval(scale=0, index=-1)
    with pytest.raises(TypeError, match="scale must be an integer"):
        DyadicInterval(scale=1.0, index=0)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="index must be an integer"):
        DyadicInterval(scale=1, index=True)


def test_dyadic_interval_overlap_same_scale() -> None:
    """Overlap relation at identical scale: |i1 - i2| <= 1."""
    k = 4
    # Self overlap (reflexivity)
    iv = DyadicInterval(k, 5)
    assert iv.overlaps(iv)

    # Adjacent overlap
    iv_next = DyadicInterval(k, 6)
    assert iv.overlaps(iv_next)
    assert iv_next.overlaps(iv)

    inter = iv.intersection(iv_next)
    assert inter is not None
    # Intersection of [5/16, 7/16] and [6/16, 8/16] is [6/16, 7/16] of width 1/16
    assert inter[0] == Fraction(6, 16)
    assert inter[1] == Fraction(7, 16)
    assert inter[1] - inter[0] == Fraction(1, 16)

    # Disjoint interiors: distance 2 touches at single boundary point 7/16, open interior is empty
    iv_touch = DyadicInterval(k, 7)
    assert not iv.overlaps(iv_touch)
    assert iv.intersection(iv_touch) is None

    # Distance 3: strictly disjoint
    iv_far = DyadicInterval(k, 8)
    assert not iv.overlaps(iv_far)
    assert iv.intersection(iv_far) is None


def test_dyadic_interval_cross_scale_overlap() -> None:
    """Cross-scale overlap: parent overlaps its refinement children."""
    parent = DyadicInterval(scale=2, index=1)  # [1/4, 3/4]
    c0, c1, c2 = parent.refine()
    # c0 = [2/8, 4/8] = [1/4, 1/2]
    # c1 = [3/8, 5/8]
    # c2 = [4/8, 6/8] = [1/2, 3/4]

    assert parent.overlaps(c0)
    assert parent.overlaps(c1)
    assert parent.overlaps(c2)

    # Subinterval outside parent bounds: [6/8, 8/8] at scale 3
    outside = DyadicInterval(scale=3, index=6)
    assert not parent.overlaps(outside)


def test_interval_refinement_coherence() -> None:
    """Interval refinement forms an overlapping sub-chain spanning the parent interval."""
    parent = DyadicInterval(scale=3, index=2)  # [2/8, 4/8] = [1/4, 1/2]
    c0, c1, c2 = parent.refine()

    assert c0.left_endpoint == parent.left_endpoint
    assert c2.right_endpoint == parent.right_endpoint

    # Children overlap adjacently
    assert c0.overlaps(c1)
    assert c1.overlaps(c2)


def test_canonical_cover_structure() -> None:
    """Canonical cover at scale k covers [0, 1] with (2^k - 1) overlapping intervals."""
    for k in (1, 2, 3, 5):
        cover = IntervalCover.canonical(scale=k)
        expected_len = (1 << k) - 1
        assert len(cover.intervals) == expected_len
        assert cover.intervals[0].left_endpoint == Fraction(0, 1)
        assert cover.intervals[-1].right_endpoint == Fraction(1, 1)

        # Consecutive intervals strictly overlap
        for i in range(expected_len - 1):
            assert cover.intervals[i].overlaps(cover.intervals[i + 1])

    with pytest.raises(ValueError, match="Canonical cover requires scale >= 1"):
        IntervalCover.canonical(scale=0)
    with pytest.raises(TypeError, match="scale must be an integer"):
        IntervalCover.canonical(scale=True)

    with pytest.raises(ValueError, match="requires 3 intervals"):
        IntervalCover(scale=2, intervals=(DyadicInterval(2, 0),))
    with pytest.raises(ValueError, match=r"intervals\[1\] must equal"):
        IntervalCover(
            scale=2,
            intervals=(DyadicInterval(2, 0), DyadicInterval(2, 2), DyadicInterval(2, 1)),
        )


def test_overlapping_chain_generation() -> None:
    """Constructive overlapping chains between any start and target indices."""
    cover = IntervalCover.canonical(scale=3)  # 7 intervals: 0 to 6
    # Forward chain
    chain_fwd = cover.find_overlapping_chain(0, 6)
    assert len(chain_fwd) == 7
    assert chain_fwd[0] == cover.intervals[0]
    assert chain_fwd[-1] == cover.intervals[6]

    # Backward chain
    chain_bwd = cover.find_overlapping_chain(5, 1)
    assert len(chain_bwd) == 5
    assert chain_bwd[0] == cover.intervals[5]
    assert chain_bwd[-1] == cover.intervals[1]

    # Single-element chain
    chain_single = cover.find_overlapping_chain(3, 3)
    assert len(chain_single) == 1
    assert chain_single[0] == cover.intervals[3]

    # Out of bounds
    with pytest.raises(IndexError):
        cover.find_overlapping_chain(-1, 2)
    with pytest.raises(IndexError):
        cover.find_overlapping_chain(0, 100)


def test_partition_boundary_overlap_witness() -> None:
    """Locate an adjacent overlap crossing a validated finite partition."""
    cover = IntervalCover.canonical(scale=4)  # 15 intervals: 0 .. 14
    # Test partition A = {0, 1, 2, 3}, B = {4, 5, ..., 14}
    set_a = {0, 1, 2, 3}
    set_b = set(range(4, 15))
    int_a, int_b = cover.find_partition_boundary_overlap(set_a, set_b)
    assert int_a == cover.intervals[3]
    assert int_b == cover.intervals[4]
    assert int_a.overlaps(int_b)

    # Irregular partition: A = {0, 2, 4}, B = {1, 3, 5, ..., 14}
    set_a2 = {0, 2, 4}
    set_b2 = {1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}
    int_a2, int_b2 = cover.find_partition_boundary_overlap(set_a2, set_b2)
    assert int_a2 == cover.intervals[0]
    assert int_b2 == cover.intervals[1]
    assert int_a2.overlaps(int_b2)

    # Invalid partition missing start index 0
    with pytest.raises(ValueError, match="set_a must contain index 0"):
        cover.find_partition_boundary_overlap(set(range(1, 15)), {0})

    # Invalid partition missing terminal index
    with pytest.raises(ValueError, match="set_b must contain the terminal index"):
        cover.find_partition_boundary_overlap({0, 14}, set(range(1, 14)))

    with pytest.raises(ValueError, match="must be disjoint"):
        cover.find_partition_boundary_overlap({0, 1}, set(range(1, 15)))
    with pytest.raises(ValueError, match="partition exactly"):
        cover.find_partition_boundary_overlap({0}, {14})
    with pytest.raises(ValueError, match="partition exactly"):
        cover.find_partition_boundary_overlap({0, 99}, set(range(1, 15)))


def test_overlap_invariant_observable_is_constant() -> None:
    """Overlap-invariant observables are constant across the finite cover chain."""
    cover = IntervalCover.canonical(scale=4)

    # Constant observable (respects overlap)
    def obs_const(iv: DyadicInterval) -> str:
        return "connected_state"

    assert cover.observable_is_constant_on_cover(obs_const)

    # Non-constant observable (violates overlap condition)
    def obs_parity(iv: DyadicInterval) -> int:
        return iv.index % 2

    assert not cover.observable_is_constant_on_cover(obs_parity)


def test_interval_rewrite_system_confluence() -> None:
    """Local and global confluence of index contraction rewrite system."""
    assert IntervalRewriteSystem.verify_local_confluence(scale=3, max_index=15)

    iv = DyadicInterval(scale=4, index=7)
    norm, steps = IntervalRewriteSystem.normalize(iv)
    assert norm == DyadicInterval(scale=4, index=0)
    assert steps == 7


def test_finite_cover_profile() -> None:
    """Cover reports distinguish exact fields from float approximations."""
    reports = compute_cover_profile(max_scale=8)
    assert len(reports) == 8

    # Scale 1: 1 interval, resolution 1
    assert reports[0].scale == 1
    assert reports[0].cover_count == 1
    assert reports[0].approximate_log_ratio is None

    # Scale 8: covering number 255, resolution 1/128
    assert reports[7].scale == 8
    assert reports[7].cover_count == 255
    assert reports[7].resolution == Fraction(1, 128)

    # This finite approximate ratio is checked only at the declared scale.
    # For k = 8: log2(255) / 7 = 7.99435 / 7 = 1.142
    # For k = 12: log2(4095) / 11 = 11.9996 / 11 = 1.09
    ratio = reports[-1].approximate_log_ratio
    assert ratio is not None
    assert 1.0 < ratio < 1.25

    with pytest.raises(ValueError, match="max_scale must be >= 1"):
        compute_cover_profile(max_scale=0)
    with pytest.raises(TypeError, match="max_scale must be an integer"):
        compute_cover_profile(max_scale=2.0)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match=f"max_scale must be <= {MAX_COVER_SCALE}"):
        compute_cover_profile(max_scale=MAX_COVER_SCALE + 1)


def test_interval_movegraph_construction() -> None:
    """Interval movegraphs possess exactly the canonical cover intervals as states."""
    k = 3
    mg = create_interval_movegraph(scale=k)
    cover = IntervalCover.canonical(scale=k)

    assert mg.level == k
    assert mg.states == set(cover.intervals)
    # n_intervals = 7; 6 adjacent pairs * 2 directions = 12 directed edges
    assert len(mg.edges) == 12

    # Verify edge attributes
    expected_mu1 = Fraction(1, 1 << k)
    expected_mu2 = Fraction(1, 1 << (2 * k))
    for e in mg.edges:
        assert isinstance(e.source, DyadicInterval)
        assert isinstance(e.target, DyadicInterval)
        assert e.source.overlaps(e.target)
        assert e.mu1 == expected_mu1
        assert e.mu2 == expected_mu2

    with pytest.raises(ValueError, match="scale must be integer >= 1"):
        create_interval_movegraph(scale=0)


def test_interval_traversal_pricing() -> None:
    """Traversal pricing across canonical interval covers respects length bound < 1."""
    for k in (1, 2, 3, 5):
        mg = create_interval_movegraph(scale=k)
        cover = IntervalCover.canonical(scale=k)
        n = len(cover.intervals)
        steps = n - 1

        # Traverse from first to last interval
        curr_price_mu1 = Fraction(0, 1)
        curr_price_mu2 = Fraction(0, 1)
        for i in range(steps):
            u = cover.intervals[i]
            v = cover.intervals[i + 1]
            out_edges = [e for e in mg.outgoing(u) if e.target == v]
            assert len(out_edges) == 1
            curr_price_mu1 += out_edges[0].mu1
            curr_price_mu2 += out_edges[0].mu2

        expected_mu1 = Fraction(steps, 1 << k)
        expected_mu2 = Fraction(steps, 1 << (2 * k))
        assert curr_price_mu1 == expected_mu1
        assert curr_price_mu2 == expected_mu2

        # Primary cost is strictly bounded by 1
        assert curr_price_mu1 < Fraction(1, 1)
        # Dissipation decreases exponentially with scale
        assert curr_price_mu2 <= Fraction(1, 1 << k)


def test_interval_coarsening_morphism() -> None:
    """Coarsening projection between interval movegraphs satisfies graph morphism properties."""
    coarse_k = 2
    fine_k = 3
    cmap = create_interval_coarsening_map(coarse_scale=coarse_k, fine_scale=fine_k)
    fine_mg = create_interval_movegraph(scale=fine_k)
    coarse_mg = create_interval_movegraph(scale=coarse_k)

    assert cmap.source_level == fine_k
    assert cmap.target_level == coarse_k

    # Check morphism condition: for every fine edge u -> v,
    # either pi(u) == pi(v) (collapse) or pi(u) -> pi(v) is an edge in coarse_mg
    res = cmap.check_morphism(fine_mg, coarse_mg)
    assert res.is_valid

    with pytest.raises(ValueError, match="coarse_scale must be int >= 1"):
        create_interval_coarsening_map(0, 2)
    with pytest.raises(ValueError, match="fine_scale must be int >= coarse_scale"):
        create_interval_coarsening_map(3, 2)


def test_cross_scale_cover_analysis() -> None:
    """Finite cover analysis verifies the declared recurrence and cost bounds."""
    analysis = analyze_cross_scale_cover(max_scale=6)
    assert analysis.max_scale == 6
    assert len(analysis.scale_reports) == 6
    assert len(analysis.growth_ratios) == 5
    assert analysis.approximate_log_ratios[0] is None

    # Check the exact finite recurrence N(k+1) = 2N(k) + 1.
    for i in range(5):
        n_k = analysis.scale_reports[i].cover_count
        n_k1 = analysis.scale_reports[i + 1].cover_count
        assert n_k1 == 2 * n_k + 1
        assert analysis.growth_ratios[i] == Fraction(n_k1, n_k)

    # All primary traversal costs strictly < 1
    for mu1 in analysis.total_mu1_costs:
        assert mu1 < Fraction(1, 1)

    # Dissipation strictly monotonically decreasing for k >= 2 (non-trivial traversals)
    for i in range(1, len(analysis.total_mu2_costs) - 1):
        assert analysis.total_mu2_costs[i + 1] < analysis.total_mu2_costs[i]

    # Approximate log ratio at this finite endpoint; no limiting claim.
    endpoint_ratio = analysis.approximate_log_ratios[-1]
    assert endpoint_ratio is not None
    assert 1.0 <= endpoint_ratio < 1.3

    with pytest.raises(ValueError, match="max_scale must be >= 1"):
        analyze_cross_scale_cover(0)

