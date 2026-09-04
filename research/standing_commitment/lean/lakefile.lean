import Lake
open Lake DSL

package standing_commitment

/-
Self-contained: core Lean only.  No sealed module is imported.  The
represented state is reconstructed verbatim in
`StandingCommitment/Base.lean` with a pin note; every theorem originating
here is in `StandingCommitment/Commitment.lean`.
-/
@[default_target]
lean_lib StandingCommitment where
  roots := #[`StandingCommitment, `StandingCommitment.AxiomReport]
