# Audit: QuotientRetention

| field | value |
|---|---|
| Path | lean4/Derivation/QuotientRetention.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | fe38f8acab7ff1ea |
| Lines | 143 |
| Imported by root `Derivation.lean` | yes (line 58) |
| Imports | Derivation.PresentationDescent (nothing from it is used; the import places the module in the fidelity chain) |
| Declarations | 1 structure (`RelationRefinement`, Prop-valued), 1 def (`collapseMap`), 9 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 9 lines (`Derivation.lean:1475`–`1483`); axioms seen: none (`RelationRefinement.refl`, `.trans`), `Quot.sound` (`collapseMap_mk`, `collapseMap_surjective`, `collapseMap_compose`), `propext, Quot.sound` (the other four). (The inventory JSON missed the two dotted names; they are in the artifact at lines 1341–1342.) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

On an arbitrary carrier `I`, let `coarse` be a former identification (a setoid) and `fine` a refinement of it: every `fine` identification was already a `coarse` one. There is a canonical collapse map `Quotient fine → Quotient coarse` that chooses no representatives. The module proves it is always surjective, and that it is injective exactly when every `coarse` identification survives in `fine`. Hence an identification made by `coarse` and refused by `fine` leaves two distinct refined classes with one coarse image: the attempted collapse fails to be injective, and the multiplicity the finer relation retains is exactly the identification the coarser one can no longer carry down. Successive refinements compose. No class is manufactured; a former identification merely ceases to descend. This is the quotient-level form of "retention", proved for any carrier and any supplied pair of equivalence relations in refinement position.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `RelationRefinement fine coarse` | 29 | structure (Prop) | `∀ {x y}, fine.r x y → coarse.r x y`. | ADMITTED (the hypothesis every theorem carries) |
| `collapseMap h` | 44 | def | `Quotient.lift (Quotient.mk coarse) (…)` : `Quotient fine → Quotient coarse`. | ADMITTED (canonical construction via the quotient universal property) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `RelationRefinement.refl` | 32 | Every setoid refines itself. | FROZEN | none | A |
| `RelationRefinement.trans` | 36 | Refinement composes. | FROZEN | none | A |
| `collapseMap_mk` | 51 | `collapseMap h ⟦x⟧_fine = ⟦x⟧_coarse` (rfl). | FROZEN | Quot.sound | A |
| `collapseMap_surjective` | 58 | `collapseMap h` is surjective. | FROZEN | Quot.sound | S |
| `failed_identification_retains_two_classes` | 67 | If `coarse.r x y` and `¬ fine.r x y`, then `⟦x⟧_fine ≠ ⟦y⟧_fine` and their collapses agree. | CONDITIONAL: `coarse.r x y`, `¬ fine.r x y` | propext, Quot.sound | S |
| `failed_identification_makes_collapse_noninjective` | 82 | Same hypotheses: `¬ Function.Injective (collapseMap h)`. | CONDITIONAL: same | propext, Quot.sound | S |
| `collapseMap_injective_iff_reverse_refinement` | 98 | `Function.Injective (collapseMap h) ↔ ∀ {x y}, coarse.r x y → fine.r x y`. | FROZEN | propext, Quot.sound | S |
| `symmetry_failure_retains_multiplicity` | 118 | For any `sigma : I → I` and `x` with `coarse.r x (sigma x)` and `¬ fine.r x (sigma x)`: two distinct fine classes with one collapse image. | CONDITIONAL: `hbefore`, `hafter` (instance of the previous with `y := sigma x`) | propext, Quot.sound | A |
| `collapseMap_compose` | 134 | `collapseMap (hfm.trans hmc) = collapseMap hmc ∘ collapseMap hfm` (funext). | FROZEN | Quot.sound | A |

## 4. External and admitted assumptions

- Core `Setoid`, `Quotient`, `Quotient.lift`, `Quotient.sound`, `Quotient.exact`, `Quotient.inductionOn`; `Function.Injective`, `Function.Surjective`; `funext`. These are the standard quotient universal property and do the real work (`Quotient.exact` is the direction "equal classes ⇒ related", which is what makes `failed_identification_retains_two_classes` go through).
- `I : Type` arbitrary; `fine coarse : Setoid I` supplied. **Generality:** the retention results are proved for *every* carrier and *every* pair of setoids in refinement position, not for a specific relation refinement. The only hypothesis is `RelationRefinement fine coarse` plus, where stated, a concrete failed identification `(x, y)`.
- `sigma : I → I` in `symmetry_failure_retains_multiplicity` is an arbitrary ambient function with no involution or invariance law — it is used only to name `y := sigma x`. Finitude rule: metatheoretic; nothing in the prose reads it as an internal symmetry of the system.
- Unearned identity: none found (all class equalities come from `Quotient.sound` on a supplied relation witness).
- Unrestricted external universe: `I : Type` is a parameter, not a field; `Quotient` lives in the same universe. None found.
- Unbounded function treated as internally available: `sigma` (above), harmless.
- Silently assumed observer / unspecified correspondence / cost function / admitted-then-forced / finite-as-universal: none found for each.

