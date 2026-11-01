# 39. Mix recipes and keep the choice procedure

Recipe S0 always produces outcome 0. Recipe S1 always produces outcome 1.
Choose S0 with chance 1/4 and S1 with chance 3/4.

**Predict:** what preparation table does the combined recipe produce?

<details><summary>Check your prediction</summary>

Outcome 0 has chance 1/4 and outcome 1 has chance 3/4. The recipe weights
are nonnegative and sum to one. This weighted combination is a **convex
mixture**: it stays within the permitted probability tables.

</details>

You can evaluate a fixed response after mixing, or evaluate it on each
recipe and mix those two answers with the same weights. The results agree.
The same distributive calculation works when mixing response rules.
Working in both arguments is called **bilinearity**.

That algebra still needs the right joint choice procedure. Let response E0
say Yes only on outcome 0, and E1 say Yes only on outcome 1. Mix S0/S1
equally, and separately mix E0/E1 equally. Pairing the two mixed tables
gives Yes chance 1/2: the four recipe/response combinations have equal weight.

If instead the same choice always pairs S0 with E0 and S1 with E1, every
trial says Yes. The separate half-and-half shares look the same, but the
choices have been coordinated. Their joint weights are different.

**Change one thing:** coordinate S0 with E1 and S1 with E0. What is
the Yes chance now?

<details><summary>Check the changed example</summary>

Zero. Neither paired response accepts its paired outcome. Separate mixture
shares alone do not specify the dependence between the two selections.

</details>

Next: [when mixture weights can be recovered](40_recover_indicator_weights.md).

AuthorityEffect: None. Supplied mixing weights and explicit joint-choice assumptions.
