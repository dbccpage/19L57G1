# Primitive-Difference Up/Down Investigation

## Boundary

This tree is an explicitly non-sealed research surface inside this
repository.  It must not modify or regenerate anything under `prompt/`,
`paper/`, `code/`, `lean4/Derivation/`, or `artifacts/`.

The source modules named in `SOURCE_MANIFEST.json` are read-only inputs.
Their definitions and proved statements may be used only through an explicit
source entry; no unlisted repository material, network material, or prior
report is an input.

## Question

Compare the pinned source boundary with a separate declared finite fixture.
The question is whether an arbitrary native stage alone supplies a replayable
successor, a presentation-stable uniqueness rule, a usable descent, and a
connected trace.  A missing, tied, or admission-dependent step is a boundary
result, not an implicit continuation.

## Current nonclaims

- A read-only source module is not evidence that its inputs were derived here.
- A pointwise extension/closure family is not yet a replayable trace.
- The local Python and Lean fixtures are not formal instances of
  `Derivation.DiffInterface.Stage`, and no bridge to that native type is
  constructed.
- A descent defined only by retaining a certified parent record is not a
  canonical descent for arbitrary larger states or maps.
- The local map laws are identity/composition laws for declared functions;
  this tree does not declare a category, a functor object, an adjunction, or a
  uniqueness quotient under presentation maps.
- The bounded checks in this tree never establish an unbounded tower by
  themselves.

## Assessed result

This tree contains a separate, deterministic finite construction after the
following inputs are declared:

- a two-label initial carrier;
- a seed edge interpreted as the initial positive relation;
- a named anchor in that carrier;
- a next-index fresh-label convention;
- a one-edge successor grammar; and
- a closure rule and replay schedule.

Within that fixture, the lifted functions satisfy identity and composition
laws, and the named descent is a retraction on certified lift records.  The
Lean move-counter schema is proved at every natural index of the declared
schedule; Python replays completed stages 0 through 15.  Neither result
derives the listed inputs, equates the local active-edge counter with the
source obstruction predicate, or establishes an endogenous unique successor.

The scoped evidence and verification limits are in `FINDINGS.md`.  The finite
machine receipt is `receipts/finite_tower_0_15.json`.  The source-boundary
receipt is `verify_manifest.py`; Lean axiom output is separately verified by
`verify_lean.py`, which parses each `#print axioms` line rather than inferring
anything from a plain `lake build`.  Neither verifier is run by CI: both are
manual receipts, and `FINDINGS.md` records the commands and what was run.
