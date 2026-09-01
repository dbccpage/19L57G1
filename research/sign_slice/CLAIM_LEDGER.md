# Claim ledger -- sign_slice

Classifications are exactly one of: DEFINITION, DECLARED_POLICY,
CONDITIONAL_THEOREM (a citation into the pinned sibling packet),
FINITE_COMPUTATION, COUNTERMODEL, OPEN, REFUSED.  No theorem-level
claim originates in this tree; see STATUS.md for the Lean scoping
statement.

| ID | statement | class | evidence |
|---|---|---|---|
| SS-01 | The GenPres grammar is the declared priced tuple, with measure `muG` and a token-forgetting iso key; a weightingless tuple is refused. | DEFINITION | `genpres.py`, `test_weightingless_tuple_is_refused`, receipt `phase_1_grammar` |
| SS-02 | ConeSection is decided by the packet's generator/holonomy criterion, reconstructed and not forked; the phase form is the same predicate. | CONDITIONAL_THEOREM (cited: the packet's `natural_section_iff_generators`, `natural_section_iff_holonomy`, `section_iff_flux_zero`) | `cone_section.py`, receipt `phase_2_predicate` |
| SS-03 | The reconstructed fixtures reproduce the packet's recorded verdicts: chain sectioned; square, star, triangle obstructed. | FINITE_COMPUTATION | `test_chain_is_sectioned_and_square_star_are_not`, receipt `phase_3_census` |
| SS-04 | Twisted equal to total does not imply the section: a declared signed walk list is blind to the square's obstruction. | COUNTERMODEL (computational; the packet's sum-blindness, cited and re-verified) | `test_negative_twisted_equals_total_is_not_sufficient`, receipt key `PB5_sum_blindness_reconstructed` |
| SS-05 | The census: 12 members under the declared bounds, 3 sectioned and 9 obstructed; the six-site occupancy-2 family is refused by the object bound; the completed classification is refused as a terminal. | FINITE_COMPUTATION | `slice_set.py`, `test_partition_matches_the_receipt`, receipt `phase_3_census` |
| SS-06 | The sign pair agrees on ConeSection and is separated by the declared mixing read-out; both facts recorded, neither collapsed into the other. | FINITE_COMPUTATION | `test_sign_pair_agrees_on_the_predicate_and_mixing_separates`, receipt keys `G5`, `phase_3_census` |
| SS-07 | Occurrence-slot relabelling moves the section class within the declared bound: 8192 of 65536 assignments section the two-label square, none of them pointwise-shaped, cheapest at distance exactly 2 from the pointwise family.  The packet's pointwise invariance is reconstructed (64 of 64 unmoved) and not contradicted. | FINITE_COMPUTATION | `occ_relabel.py`, `test_exhaustion_moves_the_square_with_price_two`, `test_witness_is_not_pointwise`, `test_pointwise_relabels_never_move_the_class`, receipt `phase_4_occ_relabel` |
| SS-08 | The obstruction register: one inspectable row per obstructed member, each with a witness walk found within the length bound, read-outs, applicability verdicts, the relabel outcome, and a priced, unexecuted leftover. | FINITE_COMPUTATION | `register.py`, receipt `phase_5_register` |
| SS-09 | Whether the occurrence-relabel finding holds beyond the exhausted member and bound -- and whether any grammar-wide statement about the slot-convention group is true -- is OPEN; promotion requires Lean this tree does not carry. | OPEN | STATUS.md Lean scoping statement |
| SS-10 | The three protected opens are unchanged, and the refusal scans fail the run on supplied vocabulary, working-denylist tokens, sealed writes, or totality sentences. | DECLARED_POLICY | `test_forbidden.py`, receipt `terminals` |
