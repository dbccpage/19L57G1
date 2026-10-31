# Cost practice answers

Attempt [the questions](COST_PRACTICE.md) first.

1. Signed changes are −2, +2, 0, total 0. Change counts are 1, 1, 0,
   total 2. Three events were attempted. It is a full-state loop:
   budget returns to 2 and every other field is unchanged.
2. Every step cost stays the same. The added 7 occurs once positively
   and once negatively in each difference. It changes the assigned levels,
   without changing their differences.
3. AB=3 and BC=−4, total −1. Direct AC=−1 too. Returning CA costs +1,
   so the loop total is 0. The cancellation uses the supplied potential.
4. No. The loop A→B→C→A costs 1+1+1=3. A potential difference around
   that return loop would be 0. Equivalently, setting A's value to 0
   would force B=1 and C=−1, whose BC difference is −2, not 1.
5. From live genesis, halt then license-off ends halted with license
   still on; count 1. License-off then halt ends halted with license
   off; count 2. The ends differ, so this is not a commuting square.
   From already halted genesis, both events keep the state: both ends
   are the same halted, license-on state and both counts are 0.
   Closedness applies to the second comparison. The first is not a
   counterexample to it.
6. No. License-off and license-on both change license, and restore
   the full initial state. Their total for the new cost is 2. That
   nonzero loop rules out an exact potential; the zero budget-loop
   result alone could not have established one. These two specific
   totals are checked computations for the newly supplied cost.

For transfer, agreement under commuting exchanges does not permit deletion
of a loop. The empty history costs 0 and the budget return loop has
state-change count 2, although their full endpoints agree. Supplying and
verifying an exact potential on every relevant step would give an
endpoint-only cost there. Merely trying several potentials or sampling
squares does not provide that verification.

A physical application needs separately declared states, event procedures,
units, measurement rules and observations that can test the correspondence.
A signed mathematical cost is not automatically a physical quantity, money or an
empirical conservation law. The [evidence route](../reasoning_lab/08_from_a_model_to_a_trial.md)
explains how to keep model calculations separate from collected readings.

AuthorityEffect: None. These are worked answers, not novice performance.
