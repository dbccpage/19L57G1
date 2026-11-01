# 65. Memory has a horizon

[Reasoning lab](README.md) · [Next](66_project_before_permission.md)

Use the [Change lab](../change_lab/README.md),
[Reasoning 56](56_a_claim_needs_an_interpretation.md) and
[59–61](59_change_and_compare.md) first. This continuation
supplies a new model from X303 research outside the sealed derivation.
We offer one candidate at a time; fractional scores are not needed.

## Predict first

Imagine a notebook with two items, A and B, and one possible mark on each.
Initially only A is marked. Give its controller a memory with two slots.
For now, suppose these three steps pass the checks in the next lesson:

| Successful step | Current marked items | Memory, oldest first |
|---|---|---|
| Mark B | A, B | Mark B |
| Erase A | B | Mark B; erase A |
| Erase B | None | ? |

Does the third success require an extra memory slot, or remove the
earliest retained record?

<details><summary>Check your prediction</summary>

The memory retains “erase A; erase B.” Its oldest record, “mark B,”
is removed from this buffer. The current notebook has no marked items.
Those are two different facts about two different parts of the model.

</details>

## Define the limit

The memory's **horizon** is the maximum number of records it retains.
Here the horizon is 2. After appending a record, retain the last two,
keeping their order. This is called **first in, first out**, or FIFO:
when full, the earliest retained record leaves first.

Removing a memory record is called **eviction**. Evicting “mark B” does
not undo that action. The later erase step accounts for B's current
unmarked status. A history summary and a current state have different jobs.

The Python controller appends one memory record after each successful
step. A refused attempt returns a refusal result and receipt but adds
no memory entry. A full memory therefore limits retained successes;
it does not, by itself, forbid further steps.

## What the retained records cannot tell you

After eviction, the two remaining records do not supply this buffer's
entire earlier history. Another archive might retain it, but this model
does not guarantee one. Losing a record is neither proof that its event
never happened nor proof that all copies elsewhere disappeared.

## Your turn

With horizon 1, which record remains after the same three successes?
Does a fourth successful step have to stop because the buffer is full?

Continue to [projection and permission](66_project_before_permission.md).

AuthorityEffect: None. These are supplied notebook operations, not observations.
