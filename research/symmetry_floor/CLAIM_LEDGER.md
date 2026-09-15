# Claim ledger — symmetry_floor

`AuthorityEffect: None.` Every claim carries its evidence class and the name
that decides it. A claim with no decider is not in this table.

Evidence classes used here: **theorem** (Lean, axiom report recorded),
**exhaustion** (every member of a declared finite space enumerated),
**computation** (deterministic Python over a declared bound), **open**.

---

## Theorem-level

| id | claim | class | evidence |
| --- | --- | --- | --- |
| SF-1 | A rule computed from the state alone cannot break a renaming the state already holds still. | theorem | `lean/SymmetryFloor.lean::floor` — **no axioms** |
| SF-2 | The same holds for any finite number of applications of the rule. | theorem | `lean/SymmetryFloor.lean::floor_iterated` — **no axioms** |
| SF-3 | SF-1 assumes nothing about `G`, `act` or `X`: not a group, not an action, not this carrier. A change of start cannot evade it. | theorem | the statement of `floor`; its binders are the evidence |
| SF-4 | Once the step offers a set, the set may be carried to itself while no member is. | theorem | `offered_set_carried`, `members_move` — `propext` |
| SF-5 | A one-member offer cannot break a renaming; two is the least that can. | theorem | `price_is_two` — `propext`; and SF-1 for the one-member case |

## Exhaustion

| id | claim | class | evidence |
| --- | --- | --- | --- |
| SF-6 | Held-set containment is necessary **and sufficient** for a rule to carry one inscription to another: it is the complete description of what a state-read rule may do. | exhaustion | `test_containment_is_necessary_and_sufficient` — 30,625 pairs, 0 disagreements |
| SF-7 | Over a closed carrier of 8 inscriptions, exactly 128 of all 16,777,216 maps agree with the renamings, matching the characterisation. | exhaustion | `test_exhaustion_over_every_map` — counted by index arithmetic, characterisation not consulted |
| SF-8 | Every rule built from a containing pair holds the floor. | exhaustion | `test_every_constructed_rule_holds_the_floor` — >20,000 rules |
| SF-9 | The declared step agrees with the renamings. | exhaustion | `test_step_agrees_with_the_renamings` — every inscription to generation 4 |

## Computation

| id | claim | class | evidence |
| --- | --- | --- | --- |
| SF-10 | Breaking one renaming costs 2 offered successors; breaking every renaming costs 4. | computation | `test_price_of_a_break` |
| SF-11 | At every generation exactly one object is held still by every renaming, and it is the one with no data. | computation | `test_the_thread_is_unique_at_every_generation`, to generation 8 |
| SF-12 | Being held still by every renaming is equivalent to distance zero. | computation | `test_the_thread_is_exactly_distance_zero`, to generation 7 |
| SF-13 | One step never lowers the distance, so the thread is left once and never regained. | computation | `test_distance_never_falls`, to generation 7 |
| SF-14 | A break does not ratchet: what is held still can rise again away from the thread. | computation | `test_a_break_does_not_ratchet` |
| SF-15 | The first break is at generation 2 and costs exactly 4 ways. | computation | `test_first_break_and_its_cost` |
| SF-16 | `objects(k) = a(ceil(k/2)) * a(floor(k/2))` with `a(n) = (3**n + 1)/2`. | computation | `test_object_count_closed_form`, to generation 10 |
| SF-17 | By generation 8, 3 objects of 1681 have a single possible past. | computation | `test_the_world_does_not_remember` |
| SF-18 | A composite renaming never holds an inscription with an odd data count; reflection alone can. | computation | `test_composite_renaming_needs_an_even_data_count`, `test_reflection_alone_tolerates_an_odd_data_count` |

## Negative

| id | claim | class | evidence |
| --- | --- | --- | --- |
| SF-19 | A map that reads which glyph is which fails both the agreement test and the floor. It is exactly what is unavailable to a state-read rule. | computation | `test_a_rule_that_reads_glyphs_is_not_a_rule_of_this_kind` |
| SF-20 | `<a\|b>` cannot tell itself from its reflection once glyphs are forgotten. | computation | `test_mirror_of_the_minimal_boundary_is_the_same_object` |

## Open

| id | claim | class |
| --- | --- | --- |
| SF-OPEN-1 | Whether supplying one asymmetry at the start is cheaper than dropping single-valuedness. Not priced here. | open |
| SF-OPEN-2 | Whether refusing a first state at all is coherent, and what it would cost. Not addressed here. | open |
| SF-OPEN-3 | Whether the closed form SF-16 continues past generation 10. Verified to 10, not proved. | open |
| SF-OPEN-4 | Whether SF-11 and SF-13 hold at every generation. Verified to 8 and 7, not proved. | open |

---

## Not claimed

No reading of this tree as any outside subject is offered. It is a growth
process over marks, and its results are about that process and nothing else.
The Lean proofs are about arbitrary maps and arbitrary renamings; they carry no
commitment to what a state is.
