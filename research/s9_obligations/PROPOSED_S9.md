# PROPOSED_S9 -- replacement text for S9.1, S9.2, S9.3 (PROMPT.md step 32)

This is a proposal.  The author applies it or does not; the sealed paper is
not edited by this run, and `paper/primitive_difference.md` is byte-identical
to the pinned blob (`verify_pins.py`, `SOURCE_PINS.json`).
AuthorityEffect: None.

Governing prompt blob `1642e3f6ac746002678e4997f738e0fabd1248c9`, snapshot
commit `db1d2b225b577d5212780ff02700efd693c8e446`.  The current bullets are
the first three of section S9 (the numbering is the prompt's).  Each diff
below quotes the current lines verbatim as `-` lines and the proposed lines
as `+` lines.  One rendering convention: this tree is ASCII-only, so the em
dash in the current F3 paragraph is written `--` in its `-` line; the author
applies the diff against the sealed text, where that character is the em
dash (`test_forbidden.test_proposed_text_touches_none_of_the_protected_bullets`
checks the `-` lines against the sealed file under exactly that
substitution).

The residual scope is written into each proposed bullet itself: the bound
N, what is finite computation, and what is Lean-carried by theorem name.
Theorem names without a namespace below live in this tree's research Lake
package, `research/s9_obligations/lean/S9Obligations/`, and each has a
`#print axioms` report within `{propext, Quot.sound}` that no CI gate reads
(a manual receipt, `STATUS.md`); the sealed names `D2_initial_pointed`,
`D2_not_pointed_iso_S2`, `S2_irrefl`, `irrefl_witness_ne`,
`selfdiff_consistent` are cited, never restated.  A bullet only narrowed
gets a narrowed bullet, not a deletion; every claim in a proposed bullet is
a row of `CLAIM_LEDGER.md`.

Out of scope and untouched: OB-1, S6.6, and the S9 last bullet (the
inscription bridge).  No diff below touches their text, and the paper's
fourth and fifth S9 bullets are not touched either (the fifth is named, not
changed, by `PYTHON_ONLY_SCOPE_DECLARED`).

## S9.1 -- the axiom lattice: narrowed, with the residual written

Outcome: narrowed.  The soundness-transfer property is characterized on
every type (`transfers_iff_has_falsum_clause`,
`pure_transfer_above_point_iff_has_falsum_clause`,
`transfers_above_point_iff` with the above-the-point W identification
`transfers_above_point_of_entails_reflexive_point_forces_singleton` and,
under decidable identity on the carrier,
`transfers_above_point_imp_entails_reflexive_point_forces_singleton`); the
lattice of extents is finite computation bounded by N = 4, and the lattice
over all carriers as an object is open.
The F3 change is a separate diff below.

```diff
--- a/paper/primitive_difference.md
+++ b/paper/primitive_difference.md
@@ S9. Unresolved obligations, first bullet @@
-* **[unresolved]** Weakest-axiom claim beyond the studied set: only
-  {no axiom, symmetry, irreflexivity} were compared.  A complete lattice
-  of one-variable/two-variable Horn axioms over one relation, with the
-  soundness-transfer property characterized, is open (finite search is
-  feasible; see F3).
+* **[narrowed -- transfer characterized (theorem), lattice bounded]**
+  Weakest-axiom claim beyond the studied set.  Over universally
+  quantified Horn clauses in at most two variables over one relation
+  (atoms `r x x`, `r x y`, `r y x`, `r y y`; the clauses mentioning the
+  metatheory's `x = y`, A3's bill, enumerated separately as `EQ_BEARING`
+  and merged only with that label), the soundness-transfer property is
+  characterized on every carrier (research package
+  `S9Obligations.AxiomLattice`): under the paper's reading of "sound"
+  (every pointed structure with the asserted pair, the one-point carrier
+  included) a clause set transfers exactly when it contains a
+  falsum-headed clause, which is the same as entailing `Irrefl`
+  (`transfers_iff_has_falsum_clause`, `transfers_iff_entails_irrefl`), so
+  no atom-headed clause transfers (`atom_head_clause_does_not_transfer`,
+  the one-point full relation being a model of every clause set without
+  a falsum head: `non_falsum_clause_set_admits_selfdiff`); under the
+  weaker reading that discounts the one-point carrier, the pure fragment
+  has the same characterization
+  (`pure_transfer_above_point_iff_has_falsum_clause`) while the clause
+  `r x x -> x = y` transfers without entailing irreflexivity
+  (`reflexive_point_forces_singleton_f3_countermodel_above_point`; see
+  F3).  The lattice itself is finite computation, bounded by carrier
+  N = 4: the meet closure of the single-clause extents has 75 elements
+  (pure), 37 (`EQ_BEARING`), 147 (merged), the same at N = 3, with the
+  N = 4 closure restricting injectively onto the N = 3 one; N = 5 was
+  refused by name.  Still open: the lattice of extents over all carriers
+  as an object; a syntactic characterization of transfer above the point
+  once the identity atom is admitted; and the converse of the
+  above-the-point identification without decidable identity on the
+  carrier (`transfers_above_point_imp_entails_reflexive_point_forces_singleton`
+  assumes it).
```

## S9.2 -- morphism classes: discharged with scope

Outcome: discharged with scope.  Within a declared menu of five morphism
conditions and for candidates on the two-element carrier with the asserted
pair, the admitting classes are decided on every type
(`admits_primary_exactly`, `admits_secondary_exactly`); the residual --
conditions outside the declared menu, and the table as an artifact, whose
cells are read as instances of the per-class theorems by a test rather
than by a Lean statement -- is written into the bullet.

```diff
--- a/paper/primitive_difference.md
+++ b/paper/primitive_difference.md
@@ S9. Unresolved obligations, second bullet @@
-* **[unresolved]** The initiality of `D2` is proved for point-preserving
-  morphisms; a characterization of *all* edge-preserving morphism classes
-  under which some two-element object remains initial is open.
+* **[theorem, scoped to a declared menu]** The initiality of `D2` is
+  proved for point-preserving morphisms (`D2_initial_pointed`: existence
+  of a point-preserving map that also preserves the oriented edge, and
+  uniqueness over every point-preserving map).  Within the declared menu
+  P (designated points preserved), E (edges preserved), NE (non-edges
+  preserved, `not r x y -> not r' (f x) (f y)`), I (injective), S
+  (surjective) -- 32 classes -- and for candidates that are pointed
+  relations on the two-element carrier with the asserted pair, the
+  classes under which some two-element object is initial are, on every
+  carrier, exactly {P}, {P,E}, {P,NE} over all pointed structures with
+  an asserted pair and exactly {P}, {P,E}, {P,NE}, {P,I}, {P,E,I},
+  {P,NE,I} over irreflexive ones (research package
+  `S9Obligations.MorphismClasses`, `admits_primary_exactly`,
+  `admits_secondary_exactly`); a class admits exactly when it contains
+  P, contains no S (and no I, unless irreflexivity is imposed), and does
+  not contain both E and NE (`admits_primary_iff`,
+  `admits_secondary_iff`; the E-with-NE exclusion is
+  `not_initial_P_E_NE`); that the admitting sets are not intervals under
+  inclusion (incomparable maximal pair {P,E}, {P,NE}; gap {P,E,NE}) is a
+  set property read off the two exact lists, finite computation bounded
+  by N = 4 as computed, which no Lean theorem states.  Among the classes
+  containing E, only {P,E} (and {P,E,I} over irreflexive objects) admit
+  an initial two-element object, and it is `D2` (`D2_initial_P_E`,
+  `initial_P_E_iff`); {P,NE}
+  selects the full two-element relation (`FULL2_initial_P_NE`; that no
+  other decidable candidate is initial for it is `initial_P_NE_iff`), or
+  `S2` over irreflexive objects (`S2_initial_P_NE_irrefl`); {P} and
+  {P,I} over irreflexive objects retain both `D2` and `S2`
+  (`two_element_initial_P_I_irrefl`, `D2_not_pointed_iso_S2`).  Residual:
+  conditions outside the declared menu are not classified, and the
+  576-cell table with its first-witness objects is finite computation
+  bounded by object carrier N = 4, its exhaustiveness living in Python
+  only (the fifth bullet).
```

## S9.3 -- witness types: discharged with scope, as a boundary

Outcome: discharged with scope.  The existence question is answered by a
Lean-carried pair under a named admission; the boundary of what stays
invisible is finite computation bounded by N = 3 and T = 3, and the
residuals are written into the bullet.

```diff
--- a/paper/primitive_difference.md
+++ b/paper/primitive_difference.md
@@ S9. Unresolved obligations, third bullet @@
-* **[unresolved]** A2 with witness *types* (proof-relevant witnesses with
-  their own identity) rather than counts: whether any witness-level
-  structure ever becomes observable below function spaces.
+* **[boundary, scoped to a declared admission and vocabularies]** A2 with
+  witness *types* (proof-relevant witnesses with their own identity)
+  rather than counts.  Admitting, beyond A2, a finite token domain and a
+  decidable equality on it (`TOKEN_DOMAIN`, `TOKEN_EQ`; outside A1's
+  bill, since it is an identity relation on the token sort, and not
+  contained in A3's bill -- function types, composition, a one-point
+  carrier -- which it does not contain either), witness-level structure
+  does become observable below function spaces, within the declared
+  vocabularies (presence; count comparisons; anonymous sharing;
+  named-token occurrence): on the two-element irreflexive object the
+  assignments `{t0},{t0}` and `{t0},{t1}` at the pairs (0,1), (1,0)
+  agree on presence and on every count comparison and are separated by
+  the one question "do the two pairs share a token", which uses
+  `TOKEN_EQ` and nothing else, and they are not isomorphic as witness
+  families (research package `S9Obligations.WitnessTypes`,
+  `S9_3_sep_V1_indistinguishable`, `S9_3_sep_V2_ANON_separates`,
+  `S9_3_sep_not_isomorphic`; both induce `S2`, `sepPresenceS2`).  The
+  boundary, finite computation bounded by carrier N = 3 and token domain
+  T = 3 with cell (3, 3) not enumerated: in every enumerated space,
+  presence, count comparisons, and anonymous sharing together still
+  leave invisible token renamings (isomorphic families) and count
+  magnitudes, and, in the one enumerated cell with T = 3, pairs that
+  differ in how many tokens two pairs share, the first of which is
+  Lean-carried (`S9_3_inv_V1_V2_ANON_indistinguishable`,
+  `S9_3_inv_not_isomorphic`); naming tokens (`TOKEN_NAMES`, a further
+  admission) hides nothing in any enumerated space, under the same
+  bound, at the cost of separating renamings that are not witness-level
+  structure.  The pair counts, the first-pair rule, and the split of the
+  invisible pairs by invariant are finite computation, bounded by N = 3
+  and T = 3 with cell (3, 3) not enumerated.  Residual: the Lean
+  vocabulary lists are a transcription of the declared vocabularies at
+  carrier 2, compared with them by no gate; whether a vocabulary
+  comparing sharing counts is below function spaces is not decided; the
+  store per pair is a set, and multisets were not computed.
```

## F3 -- the fidelity lattice: a separate diff, labelled by definition

F3's status changed, and how it changed depends on the definition of
soundness transfer.  Label: **`TRANSFER_ALL_CARRIERS`** is the paper's own
reading of "sound" (every pointed structure with the asserted pair, the
one-point carrier included); **`TRANSFER_ABOVE_POINT`** is the weaker
reading that discounts the one-point self-difference of
`selfdiff_consistent`.  Under the first the conjecture cannot fail, because
"transfers" and "entails irreflexivity" are one containment
(`F3_UNTESTED`, carried by `transfers_iff_entails_irrefl` on every type);
under the second it holds in the pure fragment (`F3_SUPPORTED_BOUNDED`,
carried by `pure_transfers_above_point_iff_entails_irrefl`) and fails once
the identity atom of A3's bill is admitted (`F3_REFUTED`, the countermodel
`reflexive_point_forces_singleton_f3_countermodel_above_point`), which is a
refutation of F3 extended to A3's bill under a soundness weaker than S7's,
not of F3 as written.  The diff replaces only the last sentence.

```diff
--- a/paper/primitive_difference.md
+++ b/paper/primitive_difference.md
@@ FRONTIER CONJECTURES, F3 @@
-**F3. The fidelity lattice.**  Irreflexivity was the unique
-soundness-transferring axiom among the three studied.  *Conjecture:* in
-the full finite lattice of universally quantified one-relation axioms,
-the soundness-transferring ones form a filter generated by
-irreflexivity -- i.e., every axiom that makes assertion sound *contains*
-irreflexivity's content.  Finite search over small axiom shapes is
-feasible with the existing enumerator; not yet run.
+**F3. The fidelity lattice.**  Irreflexivity was the unique
+soundness-transferring axiom among the three studied.  *Conjecture:* in
+the full finite lattice of universally quantified one-relation axioms,
+the soundness-transferring ones form a filter generated by
+irreflexivity -- i.e., every axiom that makes assertion sound *contains*
+irreflexivity's content.  Run over Horn clauses in at most two variables
+(`research/s9_obligations`; sweep bounded by carrier N = 4;
+`transfers_iff_entails_irrefl`, `transfers_iff_has_falsum_clause`,
+`pure_transfers_above_point_iff_entails_irrefl` and
+`reflexive_point_forces_singleton_f3_countermodel_above_point` on every
+carrier), with the outcome depending on the reading of "sound".
+Under this paper's reading (every pointed structure, the one-point
+carrier included) the conjecture cannot fail: "transfers" and "entails
+irreflexivity" are the same containment, a theorem of the encoding for
+Horn clause sets (`transfers_iff_entails_irrefl`), so the transferring
+clause sets are exactly those containing a falsum-headed clause
+(`transfers_iff_has_falsum_clause`) -- the filter generated by
+irreflexivity, with no content beyond the definition, and the finite
+sweep could not have failed it.  Under the weaker reading that discounts
+the one-point carrier (soundness above the point), the conjecture holds
+in the pure fragment (`pure_transfers_above_point_iff_entails_irrefl`)
+and fails once A3's identity atom is admitted: `r x x -> x = y`
+transfers above the point and admits the one-point self-difference
+(`reflexive_point_forces_singleton_f3_countermodel_above_point`) --
+a refutation of the conjecture extended to A3's bill under that weaker
+soundness, not of the conjecture as written.
```

## What is not proposed

* No change to the fourth and fifth S9 bullets (the finite-search bound
  and the Python-only exhaustiveness), although this run's S9.2 sweep is
  one more instance of the fifth (`PYTHON_ONLY_SCOPE_DECLARED`).
* No change to S7's terminal statement: its scope sentence names the
  wider axiom lattice as an open obligation, and S9.1 is narrowed, not
  closed.
* No change to the S9 last bullet, OB-1, or S6.6: out of scope.
