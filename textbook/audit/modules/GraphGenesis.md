# Audit: GraphGenesis

| field | value |
|---|---|
| Path | lean4/Derivation/GraphGenesis.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 75e547b8685e9514 |
| Lines | 720 (inventory records 721) |
| Imported by root `Derivation.lean` | yes (line 42) |
| Imports | Derivation.Attachment (and through it HigherStructure, PrimitivePassage, PrimDiff, PrimitiveCore). It does NOT import `Derivation.Basic`; nor does anything in its import chain (checked: `PrimitivePassage.lean` imports only `Derivation.PrimDiff` and `Derivation.PrimitiveCore`, and no module mentioning `PState` imports `Derivation.Basic`) |
| Declarations | 1 structure (`ProposalRecord`), 11 def, 28 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 28 lines (every theorem); 26 `[propext, Quot.sound]`, 2 none (`IsInternal_exact`, `internal_is_response`) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module asks where a new occurrence, a new asserted difference, a new retained difference or a new protected demand can come from in the passage kernel. Part 1 proves, field by field over the whole `PState` record, that the kernel's own response events (`refineCol`, `addCol`, and their funding `setBudget`) move only the observation and the budget, that the represented response family `nextFamilyP` ranges over columns on existing occurrences and has exactly two block shapes, and that along every trace drawn from the internal fragment the four graph stores (`occ`, `asserted`, `wit`, `prot`) are fixed. Growth therefore arrives only through supply events of an external driver or through the one-edge grammar `Attachment.upFamily` (`graph_growth_is_supplied`). Part 2 packages a one-edge extension as a `ProposalRecord`: a named member of the family with its membership proof, an embedding with retraction, freshness, preservation obligations, provenance of the new pair, and a declared cost, with no license, execution or activation field; the record is inert on a halted state and transports under renaming within the scope `act_up_comm` already had. Part 3 shows that an obstruction meeting the kernel's own hypotheses is resolved inside the existing carrier by a member of `nextFamilyP`, so the demand for carrier growth is a separately declared premise, not a consequence of obstruction.

