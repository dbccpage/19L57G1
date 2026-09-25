# STATUS: rung nine -- two-ness and the observational classes

`AuthorityEffect: None`.  Counts in this file are dated 2026-09-25.  A
receipt is not a proof; a pin proves only that a source did not move; a
gate is proved by the defect it fails on, and every injection this rung
ran is recorded in `research/second/MANUAL.md` with its observed failure.

## The question, and where it came from

Rung three's leftover X-6, quoted verbatim in `CLAIM_LEDGER.md` from two
pinned spans: rung three's own text, and the six rows rung eight carries.
Rung eight's application of the seed's next-rung rule, pinned as a third
span, selects it as the only eligible leftover: it extends the census of
challenge five, and no leftover reduces the count of declared inputs.

**The reading applied, recorded before the predictions.**  Rung eight
left for the author, without making it, the reading of a leftover that
carries six rows.  This rung recorded its own reading in `PROMPT.md`
before `PREDICTIONS.md` was frozen: it took the rows in the order rung
three named them and decided the first two, two-ness and observational
classes, which are both read off the profile of an admitted datum and
need no response.  The next row, adjacency, is declared by the seed
through a response.  The reading binds no later rung, and the author may
reject it.

`research/second/PLAN.md` item five assigns "run forward" and the census
to rungs four and five.  As in rungs three to eight, this rung follows
the seed's rule, which the plan's item six defers to, and not the list;
the plan is not edited.

## Source policy, declared before the first compile

RECONSTRUCTION, with a pin note per file, as rungs three to eight did.
`Kernel.lean` reproduces the sealed kernel slice from `Basic.lean` and
`Inertia.lean`, and `IsoKernel.lean` the sealed isomorphism structure
from `Minimality.lean` lines 169-224; both were produced from rung
eight's copies by changing only the outer namespace, and
`test_reconstruction.py` compares them declaration by declaration with
the SEALED blobs at the snapshot: 41 shared declarations, all identical
after comments and namespace lines are stripped and whitespace is
normalized; the omitted declarations are pinned by name.

One statement of this package repeats an earlier rung's lemma --
`getD_append_lt`, rung five's, proved again at rung eight -- and one
definition repeats rung eight's, `isoSymm`; both are stated again so
that the package imports nothing, and the ledger and the census note
credit them.  The Python consumes the sealed kernel, the sealed profiles
and separability, the sealed genesis readings, rung three's bases and
rung four's population, keys and partition comparison through their
public functions and copies no source of any of them.  The verifiers,
the coverage gate and four test files are hand copies of rung eight's,
each saying so in its first lines.

## What is proved, what is computed, what is open

A regime HOLDS TWO when some two of its admitted data are separable in
the sealed sense.  A REPRESENTATIVE LIST of a regime is a list of
admitted data, any two at different positions separable, with every
admitted datum collapsed with some entry.

**Proved in Lean** (50 theorems in the package, 17 of them
reconstructions; axioms within `{propext, Quot.sound}` for every one --
three with none, twenty with `propext` alone, twenty-seven with both --
and no `Classical.choice` anywhere):

- a context carried along an inhabitant of the sealed isomorphism stays
  well formed, and for an admitted datum its plugging is derivable
  exactly when the carried plugging is; so separability and collapse of
  two admitted data are carried to their images, holding two is kept in
  both directions, and a representative list is carried with its length,
  with no hypothesis on either regime;
- collapse is reflexive, symmetric and transitive;
- holding two needs two data, a form and an instance; no history of
  fewer than four events from the sealed empty regime, or of fewer than
  two from either sealed reading regime, reaches it; both bounds are
  attained by exhibited histories;
- a supply, a datum, a form and a requirement keep every separable pair
  separable, on every regime.

**Countermodels in Lean**: an instance admission and a rule admission
each end holding two, on an exhibited well-formed regime; the first
needs an argument over every context and is not a kernel computation.

**Computed** over rung three's rectangle -- three bases, 18798
sequences, 2316 distinct regimes, 402 classes of regimes:

- the least length holding two is four at EMPTY and two at L and at F;
  22, 2036 and 8676 sequences hold two, reaching 6, 315 and 1240
  regimes in 3, 82 and 156 classes;
- a regime holds two exactly when its class count is at least two; the
  largest class count is two, three and four at EMPTY, L and F, and no
  regime has more classes than data or than its named data plus one;
