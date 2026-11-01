# 27. How far the record looks

Python’s `future_trajectory` with horizon H records H readouts at
indices 0,1,...,H−1. Index 0 is the starting readout. With H=3,
the records are at 0,1,2. The state after the third update is not an
additional recorded sample. Count updates and recorded samples separately.

Now change to a **separate supplied countdown model**. It is not either
P202 clock rule. Each hidden counter drops by one per update, stopping
at zero. A lamp reads 1 when its counter is zero and 0 otherwise.
Counter A starts at 3; B at 4.

| Compared index | Lamp A | Lamp B |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 2 | 0 | 0 |

**Predict:** do these three matching samples force the lamps to match
at index 3 too?

<details><summary>Check your prediction</summary>

No. At index 3, A’s counter is zero and its lamp reads 1. B’s counter
is still one and its lamp reads 0. The finite agreement is genuine,
but extending it to the next reading would be false.

</details>

For any chosen H, counters starting at H and H+1 agree on the first
H lamp readings and differ at index H. The book proves that statement
for all natural-number H in this countdown model. Longer finite
records therefore do not give an unrestricted all-future guarantee
over this unbounded family of possible starting counters.

This does not contradict Lesson 26. The update and readout have changed.
In Lean’s P202 model the visible registers determine their next values;
here the lamp hides how far its counter remains from zero.

### An empty comparison

H=0 compares no readouts. The universal condition “every selected
sample matches” is then true without testing a single reading. It
does not establish even current agreement. The native Python helper
also returns an empty trajectory for a negative horizon; the teaching
desk rejects that input instead of treating it as a meaningful duration.

**Change one thing:** use H=1. Write the current and next lamp pairs.

<details><summary>Check the changed example</summary>

Starting counters 1 and 2 give current lamps (0,0). One update gives
counters 0 and 1, so the next lamps are (1,0).

</details>

Try the countdown section of the [clock desk](clocks.html).
Next: [move the start forward](28_move_the_start_forward.md).

AuthorityEffect: None. A supplied countermodel, not a native P202 trajectory.
