# Audit: G1Class

| field | value |
|---|---|
| Path | lean4/Derivation/G1Class.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 3b5e2a5dd75f51e9 |
| Lines | 45 |
| Imported by root `Derivation.lean` | yes (line 53) |
| Imports | `Derivation.LocalStrategy` (the only importer of that module) |
| Declarations | 3 theorems, no definitions; namespace `G1Class`, `open LocalFiniteAlphabet` |
| Axiom reports in `artifacts/lean_axioms.txt` | 3 lines; all propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

A naming module: it states the class-relative G1 exclusion separately from the class definition, so that the terminal can be cited by one name. `local_strategy_cycle_impossible` is the "strongest target form": for a finite declared local member the conjunction fires-and-clears-and-no-recurring-import is impossible, with no identity-grade premise. `g1_class_exclusion` is `LocalFiniteAlphabet.g1_local_finite_alphabet_class` under its terminal name. `clears_does_not_imply_not_fires` is the G3 counterexample: the valued strategy both clears and fires, so clearing the inherited pairs does not stop the inherited family from firing; a theorem relating repair to the absence of future demand would need a state-transition hypothesis the class does not have.

## 2. Definitions and structures

None.

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `local_strategy_cycle_impossible` | 22 | `FiniteDeclaration k S → ¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S)` | CONDITIONAL:`FiniteDeclaration k S` | propext, Quot.sound | S |
| `g1_class_exclusion` | 30 | `FiniteDeclaration k S → Fires S ∧ ¬ Clears S ∧ ¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S)` (`:= g1_local_finite_alphabet_class`) | CONDITIONAL:`FiniteDeclaration k S` | propext, Quot.sound | S |
| `clears_does_not_imply_not_fires` | 41 | `∃ S : LocalStrategy 0, Clears S ∧ Fires S` (witness `valued`) | REFUTED (of "clears ⇒ not fires") | propext, Quot.sound | S |

## 4. External and admitted assumptions

Everything is inherited from `LocalStrategy` (see that record §4): `Fires` is independent of `S`; `RecurringImport` reads a declared tag; `FiniteDeclaration` is the hypothesis. The header's non-claims ("not unrestricted G1", "does not change the inherited closure-policy obligation") are accurate. Unearned identity / external universe / unbounded function / silent observer / unspecified correspondence / cost function / admitted-as-forced / finite-as-universal: none beyond those recorded for `LocalStrategy`.

## 5. Derived consequences

No Lean module consumes `G1Class.*` (grep: only `Derivation.lean`'s `#print axioms`). Ledger: `CL-G1-CLASS-EXCLUSION` (both exclusion theorems), `CL-G1-G3-COUNTEREXAMPLE`, `CL-G1-TERMINAL-20260826`. Paper: `paper/endogenous_generator.md` 2026-08-26 section ("G1Class.g1_class_exclusion proves, for every finite declared local member, …"; "G1Class.clears_does_not_imply_not_fires exhibits …").

## 6. Counterexamples and limitations

`clears_does_not_imply_not_fires` refutes the implication `Clears S → ¬ Fires S`. Since `Fires` holds for every `S` (`fires_every_strategy`), *any* clearing member would do; the valued member is simply the one in the class that clears. The ledger says G3 "remains conjectural" and "needs an additional state-transition hypothesis". Not proved: unrestricted G1; anything dynamic.

## 7. Axiom dependencies

All three within `{propext, Quot.sound}`. None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All three theorems in the artifact; cited by name in the ledger and paper. No probe run.

## 9. Related Python implementations

`code/derivation/g1_class_receipt.py` (binds the exact class theorem reports and boundary statements; `tests/test_g1_class_receipt.py`); `code/derivation/local_strategy.py` rows for the valued strategy (`classification`, `tests/test_local_strategy.py::test_identity_and_import_boundaries_are_nonvacuous`).

## 10. Textbook placement proposal

- Prerequisites: the LocalStrategy lesson.
- Substantive: `g1_class_exclusion` (as the named terminal) and `clears_does_not_imply_not_fires` (as the reason G3 is not a corollary). Auxiliary: `local_strategy_cycle_impossible` (a weakening of the terminal).
- Lesson title: "What G1 says inside the class, and what G3 would need." Question answered: does excluding the fire/clear/no-import conjunction for finite local members settle G1 or G3? Only class-relative G1; G3 needs a transition model.
- Recommend omitting: `local_strategy_cycle_impossible` as a separate theorem (it is the third conjunct of `g1_class_exclusion`).

## 11. Interpretation findings

1. `clears_does_not_imply_not_fires` — docstring: "the one-time valued rule clears every inherited pair while the pre-repair reflective family still fires". Lean: `Clears valued ∧ Fires valued`, where `Fires` does not depend on the strategy at all. The counterexample is therefore immediate from the definitions (every strategy fires), and the ledger's framing "G3 needs an additional state-transition hypothesis" is the right conclusion; but the theorem should be taught as "the predicates as defined cannot express repair stopping the demand", not as a discovery about the valued rule. Classification: INTERPRETATION DEFECT (minor; the ledger entry `CL-G1-G3-COUNTEREXAMPLE` already says "under the current definitions").
2. `g1_class_exclusion` — see LocalStrategy §11 item 1 ("cycle", "member fires"). Same finding, same classification.
3. Vacuity: none beyond `k = 0`.
