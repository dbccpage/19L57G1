# The Primitive Difference map: derivation, obstruction, growth

Run: PR #12 (contact and passage).  This paper is the synthesis: how
the primitive difference is derived, why the first obstruction is
forced to self-resolve or create structure, how the first graph and
the first 0-, 1-, 2-, 3-simplices grow out of that forcing, which
process created each piece of structure, and which invariants the run
discovered and named.  Every claim cites a theorem or a
countermodel; the post-hoc realization table at the end is
comparison, not derivation, and nothing in the formal development
depends on it.

**Scope note (2026-08-13).**  Sections 1-9 are the PR #12 record and
are unchanged; they were written while the declared contact input was
absent.  That input now exists and the collision has been executed in
Lean.  Section 10 is this map's pointer into that run; the account is
`paper/primitive_difference_contact.md`.

## 1. The derivation of Primitive Difference

The provenance chain (sealed in PR #5, sharpened here):

1. **Supply is not difference.**  A supplied inscription is an
   occurrence, not a distinction; repetition creates occurrences,
   never identities (`PrimDiff.repetition_new_occurrence`).
2. **Bare assertion is not difference.**  A positive difference
   assertion with no laws is consistent with a one-point carrier
   asserting difference from itself (`selfdiff_consistent`).  Bare
   witness does not separate (`nimp_w_d`), and its
   indistinguishability is not even reflexive
   (`Apartness.bare_breaks_refl`).
3. **The first law that earns anything is irreflexivity.**  With it,
   the witnessed pair forces endpoint distinctness (`imp_a_d`) and a
   two-element carrier (`no_witness_on_subsingleton`).  **Within the
   declared nine-candidate signature, PD-A — the witnessed
   irreflexive relation — is the weakest studied positive-witness
   candidate forcing distinct endpoints** (`imp_a_d` against
   `nimp_w_d`).  The full 72-cell matrix
   (`primitive_implication_matrix.json`) places every other reading:
   symmetry, cotransitivity, locatedness, protection, retention, and
   operation-irreducibility are each separately priced additions,
   none derivable from the others (51 finite countermodels compiled;
   minimum carrier proved where cited; 4 located cells OPEN with
   exact metatheoretic scope).
4. **The universal status is genuine — and it belongs to W.**  The
   oriented two-element realization is initial among ALL pointed
   witnessed relations (`PrimitiveCats.d2_initial`) — a true
   universal property, not a probe battery.  Since `PtdRel` carries
   no irreflexivity, this initiality characterizes the bare-witness
   reading W (the free pointed object on one witnessed arrow) and
   restricts to the irreflexive subcategory (`d2_initial_irrefl`);
   it does not itself select irreflexivity — the reason to prefer A
   is the separate endpoint-forcing argument above.  Initiality is
   unique up to isomorphism only (`two_initials_not_identical`),
   distinct from minimum cardinality (`larger_not_initial`).  The
   orientation fork is retained whole: the symmetric object is
   initial exactly in the symmetric subcategory and not weakly
   initial outside it.
5. **Indistinguishability is earned, not assumed.**  Under the three
   positive apartness laws it is an equivalence
   (`Apartness.indist_equivalence`), with each law spent at exactly
   one clause and each omission refuted by a minimal finite
   countermodel (carriers 1, 2, 3 — the last minimal because
   cotransitivity is automatic on two points,
   `cotrans_auto_on_two`).

## 2. The first obstruction, and why it must resolve or create

Difference alone obstructs nothing.  The passage
(`PrimitivePassage`) prices every further ingredient:

- assertion (`assertWit`) supplies the positive witness; retention
  (`admitWit`) is a separate admission of an ASSERTED difference —
  an asserted Primitive Difference does not retain itself
  (`assertion_not_retained`, `retention_requires_assertion`), and
  candidate A transports into the pre-retention passage state as a
  theorem (`assert_transport`, `kernel_enters_preretained`);
- protection (`protect`) — else collapse is unobstructed
  (`no_protection_no_obstruction`; fidelity is a demand, never a
  fact: `witness_no_protection`);
- a **declared** observation (`declareObs`) — else there is no zero
  relation at all (`obst_requires_observation`; pre-observational
  states obstruct nothing, as a theorem);
- observer-zero on the pair — the declared observation is blind to
  the protected retained difference.

**The first obstruction is the first moment all four conditions
coexist** (`obstP`; every maximal proper subset refuted,
`obst_conditions_independent`).  It is a normative conflict: the
state retains and protects a difference its own declared observation
cannot see.

**The two-rule theorem** (`two_rule`) is the forcing: at an active
obstruction the response universe never runs dry —

> same-level repair family nonempty, **or** same-level exhaustion
> certified and the extension-proposal family provably nonempty
> (`extension_always_available`: the singleton column on the first
> endpoint is fresh *because* the observation is blind to the pair —
> the obstruction identifies a separator already available in the
> declared singleton-column extension universe; the grammar is
> supplied by declaration, not manufactured by the obstruction).

Refusal (an inert record) and terminalization (absorbing) are
separately typed; proposal is not execution (license and budget
gate it); and the executed response provably kills the obstruction
on remeasurement (`extension_resolves`).  So the first obstruction
is **forced to self-resolve (repair) or create structure
(extension)** — under exactly the declared hypotheses, nothing
stronger claimed.

## 3. The growth of the first graph

The growth driver iterates that forcing (`HigherStructure`):

    round k+2:  admitOcc (k+2); assertWit; admitWit; protect;
                setBudget 1;  ← obstruction active here (round_obstruction)
                addCol [k+1]  ← the structural response (round_resolution)

Provenance, stated exactly: the DRIVER supplies the graph data
(occurrence, asserted difference, retention, protection, and the
declared self-funding `setBudget 1`); what the OBSTRUCTION creates is
the observation column that resolves it.  The driver creates graph
structure; the obstruction creates observation structure.  A driver
in which the graph data itself arises as extension proposals is a
later experiment, recorded as the frontier conjecture
GRAPH_GENESIS_BY_OBSTRUCTION.

- `graphAt_spec` (induction): the grown state at stage `k+1` is
  exactly the **path graph** on `k+2` occurrences — vertices = admitted
  occurrences (0-cells), edges = retained witnessed pairs (1-cells) —
  with one observation column per resolved obstruction.
- The **creation record** of every column is the round's obstruction
  and its accepted response (`round_creation_record`: the last event
  of every round is the `addCol`; the artifact's growth log carries
  the per-round obstruction → response → resolution triple).
- Quiescence is restored after every round (`graphAt_quiescent`),
  and the growth is unbounded (`graph_growth`).

A witnessed binary relation **is** a directed graph presentation —
carrier plus binary store, identity rather than force.  What is
*not* forced is everything above dimension one.

## 4. The 0-, 1-, 2-, 3-simplices and the process that creates them

The declared cell calculus (`CEvent`, `cstep`) admits a `k+1`-cell
exactly over a complete, unfilled boundary of `k`-cells — the shell
guards (complete-unfilled-boundary predicates `shell1/2/3`; they
require ALL faces, so they are boundaries, deliberately NOT
simplicial horns, which omit a face) are load-bearing
(`shell_guard_load_bearing`) and the shell does not fill itself
(`filling_not_forced`).  The four-occurrence
demonstration (`k4_builds`) grows, in replayable creation order:

| dim | cells | created by | count |
|---|---|---|---|
| 0 | occurrences 0–3 | `addV` (passage: `admitOcc`) | 4 |
| 1 | the six witnessed edges | `addE` (passage: `admitWit`, `k4_skeleton_agrees`) | 6 |
| 2 | the four triangles | `addT` over complete edge boundaries | 4 |
| 3 | the solid cell | `addQ` over the complete face boundary | 1 |

**The process responsible for structure creation is the same at
every dimension** — an unfilled parallel boundary (the dimension-`k`
obstruction shape) resolved by creating the filling `k+1`-cell
(`ladder_dim2`, `ladder_dim3`).  This recurrence is the run's
central structural discovery, named below.

## 5. Named invariants

1. **The ladder recurrence** - the two-rule shape recurs one
   dimension up, PROVED at dimensions 2 and 3 (`ladder_dim2`,
   `ladder_dim3`) inside the passage-adjacent calculus:
   boundary-complete-and-unfilled is the dimension-`k` obstruction
   and the `k+1`-cell its structural response.  **Reconciliation
   (audit repair).**  The former frontier conjecture
   GENERAL_DIMENSIONAL_LADDER is now settled ONLY in a narrowed
   sense, and only in the standalone generalized calculus: what is
   proved at every dimension is the UNIFORM GUARDED FILLER theorem
   (`LadderGeneral.uniform_guarded_filler`) - a complete well-formed
   unfilled boundary admits its filler, and that admission strictly
   extends the complex.  That is a statement about the declared
   guarded step and NOTHING MORE.  It is not a homology claim, and
   it does not transport the two-rule reading of `ladder_dim2/dim3`
   to every dimension; the general vanishing of the composite
   boundary is a separate question (see the boundary calculus
   below).  Wherever earlier text said "the ladder is a theorem at
   every dimension", read "the uniform guarded filler is a theorem
   at every dimension".

## 6. What is forced, admitted, or unsupported (Phase IX verdicts)

- Graph: **identity** (a witnessed relation is a graph
  presentation); nothing to force.
- 2-cells from repair diamonds: **admitted, not forced** — the
  passage state carries no 2-cell data; the complete unfilled
  boundary is present and the filler absent until declared
  (`filling_not_forced`).
- Chains/boundaries/d²=0: **declaration-relative** — with the declared
  integer coefficients and alternating boundary signs the composite
  vanishes coefficientwise for every finite list
  (`BoundaryCancellation.d2_zero_unrestricted`).  The older
  demonstration-cell computations remain spot-checks.  The integer
  signless countermodel is nonzero, while earlier finite exhibits also
  show convention freedom (`boundary_not_forced`), so the realization
  carries declared content; no vanishing statement exists without a
  coefficient/sign declaration.
- Metric/amplitude realizations: **unsupported** — nothing in the
  run supplies inner products, amplitudes, or state spaces; no such
  realization is claimed.

Terminal for this phase: **HIGHER_STRUCTURE_OPTIONAL_NOT_FORCED**.

## 7. Post-hoc realization table (comparison only — nothing above
depends on this section)

