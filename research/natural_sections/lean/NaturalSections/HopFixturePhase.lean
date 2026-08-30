import NaturalSections
import NaturalSections.HopFixture

/-!
# Phase fibre: a natural section exists iff the flux vanishes, for ANY phase group

Two particles: one on the square `0-1, 0-2, 1-3, 2-3`, one on a disjoint
edge whose two sites are indexed by `Fin 2`.  Each particle carries a
phase register in a phase group `G`.  The carrier at every object is
`Fin 2 x G` (label, register); the observer is the kernel of the label
projection, so the admissible pairs are the ordered pairs of distinct
labels, each carrying a register.  A hop of the square particle across
the edge `0-1` adds the flux `Phi` to its register (`-Phi` the other way);
every other hop adds `0`; the edge particle's register never changes.

`G` is NOT assumed finite and NOT assumed to have decidable equality.
It is any type with an addition, a zero and a negation obeying the
group laws (`AbGroup`).  The finite phase groups computed in
`holonomy_phase.py` are instances (`fin4Phase`); so is any abelian group
the metatheory cares to supply.  Finiteness and decidability are used
only where they always were: on sites and labels.

Result: `section_iff_flux_zero` -- over this family a natural section
exists iff `Phi = 0`.  The obstruction is a pure phase: the permutation
part of every holonomy is the identity, and a section fails only because
the square particle's register returns shifted by `Phi` while the edge
particle's does not.  AuthorityEffect: None.
-/

namespace NaturalSections.HopPhase

open DiffInterface ContactKernel PresentationNaturality

/-- An abelian group, with its laws as fields.  Nothing here is decided;
nothing here is finite. -/
structure AbGroup (G : Type) where
  add : G → G → G
  zero : G
  neg : G → G
  add_assoc : ∀ a b c, add (add a b) c = add a (add b c)
  zero_add : ∀ a, add zero a = a
  add_zero : ∀ a, add a zero = a
  add_neg : ∀ a, add a (neg a) = zero
  neg_add : ∀ a, add (neg a) a = zero

namespace AbGroup

variable {G : Type} (P : AbGroup G)

theorem neg_zero : P.neg P.zero = P.zero := by
  have h := P.neg_add P.zero
  rw [P.add_zero] at h
  exact h

theorem neg_neg (a : G) : P.neg (P.neg a) = a := by
  have h1 : P.add (P.add (P.neg (P.neg a)) (P.neg a)) a = P.add P.zero a := by
    rw [P.neg_add]
  rw [P.add_assoc, P.neg_add, P.add_zero, P.zero_add] at h1
  exact h1

/-- Cancellation: `a + x = a` forces `x = 0`. -/
theorem cancel {a x : G} (h : P.add a x = a) : x = P.zero := by
  have h1 : P.add (P.neg a) (P.add a x) = P.add (P.neg a) a := by rw [h]
  rw [← P.add_assoc, P.neg_add, P.zero_add] at h1
  exact h1

end AbGroup

/-- The three values an edge phase can take, as a tag: decided on sites,
interpreted in `G`. -/
inductive Sign where
  | pos | negs | zero
  deriving DecidableEq, Repr

def Sign.flip : Sign → Sign
  | .pos => .negs
  | .negs => .pos
  | .zero => .zero

/-- The flux `Phi` sits on the square edge `0 -> 1`. -/
def tag (u v : Fin 4) : Sign :=
  if u = 0 ∧ v = 1 then .pos else if u = 1 ∧ v = 0 then .negs else .zero

theorem tag_antisymm : ∀ u v : Fin 4, tag v u = (tag u v).flip := by decide

/-- Which register a hop touches: label `0` (the square particle) gains
the edge tag when the square site changes; label `1` gains nothing. -/
def stag (l : Fin 2) (u v : Fin 4) : Sign :=
  if l = 0 ∧ u ≠ v then tag u v else .zero

theorem stag_antisymm : ∀ (l : Fin 2) (u v : Fin 4), stag l v u = (stag l u v).flip := by
  decide

variable {G : Type} (P : AbGroup G) (Φ : G)

def interp : Sign → G
  | .pos => Φ
  | .negs => P.neg Φ
  | .zero => P.zero

