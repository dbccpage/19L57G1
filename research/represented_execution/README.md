# Represented execution: represented operations drive a process

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.
Not registered in `.github/workflows/verify.yml`: its checks run locally
through `verify.py` (section 6).

**Result.**  A finite setting is encoded as a regime whose operation graphs
are the instances of binary forms (the merged `setting_translation`).  This
family executes represented programs by *reading those instances*, in two
commits.

*Commit 1, the word machine.*  A configuration carries the encoded graph, the
remaining word of operation indices, the active datum and an output tape;
one `step` consumes the head `k` of the word by looking the instance
`(3 + k, [active, y])` up in the graph and moving to `y`; `run` is `iterate
step` for the length of the word, by definition.  For every finite setting,
every well-formed word and every admitted datum the run halts with the word
consumed and the active datum the operations compute (`run_total`,
`run_encode`) — proved without the machine ever reading the operation
functions `F.ops`, which enter once, in the statement that reading the graph
is faithful (`lookup_encode`, through the merged `derivable_op`).  The
machine is stepwise: a configuration exists after any prefix of the word
(`iterate_add`), and running `u ++ v` is running `u` and continuing with `v`
(`run_append`).

*Commit 2, control by data.*  A controlled setting adds an enablement
relation — operation `k` may fire at datum `x` — represented in the same
device as one more binary form per operation whose *self-instance*
`(3 + nops + k, [x, x])` says `k` is enabled at `x`; the represented program
(operation graphs and enablements) is a well-formed regime of the sealed
grammar (`encodeC_wf`).  A fixed interpreter reads the enablements at the
active datum, then the chosen operation's edge, and moves: which operation
fires is read from the data.  Against the reference step `CStep`, stated on
the setting before any encoding, every successor of a state carrying the
program realises a reference step at its active datum, and every reference
step there with fuel is realised (`successors_sound`, `successors_complete`,
at any such state and not only the initial one).  The deterministic runner fires the one enabled
operation and stops with the terminal `branch` when two are — it never
selects (`run_branch`); its terminals `halt`, `exhausted`, `refuse`, `branch`
are distinct.  The clock advances exactly when an operation edge is applied
and the fuel is spent by one per firing and renewed by nothing (`fire_ok`,
`fire_exhausted`).  The state carries the program only — no store is loaded
— and the initial state does not depend on the designated pair (`init_pair`).
Computed: a branch driven by data, an iteration whose length the data set,
different programs giving different tapes, arbitrarily long runs until the
fuel is spent.  **Not delivered**, and named as the next obstacle: a retained
record that a later operation reads (CL-RE-14).

Configuration status: **DECLARED_HOST_CONFIG**.  `Config` and `State` are
structures of the metatheory whose graph fields are copies of encoded
instances.  The processes read encoded data; they do not themselves live in
the sealed grammar, and nothing here says they do.  (The *program* of commit
2 is a regime; the *state* that runs it is host.)

Lean: 114 authored theorems, 173 reports with the compiler-generated ones, all
within `{propext, Quot.sound}`, in a package importing the sealed package
and the merged `setting_translation` package.  Python: both machines
mirrored; the word machine checked against the merged `translation.run` (the
fold that reads `F.ops`, which the tests may consult and the machines never
do) on every word of length at most three from every datum of the thirteen
sealed settings, the six two-point exhibits, a three-point two-operation
setting and the first 400 settings of the sealed universe; the control
machine's successor family checked against the reference step on every datum
of four programs; the graph mutation, mid-run edit, two-graphs-one-word,
letter-names-an-operation, concatenation, empty-word, branch-by-data,
iteration-by-data, never-selects, family-permutation and fuel tests the
brief names; the named refusals; an oracle check on both machines' source;
109 tests, strict typing over the tree's own nine modules and nine test
files by a glob, two byte-identical records.
Execution base `756917dcaeff5979faa9b1346a1a8ce666b33b25` (main); no sealed
path is written.

## 1. Why this is not the merged `Chains.run` relabeled

