# Audit: BoundaryCancellation

| field | value |
|---|---|
| Path | lean4/Derivation/BoundaryCancellation.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 669de56247a20536 |
| Lines | 661 (inventory counts 662) |
| Imported by root `Derivation.lean` | yes (line 43) |
| Imports | Derivation.LadderGeneral |
| Declarations | 7 def (`sumTo`, `sumFrom`, `rowTri`, `colTri`, `dterm`, `bdNoSign`, `pushNoSign`), 37 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 37 lines (all theorems); axioms seen: none, propext, {propext, Quot.sound} |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module proves, for the declared signed boundary calculus of `LadderGeneral` (`sgn`, `bdN`, `pushN`, `coeffN`), that the composite boundary of any cell has coefficient zero at every face: `coeffN τ (pushN (bdN σ)) = 0` for every list `σ` and every list `τ` (`d2_zero_unrestricted`). The proof is a pairing of the two deletion orders of each unordered pair of positions — delete `b` then `a`, or delete `a` then `b−1` give the same face (`eraseIdx_swap`) with opposite signs (`sgn_cancel`) — carried out as an exact rearrangement of a finite double sum (`coeff_rect`, `tri_transpose`, `rect_zero`). The module records that the strict-ascent hypothesis the task expected to be load-bearing is not: the vanishing holds for repeated-vertex pseudo-cells too (`illformed_countermodel`), while ascent is load-bearing only for distinctness of faces (`eraseIdx_inj_of_asc`, `codim2_distinct`). It connects the vanishing to every cell of every replayed complex via `LadderGeneral.wf_nreplay` (`d2_zero_replayed`, `d2_zero_d4`), transports it along strictly monotone renamings (`d2_zero_renamed`, `d2_zero_shift`), and shows by countermodel that the declared alternating sign is what makes it true: with all signs `+1` the integer composite is nonzero (`signless_countermodel`, `signless_countermodel_dim3`). In the programme's terms this is a theorem about a declared realization layer (integer chains on ascending-list cells), not about the passage: no regime, observer, obstruction or witness appears; the coefficients and signs are admitted inputs and the module says so.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `sumTo` | 95 | def | `f 0 + … + f (m−1)` for `f : Nat → Int`. | ADMITTED (metatheory apparatus, so labelled) |
| `sumFrom` | 100 | def | `f a + … + f (a+m−1)`. | ADMITTED (metatheory) |
| `rowTri` | 151 | def | Row-major strict upper triangle sum `Σ_{a<n} Σ_{a<b<n} F a b`. | ADMITTED (metatheory) |
| `colTri` | 155 | def | Column-major strict upper triangle sum. | ADMITTED (metatheory) |
| `dterm` | 293 | def | Signed contribution of the ordered deletion pair `(i,j)` to the coefficient of `τ`: `sgn i * sgn j` if `(σ.eraseIdx i).eraseIdx j == τ`, else `0`. | ADMITTED |
| `bdNoSign` | 592 | def | The boundary with every coefficient `1`. | ADMITTED (countermodel exhibit) |
| `pushNoSign` | 596 | def | Pushforward through `bdNoSign`. | ADMITTED (countermodel exhibit) |

