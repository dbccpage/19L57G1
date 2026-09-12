"""Partial substrate <-> relational embedding. AuthorityEffect: None.

Graph, active, and form markers live on a small carrier. Clock, fuel, tape,
nops, and designated pair recover from `custom_domains` / reqs so the
round-trip does not inflate the sealed iso search.
"""
from __future__ import annotations

from typing import Optional

from . import _bootstrap  # noqa: F401
from research.target_a_execution.control import State as SubstrateState
from research.target_a_execution.runner import ProtectionObligation
from research.x301_formal_semantics.semantics import RelationalModel


def encode_substrate_to_relational(state: SubstrateState) -> RelationalModel:
    max_carrier = max(
        state.active,
        max(state.tape) if state.tape else 0,
        max([x for _, args in state.graph for x in args], default=0),
    )
    n_points = max(max_carrier + 1, 2)
    data = tuple(range(n_points))
    forms = (1, 1, 1) + tuple(2 for _ in range(2 * state.nops))
    insts: set[tuple[int, tuple[int, ...]]] = set(state.graph)
    insts.add((0, (state.active % n_points,)))
    reqs: set[tuple[int, int]] = set()
    if state.designated_pair is not None:
        p1, p2 = state.designated_pair
        reqs.add((p1, p2))
    return RelationalModel(
        data=data,
        forms=forms,
        insts=frozenset(insts),
        rules=frozenset(),
        reqs=frozenset(reqs),
        custom_domains={
            "clock": (state.clock,),
            "fuel": (state.fuel,),
            "tape": state.tape,
            "nops": (state.nops,),
        },
    )


def decode_relational_to_substrate(
    model: RelationalModel,
    nops: Optional[int] = None,
    tape: tuple[int, ...] = (),
    protection_obligations: tuple[ProtectionObligation, ...] = (),
    clock: Optional[int] = None,
    fuel: Optional[int] = None,
) -> SubstrateState:
    domains = dict(model.custom_domains)
    rec_nops = int(domains["nops"][0]) if "nops" in domains else (nops if nops is not None else max(0, (len(model.forms) - 3) // 2))
    rec_clock = int(domains["clock"][0]) if "clock" in domains else (clock or 0)
    rec_fuel = int(domains["fuel"][0]) if "fuel" in domains else (fuel or 0)
    rec_tape = tuple(domains["tape"]) if "tape" in domains else tape
    graph_edges: set[tuple[int, tuple[int, ...]]] = {
        (f, args) for f, args in model.insts if f >= 3
    }
    active = 0
    for f, args in model.insts:
        if f == 0 and len(args) == 1:
            active = args[0]
            break
    dp: Optional[tuple[int, int]] = None
    if model.reqs:
        dp = next(iter(model.reqs))
    return SubstrateState(
        graph=frozenset(graph_edges),
        nops=rec_nops,
        active=active,
        tape=rec_tape,
        clock=rec_clock,
        fuel=rec_fuel,
        protection_obligations=protection_obligations,
        designated_pair=dp,
    )
