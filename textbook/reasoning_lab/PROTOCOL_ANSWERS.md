# Protocol practice answers

Try [the questions](PROTOCOL_PRACTICE.md) first.

1. The final targets are A=0, B=0. Record A still holds 2; record B
   holds 0. Reading A again replaces its old 2 with 0. The first
   stored mark did not automatically follow the target update.
2. Reading B and advancing A commute: the operations do not change what
   the other reads or writes. Reading A and advancing A fail to commute
   here. Both end at A=0, but reading first leaves record A=2 while
   reading after the advance leaves it 0.
3. No. The records become 2 and 0. The agreement theorem requires the
   same probe for both readouts, as well as equal target values.
4. No. Both parity marks are 0, but the targets are 0 and 2. Copying
   retains this distinction. More generally, an injective probe is
   required to infer equal targets from equal fresh marks under the
   same-probe procedure.
5. Receiving first copies the old M=1 into B. Sending next sets M=2;
   it does not update B again. A new readout stores 1. In the other
   order, send makes M=2, receive makes B=2 and the readout stores 2.
6. Record pairs agree 3 of 3 before advancing A and 0 of 3 afterward.
   B's marks are 2,0,2 in both versions: shares 1/3 at 0 and 2/3 at 2.
   No physical observations were collected; these were supplied rows.

For transfer, an always-zero probe can give matching marks for unequal
targets. Initial zero records can exist before any readout. A configured
instrument can change A while adding zero to the diagnostic counter.
Old records can also survive later target changes. Each refutes a
different missing premise; a single stored number does not encode the
whole procedure history.

For a device, declare what the target and record values stand for, which
operations occur in which order, how probe outputs are read, and what the
counter is configured to register. Preserve actual raw observations and
conditions, and test predictions that could disagree. A theorem about
the supplied model does not establish that correspondence by itself.

AuthorityEffect: None. These are worked answers, not a comprehension or
measurement receipt.
