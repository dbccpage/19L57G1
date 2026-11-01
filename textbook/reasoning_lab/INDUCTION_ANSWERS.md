# Induction practice: answers and reasons

Try the [questions](INDUCTION_PRACTICE.md) first.

1. Thirteen. At n=0 the formula gives four, the stated start. Assuming
   the total at n is 4 + 3 × n, the next update adds three, giving
   4 + 3 × (n + 1). This covers an arbitrary nonnegative whole-number n.
2. The start case fails: at n=0 the actual total is one, while 2 × 0 is
   zero. The count formula with the actual start is 1 + 2 × n.
3. The values are 0, 2, 4, 6, 9. The step from count 3 to 4 adds three,
   not two: 9 differs from 6 + 2. Agreement through count 3 does not
   establish that this rule always adds a two-counter packet.
4. The proof allows any starting ledger. An empty list performs no
   event and returns that ledger, not necessarily an empty one. Each
   supplied event then leaves it fixed. Different supplied tokens are allowed.
5. The condition fails because that event is not a supply. Lean's
   token-erased admission increases its datum count. Python instead takes
   a token and can leave its ledger fixed on a repeat; that different
   definition does not repair the missing all-supplies premise.
6. At most three states and two rounds between them. A repetition at
   measure two breaks strict increase. Constant or repeated measures can
   accompany arbitrarily long runs without contradicting the theorem.
7. No. The proof applies to the model's exact rules. For example, the
   interpretation of a counter value, the absence of unrecorded resets,
   or the claim that each device update adds exactly one specified packet
   still needs application evidence. No such evidence was supplied here.

Return to [Lesson 53](53_keep_both_proof_jobs.md) if either proof job was
missing. Use [54](54_empty_history_one_more_event.md) for list structure
and [55](55_a_measure_that_climbs.md) for strict growth and fixed ceilings.

AuthorityEffect: None. Model answer guide; no measured learning result.
