# Audit: Generator

| field | value |
|---|---|
| Path | lean4/Derivation/Generator.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 6834f5b4c487030b |
| Lines | 296 |
| Imported by root `Derivation.lean` | yes (line 20) |
| Imports | `Derivation.RefusalFrontier` |
| Declarations | 4 def (`profile1`, `profileV`, `swap12`, `profile2`), 16 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 16 lines (every theorem); axioms seen: `propext` / `propext, Quot.sound` |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module settles the "generation half" of the frontier conjecture F5: is the composite of the declared reflective refusal semantics (`RefusalFrontier.stepRefl`, which grows the chain `reflState n`) and the pair-separation closure policy (every unordered pair of distinct carrier elements must be separable under the declared observation regime; an unseparated pair is an obstruction) a challenge generator that needs no per-round external event? It fixes the depth-1 observation regime `profile1` — the tag bit, whether some relation instance enters the element, whether some leaves it; the element's index is metatheoretic bookkeeping and is not observed — and proves that the chain has exactly three profile classes (seed, interior, tip), that the depth-1 obstructions are exactly the interior pairs (an iff), and hence that for every chain length `n ≥ 3` the pair `(1, 2)` is an obstruction: generation never dries. It then proves the horizon-free halves of the repair question: presence marking is vacuous (every receipt is already tagged), any finite set of marked indices is outrun, valued marks (reading the index itself) separate everything and so end generation, the transposition of interior points 1 and 2 does not preserve the successor relation, and depth-2 observation separates the near-end pair `(1,3)` at length 4 but is outrun by `(2,3)` at length 5. The bounded trajectories over the five-strategy repair class live in Python.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `profile1` | 55 | def | `(decide (i ∈ s.tags), decide (∃ p ∈ s.rel, p.2 = i), decide (∃ p ∈ s.rel, p.1 = i))` — the depth-1 observation of element `i` | ADMITTED (declared observation regime) |
| `profileV` | 243 | def | `(profile1 s i, i)` — the depth-1 profile together with the element's own index | ADMITTED (declared "valued automark" regime; identity-grade by construction) |
| `swap12` | 259 | def | transposition of indices 1 and 2 | ADMITTED |
| `profile2` | 277 | def | depth-1 profile plus the lists of depth-1 profiles of in-neighbours and out-neighbours | ADMITTED (declared depth-2 regime) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `reflective_chain_tags` | 35 | `∀ n, (reflState n).tags = (range n).map (·+1)` | FROZEN (∀ n) | propext | A |
| `chain_tagged_iff` | 60 | `i ∈ (reflState n).tags ↔ 1 ≤ i ∧ i ≤ n` | FROZEN | propext, Quot.sound | A |
| `chain_hasIn_iff` | 70 | `(∃ p ∈ rel, p.2 = i) ↔ 1 ≤ i ∧ i ≤ n` | FROZEN | propext, Quot.sound | A |
| `chain_hasOut_iff` | 82 | `(∃ p ∈ rel, p.1 = i) ↔ i < n` | FROZEN | propext, Quot.sound | A |
| `middle_profile` | 97 | for `1 ≤ i < n`: `profile1 (reflState n) i = (true,true,true)` | CONDITIONAL:`1 ≤ i`, `i < n` | propext, Quot.sound | S |
| `endpoint0_profile` | 105 | for `1 ≤ n`: `profile1 (reflState n) 0 = (false,false,true)` | CONDITIONAL:`1 ≤ n` | propext, Quot.sound | S |
| `endpointN_profile` | 115 | for `1 ≤ n`: `profile1 (reflState n) n = (true,true,false)` | CONDITIONAL:`1 ≤ n` | propext, Quot.sound | S |
| `depth1_obstructions_are_exactly_middle_pairs` | 131 | for `1 ≤ n`, `i, j ≤ n`, `i ≠ j`: profiles equal ↔ both interior (`1 ≤ i < n ∧ 1 ≤ j < n`) | CONDITIONAL:`1 ≤ n`, `i ≤ n`, `j ≤ n`, `i ≠ j` | propext, Quot.sound | S |
| `generation_never_dries` | 183 | for `3 ≤ n`: `1 ≠ 2 ∧ profile1 (reflState n) 1 = profile1 (reflState n) 2` | CONDITIONAL:`3 ≤ n` (∀ n, metatheoretic) | propext, Quot.sound | S |
| `automark_presence_vacuous` | 198 | for `3 ≤ n`: every `1 ≤ i ≤ n` is tagged, and still `profile1 1 = profile1 2` | CONDITIONAL:`3 ≤ n` | propext, Quot.sound | S |
| `le_foldr_max` | 204 | every member of a list is `≤ foldr max 0` | FROZEN (list lemma) | propext, Quot.sound | A |
| `finite_marks_outrun` | 221 | for any `marks : List Nat` there are `n`, interior distinct `i, j ∉ marks` with equal depth-1 profiles (witness `n = M+3`, `i = M+1`, `j = M+2`, `M = foldr max 0 marks`) | FROZEN (∀ finite list) | propext, Quot.sound | S |
| `valued_marks_collapse_generation` | 246 | `i ≠ j → profileV (reflState n) i ≠ profileV (reflState n) j` | FROZEN (immediate: the second component is `i`) | propext, Quot.sound | S |
| `middle_swap_not_relation_preserving` | 261 | for `2 ≤ n`: `(0,1) ∈ rel` and `(swap12 0, swap12 1) = (0,2) ∉ rel` | CONDITIONAL:`2 ≤ n` | propext, Quot.sound | S |
| `depth2_separates_near_ends_n4` | 287 | `profile2 (reflState 4) 1 ≠ profile2 (reflState 4) 3` | VERIFIED_FINITE (`decide`) | propext, Quot.sound | S |
| `depth2_obstruction_n5` | 292 | `profile2 (reflState 5) 2 = profile2 (reflState 5) 3 ∧ 2 ≠ 3` | VERIFIED_FINITE (`decide`) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- **The chain is inherited as a declared constructor** (`stepRefl`, `reflState : Nat → PState` from `RefusalFrontier`); the module adds nothing to its provenance. Both component declarations (reflective semantics; closure policy) are "sealed checkpoints" per the paper (FG1). The closure policy itself is not formalised here: "obstruction" is read off as profile equality of distinct elements, which is what the policy demands be separated.
- **The observation regime is declared.** `profile1`, `profile2`, `profileV` are hand-chosen; the header says they "reproduce structurally" the frontier search's per-element profile. The textbook should present them as the declared regime of the F5 question, not as the regime.
- **Indices as metatheory.** The header is explicit: "the index is metatheoretic bookkeeping; observation sees only tags and incident edges". `profileV` deliberately breaks this by observing the index; its theorem is then trivial and the paper says so ("presentation identity made observable", "identity-grade"). Finitude flag honoured by the module.
- **Quantification over `n : Nat`.** Every horizon-free theorem is a metatheoretic `∀ n`; "forever" and "never dries" (docstrings, paper FG4) are readings of that. The paper adds "self-continuation relative to those declarations, not absolute self-origination" and "no additional event is supplied per round *after* the declared reflective transition and closure policy are fixed". See §11.
- **`finite_marks_outrun` models a repair strategy as a fixed finite list**; the dynamics of per-pair marking (marks added each round) are in Python only. The theorem's content: any fixed finite mark set has an unmarked interior pair beyond its maximum.
- **Library lemmas doing work:** `List.range_succ`, `List.map_append`, `List.mem_map`, `List.mem_range`, `List.mem_cons`, `Nat.sub_add_cancel`, `Nat.eq_zero_or_pos`, `Nat.lt_or_ge`, `Nat.le_antisymm`, `omega`, `decide` on `reflState 4/5`.
- Unearned identity: none found. Unrestricted external universe: none (all on `Nat`, `Bool`, lists). Unbounded function treated as internally available: `reflState` (flagged above, inherited) and `profileV`'s index (declared identity-grade). Silently assumed observer: the regime is declared, not silent. Unspecified correspondence between presentations: the correspondence between `profile1`/`profile2` and the Python `view`/`profile2` is checked by `lean_agreement` in Python (bounded), stated in the paper; the general-`n` correspondence between `profile2` and `SeparationCapacity.profileD · · 1` is recorded as OPEN in the paper and is addressed at `n = 4, 5` only (see `SeparationCapacity` record). Cost function without justification: none in Lean (import counts are Python). Admitted condition later described as forced: none found. Finite computation presented as universal: the depth-2 outrun is two instances (`n = 4, 5`) plus 15-round trajectories; the paper says "instance-backed and bounded evidence for depth 2" and later points to `SeparationCapacity.depth_d_outrun` for the structural statement. No defect.

