# 25. Compare changes, not totals

Use the Python pulse rule from Lesson 24. Compare two intervals, each
containing three updates:

| Interval | Fast before/after | Slow before/after |
|---|---|---|
| Start at update 0 | 0 → 3 | 0 → 1 |
| Start at update 1 | 1 → 4 | 0 → 2 |

**Predict:** does each interval have the same fast-change/slow-change
ratio merely because both contain three updates?

<details><summary>Check your prediction</summary>

No. Fast changes by 3 in each. Slow changes by 1 in the first and 2 in
the second. The ratios are 3 and 3/2. Where an interval starts matters
when a pulse falls inside one interval but not the other.

</details>

The **elapsed change** is final count minus initial count. The chosen
ratio is fast change divided by slow change, in that order. It is
not necessarily the final fast count divided by the final slow count.

For the uniform Lean rule, start the counters at 10 and 3. After two
updates they are 14 and 5. Their changes are 4 and 2, giving ratio 2.
The total-count ratio 14/5 is different. Starting offsets are not elapsed ticks.

Under that Lean rule, every positive number of updates gives twice as
many new fast ticks as new slow ticks. Under the Python pulse rule,
a positive even number of updates gives ratio 2; odd intervals can
depend on their starting position. The source’s finite sixteen-update
example does not prove a constant Python ratio over every interval.

### When the dividing change is zero

Zero updates give zero change in both counters. Python’s first update
also gives zero slow change although fast changes. Neither interval
has the requested fast-change/slow-change ratio: division by zero is
not supplied by this operation. The equation `0 = 2 × 0` alone does
not define a ratio of zero changes.

**Change one thing:** start Python’s interval after its first update
and take just one more update. What ratio is available now?

<details><summary>Check the changed example</summary>

The counters move from 1/0 to 2/1. Both change by one, so the ratio
is 1. This differs from the first one-update interval, whose slow
change was zero. It does not contradict the different uniform rule.

</details>

Next: [read only what the readout contains](26_read_only_what_is_shown.md).

AuthorityEffect: None. Exact counter changes under specified update rules.
