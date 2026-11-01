# 62. Keep the support with the claim

[Reasoning lab](README.md) · [Next](63_withdraw_a_support.md)

Use Reasoning 00–07 first. The other applications are optional. This
three-lesson continuation supplies a new notebook, selected from X302
research outside the sealed derivation. It requires no new notation.

## Predict first

Imagine one parcel at one stated time. Supply these notebook entries:

| Entry | What it says | Status in this run |
|---|---|---|
| Rule 1 | If the tag is blue, the route is left | Fixed assumption |
| Rule 2 | If the route is left, the queue is L | Fixed assumption |
| a | The tag is blue | Withdrawable hypothesis |

Apply Rule 1 to a, then Rule 2 to the result. Does the queue claim
still rely on a, although Rule 2 does not mention the tag?

<details><summary>Check your prediction</summary>

Yes. The recorded chain is: a → route left → queue L. Both conclusions
rely on a. If we stop using a, this chain no longer supplies either claim.

</details>

## Write down what each step used

A **hypothesis** is an assumption this run allows us to withdraw.
The **support** of a recorded claim lists the hypotheses used along its
recorded derivation: the steps that led to that particular record.

| Record | Immediate inputs | Hypothesis support |
|---|---|---|
| Rule 1 | Supplied fixed assumption | None |
| Rule 2 | Supplied fixed assumption | None |
| Tag blue | Hypothesis a | a |
| Route left | Rule 1 and tag blue | a |
| Queue L | Rule 2 and route left | a |

When a step uses two inputs, collect the hypothesis names from both.
Count a repeated name once. Fixed assumptions contribute no withdrawable
names; they remain premises of the argument. Empty hypothesis support
does not mean that a claim has no assumptions or has been observed.

The source calls a fixed assumption an **axiom**. Here that word describes
its role in this run. It does not certify the rule as a law of real parcels.

## Keep the record separate from the sentence

Another hypothesis could directly say “route left.” That would give a
second record of the same sentence, with different support. Withdrawing
a could disable the first record while leaving the second active.

Support tracks the chosen derivation. It is not necessarily the smallest
set of assumptions from which the sentence could ever be established.

## Your turn

Suppose a step uses one record supported by a and another supported by
b and a. Which names belong to the new record's support?

Continue to [withdrawing a support](63_withdraw_a_support.md).

AuthorityEffect: None. The parcel and rules are supplied fiction.
