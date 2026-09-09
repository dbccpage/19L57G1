# Claims: the record read, and a class of laws selected against

AuthorityEffect: None.  Every claim names its hypotheses, its novelty against
the reused results, its evidence, its falsifier and its remaining obligation.
The words forced, minimal, free, canonical, equivalent, universal and complete
appear only where a proof is named.  Lean names are in `lean/Record.lean` and
`lean/Select.lean` under the namespaces `Record` and `Select`; every report
lies within `{propext, Quot.sound}` (`evidence/lean.json`).  "The merged
machine" means the `Control` machine of `research/represented_execution`;
"the observed family" means `research/coherent_process_limits`, whose
`Observe.base` transcribes the three-point setting identified from the
represented execution family's artifact — the cycle, the constant map, the
climb, in index order; "the record" means the machine's tape.

## The record read (W02)

### CL-RR-01 — the record-reading program is a well-formed regime

- **Statement**: a recorded setting's enablement relation `hctrl p x k` —
  operation `k` may fire at datum `x` when the datum before it on the
  record is `p` — is represented in the same device as the merged
  control machine, one binary form per operation, by the instance
  `(3 + nops + k, [p, x])` (`recInsts`); with the operation graphs it is the
  program (`rprogram`, `mem_rprogram`), and with the stores it is a
  well-formed regime of the sealed grammar on `3 + 2 · nops` binary forms
  (`encodeR_wf`).
- **Hypotheses**: a finite setting of the merged class.
- **Novelty**: the merged self-instance `[x, x]` is the case `p = x`; the
  device is unchanged and the relation it carries is no longer diagonal.
- **Evidence**: the theorems; computed: `record.rprogram` equals the sealed
  replay beyond the stores on every named program, every lifted memoryless
  program and a declared sample of 263 record programs.
- **Falsifier**: a recorded setting whose regime fails `wf`.
- **Obligation**: none.

### CL-RR-02 — the record enablement is read faithfully, as a relation

- **Statement**: `renabled g nops p x k` is the presence of the instance
  `(3 + nops + k, [p, x])` in the graph (`present_iff`, `renabled_iff`), and
  on the program it is the setting's relation (`renabled_rprogram`).
  Several instances of one control form may leave one record entry: a
  relation is read, not a function.
- **Hypotheses**: admitted `p`, `x`, `k`.
- **Novelty**: the merged `enabled` reads a function (`lookup … = some x`);
  that read would be wrong here, and the read is stated as membership.
- **Evidence**: the theorems; computed: the read on `turncoat` at every
  triple, and the control form with several instances leaving datum 0.
- **Falsifier**: a triple in the relation whose instance is not read, or
  read when absent.
- **Obligation**: none.

### CL-RR-03 — the record is what the process wrote, and nothing else

- **Statement**: `previous s` is the entry before the last on the tape,
  the start its own predecessor (`previous_rinit`).  After a firing from a
  synced state, the datum the step left is the `previous` of the state it
  reaches (`previous_fire`), and firing keeps the state synced
  (`fire_synced`, `rinit_synced`).
- **Hypotheses**: a synced state — one whose tape ends with its active
  datum; every state reachable from `rinit` is.
- **Novelty**: the brief's failure mode is a host consulting an external
  route log.  The enablement reads a field of the state that the merged
  `fire` writes (`fire_ok`), and only that: editing the read instance
  changes the run, adding an instance no step reads does not.
- **Evidence**: the theorems; computed: `previous` after every step of the
  three named programs from every start, and the edit test
  (`tests/test_record.py`).
- **Falsifier**: a firing after which `previous` is not the datum left.
- **Obligation**: the enablement reads one entry of the record; a deeper
  read is not built.

### CL-RR-04 — simulation and reflection; never selects; only appends

- **Statement**: every successor of a state carrying the program realises
  a reference step `RStep` at the recorded and active data
  (`rsuccessors_sound`); every reference step there, given fuel, is
  realised (`rsuccessors_complete`); the runner stops with `branch` only
  when two operations are enabled (`rrun_branch`); a step only appends
  (`rnext_tape`, `robs_prefix`, `robs_prefix_add`).
