# CLAIM LEDGER: rung two, track one -- no first demand

`AuthorityEffect: None`.  Every row carries exactly one evidence class.
A row at the level of a definition is marked so and is never counted as
content.  Counts in this file are dated 2026-09-04.

Classes used: DEFINITION (true by unfolding, by `rfl`, by a projection,
or by one rewrite), PROVED_THEOREM, RECONSTRUCTION (a sibling's or the
sealed estate's theorem, reproduced verbatim under a pin, with no credit
claimed), FINITE_COMPUTATION, CONJECTURE, OPEN, REFUSED, METATHEORY,
PREDICTION.

---

## OB1_REREAD

This row is the whole of the rung's engagement with the sealed estate's
first standing obstruction.  The sealed sentence is quoted verbatim, from
the span pinned in `SOURCE_MANIFEST.json` as `paper/paper.md` lines
488-494 with hash
`bfb9e4e0d74602110a2636b0944a75cce4075972aa75c00db503547b98daba6a`.  It is
not edited, not narrowed, and not restated in weaker words.

**The sealed sentence, quoted by pin:**

> **Result: no object-language endogenous demand generator was derived.**
> A collapsed pair, by itself, is not an active obstruction: nothing in the
> object language demands its separation.  What exists is the *declared
> pair-separation closure policy* (section 3.9) — declared metatheory that
> reissues the externally admitted requirement pattern on collapsed pairs.
> Under that declared policy, the fixed finite datum set reaches an
> all-pairs-separated fixpoint: **pair-separation closure terminates.**

**Beside it, the theorem of this rung, with its scope in its own sentence:**

> In the sealed grammar reconstructed in
> `lean/SecondNoFirst/Kernel.lean`, extended by a declared two-sided
> stake as defined in `lean/SecondNoFirst/Stake.lean`, and in no other
> grammar: a demand at a regime is at a pair the declared stake labels;
> whether a pair is a demand depends on the stake only through the label
> the declaration gives that pair; every event of the grammar is one of
> the six kinds the rung-zero census recorded, each carrying
> natural-number fields only; a supply changes no regime and so no
> demand; and under the stake that labels every pair free there is no
> demand at any regime whatever.  Hence in this grammar the first demand
> of any run has one source: the declaration, which is not an event of
> the grammar.

**Which is about what.**  The sealed sentence is about DERIVATION: it
records what the first derivation did and did not derive, and it stands
exactly as its own paper records it.  The theorem is about the GRAMMAR: it
records what this grammar, extended by a declared stake, admits as a
source of a demand.  The two are different statements about different
things.  Both stand.  Neither is evidence for or against the other, and
this rung reports no change of any kind to the sealed sentence's standing.

**Classes.**  The sealed sentence: the sealed estate's own record, quoted,
not reclassified here.  The theorem: `no_first_demand`, classed DEFINITION
in `FWDEF_CENSUS.json` -- it is an assembly whose five conjuncts are ALL at
the level of a definition, so it is never counted as content.  An earlier
draft of this paragraph said "three of its five conjuncts"; that was wrong
and is WITHDRAWN.  The theorem is true, its scope discipline is clean, and
what it shows is that the definitions were chosen well, which is a design
claim rather than a mathematical result.

**Scope excluded.**  Any grammar that is not this one.  In particular a
grammar carrying an event with a field of stake type is outside every
theorem here; naming such a grammar is a leftover of this rung and not a
result of it.

---

## Stage one: the reconstruction

