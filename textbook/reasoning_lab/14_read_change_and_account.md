# 14. Read, change, and account for the effect

Now supply an instrument operation that reads A's old value, stores that
mark, advances A, and adds 1 to a counter. The counter addition is part of
the declared rule; it is not a measured price or a discovered cause.

From A=0, compare another advance with this instrument readout.

**Predict:** if both orders end at A=2 and add the same counter value,
must their full states agree?

<details><summary>Keep the stored marks too</summary>

| Procedure | Final A | Record A | Counter |
|---|---|---|---|
| Advance, then read-and-advance | 2 | 1 | 1 |
| Read-and-advance, then advance | 2 | 0 | 1 |

The target values and counters agree. The stored marks differ, so the
full states differ. Adding a counter did not make the procedures commute.

</details>

## What is a counter allowed to establish?

**Try a change:** configure the same target change with counter addition
0. The target still changes. A zero diagnostic value therefore does not
by itself prove that no target change occurred. You must inspect what
the configured counter actually records.

Also, overlapping access does not force failure in every case. Replacing
the extra advance with the identity operation, which leaves A alone,
makes both orders agree. The source's disturbance counterexample concerns
particular operations; it is not a theorem that every overlapping pair
fails to commute.

Our desk uses fixed, explicitly defined operations and separate target/
record boxes. A software flag named “non-disturbing” is not a substitute
for checking the operation, especially if its record destination can be
the target box itself.

Continue with [15. When matching records justify matching targets](15_matching_records_and_targets.md).

AuthorityEffect: None. The source supplies a concrete noncommuting
instrument example. The book checks the smaller cyclic example above,
the equal counters, and the identity-operation control.
