# 64. Choose without claiming truth

[Previous](63_withdraw_a_support.md) · [Reasoning lab](README.md)

Return to just the original conflict a/b, without c. Two one-hypothesis
withdrawals work. How should a program choose?

## Predict first

Give both hypotheses withdrawal cost 1. Does the conflict establish that
withdrawing a is better supported by observations than withdrawing b?

<details><summary>Check your prediction</summary>

No. Both choices break this recorded conflict at the same stated cost.
No observation has ranked their truth. The source returns both tied
candidates before a default selector chooses the first by name order.

</details>

## Name the order before using “minimum”

The supplied Python rule compares withdrawals in this order:

1. Withdraw the fewest hypothesis names.
2. Among those choices, add their assigned costs and use the smallest total.
3. Keep every remaining tie. Sort by hypothesis names; the default
   revision chooses the first candidate in that order.

Costs are positive whole numbers supplied to the model. They are neither
probabilities of error nor measured confidence. With costs a=5 and b=1,
the original example selects b. At equal costs, both candidates remain
available and the default selects a because its name comes first.

The first comparison has priority. For conflicts a/b and a/c, withdrawing
a alone wins over withdrawing b and c together, even if a costs 9 and
the other two cost 1 each. It removes one hypothesis instead of two.
“Minimum” is meaningful only with this declared order.

## What a surviving claim establishes

After withdrawal, the engine retains records whose support avoids the
withdrawn names. It checks the recorded conflicts using its defined
syntax. That is a statement about the notebook.

For a deliberately simple counterexample, keep just the hypothesis
“the tag is blue” while the supplied real-world comparison says the tag
is amber. There is no opposite claim in the notebook to trigger a conflict.
The notebook can pass its conflict check and still misdescribe the parcel.
This comparison is a fictional teaching case, not a performed experiment.

For an actual parcel, identify the object, time, inspection procedure,
raw reading and interpretation. Seek observations that could distinguish
the remaining explanations. A cost preference or a checksum on a revision
receipt supplies none of those observations.

Try the [changed practice](REVISION_PRACTICE.md) before the
[separate answers](REVISION_ANSWERS.md). Optional
[source details](REVISION_SOURCES.md) state the Python and Lean boundaries.
Then return to the [reading path](../learning_path.md).

AuthorityEffect: None. The supplied decision rule does not establish truth.