Imported declared inputs (from `LadderGeneral`): `sgn`, `bdN`, `pushN`, `coeffN`, `facets`, `ascB`, `ComplexN`, `nreplay`, `emptyN`, `wf_nreplay`, `d4Events`, `d4Complex`.

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `sumTo_const_zero` | 104 | `sumTo (fun _ => 0) m = 0`. | FROZEN | propext, Quot.sound | A |
| `sumTo_congr` | 111 | If `f t = g t` for all `t < m` then `sumTo f m = sumTo g m`. | FROZEN | propext, Quot.sound | A |
| `sumTo_add` | 119 | `sumTo (f+g) m = sumTo f m + sumTo g m`. | FROZEN | propext, Quot.sound | A |
| `sumTo_split` | 129 | `sumTo f (a+m) = sumTo f a + sumFrom f a m`. | FROZEN | propext, Quot.sound | A |
| `sumFrom_shift` | 139 | `sumFrom f a m = sumFrom (fun b => f (b−1)) (a+1) m`. | FROZEN | propext, Quot.sound | A |
| `tri_transpose` | 159 | `rowTri F n = colTri F n` for every `F`, `n`. | FROZEN | propext, Quot.sound | A (the rearrangement) |
| `eraseIdx_eraseIdx_succ` | 193 | For `a ≤ c`: `(l.eraseIdx (c+1)).eraseIdx a = (l.eraseIdx a).eraseIdx c`. | FROZEN | propext, Quot.sound | A |
| `eraseIdx_swap` | 207 | For `a < b`: `(l.eraseIdx b).eraseIdx a = (l.eraseIdx a).eraseIdx (b−1)`. | FROZEN | propext, Quot.sound | S (the pairing identity) |
| `sgn_succ` | 215 | `sgn (c+1) = −sgn c`. | FROZEN | propext, Quot.sound | A |
| `sgn_cancel` | 222 | For `0 < b`: `sgn b * sgn a + sgn a * sgn (b−1) = 0`. | FROZEN | propext, Quot.sound | S (the sign cancellation) |
| `coeffN_nil` | 233 | `coeffN τ [] = 0`. | FROZEN (rfl) | none | A |
| `foldl_acc` | 235 | Accumulator shift for the sum fold. | FROZEN | propext, Quot.sound | A |
| `coeffN_append` | 245 | `coeffN` is additive over `++`. | FROZEN | propext, Quot.sound | A |
| `coeffN_singleton` | 253 | `coeffN τ [p]` is `p.1` if `p.2 == τ`, else `0`. | FROZEN | propext, Quot.sound | A |
| `coeffN_map_range` | 262 | `coeffN` of a mapped range as a `sumTo`. | FROZEN | propext, Quot.sound | A |
| `coeffN_flatMap_range` | 277 | `coeffN` of a flat-mapped range as a `sumTo` of `coeffN`s. | FROZEN | propext, Quot.sound | A |
| `coeff_push_bd` | 296 | `coeffN τ (pushN (bdN σ))` equals the double `sumTo` of `dterm` with inner bound `(σ.eraseIdx i).length`. | FROZEN | propext, Quot.sound | A |
| `coeff_rect` | 313 | Same with inner bound `σ.length − 1` (uses `List.length_eraseIdx_of_lt`). | FROZEN | propext, Quot.sound | A |
| `ite_pair_cancel` | 323 | If `u + v = 0` then `ite c u 0 + ite c v 0 = 0`. | FROZEN | propext, Quot.sound | A |
| `dterm_cancel` | 333 | For `a < b`: `dterm σ τ b a + dterm σ τ a (b−1) = 0`. | FROZEN | propext, Quot.sound | S |
| `rect_zero` | 339 | The rectangle sum of `dterm` vanishes for every `σ`, `τ`. | FROZEN | propext, Quot.sound | S |
| `d2_zero_unrestricted` | 377 | For every `σ τ : List Nat`, `coeffN τ (pushN (bdN σ)) = 0`. | FROZEN | propext, Quot.sound | S |
| `d2_zero_general` | 387 | Same, stated with unused hypotheses `ascB σ = true`, `2 ≤ σ.length`. | FROZEN (hypotheses recorded, not used; named `_hasc`, `_hlen`) | propext, Quot.sound | S |
| `d2_zero_facets` | 395 | For ascending `σ` of length ≥ 2, every facet `τ` has coefficient 0 (hypotheses unused). | FROZEN | propext, Quot.sound | A |
| `d2_zero_replayed` | 406 | For every event list `h`, `k ≥ 1`, and `σ ∈ (nreplay h emptyN).cells k`, every `τ` has coefficient 0 (via `wf_nreplay`). | CONDITIONAL: `1 ≤ k`, membership in a replayed complex (both trivially discharged — the conclusion holds unconditionally by `d2_zero_unrestricted`) | propext, Quot.sound | S |
| `d2_zero_d4` | 415 | Same for `d4Complex`. | CONDITIONAL as above (instance) | propext, Quot.sound | A |
| `ascB_tail` | 423 | `ascB (x :: y :: t) → ascB (y :: t)`. | FROZEN | propext | A |
| `ascB_head_lt` | 428 | `ascB (x :: l) → ∀ z ∈ l, x < z`. | FROZEN | propext | A |
| `eraseIdx_inj_of_asc` | 442 | For ascending `l` and in-range `i, j`: `l.eraseIdx i = l.eraseIdx j → i = j`. | CONDITIONAL: `ascB l = true`, `i, j < l.length` | propext, Quot.sound | S |
| `codim2_distinct` | 485 | For ascending `l`, `a < b < l.length`, `c < d < l.length`: equal codim-2 faces imply `a = c ∧ b = d`. | CONDITIONAL: `ascB l = true` and the range/order hypotheses | propext, Quot.sound | S |
| `eraseIdx_map` | 534 | `(l.map r).eraseIdx i = (l.eraseIdx i).map r`. | FROZEN | propext | A |
| `ascB_map` | 545 | A strictly monotone `r` preserves `ascB`. | CONDITIONAL: `∀ x y, x < y → r x < r y` | propext | A |
| `d2_zero_renamed` | 568 | For strictly monotone `r` and ascending `σ` of length ≥ 2: `σ.map r` is ascending, same length, facets commute with `map`, and its composite vanishes. | CONDITIONAL: monotone `r`, `ascB σ`, `2 ≤ σ.length` (only the first three conjuncts use them) | propext, Quot.sound | S |
| `d2_zero_shift` | 580 | Instance of the above for `x ↦ x+1`. | CONDITIONAL: `ascB σ`, `2 ≤ σ.length` | propext, Quot.sound | A |
| `signless_countermodel` | 607 | `[0,1,2]` is ascending; the signless composite has coefficient 2 at each vertex; the signed composite has 0. | VERIFIED_FINITE / REFUTED (refutes "the vanishing is independent of the sign convention") | none | S |
| `signless_countermodel_dim3` | 622 | Same on `[0,1,2,3]` at the edge `[0,1]`. | VERIFIED_FINITE / REFUTED | none | A |
| `illformed_countermodel` | 648 | `[0,0,1]` is not ascending; positions 0 and 1 give the same facet; `[0,1]` is a facet with boundary coefficient 0; the slot `[0]` of the composite collects 4 terms (vs 2 for `[0,1,2]`); the composite still vanishes at `[0]` and `[1]`. | VERIFIED_FINITE / REFUTED (refutes "distinct positions give distinct facets" without ascent; confirms vanishing is not refuted) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- Declared inputs, named as such in the docstring (lines 25–39, 78–85): integer coefficients, the alternating sign `sgn i = (−1)^i`, the ascending-list cell encoding. These are policy choices of the realization layer, not derived.
- `sumTo`/`sumFrom` take `f : Nat → Int` and `rowTri`/`colTri` take `F : Nat → Nat → Int`: metatheoretic finite sums over function-valued data; every sum is bounded by a concrete `Nat` (`σ.length`). Finitude: no unbounded totality is attributed to the system; the module labels §1 "metatheory apparatus".
- Library lemmas doing real work: `List.length_eraseIdx_of_lt` (in `coeff_rect`), `List.filter_append`, `List.foldl_append`, `List.filter_cons`, `List.range_succ`, `List.map_append`, `List.flatMap_append`, `List.flatMap_map`, `List.map_map`, `List.eraseIdx_cons_succ`, `List.mem_of_mem_eraseIdx`, `Nat.add_mod`, `Int.neg_mul`, `Int.neg_neg`, `Int.mul_comm`, `omega`. The coefficient test is the boolean `BEq` on `List Nat` throughout (docstring at line 250: "avoids any appeal to a decidability bridge").
- Unearned identity: none found.
- Unrestricted external universe: none found (all quantifications are over `List Nat` and `Nat`, metatheoretic).
- Unbounded function treated as internally available: `r : Nat → Nat` in the renaming theorems is a metatheoretic renaming; nothing claims the system holds it.
- Silently assumed observer: none.
- Unspecified correspondence between presentations: none; renamings are explicit functions with an explicit monotonicity hypothesis.
- Cost function without justification: none.
- Admitted condition later described as forced: none found. The docstring and ledger state the opposite (the signs are declared; the filler rule does not force them) and prove it by countermodel.
- Finite computation presented as universal: none found; the general theorem is general, and the countermodels are labelled as integer-coefficient countermodels only ("characteristic two changes the signless calculation", line 38–39).
- Recorded-but-unused hypotheses: `d2_zero_general`, `d2_zero_facets`, `d2_zero_replayed`, `d2_zero_d4` carry hypotheses the proof does not need. The docstring says so explicitly (lines 73–76) and the ledger repeats it.

