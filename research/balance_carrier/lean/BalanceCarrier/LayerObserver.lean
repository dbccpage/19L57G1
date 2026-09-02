import BalanceCarrier.Balance

/-!
# The layer observer: the part count of the fresh representation

Stage 1 of the balance_carrier run.  The observer reads, at every
element of the receiver, the part count of its fresh representation.  On
a raw pair `(n, k)` -- the `n`-th part of `k + 1` -- the value is
`(k + 1) / gcd(n, k + 1)`; the observer on the receiver is this raw
function lifted through the quotient.  The lift is licensed by
`layer_observer_wf`, which rests on the pinned `fresh_rep_unique`: every
raw pair equals an explicit fresh representative whose part count is the
raw value (`red_same`, `red_fresh`), and two fresh representatives of one
element share their part count.

Proved here, as pre-registered in `PREDICTIONS.md`:

* `layer_observer_wf` -- two raw pairs naming one receiver element have
  one raw value; the observer is well defined on the receiver.
* `layer_observer_constant` -- the value is `k + 1` at every fresh member
  of layer `k`.
* `layer_observer_separates` -- equal values at fresh members force equal
  part counts; `layer_observer_separates'` is the contrapositive form.
* `layer_observer_grades` -- along the divisor arrow from part count
  `k + 1` to its `(m + 1)`-fold multiple, a fresh part `c` is carried to
  the part `c * (m + 1)` of the larger layer, and the observer's value at
  that image is the source part count `k + 1`; `partCount_layer_image`
  restates this on the receiver through the pinned `layer_mul_compat`.
* `observer_value_divides` -- the value at any raw pair divides the part
  count of the layer it was read in: the observer's fibres over a layer
  lie on the divisors of its part count.

Nothing here is a statement about the running balance or its growth.
AuthorityEffect: None.
-/

namespace BalanceCarrier
namespace Observer

open Receiver Balance

/-- The raw observer: the part count of the reduced form of a raw pair. -/
def rawObs (a : Raw) : Nat := den a.2 / Nat.gcd a.1 (den a.2)

theorem gcd_den_pos (a : Raw) : 0 < Nat.gcd a.1 (den a.2) :=
  Nat.gcd_pos_of_pos_right _ (Nat.succ_pos _)

theorem rawObs_pos (a : Raw) : 0 < rawObs a := by
  unfold rawObs
  exact Nat.div_pos_iff.mpr
    ⟨gcd_den_pos a, Nat.le_of_dvd (Nat.succ_pos _) (Nat.gcd_dvd_right _ _)⟩

/-- The reduced part of a raw pair: the part over the common factor,
taken below the reduced part count. -/
def redPart (a : Raw) : Nat := (a.1 / Nat.gcd a.1 (den a.2)) % rawObs a

theorem redPart_lt (a : Raw) : redPart a < rawObs a := Nat.mod_lt _ (rawObs_pos a)

/-- The reduced part as a member of the reduced layer. -/
def redFin (a : Raw) : Fin (rawObs a - 1 + 1) :=
  ⟨redPart a, by have := redPart_lt a; have := rawObs_pos a; omega⟩

theorem den_rawObs (a : Raw) : den (rawObs a - 1) = rawObs a := by
  have := rawObs_pos a
  simp [den]
  omega

/-- The reduced representative is fresh at the reduced layer. -/
theorem red_fresh (a : Raw) : FreshAt (rawObs a - 1) (redFin a) := by
  show Nat.gcd (redPart a) (rawObs a - 1 + 1) = 1
  have hpos := rawObs_pos a
  have h1 : rawObs a - 1 + 1 = rawObs a := by omega
  rw [h1]
  unfold redPart
  rw [← Nat.gcd_rec, Nat.gcd_comm]
  unfold rawObs
  exact Nat.coprime_div_gcd_div_gcd (gcd_den_pos a)

/-- The raw identity behind `red_same`, stated over the naturals with the
observer and the reduced part folded so that the cast step is linear. -/
theorem red_same_nat (a : Raw) :
    a.1 * rawObs a
      = redPart a * den a.2
        + ((a.1 / Nat.gcd a.1 (den a.2)) / rawObs a) * (den a.2 * rawObs a) := by
  have hg1 : Nat.gcd a.1 (den a.2) * (a.1 / Nat.gcd a.1 (den a.2)) = a.1 :=
    Nat.mul_div_cancel' (Nat.gcd_dvd_left _ _)
  have hg2 : Nat.gcd a.1 (den a.2) * rawObs a = den a.2 :=
    Nat.mul_div_cancel' (Nat.gcd_dvd_right _ _)
  have hmd : redPart a + rawObs a * ((a.1 / Nat.gcd a.1 (den a.2)) / rawObs a)
      = a.1 / Nat.gcd a.1 (den a.2) :=
    Nat.mod_add_div _ _
  calc a.1 * rawObs a
      = (Nat.gcd a.1 (den a.2) * (a.1 / Nat.gcd a.1 (den a.2))) * rawObs a := by
          rw [hg1]
    _ = (Nat.gcd a.1 (den a.2) * rawObs a) * (a.1 / Nat.gcd a.1 (den a.2)) := by
          ac_rfl
    _ = den a.2 * (a.1 / Nat.gcd a.1 (den a.2)) := by rw [hg2]
    _ = den a.2 * (redPart a + rawObs a * ((a.1 / Nat.gcd a.1 (den a.2)) / rawObs a)) := by
          rw [hmd]
    _ = redPart a * den a.2
        + ((a.1 / Nat.gcd a.1 (den a.2)) / rawObs a) * (den a.2 * rawObs a) := by
          rw [Nat.mul_add]
          congr 1
          · exact Nat.mul_comm _ _
          · ac_rfl

