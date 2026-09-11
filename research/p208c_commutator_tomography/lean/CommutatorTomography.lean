/-!
# Finite Commutator Obstruction & Discrete MUB Tomography (Target P208c)

Formalizes:
1. Exact Matrix Algebra & Finite Summation over discrete indices.
2. Commutator trace identity:
   Tr([A, B]) = 0 for all finite N x N matrices.
3. Finite Commutator Trace Obstruction Theorem:
   The continuous canonical commutation relation [Q, P] = c * I with c ≠ 0 is
   algebraically obstructed on any finite carrier of dimension N ≥ 1.
4. Multi-locus microcausality on composite carrier networks:
   Observables localized on disjoint loci commute: [A ⊗ I_B, I_A ⊗ B] = 0.
5. Discrete Mutually Unbiased Bases (MUBs):
   Exact construction of d + 1 = 4 MUBs in dimension d = 3 in Z[w].
   Exact construction of d + 1 = 5 MUBs in dimension d = 4 in Z[i].
   Pairwise unbiasedness: |<u_j | v_k>|^2 = 1/d across all distinct bases.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly within `{propext, Quot.sound}`;
zero `Classical.choice`; zero `mathlib`.
-/

namespace P208cCommutatorTomography

-- =============================================================================
-- 1. Exact Summation and Finite Matrix Algebra
-- =============================================================================

/-- Recursive summation over integer lists. -/
def sum : List Int → Int
  | [] => 0
  | x :: xs => x + sum xs

theorem sum_zero {α : Type} (l : List α) :
    sum (l.map (fun _ => (0 : Int))) = 0 := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    dsimp [List.map, sum]
    omega

theorem sum_add {α : Type} (l : List α) (f g : α → Int) :
    sum (l.map (fun x => f x + g x)) = sum (l.map f) + sum (l.map g) := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    dsimp [List.map, sum]
    omega

theorem sum_sub {α : Type} (l : List α) (f g : α → Int) :
    sum (l.map (fun x => f x - g x)) = sum (l.map f) - sum (l.map g) := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
    dsimp [List.map, sum]
    omega

theorem sum_swap {α β : Type} (l₁ : List α) (l₂ : List β) (f : α → β → Int) :
    sum (l₁.map (fun x => sum (l₂.map (fun y => f x y)))) =
    sum (l₂.map (fun y => sum (l₁.map (fun x => f x y)))) := by
  induction l₁ with
  | nil =>
    dsimp [List.map, sum]
    have hz : sum (l₂.map (fun _ => (0 : Int))) = 0 := sum_zero l₂
    exact hz.symm
  | cons x xs ih =>
    dsimp [List.map, sum]
    rw [ih]
    have hdistrib : sum (l₂.map (fun y => f x y + sum (xs.map (fun x' => f x' y)))) =
        sum (l₂.map (fun y => f x y)) + sum (l₂.map (fun y => sum (xs.map (fun x' => f x' y)))) := by
      exact sum_add l₂ (fun y => f x y) (fun y => sum (xs.map (fun x' => f x' y)))
    exact hdistrib.symm

theorem sum_congr {α : Type} (l : List α) (f g : α → Int) (h : ∀ x, f x = g x) :
    sum (l.map f) = sum (l.map g) := by
  have heq : f = g := funext h
  rw [heq]

theorem sum_mul_const {α : Type} (l : List α) (c : Int) (f : α → Int) :
    sum (l.map (fun x => f x * c)) = sum (l.map f) * c := by
  induction l with
  | nil =>
    dsimp [List.map, sum]
    rw [Int.zero_mul]
  | cons x xs ih =>
    dsimp [List.map, sum]
    rw [ih]
    rw [Int.add_mul]

theorem const_mul_sum {α : Type} (l : List α) (c : Int) (f : α → Int) :
    sum (l.map (fun x => c * f x)) = c * sum (l.map f) := by
  induction l with
  | nil =>
    dsimp [List.map, sum]
    rw [Int.mul_zero]
  | cons x xs ih =>
    dsimp [List.map, sum]
    rw [ih]
    rw [Int.mul_add]

