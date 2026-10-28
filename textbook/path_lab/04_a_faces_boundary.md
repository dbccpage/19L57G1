# 04. Take a face's boundary

[Previous](03_closed_and_filled.md) · [Path lab](README.md) · [Next](05_join_two_faces.md)

## Predict first

The boundary route of ABC runs A → B → C → A. Relative to the reference
arrows A → B, B → C, A → C, which edge is used backwards?

## Choose a reference direction

Use the increasing vertex order A, B, C, D. Each edge's **reference
direction** goes from its earlier vertex to its later one. A positive
edge count follows that arrow; a negative edge count reverses it.

The chosen boundary of ABC is:

**+AB +BC −AC.**

The −AC term goes from C back to A. A minus sign here does not remove
the stored edge AC or assign it a negative physical length.

The source computes this rule by deleting vertices in order and giving
the resulting facets alternating signs: +, −, +. Deleting A gives +BC;
deleting B gives −AC; deleting C gives +AB. We supplied that convention.

## Take the boundary again

An edge contributes −1 at its starting point and +1 at its end. Reversing
its sign reverses both contributions:

| Signed edge | Endpoint contributions |
|---|---|
| +AB | −A +B |
| +BC | −B +C |
| −AC | +A −C |

Every vertex gets one positive and one negative contribution. They cancel.
Thus the boundary of this face's boundary is zero at every vertex.
We have accounted for all six contributions, not assumed the result
because the picture looks closed.

## Your turn

Replace −AC with +AC while leaving the other terms positive. What is the
endpoint count at A? At C? This changed convention does not cancel.

AuthorityEffect: None. The general source theorem concerns its declared
integer boundary formula; the face-admission rule does not force these signs.