The merged `Chains.follow F k x` is *defined* as `F.ops.getD k id x` and
`Chains.run` folds it over the word: it is the fold that reads the operation
functions, related to the encoding afterwards by `follow_derivable` and
`follow_unique`.  Reusing it as the step would have been the brief's
dirty-reference cheat.  Here the reader is defined on the instance list —
`lookup f x l` searches `l` for an edge `(f, [x, y])` and returns `y` — and
the operation's value is *derived*: `lookup_encode` says the search at form
`3 + k` from `x` returns `F.ops.getD k id x`, by the merged `derivable_op`.
The reference `evalWord` is a fold through the same `lookup`, so
`run_evalWord` relates two graph-readers with different control structure,
and `evalWord_encode` carries both to `Chains.run`.  That last theorem is the
bridge from the represented machine to the operations it represents, and it
is where `F.ops` appears — in the statement.  Commit 2 reads the enablements
the same way: `enabled_program` derives the relation from the self-instances.

## 2. The word machine (`lean/Execution.lean`)

| definition | content |
|---|---|
| `isEdge f x`, `value` | an instance is an edge of form `f` leaving `x` when it is `(f, [x, y])`; its value is `y` |
| `lookup f x l` | the value of the first such edge in `l`, if any |
| `Config` | `graph` (encoded instances), `word` (operation indices), `active`, `output` (the data visited) |
| `step` | consume the head `k` of the word by reading the edge of form `3 + k` leaving `active`; no word or no edge, no step |
| `iterate n c` | `step` iterated `n` times; a missing step is a refusal |
| `run c` | `iterate c.word.length c` |
| `evalWord g w a` | the fold over `w` through `lookup` |
| `init F w x` | the encoded instances of `F` as the graph, word `w`, start `x`, empty tape |
| `resume c v` | run a further word from a halted configuration |

| theorem | content |
|---|---|
| `lookup_mem`, `lookup_isSome` | a value read is an instance of the graph; an instance present is found |
| `lookup_encode` | reading the encoded graph at `(3 + k, x)` gives the `k`-th operation's value (CL-RE-01) |
| `iterate_evalWord`, `run_evalWord` | the configuration machine and the fold agree on the active datum (CL-RE-02) |
| `iterate_word`, `run_word`, `iterate_graph` | a halted run has consumed its word and kept its graph |
| `evalWord_append`, `run_append`, `iterate_add` | running `u ++ v` is running `u` then `v`; a configuration exists after any prefix (CL-RE-04) |
| `step_nil`, `iterate_zero`, `run_nil` | the empty word is the unit |
| `evalWord_encode` | on the encoding the fold computes `Chains.run` by reading the graph alone |
| `run_encode`, `run_total`, `run_lt` | **the word-bridge** (CL-RE-03) |

A word is a list of operation indices, not of data: `step` reads
`graph[3 + head]` at the active datum, so a two-operation setting follows the
letter, not always operation 0.

## 3. Control by data (`lean/Control.lean`)

| definition | content |
|---|---|
| `Controlled` | a finite setting with `ctrl x k`: operation `k` may fire at datum `x` |
| `CStep C x k y` | **the reference step**, on the setting: `k` enabled at `x` and `y` its value there |
| `ctrlInsts`, `program` | the enablements as self-instances `(3 + nops + k, [x, x])`; the program = operation graphs and enablements, no store |
| `encodeC` | the controlled regime: stores, program, `3 + 2 · nops` binary forms, no rule, no requirement |
| `enabled`, `enabledAt` | operation `k` is enabled at `x` when its control form's edge leaving `x` returns `x`; the enabled operations at `x`, a list nothing reads as a choice |
| `State` | the program, the operation count, `active`, `tape`, `clock`, `fuel` |
| `fire s k` | with fuel: read `k`'s edge, move, extend the tape, tick the clock, spend one fuel; else `exhausted`; no edge, `noEdge` |
| `successors s` | one state per enabled operation that fires |
| `stepDet`, `runDet`, `run` | the deterministic runner: fire the one enabled operation; `halt` when none; `branch` when two; bounded by a copy of the fuel |
| `init C x fuel` | the program, a start datum on the tape, clock zero, a declared fuel |
| `Live C s` | the live class: the program loaded, an admitted datum with an enabled operation, and fuel |

