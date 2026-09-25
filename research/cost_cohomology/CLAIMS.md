# cost_cohomology: claims

AuthorityEffect: None.

### CL-COST-COHOMOLOGY
- **Statement**: The cycle rank of the depth-3 move multigraph is 378 (232 self-loops + 146 non-self).
- **Evidence**: `test_cost_cohomology.py` (`test_cycle_rank`,
  `test_self_loop_edges_count`, `test_nonself_fundamental_cycles_count`,
  `test_vertex_edge_and_component_counts`), over the graph built by
  `research/path_dependent_cost/movegraph.py`.
- **Falsifier**: finding a different cycle rank or incorrect self-loop count.
- **Dated note (2026-09-24)**: the evidence line read "`verify_rank.py` or
  programmatic test suite".  No `verify_rank.py` has ever existed in this
  repository; `git log --all` finds the name only in the commit that wrote
  this line (`197a150b`).  That citation is withdrawn.  The claim is not
  downgraded, because the other evidence it named, the test suite, exists
  and passes.
