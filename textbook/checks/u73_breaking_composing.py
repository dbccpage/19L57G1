from __future__ import annotations

import itertools
import json
import pathlib
import sys
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.completion import KIND_ROLE_OVERRIDES  # noqa: E402

W = TypeVar("W")
G = TypeVar("G")
N = TypeVar("N")
A = TypeVar("A")


@dataclass(frozen=True)
class FiniteBreak(Generic[W]):
    carrier: list[W]
    e: Callable[[W], W]

    def is_valid(self) -> bool:
        return all(self.e(self.e(w)) == w for w in self.carrier) and all(
            self.e(w) != w for w in self.carrier
        )

    def single_orbit(self) -> bool:
        return all(
            w2 == w1 or w2 == self.e(w1)
            for w1 in self.carrier
            for w2 in self.carrier
        )

    def represents(self, s: Callable[[W], W]) -> bool:
        return all(s(w) == w or s(w) == self.e(w) for w in self.carrier)

    def orbit_constant(self, s: Callable[[W], W]) -> bool:
        return all(s(self.e(w)) == s(w) for w in self.carrier)

    def equivariant(self, s: Callable[[W], W]) -> bool:
        return all(s(self.e(w)) == self.e(s(w)) for w in self.carrier)


@dataclass(frozen=True)
class FiniteAction(Generic[W, G]):
    carrier: list[W]
    symbols: list[G]
    act: Callable[[G, W], W]

    def common_fixed_points(self) -> list[W]:
        return [
            p
            for p in self.carrier
            if all(self.act(g, p) == p for g in self.symbols)
        ]

    def sym_orbit_constant(self, s: Callable[[W], W]) -> bool:
        return all(
            s(self.act(g, w)) == s(w)
            for g in self.symbols
            for w in self.carrier
        )

    def sym_equivariant(self, s: Callable[[W], W]) -> bool:
        return all(
            s(self.act(g, w)) == self.act(g, s(w))
            for g in self.symbols
            for w in self.carrier
        )


@dataclass(frozen=True)
class FiniteWeb(Generic[N, A]):
    nodes: list[N]
    arrows: Callable[[N, N], list[A]]
    composes: Callable[[N, N, N, A, A, A], bool]

    def composable(self, a: N, b: N, c: N, f: A, g: A) -> bool:
        return any(self.composes(a, b, c, f, g, h) for h in self.arrows(a, c))

    def has_identity(self, a: N) -> bool:
        for i in self.arrows(a, a):
            left_ok = all(
                self.composes(a, a, b, i, f, f)
                for b in self.nodes
                for f in self.arrows(a, b)
            )
            right_ok = all(
                self.composes(b, a, a, f, i, f)
                for b in self.nodes
                for f in self.arrows(b, a)
            )
            if left_ok and right_ok:
                return True
        return False

    def left_reach(self, a: N, b: N, c: N, d: N, f: A, g: A, k: A, w: A) -> bool:
        return any(
            self.composes(a, b, c, f, g, u) and self.composes(a, c, d, u, k, w)
            for u in self.arrows(a, c)
        )

    def right_reach(self, a: N, b: N, c: N, d: N, f: A, g: A, k: A, w: A) -> bool:
        return any(
            self.composes(b, c, d, g, k, v) and self.composes(a, b, d, f, v, w)
            for v in self.arrows(b, d)
        )

    def rel_assoc_left(self) -> bool:
        for a, b, c, d in itertools.product(self.nodes, repeat=4):
            for f in self.arrows(a, b):
                for g in self.arrows(b, c):
                    for k in self.arrows(c, d):
                        for w in self.arrows(a, d):
                            if self.left_reach(a, b, c, d, f, g, k, w) and not self.right_reach(
                                a, b, c, d, f, g, k, w
                            ):
                                return False
        return True

    def rel_assoc(self) -> bool:
        for a, b, c, d in itertools.product(self.nodes, repeat=4):
            for f in self.arrows(a, b):
                for g in self.arrows(b, c):
                    for k in self.arrows(c, d):
                        for w in self.arrows(a, d):
                            if self.left_reach(a, b, c, d, f, g, k, w) != self.right_reach(
                                a, b, c, d, f, g, k, w
                            ):
                                return False
        return True


