"""Unit 13 check: two data come only from two different tokens.

Runs Genesis's own Python model over every history of at most five events
drawn from a two-token alphabet. This is sample computation, not a proof;
the proof is Bridge.second_token_required. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u13_second_token.py
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.bridge import event_alphabet, scenario_report  # noqa: E402
from derivation.model import AdmissionError, AdmitDatum, Regime, step  # noqa: E402

EMPTY = Regime((), (), frozenset(), frozenset(), frozenset())


def main() -> int:
    failures: list[object] = []
    alpha = event_alphabet(["<>", "<a>"], 2)
    total = admissible = two = 0
    min_len_two: int | None = None
    for k in range(6):
        for seq in itertools.product(alpha, repeat=k):
            total += 1
            r = EMPTY
            try:
                for e in seq:
                    r = step(r, e)
            except AdmissionError:
                continue
            admissible += 1
            if r.n_data() >= 2:
                two += 1
                min_len_two = k if min_len_two is None else min(min_len_two, k)
                admitted = [e.token for e in seq if isinstance(e, AdmitDatum)]
                # The theorem, for every choice of t0: some admission has
                # a token other than t0.
                for t0 in ("<>", "<a>", "zz"):
                    if not any(tok != t0 for tok in admitted):
                        failures.append(("no other token", seq, t0))
                if len(set(admitted)) < 2:
                    failures.append(("fewer than two tokens", seq))
    print(f"two-token alphabet ({len(alpha)} events), histories of at most "
          f"5 events: {total}; admissible {admissible}; reaching two data "
          f"{two}; shortest {min_len_two} events")
    print(f"every two-data history admits two different tokens: "
          f"{not any(f[0] == 'fewer than two tokens' for f in failures)}")
    if min_len_two != 2:
        failures.append(("shortest", min_len_two))

    rep = scenario_report("two_dedup", ["<>", "<a>"], 7, False)
    art = json.loads((ROOT / "artifacts" / "bridge.json").read_text())
    by_name = {s["scenario"]: s for s in art["scenarios"]}
    c2 = rep["min_events_to"]["carrier_2"]
    print(f"two_dedup: states {rep['states_reached']} (artifact "
          f"{by_name['two_dedup']['states_reached']}), max carrier "
          f"{rep['max_carrier']}, carrier 2 at {c2} events (artifact "
          f"{by_name['two_dedup']['min_events_to']['carrier_2']})")
    if rep["states_reached"] != by_name["two_dedup"]["states_reached"] or c2 != 2:
        failures.append("artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
