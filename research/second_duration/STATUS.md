# STATUS: rung seven -- duration under the CHANGING reading

`AuthorityEffect: None`.  Counts in this file are dated 2026-09-25.  A
receipt is not a proof; a pin proves only that a source did not move; a
gate is proved by the defect it fails on, and every injection this rung
ran is recorded in `research/second/MANUAL.md` with its observed failure.

## The question, and where it came from

Rung six's leftover W-1, quoted verbatim in `CLAIM_LEDGER.md` from a
pinned span: duration under the CHANGING reading.  Rung six's own
application of the seed's next-rung rule, pinned as a second span,
selects it, because it extends the census of challenge five -- the row
for duration -- it is the only eligible leftover priced small, and no
leftover reduces the count of declared inputs.

`research/second/PLAN.md` item five assigns "run forward" and the census
to rungs four and five.  As in rungs three to six, this rung follows the
seed's rule, which the plan's item six defers to, and not the list; the
plan is not edited.

## Source policy, declared before the first compile

RECONSTRUCTION, with a pin note, as rungs three to six did.  One
reconstruction module, `Kernel.lean`, reproduces the sealed kernel slice
verbatim from `Basic.lean` and `Inertia.lean`.  `test_reconstruction.py`
compares it declaration by declaration with the pinned blobs AT THE
SNAPSHOT: 37 shared declarations, all identical after comments and
namespace lines are stripped and whitespace is normalized; the four
omitted declarations are pinned by name.

`Kernel.lean` was produced from rung six's `Kernel.lean` by changing only
the outer namespace; the comparison above is against the SEALED blobs,
not rung six's copy.  Two lemmas of this package, `replayE_cons` and
`insertNew_grows`, repeat as statements rung six's lemmas of the same
names.  They are proved again here so that the package imports nothing;
the ledger credits the statements to rung six and the census note says
they are not new to the run.  The Python consumes the sealed kernel, the
sealed genesis readings, rung three's bases and rung four's population
through their public functions and copies no source of any of them.  The
verifiers, the coverage gate and four test files are hand copies of rung
six's with this rung's paths, each saying so in its first lines.

## What is proved, what is computed, what is open

A ROUND is a CHANGING event, as rung six declared it.  A GROWTH is a
round that adds a datum; a REST ROUND is any other round.  The DURATION
VECTOR of a history counts its rest rounds by the number of growths taken
before them; its interior entries are the durations between growths.

**Proved in Lean** (33 theorems in the package, 17 of them
reconstructions; axioms within `{propext, Quot.sound}` for every one --
two with none, sixteen with `propext` alone, fifteen with both -- and no
`Classical.choice` anywhere):

- for every history replayed from a base, the regime reached has the
  base's data plus the growths, and its element count is the base's plus
  the growths plus the rest rounds; so the number of segments and the sum
  of the vector are functions of the base and the regime;
- the instances and requirements of the regime reached that name a datum
  index at or above `t` are at most those of the base plus the rest
  rounds taken after the regime has more than `t` data, with no
  well-formedness hypothesis on the base;
- when the base names nothing at or above `t` and every rest round adds
  an instance or requirement naming `t` or later, every rest round lies
  after datum `t` exists; so every history from the empty regime to the
  regime of two data and one requirement between them takes its one rest
  round after the second growth.

**Countermodels in Lean**, each by kernel computation on two concrete
histories from the empty regime:

- a form then a datum, and a datum then the form, reach one regime with
  segment zero one and zero; so no function of a position, a base and a
  regime gives a segment;
- a datum, a form, a datum; and a datum, a datum, the form, reach one
  regime with the duration between the first and the second growth one
  and zero; so no function of the regime gives that duration, even from
  the empty regime.

**Computed** over rung three's rectangle -- three bases, 18798
sequences, 2316 distinct regimes:

- on every sequence the vector has one entry per growth plus one and
  sums to the number of new elements other than data;
- at every regime the vectors reached are EXACTLY the envelope -- the
  tuples of that length and sum whose later sums meet the lower bounds
  of the levels -- with no vector outside it and no tuple of it
  unreached; so a regime is reached with one vector exactly when its
  envelope has one tuple (28, 263 and 1121 regimes at EMPTY, L and F);
