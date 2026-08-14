# Native Derivation Completion — the Ultra Closure Run

## 1. The exact final question

> Starting from the inert opaque seed and the explicitly priced
> additions already studied, can the current results be composed into
> a smallest defensible obstruction-driven calculus whose runtime
> causes, choices, evaluations, continuations, and stopping conditions
> are represented and replayable?

Answered below, together with the twelve sub-questions (§16–§17 and
the FORMAL SPINE), without assuming a favorable outcome.  Several
terminals hold simultaneously; they are stated exactly in §15.

## 2. Blindness and repository boundary

- Base commit `2c605e2` (merged main after PR #10); branch
  `ultra-closure`; one research PR.
- Sealed checkpoints: PRs #1–#10.  Their modules, artifacts, and
  ledgers are reused and consumed; no earlier theorem or claim was
  altered, and no contradiction requiring repair was found.
- No external repository, architecture, or theory inspected or
  targeted; this document contains no external comparison section —
  nothing outside the repository was needed, so none is used.
  **Scope note (2026-08-13)**: true of THIS run and unchanged as a
  statement about it; it is not a standing property of the
  repository.  A declared contact package has since arrived and been
  processed under the committed statements-only discipline
  (`paper/primitive_difference_contact.md`; status
  CONTACT_PROCESSED_LEAN_ONLY).  The comparison lives entirely in
  that run's modules and in `contact/analysis/` — the sole location
  permitted to quote the arriving vocabulary.  No result of this
  document was revised, weakened, or withdrawn; the collision REUSES
  them — above all the difference interface and its zero-relation
  equivalence (`DiffInterface`, `zeroRel_equivalence`), on which the
  whole reconstruction `ObsDescent` is built.
- Prompt files byte-identical:
  `prompt/prompt.md` =
  `a613a1965e4f02fee00df4d42041fceeca176abcfaa9202c3e769021305940b5`;
  `prompt/seed_prompt.md` =
  `ee3ba0583fea2a11f1294538c912c542b3faee5316355dc226efb92ef64646ab`.

## 3. Inventory of prior checkpoints

Machine-derived, not transcribed: `completion_dependency_graph.json`
carries one record per exported theorem (295), each with source
module, source-extracted statement, axiom set (all within {propext,
Quot.sound}), declared kind and role labels, consuming modules, and
citing ledger claims.  A test pins the inventory to the axiom
artifact exactly — no orphan, no phantom.  The ten checkpoints of the
assignment map onto the modules as: seed inertia and
supply/admission (Basic/Inertia), collapse and quotient no-recovery
(Basic/Quot), bounded minimum search with tied minima
(Minimality/Counting), the witnessed irreflexive candidate
(PrimDiff), provenance prices (Bridge, RefusalFrontier), refusal
(Refusal, RefusalFrontier), reflective successor chains
(RefusalFrontier, Generator), endogenous generation vs exogenous
repair (Generator), the difference interface (DiffInterface), and the
represented kernel (Represented).

## 4. The dependency graph

Thirty bridges over twenty-seven notion nodes, every one classified
(`completion_dependency_graph.json`; human-readable table in
`paper/native_derivation_map.md`): 19 PROVED, 2 DECLARED, 8
FALSE_WITH_COUNTERMODEL, 1 OPEN.  No declared bridge is implicit in
prose; the single OPEN edge — **in the declared graph** — is the named
irreducible obligation of §10.  The graph classifies the declared
bridges; it does not claim to exhaust every possible bridge between
the notions.

## 5. The common native interface

`Completion.CommonState` carries the do-not-erase distinctions as
separate fields: carrier presentation (positions = occurrence
identities), metatheoretic inequality (bookkeeping), positive
witnessed difference (relation instances), observation columns
(observer-relative difference), protected requirements, budget,
license, refusal records.  Transports (each a definition plus a
preservation theorem):

- the represented kernel: `ofWorld` with `ofWorld_sep`,
  `ofWorld_obstruction`, `ofWorld_quiescent` — the kernel's whole
  requirement semantics transports exactly.  The common obstruction
  is the three-condition conjunction over *independent* retention,
  protection, and zero fields (`obstC_conditions_independent`
  witnesses all separations); the kernel realizes retention and
  protection by one store, and the transport instantiates both fields
  from it — a stated identification, not an erasure;
- the reflective chain: `ofPState` with `chain_transport` — carrier
  `range (n+1)`, positive witness = successor edges, horizon-free;
- the two-element difference objects: `d2Common`/`s2Common` with
  `d2_transport_oriented` and `s2_transport_symmetric` — scoped
  exactly: the S2 *relation store* is swap-invariant as a set of
  instances, while the whole encoded state is not
  (`s2_state_not_swap_invariant`: the retained/protected bookkeeping
  carries an ordered pair);
- the early collapse checkpoint: `early_collapse_transports` (the
  Challenge-2 situation in common form); the full early `Regime`
  structure transports only through the sealed token-erasure
  simulation and is recorded as a bounded bridge, not an embedding.

Transport *failures* are first-class results: `witness_not_separation`
(a witnessed pair the observer calls zero), `separation_not_witness`
(a separated pair with no witness), `meta_distinctness_inert`
(bookkeeping moves nothing).  Positive witnessed difference,
observer-relative difference, metatheoretic inequality, protected
demand, and active obstruction never merge.

## 6. Bridges: theorem or countermodel

Every arrow of §4 carries either Lean theorems or a Lean/Python
countermodel; the row-per-bridge table is
`paper/native_derivation_map.md`.  The eight FALSE bridges: seed
forces nothing; supply is not admission; the seed yields no two-ness;
two-ness yields no witnessed relation; facts entail no law; symmetric
states orient no observer equivariantly; proposals do not
self-execute; refusal terminalizes nothing.

## 7. The strongest form of Rule 1

**R1-A (operational dichotomy, refusal parallel) —
CONDITIONAL_THEOREM** (`Completion.rule1_repair_or_extension`).
Under replay well-formedness (an invariant, `wf_replay`) and a
recorded violation, the action-level alternative is binary: the
same-level repair family is non-empty, or the exhaustion certificate
holds and the extension family is non-empty **with both orientations
retained** (`augFamily_retains_ties` — the earlier single-witness
scoping is strengthened: no selector, not even the requirement's own
orientation, chooses the augmentation).  Refusal is a parallel,
non-absorbing *record*, available exactly under the certificate
(`refusal_recordable`), and not an action: `refusal_object_inert`
proves it touches no object field.  Budget/license execution remains
a separate represented gate.

**R1-B (binary compression) — DERIVED_THEOREM**
(`action_dichotomy`).  On the represented signature (carrier length,
view count), every event either preserves the presentation or
strictly grows it.  The action algebra is binary — preserve inside
the presentation, or change the presentation; refusal is a status
record outside the algebra; terminalization is not in the algebra at
all (it belongs to the history producer, §9).

**R1-C (fidelity reduction) — DERIVED_THEOREM**
(`rule1_needs_fidelity`, with the sealed
`PrimDiff.collapse_unobstructed_without_fidelity`).  With no protected
requirement there is no violation and no obstruction: Rule 1 is one
preservation law plus a prior fidelity commitment.  The preservation
law is not free for arbitrary same-level operations: the retraction
countermodel (`retraction_breaks_preservation`) and the sealed
destructive-overwrite countermodel show exactly what the acceptance
guard buys; the monotone restriction of the kernel is a declared
policy, not a theorem about all calculi.

Classification: **primitive as stated nowhere; derived for the fixed
kernel; fidelity-relative in general.**  Independence: the unguarded,
zero-budget, unlicensed, and destructive countermodels show no
hypothesis is redundant.

## 8. The strongest form of Rule 2

**Support factorization, extended** (`NoOutside`): one step
(sealed) → finite histories (`support_replay`) → successor families
(`support_repairFamily`) → certificates (`support_obstructed`) →
verdicts (`support_quiescent`).  The target shape holds exactly:

```text
same represented constitution + same represented operational support
+ same represented history
→ same successor family / certificate / verdict
```

**Effectual-outside dichotomy — DERIVED_THEOREM, operationally
scoped** (`effectual_outside_dichotomy`): whatever changes an
operational result already differs inside the represented support —
its outsideness has entered the books; what changes no operational
result has no operational authority in the kernel.  This is a theorem
about the fixed constitution.  The *absolute* form — "no outside
exists" — quantifies over unrepresented differences and is not a
formulable statement of this calculus: **ABSOLUTE_NO_OUTSIDE_
UNFORMULABLE** is itself part of the verdict, not a defect of it.

**Invariance ceiling, family form**
(`equivariant_family_invariant`): equivariant family-valued
constructions fix families of symmetry-fixed inputs — the ceiling
constrains tied menus exactly as single outputs; asymmetry enters
only through priced imports (sealed: tags, relations, positions).

**What is fixed metatheory** (the kernel constitution): the event
grammar, sep/sat laws, response menu, acceptance predicates, and the
history producer.  Rule 2's theorem form is constitution-relative;
the constitution does not derive itself (§10).

## 9. Event production (G0–G2)

- **G0 — external history**: the sealed regime.  `histUpTo` was a
  metatheoretic producer.
- **G1 — represented scheduler** (`Constitution.Policy`,
  `nextFamily`): the policy is first-order data; the interpreter maps
  represented state to the *complete* family of next event blocks.
  No hidden tie-break: the tower family is a proved singleton
  (`nextFamily_tower_singleton`); the closure family is complete on
  both the repair and extension sides
  (`closeBlocks_complete_repair`, `closeBlocks_complete_aug`) and
  retains both augmentation orientations.  No hidden fresh-name
  source: fresh identity is the canonical numeral of the carrier
  length — a deterministic function that is *not free*: it imports
  arithmetic and ordering, exactly the successor structure the
  reflective chain priced.  Budget and authorization are emitted as
  represented events (`budget_replenishment_represented`); the stop
  outcome is the represented empty family (`nextFamily_stop`).
- **G2 — state-derived generation** (`towerGen`): at each stage the
  next-family interpreter is invoked on the replayed represented
  state and the unique member of the resulting family is appended.
  Honest scope: **state-derived, prefix-compatible generation under
  metatheoretic iteration and a fixed interpreter** — the iteration
  is metatheory, no represented transition invokes the interpreter,
  and no internal-trigger claim is made.  **The reproduction
  theorem** (`driver_reproduces_tower`): the generated history equals
  the previously supplied stream, stage by stage.  What PR #10
  consumed as a supplied stream is now computed from represented
  state — relative to the fixed interpreter and its metatheoretic
  iteration.  Freshness of the canonical numeral is proved **on the
  tower invariant** (`freshName_fresh_on_tower`) and refuted in
  general (`freshName_not_fresh_generally`): the policy's freshness
  is a property of the invariant it maintains, not of arbitrary
  worlds.

Fresh-name pricing (compared): externally supplied tokens (an
exogenous act per name); occurrence identity (position import);
canonical numeral (arithmetic/ordering import — chosen here);
content hash (would import a hash function: a far larger arithmetic
commitment); de Bruijn-style position (equivalent to occurrence
identity); quotient-generated anonymous points (would import the
quotient machinery per name).  Every option priced; none free.

Phase terminal: **EVENT_SOURCE_INTERNALIZED_RELATIVE_TO_FIXED_
INTERPRETER**.

## 10. The constitution (G3–G4)

The constitution family `ConstitutionDesc` (64 members, completely
enumerated: `allDescs_complete`) is represented data; the fixed
family interpreter `interpStep` executes any description; and the
kernel's own description executes to exactly the sealed step:
`interp_describe` — **verified self-description with executable
semantics, relative to the family interpreter**.  The three levels
never conflate: quotation (a description is inert data), executable
description (`interpStep d`), verified self-description (the
theorem).

What is *not* achieved, stated as the named irreducible obligation
rather than hidden: the family interpreter is a function over the
description family and is not a member of it.  The outermost
interpretation relation remains metatheoretic.  Attempting to close
it inside the same construction reproduces the same shape one level
up (an interpreter for interpreters), which is the regress the
assignment predicted as a possible outcome.  Phase terminals:
**KERNEL_CONSTITUTION_INTERNALIZED_RELATIVE_TO_FIXED_INTERPRETER**
and **KERNEL_CONSTITUTION_REMAINS_META** (outermost layer), the
latter being the single OPEN bridge of the dependency graph.

## 11. Autonomy versus iterability

The nine-level ladder (`tower_driver_autonomy`), assessed for the
tower generation: (1) a step exists at every stage; (2) the trace is
prefix-compatible; (3) the next family is computed from represented
state by the interpreter; (4) **not attained** — internal triggering
would require a represented transition to invoke the next-family
interpreter, and here the iteration is metatheoretic (stated, not
laundered); (5–6) selection-freeness — the family is a proved
singleton, ties vacuously retained, and the closure policy retains
all ties non-vacuously; (7) resources persist by represented
replenishment events (self-funding is a visible, priced policy
choice); (8) lawfulness across expressive extensions
(instance-verified in Lean at stage 3, exhaustively bound-verified in
the mirror to 15); (9) productivity under the explicit strict-growth
measure.  An arbitrarily iterable theorem yields (1)–(2) only —
`Represented.productive_run` was exactly that; what is proved here is
(1)–(3), (5)–(9): **state-derived, selection-free, resource-explicit,
productive generation under metatheoretic iteration and a fixed
interpreter**.  Nothing stronger is claimed; adversarial obligation
#4 is answered by this separation.

## 12. Minimality and universality

Declared comparison class: the 64-member constitution family under
the fixed interpreter; declared decidable probe battery (one probe
per guard, each calibrated on a sealed kernel theorem).  Results:

- six load-bearing separations (`*_load_bearing`): switching any
  single guard off violates its probe — concrete countermodels;
- **`unique_compliant`**: the sealed kernel's description is the
  unique member passing the battery;
- both declared cost orders (enabled-capability count; lexicographic
  guards-then-gates) trivially agree on the singleton — order
  disagreement, the recurring phenomenon at every weaker milestone of
  this development, does not arise here because compliance is
  uniquely satisfied;
- the panel extension retracts onto the kernel
  (`extension_retract_replay`, split by `retract_section`) — a split
  retract, and only that.

Terminal: **UNIQUE_PROBE_COMPLIANT_DESCRIPTOR_IN_DECLARED_TOGGLE_
CLASS**.  A six-probe singleton and one split retract do not prove
categorical initiality, and none is claimed: what is proved is unique
probe-compliance in the declared 64-member toggle class, cost-order
agreement on the singleton, and the one retract.  Whether the kernel
is minimal in a wider, undeclared class is not a formulable claim
until that class is declared; "most primitive obstruction engine
possible" is therefore **underdetermined as an absolute claim and
proved as this class-relative one** — the exact answer to final
question 10.

## 13. The certification ceiling

The panel is replay-integrated (`NoOutside.CWorld`: a conservative
extension with an evaluator-admission event; `stepC_conservative`,
`admitEvaluator_base_inert`), answering the PR #10 classification.
The panel-induced non-separation is proved an equivalence relation
(`panel_equiv`), and the negative certificate is exactly
joint-quotient membership (`certNeg_iff_panelEquiv`): panel-relative
warrant, joint quotient closure, and public replay agreement are one
relation, and the sealed `cert_not_correspondence` still bounds it —
certification never reaches correspondence.  What certification
establishes: membership in the panel's joint quotient, replayably.
What it does not: anything about columns outside the panel.

## 14. The final derivation chain

```text
OpaqueSeed
→ (nothing follows: genesis_underivable; supply_no_op)
→ explicit admission boundary            [PROVED: event-indexed replay]
→ retained/witnessed distinction         [PROVED, priced: three tied
                                          two-ness routes; unique
                                          minimum witnessed route]
→ protected law / fidelity demand        [DECLARED: never entailed by
                                          facts]
→ declared observation/difference system [DECLARED laws, PROVED
                                          equivalence: zeroRel]
→ ZeroRel / observational collapse       [PROVED: kernel views]
→ active obstruction                     [PROVED: three-condition
                                          conjunction; fidelity
                                          necessary]
→ exhaustive same-level response family  [PROVED: menu exhaustion
                                          certificates; incomplete
                                          search refuted]
→ repair | extension proposal | refusal  [PROVED: rule1_trichotomy,
                                          ties retained both levels;
                                          refusal record-only]
→ authorization/resource gate            [PROVED: budget/license
                                          load-bearing]
→ replayed transition                    [PROVED: determinism,
                                          composition, support
                                          factorization]
→ remeasurement                          [PROVED: violation only from
                                          require; quiescence stable]
→ scoped certification                   [PROVED: joint-quotient
                                          exactness; ceiling]
→ represented next-event family or stop  [PROVED relative to fixed
                                          interpreter under
                                          metatheoretic iteration:
                                          driver_reproduces_tower;
                                          nextFamily_stop]
```

The candidate shape of the assignment survives with two corrections:
the protected-law arrow is DECLARED (it can never be PROVED — that is
itself a theorem), and the next-event arrow is PROVED only relative
to the fixed interpreter (the absolute version is the OPEN bridge).

## 15. Terminal verdict

```text
RELATIVE_REPLAY_CLOSURE_ONLY
EVENT_SOURCE_INTERNALIZED_RELATIVE_TO_FIXED_INTERPRETER
KERNEL_CONSTITUTION_INTERNALIZED_RELATIVE_TO_FIXED_INTERPRETER
KERNEL_CONSTITUTION_REMAINS_META
UNIQUE_PROBE_COMPLIANT_DESCRIPTOR_IN_DECLARED_TOGGLE_CLASS
ABSOLUTE_NO_OUTSIDE_UNFORMULABLE
```

FULL_NATIVE_COMPOSITION is **not** claimed: the composition closes
relative to the fixed constitution, and the constitution's outermost
interpreter is the one named, honest residue.

## 16. What `<>` does and does not force

Does: exactly one admission on first presentation, under a declared
admission reading; nothing else.  Does not: a successor state, a
second carrier element, a relation, a witness, a law, an orientation,
an observer, an obstruction, a repair, an event source, or a
constitution.  Every one of those is priced, and every price is on
the books (§14; the map).

## 17. What remains supplied, declared, or licensed

SUPPLIED_INPUT: tokens beyond the first (where used); the original
prompts.  DECLARED_POLICY: protection/fidelity commitments; the
observation grammar; the response menu; budget and license values;
the generation policy; the probe battery and comparison class.
METATHEORY: the kernel constitution (event grammar, laws, acceptance,
menu generator) and — irreducibly, per §10 — the outermost
interpreter.  Everything else in the chain is DERIVED_THEOREM,
BOUNDED_COMPUTATION, or COUNTERMODEL, per the map.

## 18. FORMAL SPINE (summary of new theorems)

Phase II: `ofWorld_sep/_obstruction/_quiescent`, `chain_transport`,
`d2_transport_oriented`, `s2_transport_symmetric`,
`witness_not_separation`, `separation_not_witness`,
`meta_distinctness_inert`, `early_collapse_transports`.
Phase III: `rule1_trichotomy`, `augFamily_retains_ties`,
`refusal_recordable`, `refusal_object_inert`, `refusal_non_absorbing`,
`action_dichotomy`, `rule1_needs_fidelity`,
`retraction_breaks_preservation`.
Phase IV: `support_replay/_repairFamily/_obstructed/_quiescent`,
`effectual_outside_dichotomy`, `equivariant_family_invariant`,
`stepC_conservative`, `admitEvaluator_base_inert`, `panel_equiv`,
`certNeg_iff_panelEquiv`, `certC_ceiling`.
Phase V–VI: `nextFamily_tower_singleton`,
`closeBlocks_complete_repair/_aug`, `nextFamily_stop`,
`driver_reproduces_tower`, `nextFamily_complete`,
`budget_replenishment_represented`, `gen_growth`,
`gen_three_quiescent`, `tower_driver_autonomy`, `interp_describe`,
`allDescs_length/_complete`.
Phase VII: six `*_load_bearing` separations, `unique_compliant`,
`minimum_unique_in_class`, `extension_retract/_replay`,
`retract_section`.
Correction pass: `rule1_repair_or_extension` (renamed from the
trichotomy — the action alternative is binary, refusal parallel),
`obstC_conditions_independent`, `s2_state_not_swap_invariant`,
`freshName_fresh_on_tower`, `freshName_not_fresh_generally`.
All 295 exported reports within {propext, Quot.sound}.

## 19. FRONTIER CONJECTURES

- **NC1 (interpreter tower).**  A staged family of interpreters, each
  describing the one below, with a represented fixed point — or a
  no-go theorem that every such tower has a metatheoretic top.  The
  single best next theorem target *for the one bridge that did not
  close*.
- **NC2 (wider comparison classes).**  A declared class with variable
  event grammars (not only guard toggles) where compliance is
  non-singleton — testing whether initiality survives or the
  tied-family phenomenon returns at the kernel level.
- **NC3 (panel dynamics).**  Certification under panel growth as a
  represented process: joint quotients refine along replay; is there
  a represented analogue of the expressiveness ceiling for panels?
- **NC4 (fidelity provenance).**  Rule 1 reduced to preservation +
  fidelity; fidelity itself is always declared.  Conjecture: in any
  kernel of the declared shape, no represented event can *derive* a
  protection — protections are exactly the axioms of the run.

## 20. Adversarial obligations, answered

1. *Explicit stream sold as endogenous generation* — refuted in the
   strong direction: `driver_reproduces_tower` generates the sealed
   stream from represented state; G0 remains documented as supplied.
2. *Represented state sold as represented constitution* — separated:
   §10's three levels; the constitution is data only in the described
   family; the interpreter is not state.
3. *Represented programme sold as represented interpreter* — the
   policy is data, `nextFamily`/`interpStep` are constitution; stated
   at every use.
4. *Replay determinism sold as autonomy* — the nine-level ladder
   separates them; determinism is level 0.
5. *Same-level exhaustion sold as global impossibility* — exhaustion
   certificates are menu-relative by definition;
   `incomplete_search_false_alarm` is the guard.
6. *Refusal record sold as absorbing terminal* — refuted:
   `refusal_object_inert`, `refusal_non_absorbing`; terminalization
   belongs to the history producer.
7. *Positive preservation sold as full conservativity* —
   `aug_preserves_satisfied` names exactly the preserved class;
   non-separation is not preserved, by design.
8. *One canonical augmentation sold as complete tie retention* —
   strengthened instead: `augFamily_retains_ties` proves both
   orientations accepted; the closure family carries both.
9. *Panel agreement sold as correspondence* — `cert_not_
   correspondence` sealed; `certNeg_iff_panelEquiv` gives the exact
   positive content.
10. *Fresh numeral sold as cost-free novelty* — priced: arithmetic
    and ordering import, §9.
11. *Finite-depth success sold as unboundedness* — horizon-free
    theorems are labeled; bounded checks carry their bounds; the
    König countermodel separates witnesses from productivity.
12. *Existence sold as uniqueness* — uniqueness claims are exactly
    `unique_compliant` and `minimum_unique_in_class`, both
    class-scoped; everything else is existence or family.
13. *Fixed signature sold as ontology-independent* — the signature is
    part of the declared constitution (§8, §17).
14. *A type boundary sold as proof that no outside exists* —
    §8's dichotomy is operational and constitution-relative;
    ABSOLUTE_NO_OUTSIDE_UNFORMULABLE is the verdict.
15. *A quoted self-description sold as executable self-representation*
    — the quotation/executable/verified levels are separate
    definitions; the outermost interpreter is the named residue.

(Obligation 16 of the run — hiding an unresolved bridge behind a
familiar name — is answered by the map: every bridge has a status,
and exactly one is OPEN, under its own name.)

## 21. Strongest defensible conclusion

From the opaque seed, nothing follows; every capability of the final
calculus is a priced, recorded import; and the priced imports compose
— by proof, not narrative — into one obstruction-driven kernel whose
runtime causes, choices, evaluations, continuations, and stopping
conditions are represented and replayable, whose event source and
constitution are themselves represented and executable relative to
one fixed family interpreter, which is the unique compliant and
initial member of its declared comparison class, and whose one
remaining outside is exactly named: the outermost interpretation
relation.  The derivation is closed relative to its constitution and
honestly open above it.
