/-!
# The sealed kernel, reconstructed verbatim

PIN NOTE (whole file).  Every declaration below is reproduced VERBATIM
from the sealed modules `lean4/Derivation/Basic.lean` (lines twenty
through one hundred and sixty-seven, and two hundred and two through two
hundred and fifteen) and `lean4/Derivation/Inertia.lean` (lines thirteen
through ninety-two) at the blobs recorded in `SOURCE_MANIFEST.json`, at
the snapshot recorded there.  The only change is the outer namespace, so
that this package stays self-contained and imports nothing sealed.  Doc
comments, section headers and proofs are the sealed ones, unedited.
`verify_pins.py` recomputes the blob hash of each sealed source at the
snapshot and at HEAD and fails on any drift, and `test_reconstruction.py`
compares this file declaration by declaration with the pinned blobs.

Why a reconstruction and not a dependency: no research tree of this
repository declares the sealed package as a Lake dependency, and the
sibling rungs reconstruct their slices the same way.  The source policy
is declared in `STATUS.md` before the first compile: RECONSTRUCTION, with
a pin note per file.

What a pin proves: that the sealed source did not move.  It does not
prove that this reconstruction is faithful; the mechanical check on that
is the declaration comparison named above, and what the comparison omits
is pinned and read by hand.

Reach: the slice the theorems of this rung need, plus the two sealed
reading regimes they take as bases.  The sealed augmentation, response
and gate machinery is NOT reconstructed.

AuthorityEffect: None.
-/

namespace SecondRun
namespace Sealed

/-- Judgment instance: a form index and an argument tuple of datum indices. -/
abbrev Inst := Nat × List Nat

/-- Deduplicating insertion: the admitted collections are sets, so
re-admission is a no-op. -/
def insertNew {α : Type} [DecidableEq α] (l : List α) (a : α) : List α :=
  if a ∈ l then l else l ++ [a]

@[simp] theorem insertNew_nil {α : Type} [DecidableEq α] (a : α) :
    insertNew [] a = [a] := rfl

theorem insertNew_of_not_mem {α : Type} [DecidableEq α] {l : List α}
    {a : α} (h : a ∉ l) : insertNew l a = l ++ [a] := by
  simp [insertNew, h]

theorem insertNew_of_mem {α : Type} [DecidableEq α] {l : List α}
    {a : α} (h : a ∈ l) : insertNew l a = l := by
  simp [insertNew, h]

/-- Membership after deduplicating insertion. -/
theorem mem_insertNew {α : Type} [DecidableEq α] {l : List α} {a x : α} :
    x ∈ insertNew l a ↔ x ∈ l ∨ x = a := by
  by_cases h : a ∈ l
  · rw [insertNew_of_mem h]
    constructor
    · exact Or.inl
    · intro hx
      cases hx with
      | inl hx => exact hx
      | inr hx => exact hx ▸ h
  · rw [insertNew_of_not_mem h]
    simp [List.mem_append]

structure Regime where
  data  : Nat
  forms : List Nat
  insts : List Inst
  rules : List Nat
  reqs  : List (Nat × Nat)
deriving Repr, DecidableEq

/-- Well-formed regime: instances respect form arity and datum bounds,
rules name admitted forms, requirements are ordered pairs of admitted data,
and every form has arity at least one. -/
def Regime.wf (r : Regime) : Prop :=
  (∀ p ∈ r.insts,
      p.1 < r.forms.length ∧
      p.2.length = r.forms.getD p.1 0 ∧
      ∀ a ∈ p.2, a < r.data) ∧
  (∀ f ∈ r.rules, f < r.forms.length) ∧
  (∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data) ∧
  (∀ a ∈ r.forms, 1 ≤ a)

/-- A context: a judgment form with slots, where `none` is a hole. -/
structure Ctx where
  form  : Nat
  slots : List (Option Nat)
deriving Repr, DecidableEq

