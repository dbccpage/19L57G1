# 01. Declare a commitment

[Previous](00_list_the_pairs.md) · [Growth lab](README.md) · [Next](02_read_the_observations.md)

## Predict first

Suppose the rule requires distinguishing only consecutive numeric labels.
When 3 arrives after 0, 1, 2, do all three new pairs require a distinction?

## A rule can apply to future arrivals

A **standing commitment** is a rule declared once that says which pairs
must be kept distinguishable whenever both items are held. It is not an
event that produces an item or chooses a repair.

We compare five supplied rules:

| Source name | Required pairs |
|---|---|
| `total` | Every pair of distinct labels |
| `adjacent` | Labels differing by one: 0/1, 1/2, and so on |
| `shared_parity` | Distinct labels both even or both odd |
| `empty` | No pairs |
| `bounded` | Distinct labels both among 0, 1, 2, 3 |

An even label is divisible by two with no remainder; an odd label has
remainder one. The labels are inputs to these rules. Changing a label
without changing an index-based rule can therefore change the task.

For `adjacent`, only 3/2 is a newly required pair. For `empty`, none is.
For `total`, all three are. The arrival is the same; the declared rule differs.

## What has not been explained

One declaration can cover later pairs. That does not explain why this
commitment was chosen or where the arrival came from. Both remain supplied.
The research source expressly leaves its first-demand obstruction open.

## Your turn

Under `bounded`, does item 4 require distinguishing 4/0? Under
`shared_parity`, does it require 4/0 or 4/1? Explain using the rule.

AuthorityEffect: None. These five examples are not all possible commitments.
