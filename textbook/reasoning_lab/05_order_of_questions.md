# 05. Does the witness depend on the pair?

[Previous](04_every_and_some.md) · [Reasoning lab](README.md) · [Next](06_carry_the_hypotheses.md)

## Predict first

Make blue and triangle questions available. For every pair of different
listed cards, can we find a question that separates that pair?

| Pair | One separating question | Answers on that pair |
|---|---|---|
| A/B | triangle? | No, Yes |
| A/C | blue? | Yes, No |
| B/C | blue? | Yes, No |

Each pair has a witness. The witness is allowed to depend on the pair.

## Change the order of the demand

Now ask for **one available question that separates every pair**.

Blue fails on A/B. Triangle fails on B/C. Neither single question works
for all three pairs. We have verified the first demand while refuting
the second, on exactly the same table and list of questions.

The second demand asks whether at least one common question exists.
More than one may qualify; we only need to be able to choose one.

Read the difference slowly:

- Choose a pair, then find a question for it.
- Choose one question first, then require it to work for every pair.

A question chosen first can serve every pair only if it passes every
one of those checks. If it does, it also supplies a witness for each
individual pair. The reverse need not follow, as this example shows.

## A family can do what one question cannot

The joint answer patterns for blue and triangle are distinct on A, B, C.
The combined pattern uses both answers. It is not a single original
Yes/No question, and we should not quietly substitute it for one.

## Your turn

Select only A and B. Does triangle now serve as one question for every
different-card pair in that smaller domain? Then select no questions.
Can any question be supplied as a common witness, even if there are no pairs?

AuthorityEffect: None. Pair and question domains are separately declared.
