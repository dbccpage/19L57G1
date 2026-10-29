# Practice: read the exact claim

[Reading guide](reading_formal_statements.md) · [Answers after your attempt](reading_formal_answers.md)

Supply this new table:

| Item | Stored code p | Requested answer q |
|---|---|---|
| K | 7 | red |
| L | 7 | red |
| M | 9 | green |

1. Name the domain and give a successful lookup g on the stored codes.
2. Replace L's requested answer by green. What pair now blocks a lookup
   on all three items? State the two incompatible equations.
3. With that changed table, restrict the domain to K and M. Does the
   successful lookup establish recovery for the excluded item L?
4. Return to the original three-item table. Allow the lookup to accept
   any code 0, 1, 2, and so on, returning either red or green. Code 12
   never occurs. Must all successful rules agree at 12?
5. Translate “there exists one g that works for every x in D” into words
   describing who receives which input. Explain why a separate g for
   each original item would be a different claim.
6. An observer record gives `Zero : R → Prop` and equivalence-law proofs.
   Someone says “we can therefore run a program deciding Zero on any R.”
   What additional ingredient has that person assumed?
7. A theorem requires a fresh arrival and no observation views. A worked
   example supplies an arrival but already has views. Does the theorem
   give its numerical conclusion for that example?
8. A finite toy table and its formal theorem agree. Name an empirical
   question still needed before using it to describe a real recorder.
9. A generic driver returns `closed` when its supplied next-step function
   returns `none`. Does the tag by itself establish that no active demand remains?

AuthorityEffect: None. Labels, codes, requested values, and domain choices
are supplied. Explain every answer from the stated task and assumptions.
