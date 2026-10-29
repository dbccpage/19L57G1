# Answers: new counts and new directions

1. The total is 4; the shares are 3/4 and 1/4. For `(6, 2)`, whose
   total is 8, the cross checks are 3 × 8 = 6 × 4 = 24 and
   1 × 8 = 2 × 4 = 8. For `(3, 2)`, total 5, the first check already
   fails: 3 × 5 = 15 differs from 3 × 4 = 12.
2. The first-to-middle and middle-to-last cross checks both pass,
   because multiplication by zero makes each side zero. First-to-last
   fails: 3 × 4 = 12 differs from 1 × 4 = 4. Transitivity requires
   the middle total to be positive. All-positive totals give the intended
   proportion-comparison domain; no value for a zero-total share is added.
3. Both separate square rows are `(9, 4)`. Add-then-square gives
   (3 + 2)² = 25 and (3 − 2)² = 1. The sum of the separate squares
   is 13 in both cases, so it is a different operation.
4. Both separate weight rows are `(4, 4)`. The sums are `(2, 2)` and
   `(2, −2)`; each has weight 4 + 4 = 8. Distinct preparations can
   have equal readings. A readout may preserve some distinctions
   and forget others.
5. Every separate weight row is `(4, 4)`. The combined sums are
   `(4, 0)`, `(2, 2)`, and `(0, 0)`, with readings 16, 8, and 0.
   Doubling both input coordinates multiplies these weights and
   readings by four; it does not double them.
6. The weights cannot determine the readout on all three rows:
   the same input `(4, 4)` would have to return both 16 and 8, for
   example. On a singleton carrier containing only the first row,
   the constant answer 16 works. The domain changed.
7. The groups are `{0}`, `{1,5}`, `{2,4}`, `{3}`. At most four readings
   are allowed. Assign each position the smaller of its number j and
   `6 − j`: the readings are `[0,1,2,3,2,1]`. This supplied group-label
   reading is reversal-preserving and attains four distinct values.
   It is not a claim about the coordinate formula at every loop size.
8. A justified connection is needed from actual preparations, the
   combination protocol, and calibrated measurement outputs to the
   model's inputs, operation, and readout. A program can implement
   a chosen model correctly while that model misdescribes an apparatus.

The checker recomputes all arithmetic examples, domain restrictions,
and finite reversal groups. No empirical result is inferred from them.