- **Hypotheses**: the state's graph is the program, its operation count the
  setting's, and its recorded and active data admitted.
- **Novelty**: stated on any synced state, not only the initial one, because
  the reference step now depends on the record.
- **Evidence**: the theorems; computed: successors against `rstep` on 27
  (record, datum) pairs of three programs; a fork stops with `branch`; the
  terminals apart.
- **Falsifier**: a successor with no reference step, or a reference step
  with no successor.
- **Obligation**: none.

### CL-RR-05 — the memoryless class embeds

- **Statement**: a controlled setting read with the record ignored
  (`lift`) has the merged reference step at every record entry
  (`lift_RStep`) and the merged enablement read (`lift_renabled`);
  `forget` reads a recorded setting at the datum as its own predecessor.
- **Hypotheses**: admitted data.
- **Novelty**: the extension is conservative by a theorem, not by
  declaration.
- **Evidence**: the theorems; computed: the lifted `forever` agrees with
  `forever` at every declared start and scale, and `forget ∘ lift` is the
  identity on it.
- **Falsifier**: a lifted program whose run differs from the memoryless one.
- **Obligation**: the runs' agreement is computed; the bisimulation of the
  two machines is not stated in Lean.

### CL-RR-06 — the distinction: a run that leaves one datum two ways

- **Statement**: on the observed family's setting, `twist` — the cycle at 0
  after 0, the constant map at 1 after 0, the constant map at 0 after 1 —
  visits `0, 1, 0, 0` from datum 0 (`twist_tape`, `twist_period`): at its
  third step it is at the datum it started from and moves elsewhere than
  the first time (`record_is_read`).  No run of the merged machine does
  that: three steps that return to the datum they started from leave it
  the same way (`memoryless_functional`, from the observed family's
  `next_active_det`).
- **Hypotheses**: none for the negative; the named program for the
  positive.
- **Novelty**: the brief's useful result — one later readout differs
  because of state the process can access — with the memoryless
  impossibility proved, not only computed.
- **Evidence**: the theorems; computed: none of the 64 memoryless programs
  of the observed family's class realizes `[0, 1, 0, 0]` from any datum;
  the tape is not functional.
- **Falsifier**: a memoryless run with the tape `[0, 1, 0, 0]`.
- **Obligation**: none.

### CL-RR-07 — remove the record and the distinction disappears

- **Statement**: `forget twist` enables the cycle at 0 only; its run from 0
  halts at `[0, 1]` (`forget_twist`).
- **Hypotheses**: none.
- **Novelty**: the brief's control: the retained field removed, the
  readout collapses.
- **Evidence**: the theorem; computed: the projection and its terminal.
- **Falsifier**: n/a (exhibited).
- **Obligation**: none.

## A class of laws and a discriminating input (W38 / W15)

### CL-RR-08 — one step by its next value; the observation is a bisimulation invariant

- **Statement**: one step of the merged runner either stops — no fuel, or
  no next value — or moves to `nextValue g nops x`, the value of the one
  enabled operation at `x`, appending it (`stepDet_spec`).  Two states with
  the same next-value function, active datum, record and fuel have the
  same observation at every scale (`obs_bisim`); a coarser observation is
  the prefix, of its own length, of a finer one (`obs_take`).
- **Hypotheses**: none.
- **Novelty**: what the tape identifies, stated exactly: the next-value
  function, and nothing finer.
- **Evidence**: the theorems; computed: `next_value` against every step of
  three programs from three starts.
- **Falsifier**: two states with one next-value function, datum, record and
  fuel and different observations.
- **Obligation**: discharged.  `Record.rnextOf` reads what the record-reading
  program says about a `(previous, active)` pair, `Record.rstepDet_spec`
  expresses one step of that machine by it, and `Select.RRel` / `rrel_next` /
  `rrel_iter` / `robs_bisim` give the same invariance there: same next-value
  function, active datum, record and fuel, same observation at every scale.
  The record is part of the relation, so `previous` — a function of the record
  — agrees too (`previous_congr`).  `robs_take` is the finest-scale corollary.

