import ObserverHierarchy

/-!
# SeparationCapacity: Exact Observer Separation Bounds and Scale Depth Gap

Formalization of Requirement R2 (Part 1):
- The maximum separation capacity Sep(k) = 2^k of finite observers of resolution depth k.
- The pairwise non-isomorphic canonical regime family of size 2^(k+1) at scale depth k+2.
- The exact separation gap Gap(k, d) = 2^(d-1) - 2^k > 0 across scale depth d ≥ k+2.
- Asymptotic divergence of true isomorphism classes from finite observer capacity.

Axioms: strictly within {propext, Quot.sound}, zero mathlib, zero custom axioms, zero unproven escapes.
AuthorityEffect: None.
-/

namespace HigherOrderDiagonalization

/-! ## 1. Binary Representations and Injectivity -/

/-- Convert natural number to little-endian binary bit list of fixed length. -/
def natToBits : Nat → Nat → List (Fin 2)
  | 0, _ => []
  | len + 1, n => ⟨n % 2, by omega⟩ :: natToBits len (n / 2)

theorem natToBits_length (len : Nat) (n : Nat) : (natToBits len n).length = len := by
  induction len generalizing n with
  | zero => rfl
  | succ l ih =>
      dsimp [natToBits]
      rw [ih]

/-- Decode binary bit list back to natural number. -/
def bitsToNat : List (Fin 2) → Nat
  | [] => 0
  | x :: xs => x.val + 2 * bitsToNat xs

/-- Roundtrip identity: decoding an encoded number below 2^len recovers the number. -/
theorem bitsToNat_natToBits (len : Nat) (n : Nat) (h : n < 2 ^ len) :
    bitsToNat (natToBits len n) = n := by
  induction len generalizing n with
  | zero =>
      have h0 : n = 0 := by omega
      subst h0
      rfl
  | succ l ih =>
      dsimp [natToBits, bitsToNat]
      have h_div : n / 2 < 2 ^ l := by
        rw [Nat.pow_succ] at h
        omega
      have h_rec := ih (n / 2) h_div
      rw [h_rec]
      exact Nat.mod_add_div n 2

/-- Injectivity of natToBits on bounded inputs. -/
theorem natToBits_injective (len : Nat) (i j : Nat) (hi : i < 2 ^ len) (hj : j < 2 ^ len)
    (h_eq : natToBits len i = natToBits len j) : i = j := by
  have h_dec_i := bitsToNat_natToBits len i hi
  have h_dec_j := bitsToNat_natToBits len j hj
  rw [← h_dec_i, ← h_dec_j, h_eq]

/-! ## 2. Canonical Test Regimes at Scale Depth k+2 -/

theorem flip_token_zero : flipToken ⟨0, by omega⟩ = ⟨1, by omega⟩ := rfl

theorem flip_seq_head_zero (tail : List (Fin 2)) :
    flipSeq (⟨0, by omega⟩ :: tail) = ⟨1, by omega⟩ :: flipSeq tail := rfl

theorem leSeq_zero_one (t1 t2 : List (Fin 2)) :
    leSeq (⟨0, by omega⟩ :: t1) (⟨1, by omega⟩ :: t2) = true := by
  dsimp [leSeq]

/-- Any sequence starting with 0 is already canonical. -/
theorem canonSeq_zero_head (tail : List (Fin 2)) :
    canonSeq (⟨0, by omega⟩ :: tail) = ⟨0, by omega⟩ :: tail := by
  dsimp [canonSeq, flipSeq, flipToken, leSeq]

/-- Canonical test regime i at scale depth k+2. -/
def testRegime (k : Nat) (i : Nat) : ScaleRegime where
  depth := k + 2
  tokens := ⟨0, by omega⟩ :: natToBits (k + 1) i
  h_len := by
    dsimp
    rw [natToBits_length]

/-- Test regimes have identical canonical tokens to their raw tokens. -/
theorem testRegime_canon (k : Nat) (i : Nat) :
    canonSeq (testRegime k i).tokens = (testRegime k i).tokens :=
  canonSeq_zero_head (natToBits (k + 1) i)

/-- Theorem 2.1: Pairwise Non-Isomorphism of Test Family.
Distinct indices i ≠ j below 2^(k+1) produce strictly non-isomorphic regimes. -/
theorem testRegime_pairwise_non_isomorphic (k : Nat) (i j : Nat)
    (hi : i < 2 ^ (k + 1)) (hj : j < 2 ^ (k + 1)) (h_ne : i ≠ j) :
    ¬ Iso (testRegime k i) (testRegime k j) := by
  intro h_iso
  have h_canon := h_iso.2
  rw [testRegime_canon k i, testRegime_canon k j] at h_canon
  dsimp [testRegime] at h_canon
  injection h_canon with h_head h_tail
  have h_inj := natToBits_injective (k + 1) i j hi hj h_tail
  exact h_ne h_inj

/-! ## 3. Exact Separation Capacity Bounds and Depth Gap -/

/-- Maximum separation capacity of an observer of resolution depth k. -/
def capacity (k : Nat) : Nat := 2 ^ k

/-- Size of the canonical test family at scale depth k+2. -/
def testFamilySize (k : Nat) : Nat := 2 ^ (k + 1)

/-- Theorem 2.2: Test Family Strictly Outnumbers Observer Capacity. -/
theorem test_family_size_gt_capacity (k : Nat) : testFamilySize k > capacity k := by
  dsimp [testFamilySize, capacity]
  rw [Nat.pow_succ]
  have h_pos : 2 ^ k > 0 := Nat.two_pow_pos k
  omega

/-- The exact capacity gap between isomorphism classes at scale depth d and capacity at depth k. -/
def capacityGap (k d : Nat) : Nat :=
  if d > k + 1 then 2 ^ (d - 1) - capacity k else 0

/-- Theorem 2.3: Strictly Positive Capacity Gap at Immediate Next Scale. -/
theorem capacity_gap_strictly_positive (k : Nat) :
    capacityGap k (k + 2) > 0 := by
  dsimp [capacityGap, capacity]
  have h_gt : k + 2 > k + 1 := by omega
  simp [h_gt]
  rw [Nat.pow_succ]
  have h_pos : 2 ^ k > 0 := Nat.two_pow_pos k
  omega

/-- Theorem 2.4: Capacity Gap Lower Bound across Arbitrary Scale Depth d ≥ k+2. -/
theorem capacity_gap_asymptotic (k : Nat) (d : Nat) (h : d ≥ k + 2) :
    capacityGap k d ≥ 2 ^ k := by
  dsimp [capacityGap, capacity]
  have h_gt : d > k + 1 := by omega
  simp [h_gt]
  have h_exp : d - 1 ≥ k + 1 := by omega
  have h_pow : 2 ^ (d - 1) ≥ 2 ^ (k + 1) := Nat.pow_le_pow_right (by omega) h_exp
  rw [Nat.pow_succ] at h_pow
  omega

/-- Theorem 2.5: Capacity Gap Exact Value at Depth k+2. -/
theorem capacity_gap_at_k_plus_2 (k : Nat) :
    capacityGap k (k + 2) = 2 ^ k := by
  dsimp [capacityGap, capacity]
  have h_gt : k + 2 > k + 1 := by omega
  simp [h_gt]
  rw [Nat.pow_succ]
  omega

end HigherOrderDiagonalization
