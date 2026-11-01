# 31. Regroup without losing a part

Keep three supplied values A=2, B=5, C=7. One notation groups A/B first:
`((2,5),7)`. Another groups B/C first: `(2,(5,7))`.

**Predict:** when we change the brackets, must B's value change? Where
do you look for B in each version?

<details><summary>Check your prediction</summary>

B stays 5. In the first version, take the first pair, then its second
entry. In the second, take the second pair, then its first entry.

</details>

An **associator** is the specified regrouping map
`((a,b),c) → (a,(b,c))`. Its inverse puts the brackets back.
These two round trips recover the original entries. The Lean source
proves those round trips and preservation of the three projections
for arbitrary component types.

The nested records have different shapes. Their specified translation
preserves the parts; writing one shape where the other is expected
without translating is a different matter. Python's disjoint-name
merge instead flattens both groupings into the same named dictionary.
The book relates these examples explicitly, without claiming a general
proof that Python implements the Lean definition.

### Combining is not a claim about independence

Suppose a supplied preparation list contains only `(A=0,B=0)` and
`(A=1,B=1)`, with equal weight. Each value of A occurs half the time,
and so does each value of B. But the list never contains `(0,1)` or
`(1,0)`. Its A/B values always match.

Knowing separate shares therefore does not determine which values
occur together. Regrouping records supplies no claim that one part's
value is statistically independent of another's.

**Change one thing:** replace the list by `(0,1)` and `(1,0)`. Have
the separate shares changed? Has the relation within each row changed?

<details><summary>Check the changed example</summary>

The separate shares remain one-half for 0 and 1. The paired values
now always differ. Retain the paired list when the pairing matters.

</details>

Next: [what makes a change local](32_what_makes_a_change_local.md).

AuthorityEffect: None. Regrouping and supplied lists, not a physical independence law.
