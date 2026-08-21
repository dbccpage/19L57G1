import Derivation.PresentationNaturality

namespace PrimitiveDifferenceTower

/-
This is a separate declared finite fixture, not an instance of
`Derivation.DiffInterface.Stage`.  Its two labelled seed points, seed
distinction, anchor, fresh-point convention, stage grammar, closure rule, and
replay moves are data of the fixture.  The results below do not construct such
data from an arbitrary input witness or identify the counter below with a
native active-obstruction predicate.
-/

abbrev Point (n : Nat) : Type := Fin (n + 2)

abbrev Map (n m : Nat) : Type := Point n → Point m

def anchorLeft (n : Nat) : Point n := ⟨0, by omega⟩

def anchorRight (n : Nat) : Point n := ⟨1, by omega⟩

theorem anchors_distinct (n : Nat) : anchorLeft n ≠ anchorRight n := by
  intro h
  have hval : (0 : Nat) = 1 := congrArg Fin.val h
  omega

def freshPoint (n : Nat) : Point (n + 1) := ⟨n + 2, by omega⟩

def upPoint {n : Nat} (x : Point n) : Point (n + 1) :=
  ⟨x.val, by omega⟩

def downPoint (n : Nat) (x : Point (n + 1)) : Point n :=
  if h : x.val < n + 2 then ⟨x.val, h⟩ else anchorLeft n

theorem down_upPoint (n : Nat) (x : Point n) :
    downPoint n (upPoint x) = x := by
  apply Fin.ext
  simp [downPoint, upPoint, x.isLt]

theorem fresh_not_in_upPoint_image (n : Nat) (x : Point n) :
    upPoint x ≠ freshPoint n := by
  intro h
  have hval : x.val = n + 2 := congrArg Fin.val h
  omega

theorem down_freshPoint (n : Nat) :
    downPoint n (freshPoint n) = anchorLeft n := by
  simp [downPoint, freshPoint]

theorem up_anchorLeft (n : Nat) :
    upPoint (anchorLeft n) = anchorLeft (n + 1) := by
  apply Fin.ext
  rfl

theorem up_anchorRight (n : Nat) :
    upPoint (anchorRight n) = anchorRight (n + 1) := by
  apply Fin.ext
  rfl

def idMap (n : Nat) : Map n n := fun x => x

def compose {n m k : Nat} (g : Map m k) (f : Map n m) : Map n k :=
  fun x => g (f x)

def upMap {n m : Nat} (f : Map n m) : Map (n + 1) (m + 1) :=
  fun x =>
    if h : x.val < n + 2 then upPoint (f ⟨x.val, h⟩) else freshPoint m

def towerUpObject (n : Nat) : Nat := n + 1

def rawTowerUpMorphism {n m : Nat} (f : Map n m) :
    Map (towerUpObject n) (towerUpObject m) := upMap f

theorem upMap_on_old {n m : Nat} (f : Map n m) (x : Point n) :
    upMap f (upPoint x) = upPoint (f x) := by
  simp [upMap, upPoint, x.isLt]

theorem upMap_on_fresh {n m : Nat} (f : Map n m) :
    upMap f (freshPoint n) = freshPoint m := by
  simp [upMap, freshPoint]

theorem point_old_or_fresh {n : Nat} (x : Point (n + 1)) :
    (∃ y : Point n, x = upPoint y) ∨ x = freshPoint n := by
  by_cases h : x.val < n + 2
  · left
    refine ⟨⟨x.val, h⟩, ?_⟩
    apply Fin.ext
    rfl
  · right
    apply Fin.ext
    simp only [freshPoint, Fin.val_mk]
    omega

theorem upMap_id (n : Nat) : upMap (idMap n) = idMap (n + 1) := by
  funext x
  rcases point_old_or_fresh x with ⟨y, rfl⟩ | rfl
  · simpa [idMap] using upMap_on_old (idMap n) y
  · simpa [idMap] using upMap_on_fresh (idMap n)

theorem upMap_comp {n m k : Nat} (g : Map m k) (f : Map n m) :
    upMap (compose g f) = compose (upMap g) (upMap f) := by
  funext x
  rcases point_old_or_fresh x with ⟨y, rfl⟩ | rfl
  · simp only [upMap_on_old, compose]
  · simp only [upMap_on_fresh, compose]

def clampedRestriction {n m : Nat} (g : Map (n + 1) (m + 1)) : Map n m :=
  fun x => downPoint m (g (upPoint x))

theorem clampedRestriction_upMap {n m : Nat} (f : Map n m) :
    clampedRestriction (upMap f) = f := by
  funext x
  unfold clampedRestriction
  rw [upMap_on_old]
  exact down_upPoint m (f x)

