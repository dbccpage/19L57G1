# Predictions, frozen before the race ran

A missed prediction is recorded next to its value in `STATUS.md` and never
edited here. `AuthorityEffect: None.`

## Chronology, stated exactly

The **Lean half was written and built before this file existed**, so its
results are recorded below as *already obtained* and are not predictions.
The **Python race had not been run** when this file was hashed: `standing.py`
existed, `run_standing.py` did not, and no value in section 3 had been
computed. Section 3 is prospective without exception.

## 1. Already obtained (Lean; values, not predictions)

Fourteen theorems, all reports within `{propext, Quot.sound}`:
`demands_grow` (a growth step adds exactly the new datum's pairs, and loses
nothing); `demands_persist_under_growth`; `growth_generates` (a fresh datum
under a commitment that keeps it apart from something already held produces
a demand the old state did not carry); `fixpoint_reopens` (a discharged
state is reopened by one growth step); `demand_count_grows` (under the total
commitment on a viewless state, one growth step adds exactly as many demands
as there were data); `empty_commitment_generates_nothing`; and the decided
accounting instance `3 → 6 → 10`.

## 2. The declared family, frozen

Four commitments — `total` (every distinct pair), `adjacent` (consecutive
labels only), `shared_parity` (distinct pairs agreeing in parity), `empty`
(nothing) — and one growth policy: one datum per round, labels `0, 1, 2, …`.
Discharge is a declared budget of up to `rate` demands per round, spent on
the oldest outstanding demands, and a discharged demand never returns.

## 3. Predicted (not yet run at freeze time)

- **Q1.** Under `total` with 24 rounds, the demands generated total `276`
  (the pair count of 24 labels) and the per-round generation is
  `0, 1, 2, …, 23`.
- **Q2.** Under `adjacent`, each round after the first generates exactly one
  demand, so 24 rounds generate `23`.
- **Q3.** Under `shared_parity`, round `k` generates about `k/2`, and 24
  rounds generate `132` — two independent parity classes of 12 labels each,
  `66` pairs apiece.
- **Q4.** Under `empty`, nothing is generated at any rate, and the backlog
  is `0` at every round.
- **Q5.** **The threshold is where the interest is.** For `adjacent` the
  least clearing budget at 24 rounds is `1`. For `total` no fixed budget
  below the round count clears the run, and the least clearing budget grows
  with the run length; concretely, at 24 rounds the least clearing budget is
  `23`.
- **Q6.** For `shared_parity` at 24 rounds the least clearing budget is
  `11`, roughly half the total commitment's.
- **Q7.** Under `total` with a budget of `1`, the backlog is monotone
  non-decreasing after round `2` and reaches its maximum at the last round.
- **Q8.** Doubling the run length under `total` at a fixed budget more than
  doubles the final backlog; under `adjacent` at budget `1` the final
  backlog is `0` at every run length.
