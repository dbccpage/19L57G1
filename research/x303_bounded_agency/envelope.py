"""Viability envelope and stable-subsystem boundary. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

from . import _bootstrap  # noqa: F401
from derivation.observe import separable
from research.x301_formal_semantics.semantics import Formula, RelationalModel, evaluate


@dataclass(frozen=True)
class StableSubsystem:
    """Protected core sorts/tokens that must persist across transitions."""

    protected_data: frozenset[object] = frozenset()
    protected_forms: frozenset[int] = frozenset()
    stability_invariants: tuple[Formula, ...] = ()

    def is_subsystem_stable(self, model: RelationalModel) -> tuple[bool, Optional[str]]:
        for d in self.protected_data:
            if d not in model.data:
                return False, f"Stable subsystem data sort element missing: {d}"
        n_forms = len(model.forms)
        for f in self.protected_forms:
            if not (0 <= f < n_forms):
                return False, f"Stable subsystem form index missing: {f}"
        for inv in self.stability_invariants:
            val = evaluate(model, inv)
            if not val.is_true:
                return False, f"Subsystem stability invariant violated: {inv} -> {val}"
        return True, None


@dataclass(frozen=True)
class ViabilityEnvelope:
    """Hard resource ceilings and required pairs, in exact rational arithmetic."""

    max_data: int
    max_forms: int
    max_arity: int
    max_insts: int
    min_data: int = 1
    min_forms: int = 1
    required_reqs: frozenset[tuple[int, int]] = frozenset()
    firm_invariants: tuple[Formula, ...] = ()
    subsystem: Optional[StableSubsystem] = None

    def __post_init__(self) -> None:
        if self.max_data < self.min_data:
            raise ValueError(f"max_data ({self.max_data}) cannot be less than min_data ({self.min_data})")
        if self.max_forms < self.min_forms:
            raise ValueError(f"max_forms ({self.max_forms}) cannot be less than min_forms ({self.min_forms})")
        if self.max_arity < 0 or self.max_insts < 0:
            raise ValueError("Ceilings cannot be negative")

    def check_viability(self, model: RelationalModel) -> tuple[bool, Optional[str]]:
        if model.n_data() < self.min_data:
            return False, f"Data sort count {model.n_data()} below minimum {self.min_data}"
        if model.n_forms() < self.min_forms:
            return False, f"Form sort count {model.n_forms()} below minimum {self.min_forms}"
        if model.n_data() > self.max_data:
            return False, f"Data sort count {model.n_data()} exceeds ceiling {self.max_data}"
        if model.n_forms() > self.max_forms:
            return False, f"Form sort count {model.n_forms()} exceeds ceiling {self.max_forms}"
        if any(arity > self.max_arity for arity in model.forms):
            return False, f"Form arity exceeds ceiling {self.max_arity}"
        if len(model.insts) > self.max_insts:
            return False, f"Instance count {len(model.insts)} exceeds ceiling {self.max_insts}"

        missing_reqs = self.required_reqs - model.reqs
        if missing_reqs:
            return False, f"State missing required separation pairs: {sorted(missing_reqs)}"

        if model.reqs:
            regime = model.to_regime()
            for i, j in model.reqs:
                if not (0 <= i < model.n_data() and 0 <= j < model.n_data()):
                    return False, f"Separation requirement indices out of range: ({i}, {j})"
                if not separable(regime, i, j):
                    return False, f"Required separation pair ({i}, {j}) collapsed: identical profiles"

        for inv in self.firm_invariants:
            val = evaluate(model, inv)
            if not val.is_true:
                return False, f"Firm invariant violated: {inv} evaluated to {val}"

        if self.subsystem is not None:
            sub_ok, sub_reason = self.subsystem.is_subsystem_stable(model)
            if not sub_ok:
                return False, f"Subsystem stability violation: {sub_reason}"

        return True, None

    def is_viable(self, model: RelationalModel) -> bool:
        ok, _ = self.check_viability(model)
        return ok

    def compute_margin(self, model: RelationalModel) -> Fraction:
        r_data = Fraction(model.n_data(), self.max_data) if self.max_data > 0 else Fraction(1, 1)
        r_forms = Fraction(model.n_forms(), self.max_forms) if self.max_forms > 0 else Fraction(1, 1)
        r_insts = Fraction(len(model.insts), self.max_insts) if self.max_insts > 0 else Fraction(1, 1)
        margin = Fraction(1, 1) - max(r_data, r_forms, r_insts)
        if margin < Fraction(0, 1):
            return Fraction(0, 1)
        if margin > Fraction(1, 1):
            return Fraction(1, 1)
        return margin
