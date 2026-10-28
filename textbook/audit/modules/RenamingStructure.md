# Audit: RenamingStructure

| field | value |
|---|---|
| Path | lean4/Derivation/RenamingStructure.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 9600c8c7fc5f6263 |
| Lines | 483 |
| Imported by root `Derivation.lean` | yes (line 41) |
| Imports | Derivation.Attachment (and through it HigherStructure, PrimitivePassage) |
| Declarations | 5 def (`idRen`, `invRen`, `compRen`, `collapseMap`, `rawRenamePairs`), 28 theorems; no new structure (inventory's "1 structure" is the word in the docstring at line 10) |
| Axiom reports in `artifacts/lean_axioms.txt` | 28 lines (every theorem); 23 `[propext, Quot.sound]`, 1 `[propext]` (`upFamily_length`), 4 none (`Renaming.ext`, `comp_id`, `id_comp`, `comp_assoc`) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module takes the `Renaming n` structure and its action `act` on passage states from `Attachment` and asks what algebraic structure they have and what that structure does to the one-edge supply family `upFamily`. It proves that identity, inverse and composition of renamings satisfy the expected laws (with `Renaming.ext` as the extensionality principle), that `act` respects identity and composition within the scope `n ≤ s.occ.length`, that `upBlock`, `upFamily` and the transport statement of `Attachment` compose and respect identity, and that the commutation `act_up_comm` iterates. It then shows the family carries the whole orbit of a parent under a renaming (nothing in the family selects a representative), and closes with countermodels: a collapsing map is not a renaming and its raw push-forward breaks well-formedness; equal size and equal cost supply no renaming law (restated from `Attachment`). The docstring says the vocabulary ("group", "action", "equivariant") is attached only at the end, after the laws are proved; the Lean matches this order.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `idRen n` | 57 | def | the identity renaming (`f = g = id`) | ADMITTED |
| `invRen σ` | 67 | def | the renaming with `f` and `g` swapped | ADMITTED |
| `compRen σ τ` | 76 | def | `f = σ.f ∘ τ.f`, `g = τ.g ∘ σ.g` | ADMITTED |
| `collapseMap` | 371 | def | `fun _ => 0` | ADMITTED (countermodel datum) |
| `rawRenamePairs f l` | 389 | def | map `f` over both coordinates of each pair, for an arbitrary `f : Nat → Nat` | ADMITTED (countermodel apparatus) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `Renaming.ext` | 48 | two renamings with equal `f` and equal `g` are equal | FROZEN | none | A |
| `comp_id` | 90 | `compRen σ (idRen n) = σ` | FROZEN | none | S |
| `id_comp` | 94 | `compRen (idRen n) σ = σ` | FROZEN | none | S |
| `comp_assoc` | 98 | `compRen (compRen σ τ) ρ = compRen σ (compRen τ ρ)` | FROZEN | none | S |
| `inv_comp` | 102 | `compRen (invRen σ) σ = idRen n` | FROZEN | propext, Quot.sound | S |
| `comp_inv` | 107 | `compRen σ (invRen σ) = idRen n` | FROZEN | propext, Quot.sound | S |
| `inv_inv` | 112 | `invRen (invRen σ) = σ` | FROZEN | propext, Quot.sound | A |
| `map_getD_range` | 118 | `(range l.length).map (l.getD · 0) = l` | FROZEN | propext, Quot.sound | A |
| `act_id` | 129 | `act (idRen n) s = s` for every `n`, `s` (no scope hypothesis) | FROZEN | propext, Quot.sound | S |
| `act_comp` | 168 | with `n ≤ s.occ.length`: `act σ (act τ s) = act (compRen σ τ) s` | CONDITIONAL: `n ≤ len` | propext, Quot.sound | S |
| `act_inv` | 233 | with `n ≤ len`: `act (invRen σ) (act σ s) = s` | CONDITIONAL: `n ≤ len` | propext, Quot.sound | S |
| `upBlock_id` | 239 | the renamed block under `idRen` is the block | FROZEN | propext, Quot.sound | A |
| `upBlock_comp` | 244 | with `n ≤ len`: renaming a block by `τ` then `σ` equals renaming by `compRen σ τ` | CONDITIONAL: `n ≤ len` | propext, Quot.sound | A |
| `upFamily_id` | 251 | `upFamily (act (idRen n) s) = upFamily s` | FROZEN | propext, Quot.sound | A |
| `upFamily_comp` | 255 | with `n ≤ len`: `upFamily (act σ (act τ s)) = upFamily (act (compRen σ τ) s)` | CONDITIONAL: `n ≤ len` | propext, Quot.sound | A |
| `upFamily_transport_comp` | 262 | with `n = len`: the two-step transport of membership equals the one-step transport by the composite | CONDITIONAL: `n = len` | propext, Quot.sound | A |
| `upFamily_transport_id` | 270 | transport by the identity is trivial | FROZEN | propext, Quot.sound | A |
| `wf_act` | 280 | with `n = len`, `WFStores s`: `WFStores (act σ s)` | CONDITIONAL: `n = len`, WFStores | propext, Quot.sound | S |
| `act_up_comm_comp` | 312 | with `n = len`, WFStores, live, `p < len`: `act_up_comm` for `compRen σ τ` | CONDITIONAL: four hypotheses | propext, Quot.sound | S |
| `act_up_comm_twostep` | 323 | same hypotheses: applying `act_up_comm` twice equals applying it once for the composite | CONDITIONAL: four hypotheses | propext, Quot.sound | S |
| `upFamily_orbit_closed` | 342 | with `n = len` and `b ∈ upFamily s`: for every `σ`, the `σ`-image of `b` is in `upFamily (act σ s)` | CONDITIONAL: `n = len`, membership | propext, Quot.sound | S |
| `star_orbit_both_present` | 353 | at the star's stage-3 state, both the block at parent 1 and its swap-image at parent 2 are in the family | VERIFIED_FINITE | propext, Quot.sound | A |
| `upFamily_length` | 362 | `(upFamily s).length = s.occ.length` | FROZEN | propext | A |
| `collapse_not_a_renaming` | 379 | `¬ ∃ σ : Renaming 2, σ.f = collapseMap` (no renaming has a non-injective `f`) | REFUTED (collapse is not a renaming) | propext, Quot.sound | S |
| `collapse_pushforward_ill_formed` | 397 | the raw push-forward of a concrete well-formed pair store by `collapseMap` contains `(0,0)`, which `WFStores`-style distinctness forbids (statement checked by `decide` on a concrete list) | VERIFIED_FINITE (REFUTED) | propext, Quot.sound | S |
| `equal_size_supplies_no_law` | 411 | restatement of `Attachment.equal_size_not_renaming_related` | REFUTED | propext, Quot.sound | A |
| `equal_cost_supplies_no_law` | 420 | restatement of `Attachment.equal_cost_non_isomorphic_extensions` | VERIFIED_FINITE (REFUTED) | propext, Quot.sound | A |
| `equivariance_summary` | 461 | with `n = len`, WFStores, live, `p < len`: a conjunction of `act_id`, `act_comp`, `act_inv`, `upFamily_transport`, `act_up_comm`, `act_up_comm_comp` | CONDITIONAL: four hypotheses | propext, Quot.sound | S |

## 4. External and admitted assumptions

- Taken as given: `Renaming n`, `act`, `upBlock`, `upFamily`, `WFStores`, `replayP` from `Attachment`/`PrimitivePassage`.
- Recurring hypotheses: `n ≤ s.occ.length` (for `act` to be an action) and `n = s.occ.length` (for transport and commutation). Both are named wherever used; `act_id` alone is unconditional.
- Library lemmas doing real work: `List.getD` lemmas and `map_getD_range` (proved here) carry the `occ` permutation; `funext` and the structure eta in `Renaming.ext`.
- Functions `Nat → X` as data: `Renaming.f/g : Nat → Nat`. Finitude flag: a renaming is a metatheoretic bijection on positions, identity above `n`; the state never carries it, and the docstrings do not say it does.
- Unearned identity: none found; every identity is proved via `Renaming.ext` or by computation.
- Unrestricted external universe: none found.
- Unbounded function treated as internally available: none found.
- Silently assumed observer: none found; `act` maps the `obs` columns by `σ.f` explicitly.
- Unspecified correspondence between presentations: none found; the only non-`Renaming` map is `collapseMap`, used to show what fails.
- Cost function without justification: "cost" appears only in the restated `equal_cost_supplies_no_law` (block length).
- Admitted condition later described as forced: none found.
- Finite computation presented as universal: none found; `star_orbit_both_present` and `collapse_pushforward_ill_formed` are stated on concrete states.

## 5. Derived consequences

No downstream Lean module imports `RenamingStructure` (grep of lean4/Derivation: CountTransport.lean mentions `Attachment.Renaming` in a docstring only). The ledger entry CL-PD2-RENAMING-STRUCTURE (Goal 1) cites all 28 theorems; paper/paper_change_log.md line 814 records the module. Within the module, `Renaming.ext` underlies the six laws, `act_comp` underlies `act_inv` and the `*_comp` family, and `act_up_comm` (from Attachment) underlies the two iterated commutations.

## 6. Counterexamples and limitations

- `collapse_not_a_renaming`: refutes "any map of positions is a renaming"; witness `fun _ => 0` on `Renaming 2` (injectivity from `gf` fails).
- `collapse_pushforward_ill_formed`: refutes "push-forward along a non-bijection preserves well-formed stores"; witness a two-element pair store collapsing to `(0,0)`.
- `equal_size_supplies_no_law`, `equal_cost_supplies_no_law`: inherited refutations.
- Not proved: that `act` is an action on all of `PState` without the scope hypothesis. `act_comp` needs `n ≤ s.occ.length`; the docstring states this scope. No claim of a global group action is made.
- Not proved: any invariant that distinguishes orbits (the module shows orbits are carried, not how many there are); `store_automorphisms`/`parent_orbits` exist only in Python.
- `upFamily_orbit_closed`'s content is modest: since `upFamily` contains a block for every parent (`upFamily_length`, `up_iff_legal`), the renamed block is in the renamed family by `upFamily_transport`. The docstring's "carries the WHOLE orbit" is true but near-immediate; it is not a selection-freeness theorem beyond what `upFamily` already is by definition.

## 7. Axiom dependencies

All 28 artifact lines lie within `{propext, Quot.sound}`; 4 use no axioms, 1 uses `propext` alone. None exceeds the whitelist.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 28 theorems are in the axiom artifact and all are cited by the ledger entry CL-PD2-RENAMING-STRUCTURE. No probe was run for this module.

## 9. Related Python implementations

code/derivation/renaming_structure.py: `id_ren`, `inv_ren`, `comp_ren`, `group_laws`, `sample_states`, `action_laws`, `transport_laws`, `coherence`, `orbit_no_selection`, `collapse_map`, `raw_rename_pairs`, `non_bijective_countermodel`, `equal_size_countermodel`, `equal_cost_countermodel`, `renaming_report`. tests/test_renaming_structure.py: 8 tests plus the runner test.

## 10. Textbook placement proposal

- Prerequisites: the `Renaming n` structure and `act` (Attachment), `upFamily`, `act_up_comm`, and the idea of a scope hypothesis on `n`.
- Substantive: the six laws (`comp_id`, `id_comp`, `comp_assoc`, `inv_comp`, `comp_inv`), `act_id`/`act_comp`/`act_inv` with their scope, `wf_act`, `upFamily_orbit_closed`, `collapse_not_a_renaming`, `equivariance_summary` as the statement to teach. Auxiliary: `inv_inv`, `map_getD_range`, all `upBlock_*`/`upFamily_*` composition lemmas, `star_orbit_both_present`, `upFamily_length`, the two restatements.
- Lesson title: "Renamings compose, act, and move the whole supply family." Question answered: does relabelling positions commute with proposing and executing a one-edge extension, and does the family prefer any labelling? (Yes within scope; no.)
- Recommend omitting: `equal_size_supplies_no_law` and `equal_cost_supplies_no_law` (duplicates of Attachment theorems); `upFamily_transport_id` (trivial).

## 11. Interpretation findings

- Vocabulary check (requested): "group laws", "action", "equivariance" in the docstrings each name a proved property (`comp_id`, `id_comp`, `comp_assoc`, `inv_comp`, `comp_inv` are theorems proved from the four fields of `Renaming` through `Renaming.ext`; `act_id`, `act_comp`, `act_inv` are theorems). None is an admitted field. The scope restriction `n ≤ s.occ.length` on the action laws is stated in the docstrings. No defect.
- `upFamily_orbit_closed` (line 342): docstring "the family carries the WHOLE orbit of a parent, nothing selects a representative". The Lean is: for `b ∈ upFamily s` and any `σ`, the renamed `b` is in `upFamily (act σ s)`. This follows in one step from `upFamily_transport`. The prose is correct but reads as if a non-trivial selection-freeness were proved; the content is that `upFamily` lists every parent. INTERPRETATION note (mild), not a defect: the ledger wording "no selection" is accurate.
- `equivariance_summary` (line 461): a conjunction of already-proved theorems under the strongest hypothesis set. Not vacuous (hypotheses satisfied by `treeState π n` via `Attachment.treeState_wf`, `tree_occ_len`). No defect.
- Vacuity check: all `CONDITIONAL` theorems have satisfiable hypotheses (genesis-reachable tree states); `collapse_not_a_renaming` is a genuine negation. None vacuous.
- No theorem states "forced", "canonical" or "universal"; the docstring at lines 1–40 explicitly refuses to call the structure a "symmetry group of the system" before the laws are proved, and after them it uses the words only for the proved laws.