## 5. Derived consequences

`SeparationCapacity` opens `Generator` and uses `profile1`, `profile2`, `middle_profile`, `endpoint0_profile`, `endpointN_profile`, `chain_hasIn_iff`, `chain_hasOut_iff`, `chain_tagged_iff` (its `incoming_edges_interior`, `outgoing_edges_interior`, `profile2_interior`, `radius_one_agrees_with_sealed_depth2*`). `CapacityBound`, `LocalStrategy`, `G1Class` inherit through it (`LocalStrategy` cites `depth2_clears_n4` against `depth2_separates_near_ends_n4`). Paper: `paper/endogenous_generator.md` FG2–FG7 (owner). Ledger: `CL-G-GENERATION`, `CL-G-OBSTRUCTIONS-EXACT`, `CL-G-REPAIR-FATES`, `CL-G-DEPTH2`, `CL-G-DIRECT-SWAP`, `CL-G-TERMINAL`, and cross-cites from `CL-CAP-BOUND`, `CL-ENDOGENOUS-FIDELITY-GENERATOR`, `CL-FR6-T10-NORMAL-FORM`.

## 6. Counterexamples and limitations

- `depth2_obstruction_n5`: the pair `(2,3)` at length 5 refutes "depth 2 repairs the chain". `middle_swap_not_relation_preserving`: `(0,1) ↦ (0,2) ∉ rel` refutes "the interior transposition is a symmetry" (and only that; no rigidity claim). `valued_marks_collapse_generation`: with the index observable there is never an obstruction — refutes "valued automark repairs"; it prevents demands.
- Not proved: minimality or uniqueness of the generator (disclaimed in the docstring); the repair-cycle exclusion over all strategies (Python, five strategies, 15 rounds; class-general open as G1/G3); the depth-`d` outrun (that is `SeparationCapacity.depth_d_outrun`); the general-`n` equality of `profile2` with the radius-1 `profileD` (open); full rigidity of the directed chain (open, FG7).
- `depth1_obstructions_are_exactly_middle_pairs` is stated for `i, j ≤ n` only; elements outside the carrier are not profiled.

