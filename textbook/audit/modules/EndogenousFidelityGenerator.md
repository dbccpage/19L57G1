# Audit: EndogenousFidelityGenerator

| field | value |
|---|---|
| Path | lean4/Derivation/EndogenousFidelityGenerator.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | da23fec966aee7fb |
| Lines | 109 |
| Imported by root `Derivation.lean` | yes (line 61) |
| Imports | Derivation.FidelityClosure (transitively QuotientRetention, PresentationDescent) |
| Declarations | 3 defs (`AdmittedStep`, `indiscreteSetoid`, `universalCollapse`), 1 abbrev (`GeneratedMultiplicity`), 6 theorems |
| Axiom reports in `artifacts/lean_axioms.txt` | 6 lines; axioms seen: none (3), `Quot.sound` (`universalCollapse_surjective`), `propext, Quot.sound` (2) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

The module states the universal property of the fidelity relation of FidelityClosure: `fidelitySetoid N` is the least equivalence relation on presentation indices that contains every *admitted step* (an attempt whose scoped arrows totalize with coherent round trips). It then compares the generated quotient with the attempted *indiscrete* quotient in which every index is erased: fidelity always refines indiscreteness, so QuotientRetention's collapse map `universalCollapse` from the generated quotient to the one-point quotient is surjective, and whenever no coherent path joins two indices their generated classes are distinct while their indiscrete images coincide. "Structure" is thus read as multiplicity that the attempted total erasure fails to remove — produced by closure under coherent translations, with no class created and no observer choosing. The network and its attempts remain supplied; the module derives their closure, not a first presentation.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `AdmittedStep N i j` | 33 | def | `∃ (a : N.Attempt i j) (u : Totalization (N.pair a)), RoundTripCoherent u`. | ADMITTED (the declared admission criterion, restated as a Prop) |
| `indiscreteSetoid I` | 61 | def | The setoid with `r _ _ := True`. | ADMITTED (the "attempted universal collapse" — a comparison ceiling) |
| `GeneratedMultiplicity N` | 74 | abbrev | `FidelityQuotient N`. | ADMITTED |
| `universalCollapse N` | 78 | def | `collapseMap (fidelity_refines_indiscrete N) : FidelityQuotient N → Quotient (indiscreteSetoid N.Index)`. | ADMITTED |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `admitted_step_has_fidelity_path` | 37 | `AdmittedStep N i j → FidelityRel N i j`. | FROZEN | none | A |
| `fidelity_is_least_equivalence_containing_admitted_steps` | 46 | For any setoid `S` on `N.Index` containing every admitted step, `FidelityRel N i j → S.r i j` (induction on paths). | FROZEN | none | S |
| `fidelity_refines_indiscrete` | 70 | `RelationRefinement (fidelitySetoid N) (indiscreteSetoid N.Index)`. | FROZEN (trivial: target is `True`) | none | A |
| `universalCollapse_surjective` | 82 | `universalCollapse N` is surjective. | FROZEN (instance of `collapseMap_surjective`) | Quot.sound | A |
| `no_coherent_path_retains_multiplicity` | 89 | `NoCoherentPath N i j → classOf N i ≠ classOf N j ∧ universalCollapse N (classOf N i) = universalCollapse N (classOf N j)`. | CONDITIONAL: `NoCoherentPath N i j` | propext, Quot.sound | S |
| `generated_structure_is_failed_erasure` | 100 | `NoCoherentPath N i j → ∃ a b : GeneratedMultiplicity N, a ≠ b ∧ universalCollapse N a = universalCollapse N b`. | CONDITIONAL: `NoCoherentPath N i j` | propext, Quot.sound | S |

## 4. External and admitted assumptions

- From FidelityClosure: `TranslationNetwork`, `FidelityPath`, `FidelityRel`, `fidelitySetoid`, `classOf`, `NoCoherentPath`; from QuotientRetention: `RelationRefinement`, `collapseMap`, `collapseMap_surjective`, `failed_identification_retains_two_classes`; from PresentationDescent: `Totalization`, `RoundTripCoherent`.
- **Is the "endogenous" generator derived from inside the regime model or admitted as a structure?** Admitted as a structure, with one derived universal property. `TranslationNetwork` (indices, carriers, attempts) is a supplied `Type 1` structure unrelated to `Regime`, `World`, `DiffObs` or any kernel object; the admission criterion (totalize + cohere) is declared in `FidelityPath.step`; what is *derived* is that the closure of the admitted steps is the least equivalence containing them (`fidelity_is_least_equivalence_containing_admitted_steps`) and that it refines the indiscrete setoid. The header (lines 22–25) says: "The translation network is still supplied … an endogenous closure relative to declared presentations and attempts, not an absolute origin". The word "generator" names the free-closure construction, not a mechanism of the regime model.
- The second half of the retained-multiplicity theorem — `universalCollapse N (classOf N i) = universalCollapse N (classOf N j)` — is immediate (`True.intro` is the coarse relation witness); the content is the first conjunct, inherited from `class_eq_iff_coherent_path`.
- `NoCoherentPath` is a negative existential over all paths (finitude rule: metatheory; the header line 22–23 says "a proposition, not a claimed decision procedure").
- Unearned identity / unrestricted universe (beyond the supplied `Type`-valued fields) / unbounded internal function / silently assumed observer / unspecified correspondence / cost function / admitted-then-forced / finite-as-universal: none found for each.
- Library lemmas doing real work: induction on the `FidelityPath` inductive (the least-equivalence proof); `Quotient` lemmas via QuotientRetention.

