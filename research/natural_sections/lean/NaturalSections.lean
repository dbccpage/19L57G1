import Derivation.PresentationNaturality

/-!
# Natural sections at one object: the fixed-pair criterion is an iff

`PresentationNaturality.no_natural_section_of_fixed_point_free` gives a
sufficient condition for the FAILURE of naturality over the one-object
family `autoFamily O F`: the automorphism fixes no admissible pair.  Its
contrapositive `fixed_pair_of_natural_section` is one half of an
equivalence the sealed module never states.  This module states and
proves the other half and the equivalence, then shows by two fixtures
that the invariant is "fixes an admissible pair" and not "has a fixed
point":

* `cycIso` on the sealed `card4Obs` fixes the carrier point `e1` and
  fixes no admissible pair, so it carries no natural section;
* the identity on a one-view observer fixes every carrier point and has
  no admissible pair at all, so it carries no section of any kind.

Sections 1-3 are about ONE-OBJECT families, exactly as the sealed
module's non-claims delimit.  Sections 4-5 lift the criterion to any
declared `HFamily`: walks over the declared arrows (forward and
backward), transport along them, a `Forest` of declared base points and
walks, and the iff in two forms -- `natural_section_iff_generators`
(no condition on the forest) and `natural_section_iff_holonomy` (bases
constant along arrows: a natural section exists iff some choice of
pairs at the bases is fixed by every closed walk).  No choice principle
is used: the forest is data.  `one_object_recovered` checks that the
general theorem specialises to section 1.  The sealed package is read
as a byte-pinned staged copy and nothing sealed is amended.
AuthorityEffect: None.
-/

namespace NaturalSections

open DiffInterface ContactKernel PresentationNaturality

variable {X R : Type}

/-! ## 1. The missing half, and the equivalence -/

/-- A fixed admissible pair gives a natural section: the constant one. -/
theorem natural_section_of_fixed_pair (O : DiffObs X R) (F : PresIso O O)
    (p : NonZeroPair O) (hp : F.mapPair p = p) :
    ∃ s : Sec (autoFamily O F), IsNatural (autoFamily O F) s :=
  ⟨fun _ => p, fun _ => hp⟩

/-- **One object: a natural section exists iff the automorphism fixes an
admissible pair.**  The forward direction is the sealed
`fixed_pair_of_natural_section`; the backward direction is the constant
section.  Over one object the whole question is this. -/
theorem natural_section_iff_fixed_pair (O : DiffObs X R) (F : PresIso O O) :
    (∃ s : Sec (autoFamily O F), IsNatural (autoFamily O F) s) ↔
      ∃ p : NonZeroPair O, F.mapPair p = p :=
  ⟨fun ⟨s, hs⟩ => fixed_pair_of_natural_section O F s hs,
   fun ⟨p, hp⟩ => natural_section_of_fixed_pair O F p hp⟩

/-- The same equivalence for the indexed family notion, through the
sealed one-object bridge `hAuto_iff_auto`. -/
theorem hnatural_section_iff_fixed_pair (O : DiffObs X R) (F : PresIso O O) :
    (∃ s : HSec (hAutoFamily O F), HIsNatural (hAutoFamily O F) s) ↔
      ∃ p : NonZeroPair O, F.mapPair p = p :=
  (hAuto_iff_auto O F).trans (natural_section_iff_fixed_pair O F)

/-- Unfolded: a fixed admissible pair is two fixed carrier points that
the observer distinguishes.  `mapPair` acts componentwise, so nothing
else could fix a pair. -/
theorem fixed_pair_iff_two_fixed_points (O : DiffObs X R) (F : PresIso O O)
    (p : NonZeroPair O) :
    F.mapPair p = p ↔
      F.car.fwd p.val.1 = p.val.1 ∧ F.car.fwd p.val.2 = p.val.2 := by
  constructor
  · intro h
    have hv : (F.car.fwd p.val.1, F.car.fwd p.val.2) = p.val :=
      congrArg Subtype.val h
    exact ⟨congrArg Prod.fst hv, congrArg Prod.snd hv⟩
  · intro h
    apply Subtype.ext
    show (F.car.fwd p.val.1, F.car.fwd p.val.2) = p.val
    rw [h.1, h.2]

/-! ## 2. A fixed point is not the invariant

Fix `e1`, cycle `e2 → e3 → e4 → e2` on the sealed four-element kernel
observer `card4Obs`.  The automorphism has a fixed point; its only fixed
pair is `(e1, e1)`, which the reflexive zero relation rules out. -/

def cyc : Card4 → Card4
  | .e1 => .e1
  | .e2 => .e3
  | .e3 => .e4
  | .e4 => .e2

def cycInv : Card4 → Card4
  | .e1 => .e1
  | .e2 => .e4
  | .e3 => .e2
  | .e4 => .e3

