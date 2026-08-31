import NaturalSections

/-!
# The equivariant bridge: the sealed selector theorem as an instance of
the section obstruction

The sealed `ContactKernel.no_equivariant_pair_valued_map` rules out a
total map `sel : DiffObs Bool Bool → Bool × Bool` commuting with the
negation relabelling `swapObs`.  The sealed `PresentationNaturality`
module records, in its section 10 and its section 14 non-claims, that
deriving that statement from the general obstruction
`no_natural_section_of_fixed_point_free` is OPEN: the two quantify over
different objects -- raw-pair-valued maps out of the observer type,
versus sections of the admissible-pair bundle.  This module supplies
the missing bridge.  The seal is not amended; the sealed OPEN record
stands where it is, and what follows is a research derivation alongside
it, citing sealed theorems by name only.

The gap is admissibility: a section assigns an admissible pair
(`NonZeroPair boolEqObs`), the sealed selector assigns a raw pair,
which may be diagonal, and no observer admits a diagonal pair because
`zero_refl` is a field.  The bridge is `pairRetract`, a map from raw
pairs to admissible pairs that commutes with the negation action --
possible because the negation action on raw pairs is free, so each of
its two orbits `{(F,F),(T,T)}` and `{(F,T),(T,F)}` maps orbitwise onto
the admissible orbit.

The derivation route, and its honesty condition.  From an equivariant
`sel`, the constant assignment `fun _ => pairRetract (sel boolEqObs)`
is a natural section of `autoFamily boolEqObs negIso`
(`sectionOf_natural`), proved from the equivariance law at
`boolEqObs`, the sealed fixed-point equation `swapObs_boolEqObs`, and
the equivariance of the retraction -- never from the fact that
negation fixes no Boolean.  The `False` is then produced by the sealed
`no_natural_section_of_fixed_point_free` applied with the sealed
`negIso_fixed_point_free`.  What is NOT claimed: independence from
`negIso_fixed_point_free` -- that sealed input is the Bool-instance
fixed-point-freeness the general obstruction consumes, cited, not
re-proved.  The claim is about the route: the sealed selector
statement is an instance of the section obstruction, which is exactly
the derivation the sealed module records as missing.

The translation is the identity: `Equivariant` unfolds to the sealed
equivariance law (`equivariant_iff_sealed_shape`, by `Iff.rfl`), and
`bridge_statement_is_the_sealed_statement` certifies that the derived
proposition IS the sealed proposition -- the equation between the two
proofs elaborates only if their statements are definitionally equal,
and it closes by `rfl`.

AuthorityEffect: None.
-/

namespace NaturalSections.EqBridge

open DiffInterface ContactKernel PresentationNaturality

/-- An equivariant pair-valued map, in this tree's vocabulary: a total
assignment of a raw Boolean pair to every observer `DiffObs Bool Bool`
that commutes with the declared relabelling action `swapObs` -- the
negation action on the carrier, acting on pairs componentwise.  This is
definitionally the sealed law (`equivariant_iff_sealed_shape`). -/
def Equivariant (sel : DiffObs Bool Bool → Bool × Bool) : Prop :=
  ∀ O : DiffObs Bool Bool, sel (swapObs O) = (!((sel O).1), !((sel O).2))

/-- The equivariant retraction of raw Boolean pairs onto the admissible
pairs of `boolEqObs`: the identity on the two admissible (off-diagonal)
pairs, and orbitwise on the diagonal orbit -- `(F,F) ↦ (F,T)` and
`(T,T) ↦ (T,F)`.  Admissibility of the values is the sealed
`boolEqObs_nonzero_ft` / `boolEqObs_nonzero_tf`. -/
def pairRetract : Bool × Bool → NonZeroPair boolEqObs
  | (false, false) => ⟨(false, true), boolEqObs_nonzero_ft⟩
  | (false, true) => ⟨(false, true), boolEqObs_nonzero_ft⟩
  | (true, false) => ⟨(true, false), boolEqObs_nonzero_tf⟩
  | (true, true) => ⟨(true, false), boolEqObs_nonzero_tf⟩

/-- The four values of the retraction, exactly as pre-registered: the
finite instance check of this rung, discharged by `decide`. -/
theorem pairRetract_table :
    (pairRetract (false, false)).val = (false, true) ∧
      (pairRetract (true, true)).val = (true, false) ∧
      (pairRetract (false, true)).val = (false, true) ∧
      (pairRetract (true, false)).val = (true, false) := by
  decide

/-- On an admissible pair the retraction is the identity: `pairRetract`
is a genuine retraction onto the admissible pairs, not merely a map
into them. -/
theorem pairRetract_fixes_admissible (p : NonZeroPair boolEqObs) :
    pairRetract p.val = p := by
  obtain ⟨⟨x, y⟩, hp⟩ := p
  cases x <;> cases y
  · exact absurd rfl hp
  · exact Subtype.ext rfl
  · exact Subtype.ext rfl
  · exact absurd rfl hp

