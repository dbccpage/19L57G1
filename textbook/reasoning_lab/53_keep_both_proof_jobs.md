# 53. Keep both proof jobs

The previous argument needed a correct start and a preserving step.
Neither can replace the other.

## A wrong start

Start with one counter, then keep adding two. The totals are 1, 3, 5, 7.
The rule preserves the property “one counter plus whole two-counter
packets,” but the proposed claim “the total is twice the update count”
already fails at count zero. The right formula is 1 + 2 × n.

## A step that fails to preserve the property

Start with a lamp value called Off. Supply a rule that flips Off to On
and On to Off. The property “the value is Off” holds initially and
fails after one update. A good start alone supplies no invariant.

An **invariant** here is a property that holds at the start and remains
true after every allowed update under the stated conditions. To prove
preservation, temporarily assume the property at the current stage and
use the update rule to establish it at the next stage. Assuming the
next stage's conclusion instead would leave the required work undone.

<details><summary>Predict: can a rule agree with 0, 2, 4, 6 and fail at the next count?</summary>

Yes. Supply a different rule that gives twice the count through count 3,
then gives twice the count plus one. Its next value is 9 rather than 8.
The earlier four values do not distinguish it from the packet rule.

</details>

For any chosen finite cutoff, we can supply a rule agreeing through
that cutoff and differing immediately afterwards. This is a constructed
counterexample to inferring every later value from those samples alone.
It does not refute the packet proof, which uses the stated packet rule.

Change the cutoff to 4. List the matching values and the first differing
value. Then explain which step premise the delayed rule fails.

Continue to [a history with any number of supplies](54_empty_history_one_more_event.md).

AuthorityEffect: None. Supplied counterexamples and checked mathematical claims.
