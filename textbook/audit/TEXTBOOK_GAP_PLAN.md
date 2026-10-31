# Textbook gap audit and teaching plan

Date: 2026-10-28. AuthorityEffect: None.

## The goal

Enable a determined teenager with no prior philosophy or mathematics study
to acquire useful intuition quickly, explain the ideas accurately, and
apply them to unfamiliar questions about observation, distinction,
information, change, and models of reality.

This is now the active goal for this chat. Completion requires evidence of
reader comprehension and transfer, as well as correct and reproducible
content. The target is an ability the reader develops, not a number of
pages, theorems, links, or passing software checks.

## Initial publication and custody

- Published Wiki: `28035b60c9b73ce98b050be5c9e0739b4c2356ab`.
- Source edition used by that Wiki: `cd3d202c5742e7c0aa3083c92bad86ff03d1d3cf`.
- PR #291 remains open, draft, and unmerged for the author.
- Base `main` for the initial audit: `e0faff5a55823181a8bd84fa30800e558e9432c0`.
- The new first-steps work is an independent source change based on main.
  It does not extend PR #291 or edit the sealed derivation.

Subsequent update, 2026-10-28: the author merged PRs #291 and #292.
The Path lab is prepared directly against the resulting main
`e00781389fb4e6b07170fe7aae748c7c57ba517f`. The initial custody bullets
above record the earlier publication, not current open-PR status.

## What is present, and what that establishes

| Population | Current finding | Interpretation |
|---|---:|---|
| Part 1 lessons | 75 | Sealed-development curriculum exists |
| Institution lessons | 18 | A research curriculum exists for four named trees |
| Sealed Lean modules | 75 | All 75 have coverage-matrix sections and assigned units |
| Canonical research trees | 123 | Counted using `ci/research_index.py`'s actual population rule |
| Trees with dedicated research lessons | 13 | Four institution trees, `standing_commitment`, three selected Boundary-lab introductions, `identification_dual`, `qm_bridge`, selected `native_bridge` claims, selected `native_structure` costs, and selected P200 recording protocols |
| Other canonical trees | 110 | No dedicated lesson treatment is established by the current curriculum |
| Manim overview scenes | 12 | Groups of lessons have short previews; individual concepts still need slower worked treatment |

The research population includes parked work, frozen experiments, tooling,
and open questions. Its size does not imply 123 active programs or 123
validated theories.

A theorem name or source path in a lesson establishes a reference, not
that its meaning has been taught. The substantive versus auxiliary
classifications still need semantic teaching review.

The [source/compiled declaration review](DECLARATION_REVIEW_2026-10-28.md)
reconciles 2,564 source heads to compiled names and locations, correcting
20 comment matches and ten missed unnamed instances in the historical
regex inventory. The module summary counts now state their population.
This improves the review baseline without certifying semantic coverage.
Unit 37's new first pass teaches classification, restriction, selection,
and the limits of example-based agreement before its optional formal
walkthrough. Changed-label practice has separate folded answers.

## The sealed derivation: no whole Lean module is missing, but teaching work remains

1. **A first toolkit for reasoning.** Build short exercises introducing a
   rule, an example, a non-example, a function, an implication, an “if and
   only if,” “every,” “some,” a counterexample, and a hypothesis. Existing
   chapters use these ideas; a zero-background route must teach their use
   before presenting long formal statements.
   The new [Reasoning lab](../reasoning_lab/README.md) supplies eight
   short lessons on these prerequisites, including functions, implication,
   equivalence, finite quantifiers, witness order, hypotheses, and evidence.
   Separate packet practice and answers test new labels and columns.
   Its finite calculations and book proofs do not establish novice mastery.
2. **Distinctions between formal systems.** Give a persistent map of the
   token-aware Python regime, token-erased Lean regime, relational
   difference setting, passage state, represented world, and institutional
   presentation. A shared term such as “observer” does not supply a bridge.
   The new [model map](../change_lab/MODEL_MAP.md) supplies these owners
   and boundaries. Its two worked passage/world comparisons show why
   activity and exhausted-menu obstruction cannot be silently identified.
