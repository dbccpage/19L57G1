# Audit: Attachment

| field | value |
|---|---|
| Path | lean4/Derivation/Attachment.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 39f7001b5e1b1fbe |
| Lines | 1172 (inventory records 1173) |
| Imported by root `Derivation.lean` | yes (line 37) |
| Imports | Derivation.HigherStructure (and through it PrimitivePassage, PrimDiff, PrimitiveCore) |
| Declarations | 2 structure (`LawfulPolicy`, `Renaming`), 2 inductive (`AttachOutcome`, `Reaches`), 37 def, 54 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 54 lines (every theorem); 43 `[propext, Quot.sound]`, 7 `[propext]`, 4 "does not depend on any axioms" (`par_le`, `clamp_rewrote_input`, `Renaming.f_inj`, `upFamily_grammar_uniform`) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module asks whether the passage kernel (`PState`, `step`, `replayP` of `PrimitivePassage`) can be driven to grow its carrier one occurrence at a time, and what such growth does and does not force. It fixes a four-event block `upBlock s p` (admit a fresh token, assert, admit and protect the witnessed pair from parent position `p` to the new position) and the family `upFamily s` of all such blocks, one per existing position. It proves what the kernel does when the block is replayed from a well-formed, live state (`up_exec_eq`, `up_executes`) and that nothing moves on a halted state. It introduces `LawfulPolicy`, a parent-choosing function with a bound, and shows that iterating the block along a policy builds a state whose witnessed pairs form a parent relation with exactly one parent per non-root position and every position reaching 0 (`treeAt_spec`, `parent_unique`, `all_reach`). It then supplies countermodels: a clamped policy silently rewrites its input, two lawful policies of equal cost give non-isomorphic shapes (path versus star), the star orbit under a renaming is not a singleton, and equal size or equal cost supplies no renaming law. The `Renaming n` structure (a bijection of the first `n` positions, identity above) and its action `act` on states are introduced so that the family can be shown to transport, which `RenamingStructure` and `GraphGenesis` build on.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `LawfulPolicy` | 61 | structure | `choose : Nat → Nat` with `lawful : ∀ k, choose (k+1) ≤ k`; a declared parent-selection policy | ADMITTED (declared policy; function Nat → Nat, metatheory) |
| `par` | 67 | def | `par π k = π.choose (k+1)` | ADMITTED |
| `clampedPar` | 73 | def | `min (c (k+1)) k`: an unlawful choice clamped into range | ADMITTED |
| `badChoice` | 77 | def | `i ↦ i + 7`, always out of range | ADMITTED (countermodel datum) |
| `AttachOutcome` | 92 | inductive | `attached (s : PState)` or `refusedParent (p k : Nat)` | ADMITTED |
| `natMax` | 99 | def | fold of `max` over a list | ADMITTED |
| `freshTok` | 114 | def | `natMax s.occ + 1` (0 on empty store) | ADMITTED |
| `upBlock` | 138 | def | `[admitOcc (freshTok s), assertWit p len, admitWit p len, protect p len]` with `len = s.occ.length` | ADMITTED (the Up grammar) |
| `upFamily` | 144 | def | `(range len).map (upBlock s)` | ADMITTED |
| `LegalOneEdgeExtension` | 148 | def | `∃ p < len, b = upBlock s p` | ADMITTED |
| `WFStores` | 164 | def | every pair in asserted/wit/prot has both coordinates `< s.occ.length` | ADMITTED (recurring hypothesis) |
| `upS1`..`upS4` | 172–181 | def | the four intermediate states of replaying `upBlock` | ADMITTED |
| `attachChecked` | 306 | def | if `p < len` then `attached (replayP (upBlock s p) s)` else `refusedParent p len` | ADMITTED |
| `s12` | 334 | def | a concrete state with `occ = [1, 2]` | ADMITTED (countermodel datum) |
| `Renaming n` | 367 | structure | `f g : Nat → Nat`, `fg`, `gf` (inverses), `fbound` (f maps `< n` into `< n`), `ffix` (f is identity on `≥ n`) | ADMITTED (Nat → Nat functions, metatheory) |
| `renPair` | 427 | def | apply `σ.f` to both coordinates | ADMITTED |
| `act` | 433 | def | rename a state: occ by index permutation via `getD`, pair stores by `renPair`, columns by `map σ.f`, other fields fixed | ADMITTED |
| `attachBlock`, `attachHist`, `treeAt`, `treeState` | 675–689 | def | the block at stage `k` under policy `π`, the history of `n` blocks, its replay from genesis, and the explicit closed-form state | ADMITTED (`treeAt : Nat → PState`, metatheory) |
| `t1`, `t2`, `t3` | 713–721 | def | intermediate states for the guard lemmas | ADMITTED |
| `Reaches E` | 955 | inductive | `Reaches E 0` and `Reaches E p → (p, c) ∈ E → Reaches E c` | ADMITTED |
| `pathPolL`, `starPolL`, `zigzagL` | 990–1002 | def | three lawful policies (parent `k`, parent 0, alternating) | ADMITTED |
| `path4E`, `star4E` | 1030–1032 | def | the two 4-vertex edge lists | ADMITTED |
| `tuples4`, `app4`, `edgeInU`, `isoMatch` | 1040–1055 | def | enumeration of the 24 permutations of 4 and the undirected-edge matching test | ADMITTED |
| `swap12`, `flip02`, `renamePair`, `blockAt` | 1069–1078 | def | raw (non-`Renaming`) relabelings and a block at positions | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `par_le` | 69 | `par π k ≤ k` for every lawful policy | FROZEN | none | A |
| `clamp_rewrote_input` | 84 | `clampedPar badChoice 0 = 0 ∧ badChoice 1 ≠ 0`: clamping silently replaces the offered parent | VERIFIED_FINITE (REFUTED: clamping is not a faithful reading) | none | S |
| `le_natMax_of_mem` | 101 | a list member is `≤ natMax` | FROZEN | propext | A |
| `freshTok_fresh` | 119 | `freshTok s ∉ s.occ` | FROZEN | propext, Quot.sound | S |
| `up_iff_legal` | 153 | `b ∈ upFamily s ↔ LegalOneEdgeExtension s b` | FROZEN (near-definitional: `mem_map` + `mem_range`) | propext, Quot.sound | S |
| `up_exec_eq` | 187 | under `WFStores s`, `s.halted = false`, `p < len`: `replayP (upBlock s p) s = upS4 s p` | CONDITIONAL: WFStores, live, `p < len` | propext, Quot.sound | S |
| `up_executes` | 252 | same hypotheses: the replayed state has `occ = s.occ ++ [freshTok s]`, `(p,len) ∈ asserted`, `∈ wit`, `∈ prot` | CONDITIONAL: same | propext, Quot.sound | S |
| `attachChecked_refuses` | 312 | `¬ p < len → attachChecked s p = refusedParent p len` | CONDITIONAL: `¬ p < len` | propext, Quot.sound | S |
| `unlawful_refused` | 325 | with `s.occ.length = 3`, `attachChecked s (badChoice 1) = refusedParent 8 3` | CONDITIONAL: length 3 | propext, Quot.sound | A |
| `length_not_fresh_countermodel` | 345 | on `s12`, `s12.occ.length ∈ s12.occ` while `freshTok s12 ∉ s12.occ` | VERIFIED_FINITE (REFUTED: "length is the fresh token" is false) | propext, Quot.sound | S |
| `halted_up_inert` | 354 | `s.halted = true → replayP (upBlock s p) s = s` | CONDITIONAL: halted | propext, Quot.sound | S |
| `Renaming.f_inj` | 375 | `σ.f x = σ.f y → x = y` | FROZEN | none | A |
| `Renaming.gbound` | 381 | `x < n → σ.g x < n` | FROZEN | propext, Quot.sound | A |
| `Renaming.gfix` | 391 | `n ≤ x → σ.g x = x` | FROZEN | propext, Quot.sound | A |
| `Renaming.fbound_iff` | 403 | `σ.f x < n ↔ x < n` | FROZEN | propext, Quot.sound | A |
| `getD_lt` | 414 | `i < l.length → l.getD i 0 ∈ l` | FROZEN | propext | A |
| `getD_append_lt` | 419 | `getD` of an append at an in-range index | FROZEN | propext, Quot.sound | A |
| `act_occ_length` | 444 | `(act σ s).occ.length = s.occ.length` | FROZEN | propext | A |
| `act_occ_mem` | 451 | with `n = s.occ.length`: `x ∈ (act σ s).occ ↔ x ∈ s.occ` | CONDITIONAL: `n = len` | propext, Quot.sound | A |
| `freshTok_act` | 472 | with `n = len`: `freshTok (act σ s) = freshTok s` | CONDITIONAL: `n = len` | propext, Quot.sound | A |
| `upBlock_transport` | 513 | with `n = len`: `upBlock (act σ s) (σ.f p)` equals `upBlock s p` with the parent renamed | CONDITIONAL: `n = len` | propext, Quot.sound | S |
| `upBlock_parent_inj` | 525 | `upBlock s p = upBlock s p' → p = p'` | FROZEN | propext | A |
| `upFamily_transport` | 533 | with `n = len`: `b ∈ upFamily s ↔ (renamed b) ∈ upFamily (act σ s)` | CONDITIONAL: `n = len` | propext, Quot.sound | S |
| `act_up_comm` | 561 | with `n = len`, WFStores, live, `p < len`: `act σ (replayP (upBlock s p) s) = replayP (upBlock (act σ s) (σ.f p)) (act σ s)` | CONDITIONAL: four hypotheses | propext, Quot.sound | S |
| `upFamily_grammar_uniform` | 663 | `s.occ = t.occ → upFamily s = upFamily t` | CONDITIONAL: equal occ stores | none | A |
| `attach_fresh` | 699 | `n + 1 ∉ range (n + 1)` | FROZEN | propext, Quot.sound | A |
| `attach_pair_not_mem` | 703 | `(par π n, n+1)` is not among the pairs `(par π k, k+1)` for `k < n` | FROZEN | propext, Quot.sound | A |
| `attach_len` | 726 | `(range (n+1)).length = n + 1` | FROZEN | propext | A |
| `attach_wf_guard` | 730 | the assert guard holds at stage `n` of `treeState` | FROZEN | propext, Quot.sound | A |
| `attach_wit_guard` | 747 | the admitWit guard holds | FROZEN | propext, Quot.sound | A |
| `attach_prot_guard` | 768 | the protect guard holds | FROZEN | propext, Quot.sound | A |
| `range_map_succ` | 781 | a `range`/`map` identity | FROZEN | propext | A |
| `treeAt_spec` | 791 | `treeAt π n = treeState π n` (the replay equals the closed form, for every `n`) | FROZEN | propext, Quot.sound | S |
| `natMax_append_singleton` | 837 | `natMax (l ++ [x]) = max (natMax l) x` | FROZEN | propext, Quot.sound | A |
| `natMax_range_le` | 848 | `natMax (range n) ≤ n` | FROZEN | propext, Quot.sound | A |
| `tree_occ_len` | 855 | `(treeState π n).occ.length = n + 1` | FROZEN | propext | A |
| `freshTok_treeState` | 862 | `freshTok (treeState π n) = n + 1` | FROZEN | propext, Quot.sound | S |
| `attachBlock_is_upBlock` | 879 | `attachBlock π n = upBlock (treeState π n) (par π n)`: the tree builder uses the Up grammar | FROZEN | propext, Quot.sound | S |
| `treeState_wf` | 886 | `WFStores (treeState π n)` | FROZEN | propext, Quot.sound | A |
| `attach_residue` | 903 | at every stage the asserted, witnessed and protected stores coincide (no residue) | FROZEN | propext, Quot.sound | S |
| `parent_lt` | 915 | every witnessed pair `(p, c)` of `treeState π n` has `p < c` | FROZEN | propext, Quot.sound | A |
| `parent_unique` | 925 | two witnessed pairs with the same child have the same parent | FROZEN | propext, Quot.sound | S |
| `parent_exists` | 940 | every `c` with `0 < c ≤ n` has a parent in the witnessed store | FROZEN | propext, Quot.sound | S |
| `all_reach_aux` | 959 | helper for `all_reach` by strong induction | FROZEN | propext, Quot.sound | A |
| `all_reach` | 984 | every `c ≤ n` satisfies `Reaches (treeState π n).wit c` | FROZEN | propext, Quot.sound | S |
| `path_edges` | 1011 | `(treeState pathPolL n).wit = (range n).map (k ↦ (k, k+1))` | FROZEN | propext, Quot.sound | A |
| `star_edges` | 1023 | `(treeState starPolL n).wit = (range n).map (k ↦ (0, k+1))` | FROZEN | propext, Quot.sound | A |
| `tree4_concrete` | 1034 | the two 4-vertex trees have exactly `path4E` and `star4E` as witnessed stores | VERIFIED_FINITE | propext, Quot.sound | A |
| `path4_star4_not_isomorphic` | 1063 | no permutation of 4 positions carries the undirected edges of `path4E` onto those of `star4E` (`tuples4.all (¬ isoMatch) = true`) | VERIFIED_FINITE (REFUTED: shape is not forced by cost) | propext, Quot.sound | S |
| `star_orbit_swap` | 1085 | swapping positions 1,2 of the star at stage 3 gives a different block at the same cost | VERIFIED_FINITE | propext, Quot.sound | A |
| `path_oriented_rigid` | 1102 | the oriented path is not fixed by `flip02` | VERIFIED_FINITE | propext, Quot.sound | A |
| `path_center_separate` | 1110 | positions 1 and 2 of the path have different undirected neighbourhoods from 0 and 3 | VERIFIED_FINITE | propext, Quot.sound | A |
| `equal_size_not_renaming_related` | 1130 | two concrete stores of equal size are not related by any `Renaming n` action (second conjunct quantifies over all `n`, `σ`) | REFUTED (general over σ) | propext, Quot.sound | S |
| `equal_cost_non_isomorphic_extensions` | 1160 | at stage 3, path and star are both reached by 3 blocks of 4 events yet their stores differ and are non-isomorphic | VERIFIED_FINITE (REFUTED: equal cost does not force shape) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- Structures taken as given: `PState`, `PEvent`, `step`, `replayP`, `genesisP` from `PrimitivePassage`; `LawfulPolicy` and `Renaming n` as declared data families.
- Recurring hypotheses: `WFStores s` (store-boundedness), `s.halted = false`, `p < s.occ.length`, and `n = s.occ.length` for renaming scope. All four are named in each theorem that needs them; none is discharged globally.
- Library lemmas doing real work: `List.mem_map`, `List.mem_range`, `List.getD` lemmas, `List.foldr` on `max`; decidability of `Nat` membership in lists is what lets `decide` close the finite theorems.
- Functions `Nat → X` treated as data: `LawfulPolicy.choose`, `Renaming.f/g`, `treeAt : Nat → PState`, `attachHist : Nat → List PEvent`. These are metatheoretic bookkeeping; the state never contains them. Finitude flag: `treeAt π n` for all `n` is a schema of finite states, not an infinite tree possessed by the system.
- Unearned identity: none found (the only identity theorems are `treeAt_spec`, proved by induction, and the `rfl`-level `upFamily_grammar_uniform`).
- Unrestricted external universe: none found.
- Unbounded function treated as internally available: none found beyond the flags above, which the docstrings do not misread.
- Silently assumed observer: none found; the `obs` field is carried unchanged by `upBlock` and by `act` maps it by `σ.f` only.
- Unspecified correspondence between presentations: `Renaming n` is a fully specified bijection with explicit inverse. The raw maps `swap12`, `flip02`, `collapse` (in RenamingStructure) are used only in countermodels and are not `Renaming` values.
- Cost function without justification: "cost" here is block length (4 events per block, 3 blocks). It is a count of events in a declared grammar, not a derived measure; `equal_cost_non_isomorphic_extensions` uses it only to show equal counts do not force shape.
- Admitted condition later described as forced: none found. The docstrings describe `upBlock` as a grammar and `LawfulPolicy` as a policy.
- Finite computation presented as universal: none found; `path4_star4_not_isomorphic` is stated for 4 positions and used as a countermodel only.

