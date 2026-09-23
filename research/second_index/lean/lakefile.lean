import Lake
open Lake DSL

package second_index

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice is reconstructed verbatim in
`SecondIndex/Kernel.lean` and the previous rung's stake and inertia slice
in `SecondIndex/Inherited.lean`, each with a pin note; every theorem
originating in this rung is in `SecondIndex/Index.lean` and
`SecondIndex/Countermodel.lean`.
-/
@[default_target]
lean_lib SecondIndex where
  roots := #[`SecondIndex, `SecondIndex.AxiomReport]