Recorded per the run directive to name mathematical objects
identical to known mathematics.  Identity claims are keyed to the
laws actually proved, not to resemblance.

| Native object (proved laws) | Known mathematics |
|---|---|
| D2, the oriented two-point witnessed irreflexive relation | the one-edge directed graph / directed edge; the walking-arrow category only after FREE completion with identities and composition (free completion, not identity) |
| `d2_initial` (unique edge-preserving pointed map to any witnessed pair) | initiality of the free/representing object on one arrow |
| S2, the symmetric two-point apartness | the complete graph K₂; the two-point set with its unique apartness |
| `IsApart` (irreflexive + symmetric + cotransitive) and `Indist` an equivalence | apartness relation in constructive mathematics; the negation-equivalence is the standard apartness-to-equality passage |
| the located axis (`Located`, OPEN cells) | decidability of the apartness; its independence mirrors the constructive/classical divide |
| ZeroRel = agreement on all declared columns, an equivalence | the kernel of an observation map; observational/bisimulation equivalence |
| observer cut, `no_terminal_pres`, cut census 2^(n−2) | bipartitions separating two marked points; failure of a terminal object in the poset of faithful quotients above three points |
| the growth's path graph, connectivity residue 1 | the path graph Pₙ; \|V\| − \|E\| = 1 characterizing trees (Euler formula, tree case) |
| cell calculus with shell guards; ladder recurrence (dims 2–3) | simplicial complexes built by cell attachment; boundary filling (complete boundaries, deliberately NOT simplicial horns, which omit a face) |
| `altNum` values 4, −2, 2, 1; shell value 2; solid value 1 | Euler characteristic; χ(∂Δ³) = χ(S²) = 2; χ(Δ³) = 1 |
| `bd1/bd2/bd3` with `d²=0`; `boundary_not_forced` | the simplicial boundary operator over ℤ; orientation-convention freedom |
| two-rule at an obstruction | completion/attachment step: resolve within the presentation or attach a cell |
| interpreter diagonal (Phase VIII paper) | finite diagonal argument for extensional incompleteness of a finite code family |
| description/interpretation non-identification (Phase VIII paper; CONJECTURE level) | the use–mention distinction; stratified metalanguage hierarchies — comparison for the declared model only |

