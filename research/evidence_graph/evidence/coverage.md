# Evidence coverage

AuthorityEffect: None.

Source snapshot: `ed028912e0b06f73dd4c5bfe1bb7c2d0e6f3034f`.

The source inventory is complete: 103 trees, 375 public files and 23426 nonblank text blocks.
The stronger all-headlines-supported criterion is **unmet**: 23372 blocks have explicit unresolved dispositions.
This conservative number includes metadata, listings and historical prose; it is not a count of false mathematical claims.

Fresh compiled reports contain 3953 theorem records (including generated public theorems, excluding compiler-internal names).
Independent commands: 31 across 24 trees; results `{'FAILED': 1, 'PASSED': 30}`.
A successful specialized check, a successful build and a successful complete verifier have different scopes. The graph does not replace any independent checker.

## Reading the artifacts

- `graph.json.gz`: scoped records and typed links; deterministic gzip of canonical JSON.
- `coverage.json.gz`: every public span and its disposition.
- `capture.json`: independently observed commands, theorem types, binders, axioms and compiler dependencies.
- `ledgers.json`: source-bound ledger population and unresolved citation digests; joins to exact graph IDs by their UTF-8 SHA-256.
- `imports.json`: exact header, comment, static-transitive and compiler populations.
- `section3_handoff.json`: source spans and scope boundaries for the separate correction owner.
- `handoff.json`: input IDs and remaining obligations for dependent work.

Use `python query.py --id RECORD_ID` to inspect one record, or `--source PATH --line N` to inspect public text at a source location.

## Stages

| Stage | Boundary | Scoped inputs |
|---|---|---|
| 0 | Opaque inscription is supplied. Its visible glyphs supply no order, pair, boundary, equality or successor structure. | `claim:scoped:supply_no_op`, `claim:paper/paper_claim_ledger.md::CL-0-INERTIA` |
| 1 | Regime fields, event grammar and replay are declarations. Their supply no-op theorem does not derive those declarations from the seed. | `claim:scoped:supply_no_op`, `claim:scoped:token_erasure` |
| 2 | Contexts and profiles define the stated observation. Candidate grammar, cost orders and demand policies are separate supplied choices. | supplied source and definitions |
| 3 | Item-count minimum and tied classes stay distinct from refined-cost class uniqueness. Neither reading chooses a concrete successor. | `claim:paper/paper_claim_ledger.md::CL-3-COST1-IMPOSSIBLE`, `claim:paper/paper_claim_ledger.md::CL-3-MIN-TWO`, `claim:paper/paper_claim_ledger.md::CL-3-NONUNIQUE-MU1`, `claim:paper/paper_claim_ledger.md::CL-3-TIE-CLASSES`, `claim:paper/paper_claim_ledger.md::CL-3-INFINITE-TIES`, `claim:paper/paper_claim_ledger.md::CL-3-UNIQUE-MU2-L`, `claim:paper/paper_claim_ledger.md::CL-3-UNIQUE-MU2-F` |
| 4 | Witness, irreflexivity, valued difference and orientation are separate interfaces. DiffObs supplies carriers, delta, Zero and each of zero_refl, zero_symm and zero_trans; packaging them does not derive them. | `claim:scoped:zero_relation` |
| 5 | Occurrence, assertion, witness, protection, observer, budget, license, refusal and halt are actual state fields with actual guards. The one-open-edge count belongs only to the declared completion graph. | `claim:paper/paper_claim_ledger.md::CL-PD2-PASSAGE` |
| 6 | Typed replay, conditional frames, the two-rule rewrite, cancellation and supplied translations are composites with hypotheses. They imply neither an autonomous event source nor an additional flow. | `claim:scoped:aligned_replay`, `claim:scoped:legal_replay`, `claim:scoped:rewrite_sound`, `claim:paper/paper_claim_ledger.md::CL-PD2-BOUNDARY-CANCELLATION`, `claim:paper/paper_claim_ledger.md::CL-FIDELITY-DESCENT`, `claim:paper/paper_claim_ledger.md::CL-TOKEN-ERASURE`, `claim:paper/paper_claim_ledger.md::CL-PD2-TRACE-ALGEBRA` |