## 5. Derived consequences

Downstream (grep of lean4/Derivation): `GraphGenesis` uses `upFamily`, `upBlock`, `up_iff_legal`, `up_exec_eq`, `up_executes`, `halted_up_inert`, `upFamily_transport`, `upBlock_parent_inj`, `act_up_comm`, `treeAt pathPolL`, `tuples4`, `isoMatch`, `equal_cost_non_isomorphic_extensions`. `RenamingStructure` uses `Renaming`, `act`, `upBlock`, `upFamily`, `WFStores`, `getD_lt`, `act_occ_length`, `freshTok_act`, `upBlock_transport`, `upFamily_transport`, `act_up_comm`, `upFamily_length`-style facts, and restates `equal_size_not_renaming_related` and `equal_cost_non_isomorphic_extensions`. Ledger: CL-PD2-ATTACHMENT (paper/paper_claim_ledger.md lines 1762–1830) cites 28 of these theorems. Paper: primitive_difference_map.md §8; observer_inventory.md notes that `up_iff_legal` is one-edge supply, not a reversal map.

## 6. Counterexamples and limitations

- `clamp_rewrote_input`: refutes "clamping an out-of-range parent is harmless"; witness `badChoice 1 = 8`, clamped to 0.
- `length_not_fresh_countermodel`: refutes "the store length is a fresh token"; witness `s12.occ = [1, 2]`.
- `path4_star4_not_isomorphic`, `equal_cost_non_isomorphic_extensions`: refute "equal cost forces one shape"; witnesses path and star on 4 positions.
- `equal_size_not_renaming_related`: refutes "equal size implies renaming-related".
- `star_orbit_swap`: the star's blocks at stage 3 are not a single orbit point.
- Not proved: that `attachChecked`'s `attached` branch strictly extends the state. Only the refusal branch has a theorem; `attachChecked` does not check `WFStores` or liveness, so on an ill-formed or halted state its `attached` value can equal `s` (`halted_up_inert`). The ledger does not claim otherwise, but a reader of `attachChecked` alone could think `attached` means "grew".
- Not proved: a single predicate "is a tree". The tree content is spread over `parent_lt`, `parent_unique`, `parent_exists`, `all_reach`, `attach_residue`; no `IsTree` definition exists in Lean (the Python `is_tree` does).
- `up_iff_legal` is completeness relative to a grammar defined by the same `upBlock`; it says nothing about blocks outside that grammar.

