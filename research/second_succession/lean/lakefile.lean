import Lake
open Lake DSL

package second_succession

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice is reconstructed verbatim in
`SecondSuccession/Kernel.lean`, with a pin note; every theorem
originating in this rung is in `SecondSuccession/Count.lean` and
`SecondSuccession/Readings.lean`.
-/
@[default_target]
lean_lib SecondSuccession where
  roots := #[`SecondSuccession, `SecondSuccession.AxiomReport]
