"""Deterministic mirror of ``lean4/Derivation/WeightProfile.lean``.

This is finite ``Nat``/``Int`` arithmetic.  It checks the positive
weight-profile relation, an explicit duplicate-free carrier policy,
unsigned-square determination, one declared signed-square/mixing
witness, and the exact two-coordinate descent classification.  It is
not a vector-space construction, a dynamics, or a uniqueness result.
"""

from __future__ import annotations

from itertools import product

from derivation.export import Json

Weights = dict[int, int]


def carrier_list(carrier: tuple[int, ...]) -> bool:
    """Carrier-facing reports require each label exactly once."""
    return len(carrier) == len(set(carrier))


def total(carrier: tuple[int, ...], w: Weights) -> int:
    """Raw list total; repeated labels count with multiplicity."""
    return sum(w.get(p, 0) for p in carrier)


def same_profile(carrier: tuple[int, ...], w: Weights,
                 v: Weights) -> bool:
    """Same normalized profile, cross-multiplied - no division."""
    tw, tv = total(carrier, w), total(carrier, v)
    return all(w.get(p, 0) * tv == v.get(p, 0) * tw for p in carrier)


def scale(w: Weights, a: int) -> Weights:
    return {p: a * x for p, x in w.items()}


def same_ray(carrier: tuple[int, ...], w: Weights, v: Weights,
             bound: int) -> bool:
    """Exists a positive pair (a, b) below the bound with
    a*w == b*v pointwise."""
    return any(
        all(a * w.get(p, 0) == b * v.get(p, 0) for p in carrier)
        for a in range(1, bound + 1) for b in range(1, bound + 1))


def all_weights(carrier: tuple[int, ...],
                maxw: int) -> list[Weights]:
    return [dict(zip(carrier, vals))
            for vals in product(range(maxw + 1), repeat=len(carrier))]


def profile_report(size: int, maxw: int, ray_bound: int
                   ) -> dict[str, Json]:
    """Equivalence, ray classification, support, order, and the
    forgotten total - exhaustive over the declared bounds."""
    carrier = tuple(range(size))
    assert carrier_list(carrier)
    ws = [w for w in all_weights(carrier, maxw)
          if total(carrier, w) > 0]
    refl = all(same_profile(carrier, w, w) for w in ws)
    symm = all(same_profile(carrier, w, v) == same_profile(carrier, v, w)
               for w in ws for v in ws)
    trans = all(
        (not (same_profile(carrier, w, v) and same_profile(carrier, v, u)))
        or same_profile(carrier, w, u)
        for w in ws for v in ws for u in ws)
    scale_inv = all(
        same_profile(carrier, scale(w, a), w)
        for w in ws for a in range(1, ray_bound + 1))
    positive_scale_stays_positive = all(
        total(carrier, scale(w, a)) > 0
        for w in ws for a in range(1, ray_bound + 1))
    zero_scale_raw_profile = all(
        same_profile(carrier, scale(w, 0), w) for w in ws)
    zero_scale_exits_domain = all(
        total(carrier, scale(w, 0)) == 0 for w in ws)
    ray_iff = all(
        same_profile(carrier, w, v)
        == same_ray(carrier, w, v, max(total(carrier, w),
                                       total(carrier, v)))
        for w in ws for v in ws)
    support = all(
        (w.get(p, 0) == 0) == (v.get(p, 0) == 0)
        for w in ws for v in ws if same_profile(carrier, w, v)
        for p in carrier)
    order = all(
        (w.get(p, 0) <= w.get(q, 0)) == (v.get(p, 0) <= v.get(q, 0))
        for w in ws for v in ws if same_profile(carrier, w, v)
        for p in carrier for q in carrier)
    forgets_total = any(
        same_profile(carrier, w, v)
        and total(carrier, w) != total(carrier, v)
        for w in ws for v in ws)
    return {
        "assignments_checked": len(ws),
        "equivalence": {"refl": refl, "symm": symm, "trans": trans},
        "scaling_invariant": scale_inv,
        "positive_scale_stays_positive": positive_scale_stays_positive,
        "zero_scale_raw_profile": zero_scale_raw_profile,
        "zero_scale_exits_positive_domain": zero_scale_exits_domain,
        "classes_are_exactly_rays": ray_iff,
        "support_preserved": support,
        "order_preserved": order,
        "total_is_forgotten": forgets_total,
    }


# ---------------------------------------------------------------------------
# The decorated presentation and what it adds

def sq(x: int) -> int:
    return x * x


def presents(carrier: tuple[int, ...], c: Weights,
             w: Weights) -> bool:
    """``c`` is a decorated presentation of ``w`` under squaring."""
    return carrier_list(carrier) and all(
        sq(c.get(p, 0)) == w.get(p, 0) for p in carrier)


def mix_sum(carrier: tuple[int, ...], c: Weights) -> int:
    """A declared MIXING read-out: the modulus of the combined
    decoration.  Declared, exactly like the modulus itself."""
    return sq(sum(c.get(p, 0) for p in carrier))


def unsigned_decoration_determined(carrier: tuple[int, ...],
                                   maxc: int) -> bool:
    """Over UNSIGNED decorations the modulus determines the
    decoration: squaring is injective on counts, so a decorated
    presentation adds no independent carrierwise datum in this
    square-presentation model."""
    return all(
        (sq(a) != sq(b)) or a == b
        for a in range(maxc + 1) for b in range(maxc + 1))