3. **A complete worked search.** The new [search lab](../search_lab/README.md)
   follows one separation demand through
   candidate generation, both cost measures, all tied alternatives,
   isomorphism witnesses, stopping bounds, export, and independent replay.
   Its worked laboratory now uses `verify_full_export`, `find_iso`, and
   `complete_within`, reproduces both seed readings, and checks bounded
   minimum responses against unpruned enumeration. Reader comprehension
   of that laboratory still requires testing.
4. **A complete worked obstruction and repair.** The search lab now varies
   protected pair demands and item budgets on one three-entry ledger,
   exhibiting both refused responses and a two-item repair. The new
   [change lab](../change_lab/README.md) holds three positions fixed while
   varying retention, protection, observation, budget, permission, and halt.
   It records 48 event applications, distinguishes proposal from execution,
   and compares refusal followed by repair with an absorbing halt. These
   are supplied passage rules, not an authorization protocol or a general
   bridge to the search grammar. Novice comprehension remains unmeasured.
5. **A connected visual account of later mathematics.** Classes, maps,
   paths, loops, signed boundaries, and descent need diagrams that grow
   from a familiar example over several steps. A twelve-second overview
   cannot carry the whole derivation of these notions for a new reader.
   The new [Path lab](../path_lab/README.md) supplies seven visual lessons
   on graphs, walks, signed endpoint counts, face guards, alternating
   boundaries, and shared-edge cancellation. Its diagrams keep cell
   membership separate from coefficient sums. The transfer exercise changes
   the shared facet's default signs. The new [Map lab](../map_lab/README.md) supplies eight more lessons
   on functions, consistent grouping, representative order, descent,
   paired answers, refinement, image-only uniqueness, and finite versus
   global domains. Its diagrams distinguish cards, class labels, and
   requested values; its transfer task changes labels and questions.
   These routes are introductions, not semantic reconciliation of every
   later theorem. The research curriculum remains open; novice
   comprehension remains unmeasured.
