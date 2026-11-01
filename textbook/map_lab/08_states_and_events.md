# 08. A map that must keep up with changes

The earlier lessons asked which answers survive storing a card's group
label. Now let the source change, and ask whether its encoding keeps up.
Begin after [functions](../reasoning_lab/01_one_answer_per_input.md) and
the [Change lab](../change_lab/README.md). You can also use the definitions
on this page directly.

## One small machine

A **state** is the information the model keeps at a particular step.
Our supplied switch has two states, named 0 and 1. These names are codes;
they are not measurements of an electrical switch.

An **event** is an input to the rule for the next state. We supply two:

| Current state | Event: flip | Event: hold |
|---|---|---|
| 0 | 1 | 0 |
| 1 | 0 | 1 |

A **deterministic step rule** gives exactly one next state for each
allowed current-state/event pair. Read one row and one event column.
It need not change the state: hold is still an event.

**Predict:** start at 1, then flip, hold, flip. Write the state after each
event before opening the explanation.

<details><summary>Follow the rule</summary>

The states are 1 → 0 → 0 → 1. The first and last states agree, but
three events occurred. Returning to the start does not erase those events.

</details>

## A boundary of this definition

“From 0, flip may produce 0 or 1” would supply a different kind of rule:
it allows several outcomes. Our table allows one. The lessons below use
the deterministic table; they do not settle questions about other rules.

**Try a change:** replace hold by “set to 0.” Starting from 1, hold would
then change the state. The event's name did not determine its meaning;
the supplied table did.

Continue with [09. Check the whole history](09_check_the_whole_history.md).
The [step desk](results.html#native-path-panel) includes both events.

AuthorityEffect: None. The switch, names, and event table are supplied
teaching data. The general path definitions come from `native_bridge`;
this table is not derived from the sealed seed.
