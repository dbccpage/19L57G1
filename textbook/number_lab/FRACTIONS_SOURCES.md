# Fraction toolkit: meaning and evidence

AuthorityEffect: None. Lessons 09–12 are supplied arithmetic apparatus.
They do not derive numbers from the opaque mark or assume a physical
probability theory. Read Number 00–02 first; the map/readout branch is
not required for this arithmetic branch.

A nonnegative fraction has a natural-number numerator and a positive
natural-number denominator. Different representations may have the
same value. Common pieces explain addition; a share of a share explains
multiplication; a quotient asks for a ratio to a positive dividing amount.
The underlying whole and unit stay explicit. A fraction greater than one
is permitted; probability bounds belong to a separate model.

## General book statements

The existing Reasoning Lean driver already includes the exact P204
`QVal` definition read-only. It stores a numerator, positive denominator
and a value-equivalence relation defined by cross multiplication. The
fraction toolkit adds seven book reports using that definition, without
adding another copy of the owner body or changing the native receipt.
Readers need not study P204 before using the elementary arithmetic.

Three general identities prove positive scaling preserves value,
addition with a common positive denominator adds the numerators, and
a supplied positive-divisor quotient multiplied by its divisor recovers
the original fraction's value. The quotient is a book definition; it is
not advertised as an existing native QVal division operation. The
positive divisor numerator makes its denominator positive. Four further
reports check changed sum/product/quotient examples and the denominator's
nonzero property.

Four added axiom sets are empty; three use exactly `propext, Quot.sound`.
The combined Reasoning driver has 155 reports: 127 empty, two `propext`,
26 both-axiom. This is a book-proof scope, not a research census or a
Python-to-Lean refinement theorem. The Number lab's separate 37-report
readout driver retains its original population.

## Finite arithmetic checks

`fraction_toolkit.py` checks every displayed changed arithmetic case and the six
practice tasks with Python's exact Fraction apparatus. Its bounded
population uses all 42 numerator/denominator representations with
numerators 0..6 and denominators 1..6. All 1,764 ordered pairs check
addition and multiplication by separate integer cross products; 1,512
positive-divisor quotients also multiply back to the original value.
The other 252 pairs retain zero-divisor refusal. Four positive scaling
factors check 168 equivalent representations. These counts include
different written representations of the same value; they are not a
census of distinct rational numbers or physical trials.

Run from the repository root:

```powershell
python textbook/number_lab/fraction_toolkit.py
python textbook/checks/u64_number_lab.py
python textbook/checks/u00_reasoning_lab_lean.py
```

Two separately assembled false Lean claims are rejected before the
unmodified source recovers: adding an extra numerator unit, and making
a positive-denominator record have denominator zero. Failed attempts,
if any, remain separate from recovery. No generated observations or
learner scores are supplied. Reading time, understanding and transfer
are not established by these calculations or proof checks.
