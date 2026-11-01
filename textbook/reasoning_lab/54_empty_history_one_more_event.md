# 54. An empty history, then one more event

A **history** is a finite list of events in their recorded order.
**Replay** applies them to a starting ledger. Unit 03's Lean supply
case returns the ledger unchanged, whatever token number is supplied.

We want to prove: replaying a history containing only supply events
returns its starting ledger. The start can already contain entries.

## Cover the two shapes of a list

An **empty list** contains no events. Its replay performs no update and
returns the start. This is the start case.

A **nonempty list** has a first event and a remaining list. Suppose the
claim holds for that remaining list. If the first event is a supply, it
leaves the ledger fixed. Replaying the rest therefore starts from the
same ledger and returns it. This is the step case.

This is **list induction**. The remaining list is shorter than the whole
list, and every finite list eventually reaches the empty shape by removing
first entries. We cover an arbitrary list by its shape, without listing
all histories. The assumption about the remaining list is the induction
hypothesis; it is not permission to assume the whole claim we are proving.

<details><summary>Predict: must all supplied token numbers be equal?</summary>

No. Each first event need only be a supply. Token 3 followed by token 8
still leaves the ledger fixed under the given supply case. The history
can retain different events even when their final ledger agrees.

</details>

Change one event to token-erased Lean `admitDatum`. Its datum count
increases, so the all-supplies condition fails. That changed history is
not covered by this proof. Python's token-aware admission has a separate
repeat-token case; do not substitute it for Lean's event definition.

[Unit 03](../units/03_supply_no_op.md) gives the actual statement and
proof. [Unit 11](../units/11_single_token_bound.md) uses a related method
with a changing ledger: the chosen store property must hold initially
and survive each permitted successful step. It does not require the
whole ledger to stay fixed.

Continue to [a measure that climbs](55_a_measure_that_climbs.md).

AuthorityEffect: None. Restatement of the book's checked supply-history
argument; native Python examples are separate implementation checks.
