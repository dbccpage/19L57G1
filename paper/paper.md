# A Least Finite Formal System from One Opaque Inscription

Every statement in this paper carries exactly one classification tag from:
**[declared metatheory]**, **[definition]**, **[finite computation]**,
**[theorem]** (machine-checked in Lean 4), **[bounded theorem]** (proved or
exhaustively computed only within explicitly declared bounds),
**[conjecture]**, **[counterexample]**, **[unresolved]**.

## 1. Experimental boundary

**[declared metatheory]** The experiment is blind: no external
architecture, theory, or project terminology is imported, targeted, or
mentioned anywhere in the derivation, the code, the proofs, or this paper.
A post-hoc comparison with known mathematics was originally permitted in
this final section; the caller's correction of 2026-08-11 withheld it, and
it is therefore omitted entirely (see `paper_change_log.md`).

**[declared metatheory]** Inputs (read-only, byte-identical throughout):

| file | bytes | SHA-256 |
|---|---|---|
| `prompt/prompt.md` | 2805 | `A613A1965E4F02FEE00DF4D42041FCEECA176ABCFAA9202C3E769021305940B5` |
| `prompt/seed_prompt.md` | 10245 | `EE3BA0583FEA2A11F1294538C912C542B3FAEE5316355DC226EFB92EF64646AB` |

**[declared metatheory]** Caller corrections received on 2026-08-11
(two sets, transcribed in `paper_change_log.md` entries 4 and 5) are part
of the challenge history and were applied before freezing.

**[declared metatheory]** Toolchain: Python 3.14.2 (pytest 9.0.2,
coverage 7.13.1, mypy 1.19.1 strict), Lean 4.33.0 with Lake 5.0.0, no
external Lean libraries.  All computational artifacts under `artifacts/`
are byte-deterministic (verified by dual runs; no timestamps, no
environment data).  The reference implementation is `code/derivation/`;
the artifact generator is `code/run_derivation.py`.

**[declared metatheory]** Declared resource bounds: candidate deltas of at
most 2 items; concrete enumeration of form arities up to 2 (the arity
dimension is additionally covered by a grammar-wide theorem, section 7.4);
15 requested augmentation rounds; node budgets 1200 (measure mu1) and 3000
(measure mu2) per tree; 100000 candidate bijections per canonicalization.

## 2. Metatheory / object language separation

**[declared metatheory]** The metatheory has: presentation tokens
(strings), event sequences, indices, finite data structures, and
arithmetic.  The object language has only what a *regime* admits.  Nothing
in the object language can see token glyphs, component counts, order,
concatenation, multiplicity, substring structure, matching, or string
equality; these live in the metatheory unless an admitted judgment
internalizes a distinction.

**[declared metatheory]** Distinctions kept separate throughout: supply
(external presentation), mention, admission (state change by explicit
event), current-state designation, retention, observation (derivability of
plugged contexts), presentation identity (token equality; metatheory
only), internal identity (datum index), observational equivalence (profile
equality), behavioral separation (profile difference), semantic
interpretation (never assigned).

## 3. Definitions (dependency order)

All definitions below are **[definition]**, implemented in
`code/derivation/model.py`, `observe.py`, `candidates.py`, `iso.py`,
`engine.py`.  The Lean development (`lean4/Derivation/`) formalizes a
*token-erased abstraction*: data are counted, not named, so token-level
admission deduplication is not directly represented.  The bridge is
proved, not asserted: `erase_step` and `erase_replay`
(`Derivation/Erasure.lean`) show that replaying a token-aware history
with deduplicating admission and then erasing tokens equals replaying the
erased history in the token-erased model (a duplicate admission erases to
a bare supply, which is a proved no-op).  **[theorem]**

1. **Regime** `(data, forms, insts, rules, reqs)`: admitted data in
   admission order (entries record presentation tokens, visible only to
   the metatheory; internal identity is the index); judgment-form arities
   (each >= 1); admitted judgment instances `(form, args)`; forms carrying
   the uniform all-tuples rule; imposed separation requirements `(i, j)`,
   `i < j`.
