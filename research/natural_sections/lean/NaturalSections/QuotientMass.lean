import NaturalSections
import NaturalSections.HopFixturePhase
import NaturalSections.TwoComplex

/-!
# Repair mass: pricing the chord-square obstruction

The faces rung decided existence: a natural section exists iff both
face fluxes vanish.  This module prices non-existence.  `d0` is the
gauge coboundary (potential differences per oriented edge), the
residual is `w - d0 theta`, and the SUPPORT mass counts the edges a
gauge-equivalent assignment must still carry (`DecidableEq` on the
fibre is declared for the mass; nothing else changes).

Results.  `repair_mass_zero_iff_faces_zero` and
`repair_mass_zero_iff_section` (commutativity-FREE): some repair has
mass zero iff both face fluxes vanish iff a natural section exists.
With declared commutativity: `residual_flux1/2` and
`reaches_of_sameClass` -- the gauge classes are exactly the flux
pairs; `repair_mass_le_one_iff` -- price at most one iff the class
lies on a declared axis (`f1 = 0`, `f2 = 0`, or the chord's
anti-diagonal `f2 = -f1`); `pairRep_*` -- price at most two, always.
The existence layer used only the five group laws; the pricing layer
buys commutativity, and that asymmetry is deliberate and recorded.
AuthorityEffect: None.
-/

namespace NaturalSections.QMass

open DiffInterface ContactKernel PresentationNaturality
open NaturalSections.HopPhase
open NaturalSections.TwoCell

variable {G : Type} (P : AbGroup G)

/-! ## Group helpers, commutativity-free -/

theorem neg_of_add_eq_zero {a c : G} (h : P.add a c = P.zero) : c = P.neg a := by
  have h1 : P.add (P.neg a) (P.add a c) = P.add (P.neg a) P.zero := by rw [h]
  rw [← P.add_assoc, P.neg_add, P.zero_add, P.add_zero] at h1
  exact h1

theorem neg_add_rev (x y : G) : P.neg (P.add x y) = P.add (P.neg y) (P.neg x) := by
  have h : P.add (P.add x y) (P.add (P.neg y) (P.neg x)) = P.zero := by
    rw [P.add_assoc, ← P.add_assoc y (P.neg y) (P.neg x), P.add_neg, P.zero_add, P.add_neg]
  exact (neg_of_add_eq_zero P h).symm

/-! ## The gauge coboundary and its telescopes -/

/-- Potential difference along `a -> b`, left convention. -/
def pot (θ : Fin 4 → G) (a b : Fin 4) : G := P.add (P.neg (θ a)) (θ b)

/-- The gauge coboundary: one potential difference per oriented edge. -/
def d0 (θ : Fin 4 → G) : E5 → G
  | .e01 => pot P θ 0 1
  | .e13 => pot P θ 1 3
  | .e32 => pot P θ 3 2
  | .e20 => pot P θ 2 0
  | .e03 => pot P θ 0 3

theorem fluxT1_d0 (θ : Fin 4 → G) : fluxT1 P (d0 P θ) = P.zero := by
  show P.add (P.add (P.add (P.neg (θ 0)) (θ 1)) (P.add (P.neg (θ 1)) (θ 3)))
      (P.neg (P.add (P.neg (θ 0)) (θ 3))) = P.zero
  rw [neg_add_rev P, P.neg_neg, P.add_assoc (P.neg (θ 0)) (θ 1),
    ← P.add_assoc (θ 1) (P.neg (θ 1)) (θ 3), P.add_neg, P.zero_add,
    P.add_assoc (P.neg (θ 0)) (θ 3),
    ← P.add_assoc (θ 3) (P.neg (θ 3)) (θ 0), P.add_neg, P.zero_add, P.neg_add]

