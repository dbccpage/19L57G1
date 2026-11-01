# 52. Start, then one more

Read [Number 00](../number_lab/00_count_and_multiply.md) for counting,
addition and multiplication, and Reasoning 02 and 06 for if-then claims
and their conditions. No later probability or instrument lesson is needed.

Start with an empty tray. Each update adds one packet containing two
counters. This is a supplied rule for a mathematical model.

| Updates performed | Packets added | Counters in the tray |
|---|---|---|
| 0 | None | 0 |
| 1 | One | 2 |
| 2 | Two | 4 |
| 3 | Three | 6 |

<details><summary>Predict: do these four rows prove the total after every possible number of updates?</summary>

The rows check only counts 0 through 3. A proof for every count needs
an argument that also covers the next step from an arbitrary count.

</details>

## Two jobs make the proof

**Start case.** After zero updates there are zero counters: zero copies
of the packet give zero. This checks the claim at the start.

**Step case.** Suppose that after some whole-number count of updates,
the tray contains that many two-counter packets. One more update adds
one more such packet. The claim therefore holds for the following count.
This argument uses an arbitrary count, not only the count 3.

The natural-number **induction principle** lets us combine those two jobs:
the claim holds at every nonnegative whole-number count. Starting from
zero, each such count is reached by repeatedly taking one more step.
This principle belongs to our admitted mathematical tools; the opaque
starting mark did not supply natural numbers or induction.

Write **n** for an arbitrary update count. Then **2 × n** is the total.
The step case says that 2 × n + 2 is 2 × (n + 1). The letter names a
count; it does not require knowing a particular value before arguing.

Change the start to four counters and the packet size to three. Explain
why the total after n updates is 4 + 3 × n. Next, check
[which conditions the proof needs](53_keep_both_proof_jobs.md).

AuthorityEffect: None. Supplied arithmetic model and induction explanation;
no device observation or learning outcome is recorded.
