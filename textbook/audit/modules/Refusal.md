# Audit: Refusal

| field | value |
|---|---|
| Path | lean4/Derivation/Refusal.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 89552213ee8bf601 |
| Lines | 289 |
| Imported by root `Derivation.lean` | yes (line 18) |
| Imports | `Derivation.Basic`, `Derivation.Inertia`, `Derivation.PrimDiff` (the last is imported but no `PrimDiff` name is used in this file) |
| Declarations | 2 inductive (`REvent`, `Mode`), 1 structure (`RState`), 10 def (`emptyR`, `stepR`, `stepOcc`, `replayR`, `replayOcc`, `isMarker`, `AtMostTokR`, `swapIdx`, `swapState`, `taggedTranslation`), 18 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 16 lines; axioms seen: `propext` / `propext, Quot.sound`. **Not in artifact:** `markers_invisible_from`, `reify_occ_from` (helpers) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module takes up a question the bridge left open: when the failed re-admission of an already admitted token is itself admitted as object-language data, can it produce a second distinguishable state without a second token? It fixes a reduced signature (supplies, token admissions, a history-only refusal marker) and a reduced state (admitted tokens in order, a list of tagged indices, a refusal counter), and declares five re-admission disciplines as one step function `stepR` indexed by a `Mode`: silent (no-op), meta (no-op in state; the marker is in the history only), fact (increment a counter), reify-untagged (append another occurrence), reify-tagged (append and tag the new index). It then proves, discipline by discipline and mostly on the concrete two-admission history, a strict hierarchy — history difference < state difference < carrier growth < witnessed difference — with a separation at each gap; one equivalence (untagged reification is occurrence admission, stepper for stepper); and the one new phenomenon: the tagged discipline's two-occurrence state is not swap-invariant, so the orientation that no equivariant rule could choose is supplied by the discipline declaration. Finally it prices the tag: the tagged two-element state translates into the regime model as one unary form plus one instance (separable there), and the untagged one into the bare two-datum regime (collapsed there).

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `REvent` | 43 | inductive | `supply tok`, `admitTok tok`, `marker tok` | ADMITTED (reduced signature) |
| `RState` | 51 | structure | `data : List Nat`, `tags : List Nat`, `refusals : Nat` | ADMITTED |
| `emptyR` | 57 | def | `⟨[], [], 0⟩` | ADMITTED |
| `Mode` | 59 | inductive | `silent`, `metaMarker`, `fact`, `reifyUntagged`, `reifyTagged` | ADMITTED (five declared disciplines) |
| `stepR` | 65 | def | one total admission step per mode (re-admission branch differs by mode; fresh admission appends in every mode) | ADMITTED (declared policy) |
| `stepOcc` | 82 | def | occurrence admission: every admission appends | ADMITTED (declared policy, the bridge's) |
| `replayR` | 87 | def | `foldl (stepR m) emptyR` | ADMITTED |
| `replayOcc` | 90 | def | `foldl stepOcc emptyR` | ADMITTED |
| `isMarker` | 107 | def | Boolean recogniser of `marker` events | ADMITTED |
| `AtMostTokR` | 139 | def | `s.data = [] ∨ s.data = [t0]` | ADMITTED (invariant) |
| `swapIdx` | 234 | def | swaps indices 0 and 1, fixes others | ADMITTED |
| `swapState` | 236 | def | applies `swapIdx` to the tag list only (`data`, `refusals` unchanged) | ADMITTED (see §6) |
| `taggedTranslation` | 273 | def | the regime `⟨2, [1], [(0,[1])], [], []⟩`: two data, one unary form, one instance marking datum 1 | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `silent_eq_meta` | 98 | `stepR .silent s e = stepR .metaMarker s e` for all `s e` | FROZEN (all states/events of the reduced signature) | propext, Quot.sound | S |
| `marker_state_invisible` | 103 | `stepR m s (.marker tok) = s` (`rfl`) | FROZEN | propext, Quot.sound | A |
| `markers_invisible_from` | 111 | folding over `h` with markers filtered out equals folding over `h`, from any start `s` | FROZEN | not in artifact | A |
| `markers_invisible` | 131 | `replayR m (h.filter (¬marker)) = replayR m h` | FROZEN | propext, Quot.sound | S |
| `nonreify_carrier_bound` | 142 | for `m ∈ {silent, metaMarker, fact}`, `AtMostTokR t0 s`, and an event whose admission (if any) carries `t0`: `AtMostTokR t0 (stepR m s e)` | CONDITIONAL:`m = silent ∨ metaMarker ∨ fact`, `AtMostTokR t0 s`, single-token event | propext, Quot.sound | S |
| `fact_state_changes` | 173 | `stepR .fact ⟨[0],[],0⟩ (admitTok 0) ≠ ⟨[0],[],0⟩` | VERIFIED_FINITE | propext, Quot.sound | S |
| `silent_state_fixed` | 178 | `stepR .silent ⟨[0],[],0⟩ (admitTok 0) = ⟨[0],[],0⟩` | VERIFIED_FINITE | propext, Quot.sound | S |
| `reifyUntagged_eq_occurrence` | 186 | `stepR .reifyUntagged s e = stepOcc s e` for all `s e` | FROZEN | propext, Quot.sound | S |
| `reify_occ_from` | 197 | the two folds agree from any start | FROZEN | not in artifact | A |
| `reifyUntagged_replay_eq_occurrence` | 207 | `replayR .reifyUntagged h = replayOcc h` | FROZEN | propext, Quot.sound | S |
| `reifyUntagged_two_admissions` | 214 | `replayR .reifyUntagged [admitTok 0, admitTok 0] = ⟨[0,0],[],0⟩` | VERIFIED_FINITE | propext, Quot.sound | S |
| `reifyTagged_two_admissions` | 220 | `replayR .reifyTagged [admitTok 0, admitTok 0] = ⟨[0,0],[1],0⟩` | VERIFIED_FINITE | propext, Quot.sound | S |
| `tag_separates` | 227 | in that state, `1 ∈ tags` and `0 ∉ tags` | VERIFIED_FINITE | propext, Quot.sound | S |
| `occurrence_state_swap_invariant` | 243 | `swapState` fixes the untagged two-admission state | VERIFIED_FINITE | propext, Quot.sound | S |
| `tagged_state_not_swap_invariant` | 252 | `swapState` moves the tagged two-admission state | VERIFIED_FINITE | propext, Quot.sound | S |
| `canonical_designation` | 262 | tagged state has `tags.head? = some 1`; untagged has `none` | VERIFIED_FINITE | propext, Quot.sound | S |
| `tagged_translation_separable` | 278 | `Derivation.separable taggedTranslation 0 1` (context: form 0 with one hole) | VERIFIED_FINITE | propext, Quot.sound | S |
| `untagged_translation_collapsed` | 285 | `Derivation.collapsed ⟨2,[],[],[],[]⟩ 0 1` (via `collapsed_of_no_insts`) | VERIFIED_FINITE (instance of a FROZEN Inertia lemma) | propext | S |

## 4. External and admitted assumptions

- **Five declared disciplines.** `stepR` is a declared policy; nothing derives any mode. The header says the disciplines are "formalized ... and compared without assuming that refusal, repetition, occurrence, and state difference are equivalent".
- **The tag is built into the discipline.** In `reifyTagged` the tag list records the *index* `s.data.length` of the new occurrence — an index into the metatheoretic list of data. The tag is thus a position-based observable supplied by the discipline, which is exactly what `tagged_translation_separable` prices as "one unary form plus one instance". Finitude flag: indices and the ordered `data` list are metatheory; the module makes this explicit (R6 price table) rather than hiding it.
- **`swapState` acts on tags only** (`data` is `[0,0]`, so swapping data would be invisible anyway; `refusals` is untouched). The swap-invariance results concern exactly the two-occurrence states and the index swap on tags. A reader should know the "swap" is not a general carrier automorphism of `RState`.
- **Tokens are `Nat`;** `tok ∈ s.data` uses decidable `Nat` equality. Admitted, harmless.
- **Library lemmas doing work:** `List.foldl`, `List.filter` simp lemmas, `decide` on small concrete states, `Inertia.collapsed_of_no_insts`, the `Derivation.separable`/`collapsed` definitions (context-based separability of `Basic.lean`).
- Unearned identity: none found. Unrestricted external universe: none (everything is on `Nat` lists). Unbounded function treated as internally available: `s.data.length` as a tag value — a metatheoretic count made object data by declaration; flagged above, declared in the paper. Silently assumed observer: the tag *is* the observer and is declared as such ("built-in unary observable"). Unspecified correspondence between presentations: `taggedTranslation` is a hand-chosen regime said to be "the translation"; no translation function is defined or proved faithful (see §6, §11). Cost function: none in Lean (admission counts are Python). Admitted condition later described as forced: none found; the paper says "declared price". Finite computation presented as universal: the hierarchy is proved on the two-admission history and the per-step facts; the paper's R9 records that the assembled four-way classification over all histories is not in Lean.

## 5. Derived consequences

`RefusalFrontier` does `open Refusal Derivation` and reuses `REvent`, `RState`, `Mode`, `stepR`, `replayR`, `emptyR` (see that module's record). No other module uses `Refusal.*`. Paper: `paper/refusal_difference.md` R3–R8 (owner); `paper/native_derivation_map.md` row "admission ⇒ two-ness PROVED: `min_witnessed_route_closes`, `reifyUntagged_eq_occurrence`". Ledger: no `CL-` entry lists `Refusal.*` theorems (grep of the ledger for `Refusal.` returns only `RefusalFrontier.*` hits inside other entries; the ledger's line 738 points to `paper/refusal_as_difference.md`). So the module's claims are owned by the write-up, not by a ledger ID — "not checked" whether that is intentional.

## 6. Counterexamples and limitations

- Separations: `markers_invisible` (history ≠ state), `fact_state_changes` vs `silent_state_fixed` with `nonreify_carrier_bound` (state ≠ carrier), `reifyUntagged_two_admissions` + `untagged_translation_collapsed` (carrier ≠ witnessed), `occurrence_state_swap_invariant` vs `tagged_state_not_swap_invariant` (per-act vs per-declaration orientation).
- Equivalence refuting an assumed non-equivalence: `reifyUntagged_eq_occurrence`.
- Not proved: the four-way determination as one theorem quantified over histories and modes (R9 `[unresolved]`); any statement for carriers above 2 or for refusals of *distinct* tokens; that `taggedTranslation` is the image of a defined translation map (it is a hand-written regime; the "translation" is a reading); that `swapState` is the only relevant symmetry. `tagged_translation_separable` exhibits one separating context (`⟨0, [none]⟩`); it does not characterise all contexts.
- `nonreify_carrier_bound` is one step; the history-level bound follows by the same induction as `Bridge.single_token_carrier_bound` but is not written here.

## 7. Axiom dependencies

All 16 artifact entries within `{propext, Quot.sound}`; the two helpers not in the artifact were not probed (their consumers `markers_invisible`, `reifyUntagged_replay_eq_occurrence` are in the artifact with `propext, Quot.sound`, which bounds the helpers' axioms). None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). 16 of 18 theorems are in `artifacts/lean_axioms.txt` and in the root inventory; `markers_invisible_from` and `reify_occ_from` are not (helpers). The paper cites the 16. No probe run (all concrete facts are `decide`; the generic ones are `rfl`/`simp` case splits read in full).

## 9. Related Python implementations

`code/derivation/refusal.py`: `RSt`, `readmit_silent`, `readmit_meta`, `readmit_fact`, `readmit_reify_untagged`, `readmit_reify_tagged`, `step`, `observable_profile`, `separable`, `swap_two`, `reachable`, `discipline_report`, `equivalence_check`, `orientation_check`, `capability_prices`; artifact `artifacts/refusal.json`. Tests `tests/test_refusal.py`: `test_silent_readmission_is_designation`, `test_fact_counts_without_growth`, `test_reify_tagged_two_admissions_witnessed_oriented`, `test_reify_untagged_symmetric_and_collapsed`, `test_equivalence_reify_untagged_is_occurrence`, `test_orientation_check`, `test_capability_prices_cover_all_disciplines`, and others.

## 10. Textbook placement proposal

- Prerequisites: Bridge (the dedup discipline and the equivariance obstruction); the regime model's `separable`/`collapsed` (Basic, Inertia); what a declared step function is.
- Substantive: `silent_eq_meta` + `markers_invisible`, `fact_state_changes`/`silent_state_fixed` + `nonreify_carrier_bound`, `reifyUntagged_eq_occurrence`, `reifyTagged_two_admissions` + `tag_separates`, `occurrence_state_swap_invariant` vs `tagged_state_not_swap_invariant` + `canonical_designation`, `tagged_translation_separable` + `untagged_translation_collapsed`. Auxiliary: `marker_state_invisible`, the two `_from` helpers, `reifyUntagged_replay_eq_occurrence`, `reifyUntagged_two_admissions`.
- Lesson title: "Refusal as a source of difference: four rungs and one price." Question answered: which way of recording a refused re-admission yields a state another object can tell apart, and what that recording costs in declared capability.
- Recommend omitting: the two `_from` helpers (inline the induction); `marker_state_invisible` (`rfl`).

## 11. Interpretation findings

1. `tagged_translation_separable` / `untagged_translation_collapsed` — paper R6: "the tagged two-occurrence state translates to the admission model's unary-mark regime, and the untagged one to the collapsed bare regime"; docstring: "The discipline's built-in observable is exactly one form plus one instance." Lean: two facts about two hand-written regimes, `⟨2,[1],[(0,[1])],[],[]⟩` and `⟨2,[],[],[],[]⟩`. No translation function from `RState` to `Regime` is defined, so "translates to" and "exactly" are readings; what is proved is that the chosen target regimes are separable resp. collapsed at `(0,1)`. Classification: INTERPRETATION DEFECT (minor; the correspondence between presentations is asserted, not defined).
2. Header: "The comparison yields a strict hierarchy ... with a separation at every gap" and R3's "strict hierarchy". Lean: each separation is a pair of concrete facts on `[admitTok 0, admitTok 0]` or a per-step lemma; there is no theorem stating the hierarchy or quantifying over histories (the paper's own R9 lists this as `[unresolved]`). Not a defect; recorded as a scope limit the textbook should repeat.
3. `nonreify_carrier_bound` — paper R3: "its carrier provably never leaves the singleton" (fact discipline). Lean: a one-step invariant preservation under a single-token event; the history-level statement is by an unwritten induction. Classification: INTERPRETATION DEFECT (minor; "never" is the induction over histories, not stated).
4. `swapState` — R5: "the untagged two-occurrence state is swap-invariant: its two elements are symmetric". Lean: `swapState` permutes tag indices only; with `data = [0,0]` this is the only visible action, so the reading is sound for this state, but it is not a statement about all automorphisms of `RState`. Not a defect; noted.
5. Vacuity: none found; all hypotheses satisfiable.
6. Finitude: tags are list positions (`s.data.length`) — a metatheoretic count admitted as object data by the discipline declaration. The paper prices it ("imports exactly the capabilities of the explicit route"). No defect.
