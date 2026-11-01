# Units 08–10: answers

Attempt the [practice](context_practice.md) first.

1. On 0: Yes; on 1: No. The profile of 0 contains `marked(_)`; the
   profile of 1 is empty. That context separates them. The datum indices
   remain 0 and 1; comparison of answers does not merge their identities.
2. The arguments are (1,0,1). The middle 0 was already supplied. Both
   holes receive the same tested datum 1.
3. `(_,2)` fails the filled-slot range condition: only 0 and 1 are admitted.
   `(0,1)` has no hole. `(_,_)` is a well-formed context. A uniform rule
   changes derivability, not these context-validity checks.
4. The first row `(_,_)` gives No/No. The next row `(_,0)` gives No/Yes
   and is the first witness in this ordering. One agreeing row does not
   justify collapse when further allowed rows remain.
5. With no forms, there are no contexts and both profiles are empty.
   With only the unary form, there is one test and both profiles are
   still empty. Under its uniform rule, both profiles contain that test.
   All three pairs agree on their respective test sets, so they are
   collapsed. Empty profiles and full profiles are different records.
6. The answer on 0 changes from No to Yes; the answer on 1 stays Yes.
   The unary separating witness disappears and the pair is collapsed.
   Adding derivable answers need not preserve separation.
7. The list is incomplete. The context using form 1 with its one hole
   gives No on 0 and Yes on 1. A completeness proof must include all
   admitted form indices, not just all slot patterns for one form.
8. At minimum, specify what “marked” represents, how the physical card
   will be inspected, and what makes the ledger complete for that question.
   A missing entry alone supplies none of those facts. Actual observation
   records are needed for an observation claim.

Seven computational tasks are checked with native Python examples and
selected Lean calculations. The eighth is a reasoning question, not an
automatically graded or observed learner result. Return to
[Unit 10](units/10_collapsed_of_no_insts.md), then continue to
[Unit 11](units/11_single_token_bound.md).

AuthorityEffect: None. Model answers and an unperformed observation question.
