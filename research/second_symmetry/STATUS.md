# STATUS: rung five -- the automorphisms of a regime along a history

`AuthorityEffect: None`.  Counts in this file are dated 2026-09-25.  A
receipt is not a proof; a pin proves only that a source did not move; a
gate is proved by the defect it fails on, and every injection this rung
ran is recorded in `research/second/MANUAL.md` with its observed failure.

## The question, and where it came from

Rung four's leftover Y-3, quoted verbatim in `CLAIM_LEDGER.md` from a
pinned span: symmetry along a history.  Rung four's own application of
the seed's next-rung rule, pinned as a second span, selects it, because
it extends the census of challenge five -- the rows for symmetry,
invariants and irreversibility -- and because no leftover reduces the
count of declared inputs.

`research/second/PLAN.md` item five assigns "run forward" and the census
to rungs four and five.  As in rungs three and four, this rung follows
the seed's rule, which the plan's item six defers to, and not the list;
the plan is not edited.

## Source policy, declared before the first compile

RECONSTRUCTION, with a pin note per file, as rungs three and four did.
Two reconstruction modules reproduce three pinned sealed sources
verbatim: the sealed kernel slice (`Kernel.lean`, from `Basic.lean` and
`Inertia.lean`) and the sealed isomorphism structure (`IsoKernel.lean`,
from `Minimality.lean` lines 169-224 only; the parked collapse transport
rung four also carried is not needed here and is not reproduced).
`test_reconstruction.py` compares them declaration by declaration with
the pinned blobs AT THE SNAPSHOT: 41 shared declarations, all identical
after comments and namespace lines are stripped and whitespace is
normalized; the omitted declarations are pinned by name.

`Kernel.lean` was produced from rung four's `Kernel.lean` by changing only
the outer namespace; the comparison above is against the SEALED blobs,
not rung four's copy.  `IsoKernel.lean` was assembled from the sealed
span itself.  The Python consumes the sealed kernel, the sealed
isomorphism procedure and rung four's population through their public
functions and copies no source of any of them.  The verifiers, the
coverage gate and four test files are hand copies of rung four's with
this rung's paths, each saying so in its first lines.

## What is proved, what is computed, what is open

**Proved in Lean** (64 theorems in the package, 17 of them
reconstructions; axioms within `{propext, Quot.sound}` for every one --
five with none, twenty-four with `propext` alone, thirty-five with both
-- and no `Classical.choice` anywhere):

- a supply keeps every automorphism, at the level of a definition;
- admitting a datum or a form loses no automorphism: each extends,
  fixing the new index;
- admitting an instance, a uniform rule or a requirement that is new
  keeps EXACTLY the automorphisms that fix the added element, and the
  automorphisms after that are also automorphisms before are exactly
  those that fix it too -- for every regime, with no decidability
  hypothesis, the descent side assuming the regime before well-formed;
- each of those three kinds loses an automorphism at some regime and
  gains one at some regime, by six exhibited witnesses of at most three
  data and two forms of arity one;
- every event keeps the regime or raises its element count by exactly
  one, so the count of the regime a history reaches is its base's count
  plus the number of the history's changing events, and no history
  returns to a regime it left.

**Computed** over rung three's rectangle -- three bases, 18798
sequences, 18795 edges, 2316 distinct regimes:

- the sealed automorphism SET equals a brute-force set at every regime,
  and its size rung four's brute-force count; sizes run from one to two
  hundred and forty;
- the size moves at the three adding kinds in both directions, and at a
  datum or a form only upward: counts by kind in `CLAIM_LEDGER.md`
  SYM-16;
- the datum law (times one more than the untouched data) and the form
  law (times one more than the untouched forms of that arity) hold on
  every datum and form edge; the fixer law and its numeric form (size
  over the count of images, kept) hold on every one of 12300 changing
  adding edges;
- the largest rise at one edge is five, at datum edges only; the
  largest fall is twenty-four, at instance edges only;
- sequences by the sizes along them: constant, rising, falling and mixed
  all occur at L and F, falling never at EMPTY, and the shortest mixed
  sequence has two events;
- no sequence returns, by a changing event, to a class an earlier prefix
  reached.

