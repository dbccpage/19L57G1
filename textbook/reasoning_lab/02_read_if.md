# 02. Read “if” in one direction

[Previous](01_one_answer_per_input.md) · [Reasoning lab](README.md) · [Next](03_check_both_directions.md)

## Predict first

Consider the claim: **If a listed card is round, then it is blue.**
Does B break it? B is blue and is not round.

## Find the case that would break the claim

An **if-then claim** says that whenever its first condition holds, its
second condition holds too. Here it fails only at a round card that
is not blue. Such a case is a **counterexample**.

| Card | Round? | Blue? | Breaks “if round, then blue”? |
|---|---|---|---|
| A | Yes | Yes | No: the required answer is present |
| B | No | Yes | No: the first condition is absent |
| C | No | No | No: the first condition is absent |

B does not break this direction. The claim does not forbid a blue card
from being triangular. All three rows pass, so it holds on this list.

This use of “if” does not say that being round causes blueness. It states
which answer combination is excluded in the declared comparison.

## Reverse it carefully

The reverse says: **If a listed card is blue, then it is round.**
Now B is a counterexample: the first condition is Yes, the required
second condition is No. The original direction did not prove its reverse.

## Your turn

In the desk, select triangle as the first question and blue as the second.
Predict whether “if triangle, then blue” holds. If it fails, name one
card and give both answers; do not merely say “false.”

AuthorityEffect: None. The comparison uses supplied two-valued answers.
