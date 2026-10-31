# 18. One length, two numbers

Start with the Number lab’s [shares and fractions](../number_lab/README.md)
if halves or division are unfamiliar. This continuation supplies a new
calibration model; it is not derived from the earlier cards or seed.

Imagine a model strip X of length 12 small steps. A unit U spans two
steps. A larger unit W spans four. These lengths are supplied facts of
the example, rather than measurements we collected.

| Record of X | Size of one unit | Reconstructed length |
|---|---|---|
| 6 U | 2 steps | 6 × 2 = 12 steps |
| ? W | 4 steps | ? × 4 = 12 steps |

**Predict before reading:** does the larger unit make the written number
larger or smaller? Fill the question marks.

<details><summary>Check your prediction</summary>

It makes the number smaller: 3 W. Three groups of four steps cover
the same twelve steps as six groups of two. The strip has not shrunk.

</details>

A **standard** specifies what one unit stands for. A **reading** is the
number written with that standard. Here **magnitude** means the reading
multiplied by the standard’s size in the supplied common model scale.
The number alone is not the complete record: “6” does not say “6 of what?”

W is twice the size of U. To preserve magnitude, divide the old reading
by two. In symbols, “new standard = scale × old standard” gives
“new reading = old reading ÷ scale.” A scale must be positive here.

Now use Y, whose supplied length is 18 steps. Its record is 9 U.
Changing to W gives 9/2 W: nine halves of W, or four and a half W.
Multiplying 9/2 by 4 reconstructs 18. Fractions avoid rounding this
exact model value. They do not remove uncertainty from real measurements.

**Change one thing:** replace W by the smaller standard V of size one
step. What number records X now? Check by multiplying back.

<details><summary>Check the changed example</summary>

12 V: the unit is half as large as U, so twice as many units fit.
12 × 1 and 6 × 2 both give 12 model steps.

</details>

Try the first section of the [calibration desk](calibration.html).
The desk selects supplied cases; it takes no measurements.

The operation is based on P201’s `rescale_standard` and `rescale_unit`.
The [source guide](CALIBRATION_SOURCES.md) states the conversion premises
and the different Python/Lean representations.

Next: [keep the kind of quantity](19_keep_the_kind_of_quantity.md).

AuthorityEffect: None. Supplied standards and exact-rational examples.
