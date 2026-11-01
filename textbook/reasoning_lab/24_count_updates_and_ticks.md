# 24. Count updates and ticks

Use the [calibration lessons](18_one_length_two_numbers.md) first if ratios
are unfamiliar. Here we supply two different clock rules from the P202
source package. Neither is derived from the earlier cards or seed.

Begin with two counters, fast and slow, both at zero. Under the Python
rule, fast gains one on every update. Slow gains one only on updates
2,4,6,... . An **update** is one application of the declared transition.
A **tick** here is one addition to a counter, not a measured second.

**Predict:** after three updates, what do the counters hold? How many
rows are needed to show the initial state and all three results?

<details><summary>Check your prediction</summary>

Fast holds 3 and slow holds 1. Four rows include the initial state:

| Updates completed | Fast | Slow |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 1 | 0 |
| 2 | 2 | 1 |
| 3 | 3 | 1 |

</details>

The counters are stored fields of the model. They do not read the
computer’s wall clock. Running the same updates more slowly on a computer
does not insert extra ticks into these formulas. That is a fact about
the supplied transition, not a demonstration that physical time has
been derived or that every clock ignores its surroundings.

The Lean source uses another rule: fast gains two and slow gains one on
every update. After three updates its counters are 6 and 3. Its A and
B registers also differ from Python’s rule: both increase by one, while
Python’s B cycles through four values. Keep the chosen rule with the record.

**Change one thing:** use the Lean rule for one update. Can its result
be substituted for the Python rule’s one-update result without explanation?

<details><summary>Check the changed example</summary>

No. Lean gives fast/slow 2/1; Python gives 1/0. Similar names and an
occasional shared ratio do not prove the two transitions are equivalent.

</details>

Try the [clock desk](clocks.html). Its Lean-rule execution is an explicit
book adapter for those field updates. The [source guide](CLOCKS_SOURCES.md)
separates that finite execution from the native Lean proofs.

Next: [compare changes over an interval](25_compare_changes_not_totals.md).

AuthorityEffect: None. Supplied counter rules; zero measured durations.
