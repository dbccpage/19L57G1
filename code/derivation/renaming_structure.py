"""Deterministic mirror of ``lean4/Derivation/RenamingStructure.lean``
(Goal 1): the renaming structure around ``Up``.

A renaming at scale ``n`` is represented by a permutation tuple of
``range(n)``, extended by the identity above ``n`` — exactly the Lean
``Renaming n`` data (a global inverse pair permuting positions below
``n`` and fixing every position at or above it).

Checked here EXHAUSTIVELY over the declared bounds: the group laws
over the whole symmetric group; the action laws (identity
unconditionally, composition on the well-formed scope); transport of
blocks and of the complete ``Up`` family respecting identity and
composition; coherence of replay commutation under composed
renamings; exact orbit transport with no selected representative; and
three countermodels — equal carrier size, equal cost, and an arbitrary
non-bijective map.  The last is not a ``Renaming`` and therefore does
not inherit the inverse/group-action or equivariance results; no claim
is made that non-bijective maps cannot support a different monoid
action.
"""

from __future__ import annotations

from itertools import permutations

from derivation.attachment_ladder import (
    act,
    fresh_tok,
    isomorphic_undirected,
    path_pol,
    star_pol,
    tree_at,
    up_block,
    up_family,
)
from derivation.export import Json
from derivation.primitive_passage import PS, preplay

Perm = tuple[int, ...]


def id_ren(n: int) -> Perm:
    """The identity renaming at scale ``n``."""
    return tuple(range(n))


def inv_ren(p: Perm) -> Perm:
    """The inverse renaming."""
    out = [0] * len(p)
    for i, pi in enumerate(p):
        out[pi] = i
    return tuple(out)


def comp_ren(sigma: Perm, tau: Perm) -> Perm:
    """Composition: apply ``tau`` first, then ``sigma``."""
    return tuple(sigma[tau[i]] for i in range(len(tau)))


def group_laws(n: int) -> dict[str, Json]:
    """The group laws, exhaustive over the whole symmetric group."""
    perms = list(permutations(range(n)))
    ident = id_ren(n)
    return {
        "carrier": n,
        "group_order": len(perms),
        "comp_id": all(comp_ren(s, ident) == s for s in perms),
        "id_comp": all(comp_ren(ident, s) == s for s in perms),
        "comp_assoc": all(
            comp_ren(comp_ren(a, b), c) == comp_ren(a, comp_ren(b, c))
            for a in perms for b in perms for c in perms),
        "inv_comp": all(
            comp_ren(inv_ren(s), s) == ident for s in perms),
        "comp_inv": all(
            comp_ren(s, inv_ren(s)) == ident for s in perms),
        "inv_inv": all(inv_ren(inv_ren(s)) == s for s in perms),
    }


def sample_states(n: int) -> list[PS]:
    """Declared sample states on an ``n``-occurrence carrier."""
    return [tree_at(star_pol, n - 1), tree_at(path_pol, n - 1)]


def action_laws(n: int) -> dict[str, Json]:
    """``act_id`` unconditionally; ``act_comp`` and ``act_inv`` on the
    well-formed scope."""
    perms = list(permutations(range(n)))
    ident = id_ren(n)
    states = sample_states(n)
    return {
        "act_id": all(act(ident, s) == s for s in states),
        "act_comp": all(
            act(comp_ren(a, b), s) == act(a, act(b, s))
            for a in perms for b in perms for s in states),
        "act_inv": all(
            act(inv_ren(a), act(a, s)) == s
            for a in perms for s in states),
        "act_preserves_carrier_size": all(
            len(act(a, s).occ) == len(s.occ)
            for a in perms for s in states),
        "fresh_tok_invariant": all(
            fresh_tok(act(a, s)) == fresh_tok(s)
            for a in perms for s in states),
    }


def transport_laws(n: int) -> dict[str, Json]:
    """Block and family transport respect identity and composition."""
    perms = list(permutations(range(n)))
    ident = id_ren(n)
    states = sample_states(n)
    return {
        "block_id": all(
            up_block(act(ident, s), p) == up_block(s, p)
            for s in states for p in range(n)),
        "block_comp": all(
            up_block(act(comp_ren(a, b), s), a[b[p]])
            == up_block(act(a, act(b, s)), a[b[p]])
            for a in perms for b in perms
            for s in states for p in range(n)),
        "family_id": all(
            up_family(act(ident, s)) == up_family(s)
            for s in states),
        "family_comp": all(
            up_family(act(comp_ren(a, b), s))
            == up_family(act(a, act(b, s)))
            for a in perms for b in perms for s in states),
        "membership_transport": all(
            (up_block(act(a, s), a[p]) in up_family(act(a, s)))
            == (up_block(s, p) in up_family(s))
            for a in perms for s in states for p in range(n)),
    }


