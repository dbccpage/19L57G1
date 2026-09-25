# PREDICTIONS: rung four -- the first-demand index up to the implemented isomorphism

`AuthorityEffect: None`.  Frozen by sha256 before the first computation
and before any Lean of this rung is built.  Scored mechanically by
`run_iso.py` for the computational rows and by `test_census.py` for the
census rows.  A missed prediction is recorded next to its value and never
edited.  A miss is a finding, not a defect.

Each prediction carries a falsifier and an explicit FORCED / NOT FORCED
label.  FORCED means the outcome follows from definitions already fixed
before this rung, so a hit evidences the ordering of the work and not
insight.  NOT FORCED means the run could have come out the other way.

## Declared before the compile: the FW-DEF census this rung commits to

The census below is a prediction, not a report.  Four classes, as the
sibling rungs use them: RECONSTRUCTION (reproduced verbatim under a pin,
not this rung's work); DEFINITION (true by unfolding, by `rfl`, by a
projection, by one rewrite, by kernel computation over concrete objects,
or by pure case exhaustion); THIN (one genuine step, or a direct
corollary of a neighbour); CONTENT (everything else).

Predicted DEFINITION:

- `separable_symm`
- `collapsed_symm`
- `uniform_freeStake`
- `uniform_allApart`
- `uniform_allSame`
- `stepE_renameSupply`
- `parity_not_uniform`
- `chain_not_uniform`
- `residue_not_uniform`
- `demand_not_class_invariant`
- `first_count_not_trajectory_invariant`
- `iso_index`

Predicted THIN:

- `honour_symm`
- `dmap_inj`
- `separable_fwd`
- `separable_transport`
- `honour_transport`
- `hasDemand_transport_of_uniform`
- `hasDemand_iff_of_uniform`
- `matched_symm`
- `replayE_renameSupply`
- `first_demand_renameSupply`
- `separable_of_unary_witness`
- `index_P2_parity`
- `quiet_P1_parity`
- `index_P2_chain`
- `quiet_P1_chain`
- `index_Q2_residue`
- `quiet_Q1_residue`

Predicted CONTENT:

- `demand_transport`
- `first_demand_matched_of_uniform`
- `unary_ctx_slots`
- `collapsed_of_unary`
- `honourCheck_sound`
- `noDemandCheck_sound`
- `demandCheck_sound`
- `matched_P`
- `matched_Q`

The names above are the ones this rung commits to before Lean has run.  A
name that changes, a target promoted or demoted between classes, or a
declaration added beyond this list is visible in the committed census and
is recorded in `STATUS.md` as unpredicted work.

## Stage one -- transport of a demand across the isomorphism

- **J-1** (NOT FORCED).  `separable_fwd` and `separable_transport` are
  PROVED over the reconstructed sealed grammar, with no decidability
  hypothesis: separability of two admitted data transports along the
  datum bijection of a sealed isomorphism, in both directions, by carrying
  the witnessing context and never by deciding collapse.
  Falsifier: OPEN, or a proof that needs a decision of collapse or
  separability, or one that needs `Classical.choice`.
- **J-2** (NOT FORCED).  `demand_transport` is PROVED: a demand of a
  stake at a regime is carried to a demand at any isomorphic regime,
  provided the stake gives the image of each held pair, ordered, the
  label it gives the pair.  Hence `hasDemand_iff_of_uniform`: under a
  UNIFORM stake, carrying a demand is invariant under the isomorphism,
  for every pair of regimes the isomorphism relates, reachable or not.
  Falsifier: OPEN, or the invariance needing a hypothesis beyond
  uniformity and the isomorphism.
- **J-3** (FORCED).  The free stake, the stake labelling every distinct
  pair apart and the stake labelling every distinct pair same are
  uniform, at the level of a definition; `one_sided_total` induces the
  same labels as the second on every pair.
  Falsifier: any of the three needing more than unfolding.
- **J-4** (NOT FORCED).  Uniformity is sufficient and this rung does NOT
  prove it necessary.  Whether a stake that is not uniform can still
  make carrying a demand invariant is recorded as a named leftover with a
  candidate named, and is not proved in either direction.
  Falsifier: the committed Lean proving necessity, or refuting it.

## Stage two -- the countermodels for the three stakes that are not uniform

- **J-5** (NOT FORCED).  `parity`, `chain` and `residue_three`, declared
  in Lean with the labels the sibling Python rules give, are each not
  uniform, and for each there are two isomorphic regimes of which one
  carries a demand and the other none.  The witnessing regimes use only
  judgment forms of arity one; the pair for `parity` and for `chain` holds
  three data, and the pair for `residue_three` holds four.
  Falsifier: any of the three having no such pair in the committed Lean,
  or a witness needing a form of arity two, or the stated data counts
  differing.
- **J-6** (NOT FORCED).  `first_demand_matched_of_uniform` is PROVED:
  under a uniform stake, two class-matched histories have exactly the
  same first counts, with no decidability hypothesis and no hypothesis on
  the bases.
  Falsifier: OPEN, or a hypothesis beyond uniformity and matching.
- **J-7** (NOT FORCED).  Under each of `parity`, `chain` and
  `residue_three` there are two class-matched histories from the empty
  base, one with a first count and one with none at any count.  For
  `parity` and `chain` one pair of histories serves both, of eight events,
  with two forms of arity one and three data, and its first count is
  eight.  For `residue_three` the pair has eleven events, three forms of
  arity one and four data, and its first count is eleven.  The two
  histories of each pair differ only in their one uniform-rule
  admission.
  Falsifier: any of the three without such a pair in the committed Lean,
  or any stated length, count or first count differing.