theorem fluxT2_d0 (θ : Fin 4 → G) : fluxT2 P (d0 P θ) = P.zero := by
  show P.add (P.add (P.add (P.neg (θ 0)) (θ 3)) (P.add (P.neg (θ 3)) (θ 2)))
      (P.add (P.neg (θ 2)) (θ 0)) = P.zero
  rw [P.add_assoc (P.neg (θ 0)) (θ 3),
    ← P.add_assoc (θ 3) (P.neg (θ 3)) (θ 2), P.add_neg, P.zero_add,
    P.add_assoc (P.neg (θ 0)) (θ 2),
    ← P.add_assoc (θ 2) (P.neg (θ 2)) (θ 0), P.add_neg, P.zero_add, P.neg_add]

/-! ## Exactness: zero fluxes reach a potential (commutativity-free) -/

variable (w : E5 → G)

/-- The explicit potential: zero at `0`, following the tree `0-1-3`
and the edge `2-0`. -/
def thetaOf : Fin 4 → G := fun v =>
  match v.val with
  | 0 => P.zero
  | 1 => w .e01
  | 2 => P.neg (w .e20)
  | _ => P.add (w .e01) (w .e13)

theorem exact_of_fluxes_zero (h1 : fluxT1 P w = P.zero) (h2 : fluxT2 P w = P.zero) :
    ∀ e, w e = d0 P (thetaOf P w) e := by
  have hc : P.add (w .e01) (w .e13) = w .e03 := eq_of_add_neg_eq_zero P h1
  intro e
  cases e with
  | e01 =>
    show w .e01 = P.add (P.neg P.zero) (w .e01)
    rw [P.neg_zero, P.zero_add]
  | e13 =>
    show w .e13 = P.add (P.neg (w .e01)) (P.add (w .e01) (w .e13))
    rw [← P.add_assoc, P.neg_add, P.zero_add]
  | e32 =>
    show w .e32 = P.add (P.neg (P.add (w .e01) (w .e13))) (P.neg (w .e20))
    rw [hc]
    have h3 : P.add (w .e03) (w .e32) = P.neg (w .e20) := eq_neg_of_add_eq_zero P h2
    have h4 : P.add (P.neg (w .e03)) (P.add (w .e03) (w .e32)) =
        P.add (P.neg (w .e03)) (P.neg (w .e20)) := by rw [h3]
    rw [← P.add_assoc, P.neg_add, P.zero_add] at h4
    exact h4
  | e20 =>
    show w .e20 = P.add (P.neg (P.neg (w .e20))) P.zero
    rw [P.neg_neg, P.add_zero]
  | e03 =>
    show w .e03 = P.add (P.neg P.zero) (P.add (w .e01) (w .e13))
    rw [P.neg_zero, P.zero_add]
    exact hc.symm

/-! ## Support mass -/

def ind [DecidableEq G] (x : G) : Nat := if x = P.zero then 0 else 1

theorem ind_eq_zero_iff [DecidableEq G] (x : G) : ind P x = 0 ↔ x = P.zero := by
  unfold ind
  split <;> simp_all

theorem ind_le_one [DecidableEq G] (x : G) : ind P x ≤ 1 := by
  unfold ind
  split <;> omega

theorem ind_eq_one_of_ne [DecidableEq G] {x : G} (h : x ≠ P.zero) : ind P x = 1 := by
  unfold ind
  split
  · exact absurd ‹x = P.zero› h
  · rfl

/-- The support mass: how many edges carry a nonzero phase. -/
def suppMass [DecidableEq G] (v : E5 → G) : Nat :=
  ind P (v .e01) + ind P (v .e13) + ind P (v .e32) + ind P (v .e20) + ind P (v .e03)