Non-identifications, recorded deliberately: the passage's obstruction
is *not* a homotopical obstruction class (no coefficient system is
derived, only declared); the controller category's simulations are
transition-system simulations, and no claim links them to any
enriched or higher-categorical structure; nothing here derives a
metric, measure, or amplitude.

## 8. Attachment and the general ladder (next-goals pass)

- The canonical map out of the kernel is injective exactly into
  irreflexive targets (`d2_map_injective`; countermodel without).
- One-edge attachment along any represented parent is lawful at
  every stage for every policy; every policy grows a tree with
  V−E=1 (`treeAt_spec`, `all_reach`, `attach_residue`) — tree-ness
  is policy-uniform, global shape is not
  (`path4_star4_not_isomorphic`).
- `Up` is the complete extension family — one block per represented
  parent, no selection — and completeness is REGISTRY-RELATIVE, an
  iff against the declared one-edge grammar (`up_iff_legal`), with
  every block executing to a strict legal extension
  (`up_executes`).  Policies are lawful by proof (`LawfulPolicy`);
  illegal choices meet a typed refusal, never a silent clamp
  (countermodel `clamp_rewrote_input`).  Tokens and positions are
  distinct throughout; the canonical fresh token is proved fresh on
  every carrier, and length-as-token fails off the initial segment
  (countermodel `length_not_fresh_countermodel`).
