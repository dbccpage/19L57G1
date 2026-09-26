"""Driver A: explore licensed retained classes by sealed replay.

AuthorityEffect: None.

Explores only licensed keys.  Expansion uses sealed Admit*/Impose replay
onto a new Node; evaluation's declared base is not mutated.  Unique
minima remain proposals.  Leftover collapsed pairs after a licensed
apply are observations, not a next demand.  Driver B is not implemented.

2026-09-25 (closeout audit, pass 1): before any admission, the parent
Node must replay to its stated regime and the License must be bound to
this declaration (source history, target, measure, bounds).  The
evaluation is then recomputed from the sealed kernel for that
declaration.  The caller's ``EvalResult`` is evidence only: it must
equal the fresh recomputation, and the executed member is taken from
the fresh recomputation, never from the caller's evidence.
"""

from __future__ import annotations

from dataclasses import dataclass

from derivation.candidates import Bounds, Delta, delta_events
from derivation.engine import READING_F, READING_L, Reading
from derivation.iso import CanonKey
from derivation.model import Event, Impose, Pair, replay
from derivation.observe import collapsed_pairs

from evaluate import (
    declared_base_mutated,
    evaluate,
)
from harness import (
    EvalResult,
    ForgedEvaluationError,
    HarnessError,
    LeftoverIsNotDemandError,
    License,
    Node,
    Proposal,
    SubstitutedMemberError,
    UniqueDeltaAutoApplyError,
    apply_unique_delta,
    check_license_binding,
    check_node_integrity,
    jsonable,
    leftover_as_demand,
    make_license,
    present,
)
from search_policy import (
    FabricatedClassError,
    PolicyCensus,
    declared_explore_first,
    record_census,
)


class UnlicensedExploreError(HarnessError):
    """Driver A expands only keys named by the License."""


@dataclass(frozen=True)
class ExploreResult:
    """New nodes plus leftover-pair observations."""

    children: tuple[Node, ...]
    leftover_pairs: tuple[tuple[Pair, ...], ...]
    leftover_are_observations: bool
    census: PolicyCensus


def representative_delta(result: EvalResult, key: CanonKey) -> Delta:
    """First member in sealed min_responses order for that class."""
    for item in result.retained:
        if item.key == key:
            return item.members[0]
    raise FabricatedClassError(
        "class key absent from the sealed quotient"
    )


def bound_evaluation(
    node: Node,
    result: EvalResult,
    license: License,
    target: Pair,
) -> EvalResult:
    """Check the parent and the License binding, then recompute from the sealed kernel.

    Refuses a parent whose history does not replay to its regime
    (``NodeIntegrityError``) and a License used away from its declaration
    (``LicenseBindingError``).  Returns the fresh sealed evaluation of the
    License's declaration; the caller's ``result`` is compared, not trusted.
    """
    check_node_integrity(node)
    check_license_binding(
        license,
        node,
        target,
        result.measure,
        Bounds(max_items=result.max_items, max_arity=result.max_arity),
    )
    return evaluate(node.regime, license.target, license.measure, license.bounds)


def check_evidence(
    result: EvalResult,
    fresh: EvalResult,
    keys: tuple[CanonKey, ...],
) -> None:
    """The caller's evidence must equal the fresh sealed recomputation.

    A class whose claimed members differ from the fresh class raises
    ``SubstitutedMemberError``; any other difference (an omitted class,
    a cost, the raw minima, the found flag) raises ``ForgedEvaluationError``.
    """
    claimed = {item.key: item.members for item in result.retained}
    recomputed = {item.key: item.members for item in fresh.retained}
    for key in keys:
        if claimed.get(key) != recomputed.get(key):
            raise SubstitutedMemberError(
                "claimed members differ from the fresh sealed class"
            )
    if result != fresh:
        raise ForgedEvaluationError(
            "evaluation evidence differs from the fresh sealed recomputation"
        )


def apply_licensed(
    node: Node,
    result: EvalResult,
    license: License,
    key: CanonKey,
    target: Pair,
) -> Node | None:
    """Replay Impose plus a freshly recomputed class member onto a new Node.

    Returns None when the key is not authorized.  A denied call does not
    write ``node.license``.  The parent must replay to its regime and the
    License must be bound to this declaration.  The executed member is
    the first member of the class as freshly recomputed from the sealed
    kernel, and the caller's evidence must equal that recomputation.
    """
    fresh = bound_evaluation(node, result, license, target)
    authorized = frozenset(license.authorized)
    if key not in authorized:
        return None
    sealed_keys = frozenset(item.key for item in fresh.retained)
    claimed = frozenset(item.key for item in result.retained)
    if key not in sealed_keys or key not in claimed or claimed - sealed_keys:
        raise FabricatedClassError(
            "class key absent from the sealed quotient"
        )
    foreign = authorized - sealed_keys
    if foreign:
        raise FabricatedClassError(
            "class key absent from the sealed quotient"
        )
    check_evidence(result, fresh, (key,))
    delta = representative_delta(fresh, key)
    extra: list[Event] = [Impose(target[0], target[1])]
    extra.extend(delta_events(node.regime, delta))
    new_history = node.history + tuple(extra)
    new_regime = replay(extra, node.regime)
    return Node(history=new_history, regime=new_regime, license=license)


