import Lake
open Lake DSL

package s9_obligations

require derivation from "../../../lean4"

@[default_target]
lean_lib S9Obligations where
  roots := #[`S9Obligations, `S9Obligations.AxiomReport]
