# 10. Check a commuting square

Another comparison exchanges two events. Begin live at budget 0,
license on. Compare “write budget 1, turn license off” with the reverse
order. The other fields are initial and unchanged.

**Predict:** do both routes reach the same entire state? What are their
two cost totals?

<details><summary>Compare both routes</summary>

| Route | Intermediate state | End state |
|---|---|---|
| budget write, license write | budget 1, license on | budget 1, license off |
| license write, budget write | budget 0, license off | budget 1, license off |

Both end live in the same state. We call this a **commuting square**:
two event orders from a given start, with equal ends. Signed budget cost
is 1 on both routes. State-change count is 2 on both routes.

</details>

For either cost, subtract the reverse route's total from the first
route's total. This **square difference** is 0 in the example.
A cost is called **closed** when that difference is 0 on every commuting
square of the declared machine.

## The premise must be checked

**Try a change:** compare budget writes 1 then 0 with 0 then 1.
From budget 0 their final budgets are 0 and 1. This is not a commuting
square. A nonzero cost difference there does not refute closedness,
because the required equal-end premise failed.

The start matters too. Halt then license-off differs from license-off
then halt when the initial state is live with license on. Halt makes
later register writes inert. If the start is already halted, both
events are inert and the two orders agree. You must check the actual
state reached before exchanging events within a longer history.

Signed budget cost is 0 on both halt/license routes even when their
license values end differently. Equal cost for that one question therefore
does not establish equal end states.

Use the [square desk](results.html#square-panel) to change the start and
both events. Continue with [11. Local agreement and global values](11_local_agreement_and_global_values.md).

AuthorityEffect: None. These comparisons use the actual passage step
and `native_structure`'s `commutes` and `d_square`. “Square” here means
this two-order comparison; it is not an admitted triangular face from
the earlier cell lessons.