## 5. Derived consequences

- `EndogenousFidelityGenerator` (line 30 `open … QuotientRetention`; lines 71–84) proves `RelationRefinement (fidelitySetoid N) (indiscreteSetoid N.Index)` and uses `collapseMap` and `collapseMap_surjective` to define and analyse the "universal collapse"; its `no_coherent_path_retains_multiplicity` is an instance of `failed_identification_retains_two_classes`.
- `RenamingStructure.lean` has its own unrelated `def collapseMap : Nat → Nat := fun _ => 0` (a countermodel of invertibility); name coincidence only.
- Paper: ledger CL-QUOTIENT-RETENTION; change log 2026-08-14; `native_derivation_completion.md` §19 ("A missing path retains two quotient classes"). Not cited in `paper/paper.md`.
- `code/derivation/completion.py` lines 781–796 bind all nine names.

## 6. Counterexamples and limitations

- `failed_identification_makes_collapse_noninjective` is the countermodel-shaped theorem (it refutes injectivity from a single failed identification). Probe instance: `I = Bool`, `fine` = equality, `coarse` = the indiscrete setoid, `x = false`, `y = true`.
- The module proves nothing about *which* identification fails or whether the failure is forced; it takes the failed pair as a hypothesis. It also proves no finiteness, counting or representative statement (ledger non-claims).
- `symmetry_failure_retains_multiplicity` adds no content beyond `failed_identification_retains_two_classes` (no law on `sigma` is used).

## 7. Axiom dependencies

All within {propext, Quot.sound}; `Quot.sound` is intrinsic to any quotient argument here. None exceeds.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- All nine theorems in `artifacts/lean_axioms.txt` (the ledger: "the nine `QuotientRetention.*` theorem reports").
- Probe: `/tmp/claude-0/-home-claude/47be43b5-43cb-5429-bc31-b53a81ca595d/scratchpad/probes/F2/cs_qr_probe.lean`, exit 0: `collapseMap_injective_iff_reverse_refinement` depends on `[propext, Quot.sound]`; the `Bool` instance of `failed_identification_makes_collapse_noninjective` typechecks with `fine := (· = ·)`, `coarse := indiscrete`.

## 9. Related Python implementations

- Tag bindings only (`code/derivation/completion.py` 781–796, `tests/test_completion.py`). The Python kernel's `iso.py`/`observe.py` quotient data by observational equivalence, but no Python function implements a collapse map between two setoids or tests its injectivity for this module: none found.

## 10. Textbook placement proposal

- Prerequisites: equivalence relations and quotients; `Quotient.lift`/`sound`/`exact` as the universal property; the idea of a former identification being refined.
- Substantive: `collapseMap` + `collapseMap_surjective`, `collapseMap_injective_iff_reverse_refinement`, `failed_identification_retains_two_classes`.
- Auxiliary: `RelationRefinement.refl/trans`, `collapseMap_mk`, `failed_identification_makes_collapse_noninjective`, `symmetry_failure_retains_multiplicity`, `collapseMap_compose`.
- Suggested lesson: "Why does a refused identification leave two classes?" — answering: because the collapse to the old quotient is onto but loses injectivity exactly at the refused pair.
- Recommend omitting: `symmetry_failure_retains_multiplicity` (a renaming of `y` as `sigma x`; its docstring "The user's symmetry form" is a provenance note, not mathematics).

## 11. Interpretation findings

1. Docstring of `symmetry_failure_retains_multiplicity` (line 115): "a former exchange identification that fails after refinement". Lean: `sigma` is an arbitrary function; no "exchange" (involution) law is assumed or used. INTERPRETATION DEFECT (minor: the docstring suggests a symmetry where the theorem uses only a point). The phrase "The user's symmetry form" also records that the statement shape was supplied from outside the module; it carries no mathematical weight.
2. Ledger CL-QUOTIENT-RETENTION "for arbitrary carrier `I` and supplied setoids": matches the Lean exactly; the retention result is general, not tied to a specific refinement. None found.
3. Vacuity: `RelationRefinement fine coarse` together with `coarse.r x y ∧ ¬ fine.r x y` is satisfiable (probe); `collapseMap_injective_iff_reverse_refinement` is non-trivial in both directions. None found.