### CL-RR-09 — the ambiguity exhibited: which operation carried the datum is not observed

- **Statement**: `forever` (the cycle everywhere) and `climbFirst` (the
  climb at 0, the cycle at 1 and 2) differ as programs (`forever_differ`)
  and have the same next value at every datum (`forever_ambiguous`), hence
  the same observation from every start, at every fuel and every scale
  (`forever_indistinguishable`).  In the selection experiment both survive
  the seen observation, no declared input separates them, and the eight
  memoryless survivors form one residual class.
- **Hypotheses**: the observed family's setting.
- **Novelty**: the brief's "missing axiom" as an exhibit: the observable
  reads where the datum went, not which operation carried it; a genuinely
  unique model within the class is refused by a theorem.
- **Evidence**: the theorems; computed: `selection.experiment`, memoryless
  class — 64 laws, 8 survivors, burden 0, 1 residual class.
- **Falsifier**: a declared input whose readout differs between the two.
- **Obligation**: none.

### CL-RR-10 — the discriminating input exhibited, and the burden computed

- **Statement**: `turncoat` (the cycle everywhere except after 2 at datum 0,
  where the constant map fires) reads the seen observation as the lifted
  `forever` does (`turncoat_agrees`) and is separated at scale 4 from
  datum 0 (`turncoat_differs_scale`) and at scale 2 from datum 2
  (`turncoat_differs_start`).  In the record class — 262144 laws with at
  most one operation per (previous, active) pair — 32768 replay the seen
  observation; three greedy experiments (start 1 at scale 6, start 2 at
  scale 2, start 0 at scale 4) separate them into 45 residual classes, the
  largest of 4096; within a residual class the next-value function read
  from the program agrees on every pair the runs reach, and between two
  classes it differs on a reached pair.
- **Hypotheses**: the declared protocol (CL-RR-11).
- **Novelty**: the brief's candidate discriminating experiment, with the
  burden — how many declared inputs, which — computed rather than argued,
  and the residual explained by the pairs the runs reach.
- **Evidence**: the theorems; computed: `selection.experiment`
  (`evidence/record.json`).
- **Falsifier**: a residual class whose members differ in next value on a
  reached pair, or two classes agreeing on all reached pairs (checked over
  the 990 pairs of the record population; the memoryless population has one
  class and no such pair).
- **Obligation**: the residual explanation is checked against the programs,
  not proved; the greedy sequence is one sequence, not a minimum.

### CL-RR-12 — the ceiling of a depth-one read

- **Statement**: every tape a record-reading run realises is functional in its
  *pairs*: two places where the same datum follows the same datum are followed
  by the same datum (`robs_functional`).  The tape of a run is a chain of the
  machine in the sense of consecutive triples (`RChain`, carried by
  `rnext_chain` / `riter_chain` from `rinit_chain`), and a chain is functional
  because `rnextOf` is a function of the pair (`rchain_functional`).
- **Hypotheses**: none beyond a run from an initial state: every recorded
  setting, start datum, fuel and scale.
- **Novelty**: the exact measure of what reading one entry of the record buys.
  The memoryless machine's tape is functional in single entries (the observed
  family's `obs_functional`); reading one entry of the record buys functionality
  in pairs and no more.  A tape that repeats a pair with two different
  successors is realised by no record-reading program at all — which is what a
  deeper read has to produce.
- **Evidence**: `Record.triplesOf`, `lastTwo`, `RChain`, `rchain_functional`,
  `rnext_chain`, `riter_chain`, `rinit_chain`, `robs_functional`.
- **Falsifier**: a record-reading run whose tape repeats a pair with two
  different successors.
- **Obligation**: none.  The depth-two read that would break this ceiling is
  not built (CL-RR-11).

