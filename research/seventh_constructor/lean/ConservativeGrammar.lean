/-!
# Conservative Event Grammar: The 7th Constructor (e_swap)

Formalization of Requirement R1:
- Syntax, operational preconditions, and transition semantics for the 7th constructor (e_swap)
- Cardinal potential preservation: N(step(r, e_swap)) = N(r)
- Admitting regime conditions: applicability without external supply (nData ≥ 2)
- Involutive semantics: e_swap(e_swap(r)) = r

Axioms: strictly within {propext, Quot.sound}, zero mathlib, zero custom axioms, zero unproven escapes.
AuthorityEffect: None.
-/

namespace SeventhConstructor

/-! ## 1. Cardinal Profile and Event Constructors -/

/-- Component counts of an admitted regime. -/
structure CardinalProfile where
  dCount : Nat  -- |D|: data tokens
  fCount : Nat  -- |F|: forms
  iCount : Nat  -- |I|: judgment instances
  rCount : Nat  -- |R|: rules
  qCount : Nat  -- |Q|: separation requirements
  deriving DecidableEq, Repr

/-- Cardinal profile potential N(r) in Nat. -/
def potential (p : CardinalProfile) : Nat :=
  p.dCount + p.fCount + p.iCount + p.rCount + p.qCount

/-- Extended event grammar containing native constructors plus the 7th constructor (swap). -/
inductive ExtendedEvent : Type where
  | supply : ExtendedEvent
  | addData : ExtendedEvent
  | addForm : ExtendedEvent
  | addInstance : ExtendedEvent
  | addRule : ExtendedEvent
  | addSeparation : ExtendedEvent
  | swap : ExtendedEvent
  deriving DecidableEq, Repr

/-- Effect of extended event constructors on cardinal profile. -/
def stepProfile (p : CardinalProfile) : ExtendedEvent → CardinalProfile
  | ExtendedEvent.supply => p
  | ExtendedEvent.addData => { p with dCount := p.dCount + 1 }
  | ExtendedEvent.addForm => { p with fCount := p.fCount + 1 }
  | ExtendedEvent.addInstance => { p with iCount := p.iCount + 1 }
  | ExtendedEvent.addRule => { p with rCount := p.rCount + 1 }
  | ExtendedEvent.addSeparation => { p with qCount := p.qCount + 1 }
  | ExtendedEvent.swap => p

/-! ## 2. Cardinality Preservation Theorems -/

/-- Theorem 1.1 (Swap Cardinality Preservation):
The 7th constructor preserves cardinal potential exactly: N(step(p, swap)) = N(p). -/
theorem swap_preserves_cardinal_potential (p : CardinalProfile) :
    potential (stepProfile p ExtendedEvent.swap) = potential p := by
  dsimp [stepProfile, potential]

/-- Theorem 1.2 (Native Constructor Strict Monotonicity):
All native non-supply event constructors strictly increase cardinal potential. -/
theorem native_non_supply_increases_potential (p : CardinalProfile) (e : ExtendedEvent)
    (h_not_supply : e ≠ ExtendedEvent.supply)
    (h_not_swap : e ≠ ExtendedEvent.swap) :
    potential (stepProfile p e) > potential p := by
  cases e with
  | supply => contradiction
  | addData =>
      dsimp [potential, stepProfile]
      omega
  | addForm =>
      dsimp [potential, stepProfile]
      omega
  | addInstance =>
      dsimp [potential, stepProfile]
      omega
  | addRule =>
      dsimp [potential, stepProfile]
      omega
  | addSeparation =>
      dsimp [potential, stepProfile]
      omega
  | swap => contradiction

/-- Supply is the identity on cardinal profiles. -/
theorem supply_is_identity (p : CardinalProfile) :
    stepProfile p ExtendedEvent.supply = p := rfl

/-! ## 3. Operational MiniRegime and In-Place Witness Exchange -/

/-- An admitted regime model carrying data tokens and relational instances. -/
structure MiniRegime where
  nData : Nat
  instances : List (Nat × Nat)
  deriving DecidableEq, Repr

/-- Operational preconditions for exchanging two retained witness indices. -/
def swap_precondition (r : MiniRegime) (i j : Nat) : Prop :=
  i < r.nData ∧ j < r.nData ∧ i ≠ j

/-- Admitting regime condition: at least 2 distinct witnesses must be retained. -/
def admitting_regime (r : MiniRegime) : Prop :=
  r.nData ≥ 2

