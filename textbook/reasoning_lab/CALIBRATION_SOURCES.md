# Calibration: sources, assumptions and checked scope

AuthorityEffect: None. Selected P201 introduction, not a full P201/P202
package review, physical validation or Python-to-Lean refinement proof.
The [six lessons](18_one_length_two_numbers.md) teach numerical meaning
before the optional formal details below.

## What is supplied and what is proved

| Item | Classification and owner |
|---|---|
| Kind labels and a common model magnitude scale | Supplied data; `PhysicalDimension`, `CalibrationStandard` in `research/p201_relational_spacetime/relational_spacetime.py` |
| Reading divided by a positive scale | Defined operation; `RelationalQuantity.rescale_standard` in that Python file; `rescale_unit` in `research/p201_relational_spacetime/lean/RelationalSpacetime.lean` |
| Ratio of same-kind common-scale magnitudes | Defined Python computation; `compute_dimensionless_ratio` |
| Common-unit rescaling preserves a cross-multiplied ratio equation | Proved conditional algebra; `P201RelationalSpacetime.dimensionless_ratio_invariant` |
| Length and duration constructors differ | Proved type-label fact; `cross_dimension_disjoint`, not a physical taxonomy theorem |
| The scale agrees with the new/old standard sizes | Explicit book-side caller premise, checked in `calibration.convert`; not checked by the native Python rescaling API |
| Standards are positive, kinds match and readings are nonnegative | This route’s explicit book-side premises; native Python dataclasses allow broader records |
| Standards and readouts describe an actual device | Open application correspondence; no observations are supplied here |

The source README and claim ledger remain historical owner statements
and are not edited. This teaching route states what the inspected
definitions establish within its narrower declared scope.

## Three representation boundaries

**Raw numbers and quantities.** A record includes its number, kind and
standard. For different standards, the Python ratio multiplies each
number by its own `base_magnitude` before dividing. A ratio of two
quantities is an ordinary ratio; this route does not introduce a
four-object cross-ratio construction.

**Python and Lean.** Python stores signed exact `Fraction` values with
named standard metadata. Lean’s `Quantity d` has a natural-number
numerator and a positive natural-number denominator, without a named
standard field. It does not normalize fraction records. Its
`dimensionless_cross_prod` returns the pair
`(q1.num × q2.den, q1.den × q2.num)`. That pair need not stay literally
equal after rescaling; the theorem supplies the cross-multiplication
identity. If the dividing numerator is zero, the pair’s denominator is
zero. The algebraic identity still holds but supplies no defined ratio.
The book separately checks the positive-denominator premise.

The Lean ratio theorem applies one shared rescaling factor to both
quantities. Mixed-standard comparison and separate conversions to a
common standard are additional checked Python calculations, not an
already-proved named-standard interpretation of that Lean theorem.

**Model and observation.** Standards V, U and W have sizes 1, 2 and 4,
respectively, in a supplied common scale. That assignment is not a
measured calibration. The unit rule is multiplicative; offsets, noise,
drift, operating range and a
device’s physical correspondence need further specification and evidence.
Changing the unit and changing the underlying magnitude remain distinct.

## Retained native counterexamples

The teaching checker calls the actual owner and retains these limits:

- Starting at 6 U with U size 2, the unchecked native call with W size 4
  and scale 1/2 returns 12 W. Its represented magnitude is 48, not 12.
- Native records may label a quantity as length while its standard is
  duration; the raw ratio call can accept it. The book check refuses it.
- A zero-size dividing standard with a nonzero written value can raise
  `ZeroDivisionError` in the native ratio call. The book refuses the
  standard first. A valid zero dividing *value* receives native refusal.

The caller checks are explicit teaching apparatus, not a repair silently
attributed to the research owner. Passing a metadata check does not prove
that the metadata matches a physical reference.

## Checked populations

| Population | Count |
|---|---:|
| Recorded conversion selections | 9 |
| Recorded comparison selections | 6 |
| Additional bounded conversions | 384 |
| Same-kind ratio cases | 2304 |
| Conversions of both operands to a common standard | 9216 |
| Cross-kind refusal cases | 6912 |

The bounded population uses readings 0..5, standards of sizes
1/2,1,2,3 and all four supplied kind labels. The conversion count is
4 kinds × 6 readings × 4 old sizes × 4 new sizes. Same-kind ratios use
two readings and two sizes; four common sizes give the rescaling count.
Cross-kind cases use twelve ordered unequal-kind pairs. Zero-divisor
refusals remain in the counts. These finite populations do not bound
the formal natural numbers or arbitrary Python fractions.

The actual event-handler fixture checks all 63 conversion predictions
and 36 comparison predictions, including incorrect choices, zero,
refusal, prediction gating and resets. It provides no browser-layout
or learning evidence. Separate changed practice checks P/R of sizes
3/6, another same-ratio pair and a mis-scaled record.

## Selected Lean evidence

The existing reasoning driver re-elaborates the exact P201 prefix through
`cross_dimension_disjoint` and closes its namespace. P202 definitions are
excluded; reviewed imports are absent. Four owner reports cover two
definitions and two theorems. Seven additional book reports cover a
positive rescaled denominator, a nonzero ratio divisor, a conditional
common-reference cross-identity and four concrete boundary examples.
The added eleven reports have nine empty axiom sets and two using exactly
`propext, Quot.sound`. With the earlier reasoning/protocol scope, the
logic/P200/P201 portion checks 56 reports. This does not replace the
native package’s
seven-theorem inventory or frozen receipt.

Source hashes use UTF-8 text with LF normalization and are stored in
`calibration.json`. Reproduction is in [DEVELOPMENT](DEVELOPMENT.md).
Book checks do not run the owner verifier that writes its research receipt.

## Work deliberately left open

P202 future-test equivalence, relative clocks, general dimensions/rates,
instrument uncertainty and physical geometry remain outside these six
lessons. Python’s clock advances fast once per step and slow on alternate
step indices, while Lean’s advances fast twice and slow once per step;
its register dynamics also differ. No cross-language clock bridge is
asserted by those six lessons. The separate [clock route](CLOCKS_SOURCES.md)
now teaches selected P202 definitions and their differing scopes.
Finite example checks, physical correspondence and independently
observed beginner comprehension remain separate obligations.
