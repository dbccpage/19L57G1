# FLW mission packet — PR14 queue, packets 5 then 2

mission_id: pr14-p5-p2
mode: coding
authority_effect: None
receipt_path: artifacts/primitive_completion_receipt.json

one_sentence: Audit obst_conditions_independent as already proved, then add the reusable pair-choice necessity lemma for observer→kernel.

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

Every path in both amendments is listed BEFORE the writes in this repair,
except the two in Amendment 1, which are listed after and labelled as such.

## forbidden_summary

Do not edit prompt/prompt.md or prompt/seed_prompt.md. Do not copy or mutate docs_external_to_this_repo/. Do not invent owned_paths beyond this list. Do not import branded vocabulary into native theorem names or statements. Do not treat comments or names as evidence. Do not close open_kernel_grade without an explicit constructive principle. Do not push origin/main. AuthorityEffect None.

## done_definition

- Packet 5 audit recorded: obst_conditions_independent remains the four-conjunct independence theorem; no new Lean.
- Packet 2: ContactKernel.kernel_from_obs_iff_pair states existence of a same-data kernel iff a non-zero pair exists; eq_ofDiffObs_of_fields recovers ofDiffObs at the kernel endpoints.
- #print axioms lines added; lake build clean; axiom reports within {propext, Quot.sound}.
- Receipt and ledger cite the new lemma with exact scope (existence/factorization, not uniqueness of the kernel).
- Tests pass.

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
- Regenerating `artifacts/lean_axioms.txt` with a shell redirect (writes CRLF
  on Windows; use `ci/regen_axiom_artifact.py`).

## blockers

none
