# PREDICTIONS: rung six -- succession through the element count

`AuthorityEffect: None`.  Frozen by sha256 before the first computation
and before any Lean of this rung is built.  Scored mechanically by
`run_succession.py` for the computational rows and by `test_census.py`
for the census rows.  A missed prediction is recorded next to its value
and never edited.  A miss is a finding, not a defect.

Each prediction carries a falsifier and an explicit FORCED / NOT FORCED
label.  FORCED means the outcome follows from definitions or receipts
already fixed before this rung, so a hit evidences the ordering of the
work and not insight.  NOT FORCED means the run could have come out the
other way.

Receipts and sources read before freezing, because a prediction below
leans on them: rung four's `receipts/iso_index.json` (577, 3928 and 14293
sequences; 75, 523 and 1718 distinct regimes at EMPTY, L and F; 402
classes); rung five's `receipts/symmetry.json` and its theorem
`size_counts_changes`; and the sealed Python genesis readings, whose
histories are six events with two datum admissions (L) and seven events
with three datum admissions (F), with no requirement at either.  The
sealed Lean reading regimes carry a requirement and are used here only
for the Lean countermodel named in M-4, never for a Python count.

## Declared before the compile: the FW-DEF census this rung commits to

Four classes, as the sibling rungs use them: RECONSTRUCTION (reproduced
verbatim under a pin, not this rung's work); DEFINITION (true by
unfolding, by `rfl`, by a projection, by one rewrite, by kernel
computation over concrete objects, or by pure case exhaustion); THIN (one
genuine step, or a direct corollary of a neighbour); CONTENT (everything
else).

Predicted DEFINITION:

- `replayE_cons`
- `size_genesis`
- `supply_uncounted`
- `every_splits`
- `admitting_splits`
- `base_matters`

Predicted THIN:

- `insertNew_grows`
- `step_grows`
- `changes_path_free`
- `changes_from_genesis`
- `changes_given_base`
- `changes_le_admitting`
- `admitting_le_every`
- `every_not_given_base`
- `admitting_not_given_base`
- `changing_not_of_regime`

Predicted CONTENT:

- `changes_counted`

The names above are the ones this rung commits to before Lean has run.  A
name that changes, a target promoted or demoted between classes, or a
declaration added beyond this list is visible in the committed census and
is recorded in `STATUS.md` as unpredicted work.  Two of them repeat, as
statements, theorems rung five proved (`step_grows` its `size_step`,
`changes_counted` its `size_counts_changes`); they are proved again here
so that the package imports nothing, and the ledger credits the
statements to rung five.

## Stage one -- the three readings in Lean

- **M-1** (NOT FORCED).  Under CHANGING, `changes_counted` is PROVED for
  every base and every history that replays: the element count of the
  regime reached is the base's count plus the count.  `changes_path_free`
  (two histories from one base to one regime carry one count) and
  `changes_given_base` (a function of base and regime gives the count)
  follow as corollaries.  No decidability hypothesis, and no hypothesis
  beyond the replay.
  Falsifier: any of the three OPEN, or needing a further hypothesis.
- **M-2** (FORCED).  `changes_from_genesis`: from the sealed empty regime
  the count under CHANGING equals the element count of the regime
  reached, with no base named.
  Falsifier: it needing more than M-1 and `size_genesis`.
- **M-3** (FORCED).  Under EVERY and under ADMITTING the count is NOT a
  function of base and regime.  `every_splits`: from the empty regime,
  the empty history and a single supply reach one regime with counts
  zero and one.  `admitting_splits`: from the empty regime, a form of
  arity one with its uniform rule admitted once, and the same with the
  rule admitted twice, reach one regime with counts two and three.  Both
  by kernel computation; `every_not_given_base` and
  `admitting_not_given_base` refute every function of base and regime.
  Falsifier: either countermodel failing to compute, or a theorem
  proving the opposite.
- **M-4** (FORCED).  Under CHANGING the count is NOT a function of the
  regime alone: the sealed reading-L regime is reached from the empty
  regime by the sealed reading-L history with count three and from
  itself by the empty history with count zero (`base_matters`), so
  `changing_not_of_regime` refutes every function of the regime alone.
  Falsifier: `base_matters` failing to compute.
