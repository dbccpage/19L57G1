# A Finite Formal System from an Opaque Seed under Declared External Challenges

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

**[declared metatheory]** Inputs (read-only throughout; every result
derives from the opaque seed inscription *under the declared external
challenges* transcribed from these files):

| file | presentation | bytes | SHA-256 |
|---|---|---|---|
| `prompt/prompt.md` | supplied = repository-canonical | 2805 | `a613a1965e4f02fee00df4d42041fceeca176abcfaa9202c3e769021305940b5` |
| `prompt/seed_prompt.md` | as supplied (CRLF) | 10245 | `ee3ba0583fea2a11f1294538c912c542b3faee5316355dc226efb92ef64646ab` |
| `prompt/seed_prompt.md` | repository-canonical (LF; normalized once at the original staging) | 9972 | `4ea4682e1da25363f9c7c1e9234b4b248f980097ae92d6f7dc1e8e8dd9bd4388` |

`prompt/prompt.md`'s byte-identity mandate holds in both the working tree
and the repository; both presentations of the seed prompt are pinned by
CI (`ci/check_prompt_hashes.py`).

**[declared metatheory]** Caller corrections received on 2026-08-11 and
2026-08-12 (four sets, transcribed in `paper_change_log.md` entries 4-7)
are part of the challenge history and were applied before freezing.

**[declared metatheory]** Toolchain: Python 3.14.2 (dependencies pinned
in `requirements.txt`), Lean 4.33.0 with Lake 5.0.0, no external Lean
libraries.  All computational artifacts under `artifacts/` are
deterministic (no timestamps, no environment data): committed summaries
carry the SHA-256 of the full exports; full trees are normalized DAG
records (parent references and edge event-deltas, no per-node histories)
under `artifacts/full/*.json.gz`, reproducibly compressed (fixed mtime
and level).  Every DAG edge carries a certificate: creation edges must
replay from their parent to the exact stored child, and merge edges carry
explicit datum/form bijections verified to map the replayed result
exactly onto the stored child representative (`verify_full_export`
re-checks all of this independently and rejects a single invalid merge
edge even when every node retains a valid creation path).  Independent verification runs in CI
(`.github/workflows/verify.yml`): pinned dependencies, pytest, separate
95% line and branch coverage gates, mypy strict, `lake build`,
forbidden-token and axiom audits, prompt-hash verification, and artifact
regeneration with content comparison.  The reference implementation is
`code/derivation/`; the artifact generator is `code/run_derivation.py`.

**[declared metatheory]** Declared resource bounds: candidate deltas of at
most 2 items; concrete enumeration of form arities up to 2 (the arity
dimension is additionally covered by a grammar-wide theorem, section 7.4);
15 requested augmentation rounds; *pre-expansion node guards* of 1200
(measure mu1) and 3000 (measure mu2) per tree — the guard is checked
before a node is expanded, and an expansion in progress completes, so an
export may contain slightly more nodes than the guard value (hence the
name; it is not a strict node cap); 100000 candidate bijections per
canonicalization or automorphism search.

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
*token-erased abstraction*: data are counted, not named.  The bridge is
proved, not asserted, and rests on two theorems rather than on duplicate
idempotence alone:

* **Erasure simulation** (`erase_step` / `erase_replay`,
  `Derivation/Erasure.lean`): replaying a token-aware history with
  deduplicating datum admission and then erasing tokens equals replaying
  the erased history in the token-erased model (a duplicate datum
  admission erases to a bare supply, a proved no-op).  **[theorem]**
* **Membership extensionality** (`Derivation/Ext.lean`): Python's
  admitted collections are sets while Lean's are deduplicated lists;
  under the proved relation `RegimeExt` (equal data counts and form
  tables, membership-equal instance/rule/requirement collections) every
  observable transports — derivability, context well-formedness,
  collapse, separability, item and delta application, and response
  validity (`derivable_ext` … `validResponse_ext`).  Two list
  representations of the same admitted sets therefore support exactly
  the same claims; no exported result depends on list order or
  representation.  **[theorem]**

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
   when its form is admitted, its slot count equals the form's arity, at
   least one slot is a hole, and its filled slots name admitted data.
   (The Python enumeration produces exactly these by construction; the
   Lean `wfCtx` carries the arity-length and hole constraints
   explicitly, so the two context spaces coincide.)
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
9. **Declared pair-separation closure policy**: from the admitted
   structure, reissue the admitted requirement pattern (separation) on
   the collapsed pairs — one challenge branch per *automorphism orbit* of
   collapsed pairs (an automorphism is a bijection pair mapping the
   regime onto itself; orbits are equivalence classes of pairs under the
   automorphism action) — or nothing at the fixpoint where every pair is
   separated.  **[declared metatheory]** A collapsed pair is not an
   active obstruction by itself; this declared policy is what makes it
   one.  The policy reads only profile equality and automorphism
   structure — never token glyphs — supplies no data, and imports no new
   goal kind.  Orbit selection is isomorphism-equivariant; raw least-pair
   selection is not (section 8.2).
