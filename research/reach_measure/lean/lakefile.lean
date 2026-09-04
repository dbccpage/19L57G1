import Lake
open Lake DSL

package reach_measure

/-
Self-contained: core Lean only.  No sealed module is imported; the sealed
item grammar and the two sealed measures are restated here in miniature,
because the result is about the FORM of a base-free measure and needs no
reconstruction of the enumerators.
-/
@[default_target]
lean_lib ReachMeasure where
  roots := #[`ReachMeasure, `ReachMeasure.AxiomReport]
