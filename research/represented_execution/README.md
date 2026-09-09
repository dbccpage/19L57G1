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

Lean: 43 authored theorems, 73 reports with the compiler-generated ones, all
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
64 tests, strict typing over twelve files, two byte-identical records.
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

**Lean** (`lean/`, `evidence/lean.json`): 43 authored theorems and 30
compiler-generated ones — nine constructor injectivity and size
specifications for `Config`, `Controlled` and `State`; five for `Fired`
(three size specifications and `ok`'s injectivity); five for `Terminal` (four
size specifications and its `ofNat_ctorIdx`); the two proof terms of
`Terminal`'s decidable equality; and nine auxiliary proof terms of five
theorems (`enabled_program`, `encodeC_wf`, `live_successor`,
`lookup_program_op`, `successors_complete`) — 73 reports, all within
`{propext, Quot.sound}`; the report
population equals the environment census of the `Execution` and `Control`
namespaces in both directions; no private theorem; forbidden-token scan
clean.  `Classical.choice` was observed once, entering through `BEq` in an
earlier `isEdge`; the definition now decides the `Prop` directly and the
reliance is gone.  The proofs unfold the machines' definitions by `show` and
by definitional `have`, never by `simp`, so that no matcher equation is
minted behind the census (the trap the merged families record).

**Python** (`execution.py`, `control.py`, `run.py`, `evidence/process.json`,
`tests/`): 64 tests, strict typing over twelve files, the two records replay
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
| `lean/Inventory.lean` | the environment census |
| `execution.py`, `control.py` | the machines mirrored; `init` is the one function of each that sees a setting |
| `run.py`, `evidence/process.json` | the artifact for Target B and its refusals |
| `verify_lean.py`, `evidence/lean.json` | the Lean build, two-way census and reliance record |
| `verify_sources.py`, `SOURCE_MANIFEST.json` | custody of the consumed inputs |
| `verify.py` | every check in order |
| `tests/` | the machines against the operations and the reference step, the brief's tests, the refusals, the oracle check, custody, the parser, the records |
| `CLAIMS.md` | one `CL-RE-*` entry per claim |
