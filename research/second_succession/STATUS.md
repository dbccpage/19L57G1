# STATUS: rung six -- succession through the element count

`AuthorityEffect: None`.  Counts in this file are dated 2026-09-25.  A
receipt is not a proof; a pin proves only that a source did not move; a
gate is proved by the defect it fails on, and every injection this rung
ran is recorded in `research/second/MANUAL.md` with its observed failure.

## The question, and where it came from

Rung five's leftover Z-4, quoted verbatim in `CLAIM_LEDGER.md` from a
pinned span: succession through the element count.  Rung five's own
application of the seed's next-rung rule, pinned as a second span,
selects it, because it extends the census of challenge five -- the row
for succession -- it is the only eligible leftover priced small, and no
leftover reduces the count of declared inputs.

`research/second/PLAN.md` item five assigns "run forward" and the census
to rungs four and five.  As in rungs three to five, this rung follows the
seed's rule, which the plan's item six defers to, and not the list; the
plan is not edited.

## Source policy, declared before the first compile

RECONSTRUCTION, with a pin note, as rungs three to five did.  One
reconstruction module, `Kernel.lean`, reproduces the sealed kernel slice
verbatim from `Basic.lean` and `Inertia.lean`; the sealed isomorphism
structure rung five also carried is not needed here and is not
reproduced.  `test_reconstruction.py` compares the module declaration by
declaration with the pinned blobs AT THE SNAPSHOT: 37 shared
declarations, all identical after comments and namespace lines are
stripped and whitespace is normalized; the four omitted declarations are
pinned by name.

`Kernel.lean` was produced from rung five's `Kernel.lean` by changing only
the outer namespace; the comparison above is against the SEALED blobs,
not rung five's copy.  Two theorems of this package, `step_grows` and
`changes_counted`, repeat as statements rung five's `size_step` and
`size_counts_changes`.  They are proved again here, in this rung's own
proofs, so that the package imports nothing; the ledger credits the
statements to rung five and the census note says they are not new to the
run.  The Python consumes the sealed kernel, the sealed genesis
readings, rung three's bases and rung four's population through their
public functions and copies no source of any of them.  The verifiers,
the coverage gate and four test files are hand copies of rung five's with
this rung's paths, each saying so in its first lines.

## What is proved, what is computed, what is open

Three readings of an accepted round are declared in `PROMPT.md`: EVERY
event, every ADMITTING event (every event but a supply), and every
CHANGING event (every event after which the regime differs).

**Proved in Lean** (34 theorems in the package, 17 of them
reconstructions; axioms within `{propext, Quot.sound}` for every one --
three with none, eighteen with `propext` alone, thirteen with both -- and
no `Classical.choice` anywhere):

- under CHANGING, the count of any history replayed from a base is the
  element count of the regime reached less that of the base; so it is a
  function of the base and the regime, and two histories from one base to
  one regime carry one count;
- from the sealed empty regime it is the element count of the regime
  reached, with no base named;
- the three counts are ordered, CHANGING at most ADMITTING at most EVERY,
  for every history.

**Countermodels in Lean**, each by kernel computation on a concrete
history from the empty regime:

- under EVERY, the empty history and one supply reach one regime with
  counts zero and one; so no function of base and regime gives the count;
- under ADMITTING, a form with its rule admitted once and admitted twice
  reach one regime with counts two and three; likewise;
- under CHANGING, the sealed reading-L regime is reached from the empty
  regime with count three and from itself with count zero; so no function
  of the regime alone gives the count, and the base must be named unless
  it is the empty regime.

**Computed** over rung three's rectangle -- three bases, 18798
sequences, 2316 distinct regimes, 402 classes:

- under CHANGING no regime and no class is reached with two counts within
  a base, and both laws -- base-relative and from the empty regime --
  hold on every sequence;
- under EVERY 33, 118 and 276 regimes split at EMPTY, L and F, the
  shortest splitting sequence one supply; under ADMITTING 15, 100 and
  259, the shortest three events at EMPTY and two at L and F;
- 86 classes are reached from more than one base; every one carries
  different base-relative counts at its bases and one count from the
  empty regime.

**Open, named and priced** (W-1 to W-3 below, rung five's Z-1 to Z-5 less
Z-4, rung four's Y-1, Y-2 and Y-4, and rung three's X-1, X-2, X-4, X-5 and
X-6 less the rows now decided).  Beyond the rectangle, whether the
CHANGING count is a function of the CLASS of a regime is OPEN behind
Z-1: the count is the element count, and that the element count is kept
by the sealed isomorphism is exactly what Z-1 asks.

## The frozen predictions, scored

Six computational rows, scored mechanically by `run_succession.py` and
recorded in `receipts/succession.json`:

