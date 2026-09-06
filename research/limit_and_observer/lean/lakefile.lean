import Lake
open Lake DSL

package limit_observer

/-
Core Lean only.  No Mathlib, no path dependency on `../../../lean4`, and no
import of `Derivation`: every theorem below is about this rung's own objects.
Sealed results are CITED in the prose by pinned path, never imported.
-/

@[default_target]
lean_lib LimitObserver where
  roots := #[`LimitObserver, `LimitObserver.AxiomReport]
