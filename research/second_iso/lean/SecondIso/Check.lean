import SecondIso.Trajectory

/-!
# Sound checks for regimes whose forms all have arity one

This file is this rung's own object.  The countermodels of this rung must
show, at concrete regimes, that a demand stands and that none stands.
Showing that none stands needs COLLAPSE, a statement over every
well-formed context, and this rung builds no decision of it in general:
that is rung three's leftover X-1, and it stays one.

What is built instead is narrower and is stated as narrower.  When every
admitted form has arity one, a well-formed context has exactly one slot,
and it is a hole; so collapse of two data reduces to agreement, form by
form, on the one-slot instance, and a one-slot context is a witness of
separability.  The Boolean checks below read exactly that, and each is
proved SOUND: a check returning `true` implies the proposition it names.
None is proved to return `true` whenever the proposition holds, and none
is a decision procedure; a check that returns `false` proves nothing.

The second part builds a sealed isomorphism from four explicitly given
maps, once a decidable conjunction of the structure's fields is shown by
kernel computation.  It adds no relation: the structure built is the
reconstructed sealed `Iso`.

AuthorityEffect: None.
-/

namespace SecondIso
namespace Check

open SecondIso.Sealed
open SecondIso.Inherited
open SecondIso.IndexSlice
open SecondIso.Trajectory

/-! ## 1. The Boolean checks, defined -/

/-- Every admitted form has arity one. -/
def unaryB (r : Regime) : Bool := r.forms.all (fun a => a == 1)

