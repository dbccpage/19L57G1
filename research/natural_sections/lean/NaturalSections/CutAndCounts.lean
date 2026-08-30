import NaturalSections
import NaturalSections.HopFixture

/-!
# The cut theorem, and the blindness of counts

Two results on the two-label square, pre-registered in `STATUS.md`.

**The cut.**  `cutFamily` keeps the square's objects and exactly its
non-flipping hops, with the same transport rule.  The constant
orientation is then a natural section (`cut_natural_section`): removing
the two flipping arrows -- the minimum deletion, by the finite
computation of NS-44 -- trivialises the class.  `cut_theorem` states the
cut's section next to the square's obstruction.

**The counts.**  `coverFamily` keeps the square's objects AND all of its
arrows and sets every transport to the identity.  Its walks are the
square's walks: `reWalk` and `unWalk` are inverse, length-preserving
translations, so every closed-walk count agrees.  Yet the cover carries
a natural section and the square does not (`dynamics_blind_to_class`):
the walks a family generates -- and therefore every count of them --
cannot carry the class.  The class lives in the transports, and a count
sees it only when read in a convention (`count_eq_length_iff`).
AuthorityEffect: None.
-/

namespace NaturalSections

open DiffInterface ContactKernel PresentationNaturality

/-! ## 1. The cut -/

/-- The square with its two flipping hops deleted: arrows are exactly the
non-flipping hops, the transport rule unchanged. -/
def cutFamily : HFamily where
  Obj := Hop.Pair4
  car _ := Bool
  res _ := Bool
  obs _ := boolEqObs
  Hom a b := PLift ((Hop.hopB Hop.squareAdj a.sites b.sites
      && !Hop.flipB Hop.squareAdj a.sites b.sites) = true)
  iso a b _ :=
    match Hop.flipB Hop.squareAdj a.sites b.sites with
    | true => negIso
    | false => PresIso.refl boolEqObs

theorem cut_no_hop_flips :
    ∀ a b : Hop.Pair4,
      (Hop.hopB Hop.squareAdj a.sites b.sites
        && !Hop.flipB Hop.squareAdj a.sites b.sites) = true →
      Hop.flipB Hop.squareAdj a.sites b.sites = false := by
  intro a b
  cases a <;> cases b <;> decide

/-- The deleted arrows are exactly the flipping hops. -/
theorem cut_removes_exactly_the_flips :
    ∀ a b : Hop.Pair4,
      (Hop.hopB Hop.squareAdj a.sites b.sites = true ∧
          ¬ ((Hop.hopB Hop.squareAdj a.sites b.sites
            && !Hop.flipB Hop.squareAdj a.sites b.sites) = true)) ↔
        (Hop.hopB Hop.squareAdj a.sites b.sites = true ∧
          Hop.flipB Hop.squareAdj a.sites b.sites = true) := by
  intro a b
  cases a <;> cases b <;> decide

/-- **The cut carries a natural section**: the constant orientation. -/
theorem cut_natural_section : HIsNatural cutFamily (fun _ => boolEqPair) := by
  intro a b h
  show (match Hop.flipB Hop.squareAdj (Hop.Pair4.sites a) (Hop.Pair4.sites b) with
    | true => negIso
    | false => PresIso.refl boolEqObs).mapPair boolEqPair = boolEqPair
  rw [cut_no_hop_flips a b h.down]
  exact mapPair_refl boolEqObs boolEqPair

/-- **The cut theorem**: deleting the two flipping hops trivialises the
class the square cannot shed otherwise.  Minimality of the deletion is
finite computation (NS-44). -/
theorem cut_theorem :
    (∃ s : HSec cutFamily, HIsNatural cutFamily s) ∧
      ¬ ∃ s : HSec Hop.squareFamily, HIsNatural Hop.squareFamily s :=
  ⟨⟨fun _ => boolEqPair, cut_natural_section⟩, Hop.square_no_natural_section⟩

