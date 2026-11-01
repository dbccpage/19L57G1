# 38. Multiply, then add

Keep the preparation and response rule from Lesson 37.

| Outcome | Preparation chance | Yes chance if this outcome | Contribution to Yes |
|---|---|---|---|
| 0 | 3/4 | 1/2 | 3/8 |
| 1 | 1/4 | 1 | 1/4 |

**Predict:** is the overall Yes chance 3/8, 1/4, or their sum?

<details><summary>Check your prediction</summary>

Add the two contributions: `3/8 + 1/4 = 3/8 + 2/8 = 5/8`.
Each outcome contributes its preparation chance times its own conditional
Yes chance. The mutually exclusive outcomes cover this model's whole list.

</details>

This multiply-and-add operation is the **valuation pairing** of the effect
and state. For the complementary No response, the contributions are
`3/4 × 1/2` and `1/4 × 0`, giving 3/8. Yes and No then total one.

The unit effect returns the total preparation chance, one. The zero effect
returns zero. Neither is a new physical observation. Exact arithmetic
can establish the model's predicted chance without establishing whether
the supplied chances describe a device.

Keep outcome labels attached to their entries. Pairing a response for
outcome 0 with the preparation chance for outcome 1 changes the question.
The native Python space also retains outcome order; a reordered space
needs an explicit correspondence before pairing.

**Change one thing:** make the preparation certain to produce outcome 1,
retaining the same response rule. What is the overall Yes chance?

<details><summary>Check the changed example</summary>

One. Outcome 0 contributes zero, and outcome 1 contributes `1 × 1`.
The effect's two weights still do not have to sum to one.

</details>

Try the first panel of the [valuation desk](valuations.html).
Next: [mix recipes while keeping the choice procedure](39_mix_recipes_keep_the_choice.md).

AuthorityEffect: None. Exact model pairing; no empirical calibration claim.
