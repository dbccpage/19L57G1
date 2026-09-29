# STATUS: continuation two -- run forward

`AuthorityEffect: None`.  Counts in this file are dated 2026-09-28.  A
receipt is not a proof; a pin proves only that a source did not move; a
gate is proved by the defect it fails on, and every injection this
attempt ran is recorded in `research/second/MANUAL.md` with its observed
failure.

## The question, and where it came from

The seed's challenge four: for each surviving engine, from each sealed
genesis reading, run to the declared bounds, quotienting by the
implemented isomorphism, retaining ties, replaying every node from
genesis, exporting the exact frontier, and recording every terminal by
kind; with the engine-dependent evaluations of challenge five, the
FORCED column of the census, which rungs five to ten left conditional on
an engine and continuation one left undecided.

It is continuation one's leftover G-1, with G-2 and G-7 inside it, quoted
in `CLAIM_LEDGER.md` from two pinned spans.  The author's ruling of
2026-09-25, recorded verbatim in `research/second/MANUAL.md` and in
`CLAUDE.md` and pinned here as a span, authorizes at most two further
research attempts, first challenge three and then challenge four.  **This
tree is the second and last.**  It is a protocol intervention by the
author, not a result of the seed's next-rung rule; `SEED.md` is
unchanged.  No attempt after it is authorized.

## The readings applied, recorded before the computation

The question is `PROMPT.md`, frozen at `c2530b12`; the predictions and
seven readings applied are `PREDICTIONS.md`, frozen at `c6b82249`, both
before any computation of this attempt and before any Lean.  The
readings applied settle what the prompt left open: carrying forward is
read on the recorded history of each frontier node; a closed run with a
cycle and no failure is UNDECIDED under ONE VALUE PER NODE; the first
failing member is taken in class order, reading L before F; every edge
into a present node is a merge; a response's moves are rung ten's moved
pairs from the parent's representative; every carried quantity is zero
at the root; the demand and honoured counts are read in the state's
mode.  One act of apparatus preceded the freeze and is disclosed there:
rung two's public tree builder was timed on E-four, which its committed
receipt already records, to choose a node guard that keeps the gate
inside fifteen minutes.

## Source policy, declared before the first compile

RECONSTRUCTION, with a pin note per file, as the earlier trees did.
`Kernel.lean` was produced from continuation one's copy by changing only
the outer namespace, and `test_reconstruction.py` compares it
declaration by declaration with the SEALED blobs at the snapshot:
thirty-seven shared declarations, all identical after comments and
namespace lines are stripped and whitespace is normalized.  The
isomorphism structure is not reconstructed here: no statement of this
package needs it.

The Python consumes the sealed kernel, genesis readings, key procedure,
isomorphism witness, automorphisms and brute-force minimum; continuation
one's engine class, generator, responder, growth, switch marker, replay
rule, probe and runner; rung two's class count, observable guard and
label function; and rung ten's holding two, exhausted forms and moved
pairs -- all through their public functions, pinned by blob, with no
source copied.  Continuation one's receipt is rebuilt by its public
`analyse` and compared with its committed bytes before its LIVE and
TWO-KINDED sets and probe signatures are used; it replays.  The
verifiers, the coverage gate and three test files are hand copies of
continuation one's, each saying so in its first lines.

## What is proved, what is computed, what is open

**Proved in Lean** (32 theorems in the package, 17 of them
reconstructions; axioms within `{propext, Quot.sound}` for every one --
two with none, seventeen with `propext` alone, thirteen with both -- and
no `Classical.choice` anywhere).  For EVERY history of sealed events and
switch markers, whoever chose it, and so for every run of every engine
of the class at every bound: no step lowers the element count and every
step that changes the regime raises it; the switch marker keeps the
regime and two of them return the state; a history leaves the element
count unchanged exactly when it leaves the regime unchanged; after a
history that changes the regime no further history reaches the first
regime; every cycle of states holds one regime throughout.  And, added
after the prediction: a pair collapsed with a common third datum is not
separable in any regime.

**Computed** at the declared bounds (two items, arity two, unpruned;
growth below four data; fifteen rounds; two hundred and fifty nodes per
run): 288 runs, 25,932 nodes, 69,490 edges, 43,846 merges; 370
FIXPOINT, 758 REFUSAL, 368 BOUND and 11,266 GUARD nodes; 128 runs
terminate, 44 cycle and 116 are not closed.

- Every node and edge replays; the quotient check finds no defect over
  the 43,818 merges it could read; 28 merges in four E-four runs at F
  were not readable within rung two's observable budget and are listed.
- The eighty quiet engines never respond; the sixty-four that respond at
  both readings are exactly continuation one's LIVE members.