## 7. Axiom dependencies

All 54 artifact lines lie within `{propext, Quot.sound}`: 43 use both, 7 use `propext` alone, 4 use none (`par_le`, `clamp_rewrote_input`, `Renaming.f_inj`, `upFamily_grammar_uniform`). None exceeds the whitelist.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 54 theorems appear in the axiom artifact. The paper ledger CL-PD2-ATTACHMENT cites 28 of them; paper/primitive_difference_map.md §8 and paper/paper_change_log.md lines 674–690 discuss the module. No probe was run for this module.

## 9. Related Python implementations

code/derivation/attachment_ladder.py: `lawful_to`, `par`, `clamped_par`, `bad_choice`, `clamp_countermodel`, `attach_checked`, `fresh_tok`, `up_block`, `up_family`, `length_not_fresh_countermodel`, `attach_block`, `attach_hist`, `tree_at`, `tree_state`, `path_pol`, `star_pol`, `zigzag_pol`, `is_tree`, `tree_report`, `undirected`, `isomorphic_undirected`, `shape_report`, `up_report`, `act`, `renaming_report`, `store_automorphisms`, `parent_orbits`. tests/test_attachment_ladder.py: `test_no_clamping_typed_refusal`, `test_tokens_positions_freshness`, `test_up_family_registry_iff`, `test_every_policy_yields_spec_trees`, `test_shape_not_forced`, `test_renaming_action_and_countermodels`, `test_tree_report_bounds`, `test_is_tree_negatives`, `test_act_maps_observation_columns`, plus runner tests.

