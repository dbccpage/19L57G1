"""Deterministic mirror of ``lean4/Derivation/Attachment.lean`` and
``lean4/Derivation/LadderGeneral.lean`` (repaired pass).

Repairs mirrored here, matching the Lean modules:

1. **No silent clamping** — policies are lawful by construction
   (``lawful_to``), the retired clamp survives only as the recorded
   countermodel (``clamp_countermodel``), and an illegal parent
   meets a typed refusal (``attach_checked``), never a rewrite.
2. **Occurrence identity** — ``occ`` stores TOKENS in admission
   order; POSITIONS (indices) are the identities used by the
   relational stores.  The canonical fresh token is one past the
   maximum (``fresh_tok``); using the length as a token fails on
   non-initial carriers (``length_not_fresh_countermodel``).
3. **Registry-relative completeness** — membership in ``up_family``
   coincides with the declared one-edge grammar, checked in both
   directions (``up_report``).
4. **Genuine renaming action** — ``act`` re-indexes the carrier and
   renames every store; replay of Up blocks commutes with the
   action, checked over the FULL permutation group on the sample
   carriers; equal size (even a literally equal family) does not
   give renaming relatedness (``renaming_report``).
5. **Well-formed cells** — the generalized shell guard requires
   strict ascent; the legacy guard's ``[0, 0]`` pseudo-cell is the
   recorded countermodel; well-formedness is checked as a replayed
   invariant (``ladder_report``).

Imported (declared, not derived): fresh token supply, protection,
budget/activation, cell encoding, boundary signs, metatheoretic
driver iteration.
"""

from __future__ import annotations

from itertools import permutations
from typing import Callable, Optional

from derivation.export import Json
from derivation.primitive_passage import (
    GENESIS_P,
    PS,
    PEvent,
    preplay,
)

Policy = Callable[[int], int]
Pair = tuple[int, int]


# ---------------------------------------------------------------------------
# 1. Lawful policies and the typed refusal

def lawful_to(pi: Policy, rounds: int) -> bool:
    """The lawfulness certificate, checked over the used range —
    the Python analogue of ``LawfulPolicy.lawful``."""
    return all(pi(k + 1) <= k for k in range(rounds + 1))


def par(pi: Policy, k: int) -> int:
    """The parent of child ``k + 1`` — the choice itself,
    unrewritten (callers hold a ``lawful_to`` certificate)."""
    return pi(k + 1)


def clamped_par(c: Policy, k: int) -> int:
    """The retired clamp, kept only as the countermodel's
    exhibit."""
    return min(c(k + 1), k)


def bad_choice(i: int) -> int:
    """An illegal, unclamped choice: parent ``i + 7`` — never
    represented."""
    return i + 7


def clamp_countermodel() -> dict[str, Json]:
    """The clamp silently rewrote the illegal choice into the root's
    choice; the repaired path refuses instead."""
    return {
        "clamped_to_root": clamped_par(bad_choice, 0) == 0,
        "choice_was_not_root": bad_choice(1) != 0,
        "rewritten_input_is_not_lawful": (
            clamped_par(bad_choice, 0) == 0 and bad_choice(1) != 0),
    }


def attach_checked(s: PS, p: int) -> dict[str, Json]:
    """Checked attachment: extend at a represented parent on a live
    state, or return the typed refusal record."""
    if p < len(s.occ) and not s.halted:
        t = preplay(up_block(s, p), s)
        return {"outcome": "attached",
                "occ_len": len(t.occ), "wit_len": len(t.wit)}
    return {"outcome": "refusedParent", "parent": p,
            "bound": len(s.occ)}


# ---------------------------------------------------------------------------
# 2. Tokens, positions, freshness; the exact Up family

def fresh_tok(s: PS) -> int:
    """The canonical fresh token: one past the maximum admitted
    token (zero on the empty carrier)."""
    return 0 if not s.occ else max(s.occ) + 1


def up_block(s: PS, p: int) -> list[PEvent]:
    """The declared one-edge block at parent POSITION ``p``: admit
    the fresh TOKEN (creating position ``len(occ)``), then assert,
    retain, protect the parent edge on positions."""
    n = len(s.occ)
    return [("admitOcc", fresh_tok(s)), ("assertWit", p, n),
            ("admitWit", p, n), ("protect", p, n)]


