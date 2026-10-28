# 03. Keep the tied answers

[Previous](02_count_the_price.md) · [Search lab](README.md) · [Next: protection](04_protect_a_distinction.md)

## Are six plans six different kinds of answer?

One plan marks A with a one-slot form; another marks B. Swap the two entry
positions, carrying the instance and the required pair with the swap.
The first result becomes the second result's structure.

An **isomorphism** is such a reversible relabeling that preserves the
specified structure. Here it must preserve form arities, instance argument
positions, rules, and required pairs. Presentation-token glyphs are excluded.

We group results when an explicit isomorphism relates them. Each group
is an **isomorphism class**. Its representative stands for the group;
it does not become the only acceptable plan.

| Kind of result | Tied plans in the group | What survives relabeling |
|---|---|---|
| One-slot mark | `F(A)`, `F(B)` | One form with one slot |
| Two-slot loop | `G(A,A)`, `G(B,B)` | Both positions name the same entry |
| Two-slot link | `G(A,B)`, `G(B,A)` | The positions name different entries |

These are three different classes under item-count pricing. A relabeling
cannot turn one slot into two. A reversible relabeling cannot turn a repeated
entry in two positions into two distinct entries.

## Write the witness

For the two mark results, map A to B, B to A, and the sole form to the
sole form. Applying that map to `F(A)` yields `F(B)`. Applying it to the
required unordered pair A/B yields the same required pair.

The executable lab obtains maps with `find_iso` and checks the mapped
structures. It also compares the entire grouping with brute-force
enumeration of all entry/form relabelings in these small cases.

## A different price changes the retained classes

Mu2 retains the two one-slot marks at price `(2, 1)`. They form one class.
“Unique up to isomorphism” here means **one class**, not one literal plan,
and not that a price rule was selected by the seed.

If we permit three-slot forms, the item-count search gains more tied classes.
The arity-two table was exhaustive only within its stated arity bound.

## Your turn

Explain why swapping the two slots of a form is a different proposed
operation from renaming entries. Our isomorphism transports each argument
in place; it supplies no independent slot-permutation operation.

AuthorityEffect: None. The isomorphism relation and price rules are declared.
