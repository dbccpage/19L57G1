# 12. Keep the target and its record separate

Begin after [the evidence route](08_from_a_model_to_a_trial.md).
We now supply a model of a recording procedure. It is an example to
reason about; no instrument has been tested by calculating its rows.

Start with two boxes. **Target A** holds the value 1. **Record A** holds
the value 0. A **readout** applies a supplied reading rule to the target
and writes the result into its record. Our first rule copies the value.

**Predict:** read A, then change its target value to 2. What is in each box?

<details><summary>Follow both boxes</summary>

| Stage | Target A | Record A |
|---|---|---|
| Initial | 1 | 0 |
| After reading | 1 | 1 |
| After changing the target | 2 | 1 |

The record keeps the earlier mark. Updating a target does not
automatically update its record.

</details>

**Try a change:** read A again. Its record becomes 2 and replaces the
stored 1. This record box stores one mark, not an append-only history.
Our lesson's timeline is an additional record of the supplied operations.

## What does the initial 0 mean?

The model initializes record boxes to 0. A genuine readout can also write
0. The value alone therefore does not tell you whether a readout happened.
The model has no separate “never read” flag or timestamp.

We will add another target B with its own record, a message box, and a
configured counter in later examples. These six boxes define a new
operational model, separate from the three-card model or passage machine.
Calling an operation a readout is a supplied definition; applying it to a
device requires a measurement procedure and collected observations.

Continue with [13. Change one place and read another](13_change_one_place_read_another.md).
Use the [protocol desk](protocols.html) to predict stored marks.

AuthorityEffect: None. P200's readout writes a record while preserving
its target. The book checks the stale-mark example and a later reread.
