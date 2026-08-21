import Derivation.PrimDiff

/-!
# Rung 3: does the orientation SIGN gap (D2 vs D2rev) resolve?

POST-SEAL extension experiment artifact.  Imports `Derivation.PrimDiff`
unmodified; read-only proof receipt via `lake env lean`.  Everything is derived
from the sealed layer; no new primitive/parameter/observation/policy/oracle is
introduced to make progress (the symmetry-breaking observable at the end is
*named as the obstruction*, not imported to advance).

## The question

Rung 2 resolved the rung-1 tie (`D2` vs `S2`) to an oriented `D2`, because `D2`
and `S2` are genuinely non-isomorphic (`D2_not_pointed_iso_S2`): an
isomorphism-invariant observable (the automorphism-group asymmetry / observer
existence) separates them.  The residual at rung 2 was the orientation SIGN,
`D2` vs `D2rev`.  Does rung 3 resolve it by a rung-2 observable, or must the
vocabulary grow?

## The finding

`D2` and `D2rev` **are isomorphic** — the carrier swap `Bool.not` carries one to
the other (`D2rev_iso_D2`).  Therefore **every isomorphism-invariant observable
assigns them the same value** (`sign_gap_invisible_to_invariants`); in
particular the rung-2 discriminator does (`Diff2_D2_D2rev_empty`), so the rung-3
difference under it is EMPTY.  The sign gap does NOT resolve from below.  It CAN
be separated — but only by a NON-invariant, symmetry-breaking observable that
names a carrier point (`readsFwd`, `readsFwd_separates`, `readsFwd_not_invariant`).
Admitting such a name is a vocabulary expansion — a priced import.  So the tower
is NOT freely +1-resolvable here: the vocabulary must grow at rung 3, for a
reason distinct from the multiplicity rung (isomorphism-blindness, not
truncation).  This is the sealed S4 fact — "the output labels remain externally
interchangeable" — shown to obstruct continuation one rung up.
-/

namespace PrimDiff
namespace Rung3

/-! ## The rung-2 observer machinery (self-contained copy of the S4 notion) -/

def IsAuto (r : Bool → Bool → Prop) (g : Bool → Bool) : Prop :=
  ∀ x y, r x y ↔ r (g x) (g y)

def HasInvSepClassifier (r : Bool → Bool → Prop) : Prop :=
  ∃ κ : Bool → Bool, κ false ≠ κ true ∧ ∀ g, IsAuto r g → ∀ x, κ (g x) = κ x

