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

## forbidden_summary

Do not edit prompt/prompt.md or prompt/seed_prompt.md. Do not copy or mutate docs_external_to_this_repo/. Do not invent owned_paths beyond this list. Do not import branded vocabulary into native theorem names or statements. Do not treat comments or names as evidence. Do not close open_kernel_grade without an explicit constructive principle. Do not push origin/main. AuthorityEffect None.

## done_definition

- Packet 5 audit recorded: obst_conditions_independent remains the four-conjunct independence theorem; no new Lean.
- Packet 2: ContactKernel.kernel_from_obs_iff_pair states existence of a same-data kernel iff a non-zero pair exists; eq_ofDiffObs_of_fields recovers ofDiffObs at the kernel endpoints.
- #print axioms lines added; lake build clean; axiom reports within {propext, Quot.sound}.
- Receipt and ledger cite the new lemma with exact scope (existence/factorization, not uniqueness of the kernel).
- Tests pass.

## falsifiers

- Claiming the observer record alone determines a kernel (pair_choice_load_bearing).
- Claiming every observer yields a kernel (kernel_no_witness_from_collapse).
- Treating the iff as uniqueness of endpoints.
- Renaming an OPEN cell into a theorem.
- Writing outside owned_paths.

## blockers

none
