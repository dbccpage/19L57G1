# Process practice: answers and reasons

Return to the [questions](CHANNELS_PRACTICE.md) before reading further.

1. (3/5) × (2/3) + (2/5) × (1/4) = 2/5 + 1/10 = 1/2.
   Contributions use each input's conditional row.
2. Flip-then-Reset always gives 0. Reset-then-Flip always gives 1.
   Associativity retains execution order and changes calculation brackets.
3. A/B still agree: both processed answers are 1. A/C still differ:
   their processed answers are 1 and 0. The next function sees the number.
4. Final records are (0, 0) and (0, 1). Read the second component.
   Recovery receives a retained copy, not just the reset component.
5. No. Their conditional rows differ. Input 0 with chance one gives
   output 0 for Keep and output 1 for Flip.
6. It is invalid as a probability row because its sum is 1/2. A separately
   specified normalization of those weights divides each by 1/2 and gives
   [1/2, 1/2]. This changes the supplied row and its interpretation.
7. Both bracketings give rows [1, 0] and [1, 0], since Reset executes
   last. Associativity preserves this sequence. Swapping Reset and Flip
   in Question 2 shows why arbitrary swaps are not licensed.

AuthorityEffect: None. Checked model answers; no empirical or learner claim.
