# Combining systems: practice answers

Attempt the [practice](COMPOSITES_PRACTICE.md) before opening this guide.

1. The merge is `{p:3,q:8,r:5}`. Projection onto q/r gives `{q:8,r:5}`.
   A shared q is refused even when both values are 8; no identification
   convention has been supplied.
2. The new shape is `(4,(9,1))`. The middle value remains 9: first pair's
   second entry becomes second pair's first entry. No preparation-share
   or statistical independence claim follows from this regrouping.
3. The first order gives `(4,3,3,6)` in A1/A2/B1/B2 order. The second
   gives `(4,3,2,6)`. Running only the relay gives `(4,2,2,6)` and is
   the baseline for either relay comparison. Comparing against the
   untouched B1=9 would combine two changes into one comparison.
4. Before: shares of 0/1 are 3/4 and 1/4. After: 1/4 and 3/4. The
   distance is `(1/2+1/2)/2 = 1/2`; all four readings change. The
   constant-zero probe gives share 1 for mark 0 in both lists, distance
   zero and no changed marks, while the underlying B1 fields still change.
5. Yes, the construction joins different writes in one operation. It
   establishes neither copying nor execution. It is the declared graph
   convention applied to the available rule's footprint.
6. The graph is preserved. The whole record is not: 0 and 8 exchange.
   The A1/B1 readouts agree for the same probe because both inputs are 3.
   Inputs 0 and 2 also give matching even/odd marks despite unequal values;
   that probe merges values and has no injective converse there.
7. No. The observable's label is not checked against its actual reads.
   Check the real function and whether it depends only on retained B
   fields, along with the update's actual writes and nonmutation premise.
   Testing one finite list still does not establish every callback's behavior.

AuthorityEffect: None. Worked supplied examples, not measured transfer results.
