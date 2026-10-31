"""Book proofs for the reasoning route; AuthorityEffect: None."""

SOURCE = r"""
import Derivation.Compression

namespace Textbook.ReasoningLab

theorem chain (P Q R : Prop) (hpq : P → Q) (hqr : Q → R) : P → R :=
  fun hp => hqr (hpq hp)

theorem both_directions (P Q : Prop) : (P ↔ Q) ↔ ((P → Q) ∧ (Q → P)) :=
  ⟨fun h => ⟨h.mp, h.mpr⟩, fun h => ⟨h.1, h.2⟩⟩

theorem no_automatic_reverse : (False → True) ∧ ¬ (True → False) :=
  ⟨fun h => False.elim h, fun h => h True.intro⟩

/-- A model implication and two contradictory interpreted answers cannot all hold.
This does not select which application premise is mistaken. -/
theorem incompatible_application_bundle (P Q : Prop)
    (rule : P → Q) (reportedP : P) (reportedNotQ : ¬ Q) : False :=
  reportedNotQ (rule reportedP)

theorem empty_domain (P : Nat → Prop) :
    (∀ x, x ∈ ([] : List Nat) → P x) ∧ ¬ (∃ x, x ∈ ([] : List Nat) ∧ P x) := by
  constructor
  · intro x hx; cases hx
  · rintro ⟨x, hx, _⟩; cases hx

theorem common_implies_individual (X T : Type) (D : List X) (Q : List T)
    (works : T → X → Prop)
    (h : ∃ q, q ∈ Q ∧ ∀ x, x ∈ D → works q x) :
    ∀ x, x ∈ D → ∃ q, q ∈ Q ∧ works q x := by
  rcases h with ⟨q, hq, hw⟩
  intro x hx
  exact ⟨q, hq, hw x hx⟩

theorem recovery_preserves_equal (D : List Nat) (p q : Nat → Nat)
    (h : Compression.FactorsOn D p q) (a b : Nat)
    (ha : a ∈ D) (hb : b ∈ D) (heq : p a = p b) : q a = q b := by
  rcases h with ⟨g, hg⟩
  exact (hg a ha).symm.trans ((congrArg g heq).trans (hg b hb))

def blue (x : Nat) : Nat := if x < 2 then 1 else 0
def round (x : Nat) : Nat := if x = 0 then 1 else 0
def triangle (x : Nat) : Nat := if x = 0 then 0 else 1

theorem round_blue_direction :
    (round 0 = 1 → blue 0 = 1) ∧ (round 1 = 1 → blue 1 = 1) ∧
    (round 2 = 1 → blue 2 = 1) := by decide

theorem reverse_fails_at_b : blue 1 = 1 ∧ round 1 ≠ 1 := by decide

theorem triangle_iff_not_round :
    ((triangle 0 = 1) ↔ (round 0 ≠ 1)) ∧
    ((triangle 1 = 1) ↔ (round 1 ≠ 1)) ∧
    ((triangle 2 = 1) ↔ (round 2 ≠ 1)) := by decide

def test (q : Fin 2) : Nat → Nat := if q.val = 0 then blue else triangle
def pairSep (q : Fin 2) (p : Fin 3) : Bool :=
  let pair := if p.val = 0 then (0, 1) else if p.val = 1 then (0, 2) else (1, 2)
  decide (test q pair.1 ≠ test q pair.2)

theorem individual_without_common :
    (∀ p : Fin 3, ∃ q : Fin 2, pairSep q p = true) ∧
    ¬ (∃ q : Fin 2, ∀ p : Fin 3, pairSep q p = true) := by decide

theorem recover_on_smaller_domain : Compression.FactorsOn [0, 2] blue round := by
  refine ⟨id, ?_⟩
  intro x hx
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
  rcases hx with hx | hx <;> subst x <;> rfl

theorem no_recovery_on_full_domain : ¬ Compression.FactorsOn [0, 1, 2] blue round := by
  rintro ⟨g, hg⟩
  have ha := hg 0 (by decide)
  have hb := hg 1 (by decide)
  change g 1 = 1 at ha
  change g 1 = 0 at hb
  have h : (1 : Nat) = 0 := ha.symm.trans hb
  exact Nat.noConfusion h

end Textbook.ReasoningLab
"""

NAMES = ["chain", "both_directions", "no_automatic_reverse", "incompatible_application_bundle", "empty_domain",
         "common_implies_individual", "recovery_preserves_equal", "round_blue_direction",
         "reverse_fails_at_b", "triangle_iff_not_round", "individual_without_common",
         "recover_on_smaller_domain", "no_recovery_on_full_domain"]
SOURCE += "\n" + "\n".join("#print axioms Textbook.ReasoningLab." + name for name in NAMES) + "\n"
