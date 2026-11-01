# 37. Chances and responses answer different questions

Supply two possible outcomes, 0 and 1. A preparation assigns them chances
3/4 and 1/4. If fractions are unfamiliar, begin with the
[fraction toolkit, Number 09–12](../number_lab/09_equal_pieces.md).

Now supply a Yes response rule: if outcome 0 occurs, its Yes chance is
1/2; if outcome 1 occurs, its Yes chance is 1.

**Predict:** which pair must sum to one: the preparation chances,
the two response chances, or both?

<details><summary>Check your prediction</summary>

The preparation chances must sum to one: one of the two listed outcomes
occurs in this model. The response chances answer two different “if”
questions. They need not sum to one across different outcomes.

</details>

A **state** in this P204 Python model is a normalized table of preparation
chances. Each is between zero and one; together they sum to one.
An **effect** is a table of Yes response chances, one for each outcome.
Each is between zero and one, with no cross-outcome sum condition.

“Always yes” has response weights 1,1. It is called the **unit effect**.
“Always no” has weights 0,0. For any effect, its **complement** replaces
each weight w by 1−w, giving the corresponding No response.

These tables are supplied model data. Writing a chance of 3/4 does not
record three successes from four actual trials, or guarantee that pattern
on the next four trials.

**Change one thing:** give the preparation chances 3/4 and 3/4.
Is that a valid state on this two-outcome space?

<details><summary>Check the changed example</summary>

No. They total 3/2, not one. The constructor refuses the table rather
than silently rescaling it.

</details>

Next: [multiply before adding](38_multiply_then_add.md).

AuthorityEffect: None. Supplied finite probability model, outside the sealed derivation.
