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
- **Not delivered**: a record read deeper than one entry — the ceiling it
  would have to break is now exact (CL-RR-12), and the sealed grammar permits
  the ternary form it would need (`Regime.wf` constrains an arity only by
  `1 ≤ a`), so the obstacle is the construction and not the grammar; an
  encoded configuration; an observable that reads which operation fired — the
  residual of the experiment is exactly what such an observable would
  separate; a second locus of activity.  The merged memoryless
  reader does not apply to a record program — several instances of one
  control form leave one record entry and `lookup` refuses such a form — so
  the two machines' agreement is claimed only through `lift_renabled`, not by
  running one reader on the other's program.
