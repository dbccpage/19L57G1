# Record reading: an enablement that reads the retained record, and a class of laws selected against

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.
Not registered in `.github/workflows/verify.yml`: its checks run locally
through `verify.py` (section 5).

**Result.**  The represented execution family's machine retains a tape and
named its next obstacle: no enablement reads it.  Here one does.  A recorded
setting's enablement `hctrl p x k` — operation `k` may fire at datum `x`
when the datum before it on the record is `p` — is represented in the same
device, one binary form per operation, by the instance
`(3 + nops + k, [p, x])`; the program is a well-formed regime
(`encodeR_wf`); the interpreter is the merged one with one change, that it
reads the record before the edge (`renabled`, `previous`), and the record
it reads is what the last firing wrote (`previous_fire`) — no host log.
Simulation and reflection hold against the reference step stated on the
setting (`rsuccessors_sound`, `rsuccessors_complete`); the runner never
selects (`rrun_branch`) and only appends (`robs_prefix`); the memoryless
class embeds (`lift_RStep`, `lift_renabled`).  **The distinction is real
and disappears with the record**: on the observed family's setting the
program `twist` visits `0, 1, 0, 0` from datum 0 — at its third step it is
where it started and leaves another way (`record_is_read`) — which no run
of the merged machine does (`memoryless_functional`), and forgetting the
record collapses the run to `[0, 1]` (`forget_twist`).

**A class of laws and a discriminating input.**  One step of the merged
runner is fixed by its *next value* at the active datum (`stepDet_spec`),
so two states with the same next-value function, datum, record and fuel
have the same observation at every scale (`obs_bisim`): the tape identifies
a law up to its next-value function and no finer.  The ambiguity is
exhibited — the cycle everywhere and the climb at 0 differ as programs and
are indistinguishable from every start at every scale
(`forever_indistinguishable`); that is the missing axiom, an observable that
reads which operation fired.  The discriminating input is exhibited — a
record-reading program agreeing with the lifted cycle at the seen
observation is separated at scale 4 and from datum 2 (`turncoat_*`).  The
experiment, declared before the readout: on the memoryless class (64 laws)
the seen observation `[0, 1, 2, 0]` retains 8, no declared input separates
them, 1 residual class; on the record class (262144 laws) it retains 32768,
three greedy experiments separate them into 45 residual classes (largest
4096), and the residual is exactly the next-value function on the pairs the
runs reach, checked against the programs.

