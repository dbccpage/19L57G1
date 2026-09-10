"""E2 vs E2' diagnostic over the endogenous_demand census.

Imports the live tree and sealed derivation read-only. Pins
``candidates.py`` to commit ``b947873``. Not a receipt.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CENSUS_COMMIT = "b947873b6147f196686163d00a0946de639f8c2c"
CANDIDATES_SHA256 = (
    "dd9f429fa6d6b7914837d4dab4160fd667db513b498599c742ac1a9fd7a560ef"
)
FINDING = Path(__file__).resolve().parent / "FINDING.md"

sys.path.insert(0, str(REPO / "code"))
sys.path.insert(0, str(REPO / "research" / "endogenous_demand"))

from derivation.engine import closure_challenge_orbits  # noqa: E402
from derivation.model import (  # noqa: E402
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Pair,
    Regime,
    Supply,
    replay,
)
from derivation.observe import collapsed_pairs, separable  # noqa: E402

import candidates as cand  # noqa: E402
from grammar import e2_violation  # noqa: E402
from reader import read_pairs_of_regime  # noqa: E402


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def check_census_pin() -> None:
    live = (REPO / "research" / "endogenous_demand" / "candidates.py").read_bytes()
    if _sha(live) != CANDIDATES_SHA256:
        raise SystemExit("candidates.py does not match the b947873 pin")
    try:
        shown = subprocess.check_output(
            ["git", "-C", str(REPO), "show", f"{CENSUS_COMMIT}:research/endogenous_demand/candidates.py"]
        )
    except (subprocess.CalledProcessError, OSError) as exc:
        raise SystemExit(f"git show {CENSUS_COMMIT}:candidates.py failed: {exc}") from exc
    if _sha(shown) != CANDIDATES_SHA256:
        raise SystemExit(f"git show {CENSUS_COMMIT}:candidates.py does not match the pin")


@dataclass(frozen=True)
class Probe:
    cid: str
    history: tuple[Event, ...] | None
    source: str
    pair: Pair | None
    pair_from: str


@dataclass(frozen=True)
class Row:
    cid: str
    e2_fails: str
    e2_status: str
    e2p_fails: str
    e2p_reason: str
    flipped: str
    pair: str
    in_reqs: str
    already_sep: str
    last_event: str
    how: str
    e2_violation: str | None


def _rule_history() -> tuple[Event, ...]:
    """The surviving-shape history shared by probe C4 and shape_probe(): two
    collapsed data, a binary form, and the single uniform rule."""
    return cand._two_data() + (AdmitForm(2), AdmitRuleAll(0))


def probes() -> tuple[Probe, ...]:
    two = cand._two_data()
    orbits = closure_challenge_orbits(replay(two))
    c2_history = two + tuple(Impose(i, j) for i, j in orbits)
    grown = two + (Supply("c"), AdmitDatum("c"))
    rule = _rule_history()
    inst = two + (AdmitForm(2), AdmitInst(0, (0, 1)))
    return (
        Probe("C1", two, "host", None, "host_next"),
        Probe("C2", c2_history, "policy", orbits[0] if orbits else None, "given"),
        Probe("C3", two + (Impose(0, 1), AdmitForm(2), AdmitInst(0, (0, 1))), "launder", (0, 1), "given"),
        Probe("C4", rule, "rule", None, "none"),
        Probe("C5", grown, "host", None, "host_holds"),
        Probe("C6", grown + (Impose(0, 2),), "impose", (0, 2), "given"),
        Probe("C7", None, "cited", None, "none"),
        Probe("C8", None, "cited", None, "none"),
        Probe("C9", cand._marked_two_data(), "inst", (0, 1), "given"),
        Probe("C10", None, "outside", None, "none"),
        Probe("I1", inst, "inst", None, "reader"),
    )


def resolve_pair(probe: Probe, regime: Regime | None) -> Pair | None:
    if probe.pair_from == "given":
        return probe.pair
    if regime is None:
        return None
    if probe.pair_from == "host_next":
        return cand.host_next_demand(regime)
    if probe.pair_from == "host_holds":
        demanded = [
            (i, j)
            for i in range(regime.n_data())
            for j in range(i + 1, regime.n_data())
            if cand.host_holds(i, j)
        ]
        return demanded[0] if demanded else None
    if probe.pair_from == "reader":
        read = read_pairs_of_regime(regime, 0)
        return read[0] if read else None
    return None


def classify(source: str, pair: Pair | None, already: bool | None, last: str) -> tuple[str, str]:
    if source == "outside":
        return "outside", "new Event constructor is a sealed-path amendment"
    if source == "cited":
        return "E1", "cited host/reflective construct; no separable witness in the tree"
    if source in {"host", "policy"}:
        return "E1", "host or declared policy chooses the pair"
    if source == "launder":
        return "E3", "pair identical to a previously supplied Impose"
    if already is True:
        extra = "; instance admitted, not produced by a rule" if last == "AdmitInst" else ""
        return "E3", f"pair {pair} is already separable{extra}"
    if source == "impose" or last == "Impose":
        return "E2'", f"last event is {last}; designation is supplied"
    if source == "inst" or last == "AdmitInst":
        return "E2'", "instance was admitted, not produced by a rule firing"
    if source == "rule":
        return "E2'", "uniform AdmitRuleAll emits no insts and designates no pair"
    return "E2'", f"no pair designated ({source})"


def flip_label(e2_fails: tuple[object, ...], e2_status: str, e2p: str, source: str) -> str:
    if source in {"cited", "outside"}:
        return "not claimed" if source == "cited" else "no"
    if e2_status == "OPEN":
        return "yes"
    if e2p in e2_fails:
        return "no"
    if e2p == "E2'":
        return "restated"
    # e2p is E1 or E3 yet absent from the census fails tuple: a mismatch, not a
    # restatement. Surface it in the cell so --check fails loudly rather than
    # silently mislabelling the row "restated".
    return f"mismatch:{e2p}"


def row_from(census: dict[str, object], probe: Probe) -> Row:
    e2_fails = census["fails"]
    assert isinstance(e2_fails, tuple)
    history = probe.history
    regime: Regime | None = replay(history) if history else None
    pair = resolve_pair(probe, regime)
    already = separable(regime, pair[0], pair[1]) if regime is not None and pair is not None else None
    last = type(history[-1]).__name__ if history else "—"
    e2p, reason = classify(probe.source, pair, already, last)
    in_reqs = pair in regime.reqs if regime is not None and pair is not None else None
    how_by_source = {
        "host": "host_next_demand" if probe.cid == "C1" else "host_holds on growth",
        "policy": "closure_challenge_orbits then Impose",
        "launder": "copy of previously imposed pair, then AdmitInst",
        "rule": "AdmitRuleAll; reader sees no insts",
        "impose": "AdmitDatum then Impose",
        "inst": "never-selects read of AdmitInst (0,[0,1])" if probe.cid == "I1" else "unary AdmitInst on datum 0",
        "cited": "",
        "outside": "",
    }
    try:
        how = how_by_source[probe.source]
    except KeyError:
        raise SystemExit(f"row_from: unknown probe source {probe.source!r} for {probe.cid}") from None
    violation = e2_violation(history) if history else None
    return Row(
        cid=probe.cid,
        e2_fails=",".join(str(x) for x in e2_fails) or "—",
        e2_status=str(census["status"]),
        e2p_fails=e2p,
        e2p_reason=reason,
        flipped=flip_label(e2_fails, str(census["status"]), e2p, probe.source),
        pair="—" if probe.source in {"cited", "outside"} else str(list(pair) if pair is not None else None),
        in_reqs="—" if probe.source in {"cited", "outside"} else str(bool(in_reqs)),
        already_sep="—" if probe.source in {"cited", "outside"} else str(already),
        last_event=last,
        how=how,
        e2_violation=violation,
    )


def render_table(rows: tuple[Row, ...]) -> str:
    headers = (
        "id", "E2 fails", "E2 status", "E2' fails", "flipped",
        "pair", "in reqs", "already sep", "last event",
    )
    body = tuple(
        (r.cid, r.e2_fails, r.e2_status, r.e2p_fails, r.flipped,
         r.pair, r.in_reqs, r.already_sep, r.last_event)
        for r in rows
    )
    widths = [len(h) for h in headers]
    for line in body:
        for i, cell in enumerate(line):
            widths[i] = max(widths[i], len(cell))

    def fmt(cells: tuple[str, ...]) -> str:
        return "| " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells)) + " |"

    lines = [fmt(headers), "| " + " | ".join("-" * w for w in widths) + " |"]
    lines.extend(fmt(line) for line in body)
    return "\n".join(lines)


def shape_probe() -> dict[str, object]:
    history = _rule_history()
    regime = replay(history)
    collapsed = collapsed_pairs(regime)
    pair = collapsed[0] if collapsed else None
    return {
        "insts": len(regime.insts),
        "read_pairs": [list(p) for p in read_pairs_of_regime(regime, 0)],
        "collapsed": [list(p) for p in collapsed],
        "already_separable": separable(regime, pair[0], pair[1]) if pair else None,
        "last": type(history[-1]).__name__,
    }


def all_rows() -> tuple[Row, ...]:
    by_id = {str(row["id"]): row for row in cand.CENSUS}
    missing = sorted({p.cid for p in probes() if p.cid not in by_id})
    if missing:
        raise SystemExit(f"probes reference ids absent from CENSUS: {missing}")
    return tuple(row_from(by_id[p.cid], p) for p in probes())


def check_finding(rows: tuple[Row, ...]) -> None:
    text = FINDING.read_text(encoding="utf-8")
    table = render_table(rows)
    if table not in text:
        raise SystemExit(
            "rendered table is not a substring of FINDING.md: FINDING.md is stale, "
            "or a pinned/live census input changed the table -- re-run "
            "`python reclassify.py` and update FINDING.md, or investigate input drift"
        )
    i1 = next(r for r in rows if r.cid == "I1")
    if i1.already_sep != "True" or i1.e2p_fails != "E3" or i1.flipped != "yes":
        raise SystemExit("I1 under E2' is not the recorded flip")
    shape = shape_probe()
    if shape["insts"] != 0 or shape["already_separable"] is not False:
        raise SystemExit("surviving-shape probe changed")
    if "- `insts = 0`" not in text:
        raise SystemExit("FINDING.md missing surviving-shape insts = 0")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    check_census_pin()
    rows = all_rows()
    table = render_table(rows)
    if args.check:
        check_finding(rows)
        print("PASS: census pin, FINDING.md table, I1 flip")
        return 0
    print(f"census commit {CENSUS_COMMIT}")
    print(f"sealed code    {REPO / 'code'}")
    print(f"CENSUS ids     {[row['id'] for row in cand.CENSUS]}")
    print()
    print(table)
    print()
    for row in rows:
        print(f"{row.cid}: {row.e2p_reason}")
        if row.how:
            print(f"     how={row.how}")
        if row.e2_violation is not None:
            print(f"     e2_violation={row.e2_violation}")
    print()
    print("=== surviving-shape probe (AdmitRuleAll only) ===")
    shape = shape_probe()
    print(
        f"insts={shape['insts']} read_pairs={shape['read_pairs']} "
        f"collapsed={shape['collapsed']} "
        f"already_separable={shape['already_separable']} "
        f"last={shape['last']}"
    )
    print("uniform rule does not emit an instance; collapsed pair stays collapsed.")
    print("that is not a generator under E1/E2'/E3.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
