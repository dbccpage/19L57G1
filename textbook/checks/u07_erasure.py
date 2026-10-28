"""Unit 07 check: token erasure, the Python side.

Genesis's Python keeps tokens and dedups on them; Lean's Regime keeps a
count. The proof that the two agree is Erasure.erase_replay (Lean). This
script runs the Python half: erasing a history (turning each duplicate
admission into a supply) never changes the replay, and the data count is
the number of distinct admitted tokens. Sample computation.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u07_erasure.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from derivation.engine import GENESIS_F, GENESIS_L  # noqa: E402
from derivation.model import (  # noqa: E402
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    Event,
    Impose,
    Supply,
    replay,
)

TOKENS = ("<>", "<a>", "<ab>")


def erase_history(h: list[Event]) -> list[Event]:
    """Gloss of Erasure.eraseHistory: a duplicate admission becomes a
    supply; everything else is kept. Threads the admitted tokens."""
    seen: set[str] = set()
    out: list[Event] = []
    for e in h:
        if isinstance(e, AdmitDatum):
            if e.token in seen:
                out.append(Supply(e.token))
            else:
                seen.add(e.token)
                out.append(e)
        else:
            out.append(e)
    return out


def main() -> int:
    failures: list[object] = []
    atoms: list[Event] = [AdmitDatum(t) for t in TOKENS] + [Supply("<a>"), AdmitForm(1)]
    cases = 0
    for k in range(5):
        for seq in itertools.product(atoms, repeat=k):
            h = list(seq)
            cases += 1
            try:
                r = replay(h)
            except Exception:
                continue
            er = erase_history(h)
            if replay(er) != r:
                failures.append(("erased replay differs", h))
            distinct = {e.token for e in h if isinstance(e, AdmitDatum)}
            if len(r.data) != len(distinct):
                failures.append(("count", h, r.data))
            dups = sum(isinstance(e, AdmitDatum) for e in h) - len(distinct)
            if sum(isinstance(e, Supply) for e in er) != sum(isinstance(e, Supply) for e in h) + dups:
                failures.append(("supply count", h))
    print(f"histories of up to 4 events over 5 atoms: {cases}; erased replay == replay: checked")

    # Genesis's two histories: no duplicate admission, so erasure is the identity.
    for name, g in (("GENESIS_L", GENESIS_L), ("GENESIS_F", GENESIS_F)):
        same = erase_history(list(g)) == list(g)
        print(f"{name}: erasure is the identity: {same}; data count {len(replay(g).data)}")
        if not same:
            failures.append(name)

    # A history with a duplicate and later structure: the duplicate is the
    # only thing erasure touches, and the later structure is unaffected.
    h = [AdmitDatum("<a>"), AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(1),
         AdmitInst(0, (0,)), Impose(0, 1)]
    er = erase_history(h)
    print(f"erased: {[type(e).__name__ + ('(' + e.token + ')' if isinstance(e, (Supply, AdmitDatum)) else '') for e in er]}")
    if replay(h) != replay(er) or not isinstance(er[1], Supply):
        failures.append("dup with structure")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
