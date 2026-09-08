# Magnification: the engine as a relation, restart at any state, and what a difference carries

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.

**Result.** The package defines a relation over the sealed carrier and
checks the six exports at their recorded representatives: 5240 nodes, 5498
edges, 4546 minimum-response rounds and 952 supplies. Each expanded fan has
one edge per computed orbit demand and minimum key, with the actual event
block bound to the response. These are finite computations using the sealed
algorithms; identifying them with the full Lean relation remains conditional
on the unproved orbit and quotient bridges.

The path theorems permit splitting and continuing a recorded path with the
whole state and the same measure and supply policy. `Rooted` starts after
the declared seed round. `fire_rename` transports `Fire` under datum
renamings; it does not establish invariance of `EngineStep` or the solver
under every datum-and-form isomorphism. A two-step check compares freshly
replayed raw successors with the exported DAG on 823 eligible nodes, using
one deterministic raw representative per computed key. Three sampled
restarts agree through four layers. These finite checks do not discharge
the general transport obligation.

`induced` is a declared constant map from settings to `R2L`. It ignores
every field and requires no difference witness. Its equality theorem records
that definition; it does not derive a restart from a primitive difference.
For an existing `Good` state, `bare_round_embeds` proves three fresh-form
responses valid at any distinct admitted pair. It establishes neither an
embedding of whole trees nor preservation of minimum classes.

Context does change minima: the explicit Lean example has a one-item `mu1`
minimum where the bare seed needs two. Of 4282 exported creation rounds,
4119 have one-item minima, 157 have one of the three chosen seed responses
among the minima, and six have two-item minima without such a response.
Those six use two instances on existing forms under `mu2`, with secondary
cost zero. Restrictions to fresh forms or different costs are possible
extensions; their necessity or sufficiency for self-similarity is unproved.

Lean: 63 authored theorems, 77 reports with the compiler-generated ones, all
within `{propext, Quot.sound}`, in a package importing the sealed package and
the merged `local_reuse` package.  Python: the census over all six sealed
exports through the sealed kernel, 38 tests, strict typing, byte-identical
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
`frontier_guard` node, below which no cutoff node appears in the recorded traversal. Completeness
for arbitrary representatives of the Lean relation additionally needs the
unproved orbit-selection and quotient-transport bridges.

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
  family, when the datum renaming fixes the regime by literal equality.
  This is a theorem about `Fire`. The broader `IsAuto` uses datum and form
  bijections with `RegimeExt`; no transport theorem for `EngineStep` under
  that broader relation is supplied.

Computed: on 823 expanded nodes whose children are all expanded, two-step
key sets from freshly replayed children agree with the exported DAG. The
calculation retains one deterministic raw child per key and continues from
that child, without replacing it with the exported representative. This
tests the selected raw representatives, not all isomorphic presentations.  Restarting the class at nodes 1, 2 and 3 of `tree_L_mu2` with
their complete regimes reproduces the exported classes at every layer to
depth four.  The conditions are the ones `local_reuse` recorded: the whole
state travels (a bare difference does not), the restarted root uses its own
orbit demands (not a seed target), and names stay fresh.

## 3. Bridge three: magnification

`lean/Magnification.lean`:

* `induced` — a declared constant function from `PrimitiveCore.Setting`
  to the demanded state `R2L` (distinct from the pre-demand export root).
  It ignores the setting, including its points and relation, and consumes
  no witness. `Setting` itself does not require its points to differ or
  its relation to hold. `induced_constant` is therefore a consequence of
  the chosen definition, not a recovered translation. A faithful translation
  of relations, retention, protection or operations remains OPEN.
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
  not a `mu1` minimum.

Computed, over all 4282 exported creation rounds: the seed's three responses
are valid at every one; the exported minimum is one item at 4119 of them and
a seed response is among the minima at 157.  Per export: `closed_L` 0 of 3
cheaper, `closed_F` 9 of 19, `tree_L_mu1` 1001 of 1009, `tree_L_mu2` 800 of
851, `tree_F_mu1` 957 of 967, `tree_F_mu2` 1352 of 1433. The other six
creation rounds are `tree_F_mu2` edges from parents 815 and 852: two
instances on existing forms cost `(2, 0)`, beating the fresh-form responses
in the second component of `mu2`. The 157 figure concerns exact membership
of the three chosen deltas, not every isomorphic first-round representative.

## 4. The answer to the question

A state reached after the seed round can carry a further path under the
same declared relation, measure and supply policy. The path laws are exact
for their recorded state lists. They supply no next-step selection, liveness,
resource-budget restart theorem, or full isomorphism invariance.

