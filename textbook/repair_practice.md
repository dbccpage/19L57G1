# Units 17–22: requests, repairs and cheapest answers

Try one group before the [separate answers](repair_answers.md).
For each answer, state the starting ledger and the comparison being made.

## Admission and cost

1. Three data occupy positions 0, 1 and 2. Which requests pass the guard:
   (0,2), (2,0), (1,1), (1,3)? Does accepting (0,2) supply a context?
2. Start from the empty ledger. Try: admit one datum, request (0,1),
   admit another datum. Does the last event rescue the failed request?
3. With two data and no forms or instances, reverse the two items of a
   successful mark plan: instance first, form second. Does it replay?
   Does writing both items on one line make its item cost one?
4. Change that starting ledger by admitting a unary form beforehand.
   Can one new instance now meet request (0,1)? Which hypothesis of the
   two-item lower bound no longer holds?

## Witnesses and all stored requests

5. In a two-datum ledger with only the binary instance `link(0,1)`,
   compare contexts `link(_,1)` and `link(_,0)`. Give their answers on
   0 and 1. Which is a witness? Does its absence from the other datum's
   profile assert a negative sentence?
6. Instead admit only `link(0,0)`. Does `link(_,_)` separate 0 and 1?
   Is that permitted instance the same kind of event as a self-demand?
7. A separate three-datum ledger has requests (0,1) and (1,2), no forms,
   and no instances. Add a unary form and only `marked(0)`. Is the chosen
   target (0,1) separated? Is the whole plan a valid response? Explain
   how changing the instance to `marked(1)` changes that answer.
8. Add the uniform rule to the binary-link ledger in question 5.
   Is the admission allowed? Does it retain the link instance? Does
   successful admission imply a valid repair of request (0,1)?

## Renaming and price rules

9. Swap positions 0 and 1 in the two-datum mark ledger with request
   (0,1). What happens to `marked(0)` and to the sorted request? Can an
   invertible renaming turn the unary form into a binary form?
10. Under item-count-first, arity-second ordering, which wins: (2,2) or
    (3,0)? Would adding each pair's numbers give the same ranking?
    Does one minimum class select a literal datum to mark?
11. In reading F, request (1,2), compare the three unary marks on 0, 1
    and 2. Which meet the request? Do the two successful marks preserve
    two data or three? Under the alternative price counting items and
    new instances, are a valid unary mark and binary link still tied?
12. A finite search reports one cheapest class, and someone concludes
    that reality must choose that structure. Which assumptions concern
    the grammar, cost and renaming? What additional evidence would connect
    those assumptions and the search result to physical observations?

AuthorityEffect: None. Eleven model/scope questions and one evidence question;
no measured learner outcome.
