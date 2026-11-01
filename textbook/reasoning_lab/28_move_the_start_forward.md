# 28. Move the start forward

Suppose a stated model gives equal readouts from two states after
**every** number of updates. The source theorem says the states after
one update also have that property.

**Predict:** which old indices become the first three indices when
we move both starting states forward by one update?

<details><summary>Check your prediction</summary>

| New index | Old index |
|---|---|
| 0 | 1 |
| 1 | 2 |
| 2 | 3 |

Every new index k corresponds to old index k+1.

</details>

If agreement holds for every old index, it holds for all of those
shifted indices too. This is **step congruence** of the all-future
relation: applying the same update to both equivalent states preserves
that relation. It is not a claim that every finite matching record
can be extended for another comparison.

### Keep track of a finite allowance

If the only evidence supplied is agreement at old indices 0,1,2,3,
then after shifting the start you retain agreement at new indices
0,1,2. Nothing in that finite premise tested new index 3, which would
be old index 4. In general, H+1 compared samples supply H shifted
comparisons. A book theorem states this bounded implication separately.

The countdown example with initial counters 1 and 2 makes the limit
visible. Its one compared sample is (0,0). After one update the
lamps are (1,0), so repeating a one-sample comparison now fails.
No all-future premise was present to begin with.

For the particular P202 Lean register model, Lesson 26 supplies an
additional theorem: equal current readouts already determine the full
readout future. That stronger model-specific fact may justify more
than the finite record alone. Name it instead of silently extending
the evidence or pretending it holds for the countdown.

**Change one thing:** only old indices 0 and 1 were compared. Which
new index is covered after moving the start forward once?

<details><summary>Check the changed example</summary>

New index 0, which is old index 1. The new next sample was not in
that two-sample allowance. Further knowledge would need another
comparison or a justified property of the particular model.

</details>

Next: [from model ticks to a clock claim](29_from_ticks_to_a_clock_claim.md).

AuthorityEffect: None. Explicit bounded and all-future premises.