## Import populations

The independently saved header population has 35 files in 22 trees. Four additional files have only comment mentions. The supplied count 38 has no attached file population, so its exact counting error cannot be reconstructed; it is not adopted as a verified census.

The saved compiler reach includes the report observer's apparatus imports; it is not mislabeled as the default product-root closure.

| Direct native import source | Compiler check |
|---|---|
| `research/admission_sign_shadow/lean/AdmissionSignShadow/ActualSectionAdapter.lean` | not replayed |
| `research/admission_sign_shadow/lean/AdmissionSignShadow/FrozenPairBridge.lean` | not replayed |
| `research/admission_sign_shadow/lean/AdmissionSignShadow/ReplayOccurrence.lean` | not replayed |
| `research/alpha_engine/lean/Harness.lean` | captured |
| `research/diagonal_identity/lean/DiagonalIdentity.lean` | not replayed |
| `research/diagonal_identity/lean/DiagonalIdentity/Collapse.lean` | not replayed |
| `research/diagonal_identity/lean/DiagonalIdentity/Dual.lean` | not replayed |
| `research/endogenous_continuum/lean/EndogenousContinuum.lean` | captured |
| `research/endogenous_demand/lean/EndogenousDemand.lean` | captured |
| `research/endogenous_demand/lean/EndogenousDemandObstruction.lean` | captured |
| `research/exchange_coefficients/lean/ExamplesAudit.lean` | not replayed |
| `research/f_class_distinctness/lean/FClassDistinctness.lean` | not replayed |
| `research/family_embedding/lean/FamilyEmbedding.lean` | not replayed |
| `research/g010_primitive_removal/lean/Capability.lean` | not replayed |
| `research/ignition/lean/Ignition.lean` | not replayed |
| `research/instance_demand/lean/InstanceDemand.lean` | captured |
| `research/iso_sound/lean/IsoSound.lean` | not replayed |
| `research/local_reuse/lean/LocalReuse.lean` | not replayed |
| `research/magnification/lean/EngineClass.lean` | not replayed |
| `research/magnification/lean/Magnification.lean` | not replayed |
| `research/natural_sections/lean/NaturalSections.lean` | not replayed |
| `research/primitive_difference_tower/lean/PrimitiveDifferenceTower.lean` | captured |
| `research/reachable/lean/Reachable.lean` | not replayed |
| `research/reading_f_iso/ReadingFIso.lean` | not replayed |
| `research/s9_obligations/lean/S9Obligations.lean` | not replayed |
| `research/s9_obligations/lean/S9Obligations/AxiomLattice.lean` | not replayed |
| `research/s9_obligations/lean/S9Obligations/MorphismClasses.lean` | not replayed |
| `research/s9_obligations/lean/S9Obligations/WitnessTypes.lean` | not replayed |
| `research/setting_translation/lean/Chains.lean` | not replayed |
| `research/setting_translation/lean/Translation.lean` | not replayed |
| `research/target_a_execution/lean/Execution.lean` | not replayed |
| `research/unboundedness/lean/ClosedFixpoint.lean` | not replayed |
| `research/unboundedness/lean/CostFloor.lean` | not replayed |
| `research/unboundedness/lean/Driver.lean` | not replayed |
| `research/unboundedness/lean/Unboundedness.lean` | not replayed |

## Research census