6. **Semantic reconciliation of the coverage map.** This change corrects
   the opening to distinguish 62 direct imports, the 63-module import
   closure, and 12 parked modules, and separates the `FROZEN` custody
   mark from theorem scope. Its claims of complete prerequisite and
   declaration coverage require independent checking.
   The [selected-chapter reading review](READING_REVIEW_2026-10-28.md)
   now removes those unsupported completeness claims, identifies an
   inconsistent declaration total and comment matches in the historical
   inventory, and checks the 75 module rows plus 93 recorded prerequisite
   nodes and 156 edges (no cycles or forward edges). This checks the
   recorded graph only. Units 44, 61, and 67 and the entrance receive a
   first semantic/readability repair; a comment-aware declaration census,
   the S/A classifications, and the remaining chapters still need review.
   The [early-chapter follow-up](EARLY_READING_REVIEW_2026-10-29.md)
   adds thirteen first passes in Units 04–16 and fixes selected errors:
   valid-but-wrong indices, overbroad erasure transport, omitted initial
   invariants, a stronger converse than the displayed proof, and one-target
   versus two-target avoidance. Fresh-data class growth is now a checked
   counterexample to the old title's blanket no-power reading. This does
   not close the remaining per-declaration semantic review.
   The [requests and cost follow-up](COST_READING_REVIEW_2026-10-29.md)
   adds six first passes in Units 17–22, separates accepting a task from
   meeting it, corrects the unknown-form counterfactual, and shows how a
   uniform rule can remove a witnessed distinction. Minimum class,
   literal choice, cost ordering, and actual admission remain separate.
   The [relation follow-up](RELATION_READING_REVIEW_2026-10-29.md) adds
   four first passes in Units 23–26. It corrects the counterexample's
   quantifier scope, the global-versus-particular inequality reading,
   implicit operational enforcement, and the overbroad fact/law title.
   Fixed relations, unrestricted positive extensions, and constrained
   extension families now have different questions and checked examples.
   The [finite and transport follow-up](FINITE_READING_REVIEW_2026-10-29.md)
   adds four first passes in Units 27–30. It qualifies raw quotient
   grouping, counts states separately from rounds, carries query pairs
   through renaming, and distinguishes candidate generation from validity.
   Fresh-context agreement now includes the uniform-rule case, and the
   malformed-base example makes the old-form range condition explicit.
   The [transitions and response follow-up](ROUND_READING_REVIEW_2026-10-29.md)
   adds five first passes in Units 31–35, bringing the consecutive revised
   opening sequence to Units 04–35. It distinguishes the full transition
   relation from selection, bounds recorded demands without assuming
   validity, and checks that a failed two-item recipe can have a longer
   repair. Stale rules and an unused source bound receive explicit scope
   notes. These selected corrections do not complete semantic coverage.
   The [representation and observation follow-up](VIEW_READING_REVIEW_2026-10-29.md)
   adds first passes in Units 36 and 38–41 while preserving Unit 37's
   earlier revision. Units 04–41 now have a consecutive concrete opening
   route. It distinguishes membership from record equality, repeated
   tokens from occurrence positions, receipt payloads from a link-only
   observation, and fixed-radius limits from failure of richer observation.
   These are selected source-grounded corrections; broader semantic and
   teaching coverage remains open.
   The [capacity and kernel follow-up](CAPACITY_READING_REVIEW_2026-10-29.md)
   adds or expands five first passes in Units 42–46. It separates bounded
   colour inputs from output label size, a static strategy family from a
   runtime, active-pair conditions from menu exhaustion, and available
   candidates from permission to execute them. The revised opening route
   now extends through Unit 46. Remaining later chapters and research
   teaching still require substantive review.
   The [panels and generation follow-up](PANEL_READING_REVIEW_2026-10-29.md)
   expands five openings in Units 47–51, extending this route through
   Unit 51. It separates panel-dependent certificates, policy-dependent
   stopping, generated candidates, completed blocks, and finite comparison
   classes. The locatedness discussion now distinguishes an explicit
   Boolean relation table from a finite carrier with arbitrary relation
   propositions. The four OPEN cells remain unresolved; later chapters
   and research teaching still need review.
   The [maps and relation laws follow-up](MAPPING_READING_REVIEW_2026-10-29.md)
   extends the consecutive opening route through Unit 56. Five examples
   separate maps from chronology or inequality preservation, an interface
   from its chosen witness, generated menus from all accepted columns,
   count agreement from connectivity, and logical negation from ignorance.
   Six new book reports support these distinctions. Later chapters and
   dedicated research teaching remain open.
   The [replay and boundary follow-up](REPLAY_READING_REVIEW_2026-10-31.md)
   continues the consecutive opening route through Unit 61. Four worked
   openings and a compression prediction distinguish notes from matched
   support, own-controller replay from another replay, bounds from pair
   distinctness, unreduced storage from coefficients, and representatives
   from grouping. Eight added book reports verify these selected claims.
   The remaining core Units and per-declaration semantic coverage stay open.
   The [protection and event-summary follow-up](PROTECTION_READING_REVIEW_2026-10-31.md)
   extends that opening route through Unit 66. Four worked examples and
   a zero-table prediction distinguish update promises, observation
   repair, separately supplied growth, raw profile comparisons, and
   event-history information. Seven book reports support the selected
   claims; obsolete names and omitted hypotheses in five curriculum rows
   are corrected. Later core lessons and broader semantic coverage remain open.
   The [descent, selection, and renaming follow-up](DESCENT_READING_REVIEW_2026-10-31.md)
   brings this revised opening sequence through Unit 74. Eight prediction
   checkpoints distinguish class answers, zero tests, ordered-pair
   transport, duplicate questions, round trips, loops, side choice,
   composition relations, and form references. Eight new book reports
   support the examples. The common record's diagonal-zero hypothesis
   and the finite numerical scope of Unit 71 are restored explicitly.
   Full semantic teaching coverage, research integration, and novice
   comprehension and transfer remain open.
7. **Evidence and reality.** Add exercises in separating a definition,
   a deduction, a computation, and a measurement. Give a model prediction,
   identify an observation that could disagree with it, and explain what
   the disagreement would change. A theorem about an observer's tests
   establishes its formal conclusion under its assumptions; an empirical
   application additionally needs a declared measurement correspondence.
   The [Reasoning-lab evidence continuation](EVIDENCE_READING_REVIEW_2026-10-31.md)
   now supplies four short lessons, a declared paper-card protocol,
   fictional raw logs, a mismatch and conflicting repeat, partial-answer
   interpretation, changed-envelope practice, and an optional blank
   physical worksheet. Its 72 finite comparisons and added axiom-free
   logical proof do not establish actual measurements, a physical cause,
   or novice transfer. Subsequent hosted checks covered the twelve exercise
   cases and a sampled phone-width result panel; full accessibility and
   the wider research bridges remain open.