theorem sum_prod {α β : Type} (l₁ : List α) (l₂ : List β) (f : α → Int) (g : β → Int) :
    sum (l₁.map (fun x => sum (l₂.map (fun y => f x * g y)))) =
    sum (l₁.map f) * sum (l₂.map g) := by
  have h_inner (x : α) : sum (l₂.map (fun y => f x * g y)) = f x * sum (l₂.map g) :=
    const_mul_sum l₂ (f x) g
  have h_simp : sum (l₁.map (fun x => sum (l₂.map (fun y => f x * g y)))) =
                sum (l₁.map (fun x => f x * sum (l₂.map g))) := by
    have heq : (fun x => sum (l₂.map (fun y => f x * g y))) = (fun x => f x * sum (l₂.map g)) :=
      funext h_inner
    rw [heq]
  rw [h_simp]
  exact sum_mul_const l₁ (sum (l₂.map g)) f

theorem sum_const {α : Type} (l : List α) (c : Int) :
    sum (l.map (fun _ => c)) = (l.length : Int) * c := by
  induction l with
  | nil =>
    dsimp [List.map, sum, List.length]
    rw [Int.zero_mul]
  | cons x xs ih =>
    dsimp [List.map, sum, List.length]
    rw [ih]
    push_cast
    rw [Int.add_mul, Int.one_mul, Int.add_comm]

/-- Discrete square matrix of dimension n over Int. -/
def Matrix (n : Nat) := Fin n → Fin n → Int

/-- Discrete matrix multiplication A @ B. -/
def matMul (n : Nat) (A B : Matrix n) : Matrix n :=
  fun i j => sum ((List.finRange n).map (fun k => A i k * B k j))

/-- Discrete matrix trace Tr(A) = sum_i A_ii. -/
def trace (n : Nat) (A : Matrix n) : Int :=
  sum ((List.finRange n).map (fun i => A i i))

/-- Discrete matrix commutator [A, B] = A B - B A. -/
def commutator (n : Nat) (A B : Matrix n) : Matrix n :=
  fun i j => matMul n A B i j - matMul n B A i j

/-- Identity matrix I_n. -/
def identity (n : Nat) : Matrix n :=
  fun i j => if i = j then 1 else 0

/-- Scalar matrix multiplication c * A. -/
def scalarMul (n : Nat) (c : Int) (A : Matrix n) : Matrix n :=
  fun i j => c * A i j


-- =============================================================================
-- 2. Trace Commutativity & Finite Commutator Trace Obstruction
-- =============================================================================

/-- Trace commutativity theorem: Tr(A B) = Tr(B A) for any n x n matrices. -/
theorem trace_matMul_comm (n : Nat) (A B : Matrix n) :
    trace n (matMul n A B) = trace n (matMul n B A) := by
  dsimp [trace, matMul]
  have hswap := sum_swap (List.finRange n) (List.finRange n) (fun i k => A i k * B k i)
  rw [hswap]
  apply sum_congr
  intro k
  apply sum_congr
  intro i
  rw [Int.mul_comm]

/-- Commutator trace vanishing theorem: Tr([A, B]) = 0. -/
theorem trace_commutator_zero (n : Nat) (A B : Matrix n) :
    trace n (commutator n A B) = 0 := by
  dsimp [trace, commutator]
  have hsub := sum_sub (List.finRange n) (fun i => matMul n A B i i) (fun i => matMul n B A i i)
  rw [hsub]
  have hcomm := trace_matMul_comm n A B
  dsimp [trace] at hcomm
  rw [hcomm]
  omega

