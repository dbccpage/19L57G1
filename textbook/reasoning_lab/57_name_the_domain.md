# 57. Name the domain

Continue the supplied card interpretation from Lesson 56. A **domain**
is the collection of objects that a particular question ranges over.
The full domain here is A, B and C.

| Domain checked | Every listed card is blue | Some listed card is blue |
|---|---|---|
| A, B | 1 | 1 |
| A, B, C | 0 | 1 |
| C | 0 | 0 |
| No cards | 1 | 0 |

<details><summary>Predict: does the first row establish that every card in the full domain is blue?</summary>

No. That row checks A and B. C is a counterexample to the larger-domain
claim. Keep the domain attached when reporting the answer.

</details>

## Why the empty row differs

“Every listed card is blue” asks whether a listed counterexample exists.
With no listed cards, none exists. Its answer is 1 under this convention.
“Some listed card is blue” needs a listed witness. With no cards, it has
none, so its answer is 0. Neither answer supplies a card.

The X301 Python evaluator looks up a domain by its name. An unknown name
returns an empty domain. A misspelling can therefore make an “every” claim
return 1. That computed answer cannot tell us whether the intended domain
was supplied correctly. Our examples check the name and list first.

## Missing information needs its own representation

In this model, absence from the supplied blue relation produces 0.
An unrecorded physical color does not thereby become amber. To represent
“not yet observed,” we would need a declared observation status or another
explicit interpretation. The empty relation alone does not provide it.

Try the same table for “triangular.” Then examine
[what a truth score means](58_read_the_score_rule.md).

AuthorityEffect: None. Finite model domains and declared evaluation conventions.