2. **Admission events**: `Supply(token)` (presentation only),
   `AdmitDatum(token)` (dedup on presentation identity — a declared
   metatheoretic convention), `AdmitForm(arity)`, `AdmitInst(form, args)`,
   `AdmitRuleAll(form)`, `Impose(i, j)`.  Ill-formed admissions are
   rejected.  **Replay**: a regime is *certified* only if it equals the
   fold of its recorded history from genesis.
3. **Context**: a form with a slot tuple containing at least one hole;
   **plug** fills every hole with one datum.  A context is *well-formed*
   when its form is admitted, its slot count equals the form's arity, and
   its filled slots name admitted data.  (The Python enumeration produces
   only arity-length slot tuples by construction; the Lean `wfCtx`
   carries the arity-length constraint explicitly.)
4. **Derivability**: membership in the admitted instances, or coverage by
   a uniform all-tuples rule.  No other inference exists.
5. **Profile** of a datum: the set of well-formed contexts whose plugging
   is derivable.  **Collapse**: equal profiles.  **Internal separability**
   (the declared sense used for every separation requirement): profiles
   differ, i.e. some well-formed context is derivable when plugged with
   one datum and not the other.
6. **Delta**: a finite multiset of items — `NewDatum`, `NewForm(arity)`,
   `NewInst(form, args)` (may reference a form added by the same delta),
   `NewRuleAll(form)`.  **Cost measures** (both declared): `mu1` = item
   count; `mu2` = (item count, sum of new-form arities), lexicographic.
7. **Valid response** to `Separate(i, j)`: the delta applies and the
   result separates the target while every previously imposed requirement
   stays separated (requirements are persistent constraints — declared
   challenge semantics).
8. **Isomorphism**: bijections on datum and form indices preserving
   arities, instances, rules, and requirement pairs (as unordered pairs);
   presentation tokens are forgotten.  **Canonical form**: minimum over
   color-class-preserving bijections of a total serialization, with
   isomorphism-invariant iterated refinement; cross-checked against a
   brute-force minimum over all bijections.
9. **Endogenous generator**: from the admitted structure alone, the least
   observationally collapsed pair of admitted data, or nothing at the
   fixpoint where every pair is separated.  It reads only profile equality
   and admission order — never token glyphs — supplies no data, and
   imports no new goal kind (it reissues the requirement pattern already
   admitted in `reqs`).
10. **External continuation policy**: the supply-and-admission of one
    fresh opaque token when the endogenous generator is at its fixpoint.
    **[declared metatheory]** This is an explicitly declared external
    policy, not a derived transition.  Runs with the policy disabled are
    the *closed-system baseline*.
11. **Admission readings.**  The challenge text underdetermines admission:
    *Reading L* — only explicit retention admits (the initial inscription
    is presented, never retained); *Reading F* — the possession phrasing
    of the initial inscription admits it at genesis.  Both readings are
    carried throughout.  **[unresolved]** No internal fact selects between
    them.

## 4. Challenge 0 — the initial inscription

The only object-language inscription is the opaque whole `<>`, treated as
one atomic datum with no inherited meaning.

* **[theorem]** (`supply_no_op`) Bare supply does not change the admitted
  state: `stepE r (supply t) = some r` for every regime and token.
* **[theorem]** (`genesis_underivable`, `underivable_of_empty`) Nothing is
  derivable at genesis, and nothing is derivable in any regime with no
  instances and no rules.
* **[theorem]** (model-scoped) No successor is internally forced: the
  model contains no transition machinery other than external-event-indexed
  admission; a proposal cannot mutate state without an admission event
  (structurally enforced; negative tests reject every ill-formed
  admission).
* **[finite computation]** (`artifacts/challenges.json`, challenge0)
  Context count 0, derivable set empty, admitted data empty (reading L) or
  the single opaque datum (reading F) — in both readings there are no
  internal observables of any kind.

Result: **inertia**.  Exactly nothing follows from the initial inscription
alone.

## 5. Challenge 1 — supply of `<a>`

* **[finite computation]** The supply is a new external presentation; it
  is not an admission (by `supply_no_op` it cannot change state).
