"""Signature transport and Challenge-3 canonical isomorphisms.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Sequence

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
from model import RelationalModel, evaluate
from valuation import RationalValuation

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
