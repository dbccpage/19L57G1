import NaturalSections
import NaturalSections.HopFixturePhase

/-!
# Faces: the chord square, over ANY phase group

The first two-dimensional rung.  Four objects, five edges: the square
`0-1, 1-3, 3-2, 2-0` plus the chord `0-3`, giving two triangular faces
`T1 = 0-1-3` and `T2 = 0-3-2` whose boundaries share the chord and
compose to the outer square walk.  Each edge carries a phase in an
arbitrary `AbGroup` (no finiteness, no decidability of the fibre); as
on the phase rung, the carrier is `(label, register)` with two labels,
and only the label-`0` particle's register moves.

Results.  `outer_flux_eq_add`: the outer walk's flux is the sum of the
two face fluxes, by the group laws alone.  `section_iff_faces_zero`: a
natural section exists iff BOTH face fluxes vanish -- forward by
walking each triangle and cancelling, backward by an explicit
potential on the four objects.  `fill_transfers`: with `T1`'s flux
zero, the section criterion is exactly `T2`'s flux.
`outer_zero_but_obstructed`: for every nonzero `Phi` there is an
assignment with outer flux zero and no natural section -- the outer
boundary sum cannot see an interior obstruction that the faces see.
AuthorityEffect: None.
-/

namespace NaturalSections.TwoCell

open DiffInterface ContactKernel PresentationNaturality
open NaturalSections.HopPhase

/-- The five edges of the chord square. -/
inductive E5 where
  | e01 | e13 | e32 | e20 | e03
  deriving DecidableEq, Repr

/-- A formal edge phase: an edge symbol with a sign, or zero.  Decided
on sites, interpreted in `G` only afterwards. -/
inductive Tag where
  | zero
  | plus (e : E5)
  | minus (e : E5)
  deriving DecidableEq, Repr

def Tag.flip : Tag → Tag
  | .zero => .zero
  | .plus e => .minus e
  | .minus e => .plus e

/-- Which formal phase a hop `u -> v` gains. -/
def tag (u v : Fin 4) : Tag :=
  match u.val, v.val with
  | 0, 1 => .plus .e01
  | 1, 0 => .minus .e01
  | 1, 3 => .plus .e13
  | 3, 1 => .minus .e13
  | 3, 2 => .plus .e32
  | 2, 3 => .minus .e32
  | 2, 0 => .plus .e20
  | 0, 2 => .minus .e20
  | 0, 3 => .plus .e03
  | 3, 0 => .minus .e03
  | _, _ => .zero

theorem tag_antisymm : ∀ u v : Fin 4, tag v u = (tag u v).flip := by decide

/-- Adjacency IS having a tagged edge: five edges, both orientations. -/
def adjB (u v : Fin 4) : Bool := decide (tag u v ≠ Tag.zero)

/-- Which register a hop touches: the label-`0` particle gains the edge
tag; the label-`1` particle gains nothing. -/
def stag (l : Fin 2) (u v : Fin 4) : Tag :=
  if l = 0 then tag u v else Tag.zero

theorem stag_antisymm : ∀ (l : Fin 2) (u v : Fin 4), stag l v u = (stag l u v).flip := by
  decide

variable {G : Type} (P : AbGroup G) (w : E5 → G)

/-- Interpret a formal phase in `G` under the edge assignment `w`. -/
def interp : Tag → G
  | .zero => P.zero
  | .plus e => w e
  | .minus e => P.neg (w e)

theorem interp_flip : ∀ t : Tag, interp P w t.flip = P.neg (interp P w t)
  | .zero => (P.neg_zero).symm
  | .plus _ => rfl
  | .minus _ => (P.neg_neg _).symm

/-- The transport of the hop `a -> b` on carriers. -/
def tr (a b : Fin 4) (x : Car G) : Car G :=
  (x.1, P.add x.2 (interp P w (stag x.1 a b)))