Relation to the regime model of `Basic.lean` (requested): none in Lean. The "graph" here is the four pair/occurrence stores of `PState` from `PrimitivePassage`. `Basic.lean`'s `Regime`, `Event` and `replayE` are not imported, not mentioned, and no bridge theorem relates a `PState` to a `Regime`. The connection between the passage kernel and the regime model is at most a verbal analogy in the paper; within this module it is not even that (the word "regime" does not occur in GraphGenesis.lean). Whether any other module proves such a bridge was not checked here.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `MentionsOnlyExisting s` | 137 | def | predicate on events: every column/point named is `< s.occ.length` (by cases on the event) | ADMITTED |
| `IsInternal` | 190 | def | Boolean: event is `refineCol`, `addCol` or `setBudget` | ADMITTED (declared fragment) |
| `IsResponseEvent` | 224 | def | Boolean: the internal kinds plus `declareObs`, `refuse`, `setLicense`, `halt` (every non-supply kind) | ADMITTED |
| `GraphStoresFixed s t` | 244 | def | `s.occ = t.occ ∧ s.asserted = t.asserted ∧ s.wit = t.wit ∧ s.prot = t.prot` | ADMITTED |
| `ProposalRecord s` | 381 | structure | block, `block_complete : block ∈ upFamily s`, `embed retract : Nat → Nat`, `retract_embed` on represented positions, `token_fresh`, `preserves_asserted/wit/prot/separated`, `newPair`, `parentPos`, `freshPos`, `newPair_provenance`, `parent_represented`, `freshPos_is_new`, `cost : Nat`; no license/execution/activation field | ADMITTED (a declared proposal schema; `embed`/`retract` are Nat → Nat data) |
| `upProposal s hwf hh p hp` | 452 | def | the proposal at parent `p` with identity embedding and retraction, `cost = (upBlock s p).length` | ADMITTED |
| `tri` | 552 | def | `treeAt pathPolL 2` (three occurrences, path) | ADMITTED (datum) |
| `triProp1`, `triProp2` | 564–568 | def | `upProposal tri` at parents 1 and 2 | ADMITTED |
| `funded s` | 606 | def | `{ s with budget := 1 }` | ADMITTED |
| `FamilyGrowsCarrier s` | 651 | def | `∃ b ∈ nextFamilyP s, ¬ GraphStoresFixed s (replayP b s)` | ADMITTED |
| `blindPair` | 666 | def | a concrete state with two occurrences, both pairs asserted, `(0,1)` retained and protected, `obs = some []`, budget 0, licensed, live | ADMITTED (datum) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `refineCol_only_obs` | 59 | for every `s v p`, `step s (refineCol v p)` has the same occ, asserted, wit, prot, refusals, licensed, halted as `s` | FROZEN | propext, Quot.sound | S |
| `addCol_only_obs` | 75 | same for `addCol c` | FROZEN | propext, Quot.sound | S |
| `extensionProposals_range_over_existing` | 99 | every block of `extensionProposals s` is `[setBudget 1, addCol [i]]` with `i < s.occ.length` | FROZEN | propext, Quot.sound | S |
| `repairFamily_range_over_existing` | 116 | every block of `repairFamily s i j` is `[setBudget 1, refineCol v q]` with the new point `q < s.occ.length` | FROZEN | propext, Quot.sound | S |
| `nextFamilyP_block_shape` | 146 | every `b ∈ nextFamilyP s` is a repair block or an extension block (two shapes, no third) | FROZEN | propext, Quot.sound | S |
| `nextFamilyP_range_over_existing` | 165 | every event of every `nextFamilyP` block satisfies `MentionsOnlyExisting s` | FROZEN | propext, Quot.sound | S |
| `IsInternal_exact` | 204 | `IsInternal e = true ↔` e is `refineCol`, `addCol` or `setBudget` (by `rfl`-level cases) | FROZEN | none | A |
| `internal_is_response` | 237 | `IsInternal e = true → IsResponseEvent e = true` | FROZEN | none | A |
| `response_step_fixes_graph` | 250 | `IsResponseEvent e = true → GraphStoresFixed s (step s e)` | FROZEN | propext, Quot.sound | S |
| `internal_step_fixes_graph` | 259 | same for `IsInternal` | FROZEN | propext, Quot.sound | A |
| `replay_fixes_graph_of_all` | 264 | if `P` is a step-wise graph-fixing predicate and `h.all P`, then `GraphStoresFixed s (replayP h s)` | FROZEN | propext, Quot.sound | A |
| `internal_family_cannot_grow_carrier` | 283 | `h.all IsInternal = true → GraphStoresFixed s (replayP h s)` | FROZEN | propext, Quot.sound | S |
| `response_replay_fixes_graph` | 291 | same for `IsResponseEvent` | FROZEN | propext, Quot.sound | S |
| `nextFamilyP_blocks_are_responses` | 299 | every block of `nextFamilyP s` is all-`IsResponseEvent` | FROZEN | propext, Quot.sound | A |
| `nextFamilyP_block_fixes_graph` | 317 | `b ∈ nextFamilyP s → GraphStoresFixed s (replayP b s)` | FROZEN | propext, Quot.sound | S |
| `graph_growth_is_supplied` | 340 | under WFStores, live, `p < len`: every `nextFamilyP` block fixes the graph while `upBlock s p` grows occ by one and adds `(p,len)` to asserted/wit/prot | CONDITIONAL: WFStores, live, `p < len` | propext, Quot.sound | S |
| `proposal_confers_no_execution` | 441 | `s.halted = true → replayP P.block s = s` for every `P : ProposalRecord s` | CONDITIONAL: halted | propext, Quot.sound | S |
| `upProposal_executes` | 507 | under WFStores, live, `p < len`: replaying `(upProposal …).block` grows occ and adds the new pair to the three stores | CONDITIONAL: WFStores, live, `p < len` | propext, Quot.sound | S |
| `proposal_transports` | 533 | with `n = len`, WFStores, live: for every `P`, `P.block` renamed by `σ` is in `upFamily (act σ s)`, and `act σ` of the executed state equals the executed renamed block (via `act_up_comm`) | CONDITIONAL: `n = len`, WFStores, live | propext, Quot.sound | S |
| `tri_wf`, `tri_live`, `tri_parent1`, `tri_parent2` | 554–561 | `tri` is store-bounded, live, with parents 1 and 2 in range | VERIFIED_FINITE | propext, Quot.sound | A |
| `proposal_family_retains_ties` | 576 | `triProp1.cost = triProp2.cost`, their executed stores differ, both blocks are in `upFamily tri` | VERIFIED_FINITE (REFUTED: equal cost does not select) | propext, Quot.sound | S |
| `obstruction_resolved_in_carrier` | 614 | under `obstP s i j = true`, `i ≠ j`, `i < len`, `(i,j) ∈ s.prot`, licensed, live: `[setBudget 1, addCol [i]] ∈ nextFamilyP s`, its replay has `obstP … i j = false`, and `GraphStoresFixed s (replay)` | CONDITIONAL: six named hypotheses | propext, Quot.sound | S |
| `family_never_grows_carrier` | 655 | `∀ s, ¬ FamilyGrowsCarrier s` | FROZEN | propext, Quot.sound | S |
| `growth_demand_not_obstruction_consequence` | 693 | on `blindPair`: obstruction certified, `nextFamilyP blindPair` is the two-member list, both members resolve, both fix the graph; and `∀ s, ¬ FamilyGrowsCarrier s` | VERIFIED_FINITE (first four conjuncts) + FROZEN (last) | propext, Quot.sound | S |
| `blindPair_resolution_keeps_carrier` | 711 | after `[setBudget 1, addCol [0]]` the occ is `[0,1]`, obs is `some [[0]]`, obstruction cleared | VERIFIED_FINITE | propext, Quot.sound | A |

