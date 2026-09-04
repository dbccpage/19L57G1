# PREDICTIONS: rung two, track one -- no first demand

`AuthorityEffect: None`.  Frozen by sha256 before the first computation
and before any Lean of this rung is built.  Scored mechanically by
`run_nofirst.py`.  A missed prediction is recorded next to its value and
never edited.  A miss is a finding, not a defect.

Each prediction carries a falsifier and an explicit FORCED / NOT FORCED
label.  FORCED means the outcome follows from the definitions already
fixed, so a hit evidences the ordering of the work and not insight; the
run says so rather than claiming credit.  NOT FORCED means the run could
have come out the other way.

## Declared before the compile: which targets are at the level of a definition

The FW-DEF census below is a prediction, not a report.  It is the labels
this run commits to before Lean has run, so that a target promoted or
demoted afterwards is visible as a change.

Predicted at the level of a definition (true by unfolding, by `rfl`, or by
one rewrite of a structure field):

- `stake_irrefl`
- `demands_subset_labelled`
- `free_stake_no_demand`
- `demand_needs_label`
- the negative half of `growth_generates_apart` and of
  `growth_generates_same` (the fresh index is not a held index before the
  growth, so the pair was not a demand)

Predicted NOT at the level of a definition:

- `reconstruction_matches`
- `supply_preserves_demands`
- `supplies_preserve_regime`
- `grammar_carries_no_stake`
- `demand_depends_only_on_the_label`
- `no_first_demand`
- `demand_iff_apart_of_no_insts`
- `apart_demand_of_no_forms`
- `fresh_profile`
- the positive half of `growth_generates_apart` and of
  `growth_generates_same`
- `apart_at_most_one`
- `apart_at_most_one_new_demand`

## Stage one -- the reconstruction

- **N-1** (FORCED).  `stake_irrefl`, `demands_subset_labelled`, and
  `free_stake_no_demand` are each at the level of a definition and are
  labelled so in the ledger and in `STATUS.md`.
  Falsifier: any of the three needing an argument beyond unfolding, a
  `rfl`, or one rewrite of the irreflexivity field.
- **N-2** (NOT FORCED).  `reconstruction_matches` is PROVED: the demands
  of the two-sided stake induced by a one-sided commitment, read over the
  represented state, are the same list as the pinned one-sided demands,
  at every represented state, with no side hypothesis.
  Falsifier: an OPEN at a named mismatch, or a proof needing a hypothesis
  beyond the two definitions.

## Stage two -- no demand without a stake

- **N-3** (NOT FORCED).  `supply_preserves_demands` is PROVED over the
  sealed regime for every stake, citing the reconstructed sealed supply
  theorem.
  Falsifier: OPEN, or a proof that does not go through that theorem.
- **N-4** (FORCED).  `demand_needs_label` is at the level of a
  definition, because the demand predicate carries the labelling
  condition as a conjunct.
  Falsifier: the predicate as written not carrying it.
- **N-5** (NOT FORCED).  `grammar_carries_no_stake` is PROVED as an
  exhaustive case statement over the reconstructed event type, and the
  number of kinds it enumerates equals the number the rung-zero census
  recorded.
  Falsifier: the case statement not closing, or the two counts differing.
- **N-6** (NOT FORCED).  `no_first_demand` is PROVED as one conjunction
  of five conjuncts, each proved separately, stated once with its scope
  in the same sentence.
  Falsifier: any conjunct OPEN, or the conjunction needing a hypothesis
  none of its conjuncts needs.
- **N-7** (NOT FORCED).  At a regime with no admitted instance, a held
  pair is a demand exactly when the stake labels it apart
  (`demand_iff_apart_of_no_insts`), and both directions are PROVED.
  Falsifier: either direction OPEN, or a countermodel at an
  instance-free regime.

## Stage three -- demands propagate

- **N-8** (NOT FORCED).  `growth_generates_apart` and
  `growth_generates_same` are both PROVED over the sealed regime, each in
  the form "is a demand of the grown regime and was not a demand before".
  Falsifier: either OPEN, or either provable only with a hypothesis that
  already asserts the conclusion.
- **N-9** (NOT FORCED).  The apart form is PROVED in a version whose
  collapse hypothesis is discharged from "no admitted instance" rather
  than assumed.
  Falsifier: no such version, so the hypothesis must be carried.
- **N-10** (NOT FORCED).  `fresh_profile` is PROVED: at a well-formed
  regime, a well-formed context derives the datum admitted by one growth
  step exactly when the context's form carries a uniform rule.
  Falsifier: OPEN, or a counterexample at a well-formed regime.
- **N-11** (NOT FORCED).  `apart_at_most_one` is PROVED: under the stake
  labelling every distinct pair apart, a regime carrying no demand has at
  most one held datum whose profile is empty.  The sibling two-sided tree
  records the corresponding statement as a conjecture with no Lean; this
  rung either proves it over the sealed regime or records OPEN at the
  exact obstruction.
  Falsifier: OPEN, or a demand-free regime under that stake with two held
  data of empty profile.
