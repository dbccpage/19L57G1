"""Deterministic mirror of ``lean4/Derivation/GraphGenesis.lean``.

Where can a new occurrence, a new asserted difference, a new
retained difference, or a new protected demand come from?

The mirror computes, over declared finite bounds, exactly what the
Lean module proves:

1. **Field invariance** — an exhaustive event battery on declared
   sample states, recording for every event kind precisely which
   state fields it can move.  The two response events move only
   ``obs`` and ``budget``; the four graph stores move only under the
   supply events of an external driver.
2. **Internal-fragment carrier invariance** — every trace over the
   internal fragment (``refineCol``, ``addCol``, ``declareObs``,
   ``refuse``) up to the declared length leaves ``occ``,
   ``asserted``, ``wit`` and ``prot`` fixed.
3. **The proposal record** — one explicit sufficient represented
   proposal schema, with its obligations as computable checks: a named
   branch plus membership in the COMPLETE Up family (without a
   canonicality or uniqueness claim), an
   embedding with its retraction, freshness of the supplied token,
   preservation of every old asserted / retained / protected pair
   and of every separated pair, the new pair's provenance, and a
   declared cost.  No license, execution, or activation field
   exists on the record.
4. **Transport** — the proposal family transports under the
   renaming action, checked over the FULL permutation group on the
   declared carrier.
5. **Ties retained** — two equal-cost proposals whose executions are
   non-isomorphic; the family records both and certifies neither as
   canonical.
6. **The Part-3 witness** — a state satisfying all four obstruction
   conditions whose complete internal response family is nonempty
   and resolves the obstruction with no carrier change, plus the
   general check that no represented response, at any declared
   sample state, grows the carrier.

Every bound used is declared in the artifact.
"""

from __future__ import annotations

from dataclasses import dataclass, fields as dataclass_fields
from itertools import permutations, product
from typing import Optional, cast

from derivation.attachment_ladder import (
    act,
    isomorphic_undirected,
    path_pol,
    tree_at,
    up_block,
    up_family,
)
from derivation.export import Json
from derivation.primitive_passage import (
    GENESIS_P,
    PS,
    Col,
    Cols,
    Pair,
    PEvent,
    next_family_p,
    obst_p,
    obstructed_pairs,
    preplay,
    pstep,
    sep_p,
)

# ---------------------------------------------------------------------------
# Declared vocabulary: fields and event kinds

STATE_FIELDS: tuple[str, ...] = (
    "occ", "asserted", "wit", "prot", "obs", "budget", "licensed",
    "refusals", "halted")

GRAPH_FIELDS: tuple[str, ...] = ("occ", "asserted", "wit", "prot")

OBSERVATION_FIELDS: tuple[str, ...] = ("obs", "budget")

INTERNAL_KINDS: tuple[str, ...] = (
    "refineCol", "addCol", "declareObs", "refuse")

FUNDING_KINDS: tuple[str, ...] = ("setBudget",)

SUPPLY_KINDS: tuple[str, ...] = (
    "admitOcc", "assertWit", "admitWit", "protect")

CONTROL_KINDS: tuple[str, ...] = ("setBudget", "setLicense", "halt")

ALL_KINDS: tuple[str, ...] = SUPPLY_KINDS + INTERNAL_KINDS + (
    "setBudget", "setLicense", "halt")


def kind(e: PEvent) -> str:
    return cast(str, e[0])


def int_arg(e: PEvent, k: int) -> int:
    return cast(int, e[k])


def col_arg(e: PEvent, k: int) -> Col:
    return cast(Col, e[k])


def is_internal(e: PEvent) -> bool:
    """True exactly on the internal fragment (Lean ``IsInternal``)."""
    return kind(e) in INTERNAL_KINDS


def is_funding(e: PEvent) -> bool:
    return kind(e) in FUNDING_KINDS


def is_response_event(e: PEvent) -> bool:
    """The internal fragment plus the funding event the represented
    family prefixes to a created column (Lean ``IsResponseEvent``)."""
    return is_internal(e) or is_funding(e)


def arg_json(a: object) -> Json:
    if isinstance(a, tuple):
        return [cast(int, x) for x in a]
    return cast(Json, a)


