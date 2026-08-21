import Lake
open Lake DSL

package primitive_difference_tower

require derivation from "../../../lean4"

@[default_target]
lean_lib PrimitiveDifferenceTower where
  roots := #[`PrimitiveDifferenceTower, `PrimitiveDifferenceTower.AxiomReport]
