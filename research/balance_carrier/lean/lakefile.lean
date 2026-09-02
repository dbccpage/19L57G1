import Lake
open Lake DSL

package balance_carrier

/-
Self-contained: core Lean only.  This package imports no sealed module
and declares no dependency.  The pinned receiver and balance definitions
are reconstructed verbatim in `BalanceCarrier/Receiver.lean` and
`BalanceCarrier/Balance.lean`, each with a pin note; every theorem
originating here is in `LayerObserver.lean` and `WalkCarrier.lean`.
-/
@[default_target]
lean_lib BalanceCarrier where
  roots := #[`BalanceCarrier, `BalanceCarrier.AxiomReport]
