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

## Institution foundations I00–I03

Use a new four-input example, after reading
[I03](institutions/units/03_information_counts_classes.md). Explain your
answers without inspecting the answer page.

| Input | Table p | Table r | Requested answer q |
|---|---|---|---|
| J | 4 | 8 | 5 |
| K | 6 | 8 | 7 |
| L | 4 | 9 | 5 |
| M | 6 | 9 | 7 |

10. With family `[p]` and carrier order J,K,L,M, give the four
    representative inputs. Scan M,L,K,J instead: which labels change,
    and which groups change? Does relabelling p's values 4→40 and 6→60
    change those first-input representatives?
11. Recover q from p using one lookup. Change L's requested answer to 12.
    Give a pair that now blocks the lookup. Could choosing a different
    lookup separately for J and L meet the original one-lookup requirement?
12. Write J's and L's signatures under `[p,r]` and under `[r,p]`.
    Which inputs does `[p,r]` still merge? Does appending p again change
    any merged pair? Explain the difference between changing a signature
    list and changing the groups defined by equal signatures.
13. Count classes for `[p]`, `[r]`, `[p,r]`, and `[p,q]` using the original
    q. Does the equal count for `[p]` and `[r]` make either table recoverable
    from the other? Name a blocking pair in each direction. Explain why
    this does not contradict the theorem about appending a known table.
14. An empty family uses the four-input carrier. How many signatures and
    how many distinct signatures are there? What if the carrier is empty?
    What if its list is J,J,K,L,M? Distinguish list length from class count.
15. A software desk shows these invented rows and reports a successful
    lookup. A school proposes using the same labels for actual sensor
    readings. What additional correspondence must be specified and tested
    before the table calculation supports a claim about that sensor?

AuthorityEffect: None. Labels, codes, requested values, and domain choices
are supplied. Explain every answer from the stated task and assumptions.
