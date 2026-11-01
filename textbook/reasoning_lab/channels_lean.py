"""Unmodified X300 deterministic source and separate book row algebra."""
import re
from .channels import ROOT,LEAN_SOURCE
OWNER_SUFFIXES='''channel_compose_assoc channel_compose_id_left channel_compose_id_right
post_processing_coarse_graining dpi_distinguishability dpi_mutual_distinction dpi_decodability
invertible_postprocessing_preserves_distinctions hartley_capacity_additive state_space_multiplicative
coarse_graining_capacity_monotonic uniform_1bit_scaled_entropy uniform_2bit_scaled_entropy
memory_retention_monotone erasure_collapses_states erasure_strictly_non_reversible erasure_image_singleton'''.split()
BOOK=r'''
namespace Textbook.Channels
structure BinMat where
  a : Nat
  b : Nat
  c : Nat
  d : Nat
deriving DecidableEq

def compose (f g : BinMat) : BinMat :=
  ⟨f.a*g.a+f.b*g.c, f.a*g.b+f.b*g.d,
   f.c*g.a+f.d*g.c, f.c*g.b+f.d*g.d⟩

theorem row_associativity (f g h : BinMat) : compose (compose f g) h = compose f (compose g h) := by
  cases f; cases g; cases h
  simp only [compose, BinMat.mk.injEq, Nat.mul_add, Nat.add_mul]
  constructor
  · ac_rfl
  constructor
  · ac_rfl
  constructor <;> ac_rfl

theorem row_totals (f g : BinMat) (D E : Nat)
    (hf0 : f.a+f.b=D) (hf1 : f.c+f.d=D)
    (hg0 : g.a+g.b=E) (hg1 : g.c+g.d=E) :
    (compose f g).a+(compose f g).b=D*E ∧
    (compose f g).c+(compose f g).d=D*E := by
  constructor
  · change (f.a*g.a+f.b*g.c)+(f.a*g.b+f.b*g.d)=D*E
    calc
      _ = f.a*(g.a+g.b)+f.b*(g.c+g.d) := by simp only [Nat.mul_add]; ac_rfl
      _ = D*E := by rw [hg0,hg1,← Nat.add_mul,hf0]
  · change (f.c*g.a+f.d*g.c)+(f.c*g.b+f.d*g.d)=D*E
    calc
      _ = f.c*(g.a+g.b)+f.d*(g.c+g.d) := by simp only [Nat.mul_add]; ac_rfl
      _ = D*E := by rw [hg0,hg1,← Nat.add_mul,hf1]

def flip : Bool → Bool := Bool.not
def reset (_ : Bool) : Bool := false
theorem swapping_changes_output : reset (flip false) ≠ flip (reset false) := by decide

def keepRows : BinMat := ⟨1,0,0,1⟩
def flipRows : BinMat := ⟨0,1,1,0⟩
def balanced (m : BinMat) : Nat × Nat := (m.a+m.c,m.b+m.d)
theorem balanced_not_channel_identity : balanced keepRows = balanced flipRows ∧ keepRows ≠ flipRows := by decide

theorem equal_records_stay_equal {Ω B C : Type} (Y : Ω → B) (g : B → C)
    (x y : Ω) (h : Y x = Y y) : g (Y x) = g (Y y) := congrArg g h

theorem recovery_on_reachable_image {Ω B C : Type} (Y : Ω → B) (g : B → C) (r : C → B)
    (h : ∀ x, r (g (Y x)) = Y x) (x y : Ω) (hne : Y x ≠ Y y) : g (Y x) ≠ g (Y y) := by
  intro heq
  apply hne
  calc
    Y x = r (g (Y x)) := (h x).symm
    _ = r (g (Y y)) := congrArg r heq
    _ = Y y := h y

theorem retained_copy (x : Bool) : (false,x).2 = x := rfl
end Textbook.Channels
'''
BOOK_SUFFIXES='row_associativity row_totals swapping_changes_output balanced_not_channel_identity equal_records_stay_equal recovery_on_reachable_image retained_copy'.split()
NAMES=tuple('X300ObserverInformation.'+n for n in OWNER_SUFFIXES)+tuple('Textbook.Channels.'+n for n in BOOK_SUFFIXES)
def build_checks():
    text=(ROOT/LEAN_SOURCE).read_text(encoding='utf-8')
    if re.search(r'^import ',text,re.M) or re.findall(r'^theorem (\w+)',text,re.M)!=OWNER_SUFFIXES:
        raise ValueError('Review changed X300 imports/theorem population')
    return text+'\n'+BOOK+'\n'+'\n'.join('#print axioms '+n for n in NAMES),NAMES
def expected_reports():
    return {n:('depends on axioms: [propext, Quot.sound]' if n.rsplit('.',1)[1] in {'row_associativity','row_totals'}
               else 'depends on axioms: [propext]' if n.endswith('.state_space_multiplicative')
               else 'does not depend on any axioms') for n in NAMES}