/-- Trace of scalar identity: Tr(c * I_n) = n * c. -/
theorem trace_scalar_identity (n : Nat) (c : Int) :
    trace n (scalarMul n c (identity n)) = (n : Int) * c := by
  dsimp [trace, scalarMul, identity]
  have hsimp : sum ((List.finRange n).map (fun i => c * (if i = i then (1 : Int) else 0))) =
               sum ((List.finRange n).map (fun _ => c)) := by
    apply sum_congr
    intro i
    rw [if_pos rfl, Int.mul_one]
  rw [hsimp]
  rw [sum_const]
  rw [List.length_finRange]

/-- **Finite Commutator Trace Obstruction Theorem.**
    On any finite carrier of dimension n ≥ 1, the canonical commutation relation
    [Q, P] = c * I is algebraically obstructed for any non-zero scalar c. -/
theorem commutator_trace_obstruction (n : Nat) (hn : n ≥ 1) (c : Int) (hc : c ≠ 0)
    (Q P : Matrix n) :
    commutator n Q P ≠ scalarMul n c (identity n) := by
  intro h_eq
  have h_tr : trace n (commutator n Q P) = trace n (scalarMul n c (identity n)) := by
    rw [h_eq]
  rw [trace_commutator_zero n Q P] at h_tr
  rw [trace_scalar_identity n c] at h_tr
  have h_prod : (n : Int) * c ≠ 0 := by
    have hn_pos : (n : Int) ≠ 0 := by omega
    exact Int.mul_ne_zero hn_pos hc
  exact h_prod h_tr.symm


-- =============================================================================
-- 3. Multi-Locus Carriers & Microcausality
-- =============================================================================

/-- Composite matrix on bipartite carrier loci (A, B). -/
def BiMatrix (nA nB : Nat) := (Fin nA × Fin nB) → (Fin nA × Fin nB) → Int

/-- Tensor product of local observables: (A ⊗ B). -/
def tensor (nA nB : Nat) (A : Matrix nA) (B : Matrix nB) : BiMatrix nA nB :=
  fun (ia, ib) (ja, jb) => A ia ja * B ib jb

/-- Matrix multiplication on bipartite composite carrier. -/
def biMatMul (nA nB : Nat) (M N : BiMatrix nA nB) : BiMatrix nA nB :=
  fun (ia, ib) (ka, kb) =>
    sum ((List.finRange nA).map (fun ja =>
      sum ((List.finRange nB).map (fun jb =>
        M (ia, ib) (ja, jb) * N (ja, jb) (ka, kb)))))

/-- Commutator on composite carrier. -/
def biCommutator (nA nB : Nat) (M N : BiMatrix nA nB) : BiMatrix nA nB :=
  fun idx1 idx2 => biMatMul nA nB M N idx1 idx2 - biMatMul nA nB N M idx1 idx2

/-- Observable at Locus A embedded on composite carrier: A ⊗ I_B. -/
def embedA (nA nB : Nat) (A : Matrix nA) : BiMatrix nA nB :=
  tensor nA nB A (identity nB)

/-- Observable at Locus B embedded on composite carrier: I_A ⊗ B. -/
def embedB (nA nB : Nat) (B : Matrix nB) : BiMatrix nA nB :=
  tensor nA nB (identity nA) B

theorem finRange_two : List.finRange 2 = [(0 : Fin 2), 1] := rfl

theorem fin2_cases (i : Fin 2) : i = 0 ∨ i = 1 := by
  obtain ⟨val, isLt⟩ := i
  match val with
  | 0 => left; rfl
  | 1 => right; rfl
  | n + 2 => omega

/-- Right identity law for 2x2 matrix multiplication. -/
theorem matMul_identity_2 (A : Matrix 2) : matMul 2 A (identity 2) = A := by
  funext i j
  rcases fin2_cases i with rfl | rfl <;> rcases fin2_cases j with rfl | rfl
  · dsimp [matMul]; rw [finRange_two]; dsimp [List.map, sum, identity]; omega
  · dsimp [matMul]; rw [finRange_two]; dsimp [List.map, sum, identity]; omega
  · dsimp [matMul]; rw [finRange_two]; dsimp [List.map, sum, identity]; omega
  · dsimp [matMul]; rw [finRange_two]; dsimp [List.map, sum, identity]; omega

