# Change log

Material changes only, newest last.

## 1. 2026-08-11 — Repository scaffold and plan

`CLAUDE.md` (execution plan, boundary, discipline, gates, stop conditions)
committed before substantive work.  Prompt inputs carried byte-identically
(SHA-256 recorded in `paper.md` section 1).

## 2. 2026-08-11 — Canonicalization defect found and fixed pre-publication

The first canonical-form implementation permuted color-class members *in
place* instead of assigning them to color-ordered positions, so the
canonical key was not isomorphism-invariant: the two unary marks (and the
paired binary variants) failed to merge, reporting 6 Challenge 3 classes
in reading L instead of 3.  Caught by the first smoke run against the hand
analysis; fixed in `code/derivation/iso.py` (`_class_perms`); regression
locked by `test_mark_variants_are_isomorphic` and the brute-force
agreement test.  No published artifact ever contained the wrong counts.

## 3. 2026-08-11 — First full artifact generation

Challenges 0-3 computed for both admission readings; four external-policy
trees and two closed-system baselines exported; byte-determinism verified
by dual runs.

## 4. 2026-08-11 — Caller correction (10 points) applied

1. Blind protocol tightened: the post-hoc comparison with known
   mathematics, originally required as a final section, is withheld
   entirely; a blindness sweep confirms no external-theory terminology
   anywhere outside the read-only seed prompt.
2. Every minimality claim now states candidate bounds, cost measure, and
   whether uniqueness is absolute or bounds-relative (paper section 7;
   ledger entries CL-3-*).
3. `CL-UNBOUNDED-WITH-SUPPLY` renamed to
   `CL-REACHES-REQUESTED-DEPTH-WITH-SUPPLY`: reaching a finite requested
   depth does not prove unboundedness; the unboundedness statement is
   downgraded to a conjecture supported by the progress theorem.
4. Termination evidence corrected: `any terminal node` replaced by
   per-branch reports (terminal / open / budget-cutoff / round-cutoff
   branches, plus an every-maximal-branch-terminates flag) in
   `CL-BRANCH-REPORTS` and `CL-ENDOGENOUS-TERMINATION`.  A related
   engine defect was found and fixed: a closed-system node reaching the
   fixpoint exactly at the round limit had been labeled as round-cut
   (`completed`) rather than terminal; terminal-ness is now checked
   before the round cutoff (`test_closed_system_terminal_at_round_
   boundary`).
5. Fresh-data supply reclassified as an explicitly declared external
   continuation policy (engine docstring, paper sections 3.10, 8.1).
6. `supply=False` runs retained and labeled as the closed-system
   baseline.
7. -9. New research obligation answered (paper section 9): the endogenous
   generator exists (least collapsed pair; token-blind; no fresh data; no
   new goal kind), is implemented deterministically
   (`next_endogenous_challenge`), preserves requirement satisfaction, and
   provably terminates at the all-pairs-separated fixpoint within
   n(n-1)/2 rounds (new Lean lemma `allPairs_length`; closed-system
   baselines terminate in 1 / 3 rounds with every maximal branch
   terminal).  Beyond the fixpoint no endogenous continuation exists: the
   native tower stops; further continuation requires the external policy.
10. Statement classification switched to the eight-way vocabulary
   (declared metatheory / definition / finite computation / theorem /
   bounded theorem / conjecture / counterexample / unresolved) throughout
   the paper and ledger.

Also in this pass: `cost1_insufficient` generalized in Lean to any
form-less, instance-less regime (now absolute over the item grammar and
instantiated for both readings); reading-F existence witness
`deltaU0F_valid` added; exported theorem count 42.

## 5. 2026-08-11 — Second caller correction (10 points) applied

1. `wfCtx` strengthened: well-formed contexts now require the slot count
   to equal the form's arity (`c.slots.length = r.forms.getD c.form 0`).
   Affected Lean proofs repaired (separation witnesses, `mark_progress`
   including a new `getD_append_lt` lemma, `separable_of_subrules`); the
   Python context enumeration already produced only arity-length slot
   tuples by construction.
2. Lean is now labeled a token-erased abstraction, never a mirror, and
   the abstraction is proved: `Derivation/Erasure.lean` adds a
   token-aware state with deduplicating admission and the simulation
   theorems `erase_step` / `erase_replay` (a duplicate admission erases
   to a bare supply, a proved no-op).  A first draft of the history-level
   statement was vacuous (`lhs = lhs`); it was caught and replaced by
   the genuine state-threaded statement before any claim cited it.
3. Claim scopes separated explicitly in paper and ledger: reading-L
   minimality Lean-proved; reading-F grammar-wide mu2 uniqueness is
   finite computation; Python class counts carry max_items=2 /
   max_arity=2; the arity-indexed `markK` family is its own theorem.
4. Every unboundedness claim removed (including the former conjecture):
   `mark_progress` is response existence for a supplied demand only;
   behavior beyond the exported depths is unresolved.
5. Claim ID renamed to
   `CL-REACHES-REQUESTED-DEPTH-WITH-EXTERNAL-SUPPLY`.
6. Fresh supply remains the declared external continuation policy;
   no-supply runs remain the closed-system baseline.
7. Termination is reported over all maximal branches (branch reports);
   no claim rests on the existence of one terminal node.
8. The counting laws (`strict_bounded_length`, `no_supply_round_bound`)
   are labeled conditional; the connection of their hypotheses to the
   transition system is recorded as computational and a Lean connection
   theorem as unresolved.
9. `separable_of_subrules` docstring and ledger weakened to exactly what
   is proved (witness transfer under a shrunken final rule set); the
   delta-level pruning corollary is recorded as computationally
   certified.
10. Axiom status stated exactly: no sorry, admit, or custom
   conclusion-producing axioms; standard `propext` and `Quot.sound`
   dependencies remain (44 per-theorem reports).

## 6. 2026-08-11 — Third caller correction (7 points) applied

1. Quotient-transition soundness repaired.  Raw least-pair challenge
   selection was not isomorphism-equivariant: on the regression regime
   (four data, one unary form, instances on data 2 and 3, collapsed
   pairs (0,1) and (2,3), renaming (2,3,0,1)) the canonical keys agree
   while the same-index least-pair selections produce non-isomorphic
   children (`test_least_pair_selection_is_not_equivariant`).  Replaced
   by one challenge branch per automorphism orbit of collapsed pairs,
   all non-isomorphic orbits retained (`automorphisms`, `pair_orbits`,
   `closure_challenge_orbits`); transition congruence under isomorphism
   is tested exhaustively over all renamings of the sample regimes.
   Every tree, count, role report, artifact, and dependent claim was
   regenerated: the numbers are unchanged and
   `expansions_with_multiple_orbits = 0` in every exported run — the
   defect was latent within the explored bounds.
2. Continuation rule reclassified: "endogenous generator" renamed to
   *declared pair-separation closure policy*; `CL-ENDOGENOUS-*` replaced
   by `CL-CLOSURE-*`; the paper now states that no object-language
   endogenous demand generator was derived and that under the declared
   policy the fixed finite datum set reaches an all-pairs-separated
   fixpoint; "native tower stops" replaced by "pair-separation closure
   terminates".
3. Lean/Python bridge repaired: instance, rule, and requirement
   admission in Lean now use deduplicating insertion (`insertNew`),
   matching the Python set semantics; the erasure simulation was
   re-proved over the new semantics, so repeated admission of every
   event kind agrees.  The bridge is stated as an abstraction with a
   proved simulation, not as an exact mirror.
4. `wfCtx` gained the hole requirement (`none ∈ c.slots`), making the
   Lean context space coincide with the Python enumeration; witnesses
   and transfers repaired.
5. Claim language corrected: "Least" removed from the paper title (and
   the new PR title); the result is stated as beginning from an opaque
   seed under declared external challenges; "admission never increases
   expressive power" weakened to "admission need not increase expressive
   power"; the remaining unboundedness sentence removed from the
   `Progress.lean` module comment; the counting laws remain labeled
   conditional.