def explore(
    node: Node,
    result: EvalResult,
    license: License,
    census: PolicyCensus,
    target: Pair,
) -> ExploreResult:
    """Expand licensed explored keys; a License of a sole class is still an apply.

    The parent, the License binding and the evidence are checked as in
    ``apply_licensed`` before any class is expanded, even when none is.
    """
    fresh = bound_evaluation(node, result, license, target)
    sealed_keys = tuple(sorted(item.key for item in fresh.retained))
    claimed = tuple(item.key for item in result.retained)
    if frozenset(claimed) != frozenset(sealed_keys):
        raise FabricatedClassError(
            "class key absent from the sealed quotient"
        )
    checked = record_census(
        sealed_keys, census.explored, census.pruned, census.open_keys
    )
    extra = frozenset(license.authorized) - frozenset(sealed_keys)
    if extra:
        raise FabricatedClassError(
            "class key absent from the sealed quotient"
        )
    check_evidence(result, fresh, sealed_keys)
    children: list[Node] = []
    leftovers: list[tuple[Pair, ...]] = []
    leftover_obs = True
    for key in checked.explored:
        if key not in license.authorized:
            raise UnlicensedExploreError(
                "Driver A explores only licensed keys"
            )
        child = apply_licensed(node, result, license, key, target)
        if child is None:
            raise UnlicensedExploreError(
                "Driver A explores only licensed keys"
            )
        children.append(child)
        pairs = collapsed_pairs(child.regime)
        leftovers.append(pairs)
        try:
            leftover_as_demand(pairs)
            leftover_obs = False
        except LeftoverIsNotDemandError:
            pass
    return ExploreResult(
        children=tuple(children),
        leftover_pairs=tuple(leftovers),
        leftover_are_observations=leftover_obs,
        census=checked,
    )


def _unique_auto_applied(node: Node, result: EvalResult) -> bool:
    """True only if uniqueness applied without a License."""
    try:
        apply_unique_delta(node, result)
    except UniqueDeltaAutoApplyError:
        return False
    return True


def _fold_reading(reading: Reading, bounds: Bounds) -> dict[str, object]:
    regime = replay(reading.genesis)
    node = Node(history=reading.genesis, regime=regime, license=None)
    before = regime
    result = evaluate(regime, reading.target, "mu1", bounds)
    mutated = declared_base_mutated(before, regime, reading.genesis)
    proposal = Proposal(
        token="sealed-minima-offerings",
        offerings=result.raw_minima,
    )
    after = present(regime, proposal)
    keys = tuple(item.key for item in result.retained)
    policy = declared_explore_first(keys)
    census = policy.census()
    license = make_license(
        granter=policy.policy_id,
        scope=f"C3-{reading.name}-mu1",
        authorized=policy.subset(),
        source=node,
        target=reading.target,
        measure="mu1",
        bounds=bounds,
    )
    explored = explore(node, result, license, census, reading.target)
    leftover_pairs = explored.leftover_pairs
    auto_applied = _unique_auto_applied(node, result)
    return {
        "reading": reading.name,
        "compute_order": [
            "evaluate",
            "wrap_raw_minima_as_proposal",
            "present",
            "license",
            "explore",
        ],
        "proposal": {
            "token": proposal.token,
            "offering_count": len(proposal.offerings),
            "changes_admitted_state": after != regime,
        },
        "evaluation": {
            "measure": "mu1",
            "cost": list(result.cost) if result.cost is not None else None,
            "raw_minima_count": len(result.raw_minima),
            "retained_class_count": len(result.retained),
            "class_keys": [jsonable(key) for key in keys],
            "mutated_declared_base": mutated,
            "grades_as_license": False,
        },
        "authorization": {
            "granter": license.granter,
            "scope": license.scope,
            "authorized_count": len(license.authorized),
            "binding": {
                "source_history_sha256": license.source,
                "target": list(license.target),
                "measure": license.measure,
                "bounds": [license.bounds.max_items, license.bounds.max_arity],
            },
            "score_is_not_license": True,
            "sole_class_license_is_apply": len(result.retained) == 1,
        },
        "census": {
            "explored_count": len(census.explored),
            "pruned_count": len(census.pruned),
            "open_count": len(census.open_keys),
            "tie_set_size": census.tie_set_size,
            "sum_equals_tie_set": (
                len(census.explored) + len(census.pruned) + len(census.open_keys)
                == census.tie_set_size
            ),
        },
        "expansion": {
            "new_node_count": len(explored.children),
            "leftover_pairs_are_observations": explored.leftover_are_observations,
            "leftover_pair_counts": [len(item) for item in leftover_pairs],
        },
        "auto_apply_unique_delta": auto_applied,
        "base_history_length": len(node.history),
        "child_history_lengths": [
            len(child.history) for child in explored.children
        ],
    }


def three_phase_record() -> dict[str, object]:
    """Timestamp-free fold over sealed C3 L/mu1 and F/mu1."""
    bounds = Bounds(max_items=2, max_arity=2)
    folds = [_fold_reading(READING_L, bounds), _fold_reading(READING_F, bounds)]
    auto_applied = False
    for fold in folds:
        if fold["auto_apply_unique_delta"] is True:
            auto_applied = True
            break
    return {
        "authority_effect": "None",
        "schema": "alpha-engine-pea-v1",
        "receipt_is_not_proof": True,
        "field_layout_is_not_temporal_proof": True,
        "demand_generation": "OPEN",
        "ob_1": "OPEN",
        "driver_b": "OPEN",
        "auto_apply_unique_delta": auto_applied,
        "folds": folds,
    }


def refuse_auto_apply(node: Node, result: EvalResult) -> None:
    """Surface used by the UniqueDelta injection."""
    apply_unique_delta(node, result)
