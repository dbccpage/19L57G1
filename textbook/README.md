# The Genesis Textbook

AuthorityEffect: None. This folder teaches the sealed derivation; it is not
part of it. Nothing here is an input to `prompt/`, `paper/`, `code/`,
`lean4/Derivation/` or `artifacts/`, and nothing here changes them. Where a
unit and the Lean disagree, the Lean wins.

The beginner routes develop one small idea at a time. The formal units
group related definitions and theorems and can contain many results.
Start with their concrete first pass, then read the definitions, hypotheses,
proofs, and limits. The formal-reading guide below helps connect a familiar
example to its actual source statement.

## Source

Units 00 to 03 were written against `main` at
`23979a46308219b4cc9e7e172e4e32511f8efdb0` (2026-10-24); Units 04 onward
against `main` at `33100245` (2026-10-28, after #283). The sealed files the
units quote are the same at both commits. Lean is quoted from
`lean4/Derivation/`. Axiom reports are read from the committed
`artifacts/lean_axioms.txt` and, for the book's own Lean, from a local
Lean 4.33.0 build of `lean4/`; a unit says so when it did not rebuild Lean.
Part 2 of the book (`textbook/institutions/`, see **Parts**) covers the
post-freeze research trees `actor_institution` (#284), `two_theorems` (#277),
`uncollapse` (#275), and `interpreter_verdict` (#278), outside the seal.

For a concrete example before the formal development, begin with
[`First steps: three cards, two questions`](first_steps/README.md): five
short lessons, a prediction-first explorer, and separate practice answers.
No previous mathematics or philosophy is assumed.
The [`Reasoning lab`](reasoning_lab/README.md) supplies the next toolkit:
rules, functions, if-then claims, witnesses, counterexamples, and hypotheses.
Its [evidence continuation](reasoning_lab/08_from_a_model_to_a_trial.md)
adds a protocol, explicitly fictional trial logs, conflicting repeats,
uncertain readings, and an optional physical worksheet. It separates
calculations on supplied records from observations actually collected.
Continue with the [`Search lab`](search_lab/README.md) for a complete
worked demand, candidate search, price comparison, protection example,
and portable event replay.
The [`Change lab`](change_lab/README.md) then separates retained pair
records, protected demands, observation, budget, permission, refusal,
and halt, with a map of the different formal settings.
The [`Path lab`](path_lab/README.md) supplies the next visual toolkit:
points, connections, walks, signed counts, faces, and cancelling boundaries.
The [`Map lab`](map_lab/README.md) then follows original cards through
class labels to requested answers, including blocked recovery, paired
questions, representative order, and uniqueness on the observed image.
Its [changing-source continuation](map_lab/08_states_and_events.md)
adds actual steps, replay, state encodings, observation preservation and
mislabelled-history checks from selected `native_bridge` research. Distinct
codes and correct step squares can still lose the requested observation.
The [`Growth lab`](growth_lab/README.md) then enters the research
`standing_commitment` tree: which pairs remain unresolved, when arrivals
create demands, and why assumed service is different from a proved repair.
The [`Boundary lab`](boundary_lab/README.md) introduces selected results
from three more research models: the declared two-sided division, repeated
labels, swap witnesses, permission restrictions, and a scoped price menu.
It keeps the models and their unresolved comparisons separate.
The [`Same-record lab`](identification_lab/README.md) asks the opposite
of separation: add judgments so two profiles match while their internal
positions remain distinct. Seven worked lessons compare side effects,
kept promises, bounded refusals, and the price of a later demand.
The [`Number lab`](number_lab/README.md) teaches totals, shares, zero,
signed steps, squares, and coordinate addition before selected finite
readout examples. It connects Unit 64's arithmetic to an introduction
to `qm_bridge`, keeping its supplied formula and open rows explicit.
After that toolkit and the Map-lab continuation, the
[Path-lab cost route](path_lab/07_two_cost_questions.md) introduces
signed path costs, potentials, return loops and commuting squares. It
explains the source's closed but non-exact state-change count and keeps
the earlier face calculus separate from native event histories.

New readers can then read [`START_HERE.md`](START_HERE.md) (see also the
short spoken introduction in [`video_script_15s.md`](video_script_15s.md)).
The [formal-reading guide](reading_formal_statements.md) links these small
examples to the formal chapters, with separate practice and answers.
For the source-placement index and recorded lesson dependency graph,
see [`derivation_coverage.md`](derivation_coverage.md); for the 75-module
audit records, see [`audit/README.md`](audit/README.md).
For the remaining teaching work and the research-to-curriculum inventory,
see [`audit/TEXTBOOK_GAP_PLAN.md`](audit/TEXTBOOK_GAP_PLAN.md).
The [Units 47–51 follow-up](audit/PANEL_READING_REVIEW_2026-10-29.md)
extends the concrete opening sequence through Unit 51 and records selected
corrections about panels, policies, candidate menus, completed stages,
and the limits of finite comparison.
The [Units 52–56 follow-up](audit/MAPPING_READING_REVIEW_2026-10-29.md)
continues through maps, interfaces, supplied growth, and relation laws,
with collapsing-map and colour-agreement examples before formal notation.
The [Units 57–61 follow-up](audit/REPLAY_READING_REVIEW_2026-10-31.md)
continues through interpreter records, controller-specific replay,
attachment, signed coefficients, and ordered compression representatives.
The revised concrete opening route now extends through Unit 61.

The [Units 62–66 follow-up](audit/PROTECTION_READING_REVIEW_2026-10-31.md)
continues through protected updates, supplied growth, zero-total profiles,
event summaries, and repeated versus reordered requests. The concrete
opening sequence now extends through Unit 66.

The [Units 67–74 follow-up](audit/DESCENT_READING_REVIEW_2026-10-31.md)
continues through class answers, zero relations, ordered-pair selection,
round trips, symmetry, composition, and consistent form renaming. The
revised concrete opening sequence reaches Unit 74; semantic coverage
and reader mastery remain separate work.

The [institution review](audit/INSTITUTIONS_READING_REVIEW_2026-10-31.md)
covers the material after Act X: eighteen worked openings for I00–I17,
selected theorem-scope corrections, and a repaired Python transition check.

## Status marks

| Mark | Meaning |
|---|---|
| **admitted** | A definition, a declared rule, a convention, or a hypothesis. Chosen, not proved. |
| **derived** | Proved in Lean from the admitted definitions, with no extra hypothesis. A countermodel proved in Lean is derived too, and is called one. |
| **verified finite** | Computed exhaustively over a declared finite search space. The unit states the bounds; the result says nothing outside them. |
| **conditional** | Proved in Lean only under an extra admitted hypothesis. The unit names the hypothesis. |
| **open** | Neither proved nor refuted, or a choice with no internal answer. |

The marks follow the paper's classification tags, which keep **[theorem]**
apart from **[finite computation]** and **[bounded theorem]**
(`paper/paper.md`, opening paragraph). A finite check is
never promoted to **derived**, and a sample check (such as Unit 01's) is
weaker still: it illustrates a theorem, it does not verify anything
exhaustively.

**derived** is always relative to the admitted definitions. No theorem in
this book proves that its own definitions were the necessary ones. Each unit
lists, under **What you need first**, the admitted definitions its claim
depends on.

## Kinds of code

| Label | What it is | Trust |
|---|---|---|
| Lean (Genesis) | Copied from `lean4/Derivation/`. | Checked by Lean's kernel when Genesis builds. The authority. |
| Python (Genesis) | Copied from `code/derivation/`. | Tested in Genesis. Tied to the Lean by executable checks, not by proof (ledger entry `CL-TOKEN-ERASURE`). |
| Lean (book) | Written for this book, held in a check script, and kernel-checked against Genesis's compiled `Derivation` library when that script runs. | Checked by Lean's kernel when the script runs; not part of Genesis's build, gates or `artifacts/lean_axioms.txt`. The script prints its own axiom report. |
| Gloss | Pseudocode written for this book. | Unchecked. Read it as a translation aid only. |

A claim proved only in the book's Lean is marked **derived (book Lean)**:
derived from the same admitted definitions, but checked by the book's
script rather than by Genesis's build. The book's Lean lives inside Python
scripts, not `.lean` files, so that it stays out of Genesis's Lean census
and toolchain tests.

Each unit that makes a computational point has a script in `checks/` that
runs Genesis's own Python. Run it from the repository root:

```
python textbook/checks/u01_genesis_underivable.py
```

From Unit 04 on, each unit also has a `checks/uNN_lean.py` holding its
Lean (book) source and the axiom report it expects. These scripts share
the runner `checks/booklean.py`, which writes the source to a temporary
file, runs `lake env lean` inside `lean4/` (or a given Lean binary with
`--lean PATH --lean-path DIR`), prints the `#print axioms` lines, and exits
0 only when every report matches. A unit's Verification table records
what each script found when it was written.

## Notation

The book writes ⟨⟩, ⟨A⟩, ⟨AB⟩ for the seed's `<>`, `<a>`, `<ab>`. Inside
Lean there are no letters, only numbered data (datum 0, datum 1, ...). ⟨AA⟩
is not in Genesis; the book uses it only as an example of a fresh token.
The letter A in ⟨A⟩ is unrelated to the candidate labels `A1`–`A5` in
`PrimDiff.lean`.

⟨ARA⟩ (A related to itself) and ⟨ARB⟩ (A related to B) are informal
inscriptions, not Genesis objects. Written down alone, ⟨ARA⟩ is one more
opaque whole and establishes no internal difference: nothing inside it is
licensed to see two endpoints, an R, or a repeated A. Units 19 and 20 use
two **later formal realizations** of them, each built from extra
admissions. (Units 23 to 25 work with an abstract relation `r` in
`PrimDiff.lean`, not with a regime, and carry their own hypotheses.)

| Inscription | Realization | What the realization admits beyond the inscription |
|---|---|---|
| ⟨ARB⟩ | `Minimality.BL` (binary link) | two data, one binary form, the instance (form 0, [datum 0, datum 1]), and the externally imposed demand that datum 0 and datum 1 be separated |
| ⟨ARA⟩ | `Minimality.BD` (binary self-loop) | two data, one binary form, the instance (form 0, [datum 0, datum 0]), and the same demand |

```lean
-- Lean (Genesis), lean4/Derivation/Minimality.lean lines 42-44
def BL : Regime := ⟨2, [2], [(0, [0, 1])], [], [(0, 1)]⟩
def BD : Regime := ⟨2, [2], [(0, [0, 0])], [], [(0, 1)]⟩
```

So `Minimality.BD_separable` (Unit 20) does not say that writing ⟨ARA⟩
separates anything. It says that in the regime `BD`, the context "form 0
with datum 0 in the second slot" holds when datum 0 fills the hole and fails
when datum 1 does, so the regime distinguishes the two data. Every later
mapping from informal notation to a Genesis structure lists the admissions
it needs, as this table does.

## No imports from nowhere

This is a standing rule of the book (author, 2026-10-28). Nothing enters the
system unless it is derived inside the system or admitted at a stated price.
In particular, the book never brings in from nowhere:

- an **observer**: a viewpoint, reader, measurer or classifier that the
  system has not admitted;
- a **container**: a background space, set, universe or totality in which
  the system's things are supposed to sit;
- a **continuum**, or any **infinity**: an infinite set of data, of
  instances, of presentations, of presentation families, of observers, or an
  unbounded supply of any of them;
- an **empty thing** treated as present: "the empty set", "the space of all
  possibilities", or a limit that has not been reached.

The system is never allowed past where it is. At each step it has exactly
what has been admitted so far: a finite ledger, built by a finite history of
events. What has not been derived or admitted is not "there but unknown"; it
is not there.

**Lean is outside the system.** Lean's types (`Nat`, `List`, `Prop`,
`Type`), its quantifiers (`∀`, `∃`), its equality and its proof checker
belong to the declared metatheory (`paper/paper.md` §2; Unit 00). `Nat` has
no largest element and `List Nat` has no longest list, but that is a fact
about the metatheory's apparatus, not something the system possesses. When
a theorem says "for every instance `i : Inst`", it is a genuine universal
statement, proved once and uniformly for an arbitrary instance; it is not a
collection of separate checks. What matters is where that quantifier lives:
it ranges over a Lean type, so it is a statement the metatheory makes
*about* the system. It puts no collection of instances, and no universal
quantifier, into the system's ledger. Every unit that discusses a universal
theorem keeps those two apart: the theorem's own quantifier, at full
strength, and what the system has admitted.

**A finite ledger does not bound what its definitions reach.** The ledger
stores finitely many admitted items, but an admitted definition can have an
unbounded extension when the metatheory reads it. The uniform rule is the
first case. In the well-formed regime `⟨0, [1], [], [0], []⟩` (one unary
form, the all-instances rule on it, no data, no instances),
`derivable` holds of `(0, [99])`, though datum 99 was never admitted, and
of `(0, [])` and `(0, [1, 2, 3])`, though form 0 has arity 1 (Unit 01;
`checks/u01_rule_extension.py`). Nothing infinite is stored: the rule is one
admitted item, a form number in a list. The unbounded part is the
metatheory's reading of `derivable`, and a unit that uses it says so. If a
later unit needs derivability restricted to admitted data, it introduces a
separate, named predicate outside the seal rather than reading the
restriction into the sealed one.

So every unit has a section **Outside the system** that lists:

1. each Lean type, quantifier or construction the unit uses that is
   metatheory, and what it is used for;
2. what the system itself holds at that point (always a finite ledger),
   and, where a definition's extension read in Lean is unbounded, that it
   is;
3. any admission the unit relies on, with its price (the events or
   hypotheses it needs);
4. any phrase in the unit that would import an observer, container or
   infinity if read as a claim about the system, and how to read it
   instead.

If a later unit needs something unbounded inside the system, it must either
derive it or admit it as a named, priced admission, and the unit must say
which.

## Unit template

1. **Claim**, with its status mark and its Lean name.
2. **What you need first**: the admitted definitions the claim depends on,
   each in Lean, then Python, then gloss. Every unit names them; no theorem
   is stated without them.
3. **The theorem** in Lean.
4. **The proof, step by step**, with no step skipped.
5. **The same fact in Python**, with the check script.
6. **Outside the system**: the metatheory's types and quantifiers the unit
   uses, what the system holds, and the price of every admission (see No
   imports from nowhere).
7. **What it shows and what it does not.**
8. **Sources**: file, theorem, axiom report, ledger entry, test.

Units 00 to 03 follow this eight-part template. From Unit 04 on, by the
author's brief of 2026-10-28, each unit keeps the **Claim** header (status,
Lean name, axioms, dependencies) and then runs through fifteen fixed
sections in this order: Question; What we already possess; New concept;
Plain-language interpretation; Pseudocode; Python; Line-by-line Python
explanation; Lean 4; Line-by-line Lean explanation; What has been proved;
What has not been proved; Outside the system; Student exercise; Answer;
Verification. The two templates carry the same obligations: the admitted
definitions are named before the theorem, no proof step is skipped, the
metatheory is listed under Outside the system, and the Verification table
plays the part of Sources. The sections were not mixed: a unit is written
in one template or the other, and this table says which.

| Units | Template |
|---|---|
| 00–03 | eight parts, above |
| 04 onward | Claim header plus the fifteen sections |

## Contents

| Unit | Claim | Lean | Status | Written |
|---|---|---|---|---|
| 00 | The mark and the external constructor | (none; seed §1, paper §2) | admitted | yes |
| 01 | Nothing is derivable at genesis | `Inertia.genesis_underivable` | derived | yes |
| 02 | Nothing is derivable without instances or rules (and one admitted rule makes unadmitted instances derivable) | `Inertia.underivable_of_empty` | derived | yes |
| 03 | Supplying a token changes nothing | `Inertia.supply_no_op` | derived | yes |
| 04 | No successor is internally forced (by the declared grammar) | (none; paper §4) | admitted | yes |
| 05 | Is ⟨⟩ admitted? Readings L and F | `Inertia.historyL_replays`, `historyF_replays` | open | yes |
| 06 | Re-admitting a token designates, it does not add | `Erasure.stepT` | admitted | yes |
| 07 | Forgetting tokens loses nothing the room can use | `Erasure.erase_replay` | derived | yes |
| 08 | Contexts, plugging, collapsed, separable | `Basic.collapsed`, `Basic.separable` | admitted | yes |
| 09 | Separable and collapsed exclude each other | `Basic.separable_not_collapsed` | derived | yes |
| 10 | With no instances, every pair is collapsed | `Inertia.collapsed_of_no_insts` | derived | yes |
| 11 | One token gives at most one datum | `Bridge.single_token_carrier_bound` | derived | yes |
| 12 | A fresh datum preserves old comparisons | `Inertia.admission_without_expressive_increase`, `Mention.collapsed_fresh_datum` | derived | yes |
| 13 | Two data need a second, different token | `Bridge.second_token_required` | derived | yes |
| 14 | Factoring through a point is equality | `PrimDiff.factors_through_point_iff` | derived | yes |
| 15 | An outside difference is not an asserted one | `PrimDiff.meta_diff_without_assertion` | derived | yes |
| 16 | ⟨A⟩ and ⟨AB⟩ are collapsed | `Inertia.R2L_collapsed`, `R2F_collapsed` | derived | yes |
| 17 | Demands are irreflexive by guard | `Basic.stepE` (impose) | admitted | yes |
| 18 | One item never answers the demand | `Minimality.cost1_insufficient_general` | derived | yes |
| 19 | The link regime `BL` (realizing ⟨ARB⟩) separates | `Minimality.BL_separable` | derived | yes |
| 20 | The self-loop regime `BD` (realizing ⟨ARA⟩) separates | `Minimality.BD_separable` | derived | yes |
| 21 | The cheapest answer is not unique under mu1 | `Minimality.mu1_minimum_not_unique` | derived | yes |
| 22 | It is unique under mu2 | `Minimality.mu2_unique` | derived | yes |
| 23 | A related pair r a b alone does not give a ≠ b (countermodel) | `PrimDiff.selfdiff_consistent` | derived | yes |
| 24 | Under irreflexivity, r a b gives a ≠ b | `PrimDiff.irrefl_witness_ne` | conditional | yes |
| 25 | Under irreflexivity, collapsing a related pair is obstructed | `PrimDiff.obstruction_under_irrefl` | conditional | yes |
| 26 | Keeping positive entries does not exclude a self-pair | `Bridge.irrefl_law_not_entailed` | derived | yes |
| 27 | An abstraction cannot see what it identifies | `Quot.quot_barrier`, `Quot.barrier_R2L` | derived | yes |
| 28 | Fixed data bound rounds that add new demands | `Counting.strict_bounded_length`, `Counting.allPairs_length`, `Counting.no_supply_round_bound` | derived / conditional | yes |
| 29 | Renaming the data changes nothing a context can see | `CountTransport.collapsed_rename`, `CountTransport.non_injective_does_not_transport` | derived | yes |
| 30 | Adding instances that avoid both targets preserves their comparison | `Mention.collapsed_append_unmentioning`, `Mention.collapsed_fresh_form` | derived | yes |
| 31 | Renaming carries transitions; choosing by index can change the outcome | `TransitionTransport.transStep_rename_fwd`, `TransitionTransport.least_pair_selection_not_congruent` | derived under stated range conditions | yes |
| 32 | The same proof with one more datum | `MinimalityF.mu2_unique_F`, `MinimalityF.genesis_mark_not_separable` | derived | yes |
| 33 | Uniform-rule items cannot minimize the declared costs | `RuleBridge.applyDelta_dropRules`, `RuleBridge.rule_item_never_minimal` | derived shortening; cost interpretation over declared measures | yes |
| 34 | Closed runs bound recorded new demands | `Rounds.round_reqs_succ`, `Rounds.closedRun_round_bound_from_empty` | derived under the declared round shape; validity separate | yes |
| 35 | A fresh mark answers a distinct pair under stated conditions | `Progress.mark_progress`, `Progress.derivable_extend` | derived (conditional response existence) | yes |
| 36 | Lists can agree on membership while differing as records | `Ext.RegimeExt`, `Ext.validResponse_ext` | derived (named operations) | yes |
| 37 | An inventory is not a derivation | `ObserverInventory.bool_irrefl_full_classification`, `ObserverInventory.residuals_not_unique` | derived; slot names declared | yes |
| 38 | Five declared ways to record a repeated token | `Refusal.nonreify_carrier_bound`, `Refusal.reifyUntagged_eq_occurrence`, `Refusal.tagged_translation_separable` | derived per discipline; the hierarchy as one theorem OPEN | yes |
| 39 | Comparing refusal protocols under declared prices | `RefusalFrontier.silent_repetition_inert`, `RefusalFrontier.min_witnessed_route_closes`, `RefusalFrontier.reflective_chain_is_initial_segment` | derived (cores); minimum computed in class, horizon 6, carrier cap 4 | yes |
| 40 | A growing chain keeps equal three-bit profiles | `Generator.depth1_obstructions_are_exactly_middle_pairs`, `Generator.generation_never_dries`, `Generator.finite_marks_outrun` | derived (specified profiles); strategy exclusion computed in class | yes |
| 41 | Every fixed radius misses some deep pairs in a long enough chain | `SeparationCapacity.depth_d_outrun`, `SeparationCapacity.depth_d_obstruction`, `SeparationCapacity.radius_one_agrees_with_sealed_depth2` | derived (specified structural profile; deep pairs and interior correspondence) | yes |
| 42 | Bounded colour windows limit the number of distinct views | `Pigeonhole.pigeonhole`, `CapacityBound.capacity_bound`, `CapacityBound.local_view_can_separate` | derived under bounded colours and locality; tightness not claimed | yes |
| 43 | Fixed colour bounds and local windows cannot clear every chain stage | `LocalFiniteAlphabet.finite_local_not_clears`, `G1Class.g1_class_exclusion`, `G1Class.clears_does_not_imply_not_fires` | derived, conditional on `FiniteDeclaration`; static class; G3, G4 conjectures | yes |
| 44 | Retained, protected, and unseen: when a pair is active | `DiffInterface.zeroRel_equivalence`, `DiffInterface.bare_reflection_certifies_active_obstruction`, `DiffInterface.drive_terminates`, `DiffInterface.bool_grammar_obstruction` | derived under declared bundles; generic closed tag need not mean no active pairs | yes |
| 45 | Replaying represented events under a fixed kernel | `Represented.support_determines`, `Represented.equiv_replay`, `Represented.represented_progress`, `Represented.cert_scope` | derived relative to fixed definitions; progress conditional on requirement WF; execution gates separate | yes |
| 46 | Repair or menu exhaustion, with two column-extension candidates | `Completion.ofWorld_obstruction`, `Completion.rule1_repair_or_extension`, `Completion.refusal_non_absorbing`, `Completion.action_dichotomy` | derived for fixed kernel under WF; transport identifies retention/protection stores; refusal historical | yes |
| 47 | Recording the evaluator panel: agreement depends on the tests | `NoOutside.effectual_outside_dichotomy`, `NoOutside.panel_equiv`, `NoOutside.certNeg_iff_panelEquiv`, `NoOutside.certC_ceiling` | derived for four fixed-kernel outputs; panel certificates read separate panel data; absolute form unformulable | yes |
| 48 | Generating candidates from a stored policy | `Constitution.driver_reproduces_tower`, `Constitution.nextFamily_stop`, `Constitution.interp_describe`, `Constitution.allDescs_complete` | derived for defined policy families; close stops at quiescence; execution gates separate; external interpreter/iteration retained | yes |
| 49 | One descriptor passes six probes in a class of 64 | `Initiality.unique_compliant`, `Initiality.accept_guard_load_bearing`, `Initiality.extension_retract_replay` | VERIFIED_FINITE, class- and battery-relative; categorical initiality not claimed | yes |
| 50 | Proving the shape of every completed tower stage | `Horizon.worldAt_spec`, `Horizon.worldAt_quiescent`, `Horizon.block_all_accepted`, `Horizon.interp_budget_bound` | FROZEN (completed-stage theorems); intermediate prefixes may be nonquiescent; separate Python budget checks | yes |
| 51 | Separate the witness, the laws, and the allowed operations | `PrimitiveCore.imp_a_d`, `PrimitiveCore.nimp_w_d`, `PrimitiveCore.nimp_a_bc`, `PrimitiveCore.e_empty_iff_d`, `PrimitiveCore.located_of_decidable` | FROZEN (17 implications, 51 countermodels); OPEN (4 located cells, scoped); VERIFIED_FINITE (the scan) | yes |
| 52 | A unique map out of the two-point arrow | `PrimitiveCats.d2_initial`, `PrimitiveCats.s2_no_hom_to_d2`, `PrimitiveCats.initials_iso`, `PrimitiveCats.two_initials_not_identical`, `PrimitiveCats.larger_not_initial`, `PrimitiveCats.no_terminal_pres`, `PrimitiveCats.no_terminal_pres2` | FROZEN; CONDITIONAL (`s2_initial_sym`, `phom2_unique_of_epi`); OPEN (terminality among surjective presentations) | yes |
| 53 | A fixed interface and the scope of its comparison | `PrimitiveContact.NativeKernel`, `PrimitiveContact.native_kernel_initial`, `PrimitiveContact.native_interface_not_representable`, `PrimitiveContact.contact_status_count` | FROZEN (re-exports); ADMITTED (interface, status strings); VERIFIED_FINITE | yes |
| 54 | From an asserted difference to a response | `PrimitivePassage.obstP_factors`, `PrimitivePassage.gate_zero_independent`, `PrimitivePassage.assertion_not_retained`, `PrimitivePassage.retention_requires_assertion`, `PrimitivePassage.two_rule`, `PrimitivePassage.extension_resolves`, `PrimitivePassage.terminal_absorbing`, `PrimitivePassage.nextFamilyP_stop` | FROZEN; ADMITTED (the pre-declaration convention and the observation policy, priced by `obst_policies_differ`); VERIFIED_FINITE (fourteen arrow witnesses) | yes |
| 55 | The first graph is supplied, its observer is created | `HigherStructure.graphAt_spec`, `HigherStructure.round_obstruction`, `HigherStructure.round_two_rule`, `HigherStructure.round_resolution`, `HigherStructure.graphAt_quiescent`, `HigherStructure.ladder_dim2`, `HigherStructure.filling_not_forced`, `HigherStructure.boundary_not_forced` | FROZEN (horizon-free round schema); ADMITTED (driver, cell calculus, sign conventions); VERIFIED_FINITE (`k4`, census, 15 mirrored rounds); OPEN (the ladder as a two-rule statement at every dimension) | yes |
| 56 | When not-apart forms an equivalence | `Apartness.indist_equivalence`, `Apartness.irrefl_alone_breaks_symm`, `Apartness.symm_without_cotrans_breaks_trans`, `Apartness.two_point_indist_trans`, `Apartness.orientations_same_apartness`, `Apartness.orientations_differ`, `Apartness.oriented_preserver_unique`, `Apartness.apart_preserver_pair`, `Apartness.clos_oriented_iff` | FROZEN; ADMITTED (the three laws); VERIFIED_FINITE (carriers 1-3 exhaustive, censuses to 4) | yes |
| 57 | The interpreter is not in its own family: what a notes-diagonal does and does not show | `InterpreterBoundary.tower_persists`, `InterpreterBoundary.family_missed`, `InterpreterBoundary.i5_boundary_is_A`, `InterpreterBoundary.i5_boundary_is_F`, `InterpreterBoundary.i5_collapse_obstructed`, `InterpreterBoundary.arbitrary_uncoded_assignment` | FROZEN; ADMITTED (the declared setting); OPEN (the denotational bridge, taught as OPEN) | yes |
| 58 | Is the controller unique? Simulations, the absorbing halt, and uniqueness only along replay | `ControllerCategory.live_census`, `ControllerCategory.tworule_executable_of_live`, `ControllerCategory.dead_without_addcol`, `ControllerCategory.refuse_distinguishes`, `ControllerCategory.erase_sim`, `ControllerCategory.no_initial_ctrl`, `ControllerCategory.strict_not_unique`, `ControllerCategory.strict_agree_on_reachable` | FROZEN; REFUTED (initiality, strict global uniqueness); CONDITIONAL (orbit agreement, one hom-set) | yes |
| 59 | Growing the carrier by one and renaming the supply | `Attachment.up_iff_legal`, `Attachment.up_executes`, `Attachment.treeAt_spec`, `Attachment.path4_star4_not_isomorphic`, `Attachment.act_up_comm`, `RenamingStructure.wf_act`, `RenamingStructure.upFamily_orbit_closed`, `RenamingStructure.collapse_not_a_renaming` | FROZEN; CONDITIONAL (`WF`, `p < s.occ.length`); REFUTED (`length` freshness, equal-cost isomorphism) | yes |
| 60 | One guard for every dimension and boundary cancellation | `LadderGeneral.uniform_guarded_filler`, `LadderGeneral.shell_refuses_general`, `LadderGeneral.pseudo_cell_countermodel`, `LadderGeneral.d2_zero_dims_2_3_4`, `BoundaryCancellation.d2_zero_unrestricted`, `BoundaryCancellation.codim2_distinct`, `BoundaryCancellation.signless_countermodel`, `BoundaryCancellation.illformed_countermodel` | FROZEN; PROOF DEFECT noted on first two conjuncts of `d2_zero_dims_2_3_4` (vacuous filter, superseded by `BoundaryCancellation.d2_zero_unrestricted`); REFUTED (signless vanishing, ill-formed facet distinctness) | yes |
| 61 | Compressing a presentation against a question list | `Compression.factors_iff_fiberConstant`, `Compression.pQ_exact`, `Compression.pQ_adequate`, `Compression.pQ_coarsest`, `Compression.factor_unique_on_image`, `Compression.descent_witness` | FROZEN; CONDITIONAL (adequacy for `pQ_coarsest`, two factoring maps on the domain for `factor_unique_on_image`, merged inputs with unequal signatures for `descent_witness`); VERIFIED_FINITE (`D4` exhibits) | yes |
| 62 | What protection buys | `StableContent.protSep_trace_stable`, `StableContent.quiescent_iff_protected_separated`, `StableContent.unprotected_separation_unstable`, `StableContent.halted_stable_not_protected`, `StableContent.openExactStabilityCharacterization` | FROZEN; CONDITIONAL (protected separation for trace stability, declared observation for the quiescence equivalence); REFUTED (unqualified converse); OPEN (live-funded converse) | yes |
| 63 | Where new occurrences come from | `GraphGenesis.response_step_fixes_graph`, `GraphGenesis.internal_family_cannot_grow_carrier`, `GraphGenesis.graph_growth_is_supplied`, `GraphGenesis.proposal_confers_no_execution`, `GraphGenesis.upProposal_executes`, `GraphGenesis.obstruction_resolved_in_carrier`, `GraphGenesis.growth_demand_not_obstruction_consequence` | FROZEN; CONDITIONAL (store bounds, live state, represented parent for `upProposal_executes`); ADMITTED (`ProposalRecord` and its cost field) | yes |
| 64 | A profile without division | `WeightProfile.profile_trans`, `WeightProfile.profile_iff_ray`, `WeightProfile.profile_scale_positive`, `WeightProfile.zero_scale_boundary`, `WeightProfile.profile_forgets_total`, `WeightProfile.unsigned_decoration_determined`, `WeightProfile.signed_square_presentations_split`, `WeightProfile.descent_iff_subsingleton_support`, `WeightProfile.claimedReadOutUniqueness_false` | FROZEN; CONDITIONAL (positive middle total for `profile_trans`, positive totals for the ray characterization); REFUTED (`ClaimedReadOutUniqueness`) | yes |
| 65 | Thirteen codes and why they are not an alphabet | `TransitionAlphabet.accepted_eq_guardHolds`, `TransitionAlphabet.wf_of_replay`, `TransitionAlphabet.retention_creates_outside_class`, `TransitionAlphabet.sig_eq_classSig`, `TransitionAlphabet.classSig_inj`, `TransitionAlphabet.exists_unique_class`, `TransitionAlphabet.classSig_not_right_congruent_occurrence`, `TransitionAlphabet.classSig_not_right_congruent_budget`, `TransitionAlphabet.refine_addCol_effect_merge`, `TransitionAlphabet.internal_family_emits_budget_write` | FROZEN; CONDITIONAL (live result for `wf_of_replay`, `WFClass` and acceptance for the classification); REFUTED (right congruence of the signature summary) | yes |
| 66 | Every step is idempotent and that is almost all the algebra there is | `TraceAlgebra.step_idem`, `TraceAlgebra.trace_absorbs`, `TraceAlgebra.comm_setLicense`, `TraceAlgebra.comm_setBudget`, `TraceAlgebra.comm_admitOcc`, `TraceAlgebra.rw_sound`, `TraceAlgebra.nf_unique`, `TraceAlgebra.nf_sound`, `TraceAlgebra.rewrite_not_complete` | FROZEN; CONDITIONAL (named insensitivity predicates for commutation); REFUTED (completeness of this rewrite system for universal replay equivalence) | yes |
| 67 | Descending a view through the observer quotient | `ObsDescent.obsQuotient_mk_eq_iff`, `ObsDescent.descend_exists_iff`, `ObsDescent.descend_unique`, `ObsDescent.descend_blocked_of_witness`, `ObsDescent.view_descends_pair_blocked`, `ObsDescent.descend_iff_factorsOn_all` | FROZEN; CONDITIONAL (class constancy for descent); REFUTED (fixed-domain agreement implying global class constancy) | yes |
| 68 | What an observer buys from an apartness and what it costs back | `ContactBridge.obsApart_irrefl`, `ContactBridge.obsApart_symm`, `ContactBridge.obsApart_cotrans`, `ContactBridge.apartObs`, `ContactBridge.apartObs_roundtrip`, `ContactBridge.indist_obsApart_iff`, `ContactBridge.obsApart_repr_iff`, `DiffAnchor.colObs_quotient_eq_iff_zeroP` | FROZEN; CONDITIONAL (decidable zero for complement cotransitivity, decidable apartness for its relation round trip); VERIFIED_FINITE | yes |
| 69 | The common kernel of a witnessed difference | `ContactKernel.kernel_endpoints_ne`, `ContactKernel.no_kernel_on_subsingleton`, `ContactKernel.kernel_from_obs_iff_pair`, `ContactKernel.toDiffObs`, `ContactKernel.kernel_not_observer`, `ContactKernel.vhom_unique_of_onto`, `ContactKernel.kernel_gateway_unique`, `ContactKernel.kernel_no_terminal` | FROZEN; CONDITIONAL (a nonzero pair from an observer, additional zero laws for an observer from a kernel, `DeltaOnto` and equal carrier maps for `vhom_unique_of_onto`); REFUTED (automatic observer laws and unrestricted terminality) | yes |
| 70 | Can a pair be chosen in a way every relabelling respects? | `PresentationNaturality.no_natural_section_of_fixed_point_free`, `PresentationNaturality.fixed_pair_of_natural_section`, `PresentationNaturality.no_natural_section_boolEq`, `PresentationNaturality.selection_is_possible_naturality_is_not`, `PresentationNaturality.card4_has_natural_section` | FROZEN; CONDITIONAL (declared presentation family and admissible ordered-pair transport); REFUTED (natural selection in the fixed-point-free example) | yes |
| 71 | When do two presentations preserve the same distinctions? | `PresentationRelativity.presentationIdentity_iff_fiberIdentity`, `PresentationRelativity.presentationIdentity_iff_residualEmpty`, `PresentationRelativity.forced_split_of_factorization_failure`, `PresentationRelativity.jointPresentation_strict_of_factorization_failure`, `ClosureSymmetry.closure_failure_iff_internal_symmetry_break`, `ResidualClosure.common_refinement_closes_current_obstruction` | FROZEN; CONDITIONAL (the supplied finite numerical domain, failed recovery and common-refinement hypotheses); VERIFIED_FINITE | yes |
| 72 | Round-trip coherence, quotient retention, and the fidelity closure | `PresentationDescent.faithful_descent_iff_round_trip_coherent`, `PresentationDescent.translation_gap_refuses_totalization`, `QuotientRetention.collapseMap_injective_iff_reverse_refinement`, `FidelityClosure.class_eq_iff_coherent_path`, `FidelityClosure.holonomy_residual_refuses_faithful_network_descent`, `NoOutsideFidelity.support_translation_never_round_trip_coherent`, `EndogenousFidelityGenerator.fidelity_is_least_equivalence_containing_admitted_steps` | FROZEN; CONDITIONAL (supplied translations and admitted coherent paths); REFUTED (support-only round trips and faithful network descent in the nontrivial-loop example) | yes |
| 73 | A side can be imposed, not chosen symmetrically, and composition without an operator | `Breaking.no_orbit_constant_equivariant_endomap`, `Breaking.selector_iff_common_fixed_point`, `Breaking.imposable_but_not_equivariant`, `Breaking.no_fixed_point_free_involution_on_Tri`, `Composing.composition_may_fail`, `Composing.composite_may_be_nonunique`, `Composing.selection_is_possible`, `Composing.skew_not_relAssoc` | FROZEN; CONDITIONAL (inhabited carrier for the selector obstruction); REFUTED (unconditional selector symmetry and unconditional relational composition laws) | yes |
| 74 | Renaming forms, transporting collapse, and canonical keys | `Derivation.renameForms_arity`, `Derivation.renameForms_gf`, `Derivation.collapsed_renameForms`, `Derivation.collapsed_renameDataForm`, `Derivation.Iso.symm`, `Derivation.Iso.collapsed_transport`, `Derivation.Iso.trans`, `Derivation.relabel_iso`, `Derivation.iso_of_relabel_eq`, `Derivation.Iso.of_components` | FROZEN; CONDITIONAL (bounded inverse form maps for transport; ordered requirements for `relabel_iso`, `iso_of_relabel_eq`, `Iso.of_components`); no completeness claim for Python canonical keys on arbitrary raw lists | yes |

The order follows the derivation. Units 27-73 follow the root import order
of `lean4/Derivation.lean` (Quot, Counting, CountTransport, Mention,
TransitionTransport, MinimalityF, RuleBridge, Rounds, Progress, Ext,
ObserverInventory, Refusal, RefusalFrontier, Generator, SeparationCapacity,
Pigeonhole, CapacityBound, LocalStrategy, G1Class, DiffInterface, Represented,
Completion, NoOutside,
Constitution, Initiality, Horizon, PrimitiveCore, PrimitiveCats, PrimitiveContact, PrimitivePassage, HigherStructure, Apartness, InterpreterBoundary, ControllerCategory, Attachment, RenamingStructure, LadderGeneral, BoundaryCancellation, Compression, StableContent, GraphGenesis, WeightProfile, TransitionAlphabet, TraceAlgebra, ObsDescent, ContactBridge, ContactKernel, PresentationNaturality, PresentationRelativity, ClosureSymmetry, ResidualClosure, PresentationDescent, QuotientRetention, FidelityClosure, NoOutsideFidelity, EndogenousFidelityGenerator, Breaking), paired with `DiffAnchor`/`DiffAnchorCompat` in Unit 68, `Composing` in Unit 73, and the parked form-renaming and isomorphism family (`FormRenaming`, `FormTransport`, `IsoCollapse`, `IsoCanon`, `IsoBridge`, and their `*Compat` shims) in Unit 74.

## Parts

| Part | Folder | Teaches |
|---|---|---|
| 1 | `textbook/units/` | the sealed derivation, from the mark forward (Units 00–74 in the contents table above) |
| 2 | `textbook/institutions/` | actors, institutions, information, knowledge, authorization, acquisition, uncollapse/recollapse, and the verdict-level interpreter boundary: the research trees `actor_institution` (#284), `two_theorems` (#277), `uncollapse` (#275), and `interpreter_verdict` (#278), outside the seal, with their own README and contents table (`Units 00–17`) |
