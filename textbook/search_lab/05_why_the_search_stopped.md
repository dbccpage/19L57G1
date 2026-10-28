# 05. Explain why the search stopped

[Previous](04_protect_a_distinction.md) · [Search lab](README.md) · [Next: replay](06_replay_the_result.md)

## Four different reasons

“The program stopped” leaves an important question unanswered: **why?**

| Recorded status | What happened in the lab | What it establishes |
|---|---|---|
| `terminal_all_separated` | Repair the original two-entry demand; disable further supply | Every admitted pair is separated, and the declared policy has no next move |
| `terminal_no_response` | Allow at most one item at the unmet initial demand | No valid response exists inside that declared candidate space |
| `completed` | Set the allowed rounds to zero | The round budget has ended; the initial demand remains unmet |
| `frontier_guard` | Set the pre-expansion node guard to zero | The guard prevents expansion of the initial node |

The labels belong to this implementation. In particular, its word
`completed` reports reaching a depth limit, not completing the mathematical
task or the textbook's teaching goal.

## Supply is a choice

With supply disabled, each of the three initial item-count classes reaches
an all-separated two-entry state. The closed run has four nodes and three
edges: one starting node and its three retained answers.

With supply enabled, the policy can present and admit a fresh entry after
all existing pairs are separated. That creates a different continuation.
The supply policy was explicitly chosen; reaching a closed-state result
did not derive a need for an additional entry.

The later pair-separation policy is supplied too: it issues a demand on
collapsed pairs, choosing representatives by the declared symmetry rule.
An undistinguished pair alone does not create a demand without that policy.

## A guard is not always a hard size cap

The engine checks its node guard **before expanding a node**, and uses
“current count greater than the guard.” One permitted expansion may add
several children. A guard of 40 can therefore leave 41 nodes. Calling it
an exact 40-node cap would misdescribe the actual rule.

## Your turn

A report says “no response” but omits its item and arity bounds. State what
information is missing before you could use that report. Then explain why
reaching a round limit is insufficient evidence that every pair is separated.

AuthorityEffect: None. The lab separately reproduces all four stopping cases.
