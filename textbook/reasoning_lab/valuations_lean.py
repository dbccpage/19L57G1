"""Exact P204 source and scoped book arithmetic; AuthorityEffect: None."""
import re
from .valuations import ROOT,LEAN_SOURCE
OWNER_SUFFIXES='''qval_eqv_refl qval_eqv_symm qval_mul_comm qval_add_comm half_plus_half_eqv_one
quarter_plus_quarter_eqv_half eval2_unit_effect eval2_zero_effect state2_normalization_preserved
eval2_linearity_state eval2_linearity_effect eval2_joint_bilinearity classical_simplex_unique_decomposition
sq_decomp1_p0_eqv sq_decomp1_p1_eqv sq_decomp1_p2_eqv sq_decomp1_p3_eqv sq_decomp2_p0_eqv
sq_decomp2_p1_eqv sq_decomp2_p2_eqv sq_decomp2_p3_eqv sq_weights_distinct non_signaling_term
operational_non_signaling_bipartite operational_non_signaling_symmetric'''.split()
OWNER_NAMES=tuple('P204OperationalValuations.'+n for n in OWNER_SUFFIXES)
BOOK_NAMES=tuple('Textbook.Valuations.'+n for n in ('natural_endpoints','bounded_pairing',
    'common_mass_unit','common_mass_mixture','eqv_not_literal','square_not_raw_center',
    'corner_weights','coordinated_choice_diff','selection_vs_sum'))
BOOK=r'''
namespace Textbook.Valuations
open P204OperationalValuations

theorem natural_endpoints (a b : Nat) (h : a+b=1) :
    (a=0 ∧ b=1) ∨ (a=1 ∧ b=0) := by
  cases a with
  | zero => exact Or.inl ⟨rfl,by simpa only [Nat.zero_add] using h⟩
  | succ a =>
    have ha : a=0 := by omega
    have hb : b=0 := by omega
    exact Or.inr ⟨congrArg Nat.succ ha,hb⟩

theorem bounded_pairing (e : Effect2) (s : State2) (d : Nat)
    (h0 : e.w0 ≤ d) (h1 : e.w1 ≤ d) : eval2 e s ≤ d*(s.p0+s.p1) := by
  rw [eval2,Nat.mul_add]
  exact Nat.add_le_add (Nat.mul_le_mul_right s.p0 h0) (Nat.mul_le_mul_right s.p1 h1)

theorem common_mass_unit (s : State2) (state_total : Nat) (h : s.p0+s.p1=state_total) :
    eval2 unitEffect2 s = state_total := (eval2_unit_effect s).trans h

theorem common_mass_mixture (a b total state_total : Nat) (s t : State2)
    (hw : a+b=total) (hs : s.p0+s.p1=state_total) (ht : t.p0+t.p1=state_total) :
    (a*s.p0+b*t.p0)+(a*s.p1+b*t.p1)=total*state_total := by
  calc
    _ = (a*s.p0+a*s.p1)+(b*t.p0+b*t.p1) := by ac_rfl
    _ = a*(s.p0+s.p1)+b*(t.p0+t.p1) := by rw [Nat.mul_add,Nat.mul_add]
    _ = total*state_total := by rw [hs,ht,← Nat.add_mul,hw]

theorem eqv_not_literal :
    QVal.eqv QVal.half (⟨2,4,by decide⟩ : QVal) ∧
      QVal.half ≠ (⟨2,4,by decide⟩ : QVal) := by
  constructor
  · rfl
  · intro h
    have bad := congrArg QVal.num h
    exact (by decide : (1 : Nat) ≠ 2) bad

theorem square_not_raw_center :
    QVal.eqv sq_decomp1.p0 sq_center.p0 ∧ sq_decomp1.p0 ≠ sq_center.p0 := by
  constructor
  · rfl
  · intro h
    have bad := congrArg QVal.num h
    exact (by decide : (2 : Nat) ≠ 1) bad

/-- Nonnegative integer coefficients at a shared denominator; zero coordinates
    force each listed corner's representation to use only that corner. -/
theorem corner_weights (a b c d total : Nat) (h : a+b+c+d=total) :
    ((b+c=0 ∧ c+d=0) → a=total ∧ b=0 ∧ c=0 ∧ d=0) ∧
    ((a+d=0 ∧ c+d=0) → b=total ∧ a=0 ∧ c=0 ∧ d=0) ∧
    ((a+d=0 ∧ a+b=0) → c=total ∧ a=0 ∧ b=0 ∧ d=0) ∧
    ((b+c=0 ∧ a+b=0) → d=total ∧ a=0 ∧ b=0 ∧ c=0) := by
  refine ⟨?_,?_,?_,?_⟩
  all_goals
    intro hz
    obtain ⟨h1,h2⟩ := hz
    refine ⟨?_,?_,?_,?_⟩ <;> omega

theorem coordinated_choice_diff :
    QVal.eqv (⟨2,4,by decide⟩ : QVal) QVal.half ∧ ¬ QVal.eqv QVal.half QVal.one := by
  exact ⟨rfl,by change ¬ ((1 : Nat)*1=1*2); decide⟩

theorem selection_vs_sum :
    QVal.eqv (⟨1,2,by decide⟩ : QVal) QVal.half ∧ ¬ QVal.eqv QVal.half QVal.one := by
  exact ⟨rfl,by change ¬ ((1 : Nat)*1=1*2); decide⟩

end Textbook.Valuations
'''

def build_checks():
    text=(ROOT/LEAN_SOURCE).read_text(encoding='utf-8')
    if 'import ' in text or re.findall(r'^theorem (\w+)',text,re.M)!=OWNER_SUFFIXES:
        raise ValueError('Review changed P204 source/import/report population')
    assert len(OWNER_NAMES)==25 and len(BOOK_NAMES)==9
    names=(*OWNER_NAMES,*BOOK_NAMES)
    return text+'\n'+BOOK+'\n'+'\n'.join('#print axioms '+n for n in names),names

def expected_reports():
    both={'qval_mul_comm','state2_normalization_preserved','eval2_linearity_state','eval2_linearity_effect',
          'eval2_joint_bilinearity','non_signaling_term','operational_non_signaling_bipartite',
          'operational_non_signaling_symmetric','natural_endpoints','common_mass_mixture','corner_weights'}
    return {n:'depends on axioms: [propext, Quot.sound]' if n.rsplit('.',1)[1] in both
            else 'does not depend on any axioms' for n in (*OWNER_NAMES,*BOOK_NAMES)}
