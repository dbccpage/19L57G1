# Claims

AuthorityEffect: None.

Statuses follow the research-tree contract. PROVED_THEOREM: in Lean, axioms
within `propext` and `Quot.sound` (the report is
`lean/ResearchInstitutionForces/AxiomReport.lean`). VERIFIED_FINITE: computed
exhaustively over the stated bound by `model.py` and silent outside it.
CONDITIONAL: under a named admission. OPEN: neither proved nor refuted.
REFUTED: a witness against a stated reading, in Lean where the row says so. A
VERIFIED_FINITE row never upgrades a theorem, and a passing test is never
cited for a PROVED_THEOREM row. `Joint.`, `Robust.`, `Staleness.` and
`Ballot.` abbreviate the namespaces under `ResearchInstitutionForces`;
AI-numbers refer to `research/actor_institution/CLAIMS.md`, TT-numbers to
`research/two_theorems/CLAIMS.md`. L0 to L3 are the lemmas of the operator's
plan of 2026-11-06, section 3.3 and section 2.

The finite bound, for every VERIFIED_FINITE row unless the row says
otherwise: carrier `[0, 1, 2, 3]`; seats are the 16 Boolean tables; every
ordered list of at most three seats, repetition allowed (4369 institutions);
questions and targets are the 16 Boolean tables.

