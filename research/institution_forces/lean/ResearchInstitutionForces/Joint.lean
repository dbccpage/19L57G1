import ResearchTwoTheorems.Institution
import ResearchActorInstitution.Institution

/-!
# The joint presentation, and separation redundancy

AuthorityEffect: None.  Outside the seal.  Consumes the sealed `Compression`
namespace, `research/two_theorems` and `research/actor_institution`
read-only; every consumed name is used as merged.

* `knows_family_iff_joint` (L0): a family `F` knows `q` on `D` exactly when
  the one-member family of its joint presentation `pQ D F` does.  So the
  reading "an actor is a finite family of presentations" and the reading
  "an actor is one presentation" agree on knowledge, once the family is
  read through its joint presentation.  The information side is the
  two-theorems `institution_is_actor`, not repeated here.
* `redundancy Q x y`: how many members of the list `Q` tell `x` from `y`.
  It is a count over list positions.  A member that occurs twice is two
  seats and counts twice (`duplicate_counts_twice`), while knowledge does
  not see the duplication at all (`duplicate_knows_inert`).
* `knows_iff_redundancy`: knowledge is "every pair the question separates
  has at least one separating seat".  This is the base case of the
  robustness count in `Robust`.

Every carrier is a finite list; `Nat → Nat` and the quantifiers over it are
the metatheory's.
-/

namespace ResearchInstitutionForces
namespace Joint

open Compression ResearchTwoTheorems.Institution

/-- **L0.**  A family knows `q` exactly when its joint presentation does. -/
theorem knows_family_iff_joint (D : List Nat) (F : Institution) (q : Nat → Nat) :
    Knows D F q ↔ Knows D [pQ D F] q := by
  rw [knows_iff_determined, knows_iff_determined]
  constructor
  · intro h x hx y hy hs
    exact h x hx y hy ((pQ_exact D F x hx y hy).mp
      ((ResearchActorInstitution.Inst.sigEq_single _ x y).mp hs))
  · intro h x hx y hy hs
    exact h x hx y hy ((ResearchActorInstitution.Inst.sigEq_single _ x y).mpr
      ((pQ_exact D F x hx y hy).mpr hs))

/-- The joint presentation of the joint presentation separates as the
family does: reading a family through `pQ` twice changes nothing. -/
theorem knows_joint_idem (D : List Nat) (F : Institution) (q : Nat → Nat) :
    Knows D [pQ D [pQ D F]] q ↔ Knows D F q := by
  rw [← knows_family_iff_joint D [pQ D F] q, ← knows_family_iff_joint D F q]

/-! ## Separation redundancy -/

/-- One seat's contribution: `1` when the member tells `x` from `y`. -/
def sepCount (m : Nat → Nat) (x y : Nat) : Nat := if m x = m y then 0 else 1

/-- The number of seats of `Q` that tell `x` from `y`, counted by position. -/
def redundancy : Institution → Nat → Nat → Nat
  | [], _, _ => 0
  | m :: Q, x, y => sepCount m x y + redundancy Q x y

theorem sepCount_le_one (m : Nat → Nat) (x y : Nat) : sepCount m x y ≤ 1 := by
  unfold sepCount
  cases Nat.decEq (m x) (m y) with
  | isTrue h => rw [if_pos h]; exact Nat.zero_le 1
  | isFalse h => rw [if_neg h]; exact Nat.le_refl 1

theorem sepCount_eq_zero {m : Nat → Nat} {x y : Nat} (h : m x = m y) :
    sepCount m x y = 0 := by
  unfold sepCount; rw [if_pos h]

theorem sepCount_eq_one {m : Nat → Nat} {x y : Nat} (h : m x ≠ m y) :
    sepCount m x y = 1 := by
  unfold sepCount; rw [if_neg h]

theorem redundancy_nil (x y : Nat) : redundancy [] x y = 0 := rfl

theorem redundancy_cons (m : Nat → Nat) (Q : Institution) (x y : Nat) :
    redundancy (m :: Q) x y = sepCount m x y + redundancy Q x y := rfl

theorem redundancy_append (Q R : Institution) (x y : Nat) :
    redundancy (Q ++ R) x y = redundancy Q x y + redundancy R x y := by
  induction Q with
  | nil => rw [List.nil_append, redundancy_nil, Nat.zero_add]
  | cons m Q ih =>
    rw [List.cons_append, redundancy_cons, redundancy_cons, ih, Nat.add_assoc]

theorem redundancy_le_length (Q : Institution) (x y : Nat) :
    redundancy Q x y ≤ Q.length := by
  induction Q with
  | nil => exact Nat.le_refl 0
  | cons m Q ih =>
    rw [redundancy_cons, List.length_cons, Nat.add_comm (List.length Q) 1]
    exact Nat.add_le_add (sepCount_le_one m x y) ih

