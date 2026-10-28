# 06. A record and a legal history

[Previous](05_refusal_and_halt.md) · [Change lab](README.md) · [Next: model boundaries](07_keep_the_model_in_view.md)

## Imagine a record with protection but no retention

The state type has separate fields for retained and protected pairs.
We can write down a raw record with B/C in protection but absent from
retention. Its active-obstruction check is false.

Can the passage's events build that record from its empty starting state?

## Follow the guards

The only event that adds a protected pair first checks that it is retained.
Retained pairs persist under every event. No event removes one. Therefore
every protected pair in a replay from genesis is retained.

The book checks this as a general Lean invariant over all histories of
this event grammar, not merely the finite examples. It also uses the
sealed theorem that every retained pair in such a history was asserted.

In everyday words: a legal history keeps protection inside retention,
and retention inside assertion. A record can have the right field names
and still fail to describe a state reachable by those events.

## Why compare raw records at all?

Comparing records can isolate which condition a predicate reads. Removing
retention from a raw record can show why that condition matters for
activity. It does not demonstrate an available event that removes retention.

The lab includes sixteen raw record comparisons. Four violate the
protection-within-retention invariant. The other twelve passing that
necessary invariant are not thereby proved reachable.

There is another subtlety: “observation declared” and the source's total
zero gate both read the same observation field. Before declaration, the
total gate uses a declared convention. The gates are not four freely
settable independent switches. The source map gives the exact convention.

## Your turn

Someone proposes to resolve an obstruction by “just clearing retention.”
Explain the difference between editing a record on paper and supplying
an event admitted by this kernel. The current event grammar offers no
retention-removal event.

AuthorityEffect: None. The new general invariant is Lean (book), outside the seal.
