# 02. Read the observations

[Previous](01_declare_a_commitment.md) · [Growth lab](README.md) · [Next](03_grow_without_repair.md)

## Predict first

All distinct pairs must be distinguishable. We hold 0, 1, 2 and can ask
“is the item in {0,1}?” Which pair still needs another distinction?

## Requirement and current success are different

A **view** in this model is a supplied list of labels. Its yes/no question
asks whether an item is in that list. A view separates two items when one
answer is Yes and the other is No. Several views separate a pair if at
least one does so.

The braces in {0,1} simply list the members: 0 and 1.

For view {0,1}, items 0 and 1 both answer Yes; item 2 answers No.
The pairs 0/2 and 1/2 are already separated. Pair 0/1 is not.

A **demand** here is a pair that meets both conditions:

1. The standing commitment requires the pair apart.
2. No current view separates it.

Thus the demand list is just 0/1. It is not the list of all possible
pairs, nor the list of all pairs mentioned by the commitment.

## Do not read absence as equality

Having no view that separates 0 and 1 does not establish that the items
are the same. It says these supplied observations do not distinguish them.
Likewise, an empty demand list may mean every requirement is met, or may
mean the commitment required nothing. Check both the rule and the views.

## Your turn

Add view {1,2}. Write each item's two-answer pattern. Is any pair still
unresolved under `total`? What changes if the commitment is `empty`?

AuthorityEffect: None. A membership question is a defined formal view,
not evidence that a physical device measures that membership.
