import Lake
open Lake DSL

package second_response

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice and the sealed isomorphism
structure are reconstructed verbatim in `SecondResponse/Kernel.lean` and
`SecondResponse/IsoKernel.lean`, with a pin note each; every theorem
originating in this rung, or restated from an earlier rung, is in
`SecondResponse/Carry.lean`, `SecondResponse/Exhaust.lean`,
`SecondResponse/ExhaustStep.lean` and `SecondResponse/Move.lean`.
-/
@[default_target]
lean_lib SecondResponse where
  roots := #[`SecondResponse, `SecondResponse.AxiomReport]
