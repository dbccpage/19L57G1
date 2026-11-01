"""Unit 16 check: uncollapse, recollapse, and families of regimes.

Checks:
  1. `research/uncollapse/model.py` declared-module/import parity (`consumed_modules`
     vs `lean_imports`);
  2. `bridge_checks` and `recollapse_witness` from `two_theorems/model.py`
     (`recollapse_changes_views`, `separable_unadmitted`);
  3. Separation comparisons on manually constructed endpoints from
     `ResearchUncollapse.lean`, not executions of applyDelta/validResponse
     (the four-field Regime mirror has no requirements):
     `uncollapse_by_delta`, `mention_not_sufficient`, `recollapse_by_rule`,
     `recollapse_by_instance`, `recollapse_breaks_requirement`,
     `family_index_dependence`, and `family_index_repaired`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i16_uncollapse.py
"""
from __future__ import annotations

import sys
from pathlib import Path

TWO_THEOREMS = Path(__file__).resolve().parents[3] / "research" / "two_theorems"
UNCOLLAPSE = Path(__file__).resolve().parents[3] / "research" / "uncollapse"


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


def main() -> int:
    unc_model = load_module_from(UNCOLLAPSE)
    expected_imports = set(unc_model.consumed_modules()) | {"Ignition"}
    actual_imports = set(unc_model.lean_imports())
    imports_ok = expected_imports == actual_imports
    print(f"uncollapse Lean imports match pinned modules: {imports_ok} ({sorted(actual_imports)})")

    tt_model = load_module_from(TWO_THEOREMS)
    Regime = tt_model.Regime
    separable = tt_model.separable

    bridge = tt_model.bridge_checks([
        tt_model.R0,
        tt_model.R0_RULE,
        tt_model.R0_BOTH,
        tt_model.R_BINARY,
        tt_model.R_RULE_ONLY,
    ])
    recol = tt_model.recollapse_witness()
    print(f"two_theorems bridge_checks: {bridge}")
    print(f"two_theorems recollapse_witness: {recol}")

    R2L = Regime(2, (), (), ())
    U0 = Regime(2, (1,), ((0, (0,)),), ())
    Rall = Regime(2, (1,), (), (0,))
    Rall0 = Regime(2, (1,), ((0, (0,)),), (0,))
    U0rule = Regime(2, (1,), ((0, (0,)),), (0,))
    U0both = Regime(2, (1,), ((0, (0,)), (0, (1,))), ())
    U0new = Regime(3, (1,), ((0, (0,)), (0, (1,))), ())
    A3 = Regime(3, (1,), ((0, (0,)),), ())
    B3 = Regime(3, (1,), ((0, (1,)),), ())

    swap01 = lambda n: 1 if n == 0 else (0 if n == 1 else n)

    u1_ok = (not separable(R2L, 0, 1)) and separable(U0, 0, 1)
    u3_ok = (not separable(Rall, 0, 1)) and (not separable(Rall0, 0, 1))
    u4_ok = separable(U0, 0, 1) and (not separable(U0rule, 0, 1)) and (not separable(U0both, 0, 1))
    u6_ok = separable(U0new, 1, 2) and (not separable(U0new, 0, 1))
    u9_ok = (not separable(A3, 1, 2)) and separable(B3, 1, 2) and (not separable(B3, swap01(1), swap01(2)))
    u10_ok = (not separable(A3, 1, 2)) and (not separable(B3, swap01(1), swap01(2)))
    print(
        f"witnesses U1={u1_ok}, U3={u3_ok}, U4={u4_ok}, U6={u6_ok}, U9={u9_ok}, U10={u10_ok}"
    )

    ok = (
        imports_ok
        and bridge["mismatch"] == 0
        and bridge["bound_violation"] == 0
        and bridge["unadmitted_in_no_view"] is True
        and bridge["unadmitted_separated_from_0"] is True
        and recol["separable_before"] is True
        and recol["separable_after"] is False
        and recol["lost_views"] == [[0]]
        and u1_ok
        and u3_ok
        and u4_ok
        and u6_ok
        and u9_ok
        and u10_ok
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
