"""Declared SearchPolicy: a subset of retained iso-class keys.

AuthorityEffect: None.

Input is the sealed retained iso-class key set.  Output is a subset.
Every retained class is recorded explored, pruned, or open, and
explored + pruned + open equals the tie-set size.  A key absent from
the sealed quotient is refused.  A silent drop of a retained class
fails the census.  Selection is a declared subset, not a necessity
claim.
"""

from __future__ import annotations

from dataclasses import dataclass

from derivation.iso import CanonKey

from harness import HarnessError


class FabricatedClassError(HarnessError):
    """A class key absent from the sealed retained set is refused."""


class CensusError(HarnessError):
    """explored + pruned + open must partition the retained set."""


@dataclass(frozen=True)
class PolicyCensus:
    """Partition of one retained tie set."""

    explored: tuple[CanonKey, ...]
    pruned: tuple[CanonKey, ...]
    open_keys: tuple[CanonKey, ...]
    tie_set_size: int

    def __post_init__(self) -> None:
        total = len(self.explored) + len(self.pruned) + len(self.open_keys)
        if total != self.tie_set_size:
            raise CensusError(
                "explored+pruned+open must equal the tie-set size"
            )


@dataclass(frozen=True)
class SearchPolicy:
    """Declared authorizer.  Output keys are a subset of ``retained``."""

    policy_id: str
    justification: str
    retained: tuple[CanonKey, ...]
    explored: tuple[CanonKey, ...]
    pruned: tuple[CanonKey, ...]
    open_keys: tuple[CanonKey, ...]

    def subset(self) -> tuple[CanonKey, ...]:
        """Authorized keys: the explored bucket, checked as a subset."""
        return record_census(
            self.retained, self.explored, self.pruned, self.open_keys
        ).explored

    def census(self) -> PolicyCensus:
        return record_census(
            self.retained, self.explored, self.pruned, self.open_keys
        )


def record_census(
    retained: tuple[CanonKey, ...],
    explored: tuple[CanonKey, ...],
    pruned: tuple[CanonKey, ...],
    open_keys: tuple[CanonKey, ...],
) -> PolicyCensus:
    """Require a disjoint cover of ``retained``.  Name extras and drops."""
    retained_set = frozenset(retained)
    if len(retained_set) != len(retained):
        raise CensusError("retained keys must be distinct")
    buckets = {
        "explored": explored,
        "pruned": pruned,
        "open": open_keys,
    }
    seen: set[CanonKey] = set()
    extras: list[CanonKey] = []
    for name, keys in buckets.items():
        del name
        if len(set(keys)) != len(keys):
            raise CensusError("census buckets cannot duplicate a key")
        for key in keys:
            if key not in retained_set:
                extras.append(key)
            if key in seen:
                raise CensusError("census buckets must be disjoint")
            seen.add(key)
    if extras:
        raise FabricatedClassError(
            "class key absent from the sealed quotient"
        )
    missing = retained_set - seen
    if missing:
        raise CensusError("silent drop of a retained class")
    return PolicyCensus(
        explored=tuple(sorted(explored)),
        pruned=tuple(sorted(pruned)),
        open_keys=tuple(sorted(open_keys)),
        tie_set_size=len(retained),
    )


def declared_explore_first(retained: tuple[CanonKey, ...]) -> SearchPolicy:
    """Declared subset: first key in sealed-key order; remainder open."""
    ordered = tuple(sorted(retained))
    explored = ordered[:1]
    open_keys = ordered[1:]
    return SearchPolicy(
        policy_id="declared-first-key-explored",
        justification=(
            "declared subset: explore the first retained key in "
            "sealed-key order; leave the rest open; prune none"
        ),
        retained=ordered,
        explored=explored,
        pruned=(),
        open_keys=open_keys,
    )
