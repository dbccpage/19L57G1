# 34. Equal shares can hide changed rows

Supply two equally weighted records. Read B1, then flip its binary value:
0 becomes 1 and 1 becomes 0.

| Row | Before B1 | After B1 |
|---|---|---|
| First | 0 | 1 |
| Second | 1 | 0 |

**Predict:** has each row kept its reading? Have the overall shares of
0 and 1 changed?

<details><summary>Check your prediction</summary>

Both rows change. But each list still contains one 0 and one 1: each
mark's share remains one-half. Keeping shares is weaker than keeping
the corresponding reading on every row.

</details>

A **marginal distribution** here is a table of shares for the selected
readout, ignoring the other fields. Repeated preparation rows still count
separately. These are supplied equal weights, not measured frequencies.

To compare two such tables, find the size of the share difference for
each mark, add those sizes and divide by two. This **total variation
distance** is zero exactly when all those shares agree. For the two lists
above it is zero, despite both paired readings changing.

The local-update theorem is stronger in a particular way: it keeps
each B reading unchanged before a relay. Applying that same update
to a retained list then keeps its shares too. A zero distance on one
list does not prove the converse or establish every possible readout.

A readout that always returns zero hides every B1 change. A coarse
readout can likewise hide some changes. A write into B therefore does
not guarantee a positive distance for every preparation and readout.

**Change one thing:** supply `[0,0,0,1]` and flip every entry. What is
the distance now?

<details><summary>Check the changed example</summary>

The lists have shares `(3/4,1/4)` and `(1/4,3/4)` for marks 0/1.
Each difference has size 1/2. Their sum is 1; dividing by two gives 1/2.
All four paired readings change.

</details>

Use the [composite desk](composites.html) to compare the paired records
with the share tables. Next: [symmetry of which object?](35_symmetry_of_which_object.md).

AuthorityEffect: None. Exact shares of supplied finite lists; zero device observations.