theorem interp_flip : ∀ t : Sign, interp P Φ t.flip = P.neg (interp P Φ t)
  | .pos => rfl
  | .negs => (P.neg_neg Φ).symm
  | .zero => (P.neg_zero).symm

/-- Objects: (square site, edge slot). -/
abbrev Obj := Fin 4 × Fin 2

/-- Carrier: (label, register). -/
abbrev Car (G : Type) := Fin 2 × G

/-- The observer sees labels only. -/
def phaseObs (G : Type) : DiffObs (Car G) (Fin 2 × Fin 2) := kernelObs (fun x => x.1)

/-- The transport of the hop `a -> b` on registers. -/
def tr (a b : Obj) (x : Car G) : Car G :=
  (x.1, P.add x.2 (interp P Φ (stag x.1 a.1 b.1)))

theorem tr_inv (a b : Obj) (x : Car G) : tr P Φ b a (tr P Φ a b x) = x := by
  show (x.1, P.add (P.add x.2 (interp P Φ (stag x.1 a.1 b.1)))
      (interp P Φ (stag x.1 b.1 a.1))) = x
  rw [stag_antisymm, interp_flip, P.add_assoc, P.neg_add, P.add_zero]

def trBij (a b : Obj) : Bij (Car G) (Car G) where
  fwd := tr P Φ a b
  bwd := tr P Φ b a
  fwd_bwd := tr_inv P Φ b a
  bwd_fwd := tr_inv P Φ a b

def hopIso (a b : Obj) : PresIso (phaseObs G) (phaseObs G) where
  car := trBij P Φ a b
  res := Bij.rfl' _
  delta_transport _ _ := rfl
  zero_transport _ := Iff.rfl

/-- A hop: the square particle to an adjacent square site with the edge
particle still, or the edge particle to the other slot with the square
particle still. -/
def hopB (a b : Obj) : Bool :=
  (a.2 == b.2 && Hop.squareAdj a.1.val b.1.val) || (a.1 == b.1 && a.2 != b.2)

def family : HFamily where
  Obj := Obj
  car _ := Car G
  res _ := Fin 2 × Fin 2
  obs _ := phaseObs G
  Hom a b := PLift (hopB a b = true)
  iso a b _ := hopIso P Φ a b

/-- The pair (square particle at register `0`, edge particle at register `0`). -/
def pair0 : NonZeroPair (phaseObs G) :=
  ⟨((0, P.zero), (1, P.zero)), fun e => (by decide : ((0 : Fin 2) = 1) → False) e⟩

def hop (a b : Obj) (h : hopB a b = true := by decide) : (family P Φ).Hom a b := ⟨h⟩

/-- The square particle circulates `0 -> 1 -> 3 -> 2 -> 0` with the edge
particle in slot `0`. -/
def walk : Walk (family P Φ) (0, 0) (0, 0) :=
  .cons (.fwd (hop P Φ (0, 0) (1, 0)))
    (.cons (.fwd (hop P Φ (1, 0) (3, 0)))
      (.cons (.fwd (hop P Φ (3, 0) (2, 0)))
        (.cons (.fwd (hop P Φ (2, 0) (0, 0))) .nil)))

/-- The walk's composite on the carrier. -/
def comp (x : Car G) : Car G :=
  tr P Φ (2, 0) (0, 0) (tr P Φ (3, 0) (2, 0) (tr P Φ (1, 0) (3, 0) (tr P Φ (0, 0) (1, 0) x)))

theorem walk_transport_val (p : NonZeroPair (phaseObs G)) :
    ((walk P Φ).transport p).val = (comp P Φ p.val.1, comp P Φ p.val.2) :=
  rfl

/-- The square particle's register gains exactly `Phi` around the walk. -/
theorem comp_label0 (φ : G) : comp P Φ (0, φ) = (0, P.add φ Φ) := by
  show (0, P.add (P.add (P.add (P.add φ Φ) P.zero) P.zero) P.zero) = _
  rw [P.add_zero, P.add_zero, P.add_zero]

