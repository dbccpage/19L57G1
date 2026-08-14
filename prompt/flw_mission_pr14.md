# FLW mission packet — PR14 queue, packets 5 then 2

mission_id: pr14-p5-p2
mode: coding
authority_effect: None
receipt_path: artifacts/primitive_completion_receipt.json

one_sentence: WITHDRAWN 2026-08-14 — the original PR14 objective is stale and is retained below only as historical provenance.

## owned_paths

- lean4/Derivation/ContactKernel.lean
- lean4/Derivation.lean
- paper/paper_change_log.md
- paper/paper_claim_ledger.md
- artifacts/
- tests/test_primitive_contact.py
- tests/test_primitive_receipt.py
- prompt/flw_mission_pr14.md
- contact/analysis/lean_theorem_transport.md

### Amendment 1 (2026-08-14) — recorded after a violation, not before it

The following two paths were **written by PR #20 while outside this list**.
That was a firewall violation, and it is recorded here as one rather than
being backdated into compliance.  The writes are retained rather than
reverted because both files carry the axiom-report count, which the same PR
moved from 1149 to 1151: reverting them would have left the paper
contradicting `artifacts/lean_axioms.txt`.  Retaining an out-of-scope write
is a judgement, not a licence — the entry exists so the judgement is
auditable.

- paper/native_derivation_map.md
- paper/primitive_difference_map.md

### Amendment 2 (2026-08-14) — review-repair scope

The PR #20 review required repairs that no path above can carry: the four
obstruction gates live in `PrimitivePassage.lean`, and the two defects that
allowed the drift (an unbound axiom artifact, an unread transport document)
are closed by new checkers and tests.  Added:

- lean4/Derivation/PrimitivePassage.lean
- ci/regen_axiom_artifact.py
- ci/check_transport_citations.py
- tests/test_axiom_artifact_bytes.py
- tests/test_transport_citations.py
- .github/workflows/verify.yml
- paper/primitive_difference_passage.md

### Amendment 3 (2026-08-14) — depth-`d` outrun

The sealed generator's structural outrun generalized to every fixed
radius, plus the OPEN record for the capacity bound it does NOT prove.

- lean4/Derivation/SeparationCapacity.lean
- contact/analysis/separation_capacity_open.md
- code/derivation/completion.py (namespace registry entry only)

### Amendment 4 (2026-08-14) — root coverage receipt

PR #20 also regenerated the root `coverage.json` outside the original
`owned_paths`.  The write is retained because it records the checked
99.20% line / 96.92% branch baseline used by that repair, and this amendment
explicitly authorizes that path for the review-repair artifact refresh.  Like
Amendment 1, this is an after-the-fact record of the earlier scope violation,
not a claim that the write was authorized when made.

- coverage.json

The paths in Amendments 2 and 3 were listed for their corresponding repair
writes.  Amendments 1 and 4 instead record earlier out-of-scope writes after
the fact and label them as violations.

### Evidence-boundary reconciliation at `de080af`

The original collision/packet-2 audit tracked seven named declarations added
after `ebb1e0b`: `ContactKernel.toDiffObs`, `.toDiffObs_fields`,
`.toDiffObs_apart`, `ContactBridge.collapse_collision_is_pair_blocked`,
`.pair_blocked_iff_collapse_collision`,
`ContactKernel.kernel_from_obs_iff_pair`, and
`.eq_ofDiffObs_of_fields`.  All seven were verified absent at `ebb1e0b`, but
they are not a census of `de080af`: packet 2R, packet 5R, and
`SeparationCapacity` were added later.  The current evidence boundary is
`de080af` plus this repair diff.  The citation checker establishes name and
line-anchor consistency, not commit provenance or a declaration count.

## forbidden_summary

Do not edit prompt/prompt.md or prompt/seed_prompt.md. Do not copy or mutate docs_external_to_this_repo/. Do not invent owned_paths beyond this list. Do not import branded vocabulary into native theorem names or statements. Do not treat comments or names as evidence. Do not close open_kernel_grade without an explicit constructive principle. Do not push origin/main. AuthorityEffect None.

## done_definition — WITHDRAWN 2026-08-14

The entire original acceptance contract is withdrawn as an active mission.
It is preserved here only to make the repair history auditable:

- The Packet 5 bullet was false: `obst_conditions_independent` did not then
  prove four-way independence.  The valid replacement has four gates in the
  proved factorization, while `obstP` itself has the three written factors
  recorded by `obstP_strict_factors`; the four `gate_*_independent` theorems
  carry the independence result.
- The Packet 2 inhabitation and factorization results remain historical
  delivered facts: `kernel_from_obs_iff_pair` and
  `eq_ofDiffObs_of_fields`.  Presentation-grade non-uniqueness is the separate
  `kernel_not_unique_of_pair`; collapsed-observer failure is
  `kernel_no_witness_from_collapse`.
- The former build, axiom-report, receipt, and test bullets describe an earlier
  checkpoint and are not acceptance criteria for the current repair.

## falsifiers

- Claiming the observer record alone determines a kernel
  (`kernel_not_unique_of_pair` — note `pair_choice_load_bearing` does NOT
  carry this; it says only that an arbitrary pair may fail).
- Claiming every observer yields a kernel (kernel_no_witness_from_collapse).
- Treating the iff as uniqueness of endpoints.
- Renaming an OPEN cell into a theorem.
- Writing outside owned_paths.
- Reading a table of verdicts as a factorization theorem (the PR #20 failure).
- Citing `obstP_factors` alone as four-way independence.
- Saying `obstP` itself has four factors.  It has three written factors;
  there are four gates in the proved factorization.
- Treating "no quotient object occurs in the proposition or construction" as
  an axiom-free claim: the fixed-action proof's `funext` step is reported
  under `Quot.sound` by Lean core.
- Regenerating `artifacts/lean_axioms.txt` with a shell redirect (writes CRLF
  on Windows; use `ci/regen_axiom_artifact.py`).

## blockers

none