* **[unresolved → resolved by convergence]** Whether `<a>` is *admitted*
  at Challenge 1 is underdetermined (no retention act is declared).  Both
  sub-readings were carried; **[finite computation]** they converge to the
  same regime at Challenge 2 close, because admission dedups on
  presentation identity (`sub_readings_converge_at_challenge2 = true`).
* **[theorem]** (`collapsed_of_no_insts`) No internal observable
  distinction arises in any sub-reading: with no admitted instances every
  pair of data is observationally collapsed.

## 6. Challenge 2 — `<a>` and `<ab>` retained

Both wholes are supplied and retained, hence admitted (both readings).

* **[finite computation]** Externally the two tokens are distinct
  (metatheory); reading L admits `(<a>, <ab>)`, reading F admits
  `(<>, <a>, <ab>)`.
* **[theorem]** (`R2L_collapsed`, `R2F_collapsed`) Every pair of admitted
  data is observationally collapsed in both readings: two externally
  different admitted inscriptions remain internally indistinguishable.
* **[counterexample]** (`admission_without_expressive_increase`) To the
  claim "a new external inscription necessarily increases internal
  expressive power": admitting a fresh datum is a real state change, yet
  the number of observational classes stays 1 (it was already <= 1).
* **[theorem]** (`historyL_replays`, `historyF_replays`) The recorded
  Challenge 0-3 histories replay exactly to the Challenge 3 regimes.

What changed by admission: the metatheoretic cardinality of the admitted
data and the replayable history.  What remains internally unavailable:
everything — glyph identity, component count, order, concatenation,
multiplicity, substring structure, matching, string equality.

## 7. Challenge 3 — required separation

The caller requires `<a>` and `<ab>` to be internally separable.

### 7.1 Declared meaning and failure of the current regime

**[definition]** Internal separability = behavioral separation by positive
derivability (profiles differ; section 3.5).

**[theorem]** (`R2L_collapsed` / `R2F_collapsed` instantiated) The current
regime fails it; no witness context exists.

### 7.2 Minimality below two items (absolute)

**[theorem]** (`cost1_insufficient_general`, instantiated as
`cost1_insufficient` for reading L and `cost1_insufficient_F` for
reading F) — *candidate bounds: none (the full item grammar: any arity,
any argument tuple, any single item); cost measure: mu1; scope: absolute
over the grammar.*  No delta of zero or one item is a valid response on a
form-less, instance-less regime: every such delta either fails to apply
(an instance or rule without an admitted form) or leaves the instance set
empty, and with no instances every pair stays collapsed (uniform rules
flood all data equally).

**[theorem]** (`deltaU0_valid`, `deltaU0F_valid`) Two-item responses
exist.  Hence the minimum cost is exactly 2 in both readings.

Capability counts **[finite computation]**: each minimum bundles exactly
one new judgment form and one new instance — a "single step" that bundles
both is measured at cost 2, never 1 (negative test
`test_smuggling_a_bundle_is_not_one_item`).

### 7.3 Non-uniqueness under mu1

**[theorem]** (`mu1_minimum_not_unique`) — *bounds: none for the
statement; measure: mu1; scope: absolute.*  There exist two valid two-item
responses (unary mark; binary link) whose results are non-isomorphic
(arity is an isomorphism invariant), while no response of at most one item
is valid.  The minimum corrective augmentation is **not unique**.

**[bounded theorem]** (engine enumeration, `artifacts/challenges.json`) —
*bounds: max_items 2, max_arity 2; measure: mu1; scope: complete within
these bounds, by exhaustive enumeration cross-checked against the unpruned
space.*  The tied minimum classes under the implemented isomorphism:

| reading | valid deltas | iso classes | classes |
|---|---|---|---|
| L | 6 | 3 | unary mark; binary link; binary self-loop |
| F | 10 | 5 | + link to the genesis datum; link from the genesis datum |

Reading F's two extra classes use the never-required genesis datum as a
relational anchor; they are non-isomorphic to each other because the
bijection must preserve the requirement pair (`test_direction_relative_
to_requirement_matters`, `F_OUT`/`F_IN`).

