# 08. Give states a potential

Can a whole path's cost be recovered just from its end and start?
A useful way is to assign one number to each state.

A **potential** is that state-to-number function. We call a cost **exact**
when every step's cost equals the potential at its after-state minus
the potential at its before-state. Both “every” and the declared step
rule matter. A plausible table for a few states is not the whole claim.

## Use budget as the assigned number

Take the state's budget itself as its potential. Start at budget 2,
write 0, then write 1. All other fields stay initial.

**Predict:** add the signed changes. Then compare the answer with final
budget minus initial budget.

<details><summary>Watch the middle value cancel</summary>

| Step | Potential after − potential before |
|---|---|
| 2 → 0 | 0 − 2 = −2 |
| 0 → 1 | 1 − 0 = +1 |

Total −2 + 1 = −1. This is also 1 − 2 = −1. In the expanded sum,
the middle 0 appears once with each sign and cancels. Such cancellation
along a path is called **telescoping**. The research proves it for every
finite event history when the step cost has the stated potential form.

</details>

The actual budget-change cost has this form even for events that also
change other fields: its definition reads only the before/after budgets.
This does not make the state-change count the same cost.

## The starting level need not be unique

**Try a change:** assign budget + 7 instead of budget. The two differences
are 7 − 9 = −2 and 8 − 7 = +1. Adding the same constant to every
potential value leaves all step costs unchanged. Recovering differences
does not by itself fix an absolute starting level.

“Height” can help picture a potential, but no physical quantity
has been measured here. The assigned values are integers in the model.

Continue with [09. Test a return loop](09_test_a_return_loop.md).

AuthorityEffect: None. NS-7/8 own `exact_pathCost` and `budgetDelta_exact`.
The book checks invariance under adding a constant for all integer
constants, states and events.
