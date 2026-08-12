# CLAUDE.md — Execution Plan

## Repository boundary

- All work uses only this repository. No network research, no external files,
  no prior project instructions, no plugins/agents/skills/memories, no user
  guidance during the derivation.
- `prompt/prompt.md` and `prompt/seed_prompt.md` are read-only inputs and must
  remain byte-identical (SHA-256 recorded in the paper).
- Toolchains already installed on this machine (Python 3.14, pytest, coverage,
  mypy, Lean 4.33 / Lake 5.0 via elan) are metatheoretic apparatus, not inputs.

## Execution plan

1. Verify Python and Lean toolchains compile a trivial file (primary
   directives 1–2). No object-language content in this step.
2. Execute `prompt/seed_prompt.md`:
   - Challenge 0: analyze the initial inscription `<>` with no object-language
     operations; prove exactly what follows and what does not.
   - Challenge 1: analyze the supply of `<a>`; separate supply, mention,
     admission, current-state designation, retention, observation, equality.
   - Challenge 2: analyze the retained pair `<a>`, `<ab>`; prove what changed
     by admission and what remains internally unavailable.
   - Challenge 3: declare a precise meaning of internal separability, prove
     the current regime fails it, enumerate all minimum one-step augmentations
     under a declared candidate space and declared cost measures, count every
     capability each candidate uses, retain all tied non-isomorphic minima.
   - Autonomous continuation: for each surviving branch, define the weakest
     deterministic challenge generator justified by that branch alone; attempt
     fifteen accepted augmentation rounds per finite branch; quotient branches
     only under an implemented isomorphism relation; replay every certified
     result from genesis; export the exact frontier under declared resource
     bounds and prove what is complete within those bounds.
3. Implement the finite reference model in `code/` with tests in `tests/`.
4. Formalize theorem-level claims and countermodels in `lean4/`.
5. Write `paper/paper.md`, `paper/paper_change_log.md`,
   `paper/paper_claim_ledger.md`. Known mathematics appears only in the final
   post-hoc comparison section.

## Assumption discipline

- Every substantive notion is classified as exactly one of: metatheory
  apparatus; supplied object-language datum; externally imposed challenge;
  admitted primitive; derived definition; proved theorem; deterministic
  computation; countermodel; optional realization; conjecture; open
  obstruction; refuted claim.
- The words "forced", "minimal", "free", "canonical", "equivalent",
  "universal", "complete" are used only with a proof or a precise conditional
  scope.
- Presentation identity, internal identity, observational equivalence,
  behavioral separation, and semantic interpretation are kept distinct.
- Supply, mention, admission, current-state designation, retention,
  observation, and equality are never conflated.
- Absence of a test is never converted into equality. A model proposal never
  mutates admitted state without a separately defined admission event.
- Receipts (hashes, test passes, parser success) are never treated as proof of
  an unverified mathematical payload.
- No known theory is targeted or named during the derivation; comparisons
  appear only in the final section of the paper.

## Proof gates

- Every theorem-level claim used by the paper has a Lean 4 proof, or is
  explicitly downgraded to computation, conjecture, countermodel, or OPEN.
- `lake build` passes with no `sorry`, `admit`, user-declared `axiom`,
  `unsafe`, or `partial`.
- Every exported theorem cited by the paper has a `#print axioms` report, and
  any library axiom reliance is recorded in the claim ledger.
- Failed theorem targets remain counterexamples or OPEN — never prose proofs.
- Minimality and necessity claims are proved by exhaustive enumeration over a
  declared finite candidate space, or downgraded to conditional scope.

## Test gates

- Python code in `code/` is deterministic and fully type-annotated; mypy
  passes in strict mode.
- All tests pass; line coverage ≥ 95% and branch coverage ≥ 95% over project
  Python code.
- Negative tests exist for every smuggling or false-minimality failure
  discovered during the derivation.
- Every certified result is replayed from genesis by an implemented replay
  rule; machine-readable branch/level/assumption/claim data is exported.
- Equality, minimality, isomorphism, survivor counts, and proof status are
  decided only by implemented algorithms, never by judgment calls outside the
  code.

## Stopping conditions

- A branch stops when no next challenge or no justified response exists, or at
  the declared resource bound (fifteen accepted augmentation rounds per finite
  branch; deterministic node/arity/cost bounds stated in the paper), with the
  exact frontier exported and a proof of what is complete within the bound.
- The task stops only when: every introduced notion has a source
  classification; every state change has a replayable admission history; every
  theorem-level claim has Lean evidence or is downgraded; every computational
  claim has deterministic Python evidence; all tied minimum branches are
  retained unless eliminated by proof; both coverage thresholds are met; Lean
  builds without forbidden escapes; the working tree is clean with all
  intentional artifacts committed; `prompt/prompt.md` is byte-identical to the
  initial file; and the paper states the strongest defensible terminal result,
  including termination or failure, without targeting a predetermined
  conclusion.