**[theorem]** (`deltaK_valid`, `deltaK_length`, `markK_pairwise_noniso`) —
*bounds: none; measure: mu1; scope: absolute.*  For every arity k >= 1 the
k-ary mark is a valid two-item (hence minimum) response, and distinct
arities give non-isomorphic results: **the mu1 tie class is countably
infinite**.  Any concrete enumeration is therefore complete only relative
to an arity bound; the table above is the max_arity = 2 slice.

### 7.4 Uniqueness under mu2

**[theorem]** (`mu2_unique`, reading L) — *bounds: item grammar-wide
(any single items a, b); measure: mu2 = (items, new-form arity sum),
lexicographic; scope: absolute over the grammar for reading L.*  Every
valid two-item response with new-form arity sum <= 1 produces a regime
isomorphic to the unary mark.  Together with the cost floor (7.2) and the
absence of valid (2, 0) deltas (any two-item delta without a new form
cannot carry an instance on a form-less regime), the mu2-minimum is
**unique up to isomorphism**: mu2 = (2, 1), the unary mark.

**[bounded theorem]** (engine) Reading F: exactly one mu2 class within the
declared bounds (the unary mark on either required datum; the mark on the
genesis datum fails the target and is refuted).  The grammar-wide Lean
analogue for reading F is **[unresolved]** (not formalized).

**[finite computation]** Uniqueness is *measure-relative*: the answer to
"is a minimum corrective augmentation necessarily unique?" is **no** under
mu1 and **yes, up to isomorphism** under mu2.  The choice between mu1 and
mu2 is a declared metatheoretic act; neither is derived.

## 8. Autonomous continuation

### 8.1 Generator decomposition

**[declared metatheory]** After Challenge 3 the challenge source is the
generator of section 3.9-3.10: the *endogenous generator* (least collapsed
pair) plus, at its fixpoint, the *external continuation policy* (fresh
supply).  Round 1 of every tree answers the externally imposed Challenge 3
requirement; later separation rounds answer the endogenous generator.

**[finite computation]** Token-blindness of the endogenous generator:
renaming every presentation token changes nothing
(`test_endogenous_generator_is_token_blind`); in the Lean model tokens are
absent by construction.

**[theorem]** (`mark_progress`) Response existence: on any well-formed
regime whose imposed requirements are all separated, every *supplied*
separation demand has a valid response (one fresh unary form plus one
mark), which moreover preserves every existing separation.  This theorem
is exactly response existence — it does **not** prove autonomous demand
generation, and it does **not** prove an unbounded tower.  Its observed
consequence: no `terminal_no_response` node occurs in any exported run.

### 8.2 Pruning lemmas for the cost-2 enumeration

* **[theorem]** (`separable_of_subrules`) A separation witness never
  inhabits a uniformly ruled form, so removing rule items preserves every
  separation: a delta containing a uniform rule is never a minimum valid
  response.
* **[bounded theorem]** (cross-check `test_pruned_cost2_contains_every_
  valid_full_delta` over bare, marked, and structurally mixed base
  regimes) Unreferenced fresh data and unreferenced fresh forms never
  matter, and an instance-only delta changes the profiles of the target
  pair only if some instance mentions a target datum.  Lean
  formalizations of these three structural prunings: **[unresolved]**;
  they enter every tree computation and are certified computationally
  against the unpruned space.

### 8.3 Branch trees (external continuation policy enabled)

**[finite computation]** (`artifacts/tree_*.json`; per-branch evidence in
`artifacts/claims.json`, `CL-BRANCH-REPORTS`).  Branches are quotiented:
isomorphic regimes merge into one node (a DAG; a *maximal branch* is a
leaf).  Every node is replay-certified from genesis.

| tree | nodes | edges | max depth | terminal | budget-cut | round-cut | open | every maximal branch terminates |
|---|---|---|---|---|---|---|---|---|
| L mu1 | 1205 | 1250 | 7 | 0 | 927 | 0 | 0 | no |
| L mu2 | 963 | 1022 | 15 | 0 | 0 | 568 | 0 | no |
| F mu1 | 1201 | 1244 | 6 | 0 | 886 | 0 | 0 | no |
| F mu2 | 1847 | 1960 | 15 | 0 | 0 | 885 | 0 | no |