def event_json(e: PEvent) -> list[Json]:
    return [kind(e)] + [arg_json(a) for a in e[1:]]


def block_json(b: tuple[PEvent, ...]) -> list[Json]:
    return [event_json(e) for e in b]


# ---------------------------------------------------------------------------
# Declared sample states and the exhaustive event battery

def blind_pair() -> PS:
    """The Part-3 witness state (Lean ``blindPair``): two
    occurrences, one asserted, retained and protected difference, an
    observation declared but empty — all four obstruction conditions
    hold at the pair ``(0, 1)``."""
    return PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
              prot=((0, 1),), obs=(), budget=0, licensed=True,
              refusals=(), halted=False)


def refinable() -> PS:
    """A state whose same-level repair family is nonempty: refining
    the declared column by position 2 separates the obstructed pair
    and breaks no protected separation."""
    return PS(occ=(0, 1, 2), asserted=((0, 1), (1, 2)),
              wit=((0, 1), (1, 2)), prot=((0, 1), (1, 2)),
              obs=((0,),), budget=2, licensed=True, refusals=(),
              halted=False)


def supply_stages() -> PS:
    """A state at which two supply events are live: the pair
    ``(0, 1)`` is asserted but not retained, and the pair ``(1, 2)``
    is retained but not protected.  It witnesses that the graph
    stores DO move — under supply events, and only there."""
    return PS(occ=(0, 1, 2), asserted=((0, 1), (1, 2)),
              wit=((1, 2),), prot=(), obs=None, budget=1,
              licensed=True, refusals=(), halted=False)


def sample_states() -> tuple[tuple[str, PS], ...]:
    """The declared sample pre-states.  One pre-observational, one
    observed-and-blind, one observed-and-separating, one refinable,
    one mid-supply, one terminal, one supplied tree, and genesis."""
    return (
        ("genesis", GENESIS_P),
        ("pre_observational",
         PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
            prot=((0, 1),), obs=None, budget=2)),
        ("blind_pair", blind_pair()),
        ("separated_pair",
         PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
            prot=((0, 1),), obs=((0,),), budget=2)),
        ("refinable", refinable()),
        ("supply_stages", supply_stages()),
        ("path3", tree_at(path_pol, 2)),
        ("terminal",
         PS(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),),
            prot=((0, 1),), obs=(), budget=2, halted=True)),
    )


def declared_columns(s: PS) -> tuple[Col, ...]:
    """The declared column universe of the battery: the empty
    column, every singleton and every ascending pair over the
    carrier, plus every column already declared in the state."""
    n = len(s.occ)
    base: list[Col] = [()]
    base += [(i,) for i in range(n)]
    base += [(i, j) for i in range(n) for j in range(i + 1, n)]
    extra: list[Col] = [] if s.obs is None else list(s.obs)
    return tuple(dict.fromkeys(base + extra))


def event_battery(s: PS, probe: int = 1) -> list[PEvent]:
    """Every event kind at every argument within the declared bound:
    positions and tokens up to ``probe`` past the carrier, and every
    column of the declared column universe."""
    n = len(s.occ)
    pos = range(n + probe)
    cols = declared_columns(s)
    out: list[PEvent] = []
    out += [("admitOcc", t) for t in range(n + probe + 1)]
    out += [("assertWit", i, j) for i in pos for j in pos]
    out += [("admitWit", i, j) for i in pos for j in pos]
    out += [("protect", i, j) for i in pos for j in pos]
    out += [("declareObs",)]
    out += [("refineCol", v, p) for v in cols for p in pos]
    out += [("addCol", c) for c in cols]
    out += [("refuse", i, j) for i in pos for j in pos]
    out += [("setBudget", b) for b in (0, 1, 2)]
    out += [("setLicense", b) for b in (False, True)]
    out += [("halt",)]
    return out


def changed_fields(s: PS, t: PS) -> tuple[str, ...]:
    return tuple(f for f in STATE_FIELDS
                 if getattr(s, f) != getattr(t, f))


