/-!
# B1(ii): the cross term is what interference reads

AuthorityEffect: None.  Core Lean only.

* ADMISSION A_amp (priced, not derived): amplitudes in the Gaussian
  integers `ℤ[i]` (pairs of integers), the involution `conj`, the modulus
  `norm c = c·c̄`, and the add-then-square readout `mix (c₁, c₂) =
  norm (c₁ + c₂)` of a two-sector mixing context.  The weights of a
  preparation are its two sector moduli.
* THEOREMS: `polarization` (the readout is the weights plus twice the cross
  term); with weights fixed, a mixing context separates two preparations
  exactly when their cross terms differ (`separates_iff_cross`), so every
  model meeting the challenge has two amplitude pairs on one weight fiber
  (`fiber_necessary`).
* WITNESSES (exact, decided): with the sign group one fiber carries two
  readouts (`sign_pair`, readouts 4 and 0; the QM_122 `mix_separates`
  witness re-proved here); with the four units of `ℤ[i]` one fiber carries
  three (`mu4_triple`, readouts 4, 2, 0); the unit readout on `μ₄` is
  invariant under conjugation and separates the three classes
  (`mu4_readout_invariant`, `mu4_readout_values`).
-/

namespace ResearchQmBridge
namespace Gauss

/-- A Gaussian integer `re + im·i`. -/
structure GI where
  re : Int
  im : Int
deriving DecidableEq, Repr

namespace GI

def add (a b : GI) : GI := ⟨a.re + b.re, a.im + b.im⟩
def mul (a b : GI) : GI := ⟨a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re⟩
def conj (a : GI) : GI := ⟨a.re, -a.im⟩
/-- The modulus `a·ā`, an integer. -/
def norm (a : GI) : Int := a.re * a.re + a.im * a.im
/-- The cross term `Re(a·b̄)`. -/
def cross (a b : GI) : Int := (mul a (conj b)).re

def one : GI := ⟨1, 0⟩
def negOne : GI := ⟨-1, 0⟩
def I : GI := ⟨0, 1⟩

theorem polarization (a b : GI) : norm (add a b) = norm a + norm b + 2 * cross a b := by
  simp only [norm, add, cross, mul, conj, Int.add_mul, Int.mul_add, Int.mul_neg, Int.sub_neg,
    Int.mul_comm b.re a.re, Int.mul_comm b.im a.im]
  omega

end GI

open GI

/-- A preparation: amplitudes on the two sectors. -/
abbrev Prep := GI × GI

/-- The weight presentation: the two sector moduli. -/
def weights (p : Prep) : Int × Int := (norm p.1, norm p.2)

/-- The readout of the two-sector mixing context. -/
def mix (p : Prep) : Int := norm (add p.1 p.2)

theorem mix_eq (p : Prep) : mix p = norm p.1 + norm p.2 + 2 * cross p.1 p.2 :=
  polarization p.1 p.2

/-- With the weights fixed, the mixing context separates exactly by the
cross term. -/
theorem separates_iff_cross (p p' : Prep) (hw : weights p = weights p') :
    mix p ≠ mix p' ↔ cross p.1 p.2 ≠ cross p'.1 p'.2 := by
  have h1 : norm p.1 = norm p'.1 := congrArg Prod.fst hw
  have h2 : norm p.2 = norm p'.2 := congrArg Prod.snd hw
  constructor
  · intro hm hc
    exact hm (by rw [mix_eq, mix_eq, h1, h2, hc])
  · intro hc hm
    rw [mix_eq, mix_eq, h1, h2] at hm
    exact hc (by omega)

/-- NECESSITY: two preparations meeting the interference challenge are two
amplitude pairs on one fiber of the weight map. -/
theorem fiber_necessary {p p' : Prep} (hw : weights p = weights p') (hm : mix p ≠ mix p') :
    p ≠ p' ∧ weights p = weights p' :=
  ⟨fun h => hm (h ▸ rfl), hw⟩

/-- The sign group suffices for one pair. -/
theorem sign_pair :
    weights (one, one) = weights (one, negOne) ∧ mix (one, one) = 4 ∧ mix (one, negOne) = 0 := by
  decide

/-- Three preparations on one fiber with three readouts, using the four units
of `ℤ[i]`. -/
theorem mu4_triple :
    weights (one, one) = weights (one, I) ∧ weights (one, I) = weights (one, negOne) ∧
      mix (one, one) = 4 ∧ mix (one, I) = 2 ∧ mix (one, negOne) = 0 := by
  decide

/-- `i ^ j`, the units of `ℤ[i]` as the cyclic group of order four. -/
def ipow : Nat → GI
  | 0 => one
  | j + 1 => mul I (ipow j)

/-- The readout of the mixing context with relative phase `i ^ j`. -/
def mu4Readout (j : Nat) : Int := mix (one, ipow j)

/-- The readout depends on the phase only through its class under
conjugation `j ↦ 4 - j`. -/
theorem mu4_readout_invariant :
    ∀ j, j < 4 → mu4Readout ((4 - j) % 4) = mu4Readout j := by
  decide

theorem mu4_readout_values : (List.range 3).map mu4Readout = [4, 2, 0] := by
  decide

end Gauss
end ResearchQmBridge