## 5. Derived consequences

- No module under `lean4/Derivation/` imports `EndogenousFidelityGenerator` (grep: only itself).
- Paper: ledger CL-ENDOGENOUS-FIDELITY-GENERATOR; `native_derivation_completion.md` §19 ("proves the universal property"); `endogenous_generator.md` ~line 253–257 ("`generated_structure_is_failed_erasure` states the resulting multiplicity as failure of the attempted universal collapse … endogenous closure relative to a supplied translation network"); change log 2026-08-14. Not cited in `paper/paper.md`.
- `code/derivation/completion.py` lines 829–840 bind the six names.

## 6. Counterexamples and limitations

- No countermodel theorem; the two retention theorems are positive consequences of a hypothesised `NoCoherentPath`.
- The theorems quantify over an arbitrary supplied network; nothing exhibits a network in which `NoCoherentPath` holds between two *interesting* indices. The probe for FidelityClosure (a network with no attempts) shows the hypothesis is satisfiable, so the theorems are not vacuous, but the content in that case is trivial (every class is a singleton).
- Not proved and not claimed: that the fidelity quotient is finite, decidable, or has more than one class for any specific regime; that the admission criterion is forced; that any kernel event generates a translation network.

## 7. Axiom dependencies

Three theorems axiom-free; `universalCollapse_surjective` uses `Quot.sound`; the two retention theorems `propext, Quot.sound`. None exceeds {propext, Quot.sound}.

## 8. Verification status

- Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0).
- All six theorems in `artifacts/lean_axioms.txt` (ledger: "six `EndogenousFidelityGenerator.*` … theorem reports").
- Probe: `textbook/audit/probes/F2/fid_probe.lean`, exit 0: `generated_structure_is_failed_erasure` depends on `[propext, Quot.sound]`; `NoCoherentPath emptyNet false true` is provable for a network with `Attempt := Empty` (so the hypothesis is satisfiable).

## 9. Related Python implementations

- `code/derivation/completion.py` 829–840 (bindings), `tests/test_completion.py`. No Python implements admitted steps, least-equivalence closure or the indiscrete comparison: none found.

## 10. Textbook placement proposal

- Prerequisites: FidelityClosure (`FidelityPath`, `fidelitySetoid`, `classOf`, `NoCoherentPath`); QuotientRetention (`collapseMap`, `failed_identification_retains_two_classes`); the notion of a least equivalence containing a relation.
- Substantive: `fidelity_is_least_equivalence_containing_admitted_steps` (the universal property) and `no_coherent_path_retains_multiplicity` (the comparison with total erasure).
- Auxiliary: `admitted_step_has_fidelity_path`, `fidelity_refines_indiscrete`, `universalCollapse_surjective`, `generated_structure_is_failed_erasure` (existential restatement), the defs.
- Suggested lesson: "What is 'structure' once every identification you can justify has been made?" — answering: whatever the least justified equivalence still keeps apart, measured against the quotient that would erase everything.
- Recommend omitting: `generated_structure_is_failed_erasure` as a separate theorem (an existential repackaging of the preceding one); `fidelity_refines_indiscrete` (trivially `True`).

## 11. Interpretation findings

1. **Module title and `endogenous_generator.md` line 256: "endogenous closure".** Lean: the closure is of a *supplied* `TranslationNetwork` under a *declared* admission criterion; the only derived content is the universal property and the refinement of indiscreteness. The header and the prose both state the supply explicitly ("relative to a supplied translation network … does not generate the first presentations, declare which translations are admissible"). The textbook must not present this module as deriving a generator from the regime model (`Regime`/`World`); it is a structure admitted at the type level. INTERPRETATION hazard, self-corrected in both sources. No defect.
2. **Header line 17: "Structure is therefore retained multiplicity produced by closure under coherent translations."** Lean: `no_coherent_path_retains_multiplicity` says two classes survive *when no coherent path exists*; "structure" is a gloss on `GeneratedMultiplicity N` (an abbrev for the quotient). The sentence is definitional naming, not a theorem. INTERPRETATION DEFECT (minor): "structure" is introduced by abbreviation, and the theorem's second conjunct (`universalCollapse` identifies the images) is trivially true for *every* pair, not only non-connected ones.
3. **Ledger: "if no coherent path joins two supplied indices, they survive as distinct generated classes although the universal collapse identifies their images."** Accurate to the Lean, including that the collapse identifies all images. None found.
4. Vacuity: `NoCoherentPath` satisfiable (probe); `fidelity_is_least_equivalence_containing_admitted_steps` is non-trivial only because `FidelityPath` has `symm`/`trans` constructors that an arbitrary `S` must absorb — it is a genuine (if standard) induction. None found.