## 5. Derived consequences

- No other Lean module imports `BoundaryCancellation` (checked: `grep BoundaryCancellation\.` finds only docstring mentions in `LadderGeneral.lean`, which cannot import it without a cycle).
- Ledger CL-PD2-BOUNDARY-CANCELLATION cites 22 theorems by name; CL-PD2-LADDER-GENERAL defers the general vanishing to it. `paper/primitive_difference_map.md` lines 201, 280 and `paper/paper_change_log.md` line 857 record the closure of the former open conjecture.
- Supersedes `LadderGeneral.d2_zero_dims_2_3_4` (and repairs its evidential gap: see the `LadderGeneral` record, §11, where the dimension-2 and -3 conjuncts of that spot-check are shown vacuous; `d2_zero_facets` and `d2_zero_unrestricted` cover those dimensions properly).

## 6. Counterexamples and limitations

- `signless_countermodel`, `signless_countermodel_dim3`: without the alternating sign the integer composite is nonzero (coefficient 2). Refutes any reading that the filler rule or the cell encoding forces the vanishing.
- `illformed_countermodel`: states exactly what fails for `[0,0,1]` (distinctness of facets; degeneracy of the boundary chain — the facet `[0,1]` has coefficient 0; the slot `[0]` collects four terms) and what does not (the composite still vanishes). Refutes the task's premise that ascent is load-bearing for the vanishing.
- Not proved (and said so, lines 64–71): the quantitative statement that each codim-2 face of an ascending cell collects exactly two ordered deletion pairs; recorded as decided on two exhibits and checked in Python (`perfect_matching`).
- Not claimed: anything for non-monotone injective renamings beyond the unrestricted vanishing; anything for other coefficient systems; any homology (no chain complex, cycles or boundaries are defined — only coefficientwise vanishing of one composite).
- No connection to the passage: `d2_zero_replayed` connects to `LadderGeneral`'s replayed complexes, not to `PrimitivePassage` states.