* The mu2 trees have **no budget cutoff**: the full isomorphism-quotient
  tree to the requested 15 rounds is finite and fully enumerated
  (963 / 1847 nodes).  Their leaves are round-cut, not terminal: the runs
  were stopped at the requested depth.  **[finite computation]** Reaching
  a finite requested depth is exactly that — *not* a proof of
  unboundedness, and no unboundedness claim is made
  (`CL-REACHES-REQUESTED-DEPTH-WITH-EXTERNAL-SUPPLY`).
* The mu1 trees hit the declared 1200-node budget at depths 7 / 6; the
  exact frontier (927 / 886 leaves) is exported.  Enumeration below the
  cut is complete within the declared bounds.
* What is and is not established about continuation beyond the runs:
  response existence for any supplied demand is **[theorem]**
  (`mark_progress`); the behavior of the external continuation policy
  past the exported depths is **[unresolved]** — this paper makes no
  claim about it.

**[finite computation]** Emergent transition roles (counts over accepted
edges): *supply* (195 / 111 / 233 / 413 per tree above), *discrimination*
(one new instance: 1047 / 858 / 1001 / 1458), *innovation* (fresh form +
instance: 8 / 53 / 10 / 83), and rare *double discrimination* (two
instances at once: 6, in F mu2 only).  The enumerated fresh-datum shape
(*auxiliary witness*) never appears among accepted minima in these runs:
in binary-form regimes, cost-1 links to existing data always suffice
first.

### 8.4 Closed-system baseline (external policy disabled)

**[finite computation]** (`artifacts/nosupply_*.json`,
`CL-ENDOGENOUS-TERMINATION`):

| baseline | nodes | terminal branches | budget-cut | round-cut | open | rounds used | pair bound | every maximal branch terminates |
|---|---|---|---|---|---|---|---|---|
| L | 4 | 3 | 0 | 0 | 0 | 1 | 1 | **yes** |
| F | 20 | 16 | 0 | 0 | 0 | 3 | 3 | **yes** |

**[theorem]** (`strict_bounded_length`, `no_supply_round_bound`,
`allPairs_length`) The counting laws behind this are *conditional*
abstract laws: a run whose measure strictly increases each round and
never exceeds B has at most B+1 states, and the requirement language of a
regime with n data has exactly n(n-1)/2 elements (stated division-free as
`2 * length = n * (n - 1)`).

**[finite computation]** The connection of those hypotheses to the actual
transition system — each accepted separation round imposes exactly one
new requirement over a fixed datum count — is discharged computationally
for the exported runs; a Lean theorem connecting the hypotheses to the
transition system itself is **[unresolved]**.

**[bounded theorem]** Closed-system termination: within the declared
bounds, every maximal branch of both baselines ends at the
all-pairs-separated fixpoint, within the pair bound (L: 1 <= 1; F: 3 <= 3;
zero budget-cut, round-cut, and open branches — the flag
`every_maximal_branch_terminates` is computed over *all* maximal
branches, never from the existence of one terminal node).

## 9. The endogenous continuation obligation

*Can the admitted structure generate its next unresolved requirement
without inspecting presentation-token glyphs, supplying a fresh external
datum, importing a new external goal, or assuming the desired
continuation?*

**Answer: yes, up to a provable fixpoint; no, beyond it.**

1. **[definition]** The endogenous generator (section 3.9) exists and is
   the weakest we can justify: it reads only the admitted structure and
   admission order, issues one requirement at a time in canonical order,
   and reissues only the requirement pattern already admitted in `reqs`
   (no new goal kind).  Weakest-ness is a declared-metatheory judgment,
   not a proved universal property (section 10, question 10).
2. **Admissibility** — **[finite computation]** token-blind (renaming
   test); supplies no data and imposes only requirements over already
   admitted data (by construction of its output type); **[theorem]** in
   the Lean model, tokens do not exist, so no glyph inspection is even
   expressible.
3. **Preservation** — **[theorem]** accepted rounds preserve satisfaction
   of all imposed requirements (validity is part of acceptance;
   `mark_progress` exhibits a preserving response), and the requirement
   set grows strictly.
