# Magnification: the engine as a relation, restart at any state, and what a difference carries

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.

**Result.**  The sealed engine's process is now a relation over the sealed
definitions (`EngineClass`), and the six exported towers are certified
against it edge by edge: every node's status is re-derived from the engine's
own decision order, every expanded node's fan is exactly one edge per orbit
demand and per minimum class with a supply edge exactly when quiet, all 4546
exported rounds are minima landing on their class representatives, and
below each export's completeness depth every fire-maximal history reaches an
exported node up to isomorphism (`evidence/census.json`, zero failures over
5240 nodes and 5498 edges).  On that basis the two questions after it have
exact answers.  **Restart at any known difference is exact at the level of
the class**: a path through a state splits into a path to it and a path
from it, the cut is determined by the record, and the class from any reached
state is the continuation of the rooted class (`Restart.path_append_iff`,
`path_cut_unique`, `rooted_restart`) — provided the whole state travels.
The relation is invariant under the sealed renaming action
(`fire_rename`), so the solver depends only on the isomorphism class of the
state; two-step equivariance holds on all 823 exported nodes whose
neighbourhood is expanded, and restarts from single nodes reproduce the
exported classes layer by layer.  **A primitive difference as such restarts
the genesis, and it restarts the same genesis every time**: every setting
magnifies to the seed `⟨2, [], [], [], [(0, 1)]⟩` (`Magnification.induced_constant`),
so the solver at a bare difference is the original derivation up to
isomorphism — one tower, not many.  **A tree of copies of itself is not
what the current repository is, and the reason is exact**: the seed's three
first-round classes are valid responses at every collapsed pair of every
`Good` state (`bare_round_embeds`, generalizing the sealed `mark_progress`),
so the seed's rounds embed everywhere — but they are the *minimum* at only
157 of the 4282 exported creation rounds, because an existing form makes a
one-item response cheaper at 4119 of them (`context_changes_minimum`, the
Lean countermodel, and the census).  The declared measures read the context,
so the tree at a difference inside a state is not the tree at the bare
difference.  What is the same at every magnification is the relation; what
differs is its minima.  A magnification-invariant solver would need a cost
blind to existing forms or a candidate space restricted to fresh ones —
declared extensions, not consequences of the inscription.

Lean: 63 authored theorems, 77 reports with the compiler-generated ones, all
within `{propext, Quot.sound}`, in a package importing the sealed package and
the merged `local_reuse` package.  Python: the census over all six sealed
exports through the sealed kernel, 32 tests, strict typing, byte-identical
record.  Execution base `60c2cb05d91cdfa099017c9cd205b52564db884b` (main);
no sealed path is written.

## 1. Bridge one: the engine's class as a relation

`lean/EngineClass.lean` states the engine over the sealed `Regime`,
`collapsed`, `validResponse`, `respond` and `TransStep`, selecting no
representative:

| definition | content |
|---|---|
| `InBounds`, `cost`, `IsMin` | the declared candidate space (two items, arity two); both declared measures as one lexicographic cost; a minimum valid response inside the bounds |
| `isMin_no_rule` | a minimum under either measure carries no rule item (from the sealed `rule_item_never_minimal`) |
| `Fire m r i j δ t` | a collapsed pair answered by a minimum: the sealed `TransStep` plus minimality (`fire_transStep`) |
| `relab`, `IsAuto`, `OrbitRep` | the relabelling `iso.py::rename` performs; an automorphism is a datum and form bijection whose relabelling is the regime up to list order (the sealed `RegimeExt`); the engine's demand is a collapsed pair least in its automorphism orbit |
| `EngineFire`, `EngineStep`, `Path`, `Rooted` | a firing on an orbit demand; fire, or grow when quiet with supply on; the recorded path; the seed round on the declared target followed by engine steps |
| `Good`, `good_rooted` | well-formed, rule-free, every standing requirement separated — preserved along every path |
| `fire_replays`, `path_replays`, `rooted_replays` | every step and every path decodes to a sealed event block replaying to its endpoint (`LocalReuse.round_replays`, `replayE_suffix`) |

