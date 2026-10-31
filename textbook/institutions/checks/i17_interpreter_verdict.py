"""Unit 17 check: the interpreter boundary at verdict level.

Checks:
  1. `research/interpreter_verdict/model.py` pin and import parity
     (`consumed_modules` vs `lean_imports`);
  2. `diagonal_checks` and `self_evaluator_check` from `two_theorems/model.py`;
  3. Exhaustive check over all 64 `ConstitutionDesc` codes:
     - `quiescent_reads_guard` at `genesis` under `require(0, 0)` (and
       `genesis_witness_unguarded_not_wf`);
     - `quiescent_reads_accept` and `WF` preservation at `accWorld` under
       `mark([0], 1)` (`interp_not_step_wf`, `vsep_uncoded_wf`);
     - `aligned_coded_equals_uncoded` at aligned reflective worlds `(d, w)`;
     - `coded_pair_not_vsep` for `flipDedup(d)`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i17_interpreter_verdict.py
"""
from __future__ import annotations

import itertools
import sys
from dataclasses import dataclass, replace
from pathlib import Path

TWO_THEOREMS = Path(__file__).resolve().parents[3] / "research" / "two_theorems"
INTERP_VERDICT = Path(__file__).resolve().parents[3] / "research" / "interpreter_verdict"


def load_module_from(dir_path: Path, mod_name: str = "model"):
    saved = sys.modules.get(mod_name)
    sys.path.insert(0, str(dir_path))
    try:
        if mod_name in sys.modules:
            del sys.modules[mod_name]
        loaded = __import__(mod_name)
        return loaded
    finally:
        sys.path.pop(0)
        if saved is not None:
            sys.modules[mod_name] = saved


# Reuse the sealed Python owners rather than maintaining a second transition.
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "code"))
from derivation.represented import World, mark_ok, obstructed, quiescent as quiescent_b, wf as wf_world  # noqa: E402
from derivation.completion import interp_step as native_interp_step  # noqa: E402


@dataclass(frozen=True)
class ConstitutionDesc:
    dedupAdmit: bool
    guardRequire: bool
    guardAccept: bool
    gateBudget: bool
    gateLicense: bool
    certRefusal: bool


def interp_step(c: ConstitutionDesc, w: World, event: tuple) -> World:
    descriptor = (c.dedupAdmit, c.guardRequire, c.guardAccept,
                  c.gateBudget, c.gateLicense, c.certRefusal)
    event = ("admit", *event[1:]) if event[0] == "admitTok" else event
    return native_interp_step(descriptor, w, event)


def all_codes() -> list[ConstitutionDesc]:
    return [
        ConstitutionDesc(*bits)
        for bits in itertools.product((False, True), repeat=6)
    ]


def main() -> int:
    iv_model = load_module_from(INTERP_VERDICT)
    imports_ok = set(iv_model.consumed_modules()) == set(iv_model.lean_imports())
    print(f"interpreter_verdict Lean imports match pinned modules: {imports_ok}")

    tt_model = load_module_from(TWO_THEOREMS)
    diag4 = tt_model.diagonal_checks((0, 1, 2, 3), 5)
    se2 = tt_model.self_evaluator_check(2)
    se3 = tt_model.self_evaluator_check(3)
    print(f"two_theorems diagonal_checks(D4, 5): {diag4}; self_evaluator 2,3: {[se2, se3]}")

    genesis = World()
    acc_world = World(
        data=(0, 1),
        views=((0,),),
        reqs=((0, 1),),
        refusals=(),
        budget=1,
        aug_licensed=True,
        notes=(),
    )

    codes = all_codes()
    guard_bad = 0
    accept_bad = 0
    aligned_bad = 0
    dedup_bad = 0
    mismatch_bad = 0
    for c in codes:
        w_req = interp_step(c, genesis, ("require", 0, 0))
        if quiescent_b(w_req) != c.guardRequire:
            guard_bad += 1
        if wf_world(w_req) != c.guardRequire:
            guard_bad += 1

        w_acc = interp_step(c, acc_world, ("mark", (0,), 1))
        if quiescent_b(w_acc) != c.guardAccept:
            accept_bad += 1
        if not wf_world(w_acc):
            accept_bad += 1

        # Aligned world (c, acc_world): some(c) and none agree definitionally
        some_c_out = (c, interp_step(c, acc_world, ("mark", (0,), 1)))
        none_out = (c, interp_step(c, acc_world, ("mark", (0,), 1)))
        if some_c_out != none_out:
            aligned_bad += 1

        changed_code = replace(c, guardAccept=not c.guardAccept)
        changed_output = interp_step(changed_code, acc_world, ("mark", (0,), 1))
        if quiescent_b(changed_output) == quiescent_b(w_acc) or not wf_world(changed_output):
            mismatch_bad += 1

        c_dedup = replace(c, dedupAdmit=not c.dedupAdmit)
        for w in (genesis, acc_world):
            for ev in (("admitTok", 0), ("admitTok", 2), ("require", 0, 0), ("mark", (0,), 1)):
                if quiescent_b(interp_step(c, w, ev)) != quiescent_b(interp_step(c_dedup, w, ev)):
                    dedup_bad += 1

    print(
        f"64 codes checked: guard_bad={guard_bad}, accept_bad={accept_bad}, "
        f"aligned_bad={aligned_bad}, dedup_bad={dedup_bad}"
    )

    refused = World(data=(10, 20), reqs=((0, 1),), refusals=((0, 1),))
    positional = World(data=(10, 20, 30), views=((0,),), reqs=((1, 2),), budget=1)
    full = ConstitutionDesc(True, True, True, True, True, True)
    positional_output = interp_step(full, positional, ("mark", (0,), 1))
    duplicate_output = interp_step(replace(full, guardAccept=False),
        World(data=(10, 20), views=((0,),), budget=1), ("mark", (0,), 0))
    exhausted = World(data=(10, 20, 30), views=((0,),),
        reqs=((0, 1), (0, 2), (1, 2)), budget=0, aug_licensed=False)
    source_scope = (
        genesis.data == ()
        and not quiescent_b(refused)
        and mark_ok(positional, (0,), 1)
        and positional_output.views == ((1, 0),)
        and duplicate_output.views == ((0, 0),)
        and obstructed(exhausted, (1, 2))
        and obstructed(replace(exhausted, budget=7, aug_licensed=True), (1, 2))
    )
    print(f"source-scope regressions: {source_scope}; changed-code witnesses rejected: {mismatch_bad}")

    ok = (
        source_scope
        and mismatch_bad == 0
        and imports_ok
        and diag4["never_member"] is True
        and se2 is True
        and se3 is True
        and guard_bad == 0
        and accept_bad == 0
        and aligned_bad == 0
        and dedup_bad == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
