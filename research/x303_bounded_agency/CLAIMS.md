# Claims: Target X303

## What it supports

1. A discrete viability envelope over x301 `RelationalModel` with exact
   `Fraction` margins.
2. FIFO memory of declared horizon.
3. `AgentController.step` refuses without mutating `self.state` object
   identity on fuel, empty pool, viability, authorization, and unlicensed apply.
4. Licensed apply checks the projected `CanonKey` before returning the
   projected model. Default authorizer allows every viable non-firewall
   evaluation; that is an explicit policy, not a committee.

## What it does not support

1. It does not import `research.alpha_engine`. `ActionProposal` is
   supply-shaped recording only.
2. Lean theorems are about a Nat carrier and a closed `Action` inductive.
3. `has_empirical_reference` is recorded; it is not a refusal gate.

## Narrowest defensible claim

Under the declared envelope and a license whose authorized keys include the
projected canonical key, `LicensedDriver.apply_licensed` returns that
projection; without such a key it raises `UnlicensedActionError`.
