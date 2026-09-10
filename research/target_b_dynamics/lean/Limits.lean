/-!
# Limits: compatible finite observations and the thread space

An observation at scale `n` is a word of length `n` over a finite carrier of
size `c` — a `Stage c n`. The bonding map from scale `n + 1` to scale `n`
forgets the last entry. A family of observations is **compatible** when the
bonding holds at *every* scale (`Compatible`), and the **thread space** is
the set of compatible families (`Thread`).

Key constructive results:
- Construction and bijection with sequence space (`toSeq_ofSeq`, `ofSeq_toSeq`).
- Eventual agreement is not compatibility (`eventual_not_compatible`).
- Cofinal rescaling on even scales (`restrictEven_eq`, `thread_even`).
- Non-locality of shift (`shift_not_local`).
- Dyadic twin separation at scale 1 (`twins_differ_at_scale_one`), refusing
  continuum or interval completions without an explicit adapter quotient.

Axioms: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
AuthorityEffect: None.
-/

namespace Limits

/-! ## 1. Stages, bonding, compatibility -/

/-- An observation at scale `n`: a word of length `n` over a carrier of size `c`. -/
abbrev Stage (c n : Nat) := Fin n → Fin c

/-- The bonding map: forget the last entry. -/
def bond (c n : Nat) (t : Stage c (n + 1)) : Stage c n :=
  fun i => t ⟨i.val, Nat.lt_succ_of_lt i.isLt⟩

/-- Compatibility at **every** scale. -/
def Compatible (c : Nat) (t : (n : Nat) → Stage c n) : Prop :=
  ∀ n, bond c n (t (n + 1)) = t n

