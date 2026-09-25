# STATUS: rung ten -- adjacency, reach, branching and exhaustion

`AuthorityEffect: None`.  Counts in this file are dated 2026-09-25.  A
receipt is not a proof; a pin proves only that a source did not move; a
gate is proved by the defect it fails on, and every injection this rung
ran is recorded in `research/second/MANUAL.md` with its observed failure.

## The question, and where it came from

Rung three's leftover X-6, quoted verbatim in `CLAIM_LEDGER.md` from two
pinned spans: rung three's own text, and the four rows rung nine carries.
Rung nine's application of the seed's next-rung rule, pinned as a third
span, selects it as the only eligible leftover: it extends the census of
challenge five, and no leftover reduces the count of declared inputs.

**The readings applied, recorded before the predictions.**  Two readings
were written into `PROMPT.md` before `PREDICTIONS.md` was frozen, and
neither binds a later rung:

- *Which rows.*  All four remaining rows -- adjacency, reach, branching
  and exhaustion -- because the seed's rung budget is nearly spent and a
  row left for a later rung may have no rung to take it.  Rung nine's
  reading, to decide some rows and name the rest, is not followed here;
  the author may reject either.
- *Which response.*  Rung nine left a remark, pinned here as a span, for
  the rung that takes X-6: whether the sealed estate's candidate space
  and minimum responses are the response the adjacency, reach and
  branching rows speak of.  This rung reads them as the SEALED
  RESPONDER, consumed unchanged: the demand is a pair the sealed
  `collapsed_pairs` returns, read off the state; the response is a
  minimum of the sealed `min_responses` at the sealed bounds (two items,
  arity two) under `mu1` and under `mu2` in turn.  The sealed responder
  refuses a regime holding a uniform rule; such a regime is counted
  outside its domain and the responder is not widened.  No engine is
  declared: a response to one demand at one regime is not a round.

`research/second/PLAN.md` item five assigns "run forward" and the census
to rungs four and five.  As in rungs three to nine, this rung follows the
seed's rule, which the plan's item six defers to, and not the list; the
plan is not edited.

## Source policy, declared before the first compile

RECONSTRUCTION, with a pin note per file, as rungs three to nine did.
`Kernel.lean` and `IsoKernel.lean` were produced from rung nine's copies
by changing only the outer namespace, and `test_reconstruction.py`
compares them declaration by declaration with the SEALED blobs at the
snapshot: 41 shared declarations, all identical after comments and
namespace lines are stripped and whitespace is normalized.

