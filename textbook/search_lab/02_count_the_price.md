# 02. Count the price

[Previous](01_form_and_instance.md) · [Search lab](README.md) · [Next: tied answers](03_keep_the_ties.md)

## Predict the cheapest repair

One **item** is one proposed addition: a new entry, a new form, a recorded
instance, or the declared all-tuples rule for a form. A **plan**, called a
delta in the code, is a finite collection of such items, applied in the
declared order: entries, forms, rules, instances.

Could a zero-item or one-item plan meet our unmet demand?

## Inspect the whole small search

For the main example, permit at most two items and forms with one or two
slots. The unpruned enumerator lists every well-formed plan in that
declared finite space. A plan is a **valid response** when the result meets
the new demand and every previously imposed separation demand.

| Items in the plan | Well-formed plans | Valid responses |
|---|---:|---:|
| Zero | 1 | 0 |
| One | 3 | 0 |
| Two | 14 | 6 |

The zero-item plan does nothing. The one-item plans add a fresh entry,
a one-slot form, or a two-slot form. None records a distinguishing instance.
An instance or rule cannot stand alone because there is no existing form.

The six successful two-item plans each add one form and one instance:
`F(A)`, `F(B)`, `G(A,A)`, `G(A,B)`, `G(B,A)`, or `G(B,B)`.

## Two declared price rules

**Item count**, called mu1, charges one for each item. All six plans cost two.

**Item count, then slots**, called mu2, first compares item counts. Only
when they tie does it compare the total slots in the newly admitted forms.
Thus the one-slot mark costs `(2, 1)` and a two-slot link costs `(2, 2)`.
The first number is checked first; if it ties, the smaller second number wins.

These are declared price rules. Neither measures money, time, or physical
energy unless a separate application supplies and checks that interpretation.

## Your turn

Explain why the search can stop considering more expensive plans after
finding the least successful item count, while still retaining every plan
tied at that price. Under mu2 it must also compare the second price component.

**Non-example:** keeping the first successful plan would miss equally cheap
alternatives. A sorted list is not permission to discard a tie.

AuthorityEffect: None. These counts are finite calculations. The separate
Lean cost-floor theorem and its broader scope are named in the source map.
