import Lake
open Lake DSL

package second_engine

/-
Self-contained: core Lean only.  No sealed module and no sibling package
is imported.  The sealed kernel slice and the sealed isomorphism
structure are reconstructed verbatim in `SecondEngine/Kernel.lean` and
`SecondEngine/IsoKernel.lean`, with a pin note each; rung nine's carrying
pieces are restated in `SecondEngine/Carry.lean`; every theorem native to
this tree is in `SecondEngine/Orbit.lean`, `SecondEngine/Stake.lean`,
`SecondEngine/Genesis.lean`, `SecondEngine/Engine.lean` and
`SecondEngine/Census.lean`.
-/
@[default_target]
lean_lib SecondEngine where
  roots := #[`SecondEngine, `SecondEngine.AxiomReport]
