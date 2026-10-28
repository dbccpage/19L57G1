# 02. An answer pattern

[Previous: a test and its witness](01_a_test_and_its_witness.md) · [First steps](README.md) · [Next: keep or replace](03_keep_or_replace.md)

## The question

Once the machine can ask two questions, how can it keep their answers
together?

Keep the order **blue?**, then **triangle?** An **answer pattern** is the
list of answers in that order.

| Card | blue? | triangle? | Answer pattern |
|---|---|---|---|
| A | Yes | No | Yes, No |
| B | Yes | Yes | Yes, Yes |
| C | No | Yes | No, Yes |

This kind of ordered answer list is called a **signature**. Keeping the
question order fixed tells us which answer belongs to which question.

## Group cards by their answers

With only **blue?**, A and B have the same pattern. C has another.
The machine therefore has two groups: **A with B**, and **C on its own**.

With both questions, all three patterns differ. There are three groups,
each containing one card.

A **profile**, in the earlier Genesis context definition, collects the
tests that succeed for an item. A signature writes down all the answers
to a chosen finite question list. In our fully supplied yes-or-no table,
the two descriptions agree on which cards are grouped together.

## Every question must agree

Two cards remain **observationally collapsed** for this machine when
every selected question gives the same answer on both. That phrase has
a precise scope: this question list and these supplied answers.

“Every” means that none of the selected questions is an exception. One
witness with different answers is enough to break the agreement.

The two cards still occupy different positions in our list. An equal
answer pattern does not turn two admitted positions into one position.

## What if there are no questions?

Select no questions in the [explorer](explorer.html), predict its groups,
then run it.

The machine has no recorded question that separates any pair, so all
three cards form one observational group. This describes its available
tests. You can still point to the three cards we supplied.

## Your turn

Select only **triangle?**. Write the two groups before checking the
explorer. Then explain the difference between “these cards share an
answer pattern” and “these are one card.”

## Connection to the longer book

Unit 08 introduces profiles and collapse. Unit 61 and Institution 00
introduce question signatures and their classes. [Exact sources](SOURCE_MAP.md).
