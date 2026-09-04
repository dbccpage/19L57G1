# Predictions, frozen before anything ran

A missed prediction is recorded next to its value in `STATUS.md` and never
edited here. `AuthorityEffect: None.`

## Chronology, stated against myself

`PROMPT.md` existed when this file was hashed. **No module of this tree
existed, no Lean package existed, and nothing had been run.**

One thing weakens these predictions and is recorded rather than left for a
reader to notice: before writing them I **read the sealed implementation** —
`model.step`, `model.replay`, `candidates.delta_events`,
`candidates.apply_delta`. They are pinned read-only inputs and any reader
may read them, but a prediction made after reading the code that decides it
is a weaker instrument than one made blind, and A1, A5 and A6 below are
predictions of that weaker kind. A2, A3, A4 and A7 do not depend on the
implementation.

## Predicted

- **A1.** `SEQUENTIAL_ACTION_HOLDS`, and by an equality stronger than the
  statement needs: `delta_events(base, d ; e)` is **literally the same event
  tuple** as `delta_events(base, d)` followed by
  `delta_events(apply(base, d), e)`, because fresh data are numbered from
  the base's datum count and every other item carries an explicit index. So
  the two sides also agree on ill-formedness — where one raises, the other
  raises at the same item. Composition is a **partial** operation and the
  partiality is shared.

- **A2.** `ADDITIVITY_HOLDS` for **every** difference cost, not only for the
  preceding rung's, wherever both sides are defined, over a signed
  coefficient type. It is a consequence of A1 and one cancellation, with no
  property of the state functional used.

- **A3.** `PATH_INDEPENDENT` for every difference cost: the total along a
  sequence of moves telescopes to the functional's value at the end minus
  its value at the start, so any two sequences with the same endpoints carry
  the same total.

- **A4.** **The sealed item count is additive too** — the length of a
  concatenation is the sum of the lengths — so additivity does **not**
  distinguish the base-relative cost from the base-free one. This
  contradicts the preceding rung's own summary of this open, which said that
  if the cost were additive the estate would have an action along a path.
  Predicted here as false: additivity is necessary and not sufficient, and
  the run should show one cost that is additive and path-dependent at the
  same time. `FW-PRIOR` requires the contradiction to be recorded by name if
  it lands.

- **A5.** `CIRCULATION_WITNESS_FOUND`, so `FW-VACUOUS` does not fire. A
  response that re-admits something already standing returns the same state,
  and that is a closed walk of length one. Predicted exactly: an instance
  item, a rule item, a datum item and a requirement item can each self-loop,
  because each absorbs a repeat; **a form item never can**, because form
  admission appends unconditionally and two forms of equal arity are two
  forms. Predicted as a count over the pinned rectangle: at least one
  self-loop exists at every base carrying at least one standing instance.

- **A6.** `COUNT_IS_NOT_A_DIFFERENCE_COST`. On the self-loop of A5 the item
  count totals at least one while every difference cost totals zero, so no
  state functional has the item count as its difference. This is a
  refutation, not a failure to find.

- **A7.** The headline, predicted rather than discovered, and to be recorded
  as missed with its value if it fails: **a difference cost has zero
  circulation on every closed walk, so it cannot carry an obstruction.**
  Obstruction is exactly the part of a cost that is not a difference of a
  state functional; a difference cost has no such part by construction.
  Predicted consequence, stated so it can be held against this tree: an
  optimizer minimizing the preceding rung's cost is descending a functional
  and can never see a nonzero circulation, however the moves are chosen.

- **A8.** Recorded, not predicted as a theorem: over the pinned rectangle
  the difference cost of total profile size is non-negative on every valid
  move, so the signed and unsigned forms agree there. If a negative value
  appears it is a finding and the unsigned form is the one that breaks.