/-- Left identity law for 2x2 matrix multiplication. -/
theorem identity_matMul_2 (A : Matrix 2) : matMul 2 (identity 2) A = A := by
  funext i j
  rcases fin2_cases i with rfl | rfl <;> rcases fin2_cases j with rfl | rfl
  · dsimp [matMul]; rw [finRange_two]; dsimp [List.map, sum, identity]; omega
  · dsimp [matMul]; rw [finRange_two]; dsimp [List.map, sum, identity]; omega
  · dsimp [matMul]; rw [finRange_two]; dsimp [List.map, sum, identity]; omega
  · dsimp [matMul]; rw [finRange_two]; dsimp [List.map, sum, identity]; omega

/-- Mixed-product theorem for tensor composition:
    (A₁ ⊗ B₁) (A₂ ⊗ B₂) = (A₁ A₂) ⊗ (B₁ B₂). -/
theorem tensor_mixed_product (nA nB : Nat) (A₁ A₂ : Matrix nA) (B₁ B₂ : Matrix nB) :
    biMatMul nA nB (tensor nA nB A₁ B₁) (tensor nA nB A₂ B₂) =
    tensor nA nB (matMul nA A₁ A₂) (matMul nB B₁ B₂) := by
  funext (ia, ib) (ka, kb)
  dsimp [biMatMul, tensor, matMul]
  have h_alg (ja : Fin nA) (jb : Fin nB) :
      (A₁ ia ja * B₁ ib jb) * (A₂ ja ka * B₂ jb kb) =
      (A₁ ia ja * A₂ ja ka) * (B₁ ib jb * B₂ jb kb) := by
    have h1 : A₁ ia ja * B₁ ib jb * (A₂ ja ka * B₂ jb kb) =
              A₁ ia ja * (B₁ ib jb * (A₂ ja ka * B₂ jb kb)) := Int.mul_assoc _ _ _
    have h2 : B₁ ib jb * (A₂ ja ka * B₂ jb kb) =
              A₂ ja ka * (B₁ ib jb * B₂ jb kb) := by
      rw [← Int.mul_assoc, Int.mul_comm (B₁ ib jb), Int.mul_assoc]
    rw [h1, h2, ← Int.mul_assoc]
  have h_congr_inner (ja : Fin nA) :
      sum ((List.finRange nB).map (fun jb => (A₁ ia ja * B₁ ib jb) * (A₂ ja ka * B₂ jb kb))) =
      sum ((List.finRange nB).map (fun jb => (A₁ ia ja * A₂ ja ka) * (B₁ ib jb * B₂ jb kb))) := by
    apply sum_congr
    intro jb
    exact h_alg ja jb
  have h_congr_outer :
      sum ((List.finRange nA).map (fun ja =>
        sum ((List.finRange nB).map (fun jb => (A₁ ia ja * B₁ ib jb) * (A₂ ja ka * B₂ jb kb))))) =
      sum ((List.finRange nA).map (fun ja =>
        sum ((List.finRange nB).map (fun jb => (A₁ ia ja * A₂ ja ka) * (B₁ ib jb * B₂ jb kb))))) := by
    apply sum_congr
    intro ja
    exact h_congr_inner ja
  rw [h_congr_outer]
  exact sum_prod (List.finRange nA) (List.finRange nB)
                 (fun ja => A₁ ia ja * A₂ ja ka)
                 (fun jb => B₁ ib jb * B₂ jb kb)

/-- **Multi-Locus Finite Microcausality Theorem on 2x2 Composite Carriers.**
    Observables on disjoint loci commute: [A ⊗ I_B, I_A ⊗ B] = 0. -/