| theorem | content |
|---|---|
| `mem_ctrlInsts`, `mem_program`, `encodeC_forms_two`, `encodeC_wf` | the represented program is a well-formed binary regime (CL-RE-07) |
| `lookup_program_op`, `enabled_iff`, `mem_enabledAt`, `enabled_program` | edges and enablements are read faithfully from the program (CL-RE-08) |
| `fire_ok`, `fire_succ`, `fire_exhausted` | what one firing does; no fuel, no firing (CL-RE-11) |
| `mem_successors`, `successors_sound`, `successors_complete` | the successor family is the reference relation (CL-RE-09) |
| `init_pair` | the initial state does not read the designated pair (CL-RE-13) |
| `live_successor` | a live state has a successor (CL-RE-12) |
| `stepDet_branch`, `runDet_branch`, `run_branch` | `branch` only where two operations are enabled: the runner never selects (CL-RE-10) |

**The executable tests** (`tests/test_control.py`) on one three-point carrier
with three operations — the cycle `0 → 1 → 2 → 0`, the constant `0`, the climb
`0 → 1 → 2 → 2`:

| program | enablements | what it shows |
|---|---|---|
| ping | cycle at 0, constant at 1 | a branch driven by data: tapes `0,1,0,1,0` from 0, `1,0,1,0,1` from 1, halt at 2 |
| climb | climb at 0 and 1 | an iteration whose length the data set: 2, 1, 0 firings from the three starts, each `halt` |
| forever | cycle everywhere | arbitrarily long runs: exactly `n` firings on fuel `n`, `exhausted`, for `n < 8` |
| fork | cycle and constant at 0 | `branch` at clock 0; successor data `{0, 1}`; the family invariant under permuting the operations |

The refusals: an enabled operation with its edge removed returns `refuse`
without writing; a start outside the carrier and an out-of-range enablement
are refused by name.  The bookkeeping: clock equals tape length minus one and
clock plus fuel left equals the declared fuel on every run; fuel decreases
3, 2, 1, 0 and then nothing fires; firing keeps the program.

**Oracle check** (`tests/test_oracle.py`, a check and not a framework): the
machine functions of both Python modules — those taking a graph, a
configuration or a state and nothing else — and the machine definitions of
both Lean modules name no operation table, no merged `F.ops`-reading fold, no
chain criterion, no cache and no reference step.  The loaders read a setting
through the merged encoder and its shape; `control.cstep` is a documented
check the tests consult.

## 3a. Two loci of activity (`lean/Product.lean`)

One active datum is one locus, and the consuming families recorded that as a
limit: no independence and no interaction between two loci can be stated of a
process that has one.  The second locus is bought by the **carrier**, not by a
new machine: `pack m a b = m * a + b` carries the pair, `prodSetting F G` is a
finite setting of the merged class on `F.n * G.n` data whose operations act at
one locus each, and the encoder and the control machine run it unchanged.

| theorem | content |
|---|---|
| `fst_pack`, `snd_pack`, `pack_lt`, `fst_lt`, `snd_lt` | packing and reading back two loci |
| `leftOp_snd`, `rightOp_fst`, `prod_left_local`, `prod_right_local` | each move touches one locus |
| `left_right_comm`, `prod_comm` | **the independence square**: moves at different loci commute, for any two operations |
| `coupling_breaks_the_square`, `uncoupled_square_holds` | **interaction**: a move that reads the other locus does not commute, on a carrier where the uncoupled pair does |

The product is of *settings*.  Section 3b runs it.

## 3b. A two-locus run, and what its record shows (`lean/Schedule.lean`)

A carrier is not a run.  Running two loci means deciding which one moves, and
the obstacle is exact: if the *interpreter* decides, the schedule is a host
choice, and `Control.stepDet` already refuses to select — it returns `branch`
when two operations are enabled.  The answer is that **the schedule is data**.
A scheduled setting names, at each datum, the one operation enabled there; the
naming is carried by the enablement instances the machine already reads, so
the interpreter finds a singleton and never selects.  Nothing about the
interpreter changes and nothing is added to the grammar.