| id | claim | class | evidence |
|---|---|---|---|
| NF-1 | The sealed kernel slice -- regime, contexts, derivability, collapse, separability, the six event kinds, the step and the replay -- is reproduced verbatim under a blob pin. | RECONSTRUCTION | `lean/SecondNoFirst/Kernel.lean`; pins on `lean4/Derivation/Basic.lean` and `Inertia.lean` in `SOURCE_MANIFEST.json`; `verify_pins.py` |
| NF-2 | The pinned one-sided stake, its demands, and its growth theorems are reproduced verbatim under a blob pin and six span pins. | RECONSTRUCTION | `lean/SecondNoFirst/Inherited.lean`; six spans of `StandingCommitment/Commitment.lean` |
| NF-3 | A two-sided stake labels every ordered index pair apart, same, or free, and is free on the diagonal by construction. | DEFINITION | `Stake.Stake`, `Stake.freeStake`, `Stake.allApart`, `Stake.allSame` |
| NF-4 | No pair of a datum with itself carries a label (`stake_irrefl`). | DEFINITION -- one rewrite of the structure field, then `rfl` | `lean_axioms.txt`; `test_diagonal_is_free_whatever_the_rule_says` |
| NF-5 | Every demand is at a labelled pair (`demands_subset_labelled`). | DEFINITION -- a projection out of `Demand` | `lean_axioms.txt` |
| NF-6 | Under the free stake there is no demand at any regime, reachable or not (`free_stake_no_demand`). | DEFINITION -- unfolding | `lean_axioms.txt`; `nofirst.json` `demands.free_stake_nodes_with_a_demand` |
| NF-7 | Over the represented state, the two-sided demands of the stake a one-sided commitment induces are, as a list and in order, the pinned one-sided demands, at every represented state and with no side hypothesis (`reconstruction_matches`). | PROVED_THEOREM | `lean_axioms.txt`; `Stake.reconstruction_matches` |
| NF-8 | `reconstruction_matches` bridges the represented state to the pinned one-sided demands and bridges NEITHER to the sealed regime. | OPEN, named and priced | leftover L-1 in `STATUS.md` |

## Stage two: no demand without a stake

| id | claim | class | evidence |
|---|---|---|---|
| NF-9 | Replaying any sequence made only of supplies returns the regime unchanged (`supplies_preserve_regime`). | PROVED_THEOREM -- induction over the sequence | `lean_axioms.txt` |
| NF-10 | For every stake, the demands after a supply are the demands before it (`supply_preserves_demands`). | DEFINITION given the reconstructed sealed theorem -- two rewrites, the content carried by `supply_no_op`. **Predicted NOT definitional; recorded as definitional. Census miss, see `STATUS.md`.** | `lean_axioms.txt`; sealed `Sealed.supply_no_op` |
| NF-11 | A pair in the demands is a pair the stake labels apart or labels same (`demand_needs_label`). | DEFINITION -- a projection and a three-way case split | `lean_axioms.txt` |
| NF-12 | Whether a pair is a demand depends on the stake only through the label the declaration gives that pair (`demand_depends_only_on_the_label`). | DEFINITION -- `unfold` then one rewrite. **Predicted NOT definitional; recorded as definitional. Census miss.** The STATEMENT is load-bearing and the PROOF is an unfolding; both are recorded. | `lean_axioms.txt` |
| NF-13 | Every event of the reconstructed grammar is one of exactly six kinds; the kind code is total, bounded by six, and injective (`grammar_carries_no_stake`). | DEFINITION -- pure case exhaustion over six constructors plus a decidable injectivity check, with no mathematical step; classed so in `FWDEF_CENSUS.json` and excepted BY NAME from that file's proof-length bound, because its twenty-two lines count constructors rather than work. Its value is that the compiler checks the case list instead of a reader checking it by eye. A fact about the RECONSTRUCTED type and about nothing else. | `lean_axioms.txt`; the six kinds match `research/second_inheritance/receipts/inheritance.json` `census.sealed_event_count` |
| NF-14 | The conjunction NO FIRST DEMAND, stated once with its scope in the same sentence (`no_first_demand`). | DEFINITION -- an assembly whose five conjuncts are ALL at the level of a definition, adding nothing beyond them. Never counted as content in any headline of this rung | `lean_axioms.txt` |
| NF-13b | That no constructor of the reconstructed event type carries a field of stake type, and that `stepE` reads `Regime -> Event -> Option Regime` and mentions no stake. | METATHEORY, read off the type SIGNATURE and checked by the compiler accepting the declaration; NOT a proposition and NOT proved by `grammar_carries_no_stake`, whose name is wider than its statement | the declarations themselves; the narrowing note in `lean/SecondNoFirst/NoFirst.lean` |
| NF-15 | At a regime with no admitted instance, a held pair is a demand exactly when the stake labels it apart (`demand_iff_apart_of_no_insts`), both directions. | PROVED_THEOREM | `lean_axioms.txt`; cites reconstructed `collapsed_of_no_insts` |
| NF-16 | At a regime with no admitted form, every held pair the stake labels apart is a demand (`apart_demand_of_no_forms`). | PROVED_THEOREM | `lean_axioms.txt` |
| NF-17 | Failing to separate is being collapsed (`collapsed_of_not_separable`), constructively, because derivability is decidable at each context. | PROVED_THEOREM | `lean_axioms.txt` |
| NF-18 | The converse direction, from "not collapsed" to "separable", is NOT available constructively over the sealed context type, which is infinite; it is used nowhere. | REFUSED, recorded | note at the head of `lean/SecondNoFirst/Inert.lean` |

