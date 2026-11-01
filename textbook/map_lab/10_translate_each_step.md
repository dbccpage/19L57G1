# 10. Translate each step

We want a second machine to keep an encoding of the switch's current
state. A correct initial code is only the beginning: it must remain
correct after the source changes.

## Two routes to the same target state

An **encoding** assigns a target state to each source state. Our example
uses the passage machine from the Change lab. Encode source 0 as its
empty initial state with budget 0, and source 1 as that state with budget
1. Every other field stays at its initial value.

Here budget is a register in a mathematical state. A write to it does
not claim a physical payment or measurement.

**Predict:** source 0 receives flip. Which target event would make the
target end at the encoding of source 1?

<details><summary>Compare the routes</summary>

| Route | First action | Second action | End |
|---|---|---|---|
| Source first | flip: 0 → 1 | encode 1 | target budget 1 |
| Target first | encode 0 | write budget 1 | target budget 1 |

The two routes agree on the entire target state. This is the **step
square**: a diagram with two routes whose ends agree. The technical word
for that agreement is “commuting.”

</details>

The translation supplies a list of target events for each source
state/event pair. In this example every list has one budget write. The
general definition also permits empty lists and longer lists.

## Keep the current source state

For “flip, flip” from 0, write budget 1, then budget 0. The second write
is calculated from the updated source state 1. Reusing the first write
would leave budget 1 and break agreement.

**Try a change:** use hold as the second event. The correct second write
is now budget 1. A translation must follow the source's actual history.

The research proves that agreement at every source step gives agreement
after every finite history. Our desk separately computes all histories
of at most five events for the supplied two-state example. A finite
display and the general theorem have different scopes.

Continue with [11. Distinct codes can hide a distinction](11_distinct_codes_and_answers.md).

AuthorityEffect: None. NB-7 supplies the history theorem; NB-9 supplies
the budget encoding. The target-event recipe is supplied data. Selecting
a recipe without supplying one remains NB-15 OPEN.