- The runs of E-four with HALT at L are, as reasoned by hand before the
  run, chains that separate and collapse the two data forever, each
  collapse by a uniform rule ending at a fixpoint.
- Eight engines carry forward at both readings, the E-four members with
  HALT or growth alone; four of them, with HALT, declare the stake and
  not the stream.
- No response ever carries a datum.
- 772 refused apart demands, every one of the transitivity shape the new
  Lean lemma closes; 970 refused same demands, not classified.
- Thirty-five run-isomorphism classes, refining continuation one's ten
  probe classes; member-one and member-two twins never differ.

**The census's FORCED column** (full table in `CLAIM_LEDGER.md`,
CEN-1 to CEN-13).  Over the class, two-ness, the class count, symmetry
and exhaustion are FORCED at round zero, exhaustion at round one too,
and NOT FORCED at every later round; branching is NOT FORCED at every
round.  Of the run readings, an invariant (the
element count) and irreversibility are FORCED AT BOUND by computation and
FORCED at every bound by proof; every other run reading is NOT FORCED
over the class, each with an executable countermodel.  Over the LIVE
members, two-ness is FORCED outright: every path of every LIVE run comes
to hold two before any bound or guard.  Succession and duration are not
functions of the state: one node of E-one with `mu1`, member one and
switch alone, at F, is reached by five and by six rounds.

**Open, named and priced** (H-1 to H-9 below, and the leftovers carried
from earlier trees).

## Superseded, dated 2026-09-28, and left standing

No earlier receipt is revised.  Continuation one's G-1, G-2 and G-7 are
answered here at the declared bounds; its receipt, its probe and its
sentence "No engine is run forward" stand as written at its attempt.
Rung two's E-six invariance stays OPEN: the quotient check found no
label disagreement at any merge of an E-six run it could read, which is
a finite computation over merges, not a proof of invariance.  The run's
draft paper and ledger under `research/second/` say that attempt two
had not begun; they are the designated closeout session's to reconcile,
and this tree does not write them.

## The frozen predictions, scored

Nineteen computational rows, scored mechanically by `run_forward.py` and
recorded in `receipts/forward.json`:

| row | value | verdict |
|---|---|---|
| R-5 | 144 engines, 108 seed-literal, 288 runs | HIT |
| R-6 | zero replay mismatches, zero quotient defects, zero key disagreements; **28 merges unchecked** | MISSED |
| R-7 | the responding engines are exactly the sixty-four LIVE; eighty quiet | HIT |
| R-8 | every quiet run has the predicted shape and is closed | HIT |
| R-9 | E-four, `mu2`, HALT at L: 23 nodes, 30 edges, 7 FIXPOINT, 1 BOUND | HIT |
| R-10 | E-four, `mu1`, HALT at L: 53 nodes, 76 edges, 21 FIXPOINT, 3 BOUND | HIT |
| R-11 | no E-four run closed, no switch-holding E-one, E-two, E-three, E-five, E-nine run closed; E-six with switch alone closed at L | HIT |
| R-12 | every E-four run under `mu1` at F meets the node guard | HIT |
| R-13 | eight carriers, four streamless; minima E-four `mu1`/`mu2`, member one, HALT, count six; no initial member | HIT |
| R-14 | no response carries a datum | HIT |
| R-15 | seventy-two of seventy-two twins run-isomorphic | HIT |
| R-16 | **thirty-five** run classes, not thirty-six; the run partition refines the probe partition | MISSED |
| R-17 | the stage verdicts over the class, round by round | HIT |
| R-18 | **succession under CHANGING and duration NOT FORCED**, not OPEN; the other rows as predicted | MISSED |
| R-19 | invariant and irreversibility FORCED AT BOUND; every cycle made of switch edges | HIT |
| R-20 | over LIVE, adjacency and reach NOT FORCED, first failing at **E-three, `mu1`, member one, growth and switch**, not E-four with HALT; both hold at F | MISSED |
| R-21 | seventy-four engines stage-forced at every complete round | HIT |
| R-22 | the four count candidates never lowered anywhere; the class count lowered in each active engine but E-six's | HIT |
| R-23 | the four streamless carriers | HIT |

Five rows are scored where their evidence lives and are marked so in the
receipt: R-1 to R-4 by `verify_lean.py`, `test_census.py` and
`test_reconstruction.py`, all met; R-24 by `run_forward.py --check`, the
replay counts and the measured time below, met.

**A scorer defect, corrected and recorded.**  The first full run scored
R-13 MISSED.  The values were the predicted ones; the scorer compared
the list of carriers in class order with a sorted list.  The comparison
was corrected to compare sorted lists, and R-23's likewise; no value and
no prediction changed.  It is recorded here because a scorer corrected
after it has spoken is exactly the move a frozen prediction exists to
forbid, and the difference is visible: the list the scorer read is in
the receipt, in class order.