| theorem | content |
|---|---|
| `enabledAt_scheduled` | at every admitted datum exactly one operation is enabled: the one the schedule names |
| `scheduled_no_branch` | so the deterministic step **cannot** return `branch` — the refusal that would expose a host scheduler is not triggered |
| `step_moves_one_locus` | **one locus at a time**: whatever the schedule, every step leaves one coordinate exactly where it was |
| `pair_run`, `pair_terminal`, `pairSwapped_run` | the alternating run `0, 2, 3, 1, 0` and its mirror `0, 1, 3, 2, 0`, both ending on spent fuel |
| `square_on_the_outcome` | the two orders reach the same datum |
| `square_fails_on_the_observation` | and record different tapes |
| `locus1_is_its_own_run`, `locus2_is_its_own_run` | the tape read at one locus, with the repeats dropped, **is** that locus's own one-locus run |
| `swap_moves_both` | the failure case: an operation at neither locus moves both in one step |

The reading, stated plainly: the square lifts to the outcome and does not lift
to the observation, because a tape totally orders events that the loci do not.
What lifts is the *projection* — and the destuttering is the whole content of
the lift, since the repeats it drops are exactly the steps that moved the
other locus.  `Schedule.alt` reads both coordinates, which is what a schedule
may do and an operation may not (`Product.coupling_breaks_the_square`).

## 3c. The machine does not read the names of the data (`lean/Rename.lean`)

A datum is a number here only because something had to be written down.  A
**renaming** is a permutation of the carrier — given as a map with a
two-sided inverse *on the carrier*, four conditions on `Nat → Nat` rather than
a bijection of a subtype, so nothing outside the grammar's arithmetic is
needed.  It carries a setting to a renamed one (operations conjugated, stores
read through the inverse, endpoints moved) and a controlled setting to a
renamed one (enablement read through the inverse).

| theorem | content |
|---|---|
| `rename_op` | an operation of the renamed setting **is** the renamed operation |
| `rename_enabledAt` | the enablement read at the renamed datum is the one read at the original |
| `rename_lookup` | and the edge leaving it is the renamed edge |
| `rename_stepDet` | **one step corresponds**: the renamed state steps to the renamed successor, or stops with the *same* terminal |
| `rename_runDet`, `rename_run` | **the whole run corresponds**: same terminal, same clock, same fuel, the renamed datum |
| `rename_tape` | and the record is the renamed record |
| `not_a_renaming` | the failure case: the collapse of two data has no inverse, and no map is one |

Presentation identity is not internal identity, and this is the theorem that
says the machine reads only the latter.  `rename.py` mirrors it and the
receipt sweeps all six permutations of the three-point carrier against all 64
deterministic programs from all three starts — 1152 runs, every one
transporting — and refuses a map that is not a permutation rather than
renaming by it.

## 3d. One interpreter, parameterised by what it reads (`lean/Runner.lean`)

Three families now run the same interpreter with three different enablement
reads — `enabledAt … s.active`, `renabledAt … (previous s) s.active`,
`r2enabledAt … (before s) (previous s) s.active` — and each copied the runner
and its theorems.  The question that raised was whether a reader must see more
than the state.  **It need not**: all three are functions `State → List Nat`.

| theorem | content |
|---|---|
| `stepDetOf_inr`, `stepDetOf_spec` | the step is characterised by what the reader named and what the edge said |
| `stepDetOf_branch`, `stepDetOf_of_two`, `stepDetOf_branch_iff` | **it never selects — both ways.** `branch` implies two were named, *and* two named implies `branch`. The first alone is satisfied by a runner that selects, since such a runner returns a state and never says `branch` at all |
| `runDetOf_branch`, `ctrl_branch_iff` | and the runner's `branch` is honest at the state it returns |
| `nextOf_tape`, `obsOf_prefix`, `obsOf_prefix_add`, `nextOf_graph` | it only appends, and keeps the program |
| `ctrl_stepDet` | **the identification, by `rfl`**: `Control.stepDet` *is* `stepDetOf ctrlReader` |
| `ctrl_runDet`, `ctrl_run`, `ctrl_run_branch` | and its runner is the generic runner at that reader |
| `blind_halts`, `greedy_branches` | the two extreme readers, so the abstraction is not vacuous |