**The exported towers against the relation** (`magnification.py`,
`evidence/census.json`).  For each export: the sealed certification; the
regime of every node replayed from genesis and hash-checked; every node's
status re-derived by replaying the engine's decision order (targets, the
round bound, the node guard at the count of nodes created before it, supply);
at every expanded node the exported fan compared with the fan the relation
demands — one edge per orbit demand and per minimum class, with the recorded
tie count, class size, cost and orbit count, the child being the class
representative, and a supply edge exactly when no demand stands; and the
completeness depth: the first depth carrying a `completed` or
`frontier_guard` node, below which every fire-maximal history reaches an
exported node up to isomorphism.

| export | nodes | edges | fans | rounds re-derived | supplies | completeness depth |
|---|---|---|---|---|---|---|
| `closed_L` | 4 | 3 | 1 | 3 of 3 | 0 | 1 (all separated) |
| `closed_F` | 20 | 19 | 4 | 19 of 19 | 0 | 3 (all separated) |
| `tree_L_mu1` | 1205 | 1250 | 83 | 1055 of 1055 | 195 | 6 (node guard) |
| `tree_L_mu2` | 963 | 1022 | 284 | 911 of 911 | 111 | 15 (round bound) |
| `tree_F_mu1` | 1201 | 1244 | 82 | 1011 of 1011 | 233 | 5 (node guard) |
| `tree_F_mu2` | 1847 | 1960 | 549 | 1547 of 1547 | 413 | 15 (round bound) |

The orbit demands are re-derived a second way, independent of the sealed
colouring: automorphisms by brute force over every datum and form bijection
pair on all 2461 nodes with at most five data and three forms, and the least
member per orbit.  No disagreement.  The automorphism-count histogram is
almost all trivial groups, with groups of 2, 6 and 24 at the symmetric
states.  The two seed rounds: on reading L the seed target `(0, 1)` is the
orbit demand of the root (`orbitRep_rootL_01`); on reading F the seed target
`(1, 2)` is not — the transposition of the first two data fixes the root and
carries it to `(0, 2)` (`not_orbitRep_rootF_12`, computed as
`F_seed_is_orbit_representative: false`).  The F tower's first round is the
declared seed round; every later round is an orbit step.

## 2. Bridge two: restart at any state

`lean/Restart.lean`:

* `path_append`, `path_split`, `path_append_iff` — a path along a
  concatenated record is a path to some cut state followed by a path from
  it; `path_cut_unique` — the cut is determined by the record.
* `rooted_restart` — a rooted state restarted with any engine path is
  rooted; `rooted_iff_path` — the rooted class is the seed round followed by
  a path.  The sealed `replayE_suffix` gives the event-level form.
* `fire_rename` — a datum renaming carries every firing onto a firing of the
  renamed regime with the same cost, the renamed response and the renamed
  successor (minimality transports because validity does,
  `validResponse_rename`, and the cost is renaming-invariant); `fire_auto` —
  at a datum automorphism the family at the image pair is the renamed
  family.  The least-pair *selection* is not congruent (sealed
  `least_pair_selection_not_congruent`); the relation is.

Computed: for every exported node whose children are all expanded, the
classes two engine steps away, recomputed from the node's regime alone,
equal the classes two edges away in the exported DAG, where a merge edge
lands on the isomorphism representative and continues from it — 823 nodes,
no failure.  Restarting the class at nodes 1, 2 and 3 of `tree_L_mu2` with
their complete regimes reproduces the exported classes at every layer to
depth four.  The conditions are the ones `local_reuse` recorded: the whole
state travels (a bare difference does not), the restarted root uses its own
orbit demands (not a seed target), and names stay fresh.

## 3. Bridge three: magnification

`lean/Magnification.lean`:

* `induced` — the regime a primitive difference (`PrimitiveCore.Setting`)
  induces on the sealed carrier: two data and the demand to separate them.
  `induced_constant`: it is the same for every setting; `induced_eq_R2L`: it
  is the reading-L root.  The setting's relation, retention, protection and
  operation family have no translation into the sealed grammar and are not
  read.