theorem cyc_cycInv : ∀ x, cyc (cycInv x) = x := by
  intro x; cases x <;> rfl

theorem cycInv_cyc : ∀ x, cycInv (cyc x) = x := by
  intro x; cases x <;> rfl

def cycBij : Bij Card4 Card4 where
  fwd := cyc
  bwd := cycInv
  fwd_bwd := cyc_cycInv
  bwd_fwd := cycInv_cyc

def cycPairBij : Bij (Card4 × Card4) (Card4 × Card4) where
  fwd p := (cyc p.1, cyc p.2)
  bwd p := (cycInv p.1, cycInv p.2)
  fwd_bwd p := by
    show (cyc (cycInv p.1), cyc (cycInv p.2)) = p
    rw [cyc_cycInv, cyc_cycInv]
  bwd_fwd p := by
    show (cycInv (cyc p.1), cycInv (cyc p.2)) = p
    rw [cycInv_cyc, cycInv_cyc]

/-- The 3-cycle is a presentation automorphism of the sealed `card4Obs`. -/
def cycIso : PresIso card4Obs card4Obs where
  car := cycBij
  res := cycPairBij
  delta_transport _ _ := rfl
  zero_transport r := by
    show r.1 = r.2 ↔ cyc r.1 = cyc r.2
    constructor
    · intro h; rw [h]
    · intro h; exact cycBij.fwd_injective h

theorem cyc_fixes_e1 : cyc .e1 = .e1 := rfl

theorem cyc_fixes_only_e1 : ∀ x, cyc x = x → x = .e1 := by
  intro x h
  cases x <;> first | rfl | cases h

/-- The 3-cycle fixes no admissible pair. -/
theorem cycIso_fixed_pair_free (p : NonZeroPair card4Obs) :
    cycIso.mapPair p ≠ p := by
  intro h
  have hv := (fixed_pair_iff_two_fixed_points card4Obs cycIso p).mp h
  have h1 := cyc_fixes_only_e1 p.val.1 hv.1
  have h2 := cyc_fixes_only_e1 p.val.2 hv.2
  exact p.property (show p.val.1 = p.val.2 from h1.trans h2.symm)

/-- **The separation.**  A fixed carrier point, no fixed admissible
pair, no natural section: "the automorphism has a fixed point" is not
the condition; "the automorphism fixes an admissible pair" is. -/
theorem fixed_point_without_natural_section :
    cyc .e1 = .e1 ∧
      ¬ ∃ s : Sec (autoFamily card4Obs cycIso),
          IsNatural (autoFamily card4Obs cycIso) s :=
  ⟨rfl, no_natural_section_of_fixed_point_free card4Obs cycIso cycIso_fixed_pair_free⟩

/-! ## 3. Fixed points everywhere, admissible pairs nowhere -/

/-- The observer that sees one value: its zero relation is total. -/
def blindObs : DiffObs Bool (Unit × Unit) := kernelObs (fun _ : Bool => ())

theorem blindObs_no_admissible_pair (p : NonZeroPair blindObs) : False :=
  p.property rfl

/-- The identity fixes every carrier point, and there is no section at
all, natural or not.  A fixed-point reading of the criterion would call
this a positive case; the fixed-pair reading correctly does not. -/
theorem identity_fixes_everything_no_section :
    (∀ x, (PresIso.refl blindObs).car.fwd x = x) ∧
      ¬ ∃ s : Sec (autoFamily blindObs (PresIso.refl blindObs)),
          IsNatural (autoFamily blindObs (PresIso.refl blindObs)) s :=
  ⟨fun _ => rfl, fun ⟨s, _⟩ => blindObs_no_admissible_pair (s ())⟩

/-! ## 4. Walks over a declared family

A declared `HFamily` lists its arrows and assumes no closure.  A walk
traverses listed arrows forward or backward; transport along a walk
folds `mapPair` and `.symm.mapPair`.  Backward traversal is legitimate
because every `mapPair` is a bijection on admissible pairs (the sealed
`mapPair_symm_left` and `mapPair_symm_right`), so an arrow constrains a
section in both directions whether or not its inverse is listed.  No
categorical structure is claimed: a walk is a list, and its transport is
a composite of the declared transports. -/

/-- One step of a walk: a declared arrow, forward or backward. -/
inductive Step (D : HFamily) : D.Obj → D.Obj → Type where
  | fwd {a b : D.Obj} (h : D.Hom a b) : Step D a b
  | bwd {a b : D.Obj} (h : D.Hom a b) : Step D b a

/-- A walk: a list of steps with chained endpoints. -/
inductive Walk (D : HFamily) : D.Obj → D.Obj → Type where
  | nil {a : D.Obj} : Walk D a a
  | cons {a b c : D.Obj} (s : Step D a b) (w : Walk D b c) : Walk D a c

