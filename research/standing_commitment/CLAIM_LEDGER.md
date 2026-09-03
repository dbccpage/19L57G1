# Claim ledger — standing_commitment

One evidence class per row. Lean names live in `lean/StandingCommitment/`;
computational evidence is `receipts/standing_commitment.json`.
`AuthorityEffect: None.`

| ID | class | statement | evidence |
|---|---|---|---|
| SC-1 | CONDITIONAL_THEOREM | The represented state and its decidable observation semantics, reconstructed verbatim from the pinned sealed module. | `lean/StandingCommitment/Base.lean`, one source projection checked exact |
| SC-2 | DEFINITION | A standing commitment: a condition on ordered pairs of data, declared once, keeping pairs apart whenever both are held. It emits nothing and reads no state. | `Standing.Commitment` |
| SC-3 | DEFINITION | The demands of a state: pairs of held data the commitment keeps apart that the state does not yet separate. Read off the state, not emitted. | `Standing.demands` |
| SC-4 | DEFINITION | Growth: take in one more datum; nothing else moves. | `Standing.grow` |
| SC-5 | PROVED_THEOREM | Demands read the data and the views and nothing else in the represented state. | `Standing.demands_congr` |
| SC-6 | PROVED_THEOREM | After a growth step the demands are exactly the new datum's pairs followed by those already there. | `Standing.demands_grow` |
| SC-7 | PROVED_THEOREM | Growth loses no demand. | `Standing.demands_persist_under_growth` |
| SC-8 | PROVED_THEOREM | **A fresh datum the commitment keeps apart from something already held produces a demand the old state did not carry, with no act between the growth and the demand.** | `Standing.growth_generates` |
| SC-9 | PROVED_THEOREM | **A discharged state is not a finished state**: one growth step reopens the process, so the fixpoint is not absorbing under growth. | `Standing.fixpoint_reopens` |
| SC-10 | PROVED_THEOREM | Under the total commitment on a viewless state, one growth step adds exactly as many demands as there were data. | `Standing.demand_count_grows` |
| SC-11 | PROVED_THEOREM | Under the empty commitment no sequence of growth steps produces a demand: generation is a property of the declaration, not of growth. | `Standing.empty_commitment_generates_nothing` |
| SC-12 | FINITE_COMPUTATION | The decided accounting instance: three data to six demands to ten, across two growth steps, with one declaration. | `Standing.accounting_instance` |
| SC-13 | FINITE_COMPUTATION | Over four frozen commitments and seven run lengths, the least declared discharge budget that clears the run equals the **peak** per-round generation, in all 28 cases. | `receipts/standing_commitment.json`, `test_the_clearing_budget_is_the_peak_on_the_frozen_family` |
| SC-14 | COUNTERMODEL | That regularity is false in general: a commitment whose generation rises and then stops has peak 3 and clearing budget 1, at every run length tested. Constructed here, after the freeze, and marked as such. | `holds_bounded`, `test_the_bounded_commitment_refutes_that_regularity` |
| SC-15 | FINITE_COMPUTATION | Generation is non-decreasing on exactly the four frozen commitments and not on the post-freeze one — which is why the regularity holds there and fails here. | `test_generation_is_non_decreasing_exactly_on_the_frozen_family` |
| SC-16 | CONJECTURE | A commitment whose demand set has no finite bound outruns any fixed budget; a finite one is cleared by any positive budget. Support: `total` 253 → 1081 on doubling the run; `bounded` 0 at every length. No Lean. | `test_an_unbounded_commitment_outruns_a_fixed_budget`, `test_a_bounded_commitment_does_not` |
| SC-17 | METATHEORY | Discharge is a declared budget, not a derived repair, and a discharged demand is recorded as discharged and never returns. | declared reading 2 in `STATUS.md` |
| SC-18 | OPEN | OB-1 is untouched. The commitment is a parameter of every theorem above and no theorem has it in its conclusion; nothing here produces one. | `OB1_UNCHANGED` |
| SC-19 | REFUSED | That this rung supplies an endogenous demand generator, or narrows the standing obstruction. It changes the accounting, from one external act per demand to one in total, and nothing else. | FW-OB1 |
| SC-20 | OPEN | The four leftovers of `STATUS.md`, executed nowhere. | `STATUS.md` |
