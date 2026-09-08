# Claims: represented operations drive a process

AuthorityEffect: None.  Every claim names its hypotheses, its novelty against
the reused results, its evidence, its falsifier and its remaining obligation.
The words forced, minimal, free, canonical, equivalent, universal and complete
appear only where a proof is named.  Lean names are in `lean/Execution.lean`
under the namespace `Execution`; every report lies within
`{propext, Quot.sound}` (`evidence/lean.json`).  "Finite setting" means the
merged `Translation.FiniteSetting`: carrier `{0, …, n-1}`, boolean-valued
stores, two endpoints in the carrier, finitely many operations closed on the
carrier.  "The encoded graph" means the instances of the merged
`Translation.encode F`, among which `(3 + k, [x, y])` is derivable exactly
when `y` is the `k`-th operation's value at `x` (the merged `derivable_op`).
A "word" is a list of operation indices; it is well-formed (`Chains.WordOk`)
when every index names an admitted operation.

### CL-RE-01 — reading the encoded graph is faithful

- **Statement**: `lookup (3 + k) x (encode F).insts = some (F.ops.getD k id x)`:
  the value the machine reads from the encoded graph at form `3 + k` from an
  admitted datum `x` is the `k`-th operation's value at `x`.  `lookup` is a
  search of the instance list for an edge `(3 + k, [x, y])`; it consults no
  operation function.
- **Hypotheses**: `k < F.ops.length`, `x < F.n`.
- **Novelty**: the merged `Chains.follow` is *defined* as `F.ops.getD k id x`
  and then related to derivability (`follow_derivable`, `follow_unique`); here
  the reader is defined on the instances and the operation's value is
  *derived* from the merged `derivable_op`.  `F.ops` appears in the
  statement, not in the definition.
- **Evidence**: `Execution.lookup_encode`, with `lookup_mem` (a value read is
  an instance) and `lookup_isSome` (an instance present is found).
- **Falsifier**: an admitted `x` and operation index `k` at which the search
  returns a different value, none, or an instance outside the graph.
- **Obligation**: none within the finite-setting class.

### CL-RE-02 — the configuration machine agrees with the graph-reading reference

- **Statement**: for every configuration `c`,
  `(run c).map Config.active = evalWord c.graph c.word c.active`, where `run`
  is `iterate step` for the length of the word by definition and `evalWord`
  is the fold over the word through the same `lookup`.  A run that halts has
  consumed its word (`run_word`) and kept its graph (`iterate_graph`).
- **Hypotheses**: none: the statement is over arbitrary configurations,
  including graphs that are not encodings.
- **Novelty**: two graph-readers with different control structure — a
  configuration carrying the remaining word, and a fold — agree; neither
  consults an operation function.
- **Evidence**: `Execution.run_evalWord`, `iterate_evalWord`, `run_word`,
  `iterate_word`, `iterate_graph`; computed: `execution.run` against
  `execution.eval_word` on every word of length at most three from every
  datum of the thirteen sealed settings, the six two-point exhibits, a
  three-point two-operation setting, and the first 400 settings of the sealed
  universe (`tests/test_execution.py`).
- **Falsifier**: a configuration whose run and fold disagree, or a halted run
  with a non-empty word.
- **Obligation**: none.

### CL-RE-03 — the word-bridge: the machine computes the operations

- **Statement**: for every finite setting `F`, every well-formed word `w` and
  every admitted datum `x`, `run (init F w x)` halts (`run_total`), and if it
  halts at `c` then `c.active = Chains.run F w x` and `c.word = []`
  (`run_encode`), with `c.active < F.n` (`run_lt`).  `Chains.run` is the
  merged fold that reads `F.ops`; `run` reads only the encoded instances.
- **Hypotheses**: `Chains.WordOk F w`, `x < F.n`; the configuration is
  `init F w x` — the encoded instances as the graph, an empty tape.
