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
| `CL-UNBOUND-07` | Engine driver trajectories under `mu2` extend to depth >= 50 with data >= 17 without dead ends | Python: `unboundedness.py`, `test_unboundedness.py` | Readings L and F, `mu2`; finite tested n; not a Lean theorem about `EngineDriver` |
| `CL-UNBOUND-08` | Closed runs (`supply=False`) terminate at finite fixpoints (L at depth 1, F at depth 3) | Python: `verify_closed_system_termination` | Computational on genesis histories |
| `CL-UNBOUND-09` | Stratified separation cost floor: cost >= 2 at genesis (empty forms), cost >= 1 post-genesis | Lean 4: `CostFloor.separation_cost_floor`, `valid_response_len_ge_two_at_genesis` | All valid responses to collapsed pairs |
| `CL-UNBOUND-10` | Separation cost floor sharpness: mark cost 2 at genesis, single instance cost 1 post-genesis | Lean 4: `CostFloor.genesis_mark_cost`, `post_genesis_inst_cost` | Measures `mu1` and `mu2` |
| `CL-UNBOUND-11` | Under `supply = false`, every engine driver step is an engine fire step | Lean 4: `ClosedFixpoint.closed_driver_is_fire` | Closed system (`supply = false`) |
| `CL-UNBOUND-12` | A `ClosedRun` with `data = 2` and `reqs = []` has length <= 1; with `data = 3` and `reqs = []` has length <= 3 | Lean 4: `ClosedFixpoint.reading_L_max_rounds`, `reading_F_max_rounds`, `closed_quiet_terminates` | Hypotheses as stated; names are mnemonic, not a binding to readings L/F. `closed_round_bound` additionally assumes `Nodup` and ordered in-range pairs; no lemma here shows an `EngineDriver` path is a `ClosedRun` |
| `CL-UNBOUND-13` | For `c ≥ 2`, no `Nat`-indexed family covers `Thread c` | Lean 4: `Continuum.thread_uncountable`, `Continuum.not_surjective_nat_to_thread` | Already-infinitary `Thread c`; non-enumerability, not cardinality $2^{\aleph_0}$. Not entered in `coherent_process_limits/CLAIMS.md`: that path is inside a tree `record_reading` pins |

## Four-Point Claim Evaluation

1. **What it supports**:
   - Supports that the Python `EngineDriver` under mu2 with supply enabled admits
     trajectories extending to depth >= n with data count >= n for the tested n
     (depth 50 / data 17 on both readings).
   - Supports that permissive `XStep` admits arbitrarily large data via a
     prescribed grow-grow-mark block (`xstep_unbounded_exists`). That construction
     is not a liveness proof for the minimum-response driver.
   - Supports that every `EngineDriver` transition refines `XStep` (subset
     inclusion). Unboundedness does not transfer along that refinement.
   - Supports that `(data, len(reqs))` is strictly monotonic, ruling out state repetition.
   - Supports that `markDelta` is non-minimal under `mu2` once an arity-1 form exists.
   - Supports that separation costs satisfy a stratified floor: >= 2 at genesis, >= 1 post-genesis.
   - Supports that a `ClosedRun` without supply is bounded under `Nodup` and
     pair-wf; quiet states admit no `EngineDriver m false` step.
   - Supports that `Thread c` for `c ≥ 2` is not `Nat`-enumerable.
2. **What it does not support**:
   - Does not establish real connected interval [0, 1] or circle S^1 manifold geometry (refused without explicit quotients).
   - Does not establish endogenous carrier unboundedness in closed systems without external supply.
   - Does not eliminate the reading underdetermination between L and F.
   - Does not prove a Lean theorem that `EngineDriver` paths are unbounded.
   - Does not prove `|Thread c| = 2^{\aleph_0}`, a metric completion of the
     finite engine, or an inverse-system universal property of a two-locus run.
3. **Narrowest defensible claim**:
   Closed runs without supply halt. With `supply = true` handed in from
   outside, the Python driver under mu2 was observed to depth 50 with data 17
   on both tested readings; Lean proves unbounded data only for a prescribed
   `XStep` block, not for `EngineDriver`. `Thread c` is non-enumerable because
   it is defined as `Nat → Fin c`. An earlier version of this sentence
   concatenated "infinite engine-driver trajectories" with "an uncountable
   complete ultrametric space of cardinality 2^ℵ₀". That is WITHDRAWN.
4. **Next test needed**:
   Evaluate whether quotient branch fan widths remain uniformly bounded or grow with
   carrier size across deeper layers.