- **N-12** (NOT FORCED).  `apart_at_most_one_new_demand` is PROVED: from
  a well-formed regime carrying no demand under that stake, one growth
  step generates at most one demand.
  Falsifier: OPEN, or two distinct held data both carrying a demand with
  the fresh datum after one growth step from a demand-free well-formed
  regime.

## Stage four -- the finite cross-check

The bound and the alphabet are frozen here and are not chosen after
seeing a count.

- **Declared rectangle.**  From each of the two sealed genesis readings,
  every sequence of at most four sealed events, enumerated without any
  pruning lemma, over the declared alphabet: one supply of one declared
  token; one datum admission per step, with a fresh token drawn from a
  declared list; a form admission of arity one and of arity two; an
  instance admission for every admitted form index and every argument
  tuple within the data bound; a rule admission for every admitted form
  index; and an imposition for every ordered pair of held data.  Within
  the rectangle, at most five data and at most two forms; a sequence
  proposing a sixth datum or a third form is not extended, and the count
  of sequences stopped that way is recorded.
- **Declared stakes.**  The free stake; the five stakes the sibling
  two-sided tree declares, consumed through that tree's public functions
  and pinned by blob; and the stake induced by the pinned one-sided total
  commitment.
- **N-13** (FORCED).  Under the free stake the demand set is empty at
  every regime of the rectangle.
  Falsifier: one non-empty free-stake demand set.
- **N-14** (FORCED).  Every demand recorded anywhere in the rectangle is
  at a pair its stake labels apart or same.
  Falsifier: one demand at a pair labelled free.
- **N-15** (NOT FORCED).  For every reading and every stake, no sequence
  of the rectangle carries a demand at an event index before the index at
  which a labelled pair is first dishonoured; that is, the first demand
  and the first dishonoured labelled pair occur at the same index in every
  sequence that has either.
  Falsifier: one sequence whose first demand index differs from its first
  dishonoured-labelled-pair index.
- **N-16** (NOT FORCED).  Of the six sealed event kinds, exactly two never
  change the demand set of any stake at any regime of the rectangle.
  Falsifier: any count other than two.
- **N-17** (NOT FORCED).  At every regime of the rectangle that carries no
  demand under the stake labelling every distinct pair apart, at most one
  held datum has the empty profile; and one growth step from such a regime
  adds at most one demand.
  Falsifier: one such regime with two empty profiles, or one growth step
  adding two demands.
- **N-18** (NOT FORCED).  The stake induced by the pinned one-sided total
  commitment and the sibling's all-apart stake give the same demand set at
  every regime of the rectangle.
  Falsifier: one regime where they differ.
- **N-19** (FORCED).  The receipt regenerates byte-identically, and the
  independently written second enumerator reaches exactly the same set of
  regimes as the first on the declared cross-check family.
  Falsifier: a byte difference, or a regime reached by one enumerator and
  not the other.

## The extrapolation

- **N-X** (NOT FORCED).  **Statement.**  Let the operator packet's rung
  four declare a removal grammar: the sealed grammar extended by an event
  that withdraws a held datum.  The at-most-one bound this rung proves --
  under the stake labelling every distinct pair apart, from a well-formed
  regime carrying no demand, one growth step generates at most one demand
  -- does NOT survive that extension.  Rung four will exhibit a
  well-formed regime carrying no demand under that stake, and a removal
  step after which the regime still carries no demand, such that one
  growth step on the removed regime generates two or more demands.

  **Why it is not forced.**  The bound proved here rests on two things:
  that the datum admitted by a growth step is derivable exactly in the
  contexts whose form carries a uniform rule, and that the base regime
  carries no demand.  A removal changes neither by construction: it
  withdraws a datum, which shifts the indices the stake reads, drops every
  admitted instance naming the withdrawn datum, and so rewrites the
  profiles of the survivors.  Whether demand-freeness and the
  one-empty-profile property are inherited by the removed regime is not
  settled by anything proved here, and the extension could preserve the
  bound just as easily as break it.  This rung's theorems do not entail
  the statement in either direction, which is why it is an extrapolation
  and not a corollary.

  **Scoring rule.**  Scored by the operator packet's rung four, the
  removal grammar, and by no earlier rung.  HIT if that rung exhibits the
  regime and the removal step described.  MISSED if that rung proves that
  under its declared removal grammar every well-formed demand-free regime
  still generates at most one demand per growth step.  VACUOUS if that
  rung's declared removal grammar admits no removal from a demand-free
  regime, or if rung four is never run.  The statement is never rescored
  by this rung and is never edited.

## What this rung does not predict

Nothing about the count of declared inputs, in either direction: that is
the parallel track's question.  Nothing about rung one's pending
extrapolation on the four-item bound, which belongs to neither track and
is not computed here.
