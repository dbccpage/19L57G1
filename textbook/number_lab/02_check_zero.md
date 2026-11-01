# 02. Check the zero case

Compare `(2, 3)` with `(0, 0)` using the cross check. The totals are
5 and 0. At the left position, 2 × 0 = 0 × 5 = 0. At the right,
3 × 0 = 0 × 5 = 0. Both checks pass.

Does the empty table therefore have the same fractional shares?
No fractional shares have been defined for a zero total. There are
no parts of a positive whole to compare; we do not assign a value to 0/0.

The raw cross-multiplied relation is still defined. Every product
vanishes against the all-zero table, so that table passes against
**every** count table on these positions.

Try a three-table chain:

| First | Middle | Last |
|---|---|---|
| `(2, 3)` | `(0, 0)` | `(3, 2)` |

First passes against middle. Middle passes against last. But first
does not pass against last: at the left position 2 × 5 differs from
3 × 5. Passing along this chain does not justify skipping the middle.

This is why the source's transitivity theorem requires the **middle
total to be positive**. Transitivity means that two successive matches
justify the first-to-last match. On the domain where every total is
positive, the proportion comparison has this property.

Change the middle table to `(4, 6)`. The first comparison passes, but
the second already fails. The zero-total exception had hidden that
difference. A hypothesis can be the part that makes an inference work.

For fraction arithmetic, continue to [09. Equal pieces](09_equal_pieces.md).
For the separate signed-step branch, use [03. Signed steps](03_signed_steps.md).
The [reading path](../learning_path.md) explains when each is useful.
