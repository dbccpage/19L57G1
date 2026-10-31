"""Selected exact P201 bodies and book examples; AuthorityEffect: None."""
from .calibration import ROOT,LEAN_SOURCE

OWNER_NAMES=tuple('P201RelationalSpacetime.'+n for n in (
    'rescale_unit','dimensionless_cross_prod','dimensionless_ratio_invariant','cross_dimension_disjoint'))
BOOK_NAMES=tuple('Textbook.Calibration.'+n for n in (
    'rescaled_den_positive','ratio_den_positive','magnitude_cross_identity',
    'larger_unit_fewer_counts','mixed_units_cross_pair','ratio_not_unique','zero_divisor_cross_pair'))
BOOK=r'''
namespace Textbook.Calibration
open P201RelationalSpacetime

theorem rescaled_den_positive {d : Dimension} (q : Quantity d) (a b : Nat)
    (ha : a > 0) (hb : b > 0) : (rescale_unit q a b ha hb).den > 0 :=
  (rescale_unit q a b ha hb).den_pos

theorem ratio_den_positive {d : Dimension} (q1 q2 : Quantity d)
    (h : q2.num > 0) : (dimensionless_cross_prod q1 q2).2 > 0 :=
  Nat.mul_pos q1.den_pos h

theorem magnitude_cross_identity {d : Dimension} (q : Quantity d)
    (a b base_num base_den : Nat) (ha : a > 0) (hb : b > 0) :
    let changed := rescale_unit q a b ha hb
    (changed.num * (base_num * a)) * (q.den * base_den) =
      (q.num * base_num) * (changed.den * (base_den * b)) := by
  dsimp [rescale_unit]
  ac_rfl

def six : Quantity .length := ⟨6,1,by decide⟩
def eighteen : Quantity .length := ⟨18,1,by decide⟩
def zero : Quantity .length := ⟨0,1,by decide⟩

theorem larger_unit_fewer_counts :
    let changed := rescale_unit six 2 1 (by decide) (by decide)
    changed.num = 6 ∧ changed.den = 2 ∧ changed.num = 3 * changed.den := by decide

theorem mixed_units_cross_pair :
    dimensionless_cross_prod six (rescale_unit eighteen 2 1 (by decide) (by decide)) = (12,18) := by decide

theorem ratio_not_unique : (6 : Nat) * 18 = 12 * 9 ∧ (6 : Nat) ≠ 12 := by decide

theorem zero_divisor_cross_pair : dimensionless_cross_prod six zero = (6,0) := by decide

end Textbook.Calibration
'''


def build_checks():
    text=(ROOT/LEAN_SOURCE).read_text(encoding='utf-8')
    marker='-- ----------------------------------------------------------------------------\n-- P202:'
    if text.count(marker)!=1 or 'import ' in text:
        raise ValueError('P201 selected source boundary/imports need review')
    selected=text.split(marker)[0]+'\nend P201RelationalSpacetime\n'
    names=(*OWNER_NAMES,*BOOK_NAMES)
    return selected+'\n'+BOOK+'\n'+'\n'.join('#print axioms '+n for n in names),names


def expected_reports():
    none='does not depend on any axioms';both='depends on axioms: [propext, Quot.sound]'
    return {n:both if n.endswith(('dimensionless_ratio_invariant','magnitude_cross_identity')) else none
            for n in (*OWNER_NAMES,*BOOK_NAMES)}
