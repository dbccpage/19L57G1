import SecondNoFirst.NoFirst

/-!
# The demand-inert event kinds

NOT PREDICTED.  This module was written after the stage-four computation
missed prediction N-16.  That prediction said two of the six sealed event
kinds never change the demand set; the rectangle found three, the third
being the admission of a judgment form.  The miss stands recorded next to
its value and is not edited; what follows is the theorem the miss
prompted, and it is labelled throughout as unpredicted work.

Three of the six kinds of the sealed grammar reconstructed here leave
every demand of every stake unchanged:

* a supply, because it changes no regime at all;
* an imposition, because a requirement enters neither derivability nor
  well-formedness of a context, so it enters no profile;
* the admission of a judgment form, because a context of the newly
  admitted form derives nothing -- no admitted instance names a form
  index that large, and the new form carries no uniform rule -- so no
  profile gains anything and no pair's collapse moves.

The third needs the regime to be well formed and is the only one of the
three with content.  The other three kinds -- the admission of a datum, of
an instance, and of a uniform rule -- are not inert, and this rung
exhibits that only computationally, in the rectangle of stage four.

AuthorityEffect: None.
-/

namespace SecondNoFirst
namespace Inert

open SecondNoFirst.Sealed
open SecondNoFirst.Stake
open SecondNoFirst.NoFirst

/-! ## 0. Transporting a demand along an agreement of observation

Collapse and separability are transported SEPARATELY.  Deriving one from
the other would need, in the direction from "not collapsed" to
"separable", a choice of witness over the context type, which is
infinite; that direction is not available constructively and is not used.
Every transport below supplies both halves and its own witness. -/