### CL-RR-13 — a record read two entries deep, and a regime of mixed arity

- **Statement**: a depth-two recorded setting's enablement `hctrl2 b p x k` —
  operation `k` may fire at `x` after `p` after `b` — is represented by the
  instance `(3 + nops + k, [b, p, x])` on a **ternary** control form.  With the
  binary stores and operation graphs that is a regime of mixed arity, and it is
  well-formed (`encodeR2_wf`); the enablement is read faithfully
  (`r2enabled_r2program`), by membership, and the successors realise the
  reference step `R2Step` (`r2successors_sound`).  The depth-one class embeds
  (`lift2`, `lift2_R2Step`).  On the observed family's setting the program
  `twist2` visits `0, 1, 2, 0, 1, 0` from datum 0 (`twist2_tape`); that tape
  carries the pair `(0, 1)` followed once by `2` and once by `0`, so **no
  record-reading program realises it** (`no_record_run_realises`, through
  CL-RR-12) — `depth_two_is_deeper` states the two halves together.
- **Hypotheses**: for the faithful read, admitted `b`, `p`, `x` and `k` in
  range; for the concrete run, the transcribed base setting.
- **Novelty**: the first family here whose encoding is **not all-binary**.
  Nothing about the sealed grammar had to move to allow it: `Regime.wf`
  constrains a form's arity only by `1 ≤ a`, so the ternary form needs no new
  admission.  And the gain is measured rather than asserted — the depth-one
  ceiling is CL-RR-12, and this is a tape above it.
- **Evidence**: `Depth.formsOf_getD_binary`, `formsOf_getD_ternary`,
  `formsOf_pos`, `encodeR2_wf`, `mem_r2program`, `r2enabled_r2program`,
  `lookup_r2program_op`, `r2successors_sound`, `lift2_R2Step`, `twist2_tape`,
  `twist2_repeats_a_pair`, `no_record_run_realises`, `depth_two_is_deeper`.
- **Falsifier**: a depth-two setting whose `encodeR2` is ill-formed; a
  record-reading run realising `[0, 1, 2, 0, 1, 0]`.
- **Obligation**: the bisimulation of the depth-two machine is not stated.
  An earlier version of this entry said the machine had no Python mirror, that
  no receipt recorded a depth-two run, and that its chain invariant and the
  ceiling of a depth-*two* read were not stated; all three are **WITHDRAWN**
  by CL-RR-14, which supplies the mirror, the receipt, the chain invariant and
  the ceiling.  A depth-`d` family for general `d` is still not built.

### CL-RR-14 — the ceiling of a depth-two read, and the ladder of depths

- **Statement**: the tape of a depth-two run is a chain of the machine's next
  value on **three** arguments (`R2Chain`, `r2stepDet_spec`, `r2next_chain`,
  `r2iter_chain`), and a chain of a three-argument function is functional in
  its triples (`r2chain_functional`).  Hence **the ceiling**: every tape a
  depth-two run realises is functional in its triples — three entries
  determine the fourth (`r2obs_functional`).  The classes are a **chain**: a
  window of `d + 1` entries contains a window of `d` (`pairsOf_of_triplesOf`,
  `triplesOf_of_quadsOf`), so a tape functional in `d` entries is functional
  in `d + 1` (`triples_of_pairs`, `quads_of_triples`).  Both proved inclusions
  are **strict** (`the_ladder`): the depth-one exhibit repeats an entry with
  two successors (`twist_repeats_an_entry`) and the depth-two exhibit repeats
  a pair (`twist2_repeats_a_pair`).
- **Hypotheses**: none beyond the machine.  The ceiling is stated of every
  program, every start, every fuel and every scale.
- **Novelty**: three ceilings, one per rung, and the ladder proved to be a
  chain rather than assumed.  The order matters: the *ceiling* of a depth is
  proved first and the exhibit above it second, so "deeper" is a theorem about
  what the shallower machine cannot do rather than a claim about a bigger
  construction.  The strictness is measured as well as proved — see below.