## 4. External and admitted assumptions

- Taken as given: `PState`, `step`, `replayP`, `obstP`, `sepP`, `nextFamilyP`, `extensionProposals`, `repairFamily`, `nextFamilyP_nonempty`, `extension_always_available`, `extension_resolves`, `obst_requires_observation` (PrimitivePassage); `upFamily`, `upBlock`, `up_iff_legal`, `up_executes`, `halted_up_inert`, `act_up_comm`, `treeAt`, `WFStores` (Attachment); `HigherStructure.pstep_budget`.
- Recurring hypotheses: `WFStores s`, `s.halted = false`, `p < s.occ.length` (Part 2); the six obstruction hypotheses of `obstruction_resolved_in_carrier` (Part 3). All named.
- Library lemmas doing real work: `List.all`, `List.mem_map`, `List.mem_flatMap`-style membership in `nextFamilyP`; decidability for the `decide` proofs on `blindPair` and `tri`.
- Functions `Nat → X` as data: `ProposalRecord.embed` and `.retract`. Finitude flag: these are metatheoretic position maps; `retract_embed` is only required on `x < s.occ.length`, so the record constrains them on the finite carrier only. The docstrings call them an "embedding of old positions", which is accurate.
- Unearned identity: none found.
- Unrestricted external universe: none found; `IsInternal` and `IsResponseEvent` are exhaustive case splits on the declared `PEvent` type, and the docstring says nothing is claimed about events outside it.
- Unbounded function treated as internally available: none found.
- Silently assumed observer: none found. `obs` is a field; `preserves_separated` is conditional on `s.obs = some cols`.
- Unspecified correspondence between presentations: `embed`/`retract` is specified by `retract_embed` on represented positions; `upProposal` instantiates it as the identity.
- Cost function without justification: `ProposalRecord.cost : Nat` is a bare declared field with no law relating it to anything; `upProposal` sets it to the block length (4). The docstring calls it "the declared resource demand". `proposal_family_retains_ties` compares two such costs. This is an admitted datum, not a derived measure; the module does not claim otherwise.
- Admitted condition later described as forced: none found. The docstring says the opposite ("the growth demand remains a separately declared premise").
- Finite computation presented as universal: none found; `growth_demand_not_obstruction_consequence` pairs its finite conjuncts with the general `family_never_grows_carrier`, and the ledger states the scope ("the family the kernel computes; other declared families OPEN").

## 5. Derived consequences

No downstream Lean module imports `GraphGenesis` (grep: none). Ledger entry CL-PD2-GRAPH-GENESIS (Goal 5) cites 18 theorems by name in three parts and states scope limits. paper/paper_change_log.md line 833 records `ProposalRecord`. Within the module, `response_step_fixes_graph` is the engine of Part 1 (it subsumes `refineCol_only_obs`/`addCol_only_obs`), and `family_never_grows_carrier` follows from `nextFamilyP_block_fixes_graph`.

## 6. Counterexamples and limitations

- `proposal_family_retains_ties`: refutes "a declared cost selects a branch"; witness two proposals on `tri` with equal cost 4 and different executed stores.
- `growth_demand_not_obstruction_consequence`: refutes "an active obstruction demands carrier growth"; witness `blindPair`, whose two-member `nextFamilyP` resolves the obstruction in the carrier.
- `proposal_confers_no_execution`: on a halted state a proposal exists and does nothing (refutes "holding a proposal moves the state").
- Not proved: that `obs` or `budget` do change under response events (only that the other seven fields do not); the ledger says so.
- Not proved: any bound on points already inside a declared column (`repairFamily_range_over_existing` bounds the new point only); the ledger says so.
- Not proved: that no response family other than `nextFamilyP` could grow the carrier; OPEN in the ledger.
- Not proved: minimality, uniqueness or any universal property of `ProposalRecord`; the docstring and ledger say none is claimed.
- Not proved: any relation between `PState` and `Basic.lean`'s `Regime` (see section 1).
- `obstruction_resolved_in_carrier` needs `s.licensed = true`; on an unlicensed state the extension route is gated (compare `ControllerCategory.LOBST`), so the theorem does not say every obstruction is resolved in the carrier, only those meeting the kernel's hypotheses. The ledger's "every obstruction meeting the kernel's own hypotheses" matches.

## 7. Axiom dependencies