## Stage two, unpredicted: the demand-inert kinds

| id | claim | class | evidence |
|---|---|---|---|
| NF-19 | An imposition changes no demand of any stake (`impose_preserves_demands`). | DEFINITION -- `Iff.rfl`; the requirement field enters neither derivability nor context well-formedness | `lean_axioms.txt` |
| NF-20 | A context of a newly admitted form derives nothing for any datum, at a well-formed regime (`new_form_derives_nothing`). | PROVED_THEOREM | `lean_axioms.txt` |
| NF-21 | Admitting a judgment form to a well-formed regime changes no pair's collapse and no pair's separability (`collapsed_addForm`, `separable_addForm`). | PROVED_THEOREM | `lean_axioms.txt` |
| NF-22 | Admitting a judgment form to a well-formed regime changes no demand of any stake: a form is demand-inert until an instance or a uniform rule reaches it (`admitForm_preserves_demands`). | PROVED_THEOREM. **NOT PREDICTED**: written after prediction N-16 missed. | `lean_axioms.txt`; `nofirst.json` `readings[].inert_event_kinds`; `test_admitting_a_form_is_inert` |
| NF-23 | Three of the six sealed event kinds leave every demand of every stake unchanged (`three_kinds_are_demand_inert`); the other three are NOT claimed inert. | PROVED_THEOREM as an assembly | `lean_axioms.txt` |
| NF-24 | The admission of a datum, of an instance, and of a uniform rule each change some demand set. | FINITE_COMPUTATION, not a theorem | `nofirst.json` `readings[].inert_event_kinds` excludes them; `test_admitting_an_instance_is_not_inert` |

## Stage three: demands propagate

| id | claim | class | evidence |
|---|---|---|---|
| NF-25 | The pinned one-sided generation theorem, re-exported with its hypotheses unchanged (`growth_generates_pinned`). | RECONSTRUCTION -- the sibling's statement and the sibling's proof; no credit claimed | `lean_axioms.txt`; span pin on `Commitment.lean` lines 142-150 |
| NF-26 | A fresh datum labelled apart from a held datum with which the grown regime collapses it is a demand of the grown regime and was not a demand before (`growth_generates_apart`). | PROVED_THEOREM for the positive half given the collapse hypothesis; the negative half is DEFINITION -- the fresh index is not a held index before the growth | `lean_axioms.txt` |
| NF-27 | The same with the collapse hypothesis DISCHARGED from "no admitted instance" rather than assumed (`growth_generates_apart_of_no_insts`). | PROVED_THEOREM; this is where the content of NF-26 sits | `lean_axioms.txt` |
| NF-28 | A fresh datum labelled same as a held datum from which the grown regime separates it is a demand of the grown regime and was not a demand before (`growth_generates_same`). | PROVED_THEOREM for the positive half; negative half DEFINITION | `lean_axioms.txt` |
| NF-29 | At a well-formed regime, a well-formed context derives the datum admitted by one growth step exactly when the context's form carries a uniform rule (`fresh_profile`). | PROVED_THEOREM | `lean_axioms.txt` |
| NF-30 | Under the stake labelling every distinct pair apart, a regime carrying no demand has at most one held datum of empty profile (`apart_at_most_one`). | PROVED_THEOREM, over the SEALED REGIME | `lean_axioms.txt`; `nofirst.json` `all_apart.max_empty_profiles_at_a_demand_free_node` |
| NF-31 | Under that stake, from a well-formed regime carrying no demand, one growth step generates at most one demand (`apart_at_most_one_new_demand`). | PROVED_THEOREM, over the SEALED REGIME | `lean_axioms.txt`; `nofirst.json` `all_apart.max_new_demands_per_growth_step` |
| NF-32 | The sibling two-sided tree records the corresponding statement over ITS OWN carrier as a CONJECTURE with no Lean, and as a FINITE_COMPUTATION for the bounded count. NF-30 and NF-31 are proofs over the sealed regime and are NOT proofs of the sibling's row; the sibling's row stands as the sibling wrote it. | RECORDED, with the carrier named | `research/two_sided_commitment/CLAIM_LEDGER.md` rows TS-09 and TS-14, pinned by blob; note at section five of `lean/SecondNoFirst/Propagate.lean` |

