# FR6 T1–T8 field draft

AuthorityEffect: None. Operator draft for a future author-authored
ledger amendment. Not a gate, not a ledger row, not a claim
registration. Does not amend `paper/paper_claim_ledger.md`.

The sealed ledger at merge-base `ce88c1b48a8de48f194a5189977ec5c4fb62ec08`
already states T1–T8. This file holds the missing field contents
(Deps / Assumptions / Python / Axioms / Falsifier) written from the
cited Lean and from `artifacts/lean_axioms.txt`. Class fields are
unchanged. T2 and T7 still have no Python evidence that covers those
theorems.

Landing these rows in `paper/` requires an author-authored seal
amendment. This draft is not that amendment. The research-tower
snapshot stays at `477a60ff24346ea87b601dd0fffb75b437e46a31`; this
branch does not touch a protected path and does not `--repin`.

An earlier attempt wrote these fields into the sealed ledger
(`665e38c`, `d4cfcfa`) and moved the snapshot onto those commits.
Those commits are not on this branch. A revert-plus-repin would have
advanced the verifier's lower bound past the protected touches; that
is not a repair.

## Assumptions (all eight rows)

The ledger header's word `shared` includes the `CL-TOKEN-ERASURE`
simulation connecting `TRegime`/`TEvent` to `Regime`/`Event`. T1–T8
are stated on different carriers:

| Side | Carriers |
|---|---|
| Lean | `RState` (T1, T2, T6 first clause), `JState` (T4), `PState` (T5 sufficient bridge, T7 bypass), `MState` (T5 minimum route), `Bool` (T8 toggle), `Nat` store codes (T3 Lean half) |
| Python | `Proto` / `FState` (search half of T3, T5, T6 in-class clause, T8 cap) |

No proved simulation maps those FR6 models onto `Regime`/`Event`.
`Assumptions: shared` is therefore not inherited. Each row below
names the FR6 carriers it uses. T3–T6 also name the declared FR6
search bounds (44 protocols, 6-event horizon, carrier cap 4) where
the claim is bounded computation. Those bounds are not the shared
section-1 bounds.

## Proposed fields

Statement and Class remain as in the sealed ledger. The fields below
are the draft fill. Python is cited only where a matching test
exists.

### CL-FR6-T1-INERTIA

- **Deps**: none.
- **Assumptions**: FR6 silent-retention model (`RState` / `REvent` /
  `stepR .silent`). Not `CL-TOKEN-ERASURE`.
- **Python**: `test_silent_protocol_is_inert` (horizon 6, one silent
  protocol; the Lean theorem is horizon-free); `refusal_frontier.json`.
- **Lean**: `RefusalFrontier.silent_repetition_inert`.
- **Axioms**: `propext, Quot.sound`.
- **Falsifier / boundary**: a silent-retention history of already-present
  tokens that changes the object state.  Boundary: every admitted token
  in the history is already in the state's data.

### CL-FR6-T2-TRACE

- **Deps**: none.
- **Assumptions**: FR6 silent-retention model (`RState` / `REvent` /
  `stepTraced` / `replayR .silent`). Not `CL-TOKEN-ERASURE`.
- **Python**: none that covers these theorems.
- **Lean**: `trace_erasure`, `histories_collapse`.
- **Axioms**: `propext, Quot.sound`; `propext, Quot.sound`.
- **Falsifier / boundary**: a traced step whose state projection differs
  from silent replay; or the two listed histories (one vs two
  presentations of token 0) erasing to different object states.
  Boundary: `histories_collapse` is that witness pair, not a universal
  over histories.

### CL-FR6-T3-CONSTRUCTORS

- **Deps**: CL-FR6-T2-TRACE.
- **Assumptions**: Lean half on `Nat × Nat` store codes
  (`storeSwap`). Search half on `Proto` / `FState` under the declared
  FR6 bounds (44 protocols, 6-event horizon, carrier cap 4). Not
  `CL-TOKEN-ERASURE`; not the shared section-1 bounds.
- **Python**: matrix cell `separable_pair -> two_result_constructors`
  refuted (recorded countermodel: the relation route — datum retention
  plus relation rule under a singleton algebra); target-relative
  checks `separable_without_tag_or_relation`,
  `oriented_without_tag_or_relation`,
  `result_distinction_without_binary_algebra`, and
  `witnessed_without_relation_rule` all empty in class
  (`refusal_frontier.json:normal_form.witnessed_without_relation_rule`
  is the relation-channel key).
- **Lean**: `singleton_algebra_monochrome`, `mono_code_swap_invariant`,
  `distinct_code_not_swap_invariant`,
  `distinction_needs_two_constructors`; `histories_collapse` (the
  collapse half, shared with CL-FR6-T2-TRACE).
- **Axioms**: `propext` (`singleton_algebra_monochrome`); none
  (`mono_code_swap_invariant`); none
  (`distinct_code_not_swap_invariant`); none
  (`distinction_needs_two_constructors`); `propext, Quot.sound`
  (`histories_collapse`).
- **Falsifier / boundary**: Lean half (near-definitional): a pair both
  equal to `c` that is not `(c, c)`; `storeSwap (c, c) ≠ (c, c)`;
  `c0 ≠ c1` with `storeSwap (c0, c1) = (c0, c1)`; or `p.1 ≠ p.2` with
  no two distinct codes from `{p.1, p.2}`.  Search half: an in-class
  separable-pair reacher with neither tag nor relation; a result-outcome
  distinction without the binary algebra; or a witnessed-relation
  reacher without the relation rule.  Boundary: the Lean lemmas do not
  carry the channel-search; the three channels are target-relative;
  no interchangeability is claimed.

### CL-FR6-T4-CARRIER

