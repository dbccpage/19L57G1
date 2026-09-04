"""Write the deterministic receipt for rung one, the stream as a response.

Usage: python research/second_stream/run_stream.py [--out PATH] [--full PATH]

No timestamp and no environment value reaches the receipt. The frozen texts
are checked against their frozen digests before computation, their captured
digests are carried into the receipt, and they are checked again before
either output write. Every prediction of ``PREDICTIONS.md`` is scored by
``score_predictions``, which is a function of the receipt's own body and
reads nothing else; the verdicts are receipt values rather than prose.

Classification (assumption discipline).  Everything here is metatheory
apparatus.  The sealed kernel and the two sibling trees are consumed
read-only by import; no line of their source is transcribed.  The tree
loop, the declared candidate space at three items, the two members of the
declared validity class, the budgets and the two availability censuses all
live in ``stream.py`` and are called from here.  What this file adds is the
declared cross-check family of bases, the deduplication of situations, the
receipt and the scoring.

Four declarations this file owns, stated so they are not inferred.

* THE CROSS-CHECK FAMILY IS DECLARED HERE.  ``PREDICTIONS.md`` R1-1 speaks
  of "the declared cross-check family"; the family is the eight bases of
  ``cross_check_family`` below, each built by applying sealed deltas to the
  sealed empty regime.  Two of them carry a uniform rule, which is what
  makes R1-1's third clause live rather than empty.  The family is small on
  purpose: the wider construction at three items grows as the cube of a
  universe that itself grows with the datum count, and a base of five data
  would cost more than the whole rectangle.
* WHERE EACH VALIDITY MEMBER IS RUN.  The inherited no-regress member
  governs the twenty runs of the rectangle, the twenty runs of the two-item
  reconstruction, both censuses and the re-derivation of the refusal
  population.  The member this rung declares is run on the deduplicated
  three-item enumeration situations and on the deduplicated refusal
  situations, and nowhere else.  Every recorded row names the member that
  produced it.
* THE WALL BOUND IS A DECLARED TERMINAL, NOT A LICENCE TO CUT A CHECK.  A
  run past ``WALL_BOUND_SECONDS`` stops and records the truncation with its
  bound and with how far it had got; no check is dropped quietly.  When it
  does not fire the receipt carries no reading of a clock, which is the
  usual case and the one the byte-identity claim is about.
* THE SPLIT IS UNCONDITIONAL.  The per-node census rows and the per-run
  edges go to a compressed export whose content hash the summary records,
  in the sibling's shape, whatever the size comes to.  A size-dependent
  split would make the receipt's shape depend on the answer.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import time
from typing import Mapping, Optional, Sequence

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import stream as ST  # noqa: E402  (also puts the sealed kernel on sys.path)

from derivation.candidates import (  # noqa: E402
    Delta,
    Item,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    apply_delta,
    canonical_delta,
    iter_full_deltas,
)
from derivation.engine import Reading  # noqa: E402
from derivation.export import (  # noqa: E402
    Json,
    delta_json,
    dumps_deterministic,
    write_json,
    write_json_gz,
)
from derivation.model import EMPTY, Pair, Regime  # noqa: E402
from two_sided import (  # noqa: E402
    APART,
    COMMITMENTS,
    SAME,
    TEdge,
    TState,
    closure_targets,
    edge_json,
    key_of,
    min_responses,
    sealed_readings,
)

REPO = ST.REPO
RUNG = 1
RUNG_NAME = "the stream as a response"

# The declared wall bound.  Named here, recorded in the receipt, and asked
# between runs and between situations.
WALL_BOUND_SECONDS = 2400.0

# The pinned two-item record this rung replays against: a supplied datum,
# replayed before use and never an authority.
SIBLING_RECEIPT = (
    REPO / "research" / "two_sided_commitment" / "receipts" / "two_sided_commitment.json"
)
SEED = REPO / "research" / "second" / "SEED.md"

# These are independent runtime anchors, not values read from the manifest or
# the receipt being written.  The check runs before the expensive build and
# before either output path is touched, so an unstaged edit cannot be adopted
# into a freshly generated receipt.
FROZEN_DISK_SHA256: tuple[tuple[pathlib.Path, str], ...] = (
    (SEED, "52439e5f75d1c599ce52dc716beb88f1dd7bfc83856ee73ce85f3a7eeec5e70e"),
    (
        HERE / "PROMPT.md",
        "efca5d969189bc2d887bd031f406cbdd9ffc3a2499491e754c1251683fb039a5",
    ),
    (
        HERE / "PREDICTIONS.md",
        "b688840362287aa3101c640bfc063655501e19534a6b84a58b88a5808b663842",
    ),
)

# R1-3 names its own population.  It is measured and checked, not assumed.
NAMED_RUNS_WITH_A_REFUSAL = ("F/parity/mu1", "L/parity/mu1", "L/residue_three/mu1")

# How many exhibits a row keeps when it carries more than a reader can use.
EXHIBIT_LIMIT = 8

FULL_PATH = "receipts/full/second_stream_full.json.gz"

VERDICT_HIT = "HIT"
VERDICT_MISSED = "MISSED"
VERDICT_VACUOUS = "VACUOUS"
VERDICT_PENDING = "PENDING"

RULES_BOTH: tuple[str, str] = (ST.RULE_NO_REGRESS, ST.RULE_STRICT_NO_REGRESS)
INHERITED = f"by_{ST.RULE_NO_REGRESS}"
DECLARED = f"by_{ST.RULE_STRICT_NO_REGRESS}"


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def _sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_frozen_disk() -> dict[pathlib.Path, str]:
    """Refuse a missing or moved frozen input before any receipt is written."""

    checked: dict[pathlib.Path, str] = {}
    for path, wanted in FROZEN_DISK_SHA256:
        try:
            relative = path.relative_to(REPO).as_posix()
        except ValueError:
            relative = path.as_posix()
        if not path.is_file():
            raise ValueError(f"frozen text is missing on disk: {relative}")
        actual = _sha(path)
        if actual != wanted:
            raise ValueError(
                f"frozen text moved on disk: {relative}: expected {wanted}, got {actual}"
            )
        checked[path] = actual
    return checked


def _j(value: object) -> Json:
    if isinstance(value, dict):
        return {str(k): _j(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_j(v) for v in value]
    if isinstance(value, (str, bool, int, float)) or value is None:
        return value
    raise TypeError(f"not JSON: {value!r}")


def _int(value: object) -> int:
    if isinstance(value, bool):
        raise TypeError("a flag is not a count")
    if isinstance(value, int):
        return value
    raise TypeError(f"not an integer: {value!r}")


def _str(value: object) -> str:
    if isinstance(value, str):
        return value
    raise TypeError(f"not a string: {value!r}")


def _bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    raise TypeError(f"not a flag: {value!r}")


def _strs(value: object) -> list[str]:
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"not an array: {value!r}")
    return [_str(v) for v in value]


def _rows(value: object) -> list[Mapping[str, Json]]:
    """A JSON array of objects, read back out of the receipt body."""

    if not isinstance(value, (list, tuple)):
        raise TypeError(f"not an array: {value!r}")
    out: list[Mapping[str, Json]] = []
    for item in value:
        if not isinstance(item, Mapping):
            raise TypeError(f"not an object: {item!r}")
        out.append(item)
    return out


def _sub(value: object) -> Mapping[str, Json]:
    if not isinstance(value, Mapping):
        raise TypeError(f"not an object: {value!r}")
    return value


def _pair_of(raw: object) -> Pair:
    if not isinstance(raw, (list, tuple)) or len(raw) != 2:
        raise TypeError(f"not a pair: {raw!r}")
    return (_int(raw[0]), _int(raw[1]))


def _tally(names: Sequence[str]) -> dict[str, Json]:
    out: dict[str, int] = {}
    for name in names:
        out[name] = out.get(name, 0) + 1
    return {k: v for k, v in sorted(out.items())}


class Deadline:
    """The declared wall bound, as an object the loops can ask."""

    def __init__(self, seconds: float) -> None:
        self.seconds = seconds
        self.start = time.perf_counter()
        self.fired = False
        self.where = ""
        self.reached = 0

    def elapsed(self) -> float:
        return time.perf_counter() - self.start

    def check(self, where: str, reached: int) -> bool:
        """True when the bound has been passed.  Records the first firing."""

        if self.elapsed() <= self.seconds:
            return False
        if not self.fired:
            self.fired = True
            self.where = where
            self.reached = reached
        return True

    def as_json(self) -> dict[str, Json]:
        row: dict[str, Json] = {
            "declared_bound_seconds": self.seconds,
            "truncated": self.fired,
        }
        if self.fired:
            row["truncation_kind"] = "terminal_wall_bound"
            row["where"] = self.where
            row["units_reached_before_truncation"] = self.reached
        return row


# ---------------------------------------------------------------------------
# The declared cross-check family
# ---------------------------------------------------------------------------


def _base(steps: Sequence[tuple[Item, ...]]) -> Regime:
    r = EMPTY
    for step in steps:
        r = apply_delta(r, canonical_delta(step))
    return r


def cross_check_family() -> list[tuple[str, Regime]]:
    """The declared family of bases R1-1 is scored over.

    Built by applying sealed deltas to the sealed empty regime, so no
    grammar is introduced here.  The family covers: no datum and no form;
    data without a form; a unary form and a binary form; a form carrying an
    instance; and two bases carrying a uniform rule, which is what keeps
    R1-1's third clause from being scored over an empty difference on every
    base.  Bases are kept small because the wider construction at three
    items grows with the cube of its own universe.

    The eighth base carries TWO forms of different arity, each with an
    instance.  Every other base of the family tops out at one form, so the
    interleaving of two new-form items with the arities they introduce was
    checked nowhere -- while seven of the nineteen real three-item
    enumerations run on bases carrying two forms.  A reviewer closed that
    gap by hand against a structurally written enumerator and found no
    disagreement; the base is added so the gap is closed by a shipped
    certificate and not by a report of one.
    """

    two: tuple[Item, ...] = (NewDatum(), NewDatum())
    return [
        ("b0_no_datum_no_form", _base([])),
        ("b1_two_data", _base([two])),
        ("b2_unary_form", _base([two, (NewForm(1),)])),
        ("b3_unary_form_ruled", _base([two, (NewForm(1),), (NewRuleAll(0),)])),
        ("b4_binary_form", _base([two, (NewForm(2),)])),
        (
            "b5_binary_form_with_instance",
            _base([two, (NewForm(2),), (NewInst(0, (0, 1)),)]),
        ),
        (
            "b6_binary_ruled_three_data",
            _base([two, (NewForm(2),), (NewRuleAll(0), NewDatum())]),
        ),
        (
            "b7_two_forms_with_instances",
            _base(
                [
                    two,
                    (NewForm(1),),
                    (NewForm(2),),
                    (NewInst(0, (0,)), NewInst(1, (0, 1))),
                ]
            ),
        ),
    ]


def cross_check_table() -> dict[str, Json]:
    """R1-1's three clauses, measured on every base of the declared family.

    Clause (a) compares the rung's item-count-parametric generator with the
    sealed unpruned one at zero, one and two items, where the generator
    delegates: a regression guard on that delegation.  Clause (b) compares
    it with the independently written wider construction at zero, two and
    three items.  Clause (c) records the one-item difference and whether it
    is exactly the closed form the frozen text names.
    """

    rows: list[Json] = []
    agree_sealed = True
    agree_wide = True
    closed_form_everywhere = True
    non_empty_somewhere = False
    for name, base in cross_check_family():
        sealed_rows: list[Json] = []
        for cost in (0, 1, 2):
            mine = set(ST.iter_k_item_deltas(base, cost, ST.BOUNDS_THREE))
            sealed = set(iter_full_deltas(base, cost, ST.BOUNDS_THREE))
            ok = mine == sealed
            agree_sealed = agree_sealed and ok
            sealed_rows.append(
                {
                    "item_count": cost,
                    "declared": len(mine),
                    "sealed": len(sealed),
                    "only_declared": len(mine - sealed),
                    "only_sealed": len(sealed - mine),
                    "agree": ok,
                }
            )
        wide_rows: list[Json] = []
        for cost in (0, 2, 3):
            mine = set(ST.iter_k_item_deltas(base, cost, ST.BOUNDS_THREE))
            wide = set(ST.iter_superset_deltas(base, cost, ST.BOUNDS_THREE))
            ok = mine == wide
            agree_wide = agree_wide and ok
            wide_rows.append(
                {
                    "item_count": cost,
                    "declared": len(mine),
                    "wider": len(wide),
                    "only_declared": len(mine - wide),
                    "only_wider": len(wide - mine),
                    "agree": ok,
                }
            )
        mine1 = set(ST.iter_k_item_deltas(base, 1, ST.BOUNDS_THREE))
        wide1 = set(ST.iter_superset_deltas(base, 1, ST.BOUNDS_THREE))
        difference = wide1 - mine1
        ruled = sorted(int(f) for f in base.rules)
        expected: set[Delta] = {canonical_delta((NewRuleAll(f),)) for f in ruled}
        matches = difference == expected
        closed_form_everywhere = closed_form_everywhere and matches
        non_empty_somewhere = non_empty_somewhere or bool(difference)
        rows.append(
            {
                "base": name,
                "data": base.n_data(),
                "forms": list(base.forms),
                "rules": ruled,
                "instances": len(base.insts),
                "versus_sealed": sealed_rows,
                "versus_wider": wide_rows,
                "one_item_declared": len(mine1),
                "one_item_wider": len(wide1),
                "one_item_difference_size": len(difference),
                "one_item_difference_is_the_ruled_forms": matches,
            }
        )
    return {
        "family_size": len(rows),
        "bases": rows,
        "agrees_with_sealed_at_zero_one_two": agree_sealed,
        "agrees_with_wider_at_zero_two_three": agree_wide,
        "one_item_difference_is_closed_form_on_every_base": closed_form_everywhere,
        "one_item_difference_non_empty_on_some_base": non_empty_somewhere,
    }


# ---------------------------------------------------------------------------
# The pinned two-item record, and the reconstruction against it
# ---------------------------------------------------------------------------


def pinned_trees() -> dict[str, Mapping[str, Json]]:
    """The committed sibling summary receipt, indexed by tree identity."""

    payload = json.loads(SIBLING_RECEIPT.read_text(encoding="utf-8"))
    return {_str(row["id"]): row for row in _rows(payload["trees"])}


def _refusal_rows(tree: ST.STree) -> list[Json]:
    return [_j(dict(rec)) for rec in tree.tree.refusals]


def two_item_reconstruction(deadline: Deadline) -> dict[str, Json]:
    """R1-2: the rung's own loop at the sibling's item bound, against the
    pinned record, and the rung's selection against the public sibling
    selection at every state and target of those runs."""

    pinned = pinned_trees()
    rows: list[Json] = []
    stats_agree = True
    selection_agree = True
    comparisons = 0
    built = 0
    mismatches: list[Json] = []
    for reading in sealed_readings():
        for commitment in COMMITMENTS:
            for measure in ST.MEASURES:
                if deadline.check("two_item_reconstruction", built):
                    break
                tree = ST.build_stream_tree(
                    reading,
                    commitment,
                    measure,
                    ST.BOUNDS_TWO,
                    ST.RULE_NO_REGRESS,
                    census=False,
                )
                built += 1
                stats = tree.stats()
                want = pinned[tree.ident]
                want_stats = _sub(want["stats"])
                mine_refusals = _refusal_rows(tree)
                same_nodes = _int(stats["nodes"]) == _int(want_stats["nodes"])
                same_edges = _int(stats["edges"]) == _int(want_stats["edges"])
                same_status = _j(stats["by_status"]) == _j(want_stats["by_status"])
                same_refusals = mine_refusals == _j(want["refusals"])
                ok = same_nodes and same_edges and same_status and same_refusals
                stats_agree = stats_agree and ok
                bad_here = 0
                for node in tree.tree.nodes:
                    for target in closure_targets(node.state):
                        mine = ST.min_responses_three(
                            node.state,
                            target,
                            measure,
                            ST.BOUNDS_TWO,
                            ST.RULE_NO_REGRESS,
                        )
                        theirs = min_responses(node.state, target, measure, ST.BOUNDS_TWO)
                        comparisons += 1
                        if (mine is None) != (theirs is None):
                            bad_here += 1
                        elif (
                            mine is not None
                            and theirs is not None
                            and (mine.deltas != theirs.deltas or mine.cost != theirs.cost)
                        ):
                            bad_here += 1
                        else:
                            continue
                        if len(mismatches) < EXHIBIT_LIMIT:
                            mismatches.append(
                                {
                                    "tree": tree.ident,
                                    "node": node.node_id,
                                    "kind": target[0],
                                    "target": list(target[1]),
                                }
                            )
                selection_agree = selection_agree and bad_here == 0
                rows.append(
                    {
                        "id": tree.ident,
                        "nodes": _int(stats["nodes"]),
                        "pinned_nodes": want_stats["nodes"],
                        "edges": _int(stats["edges"]),
                        "pinned_edges": want_stats["edges"],
                        "by_status": _j(stats["by_status"]),
                        "pinned_by_status": _j(want_stats["by_status"]),
                        "refusal_count": len(mine_refusals),
                        "pinned_refusal_count": len(_rows(want["refusals"])),
                        "nodes_agree": same_nodes,
                        "edges_agree": same_edges,
                        "by_status_agree": same_status,
                        "refusals_agree": same_refusals,
                        "selection_mismatches": bad_here,
                    }
                )
    return {
        "validity_rule": ST.RULE_NO_REGRESS,
        "item_bound": ST.BOUNDS_TWO.max_items,
        "trees_built": built,
        "trees_pinned": len(pinned),
        "rows": rows,
        "all_four_quantities_agree": stats_agree,
        "selection_agrees_everywhere": selection_agree,
        "selection_comparisons": comparisons,
        "selection_mismatch_exhibits": mismatches,
    }


# ---------------------------------------------------------------------------
# The rectangle: twenty runs at the item bound this rung moves
# ---------------------------------------------------------------------------


def _response_edges(tree: ST.STree) -> list[TEdge]:
    return [e for e in tree.tree.edges if e.challenge != "grow"]


def _min_item_counts(tree: ST.STree) -> dict[tuple[int, str, Pair], int]:
    """The item count of the retained minimum at each answered node and
    demanded pair, read off the edges the run attached."""

    out: dict[tuple[int, str, Pair], int] = {}
    for e in _response_edges(tree):
        key = (e.parent, _str(e.info["kind"]), _pair_of(e.info["target"]))
        value = _int(e.info["item_count"])
        if key not in out or value < out[key]:
            out[key] = value
    return out


def _census_two_block(tree: ST.STree) -> tuple[dict[str, Json], list[Json]]:
    """The two-item availability census of one run, summarized, with the
    rows at which a fresh datum is available while the retained minimum sits
    at a strictly smaller item count kept in full.

    Those rows are the ones R1-9's first clause is about: at them the fresh
    datum is priced out rather than invalid.  A row whose node retained no
    minimum at all -- a node the round bound, the node guard or a terminal
    stopped -- offers no item count to compare against and is counted apart.
    """

    minima = _min_item_counts(tree)
    priced_out: list[Json] = []
    available = 0
    no_retained_minimum = 0
    kinds: list[str] = []
    available_kinds: list[str] = []
    priced_kinds: list[str] = []
    nodes: set[int] = set()
    for row in tree.census_two:
        kind = _str(row["kind"])
        kinds.append(kind)
        if not _bool(row["exists"]):
            continue
        available += 1
        available_kinds.append(kind)
        node = _int(row["node"])
        least = _int(row["least_cost"])
        retained = minima.get((node, kind, _pair_of(row["target"])))
        if retained is None:
            no_retained_minimum += 1
            continue
        if retained >= least:
            continue
        out = dict(row)
        out["retained_minimum_item_count"] = retained
        out["fresh_datum_least_item_count"] = least
        priced_out.append(_j(out))
        priced_kinds.append(kind)
        nodes.add(node)
    summary: dict[str, Json] = {
        "rows": len(tree.census_two),
        "rows_by_kind": _tally(kinds),
        "rows_with_fresh_datum_available": available,
        "rows_with_fresh_datum_available_by_kind": _tally(available_kinds),
        "rows_available_where_no_minimum_was_retained": no_retained_minimum,
        "priced_out_rows": len(priced_out),
        "priced_out_nodes": len(nodes),
        "priced_out_rows_by_kind": _tally(priced_kinds),
    }
    return summary, priced_out


def _census_three_block(tree: ST.STree) -> dict[str, Json]:
    return {
        "rows": len(tree.census_three),
        "rows_with_fresh_datum_available": sum(
            1 for row in tree.census_three if _bool(row["exists"])
        ),
        "valid_fresh_datum_responses": sum(
            _int(row["valid"]) for row in tree.census_three
        ),
        "all_rows": [_j(row) for row in tree.census_three],
    }


def run_json(tree: ST.STree, reading: Reading, commitment_name: str) -> dict[str, Json]:
    stats = tree.stats()
    with_datum = [e for e in _response_edges(tree) if ST.has_fresh_datum(e.response)]
    census_two_summary, priced_out = _census_two_block(tree)
    terminals = sorted(
        {
            _str(row["terminal"])
            for row in tree.truncations
            if _str(row["terminal"]) in ST.BUDGET_TERMINALS
        }
    )
    return {
        "id": tree.ident,
        "reading": reading.name,
        "commitment": commitment_name,
        "measure": tree.tree.measure,
        "validity_rule": ST.RULE_NO_REGRESS,
        "item_bound": ST.BOUNDS_THREE.max_items,
        "stats": _j(stats),
        "response_edges": len(_response_edges(tree)),
        "response_edges_by_item_count": _tally(
            [str(_int(e.info["item_count"])) for e in _response_edges(tree)]
        ),
        "edges_selected_at_three_items": sum(
            1 for e in _response_edges(tree) if _int(e.info["item_count"]) == 3
        ),
        "nodes_stopped_by_the_node_guard": _int(_sub(stats["by_status"]).get("frontier_guard", 0)),
        "growth_edges": _int(stats["growth_edges"]),
        "edges_with_datum_item": len(with_datum),
        "edges_with_datum_item_exhibits": [
            {
                "parent": e.parent,
                "child": e.child,
                "challenge": e.challenge,
                "cost": list(e.cost),
                "response": _j(delta_json(e.response)),
                "info": _j(dict(e.info)),
            }
            for e in with_datum[:EXHIBIT_LIMIT]
        ],
        "refusals": _refusal_rows(tree),
        "refusal_count": len(tree.tree.refusals),
        "truncations": [_j(row) for row in tree.truncations],
        "budget_terminals_fired": terminals,
        "over_growth_data_bound": [_j(row) for row in tree.over_growth_bound],
        "three_item_enumerations": [_j(row) for row in tree.enumerations],
        "counters": _j(tree.counters.as_json()),
        "census_two": census_two_summary,
        "census_two_priced_out_rows": priced_out,
        "census_three": _census_three_block(tree),
        "census_two_all_rows": [_j(row) for row in tree.census_two],
        "edges": [_j(edge_json(e)) for e in tree.tree.edges],
    }


def three_item_runs(deadline: Deadline) -> tuple[list[ST.STree], list[dict[str, Json]]]:
    """The declared rectangle: both sealed readings, the five named stakes,
    both sealed measures, at the item bound this rung moves."""

    trees: list[ST.STree] = []
    rows: list[dict[str, Json]] = []
    for reading in sealed_readings():
        for commitment in COMMITMENTS:
            for measure in ST.MEASURES:
                if deadline.check("three_item_runs", len(trees)):
                    return trees, rows
                tree = ST.build_stream_tree(
                    reading,
                    commitment,
                    measure,
                    ST.BOUNDS_THREE,
                    ST.RULE_NO_REGRESS,
                    census=True,
                    counters=ST.Counters(),
                    memo=ST.EnumerationMemo(),
                )
                trees.append(tree)
                rows.append(run_json(tree, reading, commitment.name))
    return trees, rows


def versus_pinned(rows: Sequence[Mapping[str, Json]]) -> dict[str, Json]:
    """R1-3: the runs whose pinned two-item record carries no refusal, with
    the five quantities the frozen text names, at the item bound this rung
    moves."""

    pinned = pinned_trees()
    without = sorted(ident for ident, row in pinned.items() if not _rows(row["refusals"]))
    with_refusal = sorted(ident for ident in pinned if ident not in without)
    out: list[Json] = []
    agree_all = True
    for row in rows:
        ident = _str(row["id"])
        if ident not in without:
            continue
        want = pinned[ident]
        want_stats = _sub(want["stats"])
        stats = _sub(row["stats"])
        same_status = _j(stats["by_status"]) == _j(want_stats["by_status"])
        checks = (
            _int(stats["nodes"]) == _int(want_stats["nodes"]),
            same_status,
            _int(stats["edges"]) == _int(want_stats["edges"]),
            _int(stats["growth_edges"]) == _int(want_stats["growth_edges"]),
            _int(row["edges_with_datum_item"]) == _int(want["edges_with_fresh_datum"]),
        )
        ok = all(checks)
        agree_all = agree_all and ok
        out.append(
            {
                "id": ident,
                "nodes": stats["nodes"],
                "pinned_nodes": want_stats["nodes"],
                "edges": stats["edges"],
                "pinned_edges": want_stats["edges"],
                "growth_edges": stats["growth_edges"],
                "pinned_growth_edges": want_stats["growth_edges"],
                "edges_with_datum_item": row["edges_with_datum_item"],
                "pinned_edges_with_datum_item": want["edges_with_fresh_datum"],
                "by_status_agree": same_status,
                "agree": ok,
            }
        )
    return {
        "pinned_runs_without_a_refusal": without,
        "pinned_runs_with_a_refusal": with_refusal,
        "population_size": len(without),
        "population_is_the_three_named_complement": tuple(with_refusal)
        == NAMED_RUNS_WITH_A_REFUSAL,
        "rows": out,
        "rows_compared": len(out),
        "all_five_quantities_agree": agree_all and len(out) == len(without),
    }


# ---------------------------------------------------------------------------
# Situations: the refusals re-derived, and the three-item enumerations
# ---------------------------------------------------------------------------


def _shape_ok(delta: Delta) -> bool:
    """R1-6's shape: at least two instance items, or at least one uniform
    rule item."""

    insts = sum(1 for it in delta if isinstance(it, NewInst))
    rules = sum(1 for it in delta if isinstance(it, NewRuleAll))
    return insts >= 2 or rules >= 1


class Gatherer:
    """Every valid response of exactly three items at one state, one
    demanded pair and one validity member, gathered once and remembered.

    The remembering is the declared repeat rule the tree loop uses: two
    calls agreeing on the indexed regime, the commitment, the demanded pair
    and the member are one enumeration.  It is a cache and never a lemma.

    Gathering the whole valid set, rather than reading the tree's retained
    minima, is what R1-5 and R1-6 need: under the second measure a retained
    minimum is a subset of the valid set, so the retained edges do not
    answer a question about every valid response.

    BUDGETS.  Two of the five declared budgets govern one enumeration at one
    demanded pair, and both are enforced here with the terminals A8 names:
    the candidate budget, answered from the projection before the walk
    begins, and the response budget, answered from the gathered set after
    it.  A gather that fires either attaches nothing -- it returns an empty
    valid set and the terminal is recorded -- exactly as the tree loop's
    node does.  The other three do NOT apply: the enumeration budget is
    per RUN and this table is not a run, and the class budget governs
    retention at a node, which this table does not perform.  An earlier
    version enforced none of them here and presented the resulting zero as
    a measured result; the observed maxima are recorded beside the bounds so
    a reader sees the margin rather than only the pass.
    """

    def __init__(self) -> None:
        self._store: dict[tuple[object, str, str, Pair, str], tuple[int, list[Delta]]] = {}
        self.enumerations = 0
        self.repeats = 0
        self.deltas_offered = 0
        self.max_projected_candidates = 0
        self.max_valid_at_one_pair = 0
        self.budget_terminals: list[dict[str, Json]] = []

    def gather(self, s: TState, target: tuple[str, Pair], rule: str) -> tuple[int, list[Delta]]:
        key = (key_of(s)[2], s.commitment, target[0], target[1], rule)
        remembered = self._store.get(key)
        if remembered is not None:
            self.repeats += 1
            return remembered
        projected = ST.candidate_count(s.regime, 3, ST.BOUNDS_THREE)
        self.max_projected_candidates = max(self.max_projected_candidates, projected)
        if projected > ST.MAX_CANDIDATES_PER_ENUMERATION:
            self.budget_terminals.append(
                {
                    "terminal": ST.TERMINAL_CANDIDATE_BUDGET,
                    "where": "situation gatherer",
                    "kind": target[0],
                    "target": list(target[1]),
                    "commitment": s.commitment,
                    "validity_rule": rule,
                    "candidate_multisets_projected": projected,
                    "bound": ST.MAX_CANDIDATES_PER_ENUMERATION,
                }
            )
            self.enumerations += 1
            self._store[key] = (0, [])
            return 0, []
        judge = ST.Judge(s, target, rule)
        offered = 0
        valid: list[Delta] = []
        for delta, after in ST.iter_k_item_deltas_applied(s.regime, 3, ST.BOUNDS_THREE):
            offered += 1
            if ST.has_noop_item(s.regime, delta):
                continue
            if judge.accepts(delta, after):
                valid.append(delta)
                if len(valid) > ST.MAX_VALID_PER_TARGET:
                    self.enumerations += 1
                    self.deltas_offered += offered
                    self.max_valid_at_one_pair = max(
                        self.max_valid_at_one_pair, len(valid)
                    )
                    self.budget_terminals.append(
                        {
                            "terminal": ST.TERMINAL_RESPONSE_BUDGET,
                            "where": "situation gatherer",
                            "kind": target[0],
                            "target": list(target[1]),
                            "commitment": s.commitment,
                            "validity_rule": rule,
                            "valid_gathered": len(valid),
                            "bound": ST.MAX_VALID_PER_TARGET,
                        }
                    )
                    self._store[key] = (offered, [])
                    return offered, []
        self.enumerations += 1
        self.deltas_offered += offered
        self.max_valid_at_one_pair = max(self.max_valid_at_one_pair, len(valid))
        valid.sort(key=ST.delta_order_key)
        self._store[key] = (offered, valid)
        return offered, valid


def _tag_id(tag: ST.SituationTag) -> str:
    return hashlib.sha256(repr(tag).encode("utf-8")).hexdigest()[:16]


def _situation_row(
    tag_id: str,
    group: Sequence[ST.RefusalSituation],
    gatherer: Gatherer,
    rules: Sequence[str],
) -> dict[str, Json]:
    head = group[0]
    row: dict[str, Json] = {
        "situation": tag_id,
        "kind": head.kind,
        "target": list(head.pair),
        "commitment": head.commitment,
        "data": head.state.regime.n_data(),
        "forms": list(head.state.regime.forms),
        "rules": sorted(int(f) for f in head.state.regime.rules),
        "instances": len(head.state.regime.insts),
        "occurrences": len(group),
        "occurrence_nodes": [
            {"tree": s.ident(), "node": s.node, "reading": s.reading, "measure": s.measure}
            for s in group
        ],
    }
    row["candidate_multisets_projected"] = ST.candidate_count(
        head.state.regime, 3, ST.BOUNDS_THREE
    )
    for rule in rules:
        offered, valid = gatherer.gather(head.state, (head.kind, head.pair), rule)
        datum_bearing = [d for d in valid if ST.has_fresh_datum(d)]
        off_shape = [d for d in valid if not _shape_ok(d)]
        row[f"by_{rule}"] = {
            "validity_rule": rule,
            "deltas_offered_at_three_items": offered,
            "valid_three_item_responses": len(valid),
            "answered_at_exactly_three_items": bool(valid),
            "valid_with_datum_item": len(datum_bearing),
            "valid_without_two_instances_and_without_a_rule": len(off_shape),
            "datum_item_exhibits": [_j(delta_json(d)) for d in datum_bearing[:EXHIBIT_LIMIT]],
            "off_shape_exhibits": [_j(delta_json(d)) for d in off_shape[:EXHIBIT_LIMIT]],
        }
    return row


def rectangle_a(gatherer: Gatherer, deadline: Deadline) -> dict[str, Json]:
    """The recorded two-item refusals, re-derived from the pinned sources
    rather than read out of a receipt, deduplicated into situations, and put
    to the three-item space."""

    sits = ST.refusal_states(ST.BOUNDS_TWO, ST.RULE_NO_REGRESS, census=False)
    groups = ST.distinct_situations(sits)
    rows: list[Json] = []
    answered = 0
    for index, (tag, group) in enumerate(groups):
        if deadline.check("rectangle_a", index):
            break
        row = _situation_row(_tag_id(tag), group, gatherer, RULES_BOTH)
        if _bool(_sub(row[INHERITED])["answered_at_exactly_three_items"]):
            answered += 1
        rows.append(row)
    return {
        "validity_rule_of_the_refusal_population": ST.RULE_NO_REGRESS,
        "refusal_records": len(sits),
        "distinct_situations": len(groups),
        "situations_examined": len(rows),
        "situations_answered_at_exactly_three_items": answered,
        "refusal_records_by_kind": _tally([s.kind for s in sits]),
        "by_declared_member": _member_comparison(rows),
        "rows": rows,
    }


def enumeration_situations(
    trees: Sequence[ST.STree], gatherer: Gatherer, deadline: Deadline
) -> dict[str, Json]:
    """Every state and demanded pair at which a three-item enumeration was
    performed in the rectangle, deduplicated, with the whole valid
    three-item set gathered at each."""

    sits: list[ST.RefusalSituation] = []
    for tree in trees:
        for raw in tree.enumerations:
            nid = _int(raw["node"])
            sits.append(
                ST.RefusalSituation(
                    tree.tree.reading,
                    tree.tree.commitment,
                    tree.tree.measure,
                    nid,
                    _str(raw["kind"]),
                    _pair_of(raw["target"]),
                    tree.tree.nodes[nid].state,
                )
            )
    groups = ST.distinct_situations(sits)
    rows: list[Json] = []
    for index, (tag, group) in enumerate(groups):
        if deadline.check("enumeration_situations", index):
            break
        rows.append(_situation_row(_tag_id(tag), group, gatherer, RULES_BOTH))
    same_rows = [r for r in rows if _str(_sub(r)["kind"]) == SAME]

    def total(subset: Sequence[Json], field: str, member: str = INHERITED) -> int:
        return sum(_int(_sub(_sub(r)[member])[field]) for r in subset)

    return {
        "enumeration_records": len(sits),
        "distinct_situations": len(groups),
        "situations_examined": len(rows),
        "situations_by_kind": _tally([_str(_sub(r)["kind"]) for r in rows]),
        "same_kind_situations": len(same_rows),
        "same_kind_valid_three_item_responses": total(same_rows, "valid_three_item_responses"),
        "same_kind_valid_with_datum_item": total(same_rows, "valid_with_datum_item"),
        "same_kind_valid_without_two_instances_and_without_a_rule": total(
            same_rows, "valid_without_two_instances_and_without_a_rule"
        ),
        "by_declared_member": _member_comparison(rows),
        "rows": rows,
    }


# The three counted quantities each member reports at one situation, and the
# one flag.  They are separated because a flag is not a count and the typed
# readers refuse to add one.
COMPARED_COUNTS: tuple[str, ...] = (
    "valid_three_item_responses",
    "valid_with_datum_item",
    "valid_without_two_instances_and_without_a_rule",
)
COMPARED_FLAGS: tuple[str, ...] = ("answered_at_exactly_three_items",)
COMPARED_FIELDS: tuple[str, ...] = COMPARED_COUNTS + COMPARED_FLAGS


def _member_comparison(rows: Sequence[Json]) -> dict[str, Json]:
    """What the DECLARED validity member returned, beside the inherited one.

    Reported because the aggregate otherwise carries the inherited member
    alone, and a member run at thirty-three situations that separated
    nothing at any of them is a finding rather than an absence.  The member
    IS strictly stronger as a predicate -- one exhibited delta is accepted
    by the inherited member and refused by this one -- and that is a
    different statement from the one this block records.
    """

    differing: list[Json] = []
    totals: dict[str, Json] = {}
    for field in COMPARED_COUNTS:
        totals[f"inherited_{field}"] = sum(
            _int(_sub(_sub(r)[INHERITED])[field]) for r in rows
        )
        totals[f"declared_{field}"] = sum(
            _int(_sub(_sub(r)[DECLARED])[field]) for r in rows
        )
    for field in COMPARED_FLAGS:
        totals[f"inherited_{field}"] = sum(
            1 for r in rows if _bool(_sub(_sub(r)[INHERITED])[field])
        )
        totals[f"declared_{field}"] = sum(
            1 for r in rows if _bool(_sub(_sub(r)[DECLARED])[field])
        )
    for row in rows:
        a = _sub(_sub(row)[INHERITED])
        b = _sub(_sub(row)[DECLARED])
        if any(_j(a[f]) != _j(b[f]) for f in COMPARED_FIELDS):
            differing.append(
                {
                    "situation": _sub(row)["situation"],
                    "kind": _sub(row)["kind"],
                    "target": _sub(row)["target"],
                    "inherited": {f: a[f] for f in COMPARED_FIELDS},
                    "declared": {f: b[f] for f in COMPARED_FIELDS},
                }
            )
    return {
        "rows_compared": len(rows),
        "rows_on_which_the_two_members_differ": len(differing),
        "differing_rows": differing,
        "finding": (
            "the declared member is strictly stronger as a predicate and was "
            "exhibited refusing a delta the inherited member accepts; over the "
            "situations at which both were run here it returned the same valid "
            "set at every one"
        ),
        **totals,
    }


# ---------------------------------------------------------------------------
# Aggregates
# ---------------------------------------------------------------------------


def aggregate(rows: Sequence[Mapping[str, Json]]) -> dict[str, Json]:
    counters: dict[str, int] = {}
    terminals: list[str] = []
    priced_kinds: list[str] = []
    priced_rows = 0
    priced_nodes = 0
    by_item_count: dict[str, int] = {}
    guarded: dict[str, int] = {}
    avail_two = 0
    avail_two_kinds: dict[str, int] = {}
    avail_two_no_minimum = 0
    rows_two_by_kind: dict[str, int] = {}
    avail_three = 0
    valid_three = 0
    max_projected = 0
    max_projected_at: dict[str, Json] = {}
    for row in rows:
        for key, value in _sub(row["counters"]).items():
            counters[key] = counters.get(key, 0) + _int(value)
        terminals.extend(_strs(row["budget_terminals_fired"]))
        priced_nodes += _int(_sub(row["census_two"])["priced_out_nodes"])
        for raw in _rows(row["census_two_priced_out_rows"]):
            priced_rows += 1
            priced_kinds.append(_str(raw["kind"]))
        for key, value in _sub(row["response_edges_by_item_count"]).items():
            by_item_count[key] = by_item_count.get(key, 0) + _int(value)
        stopped = _int(row["nodes_stopped_by_the_node_guard"])
        if stopped:
            guarded[_str(row["id"])] = stopped
        census_two = _sub(row["census_two"])
        avail_two += _int(census_two["rows_with_fresh_datum_available"])
        avail_two_no_minimum += _int(
            census_two["rows_available_where_no_minimum_was_retained"]
        )
        for key, value in _sub(census_two["rows_with_fresh_datum_available_by_kind"]).items():
            avail_two_kinds[key] = avail_two_kinds.get(key, 0) + _int(value)
        for key, value in _sub(census_two["rows_by_kind"]).items():
            rows_two_by_kind[key] = rows_two_by_kind.get(key, 0) + _int(value)
        census_three = _sub(row["census_three"])
        avail_three += _int(census_three["rows_with_fresh_datum_available"])
        valid_three += _int(census_three["valid_fresh_datum_responses"])
        for raw in _rows(row["three_item_enumerations"]):
            projected = _int(raw["projected_candidates"])
            if projected > max_projected:
                max_projected = projected
                max_projected_at = {
                    "run": row["id"],
                    "node": raw["node"],
                    "kind": raw["kind"],
                    "target": raw["target"],
                    "data": raw["data"],
                    "forms": raw["forms"],
                }
    nodes = sum(_int(_sub(r["stats"])["nodes"]) for r in rows)
    return {
        "response_edges_by_item_count": {k: by_item_count[k] for k in sorted(by_item_count)},
        "edges_selected_at_three_items": sum(
            _int(r["edges_selected_at_three_items"]) for r in rows
        ),
        "runs_with_a_three_item_selection": {
            _str(r["id"]): _int(r["edges_selected_at_three_items"])
            for r in rows
            if _int(r["edges_selected_at_three_items"]) > 0
        },
        "nodes_stopped_by_the_node_guard": sum(guarded.values()),
        "runs_truncated_by_the_node_guard": {k: guarded[k] for k in sorted(guarded)},
        "census_two_rows_by_kind": {k: rows_two_by_kind[k] for k in sorted(rows_two_by_kind)},
        "census_two_rows_with_fresh_datum_available": avail_two,
        "census_two_rows_with_fresh_datum_available_by_kind": {
            k: avail_two_kinds[k] for k in sorted(avail_two_kinds)
        },
        "census_two_rows_available_where_no_minimum_was_retained": avail_two_no_minimum,
        "census_three_rows_with_fresh_datum_available": avail_three,
        "census_three_valid_fresh_datum_responses": valid_three,
        "max_projected_candidates_in_one_enumeration": max_projected,
        "max_projected_candidates_at": max_projected_at,
        "runs": len(rows),
        "nodes": nodes,
        "node_population": nodes,
        "edges": sum(_int(_sub(r["stats"])["edges"]) for r in rows),
        "response_edges": sum(_int(r["response_edges"]) for r in rows),
        "growth_edges": sum(_int(r["growth_edges"]) for r in rows),
        "edges_with_datum_item": sum(_int(r["edges_with_datum_item"]) for r in rows),
        "refusal_records": sum(_int(r["refusal_count"]) for r in rows),
        "runs_with_a_refusal": sorted(
            _str(r["id"]) for r in rows if _int(r["refusal_count"]) > 0
        ),
        "budget_terminal_truncation_rows": sum(len(_rows(r["truncations"])) for r in rows),
        "truncation_rows_scope": (
            "budget-terminal rows only; the pre-expansion node guard stops a node "
            "without writing one, and is reported by "
            "nodes_stopped_by_the_node_guard and runs_truncated_by_the_node_guard"
        ),
        "budget_terminals_fired": sorted(set(terminals)),
        "counters": {k: v for k, v in sorted(counters.items())},
        "census_two_rows": sum(_int(_sub(r["census_two"])["rows"]) for r in rows),
        "census_three_rows": sum(_int(_sub(r["census_three"])["rows"]) for r in rows),
        "priced_out_rows": priced_rows,
        "priced_out_nodes": priced_nodes,
        "priced_out_rows_by_kind": _tally(priced_kinds),
    }


def availability_block(
    rows: Sequence[Mapping[str, Json]], agg: Mapping[str, Json]
) -> dict[str, Json]:
    """What the two censuses saw, with the companion counters that make a
    zero a counted zero rather than a literal.

    Three counters carry the word "candidate" and they count three different
    populations, so each is named for what it counts rather than left to a
    docstring.  ``candidate_multisets_projected`` is the sum over the tree
    loop's three-item enumerations of one MULTISET over the declared
    universe, counted whether the sealed admission conditions then accept it
    or reject it.  ``deltas_offered`` counts the ADMISSIBLE deltas the same
    loop actually walked.  ``situation_deltas_offered`` in the aggregate
    counts the admissible deltas the situation gatherer walked.  The three
    differ by roughly two orders of magnitude and were once reported under
    one word.
    """

    counters = _sub(agg["counters"])
    iso_rows = [
        raw
        for r in rows
        for raw in _rows(r["truncations"])
        if _str(raw["terminal"]) == ST.TERMINAL_ISO_BUDGET
    ]
    by_kind = _sub(agg["priced_out_rows_by_kind"])
    return {
        "census_two_rows": agg["census_two_rows"],
        "census_two_rows_by_kind": agg["census_two_rows_by_kind"],
        "census_two_rows_with_fresh_datum_available": agg[
            "census_two_rows_with_fresh_datum_available"
        ],
        "census_two_rows_with_fresh_datum_available_by_kind": agg[
            "census_two_rows_with_fresh_datum_available_by_kind"
        ],
        "census_two_rows_available_where_no_minimum_was_retained": agg[
            "census_two_rows_available_where_no_minimum_was_retained"
        ],
        "census_three_rows": agg["census_three_rows"],
        "census_three_rows_with_fresh_datum_available": agg[
            "census_three_rows_with_fresh_datum_available"
        ],
        "census_three_valid_fresh_datum_responses": agg[
            "census_three_valid_fresh_datum_responses"
        ],
        "max_projected_candidates_in_one_enumeration": agg[
            "max_projected_candidates_in_one_enumeration"
        ],
        "max_projected_candidates_at": agg["max_projected_candidates_at"],
        "nodes_censused": counters["nodes_censused"],
        "nodes_visited": counters["nodes_visited"],
        "node_population": agg["node_population"],
        "three_item_enumerations_performed": counters["three_item_enumerations_performed"],
        "enumeration_memo_hits": counters["enumeration_memo_hits"],
        "candidate_multisets_projected": counters["candidate_multisets_projected"],
        "deltas_offered": counters["deltas_offered"],
        "deltas_examined": counters["deltas_examined"],
        "fresh_datum_candidates_generated": counters["fresh_datum_candidates_generated"],
        "fresh_datum_candidates_offered": counters["fresh_datum_candidates_offered"],
        "fresh_datum_candidates_examined": counters["fresh_datum_candidates_examined"],
        "fresh_datum_candidates_judged": counters["fresh_datum_candidates_judged"],
        "fresh_datum_candidates_skipped_as_noop": counters[
            "fresh_datum_candidates_skipped_as_noop"
        ],
        "fresh_datum_candidates_valid": counters["fresh_datum_candidates_valid"],
        "nodes_above_growth_data_bound": counters["nodes_above_growth_data_bound"],
        "priced_out_rows": agg["priced_out_rows"],
        "priced_out_nodes": agg["priced_out_nodes"],
        "priced_out_rows_by_kind": by_kind,
        "priced_out_rows_of_the_same_kind": _int(by_kind[SAME]) if SAME in by_kind else 0,
        "priced_out_rows_of_the_apart_kind": _int(by_kind[APART]) if APART in by_kind else 0,
        "iso_budget_rows": len(iso_rows),
    }


# ---------------------------------------------------------------------------
# The assumptions block
# ---------------------------------------------------------------------------


def assumptions() -> list[Json]:
    """Every scope clause this receipt stands on, named.

    Each entry classifies itself under the assumption discipline and says
    what it does NOT establish.  A receipt is not a proof, and none of these
    entries turns one into a proof.
    """

    return [
        {
            "id": "A1",
            "classification": "admitted primitive",
            "clause": (
                "The candidate space at three items is declared by this rung, not by "
                "the seal. The sealed unpruned generator is declared to two items and "
                "refuses above it. Below three items the rung defers to the sealed "
                "generator and declares nothing, and no sealed pruning lemma is used at "
                "any item count."
            ),
            "not_established": (
                "That the declared space is the space the seal would have declared."
            ),
        },
        {
            "id": "A2",
            "classification": "deterministic computation",
            "clause": (
                "The declared space is checked against an independently written wider "
                "construction at item counts zero, two and three on every base of the "
                "declared cross-check family, and against the sealed generator at zero, "
                "one and two."
            ),
            "not_established": (
                "Anything about bases outside the declared family, which carries at most "
                "three data and at most one form while the rectangle reaches five data "
                "and three forms."
            ),
        },
        {
            "id": "A3",
            "classification": "externally imposed challenge",
            "clause": (
                "Every demanded pair is a target and no orbit is quotiented away. That is "
                "the sibling's shipped rule, which departs from the sibling's own written "
                "question; the departure is inherited deliberately and recorded."
            ),
            "not_established": "That the orbit rule and the shipped rule agree.",
        },
        {
            "id": "A4",
            "classification": "derived definition",
            "clause": (
                "Two states merge only under the sibling's repaired key, which pairs its "
                "state key with the exact indexed regime and the commitment name. "
                "Presentation tokens stay forgotten, and the implemented relation is "
                "cross-checked against a minimum over all bijection pairs inside the "
                "sealed apparatus it calls."
            ),
            "not_established": (
                "That the merge relation is the coarsest one a reader might want."
            ),
        },
        {
            "id": "A5",
            "classification": "derived definition",
            "clause": (
                "Two situations are one situation exactly when the indexed regime "
                "component of the sibling key, the commitment name, the demand kind and "
                "the demanded pair all agree. A refusal record counts a node, not a "
                "situation, and a refusal short-circuits its node."
            ),
            "not_established": (
                "That situations distinct under this relation are distinct problems."
            ),
        },
        {
            "id": "A6",
            "classification": "declared scope",
            "clause": (
                "The inherited no-regress member governs the twenty runs of the "
                "rectangle, the twenty runs of the two-item reconstruction, both "
                "censuses and the re-derivation of the refusal population. The member "
                "this rung declares is run on the deduplicated three-item enumeration "
                "situations and on the deduplicated refusal situations, and nowhere "
                "else. Every row names the member that produced it."
            ),
            "not_established": (
                "Any statement about the declared member at a state where it was not run."
            ),
        },
        {
            "id": "A7",
            "classification": "declared scope",
            "clause": (
                "The rectangle is both sealed genesis readings, the five named stakes of "
                "the sibling tree, both sealed cost measures, responses of at most three "
                "items with form arity at most two, at most fifteen accepted rounds and a "
                "pre-expansion node guard of two hundred and fifty. The growth data bound "
                "of five governs growth alone and does not bind a response; a run that "
                "passes it is recorded with the count it reaches."
            ),
            "not_established": "Anything at four items or at arity three.",
        },
        {
            "id": "A8",
            "classification": "declared scope",
            "clause": (
                "Five budgets, each with its own terminal naming the tree, the node and "
                "the demanded pair: at most forty enumerations at three items in one run, "
                "at most one million candidates examined in one enumeration, at most two "
                "thousand valid responses gathered at one demanded pair, at most two "
                "hundred retained classes at one node, and the bijection budget the "
                "sibling raises inside its own key. A node whose gathering is cut short "
                "attaches nothing. The enumeration budget is per RUN and the class budget "
                "governs retention at a node, so both govern the tree loop alone; the "
                "candidate and response budgets govern one enumeration at one demanded "
                "pair and are enforced in the tree loop AND in the situation gatherer, "
                "which is not a run. An earlier version enforced none of the five in the "
                "gatherer while presenting its zero as measured; the observed maxima are "
                "recorded beside the bounds."
            ),
            "not_established": (
                "That a budget which did not fire here could not fire at a wider bound."
            ),
        },
        {
            "id": "A9",
            "classification": "metatheory apparatus",
            "clause": (
                "A repeated enumeration is answered from the record of the one before it "
                "whenever the indexed state, the commitment, the demanded pair and the "
                "validity member agree exactly: within one run for the tree loop, and "
                "across the situation tables for the gatherer. It is a cache and never a "
                "lemma, and both hit counts are recorded."
            ),
            "not_established": "That two situations with different tags differ in answer.",
        },
        {
            "id": "A10",
            "classification": "metatheory apparatus",
            "clause": (
                "The wall bound of the run is a declared terminal. When it does not fire "
                "the receipt carries no reading of a clock and no environment value; when "
                "it fires the receipt says so, names where, and is not byte-reproducible. "
                "It is deliberately larger than any caller's time budget and protects no "
                "such budget: it exists so that a run which stops early stops NAMED, and "
                "a caller who wants a smaller ceiling passes one on the command line and "
                "accepts a receipt that is not byte-reproducible."
            ),
            "not_established": (
                "That the bound is generous enough at a wider rectangle, or that a run "
                "finishing inside it finishes inside any other time budget."
            ),
        },
        {
            "id": "A11",
            "classification": "supplied object-language datum",
            "clause": (
                "The committed sibling summary receipt is read as the pinned two-item "
                "record. It is replayed by this rung's own loop before any comparison is "
                "made and is never cited as authority."
            ),
            "not_established": "That the sibling receipt is itself correct.",
        },
        {
            "id": "A12",
            "classification": "declared scope",
            "clause": (
                "Availability is recorded twice: at every node reached, within a bound of "
                "two items, independently of the item count at which the minimum was "
                "found; and at every state where a three-item enumeration is performed, "
                "within a bound of three items. Each census carries the count of nodes it "
                "visited and the count of candidates it examined, so a zero is a counted "
                "zero."
            ),
            "not_established": (
                "Availability at a node whose run retained no minimum to price it "
                "against; those rows are counted apart and are outside the priced-out "
                "population. The census SPACE is this rung's own declaration at every "
                "item count, not the sealed generator: the frozen deferral clause governs "
                "the candidate space of the selection, and the datum-bearing construction "
                "builds directly from the declared universe at one and two items as well "
                "as at three. It is certified equal, as a set, to the deferring "
                "generator's datum-bearing subset at costs one to three on every base of "
                "the declared cross-check family, and nowhere else."
            ),
        },
        {
            "id": "A13",
            "classification": "declared scope",
            "clause": (
                "Scoring is a function of this receipt's own body and reads nothing else. "
                "A prediction whose population turns out empty is scored VACUOUS and is "
                "evidence of nothing; the verdict is never rounded up. The extrapolation "
                "is scored PENDING because it speaks of a rectangle this rung does not "
                "compute."
            ),
            "not_established": (
                "That a HIT is evidence for the mechanism a prediction offers beside it."
            ),
        },
    ]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def _verdict(hit: bool) -> str:
    return VERDICT_HIT if hit else VERDICT_MISSED


def score_predictions(body: Mapping[str, Json]) -> tuple[dict[str, Json], dict[str, Json]]:
    """Score every prediction of ``PREDICTIONS.md`` from the receipt body.

    A function of its argument alone: it opens no file, builds no tree and
    reads no clock, so a test can hand it a body and check a verdict, and a
    reader can recompute a verdict from the committed receipt.  Verdicts are
    HIT, MISSED, VACUOUS or PENDING; an empty population scores VACUOUS and
    is never rounded up, as the frozen text requires for R1-6 and as the
    frozen scoring note applies to the rest.
    """

    cross = _sub(body["cross_check"])
    recon = _sub(body["two_item_reconstruction"])
    pinned = _sub(body["three_item_versus_pinned"])
    agg = _sub(body["aggregate"])
    rect = _sub(body["rectangle_a"])
    enum = _sub(body["enumeration_situations"])
    avail = _sub(body["availability"])
    serial = _sub(body["serialization"])
    wall = _sub(body["wall_clock_truncation"])
    runs = _rows(body["runs"])

    scored: dict[str, Json] = {}
    detail: dict[str, Json] = {}

    def record(name: str, verdict: str, observed: Mapping[str, Json]) -> None:
        scored[name] = {"verdict": verdict, "hit": verdict == VERDICT_HIT}
        detail[name] = dict(observed)

    def scored_or_vacuous(population: int, hit: bool) -> str:
        return VERDICT_VACUOUS if population == 0 else _verdict(hit)

    # R1-1 -- the three clauses of the enumerator cross-check.
    clause_a = _bool(cross["agrees_with_sealed_at_zero_one_two"])
    clause_b = _bool(cross["agrees_with_wider_at_zero_two_three"])
    clause_c = _bool(cross["one_item_difference_is_closed_form_on_every_base"]) and _bool(
        cross["one_item_difference_non_empty_on_some_base"]
    )
    record(
        "R1-1",
        scored_or_vacuous(_int(cross["family_size"]), clause_a and clause_b and clause_c),
        {
            "family_size": cross["family_size"],
            "clause_a_agrees_with_sealed": clause_a,
            "clause_b_agrees_with_wider": clause_b,
            "clause_c_difference_is_the_ruled_forms_everywhere": cross[
                "one_item_difference_is_closed_form_on_every_base"
            ],
            "clause_c_difference_non_empty_somewhere": cross[
                "one_item_difference_non_empty_on_some_base"
            ],
        },
    )

    # R1-2 -- the reconstruction against the pinned two-item record.
    built = _int(recon["trees_built"])
    record(
        "R1-2",
        scored_or_vacuous(
            built,
            built == _int(recon["trees_pinned"])
            and _bool(recon["all_four_quantities_agree"])
            and _bool(recon["selection_agrees_everywhere"]),
        ),
        {
            "trees_built": recon["trees_built"],
            "trees_pinned": recon["trees_pinned"],
            "all_four_quantities_agree": recon["all_four_quantities_agree"],
            "selection_agrees_everywhere": recon["selection_agrees_everywhere"],
            "selection_comparisons": recon["selection_comparisons"],
            "mismatch_exhibits": recon["selection_mismatch_exhibits"],
        },
    )

    # R1-3 -- the runs whose pinned record carries no refusal are unmoved.
    compared = _int(pinned["rows_compared"])
    record(
        "R1-3",
        scored_or_vacuous(
            compared,
            _bool(pinned["population_is_the_three_named_complement"])
            and compared == _int(pinned["population_size"])
            and _bool(pinned["all_five_quantities_agree"]),
        ),
        {
            "population_size": pinned["population_size"],
            "rows_compared": pinned["rows_compared"],
            "population_is_the_three_named_complement": pinned[
                "population_is_the_three_named_complement"
            ],
            "pinned_runs_with_a_refusal": pinned["pinned_runs_with_a_refusal"],
            "all_five_quantities_agree": pinned["all_five_quantities_agree"],
            "disagreeing_rows": [r for r in _rows(pinned["rows"]) if not _bool(r["agree"])],
        },
    )

    # R1-4 -- the headline: no retained minimum carries a datum item.
    retained = _int(agg["response_edges"])
    record(
        "R1-4",
        scored_or_vacuous(retained, _int(agg["edges_with_datum_item"]) == 0),
        {
            "retained_minimum_edges": agg["response_edges"],
            "retained_minimum_edges_by_item_count": agg["response_edges_by_item_count"],
            "edges_selected_at_three_items": agg["edges_selected_at_three_items"],
            "runs_with_a_three_item_selection": agg["runs_with_a_three_item_selection"],
            "scope_of_the_population": (
                "the headline is stated over every retained minimum of the rectangle; "
                "most were selected at one or two items, and the count selected at three "
                "items -- the space this rung declares -- is reported beside it so the "
                "three-item evidence is not read as the whole population"
            ),
            "edges_with_datum_item": agg["edges_with_datum_item"],
            "runs_with_such_an_edge": [
                r["id"] for r in runs if _int(r["edges_with_datum_item"]) > 0
            ],
            "exhibits": [
                e for r in runs for e in _rows(r["edges_with_datum_item_exhibits"])
            ],
        },
    )

    # R1-5 -- no VALID three-item response to a same demand carries a datum item.
    same_situations = _int(enum["same_kind_situations"])
    record(
        "R1-5",
        scored_or_vacuous(
            same_situations, _int(enum["same_kind_valid_with_datum_item"]) == 0
        ),
        {
            "same_kind_situations": enum["same_kind_situations"],
            "valid_three_item_responses_at_them": enum["same_kind_valid_three_item_responses"],
            "valid_with_datum_item": enum["same_kind_valid_with_datum_item"],
            "two_item_census_rows_by_kind": avail["census_two_rows_by_kind"],
            "two_item_census_rows_with_a_fresh_datum_response_by_kind": avail[
                "census_two_rows_with_fresh_datum_available_by_kind"
            ],
            "mechanism_scope": (
                "the verdict is about three-item responses at the enumeration "
                "situations. The mechanism offered beside the frozen claim -- that an "
                "addition falling identically on both members of a pair cannot honour a "
                "same demand -- does NOT hold generally: at the two-item bound this run "
                "records same-kind rows at which a valid response carrying a fresh datum "
                "exists, and the by-kind split above is that count. A13 already declines "
                "to read a HIT as evidence for a mechanism; this is the specific "
                "disconfirming count, recorded rather than left to be recomputed"
            ),
            "exhibits": [
                _sub(_sub(r)[INHERITED])["datum_item_exhibits"]
                for r in _rows(enum["rows"])
                if _str(_sub(r)["kind"]) == SAME
                and _int(_sub(_sub(r)[INHERITED])["valid_with_datum_item"]) > 0
            ],
        },
    )

    # R1-6 -- the shape of a valid three-item response to a same demand.
    same_valid = _int(enum["same_kind_valid_three_item_responses"])
    record(
        "R1-6",
        scored_or_vacuous(
            same_valid,
            _int(enum["same_kind_valid_without_two_instances_and_without_a_rule"]) == 0,
        ),
        {
            "valid_three_item_responses_to_a_same_demand": enum[
                "same_kind_valid_three_item_responses"
            ],
            "responses_with_at_most_one_instance_and_no_rule": enum[
                "same_kind_valid_without_two_instances_and_without_a_rule"
            ],
            "declared_member_totals": enum["by_declared_member"],
            "mechanism_scope": (
                "the shape claim is scored over VALID THREE-ITEM responses at the "
                "enumeration situations. It is not a claim about every valid response to "
                "a same demand at every bound: at two items this run records valid "
                "same-kind responses carrying one instance, no rule and a fresh datum"
            ),
            "exhibits": [
                _sub(_sub(r)[INHERITED])["off_shape_exhibits"]
                for r in _rows(enum["rows"])
                if _str(_sub(r)["kind"]) == SAME
                and _int(
                    _sub(_sub(r)[INHERITED])[
                        "valid_without_two_instances_and_without_a_rule"
                    ]
                )
                > 0
            ],
        },
    )

    # R1-7 -- at least one recorded refusal situation is answered at three items.
    examined = _int(rect["situations_examined"])
    record(
        "R1-7",
        scored_or_vacuous(
            examined, _int(rect["situations_answered_at_exactly_three_items"]) > 0
        ),
        {
            "refusal_records": rect["refusal_records"],
            "distinct_situations": rect["distinct_situations"],
            "situations_examined": rect["situations_examined"],
            "situations_answered_at_exactly_three_items": rect[
                "situations_answered_at_exactly_three_items"
            ],
            "answered": [
                _sub(r)["situation"]
                for r in _rows(rect["rows"])
                if _bool(_sub(_sub(r)[INHERITED])["answered_at_exactly_three_items"])
            ],
        },
    )

    # R1-8 -- the three-item rectangle still records a refusal somewhere.
    record(
        "R1-8",
        scored_or_vacuous(_int(agg["runs"]), _int(agg["refusal_records"]) > 0),
        {
            "runs": agg["runs"],
            "refusal_records": agg["refusal_records"],
            "runs_with_a_refusal": agg["runs_with_a_refusal"],
        },
    )

    # R1-9 -- availability at the two-item bound, with its companion counters.
    #
    # The five clauses are recorded one by one.  The last is the frozen
    # counted-zero clause; it compares two counters that are now incremented
    # independently in the census loop, so it can fail.  It used to compare a
    # value with itself, which is the very defect commit dbaa4b73 repaired
    # and which R1-9's own frozen text cites.
    r1_9_clauses = {
        "a_priced_out_rows_above_zero": _int(avail["priced_out_rows"]) > 0,
        "b_no_priced_out_row_of_the_same_kind": (
            _int(avail["priced_out_rows_of_the_same_kind"]) == 0
        ),
        "c_a_three_item_enumeration_was_performed": (
            _int(avail["three_item_enumerations_performed"]) > 0
        ),
        "d_every_node_was_censused": (
            _int(avail["nodes_censused"]) >= _int(avail["node_population"])
        ),
        "e_examined_is_not_below_offered": (
            _int(avail["fresh_datum_candidates_examined"])
            >= _int(avail["fresh_datum_candidates_offered"])
        ),
    }
    record(
        "R1-9",
        scored_or_vacuous(
            _int(avail["census_two_rows"]), all(r1_9_clauses.values())
        ),
        {
            "clauses": {k: bool(v) for k, v in sorted(r1_9_clauses.items())},
            "failing_clauses": sorted(k for k, v in r1_9_clauses.items() if not v),
            "census_two_rows": avail["census_two_rows"],
            "census_two_rows_with_fresh_datum_available": avail[
                "census_two_rows_with_fresh_datum_available"
            ],
            "census_two_rows_available_where_no_minimum_was_retained": avail[
                "census_two_rows_available_where_no_minimum_was_retained"
            ],
            "priced_out_rows": avail["priced_out_rows"],
            "priced_out_nodes": avail["priced_out_nodes"],
            "priced_out_rows_by_kind": avail["priced_out_rows_by_kind"],
            "priced_out_rows_of_the_same_kind": avail["priced_out_rows_of_the_same_kind"],
            "three_item_enumerations_performed": avail["three_item_enumerations_performed"],
            "nodes_censused": avail["nodes_censused"],
            "node_population": avail["node_population"],
            "fresh_datum_candidates_offered": avail["fresh_datum_candidates_offered"],
            "fresh_datum_candidates_examined": avail["fresh_datum_candidates_examined"],
            "fresh_datum_candidates_judged": avail["fresh_datum_candidates_judged"],
            "fresh_datum_candidates_skipped_as_noop": avail[
                "fresh_datum_candidates_skipped_as_noop"
            ],
        },
    )

    # R1-10 -- no declared budget fired, nothing escaped, the bytes repeat.
    fired = sorted(
        set(_strs(agg["budget_terminals_fired"]))
        | {_str(_sub(r)["terminal"]) for r in _rows(agg["situation_budget_terminals_fired"])}
    )
    record(
        "R1-10",
        _verdict(
            not fired
            and not _bool(agg["unhandled_abort"])
            and not _bool(wall["truncated"])
            and _bool(serial["body_renders_identically_twice"])
            and not _bool(serial["body_contains_a_carriage_return"])
        ),
        {
            "budget_terminals_fired": fired,
            "budget_terminals_fired_in_the_tree_loop": agg["budget_terminals_fired"],
            "budget_terminals_fired_in_the_situation_gatherer": agg[
                "situation_budget_terminals_fired"
            ],
            "max_projected_candidates_in_one_enumeration": avail[
                "max_projected_candidates_in_one_enumeration"
            ],
            "max_projected_candidates_at": avail["max_projected_candidates_at"],
            "candidate_budget": _sub(body["declared_budgets"])[
                "max_candidates_per_enumeration"
            ],
            "unhandled_abort": agg["unhandled_abort"],
            "wall_clock_truncated": wall["truncated"],
            "iso_budget_rows": avail["iso_budget_rows"],
            "body_renders_identically_twice": serial["body_renders_identically_twice"],
            "body_contains_a_carriage_return": serial["body_contains_a_carriage_return"],
            "body_sha256": serial["body_sha256"],
        },
    )

    # R1-11 -- how many situations the recorded refusal nodes present.
    distinct = _int(rect["distinct_situations"])
    record(
        "R1-11",
        scored_or_vacuous(_int(rect["refusal_records"]), 3 < distinct < 15),
        {
            "refusal_records": rect["refusal_records"],
            "distinct_situations": rect["distinct_situations"],
            "strictly_above_three": distinct > 3,
            "strictly_below_fifteen": distinct < 15,
        },
    )

    # R1-X -- the extrapolation, about a rectangle this rung does not compute.
    scored["R1-X"] = {"verdict": VERDICT_PENDING, "hit": False}
    detail["R1-X"] = {
        "scored_by": "the rung that reaches an item bound of four",
        "this_rung_item_bound": ST.BOUNDS_THREE.max_items,
        "three_item_edges_with_datum_item": agg["edges_with_datum_item"],
        "three_item_runs_with_a_refusal": agg["runs_with_a_refusal"],
        "every_recorded_situation_answered_at_three_items": examined
        == _int(rect["situations_answered_at_exactly_three_items"]),
        "three_item_refusal_records": agg["refusal_records"],
    }
    return scored, detail


# ---------------------------------------------------------------------------
# The receipt
# ---------------------------------------------------------------------------


def situation_tables(
    trees: Sequence[ST.STree],
    gatherer: Gatherer,
    deadline: Deadline,
    empty_rect: Mapping[str, Json],
    empty_enum: Mapping[str, Json],
) -> tuple[dict[str, Json], dict[str, Json], str]:
    """Both situation tables, with the one exception that can escape them.

    ``dual._budget`` raises a bare ``RuntimeError`` from inside the sibling's
    key, and the sibling computes that key outside every handler.  Here it is
    caught, both tables are replaced by their empty shapes, and the abort is
    recorded on the aggregate rather than ending the run.

    Split out of ``build_all`` so that the handler can be exercised on a
    gatherer that raises, without building the rectangle first.
    """

    try:
        rect: dict[str, Json] = rectangle_a(gatherer, deadline)
        enum: dict[str, Json] = enumeration_situations(trees, gatherer, deadline)
    except RuntimeError as exc:  # the bijection budget, raised outside a handler
        return dict(empty_rect), dict(empty_enum), f"RuntimeError: {exc}"
    return rect, enum, ""


def _written_hash_agrees(recorded: str, written: str) -> bool:
    """Whether the hash the receipt recorded is the one the export wrote.

    A separate function so the disagreeing case can be exercised without
    building a receipt: it is the one assertion of ``main`` that a reader
    cannot otherwise see fail.
    """

    return recorded == written


def build_all(
    deadline: Deadline, frozen_sha256: Mapping[pathlib.Path, str]
) -> dict[str, Json]:
    cross = cross_check_table()
    recon = two_item_reconstruction(deadline)
    trees, rows = three_item_runs(deadline)
    gatherer = Gatherer()
    empty_rect: dict[str, Json] = {
        "validity_rule_of_the_refusal_population": ST.RULE_NO_REGRESS,
        "refusal_records": 0,
        "distinct_situations": 0,
        "situations_examined": 0,
        "situations_answered_at_exactly_three_items": 0,
        "refusal_records_by_kind": {},
        "rows": [],
    }
    empty_enum: dict[str, Json] = {
        "enumeration_records": 0,
        "distinct_situations": 0,
        "situations_examined": 0,
        "situations_by_kind": {},
        "same_kind_situations": 0,
        "same_kind_valid_three_item_responses": 0,
        "same_kind_valid_with_datum_item": 0,
        "same_kind_valid_without_two_instances_and_without_a_rule": 0,
        "rows": [],
    }
    rect, enum, unhandled = situation_tables(
        trees, gatherer, deadline, empty_rect, empty_enum
    )
    agg = aggregate(rows)
    agg["unhandled_abort"] = bool(unhandled)
    agg["unhandled_abort_detail"] = unhandled
    agg["situation_enumerations"] = gatherer.enumerations
    agg["situation_repeats_answered_from_the_record"] = gatherer.repeats
    agg["situation_deltas_offered"] = gatherer.deltas_offered
    agg["situation_max_projected_candidates"] = gatherer.max_projected_candidates
    agg["situation_max_valid_at_one_pair"] = gatherer.max_valid_at_one_pair
    agg["situation_budget_terminals_fired"] = [_j(r) for r in gatherer.budget_terminals]
    body: dict[str, Json] = {
        "authority_effect": "None",
        "rung": RUNG,
        "rung_name": RUNG_NAME,
        "seed_sha256": frozen_sha256[SEED],
        "prompt_sha256": frozen_sha256[HERE / "PROMPT.md"],
        "predictions_sha256": frozen_sha256[HERE / "PREDICTIONS.md"],
        "declared_bounds": {
            "max_items": ST.BOUNDS_THREE.max_items,
            "max_arity": ST.BOUNDS_THREE.max_arity,
            "max_rounds": ST.MAX_ROUNDS,
            "pre_expansion_node_guard": ST.GUARD,
            "growth_data_bound": ST.MAX_DATA,
            "sibling_item_bound": ST.BOUNDS_TWO.max_items,
        },
        "declared_budgets": {
            "max_enumerations_per_run": ST.MAX_ENUMERATIONS_PER_RUN,
            "max_candidates_per_enumeration": ST.MAX_CANDIDATES_PER_ENUMERATION,
            "max_valid_per_target": ST.MAX_VALID_PER_TARGET,
            "max_classes_per_node": ST.MAX_CLASSES_PER_NODE,
            "terminals": list(ST.BUDGET_TERMINALS) + [ST.TERMINAL_ISO_BUDGET],
            "observed_maxima": {
                "tree_loop_max_projected_candidates_in_one_enumeration": agg[
                    "max_projected_candidates_in_one_enumeration"
                ],
                "tree_loop_max_projected_candidates_at": agg["max_projected_candidates_at"],
                "situation_gatherer_max_projected_candidates": agg[
                    "situation_max_projected_candidates"
                ],
                "situation_gatherer_max_valid_at_one_pair": agg[
                    "situation_max_valid_at_one_pair"
                ],
                "scope": (
                    "the enumeration and class budgets govern the tree loop alone; "
                    "the candidate and response budgets are enforced in the tree "
                    "loop and in the situation gatherer, with the same terminals"
                ),
            },
        },
        "validity_class": {
            "inherited_member": ST.RULE_NO_REGRESS,
            "declared_member": ST.RULE_STRICT_NO_REGRESS,
            "inherited_member_runs": [
                "the twenty runs of the rectangle",
                "the twenty runs of the two-item reconstruction",
                "the two-item availability census",
                "the three-item availability census",
                "the re-derivation of the refusal population",
                "the scored column of the situation tables",
            ],
            "declared_member_runs": [
                "the deduplicated three-item enumeration situations",
                "the deduplicated refusal situations",
            ],
        },
        "readings": [r.name for r in sealed_readings()],
        "commitments": [c.name for c in COMMITMENTS],
        "measures": list(ST.MEASURES),
        "assumptions": assumptions(),
        "wall_clock_truncation": deadline.as_json(),
        "cross_check": cross,
        "two_item_reconstruction": recon,
        "runs": [_j(r) for r in rows],
        "aggregate": agg,
        "three_item_versus_pinned": versus_pinned(rows),
        "rectangle_a": rect,
        "enumeration_situations": enum,
        "availability": availability_block(rows, agg),
    }
    first = dumps_deterministic(_j(body))
    second = dumps_deterministic(_j(body))
    body["serialization"] = {
        "body_sha256": hashlib.sha256(first).hexdigest(),
        "body_bytes": len(first),
        "body_renders_identically_twice": first == second,
        "body_contains_a_carriage_return": b"\r" in first,
        "scope": (
            "the body is every key of this receipt but the scoring and this block, "
            "before the split; a second invocation writes the same bytes when the "
            "declared wall bound did not fire"
        ),
    }
    scored, detail = score_predictions(body)
    body["predictions_scored"] = scored
    body["prediction_detail"] = detail
    return body


def split(payload: Mapping[str, Json]) -> tuple[dict[str, Json], dict[str, Json]]:
    """Summary plus a compressed export, in the sibling's shape.

    The per-node census rows and the per-run edges are the bulk; they move
    to the compressed export and the summary records its content hash. Every
    value a prediction is scored from stays in the summary.
    """

    bulk = ("census_two_all_rows", "edges")
    runs = _rows(payload["runs"])
    full: dict[str, Json] = {
        "authority_effect": "None",
        "runs": [
            {"id": r["id"], **{k: r[k] for k in bulk}} for r in runs
        ],
    }
    sha = hashlib.sha256(dumps_deterministic(full)).hexdigest()
    summary: dict[str, Json] = dict(payload)
    summary["runs"] = [{k: v for k, v in r.items() if k not in bulk} for r in runs]
    summary["full_export"] = {
        "path": FULL_PATH,
        "sha256_uncompressed": sha,
        "contents": [f"runs[].{k}" for k in bulk],
    }
    return summary, full


def summary_line(payload: Mapping[str, Json]) -> str:
    agg = _sub(payload["aggregate"])
    rect = _sub(payload["rectangle_a"])
    scored = _sub(payload["predictions_scored"])
    tally: dict[str, int] = {}
    for value in scored.values():
        verdict = _str(_sub(value)["verdict"])
        tally[verdict] = tally.get(verdict, 0) + 1
    order = (VERDICT_HIT, VERDICT_MISSED, VERDICT_VACUOUS, VERDICT_PENDING)
    votes = " ".join(f"{name}={tally.get(name, 0)}" for name in order)
    return (
        f"rung {RUNG} at item bound {ST.BOUNDS_THREE.max_items}: "
        f"{_int(agg['runs'])} runs, {_int(agg['nodes'])} nodes, {_int(agg['edges'])} edges, "
        f"{_int(agg['refusal_records'])} refusal records, "
        f"{_int(rect['distinct_situations'])} distinct refusal situations "
        f"({_int(rect['situations_answered_at_exactly_three_items'])} answered at three "
        f"items); {_int(agg['edges_with_datum_item'])} of "
        f"{_int(agg['response_edges'])} retained minima carry a datum item, and "
        f"{_int(agg['edges_selected_at_three_items'])} of those "
        f"{_int(agg['response_edges'])} were selected from the three-item space, in "
        f"{len(_sub(agg['runs_with_a_three_item_selection']))} of "
        f"{_int(agg['runs'])} runs; "
        f"{_int(agg['nodes_stopped_by_the_node_guard'])} nodes stopped by the node "
        f"guard in {len(_sub(agg['runs_truncated_by_the_node_guard']))} runs; {votes}"
    )


def _prediction_order(name: str) -> tuple[int, str]:
    tail = name.split("-", 1)[1]
    return (int(tail), "") if tail.isdigit() else (10**6, tail)


def _observed(row: Mapping[str, Json]) -> str:
    parts: list[str] = []
    for key in sorted(row):
        value = row[key]
        if isinstance(value, (bool, int, float, str)):
            parts.append(f"{key}={value}")
        if len(parts) >= 4:
            break
    return ", ".join(parts)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Write the rung-one receipt.")
    parser.add_argument("--out", type=pathlib.Path, default=HERE / "receipts" / "stream.json")
    parser.add_argument("--full", type=pathlib.Path, default=HERE / FULL_PATH)
    parser.add_argument(
        "--wall-bound",
        type=float,
        default=WALL_BOUND_SECONDS,
        help="the declared wall bound in seconds; passing it records a truncation",
    )
    args = parser.parse_args(argv)
    try:
        frozen_sha256 = verify_frozen_disk()
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    deadline = Deadline(float(args.wall_bound))
    body = build_all(deadline, frozen_sha256)
    try:
        verify_frozen_disk()
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    summary, full = split(body)
    out = pathlib.Path(str(args.out))
    full_path = pathlib.Path(str(args.full))
    write_json(out, summary)
    sha = write_json_gz(full_path, full)
    if not _written_hash_agrees(
        _str(_sub(summary["full_export"])["sha256_uncompressed"]), sha
    ):
        raise AssertionError("the recorded content hash is not the one written")
    scored = _sub(summary["predictions_scored"])
    detail = _sub(summary["prediction_detail"])
    for name in sorted(scored, key=_prediction_order):
        verdict = _str(_sub(scored[name])["verdict"])
        print(f"{name}: {verdict:8s} {_observed(_sub(detail[name]))}")
    print(summary_line(summary))
    print(f"wall time {deadline.elapsed():.1f}s (declared bound {deadline.seconds:.0f}s)")
    print(f"wrote {out} ({out.stat().st_size} bytes) and {full_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover - the entry point, run by hand
    sys.exit(main())
