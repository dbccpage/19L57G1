"""Relational carrier model and compositional evaluation.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional

from formulas import (
    Atom,
    BoundedExists,
    BoundedForall,
    Conj,
    Disj,
    Formula,
    Identity,
    Imp,
    Neg,
)
from valuation import FALSE, TRUE, RationalValuation, implies, join, meet, pseudo_complement

@dataclass(frozen=True)
class RelationalModel:
    """5-partition relational carrier state model.

    Compatible with code/derivation/model.py (Regime) and
    research/g012_typed_translation/codec.py (RelationalState).

    Fields:
    - data: tuple of presentation tokens (internal identities are 0-based indices)
    - forms: tuple of form arities where entry arity at index f means form f has arity >= 1
    - insts: frozenset of (form_idx, args_tuple)
    - rules: frozenset of form indices carrying uniform all-tuples rule
    - reqs: frozenset of (i, j) separation requirement pairs with i < j
    - custom_relations: optional dictionary of named relation tuples
    - custom_domains: optional dictionary mapping sort names to element tuples
    """

    data: tuple[str, ...] = ()
    forms: tuple[int, ...] = ()
    insts: frozenset[tuple[int, tuple[int, ...]]] = frozenset()
    rules: frozenset[int] = frozenset()
    reqs: frozenset[tuple[int, int]] = frozenset()
    custom_relations: Mapping[str, frozenset[tuple[Any, ...]]] = field(default_factory=dict)
    custom_domains: Mapping[str, tuple[Any, ...]] = field(default_factory=dict)

    def n_data(self) -> int:
        return len(self.data)

    def n_forms(self) -> int:
        return len(self.forms)

    def is_derivable(self, form: int, args: tuple[int, ...]) -> bool:
        """Positive derivability readout: instance is in insts or form is under all-tuples rule."""
        if form in self.rules:
            return True
        return (form, args) in self.insts

    def sort_domain(self, sort: str) -> tuple[Any, ...]:
        """Finite domain of elements for bounded quantification."""
        if sort in self.custom_domains:
            return self.custom_domains[sort]
        if sort == "data":
            return tuple(range(len(self.data)))
        if sort == "data_tokens":
            return self.data
        if sort == "forms":
            return tuple(range(len(self.forms)))
        if sort == "rules":
            return tuple(sorted(self.rules))
        if sort == "reqs":
            return tuple(sorted(self.reqs))
        return ()

    @classmethod
    def from_regime(cls, regime: Any) -> RelationalModel:
        """Convert a derivation.model.Regime to RelationalModel."""
        return cls(
            data=tuple(regime.data),
            forms=tuple(regime.forms),
            insts=frozenset(regime.insts),
            rules=frozenset(regime.rules),
            reqs=frozenset(regime.reqs),
        )

    def to_regime(self) -> Any:
        """Convert RelationalModel to derivation.model.Regime if available."""
        from derivation.model import Regime
        return Regime(
            data=self.data,
            forms=self.forms,
            insts=self.insts,
            rules=self.rules,
            reqs=self.reqs,
        )


EMPTY_MODEL = RelationalModel()


# ---------------------------------------------------------------------------
# 4. Compositional Semantic Interpretation
# ---------------------------------------------------------------------------

def _resolve_term(term: str, assignment: Mapping[str, Any]) -> Any:
    """Resolve a term string to an element via variable assignment or integer literal."""
    if term in assignment:
        return assignment[term]
    if term.isdigit():
        return int(term)
    if term.startswith("-") and term[1:].isdigit():
        return int(term)
    return term


def evaluate(
    model: RelationalModel,
    formula: Formula,
    assignment: Optional[Mapping[str, Any]] = None,
) -> RationalValuation:
    """Evaluate formula on model under assignment in the exact Heyting truth structure.

    M, sigma |= phi -> [0, 1] cap Q.
    Compositional evaluation:
    - Atom: checks presence in carrier relations, instances, rules, or requirements
    - Identity: 1 if resolved terms match, else 0
    - Conj: meet(eval(left), eval(right))
    - Disj: join(eval(left), eval(right))
    - Imp: implies(eval(ant), eval(con))
    - Neg: pseudo_complement(eval(inner))
    - BoundedForall: infimum / meet over all elements in finite domain
    - BoundedExists: supremum / join over all elements in finite domain
    """
    env = assignment or {}

    if isinstance(formula, Identity):
        v_left = _resolve_term(formula.left, env)
        v_right = _resolve_term(formula.right, env)
        return TRUE if v_left == v_right else FALSE

    if isinstance(formula, Atom):
        rel = formula.rel
        args = tuple(_resolve_term(a, env) for a in formula.args)

        # 1. Custom named relations
        if rel in model.custom_relations:
            return TRUE if args in model.custom_relations[rel] else FALSE

        # 2. Separation requirement relation 'req'
        if rel == "req":
            if len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
                pair = (min(args[0], args[1]), max(args[0], args[1]))
                return TRUE if pair in model.reqs else FALSE
            return FALSE

        # 3. Rule relation 'rule'
        if rel == "rule":
            if len(args) == 1 and isinstance(args[0], int):
                return TRUE if args[0] in model.rules else FALSE
            return FALSE

        # 4. Judgment form relation: 'form_f', integer string 'f', or 'inst'
        form_idx: Optional[int] = None
        form_args: tuple[int, ...] = ()

        if rel.startswith("form_") and rel[5:].isdigit():
            form_idx = int(rel[5:])
            form_args = tuple(int(a) for a in args if isinstance(a, int) or (isinstance(a, str) and a.isdigit()))
        elif rel.isdigit():
            form_idx = int(rel)
            form_args = tuple(int(a) for a in args if isinstance(a, int) or (isinstance(a, str) and a.isdigit()))
        elif rel == "inst" and len(args) >= 1:
            if isinstance(args[0], int):
                form_idx = args[0]
                form_args = tuple(int(a) for a in args[1:] if isinstance(a, int) or (isinstance(a, str) and a.isdigit()))

        if form_idx is not None:
            if 0 <= form_idx < len(model.forms):
                if len(form_args) == model.forms[form_idx]:
                    return TRUE if model.is_derivable(form_idx, form_args) else FALSE
            return FALSE

        # Unrecognized atomic relation defaults to bottom (refusal of ungrounded atom)
        return FALSE

    if isinstance(formula, Conj):
        return meet(evaluate(model, formula.left, env), evaluate(model, formula.right, env))

    if isinstance(formula, Disj):
        return join(evaluate(model, formula.left, env), evaluate(model, formula.right, env))

    if isinstance(formula, Imp):
        return implies(evaluate(model, formula.ant, env), evaluate(model, formula.con, env))

    if isinstance(formula, Neg):
        return pseudo_complement(evaluate(model, formula.inner, env))

    if isinstance(formula, BoundedForall):
        domain = model.sort_domain(formula.sort)
        if not domain:
            return TRUE
        curr = TRUE
        for elem in domain:
            extended = {**env, formula.var: elem}
            step_val = evaluate(model, formula.body, extended)
            curr = meet(curr, step_val)
            if curr.is_false:
                break
        return curr

    if isinstance(formula, BoundedExists):
        domain = model.sort_domain(formula.sort)
        if not domain:
            return FALSE
        curr = FALSE
        for elem in domain:
            extended = {**env, formula.var: elem}
            step_val = evaluate(model, formula.body, extended)
            curr = join(curr, step_val)
            if curr.is_true:
                break
        return curr

    raise TypeError(f"Unknown formula AST node: {type(formula)}")