/-
`LiftedMap` is the restricted domain on which the named descent has an
explicit parent map.  `clampedRestriction` is a specified raw-map operation,
not that descent; its loss on the fresh point is recorded above.
-/
structure LiftedMap (n m : Nat) where
  raw : Map (n + 1) (m + 1)
  parent : Map n m
  raw_eq_up : raw = upMap parent

theorem LiftedMap.ext {n m : Nat} {f g : LiftedMap n m}
    (h : f.parent = g.parent) : f = g := by
  cases f with
  | mk rawF parentF hF =>
    cases g with
    | mk rawG parentG hG =>
      dsimp at h
      subst parentG
      subst rawF
      subst rawG
      rfl

def liftMap {n m : Nat} (f : Map n m) : LiftedMap n m where
  raw := upMap f
  parent := f
  raw_eq_up := rfl

def descendMap {n m : Nat} (f : LiftedMap n m) : Map n m := f.parent

def towerUpMorphism {n m : Nat} (f : Map n m) : LiftedMap n m := liftMap f

def towerDownMorphism {n m : Nat} (f : LiftedMap n m) : Map n m :=
  descendMap f

theorem towerUpMorphism_raw {n m : Nat} (f : Map n m) :
    (towerUpMorphism f).raw = rawTowerUpMorphism f := rfl

theorem towerUpMorphism_identity (n : Nat) :
    (towerUpMorphism (idMap n)).raw = idMap (towerUpObject n) :=
  upMap_id n

theorem towerUpMorphism_composition {n m k : Nat}
    (g : Map m k) (f : Map n m) :
    (towerUpMorphism (compose g f)).raw =
      compose (towerUpMorphism g).raw (towerUpMorphism f).raw :=
  upMap_comp g f

theorem towerDown_after_towerUp {n m : Nat} (f : Map n m) :
    towerDownMorphism (towerUpMorphism f) = f := rfl

theorem descend_liftMap {n m : Nat} (f : Map n m) :
    descendMap (liftMap f) = f := rfl

theorem clampedRestriction_certified {n m : Nat} (f : LiftedMap n m) :
    clampedRestriction f.raw = descendMap f := by
  rw [f.raw_eq_up]
  exact clampedRestriction_upMap f.parent

def liftedId (n : Nat) : LiftedMap n n := liftMap (idMap n)

def liftedComp {n m k : Nat} (g : LiftedMap m k)
    (f : LiftedMap n m) : LiftedMap n k where
  raw := compose g.raw f.raw
  parent := compose g.parent f.parent
  raw_eq_up := by
    calc
      compose g.raw f.raw = compose (upMap g.parent) (upMap f.parent) := by
        rw [g.raw_eq_up, f.raw_eq_up]
      _ = upMap (compose g.parent f.parent) := (upMap_comp g.parent f.parent).symm

theorem descend_liftedId (n : Nat) :
    descendMap (liftedId n) = idMap n := rfl

theorem descend_liftedComp {n m k : Nat} (g : LiftedMap m k)
    (f : LiftedMap n m) :
    descendMap (liftedComp g f) = compose (descendMap g) (descendMap f) := rfl

theorem liftedComp_raw {n m k : Nat} (g : LiftedMap m k)
    (f : LiftedMap n m) :
    (liftedComp g f).raw = compose g.raw f.raw := rfl

theorem liftMap_comp {n m k : Nat} (g : Map m k) (f : Map n m) :
    liftedComp (liftMap g) (liftMap f) = liftMap (compose g f) := by
  apply LiftedMap.ext
  rfl

theorem towerUpMorphism_comp_certified {n m k : Nat}
    (g : Map m k) (f : Map n m) :
    liftedComp (towerUpMorphism g) (towerUpMorphism f) =
      towerUpMorphism (compose g f) :=
  liftMap_comp g f

inductive Move where
  | lift
  | discharge
deriving DecidableEq, Repr

structure DeclaredRoundStep (n : Nat) where
  carrierLift : Point n → Point (n + 1)
  carrierClamp : Point (n + 1) → Point n
  clamp_lift : ∀ x, carrierClamp (carrierLift x) = x
  fresh : Point (n + 1)
  fresh_not_old : ∀ x, carrierLift x ≠ fresh
  moves : List Move

def declaredRoundStep (n : Nat) : DeclaredRoundStep n where
  carrierLift := upPoint
  carrierClamp := downPoint n
  clamp_lift := down_upPoint n
  fresh := freshPoint n
  fresh_not_old := fresh_not_in_upPoint_image n
  moves := [.lift, .discharge]

structure ReplayState where
  level : Nat
  active : Nat
