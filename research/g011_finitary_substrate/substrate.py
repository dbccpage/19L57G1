"""G011: Endogenous Operational Finitary Substrate.

Provides object-level identity, finite ordinals, tree addresses, instruction code,
deterministic freshness allocation, and fuel-bounded structural recursion
without relying on host Nat, host pointers, or host memory order.

Terminal: FINITARY_SUBSTRATE_INTERNAL
AuthorityEffect: None.
"""

from __future__ import annotations
from typing import Sequence

from ordinals import Ordinal, Zero, Succ
from address import Address, Root, Child
from freshness import (
    AddressRegistry,
    fresh_address,
    fresh_index,
    max_branch_index,
    has_branch,
    root_branch_index,
)
from recursion import (
    Val,
    NumVal,
    AddrVal,
    Instr,
    Nop,
    SetZero,
    SuccReg,
    PredReg,
    CopyReg,
    AllocAddr,
    WriteMem,
    ReadMem,
    Jump,
    BranchIfZero,
    Halt,
    State,
    ExecResult,
    Halted,
    OutOfFuel,
    fetch,
    step,
    run_with_fuel,
    rec_fuel,
)

__all__ = [
    "Ordinal",
    "Zero",
    "Succ",
    "Address",
    "Root",
    "Child",
    "AddressRegistry",
    "fresh_address",
    "fresh_index",
    "max_branch_index",
    "has_branch",
    "root_branch_index",
    "Val",
    "NumVal",
    "AddrVal",
    "Instr",
    "Nop",
    "SetZero",
    "SuccReg",
    "PredReg",
    "CopyReg",
    "AllocAddr",
    "WriteMem",
    "ReadMem",
    "Jump",
    "BranchIfZero",
    "Halt",
    "State",
    "ExecResult",
    "Halted",
    "OutOfFuel",
    "fetch",
    "step",
    "run_with_fuel",
    "rec_fuel",
    "build_finitary_substrate",
]


def build_finitary_substrate() -> dict[str, str]:
    """Return status and manifest of the endogenous finitary substrate."""
    return {
        "terminal": "FINITARY_SUBSTRATE_INTERNAL",
        "authority_effect": "None",
        "ordinals": "Pure inductive Zero/Succ",
        "addressing": "Hierarchical tree paths with provable disjointness",
        "freshness": "Deterministic allocation strictly exceeding allocated indices",
        "recursion": "Fuel-bounded structural induction on Ordinal",
    }