theorem zero_mass_iff [DecidableEq G] (v : E5 → G) :
    suppMass P v = 0 ↔ ∀ e, v e = P.zero := by
  unfold suppMass
  constructor
  · intro h e
    have h01 : ind P (v .e01) = 0 := by omega
    have h13 : ind P (v .e13) = 0 := by omega
    have h32 : ind P (v .e32) = 0 := by omega
    have h20 : ind P (v .e20) = 0 := by omega
    have h03 : ind P (v .e03) = 0 := by omega
    cases e with
    | e01 => exact (ind_eq_zero_iff P _).mp h01
    | e13 => exact (ind_eq_zero_iff P _).mp h13
    | e32 => exact (ind_eq_zero_iff P _).mp h32
    | e20 => exact (ind_eq_zero_iff P _).mp h20
    | e03 => exact (ind_eq_zero_iff P _).mp h03
  · intro h
    have hz := fun e => (ind_eq_zero_iff P (v e)).mpr (h e)
    rw [hz .e01, hz .e13, hz .e32, hz .e20, hz .e03]

theorem suppMass_congr [DecidableEq G] {u v : E5 → G} (h : ∀ e, u e = v e) :
    suppMass P u = suppMass P v := by
  unfold suppMass
  rw [h .e01, h .e13, h .e32, h .e20, h .e03]

/-! ## QM1: zero repair mass = existence (commutativity-free) -/

/-- The residual of `w` after the gauge repair `theta`. -/
def residual (θ : Fin 4 → G) : E5 → G := fun e => P.add (w e) (P.neg (d0 P θ e))

theorem repair_mass_zero_iff_faces_zero [DecidableEq G] :
    (∃ θ : Fin 4 → G, suppMass P (residual P w θ) = 0) ↔
      (fluxT1 P w = P.zero ∧ fluxT2 P w = P.zero) := by
  constructor
  · intro ⟨θ, hm⟩
    have hz := (zero_mass_iff P _).mp hm
    have hw : ∀ e, w e = d0 P θ e := fun e => eq_of_add_neg_eq_zero P (hz e)
    have hfun : w = d0 P θ := funext hw
    rw [hfun]
    exact ⟨fluxT1_d0 P θ, fluxT2_d0 P θ⟩
  · intro ⟨h1, h2⟩
    refine ⟨thetaOf P w, (zero_mass_iff P _).mpr fun e => ?_⟩
    show P.add (w e) (P.neg (d0 P (thetaOf P w) e)) = P.zero
    rw [← exact_of_fluxes_zero P w h1 h2 e, P.add_neg]

/-- **QM1**: some gauge repair has mass zero iff a natural section
exists.  Composes the mass layer with the faces rung; no
commutativity. -/
theorem repair_mass_zero_iff_section [DecidableEq G] :
    (∃ θ : Fin 4 → G, suppMass P (residual P w θ) = 0) ↔
      (∃ s : HSec (TwoCell.family P w), HIsNatural (TwoCell.family P w) s) :=
  (repair_mass_zero_iff_faces_zero P w).trans (section_iff_faces_zero P w).symm

/-! ## The commutative layer: flux additivity and the gauge classes -/

section Comm

theorem add_add_add (comm : ∀ a b : G, P.add a b = P.add b a) (a b c d : G) :
    P.add (P.add a b) (P.add c d) = P.add (P.add a c) (P.add b d) := by
  rw [P.add_assoc, ← P.add_assoc b c d, comm b c, P.add_assoc c b d, ← P.add_assoc]

theorem neg_add' (comm : ∀ a b : G, P.add a b = P.add b a) (x y : G) :
    P.neg (P.add x y) = P.add (P.neg x) (P.neg y) := by
  rw [neg_add_rev P, comm]

