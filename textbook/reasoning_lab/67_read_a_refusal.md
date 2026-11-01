# 67. Read a refusal

[Previous](66_project_before_permission.md) · [Reasoning lab](README.md)

## Predict first

Give the notebook budget 3, horizon 2 and a two-mark ceiling. Successfully
mark B, erase A and erase B, charging 1 each time. Now try to mark A.
Does refusing the fourth attempt erase a retained memory record?

<details><summary>Check your prediction</summary>

No. The budget is zero, so the controller refuses. The current notebook
still has no marks; the budget stays zero; memory still contains the last
two successes, “erase A; erase B.” The success count remains three.
The refusal receipt is separate from this memory buffer.

</details>

## Preserve the conditions behind preservation

With the supplied actions, refusal retains the current notebook,
budget, memory and success count. Reasons include an exhausted budget,
an empty candidate pool, a failed envelope check and denied authorization.

This preservation relies on actions that leave their input untouched
while being evaluated. An arbitrary program can change a shared object
before later checks refuse it. Keeping the same object reference then
does not prove its contents are unchanged. The book uses the declared
nonmutating action factories, not arbitrary callbacks.

## A successful step need not change the marks

Start again with only A marked and budget 1. “Mark A” costs 1 but adds
no new mark. It can still be an accepted step: the budget becomes zero
and memory receives a success record. Acceptance does not imply that
the represented marks changed.

The evaluator records a flag called `has_empirical_reference`. In this
Python setting, it compares before/after model digests. The flag is false
for this unchanged notebook, yet the default policy can accept the action.
A true flag would likewise record a model comparison, not a performed trial.

## A budget bounds only what its cost rule bounds

Python permits a zero-cost action. With a positive budget it can succeed
repeatedly without consuming the budget. A finite budget therefore does
not alone bound the number of successes for every allowed action menu.
Once the budget is zero, the controller's initial check refuses even a
zero-cost candidate. The separate formal model instead gives every action
cost 1; its strict decrease result has that scope.

Try the [changed practice](AGENCY_PRACTICE.md) before its
[separate answers](AGENCY_ANSWERS.md). Optional
[source details](AGENCY_SOURCES.md) retain the exact model and key boundaries.
Then return to the [reading path](../learning_path.md).

AuthorityEffect: None. No physical trial or independent learning result is recorded.
