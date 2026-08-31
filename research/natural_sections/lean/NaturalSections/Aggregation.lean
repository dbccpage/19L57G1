import NaturalSections
import NaturalSections.HopFixturePhase
import NaturalSections.TwoComplex
import NaturalSections.QuotientMass

/-!
# Aggregation: which mass functions are forced

The repair-mass rung declared the support mass.  This module proves
the declaration is thinner than it looks: once per-edge gauges are
declared, ADDITIVITY over concatenations of finite edge lists plus
SINGLETON CALIBRATION force the diagnostic to be the edge sum
(`forced_sum`); with magnitude-sufficiency and homogeneity instead of
calibration, the weighted sum (`forced_weighted_sum`).  Both axioms
are load-bearing: the max aggregator is calibrated and not additive,
the doubled sum is additive and not calibrated (`max_not_additive`,
`scaled_not_calibrated`).  The chord square's support mass is the edge
sum of the indicator gauges (`suppMass_is_edge_sum`), so any additive
calibrated diagnostic on those gauges equals it
(`aggregation_determines_suppMass`).  AuthorityEffect: None.
-/

namespace NaturalSections.Aggregate

open NaturalSections.HopPhase
open NaturalSections.TwoCell
open NaturalSections.QMass

section General

variable {E : Type} {V : E → Type}
variable (j : (e : E) → V e → Nat)
variable (J : List E → ((e : E) → V e) → Nat)

/-- Additivity alone forces the empty list to zero -- no edge is
needed: concatenate the empty list with itself. -/
theorem nil_zero (hadd : ∀ l1 l2 x, J (l1 ++ l2) x = J l1 x + J l2 x)
    (x : (e : E) → V e) : J [] x = 0 := by
  have h : J [] x = J [] x + J [] x := hadd [] [] x
  omega

/-- **AG1**: additivity plus singleton calibration force the edge sum. -/
theorem forced_sum (hadd : ∀ l1 l2 x, J (l1 ++ l2) x = J l1 x + J l2 x)
    (hcal : ∀ e x, J [e] x = j e (x e)) :
    ∀ (l : List E) (x : (e : E) → V e),
      J l x = (l.map (fun e => j e (x e))).sum := by
  intro l x
  induction l with
  | nil => exact nil_zero J hadd x
  | cons a t ih =>
    have h : J (a :: t) x = J [a] x + J t x := hadd [a] t x
    rw [h, hcal a x]
    show j a (x a) + J t x = j a (x a) + (t.map (fun e => j e (x e))).sum
    rw [ih]

/-- **AG2**: additivity plus magnitude-sufficiency plus homogeneity
force the weighted sum, with weight the singleton value at gauge 1. -/
theorem forced_weighted_sum (A : E → Nat → Nat)
    (hadd : ∀ l1 l2 x, J (l1 ++ l2) x = J l1 x + J l2 x)
    (hmag : ∀ e x, J [e] x = A e (j e (x e)))
    (hhom : ∀ e k u, A e (k * u) = k * A e u) :
    ∀ (l : List E) (x : (e : E) → V e),
      J l x = (l.map (fun e => A e 1 * j e (x e))).sum := by
  have hA : ∀ e u, A e u = A e 1 * u := by
    intro e u
    have h := hhom e u 1
    rw [Nat.mul_one] at h
    rw [h, Nat.mul_comm]
  intro l x
  induction l with
  | nil => exact nil_zero J hadd x
  | cons a t ih =>
    have h : J (a :: t) x = J [a] x + J t x := hadd [a] t x
    rw [h, hmag a x, hA a]
    show A a 1 * j a (x a) + J t x =
      A a 1 * j a (x a) + (t.map (fun e => A e 1 * j e (x e))).sum
    rw [ih]

end General

/-! ## AG3: both axioms are load-bearing (two-edge fixture) -/

section Countermodels

/-- The two-edge fixture: two edges, trivial carriers, unit gauges. -/
def unitGauge : Bool → Unit → Nat := fun _ _ => 1

/-- The max aggregator. -/
def maxDiag (l : List Bool) (_ : (e : Bool) → Unit) : Nat :=
  (l.map (fun _ => 1)).foldr Nat.max 0

/-- The max aggregator is calibrated on singletons. -/
theorem max_calibrated (e : Bool) (x : (e : Bool) → Unit) :
    maxDiag [e] x = unitGauge e (x e) := rfl

/-- The max aggregator violates additivity: two unit edges give `1`,
not `2`. -/
theorem max_not_additive :
    ¬ (∀ (l1 l2 : List Bool) (x : (e : Bool) → Unit),
      maxDiag (l1 ++ l2) x = maxDiag l1 x + maxDiag l2 x) := by
  intro h
  exact absurd (h [true] [false] (fun _ => ())) (by decide)

/-- The max aggregator disagrees with the edge sum on the two-edge
list: `1` against `2`. -/
theorem max_disagrees_with_sum :
    maxDiag [true, false] (fun _ => ()) ≠
      (([true, false]).map (fun e => unitGauge e ())).sum := by
  decide

/-- The doubled sum. -/
def scaledDiag (l : List Bool) (_ : (e : Bool) → Unit) : Nat :=
  2 * (l.map (fun _ => 1)).sum

/-- The doubled sum is additive over concatenation. -/
theorem scaled_additive (l1 l2 : List Bool) (x : (e : Bool) → Unit) :
    scaledDiag (l1 ++ l2) x = scaledDiag l1 x + scaledDiag l2 x := by
  unfold scaledDiag
  rw [List.map_append, List.sum_append, Nat.mul_add]

/-- The doubled sum violates singleton calibration: `2` against `1`. -/
theorem scaled_not_calibrated :
    ¬ (∀ (e : Bool) (x : (e : Bool) → Unit),
      scaledDiag [e] x = unitGauge e (x e)) := by
  intro h
  exact absurd (h true (fun _ => ())) (by decide)

end Countermodels

/-! ## AG4: the chord square's support mass is the forced edge sum -/

section TieIn

variable {G : Type} (P : AbGroup G)

/-- The five edges of the chord square, as the declared list. -/
def allEdges : List E5 := [.e01, .e13, .e32, .e20, .e03]

/-- The support mass IS the edge sum of the indicator gauges over the
declared five-edge list. -/
theorem suppMass_is_edge_sum [DecidableEq G] (v : E5 → G) :
    suppMass P v = ((allEdges).map (fun e => ind P (v e))).sum := by
  show ind P (v .e01) + ind P (v .e13) + ind P (v .e32) + ind P (v .e20) +
      ind P (v .e03) =
    ind P (v .e01) + (ind P (v .e13) + (ind P (v .e32) +
      (ind P (v .e20) + (ind P (v .e03) + 0))))
  omega

/-- **AG4**: any additive, calibrated diagnostic over the indicator
gauges equals the support mass on the declared edge list. -/
theorem aggregation_determines_suppMass [DecidableEq G]
    (J : List E5 → (E5 → G) → Nat)
    (hadd : ∀ l1 l2 x, J (l1 ++ l2) x = J l1 x + J l2 x)
    (hcal : ∀ e x, J [e] x = ind P (x e)) (v : E5 → G) :
    J allEdges v = suppMass P v := by
  rw [suppMass_is_edge_sum P v]
  exact forced_sum (V := fun _ => G) (fun e g => ind P g) J hadd hcal allEdges v

end TieIn

end NaturalSections.Aggregate
