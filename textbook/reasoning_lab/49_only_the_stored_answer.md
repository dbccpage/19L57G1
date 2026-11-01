# 49. Process only the stored answer

A reader stores 0 for item A, 0 for B and 1 for C. The next function
receives only that stored number. It does not also receive the original item.

<details><summary>Predict: can flipping the stored number distinguish A from B?</summary>

| Original item | Stored answer | Flipped answer |
|---|---|---|
| A | 0 | 1 |
| B | 0 | 1 |
| C | 1 | 0 |

A and B still agree. A and C still differ.

</details>

If two stored inputs are equal, a deterministic function gives equal
outputs for them. Therefore a distinction seen after such processing
must already have existed in the stored answers. The original items
can differ even when this particular stored record cannot distinguish them.

## When differences survive

A flip can be undone by another flip. It preserves all distinctions
between stored binary values. A reset cannot be undone on both 0 and 1.

More generally, suppose a recovery function undoes the processing for
every stored value reachable in this model. Then processing preserves
the differences among those reachable values. The recovery premise is
essential; we have not supplied a recovery for an arbitrary function.

Change the example to a function that also reads the item label, and
outputs 0 for A and 1 for B. It can distinguish them because it has an
additional input. This does not refute the stored-answer-only result.

Try each pair in the [desk](channels.html). Continue to
[50. Reset and recovery](50_reset_and_recovery.md).

AuthorityEffect: None. Deterministic post-processing and reachable-image recovery claims.