## 7. Axiom dependencies

All 16 within `{propext, Quot.sound}`. None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 16 theorems are in `artifacts/lean_axioms.txt` and the root inventory; all are cited in `paper/endogenous_generator.md` and the `CL-G-*` ledger entries. No probe run (the two `decide` facts are on `reflState 4` and `reflState 5`; the others were read in full).

## 9. Related Python implementations

`code/derivation/generator.py`: `chain_tags`, `chain_rel`, `profile1`, `profile2`, `view`, `obstructions`, `RoundRecord`, `BranchReport`, `repair_per_pair`, `run_branch` (five strategies, 15 rounds), `exclusion_check`, `middle_pairs`, `lean_agreement`; artifact `artifacts/generator.json`. Tests `tests/test_generator.py`: `test_chain_matches_lean_shape`, `test_depth1_obstructions_are_exactly_middle_pairs`, `test_generation_never_dries_within_bound`, `test_automark_presence_is_vacuous`, `test_automark_valued_kills_generation`, `test_per_pair_repairs_but_imports_every_firing_round`, `test_depth2_first_fires_at_five_and_stays_alive`, `test_exclusion_no_endogenous_cycle_in_class`, `test_lean_agreement_all_hold`.

## 10. Textbook placement proposal

- Prerequisites: RefusalFrontier T8 (the chain and its three structure theorems); the pair-separation closure policy from the first checkpoint; what an observation regime/profile is.
- Substantive: the three profile classes, `depth1_obstructions_are_exactly_middle_pairs`, `generation_never_dries`, `automark_presence_vacuous`, `finite_marks_outrun`, `valued_marks_collapse_generation`, `depth2_separates_near_ends_n4` + `depth2_obstruction_n5`, `middle_swap_not_relation_preserving` (with its nonclaim). Auxiliary: `reflective_chain_tags`, the three `chain_*_iff`, `le_foldr_max`.
- Lesson title: "A demand that never stops, and the three ways to pay." Question answered: under depth-1 observation of the reflective chain, which pairs can never be told apart, and what each declared repair costs.
- Recommend omitting: `le_foldr_max` (library-grade); possibly `valued_marks_collapse_generation` as a theorem (its content is definitional — the index is in the profile — and is better taught as one sentence).

## 11. Interpretation findings

1. `generation_never_dries` — paper TERMINAL/FG4: "the composite always has a live obstruction ... fires at every round from the third on, forever, and the only event consumed is the internally enabled reflection"; header: "the first horizon-free challenge generator exhibited in the development, with no per-round external act". Lean: `∀ n ≥ 3, profile1 (reflState n) 1 = profile1 (reflState n) 2`. "Forever" is a metatheoretic `∀ n` over a `Nat`-indexed family of states; nothing in the system holds the totality. The paper's scoping ("self-continuation relative to those declarations, not absolute self-origination"; `OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE`) is adequate. Finitude flag only; no defect.
2. `finite_marks_outrun` — docstring: "a per-pair repair strategy is called again — and again, each call consuming a fresh import. Repair by per-pair marking never becomes endogenous." Lean: for any fixed finite list of marked indices, some larger chain has an unmarked interior pair. The dynamic reading (a strategy that keeps adding marks still imports every firing round) is Python (`repair_per_pair`, 15 rounds); the theorem shows only that no finite marking is final. Classification: INTERPRETATION DEFECT (minor; the docstring narrates the trajectory, the Lean states the static outrun).
3. `valued_marks_collapse_generation` — "every pair separates and no obstruction ever arises". Lean: `profileV` contains the index, so distinct indices give distinct profiles by `congrArg Prod.snd`. True by construction and acknowledged ("identity-grade observation"); vacuity check: the theorem is content-free relative to its regime. Not a defect; a textbook note.
4. `middle_swap_not_relation_preserving` — paper FG7 and ledger `CL-G-DIRECT-SWAP` state the nonclaim explicitly ("not a quantified automorphism theorem"). No defect.
5. Depth 2 — paper FG6: "depth 2 ... outrun in the deep interior ... fires unrepaired from length 5 within bounds". Lean: two instances (`n = 4`, `n = 5`). The structural statement is deferred to `SeparationCapacity`; the general-`n` link between `profile2` and `profileD` is recorded OPEN in the paper (G2 residual). No defect.
6. Vacuity: hypotheses `3 ≤ n`, `1 ≤ n`, `2 ≤ n` are satisfiable; none vacuous.