## Institution teaching follow-up

The [I00–I17 reading review](INSTITUTIONS_READING_REVIEW_2026-10-31.md)
adds eighteen concrete openings and checks selected scope claims from the
four existing institution research owners. It fixes the I17 book checker
without changing those owners. This improves the existing Part 2 material;
it does not add coverage of further research trees or establish reader mastery.

## First dedicated research extension

The [Growth lab](../growth_lab/README.md) now supplies eight short lessons
for `standing_commitment`: pair counting, declared rules, observations,
conditional generation, reopening, and the separate service experiment.
Its finite counterexample shows why peak arrivals need not equal the least
budget clearing a selected horizon. It distinguishes the source's proved
viewless count from the related two-sided tree's different finite setting;
that comparison is not a full treatment of the latter tree.
The [Boundary lab](../boundary_lab/README.md) now adds seven short
lessons for selected claims in `boundary_seed`, `side_free`, and
`oriented_boundary`, with a swap desk, four figures, changed-example
practice, and explicit model boundaries. The kind proposal does not
discharge `SF-OPEN-A`; no general cost or physical claim is inferred.
The [Same-record lab](../identification_lab/README.md) adds seven lessons
for `identification_dual`: equal profiles without identity merging,
third-party effects, promises versus budgets, later costs, and why a
separation pruning theorem does not transfer to the opposite goal.
Its 24 root probes, two continuations, one outside-bound reply, and two
changed-table practice probes are bounded computational evidence, not
new Lean theorems. The general identification conjectures remain open.
Wider boundary/orientation treatment and the other research clusters
still remain. The [Number lab](../number_lab/README.md) now supplies
nine lessons on counts, positive shares, the zero-total exception,
signed steps, squares, coordinate sums, lost readout information, and
reversal groups. It introduces selected `qm_bridge` claims after their
arithmetic prerequisites, retaining the supplied model and open rows.
Its 37 book/native reports do not establish a physical correspondence
or discharge the requested independent encoding review. Unit 64's
new first pass and six-part claim replace the dense opening. Its
pseudocode now separates a bounded test from the all-integer theorem,
using the zero-only box as a counterexample to the former inference.
The [Map-lab changing-source continuation](NATIVE_PATH_READING_REVIEW_2026-10-31.md)
adds six short lessons for selected `native_bridge` claims: actual-step
paths, state-threaded translation, injective codes, faithful observations,
and labels versus actual event equations. Its seven traces include locally
valid but disconnected rows; the book supplies an adjacency gate matching
the native Lean type. Event selection and later read-back rows remain open.
The [Path-lab cost continuation](PATH_COST_READING_REVIEW_2026-10-31.md)
adds six lessons for selected `native_structure` claims, covering signed
costs, potentials, full-state loops, commuting squares and verified swaps.
Its diagram and dual-cost desk separate closedness from exactness without
claiming a physical conservation law. The native action/charge questions
and the separate conservation carrier remain outside this introduction.
The [Reasoning-lab protocol continuation](OPERATIONAL_PROTOCOL_READING_REVIEW_2026-10-31.md)
adds six lessons for selected P200 claims: separate targets and records,
read/write dependencies, probe agreement, configured diagnostics and
actual relay updates. Its bounded input checks remain separate from the
formal carrier's unbounded natural-number fields and from measurements.
P201 unit/calibration rules remain a separate next teaching step.
The [I00–I03 definition follow-up](INSTITUTION_FOUNDATIONS_READING_REVIEW_2026-10-31.md)
then returns to the formal route: one continuing table, separate input/
output/lookup roles, three-step class counting, folded source proofs and
six changed-example practice tasks. This improves four Units' definitions
without certifying the remaining paragraphs of the textbook.
The [I04–I07 follow-up](INSTITUTION_ALIGNMENT_READING_REVIEW_2026-10-31.md)
continues the definition-level pass through combined reports, alignment,
loss and stationary steps, with six further changed-example tasks.
The [I08–I11 follow-up](INSTITUTION_POLICY_READING_REVIEW_2026-10-31.md)
adds worked target, fallback, approval and pair-policy distinctions and
six changed examples. The [I12–I17 continuation](INSTITUTION_ACQUISITION_READING_REVIEW_2026-10-31.md)
adds eight further tasks and works through probing, table encoding,
fixing under promises, regime updates and carried guard codes. These
selected deeper definition passes reach I17; they do not certify every
research claim or paragraph of Part 2.
The dedicated introductory tree count is now thirteen, leaving 110 without
such treatment. Directory counts guide discovery;
they do not set a requirement for equally sized modules for every tree.
Comprehension, transfer, and retention remain unmeasured.

