# 16. A connection needs an actual update

Add a message box M. Merely drawing a connection or calling M a channel
does not update B. Supply two separate operations:

1. **send:** copy A's value into M;
2. **receive:** copy M's value into B.

Start with A=0, B=0, M=0 and record B=0. Advance A to 1.

**Predict:** what does reading B store before sending? What changes after
sending and receiving? Does record B update automatically too?

<details><summary>Follow each write</summary>

| Stage | A | Message M | B | Record B |
|---|---|---|---|---|
| After advancing A | 1 | 0 | 0 | 0 |
| Read B before relay | 1 | 0 | 0 | 0 |
| Send | 1 | 1 | 0 | 0 |
| Receive | 1 | 1 | 1 | 0 |
| Read B again | 1 | 1 | 1 | 1 |

Before the relay, the local A update does not touch B or its readout.
After the declared relay, B changes. A new readout is still required to
replace its old record.

</details>

**Try a change:** read the old M into B before sending the new value.
Receiving first uses the old message. Event order and the actual copies
matter; the name “channel” supplies no extra operation.

A changed target need not change every probe's mark. Sending value 2
instead of 0 changes B, but an even/odd probe returns 0 for both. The
absence of a record change under one probe does not establish the
absence of a connection.

This model has no measured distance, speed or physical clock. Its
before/after distinction is the declared order of updates. Claims about
a device require a separate correspondence and observations.

Continue with [17. Compare a supplied list of preparations](17_compare_supplied_preparations.md).

AuthorityEffect: None. P200 proves local-record invariance before its
specified relay and supplies a relay divergence example. The book checks
explicit send/receive adapters against those Lean updates, keeping them
separate from the Python helper that constructs its own example states.