BREAKING_REPORTED_7 = [
    "Breaking.no_orbit_constant_equivariant_endomap",
    "Breaking.no_selector_of_no_common_fixed_point",
    "Breaking.no_common_fixed_point",
    "Breaking.no_orbit_constant_equivariant_selector",
    "Breaking.no_fixed_point_free_involution_on_Tri",
    "Breaking.selector_exists_at_common_fixed_point",
    "Breaking.selector_iff_common_fixed_point",
]

BREAKING_UNREPORTED_8 = [
    "Breaking.ne_image",
    "Breaking.two_cycle",
    "Breaking.fourBreak_not_singleOrbit",
    "Breaking.boolBreak_singleOrbit",
    "Breaking.constFalse_represents",
    "Breaking.constFalse_orbitConstant",
    "Breaking.constFalse_not_equivariant",
    "Breaking.imposable_but_not_equivariant",
]

COMPOSING_PARKED_7 = [
    "Composing.composition_may_fail",
    "Composing.noneCompose_no_identity",
    "Composing.composite_may_be_nonunique",
    "Composing.selection_is_possible",
    "Composing.relAssocLeft_of_relAssoc",
    "Composing.skew_not_relAssocLeft",
    "Composing.skew_not_relAssoc",
]


def all_endomaps(carrier: list[W]) -> list[Callable[[W], W]]:
    maps: list[Callable[[W], W]] = []
    for image_tuple in itertools.product(carrier, repeat=len(carrier)):
        table = dict(zip(carrier, image_tuple))
        maps.append(lambda x, t=table: t[x])
    return maps


