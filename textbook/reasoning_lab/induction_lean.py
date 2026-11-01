"""Book induction examples over admitted Nat/List and selected compiled owners."""
BOOK=r'''
namespace Textbook.Induction
open Derivation

def countAfter (base stride : Nat) : Nat → Nat
  | 0 => base
  | n+1 => countAfter base stride n + stride

theorem count_formula (base stride n : Nat) : countAfter base stride n = base+stride*n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change countAfter base stride n+stride=base+stride*(n+1)
      rw [ih,Nat.mul_succ,Nat.add_assoc]

def late (h n : Nat) : Nat := if n≤h then 2*n else 2*n+1

theorem finite_samples_not_all (h : Nat) :
    (∀ n, n≤h → late h n=2*n) ∧ ∃ n, late h n ≠ 2*n := by
  constructor
  · intro n hn; exact if_pos hn
  · refine ⟨h+1,?_⟩
    rw [late,if_neg (Nat.not_succ_le_self h)]
    exact Nat.succ_ne_self _

theorem start_needed : countAfter 1 2 0 ≠ 2*0 := by decide
theorem start_does_not_preserve : (false=false) ∧ Bool.not false ≠ false := by decide

def iterate {α : Type} (step : α → α) : Nat → α → α
  | 0,s => s
  | n+1,s => step (iterate step n s)

theorem preserved_along_run {α : Type} (step : α → α) (P : α → Prop) (s : α)
    (start : P s) (preserve : ∀ t, P t → P (step t)) (n : Nat) : P (iterate step n s) := by
  induction n with
  | zero => exact start
  | succ n ih => exact preserve _ ih

/-- The existing Unit 03 book argument, restated for this teaching route. -/
theorem supplies_hold (h : List Event) (hs : ∀ e ∈ h, ∃ t, e=Event.supply t) (r : Regime) :
    replayE h r=some r := by
  induction h with
  | nil => rfl
  | cons e rest ih =>
      obtain ⟨t,rfl⟩ := hs e (List.Mem.head rest)
      change replayE rest r=some r
      exact ih (fun e' he' => hs e' (List.Mem.tail _ he'))

theorem no_infinite_strict_bounded (f : Nat → Nat) (B : Nat)
    (strict : ∀ i, f i < f (i+1)) (bound : ∀ i, f i≤B) : False := by
  have hL : B+2≤B+1 := strict_bounded_length f (B+2) B (fun i _ => strict i) (fun i _ => bound i)
  exact Nat.not_succ_le_self (B+1) hL

theorem stationary_run (n : Nat) : iterate (fun x : Bool => x) n false=false := by
  induction n with
  | zero => rfl
  | succ n ih => exact ih
end Textbook.Induction
'''
NAMES=tuple('Textbook.Induction.'+n for n in ('count_formula','finite_samples_not_all','start_needed',
    'start_does_not_preserve','preserved_along_run','supplies_hold','no_infinite_strict_bounded','stationary_run'))
OWNER_NAMES=('Derivation.supply_no_op','Derivation.index_le_strict_mono','Derivation.strict_bounded_length')
SOURCE=BOOK+'\n'+'\n'.join('#print axioms '+n for n in (*NAMES,*OWNER_NAMES))
def expected_reports():
    return {n:('depends on axioms: [propext, Quot.sound]' if n in
               ('Textbook.Induction.no_infinite_strict_bounded',*OWNER_NAMES[1:])
               else 'depends on axioms: [propext]' if n in ('Textbook.Induction.supplies_hold',OWNER_NAMES[0])
               else 'does not depend on any axioms') for n in (*NAMES,*OWNER_NAMES)}