6. Independent verification added: pinned dependencies
   (`requirements.txt`), GitHub Actions (`.github/workflows/verify.yml`)
   running pytest with independent 95% line and branch gates
   (`ci/check_coverage.py`), mypy strict, `lake build`, forbidden-token
   and axiom audits (`ci/check_lean_audit.py`,
   `ci/check_axiom_report.py`), prompt-hash verification
   (`ci/check_prompt_hashes.py`, pinning both the supplied and the
   repository-canonical bytes), and artifact regeneration with content
   comparison (`ci/compare_artifacts.py`).
7. Generated-artifact duplication reduced: trees now export as
   normalized DAG records (root history, per-node regime hashes, edge
   event-deltas, parent references — no per-node histories); committed
   summaries carry statistics and the SHA-256 of each full export; full
   exports live under `artifacts/full/*.json.gz`, reproducibly
   compressed, and `verify_full_export` replays every node from the DAG
   (the exported artifact footprint dropped from ~17 MB to ~320 KB).

## 7. 2026-08-12 — Fourth caller correction (4 points, PR #2 review) applied

1. Every DAG edge is now certified, not only one creation edge per node.
   Merge edges carry explicit datum/form bijections, computed at attach
   time (`find_iso`, built on `canonical_witness`) and re-verified before
   storage; `verify_full_export` replays every edge — creation edges must
   reproduce the exact stored child, merge edges must map the replayed
   result exactly onto the stored representative through their stored
   bijections (bijectivity checked, tampered events rejected rather than
   crashing).  Required regression added: one invalid merge edge is
   rejected even when every node retains a valid creation path
   (`test_verify_rejects_invalid_merge_edge_despite_valid_creation_
   paths`), plus corruption of merge events and deletion of the
   certificate.
2. `node_budget` renamed to `pre_expansion_node_guard` everywhere
   (engine parameter, tree metadata, bounds keys, CLI flags, statuses
   `frontier_budget` → `frontier_guard`, branch-report key
   `budget_cutoff_branches` → `guard_cutoff_branches`, paper and
   ledger), because the guard is checked before expansion and an export
   may slightly exceed the guard value: it is not a strict node cap and
   is no longer named like one.
3. Transition equivariance rescoped honestly: no general transport of
   candidates, costs, validity, minima, or children under regime
   isomorphism is claimed; those transports are recorded as unresolved.
   The surviving classification is finite adversarial evidence —
   exhaustive congruence over all renamings of the sample regimes
   including the adversarial regression, plus a verified isomorphism
   certificate on every exported merge edge.
4. The list-vs-set gap between Lean and Python closed by proof:
   `Derivation/Ext.lean` adds the membership-extensional relation
   (`SetEq`, `RegimeExt`) with transport theorems for derivability,
   context well-formedness, collapse, separability, item and delta
   application, and response validity.  The bridge claim now rests on
   erasure simulation plus membership extensionality — never on
   duplicate-admission idempotence alone.  Exported theorem count 51.

Artifacts, ledger, paper, and CI receipts regenerated; tree statistics
unchanged except the status rename.

## 8. 2026-08-12 — Paper suite frozen

`paper.md`, `paper_claim_ledger.md`, and this log written against the
frozen artifacts; final gate run recorded in `paper.md` section 12.

## 9. 2026-08-12 — Frontier Run 006 correction pass (PR #7 verdict)

One narrow correction pass on `paper/refusal_as_difference.md` and its
evidence, per verdict; the protocol class is unchanged and no research
search was reopened.

1. Terminal split by target: FREE_REFUSAL_BRIDGE_FAILS /
   UNIQUE_MINIMUM_WITNESSED_BRIDGE_IN_CLASS /
   MULTIPLE_MINIMUM_WEAKER_BRIDGES.  The artifact shows one minimum
   protocol (datum + relation rule) for the witnessed milestones under
   both cost orders; the ties and the order disagreement live at
   two-carrier and separable/oriented pair.  The earlier single-line
   MULTIPLE_MINIMUM_BRIDGES conflated these targets.
2. New Lean theorem `min_witnessed_route_closes` verifies the actual
   computed minimum witnessed route on a state type with no tag store
   and no result store (receipt as a literal coproduct).  `stepP` is
   relabeled a sufficient, non-minimum construction; its comment no
   longer claims a binary result algebra (it has no result store).
   Axiom reports: 135, within {propext, Quot.sound}.
3. Import channels scoped by target (constructors — result outcomes;
   tags/relations — carrier profiles; relations — witnessed relations);
   the target-independent three-channel reading is withdrawn.
4. `normal_form_check` strengthened to test exactly the claims made:
   added separable/oriented pair → tag-or-relation and result
   distinction → binary algebra checks (all empty in class); claims and
   checks now match one-for-one.
5. The implication matrix renamed to the nine-state-level-notion
   matrix; the twelve declared notions remain, with histories, states,
   event classes, and orientation reported separately at their own
   levels.
6. Proto-numeral headline scoped: the declared reflective protocol
   *realizes* a successor chain (horizon-free); refusal itself derives
   no numerals.  Initiality remains open (F4).

Tests 129 → 131; coverage 99.10% line / 97.29% branch; artifact
`refusal_frontier.json` regenerated deterministically.

## 10. 2026-08-12 — F5 run: the composite generator

New research leg answering F5 of `paper/refusal_as_difference.md`:
`paper/endogenous_generator.md`, `lean4/Derivation/Generator.lean`
(16 theorems), `code/derivation/generator.py`, `code/run_generator.py`,
`tests/test_generator.py`, `artifacts/generator.json`, CL-G-* ledger
entries, CI regeneration line.

Terminal, split by claim: ENDOGENOUS_GENERATION_PROVED /
ENDOGENOUS_REPAIR_FAILS_IN_DECLARED_CLASS /
GENERATION_REPAIR_EXCLUSION_IN_CLASS.  The composite of reflective
growth and pair-separation closure fires at every round from the third
on, horizon-free, with no per-round external act — the first such
generator exhibited in the development, without a minimality or
uniqueness claim.  Its obstruction set is
identified exactly (interior pairs, an iff).  Over the declared
five-strategy repair class within the 15-round computation, no branch
fires, repairs, and never
imports: presence marking is vacuous, per-pair marking is outgrown by
every finite marking (a fresh import per repair, forever), valued
marking kills generation at the price of identity-grade observation,
and depth-2 observation is outrun in the deep interior (Lean instances
at lengths 4 and 5; general depth-d open as G2).  The direct
transposition of interior points 1 and 2 is proved not to preserve the
successor relation; full rigidity and the quantified automorphism
claim are not established here.

Axiom-hygiene note recorded for the metatheory: `omega` on conjunction
or disjunction *goals* introduces `Classical.choice` in this
toolchain; all such uses were restructured (goal-splitting, explicit
trichotomy) and the build's 151 axiom reports remain within
{propext, Quot.sound}.

## 11. 2026-08-12 — Native primitive-difference interface

Externally imposed challenge (caller request): a self-contained,
adapter-independent theorem package —
`lean4/Derivation/DiffInterface.lean` (core-only imports, 35 exported
theorems), mirrored in `code/derivation/diff_interface.py` with
artifact `diff_interface.json`, documented in
`paper/difference_interface.md` with CL-DI-* ledger entries.

Pipeline delivered and proved: typed difference operation with
equivalence-before-quotient (the quotient consumes the Setoid built
from the equivalence proof, so the ordering is dependency-enforced);
retained / observer-zero / protected as independent predicates with
active obstruction their conjunction; factored bare reflection
(embedding + retraction, a point outside the old live image, declared
parent, live-scoped preservation, and an explicitly retained,
protected, observer-zero parent/new pair) certifying an active
obstruction; map-saturated closure over abstract demand predicates
under declared preserving maps (no inverse or composition assumed),
preserving old distinctions and strictly decreasing the concrete
declared measure.  Extension requests are represented as proposal data,
never applied.  Fuel termination follows from the generic measure-based
driver; the concrete two-element demand bound is a separate fact.  A
uniform pointwise successor-step family is proved; no trace object or
finite-prefix induction theorem is claimed.  Every Boolean view over
three protected points remains obstructed (pigeonhole; exhaustive over
all eight views); proposal data is available, but no decision theorem
forces its selection.  Countermodels for freshness, tagging, an edge, a
new hash, and repetition now each include an unprotected stage and an
explicit inactivity proof.

