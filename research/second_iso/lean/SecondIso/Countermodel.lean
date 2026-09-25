import SecondIso.Check

/-!
# Countermodels for the three stakes that are not uniform

This file is this rung's own object.  `Transport.lean` and
`Trajectory.lean` prove that under a UNIFORM stake carrying a demand is
invariant under the implemented isomorphism, and that class-matched
histories have the same first counts.  Here the three declared stakes
that are not uniform are shown to escape both statements, by executable
countermodels closed by kernel computation over concrete regimes.

The three stakes are declared here with the labels the sibling Python
rules of the two-sided commitment tree give, on every ordered pair of
distinct indices: `parity` labels a pair same when its indices differ by
an even number and apart otherwise; `residueThree` labels it same when
they differ by a multiple of three and apart otherwise; `chain` labels
it apart when they differ by one and free otherwise.  They are this
rung's Lean declarations; that they are the Python rules is checked by
`test_iso.py`, which evaluates both on every pair of the rectangle's
index range, and is not proved here.

Every regime below admits only forms of arity one, so the sound checks
of `Check.lean` close every honour and dishonour statement; nothing here
decides collapse in general.

AuthorityEffect: None.
-/

namespace SecondIso
namespace Countermodel

open SecondIso.Sealed
open SecondIso.Inherited
open SecondIso.IndexSlice
open SecondIso.Transport
open SecondIso.Trajectory
open SecondIso.Check

/-! ## 1. The three stakes -/

/-- Same at an even difference, apart at an odd one. -/
def parity : Stake where
  label i j := if i = j then Label.free
    else if (i + j) % 2 = 0 then Label.same else Label.apart
  diag i := by simp

/-- Same at a difference divisible by three, apart otherwise. -/
def residueThree : Stake where
  label i j := if i = j then Label.free
    else if (max i j - min i j) % 3 = 0 then Label.same else Label.apart
  diag i := by simp

/-- Apart at a difference of one, free otherwise. -/
def chain : Stake where
  label i j := if i + 1 = j ∨ j + 1 = i then Label.apart else Label.free
  diag i := if_neg (fun h => h.elim (Nat.succ_ne_self i) (Nat.succ_ne_self i))

/-! ## 2. The regimes exhibited -/

/-- The swap of the first two indices, as the sealed `swap01`. -/
abbrev sw : Nat → Nat := swap01

/-- Three data, one form of arity one, the first datum marked.  The
second and third data are collapsed. -/
def pr0 : Regime := ⟨3, [1], [(0, [0])], [], []⟩

/-- Three data, one form of arity one, the second datum marked.  The
first and third data are collapsed. -/
def pr1 : Regime := ⟨3, [1], [(0, [1])], [], []⟩

/-- Four data, two forms of arity one, the first and third data marked by
different forms.  The second and fourth data are collapsed. -/
def rr0 : Regime := ⟨4, [1, 1], [(0, [0]), (1, [2])], [], []⟩

/-- Four data, two forms of arity one, the second and third data marked by
different forms.  The first and fourth data are collapsed. -/
def rr1 : Regime := ⟨4, [1, 1], [(0, [1]), (1, [2])], [], []⟩

/-- The swap of the first two data is an isomorphism `pr0 ≅ pr1`. -/
def isoPr : Iso pr0 pr1 := isoOf (dm := sw) (dv := sw) (fm := id) (fv := id)
  (by decide)

/-- The swap of the first two data is an isomorphism `rr0 ≅ rr1`. -/
def isoRr : Iso rr0 rr1 := isoOf (dm := sw) (dv := sw) (fm := id) (fv := id)
  (by decide)

/-! ## 3. The class-matched histories exhibited -/

/-- Two forms of arity one; a datum marked by the first form; a second
datum marked by the second form; the uniform rule on the FIRST form, which
erases the first datum's mark; a third datum. -/
def P1 : List Event :=
  [.admitForm 1, .admitForm 1, .admitDatum, .admitInst 0 [0], .admitDatum,
   .admitInst 1 [1], .admitRuleAll 0, .admitDatum]

