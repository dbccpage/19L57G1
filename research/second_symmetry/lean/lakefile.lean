import Lake
open Lake DSL

package second_symmetry

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice is reconstructed verbatim in
`SecondSymmetry/Kernel.lean` and the sealed isomorphism structure in
`SecondSymmetry/IsoKernel.lean`, each with a pin note; every theorem
originating in this rung is in `SecondSymmetry/Aut.lean`,
`SecondSymmetry/Meet.lean`, `SecondSymmetry/Grow.lean` and
`SecondSymmetry/Witness.lean`.
-/
@[default_target]
lean_lib SecondSymmetry where
  roots := #[`SecondSymmetry, `SecondSymmetry.AxiomReport]