theorem multi_locus_microcausality_2x2 (A B : Matrix 2) :
    biCommutator 2 2 (embedA 2 2 A) (embedB 2 2 B) = (fun _ _ => 0) := by
  funext idx1 idx2
  dsimp [biCommutator, embedA, embedB]
  rw [tensor_mixed_product 2 2 A (identity 2) (identity 2) B]
  rw [tensor_mixed_product 2 2 (identity 2) A B (identity 2)]
  rw [matMul_identity_2 A, identity_matMul_2 A]
  rw [identity_matMul_2 B, matMul_identity_2 B]
  omega


-- =============================================================================
-- 4. Discrete Cyclotomic Field Z[w] & Dimension 3 MUBs
-- =============================================================================

/-- Exact cyclotomic ring Z[w] where w^2 + w + 1 = 0. -/
structure Cyclo3 where
  a : Int
  b : Int
  deriving DecidableEq, Repr

namespace Cyclo3

def zero : Cyclo3 := ⟨0, 0⟩
def one : Cyclo3 := ⟨1, 0⟩
def omega : Cyclo3 := ⟨0, 1⟩
def omega2 : Cyclo3 := ⟨-1, -1⟩

def add (x y : Cyclo3) : Cyclo3 := ⟨x.a + y.a, x.b + y.b⟩
def sub (x y : Cyclo3) : Cyclo3 := ⟨x.a - y.a, x.b - y.b⟩
def mul (x y : Cyclo3) : Cyclo3 :=
  ⟨x.a * y.a - x.b * y.b, x.a * y.b + x.b * y.a - x.b * y.b⟩
def conj (x : Cyclo3) : Cyclo3 := ⟨x.a - x.b, -x.b⟩
def normSq (x : Cyclo3) : Int := x.a * x.a - x.a * x.b + x.b * x.b

instance : Add Cyclo3 := ⟨add⟩
instance : Sub Cyclo3 := ⟨sub⟩
instance : Mul Cyclo3 := ⟨mul⟩
instance : Zero Cyclo3 := ⟨zero⟩
instance : One Cyclo3 := ⟨one⟩

def dot3 (u v : Fin 3 → Cyclo3) : Cyclo3 :=
  (u 0).conj * (v 0) + (u 1).conj * (v 1) + (u 2).conj * (v 2)

def wPow (p : Nat) : Cyclo3 :=
  match p % 3 with
  | 0 => one
  | 1 => omega
  | _ => omega2

-- Basis 0 (standard computational basis)
def mub0 (k : Fin 3) : Fin 3 → Cyclo3 :=
  fun j => if j = k then ⟨1, 0⟩ else ⟨0, 0⟩

-- Bases 1, 2, 3 (Fourier-type bases)
def mubFourier (r : Nat) (k : Fin 3) : Fin 3 → Cyclo3 :=
  fun j => wPow (2 * r * j.val * j.val + j.val * k.val)

def mub1 := mubFourier 0
def mub2 := mubFourier 1
def mub3 := mubFourier 2

-- Within-basis orthonormality theorems
theorem mub0_orthonormal (j k : Fin 3) :
    normSq (dot3 (mub0 j) (mub0 k)) = if j = k then 1 else 0 := by
  revert j k; decide

theorem mub1_orthonormal (j k : Fin 3) :
    normSq (dot3 (mub1 j) (mub1 k)) = if j = k then 9 else 0 := by
  revert j k; decide

theorem mub2_orthonormal (j k : Fin 3) :
    normSq (dot3 (mub2 j) (mub2 k)) = if j = k then 9 else 0 := by
  revert j k; decide

theorem mub3_orthonormal (j k : Fin 3) :
    normSq (dot3 (mub3 j) (mub3 k)) = if j = k then 9 else 0 := by
  revert j k; decide

-- Pairwise mutual unbiasedness across all 6 distinct pairs:
-- NormSq = 1 for standard vs Fourier (physical overlap = 1/3)
-- NormSq = 3 for Fourier vs Fourier (physical overlap = 3/9 = 1/3)
theorem mub0_mub1_unbiased (j k : Fin 3) :
    normSq (dot3 (mub0 j) (mub1 k)) = 1 := by
  revert j k; decide