- Presentation invariance is a genuine positional renaming ACTION:
  replay of Up blocks commutes with it (`act_up_comm`); equal size
  — even a literally equal family — is NOT relatedness
  (countermodel `equal_size_not_renaming_related`), and two legal
  equal-cost extensions genuinely diverge (countermodel
  `equal_cost_non_isomorphic_extensions`).  Orbit-valued choices
  where symmetry remains (star leaves one orbit; the ORIENTED path
  rigid: the orientation residue refuses the undirected flip).
- The generalized calculus carries the UNIFORM GUARDED FILLER
  theorem (`LadderGeneral.uniform_guarded_filler` — narrowed from
  the former "general ladder" naming): admission plus strict
  extension under the repaired well-formed guard (exact arity,
  strict ascent — the legacy guard's `[0,0]` pseudo-cell is the
  recorded countermodel), demonstrated through dimension 4 in Lean
  and 5 in Python; well-formedness replays as an invariant.  Separately,
  `BoundaryCancellation.d2_zero_unrestricted` now proves the general
  coefficientwise composite vanishing by deletion-order pairing.  Its
  signs and integer coefficients remain declared; strict ascent is
  needed for distinct-face results, not for cancellation.
- Target-relative compression (`Compression`): factorization
  through the question signature iff fiber-constancy; the
  signature quotient is the coarsest adequate presentation with an
  image-scoped universal property; descent failures are witnessed;
  enlargement refines with an exact split characterization; NO
  absolute adequacy without a declared family (adequacy for all
  families = injectivity = no compression); repetition, digests,
  and replay records separate nothing new — replay becomes
  evidential only through a new separating question.  Refinement
  is not unique and ties are retained (countermodels), and strict
  refinement chains are bounded by the declared domain.