Nothing existing is renamed or replaced: the claim is made as an
identification, not a refactor, so no theorem name moved and no census
churned.  A fourth read costs a `Reader` and no runner at all.  `runner.py`
mirrors it and `tests/test_runner.py` checks the identification the Lean
states by `rfl` — over **every** enablement relation on the three-point
setting, deterministic or not, from every datum at every scale.

## 4. The artifact for Target B (`evidence/process.json`)

`run.py` writes the record the brief's Target B consumes and may not author:
`fragment: "control"`; the two machines' `Step`, `run`, references and
correspondence theorems; the configuration status; how a run is observed
(the final active datum, and the tape of data visited); six word-runs each
with its active datum equal to what the operations compute; eight controlled
runs each of whose transitions is a reference step; the branching example;
the iteration example; the live class; and the exact list of what is not
delivered.  Sorted keys, no timestamp, no machine path.  The receipt refuses
to record a word-run that refuses, leaves its word unconsumed or halts at a
datum other than the operations', a controlled run with a transition that is
not a reference step, or a clock that does not count the firings.

Every run carries `ops_in_index_order`.  A run's `setting_json` is the sealed
`Setting.json`, whose `ops` field is set-valued — the tables are sorted and
repetitions collapsed — so the index order the `word` and `enablements` refer
to is not recoverable from it: read literally, five of the fourteen runs did
not replay before the field was added, and the consumer family found it
(its CL-CP-09) rather than this family's own checks.
`test_every_recorded_run_replays_from_its_own_record` now rebuilds each run
from the record alone and compares the recorded outcome.

## 5. The single finish bar, met and not met

Commit 1 ships: the typed `step`/`run`, the Lean correspondence, the mutation,
the mid-run edit, the concatenate lemma, the configuration's status declared,
`process.json` written.  Commit 2 was attempted, as the brief requires, and
delivers branching by data, iteration whose length the data set, the successor
family without a selector, the four terminals, the clock, the fuel, and
non-stuckness on the live class.  What it does not deliver is exact: a
retained record that a later operation reads.  The tape is retained and
observable, but no enablement reads it, so two states with one active datum
and different tapes have one future — the merged endpoint theorem's
situation, reproduced rather than escaped.  The construction the brief names
— an enablement reading the previous datum beside the active one,
representable as a binary form with instances `[previous, active]` in the
same device — is the next single obstacle.  Represented storage growth
beyond the tape, and an encoded configuration, are likewise not built.

## 6. Evidence

**Lean** (`lean/`, `evidence/lean.json`): 114 authored theorems, and 59
compiler-generated ones **counted as the complement** of the authored names
rather than by a second heuristic — 10 constructor injectivities, 11 size
specifications, 1 constructor index, 2 proof terms of `Terminal`'s decidable
equality, 4 Prop-valued field projections of `Renaming` (which Lean classifies
as theorems), and 31 auxiliary proof terms of 17 theorems and definitions.
114 + 59 = 173 reports, and `tests/test_lean_gate.py` checks that identity and
that the six kinds partition the generated population; an earlier version
pinned the two counts separately and put the four field projections inside a
heuristic that excluded them, so the sum did not reach the total and nothing
noticed.  All within `{propext, Quot.sound}`; the report population equals the
environment census of the `Execution`, `Control`, `Product`, `Schedule`,
`Rename` and `Runner` namespaces in both directions; no private theorem;
forbidden-token scan clean.  `Classical.choice` was observed once, entering through `BEq` in an
earlier `isEdge`; the definition now decides the `Prop` directly and the
reliance is gone.  The proofs unfold the machines' definitions by `show` and
by definitional `have`, never by `simp`, so that no matcher equation is
minted behind the census (the trap the merged families record).

**Python** (`execution.py`, `control.py`, `run.py`, `evidence/process.json`,
`tests/`): 109 tests, strict typing over the tree's own modules and tests by a
**glob** and not a hand list, the two records replay
byte-identically.  `verify.py`, `verify_sources.py`, `verify_lean.py` and
`run.py` follow the merged `research/setting_translation` files with names,
pins and refusals changed; there is no shared helper across the research
trees.  One defect found and fixed while building: the sibling family also
has a `run.py` and a `verify_sources.py`, and a `sys.path` order that put the
sibling ahead of this tree loaded the sibling's custody guard silently.  This
tree's directory is now always first on the path, and `run.py` and
`verify_lean.py` refuse by name if a foreign guard is imported.

