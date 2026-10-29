# 00. Match the rows

Imagine three cards called A, B, and C. Two one-place questions, P and Q,
have these recorded answers:

| Card | P | Q |
|---|---|---|
| A | yes | yes |
| B | yes | — |
| C | — | — |

Here **yes** means that the judgment follows from an admitted instance
or rule. **—** means that it does not follow in the present record.
It does not mean that a physical observation proved the judgment false.

A card's *profile* is the set of questions giving yes. In this small
example, matching profiles means matching both entries in the table.
The source calls that relationship *collapse*. It leaves the three
internal positions intact: A remains position 0, B position 1, and C
position 2. Nobody deletes a card or merges two positions.

Our new task is: **add something so A and B have equal profiles**.
We cannot erase A's answer to Q. Predict which single recorded answer
would make the rows match.

Adding Q(B) works. It changes B's row to `yes, yes`.
Merely requesting matching profiles changes no answers; an actual
admission must supply the change.

This starting record came from a separation search. It carried promises
to keep pairs distinguishable. For this example we explicitly release
those old promises before requesting equal profiles. We retain the
cards, questions, instances, and rules. Keeping the promises would be a
different task, taught in Lesson 03.

Next: [compare two small replies](01_two_small_replies.md).
