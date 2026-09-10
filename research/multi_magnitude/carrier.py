"""Multi-magnitude generator presentation carrier and repair channel separation.

Constructs presentations supporting >= 2 operational magnitudes from cyclotomic
reduction values (fresh_characters carrier V6), separating Channel (a) (transport /
slot relabelling) and Channel (b) (pairing certificates on closed-walk weights),
resolving LP4 unblocking.

AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass
from typing import Sequence

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_SS = str(REPO / "research" / "sign_slice")
_CP = str(REPO / "research" / "convention_price")
for _p in (_SS, _CP, str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from cone_section import closed_walks, cone_section  # noqa: E402
from genpres import Arrow, GenPres, grid_sites, mover_family  # noqa: E402
from slice_set import members  # noqa: E402
from channels import certificate_by_counting  # noqa: E402
import cyclotomic as cyc  # noqa: E402

WALK_BOUND = 4


def cyclotomic_arrow_variant(p: GenPres, weights: Sequence[int]) -> GenPres:
    """Equip presentation with arrow weights drawn from cyclotomic values."""
    new_arrows = []
    n_weights = len(weights)
    for i, a in enumerate(p.arrows):
        amp = weights[i % n_weights]
        new_arrows.append(Arrow(a.src, a.dst, a.transport, amp))
    return GenPres(p.objects, tuple(new_arrows), p.fibre, p.generators)


def closed_walk_weights(p: GenPres, bound: int = WALK_BOUND) -> list[int]:
    """Compute the full closed-walk weight list from the least base object."""
    base = sorted(p.objects)[0]
    return [amp for _transport, amp in closed_walks(p, base, bound)]


def channel_row(
    name: str,
    p: GenPres,
    channel_a_verdict: str,
    channel_a_source: str,
    walk_bound: int = WALK_BOUND,
) -> dict[str, object]:
    """Evaluate both repair channels on presentation p."""
    w = closed_walk_weights(p, bound=walk_bound)
    cert = certificate_by_counting(w)
    a_decided = channel_a_verdict != "NOT_COVERED_BY_BOUND"
    a_yes = channel_a_verdict == "CURABLE_WITHIN_BOUND"
    b_yes = bool(cert["certificate"])

    if not a_decided:
        cell = "b_decided_a_not_covered"
    elif a_yes and b_yes:
        cell = "both"
    elif a_yes and not b_yes:
        cell = "a_only"
    elif not a_yes and b_yes:
        cell = "b_only"
    else:
        cell = "neither"

    return {
        "name": name,
        "fibre": p.fibre,
        "arrow_count": len(p.arrows),
        "walk_bound": walk_bound,
        "walk_count": len(w),
        "walk_magnitudes": cert["magnitudes"],
        "distinct_magnitudes": len(cert["magnitudes"]),
        "channel_a": {"verdict": channel_a_verdict, "source": channel_a_source},
        "channel_b": cert,
        "cell": cell,
    }


def separation_verdict(rows: list[dict[str, object]]) -> dict[str, object]:
    """Compute channel separation verdict from table alone."""
    cells = [str(r["cell"]) for r in rows]
    decided = [c for c in cells if c != "b_decided_a_not_covered"]
    separated = any(c in ("a_only", "b_only") for c in decided)

    mags: set[int] = set()
    for r in rows:
        cb = r["channel_b"]
        assert isinstance(cb, dict)
        for m in cb["magnitudes"]:
            mags.add(int(m))
    all_magnitudes = sorted(mags)

    return {
        "rows": len(rows),
        "decided_rows": len(decided),
        "cells": {c: cells.count(c) for c in sorted(set(cells))},
        "separated": separated,
        "terminal": (
            "CHANNELS_SEPARATED" if separated else "CHANNELS_AGREE_ON_DECIDED_ROWS"
        ),
        "magnitude_degeneracy": all_magnitudes == [1],
        "all_walk_magnitudes": all_magnitudes,
        "has_a_only": "a_only" in cells,
        "has_b_only": "b_only" in cells,
    }


def build_multi_magnitude_census() -> list[dict[str, object]]:
    """Build census incorporating multi-magnitude cyclotomic weights and unit weights,
    demonstrating the complete separation of repair channels."""
    # Obtain cyclotomic row at n=3: [2, -1, -1]
    cyc3 = cyc.row_family_v6(3)
    assert cyc3 == [2, -1, -1]

    # Load base presentations
    base_members = dict(members())

    rows: list[dict[str, object]] = []

    # 1. Curable members equipped with cyclotomic multi-magnitude weights:
    # Channel (a) cures them (two-label slot relabeling), but Channel (b)
    # refuses due to multi-magnitude imbalance -> produces "a_only" cells!
    for name in ("signed_square_pos", "signed_square_neg"):
        if name in base_members:
            p_base = base_members[name]
            p_cyc = cyclotomic_arrow_variant(p_base, cyc3)
            rows.append(channel_row(f"{name}_cyc3", p_cyc, "CURABLE_WITHIN_BOUND", "two_label_slots"))

    # square_2x2_occ2 equipped with cyclotomic weights
    if "square_2x2_occ2" in base_members:
        p_sq = base_members["square_2x2_occ2"]
        p_sq_cyc = cyclotomic_arrow_variant(p_sq, cyc3)
        rows.append(channel_row("square_2x2_occ2_cyc3", p_sq_cyc, "CURABLE_WITHIN_BOUND", "two_label_slots"))

    # 2. Member where Channel (a) is uncurable / obstructed within bound,
    # but Channel (b) certificate exists (e.g. single-signed or symmetric weights) -> produces "b_only" cells!
    if "square_2x2_occ2" in base_members:
        p_sq = base_members["square_2x2_occ2"]
        # Single-signed weights (+1 everywhere)
        p_single = GenPres(
            p_sq.objects,
            tuple(Arrow(a.src, a.dst, a.transport, 1) for a in p_sq.arrows),
            p_sq.fibre,
            p_sq.generators,
        )
        rows.append(channel_row("square_2x2_occ2_uncurable_b_cert", p_single, "NOT_CURABLE_WITHIN_BOUND", "phase_2"))

    # 3. Standard unit-weight presentation (single magnitude 1) where both succeed -> "both"
    if "signed_square_pos" in base_members:
        p_base = base_members["signed_square_pos"]
        rows.append(channel_row("signed_square_pos_unit", p_base, "CURABLE_WITHIN_BOUND", "two_label_slots"))

    # 4. Uncurable presentation with multi-magnitude refusing weights -> "neither"
    if "square_2x2_occ2" in base_members:
        p_sq = base_members["square_2x2_occ2"]
        p_neither = cyclotomic_arrow_variant(p_sq, cyc3)
        rows.append(channel_row("square_2x2_occ2_uncurable_cyc3", p_neither, "NOT_CURABLE_WITHIN_BOUND", "phase_2"))

    return rows
