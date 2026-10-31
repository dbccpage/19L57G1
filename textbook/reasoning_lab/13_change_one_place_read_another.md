# 13. Change one place and read another

Keep targets A and B and their separate records. An **intervention** is
a supplied operation that changes a specified target. Here “advance”
cycles the target through 0 → 1 → 2 → 0.

Start with A=0 and B=1; both records hold 0. Compare two procedures:

1. advance A, then read B;
2. read B, then advance A.

**Predict:** do the procedures end in the same full model state?

<details><summary>Check what each operation uses</summary>

Yes. Both end with A=1, B=1 and record B=1. Record A and the other
boxes are unchanged. Advancing A reads and writes A only. Reading B
uses B and writes record B only. Neither operation changes what the
other needs or writes.

</details>

Two operations **commute** when exchanging their order gives the same
full end state from every allowed start. The source proves this for the
named read-B/change-A operations. The finite desk displays examples.

## Leaving a target untouched is a narrower claim

**Try a change:** read A instead of B. Starting with A=0:

| Procedure | Final A | Final record A |
|---|---|---|
| Advance A, then read A | 1 | 1 |
| Read A, then advance A | 1 | 0 |

The readout itself leaves A unchanged, but moving it across a change
to A changes the stored mark. A non-disturbing readout need not commute
with every other operation.

To reason from access information, account for every read and write.
There must be no write/write conflict and no write/read conflict in
either direction. Shared reads alone need not interfere. A label claiming
disjoint access does not certify an operation's actual behavior.

Continue with [14. Read, change, and account for the effect](14_read_change_and_account.md).

AuthorityEffect: None. P200 proves specific named commutations from their
record-update definitions. It does not prove a generic commutation theorem
from arbitrary caller-supplied Python footprint labels.