/-- The retraction commutes with the negation action: negating both
components of a raw pair and retracting is retracting and transporting
along `negIso`.  Proved by finite case analysis; the fact that
negation fixes no Boolean is nowhere used. -/
theorem pairRetract_equivariant (p : Bool × Bool) :
    pairRetract (!p.1, !p.2) = negIso.mapPair (pairRetract p) := by
  obtain ⟨x, y⟩ := p
  cases x <;> cases y <;> exact Subtype.ext rfl

/-- The section an equivariant selector induces over the one-object
family of the negation automorphism at `boolEqObs`: retract the
selector's raw value at that observer. -/
def sectionOf (sel : DiffObs Bool Bool → Bool × Bool) :
    Sec (autoFamily boolEqObs negIso) :=
  fun _ => pairRetract (sel boolEqObs)

/-- **The bridge lemma.**  If `sel` is equivariant, `sectionOf sel` is
natural.  The proof consumes exactly: the equivariance law at
`boolEqObs`, the sealed `swapObs_boolEqObs` (so the law reads
`sel boolEqObs = (!.., !..)` at the fixed point), and
`pairRetract_equivariant`.  The inconsistent-looking hypothesis is
only ever rewritten with, never refuted here: the refutation is the
sealed obstruction's job, which is what makes the derivation a
derivation and not a re-proof. -/
theorem sectionOf_natural (sel : DiffObs Bool Bool → Bool × Bool)
    (h : Equivariant sel) :
    IsNatural (autoFamily boolEqObs negIso) (sectionOf sel) := by
  intro _
  have hfix : sel boolEqObs =
      (!((sel boolEqObs).1), !((sel boolEqObs).2)) := by
    have h0 := h boolEqObs
    rwa [swapObs_boolEqObs] at h0
  show negIso.mapPair (pairRetract (sel boolEqObs)) =
    pairRetract (sel boolEqObs)
  calc negIso.mapPair (pairRetract (sel boolEqObs))
      = pairRetract (!((sel boolEqObs).1), !((sel boolEqObs).2)) :=
        (pairRetract_equivariant (sel boolEqObs)).symm
    _ = pairRetract (sel boolEqObs) := (congrArg pairRetract hfix).symm

/-- **The bridge theorem.**  No equivariant pair-valued map exists --
DERIVED: an equivariant `sel` would induce a natural section of
`autoFamily boolEqObs negIso` (`sectionOf_natural`), which the sealed
`no_natural_section_of_fixed_point_free` refuses under the sealed
`negIso_fixed_point_free`.  The `False` is produced by the section
obstruction, not by a direct fixed-point computation on `sel`. -/
theorem no_equivariant_pair_valued_map_via_sections :
    ¬ ∃ sel : DiffObs Bool Bool → Bool × Bool, Equivariant sel := by
  rintro ⟨sel, h⟩
  exact no_natural_section_of_fixed_point_free boolEqObs negIso
    negIso_fixed_point_free ⟨sectionOf sel, sectionOf_natural sel h⟩

/-- The research notion is the sealed law, definitionally: the
translation between the two statements is the identity. -/
theorem equivariant_iff_sealed_shape
    (sel : DiffObs Bool Bool → Bool × Bool) :
    Equivariant sel ↔
      ∀ O : DiffObs Bool Bool,
        sel (swapObs O) = (!((sel O).1), !((sel O).2)) :=
  Iff.rfl

/-- The sealed statement's content, along the bridge: the proposition of
the read-only sealed `ContactKernel.no_equivariant_pair_valued_map`,
proved here through `no_equivariant_pair_valued_map_via_sections`
rather than by the sealed module's own fixed-point argument. -/
theorem sealed_selector_content_along_bridge :
    ¬ ∃ sel : DiffObs Bool Bool → Bool × Bool,
        ∀ O : DiffObs Bool Bool,
          sel (swapObs O) = (!((sel O).1), !((sel O).2)) :=
  fun ⟨sel, h⟩ => no_equivariant_pair_valued_map_via_sections ⟨sel, h⟩

/-- **Statement identity, machine-checked.**  This equation between the
bridge-derived proof and the sealed proof elaborates only if the two
STATEMENTS are definitionally equal types, and it closes by `rfl`
(definitional proof irrelevance).  So the types align exactly and no
translation definition is needed: the sealed theorem's content follows
along the bridge for the shared instance, with the sealed
`ContactKernel.no_equivariant_pair_valued_map` cited by name as
read-only capital. -/
theorem bridge_statement_is_the_sealed_statement :
    sealed_selector_content_along_bridge =
      ContactKernel.no_equivariant_pair_valued_map :=
  rfl

end NaturalSections.EqBridge