**Open, named and priced** (Z-1 to Z-5 below, rung four's Y-1, Y-2 and
Y-4, and rung three's X-1, X-2, X-4, X-5 and X-6 carried, less the three
rows this rung decides).

## The frozen predictions, scored

Nine computational rows, scored mechanically by `run_symmetry.py` and
recorded in `receipts/symmetry.json`:

| row | value | verdict |
|---|---|---|
| K-10 | 577, 3928, 14293 sequences; 18795 edges; 0 replay, set and count mismatches | HIT |
| K-11 | no unchanging or supply edge moves; no datum or form edge lowers; each adding kind both ways | HIT |
| K-12 | datum law 0 of 1346, form law 0 of 2200 violated | HIT |
| K-13 | fixer law 0 set and 0 numeric violations of 12300 | HIT |
| K-14 | largest rise 5 at datum edges; largest fall **24** at instance edges (predicted 20) | **MISSED** |
| K-15 | all four classes at L and F; no falling at EMPTY; shortest mixed 2 | HIT |
| K-16 | 0 element-count violations; 0 class revisits | HIT |
| K-17 | smallest 1, largest 240 | HIT |

**The miss, K-14, recorded next to its value and not edited.**  The
prediction said the largest fall at one edge is twenty, reasoning from an
instance of arity two on two of five untouched data under one form: its
images number twenty.  The largest is twenty-four, from F: admit a datum,
two forms of arity two, then an instance of the first on two of the four
data.  Before it, both forms are untouched and interchangeable, so the
images of the instance range over two forms as well as twelve ordered
pairs of data.  The prediction counted the data bijection and left out the
form bijection.  Every edge attaining twenty-four is an instance edge, as
predicted.

Eleven rows are scored where their evidence lives and are marked so in
the receipt rather than omitted: K-1, K-2, K-4, K-5, K-6, K-7 and K-8 by
the statement-shape tests of `test_census.py` and by `verify_lean.py`;
K-3 by `FWDEF_CENSUS.json`; K-9 by the committed axiom log; K-18 and K-19
by `CLAIM_LEDGER.md` and `test_census.py`; K-20 by `run_symmetry.py
--check`, `test_symmetry.py` and the measured time below.  Each is met.

### The census prediction, and its eight misses

`PREDICTIONS.md` named 35 Lean targets and a class for each, frozen
before the compile.  All 35 exist.  Scored mechanically by
`test_census.py`: **27 hits, 8 misses**, and **12 further native
theorems** were written that the frozen list did not name (two list
lemmas, two instance round trips, the requirement round trip, four
lemmas on extending a map past a range, a list-append lemma, the
insertion lemma, and one replay unfolding).

Every one of the eight misses is a DEMOTION:

| target | predicted | recorded | why |
|---|---|---|---|
| `inst_fixed_of_survives` | CONTENT | THIN | one membership case, the other closed by the unpredicted round trip `inst_back` |
| `inst_survives_of_fixed` | CONTENT | THIN | the structure rebuilt field for field, two membership cases, the inverse from `inst_back` |
| `req_fixed_of_survives` | CONTENT | THIN | the same shape, the round trip from `sortPair_round` |
| `req_survives_of_fixed` | CONTENT | THIN | the same shape |
| `inst_meet` | THIN | DEFINITION | the two neighbours assembled into an equivalence |
| `rule_meet` | THIN | DEFINITION | the same |
| `req_meet` | THIN | DEFINITION | the same |
| `kinds_move_both_ways` | THIN | DEFINITION | six neighbours assembled into a conjunction; listed as the one long-but-definitional exception |

**What the misses say.**  The content of this rung sits in six theorems:
the three descents (`inst_descends_of_fixed`, `rule_descends_of_fixed`,
`req_descends_of_fixed`), which carry an admitted element back inside the
ranges and so need the regime before well-formed; the two lifts
(`datum_lift`, `form_lift`), which extend every map past a range; and
`size_counts_changes`.  Once the round trips of an image were proved as
lemmas, the surviving direction for instances and requirements was one
case split, as it already was for rules.

## Found live, before any injection

**Nothing reached `Classical.choice`.**  Rung four found two `simp` calls
pulling it in; this package was written with `rw`, `if_pos`, `if_neg`
and `omega`, and a probe of the headline theorems before the first audit
showed `propext` and `Quot.sound` only.  Recorded because the absence is a
measured one, not assumed.