- The renaming structure around `Up` (Goal 1) is now complete:
  identity, inverse and composition with their group laws; `act` an
  action (identity unconditional, composition on the well-formed
  scope `n <= occ.length`, weakened from equality precisely so the
  extended state is covered); block and family transport respecting
  identity and composition; the naturality square closing under
  composition; and the family carrying whole orbits with no selected
  representative.  `upFamily_orbit_closed` names the exact transported
  block, rather than proving only that the target family is nonempty.
  Only after those laws is `Up` called equivariant,
  and the summary theorem states its exact scope.  Weaker data
  does not instantiate it: an arbitrary non-bijective map has no left
  inverse and its pushforward turns an irreflexive store into
  self-pairs the guard refuses.  This does not rule out other monoid
  actions by non-bijective maps; equal carrier size and equal cost do
  not supply relatedness or identification.
- Trace stability (`StableContent`, audit-repaired).  Protected
  separation is SUFFICIENT for trace stability - supply never
  touches observation, columns only add separators, and refinement
  is guarded by monotone preservation of protected separations -
  and that sufficiency is all that is proved.  The CONVERSE IS
  FALSE on an absorbed state, where every replay is inert.  A second,
  narrower countermodel is live but unfunded: no event in the stated
  restricted fragment changes the observation, so an UNPROTECTED
  separation is stable for that fragment.  The restriction omits
  occurrence admission, budget setting, and license setting and makes
  no ownership claim.  Instability is
  witness-borne: it takes a funded accepted refinement routed
  through the separating column.  Whether stability coincides with
  protection on the live funded class is OPEN.  Quiescence is a
  statement about protected separation, not about stability: no
  pair obstructs exactly when every retained protected pair is
  protected-separated.

## 9. Terminals, adversarial record, and receipt

The run ends with ten terminal codes, each mapped to theorem or
countermodel evidence, five open obligations, the twenty-attack
adversarial record (every attack with its disposition), and the two
withdrawn-or-repaired claims — all machine-readable in
`artifacts/primitive_completion_receipt.json`.  Controller
universality: refuted, with the reachable-orbit salvage
(`paper/primitive_controller_universality.md`).  Interpreter
boundary: finite code families are extensionally incomplete, and a
DECLARED boundary model satisfies A and F; the identification of the
boundary with a Primitive Difference is a frontier conjecture with
its missing theorem stated
(`paper/primitive_interpreter_boundary.md`).  The strongest
defensible terminal statement of the whole run:

> Within a declared common signature, a witnessed irreflexive
> relation is the weakest studied positive-witness candidate that
> forces distinct endpoints; the free pointed object on one
> witnessed arrow is initial, and initiality restricts to — without
> selecting — the irreflexive reading.  Positive apartness yields an
> equivalence of indistinguishability only after symmetry and
> cotransitivity are separately admitted.  Assertion, retention,
> protection, observation, response grammars, budget, and
> authorization are further independent purchases.  Once a retained,
> protected difference is collapsed by a declared observer, the
> declared finite response universe yields a same-level repair
> family or a nonempty extension-proposal family.  A separate driver
> iterates this scheme to grow path-graph data and observation
> structure, and the same shell-filling shape is proved one and two
> dimensions up.  No controller realizing this is categorically
> unique; agreement is a replay theorem on the reachable orbit.
> Higher cells and boundary operators remain declared realizations,
> and the reading of the interpreter boundary as the next Primitive
> Difference remains a frontier conjecture awaiting its denotational
> bridge.

**Scope note (2026-08-13).**  The counts above are the PR #12 run's.
After the executed collision the regenerated receipt carries thirteen
terminal codes (the three collision codes added; the pre-contact
CONTACT_INPUT_ABSENT preserved with an explicit sealed-history scope
field) and a twenty-one-attack adversarial record.  The collision
also ADDED unresolved obligations, and the receipt records them: the
four OPEN cells it declared (`ContactBridge.open_bridge_cotrans`,
`open_bridge_located`, `ContactKernel.open_kernel_grade`,
`open_kernel_bl`), each with its price — WLEM, a WLEM-implication
with OPEN converse, DNE, and metatheoretic underivability of Located
— bring `open_obligations` from four to eight, and two collision
conjectures (enlarged-corpus containment; the converse of
`located_schema_implies_wlem`) bring `frontier_conjectures` from
three to five (`artifacts/primitive_completion_receipt.json`).  The
quoted terminal
statement stands as written: nothing in the arriving development
touches the passage, the growth, or the cell calculus.

