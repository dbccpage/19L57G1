# Claims

AuthorityEffect: None.  Every Lean name below is in the
`ResearchNativeStructure` namespace and is reported in
`lean/ResearchNativeStructure/AxiomReport.lean`.  Each reports only `propext`
and `Quot.sound`, or no axiom.  All statements are about the sealed passage
state `PState`, its step `step`, and the native paths of the
`native_bridge` tree.  Counts dated 2026-09-23.

| Claim | Status | Statement | Evidence |
| --- | --- | --- | --- |
| NS-1 | PROVED_THEOREM | A swap exchanges two adjacent events only where the two orders reach the same state at the actual prefix state. Swap-generated cells relate event lists that replay to the same state and are permutations of each other. | `swap_sound`, `cell_sound`, `cell_perm` |
| NS-2 | PROVED_THEOREM | Cells whisker on both sides and compose horizontally. | `cell_append_right`, `cell_append_left`, `cell_hcomp` |
| NS-3 | PROVED_THEOREM | The sealed license, budget and occurrence frame commutations generate swaps at every state. | `swap_license`, `swap_budget`, `swap_occ` |
| NS-4 | REFUTED | "Parallel native paths are related by a cell." The budget loop and the license loop both run from genesis back to genesis, and no cell relates them. | `parallel_not_cell` |
| NS-5 | PROVED_THEOREM | A proof-relevant cell calculus. A cell is a sequence of verified swap positions, which is data. Vertical composition is strictly unital and associative; whiskering and horizontal composition are defined; interchange holds up to `FarRel`, the declared exchange of adjacent swaps at least two positions apart, and not strictly. The thin quotient is `Cell`. Two cells from genesis with the same endpoints differ and are not `FarRel`-related, and a cell composed with its inverse is not the identity, so this is a category of cells, not a groupoid. (2026-09-24; OPEN until then.) | `CellD.id_vcomp`, `CellD.vcomp_id`, `CellD.vcomp_assoc`, `CellD.inv`, `CellD.whiskerR`, `CellD.whiskerL`, `CellD.hcomp`, `CellD.toCell`, `CellD.sound`, `CellD.interchange`, `FarRel.blocks`, `FarRel.perm`, `cell_iff_nonempty`, `braid_cells_differ`, `vcomp_inv_ne_id` |
| NS-6 | PROVED_THEOREM | Pairing a square's boundary of a boundary with any 0-cochain gives the difference at the square's corners. It vanishes for every 0-cochain exactly when the square commutes. The sealed terminal/license pair has a nonzero boundary. | `boundary_boundary`, `boundary_zero_iff_commutes`, `terminal_square_boundary` |
| NS-7 | PROVED_THEOREM | Path cost is additive over concatenation. An exact cost telescopes to a potential difference and is closed on commuting squares. A closed cost is invariant under cells. A cycle of nonzero cost excludes every potential. | `pathCost_append`, `exact_pathCost`, `exact_closed`, `closed_cell_cost`, `not_exact_of_cycle` |
| NS-8 | PROVED_THEOREM | The budget change is exact, with the budget as its potential. The count of state-changing steps is not exact: the budget loop costs two. | `budgetDelta_exact`, `writes_not_exact` |
| NS-9 | VERIFIED_FINITE | On all 88,338 commuting squares at the 240 states within two steps of the twelve sealed named states, over the 28-event alphabet, both the budget change and the state-change count have zero square boundary. 2,382 squares at those states do not commute. Of the 341 histories of up to four environment writes from genesis, 70 are loops of nonzero state-change count. | `evidence/receipt.json` |
| NS-10 | PROVED_THEOREM | The state-change count is closed: every commuting square has zero boundary. With NS-8 it is a closed cost that is not exact. A writing step is its event's unconditional update under a guard, and on a commuting square no event absorbs the other. (2026-09-24; OPEN until then.) | `step_eq_or_upd`, `refine_map_ne`, `absorb_false`, `writes_closed`, `writes_closed_not_exact` |
| NS-11 | PROVED_THEOREM | Observer descent through the native core: every event except column refinement and column creation maps states with equal cores to states with equal cores. Along an event list without those two events, the end's core is a function of the start's core. | `core_descends`, `path_descends` |
| NS-12 | PROVED_THEOREM | The two funded events do not descend: states with equal cores that differ only in budget (refinement) or only in license (creation) step to different cores. | `refineCol_not_descends`, `addCol_not_descends` |
| NS-13 | VERIFIED_FINITE | Over the 952 states within four steps of the named states, grouped into 262 core classes, 31,467 unfunded same-class steps descend. There are 92 refinement failures and 224 creation failures. | `evidence/receipt.json` |
| NS-14 | PROVED_THEOREM | A declared action renames occurrence tokens. It respects identity and composition, preserves size, and fixes the core outside the occurrence store. For an injective renaming it commutes with the step and with replay, so it is a commuting self-translation of the passage. A cost invariant under the action has invariant path cost. | `actS_id`, `actS_comp`, `step_equivariant`, `size_act`, `core_act_eq`, `replayP_act`, `cost_invariant` |
| NS-15 | REFUTED | "Every renaming commutes with the step." The constant renaming does not. | `needs_injective` |
| NS-16 | VERIFIED_FINITE | On the 952-state battery, a shift and a transposition of tokens produce no equivariance failure, and the constant renaming produces 150. The license frame gives 10,560 commuting squares at the 240 square states. | `evidence/receipt.json` |
| NS-17 | OPEN | A native action that is not declared, for example one read off the state's own automorphisms, and a charge generated by any action. Plan E builds the charge side on a separate carrier. | none |

Lean reach: only the declarations named in `TREE_CONTRACT.json`.  This is
not a census of every compiled constant.
