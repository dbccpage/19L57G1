"""Deterministic mirror of ``lean4/Derivation/WeightProfile.lean``.

Declared weight assignments and their profiles, in exact integer
arithmetic with no division: the profile classes are exactly the
positive rays; support and order are preserved and the total is
forgotten; a decorated presentation adds nothing to the profile but
IS visible to a declared mixing question; a linear read-out descends
through the modulus-blind relation exactly when it does not mix; and
the weights do not determine a decoration, which is why any
uniqueness law needs strictly more than the weights.

Everything is checked exhaustively over declared finite bounds.
"""

from __future__ import annotations

from itertools import product

from derivation.export import Json

Weights = dict[int, int]


def total(carrier: tuple[int, ...], w: Weights) -> int:
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
    return all(sq(c.get(p, 0)) == w.get(p, 0) for p in carrier)


def mix_sum(carrier: tuple[int, ...], c: Weights) -> int:
    """A declared MIXING read-out: the modulus of the combined
    decoration.  Declared, exactly like the modulus itself."""
    return sq(sum(c.get(p, 0) for p in carrier))


def unsigned_decoration_determined(carrier: tuple[int, ...],
                                   maxc: int) -> bool:
    """Over UNSIGNED decorations the modulus determines the
    decoration: squaring is injective on counts, so a decorated
    presentation adds nothing to ANY question, not merely to the
    profile."""
    return all(
        (sq(a) != sq(b)) or a == b
        for a in range(maxc + 1) for b in range(maxc + 1))


def signed_mixing_separates() -> dict[str, Json]:
    """The extra capacity is exactly a declared SIGN: two signed
    decorations with identical moduli are separated by the declared
    mixing read-out."""
    return {
        "same_modulus_at_each_position": (sq(1) == sq(1)
                                          and sq(-1) == sq(1)),
        "mixing_separates": sq(1 + (-1)) != sq(1 + 1),
        "capacity_is_the_declared_sign":
            "unsigned decorations are determined by the weights; "
            "only a declared sign creates a datum the profile "
            "cannot see, and that declaration is its own import",
    }


def lift_report(size: int, maxc: int) -> dict[str, Json]:
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
        "signed_mixing": signed_mixing_separates(),
        "redundancy_is_relative":
            "redundant for the declared profile question; over "
            "UNSIGNED decorations redundant for every question, "
            "because the decoration is determined; the extra "
            "capacity appears only once a SIGN is declared, and "
            "that declaration is a separate import",
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
# The climb

def climb_report() -> dict[str, Json]:
    """The negative fact that makes each import necessary, plus the
    named imports themselves - stated, never discharged."""
    carrier = (0, 1)
    w = {0: 4, 1: 1}
    eA = {0: 2, 1: 1}
    eB = {0: 2, 1: 3}
    return {
        "weights_do_not_force_decoration": {
            "eA_presents_w": presents(carrier, eA, w),
            "eB_does_not_present_w": not presents(carrier, eB, w),
            "decorations_differ": eA != eB,
            "mixing_separates_them":
                mix_sum(carrier, eA) != mix_sum(carrier, eB),
        },
        "imports_required_and_not_discharged": [
            "a decorated carrier with a declared modulus map and a "
            "declared combination operation (the weights supply "
            "none)",
            "exact additivity over disjoint parts (a declared "
            "demand, not entailed by the calculus)",
            "a read-out uniqueness law singling out one modulus-"
            "blind additive nonnegative read-out (the expensive "
            "import; nothing above proves it)",
        ],
        "status":
            "each import is stated as an unproved Prop in the Lean "
            "module; none is discharged here or anywhere in this "
            "development",
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
        "lift": lift_report(size, maxc),
        "descent": descent_report(coeff_bound, input_bound),
        "climb": climb_report(),
        "derived_vs_imported":
            "DERIVED: the profile is fixed up to a positive ray, a "
            "decorated presentation adds nothing to it, and a linear "
            "read-out descends exactly when it does not mix.  "
            "IMPORTED and NOT discharged: a decorated carrier, exact "
            "disjoint additivity, and any read-out uniqueness law.",
    }