## 10. Textbook placement proposal

- Prerequisites: `PState` and its guards (`PrimitivePassage`), `replayP`, the meaning of `WFStores`, and the distinction between proposing a block and executing it.
- Substantive: `upBlock`/`upFamily`/`up_iff_legal` (the one-edge grammar); `up_executes` and `halted_up_inert` (what execution does and when it does nothing); `treeAt_spec` with `parent_unique`, `parent_exists`, `all_reach`, `attach_residue` (iterated attachment yields a parent structure); `equal_cost_non_isomorphic_extensions` and `path4_star4_not_isomorphic` (cost does not force shape); `act_up_comm` (the grammar is renaming-covariant). Auxiliary: all `getD`, `natMax`, `range` lemmas, the guard lemmas, `t1`–`t3`, `upS1`–`upS4`.
- Lesson title: "Growing the carrier by one: proposals, parents, and why cost does not pick a shape." Question answered: when the kernel is asked to attach one fresh occurrence to an existing position, what is forced (freshness, one parent, reachability of the root) and what is not (which shape).
- Recommend omitting from the textbook: `zigzagL` (defined, never used in a theorem), `swap12`/`flip02`/`renamePair`/`blockAt` (used only inside three finite checks; a lesson can state the checks without them), `unlawful_refused` (a special case of `attachChecked_refuses`).