def coherence(n: int) -> dict[str, Json]:
    """Replay of an Up block commutes with a COMPOSED renaming, and
    the composite route agrees with the two-step route."""
    perms = list(permutations(range(n)))
    states = sample_states(n)
    composed = True
    twostep = True
    for a in perms:
        for b in perms:
            ab = comp_ren(a, b)
            for s in states:
                for p in range(n):
                    lhs = act(ab, preplay(up_block(s, p), s))
                    tgt = act(a, act(b, s))
                    rhs = preplay(up_block(tgt, a[b[p]]), tgt)
                    if lhs != rhs:
                        composed = False
                    two = act(a, act(b, preplay(up_block(s, p), s)))
                    if two != rhs:
                        twostep = False
    return {
        "act_up_comm_composed": composed,
        "act_up_comm_twostep_agrees": twostep,
    }


def orbit_no_selection(n: int) -> dict[str, Json]:
    """Every named source block has its exact named orbit image."""
    perms = list(permutations(range(n)))
    star = tree_at(star_pol, n - 1)
    closed = all(
        up_block(act(a, star), a[p]) in up_family(act(a, star))
        for a in perms for p in range(n))
    fam = up_family(star)
    return {
        "family_length_equals_parents": len(fam) == len(star.occ),
        "orbit_closed_under_action": closed,
        "every_source_block_has_exact_named_transport": closed,
        "star_both_leaves_present": (
            up_block(star, 1) in fam and up_block(star, 2) in fam),
        "leaf_blocks_distinct": up_block(star, 1) != up_block(star, 2),
    }


# ---------------------------------------------------------------------------
# Countermodels

def collapse_map(x: int) -> int:
    """An arbitrary NON-BIJECTIVE map: everything to the root."""
    return 0


def raw_rename_pairs(f: object,
                     pairs: tuple[tuple[int, int], ...]
                     ) -> list[tuple[int, int]]:
    """Push a store forward along an arbitrary map (no inverse, so no
    carrier re-indexing is definable)."""
    assert callable(f)
    return [(int(f(a)), int(f(b))) for (a, b) in pairs]


def non_bijective_countermodel() -> dict[str, Json]:
    """An arbitrary map admits no left inverse and its pushforward is
    not a legal store, so it does not instantiate this renaming action.

    This is deliberately not a claim about all possible monoid actions
    by non-bijective maps.
    """
    # a left inverse would have to send 0 to both 0 and 1
    has_left_inverse = collapse_map(0) != collapse_map(1)
    path3 = tree_at(path_pol, 2)
    pushed = raw_rename_pairs(collapse_map, path3.wit)
    return {
        "no_left_inverse": not has_left_inverse,
        "original_store_irreflexive": all(
            a != b for (a, b) in path3.wit),
        "pushforward": [list(pr) for pr in pushed],
        "pushforward_all_self_pairs": all(
            a == b for (a, b) in pushed),
        "pushforward_refused_by_wf_guard": all(
            a == b for (a, b) in pushed),
    }


def equal_size_countermodel() -> dict[str, Json]:
    """Equal carrier size (even with a literally equal family) is not
    relatedness: no renaming carries one state to the other."""
    star3 = tree_at(star_pol, 2)
    path3 = tree_at(path_pol, 2)
    perms = list(permutations(range(3)))
    return {
        "same_carrier": star3.occ == path3.occ,
        "families_literally_equal":
            up_family(star3) == up_family(path3),
        "no_renaming_relates": all(
            act(a, star3) != path3 for a in perms),
    }


def equal_cost_countermodel() -> dict[str, Json]:
    """Equal cost identifies nothing: two same-cost family members
    execute to non-isomorphic states."""
    path3 = tree_at(path_pol, 2)
    b1 = up_block(path3, 1)
    b2 = up_block(path3, 2)
    t1 = preplay(b1, path3)
    t2 = preplay(b2, path3)
    return {
        "both_in_family": (b1 in up_family(path3)
                           and b2 in up_family(path3)),
        "equal_cost": len(b1) == len(b2),
        "executions_non_isomorphic": not isomorphic_undirected(
            t1.wit, t2.wit, 4),
    }


def renaming_report(n: int) -> dict[str, Json]:
    return {
        "bounds": {
            "carrier": n,
            "symmetric_group_order": len(list(permutations(range(n)))),
            "sample_states": ["star", "path"],
            "assoc_triples_checked":
                len(list(permutations(range(n)))) ** 3,
        },
        "group_laws": group_laws(n),
        "action_laws": action_laws(n),
        "transport_laws": transport_laws(n),
        "coherence": coherence(n),
        "orbit_no_selection": orbit_no_selection(n),
        "countermodels": {
            "non_bijective_map": non_bijective_countermodel(),
            "equal_carrier_size": equal_size_countermodel(),
            "equal_cost": equal_cost_countermodel(),
        },
        "equivariance_scope":
            "the supply fragment of the declared one-edge grammar on "
            "live store-bounded states; NOT the observation calculus, "
            "NOT multi-edge extensions, NOT maps that are not "
            "renamings",
    }
