# Maps, interfaces, and relation laws: reading review

Date: 2026-10-29. AuthorityEffect: None.

## Scope

Selected semantic and readability review of Units 52–56 against read-only
`PrimitiveCats.lean`, `PrimitiveContact.lean`, `PrimitivePassage.lean`,
`HigherStructure.lean`, `Apartness.lean`, and relevant `ContactBridge.lean`
statements, existing Python owners, artifacts, and book checks. This
follows the [panels and generation review](PANEL_READING_REVIEW_2026-10-29.md).

Five concrete openings teach a collapsing map, a directed relation versus
an observer complement, the four passage conditions, one supplied growth
round, and two distinct red cards that agree under a colour relation.
Detailed source records are optional and exercise answers folded. The
consecutive concrete opening route now covers Units 04–56. This is selected
review, not exhaustive semantic coverage or evidence of novice mastery.

The earlier Unit 54 paragraph distinguishing refinement from licensed
column creation is preserved literally. File IDs, the prerequisite graph,
historical inventories, sealed sources, native receipts, and research
results are unchanged.

## Corrections

| Unit | Previous issue | Correction and evidence |
|---|---|---|
| 52 | The initial object called the smallest witnessed carrier; symmetric targets treated as necessary; a free-point example generalized | A one-point loop is also a pointed witnessed relation and receives the collapsing map. Initiality concerns permitted maps, not size, chronology, or preservation of inequality. A map from the symmetric source exists exactly when the designated target pair has its reverse edge. A three-point target has that edge while another edge has no reverse, so global symmetry is sufficient but unnecessary. Larger-object claims retain their named-family scope. |
| 53 | The designated example liable to be identified with the entire interface; a status label or proof equality liable to be read as payload evidence or provenance | The native class has oriented and symmetric members. The oriented relation is not an observer's zero complement; a symmetric member is representable, by the existing scoped bridge theorem. This does not forbid recording direction in a separate value or relation. Status strings are declared records. Source definitions establish the re-export; equality of proofs alone does not, because of proof irrelevance. |
| 54 | A new-column proposal liable to be read as every accepted column; replay described without naming its fixed inputs | The extension universe is singleton columns over admitted positions. A two-position column can pass `colOk` while absent from the menu. Replay requires its starting state and fixed interpreter. The two-rule statement names distinct endpoints, first-endpoint range, and protected membership; no execution guard is bypassed. The author's licence/refinement distinction remains intact. |
| 55 | Natural-number indexing described as running forever; a purported count example compared two orientations of the same disconnected triangle | Describe finite histories indexed by Lean natural numbers and completed stages. The revised book check compares a four-position path with a triangle plus an isolated fourth position, both with residue 1, and checks that no triangle edge touches position 3. It does not define or prove a general connectivity theorem. Drivers, higher cells, and boundary signs remain declared apparatus. |
| 56 | Negation described as inability to assert; sufficient laws presented as converse implications; minimality generalized beyond the explicit carrier theorem | Proved not-apart is logical negation, not missing evidence. Derive its transitivity directly by contradiction using cotransitivity, without reversing a constructive implication. The three laws suffice; the examples show omissions can fail. The small-carrier evidence names subsingletons and `Bool`. Colour agreement gives an equivalence that can group distinct positions. |

## Book evidence

The five unit drivers check 178 exact reports: 39, 19, 44, 41, and 35.
Six reports are added:

| Script | Report | Exact dependencies |
|---|---|---|
| u52 | `symmetric_source_map_iff` | none |
| u52 | `global_symmetry_not_required` | `propext` |
| u53 | `symmetric_member_representable` | none |
| u54 | `singleton_menu_not_all_columns` | `propext, Quot.sound` |
| u56 | `colour_isApart` | none |
| u56 | `colour_agreement_not_identity` | `propext` |

The strengthened existing `u55.residue_blind` statement now checks
`propext, Quot.sound`; its previous count-only equality reported none.
This changes a book example's statement and dependency report, not a
native theorem or native dependency boundary. The colour model proves
properties of a declared code relation, not an empirical classification.

Five temporary false claims exercise global symmetry, orientation of the
symmetric member, accepted nonsingleton columns, the isolated position,
and identity from colour agreement. The
[injection record](../../docs/injection_record.md) records rejection and
recovery. No native receipt is regenerated under an injected claim.

## Reproduction and limits

Run `python ci/run_gates.py --job textbook` in the pinned local environment.
The PR records the clean revision and receipt. This is the textbook job,
not the twelve-family merge contract; the PR remains draft for the author.

Further chapter review, research teaching, hosted layout, and novice
transfer and retention remain open. Positive author reading feedback is
retained without assigning a score. The mathematical maps and admitted
growth rules do not establish chronology, measurement correspondence,
physical space, or universal autonomous growth.
