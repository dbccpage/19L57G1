# Cost Measurements
    
This directory contains tests for fundamental cycle computations on the estate's depth-3 move multigraph.

### Core Properties

The tests verify that on the specific depth-3 move multigraph ($|V|=262$, $|E|=638$):
- The cycle rank of the multigraph is exactly 378.
- This cycle rank decomposes directly into:
  - 232 self-loops (corresponding to repeated instance admissions).
  - 146 non-self fundamental cycles (potential consistency constraints).

This is a direct graph-theoretic computation on the generated state space.