The sealed statement says "refusal-to-carrier per variant". The cited
Lean (`judgment_variant_second_judgment_not_datum`,
`judgment_carrier_bound`) and the matching Python test cover the
**judgment variant only**. Occurrence and datum variants do add
carrier elements; that is a different row. This draft does not
promote the judgment lemmas to a per-variant theorem.

- **Deps**: none.
- **Assumptions**: FR6 judgment variant (`JState` / `stepJ`). Not
  `CL-TOKEN-ERASURE`. The Python test is one judgment protocol at
  horizon 6; the Lean carrier bound is horizon-free on token-0
  histories from `data = []` or `data = [0]`.
- **Python**: `test_judgment_protocol_two_states_only`.
- **Lean**: `judgment_variant_second_judgment_not_datum`,
  `judgment_carrier_bound`.
- **Axioms**: `propext, Quot.sound`; `propext, Quot.sound`.
- **Falsifier / boundary**: the three-step token-0 run
  `stepJ (stepJ (stepJ ⟨[], []⟩ 0) 0) 0` failing
  `data = [0] ∧ judgments = [0, 0]`; or a history of only token 0 from
  a state with `data = []` or `data = [0]` whose carrier is outside
  `{[], [0]}`.  Boundary: a history that admits a token other than 0
  is outside `judgment_carrier_bound`; occurrence and datum variants
  do add carrier elements — that is a different row.

### CL-FR6-T5-BRIDGE

- **Deps**: none.
- **Assumptions**: Lean on `PState` / `stepP` (sufficient route) and
  `MState` / `stepM` (minimum route). Search half on `Proto` /
  `FState` under the declared FR6 bounds (44 protocols, 6-event
  horizon, carrier cap 4). Not `CL-TOKEN-ERASURE`; not the shared
  section-1 bounds.
- **Python**: `test_relation_route_reaches_witnessed_irreflexive`
  (horizon 6, one protocol); `test_witnessed_minimum_unique_under_both_orders`
  (declared 6-event bound).
- **Lean**: `priced_bridge_closes`, `priced_bridge_oriented`,
  `min_witnessed_route_closes`.
- **Axioms**: `propext, Quot.sound`; `propext, Quot.sound`; `propext`.
- **Falsifier / boundary**: `bridgeState` failing the listed
  length/relation/tag facts; `swapP bridgeState = bridgeState`;
  `minState` failing the coproduct-plus-relation facts; or a second
  in-class minimum protocol at a witnessed milestone under either cost
  order.  Boundary: ties at weaker milestones are not this claim;
  `priced_bridge_oriented` is the orientation fact, reused as T7's
  bypass.

### CL-FR6-T6-LAW

- **Deps**: none.
- **Assumptions**: Lean first clause on `PState` / `bridgeState` and
  `PrimDiff.Irrefl`. In-class clause on `Proto` / `FState` under the
  declared FR6 bounds (44 protocols, 6-event horizon, carrier cap 4).
  Not `CL-TOKEN-ERASURE`; not the shared section-1 bounds.
- **Python**: `test_refusal_links_are_born_irreflexive_in_class`
  (exhaustive over the class at the declared 6-event bound — the named
  evidence for the in-class clause).
- **Lean**: `bridge_facts_not_law` (first clause only).
- **Axioms**: `propext, Quot.sound`.
- **Falsifier / boundary**: every extension of the bridge relation being
  irreflexive as a law; or an in-class reachable state with a self-edge.
  Boundary: in-class off-diagonal is a fact of fresh receipts, not the
  irreflexivity law.

### CL-FR6-T7-CEILING

- **Deps**: CL-FR6-T5-BRIDGE.
- **Assumptions**: general lemma is carrier-parametric (`S` / `R` /
  `actS` / `actR` / `F`). Bypass is the one `PState` exemplar
  `bridgeState`. Not `CL-TOKEN-ERASURE`.
- **Python**: none that covers these theorems.
- **Lean**: `equivariant_output_invariant`; bypass
  `priced_bridge_oriented` (the bridge exemplar).
- **Axioms**: none (`equivariant_output_invariant`); `propext, Quot.sound`
  (`priced_bridge_oriented`).
- **Falsifier / boundary**: an equivariant map sending a symmetry-fixed
  state to a non-fixed output; or the priced-bridge state being
  swap-invariant.  Boundary: non-fixedness is the one bridge exemplar,
  not a universal over the class.

### CL-FR6-T8-DYNAMICS

- **Deps**: none.
- **Assumptions**: FR6 reflective models (`stepU`, Boolean toggle,
  `stepRefl`). Not `CL-TOKEN-ERASURE`. The Python test is cap 4 in
  class; the Lean growth theorem is horizon-free.
- **Python**: `test_reflection_grows_to_cap` (cap 4 in class; the Lean
  growth theorem is horizon-free).
- **Lean**: `untyped_reflect_fixpoint`, `toggle_two_cycle`,
  `reflective_chain_growth`, `reflective_chain_is_initial_segment`,
  `reflective_chain_successor_relation`,
  `reflective_chain_irreflexive_facts`.
- **Axioms**: none; none; `propext`; `propext`; `propext`;
  `propext, Quot.sound`.
- **Falsifier / boundary**: `stepU` failing idempotence at depth two;
  the Boolean toggle failing to be a two-cycle; or some n for which n
  reflections do not yield carrier `range (n+1)` with the successor
  relation.  Boundary: the successor shape is declared in `stepRefl`,
  not derived from refusal; initiality (F4) remains open.

## What this file does not do

- It does not close the ledger `KNOWN_*` ratchets. Those measure
  `paper/paper_claim_ledger.md`.
- It does not reclassify mixed Class rows.
- It does not invent Python evidence for T2 or T7.
- It does not rewrite the sealed T4 statement. It records that the
  cited evidence is the judgment variant only.
