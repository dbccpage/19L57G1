"""ChannelTable: the fenced comparison, executed (FINITE_COMPUTATION).

Two repair channels on a shared signed census:

- channel (a), slot relabelling: curable within the phase-2 bound
  (two-label members, exhausted) or the phase-3 bound (the occupancy-3
  square); a member outside both bounds is NOT_COVERED_BY_BOUND, which
  is not a "no".
- channel (b), pairing certificate: the member's full closed-walk
  weight list at the declared length bound admits a decomposition into
  exact-opposite pairs plus a single-signed residual, decided by
  per-magnitude domination -- the sign-repair rung's proved exact
  characterization `certificate_iff_dominated` and its two constructive
  converses, cited as CONDITIONAL_THEOREM and reconstructed here as
  computation.  No walk is discarded: the pinned discard countermodel
  binds, so the list is the FULL enumeration from the declared least
  base object, trivial walk included.

The two channels are never treated as one repair: (a) reads
transports only, (b) reads amps only; the table records both and the
separation verdict is computed, not assumed.

Requires the pinned sign_slice modules on the path (`../sign_slice`).
AuthorityEffect: None.
"""

from __future__ import annotations

from cone_section import closed_walks
from genpres import Arrow, GenPres
from parity import perm_parity

WALK_BOUND = 6


def signed_variant(p: GenPres) -> GenPres:
    """The declared signed variant: amp -1 on parity-odd hops, +1
    elsewhere.  Transports are untouched."""

    return GenPres(
        p.objects,
        tuple(
            Arrow(a.src, a.dst, a.transport, -1 if perm_parity(a.transport) else 1)
            for a in p.arrows
        ),
        p.fibre,
        p.generators,
    )


def weight_list(p: GenPres) -> list[int]:
    """The FULL closed-walk amp list at the declared bound, from the
    least object, both traversal directions, trivial walk included."""

    base = sorted(p.objects)[0]
    return [amp for _transport, amp in closed_walks(p, base, WALK_BOUND)]


def certificate_by_counting(w: list[int]) -> dict[str, object]:
    """Per-magnitude domination on one side or the other: the pinned
    counting characterization, reconstructed."""

    magnitudes = sorted({abs(v) for v in w if v != 0})
    neg_dominated = all(
        sum(1 for v in w if v == -mag) <= sum(1 for v in w if v == mag)
        for mag in magnitudes
    )
    pos_dominated = all(
        sum(1 for v in w if v == mag) <= sum(1 for v in w if v == -mag)
        for mag in magnitudes
    )
    return {
        "certificate": neg_dominated or pos_dominated,
        "neg_dominated": neg_dominated,
        "pos_dominated": pos_dominated,
        "magnitudes": magnitudes,
    }


def row(
    name: str,
    p: GenPres,
    channel_a_verdict: str,
    channel_a_source: str,
) -> dict[str, object]:
    w = weight_list(p)
    cert = certificate_by_counting(w)
    a_decided = channel_a_verdict != "NOT_COVERED_BY_BOUND"
    a_yes = channel_a_verdict == "CURABLE_WITHIN_BOUND"
    b_yes = bool(cert["certificate"])
    if not a_decided:
        cell = "b_decided_a_not_covered"
    elif a_yes and b_yes:
        cell = "both"
    elif a_yes:
        cell = "a_only"
    elif b_yes:
        cell = "b_only"
    else:
        cell = "neither"
    return {
        "name": name,
        "arrow_amps_negative": sum(1 for a in p.arrows if a.amp < 0),
        "arrow_amps_positive": sum(1 for a in p.arrows if a.amp > 0),
        "walk_bound": WALK_BOUND,
        "walk_count": len(w),
        "walk_negative": sum(1 for v in w if v < 0),
        "walk_positive": sum(1 for v in w if v > 0),
        "channel_a": {"verdict": channel_a_verdict, "source": channel_a_source},
        "channel_b": cert,
        "cell": cell,
    }


def separation_verdict(rows: list[dict[str, object]]) -> dict[str, object]:
    """Computed from the table alone.  The separation claim is
    exhibited by an `a_only` or `b_only` cell among decided rows, and
    refused otherwise, with the table as the record."""

    cells = [str(r["cell"]) for r in rows]
    decided = [c for c in cells if c != "b_decided_a_not_covered"]
    separated = any(c in ("a_only", "b_only") for c in decided)
    mags: set[int] = set()
    for r in rows:
        cb = r["channel_b"]
        assert isinstance(cb, dict)
        for m in cb["magnitudes"]:
            assert isinstance(m, int)
            mags.add(m)
    all_magnitudes = sorted(mags)
    return {
        "rows": len(rows),
        "decided_rows": len(decided),
        "cells": {c: cells.count(c) for c in sorted(set(cells))},
        "separated": separated,
        "terminal": (
            "CHANNELS_SEPARATED"
            if separated
            else "CHANNELS_AGREE_ON_DECIDED_ROWS"
        ),
        "magnitude_degeneracy": all_magnitudes == [1],
        "all_walk_magnitudes": all_magnitudes,
    }
