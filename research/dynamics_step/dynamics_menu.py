"""
dynamics_menu.py — Response Menus & Obstruction Inspection

<!-- AuthorityEffect: None -->

Exposes the full menu of minimal candidate augmentations for an unseparated pair
without arbitrarily selecting a single delta from a tie.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, FrozenSet, List, Optional, Set, Tuple

from derivation.model import (
    Regime,
    EMPTY,
    Pair,
    Event,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    replay,
)
from derivation.observe import profiles
from derivation.candidates import (
    Bounds,
    Delta,
    min_responses,
)


@dataclass(frozen=True)
class MenuResult:
    is_separated: bool
    measure: str
    attained_cost: Optional[Tuple[int, int]]
    candidate_deltas: Tuple[Delta, ...]  # Full menu: ties are preserved
    is_tied: bool


def is_pair_separated(regime: Regime, pair: Pair) -> bool:
    """Checks whether data pair (i, j) is internally separated in the regime."""
    i, j = pair
    n = regime.n_data()
    if i < 0 or i >= n or j < 0 or j >= n:
        return False
    p = profiles(regime)
    return p[i] != p[j]


def inspect_response_menu(
    regime: Regime,
    target_pair: Pair,
    measure: str = "mu1",
    bounds: Optional[Bounds] = None,
) -> MenuResult:
    """
    Computes the menu of minimal valid responses without making a selection.
    If the pair is already separated, returns an empty menu.
    """
    if bounds is None:
        bounds = Bounds(max_items=2, max_arity=2)

    if is_pair_separated(regime, target_pair):
        return MenuResult(
            is_separated=True,
            measure=measure,
            attained_cost=None,
            candidate_deltas=(),
            is_tied=False,
        )

    resp = min_responses(regime, target_pair, measure=measure, bounds=bounds)
    if resp is None or len(resp.deltas) == 0:
        return MenuResult(
            is_separated=False,
            measure=measure,
            attained_cost=None,
            candidate_deltas=(),
            is_tied=False,
        )

    return MenuResult(
        is_separated=False,
        measure=measure,
        attained_cost=resp.cost,
        candidate_deltas=resp.deltas,
        is_tied=len(resp.deltas) > 1,
    )


@dataclass(frozen=True)
class FiveAtomCollapseExhibit:
    atom_cost: int
    uncollapsed_holds: bool
    quotient_holds: bool
    law_failed_in_quotient: bool


def five_atom_collapse_exhibit() -> FiveAtomCollapseExhibit:
    """
    Constructs a 5-atom exhibit of law-failing collapse:
      - 2 Data: ("d0", "d1")
      - 1 Form: arity 2
      - 1 Instance: Form 0 on (0, 1)
      - 1 Irreflexivity Rule
    Total atoms: 5.
    """
    events: List[Event] = [
        AdmitDatum("d0"),
        AdmitDatum("d1"),
        AdmitForm(arity=2),
        AdmitInst(form=0, args=(0, 1)),
    ]
    regime = replay(events)
    atom_cost = len(regime.data) + len(regime.forms) + len(regime.insts) + 1

    uncollapsed_holds = (
        (0, (0, 0)) not in regime.insts
        and (0, (1, 1)) not in regime.insts
    )

    # Identifying quotient map f(0) = f(1) = 0
    quotient_insts: Set[Tuple[int, Tuple[int, ...]]] = set()
    for form_id, args in regime.insts:
        collapsed_args = tuple(0 for _ in args)
        quotient_insts.add((form_id, collapsed_args))

    quotient_holds = (0, (0, 0)) not in quotient_insts
    law_failed = uncollapsed_holds and not quotient_holds

    return FiveAtomCollapseExhibit(
        atom_cost=atom_cost,
        uncollapsed_holds=uncollapsed_holds,
        quotient_holds=quotient_holds,
        law_failed_in_quotient=law_failed,
    )