Further axiom-hygiene findings recorded: `List.eq_nil_iff_forall_not_mem`
depends on `Classical.choice` in this toolchain (replaced by a
cases-based proof); the build's 186 axiom reports remain within
{propext, Quot.sound}.

## 12. 2026-08-12 — Represented progress without an outside

Externally imposed challenge (caller assignment): can all load-bearing
causes of represented progress themselves be represented, with no
hidden evaluator, selector, or source outside the replay semantics?

New leg: `lean4/Derivation/Represented.lean` (native, core-only, 48
exported theorems), `code/derivation/represented.py`,
`code/run_represented.py`, `tests/test_represented.py`, artifact
`represented.json`, `paper/represented_progress.md`, CL-RP-* ledger
entries, CI regeneration line.

Terminal, split by claim: REPRESENTED_KERNEL_EXISTS /
HIDDEN_INPUT_CLASSES_REFUTED /
CERTIFICATION_BOUNDED_BY_PANEL_QUOTIENT.  One kernel carries every
load-bearing input in its state or history (evaluator, requirement,
scheduler, tie-break, fresh names, fuel, authorization, stopping
condition) and satisfies the eight target theorems: replay
determinism/composition; the support theorem (result-affecting data
occur in the represented support); complete tied successor families
with replay-equivalence invariance; repair soundness (discharge +
preservation); augmentation soundness (exact conservativity equation +
verified expressive increase); represented progress (repair family
non-empty or certified obstruction with accepted canonical
augmentation; budget and license isolated as the represented
load-bearing hypotheses; refusal only with a verified certificate);
closure (new violations only from represented require events);
productivity (one prefix-compatible unbounded run with carrier
`range (k+1)` derived through the acceptance-guarded kernel) separated
by proof from per-length witnessing (a represented Koenig failure).
Internal certification is priced exactly: equivalent to the panel's
joint separation, refuted as correspondence, non-monotone under panel
extension.  The eight required countermodels each consume exactly one
unrepresented input and are machine-checked; obstruction requires
exhaustive failure of the declared response menu by definition, and
the incomplete-search countermodel shows why.

The `admit` event constructor is spelled `admitTok` (forbidden-token
audit).  Test count 155 -> 175; the build's 234 axiom reports remain
within {propext, Quot.sound} with no new hygiene exceptions.

## 13. 2026-08-12 — Represented-progress correction pass (PR #10 verdict)

One focused correction pass; the research programme is unchanged.

1. Terminal scoped to a fixed kernel constitution: the event grammar,
   sep/sat laws, response menu, acceptance predicates, and history
   producer are fixed metatheory; the theorems cover *runtime* inputs
   relative to that fixed `step` semantics, and the constitution does
   not derive itself.
2. Python/Lean carrier mismatch closed: every negative token, index,
   view member, requirement endpoint, mark point, budget, and note is
   rejected in the mirror, matching Lean's `Nat`; negative-domain and
   malformed-event tests added.
3. The claim that bounded runs terminalize in refusal is withdrawn:
   refusal records verified same-level exhaustion and is
   non-absorbing; run termination belongs to the metatheoretic history
   producer.
4. "Augmentation conservativity" renamed: `aug_preserves_satisfied`
   preserves satisfied positive requirements; old non-separation
   judgments are not preserved — changing them is the licensed content
   of augmentation.
5. RP8 scoped to an explicitly supplied prefix-compatible event
   stream (never called endogenous); per-event acceptance and
   per-stage quiescence verified exhaustively to the 15-round bound.
6. No-hidden-choice scoped to `repairFamily`; the structural branch's
   canonical augmentation `[i]` takes its orientation from the
   ordered, recorded requirement — a represented datum and a stated
   scoping, with no retained augmentation family claimed.
7. The evaluator panel classified as an explicit certification
   argument, not replay-integrated.
8. Countermodels split: hidden runtime inputs (scheduler, fresh-name
   source, hidden evaluator, order-sensitive tie-break) versus
   neighboring semantic/inference failures (incomplete search,
   destructive rewrite, repetition-as-progress, König witnesses).
9. Support wording changed to operational-support factorization, not
   full result causation.

Tests 175 -> 177; artifact, ledger, paper, and CI receipts
regenerated; 234 axiom reports remain within {propext, Quot.sound}.

## 14. 2026-08-12 — Ultra closure run