## 7. Axiom dependencies

All 37 theorems are in the artifact; axioms within {propext, Quot.sound}; `coeffN_nil`, `signless_countermodel`, `signless_countermodel_dim3` report none; `ascB_tail`, `ascB_head_lt`, `eraseIdx_map`, `ascB_map` report propext only. None exceed the whitelist.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 37 theorems appear in the axiom artifact (`Derivation.lean` inventory). The ledger cites 22 of them. Probe: the signless probe written for `LadderGeneral` (`textbook/audit/probes/E/lg_vacuity.lean`, exit 0) independently reproduces `signless_countermodel`'s content (a signless composite with nonzero coefficient at dimension 2 and on the 5-vertex cell). No further probe was needed: the main theorem is a general proof, read in full; `coeff_rect`'s use of `List.length_eraseIdx_of_lt` is the only place a library length lemma enters, and the hypothesis `i < σ.length` is supplied by `sumTo_congr`.

## 9. Related Python implementations

- `code/derivation/boundary_cancellation.py`: `erase_idx`, `sgn`, `asc`, `facets`, `bd_n`, `push_n`, `coeff_n`, `bd_no_sign`, `push_no_sign`, `dterm`, `swap_pair`, `rectangle`, `involution_report`, `erase_swap`, `sgn_cancel`, `rect_sum`, `pairs_cancel`, `support`, `cell_cancels`, `cell_rect_identity`, `cell_pairs_cancel`, `erase_inj`, `codim2_distinct`, `slot_multiplicity`, `codim2_faces`, `perfect_matching`, `ascending_cells`, `cancellation_report` (218 cells, dims 2–6 over 8 vertices per the ledger), `rename`, `monotone_rename`, `swap01`, `renaming_report`, `signless_countermodel`, `illformed_countermodel`.
- Tests: `tests/test_boundary_cancellation.py` (`test_declared_calculus_mirrors_lean`, `test_involution_is_the_pairing`, `test_exhaustive_cancellation_over_declared_bounds`, `test_per_cell_statements`, `test_distinctness_is_what_ascent_buys`, `test_renaming_scope`, `test_signless_countermodel`, `test_illformed_countermodel_states_exactly_what_fails`, two runner tests).