- 47, 260 and 597 regimes are reached with two vectors, and 19, 63 and
  103 with two tuples of durations between growths; the shortest
  splitting sequences have two and three events at every base;
- 3, 13 and 17 regimes with a growth and a rest round have a one-tuple
  envelope, with every rest round in the tail;
- up to the implemented isomorphism, within a base: 34, 69 and 73
  classes are reached with two vectors, none with two sums, and 3, 45
  and 50 carry regimes with different envelopes.

**Open, named and priced** (V-1 to V-3 below, and the leftovers carried
from rungs three to six).  Beyond the rectangle, that the envelope is
attained is OPEN (V-1); whether the vector sum is carried by the CLASS of
a regime is OPEN behind Z-1.

## The frozen predictions, scored

Seven computational rows, scored mechanically by `run_duration.py` and
recorded in `receipts/duration.json`:

| row | value | verdict |
|---|---|---|
| N-8 | 577, 3928, 14293 sequences; 75, 523, 1718 regimes; 0 replay mismatches | HIT |
| N-9 | 0 length and 0 sum violations at each base | HIT |
| N-10 | 0 vectors outside the envelope, 0 regimes with a tuple unreached or extra, 0 one-tuple/one-vector mismatches, at each base | HIT |
| N-11 | vector-split 47, 260, 597; gap-split 19, 63, 103; shortest 2 and 3 at each base | HIT |
| N-12 | tail-only regimes 3, 13, 17 | HIT |
| N-13 | classes with two vectors 34, 69, 73; with two sums 0, 0, 0; with two envelopes 3, 45, 50 | HIT |
| N-14 | the three Lean witnesses replay as claimed | HIT |

Ten rows are scored where their evidence lives and are marked so in the
receipt rather than omitted: N-1 to N-6 by the statement-shape tests of
`test_census.py` and by `verify_lean.py`; N-7 by the committed axiom log;
N-15 and N-16 by `CLAIM_LEDGER.md` and `test_census.py`; N-17 by
`run_duration.py --check`, `test_duration.py` and the measured time
below.  Each is met.

### The census prediction

`PREDICTIONS.md` named 16 Lean targets and a class for each, frozen
before the compile.  All 16 exist, and no native theorem was added beyond
them.  Scored mechanically by `test_census.py`: **13 hits, 3 misses, no
unpredicted native theorem**.

| target | predicted | classed | direction |
|---|---|---|---|
| `growths_counted` | THIN | CONTENT | promoted |
| `naming_step` | THIN | CONTENT | promoted |
| `naming_bounded` | CONTENT | THIN | demoted |

**The misses, as findings.**  The classes were assigned after the
compile, by a rule written into the census note and applied to rung
six's precedent: an induction over histories whose step needs a case
analysis on the step's shape is CONTENT (rung six's `changes_counted`);
one closed by a step lemma and arithmetic is THIN (rung six's
`changes_le_admitting`).  Before the compile the bound was predicted to
live in the induction; it lives in the step lemma, whose two cases for
an instance and a requirement carry the argument that a new element
naming `t` or later names an admitted datum.  `growths_counted` has the
same shape as `rest_counted` and is classed with it.  The rule is a
judgment and is written down so it can be disputed; the frozen
prediction is not edited.

**What the hits say, and what they do not.**  The N-10 row -- that the
vectors reached are exactly the envelope -- rested on an argument written
in this session before the run (reorder the rounds of any history,
keeping data and forms in order, into any tuple the bounds allow).  The
hit shows the argument survived the rectangle; it is not a proof, and
V-1 names the proof.

## Found live, before any injection

**A Lean proof step that looked like `rfl` and was not accepted as a
rewrite.**  In `naming_step`, re-admitting an instance already held
leaves the regime written as a record update with the same field, which
is the regime itself by structure eta; `omega` treated the two as
different atoms and `rw` with the equation did not fire.  The step was
closed by `Nat.le_trans (Nat.le_of_eq rfl) (Nat.le_add_right _ _)`, which
lets the kernel check the definitional equality.  Recorded because a
reader of the proof may ask why that line is not `omega`.

