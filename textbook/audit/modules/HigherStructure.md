# Audit: HigherStructure

| field | value |
|---|---|
| Path | lean4/Derivation/HigherStructure.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 5a14d7c157e19680 |
| Lines | 816 (inventory counts 817 with trailing newline) |
| Imported by root `Derivation.lean` | yes (line 33) |
| Imports | Derivation.PrimitivePassage |
| Declarations | 32 def, 1 structure (`Complex`), 1 inductive (`CEvent`), 39 theorems (the inventory's 40 includes the spurious token `instantiated` from the docstring at line 393, "the two-rule theorem instantiated at ..."; it is not a declaration) |
| Axiom reports in `artifacts/lean_axioms.txt` | 37 lines; axioms seen: none, propext, {propext, Quot.sound}. Not in artifact: `pstep_assert`, `assert_guard` |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module asks what structure is built once the primitive passage (`PrimitivePassage`: occurrences, asserted and retained witnessed differences, protection, a declared observation, obstruction, repair/extension responses) is iterated. Part 1 defines a deterministic driver `growHist` that, round by round, supplies one new occurrence and one witnessed difference to its predecessor, protects it, funds one unit of budget, and executes the extension response `addCol [k+1]`; the grown state is characterized at every stage as the path graph on the admitted occurrences with one singleton observation column per edge (`graphAt_spec`), and each round is shown to pass through an active obstruction (`round_obstruction`), a nonempty response family (`round_two_rule`), a resolution landing on the next characterized state (`round_resolution`), and quiescence (`graphAt_quiescent`). Parts 2–3 declare a separate cell calculus (`Complex`, `CEvent`, `cstep`) in which a 2-cell or 3-cell is admitted only over a complete, unfilled boundary of lower cells; the four-occurrence demonstration complex `k4` is grown on top of the passage-grown K4 skeleton, and it is shown that the boundary guard refuses an incomplete boundary and that a complete boundary does not fill itself. Part 4 computes, on that one concrete complex, an alternating cell-count statistic (`altNum`), a count of two-block observer cuts on carriers 2–4 (`cutCensus`), and the vanishing of the composite of two declared integer boundary maps (`d2_zero_triangles`, `d2_zero_tet`), together with a second boundary convention that also works (`boundary_not_forced`). The module's own thesis is that the first graph is a *driver-supplied* path on which the obstruction creates only observation columns, and that nothing above dimension one is forced by the passage: cells, coefficients and boundary signs enter by declaration.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `growBlock` | 72 | def | The events of round `k`: round 0 admits occurrence 0; round 1 admits occurrence 1, asserts/admits/protects `(0,1)`, declares the observation, sets budget 1, adds column `[0]`; round `k+2` admits `k+2`, asserts/admits/protects `(k+1,k+2)`, sets budget 1, adds column `[k+1]`. | ADMITTED (declared driver policy; the graph data is supplied, not derived) |
| `growHist` | 80 | def | Concatenation of `growBlock 0 .. k`. | ADMITTED |
| `graphAt` | 85 | def | `replayP (growHist k) genesisP`. | ADMITTED (a `Nat → PState` family; metatheoretic indexing) |
| `pathState` | 91 | def | The claimed shape of stage `k+1`: occ `0..k+1`, asserted = wit = prot = `[(i,i+1)]`, obs = singleton columns `[[i]]`, budget 0, licensed, no refusals, not halted. | ADMITTED |
| `g1`, `gA`, `g2`, `preCol`, `g3` | 248, 257, 263, 271, 287 | def | Intermediate states inside round `m+2` (after admission; after assertion; after retention; after protection and funding; after protection unfunded). | ADMITTED (proof scaffolding) |
| `Complex` | 555 | structure | Four lists of cells: vertices, oriented edges, oriented triangles, oriented tetrahedra. | ADMITTED (declared realization layer) |
| `emptyComplex` | 562 | def | All four lists empty. | ADMITTED |
| `shell1` | 565 | def | Both endpoints present, distinct, edge absent. | ADMITTED (declared guard) |
| `edgeIn` | 569 | def | `(i,j) ∈ c1`. | ADMITTED |
| `shell2` | 574 | def | Edges `ij, jk, ik` present, triangle absent. | ADMITTED (declared guard) |
| `triIn` | 578 | def | `(i,j,k) ∈ c2`. | ADMITTED |
| `shell3` | 583 | def | Four faces present, tetrahedron absent. | ADMITTED (declared guard) |
| `CEvent` | 587 | inductive | `addV`, `addE`, `addT`, `addQ`. | ADMITTED |
| `cstep` | 597 | def | Guarded admission: dedup for vertices, `shell1/2/3` for higher cells; inert otherwise. | ADMITTED (declared policy) |
| `creplay` | 609 | def | `foldl cstep`. | ADMITTED |
| `k4PassageHist` | 664 | def | `growHist 3` followed by assertion/retention/protection of the three chords `(0,2),(1,3),(0,3)`. | ADMITTED |
| `k4Events` | 684 | def | 4 vertices, 6 edges, 4 triangles, 1 tetrahedron, in that order. | ADMITTED |
| `k4` | 691 | def | `creplay k4Events emptyComplex`. | ADMITTED |
| `k4Boundary` | 693 | def | Replay of the first 14 events (no tetrahedron). | ADMITTED |
| `altNum` | 722 | def | `|c0| − |c1| + |c2| − |c3|` as an `Int`. | ADMITTED (a declared statistic) |
| `subsetsOf` | 737 | def | All sublists of a list. | ADMITTED |
| `cutCensus` | 745 | def | Number of subsets `A ⊆ range n` with `a ∈ A`, `b ∉ A`. | ADMITTED |
| `bd1`, `bd2`, `bd2'`, `bd3` | 765, 768, 772, 775 | def | Declared integer boundary assignments of an edge, triangle (two conventions), tetrahedron. | ADMITTED (declared convention) |
| `push1`, `push2` | 780, 783 | def | Pushforward of a chain through `bd1`/`bd2`. | ADMITTED |
| `coeffV`, `coeffE` | 787, 790 | def | Coefficient of a vertex / edge in a chain. | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `grow_fresh` | 101 | `m+2 ∉ range (m+2)`. | FROZEN | propext, Quot.sound | A |
| `grow_wit_not_mem` | 105 | `(m+1,m+2)` is not among the pairs `(i,i+1)`, `i < m+1`. | FROZEN | propext, Quot.sound | A |
| `grow_col_not_mem` | 114 | `[m+1]` is not among the singleton columns `[i]`, `i < m+1`. | FROZEN | propext, Quot.sound | A |
| `grow_cols_blind` | 126 | Every old singleton column `[i]`, `i < m+1`, fails to separate `m+1` from `m+2`. | FROZEN | propext, Quot.sound | A |
| `grow_col_separates` | 144 | `[m+1]` separates `m+1` from `m+2`. | FROZEN | propext, Quot.sound | A |
| `grow_pair_separated` | 156 | `[i]` separates `i` from `i+1`. | FROZEN | propext, Quot.sound | A |
| `grow_zero` | 168 | The declared observation of stage `m` has zero relation on `(m+1,m+2)`. | FROZEN | propext, Quot.sound | A |
| `pstep_admit` | 187 | If not halted and `t ∉ occ`, `step s (admitOcc t)` appends `t`. | CONDITIONAL: `s.halted = false`, `t ∉ s.occ` | propext, Quot.sound | A |
| `pstep_assert` | 194 | If not halted and the assert guard holds, `step` appends to `asserted`. | CONDITIONAL: halted = false, guard | not in artifact | A |
| `pstep_wit` | 203 | If not halted and the retention guard holds, `step` appends to `wit`. | CONDITIONAL: halted = false, guard | propext, Quot.sound | A |
| `pstep_prot` | 211 | If not halted and the protection guard holds, `step` appends to `prot`. | CONDITIONAL: halted = false, guard | propext, Quot.sound | A |
| `pstep_budget` | 219 | If not halted, `setBudget n` sets the budget. | CONDITIONAL: halted = false | propext, Quot.sound | A |
| `pstep_addCol` | 224 | If not halted, obs declared, and `colOk ∧ licensed ∧ 0 < budget`, `addCol c` appends `c` and decrements the budget. | CONDITIONAL: halted = false, `obs = some cols`, guard | propext, Quot.sound | A |
| `colOk_some` | 236 | Unfolds `colOk` when `obs = some cols`. | CONDITIONAL: `s.obs = some cols` | propext, Quot.sound | A |
| `grow_len` | 282 | `(range (m+2) ++ [m+2]).length = m+3`. | FROZEN | propext | A |
| `assert_guard` | 298 | The assert guard holds at `g1 m` for `(m+1,m+2)`. | FROZEN | not in artifact | A |
| `wit_guard` | 313 | The retention guard holds at `gA m`. | FROZEN | propext, Quot.sound | A |
| `prot_guard` | 333 | The protection guard holds at `g2 m`. | FROZEN | propext, Quot.sound | A |
| `reach_preCol` | 350 | Replaying the first five events of round `m+2` on `pathState m` gives `preCol m`. | FROZEN | propext, Quot.sound | A |
| `round_obstruction` | 381 | `obstP (preCol m) (m+1) (m+2) = true` for every `m`. | FROZEN | propext, Quot.sound | S |
| `round_two_rule` | 395 | `[m+1] ∈ extensionProposals (preCol m) (m+1) (m+2)` for every `m` (via `extension_always_available`). | FROZEN | propext, Quot.sound | S |
| `round_resolution` | 406 | `step (preCol m) (addCol [m+1]) = pathState (m+1)`. | FROZEN | propext, Quot.sound | S |
| `round_creation_record` | 469 | The last event of `growBlock (m+2)` is `addCol [m+1]` (by `rfl`). | FROZEN (definitional) | none | A |
| `graphAt_spec` | 476 | `graphAt (k+1) = pathState k` for every `k` (induction; base by `decide`). | FROZEN | propext, Quot.sound | S |
| `graph_growth` | 495 | Stage `k+1` has `k+2` occurrences and `k+1` retained witnesses. | FROZEN | propext, Quot.sound | S |
| `graphAt_quiescent` | 510 | At stage `k+1` no protected pair is obstructed. | FROZEN | propext, Quot.sound | S |
| `path_connectivity_residue` | 536 | `|occ| − |wit| = 1` at every stage `k+1`. | FROZEN | propext, Quot.sound | S (weak) |
| `ladder_dim2` | 616 | If `shell2 C i j k`, then `addT i j k` admits the triangle and changes `C`. | CONDITIONAL: `shell2 C i j k = true` (over all `C`) | propext, Quot.sound | S |
| `ladder_dim3` | 635 | Same at dimension 3 under `shell3`. | CONDITIONAL: `shell3 = true` | propext, Quot.sound | S |
| `shell_guard_load_bearing` | 654 | On `⟨[0,1,2],[(0,1)],[],[]⟩`, `addT 0 1 2` is inert. | VERIFIED_FINITE (countermodel to "incomplete boundaries fill") | propext, Quot.sound | S |
| `k4_skeleton_from_passage` | 672 | Replaying `k4PassageHist` yields wit = prot = the six K4 edges, all unobstructed. | VERIFIED_FINITE | propext, Quot.sound | S |
| `k4_builds` | 699 | `k4` equals the listed four-vertex complex with 6 edges, 4 triangles, 1 tetrahedron. | VERIFIED_FINITE | propext, Quot.sound | S |
| `k4_skeleton_agrees` | 708 | `k4.c1` equals the passage witness store of `k4PassageHist`. | VERIFIED_FINITE | propext, Quot.sound | S |
| `filling_not_forced` | 714 | `shell3 k4Boundary 0 1 2 3 = true` and `k4Boundary.c3 = []`. | VERIFIED_FINITE (countermodel to "a complete boundary fills itself") | propext, Quot.sound | S |
| `altNum_stages` | 730 | `altNum` is 4, −2, 2, 1 after vertices, edges, faces, solid. | VERIFIED_FINITE | propext, Quot.sound | S |
| `cut_census_growth` | 752 | `cutCensus 2 0 1 = 1`, `cutCensus 3 0 1 = 2`, `cutCensus 4 0 1 = 4`. | VERIFIED_FINITE | propext, Quot.sound | S |
| `d2_zero_triangles` | 796 | For every triangle of `k4` and every vertex, the coefficient of the composite boundary is 0. | VERIFIED_FINITE | propext, Quot.sound | S |
| `d2_zero_tet` | 801 | For every edge of `k4`, the coefficient of the composite boundary of the tetrahedron is 0. | VERIFIED_FINITE | propext, Quot.sound | S |
| `boundary_not_forced` | 808 | `bd2 ≠ bd2'` on `(0,1,2)`, and both have vanishing composite on every vertex of `k4`. | VERIFIED_FINITE (countermodel to "the boundary convention is determined by the graph") | propext, Quot.sound | S |

## 4. External and admitted assumptions

- Structures: `PState`, `PEvent`, `step`, `replayP`, `obstP`, `colOk`, `extensionProposals` from `PrimitivePassage` (all admitted definitions there). `Complex`, `CEvent`, `cstep` are new declared packaging.
- Library lemmas doing work: `List.mem_range`, `List.mem_map`, `List.range_succ`, `List.map_append`, `List.any_eq_true`, `decide_eq_true/false`, and `PrimitivePassage.obst_agrees_when_declared`, `replay_append`, `extension_always_available`. The induction in `graphAt_spec` has base case `decide` on a concrete state.
- Recurring hypotheses: `halted = false` plus the event's own guard in every `pstep_*` lemma; `shell2/shell3 = true` in the two ladder theorems.
- Unearned identity: none found in the Lean. The docstring (lines 25–27, 543–545) asserts "a witnessed binary relation *is* a directed graph presentation — identity, not force". No theorem states this; it is a reading of the `wit` field as an edge list. The only proved link is `k4_skeleton_agrees`, on one concrete complex.
- Unrestricted external universe: `Complex` fields are `List Nat`-based; `cutCensus` enumerates all `2^n` sublists of `range n` (metatheoretic enumeration over a declared finite carrier). None found beyond that.
- Unbounded function treated as internally available: `graphAt : Nat → PState` and the ∀`k` statements (`graphAt_spec`, `graph_growth`, "grows without bound", line 493) are metatheoretic. Each stage is a finite state; the system never holds the family. Flagged under Finitude (see §11).
- Silently assumed observer: the driver *declares* the observation (`declareObs` in round 1) and funds each column (`setBudget 1`); `obstP` is read only after declaration. No observer is assumed beyond that declared event; but note the driver, not the passage, supplies the budget.
- Unspecified correspondence between presentations: `k4_skeleton_agrees` identifies `k4.c1` (a cell list) with `wit` (a passage field) by literal list equality — the correspondence is positional identity of `Nat` labels, declared by construction of `k4Events`. Not a general bridge.
- Cost function without justification: `setBudget 1` per round is a declared self-funding policy (the paper says so: "declared self-funding policy, not derived resource availability", primitive_difference_passage.md).
- Admitted condition later described as forced: the module's docstring is careful ("admitted, never forced"). See §11 for the one place ("stage-invariant") where the docstring overreads.
- Finite computation presented as universal: `cut_census_growth` docstring says "the branching is real and grows with the carrier" from three values (n = 2, 3, 4); the ledger (CL-PD2-CATS) limits it to "carriers 2-4 only" and names carrier 5 as a Python computation. `d2_zero_*` are proved on `k4` only; the general theorem is in `BoundaryCancellation`.

## 5. Derived consequences

- The `pstep_*` step lemmas are reused by `Attachment.lean` (lines 194–232, 798–824: `pstep_admit`, `pstep_assert`, `pstep_wit`, `pstep_prot`) and `GraphGenesis.lean` (line 626: `pstep_budget`).
- `growHist`/`pathState`/`graphAt_spec` underlie the K4 demonstration here; `Attachment.lean` builds its own tree driver rather than reusing `growHist`.
- `LadderGeneral` imports this module but uses none of its declarations (checked: no `HigherStructure.` reference and no `open HigherStructure` in LadderGeneral.lean); the import orders the modules.
- Ledger entries: CL-PD2-GROWTH (all eight growth theorems), CL-PD2-LADDER (the ten cell-calculus theorems), CL-PD2-CATS (`cut_census_growth`). `paper/primitive_difference_passage.md` §"The passage feeding the growth" narrates `graphAt_spec` and the round theorems.

## 6. Counterexamples and limitations

- Countermodels: `shell_guard_load_bearing` (an incomplete boundary is not filled), `filling_not_forced` (a complete boundary with the solid cell absent is a legal state: the horn does not fill itself), `boundary_not_forced` (two distinct sign conventions both give vanishing composite, so the convention is not determined by the graph).
- Not proved: that the driver's path is the *only* lawful growth (no uniqueness or necessity theorem; `growBlock` is one declared policy); that the horn conditions `shell2/shell3` are instances of the passage's `obstP` (no theorem connects `Complex` to `PState` beyond the one list equality `k4_skeleton_agrees`; the "same obstruction shape at every dimension" is an analogy stated in prose); connectedness or acyclicity of the grown graph from the residue alone (the ledger says this explicitly; the shape comes from `graphAt_spec`); any general `d² = 0` (only `k4`); any statement about `altNum` being invariant (it changes 4 → −2 → 2 → 1).
- `round_two_rule` shows one proposal is available; it does not show the driver's choice `addCol [m+1]` is the only one (indeed `repairFamily` may also be nonempty; not checked).

## 7. Axiom dependencies

All 37 reported theorems use at most {propext, Quot.sound}; `round_creation_record` uses none; `grow_len` uses propext only. None exceed the whitelist. `pstep_assert` and `assert_guard` have no `#print axioms` line (not in `Derivation.lean`'s inventory); they are auxiliary and are used inside `reach_preCol`, whose report is clean, so transitively they cannot exceed the whitelist.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). 37 of 39 theorems appear in `artifacts/lean_axioms.txt` (lines for `Derivation.lean:621–657`). The ledger cites 19 of them by name (CL-PD2-GROWTH, CL-PD2-LADDER, CL-PD2-CATS). Probe run: none specific to this module (the `decide` theorems were accepted by the build; the vacuity probe for the related `LadderGeneral.d2_zero_dims_2_3_4` is recorded in that module's record, and its check of `HigherStructure`'s own `d2_zero_*` statements by reading confirms they test the correct dimension: `coeffV` on vertices for `push1 ∘ bd2`, `coeffE` on edges for `push2 ∘ bd3`).

## 9. Related Python implementations

- `code/derivation/primitive_passage.py`: `grow_block`, `grow_hist`, `path_state`, `k4_passage_hist`, `growth_report` (growth mirrored to 15 rounds per the ledger).
- `code/derivation/higher_structure.py`: `Complex`, `shell1/2/3`, `cstep`, `creplay`, `k4_events`, `k4`, `k4_boundary`, `alt_num`, `subsets_of`, `cut_census`, `bd1`, `bd2`, `bd2_neg`, `bd3`, `push1`, `push2`, `coeff_v`, `coeff_e`, `d2_zero_triangles`, `d2_zero_tet`, `boundary_not_forced`.
- Tests: `tests/test_higher_structure.py` (`test_k4_builds_in_creation_order`, `test_horn_guards_load_bearing`, `test_alt_num_stages`, `test_cut_census` (carriers 2–5), `test_boundary_calculus`, `test_d2_zero_fails_for_broken_convention`).

## 10. Textbook placement proposal

- Prerequisites: the passage state and its events (`PState`, `step`, `replayP`); active obstruction `obstP` and its four gates; the two-rule response (`extension_always_available`); the meaning of `sepCol` / singleton columns.
- Substantive: `round_obstruction`, `round_two_rule`, `round_resolution`, `graphAt_spec`, `graphAt_quiescent` (the round as a theorem schema); `ladder_dim2/3` with `shell_guard_load_bearing` and `filling_not_forced` (admitted, guarded, never self-filling); `boundary_not_forced` (declared content). `k4_builds`, `k4_skeleton_agrees`, `altNum_stages`, `cut_census_growth`, `d2_zero_triangles/tet` are worked-example computations.
- Auxiliary: `grow_*`, `pstep_*`, `colOk_some`, `grow_len`, `*_guard`, `reach_preCol`, `round_creation_record`, `graph_growth`, `path_connectivity_residue`.
- Lesson title: "One round of the passage, run forever: the first graph is supplied, its observer is created." Question answered: what, exactly, does an obstruction create when the driver already supplied the edge?
- Recommend omitting from the textbook: `altNum` and `altNum_stages` (a statistic on one example, with a docstring that calls it an invariant; nothing is proved about it), and `path_connectivity_residue` as a standalone claim (it is a corollary of `graph_growth` and proves neither connectedness nor acyclicity). Teach `cutCensus` only as a finite count on carriers 2–4 with the general growth left open.

## 11. Interpretation findings

1. **`altNum_stages` — INTERPRETATION DEFECT (docstring).** Module docstring lines 48–50: "the *occurrence alternation number* `altNum` — the alternating sum of cell counts, which the declared boundary calculus turns into a stage-invariant of the growth". Lean: `altNum` takes the values 4, −2, 2, 1 along the stages; no theorem relates `altNum` to the boundary calculus at all. The ledger (CL-PD2-LADDER) already corrects this: "a statistic, not an invariant". Smallest counterexample: stages 1 and 2 of the demonstration, values 4 and −2.
2. **`ladder_dim2`, `ladder_dim3` — INTERPRETATION DEFECT (docstring, mild).** Docstring lines 612–615 and 547–553: "a complete unfilled boundary is the dimension-2 obstruction ... the two-rule shape, one dimension up ... the recorded process responsible for every cell created below." Lean: under `shell2 C i j k = true`, `cstep` appends the triangle and the complex changes — a near-definitional unfolding of the declared `cstep`. No theorem connects `shell2` to `obstP`, `prot`, or any passage notion; the "obstruction shape" is a declared analogy. The ledger states the recurrence is "PROVED at dimensions 2 and 3", which is accurate for the guarded-step reading; the textbook should not present it as a theorem that the passage's obstruction recurs in dimension 2.
3. **`graph_growth` — Finitude flag.** Docstring line 493: "The first graph grows without bound". Lean: `∀ k, (graphAt (k+1)).occ.length = k+2`. The quantifier over `Nat` is metatheory; each `graphAt k` is a finite state and no state contains the family. Same for `graphAt_spec` ("at every horizon"). INTERPRETATION note, not a defect in the ledger (which says "theorem (horizon-free), mirrored to 15 rounds").
4. **`cut_census_growth` — INTERPRETATION DEFECT (docstring, scoped by ledger).** Docstring lines 749–751: "the branching is real and grows with the carrier." Lean: three values at `n = 2, 3, 4`. The ledger correctly scopes it to "carriers 2-4 only". No general growth theorem exists in Lean.
5. **Docstring claim "a witnessed binary relation *is* a directed graph presentation — identity, not force" (lines 25–27, 543–545).** No Lean statement. Classified as prose-only; it is a reading of the `wit : List (Nat × Nat)` field, not a theorem. Not a defect in any ledger entry (the ledger does not cite it), but a lesson must not present it as proved.
6. Vacuity check: `ladder_dim2/3` hypotheses are satisfiable (`k4Boundary` satisfies `shell3`, `filling_not_forced`); conclusions are non-trivial (strict change). `pstep_*` lemmas have satisfiable hypotheses (used in `reach_preCol`). No vacuous theorem found in this module. The `d2_zero_triangles` / `d2_zero_tet` checks test coefficients in the correct dimension (unlike the first two conjuncts of `LadderGeneral.d2_zero_dims_2_3_4`, see that record).
