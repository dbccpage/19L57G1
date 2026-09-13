# Unboundedness Status

AuthorityEffect: None. Outside the sealed derivation; consumes it read-only.

## Terminal verdict

`XSTEP_UNBOUNDED_LEAN; ENGINE_DRIVER_TRAJECTORIES_PYTHON`

An earlier status `UNBOUNDEDNESS_TRAJECTORIES_PROVED` treated Lean and Python as one result. That is WITHDRAWN.

Split:
- Lean: `xstep_unbounded_exists` is a wrapper of ignition's prescribed grow-grow-mark `runState`. Ignition already records that this construction is not a liveness proof for the Python minimum-response, fire-before-growth driver. `engineDriver_refines_xstep` is subset inclusion; unboundedness does not transfer along it, and under `mu2` the driver refuses `markDelta` once a form exists.
- Python: `run_driver_trajectory` under `mu2` with supply enabled was observed to depth 50 with data 17 on both readings, all distinct classes. There is no Lean theorem that `EngineDriver` paths are unbounded.
- Closed: `ClosedRun` bounds sit on `Nodup` and pair-wf; `closed_quiet_terminates` is about `EngineDriver m false` at a quiet state. Every infinite object here is handed in through `supply = true`.

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

4. **Permissive XStep unboundedness** (prescribed block, not the driver):
   - `xstep_runState_data`, `xstep_runState_good`, `xstep_runHist_replays`: The permissive grow-grow-mark sequence `runState r k` reaches data count `r.data + 2 * k` while preserving the `Good` invariant and replaying through sealed steps.
   - `xstep_unbounded_exists`: For each natural number `n`, there exists a regime reachable by replay from any good root with data count at least `r.data + n`. This is not a theorem about `EngineDriver`.

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

8. **Stratified separation cost floor (Lean 4)**:
   - `CostFloor.valid_response_len_pos_of_collapsed`: Every valid response separating a collapsed pair has length at least 1.
   - `CostFloor.valid_response_len_ge_two_at_genesis`: At genesis, when forms, instances, and rules are empty, any valid response requires length at least 2.
   - `CostFloor.separation_cost_floor`: Under both `mu1` and `mu2`, the primary cost component `(cost m δ).1` is bounded below by 2 at genesis and 1 post-genesis.
   - `CostFloor.genesis_mark_cost`, `CostFloor.post_genesis_inst_cost`: Cost bounds are sharp.

9. **Closed system quiet fixpoint theorem (Lean 4)**:
   - `ClosedFixpoint.closed_driver_is_fire`: Under `supply = false`, every engine driver transition is a fire step; growth is refused.
   - `ClosedFixpoint.fire_demand_not_in_reqs`: In a good regime, the demand pair is not already in the requirement store.
   - `ClosedFixpoint.fire_reqs_length_succ`: Each fire step increments the requirement store length by exactly one.
   - `ClosedFixpoint.closed_round_bound`, `closed_round_bound_from_empty`: A `ClosedRun` without external data growth satisfies the quadratic round bound under `Nodup` and ordered in-range pairs. No lemma here shows an `EngineDriver` path is a `ClosedRun`.
   - `ClosedFixpoint.reading_L_max_rounds`, `ClosedFixpoint.reading_F_max_rounds`: any `ClosedRun` with `data = 2` and `reqs = []` has length <= 1; with `data = 3` and `reqs = []` has length <= 3. Names are mnemonic; cite by hypotheses.
   - `ClosedFixpoint.closed_quiet_terminates`: At a quiet state with supply disabled, no engine driver transition exists.

10. **Non-enumerability of the already-infinitary thread space (Lean 4)**:
    - `Continuum.diagonal_bool`: constructive diagonalization on binary sequences.
    - `Continuum.seq_uncountable`: no sequence covers `Nat → Fin c` for any branching alphabet `c ≥ 2`.
    - `Continuum.thread_uncountable`: no `Nat`-indexed family covers `Thread c`. An earlier line said this proved cardinality $2^{\aleph_0}$. That is WITHDRAWN.
    - `Continuum.not_surjective_nat_to_thread`: no map `Nat → Thread c` is surjective.
    - `Continuum.thread_not_agrees_diagonal`: the diagonal thread differs from `T n` at scale $n + 1`.

## What remains open

1. **Continuous interval embedding / quotients**:
   `twins_are_two_threads` refuses one identification. Obtaining real interval $[0, 1]$ or circle $S^1$ geometry requires explicit quotienting of boundary twins (which are currently separated at scale 1).
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
