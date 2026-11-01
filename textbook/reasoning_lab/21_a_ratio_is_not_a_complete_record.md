# 21. A ratio is not a complete record

A team compares two lists in the same supplied U standard:

| List | First reading | Second reading | First/second |
|---|---|---|---|
| A | 6 U | 9 U | 2/3 |
| B | 12 U | 18 U | ? |

**Predict:** if the ratios match, must the two lists represent the
same individual magnitudes?

<details><summary>Check your prediction</summary>

No. List B also has ratio 2/3, but both of its magnitudes are twice
those of list A. With U of size two steps, A gives 12 and 18 steps;
B gives 24 and 36.

</details>

The ratio keeps the proportional comparison while losing the common
size. Many pairs of magnitudes can have the same ratio. Matching one
ratio does not reconstruct the original pair, establish unchanged
objects or validate a calibration procedure.

Now imagine a faulty conversion report. It relabels both readings
6 U and 9 U as 6 W and 9 W without changing the numbers. Since W is
twice U, those new records represent twice the old magnitudes. Yet
the ratio remains 2/3. The ratio check alone misses this shared mistake.

### Two checks answer different questions

1. Does the calculation preserve the stated ratio? Compare the two
   resulting divisions.
2. Does the claimed unit conversion preserve each represented magnitude?
   Multiply every reading by its own standard’s size and compare before
   with after.

Passing the first check need not pass the second. Passing both checks
establishes consistency with the supplied conversion model, not that
the model matches a real instrument.

**Change one thing:** keep the first reading 6 U but double only the
second to 18 U. What happens to the ratio?

<details><summary>Check the changed example</summary>

It becomes 1/3. Cancellation requires the same positive change applied
to both magnitudes. Changing just one is a different operation.

</details>

This repeats a familiar reasoning pattern: an unchanged summary can
hide changes in the objects it summarizes. Name what information a
comparison retains before treating agreement as a complete explanation.

Next: [carry the calibration conditions](22_carry_calibration_conditions.md).

AuthorityEffect: None. Supplied lists and a shared-error counterexample.
