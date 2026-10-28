# Audit: TransitionTransport

| field | value |
|---|---|
| Path | lean4/Derivation/TransitionTransport.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 5ac8d7c851033bbe |
| Lines | 1070 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.CountTransport |
| Declarations | 11 def (`padF`, `DRen.pad`, `mapReq`, `renameRegimeR`, `mapItem`, `respond`, `TransStep`, `formAritySum`, `regRegime`, `regSwapFun`, `regSwap`), 53 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 51 lines; axioms seen: none (`map_congr_mem`, `formAritySum_map`, `regSwapFun_invol`, `regSwapFun_bound`), propext, propext+Quot.sound. Not in artifact: `DRen.inv_f`, `DRen.inv_g` appear in the artifact (root lines 1417–1418) — all 53 are reported |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
TransitionTransport discharges residual R7 at the relation level: that one engine round — impose a collapsed pair, then apply a valid response — is congruent to a datum renaming. Unlike collapse, a round reads the requirement store, so the collapse action `renameRegime` is extended to `renameRegimeR`, which carries requirements renormalized to ordered pairs; and because a response may admit fresh data and mention them, the bijection is padded by the identity above the base datum count (`padF`), matching the implementation's fresh-index discipline. The module proves the chain `stepE_impose_rename` → `applyDelta_rename` → `respond_rename` → `validResponse_rename`, defines the transition relation `TransStep` (every collapsed pair, every valid response, no selection), and proves the congruence as mapping plus image totality. It also transports valid-response counts and both declared cost components across the renaming, and exhibits in Lean the recorded boundary: the index-least pair selection is not congruent on the regression regime.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `padF n f` | 53 | def | `f` below `n`, identity at and above | ADMITTED |
| `DRen.pad σ m hm` | 97 | def | the padding packaged as a `DRen m` for `n ≤ m` | ADMITTED |
| `mapReq f q` | 109 | def | `(min (f q.1) (f q.2), max …)` | ADMITTED (renormalising action on requirements) |
| `renameRegimeR f r` | 117 | def | `renameRegime f r` with `reqs := r.reqs.map (mapReq f)` | ADMITTED (the transition action; docstring: "the extension is forced" by `validResponse` reading `reqs`) |
| `mapItem f` | 272 | def | rename datum indices inside an item; forms fixed | ADMITTED (scope: datum bijections, identity on forms) |
| `respond r i j δ` | 677 | def | `(stepE r (.impose i j)).bind (applyDelta · δ)` — one round | ADMITTED (the Lean transition object) |
| `TransStep r i j δ s` | 820 | def (Prop) | `i < j ∧ j < r.data ∧ collapsed r i j ∧ validResponse r i j δ ∧ respond r i j δ = some s` | ADMITTED (declared relation, no selection) |
| `formAritySum` | 910 | def | arity sum of `newForm` items (duplicate of Minimality's `aritySum` under another name; not identified in Lean) | ADMITTED |
| `regRegime` | 972 | def | `⟨4,[1],[(0,[2]),(0,[3])],[],[]⟩`, the regression regime | ADMITTED |
| `regSwapFun` | 975 | def | double transposition 0↔2, 1↔3, identity above | ADMITTED |
| `regSwap` | 1000 | def | `DRen 4` from `regSwapFun` | ADMITTED |

## 3. Theorems and lemmas
Hypothesis pack used repeatedly: `hn : r.data = n`, `hinst : ∀ p ∈ r.insts, ∀ a ∈ p.2, a < r.data`, `hreq : ∀ q ∈ r.reqs, q.1 < q.2 ∧ q.2 < r.data` (the three conjuncts of `Regime.wf` that concern data; called "WF-data" below).

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `padF_lt`, `padF_ge` | 56, 60 | the two branches of `padF` | FROZEN | propext | A |
| `padF_fg`, `padF_gf` | 65, 72 | padded two-sided inverse for a `DRen n` | FROZEN | propext | A |
| `padF_inj` | 79 | `padF n σ.f` injective | FROZEN | propext | A |
| `padF_bound` | 86 | for `n ≤ m`, `padF n σ.f` maps `< m` to `< m` | CONDITIONAL: `n ≤ m` | propext | A |
| `mapReq_cases` | 121 | `mapReq f p` is `(f p.1, f p.2)` or swapped | FROZEN | propext | A |
| `mapReq_ordered` | 128 | injective `f` keeps `i < j` ordered after `mapReq` | CONDITIONAL: `f` injective | propext | A |
| `mapReq_inj_ordered` | 139 | `mapReq f` injective on ordered pairs for injective `f` | CONDITIONAL: injective `f`, both pairs ordered | propext | A |
| `mapReq_g_f` | 165 | `mapReq σ.g (mapReq σ.f (i,j)) = (i,j)` for `i < j` | CONDITIONAL: `i < j` | propext | A |
| `renameR_reqs_wf` | 185 | the requirement conjunct of wf survives `renameRegimeR σ.f` | CONDITIONAL: `hn`, `hreq` | propext, Quot.sound | A |
| `collapsed_reqs_irrel`, `separable_reqs_irrel` | 205, 209 | collapse and separability ignore `reqs` (`Iff.rfl`) | FROZEN (definitional) | propext | A |
| `collapsed_renameR` | 214 | `collapsed (renameRegimeR σ.f r) (σ.f d) (σ.f d') ↔ collapsed r d d'` | CONDITIONAL: `hn` | propext, Quot.sound | S |
| `collapsed_symm`, `separable_symm` | 221, 261 | symmetry of collapse / separability | FROZEN | propext | A |
| `separable_rename` | 228 | separability transports along `renameRegime` | CONDITIONAL: `hn` | propext, Quot.sound | S |
| `separable_renameR` | 254 | same along `renameRegimeR` | CONDITIONAL: `hn` | propext, Quot.sound | S |
| `mapItem_pad_f_g` | 278 | padded item action cancels | FROZEN | propext, Quot.sound | A |
| `insertNew_map_on` | 295 | `insertNew` commutes with a map injective relative to the inserted element (`DecidableEq α β`) | CONDITIONAL: pointwise `hinj` | propext, Quot.sound | A |
| `applyItem_data_mono`, `applyDelta_data_mono` | 310, 376 | admission never lowers `data` | FROZEN | propext | A |
| `applyItem_reqs`, `applyDelta_reqs` | 341, 393 | no item touches `reqs` | FROZEN | propext | A |
| `applyDelta_nil`, `applyDelta_cons` | 370, 372 | unfolding equations (`rfl`) | FROZEN | propext | A |
| `applyItem_rename` | 415 | one item commutes with the padded action when `n ≤ r.data` | CONDITIONAL: `n ≤ r.data` | propext, Quot.sound | S |
| `applyDelta_rename` | 495 | delta-level commutation under `n ≤ r.data` | CONDITIONAL: `n ≤ r.data` | propext, Quot.sound | S |
| `map_congr_mem` | 516 | pointwise-equal maps give equal `List.map` | FROZEN | none | A |
| `DRen.inv_f`, `DRen.inv_g` | 526, 527 | `rfl` projections | FROZEN | in artifact (root 1417–1418), propext per artifact — not re-checked | A |
| `mapReq_inv_pair` | 531 | renormalisation cancels for any two-sided inverse pair on `i < j` | CONDITIONAL: `hfg`, `i < j` | propext | A |
| `renameRegimeR_inv_pair` | 552 | full-action cancellation on regimes with ordered requirements | CONDITIONAL: `hfg`, `hreq` (ordered) | propext, Quot.sound | S |
| `renameRegimeR_g_f`, `renameRegimeR_pad_f_g` | 581, 586 | instances for `σ` and its padding | CONDITIONAL: ordered reqs | propext, Quot.sound | A |
| `renameRegimeR_padF_agree` | 593 | padded and raw spellings agree when all indices are `< n` | CONDITIONAL: WF-data | propext | A |
| `rename_insts_bound` | 622 | datum-bound conjunct of wf survives | CONDITIONAL: `hn`, `hinst` | propext, Quot.sound | A |
| `stepE_impose_rename` | 635 | imposition commutes with the action for `i < j < r.data` | CONDITIONAL: `hn`, `hreq`, `i < j`, `j < r.data` | propext, Quot.sound | S |
| `respond_reqs_ordered` | 682 | a successful round keeps requirements ordered | CONDITIONAL: `hr` (ordered before) | propext | A |
| `respond_rename` | 711 | the round commutes with the action (padded on the output) | CONDITIONAL: WF-data, `i < j`, `j < r.data` | propext, Quot.sound | S |
| `validResponse_symm` | 744 | `validResponse r a b δ ↔ validResponse r b a δ` | FROZEN | propext | A |
| `validResponse_rename` | 751 | validity transports: `validResponse (renameRegimeR σ.f r) (σ.f i) (σ.f j) (δ.map …) ↔ validResponse r i j δ` | CONDITIONAL: WF-data, `i < r.data`, `j < r.data` | propext, Quot.sound | S |
| `transStep_rename_fwd` | 828 | every `TransStep` of `r` maps to a `TransStep` of `renameRegimeR σ.f r`, children corresponding under the padded action | CONDITIONAL: WF-data | propext, Quot.sound | S |
| `transStep_image_total` | 866 | every `TransStep` of the renamed regime is the image of one of `r` | CONDITIONAL: WF-data | propext, Quot.sound | S |
| `mapItem_length` | 905 | item action preserves length (`mu1`) | FROZEN | propext | A |
| `formAritySum_map` | 918 | item action preserves `formAritySum` | FROZEN | none | A |
| `validCount_rename` | 937 | for deciders `p`, `q` characterising validity on both sides, `countP` over any list `L` is preserved by the item action | CONDITIONAL: WF-data, bounds, `hp`, `hq` (caller-supplied deciders) | propext, Quot.sound | S |
| `regSwapFun_invol`, `regSwapFun_bound` | 982, 991 | the regression permutation is an involution bounded by 4 | VERIFIED_FINITE (case split/`decide`) | none | A |
| `one_unary_form_ctx_char` | 1010 | with `forms = [1]`, `wfCtx r c ↔ c = ⟨0,[none]⟩` | CONDITIONAL: `r.forms = [1]` | propext | A |
| `reg_collapsed_01`, `reg_renamed_collapsed_01` | 1045, 1051 | `(0,1)` collapsed in `regRegime` and in its renaming | VERIFIED_FINITE (via the context characterisation then `decide`) | propext, Quot.sound | A |
| `least_pair_selection_not_congruent` | 1064 | `(0,1)` is collapsed on both sides and `mapReq regSwap.f (0,1) ≠ (0,1)` | REFUTED (refutes congruence of index-least selection; VERIFIED_FINITE components) | propext, Quot.sound | S |

## 4. External and admitted assumptions
- `DRen n` (CountTransport): a bijection of all of `Nat` bounded on `< n` — metatheory; the padding treats indices `≥ n` as fixed, matching the implementation's "fresh data receive the next indices" (declared correspondence, checked by `test_orbit_policy_transition_congruence_exhaustive`).
- Scope declared: datum bijections with the identity on forms (`mapItem` leaves form indices); form bijections are not exercised (paper 7.5 says so).
- WF-data hypotheses on every transport theorem; `n ≤ r.data` on the padded commutations.
- `validCount_rename` takes caller-supplied deciders `p`, `q` with characterising hypotheses and an arbitrary list `L`: the same division of labour as `collapsedCount_rename` (Python enumerates and decides; Lean states what the decision means). Cost measures: `mapItem_length` and `formAritySum_map` are the two components; the lexicographic combination is prose.
- Library lemmas: `Nat.min/max_eq_*`, `Nat.max_lt`, `List.map_map`, `List.map_id'`, `List.mem_map`, `List.countP_cons`, `Bool.eq_iff_iff`, `Option.map`, `decide`. Core only.
- Universe: `{α β : Type}` in two list lemmas (Type 0). `Nat → Nat` as data: `f`, `g`, `padF`, `regSwapFun` (metatheory).
- Unearned identity: none found (`renameRegimeR_inv_pair` needs ordered requirements and says so). Unrestricted universe: none. Unbounded function as internal: `padF` acts on all of `Nat`, read as acting on indices the regime does not yet have — a metatheoretic device, flagged as consistent with the prose. Silent observer: none. Presentation correspondence: `respond` vs the engine's event sequence is declared ("the exact event sequence the implementation replays"), not proved; `formAritySum` vs Minimality's `aritySum` are two Lean definitions of one measure component, never proved equal (they are definitionally the same recursion; a `rfl` lemma would close it; not present). Cost without justification: declared measures, as elsewhere. Admitted-as-forced: the docstring says the extension to `renameRegimeR` "is forced" — true in the sense that `validResponse` reads `reqs`; a design necessity, not a theorem, and not presented as one in the paper. Finite-as-universal: none found; the regression witness is labelled as a witness.

## 5. Derived consequences
`respond` → Rounds (`ClosedRun`, `respond_anatomy`), `applyDelta_cons`/`applyDelta_reqs` → Rounds, RuleBridge; `mapReq` → IsoCanon (`mapReq_eq_sortPair`); `renameRegimeR`, `applyDelta_rename` → IsoCanon (relabel lemmas; to check in that record). Ledger CL-TRANSITION-EQUIVARIANCE (Lean bullet), paper 7.5 and register row R7 ("DISCHARGED 2026-08-18 (relation level …)") rest on `transStep_rename_fwd`, `transStep_image_total`, `validCount_rename`, `least_pair_selection_not_congruent`; change log 1826–1840.

## 6. Counterexamples and limitations
- `least_pair_selection_not_congruent` refutes "the index-least collapsed-pair selection is equivariant": witness `regRegime` and the double transposition; `(0,1)` is least on both sides but maps to `(2,3)`. The further fact that the two children are non-isomorphic is computational (`test_least_pair_selection_is_not_equivariant`), stated in the docstring as not re-proved.
- Not proved: an equality-form iff over an arbitrary child (false — `mapReq` renormalises, so the action is not injective on disordered-requirement regimes; the docstring explains and this is why mapping + totality is used); transport under form bijections; the conversion of `TransStep`-congruence to equal canonical-key class sets (CL-ISO-SOUND, Python); that the ORBIT policy's selection is congruent (only that the relation is); the lexicographic ordering of `mu2`; equality of `formAritySum` with `aritySum`.

## 7. Axiom dependencies
All within {propext, Quot.sound}; four with none. None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 53 theorems in the artifact (51 matched by the inventory plus `DRen.inv_f/inv_g` at root lines 1417–1418). Paper 7.5, register R7, ledger CL-TRANSITION-EQUIVARIANCE cite them. No extra probe.

## 9. Related Python implementations
`code/derivation/engine.py` (one round: `Impose` then the response delta; the orbit policy), `code/derivation/iso.py` (`rename`, `canonical`), `code/derivation/renaming_structure.py::orbit_no_selection`. Tests: `tests/test_equivariance.py::test_regression_canonical_equal_under_rename` (L68), `::test_least_pair_selection_is_not_equivariant` (L77), `::test_regression_orbits_are_distinct_and_both_retained` (L94), `::test_orbit_policy_transition_congruence_exhaustive` (L103), `::test_orbit_representatives_cover_all_collapsed_pairs` (L127).

## 10. Textbook placement proposal
- Prerequisites: Basic (`stepE`, `applyDelta`, `validResponse`), CountTransport (`DRen`, `renameRegime`, `collapsed_rename`), the difference between a relation and a selection.
- Substantive: `renameRegimeR` and why `reqs` must be carried, `padF` and why padding is needed, `respond`, `TransStep`, `validResponse_rename`, `transStep_rename_fwd`, `transStep_image_total`, `validCount_rename`, `least_pair_selection_not_congruent`. Auxiliary: all `padF_*`, `mapReq_*`, `applyItem_*`, `applyDelta_*`, cancellation and agreement lemmas, `respond_reqs_ordered`, the `reg*` helpers.
- Lesson title: "Renaming the data does not change what can happen next — but it changes what gets picked". Question: why is the quotiented transition well defined on isomorphism classes, and why did the index-least policy still break?
- Omit: the forty auxiliary commutation lemmas from the main text; keep one worked case (`newInst`) of `applyItem_rename` to show where `padF_bound` enters.

## 11. Interpretation findings
- Paper 7.5: "the transports of candidates, costs, validity, steps and children under a datum renaming are **[theorem]** at the relation level (`transStep_rename_fwd`, `transStep_image_total`, `validCount_rename`); the conversion to equal canonical-key class sets remains computational … form bijections are not exercised". Lean: exactly these, under WF-data. Match. none found.
- Ledger: "`validCount_rename` + `mapItem_length` + `formAritySum_map` carry minima and counts of both declared measures". Lean carries `countP` over a caller-supplied list with caller-supplied deciders and preserves the two measure components separately. "Carry minima" requires that `L` be the full candidate space and that the deciders be correct — both Python-side. INTERPRETATION DEFECT (minor, same shape as `collapsedCount_rename` in CountTransport: the headline attributes to Lean a count over the candidate space, while Lean states a count over any list under correct deciders). The ledger does say "over any caller-supplied candidate list", so the overread is only in the summary phrase.
- Register row R7 header "Transition-congruence transport under datum renaming, forms fixed — DISCHARGED (relation level; form-action transport, minimum-family transport and the class-set conversion stay computational)". Exact.
- `formAritySum` (here) and `aritySum` (Minimality) are two names for one measure component with no Lean link; the ledger cites `formAritySum_map` for `mu2` while `mu2_unique` uses `aritySum`. Not a defect in any statement; a naming duplication that the textbook should collapse. Recorded.
- Vacuity: WF-data is satisfiable (`R2L`, `regRegime` after one mark); `TransStep` inhabited (e.g. `R2L`, `(0,1)`, `deltaU0`) — not checked by probe but follows from `deltaU0_valid` plus `collapsed_of_no_insts`; `transStep_image_total`'s existential is constructive (it names the preimage). none found.
- Finitude: `padF` over all of `Nat`, `DRen` on all of `Nat`: metatheory; prose never reads them as system content. none found.