## 10. The executed collision (2026-08-13)

Sections 1-9 stand unchanged.  The contact package arrived (one
external Lean file, sha256 recorded in
`contact/omega_primdiff/CONTACT_MANIFEST.json`; no prose —
PROSE_INPUT_ABSENT), was read under the committed statements-only
discipline against the interface section 9 had already committed, and
the collision was executed in Lean.  Status:
**CONTACT_PROCESSED_LEAN_ONLY** (`PrimitiveContact.contactStatusCurrent`,
`artifacts/primitive_contact.json`).  This section is the map's
pointer only; the account is `paper/primitive_difference_contact.md`,
and the arriving development's own vocabulary is quoted nowhere
outside the `contact/analysis/` directory, which is the whole
permitted location — four files, every quotation SUPPLIED_INPUT-
labeled: `contact_dictionary.md` and `contact_countermodels.json`
(103 declaration rows, the countermodel table, the gap
dispositions), and also `lean_definition_map.md` and
`lean_theorem_transport.md`, which quote arriving declaration names
and full arriving statements verbatim throughout.  `lean4/`, `code/`
and `paper/` carry none of it.

**Where the new theorems live.**  Three modules, 2015 lines in the
working tree (539 + 710 + 766; 1942 at the spine commit `ebb1e0b`),
every `#print axioms` report inside {propext, Quot.sound}
(`artifacts/lean_axioms.txt`, 1178 reports):

| module | content | headline names |
|---|---|---|
| `lean4/Derivation/ObsDescent.lean` | the arriving quotient-descent layer reconstructed in native vocabulary over the sealed `DiffInterface.DiffObs` / `ObsQuotient` | `obsQuotient_exact`, `obsQuotient_mk_eq_iff`, `obsQuotient_mk_surjective`, `descend_exists_iff`, `descend_unique`, `descend_blocked_of_witness`, `deltaDescend_exists_iff`, `view_descends_pair_blocked`, `classConstant_comp_mk_iff`, `coarsenMap`, `pairSetoid`, `collapseAllObs_*`, `intDiffObs` |
| `lean4/Derivation/ContactBridge.lean` | the complement bridge between the arriving observer stratum and sections 1 and 5 | `obsApart`, `obsSetting_w/a/bs/bc/bl/d/e`, `apartObs_roundtrip`, `isApart_repr`, `obsApart_isApart`, `indist_obsApart_iff`, `obsApart_repr_iff`, `d2_not_obs_complement`, `cotrans_schema_iff_wlem`, `stability_schema_iff_dne`, `located_schema_implies_wlem`, `declared_zero_as_view`, `pair_blocked_is_collapse_collision` with its converse `collapse_collision_is_pair_blocked` and the packaged `pair_blocked_iff_collapse_collision` |
| `lean4/Derivation/ContactKernel.lean` | the common replacement kernel and the 37-cell collision matrix | `WitnessedDiff`, `ofSetting`, `ofSetting_exact`, `ofDiffObs`, `toDiffObs` (with `toDiffObs_fields`, `toDiffObs_apart`), `toNativeKernel`, `kernel_gateway_unique`, `kernel_no_terminal_collector`, `vhom_unique_of_onto`, `kernel_licenses_entry`, `entry_pre_observation`, `contactCells` (`contactCells_length`) |

`lean4/Derivation/PrimitiveContact.lean` gained only an additive
dated section (`contactStatusHistory`, `contactStatusCurrent`,
`contactVerdictPrimary`, `contact_status_count`,
`native_interface_not_representable`); the sealed pre-contact
declarations (`contactStatus`, `NativeKernel`, `nativeKernelWitness`,
`native_kernel_initial`) are unchanged.

**Where the collision lands on this map.**

