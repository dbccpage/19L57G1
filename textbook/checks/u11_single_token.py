"""Unit 11 check: one token never yields two data.

Runs Genesis's own Python model over every history of at most seven events
drawn from a single-token alphabet, and compares with the two-token and
occurrence-discipline alternatives and with `artifacts/bridge.json`. This
is sample computation, not a proof; the proof is
Bridge.single_token_carrier_bound. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u11_single_token.py
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.bridge import (  # noqa: E402
    event_alphabet,
    occurrence_step,
    reachable_states,
    scenario_report,
)
from derivation.model import (  # noqa: E402
    AdmissionError,
    AdmitDatum,
    Event,
    Regime,
    Supply,
    replay,
    step,
)

EMPTY = Regime((), (), frozenset(), frozenset(), frozenset())
MAX_EVENTS = 7


def all_histories_bound(alphabet: list[Event], max_len: int,
                        stepper=step) -> tuple[int, int, int]:
    """Replay every history of length <= max_len over the alphabet (not
    only the reachable states): return (histories, admissible, max data)."""
    total = admissible = max_data = 0
    for k in range(max_len + 1):
        for seq in itertools.product(alphabet, repeat=k):
            total += 1
            r = EMPTY
            ok = True
            for e in seq:
                try:
                    r = stepper(r, e)
                except AdmissionError:
                    ok = False
                    break
            if ok:
                admissible += 1
                max_data = max(max_data, r.n_data())
    return total, admissible, max_data


def main() -> int:
    failures: list[object] = []

    # 1. Single token, dedup admission: every history of <= 4 events,
    # replayed one by one (4^... small alphabet).
    alpha1 = event_alphabet(["<>"], 1)   # Supply, AdmitDatum, AdmitForm(2), AdmitInst(0,(0,0))
    total, adm, mx = all_histories_bound(alpha1, 6)
    print(f"single token, every history <= 6 events over {len(alpha1)} "
          f"events: {total} histories, {adm} admissible, max data {mx}")
    if mx != 1:
        failures.append(("single token max data", mx))

    # 2. Reachable states to 7 events (the artifact's horizon).
    single = reachable_states(["<>"], MAX_EVENTS)
    mx7 = max(r.n_data() for r in single)
    print(f"single token, reachable states within {MAX_EVENTS} events: "
          f"{len(single)}; max data {mx7}")
    if mx7 != 1:
        failures.append(("single token reachable", mx7))

    # 3. The bound is sharp and needs its hypothesis.
    one = step(EMPTY, AdmitDatum("<>"))
    print(f"AdmitDatum('<>') once: data = {one.data}")
    if one.n_data() != 1:
        failures.append(("sharp", one.data))
    two = step(one, AdmitDatum("<a>"))
    print(f"then AdmitDatum('<a>'): data = {two.data} (a second token)")
    if two.n_data() != 2:
        failures.append(("second token", two.data))
    occ = occurrence_step(one, AdmitDatum("<>"))
    print(f"occurrence discipline, '<>' again: data = {occ.data} "
          f"(a declared different discipline)")
    if occ.n_data() != 2:
        failures.append(("occurrence", occ.data))

    # 4. Re-supplying and re-admitting: the busy history of the Lean check.
    busy: list[Event] = [Supply("<>"), AdmitDatum("<>"), Supply("<>"),
                         AdmitDatum("<>")]
    r = EMPTY
    for e in busy:
        r = step(r, e)
    print(f"supply, admit, supply, admit of '<>': data = {r.data}")
    if r.data != ("<>",):
        failures.append(("busy", r.data))

    # 5. Agreement with the committed artifact.
    art = json.loads((ROOT / "artifacts" / "bridge.json").read_text())
    by_name = {s["scenario"]: s for s in art["scenarios"]}
    rep = scenario_report("single_dedup", ["<>"], MAX_EVENTS, False)
    for key in ("states_reached", "max_carrier"):
        print(f"single_dedup {key}: computed {rep[key]}, artifact "
              f"{by_name['single_dedup'][key]}")
        if rep[key] != by_name["single_dedup"][key]:
            failures.append(("artifact", key))
    c2 = rep["min_events_to"]["carrier_2"]
    print(f"single_dedup min events to carrier 2: {c2} (None = not reached within search horizon)")
    if c2 is not None:
        failures.append(("carrier_2", c2))
    initial_two = replay([AdmitDatum("A"), AdmitDatum("B")])
    unchanged_two = replay([], initial_two)
    if unchanged_two.n_data() != 2:
        failures.append("nonempty-base counterexample")
    print("empty history from a two-token base keeps two: the initial invariant is required")
    for name in ("two_dedup", "occurrence"):
        print(f"{name} max_carrier (artifact): {by_name[name]['max_carrier']}, "
              f"carrier 2 at {by_name[name]['min_events_to']['carrier_2']} events")
        if by_name[name]["max_carrier"] != 2:
            failures.append(("artifact", name))

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
