# Represented execution: represented operations drive a process

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.
Not registered in `.github/workflows/verify.yml`: its checks run locally
through `verify.py` (section 6).

**Result (commit 1, the word-bridge).**  A finite setting is encoded as a
regime whose operation graphs are the instances of binary forms (the merged
`setting_translation`).  This family runs a word of operation indices by
*reading those instances*: a configuration carries the encoded graph, the
remaining word, the active datum and an output tape; one `step` consumes the
head `k` of the word by looking the instance `(3 + k, [active, y])` up in the
graph and moving to `y`; `run` is `iterate step` for the length of the word,
by definition.  For every finite setting, every well-formed word and every
admitted datum the run halts with the word consumed and the active datum the
operations compute (`run_total`, `run_encode`) — proved without the machine
ever reading the operation functions `F.ops`, which enter once, in the
statement that reading the graph is faithful (`lookup_encode`, through the
merged `derivable_op`).  The machine is stepwise: a configuration exists after
any prefix of the word (`iterate_add`), and running `u ++ v` is running `u`
and continuing with `v` (`run_append`).

Configuration status: **DECLARED_HOST_CONFIG**.  `Config` is a structure of
the metatheory whose `graph` field is a copy of the encoded instances.  The
process reads encoded data; it does not itself live in the sealed grammar,
and nothing here says it does.

Lean: 21 authored theorems, 24 reports with the compiler-generated ones, all
within `{propext, Quot.sound}`, in a package importing the sealed package and
the merged `setting_translation` package.  Python: the machine mirrored,
checked against the merged `translation.run` (the fold that reads `F.ops`,
which the tests may consult and the machine never does) on every word of
length at most three from every datum of the thirteen sealed settings, the
six two-point exhibits, a three-point two-operation setting and the first
400 settings of the sealed universe; the graph mutation, mid-run edit,
two-graphs-one-word, letter-names-an-operation, concatenation and empty-word
tests the brief names; the named refusals; an oracle check on the machine's
source; 37 tests, strict typing over ten files, a byte-identical record.
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
is where `F.ops` appears — in the statement.

## 2. The machine (`lean/Execution.lean`)

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

A word is a list of operation indices, not of data: `step` reads
`graph[3 + head]` at the active datum, so a two-operation setting follows the
letter, not always operation 0 (`test_a_letter_names_an_operation`).

## 3. The theorems

| theorem | content |
|---|---|
| `lookup_mem`, `lookup_isSome` | a value read is an instance of the graph; an instance present is found |
| `lookup_encode` | reading the encoded graph at `(3 + k, x)` gives the `k`-th operation's value (CL-RE-01) |
| `iterate_evalWord`, `run_evalWord` | the configuration machine and the fold agree on the active datum (CL-RE-02) |
| `iterate_word`, `run_word`, `iterate_graph` | a halted run has consumed its word and kept its graph |
| `evalWord_append`, `run_append` | running `u ++ v` is running `u` and continuing with `v` (CL-RE-04) |
| `iterate_add` | iterating `a + b` steps is iterating `a` then `b` |
| `step_nil`, `iterate_zero`, `run_nil` | the empty word is the unit |
| `evalWord_encode` | on the encoding the fold computes `Chains.run` by reading the graph alone |
| `run_encode` | **the word-bridge**: a halted run has consumed its word and its active datum is `Chains.run F w x` (CL-RE-03) |
| `run_total` | a well-formed word from an admitted datum runs to a halt |
| `run_lt` | the halted datum is in the carrier |

The proofs unfold the machine's definitions by `show` and `change` rather
than by `simp`, so that no matcher equation is minted behind the environment
census (the trap the merged families record).

## 4. The executable tests the brief names (`tests/test_execution.py`)

On a three-point setting with two distinct operations (`(1, 2, 0)` and the
constant `0`), so that reading the letter and reading the graph both matter:

| test | what it shows |
|---|---|
| graph mutation | redirecting the edge of operation 0 at datum 1 changes the halted datum of the word `[0, 0]` from 2 to 1 |
| mid-run edit | after one step of `[0, 0, 0]`, redirecting that edge diverges the continuation (halted datum 1, not 0) and its tape from the unedited run |
| two graphs, one word | the same word on two settings differing at one instance halts at different data |
| a letter names an operation | `[0]` and `[1]` from datum 0 halt at 1 and 0 |
| concatenation | `run(u ++ v)` equals `resume(run u, v)` on every pair of words of length at most two |
| empty word | no step, no move, empty tape, on every sealed setting |
| iterate add | `iterate (a + b)` equals `iterate a` then `iterate b` for every split of four steps |