/-- The reduced representative names the same receiver element: the
cross difference is the explicit multiple `(n / g) / (D / g)` of the
product of the part counts. -/
theorem red_same (a : Raw) : mk a = layer (rawObs a - 1) (redFin a) := by
  apply Quotient.sound
  refine ⟨(((a.1 / Nat.gcd a.1 (den a.2)) / rawObs a : Nat) : Int), ?_⟩
  show (a.1 : Int) * den (rawObs a - 1) - (redPart a : Int) * den a.2
      = (((a.1 / Nat.gcd a.1 (den a.2)) / rawObs a : Nat) : Int)
          * ((den a.2 : Int) * den (rawObs a - 1))
  rw [den_rawObs]
  have hInt : ((a.1 * rawObs a : Nat) : Int)
      = ((redPart a * den a.2
        + ((a.1 / Nat.gcd a.1 (den a.2)) / rawObs a) * (den a.2 * rawObs a) : Nat) : Int) := by
    rw [red_same_nat]
  simp only [Int.natCast_add, Int.natCast_mul] at hInt
  omega

/-- Stage 1 target: the observer is well defined on the receiver -- two
raw pairs naming one element have one raw value, because both equal a
fresh representative whose part count is that value, and the pinned
uniqueness identifies the two part counts. -/
theorem layer_observer_wf (a b : Raw) (h : R a b) : rawObs a = rawObs b := by
  have hab : mk a = mk b := Quotient.sound h
  have heq : layer (rawObs a - 1) (redFin a) = layer (rawObs b - 1) (redFin b) := by
    rw [← red_same, ← red_same, hab]
  have hk := (fresh_rep_unique (red_fresh a) (red_fresh b) heq).1
  have := rawObs_pos a
  have := rawObs_pos b
  omega

/-- The observer on the receiver: the raw observer through the quotient. -/
def partCount (x : QOne) : Nat :=
  Quotient.lift rawObs (fun a b h => layer_observer_wf a b h) x

/-- Stage 1 target: the value is constant across a layer's fresh
members, and equals the part count. -/
theorem layer_observer_constant {k : Nat} {c : Fin (k + 1)} (hf : FreshAt k c) :
    partCount (layer k c) = k + 1 := by
  show den k / Nat.gcd c.val (den k) = k + 1
  have hone : Nat.gcd c.val (den k) = 1 := hf
  rw [hone, Nat.div_one]
  rfl

/-- Stage 1 target: distinct part counts give distinct values -- equal
values at fresh members force equal part counts. -/
theorem layer_observer_separates {k k' : Nat} {c : Fin (k + 1)} {c' : Fin (k' + 1)}
    (hf : FreshAt k c) (hf' : FreshAt k' c')
    (h : partCount (layer k c) = partCount (layer k' c')) : k = k' := by
  rw [layer_observer_constant hf, layer_observer_constant hf'] at h
  omega

/-- The contrapositive form of `layer_observer_separates`. -/
theorem layer_observer_separates' {k k' : Nat} {c : Fin (k + 1)} {c' : Fin (k' + 1)}
    (hf : FreshAt k c) (hf' : FreshAt k' c') (hne : k ≠ k') :
    partCount (layer k c) ≠ partCount (layer k' c') :=
  fun h => hne (layer_observer_separates hf hf' h)

/-- Stage 1 optional target, in the declared form: along the divisor
arrow from part count `k + 1` to its `(m + 1)`-fold multiple, a fresh
part `c` is carried to the part `c * (m + 1)` of the larger layer, and
the observer's raw value at that image is the source part count. -/
theorem layer_observer_grades {k : Nat} {c : Fin (k + 1)} (hf : FreshAt k c) (m : Nat) :
    rawObs (c.val * (m + 1), k * m + k + m) = k + 1 := by
  unfold rawObs
  have hden : den (k * m + k + m) = (k + 1) * (m + 1) := by
    simp [den, Nat.mul_add, Nat.add_mul]
    omega
  show den (k * m + k + m) / Nat.gcd (c.val * (m + 1)) (den (k * m + k + m)) = k + 1
  rw [hden, Nat.gcd_mul_right]
  have hone : Nat.gcd c.val (k + 1) = 1 := hf
  rw [hone, Nat.one_mul]
  exact Nat.mul_div_cancel _ (Nat.succ_pos m)

/-- The grading restated on the receiver: the image pair names the same
element (pinned `layer_mul_compat`), so the observer's value there is the
value at the fresh source. -/
theorem partCount_layer_image (k : Nat) (c : Fin (k + 1)) (m : Nat) :
    partCount (mk (c.val * (m + 1), k * m + k + m)) = partCount (layer k c) := by
  rw [← layer_mul_compat]

/-- The observer's value at any raw pair divides the part count of the
layer it was read in. -/
theorem observer_value_divides (a : Raw) : rawObs a ∣ den a.2 := by
  unfold rawObs
  exact Nat.div_dvd_of_dvd (Nat.gcd_dvd_right _ _)

end Observer
end BalanceCarrier
