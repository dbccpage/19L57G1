"""Unit 70 check: presentation isomorphisms, admissible-pair transport, and
natural sections over declared presentation families (`PresentationNaturality`).

`PresentationNaturality` has no standalone module under `code/derivation/`
(its claim-ledger entries `CL-PN-NATURAL-SELECTION` and
`CL-PN-HETEROGENEOUS-TRANSPORT` are Lean-only by construction). This Python
(book) script builds finite models of `Bij`, `PresIso`, `zeroRel_transport`,
`mapPair`, `autoFamily`, `HFamily`, `boolEqObs`/`negIso`, `card4Obs`/`twIso`,
and `twoFamilyNeg`/`twoFamilyPos`, and checks all 24 carrier permutations of
`Card4` against `natural_section_iff_fixed_pair`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u70_presentation_naturality.py
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from typing import Callable, Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
X = TypeVar("X")
R = TypeVar("R")
Xp = TypeVar("Xp")
Rp = TypeVar("Rp")


@dataclass(frozen=True)
class Bij(Generic[A, B]):
    domain: tuple[A, ...]
    codomain: tuple[B, ...]
    fwd: Callable[[A], B]
    bwd: Callable[[B], A]

    def check_laws(self) -> bool:
        return (
            all(self.fwd(self.bwd(b)) == b for b in self.codomain)
            and all(self.bwd(self.fwd(a)) == a for a in self.domain)
        )

    def symm(self) -> Bij[B, A]:
        return Bij(self.codomain, self.domain, self.bwd, self.fwd)

    def trans(self, other: Bij[B, C]) -> Bij[A, C]:
        return Bij(
            self.domain,
            other.codomain,
            lambda a: other.fwd(self.fwd(a)),
            lambda c: self.bwd(other.bwd(c)),
        )


@dataclass(frozen=True)
class DiffObsModel(Generic[X, R]):
    carrier: tuple[X, ...]
    residuals: tuple[R, ...]
    delta: Callable[[X, X], R]
    zero: Callable[[R], bool]

    def zero_rel(self, x: X, y: X) -> bool:
        return self.zero(self.delta(x, y))

    def nonzero_pairs(self) -> list[tuple[X, X]]:
        return [
            (x, y)
            for x in self.carrier
            for y in self.carrier
            if not self.zero_rel(x, y)
        ]


@dataclass(frozen=True)
class PresIso(Generic[X, R, Xp, Rp]):
    src: DiffObsModel[X, R]
    tgt: DiffObsModel[Xp, Rp]
    car: Bij[X, Xp]
    res: Bij[R, Rp]

    def check_laws(self) -> bool:
        if not (self.car.check_laws() and self.res.check_laws()):
            return False
        delta_ok = all(
            self.res.fwd(self.src.delta(x, y))
            == self.tgt.delta(self.car.fwd(x), self.car.fwd(y))
            for x in self.src.carrier
            for y in self.src.carrier
        )
        zero_ok = all(
            self.src.zero(r) == self.tgt.zero(self.res.fwd(r))
            for r in self.src.residuals
        )
        return delta_ok and zero_ok

    def map_pair(self, p: tuple[X, X]) -> tuple[Xp, Rp]:  # type: ignore[type-var]
        return (self.car.fwd(p[0]), self.car.fwd(p[1]))  # type: ignore[return-value]


def refl_iso(obs: DiffObsModel[X, R]) -> PresIso[X, R, X, R]:
    return PresIso(
        obs,
        obs,
        Bij(obs.carrier, obs.carrier, lambda x: x, lambda x: x),
        Bij(obs.residuals, obs.residuals, lambda r: r, lambda r: r),
    )


def symm_iso(iso: PresIso[X, R, Xp, Rp]) -> PresIso[Xp, Rp, X, R]:
    return PresIso(iso.tgt, iso.src, iso.car.symm(), iso.res.symm())


def trans_iso(
    f: PresIso[X, R, Xp, Rp], g: PresIso[Xp, Rp, A, B]
) -> PresIso[X, R, A, B]:
    return PresIso(f.src, g.tgt, f.car.trans(g.car), f.res.trans(g.res))


def main() -> int:
    failures: list[str] = []

    # 1. boolEqObs and negIso
    bools = (False, True)
    bool_eq_obs = DiffObsModel(
        carrier=bools,
        residuals=bools,
        delta=lambda x, y: x ^ y,
        zero=lambda v: v is False,
    )
    not_bij = Bij(bools, bools, lambda b: not b, lambda b: not b)
    id_bool_bij = Bij(bools, bools, lambda b: b, lambda b: b)
    neg_iso = PresIso(bool_eq_obs, bool_eq_obs, not_bij, id_bool_bij)

    bool_nz = bool_eq_obs.nonzero_pairs()
    bool_fixed = [p for p in bool_nz if neg_iso.map_pair(p) == p]
    bool_ok = (
        neg_iso.check_laws()
        and bool_nz == [(False, True), (True, False)]
        and len(bool_nz) == 2
        and len(bool_fixed) == 0
    )
    print(f"Python (book) boolEqObs/negIso: raw sections={len(bool_nz)} "
          f"(selection_is_possible), natural sections={len(bool_fixed)} "
          f"(no_natural_section_boolEq): {bool_ok}")
    if not bool_ok:
        failures.append("bool_eq")

    # 2. card4Obs and twIso + coherence laws of mapPair
    card4 = ("e1", "e2", "e3", "e4")
    card4_pairs = tuple(product(card4, repeat=2))
    card4_obs = DiffObsModel(
        carrier=card4,
        residuals=card4_pairs,
        delta=lambda x, y: (x, y),
        zero=lambda r: r[0] == r[1],
    )
    tw_map = {"e1": "e2", "e2": "e1", "e3": "e3", "e4": "e4"}
    tw_bij = Bij(card4, card4, lambda x: tw_map[x], lambda x: tw_map[x])
    tw_pair_bij = Bij(
        card4_pairs,
        card4_pairs,
        lambda p: (tw_map[p[0]], tw_map[p[1]]),
        lambda p: (tw_map[p[0]], tw_map[p[1]]),
    )
    tw_iso = PresIso(card4_obs, card4_obs, tw_bij, tw_pair_bij)

    c4_nz = card4_obs.nonzero_pairs()
    c4_fixed = [p for p in c4_nz if tw_iso.map_pair(p) == p]
    r_iso = refl_iso(card4_obs)
    s_iso = symm_iso(tw_iso)
    t_iso = trans_iso(tw_iso, tw_iso)
    coherence_ok = (
        tw_iso.check_laws()
        and s_iso.check_laws()
        and t_iso.check_laws()
        and all(r_iso.map_pair(p) == p for p in c4_nz)
        and all(t_iso.map_pair(p) == tw_iso.map_pair(tw_iso.map_pair(p)) for p in c4_nz)
        and all(s_iso.map_pair(tw_iso.map_pair(p)) == p for p in c4_nz)
        and all(tw_iso.map_pair(s_iso.map_pair(p)) == p for p in c4_nz)
    )
    card4_ok = (
        len(c4_nz) == 12
        and c4_fixed == [("e3", "e4"), ("e4", "e3")]
        and coherence_ok
    )
    print(f"Python (book) card4Obs/twIso: admissible pairs={len(c4_nz)}, "
          f"fixed pairs={c4_fixed} (card4_has_natural_section), "
          f"mapPair coherence: {card4_ok}")
    if not card4_ok:
        failures.append("card4")

    # 3. Exhaustive check over all 24 permutations of Card4:
    # natural sections over autoFamily(card4Obs, F) <-> fixed admissible pairs
    perm_ok = True
    with_section = 0
    without_section = 0
    for perm in permutations(card4):
        fwd_d = dict(zip(card4, perm))
        bwd_d = {v: k for k, v in fwd_d.items()}
        c_bij = Bij(card4, card4, lambda x, d=fwd_d: d[x], lambda x, d=bwd_d: d[x])
        r_bij = Bij(
            card4_pairs,
            card4_pairs,
            lambda p, d=fwd_d: (d[p[0]], d[p[1]]),
            lambda p, d=bwd_d: (d[p[0]], d[p[1]]),
        )
        iso = PresIso(card4_obs, card4_obs, c_bij, r_bij)
        if not iso.check_laws():
            perm_ok = False
        fixed_pts = [x for x in card4 if fwd_d[x] == x]
        fixed_pairs = [p for p in c4_nz if iso.map_pair(p) == p]
        if len(fixed_pairs) != len(fixed_pts) * (len(fixed_pts) - 1):
            perm_ok = False
        if fixed_pairs:
            with_section += 1
        else:
            without_section += 1
    print(f"Python (book) all 24 Card4 automorphisms: {with_section} have natural "
          f"sections (>=2 fixed pts), {without_section} have none (0 or 1 fixed pt): "
          f"{perm_ok}")
    if not (perm_ok and with_section == 7 and without_section == 17):
        failures.append("card4_permutations")

    # 4. Heterogeneous two-object families: twoFamilyNeg vs twoFamilyPos
    # HSec consists of (p_bool, p_four) in bool_nz x c4_nz (2 x 12 = 24 sections).
    all_hsec = list(product(bool_nz, c4_nz))
    neg_natural = [
        (pb, pf)
        for pb, pf in all_hsec
        if neg_iso.map_pair(pb) == pb and tw_iso.map_pair(pf) == pf
    ]
    pos_natural = [
        (pb, pf)
        for pb, pf in all_hsec
        if refl_iso(bool_eq_obs).map_pair(pb) == pb and tw_iso.map_pair(pf) == pf
    ]
    hfamily_ok = (
        len(all_hsec) == 24
        and len(neg_natural) == 0
        and len(pos_natural) == 4
        and ((False, True), ("e3", "e4")) in pos_natural
    )
    print(f"Python (book) HFamily (twoFamilyNeg vs twoFamilyPos): total HSec={len(all_hsec)}, "
          f"twoFamilyNeg natural={len(neg_natural)}, twoFamilyPos natural={len(pos_natural)}: "
          f"{hfamily_ok}")
    if not hfamily_ok:
        failures.append("hfamily")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
