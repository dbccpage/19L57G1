# Predictions, frozen before anything ran

A missed prediction is recorded next to its value in `STATUS.md` and never
edited here. `AuthorityEffect: None.`

## Chronology, stated against myself

`PROMPT.md` existed when this file was hashed. **No module of this tree
existed, no Lean package existed, and nothing had been run.** In particular
no move graph had been built and no route pair had been looked for: P3 below
is a genuine prediction about the sealed grammar and not a report.

As in the preceding rung, the sealed implementation had been **read** before
these were written — `model.step`, `model.replay`,
`candidates.delta_events`, `candidates.iter_cost1_items`. P1, P2 and P3 are
weaker for it. P4 through P8 do not depend on the implementation.

## Predicted

- **P1. `SEARCH_SPACE_CHARACTERISED`, and the space is exactly a weighting
  of single-item moves.** Additivity forces the empty response to cost zero
  — apply the law to the empty response twice — and then forces the cost of
  any response to be the sum of its items' costs, each priced at the state
  it is applied to. So an additive cost **is** a function on (state,
  one item) pairs, extended by summation, and the hunt is over that set and
  nothing wider. Predicted as a theorem, not a computation.

- **P2. `DIRECTED_CLOSED_WALKS_ARE_STATIONARY`.** Admission only adds, so
  the reachable states carry an order that a move never decreases. A
  directed walk returning to its start must therefore stand still at every
  step. Predicted as a theorem over an abstract monotone action, with
  antisymmetry doing the work.

  **Consequence, predicted as the structural point of the rung:** in an
  estate where admission only adds, path-dependence cannot come from going
  around a directed cycle, because there are none that move. It can come
  from only two places — a move that changes nothing, and two *different*
  routes that reach the same state. The first is waste. The second is
  order.

- **P3. `TWO_ROUTES_EXIST`, and the smallest one is a form and a datum.**
  Admitting a form and admitting a datum touch different components of the
  record, so they commute: from a base with `n` data and `m` forms, form
  then datum and datum then form land on the same state. Predicted to occur
  in the rectangle at the root itself. Predicted also that this is not the
  only commuting pair, and the count is recorded rather than predicted.

- **P4. `PATH_DEPENDENT_COST_EXHIBITED`.** Given P1 and P3 a path-dependent
  cost must exist, because the two routes of a commuting square can simply
  be weighted differently and the weighting is a legitimate additive cost by
  P1. So existence is cheap and is **not** the finding. The finding is
  whether a cost with a native reading has the property, and `FW-TUNED`
  binds the run to declare its candidates before pricing them.

- **P5. The two sources are genuinely different, and the item count
  separates them.** The sealed item count is nonzero around a move that
  changes nothing, so it is not a difference of a state functional. But on
  a commuting square both routes use the same number of items, so its
  circulation there is zero. Predicted: **the item count is
  path-dependent only through waste**, which is exactly the degenerate case
  `FW-DEGENERATE` names, and a cost that distinguishes the two routes of a
  square is a strictly stronger object.

- **P6. A cost that charges an item for what is already standing is the
  natural non-degenerate one.** Predicted: pricing a form item by how much
  state it must range over, while pricing a datum item at zero, gives
  nonzero circulation on the square of P3, because the form is cheaper
  before the datum arrives than after. Predicted to be the first candidate
  that is both natively motivated and not exact. Its native reading: a form
  is a standing obligation over everything present and a datum is not an
  obligation at all, so the two are not symmetric and a cost that treats
  them symmetrically is the one making an assumption.

- **P7. Every candidate built as a difference of a count of the state will
  be exact, including the ones that look base-relative.** The number of
  contexts a move opens, the number of pluggings it makes derivable, the
  number of forms, the number of data — each is a state functional's
  difference however it is phrased, and each will show zero circulation on
  every cycle. Predicted as the trap: reading the base is **not** sufficient
  for path-dependence, and several candidates will read the base and still
  telescope.

- **P8. `RANK_COMPUTED`, and the rank is not accounted for by waste alone.**
  Predicted: the cycle rank of the rectangle's move graph exceeds the number
  of moves that change nothing, so commuting squares contribute
  independently. Sizes are recorded, not predicted. If the rank equals the
  self-loop count the prediction is missed and
  `ONLY_DEGENERATE_PATH_DEPENDENCE` fires instead.