/-- The same, with the uniform rule on the SECOND form. -/
def P2 : List Event :=
  [.admitForm 1, .admitForm 1, .admitDatum, .admitInst 0 [0], .admitDatum,
   .admitInst 1 [1], .admitRuleAll 1, .admitDatum]

/-- Three forms of arity one; three data, each marked by its own form; the
uniform rule on the FIRST form; a fourth datum. -/
def Q1 : List Event :=
  [.admitForm 1, .admitForm 1, .admitForm 1, .admitDatum, .admitInst 0 [0],
   .admitDatum, .admitInst 1 [1], .admitDatum, .admitInst 2 [2],
   .admitRuleAll 0, .admitDatum]

/-- The same, with the uniform rule on the SECOND form. -/
def Q2 : List Event :=
  [.admitForm 1, .admitForm 1, .admitForm 1, .admitDatum, .admitInst 0 [0],
   .admitDatum, .admitInst 1 [1], .admitDatum, .admitInst 2 [2],
   .admitRuleAll 1, .admitDatum]

/-! ## 4. The three stakes are not uniform -/

/-- **parity_not_uniform.**  AT THE LEVEL OF A DEFINITION: two pairs of
distinct indices with two labels, by kernel computation. -/
theorem parity_not_uniform : ¬ Uniform parity := by
  intro ⟨l, hl⟩
  have h : parity.label 0 1 = parity.label 0 2 :=
    (hl 0 1 (by decide)).trans (hl 0 2 (by decide)).symm
  exact absurd h (by decide)

/-- **residue_not_uniform.**  AT THE LEVEL OF A DEFINITION. -/
theorem residue_not_uniform : ¬ Uniform residueThree := by
  intro ⟨l, hl⟩
  have h : residueThree.label 0 1 = residueThree.label 0 3 :=
    (hl 0 1 (by decide)).trans (hl 0 3 (by decide)).symm
  exact absurd h (by decide)

/-- **chain_not_uniform.**  AT THE LEVEL OF A DEFINITION. -/
theorem chain_not_uniform : ¬ Uniform chain := by
  intro ⟨l, hl⟩
  have h : chain.label 0 1 = chain.label 0 2 :=
    (hl 0 1 (by decide)).trans (hl 0 2 (by decide)).symm
  exact absurd h (by decide)

/-! ## 5. Two isomorphic regimes, one carrying a demand and one none -/

/-- **demand_not_class_invariant.**  In the sealed grammar reconstructed
here, extended by each of the three declared stakes that are not
uniform: two regimes the sealed isomorphism relates, one carrying a
demand and the other none.  The pair `pr0`, `pr1` serves `parity` and
`chain`; the pair `rr0`, `rr1` serves `residueThree`.
AT THE LEVEL OF A DEFINITION: an assembly of the sound checks, each
closed by kernel computation. -/
theorem demand_not_class_invariant :
    (Nonempty (Iso pr0 pr1) ∧ HasDemand parity pr0 ∧ ¬ HasDemand parity pr1) ∧
    (Nonempty (Iso pr0 pr1) ∧ HasDemand chain pr0 ∧ ¬ HasDemand chain pr1) ∧
    (Nonempty (Iso rr0 rr1) ∧ HasDemand residueThree rr0 ∧
      ¬ HasDemand residueThree rr1) :=
  ⟨⟨⟨isoPr⟩, demandCheck_sound _ _ (by decide), noDemandCheck_sound _ _ (by decide)⟩,
   ⟨⟨isoPr⟩, demandCheck_sound _ _ (by decide), noDemandCheck_sound _ _ (by decide)⟩,
   ⟨⟨isoRr⟩, demandCheck_sound _ _ (by decide), noDemandCheck_sound _ _ (by decide)⟩⟩

/-! ## 6. Two class-matched histories with different first counts -/

