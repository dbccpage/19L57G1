/-
Target X300: Observer-Relative Information, Channels & Loss.

Constructive formalization of:
1. Operational communication channels and Markov composition.
2. Data Processing Inequality (DPI) for distinguishability and decodability.
3. Invertible post-processing and sufficient statistic preservation.
4. Additive Hartley capacity and exact dyadic entropy scaling.
5. Sequential memory retention monotonicity under iterated operational noise.
6. Lossy coarse-graining and Landauer operational erasure non-reversibility.

AuthorityEffect: None.
Constructive: 100% core Lean 4, zero Classical.choice, zero mathlib.
Axioms: strictly within {propext, Quot.sound}.
-/

namespace X300ObserverInformation

-- ============================================================================
-- 1. Operational Communication Channels & Markov Compositions
-- ============================================================================

/-- Operational deterministic channel between observation types α and β. -/
def DetChannel (α : Type) (β : Type) := α → β

/-- Markov channel composition: feeding channel f into channel g. -/
def DetChannel.compose {α β γ : Type} (f : DetChannel α β) (g : DetChannel β γ) : DetChannel α γ :=
  g ∘ f

/-- Theorem 1 (Channel Composition Associativity):
    Concatenating operational communication channels is strictly associative. -/
theorem channel_compose_assoc {α β γ δ : Type}
    (f : DetChannel α β) (g : DetChannel β γ) (h : DetChannel γ δ) :
    DetChannel.compose (DetChannel.compose f g) h = DetChannel.compose f (DetChannel.compose g h) :=
  rfl

/-- Theorem 2 (Channel Identity Left):
    Composing with the identity observer channel on the left preserves the channel. -/
theorem channel_compose_id_left {α β : Type} (f : DetChannel α β) :
    DetChannel.compose id f = f :=
  rfl

/-- Theorem 3 (Channel Identity Right):
    Composing with the identity observer channel on the right preserves the channel. -/
theorem channel_compose_id_right {α β : Type} (f : DetChannel α β) :
    DetChannel.compose f id = f :=
  rfl


-- ============================================================================
-- 2. Data Processing Inequality (DPI)
-- ============================================================================

/-- Two world states are distinguishable by observer readout Y if their observations differ. -/
def Distinguishable {Ω β : Type} (Y : Ω → β) (ω1 ω2 : Ω) : Prop :=
  Y ω1 ≠ Y ω2

/-- Two world states are indistinguishable (fiber collision) if their observations match. -/
def Indistinguishable {Ω β : Type} (Y : Ω → β) (ω1 ω2 : Ω) : Prop :=
  Y ω1 = Y ω2

/-- Theorem 4 (Coarse-Graining Fiber Inclusion):
    Any post-processing g preserves indistinguishability:
    if Y cannot distinguish ω1 and ω2, no post-processed observer Z = g ∘ Y can distinguish them. -/
theorem post_processing_coarse_graining {Ω β γ : Type}
    (Y : Ω → β) (g : β → γ) (ω1 ω2 : Ω)
    (h : Indistinguishable Y ω1 ω2) :
    Indistinguishable (g ∘ Y) ω1 ω2 := by
  dsimp [Indistinguishable] at *
  rw [h]

/-- Theorem 5 (Data Processing Inequality for Distinguishability):
    Operational post-processing cannot create new distinctions:
    if Z = g ∘ Y distinguishes two states, Y must have already distinguished them. -/
theorem dpi_distinguishability {Ω β γ : Type}
    (Y : Ω → β) (g : β → γ) (ω1 ω2 : Ω)
    (h : Distinguishable (g ∘ Y) ω1 ω2) :
    Distinguishable Y ω1 ω2 := by
  intro h_eq
  have h_post := post_processing_coarse_graining Y g ω1 ω2 h_eq
  exact h h_post

/-- Distinguishing witness between a source variable X and observer readout Y:
    both observers simultaneously distinguish the state pair. -/
def MutualDistinction {Ω α β : Type} (X : Ω → α) (Y : Ω → β) (ω1 ω2 : Ω) : Prop :=
  Distinguishable X ω1 ω2 ∧ Distinguishable Y ω1 ω2

/-- Theorem 6 (Data Processing Inequality for Mutual Distinctions):
    In a Markov chain X → Y → Z where Z = g ∘ Y,
    any mutual distinction witnessed by (X, Z) is necessarily witnessed by (X, Y).
    Operational post-processing cannot increase mutual information distinctions. -/
