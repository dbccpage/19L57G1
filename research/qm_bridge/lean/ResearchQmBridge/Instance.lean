import ResearchQmBridge.Residual
import ResearchQmBridge.Gauss

/-!
# The amplitude model meets the Genesis challenge

AuthorityEffect: None.

Three preparation labels `0, 1, 2` carry the amplitude pairs `(1, 1)`,
`(1, i)` and `(1, -1)` of `ℤ[i]` (`Gauss.mu4_triple`).  Read through the
model, the two weights and the mixing readout are three presentations
`Nat → Nat` on the carrier.  The weights cut the carrier into one class; with
the mixing readout it has three (`instance_information`).  So the readout is
a question the weight institution does not know (`instance_not_knows`), and
the model meets the interference challenge (`instance_challenge`).  The
challenge statement itself mentions only the three presentations.
-/

namespace ResearchQmBridge
namespace Instance

open Compression ResearchTwoTheorems.Institution Residual Gauss GI

def amp : Nat → Prep
  | 1 => (one, I)
  | 2 => (one, negOne)
  | _ => (one, one)

def carrier : List Nat := [0, 1, 2]
def w₁ (x : Nat) : Nat := (norm (amp x).1).toNat
def w₂ (x : Nat) : Nat := (norm (amp x).2).toNat
def readout (x : Nat) : Nat := (mix (amp x)).toNat
def weightsQ : Institution := [w₁, w₂]

theorem instance_information :
    information carrier weightsQ = 1 ∧ information carrier (weightsQ ++ [readout]) = 3 := by
  decide

theorem instance_not_knows : ¬ Knows carrier weightsQ readout := by
  decide

theorem instance_challenge : InterferenceChallenge carrier weightsQ readout :=
  (challenge_iff_not_knows _ _ _).mpr instance_not_knows

end Instance
end ResearchQmBridge
