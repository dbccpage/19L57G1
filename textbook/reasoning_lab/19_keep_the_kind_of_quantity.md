# 19. Keep the kind of quantity

In the previous lesson, X was 6 U with U a **length** standard. Now
someone reports “6 T,” where T is a **duration** standard. The two
records contain the same number. They describe different kinds of quantity.

This model attaches a kind label to each quantity and each standard.
Its four labels are length, duration, count and action. Only length
and duration are needed for the following example. The label “action”
is a supplied category here; it derives no physical law by its name.

| First record | Second record | Requested operation |
|---|---|---|
| 6 length units | 9 length units | Same-kind magnitude ratio |
| 6 length units | 9 duration units | Same-kind magnitude ratio |

**Predict:** should this particular operation accept both rows just
because each has two numbers?

<details><summary>Check your prediction</summary>

No. The second row fails the same-kind condition, so the Python operator
returns a refusal. It does not return zero, guess a conversion or quietly
discard a label. The first row still needs its standards and a nonzero
dividing magnitude checked before calculation.

</details>

A **refusal** says that this requested operation cannot be used under
its stated conditions. It supplies no numerical answer. A ratio of zero
would be an answer to an accepted operation, which is different.

This is not a ban on comparing length and duration in every mathematical
model. A rate such as distance per duration would require an explicitly
defined operation and a resulting kind. P201’s same-kind ratio does not
provide that construction.

**Change one thing:** suppose a record is labelled “length” but its
standard is labelled “duration.” Can a successful calculation prove the
record was assigned the right kind?

<details><summary>Check the changed example</summary>

No. The labels are supplied assumptions, not observations. The teaching
desk rejects that inconsistent record. The native Python dataclass itself
does not enforce this agreement, so the caller must check it. Even
matching labels would not prove the standard is suitable for a real device.

</details>

Lean makes `Quantity length` and `Quantity duration` distinct typed
inputs. The supplied ratio operation expects two quantities of the
same kind. The source theorem that length and duration labels differ
is about these constructors, not a discovery about nature’s categories.

Next: [convert before dividing](20_convert_before_dividing.md).

AuthorityEffect: None. Supplied kind labels and a defined refusal rule.