def graph_stores_fixed(s: PS, t: PS) -> bool:
    """Lean ``GraphStoresFixed``: the four graph stores agree."""
    return all(getattr(s, f) == getattr(t, f) for f in GRAPH_FIELDS)


def field_invariance_report(probe: int = 1) -> dict[str, Json]:
    """The exhaustive battery: which fields each event kind moves."""
    touched: dict[str, set[str]] = {k: set() for k in ALL_KINDS}
    refine_ok_rows: list[bool] = []
    addcol_rows: list[bool] = []
    internal_rows: list[bool] = []
    response_rows: list[bool] = []
    supply_only_rows: list[bool] = []
    per_state: dict[str, Json] = {}
    total = 0
    for name, s in sample_states():
        battery = event_battery(s, probe)
        per_state[name] = len(battery)
        for e in battery:
            total += 1
            ch = changed_fields(s, pstep(s, e))
            touched[kind(e)].update(ch)
            moved_graph = [f for f in ch if f in GRAPH_FIELDS]
            supply_only_rows.append(
                moved_graph == [] or kind(e) in SUPPLY_KINDS)
            outside_obs = [f for f in ch if f not in OBSERVATION_FIELDS]
            refine_ok_rows.append(
                outside_obs == [] or kind(e) != "refineCol")
            addcol_rows.append(
                outside_obs == [] or kind(e) != "addCol")
            internal_rows.append(
                moved_graph == [] or not is_internal(e))
            response_rows.append(
                moved_graph == [] or not is_response_event(e))
    return {
        "probe_past_carrier": probe,
        "total_checks": total,
        "events_per_state": per_state,
        "fields_touched_by_kind": {
            k: sorted(touched[k]) for k in sorted(touched)},
        "refineCol_only_obs": all(refine_ok_rows),
        "addCol_only_obs": all(addcol_rows),
        "internal_events_fix_graph_stores": all(internal_rows),
        "response_events_fix_graph_stores": all(response_rows),
        "graph_fields_move_only_under_supply": all(supply_only_rows),
        "every_supply_kind_moves_a_graph_store": all(
            touched[k] != set() for k in SUPPLY_KINDS),
        "supply_kinds": list(SUPPLY_KINDS),
        "internal_kinds": list(INTERNAL_KINDS),
        "control_kinds": list(CONTROL_KINDS),
    }


# ---------------------------------------------------------------------------
# The internal fragment cannot grow the carrier

def internal_alphabet(s: PS, probe: int = 1) -> list[PEvent]:
    return [e for e in event_battery(s, probe) if is_internal(e)]


def internal_fragment_report(max_len: int,
                             probe: int = 1) -> dict[str, Json]:
    """Every internal trace up to the declared length, on every
    declared sample state: the four graph stores never move."""
    rows: list[Json] = []
    fixed_rows: list[bool] = []
    total = 0
    for name, s in sample_states():
        alphabet = internal_alphabet(s, probe)
        count = 0
        for length in range(max_len + 1):
            for trace in product(alphabet, repeat=length):
                count += 1
                fixed_rows.append(
                    graph_stores_fixed(s, preplay(list(trace), s)))
        total += count
        rows.append({"state": name, "alphabet": len(alphabet),
                     "traces": count})
    return {
        "max_trace_length": max_len,
        "traces_checked": total,
        "per_state": rows,
        "all_graph_stores_fixed": all(fixed_rows),
    }


def mentions_only_existing(s: PS, e: PEvent) -> bool:
    """Lean ``MentionsOnlyExisting``: the point a refinement adds and
    every point of a created column is already represented."""
    if kind(e) == "refineCol":
        return int_arg(e, 2) < len(s.occ)
    if kind(e) == "addCol":
        return all(x < len(s.occ) for x in col_arg(e, 1))
    return True


def block_shape(b: tuple[PEvent, ...]) -> str:
    """Lean ``nextFamilyP_block_shape``: a single same-level repair,
    or a funding event followed by one created column.  There is no
    third shape."""
    if len(b) == 1 and kind(b[0]) == "refineCol":
        return "repair"
    if (len(b) == 2 and kind(b[0]) == "setBudget"
            and kind(b[1]) == "addCol"):
        return "funded_extension"
    return "other"


