# 02. Inspect every existing repair

[Previous](01_declare_an_observation.md) · [Change lab](README.md) · [Next: gates](03_budget_and_permission.md)

## Start with the one-column table

The current column is `[A]`: A answers Yes, B and C answer No. We have
retained all three pair records and protected A/B and B/C.

The new task is to distinguish B/C. We may try putting one additional
entry into the existing column. Predict the effects before reading on.

| Attempt | Resulting answers on A, B, C | What happens |
|---|---|---|
| Put A in [A] again | Yes, No, No | A is already present; no repair |
| Put B in [A] | Yes, Yes, No | B/C separates, but protected A/B collapses |
| Put C in [A] | Yes, No, Yes | B/C separates and protected A/B survives |

The **existing response menu** contains precisely these three
(current column, admitted position) choices. A structural repair must
resolve an active protected pair and preserve every already separated
protected pair. Only the C choice qualifies here.

So an active obstruction can have a repair. “Active” does not mean that
every response has failed.

## Add one protected demand

Now protect the already retained A/C pair. Keep every observation and
entry unchanged. The C choice would collapse A/C, so it no longer qualifies.
All three existing-column attempts now fail the structural repair condition.

This is **exhaustion of this menu**. It says which three moves were checked.
It does not say that every possible new question or every other machine
has been ruled out.

We can still propose a new column `[B]` or `[C]`. Appending a question
keeps the old `[A]` answers. The next lessons distinguish those proposals
from permission and budget to execute them.

## Your turn

Name the single changed field that made the old C repair invalid. Then
explain why exhaustion of the three-item existing menu leaves room for
a proposal that adds a column.

AuthorityEffect: None. All three attempts are checked in the supplied menu.
