# Instance-channel claims: Stages 1 through 4

AuthorityEffect: None. Outcome **OPEN** for OB-1 outside `NoGo.InClass`.
The existing `C_reqs` result is unchanged. A uniform materializer and a
stored-instruction composition emitter are exhibited as host operations.
`NoGo.e1_impossible` is native store without that tuple's `admitInst`,
unsatisfiable on the sealed grammar; `InClass` is the nonempty
conclusion-free cover of every Enabled instruction, so that unsat is the
scoped negative for this class, not a class-specific new obstruction.

| ID | Classification and statement | Evidence | Falsifier or remaining obligation |
|---|---|---|---|
| CL-ID-01 | Proved theorem: after any successful event, instance membership is old membership or that exact instance's admission event. | `step_insts_mem`, `new_stored_instance_needs_event` | A successful sealed event violating the stated membership equivalence. No claim about event authorship. |
| CL-ID-02 | Proved theorem: arbitrary successful histories preserve this exact event provenance; every faithful instance reader returns an instance with that provenance. | `replay_insts_mem`, `genesis_instance_origin`, `faithful_read_origin`; `replay_nil`, `replay_cons` | A faithful read without the corresponding event occurrence from genesis. Faithfulness alone is not E1. |
| CL-ID-03 | Proved theorem: uniform rule admission does not write instances; unstored derivable tuples imply coverage of their entire form. | `uniform_rule_keeps_instances`, `new_derivable_is_uniform` | A native conditional-premise rule, or a rule admission that writes `insts`. Materialization is not supplied by either theorem. |
| CL-ID-04 | Proved theorem: the singleton I1 encoding already separates its distinct endpoints. | `lone_pair_separates`; `probe.sample` for both readings | At distinct endpoints with admitted second endpoint, the displayed context fails. The finite samples also have admitted first endpoints. |
| CL-ID-05 | Proved theorem: the rule-covered control remains collapsed, despite storing the same instance. | `covered_pair_collapsed`; `probe.sample` for both readings | A well-formed separating context in that control. This prevents overgeneralizing CL-ID-04. |
| CL-ID-06 | Proved theorem: all four samples are well-formed and the two requirement-free reading histories, with and without uniform coverage, replay exactly. | `samples_well_formed`, `both_readings_replay`, `both_readings_covered_replay` | Replay or well-formedness failure. These are not replays of the requirement-bearing Challenge-3 endpoints. |
| CL-ID-07 | Deterministic computation: exhaustive one-binary-form sweep on 0..3 data, with every instance/rule subset and empty initial requirements. | `probe.sweep`, `evidence/computation.json` | 1,062 states, 17,762 successful extensions, or 2,337 uniform-conclusion cases fail to reproduce. No unbounded Python claim. |
| CL-ID-08 | Open obstruction: existence of an admitted program *outside* `NoGo.InClass` whose interpreter emits a fresh demand-instance satisfying E1, owed-separation E2, E3, E4 and a dynamics theorem. The two-edge instruction class is closed negatively by CL-ID-37. | Stages 3–4 in README; CL-ID-37; prior `endogenous_demand/CLAIMS.md` CL-ED-OPEN | A construction with those proofs on a class other than stored form-0 ternary instructions. Not resolved by occurrence being recorded as `AdmitInst`. |
| CL-ID-09 | Proved theorem: the tuple enumeration contains exactly the lists with the declared length and admitted arguments; uniform entries are exactly well-formed instances whose form is ruled; pending entries additionally are not stored. | `Closure.tuples_mem`, `uniformEntries_mem`, `pending_mem`, `pending_bound` | Missing or extra member under those definitions. The proved numerical bound is pending length at most uniform-entry length, not an asymptotic efficiency claim. |
| CL-ID-10 | Proved theorem: storing any list of well-formed instances replays through the existing instance admissions; materialization is such a replay and emits no requirement event. | `Closure.addMany_mem`, `storeMany_replay`, `materialize_replay`, `events_no_impose` | Failed replay under the well-formedness premise. A replay theorem does not identify who produces events. |
| CL-ID-11 | Proved theorem: materialization preserves data, forms, rules, requirements and well-formedness; final membership is old membership or a well-formed uniform conclusion. | `Closure.materialize_fields`, `materialize_wf`, `materialize_mem` | A changed field or failure of the membership equivalence. Literal E2 is not satisfied. |
| CL-ID-12 | Proved theorem: materialization preserves derivability for every instance and preserves collapsed/separable relations for every pair. | `Closure.materialize_derivable`, `materialize_collapsed`, `materialize_separable` | A separating context added or removed by this procedure. This does not assert equality of raw instance stores. |
| CL-ID-13 | Proved theorem: after one materialization the pending list is empty and a second pass leaves the regime equal. | `Closure.pending_empty_after`, `materialize_idempotent` | Nonempty second-pass pending list. Only this procedure on an otherwise unchanged regime is covered. |
| CL-ID-14 | Proved theorem: on `base n`, no pair is initially stored; after materialization the declared pair reader returns exactly `x < y < n`, and all such endpoints remain collapsed. | `Closure.base_no_pair`, `materialized_pairs`, `generated_pairs_unmet` | A stored pair before this procedure or a separating context afterward. The interpretation of form 0 as a demand is a convention, not this theorem's conclusion. |
| CL-ID-15 | Proved theorem: each pair read from materialized `base n` has a valid response using a fresh unary form and its instance at the first endpoint. The response both applies and replays. | `Closure.response_applies`, `response_replays`, `answer_separates`, `generated_pairs_answerable` | A response failing to separate the pair. These sample regimes have no pre-existing requirements; no minimality or unique-response claim. |
| CL-ID-16 | Proved theorem: the two- and three-data seeds are well-formed, and their seed/materialization/single-pair-response histories replay from genesis. | `Closure.seeds_well_formed`, `seeds_replay`, `replay_append`, `complete_histories_replay` | A failed native history. As in Stage 1, these are requirement-free reading analogues, not the Challenge-3 endpoints. |
| CL-ID-17 | Proved theorem: the declared reader still reads a pair after the separating response of CL-ID-15. | `Closure.answered_pair_still_read`, `answer_separates` | The stored pair disappearing or the exhibited context failing. Raw readability cannot be identified with currently unmet demand. |
| CL-ID-18 | Deterministic computation: materialization passes the stated 1,062-state binary rectangle, adds 2,337 instances in total, preserves profiles/replay, and yields 1,062 fixed points. Both reading samples have a combined response separating all their read pairs. | `materialize.sweep`, `sample`, `evidence/materialization.json`; `tests/test_materialize.py` | Counts or sample witnesses fail to replay. The combined response for all three-data pairs is computed; the general Lean response claim is per pair. |
| CL-ID-19 | Proved theorem: decoding returns exactly stored ternary instructions and binary edges; the raw emitter returns exactly instruction-enabled two-edge paths with ordered distinct endpoints. | `Emitter.length_two`, `length_three`, `codes_mem`, `edge_mem`, `instructions_mem`, `edges_mem`, `raw_mem` | Missing or extra membership under the declared layout. Distinct paths with the same output may repeat it. |
| CL-ID-20 | Proved theorem: on functional operand graphs, each emitted path has the endpoint computed by `Execution.run`; every successful two-step execution output at ordered endpoints is retained. The sample executions have their stated endpoints. | `Emitter.lookup_of_functional`, `two_edge_bridge`, `emitted_has_represented_path`, `execution_output_retained`, `seed_execution_bridge` | Failed correspondence under the stated hypotheses. No identification of an ambiguous all-path result with a first-match result. |
| CL-ID-21 | Proved theorem: without any stored instruction of the declared shape the raw emitter is empty; successful existing execution keeps its input graph. | `Emitter.no_instruction_no_output`, `represented_run_keeps_graph` | An instruction-free raw output or a graph write by that existing execution. The additional output-admission wrapper is not part of `Execution.run`. |
| CL-ID-22 | Proved theorem: pending outputs are precisely enabled, well-formed, initially unstored tuples. Their admission list replays, final membership is exact, other fields are unchanged, and well-formedness is preserved. | `Emitter.pending_mem`, `emission_replay`, `emitted_membership`, `emission_fields`, `emission_wf` | A failure under those definitions. Literal E2 is not satisfied: requirements are unchanged. |
| CL-ID-23 | Proved theorem: the stored instruction and both premises do not universally entail their composed output under sealed derivability. A reachable well-formed unruled-output example defeats that rule schema. | `Emitter.native_closure_counterexample`, `no_native_join_rule`, `unruled_output_not_derivable`, `seeds_replay`, `seeds_wf` | The counterexample output is native-derivable, or the exhibited seed is unreachable/ill-formed. No impossibility for every represented emitter is asserted. |
| CL-ID-24 | Proved theorem: the four L/F output controls replay and are well-formed; each sample family produces exactly its stated single pending output when the endpoint bounds hold; generation histories contain no impose. | `Emitter.raw_seed`, `pending_seed`, `emit_seed`, `seeds_replay`, `seeds_wf`, `histories_no_impose` | A failed sample replay or wrong output. L/F add one auxiliary datum each, yielding 3/4 data; not the sealed Challenge-3 endpoints or a minimum encoding. |
| CL-ID-25 | Proved theorem: the seeds begin collapsed. An unruled singleton emission separates the target; a covered emission leaves every pair collapsed. | `Emitter.seed_collapsed`, `unruled_emission_separates`, `fully_covered_collapsed`, `covered_emission_collapsed` | A counter-context under the stated hypotheses. Unruled output fails E3 after emission; covered output is only a conditional obligation candidate. |
| CL-ID-26 | Proved theorem: covered sample pairs have valid responses using fresh unary form 6; these apply and separate the target, and both complete reading histories replay. | `Emitter.response_applies`, `answer_separates`, `covered_answerable`, `covered_histories_replay` | A failed valid response or replay. No pre-existing requirements, uniqueness, optimality, or derived obligation meaning is claimed. |
| CL-ID-27 | Deterministic computation: the declared 5,140-state graph census replays with 2,560 admission events, 2,528 distinct new instances, 2,340 functional execution paths, and 522 instruction-free states. Both covered samples have whole response replay. | `emitter.sweep`, `sample`, `evidence/emitter.json`; `tests/test_emitter.py` | Counts or witnesses fail to reproduce. The census is not exhaustive over instruction programs, arbitrary data sizes, or repeated growth. |
| CL-ID-28 | Proved theorem: the binary-slot enumeration has length `forms.length * data^2`; its initially missing entries bound the budget. Every nonempty emission batch strictly decreases that budget. | `Dynamics.slots_mem`, `flatMap_length`, `tuples_length`, `slots_length`, `missing_le`, `missing_strict`, `budget_bound`, `emission_extends`, `pending_in_slots`, `budget_decreases` | A pending output outside that carrier or a nonempty batch without strict decrease. Nonbinary form indices are included in the coarse carrier. No tight bound or bound on repeated path events. |
| CL-ID-29 | Proved theorem: pending emptiness is equivalent to an unchanged emission state. Repetition stabilizes by the initial budget and all later states equal that state; changing forever is impossible for this law. | `Dynamics.emit_of_empty`, `empty_iff_fixed`, `rounds_succ_start`, `rounds_add`, `rounds_of_fixed`, `reaches_fixed`, `stable_by_budget`, `stable_after_budget`, `no_unbounded_strict_rounds` | A counterexample for the defined iteration with no intervening event. Does not cover response-driven carrier growth or every possible generator. |
| CL-ID-30 | Proved theorem: emission never produces an instruction of form 0; the exact instruction list, data, forms, rules, and requirements are preserved at every round, as is initial well-formedness. | `Dynamics.pending_not_instruction`, `instructions_addMany`, `emission_instructions`, `rounds_fields`, `rounds_instructions`, `rounds_wf` | A changed field or instruction under the defined law; failure of wf preservation when initially wf. Literal E2 remains unsatisfied. |
| CL-ID-31 | Proved theorem: every finite iteration has an instance-admission trace, contains no impose, and replays from its initial state or a seed already replayed from genesis. | `Dynamics.trace_replay`, `trace_no_impose`, `whole_trace_replay` | Failed replay under the stated premise. This does not derive the trace-producing operation from native structure. |
| CL-ID-32 | Proved theorem: the terminal state is closed under the declared composition, contains every initial instance, and is contained by instance membership in every closed extension on the same data/forms. | `Dynamics.closed_iff_empty`, `terminal_closed`, `enabled_mono`, `rounds_below_closed`, `terminal_extends`, `terminal_least` | A missing enabled well-formed output or a smaller closed extension by membership. No uniqueness of list/event order, response, or obligation meaning. |
| CL-ID-33 | Proved theorem: the four-data chain is reachable and well-formed, has initial budget 61, needs exactly two nonempty rounds, and is then fixed. Round two repeats one tuple along two paths. | `Dynamics.chain_replay`, `chain_wf`, `chain_rounds`, `chain_budget`, `chain_not_one_pass`, `chain_whole_replay`; `dynamics.chain_sample` | An incorrect batch, endpoint, or replay for either coverage setting. This refutes one-pass idempotence of this emitter, not Stage 2's different theorem. |
| CL-ID-34 | Proved theorem: the chain's initial form-3 graph is functional, but is not functional after its first emission. | `Dynamics.chain_functionality_boundary`; `test_chain_needs_two_rounds_and_retains_duplicate_path_events` | Functionality survives in that exact example. The Stage 3 graph-execution bridge remains conditional and cannot be applied at later rounds without its premises. |
| CL-ID-35 | Proved theorem: every pair in the covered chain remains collapsed at every round. Terminal pair `(0,3)` has a valid response using fresh unary form 4, the whole response history replays, and its stored payload remains afterward. | `Dynamics.chain_covered_collapsed`, `chain_response_valid`, `chain_response_replay`, `chain_answered_pair_retained` | Failed collapse, response, or replay. The covered output was already derivable; its obligation role is not proved. |
| CL-ID-36 | Deterministic computation: the 2,124-configuration repeated-emission census has 1,772 initial fixed points and 352 one-round cases, with 384 admission events/new instances. The separate four-data chain has two rounds, 4 events, and 3 new instances. | `dynamics.sweep`, `chain_sample`, `evidence/dynamics.json`; `tests/test_dynamics.py` | Counts, least-store comparison, or whole replay fail. The bounded census itself has no multiple-round example and is not all programs or data sizes. |
| CL-ID-37 | Proved theorem, scoped: E1 as native store (a sealed step writes a new instance without being that instance's `admitInst`) is unsatisfiable. `InClass` is stored form-0 ternary instructions: nonempty, independent of output coverage, and every `Enabled` output names a member as its instruction. The endogenous triple therefore fails on this class because E1 fails on every sealed step, including those of class members; the class is not a hypothesis of the unsat. In-class shapes: unruled Enabled output is not derivable; `impose` is not an E2′ origin; after unruled emission the endpoints separate, so E3 fails. | `NoGo.class_nonempty`, `class_independent_of_coverage`, `class_covers_enabled`, `e1_impossible`, `shape_imposed_fails_E2p`, `shape_unruled_emission_fails_E3`; `Emitter.native_closure_counterexample`; `tests/test_nogo.py` | A sealed step that stores a new instance without that `admitInst`. Does not close OB-1 outside this class. Literal `reqs` E2 is not used. The Stage-1 I1 singleton is not a member of `InClass`. |

CL-ID-01/02 and the preservation part of CL-ID-03 use `propext`; the uniform
conclusion theorem is axiom-free. CL-ID-04/05 and sample well-formedness use
`propext` and `Quot.sound`; the two replay statements use `propext`.
Stage 2 adds 28 authored and 29 generated theorem reports, all within
`{propext, Quot.sound}`. Every exact dependency set, including Stage 1's nine
generated reports, is listed in `evidence/lean.json`. Stage 3 adds 36 authored
and 30 generated reports, also within that budget, for 146 reports through
Stage 3. Stage 4 adds 45 authored theorems and 14 generated reports, including
the newly materialized `Emitter.codes.eq_1` equation in the earlier namespace.
All 205 Stage-4 reports pass the complete census and the unchanged dependency
budget. The scoped no-go adds authored reports under `InstanceDemand.NoGo`;
the live census is the `theorem_count_including_generated` field in
`evidence/lean.json`.
Unrestricted simplification initially introduced disallowed dependence in
the construction; the final direct proofs pass the unchanged dependency gate.

## Notions and assumptions

- Supplied task: attempt instance-channel demand production under the stated
  E1–E4 conditions. The alternate E2 reading is examined separately from `reqs`.
- Metatheory apparatus: the fixed verifier, compiler, history census, finite
  state enumeration, abstract faithful reader parameter, uniform materializer,
  the Stage 2 reading assigning obligation meaning to binary form 0, and the
  Stage 3 instruction interpreter, output-admission wrapper and obligation
  reading, and Stage 4 repeated-emission law. Form 0 is ternary code;
  output form is `3+o`. Iteration is explicitly supplied host apparatus.
- Admitted primitives: the sealed data, forms, instance admission, and uniform
  rules. This stage adds none to the sealed grammar.
- Derived definitions: the sample regimes and histories; well-formed-instance
  predicate, tuple list, uniform-entry and pending lists, response witnesses,
  instruction/edge decoders, enabled composition relation and functional-graph
  predicate; binary-slot enumeration, missing-slot budget, iteration trace and
  closed-extension predicate. The examples' instruction and graph instances are supplied admitted
  data; their operation-code interpretation is declared metatheory apparatus.
- Proved theorems and computations: exactly the rows above and their scopes.
- Open obstruction: event generation and obligation semantics for a represented
  emitter outside `InClass`. The host materializer keeps every well-formed
  uniform conclusion; its operation is not proved to be required by the
  admitted structure. Native store without `admitInst` is unsatisfiable on
  the sealed grammar for every class, including this one.

## Clause assessment after Stage 4

The repeated-emission candidate has a proved dynamics result: under its declared
host law, on fixed data/forms and with no intervening events, it reaches its
least closed extension within the missing-slot budget. This closes the scoped
dynamics obligation for that procedure. Native store without `admitInst` is
unsatisfiable (`NoGo.e1_impossible`); that is the scoped negative for
`InClass`. E1 and OB-1 remain OPEN outside that class.

Literal E2 remains unsatisfied at every round, because `reqs` is unchanged.
Under owed-separation E2, the covered chain has a fresh stored payload, stays
collapsed, and has a valid E4 response with whole replay. Its payload was already
derivable before emission, and a raw stored-pair reader still sees it after the
answer. These are conditional witnesses, not a derived obligation. The earlier
unruled singleton still fails E3; the unruled four-data chain's `(0,3)` is already
separable before iteration, as the Python control records.

The two-round chain rules out treating all emission as a single idempotent pass.
It also loses functionality after round one. The all-path iteration remains
defined, but the Stage 3 functional graph-execution correspondence cannot be
extended automatically to every later state. Fixed-carrier termination is not
a theorem about interleaved responses, enlarged data/forms, or all endogenous
generators. Neither Outcome A nor a general instance-channel impossibility is
established. Reconciliation and publication are Stage 5.

## Clause assessment after Stage 3

The searched candidate class is one-pass composition under stored ternary
instructions `(0,[k,l,o])`, with operand forms `3+k`, `3+l` and output form
`3+o`. All matching two-edge paths with `x < y` are retained. Its fixed syntactic
interpreter consults stored instances; a separate well-formedness/freshness
filter and admission wrapper consumes the regime. The role of its output as
an owed separation is declared, not derived.

CL-ID-20 proves a computation bridge to the existing execution model.
CL-ID-21/23 prevent promoting it to a native production rule: execution does
not write the graph, and the inference schema fails native derivability in a
reachable countermodel. E1 is therefore OPEN, with the exact missing operation
being interpretation of composed output as an admission event and an obligation.
Literal E2 fails by CL-ID-22. At the post-emission state the unruled singleton
candidate fails E3 by CL-ID-25; the covered candidate remains an unmet stored
payload with E4 response/replay witnesses by CL-ID-26. Covered output was already
derivable before storage. These are conditional witnesses under owed-separation E2, not
a proof of derived demand or a full Outcome A.

The finite census consists of 1,044 pairs-of-relations states on 0..2 active
data, with instruction presence and output coverage each toggled, plus 4,096
pairs of partial functional graphs on three active data with instruction and
output coverage present. Three additional data are admitted outside each active
graph carrier. Each census state has six forms and empty requirements. General
Lean membership/replay claims cover more than this census; Python/Lean semantic
equivalence is not proved. Repeated emitter dynamics are now assessed in Stage 4, and Stage 2's
idempotence theorem is not a theorem about this different emitter.

## Clause assessment after Stage 2

E1 remains OPEN. Neither a deterministic enumeration nor its successful sealed
replay proves that the admitted grammar produces its events. Literal E2 fails
for this procedure by CL-ID-11. The owed-separation reading has conditional
E2/E3 witnesses by CL-ID-14, and responses by CL-ID-15/16. These do not resolve
whether the role of demand was derived or supplied by the reader convention.
The rule already entails every materialized tuple; only storage is fresh.
CL-ID-17 rules out calling this raw reader a general unmet-demand filter.
CL-ID-13 is a procedure-specific fixed point, not an impossibility theorem
about represented emitters. No Outcome A or continuing dynamics is claimed.

## Negative controls

The tests inject a changed instance store after `Supply` and require
`INSTANCE_WRITER: Supply`; a wrong replay endpoint and require
`REPLAY_MISMATCH`; a missing event-population entry and require
`INSTANCE_ORIGIN`; and a nonuniform conclusion and require
`UNIFORM_CONCLUSION`. Each replacement is scoped in memory and recovery is
checked. Invalid admissions and unknown reading labels are rejected.
Verifier tests additionally exercise source-population, theorem-census,
dependency, and coverage failures. These guard tests are finite checks, not
proofs that arbitrary tampering or semantic dishonesty can be detected.

Stage 2 additionally rejects malformed form/rule/instance/requirement inputs;
omitted and extra conclusions; altered fields; duplicate, wrong and noninstance
events; corrupted replay and observation results; failed fixed points; and
failed unmet-pair or response witnesses. A control keeps all three strict pairs
in the three-data sample. A mixed-arity control preserves an existing requirement
and an unruled instance without inventing another instance on that unruled form.
All injections are local test replacements. Stage 3 adds controls for missing
instructions/edges; every alternative on an ambiguous graph; repeated output
from distinct paths; instruction-controlled output forms; invalid output arity
or bounds; preserved requirements; wrong path populations, endpoints, traces,
replay, execution output, whole histories, and sample boundary/response checks.
The supplemental source-manifest population is separately tested. The combined
Stage 3 suite had 39 tests. Stage 4 adds controls for premature termination,
wrong round populations/endpoints, changed instructions, failed budget decrease,
exceeded bounds, nonleast terminal stores, and failed trace/response replay.
The verifier also enforces coverage thresholds per measured module, so a strong
aggregate cannot hide a deficient new module. The live test count is the
`python_tests` field in `evidence/verification.json`; all four research
modules have 100% statement and branch coverage, excluding verification
apparatus. No Python-to-Lean equivalence theorem is claimed.
The scoped no-go suite reconstructs class membership, the E1 non-store
control, the in-class E3 failure after unruled emission, and a cheating
class that would drop the Enabled instruction.
