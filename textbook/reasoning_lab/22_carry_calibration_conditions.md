# 22. Carry the calibration conditions

Start with 6 U, with U of size two model steps. W has size four.
The correct scale “new standard divided by old standard” is 4/2 = 2.

| Proposed scale | New number from “6 ÷ scale” | New magnitude in W |
|---|---|---|
| 2 | 3 | 3 × 4 = 12 |
| 1/2 | 12 | 12 × 4 = 48 |

**Predict:** both proposed scales are positive. Is positivity alone
enough to make either row a valid conversion of the original length?

<details><summary>Check your prediction</summary>

No. Only scale 2 agrees with W being twice U. The other row follows
the division formula with a mismatched scale and changes the represented
magnitude. A formula needs the premises that give its inputs meaning.

</details>

For this lesson’s conversion, carry these conditions together:

- Quantity and standard have matching kind labels.
- Standard sizes are positive exact fractions; readings are nonnegative.
- The proposed scale equals new standard size divided by old size.
- Magnitudes use the same supplied common reference before and after.
- The rule changes units multiplicatively: it does not add an offset,
  change the object or include an instrument-error model.

These are conditions of the supplied teaching model. They are not
claimed to describe every instrument or every possible quantity.
Negative readings, additive offsets and uncertainty would need further
definitions and checks. A name like “calibration” does not supply them.

### What the source checks, and what the caller supplies

The native Python rescaling function checks a positive scale and the
new standard’s kind, then divides. It does not check that the scale
matches the two recorded standard sizes. Its dataclasses also permit
inconsistent kind labels or zero standard sizes. The teaching desk
checks these additional premises before calling the native functions.

Lean uses natural-number numerators and positive denominators, rather
than Python’s broader signed fractions. Its quantity has a kind but no
named standard field. The lesson’s common-reference interpretation is
therefore explicit supplied data, not an already-proved Python/Lean bridge.

**Change one thing:** take a supposed standard of size zero. Can it
serve as the positive reference required here, even if its name looks valid?

<details><summary>Check the changed example</summary>

No. The name does not repair the missing positive size. The teaching
desk refuses it; bypassing those checks can make the native ratio call
raise a division error rather than return the promised refusal.

</details>

Next: [from conversion to a device claim](23_from_conversion_to_a_device_claim.md).

AuthorityEffect: None. Explicit caller premises and source-level limits.
