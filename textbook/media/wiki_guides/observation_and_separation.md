# Observation and internal separation

## Contexts, plugging, and derivability

A **context** is a test with an empty slot. For example, “___ is linked
to datum 1” keeps its second slot fixed and lets us test different data
in the first slot.

Its representation is `(form, slots)`, with at least one slot set to
`None`. Other slots name admitted datum indices. A well-formed context
uses an admitted form, the right number of slots, and valid filled indices.
Plugging a datum fills **every hole with that same datum**.

The implemented `derivable` predicate checks whether an instance is explicitly admitted or its form has an admitted uniform rule. It does not run a hidden theorem prover or import an external interpretation.

## Profiles, collapse, and separation

For datum `d`, `profile(r, d)` collects the contexts that succeed after
plugging in `d`. Two data are **collapsed** when their profiles are equal.
They are **separable** when the profiles differ.

`witness(r, i, j)` returns the first distinguishing context in the declared
enumeration order. It returns `None` when the pair is collapsed. Agreement
of profiles does not equate the admitted datum indices.

## A small example

Admit data `a` and `b`, but no forms. Both have empty profiles. Then admit a unary form and only the instance on datum 0. The one-hole context is derivable on datum 0 and not datum 1, so it witnesses separation.

This example separates three ideas: different presentations, different datum indices, and different observations. None may be silently substituted for another.

## Requirements versus leftover pairs

`collapsed_pairs(r)` reports pairs with equal profiles. `satisfies(r)` checks that every imposed pair has unequal profiles. The first is an observation; the second checks recorded obligations. A host or declared engine policy chooses whether an observed collapsed pair becomes a new demand. The observation function does not authorize that choice.

A uniform all-tuples rule can erase a previously available positive/negative contrast for its form. Do not infer that every extension preserves every possible distinction without the exact preservation hypotheses. Candidate-response validation requires all standing requirements to remain satisfied.

## Observer claims outside the kernel

Research trees study visibility, descent, information, and channels on their own carriers. A common word “observer” does not identify their maps with kernel profiles. A bridge needs a carrier map, observation law, and the appropriate transition or replay law. See [Research atlas](research_atlas) and [Consumer integration](consumer_integration).

Primary source: [observe.py](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/code/derivation/observe.py), with [observation tests](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/tests/test_observe.py).
