# 35. Symmetry of which object?

Take the graph with separate edges A1—A2 and B1—B2. Swapping the whole
A pair with the B pair preserves its edges. Such a bijective renaming
that preserves the graph's edges is a **graph automorphism**.

Now give the registers values A1=2, A2=0, B1=2, B2=9.

**Predict:** does the graph's symmetry make this full value record
unchanged by the swap? Do identical readouts of A1 and B1 agree?

<details><summary>Check your prediction</summary>

The full record changes: 0 and 9 exchange places. But A1 and B1 both
hold 2, so applying the same probe to either gives the same mark.

</details>

Three objects have distinct symmetry questions:

| Object | What must be preserved? |
|---|---|
| Graph | Points and edges under the bijective renaming |
| Value record | The value at every renamed register |
| Update/readout procedure | Its actual action and requested marks under the corresponding renaming |

Preserving an undirected graph alone does not establish the other two.
For example, reversing a three-edge chain preserves graph distances,
but does not turn its forward copy rules into reverse copy rules.

P203's duplicate-readout Lean theorem needs only equal values at the two
read registers and the same probe. It does not require the entire four-field
record to be symmetric. Its fixed subsystem swap also has explicit
readout-translation equations. Those are separate from a theorem about
arbitrary graph automorphisms preserving arbitrary programs.

### Agreement can hide unequal values

A probe returning only even/odd gives the same answer for 0 and 2.
Equal marks do not then establish equal register values. A probe with
no merged values—an **injective** probe—permits that inference on its
declared domain. Using different probes needs a separate comparison.

**Change one thing:** both registers hold 2, but the second reader
adds one to its answer while the first returns the value. Do marks agree?

<details><summary>Check the changed example</summary>

No: the marks are 2 and 3. The same-probe premise has been removed.

</details>

Next: [make the physical comparison explicit](36_from_parts_to_a_device_claim.md).

AuthorityEffect: None. Separate graph, record and procedure properties.
