"""Exact rational multicriteria selection. AuthorityEffect: None."""
from __future__ import annotations

from fractions import Fraction
from typing import Optional, Sequence, Union

from .evaluation import ActionEvaluation, UtilityVector


class MulticriteriaSelector:
    """Select a non-dominated evaluation under exact rational weights."""

    def __init__(
        self,
        weights: tuple[Fraction, Fraction, Fraction] = (
            Fraction(1, 3),
            Fraction(1, 3),
            Fraction(1, 3),
        ),
    ):
        if sum(weights) != Fraction(1, 1):
            raise ValueError(f"Weights must sum to 1 in exact Fraction, got {sum(weights)}")
        if any(w < Fraction(0, 1) for w in weights):
            raise ValueError("Weights cannot be negative")
        self.weights = weights

    @staticmethod
    def dominates(
        u: Union[UtilityVector, tuple[Fraction, Fraction, Fraction]],
        v: Union[UtilityVector, tuple[Fraction, Fraction, Fraction]],
    ) -> bool:
        u_obj = u if isinstance(u, UtilityVector) else UtilityVector(*u)
        v_obj = v if isinstance(v, UtilityVector) else UtilityVector(*v)
        return u_obj.dominates(v_obj)

    def pareto_frontier(self, evaluations: Sequence[ActionEvaluation]) -> list[ActionEvaluation]:
        viable_evals = [e for e in evaluations if e.viable]
        if not viable_evals:
            return []
        frontier: list[ActionEvaluation] = []
        for cand in viable_evals:
            dominated = False
            for other in viable_evals:
                if other is not cand and self.dominates(other.utility, cand.utility):
                    dominated = True
                    break
            if not dominated:
                frontier.append(cand)
        return frontier

    def composite_utility(self, utilities: Union[UtilityVector, tuple[Fraction, Fraction, Fraction]]) -> Fraction:
        u_tup = utilities.as_tuple() if isinstance(utilities, UtilityVector) else utilities
        return sum((w * u for w, u in zip(self.weights, u_tup)), Fraction(0, 1))

    def rank_preferences(self, evaluations: Sequence[ActionEvaluation]) -> list[ActionEvaluation]:
        frontier = self.pareto_frontier(evaluations)
        return sorted(
            frontier,
            key=lambda e: (
                -self.composite_utility(e.utility),
                str(e.canon_key) if e.canon_key is not None else "",
                e.action.name,
            ),
        )

    def select(self, evaluations: Sequence[ActionEvaluation]) -> Optional[ActionEvaluation]:
        ranked = self.rank_preferences(evaluations)
        if not ranked:
            return None
        return ranked[0]
