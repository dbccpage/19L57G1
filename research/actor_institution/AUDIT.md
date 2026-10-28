# Derivation audit

AuthorityEffect: None. One row per group of declarations, answering the
brief's Part VI: what each depends on, whether it is admitted or derived,
whether it holds on a finite carrier only, which external functions it takes,
the smallest model that falsifies its negation (or shows its bound is tight),
whether it is invariant under renaming the carrier, and where the Python model
reproduces it. "Metatheory" marks a quantifier or type that belongs to Lean,
not to the system.

| Declarations | Depends on | Admitted / derived | Finite carrier | External function or observer | Smaller falsifying model | Renaming | Python |
|---|---|---|---|---|---|---|---|
| `Inst.Exceeds`, `exceeds_iff`, `sigEq_single`, `not_knows_single_iff` | `Knows`, `SigEq`, `knows_iff_determined` (TT) | definition admitted; equivalence derived | any `D : List Nat` | none; `Q`, `q` are metatheory quantifiers | — | `knows_rename` | `model.exceeds` |
| `exceeds_two_members`, `exceeds_three_data`, `no_exceeding_on_two_points`, `no_exceeding_single_member`, `exceeds_nil_iff` | `exceeds_iff` | derived | any `D`; the two-point result is on `[0, 1]` | none | two points: no nonempty family exceeds (the theorem itself); one member: never | by `knows_rename` | `model.exceeding_census` |
| `exceeds_three_two`, `exceeds_three_two_resolution`, `p1`, `p2`, `q3` | `decide` on `[0, 1, 2]` | derived (closed computation) | `[0, 1, 2]` | none | no smaller: AI-02 | the three tables are canonical partitions | `model.examples` |
| `correspondence_matters`, `swap01` | `decide` | derived | `[0, 1, 2]` | none | — | the point: a rewriting inside one member is not a rewriting of the carrier | `model.examples` |
| `knows_rename` | `knows_iff_determined`, `List.mem_map` | derived | any `D` | `σ`, `τ` with `σ ∘ τ = id`: metatheory | — | is the invariance | — |
| `information_congr_mem`, `aggregates_inert`, `aggregates_inert_knows`, `essential_iff`, `duplicate_inert` | `information_mono`, `information_append_of_knows`, `knows_iff_information_eq`, `known_extension_inert` (TT) | derived | any `D` | none | `essential_iff` is an equivalence: both directions exhibited by the model's residual lists | by `knows_rename` | `model.information`, `model.knows` |
| `aggregate_hides_exceeding`, `consensus_after_loss` | `decide` | derived | `[0, 1, 2, 3]`, `[0, 1, 2]` | none | three points suffice for consensus after loss; four for the digest example (on three points a two-member exceeding family's digest has three classes too, but the example needs the digest to be a single presentation that knows `q`; four points make it the identity) | canonical tables | `model.examples` |
| `Chain.Extends`, `ExtChain`, `HasStationary`, `stationary_of_bound`, `long_chain_stationary` | `information_mono`, `information_le_carrier`, `classCount_pos` | definitions admitted; theorems derived | any nonempty `D`; `D = []` excluded (`hD`) | the chain `L : List Institution`: metatheory | a chain of length `|D|` with no stationary step exists (`model.chain_check`, three points): the bound is tight | by `knows_rename` on each level | `model.chain_check` |
| `stationary_step_known`, `stationary_step_inert` | `knows_iff_information_eq`, `information_mono` | derived | any `D` | none | — | — | `model.has_stationary` |
| `information_without_determination` | `decide` | derived | `[0, 1, 2, 3]` | none | two points: `[const]` has information 1 and does not know `id`; the four-point example shows information above 1 without determination | canonical | `model.examples` |
| `Corr`, `corrB`, `corr_iff_corrB`, `agreeQ`, `corr_iff_agreeQ` | `List.all_eq_true` | definitions admitted; equivalences derived | any `D` | the target `t`: metatheory until admitted as a member | — | — | — |
| `determination_not_truth`, `truth_is_a_further_question` | `knows_const`, `Nat.zero_ne_one` | derived | any nonempty `D`; `[0, 1]` | none | one point: both constants are known and differ; `truth_is_a_further_question` needs two points | — | — |
| `truth_from_admitted_target`, `agreement_known_of_admitted` | `knows_iff_determined` | derived | any `D` | none | — | — | — |
| `Policy.Response`, `respond`, `respond_assert_iff`, `respond_demur_iff`, `demur_carries_witness`, `residual_answerable` | `knows_iff_knowsB`, `mem_residuals`, `residuals_nil_iff` (TT) | definition admitted; theorems derived | any `D` | none | `residual_answerable`: the indicator question removes the residual; nothing smaller | — | `model.residuals` |
| `evidence_is_not_a_digest` | `mem_residuals` | derived | any `D` | the digest `f : List Nat → Nat`: metatheory | — | — | — |
| `settledB`, `settledB_iff`, `demurred`, `demurred_zero_iff`, `demurred_settled`, `demurred_known`, `demurred_total_iff` | `knows_iff_determined`, `sigEq_iff_sigList` | definition admitted; theorems derived | any `D` | none | — | — | `model.demurred_check` |
| `Rule`, `ScopedSound`, `knowsB_scoped_sound`, `scoped_sound_le_knowsB`, `scoped_sound_refuses_residual` | `knows_iff_knowsB`, `residuals_nil_iff` | `ScopedSound` admitted; theorems derived under it | any `D` | the rule `A`: metatheory, and the admission | the constant-`true` rule is not `ScopedSound` on `[0, 1]` for `id`; the theorems do not apply to it | — | — |
| `authorization_not_correctness` | `knows_const`, `knows_iff_knowsB` | derived | any nonempty `D` | none | one point suffices | — | — |
| `PairClaim`, `Outcome`, `separatesB`, `outcome`, `same_*`, `apart_*`, `established_iff_eq`, `sameRel`, `scoped_identity_not_absolute` | `List.any_eq_true`, `List.all_eq_true` | definitions admitted; theorems derived | pair claims on any `x y : Nat` (not restricted to `D`) | none | `same_never_established` needs `x ≠ y`; `established_iff_eq` is the exact boundary | the outcomes depend on `Q` only through `separatesB` | `model.outcome_check` |
| `Acquisition.Transcript`, `Protocol`, `entry`, `run`, `run_succ_*`, `run_mono`, `run_length_le`, `Consistent`, `run_consistent`, `run_congr` | structural recursion on `Nat` | grammar admitted; theorems derived | the probed pairs are any naturals | `π : Protocol` and the actor `p`: metatheory; the protocol stands for the external caller probing, not for an observer in the system | — | — | `model.transcripts`, `model.consistent` |
| `merge`, `merge_agrees`, `askedB`, `askedB_iff`, `norm`, `mem_allPairs`, `dropAll` family, `nodup_subset_length`, `nodup_range_self`, `allPairs_nodup`, `uncovered_pair` | sealed `allPairs`; own constructive counting (core's `Nodup.length_le_of_subset` uses `Classical.choice`) | derived | `range n` | none | `uncovered_pair` is sharp: the complete table leaves nothing uncovered | — | — |
| `lower_bound`, `no_acquisition_below_bound`, `no_acquisition_in_fewer_steps`, `no_acquisition_below_half_square`, `transcripts_identical_capabilities_differ` | `uncovered_pair`, `run_congr`, `merge_agrees`, `allPairs_length` | derived | `range n` | `π`, `rule`: metatheory | `n = 2`, `k = 0`: one probe needed, the empty transcript fails (`empty_transcript_fixes_nothing`) | the bound depends on `n` alone | `model.game_value` (exact value for `n ≤ 6`) |
| `probe01`, `admit01`, `complete_evaluator_for_two`, `probe01_transcripts` | `decide` | derived | `range 2` | a fixed protocol and rule | — | — | — |
| `scripted`, `run_scripted`, `fullT`, `run_complete`, `fullT_length`, `sameT`, `sameT_full`, `tableE`, `tableE_length`, `table_sharp`, `complete_table_acquires`, `acquisition_cost_exact` | `allPairs_length`, `mem_allPairs`, `verdictB_eq_false_iff`, `sepB_eq_false_iff` (TT) | derived | `range n` | none beyond the protocol | — | — | `model.closure_evaluator` (a different, smaller evaluator) |
| `sharp_congr`, `classCount_congr`, `acquired`, `acquired_kernel`, `logE`, `logE_length`, `log_views` | `pQ_exact`, `count_le_of_determines` (sealed), `sharpObserver_sharp`, `bitObserver_length` (TT) | derived | `range n` | none | — | — | — |
| `Fixes`, `acquires_implies_fixes`, `empty_transcript_fixes_nothing` | `Sharp` | definition admitted; theorems derived | any `D` | none | — | — | `model.fixes`, `model.fixes_converse_check` |
| `classCount_two_iff`, `exact_promise_zero_probes_two`, `proposal_count_two` | sealed `dedupL_cons`, `memB_cons` | derived | `[0, 1]` | none | this is the smallest refutation; `n = N = 1` agrees with the count (0) | — | `model.acquisition_values` |

Hidden totalities looked for and not found: no theorem quantifies over an
infinite family inside the system; every `∀ p` is a metatheory statement about
tables read on a finite list; `allPairs n` is a finite list; the game's
"every protocol" is a quantifier in Lean and an enumeration of partitions in
Python. Hidden observers: the protocol and the admission rule are external
functions, labelled as such; the evaluator is a finite list of views. Lean's
`Nat` is never used as a carrier: every carrier is a list.
