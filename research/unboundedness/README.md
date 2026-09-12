# Unboundedness of the mu2 Quotient Tree and Engine Driver Analysis

AuthorityEffect: None. Outside the sealed derivation; consumes it read-only.

## 1. Scope and Objective

This research package investigates the unboundedness question for the mu2
quotient tree (Target 1; paper section 12, line 800, tagged `[unresolved — kind (d)]`).

The investigation addresses:
1. Whether for each n in Nat, there exists a regime reachable at depth >= n in
   the mu2 quotient tree with data count >= n, or an obstruction / collapse depth.
2. The grow-grow-mark block construction (`runHist_replays`, `runState_data`)
   in `research/ignition`, which operates under permissive `XStep`.
3. The structural gap between permissive `XStep` and the engine's
   minimum-response driver under measure `mu2`.
4. Formal Lean 4 theorems in `research/unboundedness/lean/Unboundedness.lean`
   and computational verification in `unboundedness.py`.

## 2. Key Findings

### (a) Permissive XStep Unboundedness (Lean 4)
In `research/ignition`, the grow-grow-mark block sequence `runState r k` satisfies:
- `(runState r k).data = r.data + 2 * k` (`xstep_runState_data`)
- `Good (runState r k)` (`xstep_runState_good`)
- `replayE (runHist r k) r = some (runState r k)` (`xstep_runHist_replays`)
At each horizon step `k = n`, data count reaches `r.data + 2 * n >= r.data + n`,
and the history length is `7 * n >= n`. This exhibits unbounded reachable states
under the permissive `XStep` relation (`xstep_unbounded_exists`).

### (b) The Gap Between XStep and the Engine Driver under mu2
The grow-grow-mark block uses `markDelta r = [.newForm 1, .newInst r.forms.length [r.data + 1]]`.
Under measure `mu2`, `markDelta r` has cost `(2, 1)`.
- At the initial block from a root with zero forms, no 1-item response exists, so
  `markDelta` is a minimum response (`cost = (2, 1)`).
- At all subsequent blocks (`k >= 1`), form 0 already exists in the regime.
  Adding a single instance of form 0 costs `(1, 0)` under `mu2`.
- Since `(1, 0) < (2, 1)` in lexicographic order (`single_inst_beats_fresh_mark`),
  the engine's minimum driver will not select `markDelta` when an existing form serves.
- Furthermore, the engine driver enforces a fire-before-growth discipline:
  growth (`grow r`) is permitted only when `Quiet r` holds (every admitted pair
  separated). The driver does not perform grow-grow-mark blocks; it intersperses
  single-instance responses (`cost = (1, 0)`) until all standing pairs are
  separated, then admits a single fresh datum.

### (c) Engine Driver Liveness and Unbounded Trajectories (Python & Lean 4)
1. **Liveness**: At any `Good` state:
   - If `Quiet r`, the engine executes `grow r` (`quiet_state_extends_with_supply`).
   - If a collapsed pair exists, `good_has_inBounds_valid` confirms that an
     in-bounds valid response exists. The minimum response search over the finite
     candidate space never returns empty; `terminal_no_response` is absent.
2. **Cycle Exclusion**: Data count is non-decreasing along every step
   (`driver_data_mono`, `driver_path_data_mono`). On a fixed data carrier `d`,
   firings add pairs to `reqs` without duplicates, bounded by `d * (d - 1) / 2`
   (`closedRun_round_bound`). Once all pairs are separated, the state is quiet,
   forcing `grow r`, which strictly increases data count (`quiet_grow_data_succ`).
   Hence `(data, len(reqs))` strictly increases lexicographically, excluding cycles.
3. **Computational Evidence**:
   Executing the exact deterministic engine trajectory under `mu2` with `supply=True`
   on Reading L and Reading F:
   - Reaches depth 50 with data count 17.
   - All 51 visited nodes belong to distinct isomorphism classes (`all_states_distinct = True`).
   - Reaches depth 60 with data count 19.
   - Zero terminal refusals encountered.
4. **Closed System Termination**:
   With `supply=False`, Reading L terminates at depth 1 (2 data) and Reading F
   terminates at depth 3 (3 data), confirming that external supply is what sustains
   carrier expansion.

