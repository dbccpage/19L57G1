# 50. Reset and recovery

Reset sends both possible inputs to 0. A recovery function receiving
only that final 0 would need to give 0 when the original was 0, and 1
when the original was 1. One deterministic function cannot meet both
requests at the same input.

<details><summary>Predict: does a separate retained copy change the answer?</summary>

Yes. If the whole final record is (0, original value), reading its second
component recovers the original. Starting at 0 gives (0, 0); starting
at 1 gives (0, 1). These whole records remain different.

</details>

The two requests supply different final inputs to the recovery function.
Reset of a single component does not imply erasure from every component.
Always state what was retained and what the recovery can read.

## What has been established

For the supplied reset on a carrier with at least two states, no
deterministic recovery from its output alone works on the whole carrier.
On the restricted original domain containing only 0, constant recovery
to 0 does work. The domain matters.

This mathematical obstruction contains no temperature or measured
heat. It establishes no numerical physical erasure cost. Connecting a
memory device to this reset table needs additional definitions and evidence.

Change the final record to (0, 0) for both original values. Explain why
the supposed copy now supplies no recovery of the difference.

Continue to [51. From rows to a device claim](51_from_rows_to_a_device_claim.md).

AuthorityEffect: None. Scoped reset obstruction and explicit retained-copy contrast.