One autonomous run composing the sealed estate (PRs #1-#10) into the
final native spine: `paper/native_derivation_completion.md` (verdict,
both rules, event source, constitution, autonomy, initiality,
adversarial audit), `paper/native_derivation_map.md` (one row per
bridge), four Lean modules (Completion, NoOutside, Constitution,
Initiality; 57 new exported theorems, 291 total, all within {propext,
Quot.sound}), the completion Python mirror with source-derived
inventory, and five deterministic artifacts including the receipt.

Terminals: RELATIVE_REPLAY_CLOSURE_ONLY;
EVENT_SOURCE_INTERNALIZED_RELATIVE_TO_FIXED_INTERPRETER;
KERNEL_CONSTITUTION_INTERNALIZED_RELATIVE_TO_FIXED_INTERPRETER;
KERNEL_CONSTITUTION_REMAINS_META (the single OPEN bridge);
INITIAL_KERNEL_PROVED (declared class);
ABSOLUTE_NO_OUTSIDE_UNFORMULABLE.  FULL_NATIVE_COMPOSITION not
claimed.  Highlights: the driver reproduces the previously supplied
tower stream from represented state (the supplied-vs-endogenous
laundering closed in the strong direction); the extension family
retains both orientations (strengthening the PR #10 scoping); refusal
proved object-inert; Rule 1 reduced to preservation + declared
fidelity; Rule 2's dichotomy proved operationally and its absolute
form recorded as unformulable; the kernel's own description executes
to the sealed step under the fixed family interpreter; the kernel is
the unique compliant and initial member of its declared 64-member
class.  No sealed theorem or claim was altered.

## 15. 2026-08-12 — Ultra-closure correction pass (PR #11 verdict)

One focused correction pass; no new research phase.

1. Artifacts regenerated against the final paper and ledger state,
   with the correction-pass edits applied first.
2. Generation scoped honestly: `towerGen` now invokes the next-family
   interpreter on the replayed state; the result is described
   everywhere as state-derived, prefix-compatible generation under
   metatheoretic iteration and a fixed interpreter; the
   internal-trigger claim (ladder level 4) is withdrawn as NOT
   attained.
3. Freshness proved on the tower invariant
   (`freshName_fresh_on_tower`) and refuted in general
   (`freshName_not_fresh_generally`).
4. Terminal renamed: INITIAL_KERNEL_PROVED ->
   UNIQUE_PROBE_COMPLIANT_DESCRIPTOR_IN_DECLARED_TOGGLE_CLASS; a
   six-probe singleton and one split retract do not prove categorical
   initiality, and none is claimed.
5. The common obstruction now has independent retention, protection,
   and zero conditions (`obstC_conditions_independent`); the kernel
   transport's identification of retention and protection is stated.
6. S2 symmetry scoped: relation store swap-invariant; whole state not
   (`s2_state_not_swap_invariant`).
7. `rule1_trichotomy` renamed `rule1_repair_or_extension`: the action
   alternative is binary; refusal is a parallel non-absorbing record;
   budget/license execution remains a separate gate.
8. Nat agreement enforced for every constitution descriptor: the
   mirror's `interp_step` rejects negative tokens, endpoints, points,
   and view members unconditionally, so disabled guards can never
   license states unavailable in Lean.
9. Graph scope stated: one OPEN edge in the declared graph; no claim
   that the graph exhausts every possible bridge.

Axiom reports 291 -> 295, all within {propext, Quot.sound}.

## PR #12 — Primitive Difference contact and passage, Phase I corrections

Pre-contact correction pass over PR #11's strongest labels
(full audit: `paper/pr11_correction_ledger.md`).  Ten claims audited;
two defects found and repaired:

1. **C10 (cross-language exactness), refuted and repaired.**  Old
   claim (42a33d9 item 8): "disabled guards can never license states
   unavailable in Lean."  Countermodel: descriptor `(T,T,F,F,T,T)`,
   world `{data=(10,20), views=((0,),), reqs=((0,1),), budget=0}`,
   event `mark (1,) 0` — a Lean no-op but a Python state change to
   budget `-1` (unsaturated subtraction under a disabled budget
   gate).  Replacement: the mirror's two decrement sites now saturate
   (`max(0, budget - 1)`); Lean pins the exact shared semantics
   (`Horizon.interp_budget_bound`, `Horizon.budget_saturation_noop`,
   `Horizon.mark_saturation_all_descs`); the Python suite asserts the
   identical facts over all 64 descriptors on the declared basis.
   Affected claims: 42a33d9 item 8 (recorded here as refuted; left in
   place as history), `interp_step` docstring.

2. **C6 (horizon lawfulness), closed upward.**  Old state: the only
   Lean lawfulness fact for the generated run was the stage-3
   quiescence instance, while CL-NC-AUTONOMY spoke of "lawfulness
   across extension" citing a theorem with no lawfulness conjunct.
   Replacement: `Derivation/Horizon.lean` proves the complete record
   characterization of the generated world at every stage
   (`worldAt_spec`, by induction) and derives quiescence,
   well-formedness, and per-event acceptance at every horizon
   (`worldAt_quiescent`, `worldAt_wf`, `block_all_accepted`,
   `genesis_accepted`), lifted to the driver (`gen_quiescent`,
   `gen_wf`).  Affected claims: CL-NC-AUTONOMY (rewritten, old defect
   recorded inside the entry).

Verdicts C1, C2: hold as labeled.  C3, C4, C5, C7, C8, C9: already
corrected by 42a33d9; re-verified against current Lean statements.


## PR #12 — Phases II–IX: characterization, contact, passage, growth

1. Native characterization (blind, committed before any contact
   reading): nine candidate readings, 72-cell implication matrix (17
   proved implications, 51 compiled minimum countermodels, 4 OPEN
   located cells with exact scope), genuine categories with proved
   laws, `d2_initial` as a true universal property, the orientation
   fork retained, and the observer branching theorem
   (`no_terminal_pres`).
2. Contact: the declared package is absent; terminal
   CONTACT_INPUT_ABSENT recorded with a runtime check; the native
   kernel interface committed as the fixed target of any future
   collision.  No contents invented.
3. Apartness refinement (caller directive, mid-run): positive
   apartness with indistinguishability proved an equivalence;
   minimal insufficiency countermodels at carriers 1, 2, 3; the
   orientation/apartness separation; the exact operation-preservation
   characterization (identity only; identity and swap; constants
   neither; closure iff generators).
4. Passage: the full arrow chain with per-arrow statuses; the
   four-condition active obstruction (observation declared vs
   pre-observational, a refinement over the sealed three-condition
   reading, with agreement and divergence proved); P1–P8 including
   the two-rule theorem — at an active obstruction the response
   universe never runs dry: same-level repair or certified
   exhaustion plus a provably nonempty extension family.
5. Growth: the first graph grows by iterated
   obstruction-and-response, characterized at every horizon; the
   0-, 1-, 2-, 3-simplices grow under horn-guarded declared cell
   admission with replayable creation records; named invariants
   (ladder invariant, connectivity residue, occurrence alternation
   number, cut census, orientation residue, budget trichotomy);
   d²=0 under the declared calculus with the convention proved
   non-forced.  Higher structure: admitted, never forced.
6. New claims CL-PD2-* in the ledger; papers
   `primitive_difference_contact.md`,
   `primitive_difference_passage.md`, `primitive_difference_map.md`.


## PR #12 — Phases VII–VIII and completion

1. Controller category (Phase VII): the six-toggle proxy replaced by
   a genuine 1024-member variable-event-grammar class with a
   simulation category (laws proved).  Initiality REFUTED by the
   constant-simulation countermodel, surviving restriction to the
   live subcategory; NONUNIQUE_CONTROLLER_FAMILY proved (live census
   128; refusal is response-invisible); strict refinement excludes
   constants but global uniqueness still fails (invariant-twist
   countermodel); uniqueness holds exactly on the genesis-reachable
   orbit.  Agreement is a replay theorem, not a categorical one.
2. Interpreter boundary (Phase VIII): tower persistence proved by
   finite diagonalization (every finite closure has a new top);
   universal code/evaluator exact for the declared family; the
   typed-refusal top was initially described as closing by partiality
   what totality cannot (this necessity claim is withdrawn below);
   verified self-description alongside finite non-exhaustion; and the
   boundary formalized as a Primitive Difference (candidates A and F
   satisfied, collapse obstructed, difference behaviorally grounded).
   Absolute no-outside not claimed.
3. Completion: receipt with ten terminals, five open obligations,
   the twenty-attack adversarial record, and the two
   withdrawn-or-repaired claims; papers
   `primitive_controller_universality.md`,
   `primitive_interpreter_boundary.md`; ledger claims
   CL-PD2-CONTROLLER, CL-PD2-INTERPRETER, CL-PD2-RECEIPT.

## PR #12 review pass (request-changes verdict applied)

Fourteen-point correction pass; no candidate search reopened, no
speculative idea deleted.  Old statements, countermodels/reasons, and
replacements:

1. Hosted CI red on artifact comparison: the receipt hashed
   CRLF-checkout bytes of `requirements.txt`; replaced by a
   line-ending-normalized hash (raw hashes retained for the
   `-text`-pinned `prompt/**` and `artifacts/**` files).
2. `prompt_pr12.md` claimed "verbatim" while summarizing the ultra
   prompt; the exact bytes are now committed as
   `prompt/ultra_prompt_pr12.md` and the receipt binds both; the
   0,1,3,3 → 0,1,2,3 reading is labeled ASSUMED_TYPO_CORRECTION.
3. Composition gap (blocking): the passage had no pre-retention
   witness store — `admitWit` created witness and retention
   together, so PRIMITIVE_DIFFERENCE_PASSAGE_COMPOSED overreached.
   Repaired by construction: separate `asserted` store and
   `assertWit` event; retention now requires assertion
   (`retention_requires_assertion`); `assertion_not_retained` is the
   pre-retention witness state; transport from candidate A proved
   (`assert_transport` via the `asserted_offdiag` invariant;
   `kernel_enters_preretained`; `retained_sub_asserted`).
4. `d2_initial` scoped: `PtdRel` has no irreflexivity, so the
   initiality characterizes the bare-witness reading W (free pointed
   object on one witnessed arrow); A-initiality is the restriction
   corollary; A's justification is `imp_a_d` vs `nimp_w_d` — the
   two arguments are no longer merged anywhere.
5. Native terminal rescoped: "within the declared nine-candidate
   signature, A is the weakest studied positive-witness candidate
   forcing endpoint inequality".
6. Interpreter terminals replaced: INTERPRETER_TOWER_PERSISTS →
   FINITE_CODE_FAMILY_NOT_EXTENSIONALLY_COMPLETE (the diagonal
   changes only the inert notes field; nothing about
   self-interpretation follows); INTERPRETER_BOUNDARY_IS_PRIMITIVE_
   DIFFERENCE → DECLARED_BOUNDARY_MODEL_SATISFIES_A_AND_F (the
   boundary model's relations are inserted by definition; no theorem
   links the uncoded occurrence to the missed function).  The
   stronger identification is retained as a frontier conjecture with
   its missing denotational/operational-grounding theorem stated.
7. `openTerminalPres2` was not open: closed constructively by
   `no_terminal_pres2` (free-point presentation gives every target
   two distinct commuting maps); positive fragment stays scoped to
   surjective presentations.  The earlier selection-principle
   frontier conjecture is superseded.
8. Graph provenance stated exactly: the driver SUPPLIES occurrences,
   assertions, retention, protection; the obstruction creates the
   observation column.  Graph genesis by obstruction is recorded as
   a frontier conjecture for a later experiment.
9. `horn2`/`horn3` renamed `shell2`/`shell3` (complete unfilled
   boundaries, not simplicial horns); `horn_guard_load_bearing` →
   `shell_guard_load_bearing`.
10. Higher-structure scoping: ladder proved only at dimensions 2–3
    (general recurrence a conjecture); `altNum` relabeled a
    statistic; path/no-cycle attributed to `graphAt_spec`, not
    V−E=1; D2-to-walking-arrow labeled a free completion.
11. Two-rule scoped grammar-relatively (the declared
    singleton-column universe supplies the separator; `setBudget 1`
    is declared self-funding); extension "loses nothing" replaced by
    the exact preservation statement; arrow count fixed at thirteen.
12. "51 minimum countermodels" → "51 finite countermodels; minimum
    carrier proved where cited".
13. Contact scope: this PR is the native characterization and
    passage; the external collision is deferred to a future PR with
    exact manifest and source hashes.
14. All artifacts, papers, ledger entries, and the receipt
    regenerated under the corrected statements.

## PR #12 next-goals pass (caller directive)

1. `d2_map_injective`: the unique map out of the two-element kernel
   is injective into every irreflexive pointed witnessed
   presentation; the hypothesis is not removable
   (`d2_map_not_injective_without_irrefl`).
2. One-edge attachment defined (fresh walking edge glued along a
   represented parent); every attachment policy is lawful at every
   stage, produces a tree, and preserves V−E=1 (policy-uniform
   theorems).
3. Path and star policies exhibited as non-isomorphic countermodels
   to forced global shape (decided over all carrier bijections at
   four occurrences).
4. Up defined as the complete family of legal extensions (one block
   per represented parent, never a selection); proved
   presentation-invariant; orbit-valued choices demonstrated where
   symmetry remains (star leaves one orbit; the oriented path rigid
   — undirected flip refused by the oriented stores).
5. The simplex ladder generalized to arbitrary finite dimension.
   *(Superseded by the audit repair below: `ladder_general` was
   renamed and NARROWED to `uniform_guarded_filler`, and it upgrades
   the review-pass conjecture only in that narrowed sense - guarded
   admission plus strict extension, not a dimension-general two-rule
   or homology claim.)*  Dimension-4 demonstration replayed in Lean,
   dimension 5 in Python; at this stage the general composite boundary
   vanishing remained open (superseded by Goal 4 below).

## PR #12 final repair pass (caller directive, 2026-08-13)

1. Receipt hashing made deterministic under explicit CRLF-to-LF
   canonicalization; for the current tracked inputs each result equals
   the Git blob hash.  The originally supplied CRLF
   rendering of the seed prompt is recorded as provenance; the
   blob/checkout distinction and content-mutation detection are
   tested.
2. Attachment policies are never clamped: `LawfulPolicy` carries
   the representedness proof; illegal parents meet the typed
   refusal `AttachOutcome.refusedParent`; the retired clamp is the
   recorded countermodel (`clamp_rewrote_input`).
3. Occurrence identity resolved: tokens (admission order) versus
   positions (relational identities); canonical fresh token proved
   fresh on every carrier; `length_not_fresh_countermodel` on the
   non-initial carrier `[1, 2]`; on canonical tree states tokens
   and positions provably coincide (`attachBlock_is_upBlock`).
4. Completeness made registry-relative and an iff
   (`up_iff_legal`); every Up block executes to a strict legal
   extension (`up_exec_eq`, `up_executes`).
5. Length equality replaced by a genuine positional renaming
   action with transport and replay commutation (`act_up_comm`);
   the old statement survives only as identical-carrier grammar
   uniformity; countermodels: equal size with equal family but no
   relating renaming; two legal equal-cost non-isomorphic
   extensions.
6. Generalized cells made well-formed: strict ascent in the shell
   guard; the legacy guard's `[0, 0]` pseudo-cell recorded as the
   required countermodel; well-formedness proved a replayed
   invariant (`wf_nreplay`).
7. `ladder_general` renamed and NARROWED to
   `uniform_guarded_filler`: a theorem about guarded admission and
   strict extension, not homology.
8. CL-PD2-LADDER and CL-PD2-LADDER-GENERAL reconciled in the
   ledger; at this stage the general composite vanishing remained OPEN
   (superseded by Goal 4 below).
9. Part II delivered: target-relative presentation compression
   (`Compression`, 22 theorems, axiom-clean) — factorization iff
   fiber-constancy with image-scoped uniqueness; coarsest-adequate
   quotient with exact universal property; witnessed descent
   failures; enlargement refinement with exact split
   characterization; absolute adequacy = injectivity; replay and
   digests non-evidential without a new separator; refinement
   non-unique with retained ties; strict chains bounded by the
   domain.
10. One axiom regression caught by the report and repaired:
    `omega` on a conjunction goal proves it classically; the
    conjunction is now split first, restoring
    propext/Quot.sound-only across all 707 reports.

11. Caller finals (stable content).  *(Overclaimed; corrected by
    the audit repair section below.)*  What was actually proved is
    the SUFFICIENCY direction and the quiescence iff.

## Audit repair gate (caller directive, 2026-08-13)

Four repairs required before the next derivation goal.

**A. "Stable content is exactly protected separation" was an
overclaim; withdrawn and replaced.**  The actual trace-stability
predicate is now DEFINED (`TraceStableSep`: separated after every
replay; `RestrictedStableSep`: after every replay in a syntactically
restricted fragment omitting occurrence admission, budget setting,
and license setting).  This makes no ownership claim; generated blocks
may contain `setBudget`.  Only SUFFICIENCY is proved
(`protSep_trace_stable`).  The CONVERSE IS FALSE, with the two
countermodels the audit demanded: an ABSORBED (halted) state, where
`replay_halted` makes every trace inert so an unprotected separation
is trace stable; and a LIVE but RESOURCE-BLOCKED state, where
`restricted_replay_inert_unfunded` shows no event in the stated
restricted fragment can change an unfunded observation, so an
unprotected separation is restricted-stable.  Instability is proved
to be witness-borne
(`separation_breakable`), and the residual gap - whether trace
stability implies protection on the live funded class - is recorded
as an unproved Prop (`openExactStabilityCharacterization`), never as
a theorem.  Ledger, receipt, module docstring, Python mirror, and
tests were all weakened together; `stableSep` was renamed `protSep`
because it names protected separation, not stability.

**B. Stale open obligation removed.**  `openTerminalPres2` was
closed constructively by `no_terminal_pres2` in the PR #11
correction pass but was still listed among the receipt's open
obligations.  It is removed and the artifact regenerated; the
receipt now carries four open obligations, and the test pins both
the count and the absence of the retired entry.

**C. Synthesis paper reconciled with the narrowed result.**  The
synthesis paper still described GENERAL_DIMENSIONAL_LADDER as an
open frontier conjecture about dimension-general recurrence.  It now
states the reconciliation explicitly: what is proved at every
dimension is the UNIFORM GUARDED FILLER
(`LadderGeneral.uniform_guarded_filler`) - guarded admission plus
strict extension in the standalone generalized calculus - which is
neither a homology claim nor a dimension-general transport of the
`ladder_dim2/dim3` two-rule reading.

**D. `i5_difference_grounded` renamed and narrowed.**  Its statement
was literally `family_missed`: it mentions neither the boundary pair
nor the uncoded occurrence, and connects neither to the missed
function.  It is renamed `i5_family_not_extensionally_complete` and
its docstring now says exactly what it does and does not carry.
`arbitrary_uncoded_assignment` further proves that a freely chosen
meaning for the uncoded occurrence is vacuous.  The denotational bridge
is therefore retained only as the OPEN obligation label
`openDenotationalBridge`, not as a trivially inhabited proposition.

## PR #13 carrier correction (adversarial repair, 2026-08-13)

1. Withdrawn: `tower_persists` does not force partiality, rule out a
   total evaluator, or prove self-application impossible.  I3 now
   records only one optional typed-refusal construction and its two
   definitional equations.
2. Repaired the denotational frontier: the former existential carrier
   was freely inhabitable.  `arbitrary_uncoded_assignment` proves that
   defect directly; `openDenotationalBridge` is now an obligation label
   requiring independent lawful semantics and an accessible behavioral
   consequence.
3. Removed the false event-ownership label from stability.  The second
   countermodel is explicitly restricted to a syntactic trace fragment;
   it is not a reachable-state necessity result and not a countermodel
   to full trace stability.
4. Narrowed reproducibility wording to deterministic generation under
   the declared line-ending canonicalization and fixed inputs.  Equality
   with Git blobs is verified for the current tracked inputs, not made
   true by definition for arbitrary files.

## Goal 1 - the renaming structure around Up (2026-08-13)

`Attachment` transported a single renaming; a transported arrow is
neither an action nor functoriality.  This pass supplies the missing
structure and proves its laws BEFORE using the vocabulary.

1. Identity, inverse and composition defined on `Renaming n`, with
   the group laws proved via a componentwise extensionality
   principle.
2. `act` proved to be an action: identity unconditionally,
   composition on the scope `n <= occ.length` (weakened from
   equality precisely so the extended state is covered), inversion
   as a consequence.
3. Block and family transport proved to respect identity and
   composition.
4. Coherence proved: replay of an `Up` block commutes with a
   composed renaming, and the composite and two-step routes agree.
5. Orbit closure proved with no selected representative; the family
   has exactly one block per represented parent.
6. Three countermodels recorded: an arbitrary non-bijective map (no
   left inverse; pushforward is not even a legal store), equal
   carrier size, and equal cost.  They do not instantiate the proved
   renaming/equivariance structure; no universal claim is made against
   other monoid actions by non-bijective maps.
7. Only then, in `equivariance_summary`, is `Up` described as
   equivariant, with the exact scope stated in the same theorem.

## Goal 5 - the true graph-genesis boundary (2026-08-13)

First the negative theorems about the current calculus, then one
explicit sufficient proposal schema that would change it, then the
verdict.

1. `refineCol` and `addCol` change observation structure only: seven
   other state fields are proved unchanged.
2. The internal response family ranges over columns on existing
   occurrences, in exactly two block shapes, with no third.
3. Along every internal trace the four graph stores are fixed, so the
   family cannot create occurrences, asserted, retained or protected
   pairs.
4. Corollary: current graph growth is supplied by the external driver
   or the `Up` grammar, never generated by `nextFamilyP`.
5. One explicit sufficient represented proposal schema is delivered as
   `ProposalRecord`: a NAMED complete-family member with its membership
   proof, embedding and retraction, fresh-token evidence,
   preservation obligations, the new pair with provenance, and a
   declared cost - with no license, execution or activation field.
   The named branch is not certified canonical or unique, and no
   minimality theorem is claimed for the schema.
   It transports under renaming and retains equal-cost
   non-isomorphic branches.
6. Verdict: `nextFamilyP` does not request the lift at an obstruction.  Every
   obstruction meeting the kernel's hypotheses is resolved inside the
   existing carrier, and no state admits an internal family member
   that grows the carrier.  The growth demand is not entailed by this
   represented response semantics and is separately declared.  The
   receipt's
   GRAPH_GENESIS_BY_OBSTRUCTION conjecture is settled negatively for
   this calculus; whether some OTHER declared family could request
   the lift stays OPEN.

## Goal 4 - general boundary cancellation (2026-08-13)

The dimension-2-to-5 computation is replaced by a general theorem,
and the standing conjecture GENERAL_BOUNDARY_COMPOSITE_VANISHING is
closed.

1. `d2_zero_unrestricted`: the coefficientwise composite boundary
   vanishes at every face of every finite cell.  The proof pairs the
   two orders for each unordered pair of deleted positions and cancels
   their signs; it is not a computation.
2. `d2_zero_general` records the declared ascending hypotheses and
   discharges them from the stronger theorem.
3. A premise of the task was false and is recorded as false: strict
   ascent is NOT load-bearing for the vanishing.  It IS load-bearing
   for distinctness of the codimension-two faces, which is what the
   ill-formed countermodel now exhibits.
4. Connected to replayed cells via `LadderGeneral.wf_nreplay`;
   renaming independence proved for strictly monotone renamings, with
   the non-monotone case stated exactly.
5. The signless countermodel keeps the orientation convention
   declared: without the signs the composite is nonzero, and nothing
   claims the filler rule forced the coefficients.
6. `LadderGeneral`'s docstring, the attachment/ladder mirror's
   `general_d2_zero` field, and the receipt conjecture list are all
   downgraded to corollaries or marked settled.

## Contact response correction: finite weights, no Hilbert climb
(2026-08-13)

The PR 17 contact surface was repaired after adversarial review.

1. Restricted profile equivalence and scaling to positive totals; zero scale
   now has an explicit boundary theorem instead of being called a positive-ray
   action.
2. Added the duplicate-free carrier policy. Raw list sums retain their honest
   multiplicity semantics.
3. Renamed lift-facing theorems as presentation theorems and fenced them as
   finite factorization identities.
4. Replaced the invalid `eB` non-presentation with two valid integer-square
   presentations differing by sign, scoped to one declared mixing read-out.
5. Reclassified the three alleged climb imports: one is trivially inhabited,
   one is proved by list algebra, and the proposed uniqueness schema is false
   by the zero read-out.
6. Rewrote the paper, ledger, receipt, artifact, and tests to state the actual
   ceiling: finite `Nat`/`Int` profile algebra and a sign-shadow fixture, with
   no Hilbert space, dynamics, probability law, or representation climb.

## Goals 2 and 3 - the one-step codebook and the trace algebra
(2026-08-13)

1. Repaired after adversarial review: 13 is the image size of a
   declared one-step signature (12 after guard erasure), not a native
   or presentation-invariant alphabet.  The coverage theorem proves
   every accepted well-formed step receives exactly one code; it does
   not derive the projection itself.
2. Two profile components were excluded from the class signature
   because they are provably not transition invariants; what they do
   carry invariantly was recovered as separate theorems.
3. A merge is reported as a result: refinement and extension have
   literally identical effect profiles on every well-formed state and
   differ only in acceptance domain.
4. Two common-suffix countermodels now prove the code is not a right
   congruence: equal occurrence-admission codes and equal budget-write
   codes can both be separated by a following event.  Raw events and
   states remain mandatory for replay.  No quotient, renaming
   invariance, DDA correspondence, or presentation-independent count
   is claimed.
5. A SECOND PREMISE OF MINE WAS FALSE.  I required a proof that
   occurrence supply, budget setting and license setting are never
   generated by the internal response family.  That holds for supply,
   license and the terminal, and FAILS for budget: `nextFamilyP`
   prefixes every extension block with `setBudget 1`.  The refutation
   is recorded, the repaired statement proved, and the scope note in
   `StableContent` corrected to say that its environment partition is
   a declared fragment, not a claim about the response family.
6. `Origin` is now explicitly documented as a constructor policy
   label, not issuer or causal provenance.  The internal family emits
   an event classified as environment, so the label cannot authorize
   an ownership conclusion.
7. The trace algebra derives its laws rather than assuming them, and
   one is stronger than expected: idempotence is universal, holding
   for every event at every state. Three sufficient frame families are
   proved; necessity and exhaustiveness are not. "Disjoint support
   implies commutes" is false because guards read fields their step
   never writes, with five non-commutation countermodels.
8. The two-rule rewrite system is sound, terminating and confluent, but
   not complete for universal replay equivalence: two universally
   replay-equivalent lists receive different `nf` values. This refutes
   completeness of this normalizer, not the possible existence of every
   richer universal or start-scoped canonicalizer.

## Contact collision executed - the arriving development processed
(2026-08-13)

The declared contact input, absent through every prior phase, arrived
and was executed against the interface those phases had already
committed.  Recorded facts of the run: base `a5caee2`; sealed
blind-native-base `ccd3a53`; one external Lean file bound by
`contact/omega_primdiff/CONTACT_MANIFEST.json` (manifest sha256
`3b65253d8338b5f0283a29a194fe673d0200ca091284ab92ef315246e328065f`,
file sha256
`d9cdb350a53c513e3e211e72f17262be6ba85d7da6159f910388c7137e814a89`);
no prose stage (PROSE_INPUT_ABSENT); the file was read under the
committed statements-only discipline, never copied into the
repository, and its vocabulary is quoted nowhere outside
`contact/analysis/`.  Status moves CONTACT_INPUT_ABSENT ->
**CONTACT_PROCESSED_LEAN_ONLY**, with the former preserved as
history, not deleted (`PrimitiveContact.contactStatusHistory`,
`contact_status_count`).

1. **Three new Lean modules** (2015 lines in the working tree — 539
   `ObsDescent.lean` + 710 `ContactBridge.lean` + 766
   `ContactKernel.lean`; 1942 at the spine commit `ebb1e0b`, the
   difference being the uncommitted `toDiffObs` and
   `collapse_collision` additions; every `#print axioms` report
   within {propext, Quot.sound}; `artifacts/lean_axioms.txt` grows
   from 1037 to 1149 reports).
   `lean4/Derivation/ObsDescent.lean` reconstructs the arriving
   quotient-descent layer in native vocabulary over the sealed
   `DiffInterface.DiffObs` / `ObsQuotient`: exactness
   (`obsQuotient_exact`, `obsQuotient_mk_eq_iff`,
   `obsQuotient_mk_surjective`), unary and binary descent with
   existence-iff-compatibility, global uniqueness and witness
   blocking (`descend_*`, `deltaDescend_*`), pairing and the flagship
   obstruction shape (`classConstant_pair_iff`,
   `pair_descend_exists_iff`, `view_descends_pair_blocked`), the
   mod-setoid layer collapsed to the equality layer
   (`classConstant_comp_mk_iff`, `descendMod_exists_iff`,
   `deltaDescendMod_exists_iff`, `coarsenMap`, `pairSetoid`), the
   all-zero countermodel family (`collapseAllObs_*`), and the
   integer tail as one instance plus five one-line lemmas
   (`intDiffObs`, `int_sub_ne_zero_iff`, `int_sub_ne_zero_of_gt`,
   `int_shift_cancel`, `int_two_mul_eq_zero_iff`,
   `int_add_sub_cancel`).
   `lean4/Derivation/ContactBridge.lean` builds the complement bridge
   (`obsApart` and its laws, `obsSetting` and the candidate cells
   `obsSetting_w/a/bs/d/e` with `obsSetting_bc/bl` conditional on
   pointwise decidability), the apartness meet and its round trips
   (`apartObs`, `apartObs_roundtrip`, `isApart_repr`,
   `obsApart_isApart`, `indist_obsApart_iff`), the representability
   characterization (`obsApart_repr_iff`) with four countermodels
   (`unit_total_not_repr`, `d2_not_obs_complement`,
   `triSym_not_obs_complement`, `d_not_witnessed_repr`) and the
   minimality positive (`bool_bs_repr`), the exact prices for the
   dropped hypotheses (`cotrans_schema_iff_wlem`,
   `stability_schema_iff_dne`, `located_schema_implies_wlem`, plus
   two OPEN records), the placement theorems
   (`declared_zero_as_view`, `observation_stage_realizes_observer`,
   `kernelStage`, `kernel_stage_no_obstruction`), and the bridge to
   the native collapse obstruction
   (`pair_blocked_is_collapse_collision`).
   `lean4/Derivation/ContactKernel.lean` constructs the common
   replacement kernel `WitnessedDiff` with both realizations
   (`ofSetting`, `ofSetting_exact`, `ofDiffObs`), the sealed-interface
   meeting (`toNativeKernel`), the inherited gateway
   (`kernel_gateway_unique`, `kernel_gateway_injective`), the
   non-collector (`kernel_no_terminal`,
   `kernel_no_terminal_collector`), value-grade rigidity
   (`value_presentation_fork`, `vhom_not_unique`,
   `vhom_unique_of_onto`), passage entry
   (`kernel_licenses_entry`, `entry_pre_observation`,
   `passage_gateway_unique`), and the 37-cell matrix (`contactCells`,
   `contactCells_length`).
2. **`lean4/Derivation/PrimitiveContact.lean` was extended, not
   edited.**  The sealed pre-contact declarations (`contactStatus`,
   `NativeKernel`, `nativeKernelWitness`, `native_kernel_initial`) are
   unchanged; a dated section adds the status history, the current
   status and primary verdict as declared strings, the length check,
   and one re-export
   (`native_interface_not_representable = ContactBridge.d2_not_obs_complement`).
   `lean4/Derivation.lean` gained three imports and the per-theorem
   `#print axioms` lines of the new modules.
3. **Artifacts regenerated by their generators only.**
   `artifacts/primitive_contact.json` gains `history`,
   `manifest_sha256`, `external_file_sha256_per_manifest` (read from
   the manifest field, never from the external file), `prose_status`,
   the `verdict` block with full terminal scopes, the 37-row
   `collision_cells` mirror of the Lean literal, and five finite
   enumerations E1-E5 with their bounds; the generator raises on any
   enumeration mismatch, so a red probe blocks regeneration.
   `artifacts/primitive_completion_receipt.json` gains the three
   collision terminals (10 -> 13, with CONTACT_INPUT_ABSENT retained
   and given an explicit sealed-history scope), one new adversarial
   attack with its disposition (20 -> 21), contact bounds, and the
   updated axiom block.  `completion_receipt.json`,
   `completion_dependency_graph.json` and `coverage.json` follow the
   new theorem count (1037 -> 1149).  Generators emit identical bytes
   whether or not the external file is present.
4. **Analysis quarantine.**  The `contact/analysis/` DIRECTORY is the
   only repository location that quotes the arriving vocabulary
   (SUPPLIED_INPUT), and it holds FOUR files, all of which do so:
   `contact_dictionary.md` and `contact_countermodels.json` (103
   declaration rows with native counterparts and evidence classes, the
   countermodel table, the G1-G20 gap dispositions — including the
   refused comment-borne physics and authority claims — and five
   METATHEORY scope notes), plus `lean_definition_map.md` and
   `lean_theorem_transport.md`, which quote arriving declaration names
   and full arriving Lean statements verbatim throughout.  `lean4/`,
   `code/` and `paper/` carry none of it.
5. **Verdict, tested rather than asserted.**  Primary
   CONTACT_INCOMPARABLE_WITH_COUNTERMODELS, with the asymmetry
   proved: the native -> arriving gap is signature-level and permanent
   (countermodels at carriers 1, 2 and 3, and `d2_not_obs_complement`
   quantifies over all value types), while the arriving -> native gap
   was content-level and is closed this run by the reconstruction
   under the identical axiom budget.  Also issued:
   COMMON_PRIMITIVE_KERNEL_REPLACES_BOTH, scoped to the overlap only,
   and CONTACT_EQUIVALENT_UNDER_DECIDABLE_ZERO_PLUS_APARTNESS_ADMISSIONS,
   on the relational core only.  NOT issued, with recorded reasons:
   CONTACT_STRICTLY_STRONGER (refuted by the countermodels) and
   NATIVE_STRICTLY_STRONGER (as a sealed-corpus claim it would launder
   this run's reconstruction into the sealed record; the honest
   sentence is recorded in the artifact's verdict block, and the
   containment statement is carried as a frontier CONJECTURE about
   the ENLARGED corpus).
6. **What gained scope notes** (dated 2026-08-13, marking the text
   true at its run and superseded only as to the absence of contact
   input): `paper/primitive_difference_map.md` (new section 10 plus
   the receipt-count note in section 9),
   `paper/primitive_difference_passage.md`,
   `paper/primitive_controller_universality.md`,
   `paper/primitive_interpreter_boundary.md`,
   `paper/native_derivation_completion.md`,
   `paper/native_derivation_map.md`, and the ledger entry
   CL-PD2-CONTACT.  `paper/primitive_difference_contact.md` was
   rewritten in place - it is this run's own paper, and its
   pre-contact content is preserved as the sealed history section it
   describes.
7. **Ledger extended, not amended.**  Seven new entries carry the new
   substantive claims with their evidence classes and exact evidence
   pointers: CL-PD2-CONTACT-RECONSTRUCTION (the descent layer),
   -BRIDGE (the complement bridge and the priced hypotheses),
   -COUNTERMODELS (the representability characterization and its
   refutations), -DICTIONARY (descent versus factorization),
   -KERNEL (the common replacement kernel), -ENTRY (passage entry),
   and -VERDICT (status, terminals, and the not-issued codes).  The
   sealed CL-PD2-CONTACT keeps its statement and gains only a dated
   scope note pointing at them.
8. **No sealed claim was rewritten.**  No prior theorem statement,
   terminal code, ledger claim, or countermodel was altered, weakened,
   or deleted; nothing in the arriving file bears on passage
   dynamics, growth, the cell calculus, controllers, or the
   interpreter boundary, so those records stand as written.  The only
   pre-existing claim whose WORDING became time-relative is the
   absence of contact input, which is preserved verbatim as sealed
   history in Lean (`contactStatus`,
   `contactStatusHistory`), in the receipt (CONTACT_INPUT_ABSENT with
   a sealed-history scope field), and in the ledger, each carrying a
   dated scope note instead of an edit.

## Collision audit repair - scopes narrowed to the proved statements
(2026-08-13)

An adversarial audit of the executed collision found the Lean spine
sound and the summary prose ahead of it in five places.  Every repair
below either narrows a claim to exactly what its cited theorems prove
or adds the missing theorem; no theorem statement was weakened and no
terminal code was renamed.

1. **The equivalence terminal spends TWO decidability admissions, one
   per direction.**  `isApart_repr` and `apartObs_roundtrip` carry
   `[forall x y, Decidable (r x y)]` on the ASSERTED APARTNESS;
   `obsApart_isApart` and `indist_obsApart_iff` carry
   `[forall x y, Decidable (ZeroRel O x y)]` on the ZERO relation.
   They are not interchangeable - the zero relation of `apartObs r h`
   is the negation of `r`, and `Decidable` of a negation does not
   return `Decidable` of the statement, which is exactly the residue
   `stability_schema_iff_dne` prices at DNE.  Every summary site had
   collapsed them into one banner; each now states the split, and the
   generator strings that produce the artifact and the receipt were
   the source of the error, so they were fixed there
   (`code/run_primitive_contact.py:SCOPE_EQUIVALENT`).  The word
   "exactly" was dropped where only sufficiency plus one countermodel
   is proved (`obsSetting_bc` / `obsSetting_bl`, `vhom_unique_of_onto`).
2. **The observer half of COMMON_PRIMITIVE_KERNEL_REPLACES_BOTH now
   has a theorem.**  `ContactKernel.toDiffObs` builds the observer
   record from a kernel plus the two law declarations,
   `toDiffObs_fields` proves the fields are carried unchanged and the
   kernel is recovered (`ofDiffObs (toDiffObs K hs ht) K.a K.b
   K.apart_ab = K`), and `toDiffObs_apart` proves the relations match
   - all three by `rfl`, classed DEFINITION (a record identity, not a
   derivation).  Before this the clause rested on prose while the
   only theorems in that direction were the negatives
   `kernel_not_observer` and `kernel_zero_not_trans`.
3. **The four OPEN cells the collision declared are registered as
   open obligations.**  `open_bridge_cotrans` (price WLEM),
   `open_bridge_located` (a WLEM-implication, converse OPEN),
   `open_kernel_grade` (DNE) and `open_kernel_bl` (metatheoretic
   underivability of Located) now appear in
   `primitive_completion_receipt.json:open_obligations`, taking it
   from four entries to eight; the two collision conjectures
   (enlarged-corpus containment; the converse of
   `located_schema_implies_wlem`) appear in `frontier_conjectures`,
   taking it from three to five.  The sentence in
   `paper/primitive_difference_map.md` asserting that both counts were
   unchanged was replaced by the actual accounting.
4. **Scope qualifiers carried from the analysis into the summaries.**
   The representability crown and the carrier-1 countermodel are
   Prop-valued statements (`DiffObs X Prop`), and every contact
   theorem quantifies over `Type` (universe 0); the factorization
   dictionary is stated for kernel observers on `Nat` with
   `Nat`-valued views; `kernel_no_terminal_collector` is terminality
   at the induced-apartness morphism grade, not at `VHom` grade;
   `kernel_licenses_entry` contributes endpoint distinctness only, its
   other two conjuncts being sealed constants; `quot_barrier` is more
   general than the arriving SETOID-BASED machinery (METATHEORY,
   citation only); the 37 matrix rows are machine-checked for COUNT
   and mirror-consistency, their statuses being declared labels naming
   their evidence; the field-for-field premise `H_struct` is a scratch
   compile outside the repository and is NOT reproducible from it;
   and of the nine candidate readings only Bs has a Lean-proved
   carrier minimality (the others are least-carrier-by-signature
   METATHEORY, unclaimed for D and E, inherited for Bc/Bl/F).  The
   `WITH_COUNTERMODELS` half of the primary terminal covers the
   native -> arriving direction only; the other half is an absence
   claim about the sealed corpus and now says so first.
5. **One converse added rather than a claim withdrawn.**
   `ContactBridge.collapse_collision_is_pair_blocked` and
   `pair_blocked_iff_collapse_collision` supply the direction the
   "same event in two vocabularies" reading needed;
   `PrimitiveContact.contactStatus` keeps its sealed value and loses
   its misleading doc-comment.  `artifacts/lean_axioms.txt` grows
   from 1145 to 1149 reports, all within {propext, Quot.sound}.

## Review repair - firewall scan, pair-choice grade, committed anchor
(2026-08-13)

Three leftover-prose findings from the collision review, none of
which change a theorem, a terminal, or an artifact:

1. **Vocabulary firewall is now scanned.**  `tests/test_primitive_contact.py`
   walks `git ls-files` against the working denylist of 102
   (full census minus the nine native-or-core names).  A hit outside
   `contact/analysis/` fails, except the documented native subject
   name `PrimitiveDifference` (verified at `a5caee2`).  The 111/102
   census pins in `tests/test_primitive_receipt.py` are unchanged.
2. **`pair_choice_load_bearing` is non-uniqueness, not a refutation
   of existence.**  The observer-alone row in
   `contact/analysis/lean_theorem_transport.md` is relabeled
   NON-UNIQUE / pair choice load-bearing; `ofDiffObs` still applies
   to a witnessed pair.  The word "forced" on that carrier remark is
   replaced by METATHEORY.  The collapse row remains the existence
   refutation.
3. **Anchor no longer says UNCOMMITTED.**  The five declarations
   added after `ebb1e0b` are described as committed in this
   collision.  Companion wording in `lean_definition_map.md` matches.

## Packet 5 audit and packet 2 pair-choice lemma (2026-08-14)

Base `bd2e8c8` (PR #19 merged).  Mission
`prompt/flw_mission_pr14.md`.  AuthorityEffect None.

1. **Packet 5 — audit only, no new Lean.**
   `PrimitivePassage.obst_conditions_independent` already exhibits
   the four maximal proper subsets of the `obstP` conjunction
   (retained / protected / declared / zero), each with a concrete
   non-obstructing state, plus the all-four witness.  The predicate
   reads only `wit`, `prot`, and `obs`; the independence states vary
   those stores alone.  Companions
   `obst_requires_observation`, `no_protection_no_obstruction`,
   `obst_agrees_when_declared`, `obst_diverges_when_undeclared`
   confirm the declared-observation conjunct is not a convention.
   Scope: independence of *this* four-conjunct Bool predicate, not a
   reverse-mathematics claim that no other activation signature
   exists.  `two_rule` may keep citing it as the activation theorem.

2. **Packet 2 — pair-choice necessity as a reusable lemma.**
   `ContactKernel.kernel_from_obs_iff_pair`: a kernel carrying an
   observer's `delta` and `Zero` exists iff a non-zero pair exists.
   `ContactKernel.eq_ofDiffObs_of_fields`: any such kernel equals
   `ofDiffObs` at its own endpoints.  Neither statement claims
   uniqueness of the pair (`pair_choice_load_bearing` remains the
   non-uniqueness witness; `kernel_no_witness_from_collapse` remains
   the no-pair witness).  Axiom reports 1149 → 1151, both new
   theorems axiom-free.
