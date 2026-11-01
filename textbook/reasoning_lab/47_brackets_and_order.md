# 47. Brackets and order

An exact flip sends 0 to 1 and 1 to 0. A reset sends either input to 0.

<details><summary>Predict: do flip-then-reset and reset-then-flip agree?</summary>

| Original input | Flip, then reset | Reset, then flip |
|---|---|---|
| 0 | 0 | 1 |
| 1 | 0 | 1 |

The orders disagree on both inputs. Each order defines a deterministic channel.

</details>

## What brackets change

For three processes A, B and C, compare these instructions:

1. Calculate the table for A then B; follow it by C.
2. Calculate the table for B then C; put A before it.

Both execute A, then B, then C. The brackets choose which combined table
we calculate first. For these conditional tables, they give the same
final table. That property is **associativity**.

Swapping A and B changes execution order. Equality after such a swap is
**commutation**, a separate claim that the flip/reset example refutes.

Change the example to two exact flips. Each order returns the original
input. One commuting pair does not make every pair commute.

The [desk](channels.html) compares both conditional rows for all six
named choices. Three displayed preparations illustrate each comparison;
they are not the definition of channel equality. Optional
[source details](CHANNELS_SOURCES.md) separate general deterministic
composition from the book's two-by-two row algebra.

Continue to [48. One output table can hide a difference](48_one_output_table.md).

AuthorityEffect: None. Deterministic theorem, separate binary row theorem and exact examples.
