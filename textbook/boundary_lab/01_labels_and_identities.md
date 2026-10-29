# 01. Keep labels and identities apart

Write `a` twice. That action alone does not tell a model whether you mean
one admitted item mentioned again or two admitted occurrences.

The side-free control records labels in a list. Its occurrence-admission
event appends a fresh mark, even if the label is already present:

| Event policy after two presentations of a | Admitted label list |
|---|---|
| Admit a fresh occurrence each time | `[a, a]` |
| Admit by label each time | `[a]` |

These are different supplied admission policies. The control's price
experiment uses the first: **two retained marks**, at indices 0 and 1.
If the second policy retains only one mark, the two-mark requirement
has no subject; that is not a failed separation test on two marks.

An **index** is a position in the list. It is the mark's internal
identity in this model. The label beside it is presentation data and
may repeat. Index 0 and index 1 are different identities even when both
entries say `a`.

However, being present in our representation does not automatically make
an index an internally available distinguishing report. At the control's
base setting, mark permutations are permitted and the comparison key
forgets labels. A **comparison key** is the information the comparison
retains. Here its default is just the number of marks.

The rule for “separated” will ask whether a permitted renaming preserves
that key while carrying mark 0 to mark 1. Writing the two indices in our
code is not enough to make that answer no.

**Predict:** If both labels are `a`, will merely keeping the labels in
the key make their exchange change the key?

Next: [two answers](02_compare_two_answers.md).