/-! ## 2. The cover, and the blindness of counts -/

/-- The square's objects and ALL of its arrows, every transport the
identity: the labelled configurations read through unlabelled ones. -/
def coverFamily : HFamily where
  Obj := Hop.Pair4
  car _ := Bool
  res _ := Bool
  obs _ := boolEqObs
  Hom a b := PLift (Hop.hopB Hop.squareAdj a.sites b.sites = true)
  iso _ _ _ := PresIso.refl boolEqObs

theorem cover_natural_section : HIsNatural coverFamily (fun _ => boolEqPair) :=
  fun _ _ _ => mapPair_refl boolEqObs boolEqPair

def Walk.length {D : HFamily} : {a b : D.Obj} → Walk D a b → Nat
  | _, _, .nil => 0
  | _, _, .cons _ w => w.length + 1

/-- The square's arrows ARE the cover's arrows, so its steps translate. -/
def reStep : {a b : Hop.Pair4} → Step Hop.squareFamily a b → Step coverFamily a b
  | _, _, .fwd h => .fwd h
  | _, _, .bwd h => .bwd h

def unStep : {a b : Hop.Pair4} → Step coverFamily a b → Step Hop.squareFamily a b
  | _, _, .fwd h => .fwd h
  | _, _, .bwd h => .bwd h

def reWalk : {a b : Hop.Pair4} → Walk Hop.squareFamily a b → Walk coverFamily a b
  | _, _, .nil => .nil
  | _, _, .cons s w => .cons (reStep s) (reWalk w)

def unWalk : {a b : Hop.Pair4} → Walk coverFamily a b → Walk Hop.squareFamily a b
  | _, _, .nil => .nil
  | _, _, .cons s w => .cons (unStep s) (unWalk w)

theorem unWalk_reWalk : ∀ {a b : Hop.Pair4} (w : Walk Hop.squareFamily a b),
    unWalk (reWalk w) = w
  | _, _, .nil => rfl
  | _, _, .cons s w => by
    show Walk.cons (unStep (reStep s)) (unWalk (reWalk w)) = Walk.cons s w
    rw [unWalk_reWalk w]
    cases s <;> rfl

theorem reWalk_unWalk : ∀ {a b : Hop.Pair4} (w : Walk coverFamily a b),
    reWalk (unWalk w) = w
  | _, _, .nil => rfl
  | _, _, .cons s w => by
    show Walk.cons (reStep (unStep s)) (reWalk (unWalk w)) = Walk.cons s w
    rw [reWalk_unWalk w]
    cases s <;> rfl

theorem reWalk_length : ∀ {a b : Hop.Pair4} (w : Walk Hop.squareFamily a b),
    (reWalk w).length = w.length
  | _, _, .nil => rfl
  | _, _, .cons s w => by
    show (reWalk w).length + 1 = w.length + 1
    rw [reWalk_length w]

/-- **Counts are blind to the class.**  The square and its cover share
their walks through an inverse pair of length-preserving translations,
so every closed-walk count agrees; the cover carries a natural section
and the square carries none.  What a family generates by itself cannot
carry its class; the class lives in the transports. -/
theorem dynamics_blind_to_class :
    (∀ {a b : Hop.Pair4} (w : Walk Hop.squareFamily a b),
        unWalk (reWalk w) = w ∧ (reWalk w).length = w.length) ∧
      (∀ {a b : Hop.Pair4} (w : Walk coverFamily a b), reWalk (unWalk w) = w) ∧
      (∃ s : HSec coverFamily, HIsNatural coverFamily s) ∧
      ¬ ∃ s : HSec Hop.squareFamily, HIsNatural Hop.squareFamily s :=
  ⟨fun w => ⟨unWalk_reWalk w, reWalk_length w⟩, fun w => reWalk_unWalk w,
   ⟨fun _ => boolEqPair, cover_natural_section⟩, Hop.square_no_natural_section⟩

end NaturalSections
