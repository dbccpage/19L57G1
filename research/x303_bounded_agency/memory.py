"""Finite FIFO memory horizon. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass

from . import _bootstrap  # noqa: F401
from research.x301_formal_semantics.semantics import RationalValuation


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
    """FIFO buffer of depth H with deterministic eviction."""

    horizon: int
    records: tuple[MemoryRecord, ...] = ()

    def __post_init__(self) -> None:
        if self.horizon < 1:
            raise ValueError(f"Memory horizon H must be at least 1, got {self.horizon}")
        if len(self.records) > self.horizon:
            object.__setattr__(self, "records", self.records[-self.horizon :])

    def append(self, record: MemoryRecord) -> BoundedMemory:
        new_records = (self.records + (record,))[-self.horizon :]
        return BoundedMemory(horizon=self.horizon, records=new_records)

    def is_full(self) -> bool:
        return len(self.records) >= self.horizon

    def __len__(self) -> int:
        return len(self.records)
