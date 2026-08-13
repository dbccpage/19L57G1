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
   typed-refusal top closes by partiality what totality cannot;
   self-description without self-justifying evaluation; and the
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
5. The simplex ladder generalized to arbitrary finite dimension:
   `ladder_general` upgrades the review-pass conjecture to a theorem
   of the generalized declared calculus; dimension-4 demonstration
   replayed in Lean, dimension 5 in Python; the general composite
   boundary vanishing remains the open conjecture.
6. Imported inputs kept explicit throughout: fresh supply,
   protection, observer transport, budget, activation.

