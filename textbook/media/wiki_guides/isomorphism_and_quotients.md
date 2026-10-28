# Isomorphism and quotient search

## The implemented relation

Two regimes may differ only in the names of their indices. To compare
them, try renaming data and forms, then check whether the arities,
instances, rules, and requirements match.

A **bijection** is a renaming that uses every target exactly once. An
**isomorphism witness** supplies the two bijections and the required
preservation checks.

An isomorphism is a pair of bijections: one on datum indices and one on form indices. It preserves form arities and maps instances, uniform rules, and requirements onto the corresponding sets. Requirement pairs are treated without an orientation distinction for that transport. Presentation-token strings are intentionally forgotten.

This is the declared relation used to quotient search branches. It is not “all states that seem similar” and not every possible observer equivalence.

## Canonicalization

A **canonical key** gives each regime a comparison key under the declared
renamings. Search can then retain one representative for matching keys.
The following algorithms compute or check that key within their stated
scope.

`canonical` computes a serialization minimum over color-class-preserving bijection pairs. The refinement colors are intended to be invariant under isomorphism. `canonical_bruteforce` provides a separate minimum over all bijection pairs for finite cross-checks. `find_iso` returns an explicit witness when one is found in its declared search.

The default permutation budget is 100,000. Exceeding a budget is a resource refusal, not an inequality proof. Never turn an unreadable comparison into “not isomorphic.”

## Nodes and edges both need evidence

Quotienting a node does not eliminate the obligation to justify an edge arriving at its stored representative. A merged edge carries datum/form bijections mapping its replayed child onto that representative. A valid creation path for the node cannot excuse a bad merge edge.

```text
parent -- event delta --> replayed child
                              |
                    explicit isomorphism witness
                              |
                              v
                     stored representative
```

The export verifier checks this evidence rather than accepting matching node counts.

## Equivariance of choosing a challenge

Choosing the least raw index pair can depend on a presentation. The engine instead branches over automorphism orbits of collapsed pairs. Its source names a regression for the non-equivariant least-pair policy and an exhaustive transition-congruence cross-check. This is a declared, tested policy, not evidence that all arbitrary selection policies descend to the quotient.

## Formalization ceiling

The Alpha closeout retains `CL-ISO-SOUND` as finite computation with no Lean evidence for that named claim. Other research has scoped isomorphism results, including [Reading F](research_reading_f_iso), [isomorphism soundness](research_iso_sound), and [Lean isomorphism work](research_iso_sound_lean). Their existence does not silently close the closeout's named obligation.

Primary source: [iso.py](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/code/derivation/iso.py). See [exports](artifacts_and_replay) for the independent replay path.
