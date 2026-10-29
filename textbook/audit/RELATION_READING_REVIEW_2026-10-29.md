# Recorded pairs, properties, and extensions: reading review

Date: 2026-10-29. AuthorityEffect: None.

## Scope

Selected semantic and readability review of Units 23–26 against read-only
`PrimDiff.lean`, `Bridge.lean`, the corresponding Python models, paper
sections, ledger references, artifacts, and existing book checks. This
follows the [requests and cost review](COST_READING_REVIEW_2026-10-29.md).

Four first passes introduce the relation model, a one-point counterexample,
global irreflexivity versus a particular pair, map collisions, and positive
extensions. Short claims precede optional detailed statements and sources;
exercise answers are folded. Unit 26's revised title appears in the current
overview and coverage table without changing its file ID. Historical audit
records and all sealed sources remain unchanged.

## Corrections and teaching examples

| Unit | Previous issue | Correction |
|---|---|---|
| 23 | A one-point countermodel was said to refute the implication on every carrier; Unit 13 was cited for unrelated candidate labels; the move from an admission regime to a relation was vague | One example refutes the schema quantified over all structures. It does not falsify every particular instance. A1/A3 refer back to Unit 15, A1i is defined locally, and the separate model is named explicitly. No translation from a regime is inferred. |
| 24 | A global equivalence was read as saying a particular inequality holds precisely as far as irreflexivity; “weakest” was expanded into no consequences under other laws | Irreflexivity is equivalent to inequality for every asserted pair. A specific unequal asserted pair can coexist with a self-pair elsewhere. The minimality language is restricted to the three options compared for that particular guarantee; symmetry does have consequences. Irreflexivity of a fixed definition can be proved. |
| 25 | “The merge goes through,” automatic refusal by the metatheory, and a claimed smallest mechanism suggested operational enforcement or a bridge to the admission engine | Pushforward is a construction, collision is an exhibited pair, and obstruction is the stated conjunction with target property failure. There is no execution or enforcement theorem here, no source-property premise, and no proved bridge to response validity. |
| 25 | General property loss could be confused with `FidelityObstruction` | The book's four-point example has exactly `0→1` and `2→3`. Merging 2 into 1 gives `0→1→3` without `0→3`. Transitivity holds before and fails after, but no edge's own ends merge. Hence this is property loss without the definition's required collision and without its obstruction. |
| 26 | The title and prose said facts never entail the law, and that it could never be a consequence | The theorem concerns unrestricted positive extensions on a carrier with a point. It does not prevent proving a property of an exactly specified relation, checking a complete finite table, using negative information, or restricting the allowed family. The source's extension formula is unchanged. |
| 26 | A book comment said a witness alone gives neither irreflexivity nor its negation; the extension theorem was described as if it had an asserted-pair premise | A self-pair already refutes irreflexivity. The extension theorem quantifies over any relation and a supplied point, without an edge premise. The empty-carrier exception, three bounded bridge scenarios, and absence of a general empirical claim are explicit. |

The negative diagonal checks in Unit 26 illustrate information beyond the
positive inclusion premise. A deliberately defined inequality relation
also has a direct irreflexivity proof. Neither example supplies a new
derivation from the opaque mark or a reason to protect a chosen law.
Unit 23 also separates Unit 14's A3 factorization criterion from A4's
irreducibility under an admitted operation family.

## Book proofs and computational scope

The four book drivers check 50 reports. Eight reports are new:

| Script | Theorem | Exact library dependencies |
|---|---|---|
| u24 | `mixed_specific_pair` | none |
| u25 | `disjoint_transitive` | `propext` |
| u25 | `joined_not_transitive` | `propext` |
| u25 | `join_no_collision` | `propext` |
| u25 | `transitivity_loss_not_fidelity_obstruction` | `propext` |
| u26 | `finite_negative_checks_suffice` | none |
| u26 | `inequality_relation_irrefl` | none |
| u26 | `empty_carrier_irrefl` | none |

The original native statements keep their axiom reports. The new finite
map proofs use explicit relation cases and named arrow witnesses, with no
choice axiom. Lean library dependencies are separate from properties
assumed about a model's relation.

Python calls the native merge, pushforward, relation enumeration, and
irreflexivity APIs. Unit 26 separately checks all 16 complete two-point
relations against their two diagonal absences. Of the eight positive
extensions of `D2`, two are irreflexive and six are not. Existing populations
of 69 irreflexive records and the three bridge scenarios are preserved.
The four-point transitivity example is a separate supplied case, not a new
member of the historical at-most-three-point census.

Four temporary false claims are rejected by the book runner: an unequal
one-point self-pair, no self-pair in the mixed relation, an invented pushed
shortcut using a false endpoint equation, and absence of the added
self-pair. The [injection record](../../docs/injection_record.md) describes
the exact failures. No native receipt or pin is regenerated under a defect.

## Reproduction and limits

Run `python ci/run_gates.py --job textbook` in the pinned local environment.
This is the textbook job, not all twelve gate families. The PR records its
exact source head and local receipt.

This selected-claim review does not certify all paragraphs, source anchors,
declaration teaching coverage, or substantive/auxiliary classifications.
The remaining formal and research curriculum, hosted rendering, and reader
comprehension, transfer, and retention still need evidence. No general
claim about scientific inference or physical reality follows from these
relation constructions alone.