/-- Plugging fills every hole with the same datum. -/
def plug (c : Ctx) (d : Nat) : Inst :=
  (c.form, c.slots.map (fun s => s.getD d))

/-- Derivability: membership in the admitted instances, or coverage by a
uniform all-tuples rule.  No other inference is admitted. -/
def derivable (r : Regime) (i : Inst) : Prop :=
  i ∈ r.insts ∨ i.1 ∈ r.rules

instance (r : Regime) (i : Inst) : Decidable (derivable r i) := by
  unfold derivable; infer_instance

/-- A slot is admissible when it is a hole or names an admitted datum. -/
def slotOk (n : Nat) : Option Nat → Prop
  | none => True
  | some x => x < n

instance (n : Nat) (s : Option Nat) : Decidable (slotOk n s) :=
  match s with
  | none => isTrue trivial
  | some x => Nat.decLt x n

/-- Well-formed context relative to a regime: the form is admitted, the
slot count matches the form's arity, at least one slot is a hole (a
context observes; a hole-free slot tuple is an instance, not a context —
matching the Python enumeration), and every filled slot names an admitted
datum. -/
def wfCtx (r : Regime) (c : Ctx) : Prop :=
  c.form < r.forms.length ∧
  c.slots.length = r.forms.getD c.form 0 ∧
  none ∈ c.slots ∧
  ∀ s ∈ c.slots, slotOk r.data s

instance (r : Regime) (c : Ctx) : Decidable (wfCtx r c) := by
  unfold wfCtx; infer_instance

