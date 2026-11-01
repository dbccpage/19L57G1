"""Exact P202 source bodies and scoped book claims; AuthorityEffect: None."""
from .clocks import ROOT,LEAN_SOURCE

OWNER_NAMES=tuple('P201RelationalSpacetime.'+n for n in (
    'future_equiv_refl','future_equiv_symm','future_equiv_trans','step_k_succ',
    'future_equiv_step_congruence','step_k_fast','step_k_slow','relational_clock_ratio'))
BOOK_NAMES=tuple('Textbook.Clocks.'+n for n in (
    'readout_step_depends','future_iff_current_readout','hidden_clocks_invisible',
    'positive_slow_change','zero_steps_zero_changes','offsets_not_elapsed_ratio',
    'countdown_horizon_countermodel','bounded_step_shift'))
BOOK=r'''
namespace Textbook.Clocks
open P201RelationalSpacetime

theorem readout_step_depends {s t : CarrierState} (h : readout s = readout t) :
    readout (step s) = readout (step t) := by
  exact Prod.ext (congrArg (fun p : Nat × Nat => p.1 + 1) h)
    (congrArg (fun p : Nat × Nat => p.2 + 1) h)

theorem future_iff_current_readout (s t : CarrierState) :
    FutureEquiv s t ↔ readout s = readout t := by
  constructor
  · intro h
    exact h 0
  · intro h k
    induction k generalizing s t with
    | zero => exact h
    | succ k ih => exact ih (step s) (step t) (readout_step_depends h)

def visibleSame : CarrierState := ⟨2,3,0,0⟩
def clockDifferent : CarrierState := ⟨2,3,10,7⟩

theorem hidden_clocks_invisible :
    FutureEquiv visibleSame clockDifferent ∧ visibleSame ≠ clockDifferent := by
  constructor
  · exact (future_iff_current_readout _ _).mpr rfl
  · intro h
    have bad := congrArg CarrierState.clock_fast h
    exact (by decide : (0 : Nat) ≠ 10) bad

theorem positive_slow_change (s : CarrierState) (k : Nat) (hk : k > 0) :
    (step_k k s).clock_slow - s.clock_slow > 0 := by
  rw [step_k_slow]
  omega

theorem zero_steps_zero_changes (s : CarrierState) :
    (step_k 0 s).clock_fast - s.clock_fast = 0 ∧
      (step_k 0 s).clock_slow - s.clock_slow = 0 := by
  exact ⟨Nat.sub_self s.clock_fast,Nat.sub_self s.clock_slow⟩

def offsetStart : CarrierState := ⟨2,3,10,3⟩
theorem offsets_not_elapsed_ratio :
    (step_k 2 offsetStart).clock_fast = 14 ∧
    (step_k 2 offsetStart).clock_slow = 5 ∧
    (14 : Nat) ≠ 2 * 5 ∧
    (step_k 2 offsetStart).clock_fast - offsetStart.clock_fast =
      2 * ((step_k 2 offsetStart).clock_slow - offsetStart.clock_slow) := by decide

/-- A separate supplied countdown, not the P202 transition or readout. -/
def lamp (remaining : Nat) : Nat := if remaining = 0 then 1 else 0

theorem countdown_horizon_countermodel (horizon : Nat) :
    (∀ k, k < horizon → lamp (horizon-k) = lamp (horizon+1-k)) ∧
      lamp (horizon-horizon) ≠ lamp (horizon+1-horizon) := by
  constructor
  · intro k hk
    have a : horizon-k ≠ 0 := by omega
    have b : horizon+1-k ≠ 0 := by omega
    simp [lamp,a,b]
  · have a : horizon-horizon = 0 := by omega
    have b : horizon+1-horizon = 1 := by omega
    simp [lamp,a,b]

theorem bounded_step_shift (s t : CarrierState) (horizon : Nat)
    (h : ∀ k, k < horizon+1 → readout (step_k k s) = readout (step_k k t)) :
    ∀ k, k < horizon → readout (step_k k (step s)) = readout (step_k k (step t)) := by
  intro k hk
  exact h (k+1) (by omega)

end Textbook.Clocks
'''


def build_checks():
    text=(ROOT/LEAN_SOURCE).read_text(encoding='utf-8')
    marker='structure CarrierState where\n'
    if text.count(marker)!=1 or not text.endswith('end P201RelationalSpacetime\n') or 'import ' in text:
        raise ValueError('P202 selected source boundary/imports need review')
    selected='namespace P201RelationalSpacetime\n\n'+marker+text.split(marker)[1]
    names=(*OWNER_NAMES,*BOOK_NAMES)
    return selected+'\n'+BOOK+'\n'+'\n'.join('#print axioms '+n for n in names),names


def expected_reports():
    both={'step_k_fast','step_k_slow','relational_clock_ratio','positive_slow_change',
          'countdown_horizon_countermodel','bounded_step_shift'}
    return {n:'depends on axioms: [propext, Quot.sound]' if n.rsplit('.',1)[1] in both
            else 'does not depend on any axioms' for n in (*OWNER_NAMES,*BOOK_NAMES)}
