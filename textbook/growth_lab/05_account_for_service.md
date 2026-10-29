# 05. Account for a service budget

[Previous](04_quiet_is_not_finished.md) · [Growth lab](README.md) · [Next](06_test_the_budget_rule.md)

## Predict first

Three entries are waiting. A round adds two more. Its service budget is
two entries. How many remain? Could unused budget from an earlier empty
round help, under a rule that stores no unused budget?

## A second, deliberately simpler model

The research also supplies an accounting experiment. Each round:

1. Admit the next numeric label: 0, then 1, then 2, and so on.
2. Append the new committed pairs to a waiting list.
3. Remove up to the declared budget, oldest entries first.

The **backlog** is the number of entries still waiting. In the example,
three plus two makes five; removing two leaves three. A budget is a
per-round limit. Unused capacity is not saved for another round.

The experiment has no observation views. It assumes entries can be
discharged and that a discharged entry never returns. It does not
construct a new view, prove a repair exists, or run the represented
world's authorization and repair machinery.

## Say what a zero means

An end-of-run backlog of zero means the assumed service cleared the
entries by that selected horizon. It does not mean every round had an
empty backlog, that a longer run will clear, or that an actual device
performed the assumed repairs.

The desk therefore separates the growth-and-views model from the
arrival-and-service accounting model. Compare them by stated assumptions.

## Your turn

Starting empty, arrivals add 0, 1, 2 entries in three rounds. Use budget
one. Record the actual number removed and the backlog each round.

AuthorityEffect: None. Discharge is an admitted service convention here.
