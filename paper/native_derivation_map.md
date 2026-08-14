# Native Derivation Map

One row per bridge of the completed dependency graph.  Machine form:
`artifacts/completion_dependency_graph.json` (statuses are tested
against the axiom artifact; DECLARED evidence names its declaration
site).  Statuses: PROVED / DECLARED / COMPUTED_WITHIN_BOUNDS /
FALSE_WITH_COUNTERMODEL / OPEN.  Scope: one OPEN edge in the
*declared* graph; the graph classifies the declared bridges and does
not claim to exhaust every possible bridge.

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
| active obstruction | dichotomy (refusal parallel) | same-level repair | PROVED | `represented_progress`, `rule1_repair_or_extension` | conditional on WF and constitution |
| exhaustion certificate | forces | extension proposal | PROVED | `represented_progress`, `no_bool_view_is_closed` | tied family, both orientations |
| extension proposal | executes without authorization | extension execution | FALSE | `progress_needs_license`, `progress_needs_budget` | proposals never self-execute |
| same-level repair | preserves satisfied | replay | PROVED | `step_mark_sound`, `aug_preserves_satisfied` | positive preservation only, by design |
| replay | factors through | support | PROVED | `support_determines`, `support_replay` | operational factorization |
| budget | gates | same-level repair | PROVED | `progress_needs_budget` | represented fuel |
| license | gates | extension execution | PROVED | `progress_needs_license` | represented authorization |
| exhaustion certificate | recordable as | refusal | PROVED | `refusal_needs_certificate`, `refusals_are_represented` | certificate-bearing only |
| refusal | terminalizes the run | terminal | FALSE | `refusal_non_absorbing` | status record; termination is the history producer's |
| certification panel | certifies up to | Zero/ZeroRel | PROVED | `cert_scope`, `cert_not_correspondence`, `panel_equiv` | joint-quotient exactness; never correspondence |
| next-event source | internalized as policy | replay | PROVED | `driver_reproduces_tower`, `nextFamily_complete` | relative to the fixed interpreter, under metatheoretic iteration |
| kernel constitution | represented as data | next-event source | PROVED | `interp_describe` | family-relative; verified self-description |
| kernel constitution | interprets itself absolutely | kernel constitution | OPEN | stratification boundary | the named irreducible obligation |

Theorem-name prefixes omitted for width; each resolves uniquely in
`artifacts/lean_axioms.txt`, and the JSON form carries the qualified
names.

**Scope note (2026-08-13).**  This table is the completed
dependency graph of its own run, written while the declared contact
input was absent; no row changed status at the executed collision
(`paper/primitive_difference_contact.md`), and no bridge was added to
the graph.  Two rows acquired external company, recorded here so the
table is not read as the whole story: the *observer/difference map →
Zero/ZeroRel* row is exactly the station where the arriving
development ADMITS as three fields what this row PROVES
(`ContactBridge.declared_zero_as_view`,
`observation_stage_realizes_observer`) — at the INSTANCE level, to be
exact: native `DiffInterface.DiffObs` carries the same three laws as
fields, so the two signatures are not asymmetric; what is asymmetric
is that every concrete observer of the SEALED CORPUS AT `a5caee2` is
a KERNEL OBSERVER, where the laws are proved rather than admitted,
and the declared observation stage is such an observer.  **This is
not a universal claim about native observers**: the collision modules
themselves add observers that are not kernel observers —
`ObsDescent.intDiffObs` (laws by linear arithmetic),
`ObsDescent.collapseAllObs` (laws by `trivial`), and
`ContactBridge.apartObs`, whose three law fields are discharged by
the three ADMITTED `Apartness.IsApart` fields, spent one-for-one, so
at that observer the laws are exactly as admitted as on the arriving
side.  The *irreflexivity fact →
irreflexivity law* FALSE row is echoed on the other side, where the
symmetry and transitivity fields are likewise admissions and not
derivable (`ContactKernel.kernel_not_bs`, `.kernel_zero_not_trans`).
`artifacts/lean_axioms.txt` now carries 1151 reports, including the
three collision modules plus the packet-2 pair-choice lemmas; every
one remains within {propext,
Quot.sound}, and no theorem name of this table became ambiguous
against the new declarations (checked name by name against all 1151
reports; the three non-theorem entries name their declaration site,
as the header already states).
