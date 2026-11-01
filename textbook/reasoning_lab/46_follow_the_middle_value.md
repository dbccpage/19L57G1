# 46. Follow the middle value

Put two copies of Lesson 45's box in sequence. The first output becomes
the second input. We supply this premise: the second box uses its stated
row for that current input, without consulting the earlier history or a
shared hidden choice. A device with such extra dependencies needs a
different model.

## Start with input 0

To finish at 0, the middle value can be either 0 or 1.

| Route | Chance of reaching the middle value | Next chance of 0 | Contribution |
|---|---|---|---|
| 0 → 0 → 0 | 3/4 | 3/4 | 9/16 |
| 0 → 1 → 0 | 1/4 | 1/4 | 1/16 |

Add the contributions: 5/8. Starting at 1 instead gives
(1/4) × (3/4) + (3/4) × (1/4) = 3/8.

| Original input | Final chance of 0 | Final chance of 1 |
|---|---|---|
| 0 | 5/8 | 3/8 |
| 1 | 3/8 | 5/8 |

This is **composition**: construct the whole sequence's conditional
table by multiplying along each route and adding over possible middle
values. Only after that, if desired, apply a preparation's input chances.

<details><summary>Predict: what if the second box always outputs 0?</summary>

For input 0, the contributions are (3/4) × 1 + (1/4) × 1 = 1.
For input 1 they are (1/4) × 1 + (3/4) × 1 = 1.
Both rows become [1, 0]. This conclusion follows from the supplied reset rule.

</details>

Change the second box to an exact flip. The first row becomes [1/4, 3/4].
Explain which middle value can then lead to final 0.

Try the [process desk](channels.html). Continue to
[47. Brackets and order](47_brackets_and_order.md).

AuthorityEffect: None. Supplied conditional-process premise; exact finite calculations.
