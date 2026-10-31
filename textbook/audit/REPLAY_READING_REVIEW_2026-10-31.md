# Replay, attachment, and signed boundaries: reading review

Date: 2026-10-31. AuthorityEffect: None.

## Scope

Selected semantic and readability review of Units 57–61 against the
read-only `InterpreterBoundary`, `ControllerCategory`, `Attachment`,
`RenamingStructure`, `LadderGeneral`, `BoundaryCancellation`, and
`Compression` sources and their existing book drivers. This continues the
[Units 52–56 review](MAPPING_READING_REVIEW_2026-10-29.md).

Four worked openings introduce an indexed note difference, a two-request
controller history, tokens versus positions, and the six signed vertex
contributions of a triangle. The existing compression opening gains a
prediction about reordering its domain. Detailed opening records and the
four older exercise answers are folded. Links lead back to the model map,
Change lab, and Path lab for prerequisites.

The consecutive revised opening route now extends through Unit 61. This
is selected review, not a proof audit of every paragraph or evidence that
a novice can transfer the ideas. File IDs, prerequisite-graph population,
sealed sources, native receipts, and research results remain unchanged.

## Corrections

| Unit | Issue | Correction and source evidence |
|---|---|---|
| 57 | Matched-input notes agreement could be read as global support agreement; the exercise assumed an arbitrary evaluator preserved data under a note-shaped event | At each matched input the diagonal copies that indexed output and appends a note. At index 64 it instead returns its input, while the kernel can admit a fresh token. An arbitrary evaluator need not preserve data. Appending a datum changes any output by increasing its length, independently of its old length. `diag`, `diag_hit`, and the two added book reports establish these scopes. No missing function is identified with the uncoded interpreter role. |
| 58 | The replay counterexample could be mistaken for failure of simulation agreement along its own source replay | The counterexample uses all-on replay on maps whose source disables refusal. The book proves a general controlled-replay equation for any `Sim C1 C2`, and agreement along that replay from an equal starting value. It does not infer agreement along an unrelated controller or on every raw state. The native `Sim.comm` equation supplies the induction step. |
| 59 | Well-formedness conflated endpoint bounds with distinctness; the refusal tag was liable to be read as a diagnosis of an invalid parent | `WFStores` checks bounds only. A raw record containing `(0,0)` can satisfy it while failing `wfPair`. `attachChecked` tests both parent range and liveness: a halted state with an in-range parent also returns `.refusedParent`. The example does not promote every raw record to a reachable state. The pseudocode now says positions are reachable **from** the root, matching `Reaches`. |
| 60 | “Zero” could mean the stored composite boundary list is empty | The triangle's unreduced composite has six terms, while every target coefficient is zero. This is the equality proved by `d2_zero_unrestricted`; a plus-only construction has counterexamples. The opening displays each signed term. |
| 61 | Representative labels could be mistaken for order-independent results | Reordering `[0,1,2]` to `[1,0,2]` changes the shared representative of 0 and 1 from 0 to 1 under `ind 2`. The grouping and recoverability remain. The book report and displayed report counts include this fourth book theorem. |

The root textbook table's Unit 61 row also replaces obsolete theorem
identifiers with the actual native names and states the relevant adequacy,
image, and signature-failure hypotheses. This selected row repair does
not reconcile every other row in that table.

## Book evidence

The five drivers check 180 exact reports: 28, 43, 48, 35, and 26. Eight
are added to the previous 172-report population:

| Unit | Added report | Exact dependencies |
|---|---|---|
| 57 | `diag_support_differs_elsewhere` | `propext, Quot.sound` |
| 57 | `data_append_differs` | `propext, Quot.sound` |
| 58 | `simulation_replay` | `propext, Quot.sound` |
| 58 | `same_start_same_own_replay` | `propext, Quot.sound` |
| 59 | `bounded_self_pairs` | `propext, Quot.sound` |
| 59 | `valid_parent_halted_refusal` | `propext, Quot.sound` |
| 60 | `nonempty_chain_zero_coefficients` | `propext, Quot.sound` |
| 61 | `first_match_order_changes_labels` | none |

Five temporary false versions are rejected by Lean, followed by recovery
of each original driver. They assert global support agreement at the
off-range example, substitute unrelated replay in the general simulation
equation, turn bounded self-pairs into accepted pairs, replace the six-term
list length by zero, and preserve the old representative after reordering.
The [injection record](../../docs/injection_record.md) records these tests.
No native source or receipt is changed by an injection.

## Reproduction and limits

Run `python ci/run_gates.py --job textbook` with the pinned environment.
The PR records the exact clean revision and local receipt. This scoped
job is not the twelve-family merge contract. The PR remains draft for
author review.

Later core Units, per-declaration semantic coverage, research teaching,
hosted layout, and novice transfer and retention remain open. Positive
author reading feedback is retained without assigning a score. None of
the supplied state records, signed constructions, or compression examples
establishes an empirical correspondence or a general law about reality.
