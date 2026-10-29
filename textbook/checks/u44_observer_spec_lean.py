"""Check the specification/decider distinction and reader table; AuthorityEffect: None."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from booklean import main, NONE, PROPEXT  # noqa: E402

SOURCE=r'''
import Derivation.ObsDescent
namespace Textbook.ObserverSpec
open DiffInterface Compression

def flagObserver (P : Prop) : DiffObs Bool (Bool × Bool) where
  delta x y := (x,y)
  Zero pair := pair.1 = pair.2 ∨ P
  zero_refl _ := Or.inl rfl
  zero_symm := by
    intro x y h
    rcases h with heq | hp
    · exact Or.inl heq.symm
    · exact Or.inr hp
  zero_trans := by
    intro x y z hxy hyz
    rcases hxy with hxy | hp
    · rcases hyz with hyz | hp
      · exact Or.inl (hxy.trans hyz)
      · exact Or.inr hp
    · exact Or.inr hp

theorem cross_zero_iff (P : Prop) :
    ZeroRel (flagObserver P) false true ↔ P := by
  simp [ZeroRel,flagObserver]

def deciderForP (P : Prop)
    (h : Decidable (ZeroRel (flagObserver P) false true)) : Decidable P :=
  match h with
  | isTrue hz => isTrue ((cross_zero_iff P).mp hz)
  | isFalse hn => isFalse (fun hp => hn ((cross_zero_iff P).mpr hp))

def stored (x : Nat) : Nat := ([0,0,1] : List Nat).getD x 0
def requested (x : Nat) : Nat := ([0,1,1] : List Nat).getD x 0

theorem table_all_blocked : ¬ FactorsOn [0,1,2] stored requested := by
  intro ⟨g,h⟩
  have ha := h 0 (by simp)
  have hb := h 1 (by simp)
  change g 0 = 0 at ha
  change g 0 = 1 at hb
  exact Nat.noConfusion (ha.symm.trans hb)

theorem table_small_factors : FactorsOn [0,2] stored requested := by
  refine ⟨id, ?_⟩
  intro x hx
  simp at hx
  rcases hx with rfl | rfl <;> rfl

def activeStage : Stage Bool (Bool × Bool) where
  live _ := True
  retained _ _ := True
  guarded _ _ := True
  obs := kernelObs (fun _ : Bool => false)

theorem generic_closed_can_keep_active :
    drive (P := Unit) (fun _ : Stage Bool (Bool × Bool) => none) 1 activeStage
      = .closed activeStage ∧ ActiveObstruction activeStage false true := by
  exact ⟨rfl, trivial, rfl, trivial⟩

def idleClosure {X R : Type} (S : Stage X R) (G : StageMaps S) : ClosureStep S G where
  D _ _ := False
  demands_active := fun _ _ h => False.elim h
  demand_offdiag := fun _ _ h => False.elim h
  map_saturated := ⟨fun _ _ h => False.elim h, fun _ _ _ _ h => False.elim h⟩
  obs' := S.obs
  refines := fun _ _ h => h
  discharges := fun _ _ h => False.elim h

theorem idle_changes_nothing {X R : Type} (S : Stage X R) (G : StageMaps S) :
    (idleClosure S G).apply = S := rfl

end Textbook.ObserverSpec
'''

if __name__=='__main__':
    names=['flagObserver','cross_zero_iff','deciderForP','table_all_blocked','table_small_factors',
           'generic_closed_can_keep_active','idleClosure','idle_changes_nothing']
    expected={'Textbook.ObserverSpec.'+n:PROPEXT for n in names}
    expected['Textbook.ObserverSpec.flagObserver']=NONE
    expected['Textbook.ObserverSpec.generic_closed_can_keep_active']=NONE
    expected['Textbook.ObserverSpec.idleClosure']=NONE
    expected['Textbook.ObserverSpec.idle_changes_nothing']=NONE
    for name in names:
        SOURCE+='\n#print axioms Textbook.ObserverSpec.'+name
    raise SystemExit(main(SOURCE,expected,'ObserverSpec'))