/-- Some form of arity one tells the two data apart by its one-slot
instance. -/
def sepB (r : Regime) (d d' : Nat) : Bool :=
  (List.range r.forms.length).any (fun f =>
    r.forms.getD f 0 == 1 &&
      decide (derivable r (f, [d])) != decide (derivable r (f, [d'])))

/-- Every form is of arity one and, form by form, carries a uniform rule
or agrees on the two one-slot instances. -/
def colB (r : Regime) (d d' : Nat) : Bool :=
  unaryB r && (List.range r.forms.length).all (fun f =>
    decide (f ∈ r.rules) ||
      decide ((f, [d]) ∈ r.insts) == decide ((f, [d']) ∈ r.insts))

/-- The label is honoured, by the two checks above. -/
def honourB (r : Regime) : Label → Nat → Nat → Bool
  | .apart, i, j => sepB r i j
  | .same, i, j => colB r i j
  | .free, _, _ => true

/-- The label is dishonoured, by the two checks above. -/
def dishonourB (r : Regime) : Label → Nat → Nat → Bool
  | .apart, i, j => colB r i j
  | .same, i, j => sepB r i j
  | .free, _, _ => false

/-- Every held pair's label is honoured, by the checks. -/
def noDemandCheck (S : Stake) (r : Regime) : Bool :=
  (List.range r.data).all (fun j =>
    (List.range j).all (fun i => honourB r (S.label i j) i j))

/-- Some held pair's label is dishonoured, by the checks. -/
def demandCheck (S : Stake) (r : Regime) : Bool :=
  (List.range r.data).any (fun j =>
    (List.range j).any (fun i => dishonourB r (S.label i j) i j))

/-! ## 2. A sealed isomorphism from four explicitly given maps, defined -/

/-- The fields of the sealed isomorphism structure, for four given maps,
as one conjunction.  Decidable, because every field is a bounded
statement over finite lists. -/
def IsoBy (dm dv fm fv : Nat → Nat) (r s : Regime) : Prop :=
  (∀ d ∈ List.range r.data, dm d < s.data) ∧
  (∀ d ∈ List.range s.data, dv d < r.data) ∧
  (∀ d ∈ List.range r.data, dv (dm d) = d) ∧
  (∀ d ∈ List.range s.data, dm (dv d) = d) ∧
  (∀ f ∈ List.range r.forms.length, fm f < s.forms.length) ∧
  (∀ f ∈ List.range s.forms.length, fv f < r.forms.length) ∧
  (∀ f ∈ List.range r.forms.length, fv (fm f) = f) ∧
  (∀ f ∈ List.range s.forms.length, fm (fv f) = f) ∧
  (∀ f ∈ List.range r.forms.length, s.forms.getD (fm f) 0 = r.forms.getD f 0) ∧
  (∀ p ∈ r.insts, (fm p.1, p.2.map dm) ∈ s.insts) ∧
  (∀ p ∈ s.insts, (fv p.1, p.2.map dv) ∈ r.insts) ∧
  (∀ f ∈ r.rules, fm f ∈ s.rules) ∧
  (∀ f ∈ s.rules, fv f ∈ r.rules) ∧
  (∀ q ∈ r.reqs, sortPair (dm q.1, dm q.2) ∈ s.reqs) ∧
  (∀ q ∈ s.reqs, sortPair (dv q.1, dv q.2) ∈ r.reqs)

instance (dm dv fm fv : Nat → Nat) (r s : Regime) :
    Decidable (IsoBy dm dv fm fv r s) := by
  unfold IsoBy; infer_instance

/-- The sealed isomorphism the four maps give, once the fields hold. -/
def isoOf {dm dv fm fv : Nat → Nat} {r s : Regime}
    (h : IsoBy dm dv fm fv r s) : Iso r s where
  dmap := dm
  dinv := dv
  fmap := fm
  finv := fv
  dmap_lt := h.1
  dinv_lt := h.2.1
  dinv_dmap := h.2.2.1
  dmap_dinv := h.2.2.2.1
  fmap_lt := h.2.2.2.2.1
  finv_lt := h.2.2.2.2.2.1
  finv_fmap := h.2.2.2.2.2.2.1
  fmap_finv := h.2.2.2.2.2.2.2.1
  arity := h.2.2.2.2.2.2.2.2.1
  insts_fwd := h.2.2.2.2.2.2.2.2.2.1
  insts_bwd := h.2.2.2.2.2.2.2.2.2.2.1
  rules_fwd := h.2.2.2.2.2.2.2.2.2.2.2.1
  rules_bwd := h.2.2.2.2.2.2.2.2.2.2.2.2.1
  reqs_fwd := h.2.2.2.2.2.2.2.2.2.2.2.2.2.1
  reqs_bwd := h.2.2.2.2.2.2.2.2.2.2.2.2.2.2

/-- Two prefix readings related by four given maps: both reach regimes
the maps relate, or both reach none. -/
def RelBy (dm dv fm fv : Nat → Nat) : Option Regime → Option Regime → Prop
  | some r, some s => IsoBy dm dv fm fv r s
  | none, none => True
  | _, _ => False

instance (dm dv fm fv : Nat → Nat) (a b : Option Regime) :
    Decidable (RelBy dm dv fm fv a b) := by
  cases a <;> cases b <;> unfold RelBy <;> infer_instance

/-! ## 3. Collapse and separability where every form has arity one -/

/-- **unary_ctx_slots.**  When every admitted form has arity one, every
well-formed context has a single slot, and that slot is a hole. -/
theorem unary_ctx_slots (r : Regime) (hu : ∀ a ∈ r.forms, a = 1) (c : Ctx)
    (hc : wfCtx r c) : c.slots = [none] := by
  have hlen : c.slots.length = 1 := by
    rw [hc.2.1, List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hc.1,
      Option.getD_some]
    exact hu _ (List.getElem_mem hc.1)
  have hn := hc.2.2.1
  cases hs : c.slots with
  | nil => rw [hs] at hlen; simp at hlen
  | cons x t =>
    cases t with
    | nil =>
      rw [hs] at hn
      rw [List.mem_singleton] at hn
      rw [hn]
    | cons y t' =>
      rw [hs] at hlen
      simp only [List.length_cons] at hlen
      omega

/-- **collapsed_of_unary.**  When every admitted form has arity one, two
data are collapsed as soon as, form by form, either the form carries a
uniform rule or the two one-slot instances are both admitted or both
not. -/
theorem collapsed_of_unary (r : Regime) (hu : ∀ a ∈ r.forms, a = 1)
    (d d' : Nat)
    (hmem : ∀ f, f < r.forms.length →
      f ∈ r.rules ∨ ((f, [d]) ∈ r.insts ↔ (f, [d']) ∈ r.insts)) :
    collapsed r d d' := by
  intro c hc
  have hs := unary_ctx_slots r hu c hc
  have hp : ∀ x, plug c x = (c.form, [x]) := by
    intro x
    simp [plug, hs]
  rw [hp d, hp d']
  rcases hmem c.form hc.1 with hr | hiff
  · exact ⟨fun _ => Or.inr hr, fun _ => Or.inr hr⟩
  · exact ⟨fun h => h.elim (fun hi => Or.inl (hiff.mp hi)) Or.inr,
      fun h => h.elim (fun hi => Or.inl (hiff.mpr hi)) Or.inr⟩

/-- **separable_of_unary_witness.**  A form of arity one whose one-slot
instance is derivable for one datum and not the other separates them;
the witness is the context with a single hole. -/
theorem separable_of_unary_witness (r : Regime) (f : Nat)
    (hf : f < r.forms.length) (ha : r.forms.getD f 0 = 1) (d d' : Nat)
    (hdiff : ¬ (derivable r (f, [d]) ↔ derivable r (f, [d']))) :
    separable r d d' :=
  ⟨⟨f, [none]⟩, ⟨hf, by rw [ha]; rfl, by simp, by simp [slotOk]⟩,
    by simpa [plug] using hdiff⟩

/-! ## 4. The soundness of the Boolean checks -/

/-- **sepB_sound.** -/
theorem sepB_sound (r : Regime) (d d' : Nat) (h : sepB r d d' = true) :
    separable r d d' := by
  unfold sepB at h
  rw [List.any_eq_true] at h
  obtain ⟨f, hf, hb⟩ := h
  rw [Bool.and_eq_true, beq_iff_eq, bne_iff_ne, ne_eq] at hb
  refine separable_of_unary_witness r f (List.mem_range.mp hf) hb.1 d d' ?_
  intro hiff
  exact hb.2 (decide_eq_decide.mpr hiff)

/-- **colB_sound.** -/
theorem colB_sound (r : Regime) (d d' : Nat) (h : colB r d d' = true) :
    collapsed r d d' := by
  unfold colB at h
  rw [Bool.and_eq_true] at h
  obtain ⟨hu, hall⟩ := h
  have hu' : ∀ a ∈ r.forms, a = 1 := by
    intro a ha
    unfold unaryB at hu
    rw [List.all_eq_true] at hu
    exact beq_iff_eq.mp (hu a ha)
  apply collapsed_of_unary r hu' d d'
  intro f hf
  rw [List.all_eq_true] at hall
  have hb := hall f (List.mem_range.mpr hf)
  rw [Bool.or_eq_true, decide_eq_true_iff, beq_iff_eq] at hb
  rcases hb with hr | heq
  · exact Or.inl hr
  · exact Or.inr (decide_eq_decide.mp heq)

/-- **honourCheck_sound.**  The honour check returning `true` implies
honour, for each of the three labels. -/
theorem honourCheck_sound (r : Regime) (l : Label) (i j : Nat)
    (h : honourB r l i j = true) : honour r l i j := by
  cases l with
  | apart => exact sepB_sound r i j h
  | same => exact colB_sound r i j h
  | free => trivial

/-- **dishonourCheck_sound.**  The dishonour check returning `true`
implies that the label is not honoured. -/
theorem dishonourCheck_sound (r : Regime) (l : Label) (i j : Nat)
    (h : dishonourB r l i j = true) : ¬ honour r l i j := by
  cases l with
  | apart => exact collapsed_not_separable (colB_sound r i j h)
  | same => exact separable_not_collapsed (sepB_sound r i j h)
  | free => exact absurd h (by simp [dishonourB])

/-- **noDemandCheck_sound.**  The no-demand check returning `true`
implies that the regime carries no demand under the stake. -/
theorem noDemandCheck_sound (S : Stake) (r : Regime)
    (h : noDemandCheck S r = true) : ¬ HasDemand S r := by
  intro ⟨i, j, hij, hj, _, hno⟩
  unfold noDemandCheck at h
  rw [List.all_eq_true] at h
  have hrow := h j (List.mem_range.mpr hj)
  rw [List.all_eq_true] at hrow
  exact hno (honourCheck_sound r _ i j (hrow i (List.mem_range.mpr hij)))

/-- **demandCheck_sound.**  The demand check returning `true` implies that
the regime carries a demand under the stake. -/
theorem demandCheck_sound (S : Stake) (r : Regime)
    (h : demandCheck S r = true) : HasDemand S r := by
  unfold demandCheck at h
  rw [List.any_eq_true] at h
  obtain ⟨j, hj, hrow⟩ := h
  rw [List.any_eq_true] at hrow
  obtain ⟨i, hi, hb⟩ := hrow
  have hlab : (S.label i j).labelled = true := by
    cases hl : S.label i j with
    | apart => rfl
    | same => rfl
    | free => rw [hl] at hb; exact absurd hb (by simp [dishonourB])
  exact ⟨i, j, List.mem_range.mp hi, List.mem_range.mp hj, hlab,
    dishonourCheck_sound r _ i j hb⟩

/-! ## 5. Reading the checks along a history, and relating by given maps -/

/-- **index_of_check.**  A first count, read off the checks: the prefix of
the count passes the demand check and every shorter prefix passes the
no-demand check. -/
theorem index_of_check (S : Stake) (base : Regime) (h : List Event) (k : Nat)
    (hd : (stateAt h base k).elim false (demandCheck S) = true)
    (hq : ∀ m, m < k → (stateAt h base m).elim true (noDemandCheck S) = true) :
    IsFirstDemand S base h k := by
  refine ⟨?_, ?_⟩
  · cases hs : stateAt h base k with
    | none => rw [hs] at hd; exact absurd hd (by simp)
    | some r => rw [hs] at hd; exact ⟨r, rfl, demandCheck_sound S r hd⟩
  · intro m hm r hr
    have := hq m hm
    rw [hr] at this
    exact noDemandCheck_sound S r this

/-- **no_index_of_check.**  No first count at all, read off the checks: every
prefix up to the full length passes the no-demand check, and every longer
count reaches what the full length reaches. -/
theorem no_index_of_check (S : Stake) (base : Regime) (h : List Event)
    (hq : ∀ m, m ≤ h.length → (stateAt h base m).elim true (noDemandCheck S) = true) :
    ∀ k, ¬ IsFirstDemand S base h k := by
  intro k hf
  obtain ⟨r, hr, hd⟩ := hf.1
  by_cases hk : k ≤ h.length
  · have := hq k hk
    rw [hr] at this
    exact noDemandCheck_sound S r this hd
  · have hfull : stateAt h base k = stateAt h base h.length := by
      unfold stateAt
      rw [List.take_of_length_le (by omega), List.take_length]
    have := hq h.length (Nat.le_refl _)
    rw [← hfull, hr] at this
    exact noDemandCheck_sound S r this hd

/-- **related_of_relBy.**  Readings related by four given maps are
related by the sealed isomorphism. -/
theorem related_of_relBy {dm dv fm fv : Nat → Nat} {a b : Option Regime}
    (h : RelBy dm dv fm fv a b) : Related a b := by
  cases a <;> cases b
  · trivial
  · exact absurd h (by simp [RelBy])
  · exact absurd h (by simp [RelBy])
  · exact ⟨isoOf h⟩

end Check
end SecondIso