- **J-8** (NOT FORCED).  Whether a shorter class-matched pair with
  differing first counts exists, for any of the three stakes, is NOT
  decided by this rung between the rectangle's bound of four events and
  the exhibited lengths; it is recorded OPEN at lengths five to seven for
  `parity` and `chain`, and five to ten for `residue_three`.
  Falsifier: the rung claiming a minimum length it has not enumerated.

## Stage three -- presentation tokens

- **J-9** (FORCED).  `first_demand_renameSupply`: renaming the tokens
  every supply of a history carries leaves every first count unchanged,
  because the reconstructed step ignores a supply's token and the Lean
  datum admission carries none.
  Falsifier: it needing more than an induction on the history.

## Stage four -- the finite cross-check

The bases, the bound and the alphabet are rung three's and are not chosen
after seeing a count.

- **Declared rectangle.**  Rung three's, consumed through its public
  functions and pinned by blob: the EMPTY base and the sealed readings L
  and F; every sequence of at most four events of the declared alphabet,
  without pruning; at most five data and at most two forms.
- **Declared stakes.**  Rung three's seven.
- **Declared orbit bound.**  Every bijection pair on the datum and form
  indices of one representative of each class of regimes reached: at most
  one hundred and twenty datum bijections times two form bijections, two
  hundred and forty pairs.
- **Declared token renaming.**  The five fresh tokens taken in reverse
  order, and the supply token replaced by a declared sixth token that no
  base carries.
- **J-10** (FORCED).  Replay of rung three's receipt: 577 sequences from
  EMPTY, 3928 from L, 14293 from F; every node replays from its base.
  Falsifier: any count differing, or one replay mismatch.
- **J-11** (NOT FORCED).  On every regime the rectangle reaches, the
  sealed key procedure and the brute-force minimum give the same
  partition into classes; the count of disagreements is zero.  The count
  of classes is strictly smaller than the count of distinct regimes.
  Falsifier: one disagreement, or no class with two reached regimes.
- **J-12** (NOT FORCED).  On every regime the rectangle reaches, the
  sealed automorphism list has the length of a brute-force count over
  every bijection pair; the count of disagreements is zero.  The smallest
  size is one and the largest is twenty-four.
  Falsifier: one disagreement, or either extreme differing.
- **J-13** (NOT FORCED).  Under the four uniform-labelled stakes -- the
  free stake, `total_apart`, `total_same`, `one_sided_total` -- no class
  of reached regimes holds one carrying a demand and one carrying none,
  and no class does so when every renaming of its representative is
  taken: both counts are zero.
  Falsifier: any nonzero count.  This is the rectangle's check of J-2,
  not its proof.
- **J-14** (NOT FORCED).  Under each of `parity`, `chain` and
  `residue_three`, at least one class of reached regimes holds a reached
  regime carrying a demand and a reached regime carrying none; and at
  least one class does so when every renaming is taken.
  Falsifier: any of the six counts zero.
- **J-15** (NOT FORCED).  Quotient the sequences of all three bases by the
  class of their whole prefix trajectory.  Under every one of the seven
  stakes, the first count is constant on every class: the count of
  classes with a varying first count is zero.  At least one trajectory
  class has more than one member.
  Falsifier: any nonzero count, or every class a singleton.  A HIT for
  `parity`, `chain` and `residue_three` is a property of the declared
  bound and not of the stake, by J-7.
- **J-16** (NOT FORCED).  Quotient the sequences instead by the class of
  the regime the whole sequence reaches.  Under each of the six stakes
  other than the free stake, at least one such class carries two
  different first counts; under the free stake none does.
  Falsifier: any of the six at zero, or the free stake above zero.
- **J-17** (NOT FORCED).  The declared token renaming moves no first
  count under any stake and moves no prefix out of its class, at any
  sequence of the rectangle: both counts are zero.  It does change the
  presentation of at least one reached regime, so the check is not
  vacuous.
  Falsifier: a moved count or class, or no changed presentation.
- **J-18** (FORCED).  The exhibited histories of J-7, replayed in Python
  through the sealed step with declared tokens, reach prefix regimes the
  sealed key procedure puts pairwise in one class, and give by rung
  three's forward procedure the first counts J-7 states.
  Falsifier: any prefix pair in two classes, or any count differing.
- **J-19** (FORCED).  The receipt regenerates byte-identically, carries
  no timestamp and no environment value, and stays under one megabyte.
  Falsifier: a byte difference, a forbidden key, or an oversized receipt.

## Stage five -- gates and the census of challenge five

- **J-20** (NOT FORCED).  Every theorem of this rung's Lean package
  depends on no axiom outside `propext` and `Quot.sound`, and the
  committed axiom log matches a fresh build report for report.
  Falsifier: any other axiom, or a difference between the log and a fresh
  build.
- **J-21** (NOT FORCED).  This rung decides exactly two rows of the seed's
  challenge-five census over the rectangle: succession, a second time --
  the first count is not a class invariant in general, and is an
  invariant of class-matched trajectories exactly under the proved
  sufficient condition of uniformity -- and symmetry, as DEFINABLE: the
  size of the automorphism group is computed by an implemented algorithm
  at every regime reached and agrees with a brute-force count.
  Falsifier: the ledger deciding another set of rows, or either in
  another direction.
- **J-22** (NOT FORCED).  The measured wall time of this rung's own gates
  stays under fifteen minutes, as the seed requires, and is recorded in
  `STATUS.md`.
  Falsifier: a measured time at or above fifteen minutes.

## What this rung does not predict

Nothing about the count of declared inputs, in either direction: this
rung neither reduces it nor proves it at a floor, and its receipt records
that claim as absent.  Nothing about the rows of the challenge-five census
beyond succession and symmetry.  Nothing about the frozen extrapolation
of rung three, which stays PENDING.  Nothing about the sealed estate's
standing obstructions, which this rung leaves exactly where it found
them.
