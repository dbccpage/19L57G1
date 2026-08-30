import NaturalSections
import NaturalSections.HopFixture

/-!
# Refinement: the class is a mesh invariant

A SUBDIVISION of a declared arrow `h0 : a0 -> b0` adds a fresh midpoint
object with a declared presentation and splits `h0`'s transport through
a declared factorization `F`: the first half-arrow carries `F`, the
second carries `F.symm ; iso h0`.  The original arrow is retained; its
naturality equation is implied by the halves'.

The theorem: a natural section exists iff one exists for the subdivided
family, for EVERY family, arrow, midpoint and factorization.  The
midpoint's value is forced -- `F.mapPair (s a0)` -- so refining a mesh
adds no freedom and removes none; the class never moves.  Finite chains
of subdivisions compose by transitivity of the iff.  Nothing here
orders a refinement sequence.  AuthorityEffect: None.
-/

namespace NaturalSections

open DiffInterface ContactKernel PresentationNaturality

/-- A subdivision instruction: the arrow, the midpoint's presentation,
and the declared factorization of the arrow's transport. -/
structure Subdiv (D : HFamily) where
  a0 : D.Obj
  b0 : D.Obj
  h0 : D.Hom a0 b0
  Mid : Type
  MidR : Type
  midObs : DiffObs Mid MidR
  F : PresIso (D.obs a0) midObs

variable {D : HFamily}

/-- The subdivided family: one fresh object, the two half-arrows added,
everything else retained. -/
def Subdiv.family (S : Subdiv D) : HFamily where
  Obj := Sum D.Obj Unit
  car
    | .inl x => D.car x
    | .inr _ => S.Mid
  res
    | .inl x => D.res x
    | .inr _ => S.MidR
  obs
    | .inl x => D.obs x
    | .inr _ => S.midObs
  Hom
    | .inl x, .inl y => D.Hom x y
    | .inl x, .inr _ => PLift (S.a0 = x)
    | .inr _, .inl y => PLift (S.b0 = y)
    | .inr _, .inr _ => Empty
  iso o p h :=
    match o, p, h with
    | .inl x, .inl y, h => D.iso x y h
    | .inl _, .inr _, h => h.down ▸ S.F
    | .inr _, .inl _, h => h.down ▸ (S.F.symm.trans (D.iso S.a0 S.b0 S.h0))
    | .inr _, .inr _, h => nomatch h

/-- Push a section: old objects keep their values, the midpoint takes the
forced value `F.mapPair (s a0)`. -/
def Subdiv.push (S : Subdiv D) (s : HSec D) : HSec S.family
  | .inl x => s x
  | .inr _ => S.F.mapPair (s S.a0)

theorem Subdiv.push_natural (S : Subdiv D) {s : HSec D} (hs : HIsNatural D s) :
    HIsNatural S.family (S.push s) := by
  intro o p h
  match o, p, h with
  | .inl x, .inl y, h => exact hs x y h
  | .inl x, .inr u, h =>
    cases h with
    | up e =>
      subst e
      show S.F.mapPair (s S.a0) = S.F.mapPair (s S.a0)
      rfl
  | .inr u, .inl y, h =>
    cases h with
    | up e =>
      subst e
      show (S.F.symm.trans (D.iso S.a0 S.b0 S.h0)).mapPair (S.F.mapPair (s S.a0)) = s S.b0
      rw [mapPair_trans, mapPair_symm_left]
      exact hs S.a0 S.b0 S.h0
  | .inr u, .inr v, h => exact nomatch h