The refusals: a missing edge refuses without writing (the configuration
before the missing edge is reached and no dummy datum appears); two edges on
one form leaving one datum are refused by name rather than silently ordered;
a start outside the carrier and an unknown letter refuse.

**Oracle check** (`tests/test_oracle.py`, a check and not a framework): the
machine's Python source names no `.ops`, no `translation.run`, no `follow`,
no chain criterion and no cache; the Lean definitions of `isEdge`, `value`,
`lookup`, `step`, `iterate`, `run`, `evalWord` and `resume` contain no `ops`,
no `Chains` and no `follow`.  The *tests* consult `translation.run` for the
expected values; the machine does not.

## 5. The artifact for Target B (`evidence/process.json`)

`run.py` writes the record the brief's Target B consumes and may not author:
`fragment: "words"`, the names of `Step`, `run`, `iterate`, the reference and
the correspondence theorem, the configuration status, how a run is observed
(the final active datum, and the tape of data visited, one entry per letter),
six recorded word-runs each with its active datum equal to what the
operations compute, and the exact list of what this fragment does not
deliver.  Sorted keys, no timestamp, no machine path; the receipt refuses to
record a run that refuses, leaves its word unconsumed, or halts at a datum
other than the operations'.

## 6. Evidence

**Lean** (`lean/`, `evidence/lean.json`): 21 authored theorems and 3
compiler-generated ones (the `Config` constructor's injectivity and size
specification), 24 reports, all within `{propext, Quot.sound}`; the report
population equals the environment census of the `Execution` namespace in both
directions; no private theorem; forbidden-token scan clean.  `Classical.choice`
was observed once, entering through `BEq` in an earlier `isEdge`; the
definition now decides the `Prop` directly and the reliance is gone.

**Python** (`execution.py`, `run.py`, `evidence/process.json`, `tests/`): 36
tests, strict typing over ten files, the record replays byte-identically.
`verify.py`, `verify_sources.py`, `verify_lean.py` and `run.py` follow the
merged `research/setting_translation` files with names, pins and refusals
changed; there is no shared helper across the research trees.  One defect
found and fixed while building: the sibling family also has a `run.py` and a
`verify_sources.py`, and a `sys.path` order that put the sibling ahead of this
tree loaded the sibling's custody guard silently.  This tree's directory is
now always first on the path, and `run.py` and `verify_lean.py` refuse by
name if a foreign guard is imported.

**Custody** (`verify_sources.py`, `SOURCE_MANIFEST.json`): at
`756917dcaeff5979faa9b1346a1a8ce666b33b25`, the eight derivation modules the
merged encoder loads by digest and runtime origin; the sealed
`lean4/Derivation` tree, the merged `local_reuse`, `ignition`,
`magnification` and `setting_translation` Lean trees, and the
`setting_translation` Python tree by Git tree object; the Lean configuration
of the five packages by digest.  An untracked source in any of the seven
trees is refused.  No export is read.

```powershell
cd research/represented_execution
python verify.py     # sources, tests, mypy, lean (lake build + census), process --check
```

Regenerate the two records deliberately and never under a live injection:
`python run.py --write`, `python verify_lean.py --write`.

## Not claimed

* That the configuration is a regime of the sealed grammar: it is a declared
  host record (CL-RE-05).  An encoded configuration is not built.
* Control: composition, data-dependent branching, iteration, represented
  storage growth, a retained record that changes a later readout, the
  `semantic_clock`, the resource ledger.  None is in this fragment; the
  record's `not_delivered` list is exact.
* That the Python mirror computes the Lean predicates: the agreement is on
  the stated finite populations; the Lean `lookup` reads the first edge in
  list order and the Python `lookup` the unique edge of a set, which coincide
  on every encoding and are not claimed to coincide on a graph with two edges
  leaving one datum on one form (the Python refuses such a graph by name).
* That every edge of every encoding is load-bearing for some word: the
  mutation and mid-run-edit tests are two witnesses on one setting.
* Anything about infinite carriers, undecidable stores or infinite operation
  families.

## Files and running

| file | role |
|---|---|
| `lean/Execution.lean` | the reader, the configuration machine, the reference, the word-bridge |
| `lean/Inventory.lean` | the environment census |
| `execution.py` | the machine mirrored; `init` is the one function that sees a setting |
| `run.py`, `evidence/process.json` | the artifact for Target B and its refusals |
| `verify_lean.py`, `evidence/lean.json` | the Lean build, two-way census and reliance record |
| `verify_sources.py`, `SOURCE_MANIFEST.json` | custody of the consumed inputs |
| `verify.py` | every check in order |
| `tests/` | the machine against the operations, the brief's tests, the refusals, the oracle check, custody, the parser, the records |
| `CLAIMS.md` | one `CL-RE-*` entry per claim |
