import Lake
open Lake DSL

package convention_price

/-
Self-contained: core Lean only.  This package imports no sealed module
and declares no dependency; every theorem here is on this tree's own
abstract two-label parity model.
-/
@[default_target]
lean_lib ConventionPrice where
  roots := #[`ConventionPrice, `ConventionPrice.AxiomReport]
