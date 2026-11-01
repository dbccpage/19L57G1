# 32. What makes a change local?

Start with A1=2, A2=5, B1=7, B2=0. The declared update adds one to
A2 and keeps the other three fields.

**Predict:** what can a reader of B1/B2 see immediately after that update?

<details><summary>Check your prediction</summary>

The full result is 2/6/7/0. B's pair remains 7/0, so any fixed readout
that depends only on that pair returns its previous answer.

</details>

The P203 Lean definition gives an A-update function only A's pair as
input and places its output only into A's two fields. B's pair is kept.
The local-change theorem follows from those actual dependencies. It
holds for every permitted A function, B readout and natural-number state
in that definition, not just the displayed numbers.

Here **local to A** means confined to the declared A part. It does not
mean “nearby” in metres. A **footprint** lists the registers an operation
declares that it reads or writes. That declaration and the actual
function are different objects.

Python checks that keys in a returned update dictionary belong to the
declared write set. It does not inspect every read inside the callback
or verify an observable's stated dependencies. For example, labelling
a readout “B1 only” while actually returning A2 does not make it local
to B. Its answer changes from 5 to 6 in this example.

The desk uses explicit functions that preserve the original record.
The optional source guide also retains a mutation control: the raw
Python dictionary can be changed directly despite its frozen wrapper.
The write-key check alone does not prevent that bypass.

**Change one thing:** after changing A2 to 6, copy A2 into B1.
Does the unchanged-B conclusion still apply to the whole procedure?

<details><summary>Check the changed example</summary>

No. B1 becomes 6. The procedure now includes a write into B.
The original theorem concerns the A-only update before that relay.

</details>

Next: [an available connection and an executed message](33_connection_and_execution.md).

AuthorityEffect: None. Actual functions and declared parts remain explicit.
