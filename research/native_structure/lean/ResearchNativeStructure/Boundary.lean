import ResearchNativeStructure.Cells

/-!
# Boundaries on native transitions, and path cost

AuthorityEffect: None.  Chains here are native states (0-chains), native
edges `(s, e)` (1-chains), and two-step squares from a state `u` through
`e₁ e₂` and `e₂ e₁` (2-chains).  They are paired with integer-valued
cochains, so no formal sum is stored: a boundary is read through its
pairing.

Proved here:

* `boundary_boundary`: pairing the boundary of a square's boundary with a
  0-cochain `φ` gives the difference of `φ` at the square's two corners.
* `boundary_zero_iff_commutes`: it vanishes for every `φ` exactly when the
  square commutes.  Boundary cancellation on a square is verified
  commutation, not an extra premise.
* `terminal_square_boundary`: the sealed non-commuting pair (terminal
  then license write) has a nonzero boundary.
* `pathCost_append`, `exact_pathCost`, `exact_closed`, `closed_cell_cost`,
  `not_exact_of_cycle`: path cost is additive; an exact cost telescopes to
  a potential difference and is closed on commuting squares; a closed cost
  is invariant under cells; a cycle with nonzero cost excludes a
  potential.
* `budgetDelta_exact`, `writes_not_exact`: the budget change is exact,
  with the budget as its potential.  The count of state-changing steps has
  a cycle of cost two, so it has no potential.
-/

namespace ResearchNativeStructure

open PrimitivePassage TraceAlgebra TransitionAlphabet

/-- The boundary of the edge `(s, e)`, paired with a 0-cochain. -/
def dEdge (φ : PState → Int) (s : PState) (e : PEvent) : Int :=
  φ (step s e) - φ s

/-- The boundary of the square at `u` through `e₁ e₂` and `e₂ e₁`, paired
with a 1-cochain. -/
def dSquare (ψ : PState → PEvent → Int) (u : PState) (e₁ e₂ : PEvent) : Int :=
  ψ u e₁ + ψ (step u e₁) e₂ - ψ u e₂ - ψ (step u e₂) e₁

theorem boundary_boundary (φ : PState → Int) (u : PState) (e₁ e₂ : PEvent) :
    dSquare (dEdge φ) u e₁ e₂ = φ (step (step u e₁) e₂) - φ (step (step u e₂) e₁) := by
  simp only [dSquare, dEdge]
  omega

/-- The indicator of one state. -/
def indicator (w : PState) (x : PState) : Int := if x = w then 1 else 0

theorem boundary_zero_iff_commutes (u : PState) (e₁ e₂ : PEvent) :
    (∀ φ : PState → Int, dSquare (dEdge φ) u e₁ e₂ = 0) ↔
      step (step u e₁) e₂ = step (step u e₂) e₁ := by
  constructor
  · intro h
    have h1 := h (indicator (step (step u e₁) e₂))
    rw [boundary_boundary] at h1
    simp only [indicator, if_pos rfl] at h1
    by_cases hw : step (step u e₂) e₁ = step (step u e₁) e₂
    · exact hw.symm
    · rw [if_neg hw] at h1; exact absurd h1 (by decide)
  · intro hc φ
    rw [boundary_boundary, hc]
    omega

theorem terminal_square_boundary :
    dSquare (dEdge (indicator (step (step genesisP .halt) (.setLicense false))))
      genesisP .halt (.setLicense false) ≠ 0 := by
  rw [boundary_boundary]
  decide

/-! ## Path cost -/

/-- The cost of an event list from `s`, summed along the actual steps. -/
def pathCost (c : PState → PEvent → Int) : PState → List PEvent → Int
  | _, [] => 0
  | s, e :: l => c s e + pathCost c (step s e) l

theorem pathCost_append (c : PState → PEvent → Int) (s : PState) (l₁ l₂ : List PEvent) :
    pathCost c s (l₁ ++ l₂) = pathCost c s l₁ + pathCost c (replayP l₁ s) l₂ := by
  induction l₁ generalizing s with
  | nil => simp [pathCost, replayP]
  | cons e rest ih =>
      show c s e + pathCost c (step s e) (rest ++ l₂) =
        (c s e + pathCost c (step s e) rest) + pathCost c (replayP rest (step s e)) l₂
      rw [ih]; omega

