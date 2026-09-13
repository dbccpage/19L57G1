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

### (c) Engine driver: Lean refinement, Python trajectories
1. **Lean, conditional**: At any `Good` state, `quiet_state_extends_with_supply`
   and `good_has_inBounds_valid` are existence lemmas. `engineDriver_refines_xstep`
   is subset inclusion into `XStep`. They do not prove arbitrarily long
   `EngineDriver` paths.
2. **Cycle exclusion on a step**: Data count is non-decreasing along every driver
   step (`driver_data_mono`). Quiet growth strictly increases data
   (`quiet_grow_data_succ`).
3. **Python trajectories**:
   The deterministic engine trajectory under `mu2` with `supply=True` on
   readings L and F was observed to depth 50 with data 17, all distinct classes,
   no `terminal_no_response`. That is a finite tested n, not a Lean unboundedness
   theorem for the driver.
4. **Closed system termination**:
   With `supply=False`, the Python driver on genesis L terminates at depth 1
   (2 data) and genesis F at depth 3 (3 data). External supply is what sustains
   carrier expansion. Lean `ClosedRun` bounds are a different carrier.

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
- `ClosedFixpoint.closed_round_bound`: a `ClosedRun` on carrier d satisfies `2 * (r.reqs.length + rds.length) <= d * (d - 1)` under `Nodup` and ordered in-range pairs.
- `ClosedFixpoint.reading_L_max_rounds`, `ClosedFixpoint.reading_F_max_rounds`: any `ClosedRun` with `data = 2` and `reqs = []` has length <= 1; with `data = 3` and `reqs = []` has length <= 3. Cite by hypotheses.
- `ClosedFixpoint.closed_quiet_terminates`: Quiet states admit no further transitions under `supply = false`.

### (f) Non-enumerability of the already-infinitary thread space (Lean 4: Continuum.lean)
`research/unboundedness/lean/Continuum.lean` proves that `Thread c` for `c ≥ 2`
is not `Nat`-enumerable. `Thread c` is defined as a compatible family over every
scale `n : Nat` and is `Nat → Fin c`. An earlier paragraph called this
"Rung 3 of the finite-to-continuum convergence ladder" and asserted cardinality
$2^{\aleph_0}$. Both are WITHDRAWN.
- `Continuum.diagonal_bool`: diagonal argument on binary sequences.
- `Continuum.seq_uncountable`: for $c \ge 2$, no sequence covers `Nat → Fin c`.
- `Continuum.thread_uncountable`: no sequence covers `Thread c`.
- `Continuum.not_surjective_nat_to_thread`: no function `Nat → Thread c` is surjective.
- `Continuum.thread_not_agrees_diagonal`: the diagonal thread differs from `T(n)` at scale $n + 1`.

## 3. Four-Point Claim Evaluation

1. **What it supports**:
   - Supports that the Python driver under mu2 with supply enabled was observed
     to depth >= n with data >= n for the tested n.
   - Supports that every `EngineDriver` transition refines `XStep`.
   - Supports that `(data, len(reqs))` is strictly monotonic, ruling out state repetition.
   - Supports that `markDelta` is non-minimal under `mu2` once an arity-1 form exists.
   - Supports that separation costs satisfy a stratified floor: $\ge 2$ at genesis, $\ge 1$ post-genesis.
   - Supports that a `ClosedRun` without supply is bounded under stated side conditions.
   - Supports that `Thread c` for $c \ge 2$ is not `Nat`-enumerable.
2. **What it does not support**:
   - Does not establish real connected interval $[0, 1]$ or circle $S^1$ manifold geometry (refused without explicit quotients).
   - Does not establish endogenous carrier unboundedness in closed systems without external supply.
   - Does not eliminate the reading underdetermination between L and F.
   - Does not prove a Lean theorem that `EngineDriver` paths are unbounded, nor cardinality $2^{\aleph_0}$.
3. **Narrowest defensible claim**:
   Closed runs without supply halt. With `supply = true` handed in from
   outside, the Python driver under mu2 was observed to a finite tested depth;
   Lean proves unbounded data only for a prescribed `XStep` block. `Thread c`
   is non-enumerable because it is defined as `Nat → Fin c`. An earlier
   sentence here claimed infinite driver trajectories and a complete
   ultrametric space of cardinality $2^{\aleph_0}$. That is WITHDRAWN.
4. **Next test needed**:
   Evaluate whether quotient branch fan widths remain uniformly bounded or grow with
   carrier size across deeper layers.
