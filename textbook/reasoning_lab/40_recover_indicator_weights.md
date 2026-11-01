# 40. Recover the indicator weights

An **indicator state** puts chance one on one outcome and zero on every
other outcome. For outcomes red/blue/green, supply these three states:

| Recipe | Red | Blue | Green |
|---|---|---|---|
| R | 1 | 0 | 0 |
| B | 0 | 1 | 0 |
| G | 0 | 0 | 1 |

**Predict:** which mixture weights produce the table `(1/2,1/3,1/6)`?

<details><summary>Check your prediction</summary>

Use weights 1/2,1/3,1/6 on R,B,G respectively. Only R contributes to
red, so its weight must be 1/2. The other two coordinates similarly
determine their recipe weights.

</details>

With exactly these distinct indicator states and fixed outcome labels,
the weights are unique. The allowed set of all normalized probability
tables is called a **classical simplex**. Its indicator states are its
extreme states: an indicator cannot be made by a nontrivial mixture of
the other indicators. Their contributions to its outcome would all be zero.

Uniqueness is relative to the specified candidates. It does not recover
the actual historical preparation procedure. Renaming a recipe or splitting
its use into repeated identical recipes can change the recorded procedure
without changing the aggregated table.

**Change one thing:** allow two separately named copies of R. Can the
red weight 1/2 be divided between them in more than one way?

<details><summary>Check the changed example</summary>

Yes: 1/2 and 0, or 1/4 and 1/4, for example. Their aggregate R weight
is still 1/2. This changes the candidate list by adding a duplicate;
it does not refute uniqueness over the three distinct indicator states.

</details>

Next: [restrict the allowed preparation family](41_two_recipes_one_table.md).

AuthorityEffect: None. Specified indicator candidates, not recovered physical history.
