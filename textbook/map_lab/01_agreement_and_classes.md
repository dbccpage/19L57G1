# 01. Groups depend on a declared comparison

[Previous](00_follow_a_map.md) · [Map lab](README.md) · [Next](02_choose_a_representative.md)

## Predict first

Keep blue only. Which cards belong together if “together” means they
give exactly the same kept answers?

## An equivalence relation gives consistent groups

The groups are A/B and C/D. The comparison has three useful properties:

- **Reflexive:** each card agrees with itself.
- **Symmetric:** if A agrees with B, B agrees with A.
- **Transitive:** if A agrees with B and B agrees with C, A agrees with C.

A relation with these three properties is an **equivalence relation**.
An **equivalence class** contains precisely the items equivalent to one
of its members. For equality of kept answer patterns, the classes are
also the recording map's **fibers**: the inputs sharing one output.

If we keep both blue and triangle, the four answer patterns differ.
The classes become four single-card groups. We changed the comparison
by making another question available.

## A tempting comparison that fails

Try “agrees on at least one of blue or triangle” instead. A agrees with
B on blue. B agrees with C on triangle. A and C agree on neither.
This relation is not transitive, so chaining these matches does not
justify one class containing all three.

“Every kept question agrees” and “some kept question agrees” define
different relations. The earlier reasoning toolkit matters here.

## Your turn

With no questions kept, all cards have the same empty answer pattern.
How many classes are there on all four cards? How many if the selected
domain is empty? A class requires a member; do not invent an empty class.

AuthorityEffect: None. Exact pattern equality supplies the equivalence laws
in this model; they are not assumed for arbitrary resemblance relations.
