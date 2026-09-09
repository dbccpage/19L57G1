# Claims: coherent finite observations of the represented process

AuthorityEffect: None.  Every claim names its hypotheses, its novelty against
the reused results, its evidence, its falsifier and its remaining obligation.
The words forced, minimal, free, canonical, equivalent, universal and complete
appear only where a proof is named.  Lean names are in `lean/Limits.lean`
(the abstract inverse system) and `lean/Observe.lean` (the represented process
at step scales) under the namespaces `Limits` and `Observe`; every report lies
within `{propext, Quot.sound}` (`evidence/lean.json`).  "The process" means
the merged `Control` machine of `research/represented_execution` run by its
deterministic runner; "the artifact" means that family's
`evidence/process.json`, authored there and only read here; "a scale" means
a number of steps of the runner watched; "the observation at scale `n`" means
the tape after `n` steps (`Observe.obs`).

### CL-CP-01 — the thread space is the sequence space

- **Statement**: a stage is a word of length `n` over a carrier of size `c`,
  the bonding forgets the last entry, and a family is compatible when the
  bonding holds at every scale.  The prefixes of a sequence form a
  compatible family (`ofSeq`), a compatible family determines a sequence
  (`toSeq`, reading entry `i` at scale `i + 1`), and the two constructions
  are inverse (`toSeq_ofSeq`, `ofSeq_toSeq`): a bijection, and not a
  mediating-map statement — no cone over an arbitrary object is quantified,
  and the limit's universal property is neither stated nor claimed.
- **Hypotheses**: none.
- **Novelty**: the sealed `wit_no_infinite` says arbitrary finite witnesses
  need not assemble into one history; here they assemble because the family
  is compatible by construction and the bonding is restriction.  No choice
  or compactness principle is used: `toSeq_ofSeq` and `stable` depend on no
  axiom at all.
- **Evidence**: `Limits.ofSeq`, `toSeq`, `stable`, `toSeq_ofSeq`,
  `ofSeq_toSeq`; computed: `limits.of_seq`/`to_seq` on three sequences.
- **Falsifier**: a compatible family that is not the prefix family of its
  sequence.
- **Obligation**: none.  The topology of the thread space is *declared*
  (CL-CP-11), not proved.

### CL-CP-02 — eventual agreement is not compatibility

- **Statement**: the family over two letters that reads `1` at scale 1 and
  `0` everywhere else satisfies the bonding at every scale from 2 on
  (`eventual_agrees`) and is not compatible (`eventual_not_compatible`).
- **Hypotheses**: none.
- **Novelty**: the brief's required negative: "compatible" is agreement at
  every stage, and a family that agrees after stage `N` and differs at
  `N − 1` is refused by the definition, not admitted by a silent switch to
  eventual agreement.