## Research that still needs lessons

These are proposed teaching clusters, not claims that the source packages
already form one verified mathematical chain. Each lesson needs its own
source and scope check. Full tree-by-tree placement is in
[research_inventory.md](research_inventory.md).

| Proposed cluster | Representative sources | Teenager's entry question | Scope to carry into the lesson |
|---|---|---|---|
| Boundaries, orientation, and order | `boundary_seed`, `side_free`, `oriented_boundary` | Does drawing a divider add something? What changes when its sides are named? | The side-free control's price comparison is scoped. The later oriented-boundary argument is an analytic proposal under its own assumptions; its corrected custody record does not discharge the isolated control's `SF-OPEN-A`. |
| Growth and standing commitments | `standing_commitment`, `two_sided_commitment`, `identification_dual`, `second_stake` | Why can one rule create more work when another item arrives? | Under the stated all-pairs commitment, growth from n data adds n demands. The commitment and growth are supplied; this does not generate a first commitment. |
| Native paths and faithful translations | `native_bridge`, `domain_adapters`, `represented_execution` | Does encoding the same numbers mean two machines behave the same way? | A commuting transition square alone is weak. Observation preservation and actual-step paths matter. Cycle refusals have exact carrier and observation hypotheses. |
| Costs, loops, boundaries, and conservation | `native_structure`, `conservation_ladder`, `cost_cohomology`, `m109_obstruction_homology` | If every small square balances, must the total cost come from a height? What can remain unchanged as a system moves? | Closed need not mean exact. Conservation uses its supplied action, variations, symmetry, and stationarity. The sealed reachable passage has the stated no-nontrivial-charge result; general physical conservation is not established by it. |
| Numbers, addresses, and algebra | `g011_finitary_substrate`, `m104_equality_order`, `m105_number_tower`, `m108_internal_algebra` | How do counting, negative quantities, and fractions work when we build their rules explicitly? | The grammars, constructors, equivalences, and domains must be admitted and named. A numerical development in research does not make numbers derived from the opaque mark. |
| Observation, information loss, and limits | `natural_sections`, `observer_visibility`, `limit_and_observer`, `x300_observer_information` | When can a lost distinction be recovered? When is a consistent choice impossible? | Natural-section criteria concern particular families and admissible pairs. Channel and uncertainty results retain their declared finite and exact-arithmetic domains. |
| Measurement, units, protocols, and composite systems | `p200_operational_protocols`, `p201_relational_spacetime`, `p203_composite_systems`, `p204_operational_valuations` | What changes when we change units, combine two systems, or repeat a measurement protocol? | These are admitted operational models. Calibration laws and finite constructions need an explicit bridge before a physical interpretation is claimed. |
| Finite combination effects and the readout bridge | `qm_bridge`, `p208a_path_interference` | Can two preparations with equal individual weights give different combined readouts? | The latest bridge recovers an information residual. Its readout formula is separately admitted. Under that formula, explicit pairs give readouts 4 and 0; three examples give 4, 2, 0. The general real-part row is conditional, and the later transport/native-source rows remain open. |
| Context, correlations, finite transformations, and codes | `p208b_contextuality_nonlocality`, `p208c_commutator_tomography`, `p209a_wigner_phase_space` through `p209d_nonclassical_horizons` | Can all context-dependent answers fit one shared assignment? Which mistakes can a code detect? | Teach the exact finite exhibits and their corrections. Matrix examples, parity arguments, and finite codes do not automatically supply a general physical theory. |
| Meaning, intervention, reasoning, and agency | `x301_formal_semantics`, `x302_operational_reasoning`, `x303_bounded_agency`, `m114_solver_adapter`, `alpha_engine` | What observation would distinguish two claims? Why does a good proposal still need authorization? | Interventions and target valuations are supplied in the toy models. The agency Lean carrier does not transport the Python controller. Alpha evaluation, authorization, and replay remain separate. |
| The research casebook | `second` and its fourteen rung trees, `post_seal_walk`, `evidence_graph`, `estate_honesty` | How do we learn from failed attempts and revise a claim without losing its evidence? | The second derivation is a frozen research-stage record with open obstructions and an unsatisfied original completion gate. Later freeze records govern preserved draft headers. |