variable {D : HFamily}

def Step.transport :
    {a b : D.Obj} → Step D a b → NonZeroPair (D.obs a) → NonZeroPair (D.obs b)
  | _, _, .fwd h, p => (D.iso _ _ h).mapPair p
  | _, _, .bwd h, p => (D.iso _ _ h).symm.mapPair p

def Step.inv : {a b : D.Obj} → Step D a b → Step D b a
  | _, _, .fwd h => .bwd h
  | _, _, .bwd h => .fwd h

theorem Step.inv_transport :
    ∀ {a b : D.Obj} (s : Step D a b) (p : NonZeroPair (D.obs a)),
      s.inv.transport (s.transport p) = p
  | _, _, .fwd h, p => mapPair_symm_left (D.iso _ _ h) p
  | _, _, .bwd h, p => mapPair_symm_right (D.iso _ _ h) p

theorem Step.transport_inv :
    ∀ {a b : D.Obj} (s : Step D a b) (q : NonZeroPair (D.obs b)),
      s.transport (s.inv.transport q) = q
  | _, _, .fwd h, q => mapPair_symm_right (D.iso _ _ h) q
  | _, _, .bwd h, q => mapPair_symm_left (D.iso _ _ h) q

def Walk.transport :
    {a b : D.Obj} → Walk D a b → NonZeroPair (D.obs a) → NonZeroPair (D.obs b)
  | _, _, .nil, p => p
  | _, _, .cons s w, p => w.transport (s.transport p)

def Walk.append : {a b c : D.Obj} → Walk D a b → Walk D b c → Walk D a c
  | _, _, _, .nil, v => v
  | _, _, _, .cons s w, v => .cons s (w.append v)

/-- Reverse a walk: every step inverted, in the opposite order. -/
def Walk.reverse : {a b : D.Obj} → Walk D a b → Walk D b a
  | _, _, .nil => .nil
  | _, _, .cons s w => w.reverse.append (.cons s.inv .nil)

theorem Walk.transport_append :
    ∀ {a b c : D.Obj} (w : Walk D a b) (v : Walk D b c) (p : NonZeroPair (D.obs a)),
      (w.append v).transport p = v.transport (w.transport p)
  | _, _, _, .nil, _, _ => rfl
  | _, _, _, .cons s w, v, p => Walk.transport_append w v (s.transport p)

/-- Transport back along the reversed walk undoes transport. -/
theorem Walk.reverse_transport_transport :
    ∀ {a b : D.Obj} (w : Walk D a b) (p : NonZeroPair (D.obs a)),
      w.reverse.transport (w.transport p) = p
  | _, _, .nil, _ => rfl
  | _, _, .cons s w, p => by
    show (w.reverse.append (.cons s.inv .nil)).transport (w.transport (s.transport p)) = p
    rw [Walk.transport_append, Walk.reverse_transport_transport w (s.transport p)]
    exact Step.inv_transport s p

/-- Transport along a walk undoes transport back along its reverse. -/
theorem Walk.transport_reverse_transport :
    ∀ {a b : D.Obj} (w : Walk D a b) (q : NonZeroPair (D.obs b)),
      w.transport (w.reverse.transport q) = q
  | _, _, .nil, _ => rfl
  | _, _, .cons s w, q => by
    show w.transport (s.transport ((w.reverse.append (.cons s.inv .nil)).transport q)) = q
    rw [Walk.transport_append]
    show w.transport (s.transport (s.inv.transport (w.reverse.transport q))) = q
    rw [Step.transport_inv]
    exact Walk.transport_reverse_transport w q

/-- A natural section is transported to itself along every step, backward
steps included. -/
theorem Step.transport_of_natural {s : HSec D} (hs : HIsNatural D s)
    {a b : D.Obj} (st : Step D a b) : st.transport (s a) = s b := by
  cases st with
  | fwd h => exact hs _ _ h
  | bwd h =>
    show (D.iso _ _ h).symm.mapPair (s _) = s _
    rw [← hs _ _ h]
    exact mapPair_symm_left _ _

/-- **Necessity, in its general form.**  A natural section is transported
to itself along every walk; in particular every closed walk fixes its
value at the base point. -/
theorem Walk.transport_of_natural {s : HSec D} (hs : HIsNatural D s) :
    ∀ {a b : D.Obj} (w : Walk D a b), w.transport (s a) = s b
  | _, _, .nil => rfl
  | _, _, .cons st w => by
    show w.transport (st.transport (s _)) = s _
    rw [Step.transport_of_natural hs st]
    exact Walk.transport_of_natural hs w

/-! ## 5. Forests and the iff

