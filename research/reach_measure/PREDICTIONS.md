# Predictions, frozen before either side ran

A missed prediction is recorded next to its value in `STATUS.md` and never
edited here. `AuthorityEffect: None.`

## Chronology

`reach.py` existed when this file was hashed. **Neither `sealed_side.py`
nor `dual_side.py` existed, and no value below had been computed.** The
Lean package did not exist either. Everything in this file is prospective.

## The declared measure, frozen

REACH(base, delta) is the number of pluggings that become derivable: the
growth in total profile size, summed over the data of the augmented state.
Nothing is weighted by hand. `mu3(base, delta) = (reach, item count)`,
lexicographic, reach leading.

## Predicted

- **R1.** Among the sealed Challenge-3 valid responses at the minimum item
  count, **no response contains a uniform rule**, because the estate proved
  a uniform-rule item is never a minimum valid response for separation. So
  on the sealed side the reach measure has no local-versus-global axis to
  act on, and this rung's headline cannot come from there. Whether it
  orders the tied classes differently from `mu2` is recorded, not
  predicted.
- **R2.** A single instance and a single uniform rule have identical
  sealed costs — `mu1 = 1` and `mu2 = (1, 0)` for both — while their reach
  differs whenever the rule's form has a plugging not already derivable.
  Therefore **no function of `mu1` and `mu2` can separate a local response
  from a global one**, and a base-relative measure is not a convenience but
  a necessity. Provable, and the Lean package will carry it.
- **R3.** Reach is not a refinement of the item count: there is a base and
  a pair of responses, one of two instances and one of a single rule, with
  `mu1` preferring the rule and reach preferring the two instances. So the
  two orders are not nested and reach can prefer strictly more items.
- **R4.** On the dual tree's identification demands, wherever both a
  single-instance response and a single-rule response are valid, `mu3`
  strictly prefers the instance, so the `mu1` tie set strictly shrinks at
  those demands. Predicted at a majority of the demands carrying a
  mixed-kind tie.
- **R5.** The dual tree's 164 rule-alone minima split into two groups: those
  where an instance response was also available at the same demand, where
  `mu3` re-selects; and those where only rule responses are valid, where
  `mu3` keeps the rule. **The partition is the finding**; its sizes are
  recorded, not predicted.
- **R6.** `mu3` never selects a response the sealed or dual validity test
  rejected. It re-prices the valid set and never widens it; the enumerators
  remain the authority on validity.
- **R7.** Reach is base-relative: the same delta has different reach on two
  different bases, exhibited.
