# Claims: represented operations drive a process

AuthorityEffect: None.  Every claim names its hypotheses, its novelty against
the reused results, its evidence, its falsifier and its remaining obligation.
The words forced, minimal, free, canonical, equivalent, universal and complete
appear only where a proof is named.  Lean names are in `lean/Execution.lean`
(commit 1, the word machine) and `lean/Control.lean` (commit 2, control by
data) under the namespaces `Execution` and `Control`; every report lies within
`{propext, Quot.sound}` (`evidence/lean.json`).  "Finite setting" means the
merged `Translation.FiniteSetting`: carrier `{0, …, n-1}`, boolean-valued
stores, two endpoints in the carrier, finitely many operations closed on the
carrier.  "The encoded graph" means the instances of the merged
`Translation.encode F`, among which `(3 + k, [x, y])` is derivable exactly
when `y` is the `k`-th operation's value at `x` (the merged `derivable_op`).
A "word" is a list of operation indices; it is well-formed (`Chains.WordOk`)
when every index names an admitted operation.  A "controlled setting" is a
finite setting with an enablement relation `ctrl x k`: operation `k` may fire
at datum `x`.

## Commit 1 — the word machine

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

- **Statement**: `Config` (and, in commit 2, `State`) is a structure of the
  metatheory — a graph field that is a copy of encoded instances, and the
  bookkeeping fields.  The process reads encoded data; it does not itself
  live in the sealed grammar.  This is a declaration: **DECLARED_HOST_CONFIG**.
- **Hypotheses**: n/a — a declaration, not a theorem.
- **Novelty**: the brief's two admissible exits were a declared host
  configuration or an encoded one; the first is taken and billed.  Nothing
  here claims "the process lives in the sealed grammar".  In commit 2 the
  represented *program* is itself a regime (CL-RE-07); the *state* that runs
  it is still host.
- **Evidence**: the definitions of `Config`, `init`, `State`, `Control.init`;
  the record's `config_status` field (`evidence/process.json`).
- **Falsifier**: n/a; the claim would be false if the prose anywhere sold the
  configuration as a regime.
- **Obligation**: an encoded configuration — the running state as a regime —
  is not built.  It is the stronger representation the brief names for later;
  nothing about it is claimed.

### CL-RE-06 — the artifact for Target B

- **Statement**: `evidence/process.json` names the fragment delivered
  (`control`), the two machines' `Step`, `run` and reference, the
  correspondence theorems, the configuration status, how a run is observed
  (final active datum; the tape of data visited), six recorded word-runs each
  with its active datum equal to what the operations compute, eight recorded
  controlled runs each of whose transitions is a reference step, a branching
  example, an iteration example, the live class, and the exact list of what
  is not delivered.  Sorted keys, no timestamp, no machine path.  Every run
  carries `ops_in_index_order`, the operation tables in the order its `word`
  and `enablements` index: the run's `setting_json` is the sealed
  `Setting.json`, whose `ops` field is set-valued (sorted, repetitions
  collapsed), so that field alone does not determine the run.
- **Hypotheses**: none.
- **Novelty**: the brief's contract: Target B consumes a file authored by
  Target A and may not create it; the branching and iteration examples are
  the optional fields A now declares.
- **Evidence**: `run.py`, `evidence/process.json`; the receipt refuses to
  record a word-run that refuses, leaves its word unconsumed, or halts at a
  datum other than the operations', a controlled run with a transition that
  is not a reference step, or a clock that does not count the firings
  (`tests/test_evidence.py`).  The falsifier is mechanical:
  `test_every_recorded_run_replays_from_its_own_record` rebuilds each run
  from the record alone — `ops_in_index_order` with the recorded `word` or
  `enablements`, `start` and `fuel` — and compares the recorded
  `active`/`output`/`tape`/`terminal`.
- **Falsifier**: a recorded run whose active datum is not the operations', or
  a recorded transition that is not a reference step, or a run the record
  does not replay from its own fields.
- **Obligation**: the record's `not_delivered` list is exact (CL-RE-14).
  Recorded on repair: until `ops_in_index_order` was added, `setting_json`
  was the only table field, and five of the fourteen recorded runs did not
  replay from the record read literally — the falsifier above, met by the
  record and caught by the consumer family (its CL-CP-09), not by this
  family's own checks.

## Commit 2 — control by data

### CL-RE-07 — the represented program is a well-formed regime

- **Statement**: a controlled setting's enablement relation is represented as
  one more binary form per operation whose self-instance
  `(3 + nops + k, [x, x])` says `k` is enabled at `x` (`ctrlInsts`); the
  program — operation graphs and enablements — together with the stores is a
  regime `encodeC C` on `3 + 2 · nops` binary forms, and it is well-formed
  (`encodeC_wf`).