theorem tr_inv (a b : Fin 4) (x : Car G) : tr P w b a (tr P w a b x) = x := by
  show (x.1, P.add (P.add x.2 (interp P w (stag x.1 a b)))
      (interp P w (stag x.1 b a))) = x
  rw [stag_antisymm, interp_flip, P.add_assoc, P.neg_add, P.add_zero]

def trBij (a b : Fin 4) : Bij (Car G) (Car G) where
  fwd := tr P w a b
  bwd := tr P w b a
  fwd_bwd := tr_inv P w b a
  bwd_fwd := tr_inv P w a b

def hopIso (a b : Fin 4) : PresIso (phaseObs G) (phaseObs G) where
  car := trBij P w a b
  res := Bij.rfl' _
  delta_transport _ _ := rfl
  zero_transport _ := Iff.rfl

/-- The chord-square family. -/
def family : HFamily where
  Obj := Fin 4
  car _ := Car G
  res _ := Fin 2 × Fin 2
  obs _ := phaseObs G
  Hom a b := PLift (adjB a b = true)
  iso a b _ := hopIso P w a b

def hop (a b : Fin 4) (h : adjB a b = true := by decide) : (family P w).Hom a b := ⟨h⟩

/-! ## The three closed walks at `0` -/

/-- The boundary of face `T1`: `0 -> 1 -> 3 -> 0` (back across the chord). -/
def wT1 : Walk (family P w) (0 : Fin 4) (0 : Fin 4) :=
  .cons (.fwd (hop P w 0 1))
    (.cons (.fwd (hop P w 1 3))
      (.cons (.fwd (hop P w 3 0)) .nil))

/-- The boundary of face `T2`: `0 -> 3 -> 2 -> 0` (out across the chord). -/
def wT2 : Walk (family P w) (0 : Fin 4) (0 : Fin 4) :=
  .cons (.fwd (hop P w 0 3))
    (.cons (.fwd (hop P w 3 2))
      (.cons (.fwd (hop P w 2 0)) .nil))

/-- The outer square walk: `0 -> 1 -> 3 -> 2 -> 0`, no chord. -/
def wOuter : Walk (family P w) (0 : Fin 4) (0 : Fin 4) :=
  .cons (.fwd (hop P w 0 1))
    (.cons (.fwd (hop P w 1 3))
      (.cons (.fwd (hop P w 3 2))
        (.cons (.fwd (hop P w 2 0)) .nil)))

/-! ## Fluxes -/

def fluxT1 : G := P.add (P.add (w .e01) (w .e13)) (P.neg (w .e03))
def fluxT2 : G := P.add (P.add (w .e03) (w .e32)) (w .e20)
def fluxOuter : G := P.add (P.add (P.add (w .e01) (w .e13)) (w .e32)) (w .e20)

/-- **The boundary identity**: the outer flux is the sum of the two
face fluxes -- the shared chord cancels.  Group laws only; no
commutativity is used. -/
theorem outer_flux_eq_add : fluxOuter P w = P.add (fluxT1 P w) (fluxT2 P w) := by
  show P.add (P.add (P.add (w .e01) (w .e13)) (w .e32)) (w .e20) =
    P.add (P.add (P.add (w .e01) (w .e13)) (P.neg (w .e03)))
      (P.add (P.add (w .e03) (w .e32)) (w .e20))
  rw [P.add_assoc (P.add (w .e01) (w .e13)) (P.neg (w .e03)),
    P.add_assoc (w .e03) (w .e32) (w .e20),
    ← P.add_assoc (P.neg (w .e03)) (w .e03),
    P.neg_add, P.zero_add, P.add_assoc]

/-! ## Walking the faces: a section forces both face fluxes to zero -/

def compT1 (x : Car G) : Car G := tr P w 3 0 (tr P w 1 3 (tr P w 0 1 x))
def compT2 (x : Car G) : Car G := tr P w 2 0 (tr P w 3 2 (tr P w 0 3 x))