/-- Observational collapse: no well-formed context separates the two data
by positive derivability. -/
def collapsed (r : Regime) (d d' : Nat) : Prop :=
  ∀ c : Ctx, wfCtx r c → (derivable r (plug c d) ↔ derivable r (plug c d'))

/-- Internal separability (the declared sense): some well-formed context
witnesses a difference in positive derivability.  Stated existentially so
that every separability proof carries its witness. -/
def separable (r : Regime) (d d' : Nat) : Prop :=
  ∃ c : Ctx, wfCtx r c ∧
    ¬ (derivable r (plug c d) ↔ derivable r (plug c d'))

/-- Separability contradicts collapse (constructively). -/
theorem separable_not_collapsed {r : Regime} {d d' : Nat}
    (h : separable r d d') : ¬ collapsed r d d' :=
  fun hc => h.elim fun c hc' => hc'.2 (hc c hc'.1)

/-! ## Admission events and replay -/

inductive Event where
  | supply       (token : Nat)
  | admitDatum
  | admitForm    (arity : Nat)
  | admitInst    (form : Nat) (args : List Nat)
  | admitRuleAll (form : Nat)
  | impose       (i j : Nat)
deriving Repr, DecidableEq

/-- One admission step.  `none` signals an ill-formed admission.  A bare
supply provably changes nothing (`supply_no_op`). -/
def stepE (r : Regime) : Event → Option Regime
  | .supply _ => some r
  | .admitDatum => some { r with data := r.data + 1 }
  | .admitForm a =>
      if 1 ≤ a then some { r with forms := r.forms ++ [a] } else none
  | .admitInst f args =>
      if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
          (∀ x ∈ args, x < r.data) then
        some { r with insts := insertNew r.insts (f, args) }
      else none
  | .admitRuleAll f =>
      if f < r.forms.length then
        some { r with rules := insertNew r.rules f }
      else none
  | .impose i j =>
      if i < j ∧ j < r.data then
        some { r with reqs := insertNew r.reqs (i, j) }
      else none

/-- Replay: fold the recorded history over a base regime.  All-or-nothing:
an ill-formed event poisons the whole history. -/
def replayE (h : List Event) (base : Regime) : Option Regime :=
  h.foldlM stepE base

/-! ## The Challenge 3 regimes

Reading L: only explicit retention admits; two data, no forms, no
instances, the imposed requirement.  Reading F: the initial inscription is
admitted at genesis; three data. -/

def R2L : Regime := ⟨2, [], [], [], [(0, 1)]⟩
def R2F : Regime := ⟨3, [], [], [], [(1, 2)]⟩

theorem R2L_wf : R2L.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [R2L]

theorem R2F_wf : R2F.wf := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [R2F]

/-! ## Reconstructed from the sealed `Inertia` module -/

/-- The genesis regime: nothing admitted. -/
def genesis : Regime := ⟨0, [], [], [], []⟩

/-- A bare supply changes no admitted state (supply is not admission). -/
theorem supply_no_op (r : Regime) (t : Nat) :
    stepE r (.supply t) = some r := rfl

/-- Nothing is derivable at genesis. -/
theorem genesis_underivable (i : Inst) : ¬ derivable genesis i := by
  intro h
  cases h with
  | inl h => cases h
  | inr h => cases h

/-- Nothing is derivable in any regime with no instances and no rules;
in particular no successor is generated internally: the only state
changes in the model are indexed by external events (`stepE`). -/
theorem underivable_of_empty (r : Regime) (hi : r.insts = [])
    (hr : r.rules = []) (i : Inst) : ¬ derivable r i := by
  intro h
  cases h with
  | inl h => rw [hi] at h; cases h
  | inr h => rw [hr] at h; cases h

/-- Key collapse lemma: with no admitted instances, derivability depends
only on the form, hence every pair of data is observationally collapsed
(uniform rules cannot separate). -/
theorem collapsed_of_no_insts (r : Regime) (hi : r.insts = [])
    (d d' : Nat) : collapsed r d d' := by
  intro c _
  constructor <;> intro h <;>
    cases h with
    | inl h => rw [hi] at h; cases h
    | inr h => exact Or.inr h

/-- Challenge 2 (reading L): the two admitted, externally distinct data are
observationally collapsed. -/
theorem R2L_collapsed : collapsed R2L 0 1 :=
  collapsed_of_no_insts R2L rfl 0 1

/-- Challenge 2 (reading F): all three pairs are collapsed. -/
theorem R2F_collapsed (d d' : Nat) : collapsed R2F d d' :=
  collapsed_of_no_insts R2F rfl d d'

/-- The recorded Challenge 0-3 history of reading L replays exactly to the
Challenge 3 regime (replayability of the admitted state). -/
theorem historyL_replays :
    replayE
      [.supply 0, .supply 1, .supply 1, .supply 2,
       .admitDatum, .admitDatum, .impose 0 1] genesis = some R2L := by
  decide

/-- Reading F likewise. -/
theorem historyF_replays :
    replayE
      [.supply 0, .admitDatum, .supply 1, .supply 1, .supply 2,
       .admitDatum, .admitDatum, .impose 1 2] genesis = some R2F := by
  decide

/-- Non-increase countermodel: admitting a fresh datum is a real admission
(the state changes) yet the previously collapsed pair stays collapsed —
a new external inscription does not necessarily increase internal
expressive power. -/
theorem admission_without_expressive_increase :
    ∃ s, stepE R2L .admitDatum = some s ∧ s ≠ R2L ∧ collapsed s 0 1 := by
  refine ⟨⟨3, [], [], [], [(0, 1)]⟩, by decide, by decide, ?_⟩
  exact collapsed_of_no_insts _ rfl 0 1

/-- Replay is compositional: a history extended by one event replays by
stepping the replayed prefix. -/
theorem replayE_append (h : List Event) (e : Event) (base : Regime) :
    replayE (h ++ [e]) base =
      (replayE h base).bind (fun r => stepE r e) := by
  unfold replayE
  induction h generalizing base with
  | nil =>
      cases hse : stepE base e <;> simp [List.foldlM, hse]
  | cons x xs ih =>
      simp only [List.cons_append, List.foldlM]
      cases stepE base x <;> simp [ih]

end Sealed
end SecondRun
