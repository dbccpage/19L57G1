"""E2 vs E2' diagnostic over the endogenous_demand census.

Throwaway. Imports the tree's candidates and the sealed derivation
model read-only via git-archive of the census commit. Not a receipt.

AuthorityEffect: None.
"""

from __future__ import annotations

import io
import sys
import tarfile
import tempfile
from pathlib import Path
import subprocess
from typing import Callable

REPO = Path(__file__).resolve().parents[1]
CENSUS_COMMIT = "b947873b6147f196686163d00a0946de639f8c2c"


def _load_tree() -> Path:
    archive = subprocess.check_output(
        ["git", "-C", str(REPO), "archive", "--format=tar", CENSUS_COMMIT,
         "research/endogenous_demand"],
    )
    tmp = Path(tempfile.mkdtemp(prefix="ob1_e2_"))
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        tar.extractall(tmp)
    packet = tmp / "research" / "endogenous_demand"
    sys.path.insert(0, str(REPO / "code"))
    sys.path.insert(0, str(packet))
    return packet


_load_tree()

from derivation.engine import closure_challenge_orbits  # noqa: E402
from derivation.model import (  # noqa: E402
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Pair,
    Regime,
    Supply,
    replay,
)
from derivation.observe import collapsed_pairs, separable  # noqa: E402

import candidates as cand  # noqa: E402
from grammar import e2_violation, is_impose  # noqa: E402
from reader import read_pairs_of_regime  # noqa: E402


def _sep(regime: Regime, pair: Pair | None) -> bool | None:
    if pair is None:
        return None
    return separable(regime, pair[0], pair[1])


def _pair(values: object) -> Pair | None:
    if values is None:
        return None
    if isinstance(values, (list, tuple)) and len(values) == 2:
        left, right = values
        if isinstance(left, int) and isinstance(right, int):
            return (left, right)
    return None


def eval_c1() -> dict[str, object]:
    history = cand._two_data()
    regime = replay(history)
    picked = cand.host_next_demand(regime)
    pair = _pair(picked)
    return {
        "history": history,
        "regime": regime,
        "pair": pair,
        "how_designated": "host_next_demand",
        "last_event": type(history[-1]).__name__,
    }


def eval_c2() -> dict[str, object]:
    base_h = cand._two_data()
    orbits = closure_challenge_orbits(replay(base_h))
    history = base_h + tuple(Impose(i, j) for i, j in orbits)
    regime = replay(history)
    pair = orbits[0] if orbits else None
    return {
        "history": history,
        "regime": regime,
        "pair": pair,
        "how_designated": "closure_challenge_orbits then Impose",
        "last_event": type(history[-1]).__name__,
    }


def eval_c3() -> dict[str, object]:
    supplied = cand._two_data() + (Impose(0, 1),)
    history = supplied + (AdmitForm(2), AdmitInst(0, (0, 1)))
    regime = replay(history)
    return {
        "history": history,
        "regime": regime,
        "pair": (0, 1),
        "how_designated": "copy of previously imposed pair, then AdmitInst",
        "last_event": type(history[-1]).__name__,
        "identical_to_supplied": (0, 1) in replay(supplied).reqs,
    }


def eval_c4() -> dict[str, object]:
    history = cand._two_data() + (AdmitForm(2), AdmitRuleAll(0))
    regime = replay(history)
    read = read_pairs_of_regime(regime, 0)
    collapsed = collapsed_pairs(regime)
    return {
        "history": history,
        "regime": regime,
        "pair": None,
        "how_designated": "AdmitRuleAll; reader sees no insts",
        "last_event": type(history[-1]).__name__,
        "read_pairs": [list(p) for p in read],
        "collapsed_after_rule": [list(p) for p in collapsed],
        "insts": len(regime.insts),
        "rules": sorted(regime.rules),
    }


def eval_c5() -> dict[str, object]:
    history = cand._two_data() + (Supply("c"), AdmitDatum("c"))
    regime = replay(history)
    demanded = [
        (i, j)
        for i in range(regime.n_data())
        for j in range(i + 1, regime.n_data())
        if cand.host_holds(i, j)
    ]
    pair = demanded[0] if demanded else None
    return {
        "history": history,
        "regime": regime,
        "pair": pair,
        "how_designated": "host_holds on growth",
        "last_event": type(history[-1]).__name__,
        "host_demanded": [list(p) for p in demanded],
    }