4. **Implementation** — **[finite computation]**
   `next_endogenous_challenge` in `code/derivation/engine.py`;
   deterministic; the closed-system trees of section 8.4 are its full
   quotient towers.
5. **Comparison with the external-supply tree** — **[finite computation]**
   (`CL-ENDOGENOUS-VS-EXTERNAL`): closed system L/F: 4 / 20 nodes, all
   maximal branches terminal at rounds <= 1 / 3; external policy: 963-1847
   node quotient trees at the requested 15 rounds (mu2, complete) and
   1200-node budget frontiers (mu1).
6. **Beyond the fixpoint** — **[theorem]** at the fixpoint every pair of
   admitted data is separated, so no unresolved requirement exists in the
   admitted requirement language (all n(n-1)/2 pairs are exhausted —
   `allPairs_length`); generating any further requirement would need a
   fresh datum (external supply) or a new requirement kind (external
   goal).  **The native tower stops.**  Further continuation requires the
   declared external continuation policy.

A proved finite termination of the native tower is the result; no longer
or infinite tower is forced.

## 10. The required questions

1. *Does any object-language transition follow from the initial
   inscription alone?*  **No** — **[theorem]** section 4.
2. *Can a proposed transition alter state without a separate admission
   rule?*  **No** — **[theorem]** `supply_no_op` plus the structural fact
   that every state change is an admission event; ill-formed admissions
   are rejected (negative tests).
3. *Does a new external inscription necessarily increase internal
   expressive power?*  **No** — **[counterexample]** section 6.
4. *Can two externally different admitted inscriptions remain internally
   undecidable or observationally collapsed?*  **Yes** — **[theorem]**
   section 6.
5. *If a current abstraction identifies two cases that a declared task
   requires to be separate, can any operation defined only on that
   abstraction recover the distinction?*  **No** — **[theorem]**
   (`quotient_barrier`, `quot_barrier`, `barrier_R2L`): every function out
   of the quotient is constant on identified elements.
6. *Is a minimum corrective augmentation necessarily unique?*
   **Measure-relative** — **[theorem]** not unique under mu1 (with an
   infinite tie family across arities); unique up to isomorphism under
   mu2 (grammar-wide for reading L; **[bounded theorem]** for reading F).
   Every uniqueness statement above carries its bounds and measure
   (section 7).
7. *What additional rule, if any, makes a long or unbounded sequence of
   augmentations possible rather than immediate termination?*  **The
   external continuation policy (fresh supply)** — **[bounded theorem]**
   without it the native tower terminates within n(n-1)/2 rounds
   (sections 8.4, 9); with it the process reached every requested depth
   tried (**[finite computation]**), and every supplied demand has a
   response (**[theorem]** `mark_progress`).  Whether the sequence is
   unbounded is **[unresolved]**: no unboundedness claim is made.
8. *Can unresolved requirements be counted invariantly under renaming or
   isomorphism?*  **Yes within the implementation** — **[finite
   computation]** the unresolved count (collapsed pairs) is preserved
   under all token renamings and index bijections (canonicalization
   invariance tests, exhaustive over the Challenge 3 classes); the
   requirement-language size law is **[theorem]** (`allPairs_length`).  A
   Lean transport proof of count invariance under regime isomorphism:
   **[unresolved]**.
9. *What recurring transition roles emerge from the derivation itself?*
   **[finite computation]** supply, discrimination, innovation, rare
   double discrimination; auxiliary-witness enumerated but never minimal
   in the observed runs (section 8.3).
10. *Is the final process minimal or initial among a clearly defined class
    of finite processes satisfying the same challenges?*  **Claim
    refused** — **[unresolved]**.  No universal property was proved.  What
    is proved: determinism of the engine given the declared bounds
    (byte-identical artifacts), completeness of enumerations within
    declared bounds, and the per-stage minimality/uniqueness results with
    their scopes.
