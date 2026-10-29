# 00. List the pairs

[Growth lab](README.md) · [Next](01_declare_a_commitment.md)

## Predict first

We hold three distinct items, labeled 0, 1, 2. How many pairs can we make
without pairing an item with itself? If item 3 arrives, which pairs are new?

## Count by listing

The old pairs are 0/1, 0/2, and 1/2: three pairs. The new item can be
paired with each old item: 3/0, 3/1, 3/2. There are now six pairs in all.

Here a slash means “the pair to compare.” It is not division.
The source lists a pair in one chosen order, so 0/1 and 1/0 are not counted
as two tasks. All five commitments used in this route treat the pair
symmetrically. Arbitrary commitments in the formal type need not do so.

If we hold four items and add a fresh fifth one, we add four pairs. To
understand the rule, point to each old item and pair it with the newcomer.
We do not need a formula to see why there is one new pair per old item.

## A pair is not yet a demand

Listing possible comparisons does not say which ones matter. A rule must
say which pairs require a distinction. Observations must say which are
already distinguished. We will keep these two decisions separate.

## Your turn

List the old and new pairs when item 2 arrives after items 0 and 1.
Then explain why relabeling the items does not change this pair count.

AuthorityEffect: None. Distinct item labels and the one-entry-per-pair
listing convention are supplied here.
