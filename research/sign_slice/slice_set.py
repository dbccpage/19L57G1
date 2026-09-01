"""SliceSet: the finite declared census.  FW-SET: this is a declared
slice; totality is refused, not enumerated.

Bounds, declared: at most 6 objects per member; at most 8 site hops
for reconstructed families; fibres arise from occupancies 2 and 3;
weightings are unit (all amps 1) or signed (amps in {-1, +1}).  The
occupancy-2 ladder family exceeds the object bound (15 objects) and is
REFUSED by name.  AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib

from genpres import (
    GenPres,
    chain_sites,
    grid_sites,
    iso_key,
    mover_family,
    mu_g,
    star_sites,
)

OBJECT_BOUND = 6
SITE_HOP_BOUND = 8

TRIANGLE = [(0, 1), (1, 2), (0, 2)]
SQUARE_PLUS_EDGE = grid_sites(2, 2) + [(0, 3)]
PAN_C3_TAIL = [(0, 1), (1, 2), (0, 2), (2, 3)]


def members() -> list[tuple[str, GenPres]]:
    """The declared census, in declared order."""

    out: list[tuple[str, GenPres]] = [
        ("chain_P4_occ2", mover_family(4, chain_sites(4), 2, signed=False)),
        ("square_2x2_occ2", mover_family(4, grid_sites(2, 2), 2, signed=False)),
        ("star_K13_occ2", mover_family(4, star_sites(3), 2, signed=False)),
        ("triangle_C3_occ2", mover_family(3, TRIANGLE, 2, signed=False)),
        ("square_plus_edge_occ2", mover_family(4, SQUARE_PLUS_EDGE, 2, signed=False)),
        ("pan_C3_tail_occ2", mover_family(4, PAN_C3_TAIL, 2, signed=False)),
        ("chain_P4_occ3", mover_family(4, chain_sites(4), 3, signed=False)),
        ("square_2x2_occ3", mover_family(4, grid_sites(2, 2), 3, signed=False)),
        ("star_K13_occ3", mover_family(4, star_sites(3), 3, signed=False)),
        ("square_plus_edge_occ3", mover_family(4, SQUARE_PLUS_EDGE, 3, signed=False)),
        ("signed_square_pos", mover_family(4, grid_sites(2, 2), 2, signed=True)),
        ("signed_square_neg", _negated(mover_family(4, grid_sites(2, 2), 2, signed=True))),
    ]
    for name, p in out:
        if len(p.objects) > OBJECT_BOUND:
            raise ValueError(f"census member {name} violates the object bound")
    return out


def _negated(p: GenPres) -> GenPres:
    """The sign partner: every amp negated.  Squared amps agree with
    the original; the declared mixing read-out separates the pair."""

    from genpres import Arrow

    return GenPres(
        p.objects,
        tuple(Arrow(a.src, a.dst, a.transport, -a.amp) for a in p.arrows),
        p.fibre,
        p.generators,
    )


def refused() -> list[tuple[str, str]]:
    """Members refused by the declared bounds, by name (FW-SET held by
    refusing rather than extrapolating)."""

    ladder_objects = 15  # C(6, 2): the occupancy-2 family over 6 sites
    return [
        (
            "ladder_2x3_occ2",
            f"REFUSED: {ladder_objects} objects exceeds the declared bound"
            f" of {OBJECT_BOUND}",
        )
    ]


def mixing(p: GenPres, q: GenPres) -> int:
    """The declared mixing read-out on an amp-tuple pair: the sum of
    squared amp sums, arrow by arrow (DECLARED_POLICY)."""

    return sum((a.amp + b.amp) ** 2 for a, b in zip(p.arrows, q.arrows, strict=True))


def squares(p: GenPres) -> list[int]:
    return [a.amp**2 for a in p.arrows]


def census() -> list[dict[str, object]]:
    """Classify every member by the predicate."""

    from cone_section import cone_section

    rows: list[dict[str, object]] = []
    for name, p in members():
        rows.append(
            {
                "name": name,
                "objects": len(p.objects),
                "arrows": len(p.arrows),
                "fibre": p.fibre,
                "mu_g": list(mu_g(p)),
                "iso_key_sha8": hashlib.sha256(
                    iso_key(p).encode("ascii")
                ).hexdigest()[:8],
                "sectioned": cone_section(p),
            }
        )
    return rows