- **Hypotheses**: none beyond the controlled-setting signature.
- **Novelty**: the merged encoder represents stores and operations; the
  enablement of an operation *index* cannot be an instance argument (an
  argument must be a datum), and the self-instance device makes every
  argument a datum.  The merged `Visible` results for binary regimes remain
  applicable in principle; nothing here uses them.
- **Evidence**: `Control.encodeC_wf`, `encodeC_forms_two`, `mem_program`,
  `mem_ctrlInsts`; computed: `control.encode_c` is the sealed replay of
  `events_c`, has all-binary forms and no rule or requirement, and contains
  the program (`tests/test_control.py`).
- **Falsifier**: a controlled setting whose `encodeC` is ill-formed.
- **Obligation**: none.

### CL-RE-08 — enablement and edges are read faithfully from the program

- **Statement**: `enabled (program C) nops x k = true ↔ C.ctrl x k = true`
  (`enabled_program`), where `enabled` reads the control form's edge leaving
  `x` and asks whether it returns `x`; and `lookup (3 + k) x (program C) =
  some (C.F.ops.getD k id x)` (`lookup_program_op`).  Neither reader consults
  the enablement relation or an operation function.
- **Hypotheses**: `k < nops`, `x < C.F.n`.
- **Novelty**: the enablement is derived from instances as CL-RE-01 derived
  the edges; the relation and the functions appear only in the statements.
- **Evidence**: `Control.enabled_program`, `enabled_iff`, `mem_enabledAt`,
  `lookup_program_op`; computed: `control.enabled` against the enablement
  relation on every datum and operation of four controlled settings.
- **Falsifier**: a datum and operation at which the read enablement differs
  from the relation.
- **Obligation**: none.

### CL-RE-09 — the successor family is the reference relation

- **Statement**: the reference step `CStep C x k y` — `k` enabled at `x` and
  `y` its value there — is stated on the setting before any encoding.  A
  successor is exactly a firing of an enabled operation (`mem_successors`, by
  membership: no first element is named); every successor of a state carrying
  the program realises a reference step at that state's active datum
  (`successors_sound`); every reference step there, given fuel, is realised
  by a successor (`successors_complete`).  Both are stated at any such state,
  not only the initial one, which carries the program by `init_program`.
- **Hypotheses**: the state's graph is `program C`, its operation count
  `C.F.ops.length` and its active datum admitted; for completeness,
  `0 < s.fuel`.
- **Novelty**: this is the brief's simulation and reflection for the
  represented program: the interpreter's code is fixed and the program is
  the instances it reads.
- **Evidence**: `Control.successors_sound`, `successors_complete`,
  `init_program`, `mem_successors`, `fire_ok`; computed: the set of successor
  data equals the set of enabled operations' values, and each successor is a
  reference step, on every datum of four controlled settings and at every
  state a run of them reaches (`tests/test_control.py`).
- **Falsifier**: a successor that is not a reference step, or an enabled
  operation with fuel whose value is not reached by any successor.
- **Obligation**: the correspondence is one step at a time; a bisimulation
  over whole runs is a corollary the tree does not state.  An earlier wording
  said "every successor" while the theorems were stated at the initial state
  only; the theorems now carry the general hypotheses, and the narrower
  reading is withdrawn.

### CL-RE-10 — the runner never selects; the terminals are kept apart

- **Statement**: the deterministic runner fires the one enabled operation,
  halts when none is enabled, and stops with `branch` when two are: if it
  returns `branch`, at least two operations are enabled at the state it
  returns (`run_branch`, `runDet_branch`, `stepDet_branch`).  Its four
  terminals — `halt`, `exhausted`, `refuse`, `branch` — are distinct
  constructors.
- **Hypotheses**: none.
- **Novelty**: the brief's disqualifier — successor-list order acting as a
  scheduler — is met by refusal rather than by a declared policy: no
  configuration is ever advanced along a chosen branch of a genuine fork.
- **Evidence**: the theorems; computed: the fork program returns `branch` at
  clock 0 with successor data `{0, 1}`; the family of successor data is
  invariant under permuting the operations; a program with an enabled
  operation and no edge returns `refuse` without writing; the climb halts,
  the cycle exhausts (`tests/test_control.py`).
- **Falsifier**: a run returning `branch` at a state with fewer than two
  enabled operations, or advancing along one branch of a fork.
- **Obligation**: exploring the family — a tree of runs — is not built; the
  family is available (`successors`) and the runner refuses to pick.

### CL-RE-11 — bookkeeping: the clock counts firings, fuel is spent and never renewed