theorem mub0_mub2_unbiased (j k : Fin 3) :
    normSq (dot3 (mub0 j) (mub2 k)) = 1 := by
  revert j k; decide

theorem mub0_mub3_unbiased (j k : Fin 3) :
    normSq (dot3 (mub0 j) (mub3 k)) = 1 := by
  revert j k; decide

theorem mub1_mub2_unbiased (j k : Fin 3) :
    normSq (dot3 (mub1 j) (mub2 k)) = 3 := by
  revert j k; decide

theorem mub1_mub3_unbiased (j k : Fin 3) :
    normSq (dot3 (mub1 j) (mub3 k)) = 3 := by
  revert j k; decide

theorem mub2_mub3_unbiased (j k : Fin 3) :
    normSq (dot3 (mub2 j) (mub3 k)) = 3 := by
  revert j k; decide

end Cyclo3


-- =============================================================================
-- 5. Discrete Gaussian Integers Z[i] & Dimension 4 MUBs
-- =============================================================================

/-- Exact Gaussian integer ring Z[i] where i^2 = -1. -/
structure GaussInt where
  a : Int
  b : Int
  deriving DecidableEq, Repr

namespace GaussInt

def zero : GaussInt := ⟨0, 0⟩
def one : GaussInt := ⟨1, 0⟩
def mone : GaussInt := ⟨-1, 0⟩
def iUnit : GaussInt := ⟨0, 1⟩
def miUnit : GaussInt := ⟨0, -1⟩
def two : GaussInt := ⟨2, 0⟩

def add (x y : GaussInt) : GaussInt := ⟨x.a + y.a, x.b + y.b⟩
def sub (x y : GaussInt) : GaussInt := ⟨x.a - y.a, x.b - y.b⟩
def mul (x y : GaussInt) : GaussInt := ⟨x.a * y.a - x.b * y.b, x.a * y.b + x.b * y.a⟩
def conj (x : GaussInt) : GaussInt := ⟨x.a, -x.b⟩
def normSq (x : GaussInt) : Int := x.a * x.a + x.b * x.b

instance : Add GaussInt := ⟨add⟩
instance : Sub GaussInt := ⟨sub⟩
instance : Mul GaussInt := ⟨mul⟩
instance : Zero GaussInt := ⟨zero⟩
instance : One GaussInt := ⟨one⟩

def dot4 (u v : Fin 4 → GaussInt) : GaussInt :=
  (u 0).conj * (v 0) + (u 1).conj * (v 1) + (u 2).conj * (v 2) + (u 3).conj * (v 3)

-- Basis 0 (standard basis scaled by 2 so normSq = 4)
def mub4_0 (k : Fin 4) : Fin 4 → GaussInt :=
  fun j => if j = k then two else zero

-- Basis 1
def mub4_1 (k : Fin 4) : Fin 4 → GaussInt :=
  match k with
  | 0 => fun j => match j with | 0 => one | 1 => mone | 2 => one | 3 => mone
  | 1 => fun j => match j with | 0 => one | 1 => one | 2 => mone | 3 => mone
  | 2 => fun j => match j with | 0 => one | 1 => mone | 2 => mone | 3 => one
  | 3 => fun j => match j with | 0 => one | 1 => one | 2 => one | 3 => one

-- Basis 2
def mub4_2 (k : Fin 4) : Fin 4 → GaussInt :=
  match k with
  | 0 => fun j => match j with | 0 => one | 1 => miUnit | 2 => iUnit | 3 => one
  | 1 => fun j => match j with | 0 => one | 1 => iUnit | 2 => miUnit | 3 => one
  | 2 => fun j => match j with | 0 => one | 1 => miUnit | 2 => miUnit | 3 => mone
  | 3 => fun j => match j with | 0 => one | 1 => iUnit | 2 => iUnit | 3 => mone

