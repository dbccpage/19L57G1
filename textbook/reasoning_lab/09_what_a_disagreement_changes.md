# 09. What a disagreement changes

[Previous](08_from_a_model_to_a_trial.md) · [Reasoning lab](README.md) · [Next](10_repeats_uncertainty_and_scope.md)

## Predict first

These are fictional P1/front-desk logs:

| Trial | Card | Raw dot | Raw crease |
|---|---|---|---|
| first-K | K | Y | Y |
| first-L | L | N | Y |
| first-M | M | N | N |
| new-N | N | Y | N |

The first three rows supply no counterexample. Can their agreement
overrule the fourth row?

<details>
<summary>Check your prediction</summary>

No. If the fourth row is correctly interpreted as an in-scope Yes/No,
it conflicts with the proposed universal conditional. Three earlier
compatible cases do not remove it. The rows with dot No also do not
provide positive examples of what happens when a dot is present.

</details>

## Say exactly what cannot all hold

Keep these application premises together:

1. The proposed rule applies to this card, protocol and conditions.
2. The recording procedure and legend justify interpreting dot Y as Yes.
3. They justify interpreting crease N as No, and the report is accurate.

These interpreted answers and the rule cannot all hold. The small
book proof `incompatible_application_bundle` checks this logical step.
It does not inspect a card or decide which application premise failed.

A theorem about our supplied table remains a theorem about that table.
The conflict challenges the proposed application of it to these reports.

## Investigate without rewriting the outcome

Check the card identifier, front/back choice, protocol, legend, raw
record and reading conditions. If there is a recording error, retain
the original row and add a documented correction. If the procedure
changes, label the new procedure and trial. A changed rule or decoding
can fit old rows without having been independently supported.

Then make a fresh prediction and collect a fresh reading under the
stated procedure. A mismatch does not, by itself, tell us that the dot
caused a crease, that a reader erred, or that every possible model fails.

## Your turn

Give two different explanations compatible with a reported mismatch.
For each, describe an additional check that could bear on it. Do not
treat either explanation as established by the mismatch alone.

AuthorityEffect: None. The four logs are supplied fiction, not observations.
