/-!
# Limits: compatible finite observations and the thread space

An observation at scale `n` is a word of length `n` over a finite carrier of
size `c` — a `Stage c n`.  The bonding map from scale `n + 1` to scale `n`
forgets the last entry.  A family of observations is **compatible** when the
bonding holds at *every* scale (`Compatible`), and the **thread space** is
the set of compatible families (`Thread`).

Three facts about that space, all constructive:

* **Construction, and a bijection with the sequence space.**  A sequence
  `ℕ → Fin c` gives a compatible family (`ofSeq`), a compatible family gives
  a sequence (`toSeq`: read entry `i` at scale `i + 1`), and the two are
  inverse (`toSeq_ofSeq`, `ofSeq_toSeq`).  The thread space *is* the sequence
  space in that sense — a bijection, not a mediating-map statement: no cone
  over an arbitrary object is quantified, and nothing here claims the limit's
  universal property;
  no choice or compactness principle is used, because the bonding is
  restriction and the family is assembled explicitly.  This is the contrast
  with the sealed `wit_no_infinite`, where arbitrary finite witnesses need
  not fit together: here they fit by construction.
* **Eventual agreement is not compatibility.**  A family that agrees from
  scale 2 on and disagrees at scale 1 is not compatible
  (`eventual_not_compatible`, `eventual_agrees`).
* **Cofinal rescaling.**  The subsystem of even scales has the same thread
  space, through the same sequences (`thread_even`, `even_thread`), and the
  map that carries it is the restriction of a thread to the even scales
  (`restrictEven`, `restrictEven_eq`).

And one negative about observation maps: shifting a word by one is not a
function of its prefix — the entry beyond the observed boundary is needed
(`shift_not_local`).

Topology, declared and not proved: with the discrete topology on each finite
stage and the product topology on families, the thread space is totally
disconnected.  It is not an interval and not a circle, and none is claimed.

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

/-- **Inverse.**  A compatible family is the family of prefixes of its
sequence: with `toSeq_ofSeq`, the thread space is the sequence space.  This
is a bijection and nothing more: no cone over an arbitrary object is
quantified, and the limit's universal property is not claimed. -/
theorem ofSeq_toSeq (c : Nat) (t : Thread c) : ofSeq c (toSeq c t) = t := by
  apply Subtype.ext
  funext n i
  show t.val (i.val + 1) ⟨i.val, Nat.lt_succ_self _⟩ = t.val n i
  rcases Nat.lt_or_ge n (i.val + 1) with h | h
  · exact absurd i.isLt (Nat.not_lt.mpr (Nat.le_of_lt_succ h))
  · exact (stable c t n (i.val + 1) h i.val (Nat.lt_succ_self _) i.isLt).symm

/-! ## 3. Eventual agreement is not compatibility -/

/-- A family over two letters that is constant `0` except at scale 1, where
it reads `1`. -/
def eventual : (n : Nat) → Stage 2 n
  | 1 => fun _ => ⟨1, by decide⟩
  | _ => fun _ => ⟨0, by decide⟩

/-- From scale 2 on, the family agrees with its bonding. -/
theorem eventual_agrees (n : Nat) (h : 2 ≤ n) : bond 2 n (eventual (n + 1)) = eventual n := by
  obtain ⟨k, rfl⟩ : ∃ k, n = k + 2 := ⟨n - 2, by omega⟩
  rfl

/-- And it is not compatible: the bonding fails at scale 1. -/
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

/-- The restriction of a thread to the even scales is a thread of the even
scales: the entries agree wherever two scales overlap (`stable`). -/
def restrictEven (c : Nat) (t : Thread c) : EThread c :=
  ⟨fun n => t.val (2 * n), fun n => by
    funext i
    exact stable c t (2 * (n + 1)) (2 * n) (by omega) i.val i.isLt (by omega)⟩

/-- **The rescaling map is the restriction.**  Reading a thread at the even
scales and reading its sequence at the even scales are the same thread, so
the correspondence below is carried by restriction and not only by the
sequences. -/
theorem restrictEven_eq (c : Nat) (t : Thread c) : restrictEven c t = eofSeq c (toSeq c t) := by
  apply Subtype.ext
  funext n i
  show t.val (2 * n) i = t.val (i.val + 1) ⟨i.val, Nat.lt_succ_self _⟩
  exact stable c t (2 * n) (i.val + 1) i.isLt i.val (Nat.lt_succ_self _) i.isLt

/-- **Invariance under the cofinal rescaling**: a thread of all scales and a
thread of the even scales are the same sequence, both ways.  With
`restrictEven_eq` the forward map is the restriction. -/
theorem thread_even (c : Nat) (t : Thread c) : ofSeq c (etoSeq c (eofSeq c (toSeq c t))) = t := by
  rw [etoSeq_eofSeq, ofSeq_toSeq]

/-- The same, with the restriction in place of the sequence detour. -/
theorem thread_restrictEven (c : Nat) (t : Thread c) :
    ofSeq c (etoSeq c (restrictEven c t)) = t := by
  rw [restrictEven_eq, etoSeq_eofSeq, ofSeq_toSeq]

theorem even_thread (c : Nat) (e : EThread c) : eofSeq c (toSeq c (ofSeq c (etoSeq c e))) = e := by
  rw [toSeq_ofSeq, eofSeq_etoSeq]

/-! ## 5. An observation map that cannot commute -/

/-- Shifting a word by one entry is not a function of its two-entry prefix:
two words with the same prefix `[0, 1]` shift to `[1, 2]` and `[1, 0]`.  The
entry beyond the observed boundary would have to be supplied. -/
theorem shift_not_local :
    ¬ ∃ φ : List Nat → List Nat, ∀ t : List Nat, (t.drop 1).take 2 = φ (t.take 2) := by
  rintro ⟨φ, h⟩
  have h1 : ([1, 2] : List Nat) = φ [0, 1] := h [0, 1, 2]
  have h2 : ([1, 0] : List Nat) = φ [0, 1] := h [0, 1, 0]
  have h3 : ([1, 2] : List Nat) = [1, 0] := h1.trans h2.symm
  cases h3

end Limits

#print axioms Limits.toSeq_ofSeq
#print axioms Limits.stable
#print axioms Limits.ofSeq_toSeq
#print axioms Limits.eventual_agrees
#print axioms Limits.eventual_not_compatible
#print axioms Limits.etoSeq_eofSeq
#print axioms Limits.estable
#print axioms Limits.eofSeq_etoSeq
#print axioms Limits.restrictEven_eq
#print axioms Limits.thread_even
#print axioms Limits.thread_restrictEven
#print axioms Limits.even_thread
#print axioms Limits.shift_not_local