def Diff2 (r r' : Bool → Bool → Prop) : Prop :=
  HasInvSepClassifier r ∧ ¬ HasInvSepClassifier r'

/-- `D2` has the invariant separating classifier (rigid, via sealed
`oriented_rigid`). -/
theorem D2_hasInvSep : HasInvSepClassifier D2 :=
  ⟨id, by decide, fun g hg x => by
    have hgid : ∀ z, g z = z := oriented_rigid g hg
    show id (g x) = id x
    simp [hgid x]⟩

/-! ## D2rev is rigid, and also has the observer -/

/-- `D2rev` is rigid: any endomap preserving-and-reflecting it is the identity
(mirror of the sealed `oriented_rigid`). -/
theorem D2rev_rigid (f : Bool → Bool)
    (hiff : ∀ x y, D2rev x y ↔ D2rev (f x) (f y)) : ∀ x, f x = x := by
  have h := (hiff true false).mp (by decide)
  intro x
  cases x with
  | false => exact h.2
  | true => exact h.1

/-- `D2rev` also carries the invariant separating classifier — it is the
oriented edge, merely with the two points renamed. -/
theorem D2rev_hasInvSep : HasInvSepClassifier D2rev :=
  ⟨id, by decide, fun g hg x => by
    have hgid : ∀ z, g z = z := D2rev_rigid g hg
    show id (g x) = id x
    simp [hgid x]⟩

/-! ## D2 and D2rev are isomorphic (the swap) -/

/-- The carrier swap `Bool.not` carries `D2` to `D2rev`: they are isomorphic as
unpointed structures.  This is the exact reason the sign is not separable by an
invariant. -/
theorem D2rev_iso_D2 : ∀ x y, D2rev x y ↔ D2 (Bool.not x) (Bool.not y) := by decide

/-! ## The sign gap is invisible to every isomorphism-invariant observable -/

/-- **Core obstruction.**  Any property invariant under the swap relabelling
assigns `D2` and `D2rev` the same value.  No isomorphism-invariant observable
separates the orientation sign. -/
theorem sign_gap_invisible_to_invariants
    (P : (Bool → Bool → Prop) → Prop)
    (hinv : ∀ r, P (fun x y => r (Bool.not x) (Bool.not y)) ↔ P r) :
    P D2 ↔ P D2rev := by
  have h : D2rev = fun x y => D2 (Bool.not x) (Bool.not y) := by
    funext x y; exact propext (D2rev_iso_D2 x y)
  rw [h]; exact (hinv D2).symm

/-- **Instance: the rung-2 discriminator fails.**  Both `D2` and `D2rev` have the
observer, so the rung-2 difference between them is EMPTY in both directions —
the sign gap is not a primitive difference under the rung-2 observable. -/
theorem Diff2_D2_D2rev_empty : ¬ Diff2 D2 D2rev ∧ ¬ Diff2 D2rev D2 :=
  ⟨fun h => h.2 D2rev_hasInvSep, fun h => h.2 D2_hasInvSep⟩

/-! ## Separation is possible only by breaking the carrier symmetry -/

/-- A NON-invariant observable that reads the source label directly: "does the
edge run `false → true`?".  It separates the sign — but only by naming a carrier
point. -/
def readsFwd (r : Bool → Bool → Prop) : Prop := r false true

/-- `readsFwd` separates the sign gap. -/
theorem readsFwd_separates : readsFwd D2 ∧ ¬ readsFwd D2rev := by
  refine ⟨?_, ?_⟩
  · show D2 false true; decide
  · show ¬ D2rev false true; decide

/-- …but `readsFwd` is NOT isomorphism-invariant: the swap changes its value, so
it is exactly the kind of symmetry-breaking (point-naming) observable that
`sign_gap_invisible_to_invariants` excludes.  Admitting it is a vocabulary
expansion — a priced import, not derivable from the sealed structure. -/
theorem readsFwd_not_invariant :
    ¬ (∀ r, readsFwd (fun x y => r (Bool.not x) (Bool.not y)) ↔ readsFwd r) := by
  intro hinv
  have h := hinv D2
  have hR : readsFwd D2 := by show D2 false true; decide
  have hL : ¬ readsFwd (fun x y => D2 (Bool.not x) (Bool.not y)) := by
    show ¬ D2 (Bool.not false) (Bool.not true); decide
  exact hL (h.mpr hR)

/-! ## Summary -/

/-- **Rung 3, summary.**  `D2` and `D2rev` are isomorphic (`D2rev_iso_D2`); every
isomorphism-invariant observable is blind to the sign
(`sign_gap_invisible_to_invariants`), the rung-2 discriminator included
(`Diff2_D2_D2rev_empty`); separation exists only via a non-invariant,
symmetry-breaking observable (`readsFwd_separates` with `readsFwd_not_invariant`).
The sign gap does not resolve from below — the vocabulary must grow at rung 3. -/
theorem rung3_sign_gap_obstructed :
    (∀ x y, D2rev x y ↔ D2 (Bool.not x) (Bool.not y)) ∧
    (∀ P : (Bool → Bool → Prop) → Prop,
      (∀ r, P (fun x y => r (Bool.not x) (Bool.not y)) ↔ P r) → (P D2 ↔ P D2rev)) ∧
    (¬ Diff2 D2 D2rev ∧ ¬ Diff2 D2rev D2) ∧
    (readsFwd D2 ∧ ¬ readsFwd D2rev) :=
  ⟨D2rev_iso_D2, sign_gap_invisible_to_invariants, Diff2_D2_D2rev_empty,
   readsFwd_separates⟩

/-! ## Axiom receipts -/

#print axioms D2_hasInvSep
#print axioms D2rev_rigid
#print axioms D2rev_hasInvSep
#print axioms D2rev_iso_D2
#print axioms sign_gap_invisible_to_invariants
#print axioms Diff2_D2_D2rev_empty
#print axioms readsFwd_separates
#print axioms readsFwd_not_invariant
#print axioms rung3_sign_gap_obstructed

end Rung3
end PrimDiff
