# 55. A measure that climbs

Keep three data numbered 0, 1 and 2. The possible small-first pair
requests are (0, 1), (0, 2) and (1, 2). Suppose each accepted round
keeps the data fixed and records one previously absent request.

| Recorded state | Request count |
|---|---|
| Before any round | 0 |
| After one new request | 1 |
| After two | 2 |
| After three | 3 |

The count is a **measure**: a whole number attached to a state. Here it
increases strictly at every counted round, meaning its next value is
larger. Its fixed **ceiling** is three.

## Apply the induction idea

At stage zero the measure is at least zero. If after n rounds it is at
least n, strict increase makes it at least n + 1 at the next round.
Induction supplies the claim for every stage of such a run.

The measure cannot stay at most three after four strict increases.
Thus this example has at most three rounds and four recorded states.
In general a nonnegative whole-number measure capped by B has at most
B + 1 states when it strictly increases between adjacent states.
This general bound can be loose when the starting measure is already positive.

<details><summary>Predict: does a finite set of possible states make every repeated procedure stop?</summary>

No. Use the two allowed lamp values Off and On, with the rule “keep the
current value.” Starting at Off, this procedure stays Off after any number
of updates. Its measure stays fixed, so the strict-increase premise fails.
Likewise, imposing an already recorded request leaves the request count fixed.

</details>

Adding another datum also changes the situation: requests involving
that new datum become possible, so the old ceiling of three no longer
applies. [Unit 28](../units/28_closure_must_stop.md) states the bound's
actual conditions. A bound on these counted rounds is not a bound on
every successful event or on elapsed physical time.

A mathematical induction proof establishes what the stated rule permits.
Applying it to a device additionally requires evidence for the chosen
state, update and readout rules. Matching a few observed values does
not supply every later step premise.

Try the [seven changed questions](INDUCTION_PRACTICE.md) before the
[separate answers](INDUCTION_ANSWERS.md). Optional
[source details](INDUCTION_SOURCES.md) distinguish these proofs and checks.

AuthorityEffect: None. Conditional measure argument and supplied examples;
no physical duration or learner outcome is measured.