10. **External continuation policy**: the supply-and-admission of one
    fresh opaque token when the closure policy is at its fixpoint.
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

### 8.1 Challenge-source decomposition

**[declared metatheory]** After Challenge 3 the challenge source is the
pair of declared policies of section 3.9-3.10: the *pair-separation
closure policy* (one branch per automorphism orbit of collapsed pairs)
plus, at its fixpoint, the *external continuation policy* (fresh supply).
Round 1 of every tree answers the externally imposed Challenge 3
requirement; later separation rounds answer the closure policy.

**[finite computation]** Token-blindness of the closure policy: renaming
every presentation token changes nothing
(`test_closure_policy_is_token_blind`); in the Lean model tokens are
absent by construction.

### 8.2 Quotient-transition soundness (repaired)

**[counterexample]** Raw least-pair selection is not
isomorphism-equivariant.  Regression regime: four data, one unary form,
instances on data 2 and 3; collapsed pairs (0, 1) and (2, 3); renaming by
pi = (2, 3, 0, 1) yields an isomorphic regime
(`canonical(r) = canonical(rename(r, pi))`, verified) in which index pair
(0, 1) is the *marked* collapsed pair rather than the unmarked one — the
two same-index selections produce non-isomorphic children
(`test_least_pair_selection_is_not_equivariant`), so the quotiented
transition depended on the representative labeling.

**[finite computation — finite adversarial evidence only]** The repair:
one challenge branch per automorphism orbit of collapsed pairs, all
non-isomorphic challenge orbits retained (the regression regime has
automorphism group of order 4 and two distinct orbits, both challenged).
Scope, stated honestly: no general transport theorem is claimed — the
transports of candidates, costs, validity, minima, and children under
regime isomorphism are **[unresolved]** as theorems.  What exists is
finite adversarial evidence: for every data bijection of each sample
regime, including the regression regime chosen adversarially against the
old policy, the expansion produces exactly the same set of child
isomorphism classes
(`test_orbit_policy_transition_congruence_exhaustive`), and every merge
edge in every export carries an explicitly verified isomorphism
certificate (section 1).  In the exported runs no reached state had more
than one orbit (`expansions_with_multiple_orbits = 0` in every tree and
baseline), so the regenerated trees, counts, and role reports are
numerically unchanged: the repaired defect was latent within the
explored bounds.

**[theorem]** (`mark_progress`) Response existence: on any well-formed
regime whose imposed requirements are all separated, every *supplied*
separation demand has a valid response (one fresh unary form plus one
mark), which moreover preserves every existing separation.  This theorem
is exactly response existence — it does **not** prove autonomous demand
generation, and it does **not** prove an unbounded tower.  Its observed
consequence: no `terminal_no_response` node occurs in any exported run.

### 8.3 Pruning lemmas for the cost-2 enumeration

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

### 8.4 Branch trees (external continuation policy enabled)

**[finite computation]** (committed summaries `artifacts/tree_*_summary.json` with full normalized DAG exports under `artifacts/full/`; per-branch evidence in
`artifacts/claims.json`, `CL-BRANCH-REPORTS`).  Branches are quotiented:
isomorphic regimes merge into one node (a DAG; a *maximal branch* is a
leaf).  Every node is replay-certified from genesis.

| tree | nodes | edges | max depth | terminal | guard-cut | round-cut | open | every maximal branch terminates |
|---|---|---|---|---|---|---|---|---|
| L mu1 | 1205 | 1250 | 7 | 0 | 927 | 0 | 0 | no |
| L mu2 | 963 | 1022 | 15 | 0 | 0 | 568 | 0 | no |
| F mu1 | 1201 | 1244 | 6 | 0 | 886 | 0 | 0 | no |
| F mu2 | 1847 | 1960 | 15 | 0 | 0 | 885 | 0 | no |