def family_report() -> dict[str, Json]:
    """The represented next-event family at every sample state: its
    block shapes, its range over the existing carrier, and its
    graph-store invariance."""
    shapes: dict[str, int] = {"repair": 0, "funded_extension": 0,
                              "other": 0}
    range_rows: list[bool] = []
    fixed_rows: list[bool] = []
    response_rows: list[bool] = []
    per_state: dict[str, Json] = {}
    for name, s in sample_states():
        family = next_family_p(s)
        per_state[name] = [block_json(b) for b in family]
        for b in family:
            shapes[block_shape(b)] += 1
            fixed_rows.append(graph_stores_fixed(s, preplay(b, s)))
            for e in b:
                range_rows.append(mentions_only_existing(s, e))
                response_rows.append(is_response_event(e))
    return {
        "families": per_state,
        "block_shapes": {k: shapes[k] for k in sorted(shapes)},
        "every_block_has_a_declared_shape": shapes["other"] == 0,
        "family_ranges_over_existing_carrier": all(range_rows),
        "family_blocks_are_response_events": all(response_rows),
        "family_blocks_fix_graph_stores": all(fixed_rows),
    }


# ---------------------------------------------------------------------------
# The proposal record: one explicit sufficient represented schema

AUTHORITY_WORDS: tuple[str, ...] = (
    "licen", "execut", "activ", "authorit", "budget", "gate")


@dataclass(frozen=True)
class ProposalRecord:
    """A represented growth proposal (Lean ``ProposalRecord``).

    Fields, and nothing else: one named block (proved to be a member of
    the complete Up family, but not canonical or unique), the
    old-position embedding and its retraction, the new
    pair with its provenance (parent position, fresh position), and
    the declared cost.  There is no license field, no execution
    field, and no activation field: the record is a PROPOSAL and
    carries no authority to execute.
    """

    block: tuple[PEvent, ...]
    embed: tuple[int, ...]
    retract: tuple[int, ...]
    new_pair: Pair
    parent_pos: int
    fresh_pos: int
    cost: int


def record_field_names() -> tuple[str, ...]:
    return tuple(f.name for f in dataclass_fields(ProposalRecord))


def carries_no_authority() -> bool:
    """No field of the record names a license, an execution, an
    activation, a budget, or a gate."""
    return not any(word in name
                   for name in record_field_names()
                   for word in AUTHORITY_WORDS)


def up_proposal(s: PS, p: int) -> ProposalRecord:
    """The parent-indexed proposal at a represented position, with
    the identity embedding: the declared one-edge grammar keeps every
    old position where it was.  Cost is the declared block length."""
    n = len(s.occ)
    block = tuple(up_block(s, p))
    return ProposalRecord(block=block, embed=tuple(range(n)),
                          retract=tuple(range(n + 1)),
                          new_pair=(p, n), parent_pos=p, fresh_pos=n,
                          cost=len(block))


def separated_pairs(cols: Optional[Cols], n: int) -> set[Pair]:
    """Every ordered pair of represented positions the declared
    observation separates (empty when nothing is declared)."""
    if cols is None:
        return set()
    return {(i, j) for i in range(n) for j in range(n)
            if sep_p(cols, i, j)}


OBLIGATION_KEYS: tuple[str, ...] = (
    "block_complete", "retract_embed_identity", "token_fresh",
    "preserves_asserted", "preserves_wit", "preserves_prot",
    "preserves_separated", "new_pair_provenance",
    "parent_represented", "fresh_position_is_next",
    "carries_no_authority_field")