def signed_mixing_separates() -> dict[str, Json]:
    """One declared two-coordinate signed-square/mixing witness."""
    carrier = (0, 1)
    plus = {0: 1, 1: 1}
    split = {0: 1, 1: -1}
    weights = {0: 1, 1: 1}
    return {
        "carrier_is_duplicate_free": carrier_list(carrier),
        "both_present_same_integer_square_weights": (
            all(sq(plus[p]) == weights[p] for p in carrier)
            and all(sq(split[p]) == weights[p] for p in carrier)),
        "presentations_differ": plus != split,
        "declared_mixing_separates": (
            mix_sum(carrier, plus) != mix_sum(carrier, split)),
        "scope": "two integer coordinates, the declared square map, "
                 "and this declared mixing read-out only",
    }


def presentation_report(size: int, maxc: int) -> dict[str, Json]:
    """Redundancy for the profile question, visibility to the mixing
    question - both exhaustive over the declared bounds."""
    carrier = tuple(range(size))
    cs = [dict(zip(carrier, vals))
          for vals in product(range(maxc + 1), repeat=size)]
    cs = [c for c in cs if total(carrier, {p: sq(c[p])
                                           for p in carrier}) > 0]
    redundant = True
    for c in cs:
        w = {p: sq(c[p]) for p in carrier}
        if not presents(carrier, c, w):
            redundant = False
        if not same_profile(carrier, w, w):
            redundant = False
    # over UNSIGNED decorations no pair with equal pointwise moduli
    # can differ at all - squaring is injective on counts
    unsigned_pairs_differing = [
        (c, d) for c in cs for d in cs
        if all(sq(c[p]) == sq(d[p]) for p in carrier) and c != d]
    return {
        "decorations_checked": len(cs),
        "profile_redundant_for_every_decoration": redundant,
        "unsigned_decoration_determined":
            unsigned_decoration_determined(carrier, maxc),
        "unsigned_pairs_with_equal_moduli_that_differ":
            len(unsigned_pairs_differing),
        "signed_square_fixture": signed_mixing_separates(),
        "scope": "unsigned square presentations are carrierwise "
                 "determined; a separate integer-square fixture has "
                 "two sign choices seen by one declared mixing read-out",
    }


# ---------------------------------------------------------------------------
# Descent classification for declared linear read-outs

def read_out(a: int, b: int, x: int, y: int) -> int:
    return a * x + b * y


def descends(a: int, b: int, bound: int) -> bool:
    """Is the squared read-out constant on modulus-blind inputs?"""
    vals = range(-bound, bound + 1)
    for x, y, x2, y2 in product(vals, repeat=4):
        if x * x == x2 * x2 and y * y == y2 * y2:
            if (sq(read_out(a, b, x, y))
                    != sq(read_out(a, b, x2, y2))):
                return False
    return True


def descent_report(coeff_bound: int, input_bound: int
                   ) -> dict[str, Json]:
    """The classification: descent holds exactly when the cross term
    vanishes."""
    rows = []
    classified = True
    for a in range(-coeff_bound, coeff_bound + 1):
        for b in range(-coeff_bound, coeff_bound + 1):
            d = descends(a, b, input_bound)
            if d != (a * b == 0):
                classified = False
            rows.append({"a": a, "b": b, "descends": d,
                         "cross_term_zero": a * b == 0})
    return {
        "coefficient_bound": coeff_bound,
        "input_bound": input_bound,
        "rows_checked": len(rows),
        "descent_iff_cross_term_zero": classified,
        "sign_gap_identity": all(
            sq(a + b) == sq(a - b) + 4 * (a * b)
            for a in range(-coeff_bound, coeff_bound + 1)
            for b in range(-coeff_bound, coeff_bound + 1)),
    }


# ---------------------------------------------------------------------------
# Audit of the proposed climb

def climb_report() -> dict[str, Json]:
    """Two former imports are elementary; the third schema is false."""
    singleton = (0,)
    one = {0: 1}
    zero_readout = 0
    return {
        "decorated_carrier_shape": {
            "status": "PROVABLE_TRIVIALLY",
            "witness": "D=Nat, modulus=identity, operation=addition",
        },
        "list_append_additivity": {
            "status": "PROVED_FROM_TOTAL_DEFINITION",
            "overlap_policy": "repeated labels count with multiplicity",
        },
        "claimed_readout_uniqueness": {
            "status": "FALSE_WITH_COUNTERMODEL",
            "zero_readout": zero_readout,
            "positive_singleton_total": total(singleton, one),
            "reason": "the zero read-out is profile-invariant and "
                      "append-additive but differs from positive total",
        },
        "status": "NO_PRICED_CLIMB_DERIVED",
    }


def weight_profile_report(size: int, maxw: int, maxc: int,
                          coeff_bound: int, input_bound: int
                          ) -> dict[str, Json]:
    return {
        "bounds": {
            "carrier_size": size,
            "max_weight": maxw,
            "max_decoration": maxc,
            "coefficient_bound": coeff_bound,
            "input_bound": input_bound,
            "ray_search_bound": maxw * size + 1,
        },
        "profile": profile_report(size, maxw, maxw * size + 1),
        "presentation": presentation_report(size, maxc),
        "descent": descent_report(coeff_bound, input_bound),
        "climb": climb_report(),
        "claim_ceiling":
            "finite Nat/Int weight profiles; one declared signed-square "
            "mixing witness; no vector-space, dynamics, probability, "
            "uniqueness, or representation-lift claim",
    }
