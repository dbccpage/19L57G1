# 12. Say which path changes are allowed

You may exchange two neighboring events when, from the state reached
by the preceding events, both orders reach the same state. Call that a
**verified swap**. A chain of such swaps gives an allowed path change;
the native source calls the resulting relation `Cell`.

For a closed cost, each verified swap preserves the cost. Following
several swaps preserves it again. The research proves this for arbitrary
finite swap chains.

**Predict:** if two histories start and end in the same states, must
verified swaps connect them?

<details><summary>An obstruction from the events themselves</summary>

No. From genesis, a budget write 1 followed by 0 is a return loop.
License-off followed by license-on is another. They have the same full
start and end. But exchanging adjacent events cannot turn budget writes
into license writes: a swap keeps the collection of events. The native
source proves that these parallel loops are not related by a `Cell`.

Both also have state-change count 2. Equal cost alone does not supply
an allowed path change either.

</details>

## What would a stronger rule add?

**Try a change:** declare that a particular return loop may be deleted.
You have added a new allowed path change. If you want cost to be
preserved under that new rule too, you must check it: deleting the
budget loop changes the state-change count from 2 to 0. The old theorem
about verified swaps did not authorize this extra deletion.

This also marks a terminology boundary. The earlier lessons used `cell`
for an admitted face in a vertex-list calculus. Here `Cell` is a relation
between native event histories. A shared word supplies no identification
of those two constructions.

Try the [cost practice](COST_PRACTICE.md) before its [answers](COST_ANSWERS.md).
The [source map](SOURCE_MAP.md) records what the finite desk and general
proofs each establish. No conclusion here identifies a physical force or
an empirically conserved quantity.

AuthorityEffect: None. NS-1/4 own swap soundness and the parallel-loop
counterexample; NS-7 owns cost preservation under `Cell`. The richer
proof-relevant calculus, observer descent, and action/charge questions
are outside this selected introduction.
