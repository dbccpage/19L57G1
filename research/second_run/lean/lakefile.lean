import Lake
open Lake DSL

package second_run

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice is reconstructed verbatim in
`SecondRun/Kernel.lean`, with a pin note; every theorem native to this
tree is in `SecondRun/Run.lean`.
-/
@[default_target]
lean_lib SecondRun where
  roots := #[`SecondRun, `SecondRun.AxiomReport]
