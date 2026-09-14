import Lake
open Lake DSL

package iso_sound_lean

@[default_target]
lean_lib IsoSoundLean where
  roots := #[
    `Permutation,
    `RegimeAction,
    `CanonicalMinimizer,
    `Inventory
  ]
