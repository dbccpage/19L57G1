# 06. Return to a real question

A desk receives two grey keys. Both database entries say “grey”. The
clerk declares that record 0 may never be exchanged with record 1.
Has the desk acquired a reliable way to return the correct physical key?

The rule distinguishes the **records under that permission policy**.
It does not yet establish how a physical key remains connected to its
record. A useful application needs that connection: perhaps a tracked
tray position, an attached identifier, or a repeatable measured feature.
Each proposal has its own procedure and possible failures.

Suppose a scanner reports “feature present” for one key and “feature
absent” for the other. That supplies different recorded answers.
We still need to check that the scanner was applied to the intended keys,
that the result is repeatable enough for the job, and that the records
remain associated with the items. Writing different answers is not
evidence that those conditions hold.

Use this sequence on a new problem:

1. Name the actual things and the records representing them.
2. State what information the comparison keeps.
3. State which transformations the rules permit.
4. Separate a changed permission from a changed observation.
5. Identify what observation could reveal a mismatch between the model
   and the situation.

For example, if the desk predicts successful return while a controlled
exchange makes the record-to-key association fail, the application needs
revision. The formal theorem about its declared records need not be
false. The correspondence, procedure, or chosen requirement may have
been inadequate.

Now try the [practice](PRACTICE.md) without opening the answers.
Being able to explain a changed example is more informative about your
understanding than recognizing the familiar diagram.
