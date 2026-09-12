# Unboundedness Status

AuthorityEffect: None. Outside the sealed derivation; consumes it read-only.

## Terminal verdict

`UNBOUNDEDNESS_TRAJECTORIES_PROVED`

Formal Lean 4 derivations in `research/unboundedness/lean/Unboundedness.lean` and deterministic engine simulations in `unboundedness.py` confirm that the mu2 quotient tree admits trajectories extending to depth >= n with data count >= n under external supply. Every transition of `EngineDriver` refines the permissive extension relation `XStep`. State cycling is ruled out by strict lexicographic monotonicity of `(data, len(reqs))`. Whole-tree quotient topology and branch fan width asymptotics remain open.

## What is proved

1. **Refinement of XStep and invariant preservation**:
   - `driver_step_refines_xstep`: Every `EngineDriver` transition refines permissive `XStep`.
   - `driver_step_good`: `EngineDriver` transitions preserve the `Good` state invariant.

2. **Data carrier monotonicity along driver paths**:
   - `stepE_impose_data`: Imposing a pair requirement leaves data count unchanged.
   - `respond_data_mono`: Applying a response delta never decreases data count.
   - `fire_data_mono`: Firing on an unresolved pair demand never decreases data count.
   - `driver_data_mono`: Every `EngineDriver` transition is monotonically non-decreasing in data count.
   - `driver_path_data_mono`: Data count is monotonically non-decreasing along arbitrary driver paths.
   - `quiet_grow_data_succ`: Quiet growth strictly increments data count (`(grow r).data = r.data + 1`).

3. **Response existence within declared bounds**:
   - `good_has_inBounds_valid`: For any pair of distinct admitted data in a `Good` regime, the fresh-mark construction provides an in-bounds valid response within declared bounds (`max_items=2, max_arity=2`).
   - `quiet_state_extends_with_supply`: When external supply is enabled, every quiet regime admits extension by growth.

4. **Permissive XStep unboundedness**:
   - `xstep_runState_data`, `xstep_runState_good`, `xstep_runHist_replays`: The permissive grow-grow-mark sequence `runState r k` reaches data count `r.data + 2 * k` while preserving the `Good` invariant and replaying through sealed steps.
   - `xstep_unbounded_exists`: For each natural number `n`, there exists a regime reachable by replay from any good root with data count at least `r.data + n`.

5. **Carrier distinction**:
   - `data_count_injective`: Regimes with distinct data counts have non-isomorphic carrier sizes.

6. **The mu2 minimum driver cost gap**:
   - `cost_single_inst_mu2`: A single instance of an existing form has lexicographic cost `(1, 0)` under `mu2`.
   - `cost_mark_delta_mu2`: A fresh arity-1 form with an instance has lexicographic cost `(2, 1)` under `mu2`.
   - `single_inst_beats_fresh_mark`: Once an arity-1 form exists, single-instance responses have strictly lower cost than fresh-mark responses under `mu2`.

7. **Computational trajectory execution**:
   - `run_driver_trajectory`: Deterministic engine driver runs under `mu2` with external supply enabled reach depth >= 50 with data count >= 17 on both Reading L and Reading F.
   - All visited states along the deterministic driver trajectory represent mutually distinct canonical isomorphism classes (`all_states_distinct = True`).
   - `terminal_no_response` is absent across all tested depths.
   - `verify_closed_system_termination`: Without external supply (`supply=False`), the driver terminates at finite pair-separation closure fixpoints (Reading L at depth 1 with 2 data, Reading F at depth 3 with 3 data).

## What remains open

1. **Whole-tree quotient topology**:
   The existence of infinite non-cycling paths does not resolve the global topology or continuum limits of the entire mu2 quotient tree across branching alternatives.
2. **Branch fan widths**:
   Whether the branch fan width (number of quotient equivalence classes of valid minimum responses) remains uniformly bounded or grows with carrier size at deep layers remains uncalculated.
3. **Continuation policies and higher bounds**:
   Behavior under continuation policies other than single-datum supply or under item bounds strictly exceeding 2.
4. **Reading underdetermination**:
   The structural divergence between Reading L and Reading F persists along the trajectory without collapsing to a single branch.

## Verification record

- **Lean 4 machine-checked derivations**:
  Compiled via `lake build` in `research/unboundedness/lean/`.
  All 18 declarations in `research/unboundedness/lean/Unboundedness.lean` depend solely on standard core Lean foundations within `{propext, Quot.sound}` (with several declarations axiom-free). Zero unproven axioms (`sorry`) or non-standard assumptions are used.
- **Unit test suite**:
  `python -m unittest research/unboundedness/tests/test_unboundedness.py` executes 4 unit tests covering trajectory progression, state distinction, monotonicity, XStep cost gap, and closed-system termination with exit code 0.
- **Computational verification script**:
  `python research/unboundedness/unboundedness.py` executes full trajectory evaluation and confirms non-cycling depth progression.