A primitive difference alone is not translated here. The constant `induced`
map chooses the same demanded seed for every setting, including settings
with no witnessed difference. Recovering a setting's structure requires a
separately defined and justified translation.

The three fresh-form response constructions remain valid in context, but
the minimum response family can change. This blocks preservation of that
minimum family in general. No theorem in this package embeds the whole seed
tree in every context or rules out every other definition of self-similarity.

## 5. Evidence

**Lean** (`lean/`, `evidence/lean.json`): 63 authored theorems and 14
compiler-generated ones, 77 reports — 34 `[propext, Quot.sound]`, 28
`[propext]`, 15 axiom-free; `EngineClass` 34, `Restart` 22, `Magnification`
21; the report population equals the environment census of the three
namespaces in both directions; no private theorem; forbidden-token scan
clean.  The well-formedness lemmas of `EngineClass` section 1 duplicate those
of the now-merged ignition family (PR #147). They are retained locally;
this package still imports only the sealed package and `local_reuse`.

**Python** (`magnification.py`, `run.py`, `evidence/census.json`, `tests/`):
38 tests, strict typing over nine files, the record replays byte-identically.

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

**Author-recorded regression gates at the original head `0717d6e2`**: (1) prompt hashes ok; (2) transport citations clean, 190 verified; (3) the full sealed suite under coverage, exit 0, line 99.10 %, branch 96.71 % (four workers); (4) mypy clean over 60 files; (5) artifacts reproducible, 40 JSON byte-identical and 6 full exports content-identical; (6) Lean audit clean on a fresh log, 77 sources, 1530 reports within the whitelist, report pin matching; (7) 7 skills well formed; (8) 62 paper cross-references resolve; (9) 1152 ledger evidence tokens resolve; (10) parked audit complete, 75 modules, 12 parked; (11) the four registered research checks pass; (12) prose watchlist clean with no pin regenerated, 49 terms, 130 files, 1826 hits; the identifier firewall passes over the index. Unavailable: hosted CI. Pre-existing failures observed: none.

## Not claimed

* That `closure_challenge_orbits` computes `OrbitRep` for every regime: the
  agreement is brute-forced on 2461 nodes; the sealed colouring's
  refinement of the orbit definition is not proved.
* That the sealed canonical key decides isomorphism: the sealed `IsoCanon`
  residual stands; the census uses the key as the exports do.
* General transport along form bijections or transport of orbit-selected
  `EngineStep`: `fire_rename` covers datum renamings of `Fire`; key comparisons
  and selected finite restarts do not prove the missing transport laws.
* Anything about three-item responses, other measures, or the `World`,
  passage or described-execution carriers.
* A translation of a setting's operations, retention or protection into the
  sealed grammar.

## Files and running

| file | role |
|---|---|
| `lean/EngineClass.lean` | the relation, the invariant, the decoding |
| `lean/Restart.lean` | paths, restart, renaming transport, the roots |
| `lean/Magnification.lean` | the declared constant seed, valid response constructions, the context countermodel |
| `lean/Inventory.lean` | the environment census |
| `magnification.py`, `run.py`, `evidence/census.json` | the census over the six exports and its record |
| `verify_lean.py`, `evidence/lean.json` | the Lean build, two-way census and reliance record |
| `verify_sources.py`, `SOURCE_MANIFEST.json` | custody of the consumed inputs |
| `verify.py` | every check in order |
| `tests/` | 38 tests: the census, the negative and positive controls, custody, the parser, the record |
| `CLAIMS.md` | one `CL-MG-*` entry per claim |

```powershell
cd research/magnification
python verify.py     # sources, tests, mypy, lean (lake build + census), census --check
```

Regenerate the two records deliberately and never under a live injection:
`python run.py --write`, `python verify_lean.py --write`.

## Review corrections

The original claim that “the solver depends only on the isomorphism class”
overstated datum-only `Fire` transport. General solver transport is OPEN.
The original “primitive difference as such restarts the genesis” described
a constant map as a derivation; that reading is withdrawn. The original
claim that “the seed's tree embeds at every difference” exceeded a theorem
about three valid responses. No whole-tree embedding is established.
The original two-step check reused exported representatives; it now
continues from freshly replayed children. The cutoff depths remain measured
properties of the exported traversal, not a universal completeness theorem.

Four added counterexamples initially passed the census incorrectly:
duplicate class edges, redundant non-minimum deltas with the same endpoint,
unreported response events and missing supply events. The repaired census
rejects each by name, and the unmodified exports remain positive controls.

The receipt command also refuses nonzero census failures, invalid seed responses,
and unequal or incomplete sampled restarts before accepting or writing bytes.
Two additional tests exercise those semantic refusals.
