# 66. Project before permission

[Previous](65_memory_has_a_horizon.md) · [Reasoning lab](README.md) · [Next](67_read_a_refusal.md)

Keep the two-item notebook. Initially only A is marked. An action is a
declared rule for computing a possible next notebook. In this example
it makes a new notebook without altering its input; repeating the same
calculation gives the same result.

## Predict first

Supply one candidate: “mark B,” with cost 1. Give the controller a work
budget of 3. Set a ceiling of one marked item. Can the proposed step
pass just because its cost fits the budget?

<details><summary>Check your prediction</summary>

No. Its proposed notebook has both A and B marked. That exceeds the
one-mark ceiling. An affordable change can still violate another condition.

</details>

## Keep three questions separate

A **projection** is a computed possible next state. Computing this
projection does not select it as the current state. A **viability envelope**
is the supplied collection of limits that an accepted state must satisfy.
Our envelope retains the two items and their mark form, with a mark ceiling.
“Viable” means passing these declared checks, not biological survival.

| Question | Check in this example |
|---|---|
| Can we afford it? | Cost 1 fits the remaining budget 3 |
| Does the projection fit the envelope? | Two marked items exceed a ceiling of one |
| Has it been authorized? | Apply the declared authorization policy only after evaluation |

Raise the mark ceiling to two. The projection now passes that limit.
The default authorizer allows a viable evaluation in this example,
without a panel. This is a supplied policy, not an independent person's
approval. A different supplied policy may refuse the same viable proposal.

## A license names what it allows

The Python license lists permitted structural keys. A **key** here is a
computed description used to compare represented notebook structures.
For our supplied action, the driver recomputes the projection and checks
its key against that list. An empty list refuses the application. A list
containing the proposed two-mark structure's key permits it.

Here the program computes the key from the proposed notebook. A structural
key does not certify every interpretation attached to a notebook; the
[optional source details](AGENCY_SOURCES.md) explain which fields it compares.

On success, the controller adopts the resulting notebook, subtracts
the declared cost and appends a memory record. A projection, a license
and that committed step are distinct stages. None grants permission
to operate on a real person's objects.

Continue to [reading a refusal](67_read_a_refusal.md).

AuthorityEffect: None. The budget, envelope and permission policy are supplied.