* The mu2 trees have **no guard cutoff**: the full isomorphism-quotient
  tree to the requested 15 rounds is finite and fully enumerated
  (963 / 1847 nodes).  Their leaves are round-cut, not terminal: the runs
  were stopped at the requested depth.  **[finite computation]** Reaching
  a finite requested depth is exactly that — *not* a proof of
  unboundedness, and no unboundedness claim is made
  (`CL-REACHES-REQUESTED-DEPTH-WITH-EXTERNAL-SUPPLY`).
* The mu1 trees hit the declared 1200-node pre-expansion guard at depths 7 / 6; the
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

### 8.5 Closed-system baseline (external policy disabled)

**[finite computation]** (`artifacts/closed_*_summary.json` and
`artifacts/full/closed_*.json.gz`, `CL-CLOSURE-TERMINATION`):

| baseline | nodes | terminal branches | guard-cut | round-cut | open | rounds used | pair bound | every maximal branch terminates |
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
zero guard-cut, round-cut, and open branches — the flag
`every_maximal_branch_terminates` is computed over *all* maximal
branches, never from the existence of one terminal node).

## 9. The continuation obligation

*Can the admitted structure generate its next unresolved requirement
without inspecting presentation-token glyphs, supplying a fresh external
datum, importing a new external goal, or assuming the desired
continuation?*

**Result: no object-language endogenous demand generator was derived.**
A collapsed pair, by itself, is not an active obstruction: nothing in the
object language demands its separation.  What exists is the *declared
pair-separation closure policy* (section 3.9) — declared metatheory that
reissues the externally admitted requirement pattern on collapsed pairs.
Under that declared policy, the fixed finite datum set reaches an
all-pairs-separated fixpoint: **pair-separation closure terminates.**

1. **[declared metatheory]** The policy reads only the admitted structure
   and automorphism-orbit structure, issues one requirement per orbit,
   and reissues only the requirement pattern already admitted in `reqs`
   (no new goal kind).  Its selection among conceivable policies is a
   declared-metatheory judgment, not a proved universal property
   (section 10, question 10).
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
   `closure_challenge_orbits` in `code/derivation/engine.py`;
   deterministic and isomorphism-equivariant (section 8.2); the
   closed-system trees of section 8.5 are its full quotient towers.
5. **Comparison with the external-supply tree** — **[finite computation]**
   (`CL-CLOSURE-VS-EXTERNAL`): closed system L/F: 4 / 20 nodes, all
   maximal branches terminal at rounds <= 1 / 3; external policy: 963-1847
   node quotient trees at the requested 15 rounds (mu2, no guard cutoff)
   and 1200-node guard frontiers (mu1).
6. **Beyond the fixpoint** — **[theorem]** at the fixpoint every pair of
   admitted data is separated, so no unresolved requirement exists in the
   admitted requirement language (all n(n-1)/2 pairs are exhausted —
   `allPairs_length`); generating any further requirement would need a
   fresh datum (external supply) or a new requirement kind (external
   goal).  **Pair-separation closure terminates.**  Further continuation
   requires the declared external continuation policy.

A proved finite termination of pair-separation closure is the result; no
longer or infinite tower is forced.

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
   without it pair-separation closure terminates within n(n-1)/2 rounds
   (sections 8.5, 9); with it the process reached every requested depth
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
   in the observed runs (section 8.4).
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
  indistinguishable: admission need not increase expressive power
  (counterexample to the necessity claim).
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
* (f) **[bounded theorem]** No object-language endogenous demand
  generator was derived; under the declared pair-separation closure
  policy (token-blind, isomorphism-equivariant) the fixed finite datum
  set provably reaches the all-pairs-separated fixpoint within n(n-1)/2
  rounds — pair-separation closure terminates (closed-system baselines:
  1 and 3 rounds, every maximal branch terminal).
* (g) **[finite computation]** With the declared external continuation
  policy the process reached the requested 15 rounds; the
  isomorphism-quotient tree at that depth is finite and fully enumerated
  under the refined measure (963 / 1847 nodes) and guard-bounded with exact exported frontiers under the item-count measure.  Continuation
  beyond the exported depths is **[unresolved]**; no unboundedness is
  claimed.
* (h) **[unresolved]** Two admission readings of the challenge text
  survive with no internal fact separating them; both towers are carried
  in full.

## 12. Limitations and open obstructions

