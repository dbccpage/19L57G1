# 60. Agreement and the guard

Suppose A is absent from the model's blue relation. Three report procedures
each first insert A into their own returned view and then answer “A is blue.”
They all return 1. Evaluating the unchanged starting model returns 0.

<details><summary>Predict: do three matching reports force the starting model's answer to be 1?</summary>

No. All three procedures use the same altered view. Agreement does not
establish agreement with the starting model.

</details>

The source calls these procedures observers. Its Python panel requires
at least three entries. It does not enforce distinct names, independent
information sources, or views that only discard facts. Our example uses
this actual permission to add a fact. Three entries alone establish none
of those stronger conditions.

## What the step guard actually does

A **guard** is a defined check controlling whether a proposed step proceeds.
For a unanimous positive panel, X301's Python guard refuses when the
starting evaluation is not 1, or when a candidate intervention produces
an evaluation other than 1. Otherwise it returns the proposed state, or
the current state if no new one was proposed. Without positive panel
agreement it also refuses, for a separate reason.

Return to a starting model where A is blue. An honest identity-view panel
returns 1. The candidate “remove A” produces 0. This guard refuses too,
although the original formula evaluated to 1. Its policy tests stability
under that candidate menu; refusal is not proof that the original claim
was false.

## Which state is retained?

With the pure procedures used here, refusal returns the original model
instead of the proposed state. An arbitrary callback could mutate a
shared dictionary; the constructor does not prohibit that. Retaining a
reference alone is not a general mutation-safety guarantee.

Next, read [what the refusal receipt checks](61_a_receipt_has_a_scope.md).

AuthorityEffect: None. Supplied panel/guard policy and explicit callback limits.
