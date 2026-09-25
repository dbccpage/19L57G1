import Lake
open Lake DSL

package second_profile

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice and the sealed isomorphism
structure are reconstructed verbatim in `SecondProfile/Kernel.lean` and
`SecondProfile/IsoKernel.lean`, with a pin note each; every theorem
originating in this rung is in `SecondProfile/Carry.lean`,
`SecondProfile/Classes.lean`, `SecondProfile/Stage.lean` and
`SecondProfile/Keep.lean`.
-/
@[default_target]
lean_lib SecondProfile where
  roots := #[`SecondProfile, `SecondProfile.AxiomReport]