def up_family(s: PS) -> list[list[PEvent]]:
    """One block per represented parent — the complete family of
    the declared grammar, never a selection."""
    return [up_block(s, p) for p in range(len(s.occ))]


def length_not_fresh_countermodel() -> dict[str, Json]:
    """On the lawful non-initial carrier ``(1, 2)`` the old
    length-as-token block collides (dedup silences it, no
    extension); the canonical fresh token is 3 and the repaired
    block extends strictly."""
    s12 = PS(occ=(1, 2))
    old_block: list[PEvent] = [
        ("admitOcc", 2), ("assertWit", 0, 2), ("admitWit", 0, 2),
        ("protect", 0, 2)]
    return {
        "old_block_fails_to_extend":
            len(preplay(old_block, s12).occ) == 2,
        "canonical_fresh_token": fresh_tok(s12),
        "repaired_block_extends":
            len(preplay(up_block(s12, 0), s12).occ) == 3,
    }


# ---------------------------------------------------------------------------
# 3. Trees from every lawful policy

def attach_block(pi: Policy, k: int) -> list[PEvent]:
    p = par(pi, k)
    return [("admitOcc", k + 1), ("assertWit", p, k + 1),
            ("admitWit", p, k + 1), ("protect", p, k + 1)]


def attach_hist(pi: Policy, n: int) -> list[PEvent]:
    out: list[PEvent] = [("admitOcc", 0)]
    for k in range(n):
        out.extend(attach_block(pi, k))
    return out


def tree_at(pi: Policy, n: int) -> PS:
    return preplay(attach_hist(pi, n), GENESIS_P)


def tree_state(pi: Policy, n: int) -> PS:
    edges = tuple((par(pi, k), k + 1) for k in range(n))
    return PS(occ=tuple(range(n + 1)), asserted=edges, wit=edges,
              prot=edges, obs=None, budget=0, licensed=True,
              refusals=(), halted=False)


def path_pol(i: int) -> int:
    return i - 1


def star_pol(i: int) -> int:
    return 0


def zigzag_pol(i: int) -> int:
    """An arbitrary further policy (deterministic pseudo-shape),
    lawful without clamping."""
    return (i * 7 + 3) % max(1, i)


def is_tree(s: PS) -> bool:
    """Unique ascending parent per non-root vertex, all reach 0."""
    n = len(s.occ)
    children = [c for (_, c) in s.wit]
    if sorted(children) != list(range(1, n)):
        return False
    if not all(p < c for (p, c) in s.wit):
        return False
    parent = {c: p for (p, c) in s.wit}
    for v in range(1, n):
        cur = v
        seen = 0
        while cur != 0 and seen <= n:
            cur = parent[cur]
            seen += 1
        if cur != 0:
            return False
    return True


def tree_report(rounds: int) -> dict[str, Json]:
    policies: list[tuple[str, Policy]] = [
        ("path", path_pol), ("star", star_pol),
        ("zigzag", zigzag_pol)]
    out: dict[str, Json] = {}
    for name, pi in policies:
        rows = []
        for n in range(rounds + 1):
            s = tree_at(pi, n)
            rows.append({
                "n": n,
                "spec_match": s == tree_state(pi, n),
                "V_minus_E": len(s.occ) - len(s.wit),
                "is_tree": is_tree(s),
                "pre_observational": s.obs is None,
                "block_is_up_block": attach_block(pi, n) == up_block(
                    tree_state(pi, n), par(pi, n)),
            })
        out[name] = {
            "lawful_to_rounds": lawful_to(pi, rounds),
            "all_spec_match": all(bool(r["spec_match"]) for r in rows),
            "all_residue_one": all(r["V_minus_E"] == 1 for r in rows),
            "all_trees": all(bool(r["is_tree"]) for r in rows),
            "all_blocks_are_up_blocks": all(
                bool(r["block_is_up_block"]) for r in rows),
            "rows": rows,
        }
    return out


def undirected(edges: tuple[Pair, ...]) -> set[frozenset[int]]:
    return {frozenset(e) for e in edges}


def isomorphic_undirected(e1: tuple[Pair, ...],
                          e2: tuple[Pair, ...], n: int) -> bool:
    u1, u2 = undirected(e1), undirected(e2)
    if len(u1) != len(u2):
        return False
    for perm in permutations(range(n)):
        if {frozenset(perm[x] for x in e) for e in u1} == u2:
            return True
    return False


