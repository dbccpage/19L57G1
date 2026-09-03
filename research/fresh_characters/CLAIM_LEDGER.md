# Claim ledger — fresh_characters

Exactly one evidence class per row, from the eleven declared in `PROMPT.md`.
Lean names live in `lean/FreshCharacters/`; computational evidence is
`receipts/fresh_characters.json` and `receipts/tau.yaml`. Every bounded
statement carries its bound in the same row (FW-SCOPE). No row is about the
growth of the running balance (FW-GROWTH).

`AuthorityEffect: None.`

| ID | class | statement | evidence |
|---|---|---|---|
| FC-1 | DEFINITION | The layer of part count `n` has members `0..n-1`; its step action on values is the member multiplied by the step, taken in the part count. | `Char.exponent`, bound to the pinned step law by `Char.exponent_eq_repAdd` |
| FC-2 | DEFINITION | A character of that layer is determined by where it sends the unit member; its carrier-free record is the exponent word. | `Char.IsCharacter`, `Char.exponent` |
| FC-3 | DEFINITION | The fresh total at step `a` sums the character's values over the fresh members; its carrier-free record is the exponent multiset. | `Char.freshExp`, `Char.freshMembers` |
| FC-4 | PROVED_THEOREM | Every step below a positive part count supplies a character; distinct steps give distinct exponent words; and every character agrees on the layer's members with exactly one step's word. Thus the layer has exactly the part count many character words. | `Char.characters_are_steps`, `Char.exponent_is_character`, `Char.exponent_step_injective`, `Char.character_determined_by_unit` |
| FC-5 | PROVED_THEOREM | The fresh total is a function of the receiver element, not of the fresh representation chosen for it. | `Char.freshExp_wf`, resting on the pinned `fresh_rep_unique` |
| FC-6 | PROVED_THEOREM | The step-zero character's fresh total is the fresh count many copies of the carrier's distinguished element. | `Char.freshExp_zero` |
| FC-7 | PROVED_THEOREM | Whatever the step, the fresh total has exactly the fresh count many terms. | `Char.freshExp_length` |
| FC-8 | PROVED_THEOREM | Along a divisor arrow, a character of the larger layer restricts to the corresponding character of the smaller, scaled by the arrow. | `Char.exponent_embed` |
| FC-9 | PROVED_THEOREM | In a carrier whose character values are ADDED, the step-zero total is the carrier's zero and not the fresh count whenever the layer has a fresh member. This is the recorded obstruction of menu member V1. | `Char.additive_step_zero_total`, `Char.additive_trivial_total_ne_freshCount` |
| FC-10 | DEFINITION | The fresh part of a layer is defined by the same divisor recursion the pinned balance uses: the layer's own difference divided by the fresh parts of every proper divisor layer. | `FreshPart.freshPart`, `FreshPart.layerDiff`; Python `characters.fresh_part` |
| FC-11 | FINITE_COMPUTATION | Under the fresh-part quotient carrier, every fresh total reduces to a plain integer, at every part count `1..20` and every step. | `FreshPart.total_is_constant_to_20`, kernel-decided |
| FC-12 | FINITE_COMPUTATION | Under that carrier the unit-step fresh total is the pinned balance, at every part count `1..20`. | `FreshPart.total_unit_step_is_balance_to_20`, kernel-decided |
| FC-13 | FINITE_COMPUTATION | Under that carrier the zero-step fresh total is the pinned fresh count, at every part count `1..20`. | `FreshPart.total_zero_step_is_freshCount_to_20`, kernel-decided |
| FC-14 | FINITE_COMPUTATION | Exactly two of the twenty-four declared pairs make the fresh total the balance at every part count `1..60`: the fresh-part carrier at the unit step and at the step one below the part count. Ties retained; neither is called the carrier. | `receipts/fresh_characters.json` key `stage_2_total_identity.search`; `test_the_menu_has_twenty_four_pairs_and_exactly_the_two_hits` |
| FC-15 | FINITE_COMPUTATION | Both pairs still agree with the balance at every part count `1..600` by direct recomputation. | `stage_2_total_identity.cross_check`; `test_the_hits_agree_with_the_balance_past_the_search_bound` |
| FC-16 | FINITE_COMPUTATION | The pinned running-balance checkpoints at `10, 30, 100, 1000, 10000, 100000, 1000000` are reproduced exactly from the balance recursion; `0` misses. | `stage_2_total_identity.cross_check.checkpoints`; `test_the_pinned_checkpoints_are_reproduced` |
| FC-17 | CONJECTURE | The two identities of FC-14 hold at every part count, not only within the bounds reached. Support: exhaustive to `60`, direct to `600`, kernel-decided to `20`. Proved nowhere. | none; the price is in `STATUS.md` |
| FC-18 | FINITE_COMPUTATION | The divisor sum of the totals is the part count at the zero step and vanishes at every other step, for the fresh-part carrier over the whole rectangle to `60`, and kernel-decided to `16`. At the unit step and a part count above one this reproduces the pinned `balance_divisor_sum`, checked. | `FreshPart.divisor_recursion_to_16`; `stage_3_divisor_recursion` |
| FC-19 | FINITE_COMPUTATION | The totals depend on the step only through the largest divisor the step shares with the part count, over the rectangle to `60` and kernel-decided to `20`. | `FreshPart.total_depends_on_shared_divisor_to_20`; `stage_3_divisor_recursion` |
| FC-20 | CONDITIONAL_THEOREM | The cancellation-certificate criterion is per-magnitude domination. Cited into the pinned packet and reconstructed here as computation, cross-checked against a brute-force search for a pairing into exact opposites plus a single-signed residual; `0` disagreements on the rectangle and on every list over `{-2..2}` of length `5`. | pinned `certificate_iff_dominated`; `magnitude_census.certificate_decision`; `test_the_criterion_matches_a_brute_force_search` |
| FC-21 | FINITE_COMPUTATION | At the level of the terms of a single total, every one of the 2760 families in the rectangle carries exactly one magnitude. LP4 is carried forward unchanged for that family kind. | `stage_4_magnitude_census.term_family_kind` |
| FC-22 | FINITE_COMPUTATION | At the level of the rows — the totals at every step of one layer — 54 of the 150 families in the rectangle carry two or more magnitudes, and 25 distinct magnitudes appear. The smallest diverse family is at part count `3`. LP4 has moved for that family kind. | `stage_4_magnitude_census.row_family_kind` |
| FC-23 | FINITE_COMPUTATION | 29 row families in the rectangle admit NO cancellation certificate. The smallest is at part count `3`, terms `[2, -1, -1]`, total `0`: it cancels, and no pairing into exact opposites plus a single-signed residual exists. | `stage_4_magnitude_census.row_family_kind.smallest_refusal_witness`; `test_the_smallest_refusing_row_is_the_recorded_one` |
| FC-24 | FINITE_COMPUTATION | Within the rectangle, every refusing row family sits at an odd part count, and no even part count refuses. Recorded as an observation of the rectangle; nothing is claimed outside it. | `stage_4_magnitude_census.refusal_part_counts` |
| FC-25 | FINITE_COMPUTATION | Every row family of the fresh-part carrier above part count one totals to zero. | `test_every_row_family_of_the_hit_carrier_totals_to_zero_above_one` |
| FC-26 | METATHEORY | Division of an integer combination by a monic divisor stays in the integers, which is why the fresh parts and the reductions need no denominators. | `characters.pdivmod`, `FreshPart.pdivmod`; `test_division_by_a_monic_divisor_is_exact_where_it_should_be` |
| FC-27 | FINITE_COMPUTATION | The fresh parts of the divisor layers multiply back to the layer's own difference, and the fresh part's degree is the fresh count, at every part count `1..60`. | `test_the_fresh_parts_multiply_back_to_the_layer_difference`, `test_the_fresh_part_has_the_fresh_count_as_its_degree` |
| FC-28 | REFUSED | That the six-member menu is the set of value carriers, or that the rectangle is the set of families. Both are declared and finite. | FW-SET |
| FC-29 | OPEN | The growth of the running balance, in either direction. Untouched by this run. | FW-GROWTH; `NS95_GROWTH_UNCHANGED` |
| FC-30 | OPEN | The four leftovers and the next rung, named and priced in `STATUS.md`, executed nowhere. | `stage_5_register.leftovers` |