| row | value | verdict |
|---|---|---|
| M-8 | 577, 3928, 14293 sequences; 75, 523, 1718 regimes; 0 replay mismatches | HIT |
| M-9 | CHANGING: 0 split regimes, 0 base-relative and 0 from-empty violations at each base | HIT |
| M-10 | EVERY splits at every base, shortest one supply; ADMITTING splits at every base, shortest 3, 2, 2 | HIT |
| M-11 | EVERY 33, 118, 276 against ADMITTING 15, 100, 259 | HIT |
| M-12 | 0 classes with two counts within a base; 86 shared; 0 agreeing relatively; 0 disagreeing from empty | HIT |
| M-13 | base element counts 0, 2, 3; genesis counts 6, 2, 2 (L) and 7, 3, 3 (F) | HIT |

Ten rows are scored where their evidence lives and are marked so in the
receipt rather than omitted: M-1 to M-6 by the statement-shape tests of
`test_census.py` and by `verify_lean.py`; M-7 by the committed axiom log;
M-14 and M-15 by `CLAIM_LEDGER.md` and `test_census.py`; M-16 by
`run_succession.py --check`, `test_succession.py` and the measured time
below.  Each is met.

### The census prediction

`PREDICTIONS.md` named 17 Lean targets and a class for each, frozen
before the compile.  All 17 exist.  Scored mechanically by
`test_census.py`: **17 hits, no miss, no unpredicted native theorem**.

**What a clean sheet says here, and what it does not.**  Most rows were
labelled FORCED before the run, and the Lean was designed in the same
session as the predictions, after the three readings were fixed.  A hit
on a FORCED row evidences the order of the work -- frozen, then computed
-- and not insight; the NOT FORCED rows (M-1, M-6, M-9 to M-11, M-14) are
the ones that could have gone the other way.  Two classifications were
judgment calls and are written into the census note rather than left
implicit: `changes_le_admitting` and `admitting_le_every` are inductions
whose step bounds one term by one, classed THIN with the induction as
their one genuine step; `step_grows` is a six-way case exhaustion with a
length rewrite per case, THIN as rung five classed its `size_step`.

## Found live, before any injection

**The splitting definition was read too narrowly, and fixed before the
first run.**  The first draft of `splitting` in `succession.py` compared
a sequence only with sequences sorted before it.  The frozen definition in
`PREDICTIONS.md` -- a count differing from that of a sequence of no
greater length -- also counts a sequence of EQUAL length sorted after it,
so of two equal-length sequences with different counts the lesser in order
is the witness.  The scan was widened before any count was computed; the
length it reports is the same under either reading, and
`test_of_two_equal_lengths_the_lesser_in_order_splits` pins the repaired
choice.

**A forged sequence is the only way to see a law fire.**  Over the
rectangle every law reports zero violations, which alone would not show
that the check can fail.  `test_succession.py` feeds the base report a
sequence whose CHANGING count is forged and one whose regime is forged,
and the class report a class with two counts within a base and a class
whose counts agree across two bases; each is counted.  Each scored row is
also moved and turns to MISSED.

## Leftovers, named and priced, executed nowhere

- **W-1, duration under the CHANGING reading.**  The seed's census row
  for duration reads it as rounds between growths.  Under CHANGING the
  regime carries the total number of rounds and, separately, the number
  of growths (its data); whether it carries the number of changing rounds
  between two growths -- or only bounds on it, through which data the
  admitted instances and requirements name -- is not decided.  Price:
  small; the counts and the rectangle are in place.
- **W-2, the full set of counts a base and a regime admit.**  Under EVERY
  and ADMITTING the count of a history from a base to a regime is not
  fixed; which counts occur -- whether every count at or above the
  CHANGING count occurs, and when a repeatable admission exists -- is not
  decided.  Price: small.  It refines the succession row this rung
  decides and extends no row of the census.
- **W-3, succession under an engine's accepted rounds.**  Everything here
  is over histories of the sealed step, not over a run an engine
  generates.  Waits on X-5.  Price: a rung, after X-5.
- Carried from rung five, unchanged: Z-1 (the element count across the
  isomorphism, which the succession row now also waits on beyond the
  rectangle), Z-2, Z-3 and Z-5.  Z-4 is this rung.
- Carried from rung four, unchanged: Y-1, Y-2, Y-4.
- Carried from rung three, unchanged: X-1, X-2, X-4, X-5, and X-6 less
  symmetry, invariants, irreversibility and succession: two-ness,
  observational classes, duration, adjacency, reach, branching,
  exhaustion and recurrence.

## Gates and timing

Measured on this machine, 2026-09-25, by `python ci/run_gates.py --step
"rung 6" --keep-going` at `9d5d19d2`, which ran the four registered steps
of this rung in the workflow's order:

| gate | command | measured |
|---|---|---|
| clean Lean build and axiom audit | `python3 research/second_succession/verify_lean.py` | 28.2 s |
| pins, spans, frozen texts | `python research/second_succession/verify_pins.py` | 1.6 s |
| tests under coverage (139 tests), coverage gate, receipt comparison | the rung's replay, tests and coverage step | 60.3 s |
| strict typing | `python -m mypy` | 2.1 s |

Grouped measured time **92.2 seconds**, inside the fifteen-minute
per-rung ceiling the seed sets.  The Lean row is a CLEAN build: `lake
clean`, a full rebuild, then the compiled-environment census.  Coverage
over the declared measured set (`succession.py`, `run_succession.py`,
`verify_pins.py`): **line 98.87%, branch 95.93%**, both above the 95%
floor.  The runner reported that the interpreter's pytest (9.1.1)
differs from the pin in `requirements.txt` (9.0.3); this rung's tests run
under `unittest` and do not import pytest.

These are local receipts.  Hosted CI is permanently disabled by author
decision; the workflow is the written contract and its steps were run
here by the repository's own runner.  The estate custody census, run on
the clean worktree after its pin was rewritten, reports 103 verifiers,
102 green and one pinned red that this rung did not add.

## Terminal scope

- `CHANGING_GIVEN_BASE` -- PROVED_THEOREM, every history of the sealed step.
- `CHANGING_FROM_EMPTY` -- PROVED_THEOREM, every history from the sealed empty regime.
- `CHANGING_NOT_OF_REGIME` -- COUNTERMODEL, the sealed reading-L regime.
- `EVERY_AND_ADMITTING_NOT_GIVEN_BASE` -- COUNTERMODEL, two histories each.
- `COUNTS_ORDERED` -- PROVED_THEOREM, every history.
- `COUNT_UP_TO_THE_ISOMORPHISM` -- FINITE_COMPUTATION in the rectangle; OPEN beyond (Z-1).
- `CENSUS_SUCCESSION` -- one row decided under three readings, conditional on an engine for FORCED; rungs three and four's readings stand.
- `INPUT_COUNT_UNCHANGED` -- RECORDED, value two, no proof of a floor, no reduction.
- `OBSTRUCTIONS_UNTOUCHED` -- RECORDED.

```yaml
steps_completed: [Reconstruct, Count, Readings, Rectangle, Census, Register]
write_root: research/second_succession/
snapshot: 144d9c2bcd356290cce070887f03811416bc87b1
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
prompt_sha256: ac59280878c2e8f626517bcf49079823bf5561184d6b8fa711fadc0e392cdecc
predictions_sha256: bffdd720b9dc4f96948a5e188e30d7b51b40b628c5ef81c1983e3b3765990758
bases: [EMPTY, L, F]
sequences: {EMPTY: 577, L: 3928, F: 14293}
regimes: {EMPTY: 75, L: 523, F: 1718}
classes: 402
readings: [EVERY, ADMITTING, CHANGING]
lean_theorems: {total: 34, reconstruction: 17, content: 1, thin: 10, definition: 6}
predictions_scored: {hit: 6, missed: 0, elsewhere: 10}
census_prediction_scored: {named: 17, hit: 17, missed: 0, unpredicted_native: 0}
input_count: {value: 2, proof: none, sentence: "This rung neither reduces the count of declared inputs nor proves it at a floor."}
census_rows_decided: [succession]
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
| W-1 duration under CHANGING | no | yes, duration | small | yes |
| W-2 the full set of counts | no | no, the succession row is decided | small | no |
| W-3 succession under an engine | no | not until X-5 exists | a rung | no |
| Z-1 element count across the isomorphism | no | yes, irreversibility, recurrence, and succession beyond the rectangle | moderate | yes |
| Z-2 numeric fixer law in Lean | no | no | large | no |
| Z-3 multiplication laws in Lean | no | no | large | no |
| Z-5 automorphisms along a generated run | no | not until X-5 exists | a rung | no |
| Y-1 shortest witnesses | no | yes, succession | moderate | yes |
| Y-2 necessity of uniformity | no | no | small, after X-1 | no |
| Y-4 converse of the checks at arity one | no | no | small | no |
| X-1 decision procedure | no | no | moderate | no |
| X-2 count under a generated run | no | not until X-5 exists | a rung | no |
| X-4 safety of the omissions | no | no | small | no |
| X-5 the engine | no | no | not priced | no |
| X-6 the undecided rows | no | yes | large | yes |

Four are eligible and W-1 is the only one priced small, so there is no
tie to break: the next rung is **W-1, duration under the CHANGING
reading** -- whether the number of changing rounds between two growths is
carried by the regime a history reaches, and from which base.

As rungs three to five recorded, X-1 is the leftover the others keep
waiting on; it is not eligible on the plain reading of the rule, and it
is recorded here again rather than taken.  Nothing of any leftover is
started here.
