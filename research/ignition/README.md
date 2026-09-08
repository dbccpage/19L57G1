# Ignition on the sealed carrier: the boundary, exactly

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.

**Result.** Growth has a precise effect on the sealed carrier's demands,
and an explicitly scheduled family of productive histories replays at every
finite horizon. Given any well-formed, rule-free regime whose standing requirements
are separated (`Good`), the block "grow, grow, demand the fresh pair, mark"
replays through the sealed step to a `Good` regime with two more data, one
more form and one more requirement, and does so at every horizon
(`runHist_replays`, `runState_data`, `runState_reqs`). The construction supplies
its schedule and mark response; it does not prove liveness of the minimum-response,
fire-before-growth driver. What the state supplies is proved exactly: after one
growth step the fresh datum collapses with an admitted datum **iff** that
datum is mentioned by no instance (`grow_demand_iff`); at a fixpoint that is
at most one demand (`grow_at_most_one_demand`, settling the
`two_sided_commitment` conjecture TS-14 on the sealed model); two growth steps
always create a demand (`two_grows_collapsed`); growth changes no verdict on
the old data (`grow_keeps_verdicts`) while the block's response changes one
(`block_is_activity`). A history of bare supplies of any length is lawful and changes nothing
(`idle_lawful`), so from every `Good` state the idle history and the active
block both satisfy sealed replay (`idle_and_active_both_lawful`). These
theorems establish permitted histories, not which history occurs. The sealed
step takes an event argument; no occurrence law is supplied by that interface.
This is a scope observation, not a theorem that occurrence is undefinable.
The operational assumptions are grouped as: growth is
supplied (L1); a collapsed pair of distinct data is the demand (L2 — the
sealed closure policy, whose comparison is the index identity and is provably
not a digest of the profile, `identity_not_signature_determined`); an enabled
demand is answered (L3). The host schedule, declared bounds and measures,
fresh-name convention, quotient, and branch choices remain dependencies.
Neither sufficiency of exactly these three labels nor inclusion-minimality
of the package is proved. None of the added laws follows from the opaque inscription
(`supply_no_op`, `inert_history`).

Lean: 72 authored theorems, 93 reports with the compiler-generated ones, all
within `{propext, Quot.sound}`.  Python: the extension executed by the sealed
kernel over the sealed exports, 48 tests, strict typing, byte-identical
record.  Execution base `60c2cb05d91cdfa099017c9cd205b52564db884b` (main),
identical to the planning reference; no sealed path is written.

## 1. The question, in three parts

| question | answer | where |
|---|---|---|
| Seed entailment: does any nontrivial transition follow from `<>` under the original assumptions? | No.  A supply changes nothing and every state change is indexed by an external event. | sealed `supply_no_op`; `inert_history`, `idle_lawful` |
| Native operational closure: after a finite recorded history, can the represented process account for its continuing event production with existing semantics? | Demand and response family are computed from state under the declared policies. Event occurrence remains supplied by the host iteration; idle histories satisfy replay. | `grow_demand_iff`, `two_grows_response`, `idle_and_active_both_lawful` |
| Conditional extension: which additional capabilities suffice, and which are necessary in a stated class? | The explicit grow-grow-mark construction gives productive prefixes at every horizon. The finite driver removal experiments do not establish necessity or inclusion-minimality, even within `{grow, fire}`; a fire may itself add data. | `runHist_replays`, `disabled_components`; datum-fixed bound `closedRun_round_bound` |

## 2. Starting state: what is reused, and the missing bridge

Every item was read at its statement, not its label.  The corrections listed
in the work order were confirmed by execution where they are executable
(`evidence/ignition.json:root_families`) and at their Lean statements
otherwise.