- **Statement**: a firing reads the edge, moves the datum to it, grows the
  tape by it, advances the clock by exactly one, spends exactly one fuel,
  and keeps the program (`fire_ok`); with no fuel nothing fires
  (`fire_exhausted`).  The machine has no administrative step, so the clock
  is the number of operation edges applied.
- **Hypotheses**: none.
- **Novelty**: the brief's `semantic_clock` and represented resource ledger,
  as fields of the state with proved laws rather than host counters.
- **Evidence**: `Control.fire_ok`, `fire_succ`, `fire_exhausted`; computed:
  clock equals tape length minus one and clock plus fuel left equals the
  declared fuel on every recorded run; fuel decreases 3, 2, 1, 0 and then
  refuses (`tests/test_control.py`, `tests/test_evidence.py`).
- **Falsifier**: a firing that changes the clock by other than one, the fuel
  by other than minus one, or the program.
- **Obligation**: none.

### CL-RE-12 — non-stuckness on the live class; arbitrarily long runs, no infinite run

- **Statement**: a live state — the program loaded, an admitted active datum
  with an enabled operation, and fuel — has a successor (`live_successor`).
  Computed: the cycle enabled everywhere runs exactly `n` firings on fuel `n`
  for every `n` tried and ends `exhausted`.
- **Hypotheses**: `Live C s`.
- **Novelty**: the brief's item 4, with its distinctions kept: arbitrarily
  long finite runs exist; one coherent infinite run does not, because fuel is
  a represented field nothing renews; all-run productivity and fairness are
  not at issue for the deterministic runner, and are not claimed for the
  family.
- **Evidence**: `Control.live_successor`; computed: `test_arbitrarily_long_runs_until_the_fuel_is_spent`.
- **Falsifier**: a live state with no successor.
- **Obligation**: an infinite run requires renewing the represented fuel by a
  declared law; none is declared, and the brief forbids hiding one in the
  host.

### CL-RE-13 — absent, not ignored

- **Statement**: the state carries the program only: every instance of
  `program C` has a form at or beyond the operation forms, so the difference
  relation, retention and protection are not loaded; and the initial state
  does not depend on the designated pair (`init_pair`, by reflexivity).
- **Hypotheses**: none.
- **Novelty**: the brief's two disqualifiers for protection and the pair are
  met by absence and by a theorem, not by a field that is silently ignored.
- **Evidence**: `Control.init_pair`, `mem_program`; computed:
  `test_the_program_carries_no_store`, `test_init_does_not_read_the_designated_pair`.
- **Falsifier**: a store instance in a loaded program, or two controlled
  settings differing only in endpoints with different initial states.
- **Obligation**: none.

### CL-RE-15 — two loci of activity, their independence, and what breaks it

- **Statement**: a product datum `pack m a b = m * a + b` carries two loci,
  read back by `fstOf`/`sndOf`.  Two finite settings give a product setting
  `prodSetting F G` on `F.n * G.n` data whose operations act at one locus each
  — `leftOp` on the first, `rightOp` on the second — and it is a finite
  setting of the merged class, so the merged encoder represents it and the
  control machine runs it unchanged.  **The independence square**: a move at
  one locus and a move at the other commute (`left_right_comm`, `prod_comm`),
  for any two operations, the second needing only to keep its own coordinate
  in range.  A left move leaves the second coordinate alone and a right move
  the first (`prod_left_local`, `prod_right_local`).  **Interaction**: a
  coupled move — one that reads the second locus to decide the first — does
  not commute with a move at the second locus
  (`coupling_breaks_the_square`), while the uncoupled pair on the same
  carrier does (`uncoupled_square_holds`).
- **Hypotheses**: `0 < m`, which every finite setting supplies through its
  admitted endpoint; for the product, the two settings' own closure.
- **Novelty**: two loci are a **datum** here, not a new machine — the
  interpreter, the encoder and the grammar are untouched, and the second
  locus is bought entirely by the product carrier.  That is what makes the
  square a statement about the *structure* rather than about the runner: it
  holds for every pair of local operations and fails exactly when an
  operation stops being local.
- **Evidence**: `Product.fst_pack`, `snd_pack`, `pack_lt`, `fst_lt`,
  `snd_lt`, `leftOp_snd`, `rightOp_fst`, `left_right_comm`, `prodSetting_n`,
  `prod_left_local`, `prod_right_local`, `prod_comm`,
  `coupling_breaks_the_square`, `uncoupled_square_holds`.
- **Falsifier**: two local operations that do not commute, or a coupled move
  that does.
- **Obligation**: the square is of *operations*.  Lifting it to observations,
  and the two-locus run it needs, are CL-RE-16, which also supplies the Python
  mirror this entry once lacked.  What remains after that entry: the product
  is of two loci and not of `k`, and the observing family's inverse system is
  not built over a two-locus run.  `Nat.div_lt_of_lt_mul` and
  `Nat.lt_of_mul_lt_mul_left` were both found to rely on `Classical.choice`
  by the axiom census, and `fst_lt` is proved without them — recorded because
  the census caught it, not a reading of the sources.