theorem redundancy_symm (Q : Institution) (x y : Nat) :
    redundancy Q x y = redundancy Q y x := by
  induction Q with
  | nil => rfl
  | cons m Q ih =>
    rw [redundancy_cons, redundancy_cons, ih]
    unfold sepCount
    cases Nat.decEq (m x) (m y) with
    | isTrue h => rw [if_pos h, if_pos h.symm]
    | isFalse h => rw [if_neg h, if_neg (fun e => h e.symm)]

/-- A pair has a separating seat exactly when some member separates it. -/
theorem redundancy_pos_iff (Q : Institution) (x y : Nat) :
    0 < redundancy Q x y ↔ ∃ m, m ∈ Q ∧ m x ≠ m y := by
  induction Q with
  | nil =>
    constructor
    · intro h; exact absurd h (Nat.lt_irrefl 0)
    · rintro ⟨m, hm, _⟩; cases hm
  | cons m Q ih =>
    rw [redundancy_cons]
    constructor
    · intro h
      cases Nat.decEq (m x) (m y) with
      | isTrue e =>
        rw [sepCount_eq_zero e, Nat.zero_add] at h
        obtain ⟨m', hm', hne⟩ := ih.mp h
        exact ⟨m', List.mem_cons_of_mem _ hm', hne⟩
      | isFalse ne => exact ⟨m, List.mem_cons_self, ne⟩
    · rintro ⟨m', hm', hne⟩
      cases hm' with
      | head =>
        rw [sepCount_eq_one hne]
        exact Nat.lt_of_lt_of_le (Nat.zero_lt_one) (Nat.le_add_right 1 _)
      | tail _ hm'' =>
        exact Nat.lt_of_lt_of_le (ih.mpr ⟨m', hm'', hne⟩) (Nat.le_add_left _ _)

theorem redundancy_pos_iff_not_sigEq (Q : Institution) (x y : Nat) :
    0 < redundancy Q x y ↔ ¬ SigEq Q x y := by
  rw [redundancy_pos_iff]
  constructor
  · rintro ⟨m, hm, hne⟩ hs
    exact hne (hs m hm)
  · intro h
    exact exists_separator_of_not_sigEq Q x y h

theorem redundancy_zero_iff_sigEq (Q : Institution) (x y : Nat) :
    redundancy Q x y = 0 ↔ SigEq Q x y := by
  constructor
  · intro h
    cases Nat.decEq (redundancy Q x y) 0 with
    | isTrue _ =>
      have hn : ¬ 0 < redundancy Q x y := by rw [h]; exact Nat.lt_irrefl 0
      intro m hm
      cases Nat.decEq (m x) (m y) with
      | isTrue e => exact e
      | isFalse ne => exact absurd ((redundancy_pos_iff Q x y).mpr ⟨m, hm, ne⟩) hn
    | isFalse ne => exact absurd h ne
  · intro hs
    cases Nat.decEq (redundancy Q x y) 0 with
    | isTrue e => exact e
    | isFalse ne =>
      exact absurd hs ((redundancy_pos_iff_not_sigEq Q x y).mp (Nat.pos_of_ne_zero ne))

/-- **Knowledge as a seat count.**  `Q` knows `q` on `D` exactly when every
pair of `D` that `q` separates has at least one separating seat. -/
theorem knows_iff_redundancy (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows D Q q ↔ ∀ x, x ∈ D → ∀ y, y ∈ D → q x ≠ q y → 0 < redundancy Q x y := by
  rw [knows_iff_determined]
  constructor
  · intro h x hx y hy hne
    exact (redundancy_pos_iff_not_sigEq Q x y).mpr (fun hs => hne (h x hx y hy hs))
  · intro h x hx y hy hs
    cases Nat.decEq (q x) (q y) with
    | isTrue e => exact e
    | isFalse ne => exact absurd hs ((redundancy_pos_iff_not_sigEq Q x y).mp (h x hx y hy ne))

/-! ## What a duplicate counts as -/

/-- A duplicated separating member is two seats: it raises the count by one. -/
theorem duplicate_counts_twice (m : Nat → Nat) (Q : Institution) {x y : Nat}
    (h : m x ≠ m y) :
    redundancy (m :: m :: Q) x y = redundancy (m :: Q) x y + 1 := by
  rw [redundancy_cons, redundancy_cons, sepCount_eq_one h,
    Nat.add_comm 1 (1 + redundancy Q x y)]

/-- Knowledge does not see the duplicate: the two families know the same. -/
theorem duplicate_knows_inert (D : List Nat) (m : Nat → Nat) (Q : Institution)
    (q : Nat → Nat) : Knows D (m :: m :: Q) q ↔ Knows D (m :: Q) q := by
  constructor
  · exact knows_mono (fun p hp => by
      rcases List.mem_cons.mp hp with h | h
      · rw [h]; exact List.mem_cons_self
      · exact h)
  · exact knows_mono (fun p hp => List.mem_cons_of_mem _ hp)

end Joint
end ResearchInstitutionForces