**Fifteen of nineteen, and what the misses say.**  R-9 and R-10 were
reasoned by hand to depth fifteen and hit exactly, so hand reasoning
reached the chains of E-four at L.  It did not reach reading F, where
the misses live: a response that admits two uniform rules at once and
two that admit them one at a time reach one state, so the state cannot
count its rounds (R-18); a flipped E-three state at three data holds an
apart demand no delta can answer (R-20); two rules reading different
observables give one run under `mu2` (R-16); and the observable budget
of rung two refuses some merges' regimes (R-6).  Each miss is a finding
about the object, not a defect of the run.

### The census prediction

`PREDICTIONS.md` named thirteen native Lean targets and a class for
each, frozen before the compile.  All thirteen exist and are classed as
predicted: four DEFINITION, eight THIN, one CONTENT
(`ereplay_regime_eq_of_elems_eq`).  Two native theorems were added after
the prediction and are unpredicted work: `collapsed_through` (DEFINITION)
and `not_separable_through` (THIN), written so that the structural
refusal shape rests on a proof rather than on prose.  The classifier and
the predictor are the same session; the census records a judgement.

## Found live

**The observable budget of rung two is the cost of this run.**  Rung two
reads one orbit by enumerating every datum and form bijection of the
identification tree, with no refinement, and nearly all of the run's
time is spent there.  Built serially the class takes about twelve
minutes; the receipt check therefore builds its runs in worker
processes, and the receipts do not depend on how many.

**A replay check that could crash.**  The first version of
`replay_mismatches` raised when a tampered history was inadmissible
instead of naming it; the negative test found it before any receipt was
committed, and the check now names the node or edge.

**The full export is scanned, not skipped.**  The compressed full export
holds bytes a text scanner refuses; the write-root scans decompress it
and scan the text it holds.

## Gates and timing

Measured on this machine, 2026-09-28, by `python ci/run_gates.py --step
"continuation 2" --keep-going` at `6b85f3f0`, which ran the four
registered steps of this tree in the workflow's order, while another
session's processes were running on the same machine:

| gate | command | measured |
|---|---|---|
| clean Lean build and axiom audit | `python3 research/second_run/verify_lean.py` | 57.9 s |
| pins, spans, frozen texts | `python research/second_run/verify_pins.py` | 8.0 s |
| tests under coverage, coverage gate, receipt comparison | the tree's replay, tests and coverage step | 400.4 s |
| strict typing | `python -m mypy` | 1.7 s |

Grouped measured time **468.0 seconds**, inside the fifteen-minute
ceiling the seed sets.  The first measurement, at `702a4ab8`, was
**944.9 seconds, over the ceiling**; three changes brought it inside,
none of which weakens a check: the write-root identifier scan tests for
a name before running its regex over the decompressed full export (a
token match contains its name); the pin verifier reads a path at a full
commit id once per process (such a read cannot change; reads at HEAD,
which the battery mocks, still go to git each time); and the receipt
check may use sixteen worker processes (the receipts do not depend on
the number).  The first two are departures of these hand copies from
continuation one's, and each file says so.

Coverage over the declared measured set (`fwd_census.py`, `fwd_runs.py`,
`run_forward.py`, `verify_pins.py`): **line 99.77%, branch 99.03%**,
both above the 95% floor.  The registered test floor is 150; the suite
ran 161 tests in the measured run.  The runner reported that the interpreter's pytest
(9.1.1) differs from the pin in `requirements.txt` (9.0.3); this tree's
tests run under `unittest` and do not import pytest.

Sixteen injections proved the gates this tree adds, each failing on its
defect and recovering; they are recorded in `research/second/MANUAL.md`,
where two are recorded as failing by the test's name rather than by
naming the injected edit.  The root prose watchlist is clean and matches
its pin; the root identifier firewall and the gates-skill test pass; the
generated views are current, and the estate custody pin gains this
tree's verifier.

These are local receipts.  Hosted CI is permanently disabled by author
decision; the workflow is the written contract and its steps were run
here by the repository's own runner.

## Terminal scope

