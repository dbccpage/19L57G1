# 33. A connection is not an executed message

Supply copy rules A1→A2 and B1→B2. To draw P203's **interaction graph**,
make each register a point and join each named read to each different
named write. Edges are undirected: they have no arrow in this graph.

```text
A1 — A2       B1 — B2
```

**Predict:** if we add the available rule A2→B1, how many graph edges
form the shortest route from A1 to B2? Has adding the rule executed it?

<details><summary>Check your prediction</summary>

```text
A1 — A2 — B1 — B2
```

The shortest route has three edges. Merely listing the rule has copied
no value. The graph construction executes zero updates.

</details>

**Graph distance** here counts edges on a shortest route. With no route,
the Python result is `None`, meaning unreachable. It is not a measured
length, travel time or speed. The undirected route also does not establish
a reverse copy procedure: a rule copying A2 to B1 need not copy B1 to A2.

The native graph convention also joins two different writes in the same
operation. An operation setting A2=7 and B1=8 therefore adds their edge
even though it copies neither value into the other. Conversely, hiding
an A2 read from a callback's label can make the graph miss that dependency.
The read-label assumption matters.

Now compare actual execution from A2=0, B1=0:

| Procedure | Final A2 | Final B1 |
|---|---|---|
| Add one to A2; then copy A2 to B1 | 1 | 1 |
| Copy A2 to B1; then add one to A2 | 1 | 0 |

The available connection is the same, but order changes what B receives.

**Change one thing:** add the connection but execute only the A2 update.
What is B1 now?

<details><summary>Check the changed example</summary>

B1 remains 0. An available route is not an admission that it was used.

</details>

Try the graph panel of the [composite desk](composites.html).
Next: [equal shares and changed rows](34_equal_shares_changed_rows.md).

AuthorityEffect: None. Declared graph convention and separately executed updates.
