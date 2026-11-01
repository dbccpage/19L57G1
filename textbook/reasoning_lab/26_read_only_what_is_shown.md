# 26. Read only what is shown

The Lean P202 state stores A, B and two clocks. Its **readout** returns
only A and B. Consider two supplied states:

| State | A | B | Fast | Slow | Readout |
|---|---|---|---|---|---|
| S | 2 | 3 | 0 | 0 | (2,3) |
| T | 2 | 3 | 10 | 7 | (2,3) |

**Predict:** do equal readouts make these complete states equal? Will
their A/B readouts diverge under the stated Lean update?

<details><summary>Check your prediction</summary>

The complete states differ in their clock fields. But A and B each
increase by one independently of the clocks, so their readouts remain
equal: (3,4), then (4,5), and so on.

</details>

In this source, **future-test equivalence** means equal readouts after
every number k of updates, including k=0. It refers to the selected
readout and transition, not every possible observation of the states.

The book proves that in this particular Lean model, future-test
equivalence holds exactly when the current A/B readouts are equal.
Each next readout depends only on that current pair. Repeating the
same deterministic update preserves their equality by induction.

Thus a present readout *can* determine the entire future readout
sequence under suitable model assumptions. That does not establish
such assumptions for every device, nor make invisible clock fields equal.
An observer that also reads the clocks would answer a different question.

**Change one thing:** change T’s A from 2 to 9, retaining its other fields.
Could it still satisfy this all-future equivalence with S?

<details><summary>Check the changed example</summary>

No. They already disagree at k=0: (2,3) versus (9,3). An all-future
claim that includes the present fails at its first test.

</details>

Python’s finite-horizon helper asks another, bounded question. On the
desk’s declared two-register states it likewise reads A/B rather than
clocks, but its different transition remains explicit. The next lesson
separates a finite comparison from the general definition.

Next: [how far the record looks](27_how_far_the_record_looks.md).

AuthorityEffect: None. Selected readout and transition; no physical identity claim.

For the proof method, use the [induction toolkit](52_start_then_one_more.md).
The method still needs this particular update's preservation premise.