**A forged edge is the only way to see a law fire.**  Over the rectangle
every law reports zero violations, which alone would not show that the
check can fail.  `test_symmetry.py` feeds each law a forged edge -- a
datum edge whose regime after carries an extra instance, a form edge
likewise, an instance edge whose regime after was reached by a datum --
and each counts its violation; a forged population returning to a class
and failing replay, and a tampered automorphism procedure, are counted
too.

## Leftovers, named and priced, executed nowhere

- **Z-1, the element count across the isomorphism.**  Whether two
  regimes the sealed isomorphism relates have one element count.  It
  would carry `no_return` from regimes to classes beyond the rectangle,
  deciding irreversibility up to the isomorphism and the census row for
  recurrence, which asks for an isomorphic state revisited.  Obstacle
  recorded: the Lean regime keeps its collections as lists and
  `Regime.wf` does not forbid a repeated entry, so the count is an
  invariant only of duplicate-free regimes; every regime reached from the
  empty one by the sealed step is duplicate-free, which is itself to be
  proved.  Price: moderate -- a counting argument on the two
  half-bijections in core Lean, plus the duplicate-free invariant.
- **Z-2, the numeric fixer law in Lean.**  The size before over the
  count of images before equals the same after.  Needs a finite
  enumeration of the automorphisms of a regime in Lean.  Price: large.
- **Z-3, the datum and form multiplication laws in Lean.**  The same
  obstacle as Z-2.  Price: large.
- **Z-4, succession through the element count.**  `size_counts_changes`
  reads the number of CHANGING rounds off a regime and its base; whether
  that decides the census row for succession of accepted rounds -- which
  rounds are accepted, and whether the base must be named -- is not
  claimed here.  Price: small; the theorem is in place.
- **Z-5, automorphisms along a generated run.**  Everything here is over
  histories of the sealed step, not over a run an engine generates.
  Waits on X-5.  Price: a rung, after X-5.
- Carried from rung four, unchanged: Y-1 (the shortest class-matched
  witnesses), Y-2 (necessity of uniformity), Y-4 (the converse of the
  checks at arity one).
- Carried from rung three, unchanged: X-1 (a decision for a demand at a
  regime), X-2 (the first count under a generated run), X-4 (the safety
  of rung three's omitted declarations), X-5 (the engine of the seed's
  challenge three), and X-6 less symmetry, invariants and
  irreversibility: two-ness, observational classes, duration, adjacency,
  reach, branching, exhaustion and recurrence.

## Gates and timing

Measured on this machine, 2026-09-25, serially, one run each, by a
Python timer around each command:

| gate | command | measured |
|---|---|---|
| pins, spans, frozen texts | `python research/second_symmetry/verify_pins.py` | 2.3 s |
| tests under coverage (137 tests) | `python -m coverage run -m unittest discover -s . -p "test_*.py"` | 65.9 s |
| coverage gate | `python -m coverage erase`, then after the tests `python -m coverage json -q; python check_coverage.py` | 0.6 s |
| receipt comparison | `python run_symmetry.py --check` | 1.2 s |
| strict typing | `python -m mypy` | 0.5 s, warm cache |
| clean Lean build and axiom audit | `python verify_lean.py` | 29.5 s |

Grouped measured time **100.0 seconds**, inside the fifteen-minute
per-rung ceiling the seed sets.  The mypy row was measured with a warm
cache and a cold run is longer; the ceiling is what the number is for.
The Lean row is a CLEAN build: `lake clean`, a full rebuild, then the
compiled-environment census.  Coverage over the declared measured set
(`symmetry.py`, `run_symmetry.py`, `verify_pins.py`): **line 99.29%,
branch 97.22%**, both above the 95% floor.

These are local receipts.  Hosted CI is permanently disabled by author
decision; the workflow is the written contract and its steps are run
here, each command directly from its working directory, in the order the
contract lists them.  `python ci/run_gates.py --list` enumerates the four
registered steps of this rung, three in the research job and one in the
lean job.

## Terminal scope

