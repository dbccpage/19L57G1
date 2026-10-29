# 06. State where the lookup is unique

[Previous](05_change_the_right_thing.md) · [Map lab](README.md) · [Next](07_finite_and_global.md)

## Predict first

Keep blue, using representatives A and C. A correct blue lookup must
send A to Yes and C to No. What does correctness require at label B,
which this recorder never outputs?

## The image is the set of outputs that occur

A map's **image** consists of the outputs it actually produces on its
declared domain. Here that image is the labels A and C, not every label
we could write on the page.

Every successful lookup agrees on those two labels because their required
answers are fixed by actual cards. A lookup's values on B and D are not
constrained by this recovery task. Changing them cannot change a result
for any selected card.

The desk can list two complete lookup tables that differ on unused labels
while both passing every recovery equation. That is a concrete limit on
the word **unique**: unique on the image does not mean unique everywhere.

## A quotient has no extra unnamed classes

There is a related distinction. If the lookup's input type consists
exactly of the actual classes, every such input is represented. There
are no unused label inputs of that type. Correct lookup functions then
agree everywhere on that quotient.

Our displayed four-label tables deliberately allow unused labels. Do
not silently replace that label set by the actual class set, or the
actual class set by all natural-number labels.

## Your turn

Reverse representative order. Which labels now occur? Which entries
of a complete four-label lookup remain unconstrained? Explain why
the set of recoverable questions has stayed the same.

AuthorityEffect: None. Lookup counts in the desk concern its explicitly
finite label and answer alphabets; they do not enumerate all Lean functions.