## 10. Textbook placement proposal

- Prerequisites: `LadderGeneral`'s cell encoding (`facets`, `ascB`, `sgn`, `bdN`, `pushN`, `coeffN`); finite sums as metatheory; the distinction between a declared convention and a derived fact.
- Substantive: `eraseIdx_swap`, `sgn_cancel`, `dterm_cancel`, `rect_zero`, `d2_zero_unrestricted` (the theorem and its pairing proof), `d2_zero_replayed` (the hook to replayed complexes), `eraseIdx_inj_of_asc`, `codim2_distinct` (what ascent buys), `signless_countermodel`, `illformed_countermodel`, `d2_zero_renamed`.
- Auxiliary: the `sumTo`/`sumFrom` algebra, `tri_transpose`, the `coeffN_*` additivity lemmas, `coeff_push_bd`, `coeff_rect`, `ite_pair_cancel`, `ascB_tail`, `ascB_head_lt`, `eraseIdx_map`, `ascB_map`, `d2_zero_general`, `d2_zero_facets`, `d2_zero_d4`, `d2_zero_shift`, `signless_countermodel_dim3`.
- Lesson title: "Why the boundary of a boundary is zero here, and what makes it so." Question answered: which declared choice (the alternating sign) makes the composite boundary vanish, and which expected hypothesis (strict ascent) turns out to be irrelevant to it?
- Recommend omitting: `d2_zero_general`, `d2_zero_facets` as separate items (restatements with unused hypotheses; teach `d2_zero_unrestricted` and remark that the ascending form follows); `signless_countermodel_dim3` (duplicate of the dimension-2 exhibit). Keep the "not formalized" note about the two-per-face count so students do not read `codim2_distinct` as that count.

## 11. Interpretation findings

1. **`d2_zero_replayed` / `d2_zero_d4` — INTERPRETATION note (no defect).** Docstring: "Well-formedness ... is supplied by the replayed invariant `wf_nreplay`; the vanishing is `d2_zero_general`." Lean: the conclusion follows from `d2_zero_unrestricted` with no use of membership or well-formedness; the hypotheses `1 ≤ k` and `σ ∈ (nreplay h emptyN).cells k` are logically idle (the theorem would hold for any `σ` whatsoever). This is not vacuity (the hypotheses are satisfiable, e.g. `d4Complex`), and the ledger says the hypotheses are "recorded and discharged from the stronger theorem". The textbook should not present `d2_zero_replayed` as evidence that replay or well-formedness matters for the vanishing; it matters only for membership in the guarded calculus.
2. **Ledger wording "closes the standing conjecture" (CL-PD2-BOUNDARY-CANCELLATION heading)** — accurate for the coefficientwise vanishing in the declared integer calculus; the module itself (lines 37–39) restricts the countermodel to integer coefficients. No overreach found.
3. **Vacuity check:** `d2_zero_unrestricted` is non-trivial (its negation is refuted only by the pairing; the signless variant fails). `eraseIdx_inj_of_asc` and `codim2_distinct` have satisfiable hypotheses (`[0,1,2]`) and false analogues without ascent (`illformed_countermodel`). `d2_zero_renamed`'s monotonicity hypothesis is used (for `ascB_map`), and is satisfiable (`x ↦ x+1`). None found vacuous.
4. **Finitude:** `sumTo (f : Nat → Int)` and `r : Nat → Nat` are metatheory, labelled as such in the module; no prose reads them as system content. Flag for the matrix only.