-- Basis 3
def mub4_3 (k : Fin 4) : Fin 4 → GaussInt :=
  match k with
  | 0 => fun j => match j with | 0 => one | 1 => mone | 2 => miUnit | 3 => miUnit
  | 1 => fun j => match j with | 0 => one | 1 => one | 2 => miUnit | 3 => iUnit
  | 2 => fun j => match j with | 0 => one | 1 => one | 2 => iUnit | 3 => miUnit
  | 3 => fun j => match j with | 0 => one | 1 => mone | 2 => iUnit | 3 => iUnit

-- Basis 4
def mub4_4 (k : Fin 4) : Fin 4 → GaussInt :=
  match k with
  | 0 => fun j => match j with | 0 => one | 1 => miUnit | 2 => mone | 3 => miUnit
  | 1 => fun j => match j with | 0 => one | 1 => iUnit | 2 => mone | 3 => iUnit
  | 2 => fun j => match j with | 0 => one | 1 => iUnit | 2 => one | 3 => miUnit
  | 3 => fun j => match j with | 0 => one | 1 => miUnit | 2 => one | 3 => iUnit

-- Orthonormality within each basis (inner product normSq = 16 if j=k, 0 if j≠k)
theorem mub4_0_orthonormal (j k : Fin 4) :
    normSq (dot4 (mub4_0 j) (mub4_0 k)) = if j = k then 16 else 0 := by
  revert j k; decide

theorem mub4_1_orthonormal (j k : Fin 4) :
    normSq (dot4 (mub4_1 j) (mub4_1 k)) = if j = k then 16 else 0 := by
  revert j k; decide

theorem mub4_2_orthonormal (j k : Fin 4) :
    normSq (dot4 (mub4_2 j) (mub4_2 k)) = if j = k then 16 else 0 := by
  revert j k; decide

theorem mub4_3_orthonormal (j k : Fin 4) :
    normSq (dot4 (mub4_3 j) (mub4_3 k)) = if j = k then 16 else 0 := by
  revert j k; decide

theorem mub4_4_orthonormal (j k : Fin 4) :
    normSq (dot4 (mub4_4 j) (mub4_4 k)) = if j = k then 16 else 0 := by
  revert j k; decide

-- Mutual unbiasedness across all 10 distinct pairs of bases:
-- NormSq = 4 for all pairs (physical overlap = 4 / 16 = 1/4 = 1/d)
theorem mub4_0_1_unbiased (j k : Fin 4) : normSq (dot4 (mub4_0 j) (mub4_1 k)) = 4 := by
  revert j k; decide

theorem mub4_0_2_unbiased (j k : Fin 4) : normSq (dot4 (mub4_0 j) (mub4_2 k)) = 4 := by
  revert j k; decide

theorem mub4_0_3_unbiased (j k : Fin 4) : normSq (dot4 (mub4_0 j) (mub4_3 k)) = 4 := by
  revert j k; decide

theorem mub4_0_4_unbiased (j k : Fin 4) : normSq (dot4 (mub4_0 j) (mub4_4 k)) = 4 := by
  revert j k; decide

theorem mub4_1_2_unbiased (j k : Fin 4) : normSq (dot4 (mub4_1 j) (mub4_2 k)) = 4 := by
  revert j k; decide

theorem mub4_1_3_unbiased (j k : Fin 4) : normSq (dot4 (mub4_1 j) (mub4_3 k)) = 4 := by
  revert j k; decide

theorem mub4_1_4_unbiased (j k : Fin 4) : normSq (dot4 (mub4_1 j) (mub4_4 k)) = 4 := by
  revert j k; decide

theorem mub4_2_3_unbiased (j k : Fin 4) : normSq (dot4 (mub4_2 j) (mub4_3 k)) = 4 := by
  revert j k; decide

theorem mub4_2_4_unbiased (j k : Fin 4) : normSq (dot4 (mub4_2 j) (mub4_4 k)) = 4 := by
  revert j k; decide

theorem mub4_3_4_unbiased (j k : Fin 4) : normSq (dot4 (mub4_3 j) (mub4_4 k)) = 4 := by
  revert j k; decide

end GaussInt

end P208cCommutatorTomography
