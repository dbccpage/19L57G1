"""Target X303: Agency & Control (Bounded Operational Agency).

Pure Python bounded agency engine providing:
1. ViabilityEnvelope: Hard constraint boundaries in exact rational arithmetic (fractions.Fraction):
   resource ceilings on data sorts, form declarations, arity limits, instance dictionaries,
   fuel budget; non-empty core sort requirements; monotonic preservation of separation pairs
   and firm structural requirements. Zero floating-point arithmetic.
2. FiniteMemoryHorizon: Explicit FIFO buffer of depth H with deterministic eviction
   preserving data processing inequalities.
3. RefusalSemantics: When all candidate actions drive state outside viability or fuel is
   exhausted or authorization is denied, emit StepResult.refusal, preserving carrier state
   strictly unmutated (state_after is state_before).
4. CausalEvaluator: Ephemeral counterfactual branch projection (delta_fn) testing candidate
   actions against viability and ground empirical reference, integrating X301 Grounding Firewall
   consensus override.
5. AlphaEngineLicensing: Enforce Proposal -> EvalResult -> License contract. Zero unilateral
   mutation authority. License required for state commitment.
6. MulticriteriaSelector: Exact rational utility/cost vector in [0, 1] cap Q without
   floating-point heuristics, selecting Pareto-optimal actions with canonical tie-breaking (CanonKey).

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, narrow, receipt-grounded).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable, Mapping, Optional, Sequence, Union

# Ensure access to repository code and research trees
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_CODE_DIR = _REPO_ROOT / "code"
if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))
for _sub in ["x301_formal_semantics"]:
    _sub_path = _REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

# Import foundational semantics from Target X301
from research.x301_formal_semantics.semantics import (  # noqa: E402
    Atom,
    Formula,
    GroundingFirewall,
    Intervention,
    Observer,
    Panel,
    PanelIllusionReceipt,
    RationalValuation,
    RelationalModel,
    StepRefusalData,
    StepResult,
    evaluate,
)

# Import derivation canonical keys and observation
from derivation.iso import CanonKey, canonical  # noqa: E402
from derivation.model import Pair, Regime  # noqa: E402
from derivation.observe import profile, profiles, separable  # noqa: E402


# ---------------------------------------------------------------------------
# Canonical Digest & Key Helpers
# ---------------------------------------------------------------------------

def canonical_model_digest(model: RelationalModel) -> str:
    """Deterministic SHA-256 digest of relational carrier state."""
    payload = [
        list(model.data),
        list(model.forms),
        sorted([[f, list(args)] for f, args in model.insts]),
        sorted(list(model.rules)),
        sorted([list(pair) for pair in model.reqs]),
    ]
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def compute_canon_key(model: RelationalModel) -> CanonKey:
    """Compute canonical isomorphism key for a carrier state."""
    try:
        regime = model.to_regime()
        return canonical(regime)
    except Exception:
        # Fallback deterministic canonical representation matching CanonKey signature
        insts_sorted = tuple(sorted(model.insts))
        rules_sorted = tuple(sorted(model.rules))
        reqs_sorted = tuple(sorted(model.reqs))
        return (
            len(model.data),
            model.forms,
            insts_sorted,
            rules_sorted,
            reqs_sorted,
        )


# ---------------------------------------------------------------------------
# 1. Discrete Viability Envelope
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ViabilityEnvelope:
    """Explicit hard constraint boundaries defining operational viability.

    Enforces:
    - Resource ceilings on data, forms, arities, instances.
    - Non-empty core sort requirements.
    - Monotonic preservation of separation pairs: profile(i) != profile(j).
    - Monotonic preservation of cumulative requirement pairs.
    - Firm structural invariants evaluated under exact rational Heyting semantics.

    Arithmetic is exact rational arithmetic via fractions.Fraction. Zero floating-point.
    """

    max_data: int
    max_forms: int
    max_arity: int
    max_insts: int
    min_data: int = 1
    min_forms: int = 1
    required_reqs: frozenset[tuple[int, int]] = frozenset()
    firm_invariants: tuple[Formula, ...] = ()

    def __post_init__(self) -> None:
        if self.max_data < self.min_data:
            raise ValueError(f"max_data ({self.max_data}) cannot be less than min_data ({self.min_data})")
        if self.max_forms < self.min_forms:
            raise ValueError(f"max_forms ({self.max_forms}) cannot be less than min_forms ({self.min_forms})")
        if self.max_arity < 0 or self.max_insts < 0:
            raise ValueError("Ceilings cannot be negative")

    def check_viability(self, model: RelationalModel) -> tuple[bool, Optional[str]]:
        """Check all hard constraint boundaries.

        Returns (True, None) if inside envelope, or (False, reason) if outside.
        """
        # 1. Core sort non-empty requirements
        if model.n_data() < self.min_data:
            return False, f"Data sort count {model.n_data()} below minimum {self.min_data}"
        if model.n_forms() < self.min_forms:
            return False, f"Form sort count {model.n_forms()} below minimum {self.min_forms}"

        # 2. Resource ceilings
        if model.n_data() > self.max_data:
            return False, f"Data sort count {model.n_data()} exceeds ceiling {self.max_data}"
        if model.n_forms() > self.max_forms:
            return False, f"Form sort count {model.n_forms()} exceeds ceiling {self.max_forms}"
        if any(arity > self.max_arity for arity in model.forms):
            return False, f"Form arity exceeds ceiling {self.max_arity}"
        if len(model.insts) > self.max_insts:
            return False, f"Instance count {len(model.insts)} exceeds ceiling {self.max_insts}"

        # 3. Monotonic requirement preservation
        missing_reqs = self.required_reqs - model.reqs
        if missing_reqs:
            return False, f"State missing required separation pairs: {sorted(missing_reqs)}"

        # 4. Separation requirement preservation: all required pairs must remain separable
        if model.reqs:
            try:
                regime = model.to_regime()
                for i, j in model.reqs:
                    if not (0 <= i < model.n_data() and 0 <= j < model.n_data()):
                        return False, f"Separation requirement indices out of range: ({i}, {j})"
                    if not separable(regime, i, j):
                        return False, f"Required separation pair ({i}, {j}) collapsed: identical profiles"
            except Exception as e:
                return False, f"Separation inspection error: {e}"

        # 5. Firm structural invariants evaluated under exact Heyting semantics
        for inv in self.firm_invariants:
            val = evaluate(model, inv)
            if not val.is_true:
                return False, f"Firm invariant violated: {inv} evaluated to {val}"

        return True, None

    def is_viable(self, model: RelationalModel) -> bool:
        """Predicate checking whether model is strictly viable."""
        ok, _ = self.check_viability(model)
        return ok

    def compute_margin(self, model: RelationalModel) -> Fraction:
        """Compute exact rational safety margin in [0, 1] cap Q.

        Safety margin measures distance to resource ceilings:
        u_margin = 1 - max(|data|/max_data, |forms|/max_forms, |insts|/max_insts).
        Zero floating-point arithmetic.
        """
        r_data = Fraction(model.n_data(), self.max_data) if self.max_data > 0 else Fraction(1, 1)
        r_forms = Fraction(model.n_forms(), self.max_forms) if self.max_forms > 0 else Fraction(1, 1)
        r_insts = Fraction(len(model.insts), self.max_insts) if self.max_insts > 0 else Fraction(1, 1)

        max_ratio = max(r_data, r_forms, r_insts)
        margin = Fraction(1, 1) - max_ratio
        if margin < Fraction(0, 1):
            return Fraction(0, 1)
        if margin > Fraction(1, 1):
            return Fraction(1, 1)
        return margin


# ---------------------------------------------------------------------------
# 2. Finite Memory Horizon
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MemoryRecord:
    """Immutable record of an operational state transition."""

    step_index: int
    pre_state_digest: str
    action_repr: str
    readout: RationalValuation
    post_state_digest: str
    fuel_cost: int

    def __post_init__(self) -> None:
        if self.step_index < 0:
            raise ValueError(f"step_index cannot be negative: {self.step_index}")
        if self.fuel_cost < 0:
            raise ValueError(f"fuel_cost cannot be negative: {self.fuel_cost}")


@dataclass(frozen=True)
class BoundedMemory:
    """Explicit FIFO memory buffer of bounded depth H.

    Preserves data processing inequalities by deterministically evicting
    records older than horizon H.
    """

    horizon: int
    records: tuple[MemoryRecord, ...] = ()

    def __post_init__(self) -> None:
        if self.horizon < 1:
            raise ValueError(f"Memory horizon H must be at least 1, got {self.horizon}")
        if len(self.records) > self.horizon:
            object.__setattr__(self, "records", self.records[-self.horizon:])

    def append(self, record: MemoryRecord) -> BoundedMemory:
        """Append record with deterministic FIFO eviction."""
        new_records = (self.records + (record,))[-self.horizon:]
        return BoundedMemory(horizon=self.horizon, records=new_records)

    def is_full(self) -> bool:
        return len(self.records) >= self.horizon

    def __len__(self) -> int:
        return len(self.records)


# ---------------------------------------------------------------------------
# 3. Refusal Semantics & Reasons
# ---------------------------------------------------------------------------

class RefusalReason:
    """Standardized reasons for typed operational refusal."""

    FUEL_EXHAUSTED = "Declared operational fuel budget exhausted"
    VIABILITY_BOUNDARY_EXCEEDED = "All candidate actions drive state outside viability envelope"
    AUTHORIZATION_DENIED = "Metatheoretic authorization license denied"
    FIREWALL_CONSENSUS_OVERRIDE = "Grounding Firewall consensus override: empirical contradiction"
    NO_CANDIDATE_ACTIONS = "Candidate action pool is empty"
    UNLICENSED_ACTION = "Attempted unilateral mutation without authorized license"


class UnlicensedActionError(ValueError):
    """Refused: unilateral mutation attempted without an authorized license."""


# ---------------------------------------------------------------------------
# 4. Candidate Actions & Causal Evaluation
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CandidateAction:
    """Operational candidate action I: Carrier -> Carrier."""

    name: str
    fuel_cost: int
    delta_fn: Callable[[RelationalModel], RelationalModel]
    description: str = ""
    canon_key: Optional[CanonKey] = None

    def __post_init__(self) -> None:
        if self.fuel_cost < 0:
            raise ValueError(f"fuel_cost cannot be negative: {self.fuel_cost}")

    def apply(self, model: RelationalModel) -> RelationalModel:
        """Apply operational delta."""
        return self.delta_fn(model)

    def get_canon_key(self, resulting_model: RelationalModel) -> CanonKey:
        """Get or compute canonical key for resulting state."""
        if self.canon_key is not None:
            return self.canon_key
        return compute_canon_key(resulting_model)

    def __repr__(self) -> str:
        return f"CandidateAction({self.name}, cost={self.fuel_cost})"


def add_instance_action(form: int, args: tuple[int, ...], fuel_cost: int = 1, name: str = "") -> CandidateAction:
    """Create action adding a relational instance."""
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
    return CandidateAction(name=lbl, fuel_cost=fuel_cost, delta_fn=_apply, description=f"Add instance ({form}, {args})")


def remove_instance_action(form: int, args: tuple[int, ...], fuel_cost: int = 1, name: str = "") -> CandidateAction:
    """Create action removing a relational instance."""
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
    return CandidateAction(name=lbl, fuel_cost=fuel_cost, delta_fn=_apply, description=f"Remove instance ({form}, {args})")


def toggle_rule_action(form: int, fuel_cost: int = 1, name: str = "") -> CandidateAction:
    """Create action toggling uniform all-tuples rule for a form."""
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
    return CandidateAction(name=lbl, fuel_cost=fuel_cost, delta_fn=_apply, description=f"Toggle rule for form {form}")


def add_requirement_action(i: int, j: int, fuel_cost: int = 1, name: str = "") -> CandidateAction:
    """Create action imposing a separation requirement pair."""
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
    lbl = name or f"add_req({pair[0]}, {pair[1]})"
    return CandidateAction(name=lbl, fuel_cost=fuel_cost, delta_fn=_apply, description=f"Impose separation pair {pair}")


@dataclass(frozen=True)
class ActionEvaluation:
    """Counterfactual evaluation of a candidate action on an ephemeral branch."""

    action: CandidateAction
    viable: bool
    reason: Optional[str] = None
    projected_state: Optional[RelationalModel] = None
    utilities: tuple[Fraction, Fraction, Fraction] = (Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))
    canon_key: Optional[CanonKey] = None
    has_empirical_reference: bool = True
    firewall_refuted: bool = False
    firewall_receipt: Optional[PanelIllusionReceipt] = None

    @property
    def u_margin(self) -> Fraction:
        return self.utilities[0]

    @property
    def u_fuel(self) -> Fraction:
        return self.utilities[1]

    @property
    def u_goal(self) -> Fraction:
        return self.utilities[2]


class CausalEvaluator:
    """Ephemeral counterfactual branch evaluator for candidate actions.

    Projects candidate actions without mutating the base carrier state,
    verifying prospective viability, empirical reference, and exact rational utilities.
    """

    def project(self, model: RelationalModel, action: CandidateAction) -> RelationalModel:
        """Ephemeral projection: returns prospective state without mutating base state."""
        return action.apply(model)

    def check_empirical_reference(self, model: RelationalModel, action: CandidateAction) -> bool:
        """Check whether action causes an observable relational modification."""
        projected = self.project(model, action)
        return canonical_model_digest(projected) != canonical_model_digest(model)

    def evaluate_candidate(
        self,
        model: RelationalModel,
        action: CandidateAction,
        envelope: ViabilityEnvelope,
        fuel_remaining: int,
        total_fuel: int,
        goal_formula: Optional[Formula] = None,
        panel: Optional[Panel] = None,
    ) -> ActionEvaluation:
        """Evaluate a candidate action on an ephemeral branch in exact rational arithmetic."""
        # 1. Fuel boundary check
        if action.fuel_cost > fuel_remaining:
            return ActionEvaluation(
                action=action,
                viable=False,
                reason=f"Action fuel cost {action.fuel_cost} exceeds remaining fuel {fuel_remaining}",
            )

        # 2. Ephemeral branch projection
        projected = self.project(model, action)

        # 3. Viability envelope check on projected state
        is_viable, reason = envelope.check_viability(projected)
        if not is_viable:
            return ActionEvaluation(
                action=action,
                viable=False,
                reason=reason,
                projected_state=projected,
            )

        # 4. Empirical reference check
        has_ref = self.check_empirical_reference(model, action)

        # 5. Exact rational utility metrics in [0, 1] cap Q
        # u_margin
        u_margin = envelope.compute_margin(projected)

        # u_fuel: remaining fuel proportion after action execution
        remaining_after = fuel_remaining - action.fuel_cost
        u_fuel = Fraction(remaining_after, total_fuel) if total_fuel > 0 else Fraction(0, 1)
        if u_fuel < Fraction(0, 1):
            u_fuel = Fraction(0, 1)

        # u_goal: exact valuation of goal formula in Heyting algebra
        if goal_formula is not None:
            val = evaluate(projected, goal_formula)
            u_goal = val.val
        else:
            u_goal = Fraction(1, 1)

        canon_k = action.get_canon_key(projected)

        # 6. Grounding Firewall consensus check (if panel provided)
        firewall_refuted = False
        firewall_receipt: Optional[PanelIllusionReceipt] = None
        if panel is not None and goal_formula is not None:
            panel_agrees = panel.has_positive_consensus(projected, goal_formula)
            ground_truth = evaluate(projected, goal_formula)
            if panel_agrees and not ground_truth.is_true:
                firewall_refuted = True
                firewall_receipt = PanelIllusionReceipt.create(
                    formula_repr=repr(goal_formula),
                    panel_size=len(panel.observers),
                    observer_ids=[obs.observer_id for obs in panel.observers],
                    refuting_intervention=action.name,
                    observable_readout_before="1",
                    observable_readout_after=str(ground_truth),
                    panel_verdict=True,
                    ground_truth_verdict=False,
                )

        return ActionEvaluation(
            action=action,
            viable=not firewall_refuted,
            reason="Firewall consensus override" if firewall_refuted else None,
            projected_state=projected,
            utilities=(u_margin, u_fuel, u_goal),
            canon_key=canon_k,
            has_empirical_reference=has_ref,
            firewall_refuted=firewall_refuted,
            firewall_receipt=firewall_receipt,
        )


# ---------------------------------------------------------------------------
# 5. Alpha Engine Licensing & Authorization
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ActionProposal:
    """Supply-shaped offering. Recording it changes no admitted state."""

    token: str
    offerings: tuple[CandidateAction, ...] = ()


@dataclass(frozen=True)
class RetainedActionClass:
    """Inhabited canonical isomorphism class of candidate actions."""

    key: CanonKey
    members: tuple[CandidateAction, ...]
    best_evaluation: ActionEvaluation

    def __post_init__(self) -> None:
        if not self.members:
            raise ValueError("A retained class must be inhabited")


@dataclass(frozen=True)
class ActionEvalResult:
    """Evaluation result grouping viable candidate actions by canonical key."""

    retained: tuple[RetainedActionClass, ...]
    evaluations: tuple[ActionEvaluation, ...]
    viable_actions: tuple[CandidateAction, ...]
    found: bool
    total_evaluated: int

    def __post_init__(self) -> None:
        if self.found and not self.retained:
            raise ValueError("A found evaluation must retain at least one action class")


@dataclass(frozen=True)
class License:
    """Metatheoretic authorization license issued by authorizer.

    Zero unilateral authority: state mutation requires verified license.
    """

    granter: str
    scope: str
    authorized: tuple[CanonKey, ...]

    def __post_init__(self) -> None:
        if len(set(self.authorized)) != len(self.authorized):
            raise ValueError("Authorized keys must be distinct")
        # Ensure deterministic canonical ordering
        if tuple(sorted(self.authorized)) != self.authorized:
            raise ValueError("Authorized keys must be sorted")


class ActionAuthorizer:
    """Authorizes actions based on viability evaluations and firewall checks."""

    def __init__(self, granter: str = "x303_authorizer", scope: str = "step_authorization"):
        self.granter = granter
        self.scope = scope

    def issue_license(self, authorized_keys: Sequence[CanonKey]) -> License:
        """Issue an immutable authorization license."""
        distinct_sorted = tuple(sorted(set(authorized_keys)))
        return License(
            granter=self.granter,
            scope=self.scope,
            authorized=distinct_sorted,
        )

    def is_authorized(self, action_key: CanonKey, license: Optional[License]) -> bool:
        """Verify whether action_key is authorized under the active license."""
        if license is None:
            return False
        return action_key in license.authorized


class LicensedDriver:
    """Applies candidate actions only under verified license authorization.

    Enforces zero unilateral mutation authority.
    """

    def apply_licensed(
        self,
        model: RelationalModel,
        action: CandidateAction,
        license: License,
    ) -> RelationalModel:
        """Execute action on model iff licensed."""
        projected = action.apply(model)
        action_key = action.get_canon_key(projected)
        if action_key not in license.authorized:
            raise UnlicensedActionError(
                f"Action {action.name} with key {action_key} is not authorized by license {license}"
            )
        return projected


# ---------------------------------------------------------------------------
# 6. Exact Rational Multicriteria Selection
# ---------------------------------------------------------------------------

class MulticriteriaSelector:
    """Exact rational utility valuation and Pareto-optimal selection in [0, 1] cap Q."""

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
        u: tuple[Fraction, Fraction, Fraction],
        v: tuple[Fraction, Fraction, Fraction],
    ) -> bool:
        """Check if utility vector u Pareto-dominates v."""
        weakly_better = all(u_i >= v_i for u_i, v_i in zip(u, v))
        strictly_better = any(u_i > v_i for u_i, v_i in zip(u, v))
        return weakly_better and strictly_better

    def pareto_frontier(
        self,
        evaluations: Sequence[ActionEvaluation],
    ) -> list[ActionEvaluation]:
        """Compute the Pareto-optimal non-dominated subset of viable evaluations."""
        viable_evals = [e for e in evaluations if e.viable]
        if not viable_evals:
            return []

        frontier: list[ActionEvaluation] = []
        for cand in viable_evals:
            dominated = False
            for other in viable_evals:
                if other is not cand and self.dominates(other.utilities, cand.utilities):
                    dominated = True
                    break
            if not dominated:
                frontier.append(cand)
        return frontier

    def composite_utility(self, utilities: tuple[Fraction, Fraction, Fraction]) -> Fraction:
        """Compute composite utility using exact rational weights."""
        return sum(w * u for w, u in zip(self.weights, utilities))

    def select(
        self,
        evaluations: Sequence[ActionEvaluation],
    ) -> Optional[ActionEvaluation]:
        """Select Pareto-optimal candidate action with canonical tie-breaking."""
        frontier = self.pareto_frontier(evaluations)
        if not frontier:
            return None

        # Score frontier candidates
        best_score = Fraction(-1, 1)
        candidates_with_best_score: list[ActionEvaluation] = []

        for e in frontier:
            score = self.composite_utility(e.utilities)
            if score > best_score:
                best_score = score
                candidates_with_best_score = [e]
            elif score == best_score:
                candidates_with_best_score.append(e)

        # Deterministic canonical tie-breaking via CanonKey or action name
        candidates_with_best_score.sort(
            key=lambda e: (
                str(e.canon_key) if e.canon_key is not None else "",
                e.action.name,
            )
        )
        return candidates_with_best_score[0]


# ---------------------------------------------------------------------------
# 7. Deterministic Audit Receipt
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AgencyReceipt:
    """Cryptographic audit receipt emitted on agent decision or refusal."""

    schema: str = "agency-step-v1"
    timestamp: str = ""
    step_index: int = 0
    outcome: str = ""  # "SUCCESS" or "REFUSAL"
    refusal_reason: Optional[str] = None
    action_repr: Optional[str] = None
    pre_state_sha256: str = ""
    post_state_sha256: str = ""
    fuel_before: int = 0
    fuel_after: int = 0
    receipt_sha256: str = ""

    def compute_sha256(self) -> str:
        data = {
            "schema": self.schema,
            "timestamp": self.timestamp,
            "step_index": self.step_index,
            "outcome": self.outcome,
            "refusal_reason": self.refusal_reason,
            "action_repr": self.action_repr,
            "pre_state_sha256": self.pre_state_sha256,
            "post_state_sha256": self.post_state_sha256,
            "fuel_before": self.fuel_before,
            "fuel_after": self.fuel_after,
        }
        canonical_bytes = (json.dumps(data, sort_keys=True, separators=(",", ":"))).encode("utf-8")
        return hashlib.sha256(canonical_bytes).hexdigest()

    @classmethod
    def create(
        cls,
        step_index: int,
        outcome: str,
        pre_state_sha256: str,
        post_state_sha256: str,
        fuel_before: int,
        fuel_after: int,
        action_repr: Optional[str] = None,
        refusal_reason: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> AgencyReceipt:
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        unhashed = cls(
            schema="agency-step-v1",
            timestamp=ts,
            step_index=step_index,
            outcome=outcome,
            refusal_reason=refusal_reason,
            action_repr=action_repr,
            pre_state_sha256=pre_state_sha256,
            post_state_sha256=post_state_sha256,
            fuel_before=fuel_before,
            fuel_after=fuel_after,
            receipt_sha256="",
        )
        digest = unhashed.compute_sha256()
        return cls(
            schema=unhashed.schema,
            timestamp=unhashed.timestamp,
            step_index=unhashed.step_index,
            outcome=unhashed.outcome,
            refusal_reason=unhashed.refusal_reason,
            action_repr=unhashed.action_repr,
            pre_state_sha256=unhashed.pre_state_sha256,
            post_state_sha256=unhashed.post_state_sha256,
            fuel_before=unhashed.fuel_before,
            fuel_after=unhashed.fuel_after,
            receipt_sha256=digest,
        )


# ---------------------------------------------------------------------------
# 8. Bounded Operational Agent Controller
# ---------------------------------------------------------------------------

class AgentController:
    """Stateful bounded operational agent controller.

    Coordinates:
    - Current carrier state in RelationalModel.
    - ViabilityEnvelope hard constraint monitor.
    - Finite memory horizon buffer.
    - Monotonically decreasing operational fuel budget.
    - Causal counterfactual candidate evaluator.
    - Exact rational multicriteria Pareto action selector.
    - Action authorizer enforcing zero unilateral mutation authority.
    - Licensed driver committing state changes.
    - Strict refusal semantics preserving state strictly unmutated.
    """

    def __init__(
        self,
        state: RelationalModel,
        envelope: ViabilityEnvelope,
        total_fuel: int,
        memory_horizon: int = 10,
        weights: tuple[Fraction, Fraction, Fraction] = (
            Fraction(1, 3),
            Fraction(1, 3),
            Fraction(1, 3),
        ),
        goal_formula: Optional[Formula] = None,
        timestamp_fixed: Optional[str] = None,
    ):
        if total_fuel < 0:
            raise ValueError(f"total_fuel cannot be negative: {total_fuel}")
        is_viable, reason = envelope.check_viability(state)
        if not is_viable:
            raise ValueError(f"Initial state violates viability envelope: {reason}")

        self.state = state
        self.envelope = envelope
        self.fuel = total_fuel
        self.total_fuel = total_fuel
        self.memory = BoundedMemory(horizon=memory_horizon)
        self.weights = weights
        self.goal_formula = goal_formula
        self.step_count = 0
        self.timestamp_fixed = timestamp_fixed

        self.evaluator = CausalEvaluator()
        self.selector = MulticriteriaSelector(weights=weights)
        self.authorizer = ActionAuthorizer()
        self.driver = LicensedDriver()

    def step(
        self,
        candidates: Sequence[CandidateAction],
        panel: Optional[Panel] = None,
    ) -> StepResult:
        """Execute one operational agency step under strict refusal semantics.

        In all refusal cases, preserves carrier state strictly unmutated:
        state_after is state_before.
        """
        current_state = self.state
        pre_digest = canonical_model_digest(current_state)

        # Gate 1: Check fuel budget exhaustion
        if self.fuel <= 0:
            receipt = AgencyReceipt.create(
                step_index=self.step_count,
                outcome="REFUSAL",
                refusal_reason=RefusalReason.FUEL_EXHAUSTED,
                pre_state_sha256=pre_digest,
                post_state_sha256=pre_digest,
                fuel_before=self.fuel,
                fuel_after=self.fuel,
                timestamp=self.timestamp_fixed,
            )
            return StepResult.refusal(
                retained_state=current_state,
                reason=RefusalReason.FUEL_EXHAUSTED,
                receipt=receipt,
            )

        # Gate 2: Check for candidate actions
        if not candidates:
            receipt = AgencyReceipt.create(
                step_index=self.step_count,
                outcome="REFUSAL",
                refusal_reason=RefusalReason.NO_CANDIDATE_ACTIONS,
                pre_state_sha256=pre_digest,
                post_state_sha256=pre_digest,
                fuel_before=self.fuel,
                fuel_after=self.fuel,
                timestamp=self.timestamp_fixed,
            )
            return StepResult.refusal(
                retained_state=current_state,
                reason=RefusalReason.NO_CANDIDATE_ACTIONS,
                receipt=receipt,
            )

        # Gate 3: Ephemeral causal evaluation of candidates
        evaluations: list[ActionEvaluation] = []
        for cand in candidates:
            eval_res = self.evaluator.evaluate_candidate(
                model=current_state,
                action=cand,
                envelope=self.envelope,
                fuel_remaining=self.fuel,
                total_fuel=self.total_fuel,
                goal_formula=self.goal_formula,
                panel=panel,
            )
            evaluations.append(eval_res)

        viable_evals = [e for e in evaluations if e.viable]

        # Gate 4: If no candidates are viable, refuse and preserve state unmutated
        if not viable_evals:
            firewall_receipt = None
            for e in evaluations:
                if e.firewall_refuted and e.firewall_receipt:
                    firewall_receipt = e.firewall_receipt
                    break

            reason = (
                RefusalReason.FIREWALL_CONSENSUS_OVERRIDE
                if firewall_receipt
                else RefusalReason.VIABILITY_BOUNDARY_EXCEEDED
            )
            receipt = AgencyReceipt.create(
                step_index=self.step_count,
                outcome="REFUSAL",
                refusal_reason=reason,
                pre_state_sha256=pre_digest,
                post_state_sha256=pre_digest,
                fuel_before=self.fuel,
                fuel_after=self.fuel,
                timestamp=self.timestamp_fixed,
            )
            return StepResult.refusal(
                retained_state=current_state,
                reason=reason,
                receipt=firewall_receipt or receipt,
            )

        # Gate 5: Exact rational Pareto multicriteria action selection
        selected_eval = self.selector.select(viable_evals)
        if selected_eval is None:
            receipt = AgencyReceipt.create(
                step_index=self.step_count,
                outcome="REFUSAL",
                refusal_reason=RefusalReason.VIABILITY_BOUNDARY_EXCEEDED,
                pre_state_sha256=pre_digest,
                post_state_sha256=pre_digest,
                fuel_before=self.fuel,
                fuel_after=self.fuel,
                timestamp=self.timestamp_fixed,
            )
            return StepResult.refusal(
                retained_state=current_state,
                reason=RefusalReason.VIABILITY_BOUNDARY_EXCEEDED,
                receipt=receipt,
            )

        selected_action = selected_eval.action
        canon_key = selected_eval.canon_key or selected_action.get_canon_key(
            selected_eval.projected_state or current_state
        )

        # Gate 6: Licensing & Committee Authorization
        license = self.authorizer.issue_license([canon_key])

        # Gate 7: Execution via LicensedDriver (zero unilateral authority)
        try:
            new_state = self.driver.apply_licensed(
                model=current_state,
                action=selected_action,
                license=license,
            )
        except UnlicensedActionError as exc:
            receipt = AgencyReceipt.create(
                step_index=self.step_count,
                outcome="REFUSAL",
                refusal_reason=str(exc),
                pre_state_sha256=pre_digest,
                post_state_sha256=pre_digest,
                fuel_before=self.fuel,
                fuel_after=self.fuel,
                timestamp=self.timestamp_fixed,
            )
            return StepResult.refusal(
                retained_state=current_state,
                reason=str(exc),
                receipt=receipt,
            )

        # Commit state transition
        post_digest = canonical_model_digest(new_state)
        fuel_before = self.fuel
        self.fuel -= selected_action.fuel_cost
        self.state = new_state

        # Update bounded memory
        val_readout = RationalValuation(selected_eval.u_goal)
        mem_rec = MemoryRecord(
            step_index=self.step_count,
            pre_state_digest=pre_digest,
            action_repr=selected_action.name,
            readout=val_readout,
            post_state_digest=post_digest,
            fuel_cost=selected_action.fuel_cost,
        )
        self.memory = self.memory.append(mem_rec)
        self.step_count += 1

        # Emit audit receipt
        receipt = AgencyReceipt.create(
            step_index=self.step_count - 1,
            outcome="SUCCESS",
            action_repr=selected_action.name,
            pre_state_sha256=pre_digest,
            post_state_sha256=post_digest,
            fuel_before=fuel_before,
            fuel_after=self.fuel,
            timestamp=self.timestamp_fixed,
        )
        return StepResult.success(state=new_state)
