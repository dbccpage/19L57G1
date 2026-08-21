import Derivation.PrimDiff

/-!
# Rung 2 of the primitive-difference tower: the difference between two
# primitive differences

POST-SEAL extension experiment artifact.  Imports `Derivation.PrimDiff`
**unmodified**; adds nothing to the sealed library; compiled read-only with
`lake env lean` for a proof receipt.  No new primitive, parameter, observation,
candidate menu, policy, or oracle is introduced — the rung-2 difference is built
entirely from the sealed layer's OWN observer/orientation analysis (S4).

## The move

Rung 1 (sealed, `PrimDiff.lean` / S7) fixes the strongest primitive-difference
object as a *witnessed irreflexive relation*, whose two-element realizations are
exactly the oriented `D2` and the symmetric `S2`.  These are non-isomorphic
(`D2_not_pointed_iso_S2`) yet collision-equivalent (`D2_S2_collapse_equiv`), and
the branch between them is **retained as a tie**: "nothing at this layer selects
between carrying orientation primitively (`D2`) or adding it later (`S2`)."

Frontier conjecture F1 asks for the next rung: "differences *between*
differences," each with "its own initial object and its own orientation gap,"
with "nothing above them yet."

This file supplies one rung-2 instance.  The carrier is the type of rung-1
relations; the asserted rung-2 difference between `D2` and `S2` is the
derivation's own discriminator — `D2` carries an automorphism-invariant
separating Boolean classifier and `S2` does not (S4: `oriented_classifier_exists`
vs `symmetric_no_equivariant_classifier`).  The result: that difference is a
witnessed irreflexive A1i object which is **oriented** (`D2`-shaped) — so the
rung-1 tie is *resolved* one level up, with the orientation *forced* by the
observer-existence asymmetry, not chosen.  What is NOT forced is the orientation
sign (`D2` vs `D2rev`): the rung-1 orientation gap reappears at rung 2.
-/

namespace PrimDiff
namespace Rung2

/-! ## The observer-existence discriminator (sealed notion, S4) -/

/-- A `g` preserving-and-reflecting the relation is an automorphism (the
condition used by `oriented_rigid`, `swap_is_S2_automorphism`). -/
def IsAuto (r : Bool → Bool → Prop) (g : Bool → Bool) : Prop :=
  ∀ x y, r x y ↔ r (g x) (g y)

/-- The sealed observer property (S4): the structure admits an
automorphism-invariant separating Boolean classifier. -/
def HasInvSepClassifier (r : Bool → Bool → Prop) : Prop :=
  ∃ κ : Bool → Bool, κ false ≠ κ true ∧ ∀ g, IsAuto r g → ∀ x, κ (g x) = κ x

/-- `D2` HAS an invariant separating classifier: it is rigid
(`oriented_rigid`), so the identity is the (only) automorphism and separates. -/
theorem D2_hasInvSep : HasInvSepClassifier D2 :=
  ⟨id, by decide, fun g hg x => by
    have hgid : ∀ z, g z = z := oriented_rigid g hg
    show id (g x) = id x
    simp [hgid x]⟩

/-- `S2` has NO invariant separating classifier: the swap is a nontrivial
automorphism (`swap_is_S2_automorphism`) and every swap-invariant classifier is
constant (`symmetric_no_equivariant_classifier`). -/
theorem S2_not_hasInvSep : ¬ HasInvSepClassifier S2 := by
  rintro ⟨κ, hsep, hinv⟩
  have hnot : ∀ x, κ (Bool.not x) = κ x := hinv Bool.not swap_is_S2_automorphism
  exact hsep (symmetric_no_equivariant_classifier κ hnot)

/-! ## The rung-2 primitive difference -/

