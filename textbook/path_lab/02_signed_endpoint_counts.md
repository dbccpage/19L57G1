# 02. Count arrivals and departures

[Previous](01_follow_a_walk.md) · [Path lab](README.md) · [Next](03_closed_and_filled.md)

## Predict first

Follow A → B → C. At B, there is one arrival and one departure.
What remains after we cancel them as a pair?

## Introduce a signed count

Give each arrival the count **+1** and each departure the count **−1**.
The minus sign marks the opposite contribution. One +1 and one −1 cancel
to **0**. Two arrivals give +2; two departures give −2. These whole-number
counts, positive, negative, or zero, are called **integers**.

We add the contributions at each vertex:

| Step | A | B | C |
|---|---:|---:|---:|
| A → B | −1 | +1 | 0 |
| B → C | 0 | −1 | +1 |
| Total | −1 | 0 | +1 |

B disappears from the final tally because its two contributions cancel.
The tally keeps the starting departure and final arrival. It does not
keep every step of the route. This tally is the walk's **endpoint boundary**.

## Zero is a balance, not an empty history

For A → B → A, both A and B have one arrival and one departure.
Every endpoint count is zero, although two steps occurred.

The triangular closed walk A → B → C → A also has all-zero endpoint
counts. Those counts alone cannot distinguish it from going out and back,
or from staying at A for zero steps.

## Your turn

Write the signed endpoint table for A → C → D. Which contributions cancel?
Then reverse the whole walk. What happens to its nonzero endpoint counts?

AuthorityEffect: None. The signed tally is a declared bookkeeping rule.