- no class of regimes carries two values of holding two or of the class
  count, within a base or over all three;
- holding two is never ended at EMPTY within the bound; at L it is
  ended 28 times by an instance and 126 times by a rule, at F 6 and 370
  times, and by no other kind; the class count changes by zero under a
  supply, a requirement and a form, by zero or one under a datum, by
  minus two to zero under a rule, and by minus one to two under an
  instance.

**Open, named and priced** (T-1 to T-3 below, and the leftovers carried
from rungs three to eight).  The class count as a number in Lean is not
formed (T-1).

## Superseded, dated 2026-09-25, and left standing

No earlier receipt is revised, and no earlier OPEN statement is closed.
The two rows decided here were named undecided by rungs three to eight,
and each of those sentences stands as written at its rung.

## The frozen predictions, scored

Seven computational rows, scored mechanically by `run_profile.py` and
recorded in `receipts/profile.json`:

| row | value | verdict |
|---|---|---|
| Q-8 | 577, 3928, 14293 sequences; 75, 523, 1718 regimes; 0 replay mismatches; 54, 174, 265 classes within base; 402 over 2316 regimes; 0 key and brute-force disagreements | HIT |
| Q-9 | least length four, two, two; at EMPTY 22 sequences, 6 regimes, 3 classes hold two | HIT |
| Q-10 | 0 mismatches between holding two and a class count of at least two | HIT |
| Q-11 | largest class count two, three, four; 0 regimes above their data, 0 above their named data plus one | HIT |
| Q-12 | 0 classes of regimes with two values of holding two or of the class count, within any base and over all three | HIT |
| Q-13 | no ending transition at EMPTY; at L and F exactly instance and rule admissions | HIT |
| Q-14 | changes by kind: supply, requirement, form {0}; datum {0, 1}; rule {-2, -1, 0}; instance {-1, 0, 1, 2} | HIT |

Eleven rows are scored where their evidence lives and are marked so in
the receipt rather than omitted: Q-1 to Q-6 by the statement-shape tests
of `test_census.py` and by `verify_lean.py`; Q-7 by the committed axiom
log; Q-15 to Q-17 by `CLAIM_LEDGER.md` and `test_census.py`; Q-18 by
`run_profile.py --check`, `test_profile.py` and the measured time below.
Each is met.  Five rows were labelled FORCED before the run, and a hit
on a FORCED row evidences the order of the work, not insight.

**A value the prediction allowed and the rectangle did not reach,
recorded.**  Q-14 allowed an instance admission to lower the class count
by two, and none does within the bound; the prediction is a hit on its
falsifier, and the unreached value is recorded in `CLAIM_LEDGER.md`
PRF-20 and pinned by `test_no_instance_admission_lowered_the_count_by_two`.

### The census prediction, and its four misses

`PREDICTIONS.md` named 33 Lean targets and a class for each, frozen
before the compile.  All 33 exist.  Scored mechanically by
`test_census.py`: **29 hits, 4 misses, no unpredicted native theorem**.
One DEFINITION row, `two_classes_at_four`, is longer than the line bound;
it is kernel computation and case exhaustion over one concrete regime,
and is listed in `long_but_definitional` with the reason.

| target | predicted | recorded | why |
|---|---|---|---|
| `derivable_mapCtx` | CONTENT | THIN | one rewrite by `plug_mapCtx`, then `derivable_fwd` and `derivable_bwd` |
| `collapsed_iso` | CONTENT | THIN | `derivable_mapCtx` applied twice along the exchanged structure, then the equivalences chained |
| `reps_iso` | CONTENT | THIN | `separable_iso` and `collapsed_iso` applied to the three clauses of a representative list |
| `replay_parts_le` | CONTENT | THIN | an induction closed by `step_parts_le` and arithmetic alone, which rung seven's rule, applied at rung eight, classes THIN |

**What the misses say.**  Every miss is a DEMOTION, rung three's
recorded mistake met again: the carrying of observation along the
isomorphism sits in no single statement but in the small pieces --
`plug_mapCtx`, `wfCtx_mapCtx`, `plug_args_lt`, `derivable_bwd` -- and
the headline statements assemble them.  The two CONTENT rows are
`separable_step_keep` and `twoness_lost_by_inst`.  The census is total
over the package and checked in both directions, so a later silent
promotion is visible.

## Found live, before any injection