theorem wT1_transport_val (p : NonZeroPair (phaseObs G)) :
    ((wT1 P w).transport p).val = (compT1 P w p.val.1, compT1 P w p.val.2) :=
  rfl

theorem wT2_transport_val (p : NonZeroPair (phaseObs G)) :
    ((wT2 P w).transport p).val = (compT2 P w p.val.1, compT2 P w p.val.2) :=
  rfl

theorem compT1_label0 (φ : G) : compT1 P w (0, φ) = (0, P.add φ (fluxT1 P w)) := by
  show (0, P.add (P.add (P.add φ (w .e01)) (w .e13)) (P.neg (w .e03))) =
    (0, P.add φ (P.add (P.add (w .e01) (w .e13)) (P.neg (w .e03))))
  rw [P.add_assoc (P.add φ (w .e01)) (w .e13) (P.neg (w .e03)),
    P.add_assoc φ (w .e01),
    ← P.add_assoc (w .e01) (w .e13) (P.neg (w .e03))]

theorem compT1_label1 (φ : G) : compT1 P w (1, φ) = (1, φ) := by
  show (1, P.add (P.add (P.add φ P.zero) P.zero) P.zero) = (1, φ)
  rw [P.add_zero, P.add_zero, P.add_zero]

theorem compT2_label0 (φ : G) : compT2 P w (0, φ) = (0, P.add φ (fluxT2 P w)) := by
  show (0, P.add (P.add (P.add φ (w .e03)) (w .e32)) (w .e20)) =
    (0, P.add φ (P.add (P.add (w .e03) (w .e32)) (w .e20)))
  rw [P.add_assoc (P.add φ (w .e03)) (w .e32) (w .e20),
    P.add_assoc φ (w .e03),
    ← P.add_assoc (w .e03) (w .e32) (w .e20)]

theorem fluxT1_zero_of_fixed (p : NonZeroPair (phaseObs G))
    (e : (wT1 P w).transport p = p) : fluxT1 P w = P.zero := by
  have hv := congrArg Subtype.val e
  rw [wT1_transport_val] at hv
  have h1 : compT1 P w p.val.1 = p.val.1 := congrArg Prod.fst hv
  have h2 : compT1 P w p.val.2 = p.val.2 := congrArg Prod.snd hv
  have hne : p.val.1.1 ≠ p.val.2.1 := p.property
  rcases two_labels _ _ hne with h0 | h0
  · have hx : compT1 P w (0, p.val.1.2) = (0, p.val.1.2) := by
      rw [← h0]; exact h1
    rw [compT1_label0] at hx
    exact P.cancel (congrArg Prod.snd hx)
  · have hx : compT1 P w (0, p.val.2.2) = (0, p.val.2.2) := by
      rw [← h0]; exact h2
    rw [compT1_label0] at hx
    exact P.cancel (congrArg Prod.snd hx)

theorem fluxT2_zero_of_fixed (p : NonZeroPair (phaseObs G))
    (e : (wT2 P w).transport p = p) : fluxT2 P w = P.zero := by
  have hv := congrArg Subtype.val e
  rw [wT2_transport_val] at hv
  have h1 : compT2 P w p.val.1 = p.val.1 := congrArg Prod.fst hv
  have h2 : compT2 P w p.val.2 = p.val.2 := congrArg Prod.snd hv
  have hne : p.val.1.1 ≠ p.val.2.1 := p.property
  rcases two_labels _ _ hne with h0 | h0
  · have hx : compT2 P w (0, p.val.1.2) = (0, p.val.1.2) := by
      rw [← h0]; exact h1
    rw [compT2_label0] at hx
    exact P.cancel (congrArg Prod.snd hx)
  · have hx : compT2 P w (0, p.val.2.2) = (0, p.val.2.2) := by
      rw [← h0]; exact h2
    rw [compT2_label0] at hx
    exact P.cancel (congrArg Prod.snd hx)