/-- Pull a section back: restrict to the old objects. -/
def Subdiv.pull (S : Subdiv D) (s' : HSec S.family) : HSec D :=
  fun x => s' (.inl x)

theorem Subdiv.pull_natural (S : Subdiv D) {s' : HSec S.family}
    (hs' : HIsNatural S.family s') : HIsNatural D (S.pull s') :=
  fun x y h => hs' (.inl x) (.inl y) h

/-- **The class is a mesh invariant.**  A natural section exists iff one
exists for any declared subdivision; finite chains compose by
transitivity. -/
theorem natural_section_iff_subdiv (S : Subdiv D) :
    (∃ s : HSec D, HIsNatural D s) ↔ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  ⟨fun ⟨s, hs⟩ => ⟨S.push s, S.push_natural hs⟩,
   fun ⟨s', hs'⟩ => ⟨S.pull s', S.pull_natural hs'⟩⟩

/-- Refining never removes an obstruction. -/
theorem class_refinement_invariant (S : Subdiv D)
    (h : ¬ ∃ s : HSec D, HIsNatural D s) :
    ¬ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  fun e => h ((natural_section_iff_subdiv S).mpr e)

/-- Every one-step subdivision of the two-label square is obstructed. -/
theorem square_subdiv_obstructed (S : Subdiv Hop.squareFamily) :
    ¬ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  class_refinement_invariant S Hop.square_no_natural_section

/-- Every one-step subdivision of the chain keeps its section. -/
theorem chain_subdiv_section (S : Subdiv Hop.chainFamily) :
    ∃ s' : HSec S.family, HIsNatural S.family s' :=
  (natural_section_iff_subdiv S).mp Hop.chain_has_natural_section

/-! ## Replacement

`Subdiv.family` RETAINS the original arrow, so the theorem above covers
a redundant midpoint extension; the Python fixtures REPLACE each hop by
its two halves.  A reviewer of pull request 98 pointed out the mismatch.
`Repl` is the replacement operation: the original arrow is removed from
the family, and its naturality equation is DERIVED from the two halves
(`Repl.h0_equation`).  Removing an arrow means the instruction must be
able to point at it, so a replacement carries two decidabilities as
declared data: equality of objects, and equality with the removed arrow
at its own position.  Every fixture has both. -/

structure Repl (D : HFamily) extends Subdiv D where
  decObj : DecidableEq D.Obj
  dec0 : ∀ f : D.Hom a0 b0, Decidable (f = h0)

/-- The replacement family: the fresh midpoint, the two half-arrows, and
every original arrow EXCEPT the subdivided one. -/
def Repl.family (S : Repl D) : HFamily where
  Obj := Sum D.Obj Unit
  car
    | .inl x => D.car x
    | .inr _ => S.Mid
  res
    | .inl x => D.res x
    | .inr _ => S.MidR
  obs
    | .inl x => D.obs x
    | .inr _ => S.midObs
  Hom
    | .inl x, .inl y =>
        {f : D.Hom x y // ∀ (ex : S.a0 = x) (ey : S.b0 = y), ex ▸ ey ▸ S.h0 ≠ f}
    | .inl x, .inr _ => PLift (S.a0 = x)
    | .inr _, .inl y => PLift (S.b0 = y)
    | .inr _, .inr _ => Empty
  iso o p h :=
    match o, p, h with
    | .inl x, .inl y, h => D.iso x y h.val
    | .inl _, .inr _, h => h.down ▸ S.F
    | .inr _, .inl _, h => h.down ▸ (S.F.symm.trans (D.iso S.a0 S.b0 S.h0))
    | .inr _, .inr _, h => nomatch h

def Repl.push (S : Repl D) (s : HSec D) : HSec S.family
  | .inl x => s x
  | .inr _ => S.F.mapPair (s S.a0)

theorem Repl.push_natural (S : Repl D) {s : HSec D} (hs : HIsNatural D s) :
    HIsNatural S.family (S.push s) := by
  intro o p h
  match o, p, h with
  | .inl x, .inl y, h => exact hs x y h.val
  | .inl x, .inr u, h =>
    cases h with
    | up e =>
      subst e
      show S.F.mapPair (s S.a0) = S.F.mapPair (s S.a0)
      rfl
  | .inr u, .inl y, h =>
    cases h with
    | up e =>
      subst e
      show (S.F.symm.trans (D.iso S.a0 S.b0 S.h0)).mapPair (S.F.mapPair (s S.a0)) = s S.b0
      rw [mapPair_trans, mapPair_symm_left]
      exact hs S.a0 S.b0 S.h0
  | .inr u, .inr v, h => exact nomatch h

/-- **The removed arrow's equation is derived from the two halves**: the
halves compose to its transport. -/
theorem Repl.h0_equation (S : Repl D) {s' : HSec S.family}
    (hs' : HIsNatural S.family s') :
    (D.iso S.a0 S.b0 S.h0).mapPair (s' (.inl S.a0)) = s' (.inl S.b0) := by
  have key : ∀ (p : NonZeroPair (D.obs S.a0)) (q : NonZeroPair S.midObs)
      (r : NonZeroPair (D.obs S.b0)),
      S.F.mapPair p = q →
      (S.F.symm.trans (D.iso S.a0 S.b0 S.h0)).mapPair q = r →
      (D.iso S.a0 S.b0 S.h0).mapPair p = r := by
    intro p q r h1 h2
    rw [← h1, mapPair_trans, mapPair_symm_left] at h2
    exact h2
  exact key _ _ _ (hs' (.inl S.a0) (.inr ()) ⟨rfl⟩) (hs' (.inr ()) (.inl S.b0) ⟨rfl⟩)

theorem Repl.pull_natural (S : Repl D) {s' : HSec S.family}
    (hs' : HIsNatural S.family s') : HIsNatural D (fun x => s' (.inl x)) := by
  intro x y f
  cases S.decObj S.a0 x with
  | isFalse hx => exact hs' (.inl x) (.inl y) ⟨f, fun ex _ => absurd ex hx⟩
  | isTrue hx =>
    cases S.decObj S.b0 y with
    | isFalse hy => exact hs' (.inl x) (.inl y) ⟨f, fun _ ey => absurd ey hy⟩
    | isTrue hy =>
      subst hx
      subst hy
      cases S.dec0 f with
      | isTrue hf =>
        subst hf
        exact S.h0_equation hs'
      | isFalse hf =>
        exact hs' (.inl S.a0) (.inl S.b0) ⟨f, fun _ _ he => hf he.symm⟩

/-- **Replacement invariance**: the operation the fixtures perform -- the
arrow removed, the halves added -- changes nothing about sections. -/
theorem natural_section_iff_repl (S : Repl D) :
    (∃ s : HSec D, HIsNatural D s) ↔ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  ⟨fun ⟨s, hs⟩ => ⟨S.push s, S.push_natural hs⟩,
   fun ⟨s', hs'⟩ => ⟨fun x => s' (.inl x), S.pull_natural hs'⟩⟩

/-- Every one-step replacement of a square hop leaves the square obstructed. -/
theorem square_repl_obstructed (S : Repl Hop.squareFamily) :
    ¬ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  fun e => Hop.square_no_natural_section ((natural_section_iff_repl S).mpr e)

/-- Every one-step replacement of a chain hop keeps the chain's section. -/
theorem chain_repl_section (S : Repl Hop.chainFamily) :
    ∃ s' : HSec S.family, HIsNatural S.family s' :=
  (natural_section_iff_repl S).mp Hop.chain_has_natural_section

/-! ## Replacement of an undirected edge

`Repl` removes ONE oriented declaration; the fixtures declare every hop
in both directions, so the reverse declaration survived and carried the
same constraint -- a reviewer of pull request 98 pointed it out.
`ReplE` removes BOTH oriented declarations of an edge through one shared
midpoint, with all four half-arrows declared.  Two more pieces of the
instruction are data: `ne0` (the edge joins distinct objects -- a loop
is not an edge) and `rev_inverts` (the declared reverse transport
inverts the declared forward one -- the statement that the two oriented
declarations present ONE undirected edge; every fixture satisfies it).
The removed forward equation is derived from the halves
(`ReplE.h0_equation`), the removed reverse equation from the forward one
and `rev_inverts` (`ReplE.h0r_equation`).  Concrete instances for the
square and the chain show the quantified corollaries are not vacuous. -/

structure ReplE (D : HFamily) extends Subdiv D where
  h0r : D.Hom b0 a0
  ne0 : a0 ≠ b0
  decObj : DecidableEq D.Obj
  dec0 : ∀ f : D.Hom a0 b0, Decidable (f = h0)
  dec0r : ∀ f : D.Hom b0 a0, Decidable (f = h0r)
  rev_inverts : ∀ p : NonZeroPair (D.obs a0),
    (D.iso b0 a0 h0r).mapPair ((D.iso a0 b0 h0).mapPair p) = p

/-- The edge-replacement family: both oriented declarations of the edge
removed, the shared midpoint added with all four half-arrows. -/
def ReplE.family (S : ReplE D) : HFamily where
  Obj := Sum D.Obj Unit
  car
    | .inl x => D.car x
    | .inr _ => S.Mid
  res
    | .inl x => D.res x
    | .inr _ => S.MidR
  obs
    | .inl x => D.obs x
    | .inr _ => S.midObs
  Hom
    | .inl x, .inl y =>
        {f : D.Hom x y //
          (∀ (ex : S.a0 = x) (ey : S.b0 = y), ex ▸ ey ▸ S.h0 ≠ f) ∧
          (∀ (ex : S.b0 = x) (ey : S.a0 = y), ex ▸ ey ▸ S.h0r ≠ f)}
    | .inl x, .inr _ => PLift (S.a0 = x) ⊕ PLift (S.b0 = x)
    | .inr _, .inl y => PLift (S.b0 = y) ⊕ PLift (S.a0 = y)
    | .inr _, .inr _ => Empty
  iso o p h :=
    match o, p, h with
    | .inl x, .inl y, h => D.iso x y h.val
    | .inl _, .inr _, .inl e => e.down ▸ S.F
    | .inl _, .inr _, .inr e => e.down ▸ ((D.iso S.b0 S.a0 S.h0r).trans S.F)
    | .inr _, .inl _, .inl e => e.down ▸ (S.F.symm.trans (D.iso S.a0 S.b0 S.h0))
    | .inr _, .inl _, .inr e => e.down ▸ S.F.symm
    | .inr _, .inr _, h => nomatch h

def ReplE.push (S : ReplE D) (s : HSec D) : HSec S.family
  | .inl x => s x
  | .inr _ => S.F.mapPair (s S.a0)

theorem ReplE.push_natural (S : ReplE D) {s : HSec D} (hs : HIsNatural D s) :
    HIsNatural S.family (S.push s) := by
  intro o p h
  match o, p, h with
  | .inl x, .inl y, h => exact hs x y h.val
  | .inl x, .inr u, .inl e =>
    cases e with
    | up e =>
      subst e
      show S.F.mapPair (s S.a0) = S.F.mapPair (s S.a0)
      rfl
  | .inl x, .inr u, .inr e =>
    cases e with
    | up e =>
      subst e
      show ((D.iso S.b0 S.a0 S.h0r).trans S.F).mapPair (s S.b0) = S.F.mapPair (s S.a0)
      rw [mapPair_trans, hs S.b0 S.a0 S.h0r]
  | .inr u, .inl y, .inl e =>
    cases e with
    | up e =>
      subst e
      show (S.F.symm.trans (D.iso S.a0 S.b0 S.h0)).mapPair (S.F.mapPair (s S.a0)) = s S.b0
      rw [mapPair_trans, mapPair_symm_left]
      exact hs S.a0 S.b0 S.h0
  | .inr u, .inl y, .inr e =>
    cases e with
    | up e =>
      subst e
      show S.F.symm.mapPair (S.F.mapPair (s S.a0)) = s S.a0
      rw [mapPair_symm_left]
  | .inr u, .inr v, h => exact nomatch h

/-- The removed forward equation, derived from the two forward halves. -/
theorem ReplE.h0_equation (S : ReplE D) {s' : HSec S.family}
    (hs' : HIsNatural S.family s') :
    (D.iso S.a0 S.b0 S.h0).mapPair (s' (.inl S.a0)) = s' (.inl S.b0) := by
  have key : ∀ (p : NonZeroPair (D.obs S.a0)) (q : NonZeroPair S.midObs)
      (r : NonZeroPair (D.obs S.b0)),
      S.F.mapPair p = q →
      (S.F.symm.trans (D.iso S.a0 S.b0 S.h0)).mapPair q = r →
      (D.iso S.a0 S.b0 S.h0).mapPair p = r := by
    intro p q r h1 h2
    rw [← h1, mapPair_trans, mapPair_symm_left] at h2
    exact h2
  exact key _ _ _ (hs' (.inl S.a0) (.inr ()) (.inl ⟨rfl⟩))
    (hs' (.inr ()) (.inl S.b0) (.inl ⟨rfl⟩))

/-- The removed reverse equation, derived from the forward one and
`rev_inverts`. -/
theorem ReplE.h0r_equation (S : ReplE D) {s' : HSec S.family}
    (hs' : HIsNatural S.family s') :
    (D.iso S.b0 S.a0 S.h0r).mapPair (s' (.inl S.b0)) = s' (.inl S.a0) := by
  have key : ∀ (pA : NonZeroPair (D.obs S.a0)) (pB : NonZeroPair (D.obs S.b0)),
      (D.iso S.a0 S.b0 S.h0).mapPair pA = pB →
      (D.iso S.b0 S.a0 S.h0r).mapPair pB = pA := by
    intro pA pB h
    have h2 := congrArg (D.iso S.b0 S.a0 S.h0r).mapPair h
    rw [S.rev_inverts] at h2
    exact h2.symm
  exact key _ _ (S.h0_equation hs')

theorem ReplE.pull_natural (S : ReplE D) {s' : HSec S.family}
    (hs' : HIsNatural S.family s') : HIsNatural D (fun x => s' (.inl x)) := by
  intro x y f
  cases S.decObj S.a0 x with
  | isTrue hx =>
    cases S.decObj S.b0 y with
    | isTrue hy =>
      subst hx
      subst hy
      cases S.dec0 f with
      | isTrue hf =>
        subst hf
        exact S.h0_equation hs'
      | isFalse hf =>
        exact hs' (.inl S.a0) (.inl S.b0)
          ⟨f, fun _ _ he => hf he.symm, fun ex _ => absurd ex.symm S.ne0⟩
    | isFalse hy =>
      cases S.decObj S.b0 x with
      | isTrue hbx => exact absurd (hx.trans hbx.symm) S.ne0
      | isFalse hbx =>
        exact hs' (.inl x) (.inl y)
          ⟨f, fun _ ey => absurd ey hy, fun ex _ => absurd ex hbx⟩
  | isFalse hx =>
    cases S.decObj S.b0 x with
    | isTrue hbx =>
      cases S.decObj S.a0 y with
      | isTrue hay =>
        subst hbx
        subst hay
        cases S.dec0r f with
        | isTrue hf =>
          subst hf
          exact S.h0r_equation hs'
        | isFalse hf =>
          exact hs' (.inl S.b0) (.inl S.a0)
            ⟨f, fun ex _ => absurd ex S.ne0, fun _ _ he => hf he.symm⟩
      | isFalse hay =>
        exact hs' (.inl x) (.inl y)
          ⟨f, fun ex _ => absurd ex hx, fun _ ey => absurd ey hay⟩
    | isFalse hbx =>
      exact hs' (.inl x) (.inl y)
        ⟨f, fun ex _ => absurd ex hx, fun ex _ => absurd ex hbx⟩

/-- **Edge-replacement invariance**: removing both oriented declarations
of an edge and routing through the midpoint changes nothing about
sections. -/
theorem natural_section_iff_replE (S : ReplE D) :
    (∃ s : HSec D, HIsNatural D s) ↔ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  ⟨fun ⟨s, hs⟩ => ⟨S.push s, S.push_natural hs⟩,
   fun ⟨s', hs'⟩ => ⟨fun x => s' (.inl x), S.pull_natural hs'⟩⟩

theorem square_replE_obstructed (S : ReplE Hop.squareFamily) :
    ¬ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  fun e => Hop.square_no_natural_section ((natural_section_iff_replE S).mpr e)

theorem chain_replE_section (S : ReplE Hop.chainFamily) :
    ∃ s' : HSec S.family, HIsNatural S.family s' :=
  (natural_section_iff_replE S).mp Hop.chain_has_natural_section

/-- A concrete edge replacement of the square (the non-flipping edge
`{0,1} -- {0,3}`, midpoint presented by the identity): the quantified
corollaries are not vacuous. -/
def sqReplE : ReplE Hop.squareFamily where
  a0 := .c01
  b0 := .c03
  h0 := ⟨by decide⟩
  Mid := Bool
  MidR := Bool
  midObs := boolEqObs
  F := PresIso.refl boolEqObs
  h0r := ⟨by decide⟩
  ne0 := fun e => Hop.Pair4.noConfusion e
  decObj := inferInstanceAs (DecidableEq Hop.Pair4)
  dec0 := fun f => .isTrue (by cases f; rfl)
  dec0r := fun f => .isTrue (by cases f; rfl)
  rev_inverts := fun p => Subtype.ext rfl

theorem replE_square_inhabited : Nonempty (ReplE Hop.squareFamily) := ⟨sqReplE⟩

/-- A concrete edge replacement of the chain (`{0,1} -- {0,2}`). -/
def chReplE : ReplE Hop.chainFamily where
  a0 := .c01
  b0 := .c02
  h0 := ⟨by decide⟩
  Mid := Bool
  MidR := Bool
  midObs := boolEqObs
  F := PresIso.refl boolEqObs
  h0r := ⟨by decide⟩
  ne0 := fun e => Hop.Pair4.noConfusion e
  decObj := inferInstanceAs (DecidableEq Hop.Pair4)
  dec0 := fun f => .isTrue (by cases f; rfl)
  dec0r := fun f => .isTrue (by cases f; rfl)
  rev_inverts := fun p => Subtype.ext rfl

theorem replE_chain_inhabited : Nonempty (ReplE Hop.chainFamily) := ⟨chReplE⟩

/-- A concrete edge replacement of a FLIPPING square edge
(`{0,1} -- {1,2}`, whose two oriented transports are the swap): the
`rev_inverts` obligation is discharged nontrivially, by the swap being
an involution. -/
def sqReplEFlip : ReplE Hop.squareFamily where
  a0 := .c01
  b0 := .c12
  h0 := ⟨by decide⟩
  Mid := Bool
  MidR := Bool
  midObs := boolEqObs
  F := PresIso.refl boolEqObs
  h0r := ⟨by decide⟩
  ne0 := fun e => Hop.Pair4.noConfusion e
  decObj := inferInstanceAs (DecidableEq Hop.Pair4)
  dec0 := fun f => .isTrue (by cases f; rfl)
  dec0r := fun f => .isTrue (by cases f; rfl)
  rev_inverts := fun p => by
    apply Subtype.ext
    obtain ⟨⟨x, y⟩, _⟩ := p
    cases x <;> cases y <;> rfl

theorem replE_square_flip_inhabited : Nonempty (ReplE Hop.squareFamily) := ⟨sqReplEFlip⟩

end NaturalSections
