import Lake
open Lake DSL

package second_class

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice and the sealed isomorphism
structure are reconstructed verbatim in `SecondClass/Kernel.lean` and
`SecondClass/IsoKernel.lean`, with a pin note each; every theorem
originating in this rung is in `SecondClass/Rounds.lean`,
`SecondClass/Count.lean`, `SecondClass/Clean.lean`,
`SecondClass/Recur.lean` and `SecondClass/Counter.lean`.
-/
@[default_target]
lean_lib SecondClass where
  roots := #[`SecondClass, `SecondClass.AxiomReport]