def proposal_obligations(s: PS, rec: ProposalRecord) -> dict[str, Json]:
    """Every obligation of the record, as a computable check."""
    t = preplay(list(rec.block), s)
    n = len(s.occ)
    emb = rec.embed
    tokens = [int_arg(e, 1) for e in rec.block
              if kind(e) == "admitOcc"]
    old_sep = separated_pairs(s.obs, n)
    new_sep = separated_pairs(t.obs, len(t.occ))
    return {
        "block_complete": list(rec.block) in up_family(s),
        "complete_family_retained_alongside_named_branch":
            len(up_family(s)) == n and list(rec.block) in up_family(s),
        "retract_embed_identity": all(rec.retract[emb[x]] == x
                                      for x in range(n)),
        "token_fresh": all(tok not in s.occ for tok in tokens),
        "preserves_asserted": all((emb[a], emb[b]) in t.asserted
                                  for (a, b) in s.asserted),
        "preserves_wit": all((emb[a], emb[b]) in t.wit
                             for (a, b) in s.wit),
        "preserves_prot": all((emb[a], emb[b]) in t.prot
                              for (a, b) in s.prot),
        "preserves_separated": all((emb[i], emb[j]) in new_sep
                                   for (i, j) in old_sep),
        "new_pair_provenance":
            rec.new_pair == (rec.parent_pos, rec.fresh_pos),
        "parent_represented": rec.parent_pos < n,
        "fresh_position_is_next": rec.fresh_pos == n,
        "carries_no_authority_field": carries_no_authority(),
        "cost": rec.cost,
        "separated_pairs_before": len(old_sep),
        "separated_pairs_after": len(new_sep),
    }


def proposal_report() -> dict[str, Json]:
    """Proposal obligations at every declared sample state with a
    represented parent, plus the no-authority checks."""
    per_state: dict[str, Json] = {}
    all_rows: list[bool] = []
    inert_rows: list[bool] = []
    for name, s in sample_states():
        rows: list[Json] = []
        for p in range(len(s.occ)):
            rec = up_proposal(s, p)
            obligations = proposal_obligations(s, rec)
            rows.append(obligations)
            for key in OBLIGATION_KEYS:
                all_rows.append(obligations[key] is True)
            inert_rows.append(
                (preplay(list(rec.block), s) == s) == s.halted)
        per_state[name] = rows
    return {
        "record_fields": list(record_field_names()),
        "carries_no_authority_field": carries_no_authority(),
        "obligation_keys": list(OBLIGATION_KEYS),
        "all_obligations_discharged": all(all_rows),
        "execution_is_separately_gated": all(inert_rows),
        "per_state": per_state,
    }


# ---------------------------------------------------------------------------
# Transport over the FULL permutation group, and the retained tie

def transport_report(carrier: int = 3) -> dict[str, Json]:
    """The proposal family transports under the renaming action,
    checked over the FULL permutation group on the declared
    carrier."""
    s = tree_at(path_pol, carrier - 1)
    n = len(s.occ)
    perms = list(permutations(range(n)))
    comm: list[bool] = []
    member: list[bool] = []
    equal_cost: list[bool] = []
    obligations: list[bool] = []
    for perm in perms:
        moved = act(perm, s)
        for p in range(n):
            here = up_proposal(s, p)
            there = up_proposal(moved, perm[p])
            comm.append(
                act(perm, preplay(list(here.block), s))
                == preplay(list(there.block), moved))
            member.append(list(there.block) in up_family(moved))
            equal_cost.append(here.cost == there.cost)
            checks = proposal_obligations(moved, there)
            for key in OBLIGATION_KEYS:
                obligations.append(checks[key] is True)
    return {
        "carrier": n,
        "permutation_group_size": len(perms),
        "checks": len(comm),
        "act_up_comm_all_perms": all(comm),
        "transported_block_is_complete_member": all(member),
        "cost_invariant_under_renaming": all(equal_cost),
        "transported_obligations_discharged": all(obligations),
    }


def tie_report() -> dict[str, Json]:
    """Two equal-cost proposals whose executions are
    non-isomorphic: the family retains both and certifies neither as
    canonical."""
    s = tree_at(path_pol, 2)
    first = up_proposal(s, 1)
    second = up_proposal(s, 2)
    left = preplay(list(first.block), s)
    right = preplay(list(second.block), s)
    return {
        "carrier": len(s.occ),
        "iso_carrier": len(left.occ),
        "cost": first.cost,
        "equal_cost": first.cost == second.cost,
        "blocks_differ": first.block != second.block,
        "both_complete_members": (list(first.block) in up_family(s)
                                  and list(second.block)
                                  in up_family(s)),
        "executions_non_isomorphic":
            not isomorphic_undirected(left.wit, right.wit,
                                      len(left.occ)),
        "family_size_equals_parent_count":
            len(up_family(s)) == len(s.occ),
        "left_edges": [list(e) for e in left.wit],
        "right_edges": [list(e) for e in right.wit],
    }


