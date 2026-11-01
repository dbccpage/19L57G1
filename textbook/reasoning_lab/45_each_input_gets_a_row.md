# 45. Each input gets a row

Keep a box that accepts either 0 or 1. Its supplied rule usually copies
the input, with a one-quarter chance of flipping it.

| Input given to the box | Chance of output 0 | Chance of output 1 |
|---|---|---|
| 0 | 3/4 | 1/4 |
| 1 | 1/4 | 3/4 |

Read each row separately: **if the input is 0**, the output chances are
3/4 and 1/4. Each row sums to one. Adding the whole table gives two,
because its rows answer two different conditional questions.

## A second table answers another question

Suppose the preparation supplies input 0 with chance 3/4 and input 1
with chance 1/4. These preparation chances sum to one across inputs.
The first table supplies chances across outputs for each fixed input.

<details><summary>Predict: what is the output chance of 0?</summary>

There are two ways to obtain 0. Input 0 contributes (3/4) × (3/4) = 9/16.
Input 1 contributes (1/4) × (1/4) = 1/16. Add them: 10/16 = 5/8.
The remaining output chance is 3/8.

</details>

A **channel** here is the whole table of conditional output chances,
with named inputs and outputs. It describes a supplied process. A
preparation chooses the input chances; it is separate from the channel.
For a deterministic channel, each row puts chance one on one output.

Change the preparation to chance one on input 1. Explain why the output
chance of 0 is now 1/4. The process table has stayed fixed.

Use [Number 09–12](../number_lab/09_equal_pieces.md) for the fraction
operations. Continue to [46. Follow the middle value](46_follow_the_middle_value.md).

AuthorityEffect: None. Supplied X300 model and exact book calculations; no measured frequencies.
