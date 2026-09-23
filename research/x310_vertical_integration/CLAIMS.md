# Claims: Target X310

## What it supports

1. A six-stage harness that calls sibling research packages.
2. A partial substrate codec: graph, active, clock, fuel, nops, and
   designated pair recover from the encoding. Tape and protection
   obligations are declared metadata.
3. P200 readout/step commutation on a four-state sample.
4. G014 glue on a four-count projection of the supplied pipeline carrier
   after up to two independent X301 additions, when a missing instance or
   requirement exists in the declared probe family. This is not gluing of the full
   relational model.
5. Repeated pipeline runs under a fixed timestamp share a terminal digest.

## What it does not support

1. `T^{-1} o T = id` on full `SubstrateState`.
2. `P o tau = tau o P` for a nontrivial translation.
3. Lean theorems about the Python harness.
4. A 105-check stress harness. None is in this tree.

## Narrowest defensible claim

The harness executes the six sibling entry points under a fixed
`PipelineConfig.timestamp_fixed` and writes a sorted-JSON SHA-256 of the
pipeline receipt.

## Proof obligations before a native bridge claim

Define encode and decode on a stated native state domain, prove both
round trips with all metadata accounted for, and prove transition
commutation for each permitted native event. The current count projection
forgets identities and relations; its successful descent square does not
discharge these obligations or establish a state isomorphism.