- **On section 1 (the derivation).**  The arriving core structure is
  the native valued observer field-for-field, with its three
  equivalence laws ADMITTED as fields; the native side proves the
  same laws, equality-grade, at the passage's declared observation
  stage (`ContactBridge.declared_zero_as_view`,
  `observation_stage_realizes_observer`), so the arriving stratum
  sits at the zero-relation stage, not before it
  (`kernelStage`, `kernel_stage_no_obstruction`).  Item 4's
  orientation is not importable through any difference-map
  presentation: no valued observer's zero-complement is the oriented
  two-element witness, over ANY value type
  (`ContactBridge.d2_not_obs_complement`, carrier 2; re-exported at
  the sealed interface as
  `PrimitiveContact.native_interface_not_representable`).  Item 5's
  apartness stratum and the arriving observer are inter-constructible
  with matching relations in both round trips under TWO decidability
  admissions, one per direction and not interchangeable: apartness →
  observer spends pointwise decidability of the ASSERTED APARTNESS
  relation (`isApart_repr`, `apartObs_roundtrip`), observer →
  apartness spends pointwise decidability of the ZERO relation
  (`obsApart_isApart`, `indist_obsApart_iff`).  They do not
  substitute for one another — the constructed observer's zero
  relation is the negation of the asserted apartness, and `Decidable`
  of a negation does not return `Decidable` of the statement, which
  is exactly the residue `stability_schema_iff_dne` prices at DNE.
  Sufficiency is what is proved; necessity of either admission is
  not.  The dropped hypotheses are priced: cotransitivity
  schema ↔ WLEM (`cotrans_schema_iff_wlem`), stability schema ↔ DNE
  (`stability_schema_iff_dne`), locatedness schema → WLEM
  (`located_schema_implies_wlem`, converse OPEN).
- **On sections 2-6 (obstruction, growth, cells, ladder).**
  Untouched.  Every one of the 103 arriving declarations is
  classified row-by-row in the coverage map
  (`contact/analysis/contact_countermodels.json`); none carries
  retention, protection, budget, license, response families, or
  growth.  The nearest shape is the arriving descent obstruction,
  which is collapse-collision at the quotient projection
  (`ContactBridge.pair_blocked_is_collapse_collision`) and strictly
  coarser than the four-condition `obstP`
  (`obst_conditions_independent` cited); protection and retention are
  never derivable from an observer (`obsSetting_not_c`,
  `obsSetting_not_f`, `kernel_prot_independent`).
- **On section 7 (the post-hoc table).**  No row added.  The arriving
  physics-labeled tail never instantiates its own core structure and
  is integer subtraction throughout: subsumed by
  `ObsDescent.intDiffObs` plus five one-line lemmas
  (`int_sub_ne_zero_iff`, `int_sub_ne_zero_of_gt`,
  `int_shift_cancel`, `int_two_mul_eq_zero_iff`,
  `int_add_sub_cancel`).  Its comment-borne vocabulary was REFUSED
  transport into the formal record (dispositions G1-G20 in the
  analysis file).