/-- A natural section forces BOTH face fluxes to zero. -/
theorem section_fluxes_zero (s : HSec (family P w)) (hs : HIsNatural (family P w) s) :
    fluxT1 P w = P.zero ∧ fluxT2 P w = P.zero :=
  ⟨fluxT1_zero_of_fixed P w (s (0 : Fin 4)) (Walk.transport_of_natural hs (wT1 P w)),
   fluxT2_zero_of_fixed P w (s (0 : Fin 4)) (Walk.transport_of_natural hs (wT2 P w))⟩

/-! ## Group helpers (from the five laws; no commutativity) -/

theorem eq_of_add_neg_eq_zero {x y : G} (h : P.add x (P.neg y) = P.zero) : x = y := by
  have h1 : P.add (P.add x (P.neg y)) y = P.add P.zero y := by rw [h]
  rw [P.add_assoc, P.neg_add, P.add_zero, P.zero_add] at h1
  exact h1

theorem eq_neg_of_add_eq_zero {x y : G} (h : P.add x y = P.zero) : x = P.neg y := by
  have h1 : P.add (P.add x y) (P.neg y) = P.add P.zero (P.neg y) := by rw [h]
  rw [P.add_assoc, P.add_neg, P.add_zero, P.zero_add] at h1
  exact h1

theorem add_neg_cancel_right (x y : G) : P.add (P.add x y) (P.neg y) = x := by
  rw [P.add_assoc, P.add_neg, P.add_zero]

/-! ## Both faces flat: the explicit potential is a natural section -/

/-- The potential: register the label-`0` particle carries at each
object.  `theta 0 = 0`; the rest follow the tree `0-1-3` and the edge
`2-0`. -/
def theta (v : Fin 4) : G :=
  match v.val with
  | 0 => P.zero
  | 1 => w .e01
  | 2 => P.neg (w .e20)
  | _ => P.add (w .e01) (w .e13)

def pairAt (t : G) : NonZeroPair (phaseObs G) :=
  ⟨((0, t), (1, P.zero)), fun e => (by decide : ((0 : Fin 2) = 1) → False) e⟩

/-- One hop of the candidate section: if the potential moves by exactly
the edge phase, the hop's transport carries the pair at `theta a` to
the pair at `theta b`. -/
theorem pair_step (a b : Fin 4)
    (h : P.add (theta P w a) (interp P w (tag a b)) = theta P w b) :
    (hopIso P w a b).mapPair (pairAt P (theta P w a)) = pairAt P (theta P w b) := by
  apply Subtype.ext
  show ((0, P.add (theta P w a) (interp P w (stag 0 a b))),
        (1, P.add P.zero (interp P w (stag 1 a b)))) =
      ((0, theta P w b), (1, P.zero))
  show ((0, P.add (theta P w a) (interp P w (tag a b))),
        (1, P.add P.zero P.zero)) =
      ((0, theta P w b), (1, P.zero))
  rw [P.add_zero, h]

theorem potential_natural (h1 : fluxT1 P w = P.zero) (h2 : fluxT2 P w = P.zero) :
    HIsNatural (family P w) (fun v => pairAt P (theta P w v)) := by
  have hc : P.add (w .e01) (w .e13) = w .e03 := eq_of_add_neg_eq_zero P h1
  have hd : P.add (w .e03) (w .e32) = P.neg (w .e20) := eq_neg_of_add_eq_zero P h2
  have hce : w .e03 = P.add (P.neg (w .e20)) (P.neg (w .e32)) := by
    have h3 := (add_neg_cancel_right P (w .e03) (w .e32)).symm
    rw [hd] at h3
    exact h3
  have h4 : ∀ v : Fin 4, v = 0 ∨ v = 1 ∨ v = 2 ∨ v = 3 := by decide
  intro a b hab
  rcases h4 a with ha | ha | ha | ha <;> subst ha <;>
    rcases h4 b with hb | hb | hb | hb <;> subst hb <;>
    try exact Bool.noConfusion hab.down
  · exact pair_step P w 0 1 (P.zero_add _)
  · exact pair_step P w 0 2 (P.zero_add _)
  · exact pair_step P w 0 3 (by
      show P.add P.zero (w .e03) = P.add (w .e01) (w .e13)
      rw [P.zero_add]; exact hc.symm)
  · exact pair_step P w 1 0 (P.add_neg _)
  · exact pair_step P w 1 3 rfl
  · exact pair_step P w 2 0 (P.neg_add _)
  · exact pair_step P w 2 3 (by
      show P.add (P.neg (w .e20)) (P.neg (w .e32)) = P.add (w .e01) (w .e13)
      rw [hc]; exact hce.symm)
  · exact pair_step P w 3 0 h1
  · exact pair_step P w 3 1 (add_neg_cancel_right P _ _)
  · exact pair_step P w 3 2 (by
      show P.add (P.add (w .e01) (w .e13)) (w .e32) = P.neg (w .e20)
      rw [hc]; exact hd)

