# Claims

AuthorityEffect: None.  Every Lean name below is in the
`ResearchDomainAdapters` namespace and is reported in
`lean/ResearchDomainAdapters/AxiomReport.lean`.  Each reports only `propext`
and `Quot.sound`, or no axiom.  Counts dated 2026-09-23.

**Imported and declared structure.**

- *Imported read-only:*
  - the sealed passage step;
  - `native_bridge`'s commuting translations and core;
  - `conservation_ladder`'s integer step;
  - P209b's two-element-field vectors and the matrix `matH`.
- *Declared here:*
  - the monotone counter;
  - the proposal/license event type and its map to native events.

No law of an imported domain is attributed to the sealed seed.

| Claim | Status | Statement | Evidence |
| --- | --- | --- | --- |
| DA-1 | PROVED_THEOREM | Commuting translations compose. An adapter's replay square and observation square hold for every source path. | `Sim.comp`, `comp_enc`, `Adapter.replay_obs` |
| DA-2 | PROVED_THEOREM | If a source step returns to its start in two steps, every translation into the passage gives both states the same core. | `swap_core` |
| DA-3 | PROVED_THEOREM | A monotone counter has a faithful adapter: it maps through occurrence admission to native states whose occurrence count is the counter value, and the encoding is injective on the core. | `counter_comm`, `counter_core_injective` |
| DA-4 | PROVED_THEOREM | The P209b matrix `matH` swaps the two basis vectors and is its own inverse. So every translation of its action into the passage gives both basis vectors the same core, and no translation is injective on the core. | `hStep_twice`, `quantum_core_collapse`, `no_core_faithful_quantum` |
| DA-5 | PROVED_THEOREM | The same action does have a translation with an injective encoding, through budget writes. | `vecCode_injective`, `quantum_budget_adapter` |
| DA-6 | PROVED_THEOREM | The conservation ladder's integer step at coefficient 2 has period four and moves states. Every translation into the passage gives a state and its successor the same core. | `tick_two_period`, `mechanics_moves`, `mechanics_core_collapse` |
| DA-7 | PROVED_THEOREM | Through the proposal/license adapter, a proposal maps to no native event and changes nothing. Application is column creation, and it is inert on a live state without license or without budget. Both gates are the sealed theorems, read through the adapter. | `propose_inert`, `apply_needs_license`, `apply_needs_budget` |
| DA-8 | VERIFIED_FINITE | Over the declared bounds: 32 counter squares with 33 distinct cores; four budget squares for the matrix action, with four encodings and one core; 2,401 pairs of the coefficient-2 step, all of period four and 2,400 moved; on 531 passage states, 1,593 proposals inert and 684 unlicensed or unfunded applications inert. | `evidence/receipt.json`, `tests/test_adapters.py` |
| DA-9 | OPEN | An adapter for a type-theoretic or higher-cell semantics that is not thin. `native_structure`'s cells are a proposition. | none |
| DA-10 | OPEN | An adapter for the smooth tier, and adapters for the operator families outside this repository. None is constructed here, and none is attributed to the seed. | none |

Lean reach: only the declarations named in `TREE_CONTRACT.json`.  This is
not a census of every compiled constant.
