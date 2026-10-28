"""Unit 53 check: the fixed interface, re-read from the artifact and recomputed.

Reads `artifacts/primitive_contact.json` and compares its status, history
and verdict with the constants of Genesis's `code/run_primitive_contact.py`
and with Lean's declared strings; evaluates the native kernel witness
through Genesis's `primitive_core.evaluate` (it is reading A, and the
matrix gives what A brings); re-runs Genesis's enumeration of Bool-valued
observers (E1: no observer's zero-complement is the oriented witness);
and, as Python (book), shows the reason on every carrier of at most three
points: the complement of an equivalence is symmetric, and the oriented
witness is not. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u53_primitive_contact.py
"""
from __future__ import annotations

import json
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

import run_primitive_contact as RPC  # noqa: E402
from derivation import primitive_core as P  # noqa: E402

LEAN_STATUS = "CONTACT_INPUT_ABSENT"                 # contactStatus (sealed, superseded)
LEAN_CURRENT = "CONTACT_PROCESSED_LEAN_ONLY"         # contactStatusCurrent
LEAN_VERDICT = "CONTACT_INCOMPARABLE_WITH_COUNTERMODELS"
LEAN_HISTORY = ["CONTACT_INPUT_ABSENT (pre-contact, blind-native-base ccd3a53)",
                "CONTACT_PROCESSED_LEAN_ONLY (2026-08-13, base a5caee2)"]


def equivalences(n: int) -> list[frozenset[tuple[int, int]]]:
    """Every reflexive, symmetric, transitive relation on range(n)."""
    pairs = [(x, y) for x in range(n) for y in range(n)]
    out = []
    for mask in range(1 << len(pairs)):
        r = frozenset(p for k, p in enumerate(pairs) if mask >> k & 1)
        if all((x, x) in r for x in range(n)) \
                and all((y, x) in r for (x, y) in r) \
                and all((x, w) in r for (x, y) in r for (y2, w) in r if y == y2):
            out.append(r)
    return out


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "primitive_contact.json").read_text())
    print(f"artifact status {art['status']!r}; Lean contactStatusCurrent {LEAN_CURRENT!r}; "
          f"Python STATUS_PROCESSED {RPC.STATUS_PROCESSED!r}")
    print(f"history ({len(art['history'])} entries): {art['history']}")
    print(f"  equals Lean contactStatusHistory: {art['history'] == LEAN_HISTORY}; "
          f"equals Python STATUS_HISTORY: {art['history'] == RPC.STATUS_HISTORY}; "
          f"first entry carries the sealed terminal {LEAN_STATUS!r}: "
          f"{art['history'][0].startswith(LEAN_STATUS)}")
    print(f"verdict primary: {art['verdict'].get('primary', art['verdict'].get('verdict'))!r}; "
          f"Lean contactVerdictPrimary {LEAN_VERDICT!r}; Python {RPC.VERDICT_PRIMARY!r}")
    if art["status"] != LEAN_CURRENT or art["history"] != LEAN_HISTORY \
            or RPC.STATUS_HISTORY != LEAN_HISTORY or RPC.VERDICT_PRIMARY != LEAN_VERDICT:
        failures.append("status constants")
    print(f"prose stage: {art['prose_status']}; package present {art['package_present']}, "
          f"manifest present {art['manifest_present']}")

    iface = art["native_kernel_interface"]
    print("the interface block:")
    for k, v in iface.items():
        print(f"  {k}: {v}")
    if iface["lean_binding"] != "PrimitiveContact.NativeKernel" \
            or iface["witness"] != "PrimitiveContact.nativeKernelWitness":
        failures.append("interface names")

    # the witness, read through Unit 51's evaluator
    witness = P.Setting(2, frozenset({(0, 1)}), 0, 1, frozenset(), frozenset(), frozenset())
    ev = P.evaluate(witness)
    print(f"nativeKernelWitness as a Setting: {ev}")
    print(f"  reading A holds: {ev['A']}; what A brings (matrix row A): "
          f"{[q for q in P.CANDIDATES if P.EXPECTED_MATRIX.get(f'A->{q}') == 'IMPLIES']}"
          f" implied, {[q for q in P.CANDIDATES if P.EXPECTED_MATRIX.get(f'A->{q}') == 'OPEN_LOCATED']} open")
    if not ev["A"]:
        failures.append("witness A")

    # E1: Genesis's own enumeration, re-run
    e1 = RPC.enum_bool_observers()
    print(f"E1 Bool observers re-run: {e1}; equals artifact: "
          f"{e1 == art['enumerations']['E1_bool_observers']}")
    if e1 != art["enumerations"]["E1_bool_observers"] or e1["oriented_complement_observers"] != 0:
        failures.append("E1")

    # Python (book): why — complements of equivalences are symmetric
    d2 = frozenset({(0, 1)})
    for n in range(1, 4):
        eqs = equivalences(n)
        comps = [frozenset((x, y) for x in range(n) for y in range(n) if (x, y) not in r) for r in eqs]
        sym = all(all((y, x) in c for (x, y) in c) for c in comps)
        irr = all(all((x, x) not in c for x in range(n)) for c in comps)
        print(f"  {n} points: {len(eqs)} equivalences; every complement symmetric {sym}, "
              f"irreflexive {irr}; the oriented witness among them: {d2 in comps}")
        if not (sym and irr) or d2 in comps:
            failures.append(f"complement {n}")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