A forest is DATA: a base object for every object, and a walk from the
base to the object.  It is declared, not chosen -- choosing a walk per
object without one would need a choice principle this package does not
use.  A genuine spanning forest of the arrow graph is an instance; the
theorems below do not need the tree structure, only the walks. -/

structure Forest (D : HFamily) where
  root : D.Obj → D.Obj
  path : (a : D.Obj) → Walk D (root a) a

/-- The generator of a declared arrow `h : a → b` relative to the forest:
from the base of `a` out to `a`, across `h`, and back to the base of `b`. -/
def Forest.gen (T : Forest D) {a b : D.Obj} (h : D.Hom a b) :
    Walk D (T.root a) (T.root b) :=
  (T.path a).append (.cons (.fwd h) (T.path b).reverse)

/-- The section a forest builds from a choice of pairs at the bases:
transport the base pair out along the tree walk. -/
def Forest.spread (T : Forest D) (p : HSec D) : HSec D :=
  fun a => (T.path a).transport (p (T.root a))

theorem Forest.gen_transport (T : Forest D) {a b : D.Obj} (h : D.Hom a b)
    (x : NonZeroPair (D.obs (T.root a))) :
    (T.gen h).transport x =
      (T.path b).reverse.transport ((D.iso a b h).mapPair ((T.path a).transport x)) := by
  show ((T.path a).append (.cons (.fwd h) (T.path b).reverse)).transport x = _
  rw [Walk.transport_append]
  rfl

/-- **The iff, generator form.**  Relative to any forest, a natural section
exists iff some choice of pairs at the bases is carried, by the
generator of every declared arrow, from the base pair of its source to
the base pair of its target.  No condition on the forest is needed; the
section is the spread of the base choice. -/
theorem natural_section_iff_generators (T : Forest D) :
    (∃ s : HSec D, HIsNatural D s) ↔
      ∃ p : HSec D, ∀ {a b : D.Obj} (h : D.Hom a b),
        (T.gen h).transport (p (T.root a)) = p (T.root b) := by
  constructor
  · rintro ⟨s, hs⟩
    exact ⟨s, fun h => Walk.transport_of_natural hs (T.gen h)⟩
  · rintro ⟨p, hp⟩
    refine ⟨T.spread p, ?_⟩
    intro a b h
    show (D.iso a b h).mapPair ((T.path a).transport (p (T.root a))) =
      (T.path b).transport (p (T.root b))
    rw [← hp h, Forest.gen_transport, Walk.transport_reverse_transport]

/-- A pair fixed by every closed walk at `r` is carried to itself along
any walk from `r` to a base that is `r` again. -/
theorem walk_maps_of_closed_fixed (p : HSec D) {r r' : D.Obj} (hr : r = r')
    (hfix : ∀ w : Walk D r r, w.transport (p r) = p r) (w : Walk D r r') :
    w.transport (p r) = p r' := by
  subst hr
  exact hfix w

/-- **The iff, holonomy form.**  When the forest's bases are constant along
declared arrows (one base per connected component), a natural section
exists iff some choice of pairs at the bases is fixed by every closed
walk at its base.  The generator form is the finite check; this is the
statement in terms of holonomy. -/
theorem natural_section_iff_holonomy (T : Forest D)
    (hroot : ∀ {a b : D.Obj}, D.Hom a b → T.root a = T.root b) :
    (∃ s : HSec D, HIsNatural D s) ↔
      ∃ p : HSec D, ∀ a : D.Obj, ∀ w : Walk D (T.root a) (T.root a),
        w.transport (p (T.root a)) = p (T.root a) := by
  constructor
  · rintro ⟨s, hs⟩
    exact ⟨s, fun _ w => Walk.transport_of_natural hs w⟩
  · rintro ⟨p, hp⟩
    exact (natural_section_iff_generators T).mpr
      ⟨p, fun h => walk_maps_of_closed_fixed p (hroot h) (hp _) (T.gen h)⟩

/-- The one-object forest: the single object is its own base. -/
def trivialForest (O : DiffObs X R) (F : PresIso O O) : Forest (hAutoFamily O F) where
  root _ := ()
  path _ := .nil

/-- **Consistency check.**  The general iff specialised to the one-object
family is the one-object iff of section 1: the single generator is
`F` itself, so the base condition is "F fixes an admissible pair". -/
theorem one_object_recovered (O : DiffObs X R) (F : PresIso O O) :
    (∃ s : HSec (hAutoFamily O F), HIsNatural (hAutoFamily O F) s) ↔
      ∃ p : NonZeroPair O, F.mapPair p = p :=
  (natural_section_iff_generators (trivialForest O F)).trans
    ⟨fun ⟨p, hp⟩ => ⟨p (), hp (a := ()) (b := ()) ()⟩,
     fun ⟨p, hp⟩ => ⟨fun _ => p, fun _ => hp⟩⟩

end NaturalSections