/-- **The iff, for any phase group**: a natural section exists iff both
face fluxes vanish. -/
theorem section_iff_faces_zero :
    (∃ s : HSec (family P w), HIsNatural (family P w) s) ↔
      (fluxT1 P w = P.zero ∧ fluxT2 P w = P.zero) := by
  constructor
  · intro ⟨s, hs⟩
    exact section_fluxes_zero P w s hs
  · intro ⟨h1, h2⟩
    exact ⟨fun v => pairAt P (theta P w v), potential_natural P w h1 h2⟩

/-- **Filling transfers the obstruction**: with face `T1` admitted
(flux forced to zero), the section criterion is exactly the other
face's flux. -/
theorem fill_transfers (h1 : fluxT1 P w = P.zero) :
    (∃ s : HSec (family P w), HIsNatural (family P w) s) ↔ fluxT2 P w = P.zero := by
  rw [section_iff_faces_zero]
  exact ⟨fun h => h.2, fun h => ⟨h1, h⟩⟩

/-! ## The outer boundary is blind -/

/-- The separating assignment: `Phi` on `1-3`, `-Phi` on `3-2`, zero
elsewhere. -/
def wCtr (Φ : G) : E5 → G
  | .e13 => Φ
  | .e32 => P.neg Φ
  | _ => P.zero

theorem ctr_fluxT1 (Φ : G) : fluxT1 P (wCtr P Φ) = Φ := by
  show P.add (P.add P.zero Φ) (P.neg P.zero) = Φ
  rw [P.zero_add, P.neg_zero, P.add_zero]

theorem ctr_fluxOuter (Φ : G) : fluxOuter P (wCtr P Φ) = P.zero := by
  show P.add (P.add (P.add P.zero Φ) (P.neg Φ)) P.zero = P.zero
  rw [P.add_zero, P.zero_add, P.add_neg]

/-- **The outer boundary sum cannot see the interior obstruction**:
for every nonzero `Phi`, the separating assignment has outer flux zero
and no natural section. -/
theorem outer_zero_but_obstructed (Φ : G) (hΦ : Φ ≠ P.zero) :
    fluxOuter P (wCtr P Φ) = P.zero ∧
      ¬ ∃ s : HSec (family P (wCtr P Φ)), HIsNatural (family P (wCtr P Φ)) s := by
  refine ⟨ctr_fluxOuter P Φ, fun hex => hΦ ?_⟩
  have h := (section_iff_faces_zero P (wCtr P Φ)).mp hex
  rw [← ctr_fluxT1 P Φ]
  exact h.1

/-! ## The finite instance the Python surveys -/

/-- The general iff at `Z_4`, one of the moduli `two_complex.py`
enumerates. -/
theorem section_iff_faces_zero_fin4 (w : E5 → Fin 4) :
    (∃ s : HSec (family fin4Phase w), HIsNatural (family fin4Phase w) s) ↔
      (fluxT1 fin4Phase w = 0 ∧ fluxT2 fin4Phase w = 0) :=
  section_iff_faces_zero fin4Phase w

end NaturalSections.TwoCell