* `fresh_form_valid` — at any pair of distinct admitted data of any
  well-formed regime whose requirements are separated, a fresh form with one
  instance mentioning the first datum is a valid response, for every arity
  and argument list inside the carrier; `bare_round_embeds` — the seed's
  unary mark, binary link and binary self-loop are valid at every difference
  in every `Good` state.
* `context_changes_minimum` — at the bare difference no response of at most
  one item is valid (sealed `cost1_insufficient`), while at the same
  difference inside `ctxRegime = ⟨3, [1], [(0, [0])], [], []⟩` the one-item
  response marking datum 2 with the existing form is the minimum (`ctx_min1`);
  `bare_mark_not_min_in_context` — the seed's mark stays valid there and is
  not a minimum.

Computed, over all 4282 exported creation rounds: the seed's three responses
are valid at every one; the exported minimum is one item at 4119 of them and
a seed response is among the minima at 157.  Per export: `closed_L` 0 of 3
cheaper, `closed_F` 9 of 19, `tree_L_mu1` 1001 of 1009, `tree_L_mu2` 800 of
851, `tree_F_mu1` 957 of 967, `tree_F_mu2` 1352 of 1433.

## 4. The answer to the question

**Can genesis be restarted at any known primitive difference?**

* At any *state* the process reaches: yes, exactly, at the level of the
  class (`rooted_restart`, `path_append_iff`), and the class depends only on
  the isomorphism type of the state (`fire_rename`); the exported quotient
  agrees on every node checked.  The state must travel whole: data count,
  forms, instances and standing requirements.
* At a *primitive difference as such*: yes, and it is always the same
  restart — every setting magnifies to the seed (`induced_constant`), so
  the solver at a bare difference is the original derivation up to
  isomorphism.  A setting carrying admitted operations or a relation richer
  than one witnessed pair has no translation into the sealed grammar; its
  restart needs a declared translation (OPEN, not impossible).

**Is the repository therefore a solver at any level of magnification, a tree
solver of multiple versions of itself from one chosen difference?**  The
relation is the same at every magnification and restarts anywhere; the
minima are not.  The seed's tree embeds at every difference as valid
continuations (`bare_round_embeds`), but the sealed measures read the whole
regime: an existing form makes a one-item response the minimum at 96 % of
the exported rounds, so the sub-tree at a difference inside a state is not a
copy of the seed's tree (`context_changes_minimum`).  This is not a defect
and not an impossibility of self-similarity in every calculus: it is the
exact consequence of two current properties — the candidate space offers
instances on existing forms, and both declared costs count them as one
item.  A magnification-invariant tree would require a cost blind to
existing forms or a candidate space restricted to fresh forms, each a
declared extension whose consequences are not established here.

## 5. Evidence

