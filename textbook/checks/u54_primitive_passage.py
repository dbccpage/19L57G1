"""Unit 54 check: the passage from an asserted difference to a response.

Replays the arrow witnesses of `lean4/Derivation/PrimitivePassage.lean`
through Genesis's Python mirror (`code/derivation/primitive_passage.py`):
assertion is not retention, retention needs an assertion, the four
obstruction gates at the five witness states, the two obstruction
policies at a pre-observational state (the rival policy is Python
(book), written from the Lean `obstEmptyObs`), the two-rule at
`gateWitnessAll`, licensing and budget gates, the inert refusal, the
absorbing terminal, resolution by extension, the represented next
family, the three equivalence laws of the zero relation by brute force
on small observations, and the module's `arrow_report()` against
`artifacts/primitive_passage.json`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u54_primitive_passage.py
"""
from __future__ import annotations

import json
import sys
from dataclasses import replace
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.primitive_passage import (  # noqa: E402
    GENESIS_P, PS, Cols, arrow_report, col_ok, extension_proposals,
    next_family_p, obst_p, obstructed_pairs, preplay, pstep, refine_ok,
    repair_family_p, sep_col, sep_p, zero_p,
)

# The five witness states of Lean lines 425-462, field for field.
BASE = dict(occ=(0, 1), asserted=((0, 1),), wit=((0, 1),), prot=((0, 1),),
            budget=0, licensed=True, refusals=(), halted=False)
GATE_NO_ZERO = PS(obs=((0,),), **BASE)
GATE_NO_DECLARATION = PS(obs=None, **BASE)
GATE_NO_PROTECTION = replace(PS(obs=(), **BASE), prot=())
GATE_NO_RETENTION = replace(PS(obs=(), **BASE), wit=())
GATE_ALL = PS(obs=(), **BASE)


def obst_empty_obs(s: PS, i: int, j: int) -> bool:
    """Python (book): Lean's rival policy `obstEmptyObs` (line 382):
    an undeclared observation is read as the empty observation."""
    cols: Cols = () if s.obs is None else s.obs
    return (i, j) in s.wit and (i, j) in s.prot and zero_p(cols, i, j)


def gates(s: PS, i: int, j: int) -> tuple[bool, bool, bool, bool]:
    """The four gates (Lean lines 168-184): retained, protected,
    declared, zero-under-the-declared-convention (none => True)."""
    return ((i, j) in s.wit, (i, j) in s.prot, s.obs is not None,
            True if s.obs is None else zero_p(s.obs, i, j))


