"""Target G014: Multi-Observer Descent & Natural Transport.

This module formalizes multi-observer descent, joint observation fiber spaces,
sheaf-like gluing conditions over finite observer covers, natural transport across
frame automorphisms, duplicate observer agreement, and explicit obstruction witnesses.

AuthorityEffect: None.
Claim Hygiene: Discrete finite carrier models; all properties exact and constructive.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, Generic, Mapping, Sequence, TypeVar

T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True)
class Result(Generic[T, E]):
    """Monadic Result type for explicit failure and refusal tracking."""

    _value: T | None
    _error: E | None
    _is_ok: bool

    @classmethod
    def ok(cls, value: T) -> Result[T, E]:
        return cls(_value=value, _error=None, _is_ok=True)

    @classmethod
    def err(cls, error: E) -> Result[T, E]:
        return cls(_value=None, _error=error, _is_ok=False)

    def is_ok(self) -> bool:
        return self._is_ok

    def is_err(self) -> bool:
        return not self._is_ok

    def unwrap(self) -> T:
        if not self._is_ok:
            raise ValueError(f"Called unwrap on Err: {self._error}")
        assert self._value is not None
        return self._value

    def unwrap_err(self) -> E:
        if self._is_ok:
            raise ValueError("Called unwrap_err on Ok")
        assert self._error is not None
        return self._error


@dataclass(frozen=True)
class CarrierState:
    """Discrete finite multi-locus carrier state."""

    data: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        # Check uniqueness of loci keys
        keys = [k for k, _ in self.data]
        if len(keys) != len(set(keys)):
            raise ValueError("Duplicate locus in carrier state")

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, int]) -> CarrierState:
        sorted_pairs = tuple(sorted(mapping.items(), key=lambda p: p[0]))
        return cls(data=sorted_pairs)

    def to_dict(self) -> dict[str, int]:
        return dict(self.data)

    def get(self, locus: str, default: int | None = None) -> int | None:
        for k, v in self.data:
            if k == locus:
                return v
        return default

    @property
    def loci(self) -> tuple[str, ...]:
        return tuple(k for k, _ in self.data)


@dataclass(frozen=True)
class Observer:
    """An observer inspecting a finite sub-sector (subset of loci)."""

    observer_id: str
    loci: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.loci) != len(set(self.loci)):
            raise ValueError("Duplicate locus in observer projection definition")
        # Keep loci sorted canonically
        object.__setattr__(self, "loci", tuple(sorted(self.loci)))

    def project(self, state: CarrierState) -> CarrierState:
        """Observation readout: projects state onto observer's loci."""
        state_dict = state.to_dict()
        sub_data = tuple((loc, state_dict[loc]) for loc in self.loci if loc in state_dict)
        return CarrierState(data=sub_data)


@dataclass(frozen=True)
class GluingObstruction:
    """Explicit witness of a failed descent/gluing condition."""

    observer_1: str
    observer_2: str
    overlap_locus: str
    value_1: int
    value_2: int

    def summary(self) -> str:
        return (
            f"Obstruction between observer '{self.observer_1}' and '{self.observer_2}' "
            f"on locus '{self.overlap_locus}': {self.value_1} != {self.value_2}"
        )


@dataclass(frozen=True)
class DescentCoverage:
    """A finite family of observers covering a locus universe."""

    observers: tuple[Observer, ...]

    def __post_init__(self) -> None:
        ids = [obs.observer_id for obs in self.observers]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate observer ID in coverage")

    @property
    def total_covered_loci(self) -> tuple[str, ...]:
        all_loci: set[str] = set()
        for obs in self.observers:
            all_loci.update(obs.loci)
        return tuple(sorted(all_loci))

    def is_total_cover_for(self, state: CarrierState) -> bool:
        covered = set(self.total_covered_loci)
        return all(loc in covered for loc in state.loci)

    def check_compatibility(
        self, records: Mapping[str, CarrierState]
    ) -> Result[None, GluingObstruction]:
        """Check pairwise sheaf-compatibility on overlapping loci."""
        # Check all pairs
        for i in range(len(self.observers)):
            obs_i = self.observers[i]
            rec_i = records.get(obs_i.observer_id)
            if rec_i is None:
                continue
            dict_i = rec_i.to_dict()
            for j in range(i + 1, len(self.observers)):
                obs_j = self.observers[j]
                rec_j = records.get(obs_j.observer_id)
                if rec_j is None:
                    continue
                dict_j = rec_j.to_dict()

                overlap = set(obs_i.loci).intersection(set(obs_j.loci))
                for loc in sorted(overlap):
                    val_i = dict_i.get(loc)
                    val_j = dict_j.get(loc)
                    if val_i is not None and val_j is not None and val_i != val_j:
                        return Result.err(
                            GluingObstruction(
                                observer_1=obs_i.observer_id,
                                observer_2=obs_j.observer_id,
                                overlap_locus=loc,
                                value_1=val_i,
                                value_2=val_j,
                            )
                        )
        return Result.ok(None)

    def glue(
        self, records: Mapping[str, CarrierState]
    ) -> Result[CarrierState, GluingObstruction]:
        """Sheaf-like gluing of compatible local observer records into a global state."""
        compat_res = self.check_compatibility(records)
        if compat_res.is_err():
            return Result.err(compat_res.unwrap_err())

        glued_dict: dict[str, int] = {}
        for obs in self.observers:
            rec = records.get(obs.observer_id)
            if rec is not None:
                for loc, val in rec.data:
                    glued_dict[loc] = val

        return Result.ok(CarrierState.from_mapping(glued_dict))