**A forged vector is the only way to see a law fire.**  Over the
rectangle every law reports zero violations.  `test_duration.py` feeds
the base report a vector of the wrong length, one of the wrong sum, and
one below the level bound, and the class report a class with two sums
and a pair of isomorphic regimes with different envelopes; each is
counted.  Each scored row is also moved and turns to MISSED.

## Leftovers, named and priced, executed nowhere

- **V-1, attainment of the envelope.**  That every tuple the lower bounds
  allow is the duration vector of some history from the base to the
  regime.  The argument is a reordering of the rounds of one history,
  keeping data, forms and instance order, and it holds on the rectangle;
  in Lean it needs a permutation of a history and a replay of it.
  Price: moderate.  It refines the duration row this rung decides and
  extends no row of the census.
- **V-2, duration under an engine's rounds.**  Everything here is over
  histories of the sealed step.  Waits on X-5.  Price: a rung, after
  X-5.
- **V-3, the envelope up to the isomorphism.**  The envelope moves with
  a renaming of data (DUR-17); whether the multiset of envelopes of a
  class, or its sum, is a class invariant beyond the rectangle is not
  decided.  The sum part is Z-1.  Price: moderate, after Z-1.  It
  refines the duration row and extends no row of the census.
- Carried from rung six, unchanged: W-2 and W-3.  W-1 is this rung.
- Carried from rung five, unchanged: Z-1, Z-2, Z-3 and Z-5.
- Carried from rung four, unchanged: Y-1, Y-2, Y-4.
- Carried from rung three, unchanged: X-1, X-2, X-4, X-5, and X-6 less
  symmetry, invariants, irreversibility, succession and duration:
  two-ness, observational classes, adjacency, reach, branching,
  exhaustion and recurrence.

## Gates and timing

Measured on this machine, 2026-09-25, by `python ci/run_gates.py --step
"rung 7" --keep-going` at `8013e1eb`, which ran the four registered steps
of this rung in the workflow's order:

| gate | command | measured |
|---|---|---|
| clean Lean build and axiom audit | `python3 research/second_duration/verify_lean.py` | 28.4 s |
| pins, spans, frozen texts | `python research/second_duration/verify_pins.py` | 2.4 s |
| tests under coverage (150 tests), coverage gate, receipt comparison | the rung's replay, tests and coverage step | 49.3 s |
| strict typing | `python -m mypy` | 0.8 s |

Grouped measured time **80.9 seconds**, inside the fifteen-minute
per-rung ceiling the seed sets.  The Lean row is a CLEAN build: `lake
clean`, a full rebuild, then the compiled-environment census.  Coverage
over the declared measured set (`duration.py`, `run_duration.py`,
`verify_pins.py`): **line 98.96%, branch 96.15%**, both above the 95%
floor.  The runner reported that the interpreter's pytest (9.1.1)
differs from the pin in `requirements.txt` (9.0.3); this rung's tests run
under `unittest` and do not import pytest.

These are local receipts.  Hosted CI is permanently disabled by author
decision; the workflow is the written contract and its steps were run
here by the repository's own runner.  The estate custody census, run on
the clean worktree after its pin was rewritten, reports 104 verifiers,
103 green and one pinned red that this rung did not add.

## Terminal scope

- `SEGMENTS_AND_SUM_GIVEN_BASE` -- PROVED_THEOREM, every history of the sealed step.
- `SEGMENT_NOT_GIVEN_BASE` -- COUNTERMODEL, two histories from the empty regime.
- `GAP_NOT_FROM_EMPTY` -- COUNTERMODEL, two histories from the empty regime.
- `LOWER_BOUNDS_BY_NAMED_DATA` -- PROVED_THEOREM, every history of the sealed step.
- `TAIL_FORCED` -- PROVED_THEOREM, every history meeting its hypotheses.
- `ENVELOPE_ATTAINED` -- FINITE_COMPUTATION in the rectangle; OPEN beyond (V-1).
- `DURATION_UP_TO_THE_ISOMORPHISM` -- FINITE_COMPUTATION in the rectangle; OPEN beyond (V-3, Z-1).
- `CENSUS_DURATION` -- one row decided under the CHANGING reading, conditional on an engine for FORCED.
- `INPUT_COUNT_UNCHANGED` -- RECORDED, value two, no proof of a floor, no reduction.
- `OBSTRUCTIONS_UNTOUCHED` -- RECORDED.