* **[declared metatheory]** The cost measures, the candidate grammar, the
  isomorphism relation, the persistence of requirements, the
  pair-separation closure policy (including its orbit-representative
  selection), and the external continuation policy are declared, not
  derived.  Different declarations could yield different towers; the
  mu1/mu2 split documents one such sensitivity precisely.
* **[unresolved]** Four residuals, itemized below rather than left as a
  list, because they are **not the same kind of gap** and a reader
  entitled to know what is unproved is entitled to know in what way.
  An earlier version of this bullet ran them together in one sentence;
  that wording is WITHDRAWN in favour of the register (2026-08-17). No
  status changed at that point — only the resolution at which it is
  reported.

  **R1, R2, R3 and R6 have since been discharged and are struck from
  the register (2026-08-17).**  R1-R3 were one argument, not three: a
  well-formed context always has a hole, so a plugged instance always
  mentions its datum, and a context that reaches outside the regime
  fails derivability on BOTH sides of the iff and therefore separates
  nothing.  `lean4/Derivation/Mention.lean` proves
  `collapsed_append_unmentioning` (R3) with `collapsed_fresh_datum` (R1)
  and `collapsed_fresh_form` (R2) as corollaries; the hypotheses of the
  latter two are conjuncts of `Regime.wf` rather than new assumptions.

  What that does NOT do is promote `CL-PRUNE-STRUCTURAL` to a theorem.
  Its three irrelevance inputs are now proved; the enclosing claim that
  the pruned enumeration contains every minimum still quantifies over
  the declared grammar slice and stays a **[bounded theorem]** on
  computational evidence.  Three inputs became theorems; the enumeration
  did not.

  On R6: It read "count-invariance transport under regime
  isomorphism", kind (a), needing "a Lean transport proof". That proof
  now exists: `collapsed_rename` in `lean4/Derivation/CountTransport.lean`
  proves that observational collapse transports under a renaming of the
  datum indices, and `collapsedCount_rename` carries it to the count.
  `CL-COUNT-INVARIANCE` is reclassified from **[finite computation]** to
  **[theorem]**. The count is now eight-minus-one, not eight, and the
  numbering of the surviving rows is left unchanged so that a reader
  comparing revisions can see exactly which row left.

  Five kinds appear: **(a)** exhaustively certified in Python, Lean
  absent; **(b)** partial Lean, with the bridge to the used form
  computational; **(c)** proved for one reading, bounded for the other;
  **(d)** a genuine unknown with no evidence either way; **(e)** a gap in
  the audit rather than in the mathematics.

  | # | Residual | Kind | Evidence that exists | What closing it needs |
  |---|---|---|---|---|
  | ~~R1~~ | DISCHARGED 2026-08-17 — Unreferenced fresh **data** never affect a minimum response | a | `test_pruned_cost2_contains_every_valid_full_delta`, cross-checked against the *unpruned* space over bare, marked, and structurally mixed base regimes; `collapsed_fresh_datum` (Lean) | nothing; closed |
  | ~~R2~~ | DISCHARGED 2026-08-17 — Unreferenced fresh **forms** never affect a minimum response | a | same test, same cross-check; `collapsed_fresh_form` (Lean) | nothing; closed |
  | ~~R3~~ | DISCHARGED 2026-08-17 — **Mention lemma**: an instance-only delta changes the target pair's profiles only if some instance mentions a target datum | a | same test; `collapsed_append_unmentioning` (Lean) | nothing; closed |
  | R4 | **Delta-level rule-removal bridge** | b | `separable_of_subrules` is **proved** — witness transfer under a shrunken final rule set. The step from delta *items* to shrunken rule sets is computational only | a Lean theorem over delta items, not final rule sets |
  | R5 | **Grammar-wide mu2 uniqueness for reading F** | c | `mu2_unique` is proved grammar-wide for reading **L**; reading F is a **[bounded theorem]** from engine enumeration within the declared bounds | the reading-F analogue of `mu2_unique` |
  | ~~R6~~ | **Count-invariance** transport under regime isomorphism — **DISCHARGED 2026-08-17** | — | `collapsed_rename`, `collapsedCount_rename` (Lean); `test_canonical_invariant_under_rename` retained as independent exhaustive evidence | nothing; closed |
  | R7 | **Transition-congruence** transport under regime isomorphism | a | `test_orbit_policy_transition_congruence_exhaustive` over every data bijection of each sample regime, including the adversarial regression `test_least_pair_selection_is_not_equivariant` | a Lean transport proof |
  | R8 | Counting-law **hypotheses** connected to the transition system | b | `strict_bounded_length`, `no_supply_round_bound`, `allPairs_length` are proved as *conditional abstract* laws; that each accepted round imposes exactly one new requirement over a fixed datum count is discharged computationally, for the exported runs only | a Lean theorem discharging the hypotheses for the transition system itself |

  **R7 is the remaining kind (a): the evidence is not missing, the Lean
  is.** Each is certified by exhaustive computation over a declared
  finite space, and each is reported as **[finite computation]** where
  the paper uses it — never as a theorem. R4 and R8 are kind (b): a
  weaker statement is genuinely proved and the bridge to the form
  actually used is computational. R5 is kind (c) and is asymmetric by
  reading, which is stated wherever it is cited.

