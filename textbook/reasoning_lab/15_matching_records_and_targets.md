# 15. When matching records justify matching targets

A **probe** is the supplied function turning a target value into a
recorded mark. If both targets have value 1 and both readouts use the
same probe, their new marks agree. Equality of inputs gives equality
of outputs for a function.

**Predict:** if the marks agree after both readouts, must the targets agree?

<details><summary>Try a reader that merges values</summary>

Supply an even/odd probe: even inputs give 0 and odd inputs give 1.
With A=0 and B=2, both records become 0. The targets remain different.
This probe loses a distinction, just as storing only one card question
can lose another answer.

</details>

To infer equal targets from equal fresh marks, require the same probe
to be **injective** on the relevant values: it must not give two different
target values the same mark. The book proves that implication under the
explicit injectivity hypothesis. The copying probe has this property;
the even/odd probe does not on 0/1/2.

## Carry both procedure conditions

**Try a change:** set A=B=1, copy A into record A, but always write 0 into
record B. The target values agree and the marks differ. The two observers
used different probes, so the earlier agreement theorem does not apply.

Record boxes must also have been updated by the stated procedure. Two
initial zeros do not certify that either target was read.

The source's swap rule exchanges both target boxes and both record
boxes. Swapping only target labels leaves record ownership behind and
defines a different operation. The proven swap correspondence preserves
the complete specified arrangement.

Continue with [16. A connection needs an actual update](16_a_connection_needs_an_update.md).

AuthorityEffect: None. P200's observer-agreement and swap results keep
their stated hypotheses. The injective converse and the two failure
examples are checked book claims. No agreement between physical observers
is inferred from calculating these model records.