def eval_c6() -> dict[str, object]:
    history = cand._two_data() + (Supply("c"), AdmitDatum("c"), Impose(0, 2))
    regime = replay(history)
    return {
        "history": history,
        "regime": regime,
        "pair": (0, 2),
        "how_designated": "AdmitDatum then Impose",
        "last_event": type(history[-1]).__name__,
    }


def eval_c9() -> dict[str, object]:
    history = cand._marked_two_data()
    regime = replay(history)
    return {
        "history": history,
        "regime": regime,
        "pair": (0, 1),
        "how_designated": "unary AdmitInst on datum 0",
        "last_event": type(history[-1]).__name__,
    }


def eval_i1() -> dict[str, object]:
    history = cand._two_data() + (AdmitForm(2), AdmitInst(0, (0, 1)))
    regime = replay(history)
    read = read_pairs_of_regime(regime, 0)
    pair = read[0] if read else None
    return {
        "history": history,
        "regime": regime,
        "pair": pair,
        "how_designated": "never-selects read of AdmitInst (0,[0,1])",
        "last_event": type(history[-1]).__name__,
        "read_pairs": [list(p) for p in read],
        "insts": [list(inst) for inst in sorted(regime.insts)],
    }


def eval_shape() -> dict[str, object]:
    """The candidate surviving shape, realized with the only sealed rule."""
    history = cand._two_data() + (AdmitForm(2), AdmitRuleAll(0))
    regime = replay(history)
    read = read_pairs_of_regime(regime, 0)
    collapsed = collapsed_pairs(regime)
    pair = collapsed[0] if collapsed else None
    return {
        "history": history,
        "regime": regime,
        "pair": pair,
        "how_designated": "uniform rule; no instance emitted",
        "last_event": type(history[-1]).__name__,
        "read_pairs": [list(p) for p in read],
        "collapsed_after_rule": [list(p) for p in collapsed],
        "insts": len(regime.insts),
        "already_separable": _sep(regime, pair),
    }


EVALUATORS: dict[str, Callable[[], dict[str, object]]] = {
    "C1": eval_c1,
    "C2": eval_c2,
    "C3": eval_c3,
    "C4": eval_c4,
    "C5": eval_c5,
    "C6": eval_c6,
    "C9": eval_c9,
    "I1": eval_i1,
}


def classify_e2p(cid: str, row: dict[str, object], ev: dict[str, object]) -> tuple[str, str]:
    """Return (failing_clause, reason) under E2'. Empty clause means not killed by E2' alone."""
    pair = ev.get("pair")
    regime = ev["regime"]
    assert isinstance(regime, Regime)
    p = pair if isinstance(pair, tuple) else None
    already = _sep(regime, p) if p is not None else None
    last = str(ev["last_event"])
    how = str(ev["how_designated"])
    in_reqs = bool(p is not None and p in regime.reqs)
    host = how.startswith("host") or "closure_challenge_orbits" in how or "host_holds" in how

    if cid == "C4":
        return "E2'", "uniform AdmitRuleAll emits no insts and designates no pair"
    if host:
        return "E1", "host or declared policy chooses the pair"
    if already is True:
        return "E3", f"pair {p} is already separable"
    if in_reqs or last == "Impose":
        if cid == "C3" or ev.get("identical_to_supplied") is True:
            return "E3", "pair identical to a previously supplied Impose"
        return "E2'", f"last event is {last}; designation is supplied"
    if last == "AdmitInst":
        return "E2'", "instance was admitted, not produced by a rule firing"
    if p is None:
        return "E2'", "no pair designated"
    if already is False and not host and last != "Impose":
        return "E2'", f"pair {p} is owed but not produced by a rule firing ({last})"
    return "E2'", how