/-- **matched_P.**  `P1` and `P2` are class-matched from the empty base:
the prefixes are identical up to the count six, and from the count seven
on the swap of the first two data and of the two forms relates them. -/
theorem matched_P : Matched genesis P1 genesis P2 := by
  intro k
  by_cases hk : k ≤ 6
  · have hcase : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 6 := by
      omega
    rcases hcase with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      exact related_of_relBy (dm := id) (dv := id) (fm := id) (fv := id)
        (by decide)
  · by_cases h7 : k = 7
    · subst h7
      exact related_of_relBy (dm := sw) (dv := sw) (fm := sw) (fv := sw)
        (by decide)
    · have h1 : stateAt P1 genesis k = stateAt P1 genesis 8 := by
        unfold stateAt
        rw [List.take_of_length_le (by simp [P1]; omega),
          List.take_of_length_le (by simp [P1])]
      have h2 : stateAt P2 genesis k = stateAt P2 genesis 8 := by
        unfold stateAt
        rw [List.take_of_length_le (by simp [P2]; omega),
          List.take_of_length_le (by simp [P2])]
      rw [h1, h2]
      exact related_of_relBy (dm := sw) (dv := sw) (fm := sw) (fv := sw)
        (by decide)

/-- **matched_Q.**  `Q1` and `Q2` are class-matched from the empty base:
identical up to the count nine, and from the count ten on the swap of the
first two data and of the first two forms relates them. -/
theorem matched_Q : Matched genesis Q1 genesis Q2 := by
  intro k
  by_cases hk : k ≤ 9
  · have hcase : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 6 ∨
        k = 7 ∨ k = 8 ∨ k = 9 := by
      omega
    rcases hcase with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      exact related_of_relBy (dm := id) (dv := id) (fm := id) (fv := id)
        (by decide)
  · by_cases h10 : k = 10
    · subst h10
      exact related_of_relBy (dm := sw) (dv := sw) (fm := sw) (fv := sw)
        (by decide)
    · have h1 : stateAt Q1 genesis k = stateAt Q1 genesis 11 := by
        unfold stateAt
        rw [List.take_of_length_le (by simp [Q1]; omega),
          List.take_of_length_le (by simp [Q1])]
      have h2 : stateAt Q2 genesis k = stateAt Q2 genesis 11 := by
        unfold stateAt
        rw [List.take_of_length_le (by simp [Q2]; omega),
          List.take_of_length_le (by simp [Q2])]
      rw [h1, h2]
      exact related_of_relBy (dm := sw) (dv := sw) (fm := sw) (fv := sw)
        (by decide)

/-- **index_P2_parity.**  Under `parity`, the first count of `P2` from the
empty base is eight. -/
theorem index_P2_parity : IsFirstDemand parity genesis P2 8 :=
  index_of_check _ _ _ _ (by decide) (by decide)

/-- **quiet_P1_parity.**  Under `parity`, `P1` has no first count at all
from the empty base. -/
theorem quiet_P1_parity : ∀ k, ¬ IsFirstDemand parity genesis P1 k :=
  no_index_of_check _ _ _ (by decide)

/-- **index_P2_chain.**  Under `chain`, the first count of `P2` from the
empty base is eight. -/
theorem index_P2_chain : IsFirstDemand chain genesis P2 8 :=
  index_of_check _ _ _ _ (by decide) (by decide)

/-- **quiet_P1_chain.**  Under `chain`, `P1` has no first count at all
from the empty base. -/
theorem quiet_P1_chain : ∀ k, ¬ IsFirstDemand chain genesis P1 k :=
  no_index_of_check _ _ _ (by decide)

/-- **index_Q2_residue.**  Under `residueThree`, the first count of `Q2`
from the empty base is eleven. -/
theorem index_Q2_residue : IsFirstDemand residueThree genesis Q2 11 :=
  index_of_check _ _ _ _ (by decide) (by decide)