The remaining trees belong in the full inventory and selected technical
appendices. We should choose main-text material by explanatory value and
prerequisites, rather than give every research folder an equally long chapter.

## An inventory defect to repair first

The previously published Wiki builder discovered 115 directories by checking for root README,
STATUS, or contract files. The canonical index instead counts tracked
research trees, with explicit exclusions for `notes` and `e2e_tests`.

Consequently the builder omits these ten canonical trees:

`boundary_seed`, `genesis_continuation`, `higher_order_diagonalization`,
`iso_sound_lean`, `oriented_boundary`, `portable_interface`, `second`,
`seventh_constructor`, `sign_tower`, and `twin_pricing`.

It also includes the two excluded non-tree directories. The resulting
115-directory table is neither the canonical 123-tree census nor a teaching
inventory. This defect was found after publishing the approved readability
edition. The independent first-steps change repairs this population rule;
PR #291 has not been extended.

Use `ci/research_index.py` as the owner of the population, and add a
regression where a valid tracked tree has a `FINDINGS.md` or `CLOSURE.md`
but no README, STATUS, or TREE_CONTRACT. The builder and verifier now consume the canonical population, with
regressions for markerless trees, stale rows, and misleading prose mentions.

## The teaching structure

Keep existing unit IDs for evidence custody. Add a reading route made of
smaller lessons, with a slow main explanation and optional formal detail.

1. **Seeing and telling apart.** Labels, items, tests, profiles, and a
   witnessed difference. Use a handful of cards throughout the first route.
2. **Rules and reasons.** Admissions, deductions, hypotheses,
   counterexamples, and finite bounds. Teach the notation as it is needed.
3. **Keeping and losing information.** Signatures, merging, compression,
   recovering answers, and joint views. Reuse the same cards.
4. **Change and constraints.** Events, histories, obstruction, repair,
   refusal, costs, and symmetry. Work one complete example end to end.
5. **Boundary, order, and growth.** Compare the separate research models
   explicitly, including controls and unresolved differences.
6. **Building mathematical tools.** Counting constructions, maps, graphs,
   numbers, algebra, probability models, and signed boundaries, in the
   prerequisite order needed for the next applications.
7. **Models tested by observations.** Protocols, calibration, combination effects,
   context, conserved quantities, and intervention. Every application
   names which correspondence is assumed and what could test it.
8. **Institutions and research practice.** Combined knowledge, probing,
   truth targets, authorization, fallible models, and open questions.

Parts 1–4 are the first release target. Parts 5–8 require staged source
audits and new worked lessons. A chapter can be short while the complete
curriculum remains deep.

## The contract for each core lesson

- One concrete question and one principal new idea.
- A visible example, followed by a prediction before the explanation.
- A definition that explains every new term used in it.
- A non-example that marks the boundary of the definition.
- A small change the reader can make and observe.
- A worked explanation, then a nearby problem and an unfamiliar transfer
  problem with a separate answer key.
- The exact assumptions, a useful counterexample, and a short account of
  what the result establishes.
- Optional expandable notation, implementation, source theorem, and
  receipt details after the intuitive explanation.

Avoid a glossary whose definition merely replaces one unknown word with
three new unknown words. Each prerequisite term needs an earlier lesson,
an immediate plain-language explanation, or a deliberately optional appendix.

## A first acceptance specification

These are proposed development targets, not achieved learning results or
a claim about an established educational standard.

After a twenty-minute entrance, a novice should be able to:

1. distinguish an item's label from an observation about it;
2. predict collapse or separation in a new three-item example;
3. point to the test witnessing a separation;
4. identify one admission on which the example depends;
5. explain why adding a name and adding a discriminating test have
   different effects.