# ---------------------------------------------------------------------------
# Part 3: does nextFamilyP request the lift at an obstruction?

def in_carrier_resolution(s: PS, i: int, j: int) -> dict[str, Json]:
    """The general in-carrier resolution (Lean
    ``obstruction_resolved_in_carrier``): under the Lean theorem's
    hypotheses — obstructed, distinct, represented, protected,
    licensed, live — the funded column block on the first endpoint is
    in the complete family, removes the obstruction, and changes no
    graph store."""
    hypotheses = (obst_p(s, i, j) and i != j and i < len(s.occ)
                  and (i, j) in s.prot and s.licensed
                  and not s.halted)
    block: tuple[PEvent, ...] = (("setBudget", 1), ("addCol", (i,)))
    t = preplay(block, s)
    resolved = (not obst_p(t, i, j)) and graph_stores_fixed(s, t) \
        and len(t.occ) == len(s.occ)
    return {
        "pair": [i, j],
        "hypotheses_hold": hypotheses,
        "obstructed_before": obst_p(s, i, j),
        "block_in_family": list(block) in [list(b)
                                           for b in next_family_p(s)],
        "obstructed_after": obst_p(t, i, j),
        "graph_stores_fixed": graph_stores_fixed(s, t),
        "carrier_before": len(s.occ),
        "carrier_after": len(t.occ),
        "resolved_in_carrier": resolved,
    }


def part3_report() -> dict[str, Json]:
    """Witness that growth is not entailed by ``nextFamilyP``."""
    s = blind_pair()
    cols = cast(Cols, s.obs)
    family = next_family_p(s)
    resolved = [not obst_p(preplay(b, s), 0, 1) for b in family]
    fixed = [graph_stores_fixed(s, preplay(b, s)) for b in family]
    grows: list[bool] = []
    general: list[Json] = []
    resolutions: list[bool] = []
    live_checks = 0
    for name, t in sample_states():
        for b in next_family_p(t):
            grows.append(len(preplay(b, t).occ) > len(t.occ))
        for (i, j) in obstructed_pairs(t):
            row = in_carrier_resolution(t, i, j)
            general.append({"state": name, **row})
            holds = row["hypotheses_hold"] is True
            live_checks += int(holds)
            resolutions.append(
                (not holds) or row["resolved_in_carrier"] is True)
    return {
        "witness_state": {
            "occ": list(s.occ),
            "wit": [list(p) for p in s.wit],
            "prot": [list(p) for p in s.prot],
            "obs": [list(c) for c in cols],
        },
        "four_conditions": {
            "retained": (0, 1) in s.wit,
            "protected": (0, 1) in s.prot,
            "observation_declared": s.obs is not None,
            "observer_zero_on_the_pair": not sep_p(cols, 0, 1),
            "all_four": obst_p(s, 0, 1),
        },
        "complete_family": [block_json(b) for b in family],
        "family_nonempty": len(family) > 0,
        "every_response_resolves": all(resolved),
        "every_response_fixes_graph_stores": all(fixed),
        "no_response_grows_the_carrier": not any(grows),
        "responses_checked_for_growth": len(grows),
        "general_in_carrier_resolutions": general,
        "obstructions_meeting_the_hypotheses": live_checks,
        "every_obstruction_resolved_in_carrier": all(resolutions),
        "verdict": (
            "not entailed by nextFamilyP: the four obstruction "
            "conditions are "
            "satisfiable at states whose complete internal response "
            "family is nonempty and resolves the obstruction with no "
            "carrier change, and no represented response at any "
            "declared sample state grows the carrier — so the growth "
            "demand is a separately declared premise, not a "
            "consequence of the represented nextFamilyP semantics"),
        "not_claimed": (
            "that no other declared response family could grow the "
            "carrier; only the family the kernel computes from the "
            "represented state is covered"),
    }