def shape_report() -> dict[str, Json]:
    p4 = tree_at(path_pol, 3).wit
    s4 = tree_at(star_pol, 3).wit
    return {
        "path4": [list(e) for e in p4],
        "star4": [list(e) for e in s4],
        "isomorphic_undirected": isomorphic_undirected(p4, s4, 4),
        "trees_but_shapes_differ": (
            is_tree(tree_at(path_pol, 3))
            and is_tree(tree_at(star_pol, 3))
            and not isomorphic_undirected(p4, s4, 4)),
    }


# ---------------------------------------------------------------------------
# 4. Up: completeness iff, the renaming action, orbits

def up_report() -> dict[str, Json]:
    star3 = tree_at(star_pol, 2)
    path3 = tree_at(path_pol, 2)
    fam = up_family(star3)
    n = len(star3.occ)
    return {
        "family_length_equals_parents": all(
            len(up_family(tree_at(path_pol, m))) == m + 1
            for m in range(6)),
        # completeness as an iff over the declared grammar
        "every_member_is_legal": all(
            b == up_block(star3, p) for p, b in enumerate(fam)),
        "every_legal_is_member": all(
            up_block(star3, p) in fam for p in range(n)),
        "out_of_registry_absent": up_block(star3, n) not in fam,
        # grammar uniformity over the IDENTICAL carrier — NOT
        # presentation equivalence (see renaming_report)
        "grammar_uniform_same_carrier": (
            star3.occ == path3.occ
            and up_family(star3) == up_family(path3)),
        "typed_refusal": attach_checked(star3, 9),
        "attached_ok": attach_checked(star3, 0),
        "length_not_fresh": length_not_fresh_countermodel(),
        "clamp_countermodel": clamp_countermodel(),
        "star3_parent_orbits": parent_orbits(star3),
        "path3_parent_orbits": parent_orbits(path3),
        "star_leaves_one_orbit":
            parent_orbits(star3) == [[0], [1, 2]],
        "oriented_path_rigid":
            parent_orbits(path3) == [[0], [1], [2]],
    }


def act(perm: tuple[int, ...], s: PS) -> PS:
    """The genuine positional renaming action: the token at old
    position ``i`` moves to position ``perm[i]``; every relational
    store and column is renamed by ``perm``."""
    n = len(perm)
    inv = [0] * n
    for i, fi in enumerate(perm):
        inv[fi] = i

    def f(x: int) -> int:
        return perm[x] if x < n else x

    def g(j: int) -> int:
        return inv[j] if j < n else j

    def rp(pr: Pair) -> Pair:
        return (f(pr[0]), f(pr[1]))

    obs: Optional[tuple[tuple[int, ...], ...]] = None
    if s.obs is not None:
        obs = tuple(tuple(f(x) for x in col) for col in s.obs)
    return PS(occ=tuple(s.occ[g(j)] for j in range(len(s.occ))),
              asserted=tuple(rp(pr) for pr in s.asserted),
              wit=tuple(rp(pr) for pr in s.wit),
              prot=tuple(rp(pr) for pr in s.prot),
              obs=obs, budget=s.budget, licensed=s.licensed,
              refusals=tuple(rp(pr) for pr in s.refusals),
              halted=s.halted)


def renaming_report() -> dict[str, Json]:
    """Equivariance over the FULL permutation group on the sample
    carriers, and the two required countermodels."""
    star3 = tree_at(star_pol, 2)
    path3 = tree_at(path_pol, 2)
    perms3 = list(permutations(range(3)))
    comm = all(
        act(perm, preplay(up_block(s, p), s))
        == preplay(up_block(act(perm, s), perm[p]), act(perm, s))
        for s in (star3, path3)
        for perm in perms3
        for p in range(3))
    transport = all(
        (up_block(act(perm, s), perm[p]) in up_family(act(perm, s)))
        == (up_block(s, p) in up_family(s))
        for s in (star3, path3)
        for perm in perms3
        for p in range(3))
    b1 = up_block(path3, 1)
    b2 = up_block(path3, 2)
    t1 = preplay(b1, path3)
    t2 = preplay(b2, path3)
    return {
        "act_up_comm_all_perms": comm,
        "up_family_transport_all_perms": transport,
        "fresh_tok_invariant": all(
            fresh_tok(act(perm, s)) == fresh_tok(s)
            for s in (star3, path3) for perm in perms3),
        # countermodel: equal size (equal family, even) is not
        # renaming relatedness — exhaustive over the whole group
        "equal_size_not_renaming_related": {
            "same_carrier": star3.occ == path3.occ,
            "families_equal": up_family(star3) == up_family(path3),
            "no_renaming_relates": all(
                act(perm, star3) != path3 for perm in perms3),
        },
        # countermodel: two legal equal-cost extensions diverge
        "equal_cost_divergence": {
            "both_in_family": (b1 in up_family(path3)
                               and b2 in up_family(path3)),
            "equal_cost": len(b1) == len(b2),
            "extensions_non_isomorphic": not isomorphic_undirected(
                t1.wit, t2.wit, 4),
        },
    }