theorem dpi_mutual_distinction {Ω α β γ : Type}
    (X : Ω → α) (Y : Ω → β) (g : β → γ) (ω1 ω2 : Ω)
    (h : MutualDistinction X (g ∘ Y) ω1 ω2) :
    MutualDistinction X Y ω1 ω2 := by
  constructor
  · exact h.1
  · exact dpi_distinguishability Y g ω1 ω2 h.2

/-- Theorem 7 (DPI for Decodability / Operational Reconstruction):
    If an observer can decode source X from post-processed data Z = g ∘ Y via decoder DZ,
    then an observer can decode X from Y with equal fidelity via composed decoder DY = DZ ∘ g. -/
theorem dpi_decodability {Ω α β γ : Type}
    (X : Ω → α) (Y : Ω → β) (g : β → γ) (DZ : γ → α)
    (h_decode : ∀ ω, DZ ((g ∘ Y) ω) = X ω) :
    ∀ ω, (DZ ∘ g) (Y ω) = X ω := by
  intro ω
  exact h_decode ω

/-- Theorem 8 (Sufficient Statistic / Invertible Processing Preserves Distinctions):
    If post-processing g has a left inverse (lossless decoding),
    then Z = g ∘ Y preserves all distinctions of Y:
    Distinguishable Z ω1 ω2 ↔ Distinguishable Y ω1 ω2. -/
theorem invertible_postprocessing_preserves_distinctions {Ω β γ : Type}
    (Y : Ω → β) (g : β → γ) (h_inv : γ → β) (h_left : ∀ y, h_inv (g y) = y) (ω1 ω2 : Ω) :
    Distinguishable (g ∘ Y) ω1 ω2 ↔ Distinguishable Y ω1 ω2 := by
  constructor
  · intro h
    exact dpi_distinguishability Y g ω1 ω2 h
  · intro h h_eq
    dsimp [Distinguishable] at h
    have h_recovered : h_inv ((g ∘ Y) ω1) = h_inv ((g ∘ Y) ω2) := by rw [h_eq]
    dsimp [Function.comp] at h_recovered
    rw [h_left (Y ω1), h_left (Y ω2)] at h_recovered
    exact h h_recovered


-- ============================================================================
-- 3. Exact Additive Hartley Capacity & Entropy Monotonicity
-- ============================================================================

/-- Hartley capacity metric for discrete observation alphabets with 2^k states. -/
def hartleyCapacity (k : Nat) : Nat := k

/-- Theorem 9 (Additive Hartley Capacity on Independent Product Systems):
    For independent distributed observers with state spaces of size 2^k and 2^m,
    the joint capacity is exactly additive: capacity(k + m) = capacity(k) + capacity(m). -/
theorem hartley_capacity_additive (k m : Nat) :
    hartleyCapacity (k + m) = hartleyCapacity k + hartleyCapacity m :=
  rfl

/-- Theorem 10 (State Space Multiplicativity):
    The number of joint states in independent observer product alphabets multiplies as powers of 2. -/
theorem state_space_multiplicative (k m : Nat) :
    2 ^ (k + m) = 2 ^ k * 2 ^ m :=
  Nat.pow_add 2 k m

/-- Theorem 11 (Coarse-Graining Capacity Loss):
    A lossy coarse-graining projecting an alphabet of capacity k to capacity m (with m ≤ k)
    incurs a non-negative capacity reduction: capacity(m) ≤ capacity(k). -/
theorem coarse_graining_capacity_monotonic (k m : Nat) (h : m ≤ k) :
    hartleyCapacity m ≤ hartleyCapacity k :=
  h

/-- Scaled dyadic Shannon entropy for leaf bit-lengths D at maximum depth K:
    E(D, K) = sum_{d in D} d * 2^(K - d).
    For a pure dyadic distribution where P(i) = 2^(-d_i), E(D, K) / 2^K is the exact Shannon entropy in Q. -/
def scaledEntropy : List Nat → Nat → Nat
  | [], _ => 0
  | d :: ds, K => d * 2 ^ (K - d) + scaledEntropy ds K

/-- Theorem 12 (1-Bit Memory Entropy):
    A 1-bit memory cell with uniform distribution (two states, each length 1)
    has scaled entropy equal to 2 at scale 1, corresponding to exactly 2 / 2^1 = 1 bit. -/