/-- The edge particle's register is unchanged. -/
theorem comp_label1 (φ : G) : comp P Φ (1, φ) = (1, φ) := by
  show (1, P.add (P.add (P.add (P.add φ P.zero) P.zero) P.zero) P.zero) = _
  rw [P.add_zero, P.add_zero, P.add_zero, P.add_zero]

theorem two_labels : ∀ l l' : Fin 2, l ≠ l' → l = 0 ∨ l' = 0 := by decide

/-- A pair fixed by the walk forces `Phi = 0`: one of its two labels is
the square particle, whose register moved by `Phi`. -/
theorem flux_zero_of_fixed (p : NonZeroPair (phaseObs G))
    (e : (walk P Φ).transport p = p) : Φ = P.zero := by
  have hv := congrArg Subtype.val e
  rw [walk_transport_val] at hv
  have h1 : comp P Φ p.val.1 = p.val.1 := congrArg Prod.fst hv
  have h2 : comp P Φ p.val.2 = p.val.2 := congrArg Prod.snd hv
  have hne : p.val.1.1 ≠ p.val.2.1 := p.property
  rcases two_labels _ _ hne with h0 | h0
  · have hx : comp P Φ (0, p.val.1.2) = (0, p.val.1.2) := by
      rw [← h0]; exact h1
    rw [comp_label0] at hx
    exact P.cancel (congrArg Prod.snd hx)
  · have hx : comp P Φ (0, p.val.2.2) = (0, p.val.2.2) := by
      rw [← h0]; exact h2
    rw [comp_label0] at hx
    exact P.cancel (congrArg Prod.snd hx)

/-- **Nonzero flux: no natural section**, with the permutation part of the
holonomy the identity -- a pure phase obstruction. -/
theorem no_natural_section_of_flux (hΦ : Φ ≠ P.zero) :
    ¬ ∃ s : HSec (family P Φ), HIsNatural (family P Φ) s :=
  fun ⟨s, hs⟩ =>
    hΦ (flux_zero_of_fixed P Φ (s (0, 0)) (Walk.transport_of_natural hs (walk P Φ)))

theorem interp_zero_flux : ∀ t : Sign, interp P P.zero t = P.zero
  | .pos => rfl
  | .negs => P.neg_zero
  | .zero => rfl

/-- **Zero flux: the constant pair is natural** -- every transport is the
identity on registers. -/
theorem constant_natural_of_zero_flux :
    HIsNatural (family P P.zero) (fun _ => pair0 P) := by
  intro a b _
  apply Subtype.ext
  show ((0, P.add P.zero (interp P P.zero (stag 0 a.1 b.1))),
        (1, P.add P.zero (interp P P.zero (stag 1 a.1 b.1)))) =
      ((0, P.zero), (1, P.zero))
  rw [interp_zero_flux, interp_zero_flux, P.add_zero]

/-- **The iff, for any phase group.**  No decidability of `G` is used: the
forward direction cancels in the group, the backward direction is the
constant section. -/
theorem section_iff_flux_zero :
    (∃ s : HSec (family P Φ), HIsNatural (family P Φ) s) ↔ Φ = P.zero := by
  constructor
  · intro ⟨s, hs⟩
    exact flux_zero_of_fixed P Φ (s (0, 0)) (Walk.transport_of_natural hs (walk P Φ))
  · intro hΦ
    subst hΦ
    exact ⟨fun _ => pair0 P, constant_natural_of_zero_flux P⟩

/-! ## The finite instance the Python computed -/

/-- `Z_4`, the modulus of `holonomy_phase.py`. -/
def fin4Phase : AbGroup (Fin 4) where
  add := (· + ·)
  zero := 0
  neg := fun x => 0 - x
  add_assoc := by decide
  zero_add := by decide
  add_zero := by decide
  add_neg := by decide
  neg_add := by decide

/-- The general theorem at `Z_4`: section iff flux `0`, as computed. -/
theorem section_iff_flux_zero_fin4 (Φ : Fin 4) :
    (∃ s : HSec (family fin4Phase Φ), HIsNatural (family fin4Phase Φ) s) ↔ Φ = 0 :=
  section_iff_flux_zero fin4Phase Φ

end NaturalSections.HopPhase
