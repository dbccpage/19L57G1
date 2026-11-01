# 07. Two different cost questions

Begin after the [Number lab's signed steps](../number_lab/03_signed_steps.md).
The [Map-lab continuation](../map_lab/08_states_and_events.md) explains
states and event histories. The definitions needed here are repeated below.

The earlier Path lessons used a graph of points and admitted faces.
We now supply a different setting: the passage machine from the Change
lab. Its states and events are not inferred from that graph.

## Start with one register

Keep every field of the passage state initial except its budget. Start
live, with budget 0 and license on. An event “write budget 1” sets that
register to 1. A second event “write budget 0” sets it back to 0.
Here a register is simply a stored value. These are model rules, not
measurements or payments.

| Before | Event | After |
|---|---|---|
| budget 0 | write budget 1 | budget 1 |
| budget 1 | write budget 0 | budget 0 |

A **step cost** assigns a number to a current state and an event. We will
compare two supplied rules:

- **Signed budget change:** after-budget minus before-budget.
- **State-change count:** 1 if the entire state changes, otherwise 0.

**Predict:** what total does each rule give for the two rows above?

<details><summary>Add the two kinds of cost</summary>

Signed changes are +1 and −1, giving 0. Both steps change the state, so
the change counts are 1 and 1, giving 2. Neither answer contradicts the
other: the questions counted different things.

</details>

**Try a change:** write budget 1 twice from budget 0. The second event
changes nothing. Signed change totals 1; state-change count totals 1.
The number of attempted events is 2, a third question. The count is per
changing step, not per field or instruction written down.

Continue with [08. Give states a potential](08_give_states_a_potential.md).
The [cost desk](results.html#cost-panel) lets you select both questions.

AuthorityEffect: None. The actual passage step and `native_structure`'s
`budget_delta`, `writes` and `path_cost` compute these examples.
