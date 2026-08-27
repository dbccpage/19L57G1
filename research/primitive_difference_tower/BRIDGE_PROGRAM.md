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
| B5 | Replayable evidence | Python report, Lean statements, adversarial tests, axiom inventory, and claim ledger agree on the same finite scope. | CI runs the source/receipt relation, tests, and typing; the separate research Lean/axiom receipt remains manual. |

## B1 contract

`bridge_contract.py` supplies the contract used by the later goals.  Its
two-coordinate fixture declares the coordinate swap, the diagonal repair map
`(0) -> (0,0)` and `(1) -> (1,1)`, and residual `(1,0)`.  The residual is not
a boundary in that table, and the boundary image is stable under the swap.
Those are computed facts about supplied data, not an origin story for the
data.

## B2 selection boundary

The residual orbit is exactly `(1,0)` and `(0,1)`, exchanged by the declared
swap.  Exhaustive Python enumeration and
`SymmetryObstructionBridge.residual_orbit_has_no_fixed_singleton` both show
that neither member is fixed.  A singleton can still be used after a labelled
anchor import; the report records that anchor as `ADMITTED`, and does not call
the resulting choice equivariant.

## B3 declared repair boundary

The complete declared repair table has two rows: `(0) -> (0,0)` and
`(1) -> (1,1)`.  `certify_declared_repair_obstruction` enumerates those rows
and rejects an attempted certificate if a modified table already contains the
residual.  The corresponding Lean statement is
`SymmetryObstructionBridge.residual_not_in_declared_boundary_image`.  This is
finite table nonmembership only.

## B4 continuation grammar

`continuation_trilemma.py` permits exactly three kinds of response: an
anchored singleton with a named imported anchor, the complete retained orbit,
or explicit refusal.  If two different anchors are supplied, both branches
are retained in supplied order.  The aggregate and refusal forms expose no
singleton; `SymmetryObstructionBridge.continuation_cases` and
`nonanchored_continuations_have_no_singleton` prove the matching finite Lean
grammar facts.

## B5 replayable receipt

`run_symmetry_obstruction_bridge.py` regenerates
`receipts/symmetry_obstruction_bridge.json` from the declared fixture.  Its
SHA-256 is
`518537CEBCCA2508B443F59036418776E51F3D5285BB4824DEC81E51749A9AB8`.
`verify_manifest.py` regenerates both this receipt and the pre-existing tower
receipt, then requires `CLAIM_LEDGER.md` and `FINDINGS.md` to retain both
receipt hashes and the pinned sealed-source snapshot.  The `research` job runs
this relation on every pull request and push to `main`; it is a CI provenance
and finite-replay gate, not a mathematical proof.  `verify_lean.py` remains a
separate manual Lean/axiom receipt.