**Lean** (`lean/`, `evidence/lean.json`): 63 authored theorems and 14
compiler-generated ones, 77 reports — 34 `[propext, Quot.sound]`, 28
`[propext]`, 15 axiom-free; `EngineClass` 34, `Restart` 22, `Magnification`
21; the report population equals the environment census of the three
namespaces in both directions; no private theorem; forbidden-token scan
clean.  The well-formedness lemmas of `EngineClass` section 1 duplicate those
of the ignition family (PR #147) pending its merge, and say so.

**Python** (`magnification.py`, `run.py`, `evidence/census.json`, `tests/`):
32 tests, strict typing over nine files, the record replays byte-identically.

**Negative cases** (`tests/test_magnification.py`), one per check: a
dropped tie edge → `minimum classes have no edge`; a non-minimum response on
an edge → `response is not a minimum class`; a wrong status → `status
'completed', the engine's order gives 'expanded'`; a flipped regime hash →
the sealed certification refuses the export; a rewired grandchild → `two-step
classes differ`; the least-pair policy on the sealed regression regime keeps
one of two orbits while the orbit policy keeps both.  Positive controls: the
seed target of reading L is the orbit demand of its root; the context
countermodel executes as the Lean statement says (cost 1, the mark valid but
absent from the minima, cost 2 at the seed).

**Injection record** (this family's own gates; each reversed, no receipt
regenerated while live):

| gate | injection | observed failure | reversed |
|---|---|---|---|
| custody export pin | first digit of the pinned `tree_L_mu2.json.gz` digest flipped | `FAIL: BASELINE_ARTIFACT_PIN: artifacts/full/tree_L_mu2.json.gz` | PASS |
| custody census | untracked `ZzzProbe.lean` in `lean4/Derivation` | `FAIL: SOURCE_CENSUS: lean4/Derivation: … unexpected=['lean4/Derivation/ZzzProbe.lean']` | PASS |
| census record | `totals.minima` lowered by one | `FAIL: evidence/census.json differs from fresh computation` | PASS |
| Lean report census | the `#print axioms` line of `fire_rename` removed | `FAIL: report/census mismatch: missing=['Restart.fire_rename'], extra=[]` | PASS |
| Lean forbidden token | the first forbidden token in a comment | `FAIL: forbidden source token: Restart.lean` | PASS |
| Lean record | one report's axioms edited in `evidence/lean.json` | `FAIL: evidence/lean.json differs from fresh compilation` | PASS |

**Custody** (`verify_sources.py`, `SOURCE_MANIFEST.json`): at
`60c2cb05d91cdfa099017c9cd205b52564db884b`, the seven derivation modules by digest and runtime
origin, the sealed `lean4/Derivation` tree and the `research/local_reuse/lean`
tree by Git tree object, both Lean configurations by digest, the six full
exports and their summaries by raw digest; an untracked `.py` on the import
path or `.lean` in either Lean tree is refused.

**Regression gates with this family staged**: (1) prompt hashes ok; (2) transport citations clean, 190 verified; (3) the full sealed suite under coverage, exit 0, line 99.10 %, branch 96.71 % (four workers); (4) mypy clean over 60 files; (5) artifacts reproducible, 40 JSON byte-identical and 6 full exports content-identical; (6) Lean audit clean on a fresh log, 77 sources, 1530 reports within the whitelist, report pin matching; (7) 7 skills well formed; (8) 62 paper cross-references resolve; (9) 1152 ledger evidence tokens resolve; (10) parked audit complete, 75 modules, 12 parked; (11) the four registered research checks pass; (12) prose watchlist clean with no pin regenerated, 49 terms, 130 files, 1826 hits; the identifier firewall passes over the index. Unavailable: hosted CI. Pre-existing failures observed: none.

## Not claimed

* That `closure_challenge_orbits` computes `OrbitRep` for every regime: the
  agreement is brute-forced on 2461 nodes; the sealed colouring's
  refinement of the orbit definition is not proved.
* That the sealed canonical key decides isomorphism: the sealed `IsoCanon`
  residual stands; the census uses the key as the exports do.
* Transport of firings along form bijections: `fire_rename` covers datum
  renamings; form renamings are covered computationally through the key.
* Anything about three-item responses, other measures, or the `World`,
  passage or described-execution carriers.
* A translation of a setting's operations, retention or protection into the
  sealed grammar.

## Files and running

| file | role |
|---|---|
| `lean/EngineClass.lean` | the relation, the invariant, the decoding |
| `lean/Restart.lean` | paths, restart, renaming transport, the roots |
| `lean/Magnification.lean` | the induced seed, the embedding, the context countermodel |
| `lean/Inventory.lean` | the environment census |
| `magnification.py`, `run.py`, `evidence/census.json` | the census over the six exports and its record |
| `verify_lean.py`, `evidence/lean.json` | the Lean build, two-way census and reliance record |
| `verify_sources.py`, `SOURCE_MANIFEST.json` | custody of the consumed inputs |
| `verify.py` | every check in order |
| `tests/` | 32 tests: the census, the negative and positive controls, custody, the parser, the record |
| `CLAIMS.md` | one `CL-MG-*` entry per claim |

```powershell
cd research/magnification
python verify.py     # sources, tests, mypy, lean (lake build + census), census --check
```

Regenerate the two records deliberately and never under a live injection:
`python run.py --write`, `python verify_lean.py --write`.