**The `omega` tactic reaches `Classical.choice` on some goals.**  The
first complete build passed, and its axiom reports named
`Classical.choice` for seven theorems: `step_parts_le`,
`replay_parts_le`, the three lower bounds that rest on it,
`holdsTwo_step_keep`, and `two_classes_at_four`.  In the toolchain on
this machine, `omega` closing a goal that is a CONJUNCTION, or closing a
goal that is not arithmetic at all by finding its hypotheses
contradictory, reports `Classical.choice`; the same tactic closing one
arithmetic goal does not.  Each use was rewritten to close one
arithmetic conjunct at a time, or to close `False` and discharge the
goal by `absurd`.  The frozen prediction Q-7 is met by the package as
committed; it would have missed on the first build.
`test_q7_no_omega_closes_a_conjunction_or_a_non_arithmetic_goal` reads
the text for the two repaired shapes; it is a text check and not a
proof, and the proof of the whitelist is `verify_lean.py` on a fresh
build.  Rung eight recorded three library lemmas reaching
`Classical.choice`; this is a tactic, and the handoff says so.

**A module name that shadows the standard library.**  The computation
module was first written as `profile.py`, the name of a module of the
standard library; it was renamed `profile_rows.py` before anything
imported it.

## Leftovers, named and priced, executed nowhere

- **T-1, the class count as a number in Lean.**  That any two
  representative lists of one regime have one length.  Needs a decision
  for collapse at a regime, which is rung three's X-1, or a counting
  argument that does not decide it.  Price: small after X-1.  It refines
  the classes row this rung decides and extends no row of the census.
- **T-2, the change of the class count by one event, in Lean.**  The
  rectangle shows each kind's changes (PRF-20): none under a supply, a
  requirement or a form, at most one up under a datum, never up under a
  rule, and at most two either way under an instance, with minus two
  never reached.  None of it is proved.  Price: moderate.  It refines the
  classes row and extends no row of the census.
- **T-3, holding two under an engine.**  Whether an engine's rounds
  reach or keep holding two -- the FORCED column of both rows.  Price: a
  rung, and it needs the engine of X-5 first.
- Carried from rung eight, unchanged: U-1, U-2.
- Carried from rung seven: V-1, V-2, V-3 (narrowed at rung eight).
- Carried from rung six, unchanged: W-2 and W-3.
- Carried from rung five, unchanged: Z-2, Z-3 and Z-5.
- Carried from rung four, unchanged: Y-1, Y-2, Y-4.
- Carried from rung three, unchanged: X-1, X-2, X-4, X-5, and X-6 less
  symmetry, invariants, irreversibility, succession, duration,
  recurrence, two-ness and observational classes: adjacency, reach,
  branching and exhaustion.

**A remark for the rung that takes X-6 next, recorded and not acted
on.**  This rung's reading said no responder is declared in this run.
The sealed estate has one -- the candidate space of one-step
augmentations and its minimum responses under the two declared cost
measures -- which the seed lists among the supplied objects.  Whether
that sealed responder is the response the seed's adjacency, reach and
branching rows speak of, or whether those rows wait on X-5, is for that
rung to decide and record.

## The rung budget, counted and dated

The seed allows at most twelve rungs to be attempted.  This is the
tenth rung ordinal, zero to nine; rung two ran as two tracks under one
ordinal, so eleven rung trees exist.  Counted by ordinal, two rungs
remain; counted by tree, one.  Which count the seed means is not
decided here and is recorded for the author.

## Gates and timing

Measured on this machine, 2026-09-25, by `python ci/run_gates.py --step
"rung 9" --keep-going` at `e9bf4b6d`, which ran the four registered
steps of this rung in the workflow's order:

| gate | command | measured |
|---|---|---|
| clean Lean build and axiom audit | `python3 research/second_profile/verify_lean.py` | 61.5 s |
| pins, spans, frozen texts | `python research/second_profile/verify_pins.py` | 7.8 s |
| tests under coverage (141 tests), coverage gate, receipt comparison | the rung's replay, tests and coverage step | 159.5 s |
| strict typing | `python -m mypy` | 2.1 s |

Grouped measured time **230.9 seconds**, inside the fifteen-minute
per-rung ceiling the seed sets.  Most of the test step is the pin
battery.  The Lean row is a CLEAN build: `lake clean`, a full rebuild,
then the compiled-environment census.  Coverage over the declared
measured set (`profile_rows.py`, `run_profile.py`, `verify_pins.py`):
**line 99.07%, branch 95.95%**, both above the 95% floor.  The runner
reported that the interpreter's pytest (9.1.1) differs from the pin in
`requirements.txt` (9.0.3); this rung's tests run under `unittest` and
do not import pytest.