def store_automorphisms(s: PS) -> list[tuple[int, ...]]:
    """Permutations of positions fixing the ORIENTED stores setwise
    (occurrence tokens follow positions in the drivers here)."""
    n = len(s.occ)
    out = []
    wit = set(s.wit)
    prot = set(s.prot)
    ass = set(s.asserted)
    for perm in permutations(range(n)):
        def r(p: Pair, perm: tuple[int, ...] = perm) -> Pair:
            return (perm[p[0]], perm[p[1]])
        if ({r(p) for p in wit} == wit
                and {r(p) for p in prot} == prot
                and {r(p) for p in ass} == ass):
            out.append(perm)
    return out


def parent_orbits(s: PS) -> list[list[int]]:
    """Orbits of parent choices under the store automorphisms —
    orbit-valued choices where symmetry remains."""
    n = len(s.occ)
    autos = store_automorphisms(s)
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for p in range(n):
        if p in seen:
            continue
        orbit = sorted({perm[p] for perm in autos})
        orbits.append(orbit)
        seen.update(orbit)
    return orbits


# ---------------------------------------------------------------------------
# 5. The generalized ladder (mirror of LadderGeneral), repaired

CellsN = dict[int, list[tuple[int, ...]]]


def facets(sigma: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [sigma[:i] + sigma[i + 1:] for i in range(len(sigma))]


def asc(sigma: tuple[int, ...]) -> bool:
    """Strict ascent — excludes repeated vertices."""
    return all(a < b for a, b in zip(sigma, sigma[1:]))


def shell_n(cells: CellsN, k: int, sigma: tuple[int, ...]) -> bool:
    """The repaired guard: exact arity, strict ascent, complete
    unfilled boundary."""
    return (len(sigma) == k + 1 and k >= 1 and asc(sigma)
            and all(tau in cells.get(k - 1, [])
                    for tau in facets(sigma))
            and sigma not in cells.get(k, []))


def shell_n_legacy(cells: CellsN, k: int,
                   sigma: tuple[int, ...]) -> bool:
    """The retired guard: no well-formedness conjunct — kept only
    as the countermodel's exhibit."""
    return (len(sigma) == k + 1 and k >= 1
            and all(tau in cells.get(k - 1, [])
                    for tau in facets(sigma))
            and sigma not in cells.get(k, []))


def step_v(cells: CellsN, v: int) -> CellsN:
    if (v,) in cells.get(0, []):
        return cells
    out = dict(cells)
    out[0] = cells.get(0, []) + [(v,)]
    return out


def step_n(cells: CellsN, k: int, sigma: tuple[int, ...]) -> CellsN:
    if shell_n(cells, k, sigma):
        out = dict(cells)
        out[k] = cells.get(k, []) + [sigma]
        return out
    return cells


def wf_complex(cells: CellsN) -> bool:
    """Well-formedness: every admitted cell has exact arity and
    strict ascent — the replayed invariant."""
    return all(len(sigma) == k + 1 and asc(sigma)
               for k, cs in cells.items() for sigma in cs)


def pseudo_cell_countermodel() -> dict[str, Json]:
    """The required countermodel: with one vertex admitted, the
    LEGACY guard accepts the repeated-vertex list ``[0, 0]`` as a
    1-cell; the repaired guard refuses it and the step is inert."""
    one_v = step_v({}, 0)
    return {
        "legacy_admits_pseudo_cell":
            shell_n_legacy(one_v, 1, (0, 0)),
        "repaired_refuses": not shell_n(one_v, 1, (0, 0)),
        "repaired_step_inert": step_n(one_v, 1, (0, 0)) == one_v,
    }


def combs(n: int, m: int) -> list[tuple[int, ...]]:
    """All (m+1)-vertex ascending cells over the first n vertices."""
    def aux(need: int, pool: list[int]) -> list[tuple[int, ...]]:
        if need == 0:
            return [()]
        if not pool:
            return []
        x, rest = pool[0], pool[1:]
        return ([(x,) + t for t in aux(need - 1, rest)]
                + aux(need, rest))
    return aux(m + 1, list(range(n)))


def full_shell_complex(n: int, top: bool) -> CellsN:
    """Replay the complete complex on ``n`` vertices up to dimension
    ``n-1``, optionally with the top cell."""
    cells: CellsN = {}
    for v in range(n):
        cells = step_v(cells, v)
    for k in range(1, n - 1):
        for sigma in combs(n, k):
            cells = step_n(cells, k, sigma)
    if top:
        cells = step_n(cells, n - 1, tuple(range(n)))
    return cells


def sgn(i: int) -> int:
    return 1 if i % 2 == 0 else -1


def bd_n(sigma: tuple[int, ...]) -> list[tuple[int, tuple[int, ...]]]:
    return [(sgn(i), sigma[:i] + sigma[i + 1:])
            for i in range(len(sigma))]


def push_n(ch: list[tuple[int, tuple[int, ...]]]
           ) -> list[tuple[int, tuple[int, ...]]]:
    return [(c * d, tau) for (c, s) in ch for (d, tau) in bd_n(s)]


def coeff_n(tau: tuple[int, ...],
            ch: list[tuple[int, tuple[int, ...]]]) -> int:
    return sum(c for (c, t) in ch if t == tau)


def d2_zero_dim(sigma: tuple[int, ...]) -> bool:
    ch = push_n(bd_n(sigma))
    return all(coeff_n(t, ch) == 0
               for t in {t for (_, t) in ch})


def ladder_report(max_dim: int) -> dict[str, Json]:
    per_dim: dict[str, dict[str, Json]] = {}
    for d in range(2, max_dim + 1):
        n = d + 1
        shell = full_shell_complex(n, top=False)
        filled = full_shell_complex(n, top=True)
        top_cell = tuple(range(n))
        missing = dict(shell)
        missing[d - 1] = missing.get(d - 1, [])[1:]
        per_dim[str(d)] = {
            "shell_admits_top": shell_n(shell, d, top_cell),
            "filled_has_top": filled.get(d) == [top_cell],
            "guard_load_bearing":
                step_n(missing, d, top_cell) == missing,
            "wf_invariant_holds": (wf_complex(shell)
                                   and wf_complex(filled)),
            "d2_zero_top": d2_zero_dim(top_cell),
            "cells_per_dim": {
                str(k): len(filled.get(k, []))
                for k in range(0, d + 1)},
        }
    per_dim_json: dict[str, Json] = dict(per_dim)
    return {
        "dims_checked": list(range(2, max_dim + 1)),
        "all_ladders_fire": all(
            bool(per_dim[str(d)]["shell_admits_top"])
            and bool(per_dim[str(d)]["filled_has_top"])
            for d in range(2, max_dim + 1)),
        "all_guards_load_bearing": all(
            bool(per_dim[str(d)]["guard_load_bearing"])
            for d in range(2, max_dim + 1)),
        "all_wf": all(
            bool(per_dim[str(d)]["wf_invariant_holds"])
            for d in range(2, max_dim + 1)),
        "all_d2_zero": all(
            bool(per_dim[str(d)]["d2_zero_top"])
            for d in range(2, max_dim + 1)),
        "pseudo_cell": pseudo_cell_countermodel(),
        "per_dim": per_dim_json,
        "general_d2_zero":
            "SETTLED by Goal 4 (BoundaryCancellation."
            "d2_zero_unrestricted): the coefficientwise composite "
            "vanishes at every face of every finite cell, proved by "
            "pairing deletion orders.  The dimension-bounded checks "
            "here are now a corollary spot-check, not the evidence.  "
            "Declared coefficients and signs still carry the "
            "content: without the signs the composite is nonzero "
            "(signless countermodel)",
        "filler_theorem_scope":
            "uniform guarded filler: admission and strict "
            "extension under the repaired guard, not a homology "
            "claim",
    }
