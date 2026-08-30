import NaturalSections

/-!
# Hop fixture: two hard-core particles on a four-site graph

The first families with closed walks of length above one.  Objects are
sorted pairs `{x < y}` of occupied sites (unlabelled on purpose: the
labelled family is the cover, on which a section exists by
construction).  The carrier at every object is `Bool` with the sealed
`boolEqObs`, so the admissible pairs are the two orientations.  An arrow
is a hop of one particle to an adjacent site not occupied by the other;
its transport is the swap `negIso` exactly when the mover ends on the
far side of the stayer (`flipB`), else the identity.  The flip bit is
computed from the sorted positions, never tabulated.

Three site graphs on the same six objects, differing only in adjacency:
the open chain `0-1-2-3`, the square `0-1, 0-2, 1-3, 2-3`, and the star
with hub `0`.  Predictions were written into `STATUS.md` before the
Python computation ran; the theorems here carry the chain (a natural
section exists), the square, and the star (none exists) with the
Python's witness walks.  Nothing here names a physical system.
AuthorityEffect: None.
-/

namespace NaturalSections.Hop

open DiffInterface ContactKernel PresentationNaturality

/-- Whether `b` is one hop from `a`.  With `a = (x, y)` and `b = (x', y')`
sorted: the stayer keeps its index when `x' = x` and `y` moved, or
`y' = y` and `x` moved; it changes index when `y' = x` (`y` moved below
`x`) or `x' = y` (`x` moved above `y`). -/
def hopB (adj : Nat → Nat → Bool) (a b : Nat × Nat) : Bool :=
  (a.1 == b.1 && adj a.2 b.2) || (a.2 == b.2 && adj a.1 b.1) ||
    (b.2 == a.1 && adj a.2 b.1) || (b.1 == a.2 && adj a.1 b.2)

/-- The hop flips exactly in the last two cases: the mover passed the
stayer. -/
def flipB (adj : Nat → Nat → Bool) (a b : Nat × Nat) : Bool :=
  (b.2 == a.1 && adj a.2 b.1) || (b.1 == a.2 && adj a.1 b.2)

/-- The declared family of a site graph: carrier `Bool` everywhere, one
arrow per hop, transport the swap iff the hop flips. -/
def family (Obj : Type) (sites : Obj → Nat × Nat) (adj : Nat → Nat → Bool) :
    HFamily where
  Obj := Obj
  car _ := Bool
  res _ := Bool
  obs _ := boolEqObs
  Hom a b := PLift (hopB adj (sites a) (sites b) = true)
  iso a b _ :=
    match flipB adj (sites a) (sites b) with
    | true => negIso
    | false => PresIso.refl boolEqObs

/-- The six sorted pairs of four sites. -/
inductive Pair4 where
  | c01 | c02 | c03 | c12 | c13 | c23
  deriving DecidableEq, Repr

def Pair4.sites : Pair4 → Nat × Nat
  | .c01 => (0, 1)
  | .c02 => (0, 2)
  | .c03 => (0, 3)
  | .c12 => (1, 2)
  | .c13 => (1, 3)
  | .c23 => (2, 3)

/-! ## The open chain `0-1-2-3` -/

def chainAdj (u v : Nat) : Bool := (u + 1 == v) || (v + 1 == u)

def chainFamily : HFamily := family Pair4 Pair4.sites chainAdj

/-- The orientation "smaller site first", at every object. -/
def orient : HSec chainFamily := fun _ => boolEqPair

/-- On the chain no hop flips: the particles cannot pass. -/
theorem chain_no_hop_flips :
    ∀ a b : Pair4, hopB chainAdj a.sites b.sites = true →
      flipB chainAdj a.sites b.sites = false := by
  intro a b
  cases a <;> cases b <;> decide

/-- **The chain carries a natural section**: the constant orientation. -/
theorem chain_natural_section : HIsNatural chainFamily orient := by
  intro a b h
  show (match flipB chainAdj a.sites b.sites with
    | true => negIso
    | false => PresIso.refl boolEqObs).mapPair boolEqPair = boolEqPair
  rw [chain_no_hop_flips a b h.down]
  exact mapPair_refl boolEqObs boolEqPair

