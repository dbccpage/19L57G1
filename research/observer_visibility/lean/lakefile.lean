import Lake
open Lake DSL

package observer_visibility

/-
Sealed import closure of `Derivation.PresentationNaturality` is staged into
`sealed/` by verify_lean.py (gitignored) for pin and write-root binding.
Native observer-visibility mathematics is defined in this package and does
not import Derivation.  Those modules are not a Lake target.  No path
dependency on `../../../lean4`.
-/

@[default_target]
lean_lib ObserverVisibility where
  roots := #[`ObserverVisibility, `ObserverVisibility.AxiomReport]
