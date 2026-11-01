# Numbers, standards and calibration conditions

Date: 2026-10-31. AuthorityEffect: None.

This continuation of the Reasoning lab adds Lessons 18–23 for selected
P201 claims in `p201_relational_spacetime`. It follows the Number lab's
fractions and the P200 target/record route; it asserts no derivation
of these supplied standards from the sealed seed or from P200.

## Reader route

| Lesson | New distinction |
|---|---|
| One length, two numbers | A number changes inversely with unit size while magnitude is retained |
| Keep the kind of quantity | A type label and a numerical reading are different inputs |
| Convert before dividing | Mixed-standard raw numbers do not by themselves give a magnitude ratio |
| A ratio is not a complete record | A common change or error can leave a ratio fixed |
| Carry the calibration conditions | A positive scale must also match the two standards |
| From conversion to a device claim | Exact algebra is separate from a tested physical correspondence |

Each lesson begins with a concrete question, requests a prediction,
gives an explanation and changes one premise. Six changed practice
questions have a separate answer guide. The final lesson supplies a
blank optional reference-comparison worksheet, not invented observations.

## Source and claim boundaries

The native Python rescaling function accepts a positive scale without
checking that it matches `new.base_magnitude / old.base_magnitude`.
Wrong scale 1/2 changes 6 U (U size 2) into 12 W (W size 4), changing
represented magnitude from 12 to 48. The owner dataclasses permit
quantity/standard kind mismatch; a zero standard can also cause a raw
division exception. The book checks these caller premises explicitly,
rather than silently repairing or attributing checks to the owner.

Python uses signed Fractions and standard metadata. Lean uses a
kind-indexed Nat numerator and positive Nat denominator with no named
standard field. Its invariant is a cross-multiplication equation; the
cross-product pair itself may change, and a zero dividing numerator
does not define a ratio. The mixed-standard Python computation and the
shared-factor Lean theorem have separate scopes. No refinement theorem
or instrument validation is asserted.

The source README, ledger, Python, Lean and receipt remain unchanged.
The [source guide](../reasoning_lab/CALIBRATION_SOURCES.md) identifies
supplied objects, book checks, definitions and selected proved results.
P202 clocks/future-test constructions are excluded. Their inspected
Python and Lean step schedules differ; calibration supplies no bridge.

## Reproduction and evidence

The new desk records nine conversion and six comparison selections.
The additional finite population checks 384 conversions, 2,304 same-kind
ratios, 9,216 common-standard rescalings and 6,912 cross-kind refusals.
It uses readings 0..5, standard sizes 1/2,1,2,3 and four supplied kinds.
Zero-divisor refusals are included. All calculations use exact fractions;
the finite populations do not restrict formal Nat fields or all Fractions.

Thirteen new authoring tests include four false packet mutations and a
stale desk. Actual event handlers check 63 conversion and 36 comparison
predictions, including wrong choices, zero, gates and resets. Two
assembled Lean variants reject false magnitude equality and a mismatched
kind argument; unmodified selected source recovers. These failures do
not modify research sources, pins or receipts. The standing injection
record documents them.

Four exact owner reports and seven added book reports re-elaborate the
selected P201 bodies. Nine added axiom sets are empty; two use exactly
`propext, Quot.sound`. The existing reasoning driver now checks 56
reports across its logic, P200 and P201 portions. The scope is smaller
than a native package census and does not replace its frozen evidence.

The existing canonical reasoning Python and Lean wrappers consume the
new packet/population and proofs. No new gate family or independent
pipeline is introduced. The shared renderer uses explicit new filenames,
leaving prior desks intact. The PR records clean-head textbook receipts,
live rendering samples and exact selective publication custody separately.

## What remains

Fourteen canonical research trees now have selected introductory
treatments; 109 do not. Those are discovery counts, not completeness
percentages or a requirement to give all research trees equal curricula.
P202, composite systems, wider algebra/geometry, complete semantic and
accessibility review, physical correspondence and observed beginner
comprehension/transfer/retention remain open. Software checks supply no
learner scores. The textbook's full goal remains active.