### (d) Stratified Separation Cost Floor (Lean 4: CostFloor.lean)
The cost to separate a collapsed pair is stratified:
- `CostFloor.valid_response_len_pos_of_collapsed`: Length >= 1 for every valid response.
- `CostFloor.valid_response_len_ge_two_at_genesis`: Length >= 2 at genesis when forms, instances, and rules are empty.
- `CostFloor.separation_cost_floor`: Under both `mu1` and `mu2`, `(cost m δ).1` is >= 2 at genesis and >= 1 post-genesis.
- `CostFloor.genesis_mark_cost`, `CostFloor.post_genesis_inst_cost`: The bounds are attained.

### (e) Closed-System Quiet Fixpoint Theorem (Lean 4: ClosedFixpoint.lean)
Without external supply (`supply = false`), the driver cannot grow and terminates in bounded depth:
- `ClosedFixpoint.closed_driver_is_fire`: Every transition is an engine fire step; growth is refused.
- `ClosedFixpoint.fire_demand_not_in_reqs`, `ClosedFixpoint.fire_reqs_length_succ`: Each step consumes an unseparated pair without replacement.
- `ClosedFixpoint.closed_round_bound`: Closed runs on carrier d satisfy `2 * (r.reqs.length + rds.length) <= d * (d - 1)`.
- `ClosedFixpoint.reading_L_max_rounds`, `ClosedFixpoint.reading_F_max_rounds`: Reading L terminates in <= 1 round; Reading F terminates in <= 3 rounds.
- `ClosedFixpoint.closed_quiet_terminates`: Quiet states admit no further transitions under `supply = false`.

### (f) Limit Path Space Uncountability and Continuum Cardinality (Lean 4: Continuum.lean)
Rung 3 of the finite-to-continuum convergence ladder is mechanized in `research/coherent_process_limits/lean/Continuum.lean`:
- `Limits.cantor_diagonal_bool`: Constructive diagonal argument on binary sequences.
- `Limits.seq_uncountable`: For any branching alphabet $c \ge 2$, no sequence covers `Nat → Fin c`.
- `Limits.thread_uncountable`: No sequence covers `Thread c`; the limit space has cardinality $2^{\aleph_0}$.
- `Limits.not_surjective_nat_to_thread`: No function from `Nat` to `Thread c` is surjective.
- `Limits.thread_not_agrees_diagonal`: The diagonal thread differs from candidate thread $T(n)$ at scale $n + 1$.
Coupled with `Metric.limit_converges` (Cauchy completeness) and `Limits.twins_are_two_threads` (refusal of interval identification), the limit path boundary of the branching tree is a complete, totally disconnected Cantor-like metric space of continuum cardinality $2^{\aleph_0}$.

## 3. Four-Point Claim Evaluation

1. **What it supports**:
   - Supports that the mu2 quotient tree admits trajectories extending to depth >= n
     with data count >= n for arbitrary tested n under external supply.
   - Supports that every `EngineDriver` transition refines `XStep`.
   - Supports that `(data, len(reqs))` is strictly monotonic, ruling out state repetition.
   - Supports that `markDelta` is non-minimal under `mu2` once an arity-1 form exists.
   - Supports that separation costs satisfy a stratified floor: $\ge 2$ at genesis, $\ge 1$ post-genesis (Rung 1).
   - Supports that closed driver trajectories without supply reach quiet fixpoints in $\le \binom{d_0}{2}$ steps (Rung 2).
   - Supports that under persistent branching ($c \ge 2$), the Cauchy-complete limit path boundary is uncountable ($2^{\aleph_0}$) (Rung 3).
2. **What it does not support**:
   - Does not establish real connected interval $[0, 1]$ or circle $S^1$ manifold geometry (refused without explicit quotients).
   - Does not establish endogenous carrier unboundedness in closed systems without external supply.
   - Does not eliminate the reading underdetermination between L and F.
3. **Narrowest defensible claim**:
   Under measure mu2 with external supply enabled, the engine driver admits infinite non-cycling trajectories along which data count and quotient depth increase without bound; in closed systems without supply, trajectories fixpoint in $\le \binom{d_0}{2}$ rounds; and the resulting branching path limit is an uncountable Cantor-like complete ultrametric space of cardinality $2^{\aleph_0}$.
4. **Next test needed**:
   Evaluate whether quotient branch fan widths remain uniformly bounded or grow with
   carrier size across deeper layers.