deriving DecidableEq, Repr

/- The `active` field is declared replay bookkeeping.  It is not connected
to the source interface's semantic obstruction predicate in this fixture. -/

def initialState : ReplayState := ⟨0, 0⟩

def advance (s : ReplayState) : Move → ReplayState
  | .lift => ⟨s.level + 1, 1⟩
  | .discharge => ⟨s.level, 0⟩

def replayFrom : ReplayState → List Move → ReplayState
  | s, [] => s
  | s, move :: moves => replayFrom (advance s move) moves

def replay (moves : List Move) : ReplayState := replayFrom initialState moves

theorem replayFrom_append (s : ReplayState) (xs ys : List Move) :
    replayFrom s (xs ++ ys) = replayFrom (replayFrom s xs) ys := by
  induction xs generalizing s with
  | nil => rfl
  | cons x xs ih =>
      simp only [List.cons_append, replayFrom]
      exact ih (advance s x)

def AnchorInvariant (s : ReplayState) : Prop :=
  anchorLeft s.level ≠ anchorRight s.level

theorem initial_anchorInvariant : AnchorInvariant initialState :=
  anchors_distinct 0

theorem advance_preserves_anchorInvariant (s : ReplayState) (move : Move) :
    AnchorInvariant (advance s move) := by
  cases move <;> exact anchors_distinct _

theorem replayFrom_preserves_anchorInvariant (s : ReplayState)
    (moves : List Move) : AnchorInvariant (replayFrom s moves) := by
  induction moves generalizing s with
  | nil => exact anchors_distinct _
  | cons move moves ih =>
      exact ih (advance s move)

theorem replay_preserves_anchorInvariant (moves : List Move) :
    AnchorInvariant (replay moves) :=
  replayFrom_preserves_anchorInvariant initialState moves

def activeMeasure (s : ReplayState) : Nat := s.active

theorem discharge_strictly_decreases (s : ReplayState) (h : s.active = 1) :
    activeMeasure (advance s .discharge) < activeMeasure s := by
  simp [activeMeasure, advance, h]

theorem lift_can_create_active :
    activeMeasure (advance initialState .lift) = 1 := rfl

theorem invariant_is_not_progress :
    AnchorInvariant (advance initialState .lift) ∧
      activeMeasure (advance initialState .lift) = 1 :=
  ⟨advance_preserves_anchorInvariant initialState .lift, lift_can_create_active⟩

def roundStep (n : Nat) : List Move := (declaredRoundStep n).moves

def rounds : Nat → List Move
  | 0 => []
  | n + 1 => rounds n ++ roundStep n

theorem rounds_succ (n : Nat) :
    rounds (n + 1) = rounds n ++ roundStep n := rfl

theorem replay_rounds_succ (n : Nat) :
    replay (rounds (n + 1)) =
      replayFrom (replay (rounds n)) (roundStep n) := by
  rw [rounds_succ, replay, replayFrom_append]
  rfl

theorem replay_rounds_closed (n : Nat) :
    activeMeasure (replay (rounds n)) = 0 := by
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [rounds, replay, replayFrom_append]
      simp [roundStep, declaredRoundStep, replayFrom, activeMeasure, advance]

theorem replay_rounds_level (n : Nat) :
    (replay (rounds n)).level = n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [rounds_succ, replay, replayFrom_append]
      change (replayFrom initialState (rounds n)).level + 1 = n + 1
      simpa [replay] using ih

theorem replay_rounds_preserve_anchor (n : Nat) :
    AnchorInvariant (replay (rounds n)) :=
  replay_preserves_anchorInvariant (rounds n)

def BoolSinglePairSelector : Prop :=
  ∃ s : PresentationNaturality.Sec
      (PresentationNaturality.autoFamily ContactKernel.boolEqObs
        PresentationNaturality.negIso),
    PresentationNaturality.IsNatural
      (PresentationNaturality.autoFamily ContactKernel.boolEqObs
        PresentationNaturality.negIso) s

theorem no_bool_single_pair_selector : ¬ BoolSinglePairSelector :=
  PresentationNaturality.no_natural_section_boolEq

theorem raw_bool_single_pair_selector_exists :
    Nonempty (PresentationNaturality.Sec
      (PresentationNaturality.autoFamily ContactKernel.boolEqObs
        PresentationNaturality.negIso)) :=
  PresentationNaturality.selection_is_possible_naturality_is_not.1

theorem collapsed_source_has_no_witness (a b : Bool) :
    ¬ ContactBridge.obsApart ObsDescent.collapseAllObs a b :=
  ContactKernel.kernel_no_witness_from_collapse a b

end PrimitiveDifferenceTower