- **M-5** (FORCED).  For every base and every history, the count under
  CHANGING is at most the count under ADMITTING, which is at most the
  count under EVERY (`changes_le_admitting`, `admitting_le_every`).
  Falsifier: either OPEN, or needing the history to replay.
- **M-6** (NOT FORCED).  No theorem statement of this package mentions
  the sealed isomorphism: that the count is a function of the class of
  the regime is NOT proved here and stays OPEN beyond the rectangle, with
  rung five's Z-1 as the named obstacle.
  Falsifier: the committed Lean proving it, or the ledger claiming it.
- **M-7** (FORCED).  Every theorem of the package has axioms within
  `{propext, Quot.sound}`, and none reaches `Classical.choice`.
  Falsifier: the committed axiom log naming any other axiom.

## Stage two -- the finite cross-check

The bases, the bound and the alphabet are rung three's and are not
chosen after seeing a count.

- **Declared rectangle.**  Rung three's, consumed through rung four's
  public population: three bases (EMPTY, L, F), every sequence of at most
  four declared events.  A regime is SPLIT under a reading at a base when
  two sequences of that base reaching it carry different counts.  The
  SHORTEST SPLITTING SEQUENCE of a reading at a base is the shortest
  sequence whose count differs from that of a sequence of that base of no
  greater length reaching the same regime.
- **M-8** (FORCED).  577, 3928 and 14293 sequences; 75, 523 and 1718
  distinct regimes; zero replay mismatches.
  Falsifier: any other value.
- **M-9** (NOT FORCED).  Under CHANGING, at every base: zero split
  regimes; on every sequence the count equals the element count of the
  regime reached minus that of the base; and on every sequence, counted
  from the sealed empty regime through the base's sealed genesis history
  followed by the sequence, the count equals the element count of the
  regime reached.  Zero violations of each.
  Falsifier: any split regime or any violation.
- **M-10** (NOT FORCED).  Under EVERY, at every base, at least one regime
  is split and the shortest splitting sequence has one event, a supply.
  Under ADMITTING, at every base, at least one regime is split, and the
  shortest splitting sequence has three events at EMPTY and two at L and
  at F.
  Falsifier: an unsplit base under either reading, or any other length.
- **M-11** (NOT FORCED).  At every base, more regimes are split under
  EVERY than under ADMITTING.
  Falsifier: equal or fewer at any base.
- **M-12** (FORCED given M-9 and the base counts of M-13).  Taken up to
  the implemented isomorphism: within each base, no class is reached
  with two counts under CHANGING.  At least one class is reached from
  more than one base; for every such class the base-relative counts
  under CHANGING differ between its bases, and the counts from the
  sealed empty regime agree.
  Falsifier: a class with two counts within a base; no class shared by
  two bases; a shared class whose base-relative counts agree, or whose
  counts from the empty regime differ.
- **M-13** (FORCED).  The element counts of the three bases are zero,
  two and three.  The sealed genesis histories of L and F carry, under
  EVERY, ADMITTING and CHANGING, the counts six, two and two (L) and
  seven, three and three (F).
  Falsifier: any other value.

## Stage three -- the census row and the input count

- **M-14** (NOT FORCED).  The ledger decides one row of the
  challenge-five census, succession, under the three declared readings:
  under CHANGING, DEFINABLE as a function of base and regime (PROVED for
  every history of the sealed step), and as a function of the regime
  alone when counted from the sealed empty regime (PROVED), but not a
  function of the regime alone across bases (COUNTERMODEL); under EVERY
  and ADMITTING, NOT DEFINABLE from base and regime (COUNTERMODEL); up
  to the isomorphism, a finite computation on the rectangle and OPEN
  beyond it.  FORCED in the seed's sense is conditional on an engine
  whose accepted rounds are the changing events of the sealed step, and
  no such engine exists yet; the row says so.  Rung three's and rung
  four's readings of the row stand and are not superseded.
  Falsifier: the ledger recording the row without that condition, or
  recording a reading of rung three or four as withdrawn.
- **M-15** (FORCED).  This rung neither reduces the count of declared
  inputs nor proves it at a floor; the value stays two.
  Falsifier: any claim otherwise.
- **M-16** (FORCED).  The receipt regenerates byte-identically, every
  node replays from its base, and the grouped gate time stays under
  fifteen minutes.
  Falsifier: a regeneration difference, a replay mismatch, or a measured
  time over the ceiling.