### CL-RE-16 — a two-locus run: the schedule is data, and the square lifts to the projection

- **Statement**: a *scheduled* setting `scheduled F sched` enables, at each
  datum, exactly the one operation `sched` names there
  (`enabledAt_scheduled`), so the deterministic step cannot return `branch`
  (`scheduled_no_branch`).  The schedule is carried by the ordinary
  enablement instances; the interpreter is unchanged and is told nothing it
  was not told before.  On the product carrier this is a **two-locus run**,
  and of it: **one locus moves at a time** — whatever the schedule, every
  step leaves one coordinate exactly where it was (`step_moves_one_locus`);
  the alternating schedule from `(0, 0)` realises `0, 2, 3, 1, 0` and its
  mirror `0, 1, 3, 2, 0` (`pair_run`, `pairSwapped_run`, both terminating on
  spent fuel); the two orders **reach the same datum**
  (`square_on_the_outcome`) and **record different tapes**
  (`square_fails_on_the_observation`); and the tape read at one locus with
  the adjacent repeats dropped **is that locus's own one-locus run**
  (`locus1_is_its_own_run`, `locus2_is_its_own_run`, against `solo_run`).
- **Hypotheses**: `sched x < F.ops.length` at the datum in question — a
  schedule that names an operation the setting does not have enables nothing,
  and the machine halts rather than choosing.  For `step_moves_one_locus`, a
  state carrying the two-locus program at an admitted datum.
- **Novelty**: it answers the obstacle by relocating it rather than by
  weakening it.  The runner's refusal to select stands untouched — the point
  is that a scheduled program never asks it to select.  And the observational
  result is two-sided in a way the operational square is not: the square
  **fails** on tapes, and what survives is the projection modulo stutter.
  The failure is not a defect: a tape totally orders events that the loci do
  not, and the repeats the destuttering drops are exactly the steps that
  moved the other locus.
- **Evidence**: `Schedule.enabledAt_scheduled`, `scheduled_no_branch`,
  `step_moves_one_locus`, `pair_run`, `pair_terminal`, `pairSwapped_run`,
  `square_on_the_outcome`, `square_fails_on_the_observation`, `solo_run`,
  `locus1_is_its_own_run`, `locus2_is_its_own_run`, `locus1_stutters`,
  `locus2_stutters`, `swap_moves_both`, `swap_not_local`; `product.py`,
  `tests/test_product.py` (exhaustive over every value table on two points
  and every schedule over the four product data), the record's `two_loci`
  section and its two injections in `tests/test_evidence.py`.
- **Falsifier**: a scheduled program at whose datum two operations are
  enabled; a step of a two-locus run that moves both coordinates; two orders
  reaching different data, or recording the same tape; a destuttered
  projection that is not the locus's own run.  The receipt refuses each by
  name.
- **Obligation**: the schedule is a function of the **active datum** only.  A
  schedule that reads the tape — which is what "the two loci take turns
  regardless of where they are" would need in general — is the
  record-reading family's enablement, not this one's, and is not built here.
  The alternation used is available only because the product datum happens to
  carry enough state to see whose turn it is.  Two loci, not `k`.  And the
  observation is the tape: the inverse system over a two-locus run at step
  scales is the observing family's, and is not built here.

### CL-RE-14 — what control delivers observably, and what it does not

- **Statement** (computed): on one three-point carrier with three
  operations, a program in which the cycle is enabled at 0 and the constant
  map at 1 fires a different operation at each datum (a branch driven by
  data); a program enabling the climb at 0 and 1 halts after 2, 1 and 0
  firings from the three starts (an iteration whose length the data set,
  not the interpreter); three programs from one datum give three different
  tapes.  **Not delivered**: a retained record that a later operation reads.
  The tape is retained and observable, but no enablement reads it, so two
  states with one active datum and different tapes have one future — the
  merged endpoint theorem's situation, reproduced rather than escaped.
- **Hypotheses**: the three programs, as recorded.
- **Novelty**: the brief's item 5, except its last clause; the missing
  clause is named as the obstruction, not deferred silently.
- **Evidence**: `tests/test_control.py`, the record's `branching_example`
  and `iteration_example`.
- **Falsifier**: for the delivered clauses, a recorded tape that differs on
  replay; for the remainder, an enablement in this tree that reads the tape
  (there is none).
- **Obligation**: the retained-record clause.  The construction the brief
  names — an enablement that reads the previous datum beside the active one,
  representable as a binary form with instances `[previous, active]` in the
  same device — is not built here and is the next single obstacle.
