# Claim and assumption ledger

AuthorityEffect: None.

New theorems below name exact declarations in `lean/LocalReuse.lean`;
existing results are explicitly labeled and retain their source namespace.
The separately compiled environment census covers authored and generated
theorem declarations. A successful build certifies those statements, including
their hypotheses; it does not decide the intended interpretation of an outside
problem. Computed entries are supported by `evidence/computations.json` and
the named mutation or counterexample tests.

| ID | Classification and statement | Evidence | Boundary |
|---|---|---|---|
| LR-01 | Proved theorem: arbitrary-cut replay composition and restart, token-aware and erased | `LocalReuse.replayE_suffix`, `replayT_suffix`, `replayE_restart`, `replayT_restart` | full existing regime and recorded event suffix; failure stays failure |
| LR-02 | Proved theorem: valid response paths split and concatenate at a unique cut | `responsePath_append_iff`, `responsePath_cut_unique` | actual `TransStep`, with ordered in-range collapsed target and valid response |
| LR-03 | Proved theorem: every supplied finite valid suffix family shares a recorded prefix and replays | `finite_response_fan`, `responsePath_replays`, `round_replays`, `delta_replays` | does not establish distinct branches of any requested cardinality or executable cost |
| LR-04 | Existing proved theorem, re-exported under this packet's name: a unary form and mark answer an admitted distinct target | `supplied_target_has_response`, which is a single application of `Derivation.mark_progress` in `lean4/Derivation/Progress.lean` and adds no hypothesis | well-formed state and all standing requirements already satisfied; no policy or minimum claim; nothing here is new proof work |
| LR-05 | Proved theorem: datum renaming transports finite response paths | `contextPath_transport` | well-formed source at every round, explicit renaming, requirement transport, fresh-index padding; forward relation-level theorem. Round-count preservation follows from this theorem's own conclusion |
| LR-05b | Deterministic apparatus, not evidence for LR-05: `contextPath_transport_length` is `(rounds.map (mapRound rename)).length = rounds.length`, discharged by `simp` | `contextPath_transport_length` | an arbitrary `Nat -> Nat`, unused in the proof; it holds for any function whatever, says nothing about transport or validity, and must not be cited as though it did |
| LR-06 | Proved theorem/countermodel: existing instances cannot be removed by any admission history | `replayE_retains_instance`, `no_admission_reversal` | actual event grammar; does not forbid separately declared representation changes |
| LR-07 | Proved theorem/countermodel: a separated two-datum state can have no positive response path | `difference_can_have_no_response_step`, `no_positive_path_from_markedRight` | response relation needs a collapsed target; external supply is a separate policy |
| LR-08 | Proved theorem: finite fixed-carrier response bound. `fixed_carrier_round_bound` re-exports the existing `Derivation.closedRun_round_bound` in `lean4/Derivation/Rounds.lean` and adds no hypothesis; `no_seven_closed_rounds_on_two_data` is the new consequence drawn here | `fixed_carrier_round_bound`, `no_seven_closed_rounds_on_two_data` | `ClosedRun`, ordered standing requirements without duplicates; no external datum supply |
| LR-09 | Deterministic computation: seven-round branching and one compatible depth-two restart | `open_run`, `restart`, `trees`; `test_original_seven_round_run_and_full_export`, `test_restart_matches_endpoints_edges_costs_and_classes` | declared sample only; all exported records compared with multiplicity |
| LR-10 | Countermodels: a fresh root need not resume a closure step, generated names may collide, and a valid regime may fall outside the fast driver domain | `phase_reset`, `name_collisions`, `domain_limits`, `multiple_challenges` | stronger unconditional driver-portability claims are refuted; ordinary conditional reuse survives |
| LR-11 | Deterministic computation: supplied measure and grammar determine tied class count | `branch_widths`; `test_all_tied_classes_are_retained` | requested widths such as ten or one billion are neither a driver parameter nor a proved supply of distinct valid classes |
| LR-12 | Countermodel: discarding a standing requirement changes acceptance | `test_standing_requirements_are_not_discardable` | difference-only restart loses semantic context |
| LR-13 | OPEN: every outside problem has a faithful representation and a sound answer interface | explicit `arbitrary_problem_encoding` field | no encoding class or proof has been supplied |
| LR-14 | OPEN: arbitrary requested changes of representation or carrier are enabled and improve the search | explicit `automatic_representation_or_carrier_repair` field | needs typed maps, observation and cost obligations, and evidence |
| LR-15 | NOT PROVED: universal refinement of the Python driver or an undecidability result for broader questions | explicit `universal_python_refinement`, `undecidability` fields | finite checks and missing definitions do not establish either theorem |
| LR-16 | Proved theorem: finite passage suffix families share a complete replayed prefix | `passage_finite_fan` | actual `PrimitivePassage.PState` and `PEvent`; endpoint equality, with no distinctness or success guarantee |
| LR-17 | Proved theorem: a certified trace rewrite preserves replay inside any prefix and suffix | `passage_rewrite_at_cut` | premise is the existing `TraceAlgebra.RwStar`, not an arbitrary alteration of events |
| LR-18 | Proved theorem: a halted passage cut absorbs every later suffix | `passage_halted_cut` | keeping the same halted state cannot restart progress |
| LR-19 | Existing proved countermodel: the declared trace rewrite normalizer is incomplete | `TraceAlgebra.rewrite_not_complete` in `lean4/Derivation/TraceAlgebra.lean` | no impossibility result for richer rewrite calculi |
| LR-20 | Existing proved theorem: composed and successive renamings commute with one declared supply-extension block | `RenamingStructure.act_up_comm_comp`, `act_up_comm_twostep` in `lean4/Derivation/RenamingStructure.lean` | well-formed stores, nonhalted state, carrier length equality, in-range parent; one `Up` block, not arbitrary carrier maps |
| LR-21 | Existing proved theorem/countermodel: declared alternating boundary cancels on double application; all-positive signs need not | `BoundaryCancellation.d2_zero_unrestricted`, `signless_countermodel` in `lean4/Derivation/BoundaryCancellation.lean` | integer coefficients and signs are declared; no automatic repair or driver bridge |

The existing regime/event types, candidate grammar, cost measures, observation
relation, quotient, root challenge, continuation policy, and resource bounds
are declared metatheory apparatus or imposed challenges, as classified in the
source. `ResponsePath`, `ContextPath`, and the event-list maps are new derived
definitions over those existing types. No new primitive operation is admitted.
The witness histories are supplied test data, the verifiers are apparatus,
and all status classifications above are scoped to their named evidence.