def row_record(census_row: dict[str, object]) -> dict[str, object]:
    cid = str(census_row["id"])
    e2_fails = tuple(census_row["fails"])
    e2_status = str(census_row["status"])
    e2_reason = str(census_row["reason"])
    if cid in {"C7", "C8"}:
        return {
            "id": cid,
            "e2_fails": ",".join(e2_fails) or "—",
            "e2_status": e2_status,
            "e2p_fails": "E1",
            "e2p_reason": "cited host/reflective construct; no separable witness in the tree",
            "flipped": "not claimed",
            "witness": "none",
            "pair": "—",
            "in_reqs": "—",
            "already_separable": "—",
            "last_event": "—",
        }
    if cid == "C10":
        return {
            "id": cid,
            "e2_fails": "—",
            "e2_status": e2_status,
            "e2p_fails": "outside",
            "e2p_reason": "new Event constructor is a sealed-path amendment",
            "flipped": "no",
            "witness": "none",
            "pair": "—",
            "in_reqs": "—",
            "already_separable": "—",
            "last_event": "—",
        }
    ev = EVALUATORS[cid]()
    regime = ev["regime"]
    assert isinstance(regime, Regime)
    pair = ev.get("pair")
    p = pair if isinstance(pair, tuple) else None
    already = _sep(regime, p)
    in_reqs = p in regime.reqs if p is not None else False
    history = ev["history"]
    assert isinstance(history, tuple)
    e2p_clause, e2p_reason = classify_e2p(cid, census_row, ev)
    flipped = "yes" if (cid == "I1" or set(e2_fails) != {e2p_clause}) and cid == "I1" else "no"
    if cid == "I1":
        flipped = "yes"
    elif e2p_clause not in e2_fails and e2_status == "defeated":
        flipped = "restated"
        if e2p_clause in {"E1", "E2", "E3"} and e2p_clause in e2_fails:
            flipped = "no"
    return {
        "id": cid,
        "e2_fails": ",".join(e2_fails) or "—",
        "e2_status": e2_status,
        "e2p_fails": e2p_clause,
        "e2p_reason": e2p_reason,
        "flipped": flipped,
        "witness": "yes",
        "pair": list(p) if p is not None else None,
        "in_reqs": in_reqs,
        "already_separable": already,
        "last_event": ev["last_event"],
        "how": ev["how_designated"],
        "e2_violation": e2_violation(history),
        "e2_reason": e2_reason,
        "collapsed": [list(q) for q in collapsed_pairs(regime)],
        "reqs": [list(q) for q in sorted(regime.reqs)],
    }


def print_table(rows: list[dict[str, object]]) -> None:
    headers = (
        "id", "E2 fails", "E2 status", "E2' fails", "flipped",
        "pair", "in reqs", "already sep", "last event",
    )
    body: list[tuple[str, ...]] = []
    for row in rows:
        body.append((
            str(row["id"]),
            str(row["e2_fails"]),
            str(row["e2_status"]),
            str(row["e2p_fails"]),
            str(row["flipped"]),
            str(row["pair"]),
            str(row["in_reqs"]),
            str(row["already_separable"]),
            str(row["last_event"]),
        ))
    widths = [len(h) for h in headers]
    for line in body:
        for i, cell in enumerate(line):
            widths[i] = max(widths[i], len(cell))

    def fmt(cells: tuple[str, ...]) -> str:
        return "| " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells)) + " |"

    print(fmt(headers))
    print("| " + " | ".join("-" * w for w in widths) + " |")
    for line in body:
        print(fmt(line))
    print()
    for row in rows:
        print(f"{row['id']}: {row['e2p_reason']}")
        if row.get("how"):
            print(f"     how={row['how']}")
        if row.get("e2_violation") is not None:
            print(f"     e2_violation={row['e2_violation']}")


def main() -> int:
    print(f"census commit {CENSUS_COMMIT}")
    print(f"sealed code    {REPO / 'code'}")
    print(f"CENSUS ids     {[row['id'] for row in cand.CENSUS]}")
    print()
    rows = [row_record(row) for row in cand.CENSUS]
    print_table(rows)
    print()
    print("=== surviving-shape probe (AdmitRuleAll only) ===")
    shape = eval_shape()
    print(
        f"insts={shape['insts']} read_pairs={shape['read_pairs']} "
        f"collapsed={shape['collapsed_after_rule']} "
        f"already_separable={shape['already_separable']} "
        f"last={shape['last_event']}"
    )
    print("uniform rule does not emit an instance; collapsed pair stays collapsed.")
    print("that is not a generator under E1/E2'/E3.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