/-- The thread space: the compatible families. -/
abbrev Thread (c : Nat) := { t : (n : Nat) → Stage c n // Compatible c t }

/-! ## 2. Construction: the thread space is the sequence space -/

/-- A sequence gives a compatible family: its prefixes. -/
def ofSeq (c : Nat) (s : Nat → Fin c) : Thread c :=
  ⟨fun _ i => s i.val, fun _ => rfl⟩

/-- A compatible family gives a sequence: read entry `i` at scale `i + 1`. -/
def toSeq (c : Nat) (t : Thread c) : Nat → Fin c :=
  fun i => t.val (i + 1) ⟨i, Nat.lt_succ_self i⟩

theorem toSeq_ofSeq (c : Nat) (s : Nat → Fin c) : toSeq c (ofSeq c s) = s := rfl

/-- Two scales of a thread agree on their common entries. -/
theorem stable (c : Nat) (t : Thread c) :
    ∀ (n m : Nat), m ≤ n → ∀ (i : Nat) (hm : i < m) (hn : i < n),
      t.val n ⟨i, hn⟩ = t.val m ⟨i, hm⟩
  | 0, _, _, i, _, hn => absurd hn (Nat.not_lt_zero i)
  | n + 1, m, hmn, i, hm, hn => by
      rcases Nat.eq_or_lt_of_le hmn with rfl | hlt
      · rfl
      · have hi : i < n := Nat.lt_of_lt_of_le hm (Nat.le_of_lt_succ hlt)
        have h1 : t.val (n + 1) ⟨i, hn⟩ = bond c n (t.val (n + 1)) ⟨i, hi⟩ := rfl
        rw [h1, t.property n]
        exact stable c t n m (Nat.le_of_lt_succ hlt) i hm hi

/-- Inverse bijection between sequence space and thread space. -/
theorem ofSeq_toSeq (c : Nat) (t : Thread c) : ofSeq c (toSeq c t) = t := by
  apply Subtype.ext
  funext n i
  show t.val (i.val + 1) ⟨i.val, Nat.lt_succ_self _⟩ = t.val n i
  rcases Nat.lt_or_ge n (i.val + 1) with h | h
  · exact absurd i.isLt (Nat.not_lt.mpr (Nat.le_of_lt_succ h))
  · exact (stable c t n (i.val + 1) h i.val (Nat.lt_succ_self _) i.isLt).symm

/-! ## 3. Eventual agreement is not compatibility -/

/-- A family over two letters constant 0 except at scale 1, where it reads 1. -/
def eventual : (n : Nat) → Stage 2 n
  | 1 => fun _ => ⟨1, by decide⟩
  | _ => fun _ => ⟨0, by decide⟩

/-- From scale 2 on, the family agrees with its bonding. -/
theorem eventual_agrees (n : Nat) (h : 2 ≤ n) : bond 2 n (eventual (n + 1)) = eventual n := by
  obtain ⟨k, rfl⟩ : ∃ k, n = k + 2 := ⟨n - 2, by omega⟩
  rfl

/-- Eventual agreement is not compatibility: bonding fails at scale 1. -/
theorem eventual_not_compatible : ¬ Compatible 2 eventual := by
  intro h
  have h1 := congrFun (h 1) ⟨0, Nat.zero_lt_one⟩
  have h2 : (⟨0, by decide⟩ : Fin 2) = ⟨1, by decide⟩ := h1
  have h3 : (0 : Nat) = 1 := congrArg Fin.val h2
  cases h3

/-! ## 4. Cofinal rescaling: the even scales -/

/-- The bonding of the even subsystem: forget the last two entries. -/
def ebond (c n : Nat) (t : Stage c (2 * (n + 1))) : Stage c (2 * n) :=
  fun i => t ⟨i.val, Nat.lt_of_lt_of_le i.isLt (by omega)⟩

def ECompatible (c : Nat) (t : (n : Nat) → Stage c (2 * n)) : Prop :=
  ∀ n, ebond c n (t (n + 1)) = t n

abbrev EThread (c : Nat) := { t : (n : Nat) → Stage c (2 * n) // ECompatible c t }

def eofSeq (c : Nat) (s : Nat → Fin c) : EThread c :=
  ⟨fun _ i => s i.val, fun _ => rfl⟩

def etoSeq (c : Nat) (t : EThread c) : Nat → Fin c :=
  fun i => t.val (i + 1) ⟨i, by omega⟩

theorem etoSeq_eofSeq (c : Nat) (s : Nat → Fin c) : etoSeq c (eofSeq c s) = s := rfl

theorem estable (c : Nat) (t : EThread c) :
    ∀ (n m : Nat), m ≤ n → ∀ (i : Nat) (hm : i < 2 * m) (hn : i < 2 * n),
      t.val n ⟨i, hn⟩ = t.val m ⟨i, hm⟩
  | 0, _, _, i, _, hn => absurd hn (by omega)
  | n + 1, m, hmn, i, hm, hn => by
      rcases Nat.eq_or_lt_of_le hmn with rfl | hlt
      · rfl
      · have hi : i < 2 * n := by
          have := Nat.le_of_lt_succ hlt
          omega
        have h1 : t.val (n + 1) ⟨i, hn⟩ = ebond c n (t.val (n + 1)) ⟨i, hi⟩ := rfl
        rw [h1, t.property n]
        exact estable c t n m (Nat.le_of_lt_succ hlt) i hm hi

theorem eofSeq_etoSeq (c : Nat) (t : EThread c) : eofSeq c (etoSeq c t) = t := by
  apply Subtype.ext
  funext n i
  show t.val (i.val + 1) ⟨i.val, by omega⟩ = t.val n i
  rcases Nat.lt_or_ge n (i.val + 1) with h | h
  · exact estable c t (i.val + 1) n (Nat.le_of_lt h) i.val i.isLt (by omega)
  · exact (estable c t n (i.val + 1) h i.val (by omega) i.isLt).symm

/-- Restriction of a thread to the even scales is an even thread. -/
def restrictEven (c : Nat) (t : Thread c) : EThread c :=
  ⟨fun n => t.val (2 * n), fun n => by
    funext i
    exact stable c t (2 * (n + 1)) (2 * n) (by omega) i.val i.isLt (by omega)⟩

theorem restrictEven_eq (c : Nat) (t : Thread c) : restrictEven c t = eofSeq c (toSeq c t) := by
  apply Subtype.ext
  funext n i
  show t.val (2 * n) i = t.val (i.val + 1) ⟨i.val, Nat.lt_succ_self _⟩
  exact stable c t (2 * n) (i.val + 1) i.isLt i.val (Nat.lt_succ_self _) i.isLt

theorem thread_even (c : Nat) (t : Thread c) : ofSeq c (etoSeq c (eofSeq c (toSeq c t))) = t := by
  rw [etoSeq_eofSeq, ofSeq_toSeq]

theorem thread_restrictEven (c : Nat) (t : Thread c) :
    ofSeq c (etoSeq c (restrictEven c t)) = t := by
  rw [restrictEven_eq, etoSeq_eofSeq, ofSeq_toSeq]

theorem even_thread (c : Nat) (e : EThread c) : eofSeq c (toSeq c (ofSeq c (etoSeq c e))) = e := by
  rw [toSeq_ofSeq, eofSeq_etoSeq]

/-! ## 5. An observation map that cannot commute -/

/-- Shifting a word by one entry is not a function of its two-entry prefix:
two words with the same prefix [0, 1] shift to [1, 2] and [1, 0]. -/
theorem shift_not_local :
    ¬ ∃ φ : List Nat → List Nat, ∀ t : List Nat, (t.drop 1).take 2 = φ (t.take 2) := by
  rintro ⟨φ, h⟩
  have h1 : ([1, 2] : List Nat) = φ [0, 1] := h [0, 1, 2]
  have h2 : ([1, 0] : List Nat) = φ [0, 1] := h [0, 1, 0]
  have h3 : ([1, 2] : List Nat) = [1, 0] := h1.trans h2.symm
  cases h3

/-! ## 6. Two sequences that an interval reading would identify -/

def twinLo : Nat → Fin 2 := fun i => if i = 0 then ⟨0, by decide⟩ else ⟨1, by decide⟩
def twinHi : Nat → Fin 2 := fun i => if i = 0 then ⟨1, by decide⟩ else ⟨0, by decide⟩

theorem twins_differ_at_zero : twinLo 0 ≠ twinHi 0 := by decide

theorem twins_differ_at_scale_one :
    (ofSeq 2 twinLo).val 1 ≠ (ofSeq 2 twinHi).val 1 := by
  intro h
  have h0 : (ofSeq 2 twinLo).val 1 ⟨0, by decide⟩ = (ofSeq 2 twinHi).val 1 ⟨0, by decide⟩ := by
    rw [h]
  exact twins_differ_at_zero h0

theorem twins_are_two_threads : ofSeq 2 twinLo ≠ ofSeq 2 twinHi := by
  intro h
  exact twins_differ_at_scale_one (by rw [h])

theorem threads_are_sequences (s t : Nat → Fin 2) (h : ofSeq 2 s = ofSeq 2 t) : s = t := by
  have h1 : toSeq 2 (ofSeq 2 s) = toSeq 2 (ofSeq 2 t) := by rw [h]
  rw [toSeq_ofSeq, toSeq_ofSeq] at h1
  exact h1

end Limits
