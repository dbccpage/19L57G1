# 63. Withdraw a support

[Previous](62_keep_the_support.md) · [Reasoning lab](README.md) · [Next](64_choose_without_claiming_truth.md)

Keep the same parcel, time, rules and recorded chain from Lesson 62.
Add hypothesis b: **the route is not left**. The notebook now has a
route-left record supported by a and a not-left record supported by b.

## Predict first

Does this conflict tell us which hypothesis is wrong about a real parcel?

<details><summary>Check your prediction</summary>

No. Under the supplied Rule 1, a and b cannot both be correct for this
parcel at this time. The conflict alone does not identify a false report,
a mistaken rule, or a failed interpretation of “blue” or “left.”

</details>

## Two ways to break this recorded conflict

The conflict's **support set** contains a and b. “Set” means a collection
of names with no repeated member. Here either withdrawal breaks the conflict:

| Withdraw | Records deactivated | Records kept active |
|---|---|---|
| a | Tag blue; its route-left record; its queue-L record | b and both fixed rules |
| b | The not-left record | a, its route-left and queue-L records, and both fixed rules |

To **deactivate** a record is to stop using it as a current premise. The
program keeps the old record for inspection. No parcel is moved, and no
historical report is erased by this notebook operation.

The queue record is deactivated when a is withdrawn even though queue L
does not directly contradict b. Its support was lost farther up the chain.
This downstream effect is called a **cascade**.

## Another route can survive

Add hypothesis c: “route left,” recorded independently of a. We now have
two conflicts, with supports a/b and b/c. Withdrawing a alone leaves
c and b in conflict. Withdrawing b breaks both conflicts.

A withdrawal must remove at least one hypothesis from **every** recorded
conflict support. A collection doing this is called a **hitting set**:
it touches each conflict. Here b alone works; a and c together also work.

## Find out what has actually been checked

The Python engine checks direct opposites and unequal values assigned to
the same variable among active records. It does not automatically apply
all possible inference steps. We explicitly recorded the route-left step
before asking for revision. “No detected conflict” alone does not prove
that all consequences of all premises are mutually compatible.

If a recorded conflict depends only on fixed assumptions, withdrawing
hypotheses cannot repair it. The source reports an error. Investigating
the fixed setup requires a separate decision outside this revision rule.

Try choosing between the two repairs in
[Lesson 64](64_choose_without_claiming_truth.md).

AuthorityEffect: None. Withdrawal changes the declared notebook, not reality.
