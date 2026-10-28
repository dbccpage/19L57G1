import ResearchTwoTheorems.Institution

/-!
# B1(i): an interference challenge is a question the weights do not know

AuthorityEffect: None.  Outside the seal; consumes `research/two_theorems`
read-only.

* EXTERNALLY IMPOSED CHALLENGE: `InterferenceChallenge D Q₀ q`.  `D` is a
  finite carrier of preparation labels, `Q₀` the weight presentations (one
  per reference context), `q` the readout of one further context.  The
  challenge asks for two preparations the weights do not tell apart on
  which `q` differs.  It mentions no group, phase, ring or amplitude.
* THEOREMS: the challenge holds exactly when the institution `Q₀` does not
  know `q` (`challenge_iff_not_knows`), exactly when adding `q` raises
  Genesis information (`challenge_iff_information_ne`), and then the rise
  is strict (`challenge_information_lt`).

The content is the identification, not the proof: each statement is a
two-line consequence of the merged `two_theorems` results.
-/

namespace ResearchQmBridge
namespace Residual

open Compression ResearchTwoTheorems.Institution

/-- CHALLENGE: two preparations with equal weights that the context `q`
separates. -/
def InterferenceChallenge (D : List Nat) (Q₀ : Institution) (q : Nat → Nat) : Prop :=
  ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ SigEq Q₀ x y ∧ q x ≠ q y

theorem challenge_iff_not_knows (D : List Nat) (Q₀ : Institution) (q : Nat → Nat) :
    InterferenceChallenge D Q₀ q ↔ ¬ Knows D Q₀ q :=
  (not_knows_iff_witness D Q₀ q).symm

theorem challenge_information_lt {D : List Nat} {Q₀ : Institution} {q : Nat → Nat}
    (h : InterferenceChallenge D Q₀ q) :
    information D Q₀ < information D (Q₀ ++ [q]) :=
  information_lt_of_not_knows ((challenge_iff_not_knows D Q₀ q).mp h)

theorem challenge_iff_information_ne (D : List Nat) (Q₀ : Institution) (q : Nat → Nat) :
    InterferenceChallenge D Q₀ q ↔ information D (Q₀ ++ [q]) ≠ information D Q₀ := by
  rw [challenge_iff_not_knows, knows_iff_information_eq]

/-- Meeting the challenge or knowing the readout: one of the two always
holds, decided on the represented carrier. -/
theorem challenge_or_knows (D : List Nat) (Q₀ : Institution) (q : Nat → Nat) :
    Knows D Q₀ q ∨ InterferenceChallenge D Q₀ q :=
  know_or_witness D Q₀ q

instance (D : List Nat) (Q₀ : Institution) (q : Nat → Nat) :
    Decidable (InterferenceChallenge D Q₀ q) :=
  decidable_of_iff _ (challenge_iff_not_knows D Q₀ q).symm

end Residual
end ResearchQmBridge
