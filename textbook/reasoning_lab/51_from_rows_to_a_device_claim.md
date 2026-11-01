# 51. From rows to a device claim

A conditional row must have nonnegative chances summing to one.
The row [1/4, 1/4] sums to 1/2 and is refused by this model.

<details><summary>Predict: can we quietly replace it by [1/2, 1/2]?</summary>

No. That supplies a different row. If the original entries were counts
or unnormalized weights, say so and describe a separate normalization
procedure. Do not present its result as the unchanged input.

</details>

Name the input and output sets too. A zero-chance entry is different
from permission to omit a required process row. Every middle value
reachable under the first process needs a row in the next process.

## An optional physical worksheet

Before trials, specify the preparation procedure, what the labels 0 and
1 mean, how each output is read, the number of trials and the handling
of unclear readings. State whether earlier trials, hidden settings or
shared choices can affect the next box.

| Given input | Agreed output 0 count | Agreed output 1 count | Unclear count | Procedure/settings |
|---|---|---|---|---|
| 0 |  |  |  |  |
| 1 |  |  |  |  |

Leave the worksheet blank unless you perform the activity. Counted
fractions describe the performed trials under the stated procedure;
they do not certify an exact future probability. Retain disagreements
and unclear readings rather than silently redistributing them.

To apply the sequence calculation, justify the conditional rows and
the premise that the second process uses only its current input in
the stated way. Shared dependence can require a larger state model.

Change a setting between the two sets of trials. Explain why pooling
their counts without recording the change can hide a process difference.

Try the seven [changed questions](CHANNELS_PRACTICE.md) before the
[separate answers](CHANNELS_ANSWERS.md). The optional
[source guide](CHANNELS_SOURCES.md) records implementation boundaries.

AuthorityEffect: None. Proposed observation procedure; no physical activity or learner result recorded.
