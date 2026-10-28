# 03. Check both directions

[Previous](02_read_if.md) · [Reasoning lab](README.md) · [Next](04_every_and_some.md)

## Predict first

We know that round implies blue on A, B, C. Can we therefore say:
“a listed card is round **if and only if** it is blue”?

## Two checks, not one

Use P and Q as short names for two conditions, such as round and blue.
“P **if and only if** Q” combines two directions:

1. If P, then Q.
2. If Q, then P.

Both must hold. Round implies blue, but blue does not imply round: B
blocks the reverse. Therefore the two-way claim fails.

In a complete Yes/No table, a two-way claim holds exactly when P and Q
have the same answer on each listed row. Either kind of mismatch breaks
it. This is a definition of the comparison, not an extra fact about cards.

## A two-way claim that passes

Here **not round?** reverses the supplied round answer: Yes becomes No,
and No becomes Yes. Its answers on A, B, C are No, Yes, Yes.
Those match **triangle?**. Thus “triangle if and only if not round” holds
on this list.

It need not hold on a larger list. A new square card that is neither
round nor triangular would have not-round Yes and triangle No. The
original table did not include that card.

## Your turn

Remove B from the declared list without changing any answers. Does
“round if and only if blue” now hold on A and C? State the list in your
answer. Removing a counterexample changes the claim's scope.

AuthorityEffect: None. “Not” here complements a supplied Boolean answer;
it does not turn failure of positive derivability into a physical negative fact.