| Claim | Status | Statement | Evidence |
| --- | --- | --- | --- |
| IF-00 | PROVED_THEOREM | L0. A family `F` knows `q` on `D` exactly when the one-member family of its joint presentation `pQ D F` does; reading a family through its joint presentation twice changes nothing. The information side is TT `institution_is_actor`. | `Joint.knows_family_iff_joint`, `Joint.knows_joint_idem` |
| IF-00c | VERIFIED_FINITE | L0 on every subset of `[0, 1, 2, 3]` as carrier (16), every institution of the bound and every Boolean question: 1118464 cases, no violation. | `model.l0_check`, `tests/test_model.py::test_l0_joint_presentation` |
| IF-01 | PROVED_THEOREM | Separation redundancy `redundancy Q x y`, the number of seats separating `x` from `y`, is additive over appended lists, symmetric, bounded by the number of seats, and positive exactly when some seat separates the pair, exactly when the signatures differ. `Q` knows `q` exactly when every pair that `q` separates has at least one separating seat. | `Joint.redundancy_append`, `Joint.redundancy_symm`, `Joint.redundancy_le_length`, `Joint.redundancy_pos_iff`, `Joint.redundancy_pos_iff_not_sigEq`, `Joint.redundancy_zero_iff_sigEq`, `Joint.knows_iff_redundancy`; `Joint.sepCount_le_one`, `Joint.sepCount_eq_zero`, `Joint.sepCount_eq_one`, `Joint.redundancy_nil`, `Joint.redundancy_cons` |
| IF-02 | PROVED_THEOREM | A duplicate is a seat. A separating presentation listed twice raises the redundancy of the pair by one, and the family with the duplicate knows exactly what the family without it knows. | `Joint.duplicate_counts_twice`, `Joint.duplicate_knows_inert` |
| IF-03 | PROVED_THEOREM | L1, replacement. Every family obtained from `Q` by replacing at most `k` seats with arbitrary presentations knows `q` on `D` exactly when every pair of `D` that `q` separates has at least `k + 1` separating seats in `Q`. Necessity replaces each separating seat of the weak pair by a constant. | `Robust.robust_iff`; `Robust.repl_refl`, `Robust.repl_mono`, `Robust.repl_length`, `Robust.redundancy_le_repl`, `Robust.repl_blunt`, `Robust.sigEq_blunt`, `Robust.repl_zero_aux`, `Robust.repl_zero` |
| IF-04 | PROVED_THEOREM | L1, deletion. Every family obtained from `Q` by deleting at most `k` seats knows `q` exactly when the same count holds: the threshold for deletion equals the threshold for replacement. | `Robust.deletion_robust_iff`; `Robust.del_mono`, `Robust.redundancy_le_del`, `Robust.del_agreeing`, `Robust.sigEq_agreeing` |
| IF-05 | PROVED_THEOREM | The L1 condition is a Boolean computation over the carrier. On four points `[parity, half]` knows the identity at `k = 0` and not at `k = 1`; the duplicated family at `k = 1` and not at `k = 2`. | `Robust.robustB_iff`, `Robust.robust_parity_half` |
| IF-03c | VERIFIED_FINITE | L1 for replacement by Boolean tables and for deletion, for every institution of the bound, every Boolean question and every `k` from 0 to 3: 279616 cases, 78932 of them robust, no violation. | `model.l1_check`, `tests/test_model.py::test_l1_replacement_and_deletion_thresholds` |
| IF-06 | PROVED_THEOREM | L2 (a). Adding seats never breaks a decision; knowledge depends on the seats as a set, so any removal can be written as `K ++ R`. | `Staleness.add_preserves`, `Staleness.knows_congr_mem` |
| IF-07 | PROVED_THEOREM | L2 (b), removal and corruption, corrected. The kept seats `K` of `K ++ R` know `q` exactly when every `q`-separated pair has fewer separating seats in `R` than in `K ++ R`. The decision survives every replacement of the seats `R` (relabellings included) exactly when `K` alone knows `q`. The plan's count of `R`-many-plus-one seats per pair is sufficient for every removal of that size (IF-04) and not necessary for a particular one: removing a constant seat from `[id, const]` on two points keeps the decision although the pair has one seat. | `Staleness.removal_iff`, `Staleness.seat_corruption_iff`, `Staleness.relabel_of_kept`, `Staleness.sigEq_append_consts`, `Staleness.removal_count_not_necessary`, `Staleness.sigEq_symm` |
| IF-07c | VERIFIED_FINITE | L2 (b) for every institution of the bound, every set of removed seats and every Boolean question: the kept seats know `q` exactly when the count holds, and the decision survives every Boolean replacement of the removed seats exactly when the kept seats know `q`; 541200 cases, no violation. | `model.l2_removal_check`, `tests/test_model.py::test_l2_removal_and_seat_corruption` |
| IF-08 | PROVED_THEOREM | A particular bijective relabelling of one seat is not decided by counts. On four points `[parity, half]` knows the identity; relabelling `parity` by the swap of 0 and 2 keeps that although `[half]` alone does not know it; relabelling by the swap of 1 and 2 destroys it. | `Staleness.relabel_can_be_harmless`, `Staleness.relabel_can_break` |
| IF-08r | REFUTED | The plan's L2 (b) read for one particular relabelling (F3): "the relabelling preserves the decision iff the L1 condition holds for the affected seats". Witness: the swap of 0 and 2 inside `parity` preserves knowledge of the identity on four points while the unaffected seat `half` separates neither the pair 0, 1 nor the pair 2, 3, so the count fails for the affected seat. The worst-case reading is true (IF-07). | `Staleness.relabel_can_be_harmless` |
| IF-09 | PROVED_THEOREM | L2 (c). Given `Knows D Q q`, the decision holds on `D ++ [x]` exactly when `q` is constant on the signature class of `x` in `D ++ [x]`. On `[0, 2]`, `[half]` knows `parity`; adding the point 1 breaks it. | `Staleness.extension_iff`, `Staleness.extension_breaks` |
| IF-09c | VERIFIED_FINITE | L2 (c) for every carrier strictly inside `[0, 1, 2, 3]`, every new point, every institution of the bound and every Boolean question known on the carrier: 2128688 cases, 197640 of them broken by the extension, no violation. | `model.l2_extension_check`, `tests/test_model.py::test_l2_carrier_extension` |
| IF-10 | PROVED_THEOREM | L2 (d). Admitting a target `t` as a seat never breaks a decision and makes agreement with `t` known. On two points the empty institution knows the constant 0, which fails the target `id`; with the target seated, the decision and the agreement question are both known. A target declared but not seated changes nothing, because `Knows` has no target argument; that is a remark about the definition, not a theorem. | `Staleness.target_member_preserves`, `Staleness.decision_holds_target_fails` |
| IF-10c | VERIFIED_FINITE | L2 (a) and (d) for every institution of the bound, every known Boolean question and every Boolean target: the extended family knows the question and the agreement question; 744544 cases, no violation; 698010 of them are decisions failing their target. | `model.l2_add_and_target_check`, `tests/test_model.py::test_l2_addition_and_targets` |
| IF-11 | PROVED_THEOREM | L3, per-seat ballot maps. If every member of `B` is known by `Q`, whatever `B` knows `Q` knows. Hence with one ballot map per seat (`ballots` pairs them in order and stops at the shorter list), and with one map for every seat, what the ballots know the seats know; a rule that sees one tally knows at most what the ballots know. | `Ballot.knows_of_known_members`, `Ballot.mem_ballots`, `Ballot.ballot_known`, `Ballot.ballot_compression`, `Ballot.uniform_ballot_compression`, `Ballot.tally_known`, `Ballot.tally_compression` |
| IF-12 | PROVED_THEOREM | The sincere ballot of a seat (AYE or NAY where the question is settled on the seat's class, ABSTAIN elsewhere) is known by that seat alone, so L3 covers sincere ballots. | `Ballot.sincere_known`, `Ballot.sincere_compression`, `Ballot.settledAt_eq`, `Ballot.settledAt_congr` |
| IF-13 | PROVED_THEOREM | The converse of L3 fails. On four points `[parity, half]` knows `xorPH` and no seat alone does; both sincere ballots on `xorPH` are ABSTAIN at every point, and those ballots do not know `xorPH`. An injective ballot map loses nothing on the same family. | `Ballot.ballot_loses_exceeding`, `Ballot.injective_ballot_keeps` |
| IF-13r | REFUTED | The plan's L3 sentence "any ballot map that is constant on a member's classes loses exceeding knowledge that pooling keeps". Every ballot `f ∘ m` is constant on the classes of `m`, and the injective ballot of IF-13 keeps the exceeding knowledge of `xorPH`. | `Ballot.injective_ballot_keeps`, `Ballot.ballot_loses_exceeding` |
| IF-13c | VERIFIED_FINITE | L3 for every institution of the bound, every choice of ballot maps from the seat's two values to three ballot values (nine per seat) and every Boolean question: 48109840 cases, no violation, 10465788 strict losses. Sincere ballots on each Boolean question, 69904 cases: each is a function of its seat, they and every tally of them know no more than the seats, and they lose the question in 2928 cases, every one of them a case where the family knows it and no single seat does. | `model.l3_check`, `tests/test_model.py::test_l3_ballot_compression` |
| IF-14 | PROVED_THEOREM | The re-review rule. A decision needs re-review on removal, on relabelling, on carrier extension and on a newly admitted target, and never on an added seat alone: the last is IF-06, and each of the others breaks a decision on a named witness. | `Staleness.add_preserves`; `ResearchActorInstitution.Inst.consensus_after_loss` (AI-06), `Staleness.relabel_can_break`, `ResearchActorInstitution.Inst.correspondence_matters` (AI-04), `Staleness.extension_breaks`, `Staleness.decision_holds_target_fails` |
| IF-15o | OPEN | Robustness against capture of sources rather than seats. The count of IF-03 is per seat; when several seats copy one source, the relevant count is of separating sources, which needs an admitted map from seats to sources. No such map is defined here. | not in Lean |
| IF-16o | OPEN | L2 (b) for bijective relabellings only: the exact condition under which every bijective relabelling of the seats `R` preserves a decision. IF-07 quantifies over every replacement; IF-08 shows the bijective case differs: there the count condition is sufficient and not necessary. A seat injective on the carrier is a second kind of counterexample to necessity, since every bijective relabelling of it stays injective. | not in Lean |
| IF-17o | OPEN | A price for the admission `ScopedSound` of AI-13, which this tree does not use. The plan asked that it be priced or recorded as unpriced; it is recorded unpriced in `AUDIT.md`, and no price is derived. | `AUDIT.md`, Admissions |
| inputs | VERIFIED_FINITE | The pinned consumed research modules are exactly the outside imports of every module of `lean/`, and their files exist. Unchanged contents are not checked: no digests are pinned. | `tests/test_model.py::test_imports_are_the_pinned_research_modules`, `tests/test_model.py::test_consumed_modules_exist` |
| reach | VERIFIED_FINITE | Every `theorem` of the four modules is named in the axiom report and in `TREE_CONTRACT.json`, in file order, with no duplicate: 59 names. | `model.theorem_names`, `tests/test_model.py::test_axiom_report_covers_every_theorem_and_matches_contract` |
| fast form | VERIFIED_FINITE | The bitmask form of knowledge used by the heavier checks agrees with the definition read directly, on every carrier for every family of at most two seats and on the full carrier for every family of three: 135424 cases, no violation. | `model.fast_form_check`, `tests/test_model.py::test_fast_form_agrees_with_the_definition` |

Cross-check, reported and not reproduced here. The coordinating session
reported on 2026-11-06 that an exhaustive Rust check in the engine repository
(its pull request 1509; 4369 institutions and 16 questions on `[0, 1, 2, 3]`)
finds L1, L2 (a), L2 (c) and L3 holding, and narrows two of the plan's
statements in the same way as this ledger: L2 (b) is exact for removal and for
relabelling by arbitrary maps (IF-07) and only sufficient for bijective
relabellings (IF-08, IF-08r, IF-16o); L2 (d) leaves `Knows` unchanged only for
a target that is not seated, and a seated target can only enlarge what is
known (IF-10). That check is not a receipt of this tree: its command, tool
versions and exit status were not seen here, and no row above cites it.

Lean reach: exactly the 59 theorems named in `TREE_CONTRACT.json`, which are
every `theorem` of the four modules. Definitions and the two inductive
relations are not reported. This is not a census of every compiled constant.
