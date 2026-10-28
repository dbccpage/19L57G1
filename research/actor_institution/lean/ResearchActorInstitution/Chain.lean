import ResearchTwoTheorems.Institution
import ResearchActorInstitution.Institution

/-!
# Chains of institutions, and determination against truth

* An *extension chain* is a list of institutions each retaining the members
  of the last.  `long_chain_stationary`: any extension chain longer than the
  carrier has a step at which the information does not move (the two-theorems
  tree's TT-35o, now a theorem).  `stationary_step_known`: at such a step every
  new member is already known by the old institution, so
  (`stationary_step_inert`) nothing becomes known that was not known before.
* `information_without_determination`: information is not knowledge of any
  particular question — `[parity]` has two classes on four points and does
  not know `half`.
* `determination_not_truth`: knowing is not corresponding to a target.  On any
  nonempty carrier every institution knows two claims that disagree
  everywhere, so at most one of them can agree with any target.
* `truth_is_a_further_question`: whether a known claim agrees with a target is
  itself a question, and the institution need not know it.
* `truth_from_admitted_target`: what buys agreement with a target is admitting
  the target as a member.  That admission is the price of "truth" in this
  setting; no theorem here reduces it.

AuthorityEffect: None.
-/

namespace ResearchActorInstitution
namespace Chain

open Compression ResearchTwoTheorems.Institution

/-- `Q'` retains every member of `Q`. -/
def Extends (Q Q' : Institution) : Prop := ∀ p, p ∈ Q → p ∈ Q'

/-- A list of institutions, each extending the previous one. -/
def ExtChain : List Institution → Prop
  | [] => True
  | [_] => True
  | Q :: Q' :: t => Extends Q Q' ∧ ExtChain (Q' :: t)

/-- Some step of the chain leaves the information on `D` unchanged. -/
def HasStationary (D : List Nat) : List Institution → Prop
  | Q :: Q' :: t => information D Q' = information D Q ∨ HasStationary D (Q' :: t)
  | _ => False

/-- A chain of `t.length` steps starting above `information D Q` must stall
once the carrier bound is exhausted. -/
theorem stationary_of_bound (D : List Nat) :
    ∀ (t : List Institution) (Q : Institution), ExtChain (Q :: t) →
      D.length < information D Q + t.length → HasStationary D (Q :: t) := by
  intro t
  induction t with
  | nil =>
    intro Q _ hlt
    have := information_le_carrier D Q
    simp only [List.length_nil] at hlt
    show False
    omega
  | cons Q' t ih =>
    intro Q hc hlt
    have hext : Extends Q Q' := hc.1
    have hc' : ExtChain (Q' :: t) := hc.2
    show information D Q' = information D Q ∨ HasStationary D (Q' :: t)
    cases Nat.decEq (information D Q') (information D Q) with
    | isTrue h => exact Or.inl h
    | isFalse hne =>
      apply Or.inr
      apply ih Q' hc'
      have hmono : information D Q ≤ information D Q' := information_mono hext
      simp only [List.length_cons] at hlt
      omega

/-- **Crash by compression (TT-35o).**  An extension chain on a nonempty
carrier that is longer than the carrier has a stationary step. -/
theorem long_chain_stationary (D : List Nat) (hD : D ≠ []) (L : List Institution)
    (hc : ExtChain L) (hlen : D.length < L.length) : HasStationary D L := by
  cases L with
  | nil => simp only [List.length_nil] at hlen; exact absurd hlen (Nat.not_lt_zero _)
  | cons Q t =>
    apply stationary_of_bound D t Q hc
    have h1 := classCount_pos D Q hD
    simp only [List.length_cons] at hlen
    show D.length < classCount D Q + t.length
    omega

/-- At a stationary step every member of the new institution was already
known by the old one. -/
theorem stationary_step_known {D : List Nat} {Q Q' : Institution} (hext : Extends Q Q')
    (hstat : information D Q' = information D Q) : ∀ p, p ∈ Q' → Knows D Q p := by
  intro p hp
  rw [knows_iff_information_eq]
  apply Nat.le_antisymm
  · have h1 : information D (Q ++ [p]) ≤ information D Q' := by
      apply information_mono
      intro r hr
      rcases List.mem_append.mp hr with hr | hr
      · exact hext r hr
      · rw [List.mem_singleton.mp hr]; exact hp
    rw [hstat] at h1
    exact h1
  · exact information_mono (fun r hr => List.mem_append_left _ hr)

/-- A stationary step changes what is known of nothing. -/
theorem stationary_step_inert {D : List Nat} {Q Q' : Institution} (hext : Extends Q Q')
    (hstat : information D Q' = information D Q) (q : Nat → Nat) :
    Knows D Q' q ↔ Knows D Q q := by
  constructor
  · intro h
    rw [knows_iff_determined] at h ⊢
    intro x hx y hy hs
    apply h x hx y hy
    intro p hp
    have hk := stationary_step_known hext hstat p hp
    exact (knows_iff_determined D Q p).mp hk x hx y hy hs
  · exact knows_mono hext

/-- Information is not knowledge of a given question: `[parity]` carries
two classes on four points and does not know `half`. -/
theorem information_without_determination :
    2 ≤ information [0, 1, 2, 3] [parity] ∧ ¬ Knows [0, 1, 2, 3] [parity] half := by
  decide

/-! ## Determination is not truth -/

/-- `q` agrees with the target `t` on the carrier. -/
def Corr (D : List Nat) (q t : Nat → Nat) : Prop := ∀ x, x ∈ D → q x = t x

def corrB (D : List Nat) (q t : Nat → Nat) : Bool := D.all (fun x => decide (q x = t x))

theorem corr_iff_corrB (D : List Nat) (q t : Nat → Nat) : Corr D q t ↔ corrB D q t = true := by
  unfold Corr corrB
  rw [List.all_eq_true]
  constructor
  · intro h x hx; exact decide_eq_true (h x hx)
  · intro h x hx; exact of_decide_eq_true (h x hx)

/-- **Functional determination is not established truth.**  On a nonempty
carrier every institution knows two claims that agree with each other
nowhere, so knowing a claim cannot mean that it agrees with a target. -/
theorem determination_not_truth (D : List Nat) (Q : Institution) (hD : D ≠ []) :
    ∃ q t : Nat → Nat, Knows D Q q ∧ Knows D Q t ∧ ¬ Corr D q t := by
  refine ⟨fun _ => 0, fun _ => 1, knows_const D Q 0, knows_const D Q 1, ?_⟩
  intro h
  cases D with
  | nil => exact hD rfl
  | cons x _ => exact Nat.zero_ne_one (h x List.mem_cons_self)

/-- The agreement of `q` with `t`, as a question on the carrier. -/
def agreeQ (q t : Nat → Nat) : Nat → Nat := fun x => if q x = t x then 1 else 0

theorem corr_iff_agreeQ (D : List Nat) (q t : Nat → Nat) :
    Corr D q t ↔ ∀ x, x ∈ D → agreeQ q t x = 1 := by
  unfold Corr agreeQ
  constructor
  · intro h x hx; rw [if_pos (h x hx)]
  · intro h x hx
    have := h x hx
    cases Nat.decEq (q x) (t x) with
    | isTrue e => exact e
    | isFalse ne => rw [if_neg ne] at this; exact absurd this (by decide)

/-- **Truth is a further question.**  The empty institution knows the
constant claim `0`; whether that claim agrees with the target `id` is a
question it does not know. -/
theorem truth_is_a_further_question :
    Knows [0, 1] [] (fun _ => 0) ∧
    ¬ Knows [0, 1] [] (agreeQ (fun _ => 0) (fun x => x)) := by
  unfold agreeQ
  decide

/-- **The price of truth.**  If the target is admitted as a member and the
claim agrees with it on the carrier, the claim is known. -/
theorem truth_from_admitted_target {D : List Nat} {Q : Institution} {q t : Nat → Nat}
    (ht : t ∈ Q) (hc : Corr D q t) : Knows D Q q := by
  rw [knows_iff_determined]
  intro x hx y hy hs
  rw [hc x hx, hc y hy]
  exact hs t ht

/-- With the target admitted, agreement with it is known too. -/
theorem agreement_known_of_admitted {D : List Nat} {Q : Institution} {q t : Nat → Nat}
    (ht : t ∈ Q) (hq : Knows D Q q) : Knows D Q (agreeQ q t) := by
  rw [knows_iff_determined] at hq ⊢
  intro x hx y hy hs
  unfold agreeQ
  rw [hq x hx y hy hs, hs t ht]

end Chain
end ResearchActorInstitution