def main() -> int:
    failures: list[str] = []

    # 1. Breaking: emptyBreak, boolBreak, fourBreak
    empty_break: FiniteBreak[int] = FiniteBreak(carrier=[], e=lambda x: x)
    if not (
        empty_break.is_valid()
        and empty_break.orbit_constant(lambda x: x)
        and empty_break.equivariant(lambda x: x)
    ):
        failures.append("emptyBreak vacuous selector check failed")

    bool_break = FiniteBreak(carrier=[False, True], e=lambda b: not b)
    if not (bool_break.is_valid() and bool_break.single_orbit()):
        failures.append("boolBreak should be valid and singleOrbit")

    four_carrier = [(False, False), (False, True), (True, False), (True, True)]
    four_break = FiniteBreak(carrier=four_carrier, e=lambda p: (not p[0], p[1]))
    if not four_break.is_valid() or four_break.single_orbit():
        failures.append("fourBreak should be valid and NOT singleOrbit")

    # Exhaustive check of all 4 selectors on boolBreak
    const_false = lambda _b: False
    if not (
        bool_break.represents(const_false)
        and bool_break.orbit_constant(const_false)
        and not bool_break.equivariant(const_false)
    ):
        failures.append("imposable_but_not_equivariant failed on constFalse")

    for s in all_endomaps(bool_break.carrier):
        if bool_break.orbit_constant(s) and bool_break.equivariant(s):
            failures.append("found orbit-constant equivariant selector on boolBreak")

    # 2. Tri: exhaustive check of all 27 endomaps
    tri_carrier = [0, 1, 2]
    tri_endomaps = all_endomaps(tri_carrier)
    involutions_on_tri = [
        fn for fn in tri_endomaps if all(fn(fn(w)) == w for w in tri_carrier)
    ]
    if len(involutions_on_tri) != 4:
        failures.append(f"expected 4 involutions on Tri, got {len(involutions_on_tri)}")
    if any(all(fn(w) != w for w in tri_carrier) for fn in involutions_on_tri):
        failures.append("found fixed-point-free involution on Tri")

    # triSymmetry (3-cycle rotation) vs. an action on Tri with a common fixed point
    tri_rot = FiniteAction(
        carrier=tri_carrier,
        symbols=[0],
        act=lambda _g, w: (w + 1) % 3,
    )
    if tri_rot.common_fixed_points() != []:
        failures.append("triSymmetry should have no common fixed point")
    if any(tri_rot.sym_orbit_constant(s) and tri_rot.sym_equivariant(s) for s in tri_endomaps):
        failures.append("triSymmetry should admit no orbit-constant equivariant selector")

    tri_fix0 = FiniteAction(
        carrier=tri_carrier,
        symbols=[0],
        act=lambda _g, w: 0 if w == 0 else (2 if w == 1 else 1),
    )
    if tri_fix0.common_fixed_points() != [0]:
        failures.append("tri_fix0 should have unique common fixed point 0")
    valid_selectors_fix0 = [
        s for s in tri_endomaps if tri_fix0.sym_orbit_constant(s) and tri_fix0.sym_equivariant(s)
    ]
    if len(valid_selectors_fix0) != 1 or any(valid_selectors_fix0[0](w) != 0 for w in tri_carrier):
        failures.append("selector_iff_common_fixed_point failed on tri_fix0")

    # 3. Composing: noneCompose, allCompose, skewCompose
    none_compose = FiniteWeb(
        nodes=[0],
        arrows=lambda _a, _b: [False, True],
        composes=lambda _a, _b, _c, _f, _g, _h: False,
    )
    if none_compose.composable(0, 0, 0, True, True) or none_compose.has_identity(0):
        failures.append("noneCompose failed composition_may_fail or noneCompose_no_identity")

    all_compose = FiniteWeb(
        nodes=[0],
        arrows=lambda _a, _b: [False, True],
        composes=lambda _a, _b, _c, _f, _g, _h: True,
    )
    composites_tt = [
        h for h in all_compose.arrows(0, 0) if all_compose.composes(0, 0, 0, True, True, h)
    ]
    if len(composites_tt) != 2:
        failures.append("allCompose failed composite_may_be_nonunique")
    all_select = lambda _a, _b, _c, _f, _g: True
    if not all(
        all_compose.composes(0, 0, 0, f, g, all_select(0, 0, 0, f, g))
        for f in [False, True]
        for g in [False, True]
    ):
        failures.append("allCompose failed selection_is_possible")

    skew_compose = FiniteWeb(
        nodes=[0],
        arrows=lambda _a, _b: [False, True],
        composes=lambda _a, _b, _c, f, g, h: h == (f and (not g)),
    )
    if not skew_compose.left_reach(0, 0, 0, 0, True, False, True, False):
        failures.append("skewCompose should reach False on the left for (True, False, True)")
    if skew_compose.right_reach(0, 0, 0, 0, True, False, True, False):
        failures.append("skewCompose should NOT reach False on the right for (True, False, True)")
    if skew_compose.rel_assoc_left() or skew_compose.rel_assoc():
        failures.append("skewCompose failed skew_not_relAssocLeft / skew_not_relAssoc")

    # 4. Audit checks against artifacts/lean_axioms.txt and KIND_ROLE_OVERRIDES
    axioms_text = (REPO_ROOT / "artifacts" / "lean_axioms.txt").read_text(encoding="utf-8")
    for name in BREAKING_REPORTED_7:
        if f"'{name}'" not in axioms_text:
            failures.append(f"expected {name} in artifacts/lean_axioms.txt")
        if name not in KIND_ROLE_OVERRIDES:
            failures.append(f"expected {name} in KIND_ROLE_OVERRIDES")
    for name in BREAKING_UNREPORTED_8:
        if f"'{name}'" in axioms_text:
            failures.append(f"audit finding violated: {name} was not in artifacts/lean_axioms.txt")
    for name in COMPOSING_PARKED_7:
        if f"'{name}'" not in axioms_text:
            failures.append(f"expected parked {name} in artifacts/lean_axioms.txt")

    result = {
        "unit": 73,
        "modules": ["Breaking", "Composing"],
        "tri_involutions": len(involutions_on_tri),
        "breaking_reported_in_artifact": len(BREAKING_REPORTED_7),
        "breaking_unreported_in_artifact": len(BREAKING_UNREPORTED_8),
        "composing_parked_in_artifact": len(COMPOSING_PARKED_7),
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
