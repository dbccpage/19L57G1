import Lake
open Lake DSL

package second_nofirst

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice is reconstructed verbatim in
`SecondNoFirst/Kernel.lean` and the pinned one-sided stake in
`SecondNoFirst/Inherited.lean`, each with a pin note; every theorem
originating in this rung is in `SecondNoFirst/Stake.lean`,
`SecondNoFirst/NoFirst.lean`, and `SecondNoFirst/Propagate.lean`.
-/
@[default_target]
lean_lib SecondNoFirst where
  roots := #[`SecondNoFirst, `SecondNoFirst.AxiomReport]