theorem chain_has_natural_section :
    ∃ s : HSec chainFamily, HIsNatural chainFamily s :=
  ⟨orient, chain_natural_section⟩

/-! ## The square `0-1, 0-2, 1-3, 2-3` -/

def squareAdj : Nat → Nat → Bool
  | 0, 1 | 1, 0 | 0, 2 | 2, 0 | 1, 3 | 3, 1 | 2, 3 | 3, 2 => true
  | _, _ => false

def squareFamily : HFamily := family Pair4 Pair4.sites squareAdj

def sqHop (a b : Pair4) (h : hopB squareAdj a.sites b.sites = true := by decide) :
    squareFamily.Hom a b :=
  ⟨h⟩

/-- The Python's witness: `{0,1} → {0,3} → {0,2} → {1,2} → {0,1}`; the last
hop moves `2` below `1`, so the walk flips once. -/
def sqWalk : Walk squareFamily .c01 .c01 :=
  .cons (.fwd (sqHop .c01 .c03))
    (.cons (.fwd (sqHop .c03 .c02))
      (.cons (.fwd (sqHop .c02 .c12))
        (.cons (.fwd (sqHop .c12 .c01)) .nil)))

/-- The closed walk transports every admissible pair to its swap. -/
theorem sqWalk_transport (p : NonZeroPair boolEqObs) :
    sqWalk.transport p = negIso.mapPair p := by
  apply Subtype.ext
  obtain ⟨⟨x, y⟩, _⟩ := p
  cases x <;> cases y <;> rfl

/-- **The square carries no natural section**: a natural section is fixed
by the closed walk (`Walk.transport_of_natural`), the walk is the swap,
and the swap fixes no admissible pair (the sealed
`negIso_fixed_point_free`). -/
theorem square_no_natural_section :
    ¬ ∃ s : HSec squareFamily, HIsNatural squareFamily s :=
  fun ⟨s, hs⟩ =>
    negIso_fixed_point_free (s .c01)
      ((sqWalk_transport (s .c01)).symm.trans (Walk.transport_of_natural hs sqWalk))

/-! ## The star with hub `0` -/

def starAdj : Nat → Nat → Bool
  | 0, 1 | 1, 0 | 0, 2 | 2, 0 | 0, 3 | 3, 0 => true
  | _, _ => false

def starFamily : HFamily := family Pair4 Pair4.sites starAdj

def stHop (a b : Pair4) (h : hopB starAdj a.sites b.sites = true := by decide) :
    starFamily.Hom a b :=
  ⟨h⟩

/-- The Python's witness: six hops through the hub, flipping three times. -/
def stWalk : Walk starFamily .c01 .c01 :=
  .cons (.fwd (stHop .c01 .c13))
    (.cons (.fwd (stHop .c13 .c03))
      (.cons (.fwd (stHop .c03 .c23))
        (.cons (.fwd (stHop .c23 .c02))
          (.cons (.fwd (stHop .c02 .c12))
            (.cons (.fwd (stHop .c12 .c01)) .nil)))))

theorem stWalk_transport (p : NonZeroPair boolEqObs) :
    stWalk.transport p = negIso.mapPair p := by
  apply Subtype.ext
  obtain ⟨⟨x, y⟩, _⟩ := p
  cases x <;> cases y <;> rfl

/-- **The star carries no natural section** either: a tree in the site
graph, but the particles can trade places through the hub. -/
theorem star_no_natural_section :
    ¬ ∃ s : HSec starFamily, HIsNatural starFamily s :=
  fun ⟨s, hs⟩ =>
    negIso_fixed_point_free (s .c01)
      ((stWalk_transport (s .c01)).symm.trans (Walk.transport_of_natural hs stWalk))

/-- **The separation.**  Same six objects, same carriers, same admissible
pairs, same hop rule; only the site adjacency differs, and that alone
decides whether a natural section exists. -/
theorem chain_square_star_separation :
    (∃ s : HSec chainFamily, HIsNatural chainFamily s) ∧
      (¬ ∃ s : HSec squareFamily, HIsNatural squareFamily s) ∧
      ¬ ∃ s : HSec starFamily, HIsNatural starFamily s :=
  ⟨chain_has_natural_section, square_no_natural_section, star_no_natural_section⟩

end NaturalSections.Hop