| concern | reused result (exact) | what was missing |
|---|---|---|
| Events and response search | `model.step`/`replay`; `observe.collapsed_pairs`; `candidates.min_responses` within `Bounds(2, 2)`; `iso.canonical`; `engine.closure_challenge_orbits`; `export.verify_full_export` | a proof of what growth does to the demand set |
| Existing uniqueness | Challenge 3 at bounds (2, 2): L/mu1 six raw minima in three classes, F/mu1 ten in five, mu2 two raw in one class for both readings — confirmed by `ig.fire` at the roots; `mu2_unique`, `mu2_unique_F` prove the two-item, arity-sum-bounded uniqueness up to `Iso` | nothing; singleton families are accepted as families of one |
| Residuals and joint repair | `Compression.pQ_exact`, `chain_count`; `PresentationRelativity.forced_split_of_factorization_failure`, `jointPresentation` | the same statements *on the sealed carrier* (section 5) |
| Generation, policy, invocation | `Constitution.tower_driver_autonomy`: state-derived, prefix-compatible generation under metatheoretic iteration and a fixed interpreter, with a represented budget reset and a fresh-name convention that are declared; level 4 (represented invocation) explicitly unachieved.  `Horizon.gen_quiescent`, `gen_wf` at every stage.  `InterpreterBoundary.tower_persists`, `family_missed`: a finite code family misses a step function that differs only at the inert notes field; no impossibility of self-application | the same autonomy ladder on the *sealed* `Regime` carrier with the sealed events (section 4) |
| Repair obstruction | `G1Class.g1_class_exclusion` for the declared fixed-radius finite-alphabet class; G3 and G4 conjectures; `OB1_UNCHANGED` | not applied: no strategy here is a local finite-alphabet repair; the mark is the sealed fresh-form response |
| Standing demands and growth | `standing_commitment`: demands as a consequence of growth on the `World` carrier (`growth_generates`, `fixpoint_reopens`, `demand_count_grows`); commitment and growth supplied.  `two_sided_commitment`: TS-09 (at most one demand per growth from a demand-free total-apart state, finite), TS-14 (conjecture) | the theorem on the sealed `Regime` carrier: `grow_demand_iff`, `grow_at_most_one_demand`, `two_grows_collapsed` |
| Represented descriptions and stepping | `described_replay`: a stepper on a reconstructed class `DR-C-2-1-3`; the description is a validated argument, never read by the stepped process; cross-language bridge OPEN | not consumed: a different carrier, no translation theorem |
| Route dependence | `reach_additivity`: difference costs telescope; `path_dependent_cost`: `rule_span` additive, base-relative, not exact, `commit_early`/`commit_late` on an abstract model | the negative on the sealed carrier: the future factors through the endpoint (section 6) |
| Reuse and execution context | `local_reuse`: `replayE_suffix`, `delta_replays`, `round_replays`, `finite_response_fan`; a state alone is not a driver checkpoint | imported as a Lake dependency, not re-proved |

The bridge supplied here is a proof over sealed events of when growth creates
a demand, together with lawful idle and productive histories. A formal
occurrence law and its relation to the minimum-response driver remain OPEN.

## 3. The contract

**Carrier.**  The sealed `Derivation.Regime` (Lean, token-erased) and
`derivation.model.Regime` (Python, with presentation tokens).  Admissible
initial histories: any sealed event list replaying from genesis to a `Good`
regime; the two Challenge 2 closes are `Good` (`rootL_good`, `rootF_good`).
Transition grammar: the sealed `Event` and `stepE`/`step`; the extension adds
no event.  Observation: the sealed profiles — `collapsed`/`separable` on
pairs of admitted data; `verdicts` executes it.  Equality: the sealed `Iso`
(Lean) and canonical key (Python); every class is retained.  Resources: the
declared candidate space (two items, arity two), the sealed permutation
budget, and a step count; no budget field exists on this carrier.

**Replay scope.** The realized driver histories certify by sealed replay.
The theorem statements quantify over `Good` states; they do not assert that
every host structure satisfying `Good` has been reached from genesis.
`phantom_grow` is a negative control that fails the supplied history's certificate.

**Acceptance predicate**, each criterion reported on its own:

| criterion | verdict | evidence |
|---|---|---|
| Enabledness | at every `Good` state with a collapsed pair a valid response exists; after two growths always | sealed `mark_progress`; `two_grows_response` |
| Occurrence / liveness | Idle histories of every length satisfy replay. `runHist` supplies productive prefixes in the permissive `XStep` relation. The Python driver fires before growth, but its liveness at arbitrary horizons is OPEN; that priority is not a hypothesis or conclusion of `runHist_replays`. | `idle_lawful`; `runHist_replays`; finite `drive` experiments |
| Operational closure | the demand set and the response family are functions of the state and the declared laws.  Host functions that still touch the semantic result: orbit selection (`closure_challenge_orbits`), the candidate enumeration and cost (`min_responses`), the canonical-key quotient, the fresh-name function, the step schedule (fire before grow), the declared bounds, and the branch selection of a realized history | `fire`, `drive`; not formalized |
| Activity | a fire flips the verdict on its target; growth flips no verdict on old data; a supply is inert | `block_is_activity`, `grow_keeps_verdicts`; `every_fire_is_activity`, `no_grow_is_activity` in every exhibit |
| Persistence | finite episode: the block.  Recurrent: every two growths create a demand; at a fixpoint one growth creates a demand iff an unmentioned datum exists.  Unbounded: the run, conditional on unbounded growth.  Fixed carrier: datum-fixed rounds are bounded (sealed); closed runs with datum-adding minima are a finite computation here and OPEN in general | `two_grows_collapsed`, `grow_demand_iff`, `runState_data`; sealed `closedRun_round_bound` |
| Branch handling | all minimum-response classes for each offered orbit target retained; a singleton family kept as one; every realized selection is explicit and recorded with the full offered family size; exhaustion is refused | `retains_all_classes`, `Realized.selections`, `Realized.family_sizes` |

**The typed square.**  Represented configuration `r` — permitted extension
step `XStep r t` — successor `t`; decode: the sealed event block (`[admitDatum]`
for growth, `impose i j :: δ.map itemEvent` for a fire); replay: the sealed
`replayE`.  The square commutes (`grow_replays`, `fire_replays`,
`xstep_replays`), including refusal (`replayE` is all-or-nothing), inherited
requirements (`good_fire` keeps every standing requirement separated) and the
resource shape (rule-free responses only, mirroring `rule_item_never_minimal`).
The input invariant `Good` is established at both roots and preserved
inductively (`good_xstep`, `runState_good`).

**Dependency account.**