## 11. Interpretation findings

- "Attachment point" check (requested): the module has no declaration named "attachment point". The parent position `p` in `upBlock s p` is the only candidate. It appears in a proposal (`upFamily` is a list of event blocks; nothing in the module executes a block except the explicitly separate `replayP`/`attachChecked`/`treeAt`). This is consistent with the project note that attachment points are proposals only; the Lean does not contradict it. No defect.
- `up_iff_legal` (line 153): docstring and ledger call the family "complete". The theorem is `b ∈ upFamily s ↔ ∃ p < len, b = upBlock s p`, and `LegalOneEdgeExtension` is defined by the same `upBlock`. The proof is `mem_map` and `mem_range`. Completeness is relative to the module's own grammar. The ledger says "REGISTRY-RELATIVE", so no defect; a textbook must not read it as "every legal one-edge extension of the kernel is in the family".
- `attachChecked` (line 306): the name suggests a checked attachment, but only the parent bound is checked; `WFStores` and liveness are not, and `attached s` can be returned with `s` unchanged (halted case, `halted_up_inert`). Classified INTERPRETATION DEFECT (naming), small: the ledger wording "typed refusal" is correct for the refusal branch; nothing is claimed for the attached branch. Missing hypothesis if one wanted "attached means grew": `WFStores s ∧ s.halted = false`.
- `equal_size_not_renaming_related` (line 1130): first conjunct is a `decide` on concrete lists, second conjunct is general over `n` and `σ`. Both checked; neither vacuous. No defect.
- Finitude flags: `LawfulPolicy.choose : Nat → Nat` and `treeAt : Nat → PState` are metatheoretic schemata. The docstrings speak of "every stage" and "every n"; this is a statement about the family of finite states indexed by `n`, not about an infinite tree inside the system. No prose in paper/ was found reading it otherwise (grep for "infinite tree", "unbounded tree": none).
- Vacuity check: `up_exec_eq`, `up_executes`, `act_up_comm` have satisfiable hypotheses (genesis-reachable `treeState π n` satisfies them by `treeState_wf`, `tree_occ_len`); `halted_up_inert` is a genuine implication, not vacuous. None vacuous.
- No theorem in the module reads as "forced", "necessary", "universal" or "canonical" in its Lean statement; the only such words in docstrings are negations ("shape is not forced"), and the Lean matches.