## Stage four: the finite cross-check

| id | claim | class | evidence |
|---|---|---|---|
| NF-33 | Over the declared rectangle -- every sequence of at most four sealed events from each sealed genesis reading, over the declared alphabet, unpruned -- the free stake carries no demand at any regime reached. | FINITE_COMPUTATION | `nofirst.json`; prediction N-13 HIT |
| NF-34 | Every demand recorded anywhere in the rectangle is at a pair its stake labels, and the classifier's population equals the population computed independently by the honour walk. | FINITE_COMPUTATION | `nofirst.json` `demands`; prediction N-14 HIT |
| NF-35 | In every sequence of the rectangle carrying a demand, the first demand and the first dishonoured labelled pair fall at the same event index, for all seven stakes. | FINITE_COMPUTATION | `nofirst.json` `first_demand`; prediction N-15 HIT |
| NF-36 | THREE sealed event kinds are demand-inert in the rectangle, not two. | FINITE_COMPUTATION; **prediction N-16 MISSED, recorded next to its value and not edited** | `nofirst.json` `inert_event_kinds`; the miss is the finding that produced NF-22 |
| NF-37 | At every regime of the rectangle carrying no demand under the all-apart stake, at most one held datum has the empty profile, and one growth step adds at most one demand. | FINITE_COMPUTATION agreeing with NF-30 and NF-31 | `nofirst.json` `all_apart`; prediction N-17 HIT |
| NF-38 | The stake induced by the pinned one-sided total commitment and the sibling's all-apart stake give the same demand set at every regime of the rectangle. | FINITE_COMPUTATION | `nofirst.json` `one_sided_total_differs_from_all_apart_at`; prediction N-18 HIT |
| NF-39 | The receipt regenerates byte-identically, and an independently written second enumerator reaches exactly the regimes the first reaches on the declared cross-check family. | FINITE_COMPUTATION | `nofirst.json` `crosscheck`; prediction N-19 HIT; `test_receipt_regenerates_byte_identically`, `test_the_two_enumerators_reach_the_same_regimes` |

## The extrapolation

| id | claim | class | evidence |
|---|---|---|---|
| NF-40 | The at-most-one bound of NF-31 does NOT survive the removal grammar the operator packet's rung four will declare. | PREDICTION, NOT FORCED, PENDING | `PREDICTIONS.md` N-X, with its falsifier and its scoring rule; scored by that rung and by no earlier one |

## What this rung does not claim

| id | claim | class |
|---|---|---|
| NF-41 | Nothing about the count of declared inputs, in either direction. That is the parallel track's question. | REFUSED (FW-COUNT); `nofirst.json` `input_count_claim` is `none` |
| NF-42 | Nothing about rung one's pending extrapolation on the four-item bound; four items are not computed here. | REFUSED |
| NF-43 | Every declaration the reconstruction SHARES with its pinned source is identical to it at the snapshot: 46 across four sources, comments and namespace aside. Whether the declarations it OMITS are safe to omit is still read by hand. | FINITE_COMPUTATION for the shared half, `test_reconstruction.py`; OPEN for the omitted half. Narrows an earlier row that recorded the whole question as OPEN |
| NF-44 | No claim about any grammar that is not the one reconstructed here. | REFUSED (FW-SET) |

## Library axiom reliance

Every one of the sixty-four theorems of this rung's package reports axioms
within `{propext, Quot.sound}`; eight report no axiom at all.  The full
report is `receipts/lean_axioms.txt`, checked against a fresh build by
`verify_lean.py`.  No user-declared axiom, no `sorry`, no `admit`, no
`unsafe`, no `partial`, in code or in comments.
