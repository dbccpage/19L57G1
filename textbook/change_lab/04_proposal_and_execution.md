# 04. A proposal is not an execution

[Previous](03_budget_and_permission.md) · [Change lab](README.md) · [Next: refusal and halt](05_refusal_and_halt.md)

## Keep all three pairs protected

The current column `[A]` leaves B/C active and its existing repair menu
is exhausted. The passage's **extension proposal family** considers new
columns containing exactly one admitted position.

`[B]` and `[C]` both separate B/C and qualify. `[A]` does not. The family
retains both qualifying singleton proposals; it does not select one for us.

## State which family was enumerated

If instead we inspect every membership pattern on three positions, there
are eight sorted, duplicate-free column patterns. Four qualify here:
`[B]`, `[C]`, `[A,B]`, and `[A,C]`.

The last two are valid columns, but they are not singletons. They do not
belong to the narrower proposal family. Thus “both singleton proposals
were retained” does not mean “every possible column list was enumerated.”

The packet shows all eight canonical membership patterns. It does not
enumerate every literal list with reordered or repeated members.

## A proposed event block still has guards

For each singleton extension, the next-event function lists a block:

1. Set the budget to one.
2. Attempt to add that column.

The funding event is explicit. The block does not turn permission on.
Starting with budget zero and permission off, executing the block changes
the budget to one but leaves the column absent and B/C active.

The state changed, yet the proposed repair did not happen. A generated
block is not a promise that every event in it will execute successfully.
The step function still checks its actual guards.

## Your turn

Give the two separate facts needed to establish that a column was added:
what proposal or event was supplied, and what happened when the event was
replayed under the current guards. Explain why a changed budget alone is
insufficient evidence of a resolved distinction.

AuthorityEffect: None. Proposal membership and execution are separately checked.