11. *At what first stage do familiar mathematical structures become
    definable?*  **Withheld** — the caller's blind-protocol correction
    forbids naming external structures; the question cannot be answered
    without doing so.  **[unresolved]** by instruction.  What can be said
    internally: from Challenge 3 round 1 onward, each datum's internal
    identity is exactly its profile, and the two surviving discrimination
    styles are attribute-like (unary marks) and relation-like (binary
    links); their formal properties are fully captured by the exported
    structures.

## 11. Strongest defensible terminal result

**Terminal statement** (each clause tagged):

Within the declared metatheory and candidate grammar:

* (a) **[theorem]** The initial inscription generates nothing: no
  derivable judgment, no internally forced successor; supply without
  admission never changes state.
* (b) **[theorem]** Admission without judgment structure yields total
  observational collapse; externally distinct data can remain internally
  indistinguishable, and admission alone never increased expressive power
  (counterexample to necessity).
* (c) **[theorem]** The first separability requirement has minimum
  response cost exactly two items, absolutely over the item grammar, in
  both admission readings.
* (d) **[theorem]** Under the item-count measure the minimum is not
  unique — three non-isomorphic tied classes in reading L and five in
  reading F within the declared bounds (**[bounded theorem]**), and a
  countably infinite tie family indexed by arity (one member for every
  arity k >= 1).  Under the
  refined measure the minimum is unique up to isomorphism (grammar-wide
  for reading L; within bounds for reading F).
* (e) **[theorem]** Response existence: every supplied separation demand
  on a well-formed accepted regime is answerable.
* (f) **[bounded theorem]** The endogenous continuation exists, is
  token-blind, and provably terminates: the native tower stops at the
  all-pairs-separated fixpoint within n(n-1)/2 rounds (closed-system
  baselines: 1 and 3 rounds, every maximal branch terminal).
* (g) **[finite computation]** With the declared external continuation
  policy the process reached the requested 15 rounds; the
  isomorphism-quotient tree at that depth is finite and fully enumerated
  under the refined measure (963 / 1847 nodes) and budget-bounded with
  exact exported frontiers under the item-count measure.  Continuation
  beyond the exported depths is **[unresolved]**; no unboundedness is
  claimed.
* (h) **[unresolved]** Two admission readings of the challenge text
  survive with no internal fact separating them; both towers are carried
  in full.

## 12. Limitations and open obstructions

* **[declared metatheory]** The cost measures, the candidate grammar, the
  isomorphism relation, the persistence of requirements, the endogenous
  generator's canonical order, and the external continuation policy are
  declared, not derived.  Different declarations could yield different
  towers; the mu1/mu2 split documents one such sensitivity precisely.
* **[unresolved]** Lean formalizations of: the three structural pruning
  lemmas (datum/form irrelevance, mention lemma) and the delta-level
  rule-removal bridge (the proved `separable_of_subrules` covers witness
  transfer under a shrunken final rule set; the bridge from delta items
  to shrunken rule sets is computational); grammar-wide mu2 uniqueness
  for reading F; count-invariance transport under isomorphism; a theorem
  connecting the strict-growth/boundedness hypotheses of the counting
  laws to the transition system; the behavior of the external
  continuation policy beyond the exported depths.
* **[bounded theorem]** All tree-level results are relative to the
  declared bounds (items <= 2, arity <= 2 concrete, 15 rounds, node
  budgets); the exact frontiers are exported for continuation.
* **[unresolved]** The admission-reading underdetermination (L vs F) is a
  fact about the challenge text, not about the object language; it cannot
  be internally resolved.
* Coverage and build gates at freeze: 72 tests passing; line coverage
  99.86%, branch coverage 98.81% (thresholds 95/95); `lake build` clean.
  Axiom status, exactly: no `sorry`, no `admit`, no custom
  conclusion-producing axioms, no `unsafe`, no `partial`; the standard
  Lean-core dependencies `propext` and `Quot.sound` remain, per-theorem
  in `artifacts/lean_axioms.txt` (44 exported reports; several theorems
  are axiom-free).

## 13. Post-hoc comparison

Withheld in full, per the caller's blind-protocol correction of
2026-08-11 (`paper_change_log.md`, entry 4).  No external theory,
architecture, or terminology is named anywhere in this repository outside
the read-only seed prompt.