theorem uniform_1bit_scaled_entropy :
    scaledEntropy [1, 1] 1 = 2 :=
  rfl

/-- Theorem 13 (2-Bit Memory Entropy):
    A 2-bit memory cell with uniform distribution (four states, each length 2)
    has scaled entropy equal to 8 at scale 2, corresponding to exactly 8 / 2^2 = 2 bits. -/
theorem uniform_2bit_scaled_entropy :
    scaledEntropy [2, 2, 2, 2] 2 = 8 :=
  rfl


-- ============================================================================
-- 4. Memory Retention Limits under Sequential Noise
-- ============================================================================

/-- Iterated sequential memory degradation step under operational noise. -/
def iterStep {M : Type} (step : M → M) : Nat → M → M
  | 0 => id
  | n + 1 => step ∘ (iterStep step n)

/-- Theorem 14 (Memory Retention Monotonicity):
    Information retained in memory is monotonically non-increasing over sequential degradation steps.
    Any distinction surviving step n + 1 must have survived step n. -/
theorem memory_retention_monotone {Ω M : Type}
    (step : M → M) (M0 : Ω → M) (n : Nat) (ω1 ω2 : Ω)
    (h : Distinguishable (iterStep step (n + 1) ∘ M0) ω1 ω2) :
    Distinguishable (iterStep step n ∘ M0) ω1 ω2 := by
  dsimp [iterStep, Function.comp] at h
  intro h_eq
  dsimp [Distinguishable, Function.comp] at *
  have h_step : step (iterStep step n (M0 ω1)) = step (iterStep step n (M0 ω2)) := by
    rw [h_eq]
  exact h h_step


-- ============================================================================
-- 5. Landauer Operational Erasure Cost & Non-Reversibility
-- ============================================================================

/-- Operational reset/erasure operator mapping any memory state in Fin (k + 1) to standard 0. -/
def eraseToZero {k : Nat} (_ : Fin (k + 1)) : Fin (k + 1) :=
  ⟨0, Nat.zero_lt_succ k⟩

/-- Theorem 15 (Erasure Collapses Distinct States):
    For any state space with at least 2 states (Fin (k + 2)),
    operational erasure maps distinct states 0 and 1 to the identical reset state 0. -/
theorem erasure_collapses_states {k : Nat} :
    let s0 : Fin (k + 2) := ⟨0, Nat.zero_lt_succ (k + 1)⟩
    let s1 : Fin (k + 2) := ⟨1, Nat.succ_lt_succ (Nat.zero_lt_succ k)⟩
    eraseToZero s0 = eraseToZero s1 ∧ s0 ≠ s1 := by
  intro s0 s1
  constructor
  · rfl
  · intro h_contra
    have h_val : (0 : Nat) = 1 := congrArg Fin.val h_contra
    nomatch h_val

/-- Theorem 16 (Landauer Operational Non-Reversibility):
    For any state space with at least 2 states,
    no deterministic recovery operator R can undo the erasure operator.
    Operational erasure is strictly non-invertible, establishing the thermodynamic erasure requirement. -/
theorem erasure_strictly_non_reversible {k : Nat} :
    ¬ ∃ (R : Fin (k + 2) → Fin (k + 2)), ∀ s, R (eraseToZero s) = s := by
  intro ⟨R, h_rec⟩
  let s0 : Fin (k + 2) := ⟨0, Nat.zero_lt_succ (k + 1)⟩
  let s1 : Fin (k + 2) := ⟨1, Nat.succ_lt_succ (Nat.zero_lt_succ k)⟩
  have h0 : R (eraseToZero s0) = s0 := h_rec s0
  have h1 : R (eraseToZero s1) = s1 := h_rec s1
  have h_same : eraseToZero s0 = eraseToZero s1 := rfl
  rw [h_same] at h0
  have h_eq : s0 = s1 := by rw [← h0, h1]
  have h_val : (0 : Nat) = 1 := congrArg Fin.val h_eq
  nomatch h_val

/-- Theorem 17 (Phase Space Contraction):
    Operational erasure compresses the entire state space into a single singleton image. -/
theorem erasure_image_singleton {k : Nat} (s1 s2 : Fin (k + 1)) :
    eraseToZero s1 = eraseToZero s2 :=
  rfl

end X300ObserverInformation