def main() -> int:
    failures: list[str] = []

    # --- assertion, retention, protection (Lean 692-883)
    pre_ret = preplay([("admitOcc", 7), ("admitOcc", 8), ("assertWit", 0, 1)],
                      GENESIS_P)
    print(f"after admitOcc 7, admitOcc 8, assertWit 0 1: asserted={pre_ret.asserted} "
          f"wit={pre_ret.wit} occ={pre_ret.occ}")
    if pre_ret.asserted != ((0, 1),) or pre_ret.wit != ():
        failures.append("assertion_not_retained")
    s0 = preplay([("admitOcc", 7), ("admitOcc", 8)], GENESIS_P)
    print(f"admitWit 0 1 with nothing asserted is a no-op: "
          f"{pstep(s0, ('admitWit', 0, 1)) == s0}")
    if pstep(s0, ("admitWit", 0, 1)) != s0:
        failures.append("retention_requires_assertion")
    ret = pstep(pre_ret, ("admitWit", 0, 1))
    print(f"admitWit 0 1 after the assertion: wit={ret.wit}")
    if ret.wit != ((0, 1),):
        failures.append("retention_completes")
    print(f"protect 0 1 before retention is a no-op: "
          f"{pstep(pre_ret, ('protect', 0, 1)) == pre_ret}; "
          f"after: prot={pstep(ret, ('protect', 0, 1)).prot}")
    if (pstep(pre_ret, ("protect", 0, 1)) != pre_ret
            or pstep(ret, ("protect", 0, 1)).prot != ((0, 1),)):
        failures.append("protection")
    # witness_no_protection / no_protection_no_obstruction: declared, zero,
    # retained, not protected -> not obstructed
    declared = pstep(ret, ("declareObs",))
    print(f"declared but unprotected: obs={declared.obs} prot={declared.prot} "
          f"obst={obst_p(declared, 0, 1)}")
    if declared.obs != () or obst_p(declared, 0, 1):
        failures.append("no_protection_no_obstruction")

    # --- the four gates at the five witnesses (Lean 425-575)
    print("gates (retained, protected, declared, zeroDecl) and obstP:")
    expect = {
        "NoZero": ((True, True, True, False), False),
        "NoDeclaration": ((True, True, False, True), False),
        "NoProtection": ((True, False, True, True), False),
        "NoRetention": ((False, True, True, True), False),
        "All": ((True, True, True, True), True),
    }
    for name, s in (("NoZero", GATE_NO_ZERO), ("NoDeclaration", GATE_NO_DECLARATION),
                    ("NoProtection", GATE_NO_PROTECTION),
                    ("NoRetention", GATE_NO_RETENTION), ("All", GATE_ALL)):
        g, o = gates(s, 0, 1), obst_p(s, 0, 1)
        print(f"  gateWitness{name}: {g} -> {o}")
        if (g, o) != expect[name]:
            failures.append(f"gate {name}")
    # obstP_factors: obstP == all four gates, at every witness
    for s in (GATE_NO_ZERO, GATE_NO_DECLARATION, GATE_NO_PROTECTION,
              GATE_NO_RETENTION, GATE_ALL):
        if obst_p(s, 0, 1) != all(gates(s, 0, 1)):
            failures.append("obstP_factors")

    # --- the two policies differ exactly before a declaration (Lean 382-410)
    pre = GATE_NO_DECLARATION
    print(f"preRetainedObstructed: obstEmptyObs={obst_empty_obs(pre, 0, 1)} "
          f"obstP={obst_p(pre, 0, 1)}")
    if not (obst_empty_obs(pre, 0, 1) and not obst_p(pre, 0, 1)):
        failures.append("obst_policies_differ")
    for s in (GATE_NO_ZERO, GATE_NO_PROTECTION, GATE_NO_RETENTION, GATE_ALL):
        if obst_empty_obs(s, 0, 1) != obst_p(s, 0, 1):
            failures.append("obst_policies_agree_when_declared")

    # --- the two-rule and the next family at gateWitnessAll (Lean 961-1290)
    rep = repair_family_p(GATE_ALL, 0, 1)
    ext = extension_proposals(GATE_ALL, 0, 1)
    nxt = next_family_p(GATE_ALL)
    print(f"gateWitnessAll: obstructedPairs={obstructed_pairs(GATE_ALL)} "
          f"repairFamily={rep} extensionProposals={ext}")
    print(f"  nextFamilyP={nxt}")
    expected_next = [(("setBudget", 1), ("addCol", (0,))),
                     (("setBudget", 1), ("addCol", (1,)))]
    if rep != [] or ext != [(0,), (1,)] or nxt != expected_next:
        failures.append("two_rule / nextFamilyP at gateWitnessAll")
    print(f"  both singleton columns are in range, new, and separate (0,1): "
          f"colOk {[col_ok(GATE_ALL, (p,)) for p in range(2)]}, "
          f"sepCol {[sep_col((p,), 0, 1) for p in range(2)]}; "
          f"the repair family is empty because no column exists to refine")
    if refine_ok(GATE_ALL, (), 0) or sep_p((), 0, 1):
        failures.append("repair family on the empty observation")

    # --- proposal vs execution (Lean 1098-1125, 1185-1222)
    unlicensed = replace(GATE_ALL, licensed=False, budget=5)
    funded = replace(GATE_ALL, budget=5)
    print(f"addCol [0] unlicensed (budget 5): no-op {pstep(unlicensed, ('addCol', (0,))) == unlicensed}")
    print(f"addCol [0] unfunded (licensed): no-op {pstep(GATE_ALL, ('addCol', (0,))) == GATE_ALL}")
    done = pstep(funded, ("addCol", (0,)))
    print(f"addCol [0] funded+licensed: obs={done.obs} budget={done.budget} "
          f"obst={obst_p(done, 0, 1)}")
    if (pstep(unlicensed, ("addCol", (0,))) != unlicensed
            or pstep(GATE_ALL, ("addCol", (0,))) != GATE_ALL
            or done.obs != ((0,),) or done.budget != 4 or obst_p(done, 0, 1)):
        failures.append("licence / budget / extension_resolves")
    # the represented block [setBudget 1, addCol [0]] resolves from budget 0
    blk = preplay(nxt[0], GATE_ALL)
    print(f"replay of the next-family block from gateWitnessAll: obs={blk.obs} "
          f"budget={blk.budget} obst={obst_p(blk, 0, 1)} nextFamilyP={next_family_p(blk)}")
    if blk.obs != ((0,),) or blk.budget != 0 or obst_p(blk, 0, 1) or next_family_p(blk) != []:
        failures.append("block resolves / nextFamilyP_stop")

    # --- refusal is a record (Lean 1130-1141), terminal absorbs (1148-1158)
    refused = pstep(funded, ("refuse", 0, 1))
    print(f"refuse 0 1: refusals={refused.refusals}, stores unchanged "
          f"{(refused.occ, refused.wit, refused.prot, refused.obs) == (funded.occ, funded.wit, funded.prot, funded.obs)}, "
          f"halted={refused.halted}, still obstructed={obst_p(refused, 0, 1)}")
    if (refused.refusals != ((0, 1),) or refused.halted
            or not obst_p(refused, 0, 1)
            or pstep(refused, ("refuse", 0, 1)) != refused):
        failures.append("refusal")
    print(f"refuse without a certificate (gateWitnessNoZero): no-op "
          f"{pstep(GATE_NO_ZERO, ('refuse', 0, 1)) == GATE_NO_ZERO}")
    if pstep(GATE_NO_ZERO, ("refuse", 0, 1)) != GATE_NO_ZERO:
        failures.append("refusal certificate")
    halted = pstep(funded, ("halt",))
    events = [("admitOcc", 9), ("assertWit", 0, 1), ("admitWit", 0, 1),
              ("protect", 0, 1), ("declareObs",), ("refineCol", (), 0),
              ("addCol", (1,)), ("refuse", 0, 1), ("setBudget", 3),
              ("setLicense", False), ("halt",)]
    absorbing = all(pstep(halted, e) == halted for e in events)
    print(f"halted state absorbs all {len(events)} event kinds: {absorbing}")
    if not absorbing:
        failures.append("terminal_absorbing")

    # --- determinism: replay is a function, so equal histories give equal states
    h = [("admitOcc", 7), ("admitOcc", 8), ("assertWit", 0, 1), ("admitWit", 0, 1),
         ("protect", 0, 1), ("declareObs",), ("setBudget", 1), ("addCol", (0,))]
    a, b = preplay(h, GENESIS_P), preplay(h, GENESIS_P)
    print(f"the same history replayed twice gives the same state: {a == b}; "
          f"final obs={a.obs} obst={obst_p(a, 0, 1)}")
    if a != b or a.obs != ((0,),):
        failures.append("replay_deterministic")

    # --- zero is an equivalence (Lean 907-953): brute force, cols over {0,1,2}
    pts = (0, 1, 2)
    subsets = [tuple(p for p in pts if m >> p & 1) for m in range(8)]
    checked = 0
    for k in range(3):
        for cols in product(subsets, repeat=k):
            for i, j, l in product(pts, repeat=3):
                z = zero_p(cols, i, j)
                if not zero_p(cols, i, i):
                    failures.append("zero_refl")
                if z != zero_p(cols, j, i):
                    failures.append("zero_symm")
                if z and zero_p(cols, j, l) and not zero_p(cols, i, l):
                    failures.append("zero_trans")
                checked += 1
    print(f"zero_refl/symm/trans checked on {checked} (cols, i, j, l) cases "
          f"(up to 2 columns over 3 points)")

    # --- the arrow report against the artifact
    art = json.loads((ROOT / "artifacts" / "primitive_passage.json").read_text())
    rep_now = arrow_report()
    print(f"arrow_report(): {sum(rep_now.values())}/{len(rep_now)} true; "
          f"matches artifact arrows: {rep_now == art['arrows']}")
    if rep_now != art["arrows"] or not all(rep_now.values()):
        failures.append("arrow_report vs artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
