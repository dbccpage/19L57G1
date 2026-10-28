# Audit: NoOutsideFidelity

| field | value |
|---|---|
| Path | lean4/Derivation/NoOutsideFidelity.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 421e14d82f9619e6 |
| Lines | 105 |
| Imported by root `Derivation.lean` | yes (line 60) |
| Imports | Derivation.FidelityClosure, Derivation.PresentationRelativity |
| Declarations | 2 defs (`supportTranslationPair`, `supportTotalization`), 6 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 6 lines; axioms seen: `propext` (5), `propext, Quot.sound` (`notes_fiber_has_no_operational_authority`) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The kernel's operational support projection `supp : World → Supp` forgets exactly the `notes` field of the seven-field `World` record. This module places that fact in the translation calculus of PresentationDescent. Two worlds (`genesis` and `genesis` with `notes := [0]`) share a support and differ, so `supp` is not injective. For *every* proposed backward map `Supp → World`, the resulting total translation pair fails round-trip coherence (a coherent left inverse would make `supp` injective), hence no faithful common descent can erase the `World`/`Supp` presentation index while preserving this forward projection. At the same time the notes fiber has no operational authority: replaying any history from two worlds that differ only in notes gives the same support, repair family, obstruction verdict and quiescence (restating `effectual_outside_dichotomy`). The module does not assert an absolute outside; it identifies the repository's operational use of "outside" with the fiber of a declared non-invertible presentation map.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `supportTranslationPair backward` | 48 | def | `TranslationAttempt World Supp` with `forward w := some (supp w)`, `backward s := some (backward s)`. | ADMITTED (`backward` is a universally quantified parameter) |
| `supportTotalization backward` | 53 | def | The evident `Totalization` (`forward := supp`, `backward := backward`, both realizations `rfl`). | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `support_fiber_contains_distinct_notes` | 30 | `∃ w w' : World, supp w = supp w' ∧ w.notes ≠ w'.notes ∧ w ≠ w'` (witness `genesis`, `{genesis with notes := [0]}`). | VERIFIED_FINITE (concrete witness; `decide` on `[] ≠ [0]`) | propext | S |
| `support_projection_not_injective` | 40 | `¬ Function.Injective supp`. | FROZEN (follows from the finite witness; the statement is about the whole function) | propext | S |
| `support_translation_never_round_trip_coherent` | 62 | For every `backward : Supp → World`, `¬ RoundTripCoherent (supportTotalization backward)`. | FROZEN (universal over `backward`; uses only the `left` triangle) | propext | S |
| `support_translation_never_faithfully_erases_index` | 75 | For every `backward`, `¬ Nonempty (FaithfulCommonDescent (supportTotalization backward))`. | FROZEN | propext | S |
| `no_support_inverse_faithfully_erases_index` | 83 | `¬ ∃ backward, Nonempty (FaithfulCommonDescent (supportTotalization backward))`. | FROZEN (restatement) | propext | A |
| `notes_fiber_has_no_operational_authority` | 92 | For any `w`, `newNotes`, `history`, `requirement`: the four kernel results after replay agree between `{w with notes := newNotes}` and `w`. | FROZEN (alias of `PresentationRelativity.notes_update_kernel_results_agree`, itself an instance of `NoOutside.effectual_outside_dichotomy`) | propext, Quot.sound | S |

## 4. External and admitted assumptions

- From Represented/NoOutside: the seven-field `World` record with its `notes : List Nat` field, `Supp`, `supp`, `genesis`, `replay`, `repairFamily`, `obstructedB`, `quiescentB`, `Event`, `Req`. From PresentationDescent: `TranslationAttempt`, `Totalization`, `RoundTripCoherent`, `FaithfulCommonDescent`, `incoherence_forces_index_retention`. From PresentationRelativity: `notes_update_kernel_results_agree`.
- The quantification `∀ backward : Supp → World` ranges over all ambient Lean functions (finitude rule). Here that is the intended strength: the result is a *negative* universal, and a negative over a larger class is a stronger refutation, not a smuggled capacity. The header says "universal over the backward map".
- The import of `FidelityClosure` is not used by any declaration (checked: no `FidelityPath`, `FidelityRel`, `TranslationNetwork` occurs); only PresentationDescent names are used.
- Unearned identity: none found. The one equality chain (`w = backward (supp w) = backward (supp w') = w'`) uses the hypothesised `left` triangle.
- Unrestricted external universe: only through `FaithfulCommonDescent`'s `Carrier : Type` (see PresentationDescent); the theorems here are negations, so a larger universe only strengthens them.
- Unbounded function treated as internally available: `backward` (above — universally quantified, not possessed).
- Silently assumed observer: none found.
- Unspecified correspondence between presentations: none found; the forward correspondence is the fixed `supp`.
- Cost function: none.
- Admitted condition later described as forced: none found.
- Finite computation presented as universal: `support_fiber_contains_distinct_notes` is a two-element witness; `support_projection_not_injective` correctly generalises it to a `¬ Injective` statement, which only needs one witness pair.

