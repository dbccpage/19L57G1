"""Additive price cocycles on traces and 2-cell homotopy price invariance.

Target G013: Coherent Trace Calculus & Higher Cell Algebra.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Mapping, Optional, Sequence, Tuple

from higher_cell import Cell2, Cell2Kind
from trace import State, Trace, Transition


@dataclass(frozen=True)
class PriceCocycle:
    """An additive price cocycle on computational transitions and execution traces.

    C(p * q) = C(p) + C(q)
    C(id_s) = 0
    """

    cost_map: Mapping[str, float]
    default_cost: float = 0.0

    def step_cost(self, trans: Transition) -> float:
        """Compute the cost of an elementary transition."""
        if trans.label in self.cost_map:
            return self.cost_map[trans.label]
        if trans.cost > 0.0:
            return trans.cost
        return self.default_cost

    def trace_price(self, trace: Trace) -> float:
        """Evaluate the total price of a trace by summing elementary step prices."""
        if trace.is_identity:
            return 0.0
        return sum(self.step_cost(t) for t in trace.transitions)

    def verify_additivity(self, p: Trace, q: Trace) -> Tuple[bool, float, float, float]:
        """Verify the cocycle additivity condition C(p * q) == C(p) + C(q)."""
        composite = p.concat(q)
        c_comp = self.trace_price(composite)
        c_p = self.trace_price(p)
        c_q = self.trace_price(q)
        c_sum = c_p + c_q
        is_additive = abs(c_comp - c_sum) < 1e-9
        return is_additive, c_comp, c_sum, abs(c_comp - c_sum)

    def verify_homotopy_invariance(self, cell: Cell2) -> Tuple[bool, float, float]:
        """Verify that a 2-cell alpha : p => q preserves trace price: C(p) == C(q)."""
        c_src = self.trace_price(cell.source_trace)
        c_tgt = self.trace_price(cell.target_trace)
        is_invariant = abs(c_src - c_tgt) < 1e-9
        return is_invariant, c_src, c_tgt


@dataclass(frozen=True)
class HomotopyPriceAudit:
    """Audit certificate recording price invariance across a collection of 2-cells."""

    total_cells_checked: int
    invariant_cells: int
    all_invariant: bool
    max_divergence: float
    violations: Tuple[str, ...] = ()


def audit_2cell_homotopy_invariance(
    cocycle: PriceCocycle,
    cells: Sequence[Cell2],
) -> HomotopyPriceAudit:
    """Audit a set of 2-cells for homotopy price invariance."""
    violations = []
    max_div = 0.0
    passed = 0

    for cell in cells:
        inv, c_src, c_tgt = cocycle.verify_homotopy_invariance(cell)
        div = abs(c_src - c_tgt)
        if div > max_div:
            max_div = div
        if inv:
            passed += 1
        else:
            violations.append(
                f"2-cell {cell.kind.value} price mismatch: src={c_src} != tgt={c_tgt} (diff={div})"
            )

    return HomotopyPriceAudit(
        total_cells_checked=len(cells),
        invariant_cells=passed,
        all_invariant=(passed == len(cells)),
        max_divergence=max_div,
        violations=tuple(violations),
    )