| item | source | evidence |
|---|---|---|
| first comparison | the index identity `i ≠ j` on admitted data — metatheory (the carrier's numbering), read by the closure policy; provably not a digest of the profile | `demand_iff_residual`, `identity_not_signature_determined` |
| commitment | the total standing commitment (every distinct pair separated) — **declared** (L2, the sealed closure policy; OB-1 unchanged) | `fire_at` refuses a non-demand |
| demand | derived: `demands r = collapsed_pairs r`; growth creates exactly the unmentioned pairs | `grow_demand_iff` |
| event production | growth events — **declared** (L1); response events — decoded from the response family | `grow_replays`, `fire_replays` |
| invocation | metatheory: the fire-before-growth driver and, separately, the grow-grow-mark iteration `runHist`; neither has represented invocation (Constitution level 4 remains unreached) | `idle_lawful`; `drive`; `runHist` |
| response family | derived: the sealed `min_responses` (executed) and every valid response (Lean) | `fire_at`, `TransStep` |
| choice | none in the family; one explicit selection per realized history | `drive(selections)` |
| fresh data | the sealed engine's deterministic name `g<n>`, refused on collision — metatheory | `grow`, `fresh_token` |
| observable distinctions | derived: the sealed profile observation; responses add a form and an instance through the sealed grammar | `verdicts` |
| resource renewal | none represented; the declared bounds are host constants and the mark response is always affordable within them | `mark_progress` |
| continuation | the supplied block schedule and mark response produce lawful prefixes at every finite horizon; driver liveness remains OPEN | `runHist_replays` |

## 4. Bridge B: demand, growth and event production on the executed carrier

An admitted event and the demand set: `admitDatum` **creates** exactly the
pairs of the fresh datum with the unmentioned data (`grow_demand_iff`),
**preserves** every standing separation (`separable_grow`), and at a fixpoint
creates at most one demand (`grow_at_most_one_demand`); a fire **answers**
its demand and preserves every inherited requirement (`good_fire`); two
growths **reopen** a fixpoint (`two_grows_collapsed`) — the sealed-carrier
form of the `standing_commitment` result `fixpoint_reopens`.

The cycle event → demand → response → event is the block; its iteration is the
run.  The first post-initialization semantic step that the state does not
justify is the *occurrence* of a growth event and of a firing: the state
licenses them (enabledness) and nothing in the sealed laws makes them happen.
This is not hidden: `drive` takes `growth`, `closure` and `selections` as
inputs, and `runHist` is a metatheoretic iteration.

Input-directed behaviour was tested on several represented inputs: from the
three tied reading-L openings, growth creates 1, 0 and 1 demands (the unary
mark and the self-loop leave a datum unmentioned; the binary link mentions
both), and the realized histories differ (`gffgfffgfg` against `ggfgfgfgfg`);
a scripted driver returning the same events for every state fails
`input_dependent`.  Growth is represented as a recorded event, never as a
budget reset; there is no budget on this carrier.  No new separator is
imported: the responses are the sealed minimum family, and no local
finite-alphabet strategy is involved, so the G1 exclusion is not applied.

## 5. Bridge A: the residual, on the actual carrier

The profile presentation is represented as the declared question family
`questions r` (one question per well-formed context, `mem_ctxList`), and
signature agreement is exactly the sealed collapse (`sigEq_iff_collapsed`).
Then, for admitted `i, j`:

* `i ≠ j ∧ collapsed r i j` **iff** `pQ D (questions r) i = pQ D (questions r) j ∧ id i ≠ id j`
  (`demand_iff_residual`; as a typed `DirectionalResidual`, `demand_residual`).
  The sealed closure demand is the residual of the profile relative to the
  identity comparison.
* The identity comparison is not signature-determined whenever a demand exists
  (`identity_not_signature_determined`), so the demand generator reads a
  separator the profile does not carry: the carrier's numbering, which no
  represented operation of the sealed model reads except through externally
  supplied event arguments.  The read is licensed by the declared closure
  policy, and by nothing derived.
* A demand refutes factorization of the identity through the profile
  (`demand_refutes_factorization`); the sealed
  `forced_split_of_factorization_failure` then says every presentation carrying
  both must split the pair — which is the demand restated, not a transition.
* The joint presentation has the promised fibers, `j x = j y ↔ p x = p y ∧ q x = q y`
  (`joint_eq_iff`), is idempotent under a repeated comparison
  (`joint_idempotent`), its partition is independent of the carrier order
  (`partition_order_free`) and its representative is not
  (`representative_order_dependent`).  Strict refinement on a fixed carrier is
  bounded by the sealed `chain_count` under its chain hypotheses. This does
  not show that arbitrary firing histories form strict refinement chains;
  the separate datum-fixed round bound counts fresh standing requirements.

The first point at which residual-driven operation requires an added law is
the conversion of the residual into an `impose` event: the sealed grammar
supplies `impose` externally, and the extension's L2 is that conversion.

## 6. Bridge C, and the exhibits

**Two different history classes.** The sealed class `H` contains event lists
accepted by replay, including idle lists. `XStep` restricts a step to growth
or a valid rule-free response; it imposes neither firing priority nor minimum
cost. `runHist_replays` and `runHist_prefix` prove a productive family in this
permissive relation. The Python driver's fire-before-growth policy is a
separate restriction. Already at the reading-L root a demand exists, whereas
`runHist` starts by growing. Its response can also cost more than a minimum.
Thus `runHist` is not a witness of the driver's history class. That class's
formalization, arbitrary-horizon liveness and exact relation to the sealed
exports remain OPEN. Replay certification alone establishes none of those
three claims.

**Exhibit 1 (history with operational consequences).**  From
`⟨2,[1],[],[],[]⟩`, commit a rule then grow, or grow then commit: one endpoint
(`routes_agree`), span totals 2 and 3 (`routes_cost_differ`, the merged
`path_dependent_cost` example restated on the sealed events), and *every*
common sealed event suffix agrees (`future_factors_through_endpoint`,
`routes_indistinguishable`). So no such suffix distinguishes a
retained route-dependent quantity: the quantity is absent from the state, and
storing it is a separately classified extension not built here. A host driver
that reads the earlier history and chooses different suffixes is outside this
theorem. Negative for common-suffix replay, by theorem.

**Exhibit 2 (repeated production and response).**  `linked_episodes` from
each reading and measure: after the sealed root round, one realized
fire-maximal history of ten steps per retained class.  Reading L, mu2: steps
`gffgfffgfg`, six fires, four growths each creating one demand, families of
size 1, 1, 3, 1, 1, 5, targets (1,2), (0,2), (1,3), (2,3), (0,3), (1,4), final
state six data and seven requirements, `Good`, certified.  Reading L, mu1,
the binary-link opening: the first growth creates no demand and the second
creates the fresh-pair demand (2,3) — the earlier response determined the
later demand.  Reading F's openings are not all fixpoints: the unary mark
leaves two data unmentioned and fires twice before any growth, the self-loop
fires once, and the three binary links grow first.  Removal: with L2 off,
eight growths, no verdict changes, 36 (L)
and 45 (F) standing demands; with L1 off, the run stops at the fixpoint
(immediately for L, after two fires for F); with both, five and six fires in
eight steps. These are finite driver experiments. `runHist_replays` with
`runState_reqs` describes the different grow-grow-mark construction.

**Exhibit 3 (coupled local records).**  Not attempted.  No mechanism was
installed to complete the table; the carrier has no second record interface
beyond forms and instances, and two functions reading one regime are two
views, not an interaction.  UNRESOLVED.

**Fixpoint census over the sealed closed exports.**  At every
`terminal_all_separated` node of `closed_L` (3 of 4 nodes) and `closed_F` (16
of 20): the state is `Good`, one growth creates as many demands as there are
unmentioned data (histogram L `{0: 1, 1: 2}`, F `{0: 4, 1: 12}`), and two
growths always create the fresh-pair demand.

## 7. The boundary, and the priced control

**Obstruction, stated exactly.**  Signature: the sealed `Regime`, `Event`,
`stepE`, with `collapsed`/`separable` as observation and event lists accepted
by `stepE` as histories.  Candidate class: any activity property stated over
that signature alone, with the sealed step as the only premise.  Property that
fails: occurrence of a non-idle transition.  Countermodel: from every `Good`
state, the bare-supply history and the block are both lawful, the first
inert and the second active (`idle_and_active_both_lawful`,
`blockState_ne`, `block_is_activity`).  Both interpretations satisfy the
sealed premises, and no admitted premise excludes the idle one — none exists
to weaken.  Hypothesis to change: add an occurrence law to the history class
(L3). The sealed step requires an event argument and has no specified
event-occurrence law. This observation does not prove that a state-based
successor or an occurrence predicate could not be defined with added premises.

**The declared extension `{grow, fire}`, priced.**  Comparison: one (index
identity, through collapsed pairs).  Scheduling: one (fire whenever enabled,
grow otherwise).  Selection: none in the family; one per realized history.
Fresh identity: one (growth, deterministic name).  Observable distinctions:
none new. Resource renewal: none represented. In the finite removal tests, L2 off removes
all activity; L1 off ends the run at the fixpoint; L3 off admits the idle
history. These removal results concern the recorded finite experiments.
Inclusion-minimality within this grammar remains OPEN: a fire may add a datum,
and the datum-fixed termination theorem does not cover such runs. The earlier
inclusion-minimality claim is withdrawn. A commitment over profiles rather than indices (TS-17) and a
represented budget (the `World` carrier's `setBudget`) are incomparable
alternatives not built; minimality across grammars is unresolved.  Old
behaviour is recovered under the decoding projection (`xstep_replays`); the
extension changes what old observations distinguish — a fire separates a pair
the old observation collapsed — and is therefore not called conservative.
A declared extension is a conditional result; it is not a consequence of the
inscription and its usefulness does not select it.

## 8. Evidence

**Lean** (`lean/Ignition.lean`, `lean/Inventory.lean`, `evidence/lean.json`):
a local Lake package importing the pinned sealed package and the merged
`local_reuse` package; 72 authored theorems and 21 compiler-generated ones,
93 reports, 64 within `[propext, Quot.sound]`, 21 `[propext]`, 8 axiom-free;
the report population equals the compiled-environment census of the
`Ignition` namespace in both directions; no private theorem; forbidden-token
scan clean.  Scope: the theorem statements under their hypotheses; the
engine's minimum selection and orbit quotient are not formalized.

**Python** (`ignition.py`, `run.py`, `evidence/ignition.json`, `tests/`): the
extension executed by the sealed kernel; 48 tests; strict typing over nine
files; the record replays byte-identically.

**Negative cases**, one per claim tested (`tests/test_ignition.py`):

| defect | applied to | observed |
|---|---|---|
| hidden supplied comparison | the demand source | `glyph_demands` differs between two presentations of one structure; `demands` does not |
| dropped tied alternative | branch handling | `fire_first_class_only` fails `retains_all_classes`; `fire_at` passes |
| illicit dependence on presentation | the demand source | same as the first row: the sealed demand is presentation-blind, the glyph reader is not |
| precomputed future script | input-directed behaviour | the script fails `input_dependent`; the conditional fire passes |
| unrepresented growth | replayability | `phantom_grow` fails `certify`; `grow` passes |
| inert difference sold as activity | the activity criterion | a supply is `is_inert` and not `is_activity`; a fire is |
| invalid demand translation | the demand | a separated pair and a standing requirement are refused by name |
| failure to preserve an inherited requirement | validity | the regressing mark is rejected by `response_valid_naive` and never offered |
| negative argument or requirement index | Python well-formedness | `well_formed` and `good` reject both malformed host structures |
| absent branch selection | realized history | a missing selection fails by name, including for a singleton; explicit zero succeeds |
| per-target count presented as a full family | branch record | a state with multiple demand orbits records the total offered family separately from each target's response classes |
| productive block presented as fire-before-growth | scheduler claim | at the reading-L root a demand exists; the block grows first while the driver fires first |

**Positive controls.**  A singleton family (mu2 at both roots) is accepted as
a family of one at cost (2, 1); an input-dependent machine (the fire from
different states) passes the same check the script fails.

**Injection record** (this family's own gates; each reversed, no receipt
regenerated while live):

| gate | injection | observed failure | reversed |
|---|---|---|---|
| custody pin | first digit of the pinned `model.py` digest flipped | `FAIL: BASELINE_SOURCE_PIN: code/derivation/model.py` | PASS |
| custody census | untracked `ZzzProbe.lean` in `research/local_reuse/lean` | `FAIL: SOURCE_CENSUS: research/local_reuse/lean: … unexpected=['research/local_reuse/lean/ZzzProbe.lean']` | PASS |
| computation record | `span_total_late` changed from 3 to 4 | `FAIL: evidence/ignition.json differs from fresh computation` | PASS |
| Lean report census | the `#print axioms` line of `grow_demand_iff` removed | `FAIL: report/census mismatch: missing=['Ignition.grow_demand_iff'], extra=[]` | PASS |
| Lean forbidden token | the first forbidden token in a comment | `FAIL: forbidden source token: Ignition.lean` | PASS |
| Lean record | one report's axioms edited in `evidence/lean.json` | `FAIL: evidence/lean.json differs from fresh compilation` | PASS |

**Custody** (`verify_sources.py`, `SOURCE_MANIFEST.json`): at
`60c2cb05d91cdfa099017c9cd205b52564db884b`, the seven derivation modules by
digest and runtime origin, the sealed `lean4/Derivation` tree and the
`research/local_reuse/lean` tree by Git tree object, both Lean configurations
by digest, the two closed exports and summaries by raw digest; an untracked
`.py` on the import path or `.lean` in either Lean tree is refused.
`prompt/` and `paper/` are not read and not pinned.

**Regression gates at the execution base with this family staged**: prompt
hashes (1), transport citations (2), the full sealed suite under coverage
(3), strict typing (4), artifact comparison (5), the Lean audit and report
pin on a fresh log (6), skills (7), paper citations (8), ledger evidence (9),
parked audit (10), the registered research checks (11), the prose watchlist
census with no pin regenerated (12), and the identifier firewall — the
outcomes are in the pull request; a local pass is a local receipt, not hosted
CI.

## 9. The report

1. **What can now continue, and what still needs to be supplied.** From any
   `Good` state the explicitly scheduled grow-grow-mark histories replay at
   every finite horizon and change one verdict per block. Growth events,
   the fresh-pair target, the mark response and the iteration are supplied
   by that construction. The distinct Python driver computes minimum families
   from state and requires explicit choices; its recorded runs are finite.
   Neither construction supplies represented invocation.
2. **What is new.**  The growth–demand characterization on the sealed carrier
   (`grow_demand_iff`, `grow_at_most_one_demand`, `two_grows_collapsed`); the
   horizon-uniform productive run in the sealed event language
   (`runHist_replays` and its counts); the invariant `Good` preserved by every
   sealed `TransStep` with the new well-formedness lemmas
   (`applyDelta_wf`, `good_fire`); the residual bridge on the actual carrier
   (`demand_iff_residual`, `identity_not_signature_determined`); the idle
   countermodel (`idle_lawful`, `idle_and_active_both_lawful`); the endpoint
   factoring of every common event suffix (`future_factors_through_endpoint`).
   Not new: the tower on the `World` carrier, the span example, the replay
   cuts.
3. **Which operational distinction changes, with one readable replay.**  From
   the reading-L mark `⟨2,[1],[(0,[0])],[],[(0,1)]⟩`: grow — the fresh datum 2
   collapses with the unmentioned datum 1, demand (1,2); fire — (1,2)
   separated; fire again on (0,2); then grow. This is the recorded prefix
   (`evidence/ignition.json:exhibits.linked_L_mu2`).  Countermodel on the same
   law: from the binary link, the first growth creates no demand and the
   second creates (2,3).
4. **Status of each result.**  Seed-derived: nothing beyond Challenges 0–3.
   Conditional on existing declarations: the demand (the closure policy) and
   the response family (the candidate space and measures).  Conditional on
   the construction: the prescribed growth and response blocks, their
   iteration, and the resulting productive run.
5. **Proved, bounded, OPEN.**  Proved: no sealed premise excludes the idle
   history; every growth-demand statement above; the productive run.
   Bounded: datum-fixed closed runs terminate (sealed theorem); the closed
   exports terminate at their exported depth (finite). OPEN: liveness of the
   minimum-response driver at arbitrary horizons; termination of
   closed runs whose minimum responses admit data; universal engine
   refinement of `XStep`; exhibit 3; minimality of `{grow, fire}` within or across
   grammars; a commitment over profiles rather than indices.
6. **The next bridge.** Formalize the driver's minimum selection, orbit
   handling and fire-before-growth relation. Determine whether its arbitrary
   prefixes can always extend, accounting for datum-adding responses and
   resource guards. A proof connecting its bounded tree to the exported towers
   would then have a specified target. A
   represented occurrence field on the sealed carrier (the `World` carrier's
   budget, relocated) would make L3 represented data without making it
   self-invoking.

## Not claimed

* That any law here is a consequence of the opaque inscription.
* That the sealed engine refines `XStep` universally, or that minimum
  selection and orbit selection are formalized.
* Anything about responses of three or more items, other measures, or other
  carriers (`World`, passage states, described execution states).
* Necessity or inclusion-minimality of the three law groups within or outside
  the grammar `{grow, fire}`; arbitrary-horizon liveness of the minimum driver.
* Exhibit 3, and any correspondence between a cost and an obstruction.

## Files and running

| file | role |
|---|---|
| `lean/Ignition.lean`, `lean/Inventory.lean` | the theorems; the environment census |
| `ignition.py` | the extension executed by the sealed kernel; the exhibits; the negative controls |
| `run.py`, `evidence/ignition.json` | the deterministic computation record |
| `verify_lean.py`, `evidence/lean.json` | the Lean build, two-way census and reliance record |
| `verify_sources.py`, `SOURCE_MANIFEST.json` | custody of the consumed inputs |
| `verify.py` | every check in order |
| `tests/` | 48 tests: the exhibits, the negative and positive controls, custody, the parser, the record |
| `CLAIMS.md` | one `CL-IG-*` entry per claim |

```powershell
cd research/ignition
python verify.py     # sources, tests, mypy, lean (lake build + census), computation --check
```

Regenerate the two records deliberately and never under a live injection:
`python run.py --write`, `python verify_lean.py --write`.
