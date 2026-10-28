# Audit: PresentationDescent

| field | value |
|---|---|
| Path | lean4/Derivation/PresentationDescent.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | ee3c6c5f79ef419f |
| Lines | 225 |
| Imported by root `Derivation.lean` | yes (line 57) |
| Imports | Derivation.PresentationNaturality |
| Declarations | 4 structures (`TranslationAttempt`, `Totalization`, `RoundTripCoherent` [Prop-valued], `FaithfulCommonDescent`), 2 inductives (`TranslationGap`, `CoherenceResidual`), 3 defs (`coherent_to_bij`, `CoincidentImages`, `coherent_to_faithful_descent`), 7 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 7 lines; axioms seen: `propext` for `translation_gap_refuses_totalization` (from `simp` on `Option`), none for the other six |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

Two presentation carriers `P` and `Q` are given as types, with no prior common carrier. A *translation attempt* is a pair of scoped (partial, `Option`-valued) maps between them; a *totalization* is a pair of total maps that realize the scoped ones exactly. The module asks when the two presentation indices can be faithfully erased — when there is a common carrier into which both presentations embed injectively so that each embedding agrees with the other composed with the translation. The answer is exact: such a *faithful common descent* exists if and only if the two round trips of the totalization close (`u.backward ∘ u.forward = id` and `u.forward ∘ u.backward = id`). A gap in a scoped translation refuses every exact totalization; a round-trip residual refuses every faithful common descent for that declared pair. The module claims nothing about other translation pairs and introduces no observer, metric or preferred quotient. `coherent_to_bij` links a coherent totalization to the `Bij` of `PresentationNaturality`.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `TranslationAttempt P Q` | 39 | structure | `forward : P → Option Q`, `backward : Q → Option P`. | ADMITTED (supplied arrows) |
| `Totalization t` | 46 | structure | Total `forward`, `backward` with `t.forward p = some (forward p)` and dually. | ADMITTED |
| `TranslationGap t` | 54 | inductive | A `p` with `t.forward p = none`, or a `q` with `t.backward q = none`. | ADMITTED |
| `RoundTripCoherent u` | 80 | structure (Prop) | `∀ p, u.backward (u.forward p) = p` and `∀ q, u.forward (u.backward q) = q`. | ADMITTED (the declared coherence 2-cell) |
| `CoherenceResidual u` | 87 | inductive (Type) | A point at which one of the two round trips fails. | ADMITTED |
| `coherent_to_bij h` | 104 | def | From `RoundTripCoherent u` build `Bij P Q`. | ADMITTED |
| `CoincidentImages left right` | 117 | def | Each image is contained in the other (`∀ p ∃ q, left p = right q` and dually). | ADMITTED |
| `FaithfulCommonDescent u` | 126 | structure (Type 1) | `Carrier : Type`, injective `left : P → Carrier`, `right : Q → Carrier`, `left p = right (u.forward p)`, `right q = left (u.backward q)`. | ADMITTED (the declared notion of "faithful descent"; its `Carrier : Type` field is metatheoretic existential output — see §4) |
| `coherent_to_faithful_descent h` | 156 | def | Witness with `Carrier := P`, `left := id`, `right := u.backward`. | ADMITTED (one witness; docstring disclaims preference) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `translation_gap_refuses_totalization` | 60 | A `TranslationGap t` implies `¬ Nonempty (Totalization t)`. | FROZEN | propext | S |
| `coherence_residual_refutes_round_trip` | 93 | A `CoherenceResidual u` implies `¬ RoundTripCoherent u`. | FROZEN | none | A |
| `faithful_common_descent_has_coincident_images` | 138 | Any `FaithfulCommonDescent u` has `CoincidentImages d.left d.right`. | FROZEN | none | A |
| `faithful_descent_to_coherent` | 176 | Any `FaithfulCommonDescent u` yields `RoundTripCoherent u` (uses both injectivity fields and both identification equations). | FROZEN | none | S |
| `faithful_descent_iff_round_trip_coherent` | 196 | `Nonempty (FaithfulCommonDescent u) ↔ RoundTripCoherent u`. | FROZEN | none | S |
| `incoherence_forces_index_retention` | 212 | `¬ RoundTripCoherent u → ¬ Nonempty (FaithfulCommonDescent u)`. | FROZEN | none | A |
| `residual_forces_index_retention` | 221 | A `CoherenceResidual u` implies `¬ Nonempty (FaithfulCommonDescent u)`. | FROZEN | none | S |

## 4. External and admitted assumptions

- Type parameters `P Q : Type` are the two presentations; nothing links them to any regime, data or observer in the kernel. The results are pure statements about functions between types.
- `FaithfulCommonDescent` carries a field `Carrier : Type`, so the structure lives in `Type 1` and `Nonempty (FaithfulCommonDescent u)` quantifies existentially over the ambient universe. Under the finitude rule this is metatheory: the docstring (line 121–124) says "`Carrier` is existential output data, not a common world assumed before `P` and `Q`". Flagged; not read by the prose as a system-internal container.
- The `Option`-valued scoped translations are supplied data; totality is a separate supplied witness (`Totalization`), never inferred.
- Unearned identity: none found — both equalities in `faithful_descent_to_coherent` are derived by cancelling an injective map.
- Unrestricted external universe: the `Carrier : Type` field (above). The theorem `faithful_descent_iff_round_trip_coherent` shows that universe quantification adds nothing: a descent exists iff one exists with `Carrier := P`.
- Unbounded function treated as internally available: none found (the maps are supplied parameters).
- Silently assumed observer: none found.
- Unspecified correspondence between presentations: none found — the correspondence is the explicit `Totalization`.
- Cost function: none.
- Admitted condition later described as forced: none found. "Forces index retention" is conditional on an explicit residual.
- Finite computation presented as universal: none (no finite computation here).
- Library lemmas doing real work: `simp` on `some _ = none` (gives `propext`); `Function.Injective`, `Function.injective_id`; `congrArg`; `calc`.