After the first hour, the reader should also recover a simple claim from
a presentation, exhibit a pair that blocks recovery, and explain the
consequence of one changed assumption. These are tasks to test with
previously unseen examples, not phrases to memorize.

A small novice pilot should record completion time, incorrect predictions,
where an unfamiliar word blocks progress, and the reader's own explanation.
Proposed provisional targets are at least four of the five entrance tasks
correct with reasons, plus success on a changed example. A delayed check
should assess whether the intuition survives beyond the session. The
targets should be revised from observed performance rather than treated
as established guarantees.

No novice comprehension pilot or delayed-transfer evidence was located
in the textbook materials inspected for this audit. Software and Lean
checks establish other properties. Goal completion remains open until
the reader-facing criteria have been met.

## Next work packages

| Order | Concrete deliverable | Acceptance |
|---|---|---|
| 1 | Repair research discovery and reconcile the coverage map | Canonical population matches; the missing-marker fixture fails before and passes after repair; no classifier population or frozen source is altered |
| 2 | Build the first five small lessons and a single coherent card-based explorer | One idea per lesson, explicit prerequisites, prediction and counterexample, working widget, exact source and scope |
| 3 | Create the entrance and transfer assessment with separate answers | Unseen examples test the five stated abilities; no answer leakage in the learner route |
| 4 | Run and record a novice pilot when readers are available | Record comprehension and time; revise specific failed explanations |
| 5 | Add boundary/order/growth and native-path/cost research modules | Read owner ledgers and corrections; keep analytic proposals, finite calculations, conditional theorems, and open bridges distinct |
| 6 | Continue numerical and operational prerequisites beyond the Number lab's first finite readout introduction | The first counts/shares/signs/coordinate toolkit now exists; wider number constructions, protocol/calibration/composition lessons, and later bridge rows remain open. No general physical claim is inferred from finite exhibits |
| 7 | Expand the research casebook and application route | Show successful results, counterexamples, failures, custody, and remaining questions with their actual evidence |

## First deliverable and audit limits

The first-steps route now supplies Lessons 00–04, the card explorer,
practice on a different four-item table, a separate assessment and answer
keys, and an exact source map. Its finite model check covers 64 tables;
the sealed Python replay covers all four question subsets (256 histories).
The lookup check independently enumerates possible recovery rules.
These are computational checks, not evidence of reader comprehension.

The search lab adds eight short lessons, a results desk, and separate
practice answers. It records all fourteen well-formed two-item plans in
the main case, all minimum ties, explicit relabeling maps, protection and
budget changes, and distinct stopping reasons. Its longer portable export
has 128 nodes and 130 edges, including three independently checked merge
edges. A changed price still passes the limited replay verifier; a separate
full lesson-record check rejects it. This makes evidence scope itself a
worked lesson. The lab does not supply a general Python-to-Lean refinement
proof, a license protocol, or the later research curriculum.

The change lab adds eight short lessons, separate practice answers, a
model map, and a recorded passage desk. Its book-Lean checks prove 118
concrete equalities and two general protection-within-retention invariants.
It also corrects Units 54–55: refinement has no licence gate; activity
does not imply menu exhaustion; singleton proposals need not be unique;
and the driver supplies the selected event and funding. The displayed
columns do not create their own execution. Neither passing software
checks nor the new book invariant establishes reader comprehension.

The research table records the canonical indexed population at the audit
snapshot and a proposed teaching placement. It does not run research
verifiers or assert that every tree is active, valid, or connected to the
others. New tree additions require refreshing that inventory.

Primary semantic reading for the proposed clusters includes source
README/status/claim records for the native bridge, native structure,
conservation, domain adapters, boundary/side-free/oriented-boundary work,
standing commitments, natural sections, the second-derivation freeze,
the finite readout bridge, and selected numerical, operational, and
information packages. This is a curriculum audit, not a revalidation of all
123 research trees. Each future lesson must read its owner's current
claim ledger and corrections before importing any claim.

For the current route's commands and verification reach, see
[../first_steps/DEVELOPMENT.md](../first_steps/DEVELOPMENT.md). The whole
teaching goal remains open until the later curriculum and reader evidence
exist.