```yaml
steps_completed: [Reconstruct, Rounds, Gaps, Rectangle, Census, Register]
write_root: research/second_duration/
snapshot: d6dca75058e2d65ad5be19d682fb2a6b93291ecc
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
prompt_sha256: 90ee1d2266f7d1a1269f21655dbd3a131542409e58cca79444d7b4ef720317b7
predictions_sha256: 338d1b115327e1b99caf1699eade18f8b9e217dda3c328b6c8fc4987dfcf6f0e
bases: [EMPTY, L, F]
sequences: {EMPTY: 577, L: 3928, F: 14293}
regimes: {EMPTY: 75, L: 523, F: 1718}
reading: CHANGING
lean_theorems: {total: 33, reconstruction: 17, content: 3, thin: 10, definition: 3}
predictions_scored: {hit: 7, missed: 0, elsewhere: 10}
census_prediction_scored: {named: 16, hit: 13, missed: 3, unpredicted_native: 0}
input_count: {value: 2, proof: none, sentence: "This rung neither reduces the count of declared inputs nor proves it at a floor."}
census_rows_decided: [duration]
authority_effect: None
final_state: true
```

## The next rung, named so it cannot be smuggled in later

The seed's rule takes the smallest named leftover that EITHER reduces the
count of declared inputs OR extends the census of challenge five, and on
a tie the one named first.  Rung six recorded that a leftover refining a
decided row is not eligible.  Applied to this rung's leftovers and the
ones carried, with that reading applied again to every carried row:

| leftover | reduces the input count | extends the census | price | eligible |
|---|---|---|---|---|
| V-1 attainment of the envelope | no | no, the duration row is decided | moderate | no |
| V-2 duration under an engine | no | not until X-5 exists | a rung | no |
| V-3 the envelope up to the isomorphism | no | no, the duration row is decided | moderate, after Z-1 | no |
| W-2 the full set of counts | no | no, the succession row is decided | small | no |
| W-3 succession under an engine | no | not until X-5 exists | a rung | no |
| Z-1 element count across the isomorphism | no | yes, recurrence; irreversibility up to the isomorphism | moderate | yes |
| Z-2 numeric fixer law in Lean | no | no | large | no |
| Z-3 multiplication laws in Lean | no | no | large | no |
| Z-5 automorphisms along a generated run | no | not until X-5 exists | a rung | no |
| Y-1 shortest witnesses | no | no, the succession row is decided | moderate | no |
| Y-2 necessity of uniformity | no | no | small, after X-1 | no |
| Y-4 converse of the checks at arity one | no | no | small | no |
| X-1 decision procedure | no | no | moderate | no |
| X-2 count under a generated run | no | not until X-5 exists | a rung | no |
| X-4 safety of the omissions | no | no | small | no |
| X-5 the engine | no | no | not priced | no |
| X-6 the undecided rows | no | yes | large | yes |

**One reclassification, recorded rather than made silently.**  Rungs
four to six marked Y-1 eligible because it extends the succession row.
Rung six decided that row and, in the same file, recorded that a
leftover refining a decided row is not eligible; applied to Y-1, that
reading makes it ineligible, and it is marked so above.  Had Y-1 stayed
eligible it would tie Z-1 at moderate, and the tie would turn on whether
"named first" means first in time (Y-1, rung four) or first in the list;
the reclassification removes the tie rather than resolving it.

Two are eligible and Z-1 is the smaller, so the next rung is **Z-1, the
element count across the isomorphism** -- whether two regimes the sealed
isomorphism relates have one element count, which would decide the
recurrence row and carry irreversibility, and the sum of the duration
vector, from regimes to classes beyond the rectangle.

As rungs three to six recorded, X-1 is the leftover the others keep
waiting on; it is not eligible on the plain reading of the rule, and it
is recorded here again rather than taken.  Nothing of any leftover is
started here.