- **On section 8 (compression).**  The factorization dictionary is
  proved, at the scope its statements carry: for kernel observers on
  the carrier `Nat` with `Nat`-valued views (`p q : Nat → Nat`, the
  typing forced by the sealed `Compression` layer's `D : List Nat`),
  global quotient descent is exactly native list-scoped factorization
  quantified over every represented domain
  (`ObsDescent.descend_iff_factorsOn_all`,
  `classConstant_iff_fiberConstant_all`), while per fixed domain the
  native notion is strictly weaker
  (`fiberConstant_fixed_D_not_classConstant`).  Nothing is proved
  here for kernel observers at other carriers or view types.  The
  uniqueness-scope difference is exactly codomain coverage by the
  projection (`obsQuotient_mk_surjective` against the sealed
  `factor_unique_on_image` / `factor_not_unique_off_image` /
  `phom2_unique_of_epi`).  `Derivation.quot_barrier` remains strictly
  more general than anything the arriving SETOID-BASED machinery can
  state — METATHEORY, a citation-only comparison of two signatures,
  with no transport theorem written or claimed in either direction.
- **On section 9 (terminals and receipt).**  The pre-contact kernel
  interface committed with this run's receipt
  (`PrimitiveContact.NativeKernel`, under the CONTACT_INPUT_ABSENT
  terminal) is met by construction:
  `ContactKernel.toNativeKernel : WitnessedDiff X R →
  PrimitiveContact.NativeKernel`.  The common kernel `WitnessedDiff`
  (valued difference presentation, designated endpoints,
  diagonal-zero law, refutation-grade witness — no symmetry, no
  transitivity, no stores) is realized from native candidate-A
  settings (`ofSetting`, exact under pointwise decidability by
  `ofSetting_exact`, the gap otherwise recorded OPEN in
  `open_kernel_grade`) and from arriving-shape observers plus a
  chosen non-zero pair (`ofDiffObs`, the pair proved load-bearing by
  `pair_choice_load_bearing`); in the reverse direction the kernel
  together with the two law declarations IS the observer record,
  field-for-field and losslessly (`toDiffObs`, `toDiffObs_fields`,
  `toDiffObs_apart` — a record identity, DEFINITION grade, not a
  derivation).  It inherits the initial gateway from
  the sealed `d2_initial` (`kernel_gateway_unique`,
  `kernel_gateway_injective`), has provably no terminal collector AT
  THE INDUCED-APARTNESS MORPHISM GRADE
  (`kernel_no_terminal_collector`, `kernel_no_terminal`: morphisms of
  the `apartObj` presentations, which discard the value data —
  nothing is proved about terminality in the valued morphism category
  `VHom`), carries value grade as presentation, off-image
  non-uniqueness and all (`value_presentation_fork`,
  `vhom_not_unique`), rigidified UNDER delta-surjectivity
  (`vhom_unique_of_onto` — sufficiency plus one non-onto
  countermodel, no equivalence), and licenses passage entry
  pre-retention and pre-observation (`kernel_licenses_entry`,
  `entry_pre_observation`, `passage_gateway_unique`) — where the
  kernel's own contribution is ENDPOINT DISTINCTNESS ONLY: the other
  two conjuncts (candidate A at the sealed pre-retention state, empty
  retention store) are sealed constants that do not mention the
  kernel, and no map from an arbitrary kernel into the passage state
  is claimed.

**Terminals issued** (scopes in full in
`artifacts/primitive_contact.json` and the receipt):
CONTACT_INCOMPARABLE_WITH_COUNTERMODELS (primary), with the asymmetry
proved — the native→arriving gap is signature-level and permanent
(countermodels exhibited at carriers 1/2/3; carrier MINIMALITY is
proved for one reading only, Bs at 3 by `bool_bs_repr`, the rest
being least-carrier-by-signature METATHEORY or explicitly unclaimed),
while the arriving→native half of the code is an ABSENCE claim about
the sealed corpus rather than a countermodel — that gap was
content-level and is closed this run by `ObsDescent` under the
identical axiom budget; COMMON_PRIMITIVE_KERNEL_REPLACES_BOTH, scoped
to the overlap only (it does not replace native orientation, stores,
operations, or passage dynamics);
CONTACT_EQUIVALENT_UNDER_DECIDABLE_ZERO_PLUS_APARTNESS_ADMISSIONS, on
the relational core only, under two decidability admissions (one per
direction) and a field-for-field premise that is not reproducible
from this repository.  **Not issued**, with recorded reasons:
CONTACT_STRICTLY_STRONGER (refuted by the countermodels) and
NATIVE_STRICTLY_STRONGER (it would launder this run's reconstruction
into the sealed record).  The 37 collision cells are machine-readable
in `ContactKernel.contactCells`, mirrored in
`artifacts/primitive_contact.json` and cross-checked by test, with
five independent finite enumerations (E1-E5) whose bounds are
recorded in the artifact.  What is machine-checked about the cells is
their COUNT (`contactCells_length = 37`) and the byte-level agreement
of the Lean literal with its artifact mirror; each row's status and
size annotation is a DECLARED LABEL naming the theorem that carries
it, and it is that named theorem — not the row — that is the
evidence.