- **Evidence**: `Depth.r2nextOf`, `r2stepDet_spec`, `r2next_of_inl`,
  `r2next_of_inr`, `quadsOf`, `lastThree`, `lastThree_reverse`,
  `lastThree_ne_none`, `quadsOf_snoc_none`, `quadsOf_snoc`, `R2Chain`,
  `r2chain_functional`, `before_of_reverse`, `r2next_chain`, `r2iter_succ`,
  `r2iter_chain`, `r2init_chain`, `r2obs_functional`, `pairsOf_of_triplesOf`,
  `triplesOf_of_quadsOf`, `triples_of_pairs`, `quads_of_triples`,
  `twist_repeats_an_entry`, `the_ladder`; `depth.py`, `tests/test_depth.py`,
  and the record's `depth_two` section.  **Computed** (`depth.ladder`, over
  *every* deterministic program of each depth on a two-point setting at fuel
  six, exhaustive and not sampled): the three depths realise 10, 22 and 70
  tapes; every realised tape meets its own depth's ceiling; 8 then 38 of them
  break the ceiling of the depth below, which by that ceiling is exactly the
  set the depth below cannot realise.
- **Falsifier**: a depth-two run realising a tape not functional in its
  triples; a tape functional in `d` entries and not in `d + 1`; a rung
  realising nothing the rung below cannot.  The receipt refuses each by name,
  and also refuses a depth-two program whose instances are not the sealed
  replay of its own admission history.
- **Obligation**: a machine of depth `d` for `d > 2` is built neither here nor
  in the Lean, so each ceiling is proved at its own rung and not for a general
  `d`.  `depth.functional` is written for any window size so that the
  statement checked at each rung is the same one, but that is apparatus and
  not a theorem.  The bisimulation of the depth-two machine is still not
  stated.

### CL-RR-15 — the burden as a minimum, and a second readout

- **Statement** (computed). **The minimum.** The greedy sequence is one
  sequence; `minimum_burden` searches every subset of the declared inputs by
  increasing size and reports the least that separates the retained laws as
  finely as all of them together do.  On the record class it is **3** — the
  same length as the greedy sequence, so the greedy sequence is optimal here,
  though it is a *different* set of three.  **No single start suffices**: for
  each of the three declared starts, all eight of its scales together leave
  the partition coarser than the residual.  The search is exhaustive and
  cheap for a stated reason: laws with equal readouts on all the declared
  inputs have equal readouts on any subset, so one representative per residual
  class decides every subset.
  **The second readout.**  Reporting the index of the operation that produced
  each entry beside the entry takes the record class's residual from **45
  classes with a largest class of 4096** to **896 classes with a largest class
  of 64**, and within every class of the refined partition the laws agree on
  their enablement — index and value — at every pair the runs reach.  What is
  left to distinguish them is the enablement at pairs no run reaches: the
  largest class is 4³, four choices at each of three unreached pairs.  That is
  the collapse the rung predicted, and it is measured rather than asserted.
- **Hypotheses**: the protocol as declared before any readout; the identified
  setting.
- **Novelty**: the second readout is **not free**, and the reason is a theorem
  already here: which operation carried the datum is not a function of the
  record (`Select.forever_indistinguishable`, from `Select.obs_bisim`), so the
  index is genuinely more than the tape and not a rearrangement of it.
- **Status of the second readout**: **HOST READOUT**, declared as such.  The
  index is reported by the *interpreter*; the process does not write it.  The
  tape and the clock are represented fields of the state and this is not one.
  Making it one would be a change to the machine — a field written by firing —
  and that change is **not made here**.  The precedent is named rather than
  borrowed.
- **Evidence**: `selection.minimum_burden`, `fired_at`, `annotated_run`,
  `annotated_signature`, `annotated_partition`, `second_readout`; the record's
  `selection.classes.*.minimum_burden` and `.second_readout`;
  `tests/test_selection.py`, which re-derives the minimum by an independent
  exhaustive search over smaller subsets, and checks the refinement against
  partitioning by the annotated runs themselves on the class small enough to
  do both.
