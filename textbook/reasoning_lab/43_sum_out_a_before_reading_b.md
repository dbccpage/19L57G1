# 43. Sum out A before reading B

Supply this correlated joint preparation:

| A | B | Joint chance |
|---|---|---|
| 0 | 0 | 1/2 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1/2 |

**Predict:** without keeping a particular A result, what is B's chance
of 0? If we keep only A=0, what is B's chance of 0 in that branch?

<details><summary>Check your prediction</summary>

Without selection, add the two rows with B=0: `1/2 + 0 = 1/2`.
In the A=0 branch, the joint chance of B=0 and that branch is 1/2,
and the branch itself has chance 1/2. The conditional chance is
`(1/2)/(1/2) = 1`.

</details>

B's **marginal state** sums over the A labels, retaining a chance for
each B value. Evaluating the same B effect on this marginal agrees with
the full A-branch sum from Lesson 42. A product outcome space permits
correlated tables like this one. It does not require independent parts.

A **product state** is a further choice: it assigns each pair the product
of its separate A and B chances. Here both marginals are half/half, so
their product state would give 1/4 to all four pairs. That differs from
the supplied correlated table despite having the same marginals.

Conditioning on one A branch changes the comparison group; it is not
the operation of summing over all A branches. A zero-chance branch
supplies no conditional ratio. No physical communication or change
to the joint state is established by these table calculations.

**Change one thing:** put equal chance on 01 and 10 instead. Does B's
marginal change? What happens in the A=0 branch?

<details><summary>Check the changed example</summary>

B's marginal remains half/half. In the A=0 branch, B is now certainly 1.
The marginals alone do not determine the joint correlations.

</details>

Explore the second panel of the [valuation desk](valuations.html).
Next: [connect a chance table to observations](44_from_chances_to_observations.md).

AuthorityEffect: None. Supplied joint chances, explicit retained branches.
