# Clock and future-reading practice

Attempt these changed examples after Lessons 24–29 before opening the
[answers](CLOCKS_ANSWERS.md). All records and rules are supplied models.

1. Use Python’s pulse rule with initial counters fast=20, slow=9 and
   update index 0. Begin an interval after three updates and continue
   for five more. Give both endpoint counts, the two changes and their
   fast-change/slow-change ratio. Would final fast/slow totals answer
   the same question?
2. Use the uniform Lean rule with the same initial counters. Begin
   after two updates and continue for three. Give the endpoints and
   elapsed ratio. Does the result prove the Python schedule is the
   same transition? What happens to the requested ratio for zero updates?
3. In the separate countdown, start at 4 and 5. Write the four lamp
   pairs at indices 0..3 and the next pair at 4. Which all-future
   assertion does this refute, and why does it not refute the native
   Lean readout theorem?
4. In Lean’s P202 model, both states have A=5 and B=7. One has clocks
   0,0; the other 99,42. Are complete states equal? Are all future
   A/B readouts equal under the source rule? Change the second B to
   8: at which first index does that future-equivalence claim fail?
5. Python’s future helper uses horizon 2 from A=1, B=3. Which indices
   and register readouts does it record? Does it include the state
   after two updates? Separately, if only old indices 0,1,2 were
   compared in an arbitrary model, which new indices are covered after
   shifting the start once? What extra premise would justify more?
6. A team sees a repeated ratio 2 and claims that a device has the
   uniform rule, that its total counter readings must be 2:1, and
   that its future readings are settled. Choose one claim and give
   a changed model counterexample or missing assumption. Specify a
   physical comparison that could test the proposed correspondence.
   Have these written examples themselves collected a physical duration?

AuthorityEffect: None. Separate study questions; no stored reader score.