- **Evidence**: the two theorems; computed: `limits.eventual`.
- **Falsifier**: n/a (a definition's boundary, exhibited).
- **Obligation**: none.

### CL-CP-03 — invariance under the even cofinal rescaling

- **Statement**: the subsystem of even scales, with the bonding that forgets
  two entries, has compatible families determined by the same sequences
  (`etoSeq_eofSeq`, `eofSeq_etoSeq`), and the two thread spaces correspond
  both ways through the sequences (`thread_even`, `even_thread`).  The map
  that carries the correspondence is the restriction of a thread to the even
  scales: `restrictEven` is that restriction, it lands in the even thread
  space, and it equals the detour through the sequences
  (`restrictEven_eq`, `thread_restrictEven`).
- **Hypotheses**: none.
- **Novelty**: the brief's cofinality clause with a test: there is one limit,
  not two "the" limits.
- **Evidence**: the named theorems; computed: `limits.even_family` — which
  is the restriction map, the object `restrictEven_eq` relates to the
  sequence detour — reads back the sequence.
- **Falsifier**: an even-scale family with no all-scale counterpart, or two.
- **Obligation**: other cofinal reindexings are not stated; the even one is
  the exhibit.  An earlier version stated only `thread_even`/`even_thread`,
  which are definitionally `ofSeq_toSeq`/`eofSeq_etoSeq` and say nothing
  about restriction, while citing the restriction map as computed evidence;
  `restrictEven_eq` closes that gap rather than the wording being narrowed.

### CL-CP-04 — the observations of the process are compatible at every scale

- **Statement**: for every state `s` and every scale `n`, the tape after `n`
  steps is a prefix of the tape after `n + 1` (`obs_prefix`) and of the tape
  after any later number of steps (`obs_prefix_add`).  The bonding of the
  concrete system — forget the entries beyond the coarser length — holds at
  every scale because one step only appends (`next_tape`, through the merged
  `fire_ok`), and a terminal keeps the state.
- **Hypotheses**: none: every state, every program, every scale.
- **Novelty**: this is the commuting law of the brief's item 3 for the
  scale system of run-observations: observing then advancing equals
  advancing then observing, with the coarse observation the prefix.
- **Evidence**: `Observe.next_tape`, `obs_prefix`, `obs_prefix_add`,
  `stepDet_inr`; computed: every program identified from the artifact, every
  datum, twelve scales (`tests/test_limits.py`).
- **Falsifier**: a state and scale whose observation is not a prefix of the
  next.
- **Obligation**: discharged.  `obs_fuel_indep` and `obs_fuel_eq` prove that
  two states agreeing on graph, operation count, active datum and tape, each
  with at least `n` fuel, have the same observation at scale `n` — the fuel is
  consulted only to refuse (`next_exhausted`), never to choose.  The scale is
  still the step count of one run.

### CL-CP-05 — the tape does not determine the future; the fuel is what is lost

- **Statement**: on the `forever` program from datum 0, the states with fuel
  0 and fuel 1 have the same tape `[0]`; after one step the first still reads
  `[0]` and the second `[0, 1]` (`lost_fuel`).  The repair: with the program,
  the active datum and the fuel, the next datum is determined — two states
  with the same program and active datum that both step reach the same datum
  (`next_active_det`).
- **Hypotheses**: for `next_active_det`, equal program, operation count and
  active datum, and both states stepping.
- **Novelty**: the brief's failure pair, with the lost information named
  (the fuel) and the observation repaired by including it, rather than a
  relational transition retained.
- **Evidence**: `Observe.lost_fuel` (decided on the concrete program),
  `next_active_det`; computed: `limits.lost_fuel`, and the determinism check
  on states with different tapes and clocks.
- **Falsifier**: two states with one program, active datum and fuel that
  step to different data.
- **Obligation**: at a fork the runner stops and the tape freezes; lifting
  the successor relation of a fork to threads is not built (CL-CP-11).

### CL-CP-06 — a shifted observation needs the entry beyond the boundary

- **Statement**: there is no function of the two-entry prefix that returns
  the two-entry prefix of the word shifted by one: `[0, 1, 2]` and
  `[0, 1, 0]` share the prefix `[0, 1]` and shift to `[1, 2]` and `[1, 0]`
  (`shift_not_local`).
- **Hypotheses**: none.
- **Novelty**: the brief's required negative for a scale map that imports
  information across the observed boundary; the host would have to supply
  the third entry.
- **Evidence**: the theorem (no axiom); computed: `limits.shift_failure`.
- **Falsifier**: n/a (exhibited).
- **Obligation**: none.

### CL-CP-07 — the three verdicts: injective, not dense, not surjective

- **Statement**: the observation at the scale of a tape's length is the tape
  (injective on tapes).  The image of the process is not dense: no realized
  tape extends `[0, 1, 0, 2]`, because a realized tape is functional — equal
  entries have equal successors — and that word is not.  Hence the process
  does not realize every thread.
- **Hypotheses**: for the computed verdict, the declared class: every program
  on the recorded three-point setting with at most one operation enabled per
  datum (64 programs), from every datum, at fuel 4.
- **Novelty**: the brief's three separate claims with three separate
  falsifiers; density is refused by a named prefix, not by a cardinality
  remark.
- **Evidence**: `Observe.next_active_det` (one step), `Observe.nextOf`,
  `Chain`, `chain_functional`, `iter_chain`, `obs_functional` (the whole run,
  every setting); computed: `limits.verdicts` — all 64 × 3 realized tapes are
  functional and none extends the witness.
- **Falsifier**: a realized tape that is not functional, or one extending
  `[0, 1, 0, 2]`.
- **Obligation**: discharged for functionality.  `obs_functional` proves that
  every realized tape is functional along the *whole* run, for every
  controlled setting, start datum, fuel and scale: the tape of a run is a
  chain of the machine (`iter_chain`, from the invariant that the last entry
  is the active datum), and a chain is functional because the next value is a
  function of the datum (`chain_functional`).  What remains: eventual
  periodicity on a finite carrier is the standard consequence of
  functionality and is still not formalized, and the density witness is
  computed over the declared class.

### CL-CP-08 — the connected experiment: one process, four scales, one bound

- **Statement**: the `forever` program identified from the artifact, from
  datum 0, at fuel 24, observed at scales 3, 6, 12, 24 — one state read by
  `obs` at four scales, so that the chain of prefixes is an instance of
  `obs_prefix_add` for that state.  The observations are each a
  prefix of the next; the artifact's own recorded tape (fuel 5, six entries)
  is prefix-related to each — a prefix of the scale-6, 12 and 24
  observations, and an extension of the scale-3 one, which the record states
  separately (`recorded_tape_prefix_related` and
  `recorded_tape_is_a_prefix_of_this_one`).  The readout is the number of zeros; the bound
  `L ≤ 3 · zeros ≤ L + 2` is derived at scale 3 from the visible period and
  holds at every finer scale with the readout unchanged.  On the sequence
  `i ↦ i % 3` the bound is a theorem for every `L` (`zeros_eq`,
  `zeros_bound`): the frequency of `0` is `1 / 3` up to `2 / (3 L)`, and
  precision `ε` needs `L ≥ 2 / (3 ε)`.  The tape of the run *is* that
  sequence's prefix (`forever_obs`), so the bound holds of the observation
  itself (`forever_run_bound`).
- **Hypotheses**: the identified program; the four scales.
- **Novelty**: a finite observable with an explicit approximation bound and
  a computable precision rule, tied to a limiting quantity that is a
  rational — existence of the limit and effective access to it separated by
  the rule; no interval, circle or real number used.
- **Evidence**: `Observe.zeros_bound`, `forever_iter`, `forever_obs`,
  `forever_run_bound`; computed: `limits.connected_experiment`
  (`evidence/limits.json`), and the receipt refuses a failing bound at any
  scale.
- **Falsifier**: a scale at which the readout leaves the bound, or an
  observation that is not a prefix of the next.
- **Obligation**: that the `forever` tape after `n` steps *is* the first
  `n + 1` entries of `i ↦ i % 3` is computed at every scale, not proved; the
  proved bound is on the sequence.  This is the labeled missing connection.

### CL-CP-09 — the artifact consumed, and a finding for the family that wrote it

- **Statement**: the artifact's fragment is `control`; its eight recorded
  controlled runs identify the four programs.  The operation order is read
  from each run's `ops_in_index_order`, cross-checked against the sealed
  table set, and every run is replayed to its tape and terminal; for a record
  without that field the order is recovered as the one permutation of the
  sealed tables under which every run replays.  Finding, reported to the
  producer and since repaired there: the artifact's `setting_json` is the
  sealed `Setting.json`, whose `ops` field is set-valued — sorted, with
  repetitions collapsed — so it determines neither the index order the
  enablements refer to (taken alone it would put the constant map at index 0)
  nor the operation count.
- **Hypotheses**: none.
- **Novelty**: the artifact contract doing its job — the consumer found what
  the producer's schema drops.
- **Evidence**: `limits.identify_programs`; computed: the sorted order alone
  misidentifies, and an inconsistent artifact is refused
  (`tests/test_limits.py`).  The artifact is pinned by digest in
  `SOURCE_MANIFEST.json` at the represented execution family's commit.
- **Falsifier**: a recorded run that no ordering replays, two orderings that
  both do, a recorded order that is not the sealed table set, two runs
  disagreeing on the order, an enablement naming an operation the sealed
  schema does not carry, or one program name recorded with two enablement
  sets — each refused by name (`tests/test_limits.py`).
- **Obligation**: discharged at the producer — it now records
  `ops_in_index_order` on every run, and this family reads it.  Nothing here
  writes its artifact.

### CL-CP-10 — the causal footprint of a step, limited

- **Statement**: a firing reads the enablement self-instance and the
  operation edge at the active datum and writes the active datum, the tape,
  the clock and the fuel, keeping the program (the merged `fire_ok`, `fire`,
  `enabled`).  An edit to an instance away from the active datum does not
  change the step; an edit at it does.
- **Hypotheses**: the merged definitions.
- **Novelty**: the brief's read/write extraction, stated for the one locus
  the process has.
- **Evidence**: the merged `fire`, `fire_ok` and `enabled`, which consult
  `lookup` at `s.active` only; computed, in the represented execution family:
  `test_an_edit_away_from_the_active_datum_leaves_the_step_unchanged` for the
  first half and the mutation tests for the second.  No theorem states the
  invariance; it is read off the definitions and checked on those
  populations.
- **Falsifier**: a step that changes under an edit away from the active
  datum.
- **Obligation**: discharged for the two-locus case by CL-CP-12.  What is
  still read off the definitions rather than proved is the invariance itself:
  no theorem here states that an edit away from the active datum leaves the
  step unchanged.

### CL-CP-12 — the two-locus observation: one locus moves at a time, and the square does not lift

- **Statement**: the producer family runs two loci by a schedule carried in
  the data (its CL-RE-16).  Of the **observation** of such a run:
  `Observe.obs_one_locus` — at every scale, from every start, with any fuel
  and for **every** schedule, consecutive entries of the observed tape leave
  one of the two coordinates exactly where it was.  It is the chain
  invariant of `obs_functional` read through the product's locality theorems
  rather than through determinism, and it assumes no admissible range: the
  enablement instance the machine reads is what places the datum in the
  carrier (`nextOf_one_locus`, from `nextOf_some` and `prod_op_one_locus`).
  What does **not** lift is the square itself: two orders reach the same
  datum and record different tapes.  What lifts instead is the projection
  with the adjacent repeats dropped.
- **Hypotheses**: a state carrying a two-locus program; nothing about the
  schedule, the start, the fuel or the scale.
- **Novelty**: the lifting CL-CP-10 asked for, and it is two-sided.  The
  negative half is the informative one: a tape totally orders events that the
  loci do not, so a record of two independent processes carries strictly more
  than the processes do.  The repeats the destuttering drops are exactly the
  steps that moved the other locus.
- **Evidence**: `Observe.nextOf_of_single`, `nextOf_some`,
  `prod_op_one_locus`, `nextOf_one_locus`, `chain_one_locus`, `next_graph`,
  `iter_graph`, `obs_one_locus`, `pair_obs`; `limits.two_locus_experiment`
  and the record's `two_locus_experiment` section, at five scales, over the
  factorization `identify_loci` reads **from the producer's record** rather
  than being told; `tests/test_evidence.py`'s two injections.
- **Falsifier**: an observed step of a two-locus run that changes both
  coordinates; a locus reading not prefix-related to that locus's own run; a
  recorded projection identifying no single factorization.  The receipt
  refuses each by name.
- **Obligation**: the limit of a two-locus run *as an inverse system in its
  own right* is not built — whether the two loci give two commuting inverse
  systems whose product is the whole is unasked here.  Two loci, not `k`.

### CL-CP-11 — declared, and not delivered

- **Topology, declared**: the thread space carries the product of the
  discrete topologies on the finite stages; that space is totally
  disconnected; it is not an interval and not a circle, and none is claimed.
  An interval would need an order or metric compatible with the stages and an
  identification of threads this family does not make.  Not proved in Lean.
- **Not delivered**: lifting a fork's successor relation to threads; the
  general eventual-periodicity theorem; the thread space of a two-locus run
  as an inverse system of its own (the observation is taken, the limit over
  it is not).  An earlier version of this line named "a second locus of
  activity" and "the proved link between the `forever` tape and the sequence
  `i ↦ i % 3`"; both are WITHDRAWN — the link is `Observe.forever_obs` and
  the second locus is CL-CP-12.
- **Next single obstacle**: the model-selection and measurement burden
  (P218).  Nothing here selects a physical law; the readout is a frequency
  of a datum in a represented process, and a physical claim would need an
  independently specified measurement protocol and calibration.