- **Falsifier**: a subset of the declared inputs smaller than the reported
  minimum that reaches the residual; a class of the refined partition whose
  members disagree on a reached pair.  The receipt refuses the second by name,
  and the refusal is injected by reporting the plain partition as if it were
  the refinement.
- **Obligation**: the second readout is a host report.  An observable that the
  *process writes* — a represented field carrying the index, as the tape
  carries the datum — is not built, and until it is, the collapse recorded
  here is a fact about what an outside observer could learn and not about what
  the process makes available.  The minimum is a minimum over the **declared**
  inputs; a different input family could be shorter.

### CL-RR-16 — three readers, one runner

- **Statement**: the producer family's `Runner` is the interpreter over an
  enablement reader `State → List Nat`.  This family's two machines are that
  machine at two readers: `recordReader s = renabledAt … (previous s)
  s.active` and `depthReader s = r2enabledAt … (before s) (previous s)
  s.active`, with `rstepDet_is_generic` and `r2stepDet_is_generic` both `rfl`,
  the runners and observations identified alongside (`rrunDet_is_generic`,
  `robs_is_generic`, `r2obs_is_generic`), and this family's compatibility
  *derived* from `Runner.obsOf_prefix_add` rather than proved again
  (`robs_prefix_is_generic`).  `Depth.three_readers_one_runner` states the
  three identifications together.
- **Hypotheses**: none.
- **Novelty**: the rung that asked for this named its own failure — that a
  reader would have to see more than the state.  **It does not happen**:
  `previous` and `before` are functions of the state, so a deeper read is
  still a read.  That is the finding, and it is what makes the runner one
  runner rather than three that look alike.
- **Evidence**: `Record.recordReader`, `rstepDet_is_generic`,
  `rnext_is_generic`, `riter_is_generic`, `robs_is_generic`,
  `rrunDet_is_generic`, `robs_prefix_is_generic`; `Depth.depthReader`,
  `r2stepDet_is_generic`, `r2next_is_generic`, `r2iter_is_generic`,
  `r2obs_is_generic`, `three_readers_one_runner`; `tests/test_depth.py`, over
  every deterministic program of each depth on the two-point setting.
- **Falsifier**: a state at which one of the two machines and the generic
  machine at its reader differ.  The Lean says they cannot, by `rfl`.
- **Obligation**: the copies are **not removed**.  `rstepDet`, `rrunDet`,
  `rnext`, `robs`, `r2stepDet` and the rest stay in these files, and so do
  their separate theorems.  What is gone is the excuse for them and the cost
  of the next reader; a reader who wants the duplication actually deleted is
  owed a different change from this one.

### CL-RR-11 — the protocol declared before the readout; the artifact; not delivered

- **Declared first**: the classes, the starts `0, 1, 2`, the scales `1..8`,
  the fuel, the seen observation's program, start and scale, the survivor
  rule (replay) and the separation rule (declared inputs only) are
  constants of `selection.py`, recorded in `declared_before_readout`; nothing
  removes a law after the readout.  A seen observation of the wrong scale,
  a class none of whose laws replays it, and an exhibited pair that does
  not survive are refused by the receipt.
- **The artifact**: the represented execution family's `process.json` is
  read through the observed family's `identify_programs`, never written;
  the finding that its schema loses the operation order is inherited, and
  every run recorded here carries its operation tables in index order.
- **Not delivered**: a record read deeper than *two* entries, and a depth-`d`
  family for general `d`; a Python mirror of the depth-two machine (CL-RR-13
  is proved, not computed); an encoded configuration; an observable that reads which operation fired — the
  residual of the experiment is exactly what such an observable would
  separate; a second locus of activity.  The merged memoryless
  reader does not apply to a record program — several instances of one
  control form leave one record entry and `lookup` refuses such a form — so
  the two machines' agreement is claimed only through `lift_renabled`, not by
  running one reader on the other's program.
