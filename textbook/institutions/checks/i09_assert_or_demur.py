"""Unit 09 check: assert or demur, residuals, and the demurred claim.

Checks:
  1. `demurred_check(3)` from `actor_institution/model.py`: `demurred` is always
     known and is total iff the claim is known;
  2. `residual_answerable` and `evidence_is_not_a_digest` on `residuals_parity_half`;
  3. `residual_checks` and `grounding_checks` from `two_theorems/model.py`.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i09_assert_or_demur.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import _tree  # noqa: F401
from model import HALF4, PARITY4, demurred_check, examples, residuals, sig  # noqa: E402

TWO_THEOREMS = Path(__file__).resolve().parents[3] / "research" / "two_theorems"


def load_two_theorems_model():
    saved = sys.modules.get("model")
    sys.path.insert(0, str(TWO_THEOREMS))
    try:
        del sys.modules["model"]
        import model as tt_model  # type: ignore[no-redef]
        return tt_model
    finally:
        sys.path.pop(0)
        if saved is not None:
            sys.modules["model"] = saved


def main() -> int:
    dem = demurred_check(3)
    print(f"demurred_check(3): {dem}")

    res_ph = examples()["residuals_parity_half"]
    x0, y0 = res_ph[0]
    ind = tuple(1 if z == x0 else 0 for z in range(4))
    res_after = residuals(4, (PARITY4, ind), HALF4)
    same_sig_on_residual = sig((PARITY4,), x0) == sig((PARITY4,), y0)
    print(f"residuals(PARITY4, HALF4): {res_ph}; (x0, y0) removed by indicator: {(x0, y0) not in res_after}")

    tt_model = load_two_theorems_model()
    D4 = (0, 1, 2, 3)
    pool4 = [
        tt_model.Table({x: x % 2 for x in D4}),
        tt_model.Table({x: x // 2 for x in D4}),
        tt_model.Table({x: (x == 1) * 1 for x in D4}),
        tt_model.Table({x: 0 for x in D4}),
    ]
    D3 = (0, 1, 2)
    pool3 = [
        tt_model.Table({x: x % 2 for x in D3}),
        tt_model.Table({x: x // 2 for x in D3}),
        tt_model.Table({x: (x == 1) * 1 for x in D3}),
        tt_model.Table({x: 0 for x in D3}),
    ]
    rc = tt_model.residual_checks(D4, pool4, 2)
    gc = tt_model.grounding_checks(D3, pool3, 2)
    print(f"two_theorems residual_checks(D4): {rc}")
    print(f"two_theorems grounding_checks(D3): {gc}")

    ok = (
        dem["checked"] == 160
        and dem["violations"] == 0
        and len(res_ph) == 4
        and (x0, y0) not in res_after
        and sorted(res_after) == [(1, 3), (3, 1)]
        and same_sig_on_residual is True
        and rc["nil_iff_violations"] == 0
        and rc["antitone_violations"] == 0
        and gc["silence_grounded"] is True
        and gc["self_report_grounded"] is True
        and gc["members_grounded"] is True
        and gc["mono_violations"] == 0
        and gc["carrier_violations"] == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
