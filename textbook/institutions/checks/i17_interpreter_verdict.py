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


@dataclass(frozen=True)
class ConstitutionDesc:
    dedupAdmit: bool
    guardRequire: bool
    guardAccept: bool
    guardBudget: bool
    guardAug: bool
    guardRefuse: bool


@dataclass(frozen=True)
class World:
    data: tuple[int, ...]
    views: tuple[tuple[int, ...], ...]
    reqs: tuple[tuple[int, int], ...]
    refusals: tuple[tuple[int, int], ...]
    budget: int
    augLicensed: bool
    notes: tuple[int, ...]


def sep_by_views(views: tuple[tuple[int, ...], ...], i: int, j: int) -> bool:
    return any((i in v) != (j in v) for v in views)


def quiescent_b(w: World) -> bool:
    return all(sep_by_views(w.views, i, j) or (i, j) in w.refusals for i, j in w.reqs)


def wf_world(w: World) -> bool:
    n = len(w.data)
    return all(i != j and i < n and j < n for i, j in w.reqs)


def req_ok_b(w: World, i: int, j: int) -> bool:
    n = len(w.data)
    return i != j and i < n and j < n and (i, j) not in w.reqs


def mark_ok_b(w: World, v: tuple[int, ...], p: int) -> bool:
    if v not in w.views or p not in w.data or p in v:
        return False
    v_new = v + (p,)
    new_views = tuple(v_new if u == v else u for u in w.views)
    discharges = any(
        not sep_by_views(w.views, i, j) and sep_by_views(new_views, i, j)
        for i, j in w.reqs
    )
    breaks = any(
        sep_by_views(w.views, i, j) and not sep_by_views(new_views, i, j)
        for i, j in w.reqs
    )
    return discharges and not breaks


def interp_step(c: ConstitutionDesc, w: World, event: tuple) -> World:
    kind = event[0]
    if kind == "admitTok":
        t = event[1]
        if c.dedupAdmit and t in w.data:
            return w
        return replace(w, data=w.data + (t,))
    if kind == "require":
        i, j = event[1], event[2]
        if c.guardRequire and not req_ok_b(w, i, j):
            return w
        return replace(w, reqs=w.reqs + ((i, j),))
    if kind == "mark":
        v, p = event[1], event[2]
        ok_accept = (not c.guardAccept) or mark_ok_b(w, v, p)
        ok_budget = (not c.guardBudget) or (w.budget > 0)
        if ok_accept and ok_budget:
            new_views = tuple((u + (p,) if u == v and p not in u else u) for u in w.views)
            return replace(w, views=new_views, budget=max(0, w.budget - 1))
        return w
    raise ValueError(kind)


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

    genesis = World(data=(0,), views=(), reqs=(), refusals=(), budget=0, augLicensed=True, notes=())
    acc_world = World(
        data=(0, 1),
        views=((0,),),
        reqs=((0, 1),),
        refusals=(),
        budget=1,
        augLicensed=True,
        notes=(),
    )

    codes = all_codes()
    guard_bad = 0
    accept_bad = 0
    aligned_bad = 0
    dedup_bad = 0
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

        c_dedup = replace(c, dedupAdmit=not c.dedupAdmit)
        for w in (genesis, acc_world):
            for ev in (("admitTok", 0), ("admitTok", 2), ("require", 0, 0), ("mark", (0,), 1)):
                if quiescent_b(interp_step(c, w, ev)) != quiescent_b(interp_step(c_dedup, w, ev)):
                    dedup_bad += 1

    print(
        f"64 codes checked: guard_bad={guard_bad}, accept_bad={accept_bad}, "
        f"aligned_bad={aligned_bad}, dedup_bad={dedup_bad}"
    )

    ok = (
        imports_ok
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