/-- A demand transports along any pair of agreements -- of the data count,
of separability, and of collapse -- between two regimes.  This is the one
bridge the three inertia theorems share. -/
theorem demand_congr (S : Stake) (r r' : Regime)
    (hdata : r'.data = r.data)
    (hsep : ∀ i j, separable r' i j ↔ separable r i j)
    (hcol : ∀ i j, collapsed r' i j ↔ collapsed r i j) (i j : Nat) :
    Demand S r' i j ↔ Demand S r i j := by
  unfold Demand honour
  rw [hdata]
  refine and_congr_right (fun _ => and_congr_right (fun _ =>
    and_congr_right (fun _ => not_congr ?_)))
  cases S.label i j with
  | apart => exact hsep i j
  | same => exact hcol i j
  | free => exact Iff.rfl

/-! ## 1. An imposition is demand-inert -/

/-- The regime an imposition reaches. -/
def addReq (r : Regime) (i j : Nat) : Regime :=
  { r with reqs := insertNew r.reqs (i, j) }

theorem stepE_impose (r : Regime) (i j : Nat) (h : i < j) (hj : j < r.data) :
    stepE r (.impose i j) = some (addReq r i j) := by
  show (if i < j ∧ j < r.data then some (addReq r i j) else none) = some (addReq r i j)
  rw [if_pos ⟨h, hj⟩]

/-- **impose_preserves_demands.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake, an imposition changes no
demand of any stake.
AT THE LEVEL OF A DEFINITION: an imposition writes only the requirement
field, and that field enters neither derivability nor the well-formedness
of a context, so both sides unfold to the same proposition. -/
theorem impose_preserves_demands (S : Stake) (r : Regime) (i j : Nat)
    (a b : Nat) : Demand S (addReq r i j) a b ↔ Demand S r a b := Iff.rfl

/-! ## 2. Admitting a form is demand-inert -/

/-- The regime a form admission reaches. -/
def addForm (r : Regime) (a : Nat) : Regime :=
  { r with forms := r.forms ++ [a] }

theorem stepE_admitForm (r : Regime) (a : Nat) (h : 1 ≤ a) :
    stepE r (.admitForm a) = some (addForm r a) := by
  show (if 1 ≤ a then some (addForm r a) else none) = some (addForm r a)
  rw [if_pos h]

/-- Appending to the form list does not move the arity of a form already
admitted. -/
theorem getD_append_left (l : List Nat) (a i : Nat) (h : i < l.length) :
    (l ++ [a]).getD i 0 = l.getD i 0 := by
  simp [List.getD_eq_getElem?_getD, List.getElem?_append_left h]

/-- A context naming a form admitted before the new one is well formed
after the admission exactly when it was well formed before. -/
theorem wfCtx_addForm_left (r : Regime) (a : Nat) (c : Ctx)
    (hlt : c.form < r.forms.length) :
    wfCtx (addForm r a) c ↔ wfCtx r c := by
  have harity : (addForm r a).forms.getD c.form 0 = r.forms.getD c.form 0 :=
    getD_append_left r.forms a c.form hlt
  have hlen : c.form < (addForm r a).forms.length := by
    show c.form < (r.forms ++ [a]).length
    rw [List.length_append]
    omega
  constructor
  · intro h
    obtain ⟨_, h2, h3, h4⟩ := h
    rw [harity] at h2
    exact ⟨hlt, h2, h3, h4⟩
  · intro h
    obtain ⟨_, h2, h3, h4⟩ := h
    rw [← harity] at h2
    exact ⟨hlen, h2, h3, h4⟩

/-- A context of the newly admitted form derives nothing, whatever datum
is plugged into it: no admitted instance of a well-formed regime names a
form index that large, and the new form carries no uniform rule. -/
theorem new_form_derives_nothing (r : Regime) (hwf : r.wf) (a : Nat) (c : Ctx)
    (hnew : c.form = r.forms.length) (d : Nat) :
    ¬ derivable (addForm r a) (plug c d) := by
  intro h
  cases h with
  | inl hm =>
      have hb := (hwf.1 _ hm).1
      show False
      rw [show (plug c d).1 = c.form from rfl, hnew] at hb
      exact absurd hb (Nat.lt_irrefl _)
  | inr hr =>
      have hb := hwf.2.1 _ hr
      show False
      rw [show (plug c d).1 = c.form from rfl, hnew] at hb
      exact absurd hb (Nat.lt_irrefl _)

/-- **collapsed_addForm.**  Admitting a judgment form to a well-formed
regime changes no pair's collapse: the contexts of forms already admitted
answer exactly as before, and the contexts of the new form derive nothing
for any datum, so they separate nothing. -/
theorem collapsed_addForm (r : Regime) (hwf : r.wf) (a : Nat) (d d' : Nat) :
    collapsed (addForm r a) d d' ↔ collapsed r d d' := by
  constructor
  · intro h c hw
    exact h c ((wfCtx_addForm_left r a c hw.1).mpr hw)
  · intro h c hw
    by_cases hlt : c.form < r.forms.length
    · exact h c ((wfCtx_addForm_left r a c hlt).mp hw)
    · have hb : c.form < (r.forms ++ [a]).length := hw.1
      rw [List.length_append] at hb
      have hnew : c.form = r.forms.length := by simp at hb; omega
      constructor
      · intro hd
        exact absurd hd (new_form_derives_nothing r hwf a c hnew d)
      · intro hd
        exact absurd hd (new_form_derives_nothing r hwf a c hnew d')

/-- **separable_addForm.**  Admitting a judgment form to a well-formed
regime separates no pair it did not already separate, and unseparates
none: a witness of the new form derives nothing on either side, so it
cannot be a witness at all. -/
theorem separable_addForm (r : Regime) (hwf : r.wf) (a : Nat) (d d' : Nat) :
    separable (addForm r a) d d' ↔ separable r d d' := by
  constructor
  · intro ⟨c, hw, hne⟩
    by_cases hlt : c.form < r.forms.length
    · exact ⟨c, (wfCtx_addForm_left r a c hlt).mp hw, hne⟩
    · exfalso
      have hb : c.form < (r.forms ++ [a]).length := hw.1
      rw [List.length_append] at hb
      have hnew : c.form = r.forms.length := by simp at hb; omega
      exact hne ⟨fun hd => absurd hd (new_form_derives_nothing r hwf a c hnew d),
                 fun hd => absurd hd (new_form_derives_nothing r hwf a c hnew d')⟩
  · intro ⟨c, hw, hne⟩
    exact ⟨c, (wfCtx_addForm_left r a c hw.1).mpr hw, hne⟩

/-- **admitForm_preserves_demands.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake: admitting a judgment form to
a well-formed regime changes no demand of any stake.  A form is
demand-inert until an instance or a uniform rule reaches it.

This is the third of the three inert kinds, and the only one of the three
with content.  It was not predicted; it was proved after the stage-four
rectangle found the count to be three where the frozen prediction said
two. -/
theorem admitForm_preserves_demands (S : Stake) (r : Regime) (hwf : r.wf)
    (a : Nat) (i j : Nat) :
    Demand S (addForm r a) i j ↔ Demand S r i j :=
  demand_congr S r (addForm r a) rfl
    (fun x y => separable_addForm r hwf a x y)
    (fun x y => collapsed_addForm r hwf a x y) i j

/-! ## 3. The three together -/

/-- **three_kinds_are_demand_inert.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake, and in no other grammar:
of the six event kinds the rung-zero census recorded, three leave every
demand of every stake unchanged -- the supply, the imposition, and the
admission of a judgment form, the last of these at a well-formed regime.

The remaining three kinds -- the admission of a datum, of an instance, and
of a uniform rule -- are NOT claimed inert, and nothing here says they are
not; the rectangle of stage four exhibits each of them changing a demand
set, which is a finite computation and not a theorem. -/
theorem three_kinds_are_demand_inert :
    (∀ (S : Stake) (r r' : Regime) (t i j : Nat),
        stepE r (.supply t) = some r' → (Demand S r' i j ↔ Demand S r i j))
  ∧ (∀ (S : Stake) (r : Regime) (i j a b : Nat),
        Demand S (addReq r i j) a b ↔ Demand S r a b)
  ∧ (∀ (S : Stake) (r : Regime), r.wf → ∀ (a i j : Nat),
        Demand S (addForm r a) i j ↔ Demand S r i j) :=
  ⟨fun S r r' t i j h => supply_preserves_demands S r r' t h i j,
   fun S r i j a b => impose_preserves_demands S r i j a b,
   fun S r hwf a i j => admitForm_preserves_demands S r hwf a i j⟩

end Inert
end SecondNoFirst