- **Novelty**: the merged `E_iff` and `E_iff_noChain` decide reading `E` with
  `Chains.run`; they do not execute a represented word.  This is the first
  result in the repository in which a word runs by reading encoded instances,
  and its agreement with the operations is a theorem rather than the
  definition.
- **Evidence**: `Execution.run_encode`, `run_total`, `run_lt`, through
  `evalWord_encode` and CL-RE-01; computed: the same population as CL-RE-02
  against the merged `translation.run`, which the tests consult for the
  expected value and the machine never does.
- **Falsifier**: a well-formed word and admitted datum on which the machine
  refuses, halts with a word remaining, or halts at a different datum than
  the operations compute.
- **Obligation**: the two executable tests the brief names are computed, not
  proved: redirecting one instance changes the halted datum (graph mutation),
  and redirecting one instance after `k` steps diverges the continuation from
  the unedited run (mid-run edit), each on the three-point two-operation
  setting (`tests/test_execution.py`).  That *every* reachable edge is
  load-bearing is not claimed.

### CL-RE-04 — the machine is stepwise, not a whole-word fold

- **Statement**: `evalWord g (u ++ v) a = (evalWord g u a).bind (evalWord g v)`
  and its run form `run_append`; `iterate (a + b) c = (iterate a c).bind (iterate b)`,
  so a configuration exists after any prefix of the word; the empty word is
  the unit (`run_nil`, `step_nil`, `iterate_zero`).
- **Hypotheses**: none.
- **Novelty**: the merged `Chains.run_append` is the same law for the
  `F.ops` fold; here it holds for the configuration machine, whose
  intermediate configurations are the objects a mid-run edit acts on.
- **Evidence**: `Execution.evalWord_append`, `run_append`, `iterate_add`,
  `run_nil`; computed: `run(u ++ v)` against `resume(run u, v)` and
  `iterate (a + b)` against `iterate a` then `iterate b` (`tests/test_execution.py`).
- **Falsifier**: a word pair or step split on which the two sides differ.
- **Obligation**: none.

### CL-RE-05 — the configuration is a declared host record

- **Statement**: `Config` is a structure of the metatheory — a graph field
  that is a copy of the encoded instances, a word, an active datum, a tape.
  The process reads encoded data; it does not itself live in the sealed
  grammar.  This is a declaration: **DECLARED_HOST_CONFIG**.
- **Hypotheses**: n/a — a declaration, not a theorem.
- **Novelty**: the brief's two admissible exits were a declared host
  configuration or an encoded one; the first is taken and billed.  Nothing
  here claims "the process lives in the sealed grammar".
- **Evidence**: the definition of `Config` and `init`; the record's
  `config_status` field (`evidence/process.json`).
- **Falsifier**: n/a; the claim would be false if the prose anywhere sold the
  configuration as a regime.
- **Obligation**: an encoded configuration — `init F w x` as a regime, the
  word represented as instances — is not built.  It is the stronger
  representation the brief names for later; nothing about it is claimed.

### CL-RE-06 — the artifact for Target B

- **Statement**: `evidence/process.json` names the fragment delivered
  (`words`), the machine's `Step`, `run`, `iterate` and reference, the
  correspondence theorem, the configuration status, how a run is observed
  (final active datum; the tape of data visited), and six recorded word-runs,
  each with its active datum equal to what the operations compute.  Sorted
  keys, no timestamp, no machine path.
- **Hypotheses**: none.
- **Novelty**: the brief's contract: Target B consumes a file authored by
  Target A and may not create it.
- **Evidence**: `run.py`, `evidence/process.json`; the receipt refuses to
  record a run that refuses, leaves its word unconsumed, or halts at a datum
  other than the operations' (`tests/test_evidence.py`).
- **Falsifier**: a recorded run whose active datum is not the operations'.
- **Obligation**: the record's `not_delivered` list is exact: control,
  branching, iteration, a retained record, the `semantic_clock` and the
  resource ledger are not in this fragment.
