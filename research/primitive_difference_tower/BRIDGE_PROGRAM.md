# Five-goal symmetry--obstruction--repair bridge

## Scope

This programme is a finite bridge on top of PDT-0--PDT-8.  It does not
construct its carrier, symmetry, repair differential, residual, or response
grammar from a native `Derivation.DiffInterface.Stage`.  Every one of those
objects remains an explicitly typed input until a later theorem proves a
specific relation to another input.

The word *obstruction* below means only non-membership in a declared finite
repair image.  It does not mean nonzero general `H1`, a physical defect, or an
instruction to add structure.

## Goals

| Goal | Deliverable | Success condition | Nonclaim |
|---|---|---|---|
| B1 | Finite bridge contract | Presentation labels, involution, repair table, residual, and provenance validate independently. | The contract does not generate any input. |
| B2 | Equivariant-selection boundary | The displayed swap orbit has no invariant singleton selection, with an explicit anchored positive alternative. | No universal no-selector theorem. |
| B3 | Declared-repair obstruction | The displayed residual is outside the declared boundary image, while the image is symmetry-stable. | No theorem about a different repair grammar or general cohomology. |
| B4 | Continuation trilemma | The declared candidate grammar classifies anchored singleton import, full-orbit retention, and refusal; no category is silently selected. | No claim that an obstruction creates its own continuation. |
| B5 | Replayable evidence | Python report, Lean statements, adversarial tests, axiom inventory, and claim ledger agree on the same finite scope. | Manual receipts remain manual unless a future CI contract explicitly adopts them. |

## B1 contract

`bridge_contract.py` supplies the contract used by the later goals.  Its
two-coordinate fixture declares the coordinate swap, the diagonal repair map
`(0) -> (0,0)` and `(1) -> (1,1)`, and residual `(1,0)`.  The residual is not
a boundary in that table, and the boundary image is stable under the swap.
Those are computed facts about supplied data, not an origin story for the
data.