- `RUNS_BUILT` -- FINITE_COMPUTATION, 288 runs to the declared bounds, every terminal by kind, every frontier exported.
- `REPLAYED` -- FINITE_COMPUTATION, every node and edge; quotient defects none over the merges readable, 28 unreadable.
- `NO_RETURN` -- PROVED_THEOREM, every history of every engine.
- `CENSUS_FORCED_DECIDED` -- FINITE_COMPUTATION and COUNTERMODEL, all twelve rows, every set, both readings, every round.
- `TWO_NESS_FORCED_ON_LIVE` -- FINITE_COMPUTATION, holding at every bound.
- `STREAMLESS_CARRY` -- FINITE_COMPUTATION, four engines, at the declared bounds only.
- `SUCCESSION_NOT_A_STATE_FUNCTION` -- COUNTERMODEL.
- `REFUSAL_SHAPE` -- PROVED_THEOREM for the shape, FINITE_COMPUTATION for its census.
- `INPUT_COUNT_AT_BOUNDS` -- RECORDED, no floor proof, no unbounded reduction.
- `OBSTRUCTIONS_UNTOUCHED` -- RECORDED.

```yaml
steps_completed: [Declare, Reconstruct, Run, Replay, Census, Carry, Crosscheck, Register]
write_root: research/second_run/
snapshot: b368f28c39ec85798ddc5c1bb2dfe3106770bc72
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
prompt_sha256: 3fd06a04a81e39ee3e9b650fd34f76e0d01788559c7d7f21472ee9a2967a9810
predictions_sha256: 086bcee42d86e31f7d488626c814005a7e5da263310d1aa6866f0c498e79e594
attempt: continuation two of two, under the author's ruling of 2026-09-25
runs: {engines: 144, runs: 288, nodes: 25932, edges: 69490, merges: 43846}
terminals: {fixpoint: 370, refusal: 758, bound: 368, guard: 11266}
closure: {terminates: 128, cycles: 44, not_closed: 116}
carriers: {both_readings: 8, streamless: 4}
run_classes: 35
lean_theorems: {total: 32, reconstruction: 17, definition: 5, thin: 9, content: 1}
predictions_scored: {hit: 15, missed: 4, elsewhere: 5}
census_prediction_scored: {named: 13, hit: 13, missed: 0, unpredicted_native: 2}
input_count: {value_at_bounds: 1, reading: "carries forward, literal", proof: none, sentence: "At the declared bounds four engines carry forward declaring the stake and not the stream; this is not a floor proof and not a reduction outside those bounds."}
census_rows_decided: [two-ness, class count, succession, duration, adjacency, reach, invariant, irreversibility, symmetry, branching, exhaustion, recurrence]
injections: 16
gate_time_seconds: 468.0
authority_effect: None
final_state: true
```

## Leftovers, named and priced, executed nowhere

- **H-1, the carriers past the bounds.**  Whether the runs of the four
  streamless carriers go on past fifteen rounds and two hundred and
  fifty nodes.  For E-four with HALT at L the run is a chain whose next
  link is reasoned by hand; a Lean statement of that chain would need the
  responder in Lean (G-4).  Price: large.
- **H-2, the refused same demands.**  970 counted and not classified:
  whether each is refused by the two-item bound or by structure.  Price:
  moderate; a search at three items, or a proof of a shape.
- **H-3, the twenty-eight unchecked merges.**  A label check within a
  budget that refines before it enumerates.  Price: small, but it changes
  a sibling's observable, which this tree may not do.
- **H-4, the 482 regimes above the brute-force limit.**  Price: large
  factorial cost, or a proof that the key procedure is exact.
- **H-5, a distance on adjacency.**  The seed's question seven asks for
  one; none was declared here.  Price: a declaration and its census.
- **H-6, a reading of carrying forward that admits switch.**  Under it
  the switch-holding runs that never close would be counted.  Price:
  small, and a declaration.
- **H-7, closed runs with cycles under ONE VALUE PER NODE.**  Forty-four
  runs are UNDECIDED by the frozen reading; the supplementary pass finds
  one value per node on every one.  Price: small, a declaration.
- **H-8, the run of E-one and E-five under `mu2` with switch alone.**
  Why two rules reading different observables give one run.  Price:
  small, a comparison of their labels on the states reached.
- **H-9, five data.**  Rung two's X and rung three's I-X stay PENDING.
- Carried from continuation one, unchanged: G-3, G-4, G-5, G-6, G-8,
  G-9.  G-1, G-2 and G-7 are taken here.
- Carried from rungs three to ten, unchanged: S-1 to S-5, T-1 to T-3,
  U-1, U-2, V-1 to V-3, W-2, W-3, Z-2, Z-3, Z-5, Y-1, Y-2, Y-4, X-1, X-2,
  X-4.

## The attempt budget, counted and dated

The author's ruling counts the original budget by distinct research
attempts: twelve, spent.  It authorizes at most two more in an
explicitly identified continuation.  This is the second.  No further
attempt is authorized, and none is started here.  The run's paper,
change log and claim ledger belong to a designated closeout session, not
to a research attempt; the author approves the final snapshot.
