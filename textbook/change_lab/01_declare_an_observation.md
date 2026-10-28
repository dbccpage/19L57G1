# 01. Declare an observation

[Previous](00_pair_records.md) · [Change lab](README.md) · [Next: repairs](02_inspect_the_repairs.md)

## Two different empty-looking situations

In one ledger, no observation has been declared. In another, an
observation has been declared with no questions. Should we treat those
as the same state?

The passage machine keeps them separate:

- **Undeclared observation:** there is no declared comparison to consult.
- **Declared, empty observation:** the declared list contains no question
  that could distinguish any pair.

Under this machine's chosen policy, the first state has no active
obstruction. In the second, a retained protected pair can be active.
That policy is a definition. It is not a theorem saying every possible
machine must choose the same convention.

## What a column means

A **column** lists the positions on which one question answers Yes.
Everyone else answers No. The column `[A]` has this table:

| Entry | In the column [A]? |
|---|---|
| A | Yes |
| B | No |
| C | No |

It distinguishes A/B and A/C, but not B/C. We supply the column's
membership answers; the machine has not discovered a physical property.

## When a pair is active

B/C is an **active obstruction** in this passage setting exactly when:

1. Its pair record is retained.
2. It has a protected demand.
3. An observation is declared.
4. None of the declared columns distinguishes B from C.

“Observer-zero” is the source's name for the last condition. It describes
agreement under the declared observation, not identity of the admitted entries.

An active obstruction identifies an outstanding distinction. Whether
an existing repair is available is a further question, taken up next.

## Your turn

Keep B/C retained and protected. Compare no declared observation with a
declared empty list. State the chosen obstruction verdict in each case
and why that verdict alone supplies no new observation.

AuthorityEffect: None. The pre-observation policy is a declared convention.
