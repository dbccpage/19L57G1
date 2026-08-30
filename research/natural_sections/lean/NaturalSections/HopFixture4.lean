import NaturalSections
import NaturalSections.HopFixture

/-!
# Four-label hop fixture: nontrivial holonomy with a natural section

Four particles on the square `0-1, 0-2, 1-3, 2-3` plus a disjoint edge
`4-5`, in the configuration component where two particles sit on the
square and two fill the edge.  The edge particles cannot move (their
sites are both occupied and connect to nothing else) and their sites are
the largest, so they hold sorted indices `2` and `3` in every
configuration; the square particles hold indices `0` and `1` and trade
places exactly as in the two-label fixture.  The objects are therefore
the six two-element occupied sets of the square (`Hop.Pair4`), the
carrier is `Fin 4`, and a hop's transport is the transposition of
indices `0` and `1` when the two-label flip bit is set, the identity
otherwise.

The pre-registered prediction (`STATUS.md`): the holonomy group is
nontrivial (the two-label witness walk swaps `0` and `1`) and a natural
section exists all the same -- the constant pair `(2, 3)` -- because the
criterion of `natural_section_iff_holonomy` asks for a fixed admissible
pair, not for trivial holonomy.  AuthorityEffect: None.
-/

namespace NaturalSections.Hop4

open DiffInterface ContactKernel PresentationNaturality

def fourObs : DiffObs (Fin 4) (Fin 4 × Fin 4) := kernelObs (fun i => i)

def swap01 (i : Fin 4) : Fin 4 := if i.val = 0 then 1 else if i.val = 1 then 0 else i

theorem swap01_invol : ∀ i : Fin 4, swap01 (swap01 i) = i := by decide

def swap01Bij : Bij (Fin 4) (Fin 4) where
  fwd := swap01
  bwd := swap01
  fwd_bwd := swap01_invol
  bwd_fwd := swap01_invol

def swap01PairBij : Bij (Fin 4 × Fin 4) (Fin 4 × Fin 4) where
  fwd p := (swap01 p.1, swap01 p.2)
  bwd p := (swap01 p.1, swap01 p.2)
  fwd_bwd p := by
    show (swap01 (swap01 p.1), swap01 (swap01 p.2)) = p
    rw [swap01_invol, swap01_invol]
  bwd_fwd p := by
    show (swap01 (swap01 p.1), swap01 (swap01 p.2)) = p
    rw [swap01_invol, swap01_invol]

/-- The transposition of indices `0` and `1` as a presentation automorphism. -/
def swap01Iso : PresIso fourObs fourObs where
  car := swap01Bij
  res := swap01PairBij
  delta_transport _ _ := rfl
  zero_transport r := by
    show r.1 = r.2 ↔ swap01 r.1 = swap01 r.2
    constructor
    · intro e; rw [e]
    · intro e; exact swap01Bij.fwd_injective e

/-- The component: square objects, four indices, the two-label hop rule
acting on indices `0` and `1` only. -/
def family : HFamily where
  Obj := Hop.Pair4
  car _ := Fin 4
  res _ := Fin 4 × Fin 4
  obs _ := fourObs
  Hom a b := PLift (Hop.hopB Hop.squareAdj a.sites b.sites = true)
  iso a b _ :=
    match Hop.flipB Hop.squareAdj a.sites b.sites with
    | true => swap01Iso
    | false => PresIso.refl fourObs

theorem pair_ext {x y : NonZeroPair fourObs} (e : x.val = y.val) : x = y :=
  Subtype.ext e

def pair01 : NonZeroPair fourObs :=
  ⟨(0, 1), fun e => (by decide : ((0 : Fin 4) = 1) → False) e⟩

/-- The frozen edge particles, as an oriented pair. -/
def pair23 : NonZeroPair fourObs :=
  ⟨(2, 3), fun e => (by decide : ((2 : Fin 4) = 3) → False) e⟩

def sqHop (a b : Hop.Pair4) (h : Hop.hopB Hop.squareAdj a.sites b.sites = true := by decide) :
    family.Hom a b :=
  ⟨h⟩

/-- The two-label witness walk, on this family. -/
def walk : Walk family .c01 .c01 :=
  .cons (.fwd (sqHop .c01 .c03))
    (.cons (.fwd (sqHop .c03 .c02))
      (.cons (.fwd (sqHop .c02 .c12))
        (.cons (.fwd (sqHop .c12 .c01)) .nil)))

theorem walk_transport_val (p : NonZeroPair fourObs) :
    (walk.transport p).val = (swap01 p.val.1, swap01 p.val.2) :=
  rfl

/-- **The holonomy is nontrivial**: the closed walk moves the pair `(0, 1)`. -/
theorem walk_moves_pair01 : walk.transport pair01 ≠ pair01 := by
  intro e
  have hv : (swap01 (0 : Fin 4), swap01 (1 : Fin 4)) = ((0 : Fin 4), (1 : Fin 4)) :=
    (walk_transport_val pair01).symm.trans (congrArg Subtype.val e)
  exact absurd (congrArg Prod.fst hv) (by decide)

/-- **The constant pair `(2, 3)` is natural**: no hop moves the frozen
indices, decided hop by hop. -/
theorem constant23_natural : HIsNatural family (fun _ => pair23) := by
  intro a b h
  show (match Hop.flipB Hop.squareAdj (Hop.Pair4.sites a) (Hop.Pair4.sites b) with
    | true => swap01Iso
    | false => PresIso.refl fourObs).mapPair pair23 = pair23
  cases a <;> cases b <;> first
    | exact absurd h.down (by decide)
    | exact pair_ext (by decide)

theorem section_exists : ∃ s : HSec family, HIsNatural family s :=
  ⟨fun _ => pair23, constant23_natural⟩

/-- **Nontrivial holonomy, natural section.**  With the three-label
fixture (`Hop3.parity_and_fixed_pair_come_apart`) this pins the
invariant from both sides: finer than parity, coarser than trivial
holonomy -- exactly a fixed admissible pair. -/
theorem nontrivial_holonomy_with_natural_section :
    (walk.transport pair01 ≠ pair01) ∧ ∃ s : HSec family, HIsNatural family s :=
  ⟨walk_moves_pair01, section_exists⟩

end NaturalSections.Hop4
