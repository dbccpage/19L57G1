# Crosswalk

AuthorityEffect: None. Outside the seal.

This table settles eight words that the companion repository (named CW
below: `dbccpage/cognitive_warfare_actors_institutions_and_the_limits_of_superintelligence`,
supplied by the operator) and this repository use for different objects. It
follows the plan of 2026-11-06, section 2. CW's words are **supplied
vocabulary**, classified as such under the vocabulary ruling in
`CLAUDE.md`: the table is a reading of CW objects in terms of the finite core
here, not a derivation of either from the other and not a proved bridge,
except where a row names a theorem. Nothing here is an input to the sealed
derivation.

The rule adopted: **the finite definitions of this repository are the core,
and each CW object is read as a declared lift**, which must name its finite
carrier before it is used.

| Term | Core here (Lean) | CW object, read as a lift | Obligation and where it stands |
|---|---|---|---|
| carrier | a finite list `D : List Nat` of cases or states | CW's admitted latent state space and its compatible-model set, restricted to a finite listed set | each CW use names its finite carrier; an unbounded state space is not admitted. Open on the CW side. |
| presentation | `p : Nat → Nat` read only on `D`, that is a finite table `D → Nat` (TT-41) | CW's context-indexed presentation map with a finite context set becomes the finite family of its sections, one table per context | none: a definition. `Nat → Nat` is metatheory; only the table on `D` is internal. |
| actor | one presentation (TT-R1) | CW's actor with many presentations becomes a finite family `F` read through its joint presentation `pQ D F` | **L0, proved**: `Joint.knows_family_iff_joint` (IF-00). The two readings know the same. |
| institution | `Q : List (Nat → Nat)`, a finite list of seats | CW's ledger institution is `Q` together with correspondence admissions, a retention policy, lifecycle events and a mandate, which are not objects here | consistent with "an institution is a kind of actor", because `pQ D Q` is a presentation (L0). The added fields are CW's. |
| presentation family | the institution's seat list `Q` | CW used this name for its model-uncertainty set, which is the carrier `D` (or its set of tables), not `Q` | **renamed on the CW side: presentation family (CW, model-uncertainty set) → model family.** "Presentation family" is kept for `Q`. The CW patch is a separate erratum to its `docs/research.md`. |
| fiber | a signature class of `pQ D Q` in `D` | CW's preimage of a compression over arbitrary types | CW's two fiber theorems use the choice principle over arbitrary types; they would need constructive restatement over lists before import. Not done here. |
| knowledge, information | `Knows` (factoring through `pQ`); `classCount` | CW prose definitions | none beyond the renaming above. Separation redundancy (IF-01) is the robustness count added here. |
| authorization | `Rule`, constrained by the admission `ScopedSound` (AI-13) | CW's "evaluated and mandated", with the mandate supplied from outside | keep both, as separate fields: `ScopedSound` is a soundness admission and the mandate is a jurisdiction grant. `ScopedSound` is **unpriced** and recorded so (`AUDIT.md`, IF-17o). |

## A correction to an earlier summary

`pQ_exact` says the institution separates exactly the *pairs* that some seat
separates. It does not say the institution knows only what some seat knows:
`Inst.exceeds_iff` and TT `institution_exceeds_members` prove the opposite,
and L3 here (IF-13) shows that ballots can lose exactly that excess.
