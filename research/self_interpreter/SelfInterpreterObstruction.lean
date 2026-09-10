/-!
# Absolute Self-Interpreter Obstruction in Lean 4

Target 9 formalization: Diagonal state-capacity obstruction theorem establishing
the irreducibility of the stratification boundary.

Mathematical Content:
1. Represented Transition Machines:
   - A host machine with vertex capacity $k$ has state space bounded by $k$ (`Fin k`),
     a deterministic transition map `step : Fin k → Fin k`, an initial state `init`,
     and an emission/observation map `emit : Fin k → Nat`.
2. Constructive Pigeonhole Principle for Traces:
   - In any execution trace of length $k + 1$ in state capacity $k$, there exist two
     distinct time steps $i < j ≤ k$ with identical internal states: `run H i = run H j`.
   - Consequently, the host observation repeats: `obs H i = obs H j`.
3. Diagonal Counter-Guest:
   - For any $m > k$, the cyclic guest machine $C_m$ has state space `Fin m`,
     step `v ↦ (v + 1) % m`, and emission `emit(v) = v.val`.
   - On the prefix $0, 1, \dots, k$, all observations of $C_m$ are strictly distinct:
     `∀ i < j ≤ k, obs C_m i ≠ obs C_m j`.
4. State-Capacity Obstruction Theorem:
   - No host machine with vertex capacity $k$ can faithfully simulate the transition
     behavior of the guest machine $C_{k+1}$ (or any $C_m$ with $m > k$).
   - The stratification boundary between represented evaluator and guest programs
     is mathematically irreducible for static graph representations.

Axioms used: strictly contained in `{propext, Quot.sound}`.
-/

namespace SelfInterpreterObstruction

/-! ## 1. Capacity Machines, Traces, and Observations -/

/-- A deterministic transition machine with vertex capacity `k`. -/
structure CapacityMachine (k : Nat) where
  init : Fin k
  step : Fin k → Fin k
  emit : Fin k → Nat

/-- State at time `t`. -/
def run {k : Nat} (M : CapacityMachine k) : Nat → Fin k
  | 0 => M.init
  | t + 1 => M.step (run M t)

/-- Observable readout at time `t`. -/
def obs {k : Nat} (M : CapacityMachine k) (t : Nat) : Nat :=
  M.emit (run M t)

/-! ## 2. Constructive State Compression and Pigeonhole Principle -/

/-- Project `Fin (k + 1)` to `Fin k` by removing a specified point `x`. -/
def dropElem {k : Nat} (x y : Fin (k + 1)) (h : y ≠ x) : Fin k :=
  if hlt : y.val < x.val then
    ⟨y.val, by
      have : x.val ≤ k := Nat.le_of_lt_succ x.isLt
      omega⟩
  else
    ⟨y.val - 1, by
      have hne : y.val ≠ x.val := fun heq => h (Fin.ext heq)
      have : y.val > x.val := by omega
      have hy : y.val ≤ k := Nat.le_of_lt_succ y.isLt
      omega⟩

theorem dropElem_injective {k : Nat} (x : Fin (k + 1)) (y1 y2 : Fin (k + 1))
    (h1 : y1 ≠ x) (h2 : y2 ≠ x) (heq : dropElem x y1 h1 = dropElem x y2 h2) :
    y1 = y2 := by
  dsimp [dropElem] at heq
  split at heq
  · split at heq
    · injection heq with heq'
      exact Fin.ext heq'
    · injection heq with heq'
      have hne2 : y2.val ≠ x.val := fun h => h2 (Fin.ext h)
      omega
  · split at heq
    · injection heq with heq'
      have hne1 : y1.val ≠ x.val := fun h => h1 (Fin.ext h)
      omega
    · injection heq with heq'
      have hne1 : y1.val ≠ x.val := fun h => h1 (Fin.ext h)
      have hne2 : y2.val ≠ x.val := fun h => h2 (Fin.ext h)
      have : y1.val = y2.val := by omega
      exact Fin.ext this

/-- Decidable linear search for a matching value in `1..bound`. -/
def hasMatch {n : Nat} (x : Fin n) (f : Nat → Fin n) : Nat → Bool
  | 0 => false
  | b + 1 => (f (b + 1) == x) || hasMatch x f b

theorem hasMatch_true {n : Nat} (x : Fin n) (f : Nat → Fin n) (b : Nat)
    (h : hasMatch x f b = true) :
    ∃ j, 1 ≤ j ∧ j ≤ b ∧ f j = x := by
  induction b with
  | zero =>
    simp [hasMatch] at h
  | succ b ih =>
    simp only [hasMatch, Bool.or_eq_true] at h
    cases h with
    | inl h1 =>
      rw [beq_iff_eq] at h1
      exact ⟨b + 1, by omega, by omega, h1⟩
    | inr h2 =>
      obtain ⟨j, hj1, hj2, heq⟩ := ih h2
      exact ⟨j, hj1, by omega, heq⟩

