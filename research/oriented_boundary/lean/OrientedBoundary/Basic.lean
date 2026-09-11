/-
The (B)-is-empty lemma: the load-bearing result that discharges SF-OPEN-A.

Open, analytic result. Touches nothing under the seal. Analytic, not blind
(../CLOSURE.md). Axioms are within {propext, Quot.sound}; no
sorry/admit/axiom/mathlib.

A judgment is read by its action on the tested ordered pair (x, y): the pair
(d x y, d y x). The swap σ = (x y) preserves it iff it is symmetric on the pair;
it "distinguishes" the pair (a mechanism-(A) witness) iff it is asymmetric.
-/
namespace OrientedBoundary

/-- A judgment, read on the tested pair as `(d x y, d y x)`. -/
abbrev Judgment := Bool × Bool

/-- `d` distinguishes the pair — a mechanism-(A) witness — iff it is asymmetric. -/
def distinguishes (d : Judgment) : Bool := d.1 != d.2

/-- The swap preserves `d` iff `d` is symmetric on the pair. -/
def swapPreserves (d : Judgment) : Bool := d.1 == d.2

/-- σ ∈ Aut(M) iff it preserves every admitted judgment. -/
def swapInAut (js : List Judgment) : Bool := js.all swapPreserves

/-- Preserving and distinguishing are exact opposites on a judgment. -/
theorem swap_iff (d : Judgment) : swapPreserves d = true ↔ distinguishes d = false := by
  rcases d with ⟨a, b⟩; cases a <;> cases b <;> decide

/-- **(B) is empty.** σ ∈ Aut iff no admitted judgment distinguishes the pair.
There is no witnessless route to σ ∉ Aut. -/
theorem b_is_empty (js : List Judgment) :
    swapInAut js = true ↔ ∀ d ∈ js, distinguishes d = false := by
  rw [swapInAut, List.all_eq_true]
  constructor
  · intro h d hd; exact (swap_iff d).1 (h d hd)
  · intro h d hd; exact (swap_iff d).2 (h d hd)

/-- The discharge, stated directly: σ ∉ Aut forces an admitted distinguishing
witness (mechanism A). "Withdraw σ with no witness" — route (B) — cannot occur.
Proved by structural induction (core only; no `Classical`, no mathlib). -/
theorem not_in_aut_needs_witness :
    ∀ (js : List Judgment), swapInAut js = false → ∃ d ∈ js, distinguishes d = true
  | [], h => by simp [swapInAut] at h
  | d :: ds, h => by
      have hcons : swapInAut (d :: ds) = (swapPreserves d && swapInAut ds) := rfl
      rw [hcons] at h
      cases hd : swapPreserves d with
      | false =>
          have hdist : distinguishes d = true := by
            rcases d with ⟨a, b⟩; cases a <;> cases b <;> simp_all [swapPreserves, distinguishes]
          exact ⟨d, by simp, hdist⟩
      | true =>
          rw [hd, Bool.true_and] at h
          obtain ⟨d', hmem, hdist⟩ := not_in_aut_needs_witness ds h
          exact ⟨d', by simp [hmem], hdist⟩

/-- Unoriented reading (AP1): with only a symmetric judgment, the swap is an
automorphism — it separates nothing the bare boundary did not. -/
theorem s2u_swap_is_automorphism : swapInAut [(false, false)] = true := by decide

/-- Oriented reading (AP2): one asymmetric admitted witness breaks it — orientation
costs exactly one capability. -/
theorem s2o_swap_is_not_automorphism : swapInAut [(false, false), (true, false)] = false := by
  decide

/-- One asymmetric witness is enough, and (by `b_is_empty`) necessary. -/
theorem s2o_breaks_at_one_witness :
    (([(false, false), (true, false)] : List Judgment).filter distinguishes).length = 1 := by
  decide

end OrientedBoundary
