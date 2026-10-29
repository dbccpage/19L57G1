# 06. Keep the convention visible

[Previous](05_join_two_faces.md) · [Path lab](README.md) · [Practice](PRACTICE.md)

## Predict first

Suppose someone checks a repeated-vertex list A, A, B and finds that its
double boundary cancels. Must it be a valid admitted triangular face?

## A true calculation can be weaker than a valid representation

No. A, A, B fails the strict increasing-order guard. It repeats a vertex.
The boundary formula can still be evaluated on that raw list, and the
source's cancellation theorem still applies to it. Cancellation by itself
does not establish that the list describes a well-formed admitted cell.

The native theorem proves double-boundary cancellation for every finite
vertex list, including repeated entries. Increasing order instead ensures
that deleting different positions gives different facets. Those are
different properties with different hypotheses.

## The signs matter

If every deletion were counted positively, the second boundary of ABC
would give +2 at each vertex. Under the alternating signed convention
the second boundary is zero. This comparison explains which rule carries
the cancellation; a complete outline alone does not choose the signs.

Do not confuse this all-positive deletion rule with keeping the signed
edge-boundary rule but changing just one edge's coefficient in Lesson 04.
Those are two different changes and give different endpoint counts.

## What we can take into an application

We can ask which connections a model records, which routes it allows,
what its signed tally keeps, and what additional record a face requires.
Before treating a drawing as a model of a device or a physical region,
state and test what its vertices, connections, signs, and measurements mean.

The placed points and exact counts here supply no measurement of space,
no claim about travel time, and no general law about physical boundaries.

## Your turn

Give one example where a zero count coexists with a nonempty record,
and one where a zero double boundary coexists with a failed cell guard.

AuthorityEffect: None. The actual source theorems retain their stated
definitions; these teaching pictures supply no automatic model transport.