theorem hasMatch_false {n : Nat} (x : Fin n) (f : Nat → Fin n) (b : Nat)
    (h : hasMatch x f b = false) :
    ∀ j, 1 ≤ j → j ≤ b → f j ≠ x := by
  induction b with
  | zero =>
    intro j hj1 hj2
    omega
  | succ b ih =>
    intro j hj1 hj2
    simp only [hasMatch, Bool.or_eq_false_iff] at h
    have h_not : (f (b + 1) == x) = false := h.1
    have h_rec : hasMatch x f b = false := h.2
    rw [beq_eq_false_iff_ne] at h_not
    by_cases hj_last : j = b + 1
    · subst hj_last
      exact h_not
    · have hj_le : j ≤ b := by omega
      exact ih h_rec j hj1 hj_le

/-- Constructive Pigeonhole Principle for functions `f : Nat → Fin k`:
    Any sequence of `k + 1` values on `0..k` contains a collision. -/
theorem fin_pigeonhole : ∀ {k : Nat} (f : Nat → Fin k),
    ∃ i j, i < j ∧ j ≤ k ∧ f i = f j
  | 0, f => False.elim (Nat.not_lt_zero (f 0).val (f 0).isLt)
  | 1, f => by
    have h : f 0 = f 1 := by
      have h0 : (f 0).val = 0 := by have := (f 0).isLt; omega
      have h1 : (f 1).val = 0 := by have := (f 1).isLt; omega
      exact Fin.ext (by omega)
    exact ⟨0, 1, by omega, by omega, h⟩
  | k + 2, f => by
    by_cases h_match : hasMatch (f 0) f (k + 2) = true
    · obtain ⟨j, hj1, hj2, hj_eq⟩ := hasMatch_true (f 0) f (k + 2) h_match
      exact ⟨0, j, by omega, hj2, hj_eq.symm⟩
    · have h_false : hasMatch (f 0) f (k + 2) = false := by
        cases h : hasMatch (f 0) f (k + 2)
        · rfl
        · contradiction
      have h_ne : ∀ m, m ≤ k + 1 → f (m + 1) ≠ f 0 := by
        intro m hm
        exact hasMatch_false (f 0) f (k + 2) h_false (m + 1) (by omega) (by omega)
      let g (m : Nat) : Fin (k + 1) :=
        if hm : m ≤ k + 1 then
          dropElem (f 0) (f (m + 1)) (h_ne m hm)
        else
          ⟨0, by omega⟩
      obtain ⟨i', j', hij', hj'k, hg⟩ := fin_pigeonhole (k := k + 1) g
      have hi'k : i' ≤ k + 1 := by omega
      have h_gi : g i' = dropElem (f 0) (f (i' + 1)) (h_ne i' hi'k) := by
        dsimp [g]; simp [hi'k]
      have h_gj : g j' = dropElem (f 0) (f (j' + 1)) (h_ne j' hj'k) := by
        dsimp [g]; simp [hj'k]
      rw [h_gi, h_gj] at hg
      have heq_f := dropElem_injective (f 0) (f (i' + 1)) (f (j' + 1))
        (h_ne i' hi'k) (h_ne j' hj'k) hg
      exact ⟨i' + 1, j' + 1, by omega, by omega, heq_f⟩

/-- Any capacity-k machine repeats an internal state within time `k`. -/
theorem capacity_repetition {k : Nat} (M : CapacityMachine k) :
    ∃ i j, i < j ∧ j ≤ k ∧ run M i = run M j :=
  fin_pigeonhole (run M)

/-- Consequently, any capacity-k machine repeats an observation within time `k`. -/
theorem capacity_obs_repetition {k : Nat} (M : CapacityMachine k) :
    ∃ i j, i < j ∧ j ≤ k ∧ obs M i = obs M j := by
  obtain ⟨i, j, hij, hj, hrun⟩ := capacity_repetition M
  refine ⟨i, j, hij, hj, ?_⟩
  dsimp [obs]
  rw [hrun]

/-! ## 3. The Cyclic Guest Machine Family -/

/-- The canonical cyclic guest graph with `m` vertices. -/
def cyclicGuest (m : Nat) (hm : m > 0) : CapacityMachine m where
  init := ⟨0, hm⟩
  step := fun v => ⟨(v.val + 1) % m, Nat.mod_lt _ hm⟩
  emit := fun v => v.val

theorem cyclicGuest_run (m : Nat) (hm : m > 0) (t : Nat) :
    (run (cyclicGuest m hm) t).val = t % m := by
  induction t with
  | zero =>
    rfl
  | succ t ih =>
    have : (run (cyclicGuest m hm) (t + 1)).val = ((run (cyclicGuest m hm) t).val + 1) % m := rfl
    rw [this, ih]
    rw [Nat.add_mod (t % m) 1 m, Nat.mod_mod, ← Nat.add_mod t 1 m]

theorem cyclicGuest_obs (m : Nat) (hm : m > 0) (t : Nat) :
    obs (cyclicGuest m hm) t = t % m := by
  dsimp [obs, cyclicGuest]
  exact cyclicGuest_run m hm t

/-- On the prefix `0..m-1`, all observations of `cyclicGuest m` are distinct. -/
theorem cyclicGuest_obs_injective (m : Nat) (hm : m > 0) {i j : Nat}
    (hi : i < m) (hj : j < m)
    (heq : obs (cyclicGuest m hm) i = obs (cyclicGuest m hm) j) :
    i = j := by
  rw [cyclicGuest_obs, cyclicGuest_obs] at heq
  rw [Nat.mod_eq_of_lt hi, Nat.mod_eq_of_lt hj] at heq
  exact heq

/-! ## 4. State-Capacity Obstruction and Stratification Irreducibility -/

/-- Faithful simulation of a guest machine by a host machine on scale `S`. -/
def FaithfulSimulation {k m : Nat} (H : CapacityMachine k) (G : CapacityMachine m) (S : Nat) : Prop :=
  ∀ t, t < S → obs H t = obs G t

/-- State-Capacity Obstruction Theorem:
    No host machine of vertex capacity `k` can faithfully simulate
    the cyclic guest machine of capacity `k + 1` on scale `k + 1`. -/
theorem state_capacity_obstruction (k : Nat) (H : CapacityMachine k) :
    ¬ FaithfulSimulation H (cyclicGuest (k + 1) (Nat.succ_pos k)) (k + 1) := by
  intro hsim
  obtain ⟨i, j, hij, hj, h_rep⟩ := capacity_obs_repetition H
  have hi_lt : i < k + 1 := by omega
  have hj_lt : j < k + 1 := by omega
  have h1 := hsim i hi_lt
  have h2 := hsim j hj_lt
  rw [h1, h2] at h_rep
  have h_eq : i = j := cyclicGuest_obs_injective (k + 1) (Nat.succ_pos k) hi_lt hj_lt h_rep
  omega

/-- Stratification Boundary Irreducibility Theorem:
    There exists no universal host machine of capacity `k` capable of
    evaluating all guest graphs of capacity `k + 1`. -/
theorem stratification_boundary_irreducible (k : Nat) :
    ¬ ∃ (H : CapacityMachine k),
        FaithfulSimulation H (cyclicGuest (k + 1) (Nat.succ_pos k)) (k + 1) := by
  intro ⟨H, hsim⟩
  exact state_capacity_obstruction k H hsim

/-- General Capacity Separation:
    A host of capacity `k` cannot simulate any guest of capacity `m > k`. -/
theorem capacity_separation {k m : Nat} (hm : m > k) (H : CapacityMachine k) :
    ¬ FaithfulSimulation H (cyclicGuest m (by omega)) (k + 1) := by
  intro hsim
  obtain ⟨i, j, hij, hj, h_rep⟩ := capacity_obs_repetition H
  have hi_lt : i < m := by omega
  have hj_lt : j < m := by omega
  have h1 := hsim i (by omega)
  have h2 := hsim j (by omega)
  rw [h1, h2] at h_rep
  have h_eq : i = j := cyclicGuest_obs_injective m (by omega) hi_lt hj_lt h_rep
  omega

end SelfInterpreterObstruction

#print axioms SelfInterpreterObstruction.dropElem_injective
#print axioms SelfInterpreterObstruction.hasMatch_true
#print axioms SelfInterpreterObstruction.hasMatch_false
#print axioms SelfInterpreterObstruction.fin_pigeonhole
#print axioms SelfInterpreterObstruction.capacity_repetition
#print axioms SelfInterpreterObstruction.capacity_obs_repetition
#print axioms SelfInterpreterObstruction.cyclicGuest_run
#print axioms SelfInterpreterObstruction.cyclicGuest_obs
#print axioms SelfInterpreterObstruction.cyclicGuest_obs_injective
#print axioms SelfInterpreterObstruction.state_capacity_obstruction
#print axioms SelfInterpreterObstruction.stratification_boundary_irreducible
#print axioms SelfInterpreterObstruction.capacity_separation