/-- **quiet_Q1_residue.**  Under `residueThree`, `Q1` has no first count
at all from the empty base. -/
theorem quiet_Q1_residue : ∀ k, ¬ IsFirstDemand residueThree genesis Q1 k :=
  no_index_of_check _ _ _ (by decide)

/-- **first_count_not_trajectory_invariant.**  In the sealed grammar
reconstructed here, extended by each of the three declared stakes that
are not uniform: two class-matched histories from the empty base, one
with a first count and one with none.
AT THE LEVEL OF A DEFINITION: a conjunction, each clause applied by
name. -/
theorem first_count_not_trajectory_invariant :
    Matched genesis P1 genesis P2 ∧
    (∀ k, ¬ IsFirstDemand parity genesis P1 k) ∧ IsFirstDemand parity genesis P2 8 ∧
    (∀ k, ¬ IsFirstDemand chain genesis P1 k) ∧ IsFirstDemand chain genesis P2 8 ∧
    Matched genesis Q1 genesis Q2 ∧
    (∀ k, ¬ IsFirstDemand residueThree genesis Q1 k) ∧
      IsFirstDemand residueThree genesis Q2 11 :=
  ⟨matched_P, quiet_P1_parity, index_P2_parity, quiet_P1_chain, index_P2_chain,
   matched_Q, quiet_Q1_residue, index_Q2_residue⟩

/-! ## 7. The rung's statement, in one place -/

/-- **iso_index.**  The first-demand index up to the implemented
isomorphism, over the sealed grammar reconstructed here extended by a
declared two-sided stake:

1. under a uniform stake, carrying a demand is invariant under the
   isomorphism, at every pair of regimes it relates;
2. under a uniform stake, class-matched histories have the same first
   counts;
3. the three declared stakes that are not uniform escape both, by
   exhibited countermodels;
4. renaming the token every supply carries moves no first count.

AT THE LEVEL OF A DEFINITION: a conjunction, each clause applied by
name. -/
theorem iso_index :
    (∀ S : Stake, Uniform S → ∀ r s : Regime, Iso r s →
      (HasDemand S r ↔ HasDemand S s)) ∧
    (∀ S : Stake, Uniform S → ∀ (base base' : Regime) (h h' : List Event),
      Matched base h base' h' → ∀ k,
        (IsFirstDemand S base h k ↔ IsFirstDemand S base' h' k)) ∧
    ((Nonempty (Iso pr0 pr1) ∧ HasDemand parity pr0 ∧ ¬ HasDemand parity pr1) ∧
     (Nonempty (Iso pr0 pr1) ∧ HasDemand chain pr0 ∧ ¬ HasDemand chain pr1) ∧
     (Nonempty (Iso rr0 rr1) ∧ HasDemand residueThree rr0 ∧
       ¬ HasDemand residueThree rr1)) ∧
    (Matched genesis P1 genesis P2 ∧
      (∀ k, ¬ IsFirstDemand parity genesis P1 k) ∧ IsFirstDemand parity genesis P2 8 ∧
      (∀ k, ¬ IsFirstDemand chain genesis P1 k) ∧ IsFirstDemand chain genesis P2 8 ∧
      Matched genesis Q1 genesis Q2 ∧
      (∀ k, ¬ IsFirstDemand residueThree genesis Q1 k) ∧
        IsFirstDemand residueThree genesis Q2 11) ∧
    (∀ (S : Stake) (g : Nat → Nat) (base : Regime) (h : List Event) (k : Nat),
      IsFirstDemand S base (h.map (renameSupply g)) k ↔ IsFirstDemand S base h k) :=
  ⟨fun _ hu _ _ h => hasDemand_iff_of_uniform hu h,
   fun _ hu _ _ _ _ hm k => first_demand_matched_of_uniform hu hm k,
   demand_not_class_invariant,
   first_count_not_trajectory_invariant,
   first_demand_renameSupply⟩

end Countermodel
end SecondIso
