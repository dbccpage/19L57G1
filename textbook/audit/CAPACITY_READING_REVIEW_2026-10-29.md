# Capacity, static strategies, and guarded kernel work: reading review

Date: 2026-10-29. AuthorityEffect: None.

## Scope

Selected semantic and readability review of Units 42–46 against read-only
`Pigeonhole.lean`, `CapacityBound.lean`, `LocalStrategy.lean`, `G1Class.lean`,
`DiffInterface.lean`, `Represented.lean`, `Completion.lean`, their Python
owners, existing artifacts, and book checks. This follows the
[representation and observation review](VIEW_READING_REVIEW_2026-10-29.md).

Five first passes use two-colour windows, parity answers, the three
active-pair conditions, a mark losing an unprotected distinction, and an
exhausted repair menu with two new-column candidates. Formal details and
source classifications are optional; exercise answers are folded.
Titles and current summary tables state the scope. File IDs and the
recorded prerequisite graph are unchanged. Units 04–46 now have concrete
openings throughout that consecutive range; this count is not evidence
of complete semantic coverage or reader mastery.

## Corrections

| Unit | Previous issue | Correction and evidence |
|---|---|---|
| 42 | One library proof's choice dependency attributed to Boolean equality itself | `beq_trap` uses the generic `beq_self_eq_true` proof and retains its isolated dependency report. The book proves the identical `(n == n) = true` proposition without axioms by reducing the selected Boolean instance to decidable equality. The report measures a proof, not the minimum dependencies of all proofs or computation. Native counting code and its dependency boundary are unchanged. |
| 42 | Index-reading called nonlocal without reference to the colouring; one-colour fixture generalized beyond its statement; bound attributed to locality alone | Identity view with identity colours is local at radius 0 but has no finite colour bound. Identity view with constant colour is not local. A new book theorem proves any one-colour local view constant; the native fixture only supplies a constant-view example. Both palette bound and window width count possible windows, while locality carries equality to the view. Output labels need not be numerically bounded. |
| 43 | Unbounded identity-colour examples said outside the whole class; zero-colour hypothesis called vacuous; static fields liable to be read as a running repair process | Identity-valued examples are `LocalStrategy` members outside its fixed-finite-palette subclass. `FiniteDeclaration 0` is impossible; an implication under it is vacuous. Colouring can use arbitrary computation, families and factors can vary by stage, and an import tag does not measure runtime cost. Existing parity and shifting checks retain their exact scope. |
| 44 | Incorrect Unit 29 prerequisite for three active-pair conditions; dense interface opening | The conjunction is introduced by this separate interface. The new table distinguishes retained, protected, and observer-zero. Existing observer-spec checks show an idle closure and a generic closed result can leave active work; no duplicate driver theorem is added. Proposals remain data, not evidence of exhausted alternatives or execution. |
| 45 | Notes treated as literally inert; available augmentation conflated with an executed event; preservation broadened to every old separation | The note event changes the full record while operational support agrees. Progress returns a repair candidate or an augmentation satisfying its structural predicate; budget and license separately gate `step`. With only `(1,2)` recorded, marking 1 in column `[0]` repairs that pair while losing separation of `(0,1)`. This is weaker than Unit 44's refining `ClosureStep`. `WF` checks the recorded endpoints, not every raw-world invariant. |
| 46 | Recorded violation conflated with exhaustive obstruction; a refusal theorem treated as an iff between present record membership and present certificate | `ofWorld_obstruction` maps common-state activity to `violB`; `obstructedB` additionally requires menu exhaustion. Both singleton candidates are retained under the stated target conditions, but execution still has gates. A refusal remains recorded after augmentation resolves the pair and the current exhaustion predicate becomes false. The four preserved verdicts are named; the refusal event itself reads its record for duplicate insertion. |

References to the two-point arrow patterns now lead to Unit 37 rather
than early context-separation units. Requirement guards from the two
models are not silently identified: this world's guard permits both
orientations of distinct admitted pairs. No native source comment or
statement is edited to achieve these corrections.

## Book reports and checks

The five main unit drivers check 146 exact reports. Eight are new:

| Script | Report | Exact library dependencies |
|---|---|---|
| u42 | `beq_without_choice` | none |
| u42 | `identity_local_zero` | none |
| u42 | `identity_colours_unbounded` | none |
| u42 | `constant_colour_not_identity` | none |
| u42 | `one_colour_view_constant` | `propext, Quot.sound` |
| u45 | `note_changes_record_not_support` | `propext, Quot.sound` |
| u45 | `accepted_mark_can_merge_unprotected` | `propext, Quot.sound` |
| u46 | `past_refusal_without_current_certificate` | `propext, Quot.sound` |

The existing isolated `beq_trap` comparison still reports
`propext, Classical.choice, Quot.sound`; it is not a native result or a
change to the native axiom boundary. All eight added reports stay within
the existing native boundary. The separate eight observer-spec reports
are retained in the canonical book job, including the earlier generic
driver and idle-closure examples.

Four temporary false propositions and one temporary proof substitution
exercise the checks. The [injection record](../../docs/injection_record.md)
records their rejection and recovery. The proof substitution is accepted
by the kernel but rejected by the exact report: truth of the proposition
and accuracy of the dependency claim are separate checks. Native owners,
receipts, inventories, and watchlist populations are untouched.

## Reproduction and limits

Run `python ci/run_gates.py --job textbook` in the pinned local environment.
The PR records the clean source revision and receipt. This is the textbook
job, not the twelve-family merge contract; the PR stays draft for the author.

This is selected semantic and readability review of five chapters. Later
formal work, source placement, classification, research teaching, hosted
layout, and novice comprehension, transfer, and retention remain open.
The author's positive reading feedback is retained without assigning a
score. These models do not establish a physical law, an operational
authorization protocol, or universal limits on learning and observation.