| Tree | Registration | Status | Lean files | Test files | Independent command results |
|---|---|---|---:|---:|---|
| `admission_sign_shadow` | local receipt only | unmarked | 6 | 3 | inspected; not replayed |
| `admit_leftover` | local receipt only | parked | 0 | 1 | inspected; not replayed |
| `alpha_engine` | local receipt only | unmarked | 2 | 15 | python verify.py: PASSED |
| `balance_carrier` | local receipt only | unmarked | 6 | 2 | python verify_lean.py: PASSED; python verify_pins.py: PASSED |
| `blind_restart` | workflow (gate 11) | unmarked | 0 | 1 | inspected; not replayed |
| `boundary_seed` | workflow (gate 11) | unmarked | 9 | 15 | inspected; not replayed |
| `closed_family` | local receipt only | unmarked | 4 | 1 | inspected; not replayed |
| `coherent_process_limits` | local receipt only | unmarked | 9 | 4 | inspected; not replayed |
| `concurrency` | local receipt only | unmarked | 5 | 4 | inspected; not replayed |
| `convention_price` | local receipt only | unmarked | 4 | 2 | inspected; not replayed |
| `cost_cohomology` | local receipt only | unmarked | 0 | 1 | python verify_sources.py: PASSED |
| `described_replay` | local receipt only | unmarked | 8 | 3 | inspected; not replayed |
| `diagonal_identity` | local receipt only | unmarked | 7 | 2 | inspected; not replayed |
| `dynamics_step` | local receipt only | parked | 0 | 1 | inspected; not replayed |
| `endogenous_continuum` | local receipt only | unmarked | 11 | 12 | python verify.py --check: PASSED |
| `endogenous_demand` | local receipt only | unmarked | 3 | 8 | python verify.py: FAILED |
| `estate_honesty` | local receipt only | unmarked | 0 | 1 | inspected; not replayed |
| `exchange_coefficients` | local receipt only | unmarked | 3 | 1 | inspected; not replayed |
| `f_class_distinctness` | local receipt only | unmarked | 2 | 6 | inspected; not replayed |
| `family_embedding` | local receipt only | unmarked | 2 | 3 | inspected; not replayed |
| `fresh_characters` | local receipt only | unmarked | 7 | 2 | inspected; not replayed |
| `full_accounting` | local receipt only | unmarked | 0 | 0 | inspected; not replayed |
| `g001_target_charter` | local receipt only | unmarked | 4 | 2 | inspected; not replayed |
| `g010_primitive_removal` | local receipt only | unmarked | 4 | 4 | inspected; not replayed |
| `g011_finitary_substrate` | local receipt only | unmarked | 5 | 5 | inspected; not replayed |
| `g012_typed_translation` | local receipt only | unmarked | 5 | 4 | python verify.py --check: PASSED |
| `g013_trace_calculus` | local receipt only | unmarked | 6 | 5 | python verify.py --check: PASSED |
| `g014_observer_descent` | local receipt only | unmarked | 2 | 1 | python verify.py: PASSED |
| `g015_autonomous_stepping` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `g018_self_hosting` | local receipt only | unmarked | 5 | 4 | python verify.py --check: PASSED |
| `g1_local_class` | local receipt only | parked | 0 | 0 | inspected; not replayed |
| `genesis_continuation` | local receipt only | unmarked | 0 | 0 | inspected; not replayed |
| `grammar_fit` | local receipt only | unmarked | 0 | 1 | inspected; not replayed |
| `higher_order_diagonalization` | local receipt only | unmarked | 4 | 4 | inspected; not replayed |
| `identification_dual` | local receipt only | unmarked | 0 | 1 | inspected; not replayed |
| `ignition` | local receipt only | unmarked | 2 | 4 | inspected; not replayed |
| `instance_demand` | local receipt only | unmarked | 6 | 7 | python verify.py: PASSED |
| `internal_syntax_logic` | local receipt only | unmarked | 5 | 1 | inspected; not replayed |
| `iso_sound` | local receipt only | unmarked | 2 | 7 | inspected; not replayed |
| `iso_sound_lean` | local receipt only | unmarked | 4 | 2 | inspected; not replayed |
| `limit_and_observer` | workflow (gate 11) | unmarked | 2 | 11 | inspected; not replayed |
| `local_reuse` | local receipt only | unmarked | 2 | 3 | inspected; not replayed |
| `m104_equality_order` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `m105_number_tower` | local receipt only | unmarked | 4 | 1 | inspected; not replayed |
| `m108_internal_algebra` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `m109_obstruction_homology` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `m114_solver_adapter` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `magnification` | local receipt only | unmarked | 4 | 4 | inspected; not replayed |
| `multi_depth` | local receipt only | unmarked | 1 | 1 | inspected; not replayed |
| `multi_magnitude` | local receipt only | unmarked | 0 | 1 | inspected; not replayed |
| `natural_sections` | local receipt only | unmarked | 19 | 17 | inspected; not replayed |
| `observer_visibility` | local receipt only | unmarked | 2 | 3 | inspected; not replayed |
| `oriented_boundary` | local receipt only | unmarked | 2 | 2 | python verify_lean.py --check: PASSED |
| `p200_operational_protocols` | local receipt only | unmarked | 5 | 4 | inspected; not replayed |
| `p201_relational_spacetime` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `p203_composite_systems` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `p204_operational_valuations` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `p208a_path_interference` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `p208b_contextuality_nonlocality` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `p208c_commutator_tomography` | local receipt only | unmarked | 2 | 1 | python verify.py --check: PASSED |
| `p209a_wigner_phase_space` | local receipt only | unmarked | 2 | 1 | python verify.py --check: PASSED |
| `p209b_clifford_symplectic` | local receipt only | unmarked | 2 | 1 | python verify.py --check: PASSED |
| `p209c_stabilizer_codes` | local receipt only | unmarked | 2 | 1 | python verify.py --check: PASSED |
| `p209d_nonclassical_horizons` | local receipt only | unmarked | 2 | 1 | python verify.py --check: PASSED |
| `partial_decide` | workflow (gate 11) | unmarked | 0 | 1 | inspected; not replayed |
| `path_dependent_cost` | local receipt only | unmarked | 3 | 2 | python verify_lean.py: PASSED; python verify_pins.py: PASSED; python -m unittest test_path_dependent: PASSED |
| `portable_interface` | workflow (gate 11) | unmarked | 0 | 1 | inspected; not replayed |
| `post_seal_walk` | local receipt only | unmarked | 0 | 0 | inspected; not replayed |
| `priced_admissions` | local receipt only | unmarked | 0 | 1 | inspected; not replayed |
| `primitive_difference_tower` | workflow (gate 11) | unmarked | 3 | 8 | python verify_lean.py: PASSED; python verify_manifest.py: PASSED |
| `reach_additivity` | local receipt only | unmarked | 3 | 2 | python verify_lean.py: PASSED; python verify_pins.py: PASSED |
| `reach_measure` | local receipt only | unmarked | 3 | 2 | python verify_lean.py: PASSED; python verify_pins.py: PASSED |
| `reachable` | local receipt only | unmarked | 2 | 3 | inspected; not replayed |
| `reading_f_iso` | local receipt only | unmarked | 1 | 0 | inspected; not replayed |
| `record_reading` | local receipt only | unmarked | 4 | 6 | inspected; not replayed |
| `redheffer` | local receipt only | unmarked | 1 | 1 | inspected; not replayed |
| `represented_execution` | local receipt only | unmarked | 7 | 9 | python verify.py: PASSED |
| `s9_obligations` | local receipt only | unmarked | 5 | 5 | inspected; not replayed |
| `second` | local receipt only | unmarked | 0 | 0 | python verify_sources.py: PASSED |
| `second_inheritance` | workflow (gate 11) | unmarked | 0 | 1 | inspected; not replayed |
| `second_nofirst` | workflow (gate 11) | unmarked | 9 | 6 | python verify_lean.py: PASSED; python verify_pins.py: PASSED |
| `second_stake` | workflow (gate 11) | unmarked | 0 | 2 | inspected; not replayed |
| `second_stream` | workflow (gate 11) | unmarked | 0 | 2 | inspected; not replayed |
| `self_interpreter` | local receipt only | unmarked | 1 | 0 | inspected; not replayed |
| `setting_translation` | local receipt only | unmarked | 5 | 4 | inspected; not replayed |
| `seventh_constructor` | local receipt only | unmarked | 4 | 4 | inspected; not replayed |
| `side_free` | workflow (gate 11) | unmarked | 3 | 11 | inspected; not replayed |
| `sign_slice` | local receipt only | unmarked | 0 | 3 | inspected; not replayed |
| `sign_tower` | local receipt only | unmarked | 6 | 5 | inspected; not replayed |
| `standing_commitment` | local receipt only | unmarked | 4 | 2 | inspected; not replayed |
| `symmetry_floor` | local receipt only | unmarked | 1 | 1 | inspected; not replayed |
| `target_a_execution` | local receipt only | unmarked | 4 | 5 | inspected; not replayed |
| `target_b_dynamics` | local receipt only | unmarked | 5 | 4 | inspected; not replayed |
| `thinghood` | local receipt only | unmarked | 0 | 1 | inspected; not replayed |
| `twin_pricing` | local receipt only | unmarked | 4 | 3 | inspected; not replayed |
| `two_sided_commitment` | local receipt only | unmarked | 0 | 1 | inspected; not replayed |
| `typed_translation` | workflow (gate 11) | unmarked | 2 | 6 | inspected; not replayed |
| `unboundedness` | local receipt only | unmarked | 9 | 3 | inspected; not replayed |
| `x300_observer_information` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `x301_formal_semantics` | local receipt only | unmarked | 2 | 4 | inspected; not replayed |
| `x302_operational_reasoning` | local receipt only | unmarked | 2 | 1 | inspected; not replayed |
| `x303_bounded_agency` | local receipt only | unmarked | 2 | 3 | inspected; not replayed |
| `x310_vertical_integration` | local receipt only | unmarked | 2 | 4 | python verify.py --check: PASSED |