theorem fluxT1_add (comm : ∀ a b : G, P.add a b = P.add b a) (u v : E5 → G) :
    fluxT1 P (fun e => P.add (u e) (v e)) = P.add (fluxT1 P u) (fluxT1 P v) := by
  show P.add (P.add (P.add (u .e01) (v .e01)) (P.add (u .e13) (v .e13)))
      (P.neg (P.add (u .e03) (v .e03))) =
    P.add (P.add (P.add (u .e01) (u .e13)) (P.neg (u .e03)))
      (P.add (P.add (v .e01) (v .e13)) (P.neg (v .e03)))
  rw [add_add_add P comm, neg_add' P comm, add_add_add P comm]

theorem fluxT2_add (comm : ∀ a b : G, P.add a b = P.add b a) (u v : E5 → G) :
    fluxT2 P (fun e => P.add (u e) (v e)) = P.add (fluxT2 P u) (fluxT2 P v) := by
  show P.add (P.add (P.add (u .e03) (v .e03)) (P.add (u .e32) (v .e32)))
      (P.add (u .e20) (v .e20)) =
    P.add (P.add (P.add (u .e03) (u .e32)) (u .e20))
      (P.add (P.add (v .e03) (v .e32)) (v .e20))
  rw [add_add_add P comm (u .e03) (v .e03) (u .e32) (v .e32),
    add_add_add P comm (P.add (u .e03) (u .e32)) (P.add (v .e03) (v .e32))
      (u .e20) (v .e20)]

theorem fluxT1_neg (comm : ∀ a b : G, P.add a b = P.add b a) (v : E5 → G) :
    fluxT1 P (fun e => P.neg (v e)) = P.neg (fluxT1 P v) := by
  show P.add (P.add (P.neg (v .e01)) (P.neg (v .e13))) (P.neg (P.neg (v .e03))) =
    P.neg (P.add (P.add (v .e01) (v .e13)) (P.neg (v .e03)))
  rw [neg_add' P comm, neg_add' P comm]

theorem fluxT2_neg (comm : ∀ a b : G, P.add a b = P.add b a) (v : E5 → G) :
    fluxT2 P (fun e => P.neg (v e)) = P.neg (fluxT2 P v) := by
  show P.add (P.add (P.neg (v .e03)) (P.neg (v .e32))) (P.neg (v .e20)) =
    P.neg (P.add (P.add (v .e03) (v .e32)) (v .e20))
  rw [neg_add' P comm, neg_add' P comm]

/-- **QM2, one direction**: every repair stays in the flux class. -/
theorem residual_flux1 (comm : ∀ a b : G, P.add a b = P.add b a) (θ : Fin 4 → G) :
    fluxT1 P (residual P w θ) = fluxT1 P w := by
  have h : fluxT1 P (residual P w θ) =
      P.add (fluxT1 P w) (fluxT1 P (fun e => P.neg (d0 P θ e))) :=
    fluxT1_add P comm w (fun e => P.neg (d0 P θ e))
  rw [fluxT1_neg P comm (d0 P θ), fluxT1_d0 P θ, P.neg_zero, P.add_zero] at h
  exact h

theorem residual_flux2 (comm : ∀ a b : G, P.add a b = P.add b a) (θ : Fin 4 → G) :
    fluxT2 P (residual P w θ) = fluxT2 P w := by
  have h : fluxT2 P (residual P w θ) =
      P.add (fluxT2 P w) (fluxT2 P (fun e => P.neg (d0 P θ e))) :=
    fluxT2_add P comm w (fun e => P.neg (d0 P θ e))
  rw [fluxT2_neg P comm (d0 P θ), fluxT2_d0 P θ, P.neg_zero, P.add_zero] at h
  exact h

/-- **QM2, other direction**: anything in the flux class is reached by
some repair -- the gauge classes are exactly the flux pairs. -/
theorem reaches_of_sameClass (comm : ∀ a b : G, P.add a b = P.add b a) (w' : E5 → G)
    (h1 : fluxT1 P w' = fluxT1 P w) (h2 : fluxT2 P w' = fluxT2 P w) :
    ∃ θ, ∀ e, w' e = residual P w θ e := by
  have hf1 : fluxT1 P (fun e => P.add (w e) (P.neg (w' e))) = P.zero := by
    have h := fluxT1_add P comm w (fun e => P.neg (w' e))
    rw [fluxT1_neg P comm w', h1, P.add_neg] at h
    exact h
  have hf2 : fluxT2 P (fun e => P.add (w e) (P.neg (w' e))) = P.zero := by
    have h := fluxT2_add P comm w (fun e => P.neg (w' e))
    rw [fluxT2_neg P comm w', h2, P.add_neg] at h
    exact h
  refine ⟨thetaOf P (fun e => P.add (w e) (P.neg (w' e))), fun e => ?_⟩
  have hdiff : ∀ e, P.add (w e) (P.neg (w' e)) =
      d0 P (thetaOf P (fun e => P.add (w e) (P.neg (w' e)))) e :=
    exact_of_fluxes_zero P (fun e => P.add (w e) (P.neg (w' e))) hf1 hf2
  show w' e = P.add (w e) (P.neg (d0 P _ e))
  rw [← hdiff e, neg_add_rev P, P.neg_neg, comm (w' e) (P.neg (w e)),
    ← P.add_assoc, P.add_neg, P.zero_add]

/-! ## QM3: the exact price under the support mass -/

end Comm

/-- The single-edge assignment. -/
def single (e0 : E5) (c : G) : E5 → G := fun e => if e = e0 then c else P.zero

theorem single_mass_le_one [DecidableEq G] (e0 : E5) (c : G) :
    suppMass P (single P e0 c) ≤ 1 := by
  have h0 : ind P P.zero = 0 := (ind_eq_zero_iff P _).mpr rfl
  have h1 := ind_le_one P c
  cases e0 with
  | e01 =>
    show ind P c + ind P P.zero + ind P P.zero + ind P P.zero + ind P P.zero ≤ 1
    omega
  | e13 =>
    show ind P P.zero + ind P c + ind P P.zero + ind P P.zero + ind P P.zero ≤ 1
    omega
  | e32 =>
    show ind P P.zero + ind P P.zero + ind P c + ind P P.zero + ind P P.zero ≤ 1
    omega
  | e20 =>
    show ind P P.zero + ind P P.zero + ind P P.zero + ind P c + ind P P.zero ≤ 1
    omega
  | e03 =>
    show ind P P.zero + ind P P.zero + ind P P.zero + ind P P.zero + ind P c ≤ 1
    omega

theorem single_e01_flux1 (c : G) : fluxT1 P (single P .e01 c) = c := by
  show P.add (P.add c P.zero) (P.neg P.zero) = c
  rw [P.add_zero, P.neg_zero, P.add_zero]

theorem single_e01_flux2 (c : G) : fluxT2 P (single P .e01 c) = P.zero := by
  show P.add (P.add P.zero P.zero) P.zero = P.zero
  rw [P.add_zero, P.add_zero]

theorem single_e32_flux1 (c : G) : fluxT1 P (single P .e32 c) = P.zero := by
  show P.add (P.add P.zero P.zero) (P.neg P.zero) = P.zero
  rw [P.zero_add, P.neg_zero, P.add_zero]

theorem single_e32_flux2 (c : G) : fluxT2 P (single P .e32 c) = c := by
  show P.add (P.add P.zero c) P.zero = c
  rw [P.zero_add, P.add_zero]

theorem single_e03_flux1 (c : G) : fluxT1 P (single P .e03 c) = P.neg c := by
  show P.add (P.add P.zero P.zero) (P.neg c) = P.neg c
  rw [P.zero_add, P.zero_add]

theorem single_e03_flux2 (c : G) : fluxT2 P (single P .e03 c) = c := by
  show P.add (P.add c P.zero) P.zero = c
  rw [P.add_zero, P.add_zero]

/-- Any assignment of mass at most one has fluxes on a declared axis:
`f1 = 0`, `f2 = 0`, or the chord's anti-diagonal `f2 = -f1`. -/
theorem mass_le_one_axes [DecidableEq G] (v : E5 → G) (h : suppMass P v ≤ 1) :
    fluxT1 P v = P.zero ∨ fluxT2 P v = P.zero ∨ fluxT2 P v = P.neg (fluxT1 P v) := by
  unfold suppMass at h
  by_cases h03 : v .e03 = P.zero
  · by_cases h32 : v .e32 = P.zero
    · by_cases h20 : v .e20 = P.zero
      · -- e03, e32, e20 all zero: fluxT2 = 0
        refine Or.inr (Or.inl ?_)
        show P.add (P.add (v .e03) (v .e32)) (v .e20) = P.zero
        rw [h03, h32, h20, P.add_zero, P.add_zero]
      · -- e20 nonzero: everything else zero, fluxT1 = 0
        have k20 := ind_eq_one_of_ne P h20
        have i01 : ind P (v .e01) = 0 := by
          have := ind_le_one P (v .e01); have := ind_le_one P (v .e13)
          have := ind_le_one P (v .e32); have := ind_le_one P (v .e03); omega
        have i13 : ind P (v .e13) = 0 := by
          have := ind_le_one P (v .e01); have := ind_le_one P (v .e13)
          have := ind_le_one P (v .e32); have := ind_le_one P (v .e03); omega
        refine Or.inl ?_
        show P.add (P.add (v .e01) (v .e13)) (P.neg (v .e03)) = P.zero
        rw [(ind_eq_zero_iff P _).mp i01, (ind_eq_zero_iff P _).mp i13, h03,
          P.add_zero, P.neg_zero, P.add_zero]
    · -- e32 nonzero: everything else zero, fluxT1 = 0
      have k32 := ind_eq_one_of_ne P h32
      have i01 : ind P (v .e01) = 0 := by
        have := ind_le_one P (v .e01); have := ind_le_one P (v .e13)
        have := ind_le_one P (v .e20); have := ind_le_one P (v .e03); omega
      have i13 : ind P (v .e13) = 0 := by
        have := ind_le_one P (v .e01); have := ind_le_one P (v .e13)
        have := ind_le_one P (v .e20); have := ind_le_one P (v .e03); omega
      refine Or.inl ?_
      show P.add (P.add (v .e01) (v .e13)) (P.neg (v .e03)) = P.zero
      rw [(ind_eq_zero_iff P _).mp i01, (ind_eq_zero_iff P _).mp i13, h03,
        P.add_zero, P.neg_zero, P.add_zero]
  · -- e03 nonzero: everything else zero, the anti-diagonal
    have k03 := ind_eq_one_of_ne P h03
    have i01 : ind P (v .e01) = 0 := by
      have := ind_le_one P (v .e01); have := ind_le_one P (v .e13)
      have := ind_le_one P (v .e32); have := ind_le_one P (v .e20); omega
    have i13 : ind P (v .e13) = 0 := by
      have := ind_le_one P (v .e01); have := ind_le_one P (v .e13)
      have := ind_le_one P (v .e32); have := ind_le_one P (v .e20); omega
    have i32 : ind P (v .e32) = 0 := by
      have := ind_le_one P (v .e01); have := ind_le_one P (v .e13)
      have := ind_le_one P (v .e32); have := ind_le_one P (v .e20); omega
    have i20 : ind P (v .e20) = 0 := by
      have := ind_le_one P (v .e01); have := ind_le_one P (v .e13)
      have := ind_le_one P (v .e32); have := ind_le_one P (v .e20); omega
    refine Or.inr (Or.inr ?_)
    show P.add (P.add (v .e03) (v .e32)) (v .e20) =
      P.neg (P.add (P.add (v .e01) (v .e13)) (P.neg (v .e03)))
    rw [(ind_eq_zero_iff P _).mp i01, (ind_eq_zero_iff P _).mp i13,
      (ind_eq_zero_iff P _).mp i32, (ind_eq_zero_iff P _).mp i20,
      P.add_zero, P.add_zero, P.add_zero, P.zero_add, P.neg_neg]

section Price

/-- **QM3, price at most one**: a repair of mass at most one exists
iff the class lies on a declared axis.  The chord's anti-diagonal is
an axis only because the chord lies in both faces. -/
theorem repair_mass_le_one_iff [DecidableEq G]
    (comm : ∀ a b : G, P.add a b = P.add b a) :
    (∃ θ, suppMass P (residual P w θ) ≤ 1) ↔
      (fluxT1 P w = P.zero ∨ fluxT2 P w = P.zero ∨
        fluxT2 P w = P.neg (fluxT1 P w)) := by
  constructor
  · intro ⟨θ, hm⟩
    have hax := mass_le_one_axes P (residual P w θ) hm
    rw [residual_flux1 P w comm θ, residual_flux2 P w comm θ] at hax
    exact hax
  · intro hax
    have reach : ∀ s : E5 → G, fluxT1 P s = fluxT1 P w → fluxT2 P s = fluxT2 P w →
        suppMass P s ≤ 1 → ∃ θ, suppMass P (residual P w θ) ≤ 1 := by
      intro s hs1 hs2 hsm
      obtain ⟨θ, hθ⟩ := reaches_of_sameClass P w comm s hs1 hs2
      exact ⟨θ, by rw [← suppMass_congr P hθ]; exact hsm⟩
    rcases hax with h1 | h2 | h3
    · refine reach (single P .e32 (fluxT2 P w)) ?_ ?_ (single_mass_le_one P _ _)
      · rw [single_e32_flux1, h1]
      · rw [single_e32_flux2]
    · refine reach (single P .e01 (fluxT1 P w)) ?_ ?_ (single_mass_le_one P _ _)
      · rw [single_e01_flux1]
      · rw [single_e01_flux2, h2]
    · refine reach (single P .e03 (P.neg (fluxT1 P w))) ?_ ?_ (single_mass_le_one P _ _)
      · rw [single_e03_flux1, P.neg_neg]
      · rw [single_e03_flux2, h3]

/-- The two-edge representative carrying the class `(f1, f2)`. -/
def pairRep (f1 f2 : G) : E5 → G
  | .e01 => f1
  | .e32 => f2
  | _ => P.zero

theorem pairRep_flux1 (f1 f2 : G) : fluxT1 P (pairRep P f1 f2) = f1 := by
  show P.add (P.add f1 P.zero) (P.neg P.zero) = f1
  rw [P.add_zero, P.neg_zero, P.add_zero]

theorem pairRep_flux2 (f1 f2 : G) : fluxT2 P (pairRep P f1 f2) = f2 := by
  show P.add (P.add P.zero f2) P.zero = f2
  rw [P.zero_add, P.add_zero]

theorem pairRep_mass_le_two [DecidableEq G] (f1 f2 : G) :
    suppMass P (pairRep P f1 f2) ≤ 2 := by
  have h0 : ind P P.zero = 0 := (ind_eq_zero_iff P _).mpr rfl
  have ha := ind_le_one P f1
  have hb := ind_le_one P f2
  show ind P f1 + ind P P.zero + ind P f2 + ind P P.zero + ind P P.zero ≤ 2
  omega

/-- **QM3, price at most two, always**: every class is repaired to at
most two edges. -/
theorem repair_mass_le_two [DecidableEq G]
    (comm : ∀ a b : G, P.add a b = P.add b a) :
    ∃ θ, suppMass P (residual P w θ) ≤ 2 := by
  obtain ⟨θ, hθ⟩ := reaches_of_sameClass P w comm
    (pairRep P (fluxT1 P w) (fluxT2 P w))
    (pairRep_flux1 P _ _) (pairRep_flux2 P _ _)
  exact ⟨θ, by rw [← suppMass_congr P hθ]; exact pairRep_mass_le_two P _ _⟩

end Price

/-! ## The finite instance the Python surveys -/

/-- QM1 at `Z_4`: zero repair mass iff a natural section exists, at
one of the surveyed moduli. -/
theorem repair_mass_zero_iff_section_fin4 (w : E5 → Fin 4) :
    (∃ θ : Fin 4 → Fin 4, suppMass fin4Phase (residual fin4Phase w θ) = 0) ↔
      (∃ s : HSec (TwoCell.family fin4Phase w),
        HIsNatural (TwoCell.family fin4Phase w) s) :=
  repair_mass_zero_iff_section fin4Phase w

end NaturalSections.QMass
