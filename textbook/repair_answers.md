# Units 17–22: answers

Attempt one group of [practice questions](repair_practice.md) first.

## Admission and cost

1. Only (0,2) passes: smaller first, both below 3. The other pairs fail
   order, self-pair or range checks. Recording (0,2) adds no context.
2. No. At the request event only position 0 exists. Replay returns failure
   at that step; the later admission is not a successful continuation of it.
3. It fails: the instance's form is absent when the first item is tried.
   A delta applies left to right. Layout on the page does not change the
   two-item list length; bundling it typographically creates no new item kind.
4. Yes: admit its instance on 0 or on 1, with no uniform rule. The
   hypothesis that the starting form list is empty no longer holds.

## Witnesses and all stored requests

5. `link(_,1)` gives Yes/No and is a witness. `link(_,0)` gives No/No
   and is not. No here means that plugging is not derivable under the
   supplied instance/rule checks; it is not an admitted negative judgment.
6. Yes: `link(_,_)` gives Yes on 0, through `link(0,0)`, and No on 1,
   through `link(1,1)`. Both holes receive the same tested datum. An
   instance can repeat an index; the request guard independently rejects
   asking a datum to be separated from itself.
7. Marking 0 separates (0,1), but leaves (1,2) with No/No. The plan
   replays and fails validity because that stored request remains unmet.
   Marking 1 instead gives No/Yes on (0,1) and Yes/No on (1,2), meeting
   both. Neither request had to be satisfied in the starting ledger.
8. Yes, the rule is allowed and retains the instance. It makes all
   contexts of that form derive on both data, so (0,1) collapses. Replay
   success and valid response are distinct checks.

## Renaming and price rules

9. The instance becomes `marked(1)`. The request maps to (1,0), then
   sorts to (0,1). Swapping again undoes the map. Renaming preserves
   form arity, so a one-place form cannot become a two-place form.
10. (2,2) wins because its first component is smaller. Addition would
    rank the sums 4 and 3 the other way. The supplied order is not addition.
    One minimum class identifies a shape under renaming, not a literal
    choice of which datum receives the instance or an executed event.
11. Marking 0 leaves the requested pair at No/No; marking 1 or 2
    separates it. All three data remain in the ledger. The two successful
    marks are isomorphic by swapping 1 and 2 while fixing 0. Under the
    alternative price, a valid mark and link each cost (2,1): two items
    and one new instance. Neither can be beaten by fewer than two items
    or by a two-item, zero-instance plan on the form-less starting ledger.
    They remain different minimum classes under that price.
12. The search has a declared item grammar, bounds, cost order and
    isomorphism relation. Those choices delimit its conclusion. To make
    a physical claim, specify what data, instances and procedures represent,
    justify the correspondence, and compare predictions with recorded
    observations. A finite-search receipt supplies none of those observations.

The model calculations and scope claims have executable or proof checks.
The final question asks for empirical evidence not collected here. These
checks do not establish a reader's understanding or retention. Return to
[Unit 22](units/22_mu2_unique.md), then continue to
[Unit 23](units/23_selfdiff_consistent.md).

AuthorityEffect: None. Model answers and an unperformed evidence question.