These are local receipts.  Hosted CI is permanently disabled by author
decision; the workflow is the written contract and its steps were run
here by the repository's own runner.  The estate custody census, run on
the clean worktree when its pin was rewritten, reports 106 verifiers,
105 green and one pinned red that this rung did not add.

## Terminal scope

- `OBSERVATION_CARRIED` -- PROVED_THEOREM, separability, collapse, holding two and representative lists, every inhabitant of the sealed isomorphism, no hypothesis on either regime.
- `COLLAPSE_IS_AN_EQUIVALENCE` -- PROVED_THEOREM, at the level of a definition.
- `TWONESS_NEEDS` -- PROVED_THEOREM, two data, a form and an instance.
- `TWONESS_FIRST_STAGE` -- PROVED_THEOREM for the bounds, four from the empty regime and two from each reading regime; DEFINITION for the witnesses.
- `TWONESS_KEPT_BY_FOUR_KINDS` -- PROVED_THEOREM, every regime.
- `TWONESS_ENDED_BY_TWO_KINDS` -- COUNTERMODEL, one exhibited regime each.
- `RECTANGLE_MEASURED` -- FINITE_COMPUTATION, the frozen rectangle only.
- `CLASS_COUNT_AS_A_NUMBER` -- OPEN in Lean (T-1); FINITE_COMPUTATION on the rectangle.
- `CENSUS_TWONESS` -- one row decided, DEFINABLE, conditional on an engine for FORCED.
- `CENSUS_CLASSES` -- one row decided, DEFINABLE as a relation, the number OPEN in Lean, conditional on an engine for FORCED.
- `INPUT_COUNT_UNCHANGED` -- RECORDED, value two, no proof of a floor, no reduction.
- `OBSTRUCTIONS_UNTOUCHED` -- RECORDED.

```yaml
steps_completed: [Reconstruct, Carry, Classes, Stage, Keep, Rectangle, Census, Register]
write_root: research/second_profile/
snapshot: ff584d441caad8300d01cbfda8b316846a8b5fc4
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
prompt_sha256: df68d1cc735c3bfc8559e3dd96e3fc93b02f008cfdcb0679bbb1b19b8575a5f7
predictions_sha256: 7fc9a68c6447a7df85c0ff3ea3f4b7092045c0e7e6d847158b69cc469a539499
bases: [EMPTY, L, F]
sequences: {EMPTY: 577, L: 3928, F: 14293}
regimes: {EMPTY: 75, L: 523, F: 1718}
classes: {EMPTY: 54, L: 174, F: 265, all: 402}
lean_theorems: {total: 50, reconstruction: 17, content: 2, thin: 21, definition: 10}
predictions_scored: {hit: 7, missed: 0, elsewhere: 11}
census_prediction_scored: {named: 33, hit: 29, missed: 4, unpredicted_native: 0}
input_count: {value: 2, proof: none, sentence: "This rung neither reduces the count of declared inputs nor proves it at a floor."}
census_rows_decided: [two-ness, observational classes]
census_rows_extended: []
gate_time_seconds: 230.9
authority_effect: None
final_state: true
```

## The next rung, named so it cannot be smuggled in later

The seed's rule takes the smallest named leftover that EITHER reduces the
count of declared inputs OR extends the census of challenge five, and on
a tie the one named first -- first in the list below, by the author's
ruling of 2026-09-25.  A leftover refining a decided row is not
eligible, as rungs six to eight read it.

| leftover | reduces the input count | extends the census | price | eligible |
|---|---|---|---|---|
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
| X-6 the undecided rows | no | yes | large | yes |

One leftover is eligible, so the next rung is **X-6, the undecided rows
of the census**, now four -- adjacency, reach, branching and exhaustion,
in the order rung three named them.  The reading of a leftover carrying
several rows stays the author's to settle; this rung's reading is
recorded above and binds no later rung.  The remark above, on the
sealed responder, is for that rung.

As rungs three to eight recorded, X-1 is the leftover the others keep
waiting on -- T-1 and Y-2 now among them; it is not eligible on the
plain reading of the rule, and it is recorded here again rather than
taken.  Nothing of any leftover is started here.
