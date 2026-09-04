/-!
# The sealed kernel, reconstructed verbatim

PIN NOTE (whole file).  Every declaration below is reproduced VERBATIM
from the sealed modules `lean4/Derivation/Basic.lean` and
`lean4/Derivation/Inertia.lean` at the blobs recorded in
`SOURCE_MANIFEST.json`, at the snapshot recorded there.  The only changes
are the outer namespace, so that this package stays self-contained and
imports nothing sealed, and the doc comments, which are this file's own.
`verify_pins.py` recomputes the blob hash of each sealed source at the
snapshot and at HEAD and fails on any drift.

Why a reconstruction and not a dependency: the sealed package is not
declared as a Lake dependency by any research tree of this repository,
and the sibling `standing_commitment` reconstructs its slice the same
way.  The source policy is declared in `STATUS.md` before the first
compile: RECONSTRUCTION, with a pin note per group of definitions.

What a pin proves: that the sealed source did not move.  It does not
prove that this reconstruction is faithful; that is read by hand, and the
one mechanical check on it is that the reconstructed theorems elaborate
with the sealed proofs unchanged.

Reach: only the slice the theorems of this rung need.  The sealed
augmentation, response, and gate machinery is NOT reconstructed, because
this rung asks where a demand can come from, not how one is discharged.

AuthorityEffect: None.
-/

namespace SecondNoFirst
namespace Sealed

/-! ## Reconstructed from the sealed `Basic` module -/

/-- Judgment instance: a form index and an argument tuple of datum indices. -/
abbrev Inst := Nat × List Nat

/-- Deduplicating insertion: the admitted collections are sets, so
re-admission is a no-op. -/
def insertNew {α : Type} [DecidableEq α] (l : List α) (a : α) : List α :=
  if a ∈ l then l else l ++ [a]

theorem insertNew_of_not_mem {α : Type} [DecidableEq α] {l : List α}
    {a : α} (h : a ∉ l) : insertNew l a = l ++ [a] := by
  simp [insertNew, h]

theorem insertNew_of_mem {α : Type} [DecidableEq α] {l : List α}
    {a : α} (h : a ∈ l) : insertNew l a = l := by
  simp [insertNew, h]

/-- The admitted state: a count of admitted data (internal identity is the
index), a list of judgment-form arities, admitted judgment instances,
forms carrying the uniform all-tuples rule, and externally imposed
separation requirements. -/
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
slot count matches the form's arity, at least one slot is a hole, and
every filled slot names an admitted datum. -/
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
witnesses a difference in positive derivability. -/
def separable (r : Regime) (d d' : Nat) : Prop :=
  ∃ c : Ctx, wfCtx r c ∧
    ¬ (derivable r (plug c d) ↔ derivable r (plug c d'))

/-- Separability contradicts collapse (constructively). -/
theorem separable_not_collapsed {r : Regime} {d d' : Nat}
    (h : separable r d d') : ¬ collapsed r d d' :=
  fun hc => h.elim fun c hc' => hc'.2 (hc c hc'.1)

/-! ## Admission events and replay, reconstructed -/

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

/-! ## Reconstructed from the sealed `Inertia` module -/

/-- The genesis regime: nothing admitted. -/
def genesis : Regime := ⟨0, [], [], [], []⟩

/-- A bare supply changes no admitted state (supply is not admission).
This is the sealed theorem, reconstructed with its sealed proof unchanged;
it is cited in the ledger as the sealed theorem it is, not as a theorem of
this rung. -/
theorem supply_no_op (r : Regime) (t : Nat) :
    stepE r (.supply t) = some r := rfl

/-- Nothing is derivable at genesis. -/
theorem genesis_underivable (i : Inst) : ¬ derivable genesis i := by
  intro h
  cases h with
  | inl h => cases h
  | inr h => cases h

/-- Nothing is derivable in any regime with no instances and no rules. -/
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

end Sealed
end SecondNoFirst
