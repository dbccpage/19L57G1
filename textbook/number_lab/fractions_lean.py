"""Book fraction identities over the already consumed QVal; AuthorityEffect: None."""
BOOK=r'''
namespace Textbook.Fractions
open P204OperationalValuations

theorem scale_equivalent (a b k : Nat) (hb : b>0) (hk : k>0) :
    QVal.eqv (⟨a,b,hb⟩ : QVal) (⟨a*k,b*k,Nat.mul_pos hb hk⟩ : QVal) := by
  show a*(b*k)=(a*k)*b
  ac_rfl

theorem add_common_denominator (a b d : Nat) (hd : d>0) :
    QVal.eqv ((⟨a,d,hd⟩ : QVal)+(⟨b,d,hd⟩ : QVal)) (⟨a+b,d,hd⟩ : QVal) := by
  show (a*d+b*d)*d=(a+b)*(d*d)
  rw [Nat.add_mul,Nat.add_mul]
  ac_rfl

theorem multiply_changed_case :
    QVal.eqv ((⟨2,3,by decide⟩ : QVal)*(⟨9,10,by decide⟩ : QVal))
      (⟨3,5,by decide⟩ : QVal) := rfl

/-- A supplied book quotient; the positive divisor numerator is essential. -/
def divide (a b : QVal) (hb : b.num>0) : QVal :=
  ⟨a.num*b.den,a.den*b.num,Nat.mul_pos a.den_pos hb⟩

theorem divide_cancels (a b : QVal) (hb : b.num>0) :
    QVal.eqv (divide a b hb * b) a := by
  show ((a.num*b.den)*b.num)*a.den=a.num*((a.den*b.num)*b.den)
  ac_rfl

theorem changed_sum :
    QVal.eqv ((⟨1,3,by decide⟩ : QVal)+QVal.quarter) (⟨7,12,by decide⟩ : QVal) := rfl

theorem changed_quotient :
    QVal.eqv (divide (⟨3,4,by decide⟩ : QVal) QVal.half (by decide))
      (⟨3,2,by decide⟩ : QVal) := rfl

theorem denominator_nonzero (a : QVal) : a.den ≠ 0 := Nat.ne_of_gt a.den_pos

end Textbook.Fractions
'''
NAMES=tuple('Textbook.Fractions.'+n for n in ('scale_equivalent','add_common_denominator',
    'multiply_changed_case','divide_cancels','changed_sum','changed_quotient','denominator_nonzero'))
SOURCE=BOOK+'\n'+'\n'.join('#print axioms '+n for n in NAMES)

def expected_reports():
    both={'scale_equivalent','add_common_denominator','divide_cancels'}
    return {n:'depends on axioms: [propext, Quot.sound]' if n.rsplit('.',1)[1] in both
            else 'does not depend on any axioms' for n in NAMES}