## 5. Derived consequences

- No module under `lean4/Derivation/` imports `NoOutsideFidelity` (grep: only itself).
- Paper: ledger CL-ENDOGENOUS-FIDELITY-GENERATOR "Operational witness" paragraph; `endogenous_generator.md` ~lines 261–268; change log 2026-08-14 ("This is not an ontological no-outside theorem"). Individual theorem names are not cited in `paper/` (grep: none). Not cited in `paper/paper.md`.
- `code/derivation/completion.py` lines 816–827 bind the six names.

## 6. Counterexamples and limitations

- `support_fiber_contains_distinct_notes` is the countermodel: the pair `(genesis, genesis with notes := [0])` refutes injectivity of `supp`.
- Scope: the failure is of *this* correspondence (`supp` forward, any backward). It does not say that no bijection `World ≃ Supp` exists as types (none is possible by cardinality only if `List Nat` is infinite in the relevant sense — not checked and not claimed), and it says nothing ontological. The header and all three prose sources state this.
- Only the left triangle is used; the right triangle (`supp (backward s) = s`) may or may not hold for a given `backward` — not checked, not needed.
- `notes_fiber_has_no_operational_authority` is a renaming of an existing theorem; it adds no content.

## 7. Axiom dependencies

Five theorems use `propext` only (from `simp [genesis]`); `notes_fiber_has_no_operational_authority` inherits `propext, Quot.sound` from `effectual_outside_dichotomy`. None exceeds {propext, Quot.sound}.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- All six theorems in `artifacts/lean_axioms.txt` (ledger: "six `NoOutsideFidelity.*` … theorem reports").
- Probe: `textbook/audit/probes/F2/fid_probe.lean`, exit 0: `no_support_inverse_faithfully_erases_index` depends on `[propext]`.

## 9. Related Python implementations

- `code/derivation/completion.py` 816–827 (bindings), `tests/test_completion.py`. The Python kernel `code/derivation/model.py` has no `notes` field and no `supp` projection (grep `notes`, `def supp` in `code/derivation/*.py`: only the completion bindings and an unrelated `support` in `boundary_cancellation.py`). None found.

## 10. Textbook placement proposal

- Prerequisites: the `World`/`Supp` records and `supp`; `effectual_outside_dichotomy` (NoOutside); PresentationDescent's round-trip criterion.
- Substantive: `support_translation_never_round_trip_coherent` and `support_translation_never_faithfully_erases_index` (the universal-over-`backward` negative), with `support_fiber_contains_distinct_notes` as its witness; `notes_fiber_has_no_operational_authority` as the companion "and yet notes change nothing operational".
- Auxiliary: `support_projection_not_injective`, `no_support_inverse_faithfully_erases_index`, the two defs.
- Suggested lesson: "Is the notes field 'outside' the kernel?" — answering: it is outside the support projection's image of distinctions (no inverse can recover it) and outside operational authority (it changes no verdict); both facts are about a declared projection, not about a world.
- Recommend omitting: `no_support_inverse_faithfully_erases_index` (identical content to the `∀` form).

## 11. Interpretation findings

1. **Header line 17–18: "no faithful coincident-image descent can erase the `World`/`Supp` presentation index".** Lean: `¬ Nonempty (FaithfulCommonDescent (supportTotalization backward))`, where `FaithfulCommonDescent` is defined by injective embeddings plus the two identification equations (coincident images is a consequence). Same phrasing issue as PresentationDescent §11.1; harmless here since the statement is a negation (a negation over the Lean definition implies the negation over any stronger prose definition). INTERPRETATION DEFECT (wording, inherited).
2. **Ledger: "the existing support projection cannot participate in a coherent round trip with any proposed backward map".** Matches `support_translation_never_round_trip_coherent` exactly. None found.
3. Vacuity: `supportTotalization backward` always exists (both arrows total), so the negated coherence is not vacuous by absence of a totalization. The witness pair is concrete. None found.
