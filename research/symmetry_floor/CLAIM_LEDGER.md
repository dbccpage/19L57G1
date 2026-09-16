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
| SF-1 | A renaming-equivariant single-valued rule cannot break a renaming the state already holds still. The successor may still be a different state. | theorem | `lean/SymmetryFloor.lean::floor` — **no axioms** |
| SF-2 | The same held-renaming preservation holds for any finite number of applications of the rule. | theorem | `lean/SymmetryFloor.lean::floor_iterated` — **no axioms** |
| SF-3 | SF-1 assumes no group laws, action laws or carrier structure. It does assume both equivariance and that the chosen state is fixed by the renaming; a non-fixed start is outside the hypothesis. | theorem | the statement of `floor`; its binders are the evidence |
| SF-4 | Once the step offers a set, the set may be carried to itself while no member is. | theorem | `offered_set_carried`, `members_move` — `propext` |
| SF-5 | At a fixed source under an equivariant rule, a one-member invariant offer cannot break the renaming; the displayed two-member offer can. | theorem | `price_is_two` — `propext`; and SF-1 for the one-member case |

## Exhaustion

| id | claim | class | evidence |
| --- | --- | --- | --- |
| SF-6 | On the declared four-renaming carrier, held-set containment is necessary **and sufficient** for an equivariant rule to carry one inscription to another. | exhaustion | `test_containment_is_necessary_and_sufficient` — 30,625 pairs, 0 disagreements |
| SF-7 | Over a closed carrier of 8 inscriptions, exactly 128 of all 16,777,216 maps agree with the renamings, matching the characterisation. | exhaustion | `test_exhaustion_over_every_map` — counted by index arithmetic, characterisation not consulted |
| SF-8 | Every constructed equivariant rule from a containing pair preserves the held set. | exhaustion | `test_every_constructed_rule_holds_the_floor` — >20,000 rules |
| SF-9 | The declared step agrees with the renamings. | exhaustion | `test_step_agrees_with_the_renamings` — every inscription to generation 4 |

## Computation

| id | claim | class | evidence |
| --- | --- | --- | --- |
| SF-10 | Over all invariant offered sets in the declared 175-inscription price carrier, breaking one non-identity renaming costs 2 states and breaking all three costs 4. | computation | `test_price_of_a_break`; dynamic programming over complete renaming orbits |
| SF-11 | In each checked generation 0 through 8, exactly one object is held still by every renaming, and it is the one with no data. | computation | `test_the_thread_is_unique_at_every_generation` |
| SF-12 | Being held still by every renaming is equivalent to distance zero. | computation | `test_the_thread_is_exactly_distance_zero`, to generation 7 |
| SF-13 | Across every checked edge from source generations 0 through 7, distance never falls; no checked path can return to distance zero after adding data. | computation | `test_distance_never_falls` |
| SF-14 | A break does not ratchet: what is held still can rise again away from the thread. | computation | `test_a_break_does_not_ratchet` |
| SF-15 | The first break is at generation 2 and costs exactly 4 ways. | computation | `test_first_break_and_its_cost` |
| SF-16 | `objects(k) = a(ceil(k/2)) * a(floor(k/2))` with `a(n) = (3**n + 1)/2`. | computation | `test_object_count_closed_form`, to generation 10 |
| SF-17 | By generation 8, 3 objects of 1681 have a single possible past. | computation | `test_the_world_does_not_remember` |
| SF-18 | Through generation 8, the composite renaming holds no inscription with odd data count; reflection alone does hold such examples. | computation | `test_composite_renaming_needs_an_even_data_count`, `test_reflection_alone_tolerates_an_odd_data_count` |

## Negative

| id | claim | class | evidence |
| --- | --- | --- | --- |
| SF-19 | A state function that distinguishes glyphs fails both equivariance and held-set preservation. This is a negative control showing that state dependence alone does not imply equivariance. | computation | `test_a_rule_that_reads_glyphs_is_not_a_rule_of_this_kind` |
| SF-20 | `<a\|b>` cannot tell itself from its reflection once glyphs are forgotten. | computation | `test_mirror_of_the_minimal_boundary_is_the_same_object` |

## Open

| id | claim | class |
| --- | --- | --- |
| SF-OPEN-1 | Whether supplying one asymmetry at the start is cheaper than dropping single-valuedness. Not priced here. | open |
| SF-OPEN-2 | Whether refusing a first state at all is coherent, and what it would cost. Not addressed here. | open |
| SF-OPEN-3 | Whether the closed form SF-16 continues past generation 10. Verified to 10, not proved. | open |
| SF-OPEN-4 | Whether SF-11 and SF-13 hold at every generation. Verified to 8 and 7, not proved. | open |
| SF-OPEN-5 | **Is there a floor for set-valued rules too?** Under its explicit equivariance and fixed-state hypotheses, SF-1 constrains a single-valued rule, and SF-10 prices invariant offered sets on the declared finite carrier. Neither bounds how much a set-valued rule may produce *per step*. A bound of the form "a step offering `n` successors cannot lower the held set by more than `f(n)`" is not established here, in either direction. | open |
| SF-OPEN-6 | **This tree does not check whether a result is already known.** SF-1 is a statement about maps agreeing with declared renamings, and no prior-result search is part of this tree's receipt. The gap is procedural, not mathematical: the tree has no required "nearest known result, and how this differs" field. Recorded here so the absence of that check is explicit rather than mistaken for a novelty claim. | open |

---

## The three named hunts

`SF-OPEN-1`, `SF-OPEN-2` and `SF-OPEN-5` are the object-level questions this
tree names and does not answer. Their status is **OPEN here**; no claim of
novelty, or of absence from prior work, is made.

`SF-OPEN-6` is different in kind: it is a defect in how trees are built, not a
question about the carrier. It is listed with the others because it is the one
that decides whether the other three are worth the work.

---

## Not claimed

No reading of this tree as any outside subject is offered. It is a growth
process over marks, and its results are about that process and nothing else.
The Lean proofs are about arbitrary types and maps satisfying the stated
equivariance and fixed-state hypotheses; they carry no commitment to what a
state is.
