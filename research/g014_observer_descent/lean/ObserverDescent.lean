/-
Target G014: Multi-Observer Descent & Natural Transport.

Constructive formalization of:
1. Sheaf-like descent over finite observer coverages.
2. Compatible local observer records glue to a unique global carrier state.
3. Explicit failed-gluing obstruction witnesses.
4. Natural transport commutation along frame automorphisms.
5. Symmetric duplicate observer agreement.

AuthorityEffect: None.
Constructive: 100% core Lean 4, zero Classical.choice, zero mathlib.
Axioms: strictly within {propext, Quot.sound}.
-/

namespace G014ObserverDescent

/-- Discrete finite loci in a minimal tripartite carrier universe. -/
inductive Locus
  | L1
  | L2
  | L3
  deriving DecidableEq, Repr

/-- Global carrier state assigning discrete values to each locus. -/
structure CarrierState where
  v1 : Nat
  v2 : Nat
  v3 : Nat
  deriving DecidableEq, Repr

/-- Valuation at a specific locus. -/
def CarrierState.get (s : CarrierState) : Locus → Nat
  | Locus.L1 => s.v1
  | Locus.L2 => s.v2
  | Locus.L3 => s.v3

@[ext]
theorem CarrierState.ext' (s1 s2 : CarrierState) (h1 : s1.v1 = s2.v1) (h2 : s1.v2 = s2.v2) (h3 : s1.v3 = s2.v3) :
    s1 = s2 := by
  cases s1; cases s2; congr

/-- Observer 12 observes loci L1 and L2. -/
structure Record12 where
  v1 : Nat
  v2 : Nat
  deriving DecidableEq, Repr

/-- Observer 23 observes loci L2 and L3. -/
structure Record23 where
  v2 : Nat
  v3 : Nat
  deriving DecidableEq, Repr

/-- Projection of global state onto Observer 12. -/
def pi12 (s : CarrierState) : Record12 :=
  ⟨s.v1, s.v2⟩

/-- Projection of global state onto Observer 23. -/
def pi23 (s : CarrierState) : Record23 :=
  ⟨s.v2, s.v3⟩

/-- Overlap compatibility condition on shared locus L2. -/
def Compatible (r12 : Record12) (r23 : Record23) : Prop :=
  r12.v2 = r23.v2

instance (r12 : Record12) (r23 : Record23) : Decidable (Compatible r12 r23) :=
  inferInstanceAs (Decidable (r12.v2 = r23.v2))

/-- Sheaf-like gluing operation: stitches compatible records into a global state. -/
def glue (r12 : Record12) (r23 : Record23) : CarrierState :=
  ⟨r12.v1, r12.v2, r23.v3⟩

/-- Theorem 1 (Gluing Existence & Preservation): Gluing compatible records preserves both observations. -/
theorem gluing_preserves_observations (r12 : Record12) (r23 : Record23) (h : Compatible r12 r23) :
    pi12 (glue r12 r23) = r12 ∧ pi23 (glue r12 r23) = r23 := by
  dsimp [glue, pi12, pi23, Compatible] at *
  constructor
  · rfl
  · cases r23
    dsimp
    congr

/-- Theorem 2 (Gluing Uniqueness): If a global state projects to compatible records, it equals their glue. -/
theorem gluing_unique (s : CarrierState) (r12 : Record12) (r23 : Record23)
    (h1 : pi12 s = r12) (h2 : pi23 s = r23) :
    s = glue r12 r23 := by
  cases s
  dsimp [pi12, pi23, glue] at *
  cases h1; cases h2
  rfl

/-- Theorem 3 (Failed-Gluing Obstruction Witness): If records disagree on the overlap locus,
    no global carrier state can simultaneously project to both. -/
theorem failed_gluing_obstruction (r12 : Record12) (r23 : Record23)
    (h_obs : r12.v2 ≠ r23.v2) :
    ¬ ∃ (s : CarrierState), pi12 s = r12 ∧ pi23 s = r23 := by
  intro ⟨s, h1, h2⟩
  have eq1 : s.v2 = r12.v2 := by
    have := congrArg Record12.v2 h1
    exact this
  have eq2 : s.v2 = r23.v2 := by
    have := congrArg Record23.v2 h2
    exact this
  have h_contra : r12.v2 = r23.v2 := by rw [← eq1, eq2]
  exact h_obs h_contra

/-- Frame automorphism: permutation swapping L1 and L3 (reflection around L2). -/
def swap13 (s : CarrierState) : CarrierState :=
  ⟨s.v3, s.v2, s.v1⟩

theorem swap13_involutive (s : CarrierState) : swap13 (swap13 s) = s := by
  cases s; rfl

/-- Transported record under swap13. -/
def transport_record (r : Record12) : Record23 :=
  ⟨r.v2, r.v1⟩

/-- Theorem 4 (Natural Transport Commutation): Observation in transported frame
    equals transported observation. -/
theorem natural_transport_commutation (s : CarrierState) :
    pi23 (swap13 s) = transport_record (pi12 s) := by
  dsimp [swap13, pi23, transport_record, pi12]

/-- Symmetric duplicate observers: two observers measuring symmetric loci L1 and L3. -/
def readout1 (s : CarrierState) : Nat := s.v1
def readout3 (s : CarrierState) : Nat := s.v3

/-- Theorem 5 (Symmetric Duplicate Agreement): If a state is symmetric under frame swap,
    duplicate observers yield identical readouts. -/
theorem symmetric_duplicate_agreement (s : CarrierState) (h_symm : swap13 s = s) :
    readout1 s = readout3 s := by
  have h : (swap13 s).v1 = s.v1 := by rw [h_symm]
  dsimp [swap13] at h
  exact h.symm

/-- Theorem 6 (Unrepresented Asymmetry Obstruction): If duplicate observers disagree,
    the carrier state cannot be symmetric. -/
theorem duplicate_disagreement_witnesses_asymmetry (s : CarrierState) (h_neq : readout1 s ≠ readout3 s) :
    swap13 s ≠ s := by
  intro h_symm
  have h_agree := symmetric_duplicate_agreement s h_symm
  exact h_neq h_agree

end G014ObserverDescent
