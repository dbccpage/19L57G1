# Native Derivation Map

One row per bridge of the completed dependency graph.  Machine form:
`artifacts/completion_dependency_graph.json` (statuses are tested
against the axiom artifact; DECLARED evidence names its declaration
site).  Statuses: PROVED / DECLARED / COMPUTED_WITHIN_BOUNDS /
FALSE_WITH_COUNTERMODEL / OPEN.

| source | relation | target | status | Lean / evidence | countermodel or boundary |
|---|---|---|---|---|---|
| seed | forces successor state | admission | FALSE | `genesis_underivable`, `supply_no_op` | nothing follows from the seed alone |
| supply | is | admission | FALSE | `supply_no_op` | supply never mutates admitted state |
| admission | changes state via event | retention | PROVED | `historyL_replays`, `historyF_replays` | event-indexed, replayable |
| seed | yields | two-ness | FALSE | `single_token_carrier_bound`, `second_token_required` | one deduplicated token bounds the carrier at one |
| admission | priced routes to | two-ness | PROVED | `min_witnessed_route_closes`, `reifyUntagged_eq_occurrence` | three tied purchases; order-dependent winners |
| two-ness | yields | witnessed relation | FALSE | `no_forms_no_witness` | the relation channel is a separate purchase |
| admission | priced relation route to | witnessed relation | PROVED | `min_witnessed_route_closes` | unique minimum in class under both cost orders |
| witnessed relation | born off-diagonal | irreflexivity fact | PROVED | `reflective_chain_irreflexive_facts` | horizon-free on the chain; class form bounded |
| irreflexivity fact | entails | irreflexivity law | FALSE | `irrefl_law_not_entailed`, `bridge_facts_not_law` | the law is always a separate declaration |
| irreflexivity law | declared as | protected requirement | DECLARED | `Stage.guarded`, `World.reqs` | protection is a fidelity commitment |
| two-ness | equivariantly yields | orientation | FALSE | `symmetric_no_equivariant_classifier`, `equivariant_output_invariant` | invariance ceiling; bypass is priced |
| admission | priced asymmetry yields | orientation | PROVED | `priced_bridge_oriented` | cost relocated, never eliminated |
| observer/difference map | declared with laws | Zero/ZeroRel | PROVED | `zeroRel_equivalence` | equivalence before any quotient |
| Zero/ZeroRel | with retention+protection is | active obstruction | PROVED | `bare_reflection_certifies_active_obstruction`, `no_guard_no_obstruction` | three separated conditions |
| protected requirement | necessary for | active obstruction | PROVED | `no_guard_no_obstruction`, `collapse_unobstructed_without_fidelity` | no fidelity, no obstruction |
| active obstruction | checked against | response menu | DECLARED | `responseMenu` | the menu is constitution |
| response menu | exhaustive failure gives | exhaustion certificate | PROVED | `incomplete_search_false_alarm` | truncated search falsely certifies |
| active obstruction | trichotomy | same-level repair | PROVED | `represented_progress`, `rule1_trichotomy` | conditional on WF and constitution |
| exhaustion certificate | forces | extension proposal | PROVED | `represented_progress`, `no_bool_view_is_closed` | tied family, both orientations |
| extension proposal | executes without authorization | extension execution | FALSE | `progress_needs_license`, `progress_needs_budget` | proposals never self-execute |
| same-level repair | preserves satisfied | replay | PROVED | `step_mark_sound`, `aug_preserves_satisfied` | positive preservation only, by design |
| replay | factors through | support | PROVED | `support_determines`, `support_replay` | operational factorization |
| budget | gates | same-level repair | PROVED | `progress_needs_budget` | represented fuel |
| license | gates | extension execution | PROVED | `progress_needs_license` | represented authorization |
| exhaustion certificate | recordable as | refusal | PROVED | `refusal_needs_certificate`, `refusals_are_represented` | certificate-bearing only |
| refusal | terminalizes the run | terminal | FALSE | `refusal_non_absorbing` | status record; termination is the history producer's |
| certification panel | certifies up to | Zero/ZeroRel | PROVED | `cert_scope`, `cert_not_correspondence`, `panel_equiv` | joint-quotient exactness; never correspondence |
| next-event source | internalized as policy | replay | PROVED | `driver_reproduces_tower`, `nextFamily_complete` | relative to the fixed interpreter |
| kernel constitution | represented as data | next-event source | PROVED | `interp_describe` | family-relative; verified self-description |
| kernel constitution | interprets itself absolutely | kernel constitution | OPEN | stratification boundary | the named irreducible obligation |

Theorem-name prefixes omitted for width; each resolves uniquely in
`artifacts/lean_axioms.txt`, and the JSON form carries the qualified
names.