/-- A cost is exact when it is the boundary of a potential. -/
def Exact (c : PState → PEvent → Int) : Prop := ∃ φ : PState → Int, ∀ s e, c s e = dEdge φ s e

/-- A cost is closed when every commuting square has zero boundary. -/
def Closed (c : PState → PEvent → Int) : Prop :=
  ∀ u e₁ e₂, step (step u e₁) e₂ = step (step u e₂) e₁ → dSquare c u e₁ e₂ = 0

theorem exact_pathCost (φ : PState → Int) (s : PState) (l : List PEvent) :
    pathCost (dEdge φ) s l = φ (replayP l s) - φ s := by
  induction l generalizing s with
  | nil => simp [pathCost, replayP]
  | cons e rest ih =>
      show dEdge φ s e + pathCost (dEdge φ) (step s e) rest = φ (replayP rest (step s e)) - φ s
      rw [ih]; simp only [dEdge]; omega

theorem pathCost_congr {c c' : PState → PEvent → Int} (h : ∀ s e, c s e = c' s e)
    (s : PState) (l : List PEvent) : pathCost c s l = pathCost c' s l := by
  induction l generalizing s with
  | nil => rfl
  | cons e rest ih => simp only [pathCost, h, ih]

theorem exact_closed {c : PState → PEvent → Int} (h : Exact c) : Closed c := by
  obtain ⟨φ, hφ⟩ := h
  intro u e₁ e₂ hc
  have hd : dSquare c u e₁ e₂ = dSquare (dEdge φ) u e₁ e₂ := by simp only [dSquare, hφ]
  rw [hd, boundary_boundary, hc]
  omega

theorem closed_swap_cost {c : PState → PEvent → Int} (hc : Closed c) {s : PState}
    {l l' : List PEvent} (h : Swap s l l') : pathCost c s l = pathCost c s l' := by
  cases h with
  | mk a b e₁ e₂ hcomm =>
      rw [pathCost_append, pathCost_append]
      congr 1
      have hsq := hc (replayP a s) e₁ e₂ hcomm
      simp only [dSquare] at hsq
      show c (replayP a s) e₁ + (c (step (replayP a s) e₁) e₂ +
          pathCost c (step (step (replayP a s) e₁) e₂) b) =
        c (replayP a s) e₂ + (c (step (replayP a s) e₂) e₁ +
          pathCost c (step (step (replayP a s) e₂) e₁) b)
      rw [hcomm]
      omega

/-- **Cost transport along cells**, under the closedness premise. -/
theorem closed_cell_cost {c : PState → PEvent → Int} (hc : Closed c) {s : PState}
    {l l' : List PEvent} (h : Cell s l l') : pathCost c s l = pathCost c s l' := by
  induction h with
  | refl _ => rfl
  | swap h => exact closed_swap_cost hc h
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂

theorem not_exact_of_cycle {c : PState → PEvent → Int} {s : PState} {l : List PEvent}
    (hcyc : replayP l s = s) (hcost : pathCost c s l ≠ 0) : ¬ Exact c := by
  intro ⟨φ, hφ⟩
  apply hcost
  rw [pathCost_congr hφ, exact_pathCost, hcyc]
  omega

/-! ## Native instances -/

/-- The change of the budget field along a step. -/
def budgetDelta (s : PState) (e : PEvent) : Int := ((step s e).budget : Int) - (s.budget : Int)

theorem budgetDelta_exact : Exact budgetDelta :=
  ⟨fun s => (s.budget : Int), fun _ _ => rfl⟩

/-- One for a state-changing step, zero for an inert one. -/
def writes (s : PState) (e : PEvent) : Int := if step s e = s then 0 else 1

theorem writes_not_exact : ¬ Exact writes :=
  not_exact_of_cycle (s := genesisP) (l := [.setBudget 1, .setBudget 0]) rfl (by decide)

end ResearchNativeStructure
