# 48. One output table can hide a difference

Supply input 0 and input 1 with equal chances. One box keeps the value;
another flips it.

<details><summary>Predict: which box gives more output zeros?</summary>

Neither. Both give output chances [1/2, 1/2]. Yet their rules differ:

| Given input | Keep | Flip |
|---|---|---|
| 0 | 0 | 1 |
| 1 | 1 | 0 |

Their output chance tables agree for this preparation, while each
conditional row differs. Every paired input/output value changes under flip.

</details>

## Ask which object is being compared

A preparation's output distribution answers how chances are spread
over outputs. A channel's rows answer what happens for each given input.
An actual trial record can retain the paired input and output. These
are three different kinds of data.

For these binary channels, agreeing on both conditional rows makes them
the same channel table. It need not establish identical machinery or
identical procedure histories.

Change the preparation to chance one on 0. Keep outputs 0; Flip outputs 1.
This changed input distinguishes the two supplied channels.

The earlier [share comparison](34_equal_shares_changed_rows.md) makes a
related distinction using finite lists. A list's counted share and a
supplied chance are not automatically interchangeable.

Continue to [49. Process only the stored answer](49_only_the_stored_answer.md).

AuthorityEffect: None. Exact counterexample within supplied binary channels.