/-- The rung-2 asserted difference on the carrier of rung-1 relations: `r` has
the observer, `r'` does not.  This is the difference the sealed analysis singles
out between the two retained realizations. -/
def Diff2 (r r' : Bool → Bool → Prop) : Prop :=
  HasInvSepClassifier r ∧ ¬ HasInvSepClassifier r'

/-- **Irreflexive** by construction (`P ∧ ¬P`): a valid A1i fidelity commitment
one rung up, with no axiom imported. -/
theorem Diff2_irrefl : Irrefl Diff2 := fun _ h => h.2 h.1

/-- **Witnessed**: the pair `(D2, S2)` is asserted. -/
theorem Diff2_witness : Diff2 D2 S2 := ⟨D2_hasInvSep, S2_not_hasInvSep⟩

/-- **Oriented, not symmetric**: the reverse is not asserted.  The rung-1 tie is
directional one level up. -/
theorem Diff2_not_reverse : ¬ Diff2 S2 D2 := fun h => S2_not_hasInvSep h.1

/-! ## The rung-2 difference IS the oriented object `D2` -/

/-- Encode the two retained rung-1 realizations as a two-element carrier:
`false ↦ D2`, `true ↦ S2`. -/
def enc : Bool → (Bool → Bool → Prop) := fun b => cond b S2 D2

/-- The rung-2 difference restricted to the `{D2, S2}` carrier. -/
def diff2Bool (x y : Bool) : Prop := Diff2 (enc x) (enc y)

/-- **Headline.**  The difference between the two rung-1 primitive differences,
read on the two-element carrier `{D2, S2}`, is *exactly the oriented `D2`*.
The rung-1 orientation tie is therefore resolved at rung 2, and resolved
canonically: the orientation is forced by the observer-existence asymmetry. -/
theorem rung2_is_D2 : diff2Bool = D2 := by
  funext x y
  apply propext
  unfold diff2Bool enc
  cases x <;> cases y
  · exact iff_of_false (fun h => h.2 h.1) (by decide)
  · exact iff_of_true Diff2_witness (by decide)
  · exact iff_of_false Diff2_not_reverse (by decide)
  · exact iff_of_false (fun h => h.2 h.1) (by decide)

/-- Consequently the rung-2 difference inherits `D2`'s **rigidity**: any
endomap preserving-and-reflecting it is the identity.  Unlike the rung-1
symmetric branch `S2`, the rung-2 object has no nontrivial automorphism — its
orientation is internal. -/
theorem rung2_rigid (f : Bool → Bool)
    (hiff : ∀ x y, diff2Bool x y ↔ diff2Bool (f x) (f y)) : ∀ x, f x = x := by
  rw [rung2_is_D2] at hiff
  exact oriented_rigid f hiff

/-- And it inherits `D2`'s **invariant separating classifier**: the rung-2
difference is itself observable. -/
theorem rung2_hasInvSep : HasInvSepClassifier diff2Bool := by
  rw [rung2_is_D2]; exact D2_hasInvSep

/-! ## Sealed initiality transfers to rung 2 -/

/-- The sealed initiality theorem `D2_initial_pointed`, instantiated at the
rung-2 structure `(carrier of rung-1 relations, Diff2, D2, S2)`: the oriented
two-element object maps **uniquely** into the rung-2 difference, preserving the
oriented edge.  `D2` is initial one rung up as well. -/
theorem D2_initial_into_rung2 :
    ∃ f : Bool → (Bool → Bool → Prop),
      (f false = D2 ∧ f true = S2 ∧ ∀ x y, D2 x y → Diff2 (f x) (f y)) ∧
      ∀ g : Bool → (Bool → Bool → Prop),
        g false = D2 → g true = S2 → ∀ t, g t = f t :=
  D2_initial_pointed Diff2 D2 S2 Diff2_witness

/-! ## Residual: the orientation SIGN is not forced (the gap recurs) -/

/-- The opposite labelling convention (`r'` has the observer, `r` does not). -/
def Diff2rev (r r' : Bool → Bool → Prop) : Prop :=
  ¬ HasInvSepClassifier r ∧ HasInvSepClassifier r'

/-- Read on the same carrier, the opposite convention is `D2rev` — the reversed
orientation.  Nothing at rung 2 selects between `Diff2` and `Diff2rev`: this is
exactly the sealed `D2` / `D2rev` orientation gap, reappearing one rung up. -/
theorem rung2rev_is_D2rev : (fun x y => Diff2rev (enc x) (enc y)) = D2rev := by
  funext x y
  apply propext
  unfold enc
  cases x <;> cases y
  · exact iff_of_false (fun h => h.1 h.2) (by decide)
  · exact iff_of_false (fun h => h.1 D2_hasInvSep) (by decide)
  · exact iff_of_true ⟨S2_not_hasInvSep, D2_hasInvSep⟩ (by decide)
  · exact iff_of_false (fun h => h.1 h.2) (by decide)

/-- The residual rung-2 tie `D2` vs `D2rev` is real but **collision-invisible** —
the sealed orientation gap verbatim (`orientation_data_invisible_to_collapse`):
no point-fixing map identifies the two conventions, yet they collide identically.
So rung 2 kills the symmetric/oriented ambiguity and reintroduces exactly the
sign ambiguity of rung 1. -/
theorem rung2_residual_is_orientation_gap :
    (∀ f : Bool → Bool, f false = false → f true = true →
        ¬ (∀ x y, D2 x y ↔ D2rev (f x) (f y))) ∧
      (CollapseCollision D2 (fun _ => ()) ↔
        CollapseCollision D2rev (fun _ => ())) :=
  orientation_data_invisible_to_collapse

/-! ## General principle: rung-2 orientation ⟺ a sealed separating observable

The orientation of the rung-2 difference is not an artefact of the specific
discriminator chosen.  For ANY property `P` on rung-1 relations, the
`P`-difference is irreflexive, and on a two-element carrier it is either the
oriented `D2` (when `P` separates the pair) or empty (when `P` does not).  So
whether the difference between two rung-1 objects is a genuine oriented
primitive difference, or collapses to non-primitive metatheoretic inequality
(A3, `factors_through_point_iff`), is decided EXACTLY by whether the sealed
layer supplies an observable separating them.  The `D2`/`S2` orientation
asymmetry (S4) is one such supplied observable; presence-invisible data (e.g.
witness multiplicity, `multiplicity_invisible_to_presence`) is not, and yields
no rung-2 primitive difference. -/

/-- The `P`-difference for any property `P` of rung-1 relations. -/
def PDiff (P : (Bool → Bool → Prop) → Prop) (r r' : Bool → Bool → Prop) : Prop :=
  P r ∧ ¬ P r'

theorem PDiff_irrefl (P : (Bool → Bool → Prop) → Prop) : Irrefl (PDiff P) :=
  fun _ h => h.2 h.1

/-- **Separating ⇒ oriented.**  If `P` holds of `a` and fails of `b`, the
`P`-difference on the two-element carrier `{a, b}` is exactly the oriented `D2`.
`rung2_is_D2` is the instance `P = HasInvSepClassifier`, `a = D2`, `b = S2`. -/
theorem pdiff_separating_is_D2
    {P : (Bool → Bool → Prop) → Prop} {a b : Bool → Bool → Prop}
    (ha : P a) (hb : ¬ P b) :
    (fun x y => PDiff P (cond x b a) (cond y b a)) = D2 := by
  funext x y
  apply propext
  cases x <;> cases y
  · exact iff_of_false (fun h => h.2 h.1) (by decide)
  · exact iff_of_true ⟨ha, hb⟩ (by decide)
  · exact iff_of_false (fun h => hb h.1) (by decide)
  · exact iff_of_false (fun h => h.2 h.1) (by decide)

/-- **Non-separating ⇒ empty.**  If `P` cannot tell the pair apart
(`P a ↔ P b`), the `P`-difference on `{a, b}` has no witness: no rung-2 primitive
difference exists.  A pair the sealed layer observes as identical yields only
metatheoretic inequality one rung up, which is not primitive. -/
theorem pdiff_nonseparating_empty
    {P : (Bool → Bool → Prop) → Prop} {a b : Bool → Bool → Prop}
    (hPab : P a ↔ P b) :
    ∀ x y, ¬ PDiff P (cond x b a) (cond y b a) := by
  intro x y h
  cases x <;> cases y
  · exact h.2 h.1
  · exact h.2 (hPab.mp h.1)
  · exact h.2 (hPab.mpr h.1)
  · exact h.2 h.1

/-! ## Axiom receipts -/

#print axioms D2_hasInvSep
#print axioms S2_not_hasInvSep
#print axioms Diff2_irrefl
#print axioms Diff2_witness
#print axioms Diff2_not_reverse
#print axioms rung2_is_D2
#print axioms rung2_rigid
#print axioms rung2_hasInvSep
#print axioms D2_initial_into_rung2
#print axioms rung2rev_is_D2rev
#print axioms rung2_residual_is_orientation_gap
#print axioms PDiff_irrefl
#print axioms pdiff_separating_is_D2
#print axioms pdiff_nonseparating_empty

end Rung2
end PrimDiff
