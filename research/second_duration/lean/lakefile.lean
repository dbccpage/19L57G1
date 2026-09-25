import Lake
open Lake DSL

package second_duration

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice is reconstructed verbatim in
`SecondDuration/Kernel.lean`, with a pin note; every theorem
originating in this rung is in `SecondDuration/Rounds.lean` and
`SecondDuration/Gaps.lean`.
-/
@[default_target]
lean_lib SecondDuration where
  roots := #[`SecondDuration, `SecondDuration.AxiomReport]
