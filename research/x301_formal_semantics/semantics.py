"""Target X301: Formal Semantics, Empirical Reference & Intervention Grounding.

Pure Python semantics engine providing:
1. Operational Formula AST (atomic relations, identity, conjunction, disjunction,
   implication, operational refusal/negation, bounded finite quantifiers).
2. Exact Rational Heyting Truth Structure on [0, 1] cap Q without host oracles.
3. Relational Carrier State Model (5-partition data, forms, insts, rules, reqs).
4. Signature Transport & Canonical Isomorphism Invariance across Challenge-3
   Reading L (3 classes: U0, BL, BD) and Reading F (5 classes: MarkF, DiagF, LinkF, OutF, InF).
5. Executable Interventions & Counterfactual Discrimination (empirical reference,
   behavioral congruence).
6. Multi-Observer Panel Consensus (N >= 3) vs Ground Reality (Grounding Firewall),
   emitting PanelIllusionReceipt with SHA-256 digest and returning typed refusal
   StepResult.refusal, preserving carrier state strictly unmutated.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, narrow, receipt-grounded).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from typing import Any, Callable, Iterator, Mapping, Optional, Sequence, Union


# ---------------------------------------------------------------------------
# 1. Exact Rational Heyting Truth Structure
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RationalValuation:
    """Exact rational truth valuation in [0, 1] cap Q.

    Operates over an exact rational Heyting truth structure (poset):
    - Top element (True): 1
    - Bottom element (False): 0
    - Intermediate values: partial / constructive evidence weights
    - Meet: min(a, b)
    - Join: max(a, b)
    - Heyting Implication: 1 if a <= b else b
    - Pseudo-complement / Operational Negation: 1 if a == 0 else 0
    """

    val: Fraction

    def __init__(self, val: Union[Fraction, int, str, float]):
        if isinstance(val, RationalValuation):
            frac = val.val
        elif isinstance(val, Fraction):
            frac = val
        elif isinstance(val, int):
            frac = Fraction(val, 1)
        elif isinstance(val, str):
            frac = Fraction(val)
        else:
            frac = Fraction(str(val))

        if not (Fraction(0, 1) <= frac <= Fraction(1, 1)):
            raise ValueError(f"Valuation must be in [0, 1], got {frac}")
        object.__setattr__(self, "val", frac)

    @property
    def is_true(self) -> bool:
        return self.val == Fraction(1, 1)

    @property
    def is_false(self) -> bool:
        return self.val == Fraction(0, 1)

    def __bool__(self) -> bool:
        return self.is_true

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RationalValuation):
            return self.val == other.val
        if isinstance(other, (Fraction, int)):
            return self.val == other
        return False

    def __lt__(self, other: RationalValuation) -> bool:
        return self.val < other.val

    def __le__(self, other: RationalValuation) -> bool:
        return self.val <= other.val

    def __gt__(self, other: RationalValuation) -> bool:
        return self.val > other.val

    def __ge__(self, other: RationalValuation) -> bool:
        return self.val >= other.val

    def __hash__(self) -> int:
        return hash(self.val)

    def __repr__(self) -> str:
        return f"RationalValuation({self.val})"

    def __str__(self) -> str:
        return str(self.val)

    def __and__(self, other: RationalValuation) -> RationalValuation:
        return meet(self, other)

    def __or__(self, other: RationalValuation) -> RationalValuation:
        return join(self, other)

    def __invert__(self) -> RationalValuation:
        return pseudo_complement(self)


TRUE = RationalValuation(Fraction(1, 1))
FALSE = RationalValuation(Fraction(0, 1))
HALF = RationalValuation(Fraction(1, 2))


def meet(a: RationalValuation, b: RationalValuation) -> RationalValuation:
    """Greatest lower bound in the valuation poset: min(a, b)."""
    return a if a.val <= b.val else b


def join(a: RationalValuation, b: RationalValuation) -> RationalValuation:
    """Least upper bound in the valuation poset: max(a, b)."""
    return b if a.val <= b.val else a


def implies(a: RationalValuation, b: RationalValuation) -> RationalValuation:
    """Heyting implication in the linearly ordered valuation poset.

    a -> b = 1 if a <= b else b.
    Satisfies the adjunction: meet(c, a) <= b iff c <= implies(a, b).
    """
    if a.val <= b.val:
        return TRUE
    return b


def pseudo_complement(a: RationalValuation) -> RationalValuation:
    """Operational negation / pseudo-complement: a -> 0."""
    return implies(a, FALSE)


# ---------------------------------------------------------------------------
# 2. Operational Formula AST
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Formula:
    """Base abstract syntax tree node for represented operational formulas."""
    pass


@dataclass(frozen=True)
class Atom(Formula):
    """Atomic relation statement R(t_1, ..., t_k)."""

    rel: str
    args: tuple[str, ...]

    def __init__(self, rel: str, args: Sequence[str]):
        object.__setattr__(self, "rel", str(rel))
        object.__setattr__(self, "args", tuple(str(a) for a in args))

    def __repr__(self) -> str:
        args_str = ", ".join(self.args)
        return f"{self.rel}({args_str})"


@dataclass(frozen=True)
class Identity(Formula):
    """Internal identity statement left == right."""

    left: str
    right: str

    def __repr__(self) -> str:
        return f"({self.left} = {self.right})"


@dataclass(frozen=True)
class Conj(Formula):
    """Compositional conjunction left and right."""

    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} ∧ {self.right})"


@dataclass(frozen=True)
class Disj(Formula):
    """Compositional disjunction left or right."""

    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} ∨ {self.right})"


@dataclass(frozen=True)
class Imp(Formula):
    """Compositional intuitionistic implication ant -> con."""

    ant: Formula
    con: Formula

    @property
    def antecedent(self) -> Formula:
        return self.ant

    @property
    def consequent(self) -> Formula:
        return self.con

    def __repr__(self) -> str:
        return f"({self.ant} → {self.con})"


@dataclass(frozen=True)
class Neg(Formula):
    """Operational refusal / constructive negation: inner -> False."""

    inner: Formula

    def __repr__(self) -> str:
        return f"¬({self.inner})"


@dataclass(frozen=True)
class BoundedForall(Formula):
    """Bounded universal quantifier over a finite carrier sort: forall var in sort. body."""

    var: str
    sort: str
    body: Formula

    @property
    def domain_sort(self) -> str:
        return self.sort

    def __repr__(self) -> str:
        return f"(∀{self.var}:{self.sort}. {self.body})"


@dataclass(frozen=True)
class BoundedExists(Formula):
    """Bounded existential quantifier over a finite carrier sort: exists var in sort. body."""

    var: str
    sort: str
    body: Formula

    @property
    def domain_sort(self) -> str:
        return self.sort

    def __repr__(self) -> str:
        return f"(∃{self.var}:{self.sort}. {self.body})"


# Formula AST convenience constructors
def atom(rel: str, *args: str) -> Atom:
    return Atom(rel, args)

def eq(left: str, right: str) -> Identity:
    return Identity(left, right)

def conj(left: Formula, right: Formula) -> Conj:
    return Conj(left, right)

def disj(left: Formula, right: Formula) -> Disj:
    return Disj(left, right)

def imp(ant: Formula, con: Formula) -> Imp:
    return Imp(ant, con)

def neg(inner: Formula) -> Neg:
    return Neg(inner)

def forall(var: str, sort: str, body: Formula) -> BoundedForall:
    return BoundedForall(var, sort, body)

def exists(var: str, sort: str, body: Formula) -> BoundedExists:
    return BoundedExists(var, sort, body)


# ---------------------------------------------------------------------------
# 3. Relational Carrier Model
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 5. Signature Transport & Canonical Isomorphism Invariance
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Isomorphism:
    """Isomorphism between relational carriers.

    Consists of:
    - pi: bijection on data indices (tuple of length n_data where pi[old] = new)
    - phi: bijection on form indices (tuple of length n_forms where phi[old] = new)
    - const_map: optional mapping for named constants
    - rel_map: optional mapping for named relations
    """

    pi: tuple[int, ...]
    phi: tuple[int, ...]
    const_map: Mapping[str, str] = field(default_factory=dict)
    rel_map: Mapping[str, str] = field(default_factory=dict)

    def inverse(self) -> Isomorphism:
        inv_pi = [0] * len(self.pi)
        for old, new in enumerate(self.pi):
            inv_pi[new] = old
        inv_phi = [0] * len(self.phi)
        for old, new in enumerate(self.phi):
            inv_phi[new] = old
        inv_const = {v: k for k, v in self.const_map.items()}
        inv_rel = {v: k for k, v in self.rel_map.items()}
        return Isomorphism(tuple(inv_pi), tuple(inv_phi), inv_const, inv_rel)


def pushforward(tau: Isomorphism, model: RelationalModel) -> RelationalModel:
    """Functorial push-forward tau_*(M) of relational carrier state under isomorphism tau."""
    n = model.n_data()
    nf = model.n_forms()

    if sorted(tau.pi) != list(range(n)):
        raise ValueError(f"pi must be a valid permutation of range({n}), got {tau.pi}")
    if sorted(tau.phi) != list(range(nf)):
        raise ValueError(f"phi must be a valid permutation of range({nf}), got {tau.phi}")

    # Transport data tokens under permutation pi
    new_data = [""] * n
    for d, tok in enumerate(model.data):
        new_data[tau.pi[d]] = tok

    # Transport form arities under permutation phi
    new_forms = [0] * nf
    for f, arity in enumerate(model.forms):
        new_forms[tau.phi[f]] = arity

    # Transport instances: (phi(f), pi(args))
    new_insts = frozenset(
        (tau.phi[f], tuple(tau.pi[a] for a in args))
        for (f, args) in model.insts
    )

    # Transport rules: phi(f)
    new_rules = frozenset(tau.phi[f] for f in model.rules)

    # Transport requirements: (min(pi(i), pi(j)), max(pi(i), pi(j)))
    new_reqs = frozenset(
        (min(tau.pi[i], tau.pi[j]), max(tau.pi[i], tau.pi[j]))
        for (i, j) in model.reqs
    )

    # Transport custom relations
    new_relations: dict[str, frozenset[tuple[Any, ...]]] = {}
    for rname, tups in model.custom_relations.items():
        target_rname = tau.rel_map.get(rname, rname)
        new_tups = []
        for tup in tups:
            new_tup = tuple(
                tau.pi[item] if isinstance(item, int) and 0 <= item < n else item
                for item in tup
            )
            new_tups.append(new_tup)
        new_relations[target_rname] = frozenset(new_tups)

    return RelationalModel(
        data=tuple(new_data),
        forms=tuple(new_forms),
        insts=new_insts,
        rules=new_rules,
        reqs=new_reqs,
        custom_relations=new_relations,
        custom_domains=model.custom_domains,
    )


def rename_formula(tau: Isomorphism, formula: Formula) -> Formula:
    """Rename formula tau(phi) under isomorphism signature transport."""
    if isinstance(formula, Identity):
        new_l = tau.const_map.get(formula.left, formula.left)
        new_r = tau.const_map.get(formula.right, formula.right)
        if new_l.isdigit():
            idx = int(new_l)
            if 0 <= idx < len(tau.pi):
                new_l = str(tau.pi[idx])
        if new_r.isdigit():
            idx = int(new_r)
            if 0 <= idx < len(tau.pi):
                new_r = str(tau.pi[idx])
        return Identity(new_l, new_r)

    if isinstance(formula, Atom):
        rel = formula.rel
        target_rel = tau.rel_map.get(rel, rel)
        if target_rel.startswith("form_") and target_rel[5:].isdigit():
            f = int(target_rel[5:])
            if 0 <= f < len(tau.phi):
                target_rel = f"form_{tau.phi[f]}"
        elif target_rel.isdigit():
            f = int(target_rel)
            if 0 <= f < len(tau.phi):
                target_rel = str(tau.phi[f])

        def _rename_form_arg(arg: str) -> str:
            mapped = tau.const_map.get(arg, arg)
            if mapped.isdigit():
                idx = int(mapped)
                if 0 <= idx < len(tau.phi):
                    return str(tau.phi[idx])
            return mapped

        def _rename_data_arg(arg: str) -> str:
            mapped = tau.const_map.get(arg, arg)
            if mapped.isdigit():
                idx = int(mapped)
                if 0 <= idx < len(tau.pi):
                    return str(tau.pi[idx])
            return mapped

        if target_rel == "rule" or rel == "rule":
            new_args = [_rename_form_arg(a) for a in formula.args]
        elif target_rel == "inst" or rel == "inst":
            new_args = []
            for i, a in enumerate(formula.args):
                if i == 0:
                    new_args.append(_rename_form_arg(a))
                else:
                    new_args.append(_rename_data_arg(a))
        else:
            new_args = [_rename_data_arg(a) for a in formula.args]

        return Atom(target_rel, new_args)

    if isinstance(formula, Conj):
        return Conj(rename_formula(tau, formula.left), rename_formula(tau, formula.right))

    if isinstance(formula, Disj):
        return Disj(rename_formula(tau, formula.left), rename_formula(tau, formula.right))

    if isinstance(formula, Imp):
        return Imp(rename_formula(tau, formula.ant), rename_formula(tau, formula.con))

    if isinstance(formula, Neg):
        return Neg(rename_formula(tau, formula.inner))

    if isinstance(formula, BoundedForall):
        return BoundedForall(formula.var, formula.sort, rename_formula(tau, formula.body))

    if isinstance(formula, BoundedExists):
        return BoundedExists(formula.var, formula.sort, rename_formula(tau, formula.body))

    raise TypeError(f"Unknown formula AST node: {type(formula)}")


def rename_assignment(
    tau: Isomorphism,
    assignment: Mapping[str, Any],
    data_vars: Sequence[str] = (),
) -> dict[str, Any]:
    """Transport variable assignment sigma under isomorphism tau."""
    new_env: dict[str, Any] = {}
    for var, val in assignment.items():
        if isinstance(val, int) and (var in data_vars or 0 <= val < len(tau.pi)):
            new_env[var] = tau.pi[val]
        else:
            new_env[var] = val
    return new_env


def check_transport_invariance(
    model: RelationalModel,
    tau: Isomorphism,
    formula: Formula,
    assignment: Optional[Mapping[str, Any]] = None,
) -> bool:
    """Verify semantic truth invariance under isomorphism: M, sigma |= phi <=> tau_*(M), tau(sigma) |= tau(phi)."""
    env = assignment or {}
    v1 = evaluate(model, formula, env)
    tau_m = pushforward(tau, model)
    tau_phi = rename_formula(tau, formula)
    tau_env = rename_assignment(tau, env)
    v2 = evaluate(tau_m, tau_phi, tau_env)
    return v1 == v2


def check_isomorphism(
    tau: Isomorphism,
    m1: RelationalModel,
    m2: RelationalModel,
) -> bool:
    """Verify that tau is a relational isomorphism from m1 to m2.

    Checks that tau_*(m1) matches m2 across data count, form arities,
    instances, rules, separation requirements, and custom relations.
    Returns False if tau is not an admissible bijection on m1 or if
    the transported structure fails to coincide with m2.
    """
    try:
        tau_m1 = pushforward(tau, m1)
    except ValueError:
        return False

    return (
        tau_m1.n_data() == m2.n_data()
        and tau_m1.forms == m2.forms
        and tau_m1.insts == m2.insts
        and tau_m1.rules == m2.rules
        and tau_m1.reqs == m2.reqs
        and tau_m1.custom_relations == m2.custom_relations
    )


# ---------------------------------------------------------------------------
# 6. Challenge-3 Canonical Isomorphism Classes (Reading L & F)
# ---------------------------------------------------------------------------

def get_challenge3_l_classes() -> dict[str, tuple[RelationalModel, RelationalModel, Isomorphism]]:
    """Return the 3 Challenge-3 Reading L canonical isomorphism classes.

    Under Reading L (strict admission):
    - Genesis: 2 admitted data (indices 0 and 1), target pair (0, 1).
    - 3 canonical classes at minimal cost mu1 = 2:
      1. U0: form arity 1, mark on datum 0: AdmitForm(1), AdmitInst(0, (0,))
      2. BL: form arity 2, asymmetric link: AdmitForm(2), AdmitInst(0, (0, 1))
      3. BD: form arity 2, diagonal self-loop: AdmitForm(2), AdmitInst(0, (0, 0))
    - Each class carries its isomorphic swap representative under transposition pi = (1, 0).
    """
    # Transposition swapping target data 0 and 1
    pi = (1, 0)
    phi = (0,)
    tau = Isomorphism(pi, phi)

    # 1. U0
    u0_a = RelationalModel(
        data=("<a>", "<ab>"),
        forms=(1,),
        insts=frozenset({(0, (0,))}),
        rules=frozenset(),
        reqs=frozenset({(0, 1)}),
    )
    u0_b = RelationalModel(
        data=("<a>", "<ab>"),
        forms=(1,),
        insts=frozenset({(0, (1,))}),
        rules=frozenset(),
        reqs=frozenset({(0, 1)}),
    )

    # 2. BL
    bl_a = RelationalModel(
        data=("<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (0, 1))}),
        rules=frozenset(),
        reqs=frozenset({(0, 1)}),
    )
    bl_b = RelationalModel(
        data=("<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (1, 0))}),
        rules=frozenset(),
        reqs=frozenset({(0, 1)}),
    )

    # 3. BD
    bd_a = RelationalModel(
        data=("<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (0, 0))}),
        rules=frozenset(),
        reqs=frozenset({(0, 1)}),
    )
    bd_b = RelationalModel(
        data=("<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (1, 1))}),
        rules=frozenset(),
        reqs=frozenset({(0, 1)}),
    )

    return {
        "U0": (u0_a, u0_b, tau),
        "BL": (bl_a, bl_b, tau),
        "BD": (bd_a, bd_b, tau),
    }


def get_challenge3_f_classes() -> dict[str, tuple[RelationalModel, RelationalModel, Isomorphism]]:
    """Return the 5 Challenge-3 Reading F canonical isomorphism classes.

    Under Reading F (possession admission):
    - Genesis: 3 admitted data (datum 0 is <>, target pair is (1, 2)).
    - 5 canonical classes at minimal cost mu1 = 2:
      1. MarkF (U0F): form arity 1, mark on target datum 1
      2. DiagF (BDF): form arity 2, diagonal self-loop on target datum 1
      3. LinkF (BLF): form arity 2, asymmetric link between target data (1, 2)
      4. OutF (FOUTF): form arity 2, link directed out to genesis datum (1, 0)
      5. InF (FINF): form arity 2, link directed in from genesis datum (0, 1)
    - Each class carries its isomorphic swap representative under transposition pi = (0, 2, 1).
    """
    # Transposition swapping target data 1 and 2, fixing genesis datum 0
    pi = (0, 2, 1)
    phi = (0,)
    tau = Isomorphism(pi, phi)

    # 1. MarkF
    mark_a = RelationalModel(
        data=("<>", "<a>", "<ab>"),
        forms=(1,),
        insts=frozenset({(0, (1,))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )
    mark_b = RelationalModel(
        data=("<>", "<a>", "<ab>"),
        forms=(1,),
        insts=frozenset({(0, (2,))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )

    # 2. DiagF
    diag_a = RelationalModel(
        data=("<>", "<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (1, 1))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )
    diag_b = RelationalModel(
        data=("<>", "<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (2, 2))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )

    # 3. LinkF
    link_a = RelationalModel(
        data=("<>", "<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (1, 2))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )
    link_b = RelationalModel(
        data=("<>", "<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (2, 1))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )

    # 4. OutF
    out_a = RelationalModel(
        data=("<>", "<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (1, 0))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )
    out_b = RelationalModel(
        data=("<>", "<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (2, 0))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )

    # 5. InF
    in_a = RelationalModel(
        data=("<>", "<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (0, 1))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )
    in_b = RelationalModel(
        data=("<>", "<a>", "<ab>"),
        forms=(2,),
        insts=frozenset({(0, (0, 2))}),
        rules=frozenset(),
        reqs=frozenset({(1, 2)}),
    )

    return {
        "MarkF": (mark_a, mark_b, tau),
        "DiagF": (diag_a, diag_b, tau),
        "LinkF": (link_a, link_b, tau),
        "OutF": (out_a, out_b, tau),
        "InF": (in_a, in_b, tau),
    }


# ---------------------------------------------------------------------------
# 7. Executable Interventions & Counterfactual Discrimination
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Intervention:
    """Executable state perturbation I: Carrier -> Carrier."""

    name: str
    delta_fn: Callable[[RelationalModel], RelationalModel]
    description: str = ""

    def apply(self, model: RelationalModel) -> RelationalModel:
        return self.delta_fn(model)

    def __repr__(self) -> str:
        return f"Intervention({self.name})"


def add_instance_intervention(form: int, args: tuple[int, ...], name: str = "") -> Intervention:
    def _apply(m: RelationalModel) -> RelationalModel:
        new_insts = m.insts | {(form, args)}
        return RelationalModel(
            data=m.data,
            forms=m.forms,
            insts=new_insts,
            rules=m.rules,
            reqs=m.reqs,
            custom_relations=m.custom_relations,
            custom_domains=m.custom_domains,
        )
    lbl = name or f"add_inst({form}, {args})"
    return Intervention(name=lbl, delta_fn=_apply, description=f"Add instance ({form}, {args})")


def remove_instance_intervention(form: int, args: tuple[int, ...], name: str = "") -> Intervention:
    def _apply(m: RelationalModel) -> RelationalModel:
        new_insts = m.insts - {(form, args)}
        return RelationalModel(
            data=m.data,
            forms=m.forms,
            insts=new_insts,
            rules=m.rules,
            reqs=m.reqs,
            custom_relations=m.custom_relations,
            custom_domains=m.custom_domains,
        )
    lbl = name or f"rem_inst({form}, {args})"
    return Intervention(name=lbl, delta_fn=_apply, description=f"Remove instance ({form}, {args})")


def toggle_rule_intervention(form: int, name: str = "") -> Intervention:
    def _apply(m: RelationalModel) -> RelationalModel:
        new_rules = m.rules - {form} if form in m.rules else m.rules | {form}
        return RelationalModel(
            data=m.data,
            forms=m.forms,
            insts=m.insts,
            rules=new_rules,
            reqs=m.reqs,
            custom_relations=m.custom_relations,
            custom_domains=m.custom_domains,
        )
    lbl = name or f"toggle_rule({form})"
    return Intervention(name=lbl, delta_fn=_apply, description=f"Toggle all-tuples rule on form {form}")


def add_requirement_intervention(i: int, j: int, name: str = "") -> Intervention:
    pair = (min(i, j), max(i, j))
    def _apply(m: RelationalModel) -> RelationalModel:
        new_reqs = m.reqs | {pair}
        return RelationalModel(
            data=m.data,
            forms=m.forms,
            insts=m.insts,
            rules=m.rules,
            reqs=new_reqs,
            custom_relations=m.custom_relations,
            custom_domains=m.custom_domains,
        )
    lbl = name or f"impose_req({pair[0]}, {pair[1]})"
    return Intervention(name=lbl, delta_fn=_apply, description=f"Add requirement ({pair[0]}, {pair[1]})")


def has_empirical_reference(
    formula: Formula,
    model: RelationalModel,
    intervention_pool: Sequence[Intervention],
    assignment: Optional[Mapping[str, Any]] = None,
) -> bool:
    """Check if formula has empirical reference grounded in executable interventions.

    An assertion phi possesses empirical reference relative to an intervention pool
    iff there exists an intervention I in the pool whose observable readout discriminates phi:
    evaluate(model, phi) != evaluate(I(model), phi).
    """
    env = assignment or {}
    base_val = evaluate(model, formula, env)
    for interv in intervention_pool:
        perturbed = interv.apply(model)
        pert_val = evaluate(perturbed, formula, env)
        if base_val != pert_val:
            return True
    return False


def find_discriminating_witness(
    formula: Formula,
    model: RelationalModel,
    intervention_pool: Sequence[Intervention],
    assignment: Optional[Mapping[str, Any]] = None,
) -> Optional[Intervention]:
    """Find a concrete counterfactual intervention witness that discriminates formula."""
    env = assignment or {}
    base_val = evaluate(model, formula, env)
    for interv in intervention_pool:
        perturbed = interv.apply(model)
        pert_val = evaluate(perturbed, formula, env)
        if base_val != pert_val:
            return interv
    return None


def are_behaviorally_congruent(
    phi: Formula,
    psi: Formula,
    models: Sequence[RelationalModel],
    intervention_pool: Sequence[Intervention],
    assignment: Optional[Mapping[str, Any]] = None,
) -> bool:
    """Check behavioral congruence: phi =_obs psi.

    Two formulas are behaviorally congruent across a domain of carrier states and
    interventions iff no admissible intervention can ever distinguish them.
    Ungrounded decorative distinctions lacking an intervention witness are identified.
    """
    env = assignment or {}
    for m in models:
        if evaluate(m, phi, env) != evaluate(m, psi, env):
            return False
        for interv in intervention_pool:
            pert = interv.apply(m)
            if evaluate(pert, phi, env) != evaluate(pert, psi, env):
                return False
    return True


# ---------------------------------------------------------------------------
# 8. Multi-Observer Panel Consensus & The Grounding Firewall
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Observer:
    """Independent observer evaluating assertions over a partial projection."""

    observer_id: str
    projection_fn: Callable[[RelationalModel], RelationalModel]
    description: str = ""

    def evaluate(
        self,
        model: RelationalModel,
        formula: Formula,
        assignment: Optional[Mapping[str, Any]] = None,
    ) -> RationalValuation:
        projected_carrier = self.projection_fn(model)
        return evaluate(projected_carrier, formula, assignment)


@dataclass(frozen=True)
class Panel:
    """Panel of N >= 3 independent observers evaluating assertions under partial projections."""

    observers: tuple[Observer, ...]

    def __init__(self, observers: Sequence[Observer]):
        obs_tuple = tuple(observers)
        if len(obs_tuple) < 3:
            raise ValueError(
                f"Panel protocol requires N >= 3 observers, got {len(obs_tuple)}"
            )
        object.__setattr__(self, "observers", obs_tuple)

    def unanimous_consensus(
        self,
        model: RelationalModel,
        formula: Formula,
        assignment: Optional[Mapping[str, Any]] = None,
    ) -> tuple[bool, RationalValuation]:
        """Compute whether all N observers unanimously agree on formula valuation."""
        verdicts = [obs.evaluate(model, formula, assignment) for obs in self.observers]
        first = verdicts[0]
        all_agree = all(v == first for v in verdicts)
        return (all_agree, first if all_agree else FALSE)

    def has_positive_consensus(
        self,
        model: RelationalModel,
        formula: Formula,
        assignment: Optional[Mapping[str, Any]] = None,
    ) -> bool:
        """Check if all observers unanimously certify True."""
        is_agree, val = self.unanimous_consensus(model, formula, assignment)
        return is_agree and val.is_true


@dataclass(frozen=True)
class PanelIllusionReceipt:
    """Immutable, byte-pinned receipt documenting false panel consensus overridden by ground intervention."""

    schema: str = "panel-illusion-v1"
    timestamp: str = ""
    formula_repr: str = ""
    panel_size: int = 0
    observer_ids: tuple[str, ...] = ()
    panel_verdict: bool = True
    refuting_intervention: str = ""
    observable_readout_before: str = ""
    observable_readout_after: str = ""
    ground_truth_verdict: bool = False
    firewall_action: str = "STEP_REFUSAL_STATE_PRESERVED"
    receipt_sha256: str = ""

    def compute_sha256(self) -> str:
        payload = {
            "schema": self.schema,
            "timestamp": self.timestamp,
            "formula_repr": self.formula_repr,
            "panel_size": self.panel_size,
            "observer_ids": list(self.observer_ids),
            "panel_verdict": self.panel_verdict,
            "refuting_intervention": self.refuting_intervention,
            "observable_readout_before": self.observable_readout_before,
            "observable_readout_after": self.observable_readout_after,
            "ground_truth_verdict": self.ground_truth_verdict,
            "firewall_action": self.firewall_action,
        }
        canonical_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(canonical_bytes).hexdigest()

    def verify_checksum(self) -> bool:
        return self.receipt_sha256 == self.compute_sha256()

    @classmethod
    def create(
        cls,
        formula_repr: str,
        panel_size: int,
        observer_ids: Sequence[str],
        refuting_intervention: str,
        observable_readout_before: str,
        observable_readout_after: str,
        panel_verdict: bool = True,
        ground_truth_verdict: bool = False,
        timestamp: Optional[str] = None,
    ) -> PanelIllusionReceipt:
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        unhashed = cls(
            schema="panel-illusion-v1",
            timestamp=ts,
            formula_repr=formula_repr,
            panel_size=panel_size,
            observer_ids=tuple(observer_ids),
            panel_verdict=panel_verdict,
            refuting_intervention=refuting_intervention,
            observable_readout_before=observable_readout_before,
            observable_readout_after=observable_readout_after,
            ground_truth_verdict=ground_truth_verdict,
            firewall_action="STEP_REFUSAL_STATE_PRESERVED",
            receipt_sha256="",
        )
        digest = unhashed.compute_sha256()
        return cls(
            schema=unhashed.schema,
            timestamp=unhashed.timestamp,
            formula_repr=unhashed.formula_repr,
            panel_size=unhashed.panel_size,
            observer_ids=unhashed.observer_ids,
            panel_verdict=unhashed.panel_verdict,
            refuting_intervention=unhashed.refuting_intervention,
            observable_readout_before=unhashed.observable_readout_before,
            observable_readout_after=unhashed.observable_readout_after,
            ground_truth_verdict=unhashed.ground_truth_verdict,
            firewall_action=unhashed.firewall_action,
            receipt_sha256=digest,
        )


@dataclass(frozen=True)
class StepRefusalData:
    """Payload carried by a typed step refusal."""

    retained_state: RelationalModel
    reason: str
    receipt: Optional[PanelIllusionReceipt] = None


class _RefusalDescriptor:
    """Dual-mode descriptor supporting both class constructor and instance attribute access.

    Class access: StepResult.refusal(state, reason, receipt) -> StepResult
    Instance access: result.refusal -> Optional[StepRefusalData]
    """

    def __get__(self, instance: Optional[StepResult], owner: type[StepResult]) -> Any:
        if instance is None:
            # Called on class: StepResult.refusal(...)
            return owner._make_refusal
        # Called on instance: result.refusal
        if instance.is_refusal:
            return StepRefusalData(
                retained_state=instance.state,
                reason=instance.reason or "refusal",
                receipt=instance.receipt,
            )
        return None


@dataclass(frozen=True)
class StepResult:
    """Outcome of a state transition or grounding firewall step.

    Preserves state strictly unmutated on refusal.
    """

    is_success: bool
    is_refusal: bool
    state: RelationalModel
    reason: Optional[str] = None
    receipt: Optional[PanelIllusionReceipt] = None

    refusal = _RefusalDescriptor()

    @classmethod
    def success(cls, state: RelationalModel) -> StepResult:
        return cls(
            is_success=True,
            is_refusal=False,
            state=state,
            reason=None,
            receipt=None,
        )

    @classmethod
    def _make_refusal(
        cls,
        retained_state: RelationalModel,
        reason: str = "Grounding firewall refutation",
        receipt: Optional[PanelIllusionReceipt] = None,
    ) -> StepResult:
        return cls(
            is_success=False,
            is_refusal=True,
            state=retained_state,
            reason=reason,
            receipt=receipt,
        )


class GroundingFirewall:
    """The Grounding Firewall: enforces that empirical ground interventions override panel consensus."""

    @staticmethod
    def evaluate_and_step(
        model: RelationalModel,
        formula: Formula,
        panel: Panel,
        candidate_interventions: Sequence[Intervention],
        assignment: Optional[Mapping[str, Any]] = None,
        proposed_mutation: Optional[RelationalModel] = None,
    ) -> StepResult:
        """Evaluate formula under panel consensus vs ground intervention testing.

        If unanimous panel consensus certifies phi, but ground reality or a counterfactual
        intervention refutes phi:
        - Override committee consensus
        - Emit PanelIllusionReceipt
        - Return typed refusal StepResult.refusal, preserving model strictly unmutated
        """
        env = assignment or {}

        # 1. Evaluate panel unanimous consensus
        panel_certifies = panel.has_positive_consensus(model, formula, env)

        # 2. Evaluate ground truth on actual carrier state
        ground_val_before = evaluate(model, formula, env)

        # 3. Check counterfactual interventions
        refuting_intervention: Optional[Intervention] = None
        readout_after: Optional[RationalValuation] = None

        if panel_certifies and not ground_val_before.is_true:
            # Direct contradiction: panel says True, but carrier state is False
            for interv in candidate_interventions:
                pert = interv.apply(model)
                v_after = evaluate(pert, formula, env)
                if not v_after.is_true:
                    refuting_intervention = interv
                    readout_after = v_after
                    break
            if refuting_intervention is None and candidate_interventions:
                refuting_intervention = candidate_interventions[0]
                readout_after = ground_val_before

        # Also search candidate interventions if panel claims True
        if panel_certifies and refuting_intervention is None:
            for interv in candidate_interventions:
                pert = interv.apply(model)
                v_after = evaluate(pert, formula, env)
                if not v_after.is_true:
                    refuting_intervention = interv
                    readout_after = v_after
                    break

        # 4. Trigger Grounding Firewall if panel consensus is refuted by ground reality / intervention
        if panel_certifies and (refuting_intervention is not None or not ground_val_before.is_true):
            interv_name = refuting_intervention.name if refuting_intervention else "ground_carrier_check"
            after_str = str(readout_after) if readout_after is not None else str(ground_val_before)
            receipt = PanelIllusionReceipt.create(
                formula_repr=repr(formula),
                panel_size=len(panel.observers),
                observer_ids=[obs.observer_id for obs in panel.observers],
                refuting_intervention=interv_name,
                observable_readout_before=str(ground_val_before),
                observable_readout_after=after_str,
                panel_verdict=True,
                ground_truth_verdict=False,
            )
            # FIREWALL OVERRIDE: Refusal preserving original carrier state unmutated
            return StepResult.refusal(
                retained_state=model,
                reason="Grounding firewall override: unanimous panel consensus refuted by ground intervention",
                receipt=receipt,
            )

        # 5. If panel agrees and ground reality validates formula
        if panel_certifies and ground_val_before.is_true:
            next_state = proposed_mutation if proposed_mutation is not None else model
            return StepResult.success(state=next_state)

        # 6. Panel did not reach positive consensus
        return StepResult.refusal(
            retained_state=model,
            reason="Panel did not certify formula",
            receipt=None,
        )


def evaluate_with_grounding_firewall(
    model: RelationalModel,
    formula: Formula,
    panel: Panel,
    candidate_interventions: Sequence[Intervention],
    assignment: Optional[Mapping[str, Any]] = None,
    proposed_mutation: Optional[RelationalModel] = None,
) -> StepResult:
    """Convenience entry point for the Grounding Firewall protocol."""
    return GroundingFirewall.evaluate_and_step(
        model=model,
        formula=formula,
        panel=panel,
        candidate_interventions=candidate_interventions,
        assignment=assignment,
        proposed_mutation=proposed_mutation,
    )

