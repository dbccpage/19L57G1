# 30. Join records and keep their names

A register is a named place for a value. Supply one part with
`A1 = 2, A2 = 5`, and another with `B1 = 7, B2 = 0`.

**Predict:** what does their combined record contain? Does joining the
records add their numbers together?

<details><summary>Check your prediction</summary>

| A1 | A2 | B1 | B2 |
|---|---|---|---|
| 2 | 5 | 7 | 0 |

All four named values remain. No addition, averaging or physical
interaction has been specified.

</details>

In P203's Python model, **composition** here means merging records
whose register names are disjoint: no name belongs to both parts.
A **projection** keeps only the named part you ask for. Projecting
this combined record onto A1/A2 recovers 2/5; onto B1/B2 recovers 7/0.
Keeping no names gives an empty record, not a record containing zero.

Names matter. If both supplied parts contain `x`, the merge is refused,
even when both assign it 2. The rule does not silently decide whether
the two entries refer to one register or to two different registers.
That identification would need an additional convention.

**Change one thing:** rename A2 to B1 while retaining the other names.
Can the same disjoint-name merge still be performed?

<details><summary>Check the changed example</summary>

No. B1 now occurs in both parts. Giving it a fresh name would make a
different supplied naming arrangement; it would not prove that two
physical places are distinct.

</details>

This route uses a separate supplied P203 model. Its names and field
updates are not derived from the earlier clock rules or the sealed seed.

Next: [regroup without losing a part](31_regroup_without_losing_parts.md).

AuthorityEffect: None. Supplied register records; zero physical observations.
