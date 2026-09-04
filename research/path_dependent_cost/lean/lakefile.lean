import Lake
open Lake DSL

package path_dependent_cost

/-
Self-contained: core Lean only.  This package imports no sealed module and
reconstructs none.  Every statement is about an abstract state, an abstract
one-item action and an abstract weighting; the sealed grammar supplies one
instance and `movegraph.py` checks it over a declared rectangle.
-/
@[default_target]
lean_lib PathDependentCost where
  roots := #[`PathDependentCost, `PathDependentCost.AxiomReport]
