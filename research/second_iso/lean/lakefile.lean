import Lake
open Lake DSL

package second_iso

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice is reconstructed verbatim in
`SecondIso/Kernel.lean`, the sealed isomorphism and collapse transport in
`SecondIso/IsoKernel.lean`, the track-one sibling's stake and demand
slice in `SecondIso/Inherited.lean`, and rung three's prefix reading and
first count in `SecondIso/IndexSlice.lean`, each with a pin note; every
theorem originating in this rung is in `SecondIso/Transport.lean`,
`SecondIso/Trajectory.lean`, `SecondIso/Check.lean` and
`SecondIso/Countermodel.lean`.
-/
@[default_target]
lean_lib SecondIso where
  roots := #[`SecondIso, `SecondIso.AxiomReport]
