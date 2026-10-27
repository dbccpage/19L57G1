# Claims

AuthorityEffect: None.

Statuses: READING (a declared reading of a word, not derived); PROVED_THEOREM
(a Lean declaration named in `TREE_CONTRACT.json`, axioms within
`{propext, Quot.sound}`); VERIFIED_FINITE (checked by `model.py` on the
instances named, nothing beyond them); OPEN.

| Claim | Status | Statement | Evidence |
|---|---|---|---|
| TT-R1 | READING | An actor is a presentation `Nat → Nat` on a carrier `D`; an observer is an evaluator; an institution is a question family; information is `classCount`; knowledge is `FactorsOn D (pQ D Q) q`; wisdom at question level is know-or-witness; the admitted carrier is `List.range r.data`. | `README.md`, Declared vocabulary |
| TT-01 | PROVED_THEOREM | An observer merges two points exactly when they have the same signature on its questions. | `verdictB_false_iff_sigEq` |
| TT-02 | PROVED_THEOREM | Observed separation never holds of a point and itself; a separating view says nothing of a third point. | `sep_irrefl`, `verdict_irrefl`, `sep_witness_ne`, `separation_fact_not_law` |
| TT-03 | PROVED_THEOREM | `Sharp D E p` is Genesis fiber identity, and presentation identity, between `p` and the observer's canonical compression. | `sharp_iff_fiberIdentity`, `sharp_iff_presentationIdentity` |
| TT-04 | PROVED_THEOREM | Any Boolean an observer computes of two points depends only on their signatures; among any `2^m + 1` points an `m`-view observer merges a pair. | `verdict_ceiling`, `resolution_ceiling`, `not_sharp_of_many_fibers` |
| TT-05 | PROVED_THEOREM | An actor on `D` has a sharp `m`-view observer exactly when it has at most `2^m` fibers; the bit observer of its fiber index is one. | `sharp_observable_iff`, `sharp_observable_of_fibers_le`, `not_sharp_observable_of_fibers_gt`, `bitObserver_sharp` |
| TT-05c | VERIFIED_FINITE | TT-05 over every presentation and every `m`-view observer, `|D| ∈ {3, 4}`, `m ∈ {1, 2}`; `bitObserver` sharp in every admitted case. | `model.resolution_check`, `tests/test_model.py::test_resolution` |
| TT-06 | PROVED_THEOREM | An observer is adequate for every question exactly when it separates all distinct carrier points; `m` views cannot on more than `2^m` points. | `absolute_observer_iff`, `no_absolute_observer_of_large_carrier` |
| TT-07 | PROVED_THEOREM | At `(k, d) ∈ {(1,0), (2,0), (3,0), (2,1), (3,1), (2,2)}` Genesis's capacity size `k^(2d+1) + 2d + 2` is exact: forced collision at it, an interior-injective `d`-local view one below it. | `tight_1_0` … `tight_2_2`, `exact_threshold` |
| TT-07c | VERIFIED_FINITE | The window-distinct construction gives an interior-injective colouring one below the size for every `k ≤ 4`, `d ≤ 2` with `k^(2d+1) ≤ 1100`; exhaustive forced collision at the size for `(2,0)`, `(3,0)`, `(2,1)`; the six Lean lists are the construction's output. | `model.tight`, `model.forced_collision_exhaustive`, `test_lean_lists_are_the_construction` |
| TT-07o | OPEN | Exactness of the capacity size for all `k ≥ 1`, `d ≥ 0`. | not in Lean; the construction is general but unproved |
| TT-08 | PROVED_THEOREM | Knowledge is signature determination; members and the actor are known; knowledge is closed under computation and monotone in the institution. | `knows_iff_determined`, `knows_member`, `knows_actor`, `knows_comp`, `knows_join`, `knows_mono` |
| TT-09 | PROVED_THEOREM | Adjoining a question keeps the information exactly when it is known, and raises it strictly otherwise; ignorance has a witness pair and a split. | `knows_iff_information_eq`, `information_lt_of_not_knows`, `not_knows_iff_witness`, `not_knows_iff_split`, `information_known_le`, `information_mono`, `information_le_carrier` |
| TT-10 | PROVED_THEOREM | Known questions and the actor itself add nothing; an institution is an actor with the same information. | `known_extension_inert`, `self_inclusion_inert`, `self_inclusion_information`, `institution_is_actor`, `information_append_of_knows` |
| TT-11 | PROVED_THEOREM | A member is fiber-identical to the institution exactly when it alone knows every member; parity and half on four points exceed each member. | `member_sharp_iff`, `institution_exceeds_members` |
| TT-12 | PROVED_THEOREM | An observer is sharp for an institution's actor exactly when each knows the other's questions. | `sharp_institution_iff_mutual_knowledge` |
| TT-13 | PROVED_THEOREM | The pooled observer merges exactly when the panel certifies non-separation; unanimous separation implies pooled separation, not conversely. | `pooled_merges_iff`, `pooled_merges_iff_certNeg`, `certPos_imp_pooled`, `pooled_not_certPos` |
| TT-14 | PROVED_THEOREM | The information of `m` views is at most `2^m`. | `information_le_resolution` |
| TT-15 | PROVED_THEOREM | For every question, knowledge or a witness pair of ignorance, constructively, on every represented carrier. | `know_or_witness`, `wise_of_represented` |
| TT-15c | VERIFIED_FINITE | TT-08 to TT-13 and TT-15 over eleven families from a four-question pool on four points; panels over every pair of one-view observers on three points. | `model.knowledge_checks`, `model.panel_checks`, `model.mutual_knowledge_check` |
| TT-16 | PROVED_THEOREM | No evaluator on a code set realises every Boolean function of the codes; every catalogue misses its diagonal. | `no_closed_self_interpreter`, `catalogue_incomplete`, `diag_not_member` |
| TT-17 | PROVED_THEOREM | The diagonal of the `mod` catalogue is known on `[0,1,2,3]` to the catalogue of size 3 and unknown to the one of size 2: membership incompleteness is universal, knowledge incompleteness contingent. | `diag_known_witness`, `diag_unknown_witness`, `membership_vs_knowledge` |
| TT-18 | PROVED_THEOREM | For every list of codes there is a world function that differs in support from every coded one (the tower persists operationally). | `tower_persists_operational` |
| TT-18o | OPEN | A denotational bridge to interpreters. | as in the sealed `InterpreterBoundary` |
| TT-19 | PROVED_THEOREM | A merged pair is collapsed under every observer; the constant map collapses every pair and is not faithful on two points. | `collapsed_of_merged`, `constant_collapses_all`, `constant_not_faithful` |
| TT-20 | PROVED_THEOREM | Faithfulness is fiber identity with the identity; the institution's actor is faithful exactly when the institution knows the identity; the empty institution's actor is constant. | `faithful_iff_fiberIdentity`, `faithful_actor_iff`, `empty_actor_constant`, `empty_actor_not_faithful` |
| TT-21 | PROVED_THEOREM | Sharpness transports along every correspondence; a sharp observation through `f` forces `f` to merge only within the actor's fibers; for the identity actor that is faithfulness, and faithfulness suffices. | `verdict_pullback`, `sharp_pullback_iff`, `fiberConstant_of_sharp_pullback`, `faithful_of_sharp_identity`, `sharp_identity_pullback` |
| TT-21c | VERIFIED_FINITE | TT-19 to TT-21 over every map of three points into three letters, every observer of at most two views and every actor. | `model.correspondence_checks` |
| TT-22 | PROVED_THEOREM | Relative to an enumeration of the well-formed contexts, the regime's observer separates admitted data exactly when Genesis declares them separable and merges exactly when collapsed; collapse is signature equality. | `mem_admitted`, `mem_ctxView`, `verdict_regime_iff`, `collapsed_iff_verdict_false`, `collapsed_iff_sigEq` |
| TT-22h | OPEN | The enumeration hypothesis for general regimes is discharged by `Ignition.ctxList` in `research/ignition`, not imported here; proved here for one-unary-form regimes. | `unary_enumeration` |
| TT-23 | PROVED_THEOREM | The regime's observer is sharp for an actor exactly when collapse coincides with its fibers; a regime knows a question exactly when it respects collapse; a regime with `n` contexts has at most `min(2^n, data)` classes; an unadmitted datum lies in no view. | `sharp_regime_iff`, `regime_knows_iff`, `regimeInformation_le`, `not_mem_ctxView_of_unadmitted` |
| TT-24 | PROVED_THEOREM | Verdicts are monotone in views; a regime that collapses a pair an earlier regime separated has lost or altered a view; one rule admission does so on two data. | `verdict_mono`, `recollapse_changes_views`, `R0_separable`, `R0rule_collapsed`, `recollapse_witness`, `recollapse_witness_changes_views` |
| TT-24c | VERIFIED_FINITE | TT-22 to TT-24 on five small regimes with contexts enumerated in Python; view monotonicity over every one-view observer on three points. | `model.bridge_checks`, `model.recollapse_witness`, `model.verdict_mono_check` |
| TT-25 | OPEN | The author's own statements of the two theorems; this ledger is to be re-mapped against them when received. | `README.md`, The two statements |

Lean reach: only the declarations named in `TREE_CONTRACT.json` are
checked by `verify.py`; every one of them reports axioms within
`{propext, Quot.sound}`.  A VERIFIED_FINITE row says the model and the
library agree on the instances named, nothing more.