**Custody** (`verify_sources.py`, `SOURCE_MANIFEST.json`): at
`756917dcaeff5979faa9b1346a1a8ce666b33b25`, the eight derivation modules the
merged encoder loads by digest and runtime origin; the sealed
`lean4/Derivation` tree, the merged `local_reuse`, `ignition`,
`magnification` and `setting_translation` Lean trees, and the
`setting_translation` Python tree by Git tree object; the Lean configuration
of the five packages by digest.  An untracked source in any of the seven
trees is refused.  No export is read.  The two records are `-text` by an
in-tree `.gitattributes`, so a CRLF checkout cannot rewrite them.

```powershell
cd research/represented_execution
python verify.py     # sources, tests, mypy, lean (lake build + census), process --check
```

The mypy census is a **glob** of the tree's own `*.py`, not a hand list.  That
was a repair, and it was demonstrated before it was made: an unannotated,
type-broken `zzz_probe_orphan.py` that nothing imported left the run reporting
`Success: no issues found in 15 source files`; with the glob it is named.  A
module that *is* imported by a listed one was already checked — `follow_imports`
visits it and strict applies there — so the hole was exactly the unimported
file, which is the same census drift the runner glob and the parked-module
audit were built for.

Regenerate the two records deliberately and never under a live injection:
`python run.py --write`, `python verify_lean.py --write`.

## Not claimed

* That the running state is a regime of the sealed grammar: it is a declared
  host record (CL-RE-05).  The represented *program* of a controlled setting
  is a regime (CL-RE-07); the *state* is not.
* A retained record that a later operation reads; represented storage growth
  beyond the tape; an encoded configuration (section 5, CL-RE-14).
* Exploring the successor family as a tree of runs: the family is available
  and the runner refuses to pick; no run through a fork is built.
* An infinite run: the fuel is a represented field nothing renews, and no
  renewing law is declared.
* That the Python mirrors compute the Lean predicates: the agreement is on
  the stated finite populations; the Lean `lookup` reads the first edge in
  list order and the Python `lookup` the unique edge of a set, which coincide
  on every `encode` and `encode_c` graph and are not claimed to coincide on a
  graph with two edges leaving one datum on one form (the Python refuses such
  a graph by name).  A later family's record-reading program is such a graph
  on its control forms; it is read by membership there, not by `lookup`.
* That every edge of every encoding is load-bearing for some word.
* Anything about infinite carriers, undecidable stores or infinite operation
  families.

## Files and running

| file | role |
|---|---|
| `lean/Execution.lean` | the reader, the word machine, the reference, the word-bridge |
| `lean/Control.lean` | controlled settings, the represented program, the data-driven machine, the reference step |
| `lean/Product.lean` | two loci as a product carrier, the independence square, and the coupling that breaks it |
| `lean/Schedule.lean` | the schedule as data, a two-locus run, and the square on outcomes and on observations |
| `lean/Rename.lean` | renaming the carrier, and the run that corresponds under it |
| `lean/Runner.lean` | the interpreter over an enablement reader, and the merged machine as one instance |
| `lean/Inventory.lean` | the environment census |
| `execution.py`, `control.py` | the machines mirrored; `init` is the one function of each that sees a setting |
| `product.py` | the product carrier, the schedule as data, and reading a tape at one locus |
| `rename.py` | permutations of the carrier, the conjugation, and the transport sweep |
| `runner.py` | the interpreter over a reader, and the readers |
| `run.py`, `evidence/process.json` | the artifact for Target B and its refusals |
| `verify_lean.py`, `evidence/lean.json` | the Lean build, two-way census and reliance record |
| `verify_sources.py`, `SOURCE_MANIFEST.json` | custody of the consumed inputs |
| `verify.py` | every check in order |
| `tests/` | the machines against the operations and the reference step, the brief's tests, the refusals, the oracle check, custody, the parser, the records |
| `CLAIMS.md` | one `CL-RE-*` entry per claim |
