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

## Four-Point Claim Evaluation

1. **What it supports**:
   - Supports that the mu2 quotient tree admits trajectories extending to depth >= n
     with data count >= n for arbitrary tested n under external supply.
   - Supports that every `EngineDriver` transition refines `XStep`.
   - Supports that `(data, len(reqs))` is strictly monotonic, ruling out state repetition.
   - Supports that `markDelta` is non-minimal under `mu2` once an arity-1 form exists.
2. **What it does not support**:
   - Does not establish whole-tree infinite quotient topology or continuum limits.
   - Does not establish behavior under alternative continuation policies or
     unbounded item bounds (> 2).
   - Does not eliminate the reading underdetermination between L and F.
3. **Narrowest defensible claim**:
   Under the declared bounds and measure mu2 with external supply enabled, the engine
   driver admits infinite non-cycling trajectories along which data count and quotient
   tree depth increase without bound; no collapse depth exists for the supply-enabled tree.
4. **Next test needed**:
   Evaluate whether quotient branch fan widths remain uniformly bounded or grow with
   carrier size across deeper layers.