- `SURVIVAL_AT_EACH_KIND` -- PROVED_THEOREM, every regime, all six kinds.
- `FIXERS_ARE_THE_COMMON_AUTOMORPHISMS` -- PROVED_THEOREM, the three adding kinds, both sides.
- `ADDING_KINDS_MOVE_BOTH_WAYS` -- COUNTERMODEL, six witnesses.
- `ELEMENT_COUNT_COUNTS_CHANGES` -- PROVED_THEOREM, every history of the sealed step.
- `NO_RETURN_TO_A_REGIME` -- PROVED_THEOREM, every history.
- `NO_RETURN_TO_A_CLASS` -- FINITE_COMPUTATION in the rectangle; OPEN beyond (Z-1).
- `SIZES_ALONG_HISTORIES` -- FINITE_COMPUTATION, the frozen rectangle only.
- `CENSUS_SYMMETRY_INVARIANT_IRREVERSIBILITY` -- three rows decided, each conditional on an engine for FORCED.
- `INPUT_COUNT_UNCHANGED` -- RECORDED, value two, no proof of a floor, no reduction.
- `OBSTRUCTIONS_UNTOUCHED` -- RECORDED.

```yaml
steps_completed: [Reconstruct, Survival, Growth, Witnesses, Rectangle, Census, Register]
write_root: research/second_symmetry/
snapshot: 630622da034a17113b7bce0c34f2d9d122ea25f1
sealed_paths_touched: []
shared_files_touched:
  - .github/workflows/verify.yml (append only)
  - .claude/skills/gates/SKILL.md (append only, by the author's ruling of 2026-09-25)
  - research/second/MANUAL.md (append only)
  - research/README.md (generated view)
  - docs/index/pins.md (generated view)
  - docs/lean_build_order.md (generated view)
  - ci/tree_custody_pin.json (generated view)
census_pin_regenerated: false
prompt_sha256: 7b3f73c0af7b1e5ed61bb5cb48da6e079eccf310b4b7b76c67538ddc69e6bbb9
predictions_sha256: bcedea00300218386e0ca9df39d476482319234521131f67267d1f699f858ae9
bases: [EMPTY, L, F]
sequences: {EMPTY: 577, L: 3928, F: 14293}
edges: 18795
regimes: {distinct: 2316}
lean_theorems: {total: 64, reconstruction: 17, content: 6, thin: 27, definition: 14}
predictions_scored: {hit: 8, missed: 1, elsewhere: 12}
census_prediction_scored: {named: 35, hit: 27, missed: 8, unpredicted_native: 12}
input_count: {value: 2, proof: none, sentence: "This rung neither reduces the count of declared inputs nor proves it at a floor."}
census_rows_decided: [symmetry, invariant, irreversibility]
authority_effect: None
final_state: true
```

## The next rung, named so it cannot be smuggled in later

The seed's rule takes the smallest named leftover that EITHER reduces the
count of declared inputs OR extends the census of challenge five, and on
a tie the one named first.  Applied to this rung's leftovers and the ones
carried:

| leftover | reduces the input count | extends the census | price | eligible |
|---|---|---|---|---|
| Z-1 element count across the isomorphism | no | yes, irreversibility and recurrence | moderate | yes |
| Z-2 numeric fixer law in Lean | no | no, the invariant row is decided | large | no |
| Z-3 multiplication laws in Lean | no | no | large | no |
| Z-4 succession through the element count | no | yes, succession | small | yes |
| Z-5 automorphisms along a generated run | no | not until X-5 exists | a rung | no |
| Y-1 shortest witnesses | no | yes, succession | moderate | yes |
| Y-2 necessity of uniformity | no | no | small, after X-1 | no |
| Y-4 converse of the checks at arity one | no | no | small | no |
| X-1 decision procedure | no | no | moderate | no |
| X-2 count under a generated run | no | not until X-5 exists | a rung | no |
| X-4 safety of the omissions | no | no | small | no |
| X-5 the engine | no | no | not priced | no |
| X-6 the undecided rows | no | yes | large | yes |

Four are eligible and Z-4 is the only one priced small, so there is no
tie to break: the next rung is **Z-4, succession through the element
count** -- whether the count of changing rounds that a regime and its base
carry decides the census row for succession of accepted rounds, and on
which declared reading of an accepted round.

As rungs three and four recorded, X-1 is the leftover the others keep
waiting on; it is not eligible on the plain reading of the rule, and it
is recorded here again rather than taken.  Nothing of any leftover is
started here.