def natural_transport(
    obs: Observer, state: CarrierState, locus_perm: Mapping[str, str]
) -> tuple[Observer, CarrierState, CarrierState]:
    """Transport an observer and carrier state along a frame automorphism / permutation.

    Returns:
    - Transported observer sigma(O)
    - Transported state sigma(S)
    - Transported readout sigma(pi_O(S))
    """
    transported_loci = tuple(locus_perm.get(loc, loc) for loc in obs.loci)
    transported_obs = Observer(
        observer_id=f"{obs.observer_id}_transported",
        loci=transported_loci,
    )

    state_dict = state.to_dict()
    transported_state_dict = {
        locus_perm.get(k, k): v for k, v in state_dict.items()
    }
    transported_state = CarrierState.from_mapping(transported_state_dict)

    transported_readout = transported_obs.project(transported_state)
    return transported_obs, transported_state, transported_readout


def verify_descent_and_gluing_invariants(
    coverage: DescentCoverage, state: CarrierState
) -> dict[str, Any]:
    """Verify all G014 descent, gluing, natural transport, and obstruction invariants."""
    # 1. Generate local records
    records = {obs.observer_id: obs.project(state) for obs in coverage.observers}

    # 2. Verify compatible records glue to unique global state
    glue_res = coverage.glue(records)
    assert glue_res.is_ok(), f"Compatible records failed to glue: {glue_res.unwrap_err()}"
    glued_state = glue_res.unwrap()

    # If coverage is total, glued state must match original state exactly
    if coverage.is_total_cover_for(state):
        assert glued_state == state, "Glued state does not equal original state"

    # 3. Verify gluing preserves every required observation
    for obs in coverage.observers:
        projected_from_glued = obs.project(glued_state)
        original_record = records[obs.observer_id]
        assert (
            projected_from_glued == original_record
        ), f"Gluing altered observation for observer {obs.observer_id}"

    # 4. Construct explicit obstruction witness (perturbed record)
    obstruction_witness_verified = False
    if len(coverage.observers) >= 2:
        obs1 = coverage.observers[0]
        obs2 = coverage.observers[1]
        overlap = set(obs1.loci).intersection(set(obs2.loci))
        if overlap:
            test_locus = sorted(overlap)[0]
            perturbed_records = dict(records)
            orig_rec = records[obs2.observer_id]
            perturbed_dict = orig_rec.to_dict()
            perturbed_dict[test_locus] = (perturbed_dict[test_locus] + 1)
            perturbed_records[obs2.observer_id] = CarrierState.from_mapping(perturbed_dict)

            obstructed_glue = coverage.glue(perturbed_records)
            assert obstructed_glue.is_err(), "Perturbed incompatible records failed to obstruct"
            err = obstructed_glue.unwrap_err()
            assert err.overlap_locus == test_locus
            assert err.value_1 != err.value_2
            obstruction_witness_verified = True

    # 5. Natural transport commutation
    locus_perm = {loc: f"perm_{loc}" for loc in state.loci}
    obs0 = coverage.observers[0]
    t_obs, t_state, t_readout = natural_transport(obs0, state, locus_perm)
    orig_readout = obs0.project(state)
    expected_readout_dict = {
        locus_perm[k]: v for k, v in orig_readout.to_dict().items()
    }
    assert t_readout.to_dict() == expected_readout_dict, "Natural transport failed commutation"

    return {
        "status": "PASS",
        "total_observers": len(coverage.observers),
        "total_covered_loci": len(coverage.total_covered_loci),
        "glued_state_equality": glued_state == state if coverage.is_total_cover_for(state) else "partial",
        "obstruction_witness_verified": obstruction_witness_verified,
        "natural_transport_commutes": True,
    }
