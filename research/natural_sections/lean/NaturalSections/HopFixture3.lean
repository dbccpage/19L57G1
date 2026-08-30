import NaturalSections
import NaturalSections.HopFixture

/-!
# Three-label hop fixture: parity and the fixed pair come apart

Three hard-core particles on four sites, so one hole.  An object is the
hole's position; the carrier is `Fin 3`, index `i` the `i`-th smallest
occupied site; the observer is the kernel of the identity, so the
admissible pairs are the ordered pairs of distinct indices.  A hop moves
the hole to an adjacent site (the particle there moves into the hole);
its transport is the induced permutation of sorted indices, computed by
`hopPerm` from positions and never tabulated.  The same `hopPerm` serves
every site graph; only the adjacency differs.

The pre-registered question (`STATUS.md`): on the square the hole
circulating the 4-cycle induces a 3-cycle of the particles -- an even
permutation fixing no label.  Parity calls that clean; the criterion
`natural_section_iff_holonomy` calls it obstructed.  The theorems below
carry the square (a 3-cycle, even, no natural section), the star (a
tree: no closed walk moves anything, a natural section exists) and the
chain (order preserved, the constant orientation is natural).  Nothing
here names a physical system.  AuthorityEffect: None.
-/

namespace NaturalSections.Hop3

open DiffInterface ContactKernel PresentationNaturality

/-- The hole's position on four sites. -/
inductive Hole where
  | h0 | h1 | h2 | h3
  deriving DecidableEq, Repr

def Hole.site : Hole → Nat
  | .h0 => 0
  | .h1 => 1
  | .h2 => 2
  | .h3 => 3

/-- The `i`-th smallest occupied site when the hole is at `h`. -/
def occ (h : Hole) (i : Fin 3) : Nat :=
  if i.val < h.site then i.val else i.val + 1