* **[unresolved — kind (d), a genuine unknown]** The behavior of the
  external continuation policy beyond the exported depths. Unlike
  R1–R8 this is not a missing formalization of something already
  computed: no evidence exists in either direction, and **no claim is
  made**. Reaching every requested depth tried is exactly that, and is
  not a proof of unboundedness (`CL-REACHES-REQUESTED-DEPTH-WITH-
  EXTERNAL-SUPPLY`).
* **[bounded theorem]** All tree-level results are relative to the
  declared bounds (items <= 2, arity <= 2 concrete, 15 rounds, node guards); the exact frontiers are exported for continuation.  The
  multi-orbit statistic is 0 within these bounds; beyond them, states
  with several challenge orbits are possible (the regression regime is
  one), and the equivariant policy is what keeps the quotient transition
  well defined there.
* **[unresolved]** The admission-reading underdetermination (L vs F) is a
  fact about the challenge text, not about the object language; it cannot
  be internally resolved.
* Gate status, **measured on 2026-08-16** rather than quoted from an
  earlier freeze: 435 tests passing; line coverage 99.10%, branch
  coverage 96.73% (independent gates at 95% each, enforced locally and in
  CI); `lake build` clean across 56 sources.  Axiom status, exactly: no
  `sorry`, no `admit`, no custom conclusion-producing axioms, no
  `unsafe`, no `partial`; the standard Lean-core dependencies `propext`
  and `Quot.sound` remain, per-theorem in `artifacts/lean_axioms.txt`
  (1314 exported reports, of which 413 are axiom-free), audited
  mechanically in CI.  An earlier version of this bullet reported the
  status "at freeze" as "82 tests passing", "line coverage 99.77%, branch
  coverage 98.75%" and "51 exported reports".  Those figures were true of
  an earlier state and were not updated as the development continued;
  they are WITHDRAWN in favour of the measured values above.  A receipt
  that is not re-measured is a claim about the past wearing the tense of
  the present.

  **Re-measured 2026-08-17 and unchanged**: 435 tests, line 99.10%,
  branch 96.73%, 56 Lean sources, 1314 axiom reports within {propext,
  Quot.sound}.  Captured output in `verification_20260817.md`.  Two
  independent measurements a day apart agreeing is a stronger receipt
  than one, and it is recorded here so that the next reader does not
  have to take a single reading on trust.  It remains a receipt: it says
  what the commands printed, not that the mathematics is right.

  **Superseded the same day by the R6 work**: adding
  `lean4/Derivation/CountTransport.lean` moves the Lean figures to 57
  sources and 1322 axiom reports, still entirely within {propext,
  Quot.sound}.  The Python figures are unchanged, because the residual
  it discharges was one whose Python evidence already existed.  The
  1314/56 reading above is left standing rather than overwritten: it was
  true when taken, and a receipt that is silently edited to match a later
  state is no longer a receipt.
* **[open obstruction — metatheoretic; kind (e), a gap in the audit
  rather than in the mathematics]** Elaboration is not auditing.
  Every module under `lean4/Derivation/` is elaborated by CI against a
  pinned census, but a module the root does not import contributes no
  `#print axioms` report, so the axiom whitelist never inspects it.
  "Axiom-clean" is therefore a claim about the 1314 enumerated reports,
  not about every declaration in the tree.  Closing this needs a
  compiler-emitted declaration census; the obvious regex approach is the
  one already known to fail here — a docstring line beginning with the
  word `theorem` defeated a grep count twice — so it is left OPEN rather
  than closed badly.

## 13. Post-hoc comparison

Withheld in full, per the caller's blind-protocol correction of
2026-08-11 (`paper_change_log.md`, entry 4).  No external theory,
architecture, or terminology is named anywhere in this repository outside
the read-only seed prompt.