All 28 artifact lines lie within `{propext, Quot.sound}`; 2 use no axioms. None exceeds the whitelist.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 28 theorems appear in the axiom artifact; 18 are cited in CL-PD2-GRAPH-GENESIS. No probe was run for this module. The import chain was checked with grep (`^import` lines of GraphGenesis, Attachment, PrimitivePassage, and of every module mentioning `PState`): no path to `Derivation.Basic`.

## 9. Related Python implementations

code/derivation/graph_genesis.py: `kind`, `is_internal`, `is_funding`, `is_response_event`, `blind_pair`, `refinable`, `supply_stages`, `sample_states`, `declared_columns`, `event_battery`, `changed_fields`, `graph_stores_fixed`, `field_invariance_report`, `internal_alphabet`, `internal_fragment_report`, `mentions_only_existing`, `block_shape`, `family_report`, `ProposalRecord` (class), `record_field_names`, `carries_no_authority`, `up_proposal`, `separated_pairs`, `proposal_obligations`, `proposal_report`, `transport_report`, `tie_report`, `in_carrier_resolution`, `part3_report`. tests/test_graph_genesis.py: `test_event_classification_is_exact`, `test_field_invariance_battery`, `test_declared_columns_and_battery`, `test_internal_fragment_cannot_grow_carrier`, `test_family_shape_range_and_invariance`, `test_proposal_record_obligations`, `test_transport_over_full_permutation_group`, `test_equal_cost_tie_is_retained`, `test_part3_obstruction_does_not_request_the_lift`, `test_json_helpers`, `test_declared_vocabulary`, `test_runner_byte_stable`.

## 10. Textbook placement proposal

- Prerequisites: the `PState` fields and `step` guards; `nextFamilyP`, `obstP` and the extension/repair families (PrimitivePassage); `upFamily` and `up_executes` (Attachment).
- Substantive: `response_step_fixes_graph` and `internal_family_cannot_grow_carrier` (Part 1's content); `graph_growth_is_supplied`; the `ProposalRecord` schema with `proposal_confers_no_execution` and `upProposal_executes`; `obstruction_resolved_in_carrier`, `family_never_grows_carrier`, `growth_demand_not_obstruction_consequence`. Auxiliary: `IsInternal_exact`, `internal_is_response`, `replay_fixes_graph_of_all`, `nextFamilyP_blocks_are_responses`, the `tri_*` facts, `blindPair_resolution_keeps_carrier`.
- Lesson title: "Where new occurrences come from: the response family never grows the carrier." Question answered: can the kernel's own repair/extension responses ever add an occurrence or a difference, and does an obstruction demand that they do? (No; no.)
- Recommend omitting: `refineCol_only_obs` and `addCol_only_obs` as separate items (special cases of `response_step_fixes_graph`); `preserves_separated` detail of `ProposalRecord` can be summarised.

## 11. Interpretation findings

- Attachment-point / proposal check (requested): `ProposalRecord` is explicitly a proposal. The Lean structure has no field that executes or licenses; the docstring says so, and the ledger says "'The record carries no authority' is structural (there is no such field), not a theorem." Consistent with the project note that attachment points are proposals only. No defect.
- Basic.lean bridge (requested): the module's "graph" is the `PState` store quadruple; no import of or theorem about `Basic.lean`'s regime model exists. Any paper sentence treating the passage kernel's carrier as "the regime's data" would be an INTERPRETATION DEFECT; none was found in the grep of paper/*.md for this module's theorem names (only the ledger and change log mention them), so: none found, with the caveat that paper.md's general prose about passage versus regime was not read in full here.
- `cost` field: declared, unconstrained. The ledger says "a declared cost". `proposal_family_retains_ties` shows equal declared costs with different outcomes. No prose reads cost as derived. No defect; flagged as an admitted datum.
- `graph_growth_is_supplied` (line 340): the name suggests a disjunction "growth comes from the driver OR the grammar"; the Lean proves only "every `nextFamilyP` block fixes the graph, and `upBlock` grows it" under WFStores/live/`p < len`. It does not prove that the external driver and the grammar are the only growth sources (that would need a classification of all events, which `response_step_fixes_graph` gives for response events, leaving the supply events `admitOcc`, `assertWit`, `admitWit`, `protect` as the complement). The ledger states it correctly ("growth comes from the external driver or the Up grammar, never from nextFamilyP"), and the complement is exact by `IsResponseEvent` covering every non-supply kind. INTERPRETATION note only; no defect.
- `family_never_grows_carrier` is universal over `s`; checked that it does not depend on WFStores (it uses `nextFamilyP_block_fixes_graph`, which is unconditional). Correct.
- Vacuity check: `obstruction_resolved_in_carrier`'s six hypotheses are jointly satisfiable (`funded blindPair`-style states; `blindPair` itself satisfies all but is used with budget 0, and the theorem funds internally via `setBudget 1`). `proposal_confers_no_execution` is a genuine implication. None vacuous.
