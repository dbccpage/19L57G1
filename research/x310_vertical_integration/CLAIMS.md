# Claims: Target X310

## What it supports

1. A six-stage harness that calls sibling research packages.
2. A partial substrate codec: graph, active, clock, fuel, nops, and
   designated pair recover from the encoding. Tape and protection
   obligations are declared metadata.
3. P200 readout/step commutation on a four-state sample.
4. G014 glue on a synthetic four-locus carrier, not the live pipeline
   carrier.
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