/-- Theorem 1.3 (Admitting Regime Solvability):
Any regime satisfying the admitting condition admits at least one valid in-place swap. -/
theorem admitting_regime_has_swap (r : MiniRegime) (h : admitting_regime r) :
    ∃ i j, swap_precondition r i j := by
  dsimp [admitting_regime] at h
  have h0 : 0 < r.nData := by omega
  have h1 : 1 < r.nData := by omega
  have h_ne : 0 ≠ 1 := by decide
  exact ⟨0, 1, h0, h1, h_ne⟩

/-- Transposition permutation on witness indices: tau_(i, j)(x). -/
def transposition (i j x : Nat) : Nat :=
  if x = i then j else if x = j then i else x

@[simp] theorem transposition_apply_i (i j : Nat) :
    transposition i j i = j := by
  dsimp [transposition]
  rw [if_pos rfl]

@[simp] theorem transposition_apply_j (i j : Nat) (h_ne : i ≠ j) :
    transposition i j j = i := by
  dsimp [transposition]
  rw [if_neg (Ne.symm h_ne)]
  rw [if_pos rfl]

theorem transposition_apply_other (i j x : Nat) (hi : x ≠ i) (hj : x ≠ j) :
    transposition i j x = x := by
  dsimp [transposition]
  rw [if_neg hi, if_neg hj]

/-- Theorem 1.4 (Transposition Involutive Property):
Applying the transposition twice returns the original index. -/
theorem transposition_involutive (i j x : Nat) :
    transposition i j (transposition i j x) = x := by
  dsimp [transposition]
  split <;> rename_i h1
  · split <;> rename_i h2
    · subst_vars; rfl
    · split <;> rename_i h3
      · subst_vars; rfl
      · contradiction
  · split <;> rename_i h2
    · split <;> rename_i h3
      · subst_vars; rfl
      · contradiction
    · rfl

/-- Transposition preserves the bound on data indices. -/
theorem transposition_lt (i j x n : Nat) (hi : i < n) (hj : j < n) (hx : x < n) :
    transposition i j x < n := by
  dsimp [transposition]
  split
  · exact hj
  · split
    · exact hi
    · exact hx

/-- Transition semantics of the 7th constructor on a MiniRegime. -/
def swapStep (r : MiniRegime) (i j : Nat) : MiniRegime :=
  { nData := r.nData,
    instances := r.instances.map (fun p => (transposition i j p.1, transposition i j p.2)) }

/-- Theorem 1.5 (MiniRegime Data Cardinality Preservation):
The swap step leaves the number of admitted data tokens invariant. -/
theorem swap_data_cardinality (r : MiniRegime) (i j : Nat) :
    (swapStep r i j).nData = r.nData := rfl

/-- Theorem 1.6 (MiniRegime Instance Cardinality Preservation):
The swap step leaves the number of relational instances invariant. -/
theorem swap_instances_cardinality (r : MiniRegime) (i j : Nat) :
    (swapStep r i j).instances.length = r.instances.length := by
  dsimp [swapStep]
  exact List.length_map _

/-- Theorem 1.7 (MiniRegime Swap Involutive Property):
Applying the in-place swap constructor twice yields the exact original regime. -/
theorem swap_regime_involutive (r : MiniRegime) (i j : Nat) :
    swapStep (swapStep r i j) i j = r := by
  cases r with | mk nData insts =>
  dsimp [swapStep]
  congr 1
  induction insts with
  | nil => rfl
  | cons head tail ih =>
      dsimp [List.map]
      rw [transposition_involutive i j head.1, transposition_involutive i j head.2]
      rw [ih]

/-- Theorem 1.8 (No External Tokens Introduced):
If all instances in r reference admitted tokens, all instances in swapStep(r) reference admitted tokens. -/
theorem swap_preserves_internal_scope (r : MiniRegime) (i j : Nat)
    (hi : i < r.nData) (hj : j < r.nData)
    (h_wf : ∀ p ∈ r.instances, p.1 < r.nData ∧ p.2 < r.nData) :
    ∀ p ∈ (swapStep r i j).instances, p.1 < (swapStep r i j).nData ∧ p.2 < (swapStep r i j).nData := by
  intro p hp
  dsimp [swapStep] at hp
  rw [List.mem_map] at hp
  rcases hp with ⟨orig, h_orig_mem, h_orig_eq⟩
  subst h_orig_eq
  have h_bounds := h_wf orig h_orig_mem
  dsimp [swapStep]
  exact ⟨transposition_lt i j orig.1 r.nData hi hj h_bounds.1,
         transposition_lt i j orig.2 r.nData hi hj h_bounds.2⟩

end SeventhConstructor
