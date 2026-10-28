# 03. Budget and permission

[Previous](02_inspect_the_repairs.md) · [Change lab](README.md) · [Next: proposals](04_proposal_and_execution.md)

## Possible is a different question from executable now

A **budget** is a number stored in this machine. An accepted column
refinement or append needs a positive budget and subtracts one unit when
it executes. The unit is part of the model. An application must supply
and check any interpretation as a measured resource.

A **permission switch**, called `licensed` in the source, controls creation
of new columns. It is a supplied program setting, not a proof of authority
in a real organization.

## The two operations have different gates

| Proposed operation | Structural condition | Budget needed? | Permission switch needed? |
|---|---|---|---|
| Change an existing column | It resolves an active pair and preserves protected separations | Yes | No |
| Append a new column | It separates an active protected pair and satisfies the column guard | Yes | Yes |

Both also require an unhalted machine. Their guard functions can describe
a structural possibility even when the event cannot execute right now.

## Predict two cases

With only A/B and B/C protected, changing `[A]` to `[A,C]` is a structural
repair. With budget one and permission off, **it still executes**. The
permission gate does not apply to this operation.

Appending `[B]` with the same budget and permission off changes nothing.
Turn permission on, keep the budget positive, and that event can execute.

With budget zero, neither observation change executes. A proposal may
still be listed. Raising the budget changes the resource setting; it
does not add the proposed column by itself.

## Your turn

Protect all three pairs. Set budget one and permission off. Explain why
changing the old column to `[A,C]` fails for a structural reason, while
appending `[B]` fails at the permission gate. Turning permission on fixes
only the latter failure.

AuthorityEffect: None. These are the actual passage event guards.