Lean: 117 authored theorems, 151 reports with the compiler-generated ones,
all within `{propext, Quot.sound}`, in a package importing the sealed
package and the observed family's package.  Python: the machine mirrored;
the artifact read through the observed family and never written, every
run recorded with its operation tables in index order; 83 tests, strict
typing over eleven files, two byte-identical records.  Base
`9fa450d01e436687de5a3549e8a7c80cb390e207`, the observed family's commit
with its obligations discharged, at which both consumed families are frozen and pinned; no sealed path and
no sibling path is written.  (2026-09-25: the base was `6df9aa31`, the
commit named above until then.  It moved to the commit that corrects only the
observed family's `README.md` registration line; no consumed source, tree
census or digest other than that directory's tree object moved.)

## 1. The record read (`lean/Record.lean`)

| definition | content |
|---|---|
| `Recorded`, `RStep` | a setting with a record-reading enablement; the reference step, before any encoding |
| `recInsts`, `rprogram`, `encodeR` | the instances `(3 + nops + k, [p, x])`; the program; the regime |
| `present`, `renabled`, `renabledAt` | the read: presence of the instance — a relation, not a function |
| `previous` | the entry before the last on the record; the start its own predecessor |
| `rsuccessors`, `rstepDet`, `rrun`, `rinit` | the family, the runner, the initial state; `fire` is the merged one |
| `Synced` | a state whose record ends with its active datum |
| `lift`, `forget` | the memoryless class read as recorded; the record forgotten |
| `twist` | the cycle at 0 after 0, the constant map at 1 after 0 and at 0 after 1 |

| theorem | content |
|---|---|
| `encodeR_wf`, `mem_rprogram` | the program is a well-formed regime (CL-RR-01) |
| `present_iff`, `renabled_rprogram` | the read is faithful, as a relation (CL-RR-02) |
| `previous_fire`, `fire_synced`, `previous_rinit` | **the record is what the process wrote** (CL-RR-03) |
| `rsuccessors_sound`, `rsuccessors_complete`, `rrun_branch`, `robs_prefix` | simulation, reflection, never selects, only appends (CL-RR-04) |
| `lift_RStep`, `lift_renabled` | the memoryless class embeds (CL-RR-05) |
| `twist_tape`, `record_is_read`, `memoryless_functional` | **the distinction**, and its impossibility without the record (CL-RR-06) |
| `forget_twist` | the record forgotten, the distinction gone (CL-RR-07) |
| `triplesOf`, `lastTwo`, `RChain`, `rchain_functional`, `rnext_chain`, `riter_chain`, `robs_functional` | **the ceiling of a depth-one read**: every realised tape is functional in its pairs (CL-RR-12) |

## 2. The selection (`lean/Select.lean`)

| definition | content |
|---|---|
| `nextValue` | the value of the one enabled operation at a datum, or none |
| `Rel` | same next-value function, datum, record, fuel |
| `climbFirst`, `turncoat` | the ambiguous partner of `forever`; the discriminated partner of its lift |

| theorem | content |
|---|---|
| `stepDet_spec`, `obs_bisim`, `obs_take` | one step by its next value; **the observation is a bisimulation invariant**; the finest scale suffices (CL-RR-08) |
| `Record.rnextOf`, `Record.rstepDet_spec`, `previous_congr`, `RRel`, `rrel_next`, `rrel_iter`, `robs_bisim`, `robs_take` | **the same for the record-reading machine**, with `previous` carried by the record (CL-RR-08's obligation) |
| `forever_differ`, `forever_ambiguous`, `forever_indistinguishable` | **the ambiguity exhibited** (CL-RR-09) |
| `turncoat_agrees`, `turncoat_differs_scale`, `turncoat_differs_start` | **the discriminating input exhibited** (CL-RR-10) |

## 2a. A record read two entries deep (`lean/Depth.lean`)

Reading one entry buys functionality in pairs and no more (CL-RR-12).  Reading
two breaks that ceiling — and it is the first encoding here that is **not
all-binary**: a depth-two enablement needs three data at once, so its control
forms are ternary, `(3 + nops + k, [before, previous, active])`.  The sealed
grammar admits a regime of mixed arity with no new admission, because
`Regime.wf` constrains a form's arity only by `1 ≤ a`.

| theorem | content |
|---|---|
| `formsOf_getD_binary`, `formsOf_getD_ternary`, `formsOf_pos`, `encodeR2_wf` | **a regime of mixed arity is still a regime** |
| `r2enabled_r2program`, `lookup_r2program_op`, `r2successors_sound` | the enablement and the edge are read faithfully; the successors are reference steps |
| `lift2`, `lift2_R2Step` | the depth-one class embeds |
| `twist2_tape`, `no_record_run_realises`, `depth_two_is_deeper` | **a tape no depth-one program realises**: `0, 1, 2, 0, 1, 0`, whose pair `(0, 1)` is followed once by `2` and once by `0` (CL-RR-13) |

### The ceiling of a depth-two read, and the ladder

| theorem | content |
|---|---|
| `r2nextOf`, `r2stepDet_spec` | one step of the depth-two runner, by its next value |
| `R2Chain`, `r2chain_functional`, `r2next_chain`, `r2iter_chain` | the tape of a depth-two run is a chain of a three-argument function |
| `r2obs_functional` | **the ceiling**: every tape a depth-two run realises is functional in its *triples* — three entries determine the fourth |
| `pairsOf_of_triplesOf`, `triplesOf_of_quadsOf` | a window of `d + 1` contains a window of `d` |
| `triples_of_pairs`, `quads_of_triples` | **the ladder only grows**: a tape functional in `d` entries is functional in `d + 1` |
| `twist_repeats_an_entry`, `the_ladder` | and both proved inclusions are **strict**, by the two exhibits |

Three ceilings are now proved — `Observe.obs_functional` for a memoryless run,
`Record.robs_functional` for a depth-one read, `r2obs_functional` for a
depth-two one — and the classes they bound are a chain with two strict steps.
`depth.py` mirrors the machine and computes the ladder exhaustively: over
*every* deterministic program of each depth on a two-point setting at fuel
six, the three depths realise **10, 22 and 70** tapes; every tape meets its
own depth's ceiling, and 8 then 38 of them break the ceiling of the depth
below — which by that ceiling the depth below cannot realise.  The inclusion
is **strict**: the depth below cannot realise 12 and 48, and the extra 4 and
10 are short tapes, runs that stopped before the fuel ran out.  They are
functional at the shallower window; the ceiling says nothing about when a
machine may halt, so it does not reach them.  An earlier version of this
sentence said "exactly the set", which was false.

A machine of depth `d` for `d > 2` is built neither here nor in the Lean, so
the ceiling is proved one rung at a time and not for a general `d`.
`depth.functional` is written for any window size, so the statement checked at
each rung is the same statement.

### Three readers, one runner

The producer family parameterised the interpreter over an enablement reader
`State → List Nat` and asked whether a reader must see more than the state.
This family is the answer twice over: reading one entry of the record needs
`previous s`, reading two needs `before s` beside it, and **both are functions
of the state**.

| theorem | content |
|---|---|
| `Record.recordReader`, `rstepDet_is_generic` | the depth-one machine is the generic runner at its reader, by `rfl` |
| `Record.rrunDet_is_generic`, `robs_prefix_is_generic` | and so is its runner; its compatibility is *derived* from `Runner.obsOf_prefix_add`, not proved again |
| `Depth.depthReader`, `r2stepDet_is_generic`, `r2obs_is_generic` | and so is the depth-two machine |
| `Depth.three_readers_one_runner` | **the three machines are the one machine at three readers** — three `rfl`s |

The rung that asked for this named its own failure: that a reader would have to
see more than the state.  It does not happen, so the copies of the runner in
these files are copies and not obligations, and a fourth read costs a reader
and no runner at all.  `tests/test_depth.py` checks the identification the
Lean states by `rfl`, over every deterministic program of each depth on the
two-point setting.

## 3. The experiment (`selection.py`)

Declared before any readout: two classes (memoryless, at most one operation
per datum; record, at most one per (previous, active) pair), the starts
`0, 1, 2`, the scales `1..8` with fuel 8, and the seen observation — the
artifact's recorded `forever` run from datum 0 at scale 3.  A law is
retained when its own run reads the seen observation; the retained laws are
separated by the declared inputs only, each read as the prefix of one run
per start at the finest scale (`obs_take`); the greedy sequence takes at
each step the input refining the partition most.

| class | laws | survivors | experiments (start, scale → classes) | residual classes | largest |
|---|---|---|---|---|---|
| memoryless | 64 | 8 | none refines | 1 | 8 |
| record | 262144 | 32768 | (1, 6) → 11; (2, 2) → 37; (0, 4) → 45 | 45 | 4096 |

The law that produced the seen observation is in the largest residual class
of each: the record class identifies it least of all.  With one residual
class there is no pair of classes to differ on, so the between-class check is
recorded as not made rather than as vacuously true.

Within every residual class the next-value function read from the program
agrees on every pair the runs reach; between two classes it differs on a
reached pair.  The residual is the operation index on reached pairs and the
enablements on unreached ones — what an observable reading which operation
fired would separate, and the tape cannot.

## 4. The artifact consumed

`research/represented_execution/evidence/process.json` is read through the
observed family's `identify_programs`, never written; the finding that its
schema is set-valued is inherited — the producer has since repaired it, and
the observed family now reads its `ops_in_index_order` — and every run
recorded here carries the same field.  The receipt refuses a setting whose tables
in index order are not the transcribed `Observe.base`.

## 5. Evidence

**Lean** (`lean/`, `evidence/lean.json`): 117 authored theorems and 34
compiler-generated ones (the structure's injectivity and size lemmas and
the proof terms of case splits), 151 reports, all within
`{propext, Quot.sound}`; the report population equals the environment
census of the `Record`, `Select` and `Depth` namespaces in both directions; no
private theorem; forbidden-token scan clean.  The concrete runs are decided
by the kernel on the observed family's transcribed setting.

**Python** (`record.py`, `selection.py`, `run.py`, `evidence/record.json`,
`tests/`): 83 tests, strict typing over the tree's own modules and tests by a
**glob** and not a hand list, the two records replay
byte-identically.  The house files follow the sibling families' with
names, pins and refusals changed; this tree's directory is always first on
the path, and `run.py` and `verify_lean.py` refuse by name if a foreign
guard is imported.

**Custody** (`verify_sources.py`, `SOURCE_MANIFEST.json`): at
`9fa450d01e436687de5a3549e8a7c80cb390e207`, the eight derivation modules and
the consumed `translation`, `execution`, `control` and `limits` modules by
digest and runtime origin; the sealed `lean4/Derivation` tree, the merged
`local_reuse`, `ignition`, `magnification`, `setting_translation`,
`represented_execution` and `coherent_process_limits` Lean trees, and the
`setting_translation`, `represented_execution` and
`coherent_process_limits` Python trees by Git tree object; the Lean
configuration of the seven packages and the represented execution family's
artifact by digest.  An untracked source in any of the eleven trees is
refused.  (2026-09-25: the eleven Git tree pins and the untracked-source
refusal are withdrawn.  The Python trees are pinned through the runtime
modules above, and the Lean trees by the 30 files of the local package's
import closure, each by digest; an edit to a file this family does not read
no longer fails its custody check.)  The two records are `-text` by an in-tree `.gitattributes`.

```powershell
cd research/record_reading
python verify.py     # sources, tests, mypy, lean (lake build + census), record --check
```

Regenerate the two records deliberately and never under a live injection:
`python run.py --write`, `python verify_lean.py --write`.

## Not claimed

* A record read deeper than *two* entries, or a depth-`d` family for general
  `d`: depth two is built (CL-RR-13), depth three is not, and each ceiling is
  proved at its own rung rather than for a general `d`.  An earlier version of
  this line added that "the ceiling of a depth-two read — functionality in
  triples — is not stated"; that is WITHDRAWN, it is `r2obs_functional`
  (CL-RR-14).
* The **bisimulation** of the depth-two machine: the chain invariant is
  stated (CL-RR-14) and the bisimulation is not.  An earlier version of this
  line also said the depth-two machine had no Python mirror and no receipt;
  that is WITHDRAWN — `depth.py` and the record's `depth_two` section.
* An encoded configuration: the state is a declared host record.
* That a shorter separating family exists outside the declared inputs.  An
  earlier version of this line said only that "the greedy experiment sequence
  is a minimum: it is one sequence"; the minimum over the declared inputs is
  now computed and is 3, the same length as the greedy sequence though a
  different set (CL-RR-15).
* An observable the **process writes** that reads which operation fired.  The
  host readout is built and measured (CL-RR-15) and takes the record class's
  residual from 45 classes to 896; a represented field carrying the index is
  not built, and that would be a change to the machine rather than a second
  reading of it.
* That the minimum burden is a minimum over anything but the **declared**
  inputs.
* That the merged memoryless reader applies to a record program: it does not.
  A record program carries several instances of one control form leaving one
  record entry, and `execution.lookup` refuses such a form by name, so
  `control.enabled_at`, `control.step_det` and `limits.obs` must not be
  applied to it.  The dispatch in `selection.py` is what keeps them apart and
  `tests/test_record.py` pins the refusal.
* A second locus of activity.
* That the Python mirrors compute the Lean predicates: the agreement is on
  the stated finite populations.

## Files and running

| file | role |
|---|---|
| `lean/Record.lean` | the record-reading enablement, the interpreter, the reference, the embedding, the distinction |
| `lean/Select.lean` | one step by its next value, the bisimulation, the ambiguity, the discriminating input |
| `lean/Depth.lean` | the depth-two read: ternary control forms, a regime of mixed arity, a tape no depth-one program realises, and the ceiling of a depth-two read |
| `lean/Inventory.lean` | the environment census |
| `record.py` | the machine mirrored, as the producer family's interpreter at `record_reader`; the named programs |
| `depth.py` | the depth-two machine mirrored, windows of a tape, and the exhaustive ladder sweep |
| `selection.py` | the protocol, the classes, the survivors, the burden, the residual; the class of a law is dispatched **once**, in `reader_of`, and every run below goes through the producer family's one interpreter at that reader |
| `run.py`, `evidence/record.json` | the record and its refusals |
| `verify_lean.py`, `evidence/lean.json` | the Lean build, two-way census and reliance record |
| `verify_sources.py`, `SOURCE_MANIFEST.json` | custody of the consumed inputs |
| `verify.py` | every check in order |
| `tests/` | the machine, the experiment, custody, the parser, the records |
| `CLAIMS.md` | one `CL-RR-*` entry per claim |