RESTATED, credited: `Carry.lean` is rung nine's module of the same name,
unedited but for the namespace, less its two headline statements, which
this rung does not use.  `HoldsTwo` (rung nine), `separable_step_keep`
(rung nine, proved differently here, as a corollary of `ctx_step_keep`),
`getD_append_lt` (rung five) and `step_wf` (rung three's `wf_step_any`)
are stated and proved again so that the package imports nothing.  The
Python consumes the sealed kernel, the sealed profiles and collapsed
pairs, the sealed responder with its unpruned enumeration and its
reference validity, the sealed key procedure and brute-force minimum,
the sealed genesis readings, rung three's bases and rung four's
population through their public functions, and copies no source of any
of them.  The verifiers, the coverage gate and four test files are hand
copies of rung nine's, each saying so in its first lines.

## What is proved, what is computed, what is open

A form EXHAUSTED distinguishes no two admitted data; a pair of data is
MOVED when it is separable on one side and collapsed on the other.

**Proved in Lean** (56 theorems in the package, 17 of them
reconstructions; axioms within `{propext, Quot.sound}` for every one --
three with none, twenty-seven with `propext` alone, twenty-six with both
-- and no `Classical.choice` anywhere):

- a form admitted in the source is exhausted exactly when its image under
  an inhabitant of the sealed isomorphism is, with no hypothesis on
  either regime; a form is exhausted exactly when it does not
  distinguish, and a regime holds two exactly when some form
  distinguishes;
- a ruled form, a form no held instance lies on, and every form of a
  regime of at most one datum are exhausted; a fresh form of a
  well-formed regime is exhausted; the empty regime has none, and one
  form admission reaches one;
- a supply, a requirement, a form and a rule keep exhaustion; a supply,
  a requirement, a form and a datum keep distinguishing; the four other
  changes are exhibited, so exhaustion is begun only by instance and rule
  admissions (besides a fresh form) and ended only by datum and instance
  admissions;
- an instance admission mentioning neither datum of a pair leaves the
  pair as it was; on a well-formed regime every other event keeps a
  collapsed pair collapsed; so for a well-formed base and every history,
  a pair moved apart is mentioned by an instance of the history, and a
  pair moved together is so mentioned or the history holds a rule;
- one instance moves two pairs apart at once, and one instance can move
  one pair apart and another together.

**Computed** over rung three's rectangle -- three bases, 18798
sequences, 2316 distinct regimes in 402 classes:

- 47, 402 and 1441 regimes at EMPTY, L and F are in the responder's
  domain, 28, 121 and 277 outside it, exactly the ruled ones;
- 34, 597 and 2479 demands, NONE refused; answered at one item 14, 315
  and 1514 times and at two items 20, 282 and 965 times, under both
  measures;
- no response holds a rule item or moves a pair its instances do not
  mention; every response moves its demand apart; 0, 114 and 1152
  responses per measure also move a pair together;
- the reach is nonempty exactly when two pairs move, holds every datum
  collapsed with the demand, and is at most three;
- the first adjacency edge is at three events from EMPTY, one from L and
  zero from F; no finite distance exceeds two, and at EMPTY `mu2` reaches
  two where `mu1` stops at one;
- the first demand with two tie classes is at two, zero and zero events
  under `mu1` and three, one and one under `mu2`; the largest tie-class
  count is five, eight and sixteen under `mu1`;
- no class of regimes carries two values of the exhausted count or of
  either measure's response signature;
- the sealed responder agrees with the unpruned sealed enumeration and
  the sealed reference validity at all 68 situations of the EMPTY
  family, and every response of the population passes the reference
  validity.

**Open, named and priced** (S-1 to S-5 below, and the leftovers carried
from rungs three to nine).

## Superseded, dated 2026-09-25, and left standing

No earlier receipt is revised, and no earlier OPEN statement is closed.
The four rows decided here were named undecided by rungs three to nine,
and each of those sentences stands as written at its rung.  Rung nine's
reading of a leftover carrying several rows -- decide the first two and
name the rest -- is not superseded; this rung applied a different
reading for itself, recorded above.

## The frozen predictions, scored

Twelve computational rows, scored mechanically by `run_response.py` and
recorded in `receipts/response.json`:

| row | value | verdict |
|---|---|---|
| R-9 | 577, 3928, 14293 sequences; 75, 523, 1718 regimes; 0 replay mismatches; 402 classes over 2316 regimes; 0 key and brute-force disagreements | HIT |
| R-10 | 47, 402, 1441 regimes inside the domain and 28, 121, 277 outside; 0 regimes where the responder's behaviour and the rule set disagree | HIT |
| R-11 | 0 demands refused at every base under both measures; 0 refusal disagreements between the measures | **MISSED** |
| R-12 | 0 responses with a rule item, 0 mentioning no demanded datum, 0 moving an unmentioned pair | HIT |
| R-13 | 0 responses not moving their demand apart; 0, 114, 1152 moving a pair together | HIT |
| R-14 | 0 reach mismatches, 0 class violations; empty and nonempty reach at every base | HIT |
| R-15 | first edge at 3, 1, 0 under both measures; largest finite distance 2 | HIT |
| R-16 | first two tie classes at 2, 0, 0 under `mu1` and 3, 1, 1 under `mu2`; 0 `mu2` responses outside `mu1`; tie count one at L and F | HIT |
| R-17 | 0 classes with two values of the exhausted count or of either signature | HIT |
| R-18 | 0 mismatches, 0 ruled forms distinguishing; changes by kind exactly as predicted | HIT |
| R-19 | first exhausted form at 1, 1, 1; beside holding two at 3 at L and F, none at EMPTY | HIT |
| R-20 | 0 disagreements at 68 situations; 0 reference-validity failures | HIT |

Twelve rows are scored where their evidence lives and are marked so in
the receipt rather than omitted: R-1 to R-7 by the statement-shape tests
of `test_census.py` and by `verify_lean.py`; R-8 by the committed axiom
log; R-21 to R-23 by `CLAIM_LEDGER.md` and `test_census.py`; R-24 by
`run_response.py --check`, `test_response.py` and the measured time
below.  Each is met.  Three rows were labelled FORCED before the run
(R-9, R-23, R-24), and a hit on a FORCED row evidences the order of the
work, not insight.

**The miss, R-11, recorded next to its value.**  The prediction said a
demand would be refused within two items at L and at F.  None is, at any
base.  The refusal this session had in mind before the run was a regime
holding requirements on several collapsed data; at two items the sealed
responder answers it with a new form of arity two and one instance on
it, which tells three data apart at once.  The miss is a finding: within
the rectangle the sealed responder never runs out of responses at its
bound.  A refused demand does exist beside the rectangle -- four data
with a requirement on every pair -- and `test_a_refused_demand` pins it.

### The census prediction, and its two misses

`PREDICTIONS.md` named 39 Lean targets and a class for each, frozen
before the compile.  All 39 exist.  Scored mechanically by
`test_census.py`: **37 hits, 2 misses, no unpredicted native theorem**.

| target | predicted | recorded | why |
|---|---|---|---|
| `holdsTwo_iff_distinguishes` | THIN | DEFINITION | the witness of separability is repackaged as a witness of distinguishing and back, by projections |
| `mem_plug_of_hole` | THIN | DEFINITION | a one-line term by `List.mem_map` |

**What the misses say.**  Both are demotions to DEFINITION, the same
direction as rung nine's four misses one class further down: this
session, having taken rung nine's lesson that assemblies are THIN,
still overrated the smallest pieces.  The census is total over the
package and checked in both directions, so a later silent promotion is
visible.

## Found live

**A refusal the rectangle does not reach** (R-11 above).

**The sealed responder's domain.**  The sealed `min_responses` builds its
fast view only on a regime holding no uniform rule and refuses any other
with a `ValueError`; 426 of the 2316 distinct regimes of the rectangle
are outside it.  The rows decided here are decided on the domain, and
the widening is named as S-1.

**A reach that the measure does not change but the graph does.**  The
largest reach and the counts of responses moving a pair together are the
same under both measures at every base, while the adjacency graph is not:
at EMPTY the largest finite distance is one under `mu1` and two under
`mu2`, and the largest edge count fifteen and twelve.  Recorded, not
interpreted.

## Leftovers, named and priced, executed nowhere

- **S-1, the rows on ruled regimes.**  The 426 regimes outside the
  sealed responder's domain.  Deciding the response rows there needs a
  responder the sealed estate does not declare -- the sealed unpruned
  enumeration and reference validity would serve -- and that is a
  declaration of this run, to be priced.  Price: small in Python; it
  refines decided rows and extends none.
- **S-2, the responses to a same-kind demand.**  The stake's other
  demand kind, answered by the sibling two-sided responder, is not read
  here.  Price: moderate; it refines decided rows.
- **S-3, the response rows in Lean.**  No Lean statement here is about a
  minimum, a cost or a tie; that needs the sealed candidate space
  reconstructed and an enumeration proved complete, which is close to
  rung three's X-1.  Price: large.
- **S-4, the distance beyond the bound.**  Within the rectangle no
  finite distance exceeds two.  Whether that is the bound's or the
  grammar's is not decided.  Price: moderate; it refines a decided row.
- **S-5, the FORCED column of the four rows.**  Conditional on an
  engine.  Price: a rung, and it needs X-5 first.
- Carried from rung nine, unchanged: T-1, T-2, T-3.
- Carried from rung eight, unchanged: U-1, U-2.
- Carried from rung seven: V-1, V-2, V-3.
- Carried from rung six, unchanged: W-2 and W-3.
- Carried from rung five, unchanged: Z-2, Z-3 and Z-5.
- Carried from rung four, unchanged: Y-1, Y-2, Y-4.
- Carried from rung three, unchanged: X-1, X-2, X-4, X-5.  X-6 is closed
  here: its last four rows are decided.

## The rung budget, counted and dated

The seed allows at most twelve rungs to be attempted.  This is the
eleventh rung ordinal, zero to ten; rung two ran as two tracks under one
ordinal, so twelve rung trees now exist.  Counted by ordinal, one rung
remains; counted by tree, none.  Which count the seed means is not
decided here and is recorded for the author, as rung nine recorded it.

## Gates and timing

Measured on this machine, 2026-09-25, by `python ci/run_gates.py --step
"rung 10" --keep-going` at `68eee7e7`, which ran the four registered
steps of this rung in the workflow's order:

| gate | command | measured |
|---|---|---|
| clean Lean build and axiom audit | `python3 research/second_response/verify_lean.py` | 27.4 s |
| pins, spans, frozen texts | `python research/second_response/verify_pins.py` | 4.0 s |
| tests under coverage (150 tests), coverage gate, receipt comparison | the rung's replay, tests and coverage step | 144.9 s |
| strict typing | `python -m mypy` | 0.8 s |

Grouped measured time **177.1 seconds**, inside the fifteen-minute
per-rung ceiling the seed sets.  The registered test floor is 140.  Most
of the test step is the pin battery and the three full builds of the
receipt.  Coverage over the declared measured set (`response_rows.py`,
`run_response.py`, `verify_pins.py`): **line 99.41%, branch 97.73%**,
both above the 95% floor.  The runner reported that the interpreter's
pytest (9.1.1) differs from the pin in `requirements.txt` (9.0.3); this
rung's tests run under `unittest` and do not import pytest.

These are local receipts.  Hosted CI is permanently disabled by author
decision; the workflow is the written contract and its steps were run
here by the repository's own runner.  The estate custody census, run on
the clean worktree when its pin was rewritten, reports 107 verifiers,
106 green and one pinned red that this rung did not add.

## Terminal scope

- `EXHAUSTION_CARRIED` -- PROVED_THEOREM, every inhabitant of the sealed isomorphism, an admitted form, no hypothesis on either regime.
- `EXHAUSTION_IS_NOT_DISTINGUISHING` -- PROVED_THEOREM, constructive; holding two is some form distinguishing, at the level of a definition.
- `EXHAUSTION_BY_KIND` -- PROVED_THEOREM for the keeping kinds, every regime; COUNTERMODEL for the four changes.
- `EXHAUSTION_FIRST_STAGE` -- DEFINITION, one event from the empty regime.
- `MOVED_PAIRS_ARE_MENTIONED` -- PROVED_THEOREM, every well-formed base and every history; a pair moved together may instead be moved by a rule.
- `ONE_INSTANCE_MOVES_TWO` -- COUNTERMODEL, one exhibited regime each for two pairs apart and for one apart and one together.
- `RECTANGLE_MEASURED` -- FINITE_COMPUTATION, the frozen rectangle and the sealed responder's domain only.
- `NO_REFUSAL_WITHIN_THE_RECTANGLE` -- FINITE_COMPUTATION; the frozen prediction R-11 MISSED.
- `RESPONSE_ROWS_IN_LEAN` -- OPEN (S-3); no Lean statement here is about a minimum, a cost or a tie.
- `CENSUS_ADJACENCY`, `CENSUS_REACH`, `CENSUS_BRANCHING` -- three rows decided, USEFUL REALIZATION under the named declaration of the sealed responder and one measure, priced at two declared capabilities, conditional on an engine for FORCED.
- `CENSUS_EXHAUSTION` -- one row decided, DEFINABLE, conditional on an engine for FORCED.
- `INPUT_COUNT_UNCHANGED` -- RECORDED, value two, no proof of a floor, no reduction.
- `OBSTRUCTIONS_UNTOUCHED` -- RECORDED.

```yaml
steps_completed: [Reconstruct, Restate, Exhaust, Move, Rectangle, Crosscheck, Census, Register]
write_root: research/second_response/
snapshot: 77ad2a7839aff8c9ec9b0204a5e9d6927fe8ae38
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
prompt_sha256: 09e9df8c4349b1ef3307f7cb606284534ca0e5b735163c6e7098805d18aa6093
predictions_sha256: 2fc139d7f455da1abb28548e355b0175ec4d918522c555207043c34c4b55cafa
bases: [EMPTY, L, F]
sequences: {EMPTY: 577, L: 3928, F: 14293}
regimes: {EMPTY: 75, L: 523, F: 1718}
regimes_in_domain: {EMPTY: 47, L: 402, F: 1441}
demands: {EMPTY: 34, L: 597, F: 2479}
refused: 0
lean_theorems: {total: 56, reconstruction: 17, content: 8, thin: 23, definition: 8}
predictions_scored: {hit: 11, missed: 1, elsewhere: 12}
census_prediction_scored: {named: 39, hit: 37, missed: 2, unpredicted_native: 0}
input_count: {value: 2, proof: none, sentence: "This rung neither reduces the count of declared inputs nor proves it at a floor."}
census_rows_decided: [adjacency, reach, branching, exhaustion]
census_rows_extended: []
gate_time_seconds: 177.1
authority_effect: None
final_state: true
```

## The next rung, named so it cannot be smuggled in later

The seed's rule takes the smallest named leftover that EITHER reduces the
count of declared inputs OR extends the census of challenge five, and on
a tie the one named first -- first in the list below, by the author's
ruling of 2026-09-25.  A leftover refining a decided row is not
eligible, as rungs six to nine read it.

| leftover | reduces the input count | extends the census | price | eligible |
|---|---|---|---|---|
| S-1 the rows on ruled regimes | no | no, the rows are decided | small | no |
| S-2 responses to a same-kind demand | no | no, the rows are decided | moderate | no |
| S-3 the response rows in Lean | no | no | large | no |
| S-4 the distance beyond the bound | no | no, the adjacency row is decided | moderate | no |
| S-5 the FORCED column of the four rows | no | not until X-5 exists | a rung | no |
| T-1 the class count as a number in Lean | no | no, the classes row is decided | small after X-1 | no |
| T-2 the change of the class count in Lean | no | no, the classes row is decided | moderate | no |
| T-3 holding two under an engine | no | not until X-5 exists | a rung | no |
| U-1 recurrence from an unclean base | no | no, the recurrence row is decided | small | no |
| U-2 the recurrence equivalence in Lean | no | no, the recurrence row is decided | small | no |
| V-1 attainment of the envelope | no | no, the duration row is decided | moderate | no |
| V-2 duration under an engine | no | not until X-5 exists | a rung | no |
| V-3 the multiset of envelopes of a class | no | no, the duration row is decided | moderate | no |
| W-2 the full set of counts | no | no, the succession row is decided | small | no |
| W-3 succession under an engine | no | not until X-5 exists | a rung | no |
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

**No leftover is eligible.**  With X-6 closed, every row the seed's
challenge five names is decided in at least its DEFINABLE or USEFUL
REALIZATION column, and no leftover reduces the count of declared
inputs; so the rule, read plainly as rungs three to nine read it,
selects no next rung.  This is recorded, not resolved.  Two facts are
recorded beside it for the author, and neither is acted on:

- X-5, the engine of the seed's challenge three, is the leftover that the
  FORCED column of every row waits on -- S-5, T-3, V-2, W-3, Z-5 and X-2
  among them -- and the seed's completion gate names every engine of the
  declared class run to bounds, refuted, or OPEN.  Whether "extends the
  census" covers deciding a FORCED column is a reading the seed leaves
  open; rungs three to nine read it as no, and this rung does not change
  that reading.
- The rung budget, counted by tree, is spent; counted by ordinal, one
  rung remains.  The seed's section nine also names the run's own paper,
  change log and claim ledger under `research/second/`, which no rung has
  written.

Nothing of any leftover is started here.
