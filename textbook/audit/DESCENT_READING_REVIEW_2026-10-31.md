# Descent, selection, and consistent renaming: reading review

Date: 2026-10-31. AuthorityEffect: None.

## Scope

Selected semantic and readability review of Units 67–74 against their
read-only source definitions and existing book drivers. The relevant
owners are `ObsDescent`, `ContactBridge`, `ContactKernel`,
`PresentationNaturality`, `PresentationRelativity`, `ClosureSymmetry`,
`ResidualClosure`, the five fidelity modules, `Breaking`, `Composing`,
and the parked form/isomorphism modules. This follows the
[Units 62–66 review](PROTECTION_READING_REVIEW_2026-10-31.md).

Seven worked openings replace short abstract summaries. Unit 71 retains
its earlier numerical first pass and gains a duplicate-question
prediction. All eight Units now have prediction checkpoints and folded
older exercise answers. Source records and formal opening summaries are
optional where present. The revised concrete opening sequence reaches
the last core Unit, 74; this does not establish complete semantic teaching
coverage, adequate prerequisites for every declaration, or novice mastery.

## Selected findings and examples

| Unit | Finding or density problem | Revision and evidence |
|---|---|---|
| 67 | Class constancy and paired views were stated abstractly | A two-row table shows a constant answer descending through the single class of `collapseAllObs`, while identity and the paired view fail. The existing `collapseAll_flagship` proves the contrast. |
| 68 | The two directions and their different decision assumptions were introduced before an example | Red/red/blue cards show the zero classes and complement cotransitivity. `color_bridge_table` checks the finite example. In the abstract direction, zero decidability remains a hypothesis; the reverse construction and its relation round trip retain their distinct assumptions. |
| 69 | The opening checklist omitted the diagonal-zero proof field, and the question suggested a largest common structure | The opening now states the diagonal-zero law and designated nonzero endpoints. The asymmetric `boolKernel` table shows why this interface does not supply observer symmetry. An inhabited observer needs an actual nonzero pair to supply a kernel. The question asks about the declared common interface; no general maximality assertion is inferred. |
| 70 | The first pass discussed choosing a point although the actual output is an ordered nonzero pair | The two admissible ordered Bool pairs are exchanged by `negIso`. An explicit choice is possible but not natural; the unordered pair of both points is a different output and is fixed. The four-point positive example keeps the obstruction scoped to its actual family. |
| 71 | A failed comparison needed a prediction about an ineffective repair | Duplicating the old question preserves two classes; adjoining the new question yields three in the existing example. `three_item_refinement_counts` checks all counts. The finite numerical domain and directional factorization remain explicit. |
| 72 | The question inaccurately attributed generic carriers to Unit 71; local round trips and network loops were easy to conflate | The cross-reference now states Unit 71's `List Nat`/numerical scope. A two-row flip/identity translation table fails round trips despite bijective individual maps. Flip/flip repairs the local round trips, yet the existing one-step self-loop changes an item. The book checks the exact local and loop values and retains the native no-faithful-network-descent result. The old two-step comment is corrected. |
| 73 | Abstract selector conditions and a separate composition relation arrived together | A constant-side/swap table distinguishes orbit constancy from equivariance. Identity has the opposite combination. The empty-carrier case preserves the inhabitant hypothesis. A separate paragraph distinguishes allowing two composites from selecting one; the native `allCompose` example admits a total selector without uniqueness. |
| 74 | Form indices, arities, datum indices, and comparison hypotheses were introduced together | The two-form swap updates arities, instances, and rules while keeping datum 0 fixed. A book counterexample proves that the raw record with requirement `(2,0)` has no self-`Iso`; the ordered-requirement hypothesis is material. List multiplicity, record equality, and budget-limited Python search remain separate. |

The root textbook map's rows 67–74 now use checked source identifiers and
explicit scope notes. In particular the native uniqueness hypothesis is
`DeltaOnto` plus equal carrier maps, rather than the obsolete `VHomOnto`
label. The row for Unit 71 matches its current title and numerical source.
This does not reconcile every earlier curriculum reference.

## Book evidence

The eight drivers check 302 exact reports: 24, 34, 59, 34, 34, 41, 27,
and 49. Eight reports are added to the previous 294-report population:

| Unit | Added report | Exact dependencies |
|---|---|---|
| 68 | `color_bridge_table` | `propext` |
| 69 | `boolKernel_table` | none |
| 70 | `ordered_pair_swap_table` | none |
| 71 | `three_item_refinement_counts` | none |
| 72 | `round_trip_and_loop_table` | none |
| 73 | `chosen_side_swap_table` | none |
| 74 | `form_swap_table` | `propext` |
| 74 | `unordered_no_self_iso` | `propext, Quot.sound` |

Nine temporary false versions are rejected by Lean, followed by recovery
of all eight original drivers. See the
[injection record](../../docs/injection_record.md). The colour example
exposes its finite comparisons before computation; it does not add a
classical decision principle for arbitrary observers. No native source,
receipt, fixed vocabulary population, or research result is changed.

## Reproduction and limits

Run `python ci/run_gates.py --job textbook` with the pinned environment.
The PR records the exact clean head and local receipt. The textbook job
is not the twelve-family merge contract; author merge control is retained.

The review improves examples and selected hypotheses. Per-declaration
semantic coverage, wider research teaching, hosted layout, novice
comprehension, transfer, and retention remain open. The author's positive
reading feedback is retained without a score. None of the supplied
colour tables, comparison rules, translations, or symmetries establishes
a correspondence with a physical system merely by having a formal model.
