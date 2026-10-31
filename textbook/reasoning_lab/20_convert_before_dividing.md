# 20. Convert before dividing

Keep X at 12 model steps and Y at 18. A ratio asks how much of the
second magnitude fits into the first. X/Y means X divided by Y; reversing
their order generally changes the answer.

U spans two steps and V one. Consider these supplied records:

| Quantity | Written record | Common-scale magnitude |
|---|---|---|
| X | 6 U | 6 × 2 = 12 |
| Y | 18 V | 18 × 1 = 18 |

**Predict:** is X/Y equal to 6/18 or 12/18? Which information would the
first calculation discard?

<details><summary>Check your prediction</summary>

Use 12/18, which reduces to 2/3. Dividing 6 by 18 would give 1/3 while
silently treating U and V as equally sized. They are not.

</details>

You can instead convert Y to 9 U and calculate 6/9 = 2/3. If both
records use the same standard, its size appears in numerator and
denominator and cancels. If their standards differ, convert first or
include each standard size explicitly.

Changing both records correctly to W gives 3 W and 9/2 W. Their ratio
is still 2/3. Multiplying that proposed answer by 9/2 gives 3, checking
the division. This is **unit invariance** of the ratio under the stated
conversion: the ratio stays fixed while the individual written numbers change.

### Zero needs two separate cases

Zero length divided by a positive length gives zero. A positive length
divided by zero has no ratio under this operation. Neither does zero
divided by zero. The source’s Python operator refuses a zero dividing
value; the desk also requires positive standard sizes.

**Change one thing:** divide Y by X instead. Is its answer still 2/3?

<details><summary>Check the changed example</summary>

No. 18/12 is 3/2, or one and a half. X/Y and Y/X are different questions.
Their answers are reciprocal when both magnitudes are nonzero.

</details>

The Lean source proves a cross-multiplication identity. For fractions
a/b and c/d with nonzero denominators, equality can be checked by
`a × d = c × b`. P201’s raw cross-product pair can change from `(6,9)`
to `(12,18)` under rescaling; its ratio is unchanged. The theorem does
not say those two pairs are literally equal, and its algebra alone
does not make division by zero meaningful.

Try the second section of the [calibration desk](calibration.html).
Next: [a ratio is not a complete record](21_a_ratio_is_not_a_complete_record.md).

AuthorityEffect: None. Exact comparisons under supplied standards.
