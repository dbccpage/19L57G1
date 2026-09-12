# Claims: Unboundedness of the mu2 Quotient Tree

AuthorityEffect: None.

| ID | Claim | Evidence | Scope |
|---|---|---|---|
| `CL-UNBOUND-01` | `EngineDriver` transitions refine `XStep` | Lean 4: `Unboundedness.driver_step_refines_xstep` | Declared bounds, `mu1` and `mu2` |
| `CL-UNBOUND-02` | `EngineDriver` transitions preserve the `Good` state invariant | Lean 4: `Unboundedness.driver_step_good` | Valid responses and quiet growths |
| `CL-UNBOUND-03` | Data count is monotonically non-decreasing along driver steps and paths | Lean 4: `driver_data_mono`, `driver_path_data_mono` | All driver trajectories |
| `CL-UNBOUND-04` | Every collapsed pair in a good regime admits an in-bounds valid response | Lean 4: `good_has_inBounds_valid` | Bounds(max_items=2, max_arity=2) |
| `CL-UNBOUND-05` | Permissive `XStep` admits reachable states with data count >= r.data + n at horizon n | Lean 4: `xstep_unbounded_exists` | Rooted runs from good states |
| `CL-UNBOUND-06` | Single-instance responses strictly beat `markDelta` under `mu2` once a form exists | Lean 4: `single_inst_beats_fresh_mark`; Python: `verify_xstep_gap` | Measure `mu2` in context with arity-1 form |
| `CL-UNBOUND-07` | Engine driver trajectories under `mu2` extend to depth >= 50 with data >= 17 without dead ends | Python: `unboundedness.py`, `test_unboundedness.py` | Readings L and F, `mu2` |
| `CL-UNBOUND-08` | Closed runs (`supply=False`) terminate at finite fixpoints (L at depth 1, F at depth 3) | Python: `verify_closed_system_termination` | Sealed closed exports baseline |
| `CL-UNBOUND-09` | Stratified separation cost floor: cost >= 2 at genesis (empty forms), cost >= 1 post-genesis | Lean 4: `CostFloor.separation_cost_floor`, `valid_response_len_ge_two_at_genesis` | All valid responses to collapsed pairs |
| `CL-UNBOUND-10` | Separation cost floor sharpness: mark cost 2 at genesis, single instance cost 1 post-genesis | Lean 4: `CostFloor.genesis_mark_cost`, `post_genesis_inst_cost` | Measures `mu1` and `mu2` |
| `CL-UNBOUND-11` | Under `supply = false`, every engine driver step is an engine fire step | Lean 4: `ClosedFixpoint.closed_driver_is_fire` | Closed system (`supply = false`) |
| `CL-UNBOUND-12` | Closed runs terminate at quiet fixpoints in bounded rounds (L <= 1, F <= 3) | Lean 4: `ClosedFixpoint.reading_L_max_rounds`, `reading_F_max_rounds`, `closed_quiet_terminates` | Reading L and Reading F roots |
| `CL-UNBOUND-13` | Branching thread space is uncountable (cardinality 2^ℵ₀) and Cauchy-complete | Lean 4: `Limits.thread_uncountable`, `Limits.not_surjective_nat_to_thread`, `Metric.limit_converges` | Branching systems (c >= 2) |

## Four-Point Claim Evaluation

1. **What it supports**:
   - Supports that the mu2 quotient tree admits trajectories extending to depth >= n
     with data count >= n for arbitrary tested n under external supply.
   - Supports that every `EngineDriver` transition refines `XStep`.
   - Supports that `(data, len(reqs))` is strictly monotonic, ruling out state repetition.
   - Supports that `markDelta` is non-minimal under `mu2` once an arity-1 form exists.
   - Supports that separation costs satisfy a stratified floor: >= 2 at genesis, >= 1 post-genesis (Rung 1).
   - Supports that closed driver trajectories without supply reach quiet fixpoints in <= binomial(d_0, 2) steps (Rung 2).
   - Supports that under persistent branching (c >= 2), the Cauchy-complete limit path boundary is uncountable (2^ℵ₀) (Rung 3).
2. **What it does not support**:
   - Does not establish real connected interval [0, 1] or circle S^1 manifold geometry (refused without explicit quotients).
   - Does not establish endogenous carrier unboundedness in closed systems without external supply.
   - Does not eliminate the reading underdetermination between L and F.
3. **Narrowest defensible claim**:
   Under measure mu2 with external supply enabled, the engine driver admits infinite non-cycling trajectories along which data count and quotient depth increase without bound; in closed systems without supply, trajectories fixpoint in <= binomial(d_0, 2) rounds; and the resulting branching path limit is an uncountable Cantor-like complete ultrametric space of cardinality 2^ℵ₀.
4. **Next test needed**:
   Evaluate whether quotient branch fan widths remain uniformly bounded or grow with
   carrier size across deeper layers.