## 5. Derived consequences

- `FidelityClosure` builds `FidelityPath` steps from `Totalization (N.pair a)` + `RoundTripCoherent u` (its line 57–58) and uses `CoherenceResidual` (line 136).
- `NoOutsideFidelity` instantiates `TranslationAttempt World Supp`, `Totalization`, `RoundTripCoherent`, `FaithfulCommonDescent` for the support projection (lines 49–85).
- `EndogenousFidelityGenerator` quantifies over `Totalization (N.pair a)` with `RoundTripCoherent u` (line 35).
- Paper: ledger CL-FIDELITY-DESCENT (with a 2026-08-18 correction note on the statement of the right-hand side); `native_derivation_completion.md` §19 "Premetric fidelity closure and retained multiplicity"; `endogenous_generator.md` ~line 251; change log 2026-08-14 "Heterogeneous fidelity closure". Not cited in `paper/paper.md`.
- `docs/index/pins.md` line 352: five research trees pin this file (`coherent_process_limits`, `endogenous_demand`, `g010_primitive_removal`, `represented_execution`, `setting_translation`).

## 6. Counterexamples and limitations

- Countermodel-shaped theorems: `translation_gap_refuses_totalization` (a `none` refutes any exact totalization), `coherence_residual_refutes_round_trip`, `residual_forces_index_retention`. Each takes its witness as an explicit hypothesis; no concrete instance is built in this module (the concrete instance is `NoOutsideFidelity.support_translation_never_round_trip_coherent`).
- The module does not prove that failure of one pair rules out all equivalences between `P` and `Q` (header lines 26–28 say so explicitly); it does not say the disjoint union `P ⊕ Q` is a descent (excluded by `CoincidentImages` and the identification equations).
- `CoincidentImages` is derived, not part of the definition of descent — the ledger's 2026-08-18 correction records that an earlier prose version had it the wrong way round. `native_derivation_completion.md` line 498 still reads "`FaithfulCommonDescent` is independently defined by injective embeddings with coincident images" — see §11.

## 7. Axiom dependencies

Six theorems axiom-free; `translation_gap_refuses_totalization` uses `propext` only. Nothing exceeds {propext, Quot.sound}: none.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- All seven theorems are in `artifacts/lean_axioms.txt`; the ledger cites "the seven `PresentationDescent.*` theorem reports".
- Probe: `textbook/audit/probes/F2/cs_qr_probe.lean` (shared with ClosureSymmetry/QuotientRetention), exit 0: `#print axioms PresentationDescent.faithful_descent_iff_round_trip_coherent` → no axioms.

## 9. Related Python implementations

- `code/derivation/completion.py` lines 766–779 bind the seven theorem names to tags for the dependency graph; `tests/test_completion.py` pins them. No Python implements `TranslationAttempt`, `Totalization` or `FaithfulCommonDescent` (grep for `round_trip`, `faithful_descent`, `TranslationAttempt` in `code/` and `tests/`: only the binding entries).

## 10. Textbook placement proposal

- Prerequisites: injective functions and two-sided inverses; `Option` as a model of a partial map; `Bij` from PresentationNaturality.
- Substantive: `faithful_descent_iff_round_trip_coherent` (the exact criterion), `faithful_descent_to_coherent` (the direction that needs injectivity), `translation_gap_refuses_totalization`, `residual_forces_index_retention`.
- Auxiliary: `coherence_residual_refutes_round_trip`, `faithful_common_descent_has_coincident_images`, `incoherence_forces_index_retention`, `coherent_to_bij`, `coherent_to_faithful_descent`.
- Suggested lesson: "When can two presentation labels be dropped without loss?" — answering: exactly when the declared translations invert each other both ways; a single failed round trip keeps both labels for that pair.
- Recommend omitting: `CoincidentImages` as a taught notion (it is a derived property retained only to block the "coproduct is a descent" misreading; one sentence suffices).

## 11. Interpretation findings

1. **`native_derivation_completion.md` line 498**: "`FaithfulCommonDescent` is independently defined by injective embeddings with coincident images." Lean: `FaithfulCommonDescent` is defined by injective embeddings with the two *identification equations* `left p = right (u.forward p)` and `right q = left (u.backward q)`; coincident images is a *consequence* (`faithful_common_descent_has_coincident_images`). Injective embeddings with merely coincident images would not force coherence: take `P = Q = Bool`, `u.forward = not`, `u.backward = id` (so the left round trip `id (not p) = p` fails), and `left = right = id : Bool → Bool`, which are injective with coincident images; this would be a "descent" under the prose definition while `RoundTripCoherent u` is false. The Lean definition excludes it because `left p = right (u.forward p)` would require `p = not p`. The ledger CL-FIDELITY-DESCENT already corrected this wording on 2026-08-18; the completion write-up and `endogenous_generator.md` line 252 ("faithful common descent with coincident images") still carry the older phrasing. INTERPRETATION DEFECT (prose; Lean is correct).
2. Vacuity: `RoundTripCoherent u` is satisfiable (identity translations); `FaithfulCommonDescent u` is inhabited exactly when coherent. `TranslationGap t` is unsatisfiable when both scoped maps are total, which is the intended case split. No vacuous theorem found.
3. Docstring line 23 "forbids faithful elimination of its presentation index": matched by Lean (`¬ Nonempty (FaithfulCommonDescent u)` for the given `u`). None found.