/-- The index of an occupied site `s` (never the hole) when the hole is
at `h'`. -/
def rank (h' : Hole) (s : Nat) : Nat :=
  if s < h'.site then s else s - 1

/-- The hop `h → h'`: the particle at `h'.site` moves into the hole at
`h.site`; every particle's new index is its rank among the sites other
than `h'.site`. -/
def raw (h h' : Hole) (i : Fin 3) : Nat :=
  let s := occ h i
  rank h' (if s = h'.site then h.site else s)

theorem raw_lt : ∀ (h h' : Hole) (i : Fin 3), raw h h' i < 3 := by
  intro h h'
  cases h <;> cases h' <;> decide

def hopPerm (h h' : Hole) (i : Fin 3) : Fin 3 := ⟨raw h h' i, raw_lt h h' i⟩

/-- The reverse hop undoes a hop, for every pair of hole positions. -/
theorem hop_inv : ∀ (h h' : Hole) (i : Fin 3), hopPerm h' h (hopPerm h h' i) = i := by
  intro h h'
  cases h <;> cases h' <;> decide

def hopBij (h h' : Hole) : Bij (Fin 3) (Fin 3) where
  fwd := hopPerm h h'
  bwd := hopPerm h' h
  fwd_bwd := hop_inv h' h
  bwd_fwd := hop_inv h h'

/-- The kernel observer on three indices: zero exactly on equal indices. -/
def threeObs : DiffObs (Fin 3) (Fin 3 × Fin 3) := kernelObs (fun i => i)

def hopPairBij (h h' : Hole) : Bij (Fin 3 × Fin 3) (Fin 3 × Fin 3) where
  fwd p := (hopPerm h h' p.1, hopPerm h h' p.2)
  bwd p := (hopPerm h' h p.1, hopPerm h' h p.2)
  fwd_bwd p := by
    show (hopPerm h h' (hopPerm h' h p.1), hopPerm h h' (hopPerm h' h p.2)) = p
    rw [hop_inv, hop_inv]
  bwd_fwd p := by
    show (hopPerm h' h (hopPerm h h' p.1), hopPerm h' h (hopPerm h h' p.2)) = p
    rw [hop_inv, hop_inv]

def hopIso (h h' : Hole) : PresIso threeObs threeObs where
  car := hopBij h h'
  res := hopPairBij h h'
  delta_transport _ _ := rfl
  zero_transport r := by
    show r.1 = r.2 ↔ hopPerm h h' r.1 = hopPerm h h' r.2
    constructor
    · intro e; rw [e]
    · intro e; exact (hopBij h h').fwd_injective e

/-- Hole positions are adjacent when their sites are. -/
def adjH (adj : Nat → Nat → Bool) (h h' : Hole) : Bool := adj h.site h'.site

/-- The declared family of a site graph: one arrow per hop of the hole. -/
def family (adj : Nat → Nat → Bool) : HFamily where
  Obj := Hole
  car _ := Fin 3
  res _ := Fin 3 × Fin 3
  obs _ := threeObs
  Hom h h' := PLift (adjH adj h h' = true)
  iso h h' _ := hopIso h h'

/-- The orientation "index 0 before index 1". -/
def pair01 : NonZeroPair threeObs :=
  ⟨(0, 1), fun e => (by decide : ((0 : Fin 3) = 1) → False) e⟩

/-- Pairs over `threeObs` are equal when their values are; stated here so
the value equality is syntactically over `Fin 3 × Fin 3`, where `decide`
finds its instance. -/
theorem pair_ext {x y : NonZeroPair threeObs} (e : x.val = y.val) : x = y :=
  Subtype.ext e

/-! ## The square: a 3-cycle, even, and no natural section -/

def sq3Family : HFamily := family Hop.squareAdj

def sq3Hop (a b : Hole) (h : adjH Hop.squareAdj a b = true := by decide) :
    sq3Family.Hom a b :=
  ⟨h⟩

/-- The Python's witness: the hole goes `3 → 1 → 0 → 2 → 3` around the
square, i.e. the occupied sets `{0,1,2} → {0,2,3} → {1,2,3} → {0,1,3} →
{0,1,2}`. -/
def sq3Walk : Walk sq3Family .h3 .h3 :=
  .cons (.fwd (sq3Hop .h3 .h1))
    (.cons (.fwd (sq3Hop .h1 .h0))
      (.cons (.fwd (sq3Hop .h0 .h2))
        (.cons (.fwd (sq3Hop .h2 .h3)) .nil)))

/-- The 3-cycle `0 → 1 → 2 → 0` on indices. -/
def c3 (i : Fin 3) : Fin 3 := ⟨(i.val + 1) % 3, Nat.mod_lt _ (by decide)⟩

def swap01 (i : Fin 3) : Fin 3 := if i.val = 0 then 1 else if i.val = 1 then 0 else i
def swap12 (i : Fin 3) : Fin 3 := if i.val = 1 then 2 else if i.val = 2 then 1 else i

theorem c3_no_fixed : ∀ i : Fin 3, c3 i ≠ i := by decide

/-- The 3-cycle is a composite of two transpositions: an EVEN permutation. -/
theorem c3_is_even : ∀ i : Fin 3, c3 i = swap01 (swap12 i) := by decide

theorem c3_order_three : ∀ i : Fin 3, c3 (c3 (c3 i)) = i := by decide

/-- The four hops compose to the 3-cycle. -/
theorem sq3_comp : ∀ i : Fin 3,
    hopPerm .h2 .h3 (hopPerm .h0 .h2 (hopPerm .h1 .h0 (hopPerm .h3 .h1 i))) = c3 i := by
  decide

theorem sq3_transport_val (p : NonZeroPair threeObs) :
    (sq3Walk.transport p).val = (c3 p.val.1, c3 p.val.2) := by
  show (hopPerm .h2 .h3 (hopPerm .h0 .h2 (hopPerm .h1 .h0 (hopPerm .h3 .h1 p.val.1))),
        hopPerm .h2 .h3 (hopPerm .h0 .h2 (hopPerm .h1 .h0 (hopPerm .h3 .h1 p.val.2)))) = _
  rw [sq3_comp, sq3_comp]

/-- The closed walk fixes no admissible pair: the 3-cycle fixes no index. -/
theorem sq3_no_fixed_pair (p : NonZeroPair threeObs) : sq3Walk.transport p ≠ p := by
  intro e
  have hv := congrArg Subtype.val e
  rw [sq3_transport_val] at hv
  exact c3_no_fixed p.val.1 (congrArg Prod.fst hv)

/-- **The square carries no natural section at three labels**, although
the obstructing holonomy is an even permutation. -/
theorem square3_no_natural_section :
    ¬ ∃ s : HSec sq3Family, HIsNatural sq3Family s :=
  fun ⟨s, hs⟩ => sq3_no_fixed_pair (s .h3) (Walk.transport_of_natural hs sq3Walk)

/-- **Parity and the fixed pair come apart.**  The holonomy of `sq3Walk` is
even (a composite of two transpositions), fixes no index, and there is
no natural section: the criterion the theorems prove is the fixed pair,
not parity. -/
theorem parity_and_fixed_pair_come_apart :
    (∀ i : Fin 3, c3 i = swap01 (swap12 i)) ∧
      (∀ p : NonZeroPair threeObs, sq3Walk.transport p ≠ p) ∧
      ¬ ∃ s : HSec sq3Family, HIsNatural sq3Family s :=
  ⟨c3_is_even, sq3_no_fixed_pair, square3_no_natural_section⟩

/-! ## The star: a tree, so a natural section exists -/

def st3Family : HFamily := family Hop.starAdj

def st3Hop (a b : Hole) (h : adjH Hop.starAdj a b = true := by decide) :
    st3Family.Hom a b :=
  ⟨h⟩

/-- The forest: base the hole at the hub, one hop out to each leaf. -/
def st3Forest : Forest st3Family where
  root _ := .h0
  path
    | .h0 => .nil
    | .h1 => .cons (.fwd (st3Hop .h0 .h1)) .nil
    | .h2 => .cons (.fwd (st3Hop .h0 .h2)) .nil
    | .h3 => .cons (.fwd (st3Hop .h0 .h3)) .nil

def st3Base : HSec st3Family := fun _ => pair01

/-- Every generator carries the base pair to itself: decided hop by hop. -/
theorem star3_generators :
    ∀ {a b : st3Family.Obj} (h : st3Family.Hom a b),
      (st3Forest.gen h).transport (st3Base (st3Forest.root a)) =
        st3Base (st3Forest.root b) := by
  intro a b h
  rw [Forest.gen_transport]
  -- The iso ignores the arrow's proof, so the goal has an `h`-free form.
  show (st3Forest.path b).reverse.transport
      ((hopIso a b).mapPair ((st3Forest.path a).transport pair01)) = pair01
  cases a <;> cases b <;> first
    | exact absurd h.down (by decide)
    | exact pair_ext (by decide)

/-- **The star carries a natural section at three labels**: the spread of
the base pair along the forest, by `natural_section_iff_generators`. -/
theorem star3_has_natural_section :
    ∃ s : HSec st3Family, HIsNatural st3Family s :=
  (natural_section_iff_generators st3Forest).mpr ⟨st3Base, star3_generators⟩

/-! ## The chain: order preserved, the constant orientation is natural -/

def ch3Family : HFamily := family Hop.chainAdj

theorem chain3_natural_section : HIsNatural ch3Family (fun _ => pair01) := by
  intro a b h
  show (hopIso a b).mapPair pair01 = pair01
  cases a <;> cases b <;> first
    | exact absurd h.down (by decide)
    | exact pair_ext (by decide)

theorem chain3_has_natural_section :
    ∃ s : HSec ch3Family, HIsNatural ch3Family s :=
  ⟨fun _ => pair01, chain3_natural_section⟩

/-- **The separation at three labels.**  Same four objects, same carrier,
same admissible pairs, same hop rule; only the adjacency differs.  The
chain and the star carry a natural section; the square does not, and
its obstruction is even. -/
theorem chain3_star3_square3_separation :
    (∃ s : HSec ch3Family, HIsNatural ch3Family s) ∧
      (∃ s : HSec st3Family, HIsNatural st3Family s) ∧
      ¬ ∃ s : HSec sq3Family, HIsNatural sq3Family s :=
  ⟨chain3_has_natural_section, star3_has_natural_section, square3_no_natural_section⟩

end NaturalSections.Hop3