## Open work and precedents

| ID | Disposition | Required evidence or scope |
|---|---|---|
| `frontier:analytic_limit` | OPEN: Analytic limit | Finite carriers, finite covers and checked potentials need a separate analytic construction and limit theorem. |
| `frontier:demand_channel` | OPEN: Demand and instance channels | The reqs result is scoped to C_reqs; inspect the distinct instance grammar and its declared InClass/I1Class boundary. |
| `frontier:driver_b` | OPEN: Driver B | Provide demand generation and the missing driver without converting proposal, evaluation or uniqueness into a license. |
| `frontier:instance_channel` | OPEN: Represented instance generation | Provide a native demand bridge beyond the represented classes before claiming the open general obligation is closed. |
| `frontier:pipeline_carrier` | OPEN: Integrated carrier | Connect every stage on one declared carrier, with full state/protection metadata and actual step commutation. |
| `frontier:represented_readback` | OPEN: Represented execution and read-back | State precisely which finite carriers and words the encode/lookup/run facts cover; construct each additional reverse map and guard law. |
| `frontier:second_3` | OPEN: Challenge 3 engine | Declare engine state and demand sources; retain all minimum ties and refusal outcomes. |
| `frontier:second_4` | OPEN: Challenge 4 forward run | Run the declared engine under explicit bounds and report every surviving process and terminal. |
| `frontier:second_5` | OPEN: Challenge 5 definability census | Separate each stage's definitions, realizations, supplied capabilities and forced conclusions. |
| `frontier:tower_native` | OPEN: Native tower bridge | Map arbitrary native stages into the admitted fixture without concealing anchor, carrier, naming, grammar or schedule inputs. |
| `frontier:tower_unbounded` | OPEN: Unbounded endogenous successor | A finite horizon and a universally quantified counter schema do not supply an unbounded native successor source. |
| `precedent:additive_cost` | SCOPED_PRECEDENT | Exact trace-price addition; branch-price equality is an explicit premise of its invariance result. |
| `precedent:budget_accounting` | SCOPED_PRECEDENT | Represented exact budget fields and guards; no charge generated by a symmetry action follows. |
| `precedent:finite_form_matrices` | SCOPED_PRECEDENT | Six explicitly displayed two-element-field matrices preserve the declared form; no arbitrary-field result follows. |
| `precedent:path_cost` | SCOPED_PRECEDENT | Abstract exactness implications have supplied action/cost hypotheses; finite route prices have a declared depth-three grammar. |
| `precedent:signed_boundary` | SCOPED_PRECEDENT | Signed deletion coefficients and cancellation for the declared finite-list grammar; scope is the compiled coefficient statement. |

Every row is bound to the immutable input snapshot. Run `refresh.py` for current-head drift and added/removed populations; do not silently replace the historical receipt.
