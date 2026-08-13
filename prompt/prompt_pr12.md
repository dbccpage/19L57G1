# PR #12 run inputs (recorded)

This file records the externally supplied inputs of the PR #12 run
("Primitive Difference Contact and Passage").  Inputs 1 and 3 are
verbatim; Input 2 is summarized here and preserved byte-exact in
`prompt/ultra_prompt_pr12.md`.  The completion receipt carries the
SHA-256 of both files.  Three inputs arrived, in order.

## Input 1 — framing instruction (run start)

> Create a dynamic workflow to complete this prompt and ensure the
> final result is a derivation of the primitive difference, show it
> to be the first obstruction forced to self-resolve or create
> structure and then demonstrate the growth of the first graph, the
> 0,1,3, and 3 simplices and record the process responsible for the
> structure creation. Name any invariants you discover and any
> mathematical objects identical to known math.

ASSUMED_TYPO_CORRECTION: the caller's literal "0,1,3, and 3
simplices" is read as "0, 1, 2, and 3" — the run demonstrates all
four dimensions.  The reading is an assumption, labeled as such, not
a record of the caller's bytes (which are preserved above).

## Input 2 — the ultra prompt (run start)

The FULL VERBATIM BYTES of the ultra prompt are committed as
`prompt/ultra_prompt_pr12.md`; the completion receipt binds that
file's SHA-256.  This file is the run-input summary, not the byte
record.  Head of the prompt, for orientation:

# 19L57G1 Ultra Run — Primitive Difference Contact and Passage

Run this as one autonomous **ultra-mode workflow** after PR #11 is
corrected, merged, and `main` is green.

This is not another estate-summary run. It is the collision and
passage run:

1. identify the strongest native object that deserves the name
   **Primitive Difference**;
2. prove its true universal or non-universal status;
3. collide it with the supplied external Primitive Difference Lean
   development without deferring to either side;
4. build the strongest common replacement;
5. pass from Primitive Difference through presentation, observation,
   obstruction, repair/refusal/extension, replay, and represented
   continuation;
6. determine exactly where the remaining interpreter boundary lies.

Continue until the theorem lattice closes or a smallest named
obstruction remains. Do not stop after one equivalence, one
countermodel, or one attractive definition.

Do not ask the user questions. Do not wait for guidance. Branch on
genuine alternatives and return the strongest defensible terminal
result.

[Summary of sections 0–18 — the byte record is
`prompt/ultra_prompt_pr12.md`: the
preconditions and repository discipline (branch, research PR,
blind-native-base tag, sealed PRs #1–#11, contact package protocol
with CONTACT_MANIFEST.json and the lean4-before-prose reading order,
and the absence rule "complete the native phases and terminate with
CONTACT_INPUT_ABSENT; do not invent its contents"); the evidence
classes; the twelve PR #11 audit items; the final research question
and its eleven sub-questions; Phase I (correction ledger, §4.1–4.6);
Phase II (native candidates PD-A…PD-F, implication lattice, minimum
carrier and true universal property, orientation fork); Phases
III–IV (contact collision protocol, Lean before prose); Phase V
(common kernel outputs); Phase VI (the passage chain and theorems
P1–P8); Phase VII (genuine controller category and initiality test);
Phase VIII (interpreter boundary I0–I5); Phase IX (earliest higher
structure); §13 deterministic Python requirements; §14 Lean
requirements; §15 papers, maps, and receipts; §16 adversarial
obligations (twenty attacks); §17 exact terminals; §18 definition of
done.]

## Input 3 — caller directive (mid-run, after the passage commit)

> Working only in your native vocabulary, define a positive apartness
> structure with irreflexivity, symmetry, and cotransitivity. Define
> indistinguishability as the negation of apartness and prove it is
> an equivalence. Prove by finite countermodels that bare assertion
> and irreflexivity alone are insufficient. For the oriented
> two-point relation, separate the retained orientation from the
> symmetric apartness used to form indistinguishability. Then
> characterize exactly which admitted operations preserve the
> retained oriented witness. Do not introduce observers, quotients,
> repair terminology, or claims of forced extension until the
> required structure has been proved.

Discharged by `lean4/Derivation/Apartness.lean`,
`code/derivation/apartness.py`, `artifacts/apartness.json`
(commit "Apartness refinement").

## Supersession note

Input 1 explicitly requests naming "any mathematical objects
identical to known math."  This supersedes, for this run only, the
2026-08-11 caller correction that withheld the post-hoc comparison:
the comparison appears in exactly one clearly marked, derivation-inert
section (`paper/primitive_difference_map.md`, final section), and
nowhere in the Lean or Python sources.
