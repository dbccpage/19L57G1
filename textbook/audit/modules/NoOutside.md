# Audit: NoOutside

| field | value |
|---|---|
| Path | lean4/Derivation/NoOutside.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 8da63ea963fcabe5 |
| Lines | 270 |
| Imported by root `Derivation.lean` | yes (line 25) |
| Imports | Derivation.Represented |
| Declarations | 1 structure, 1 inductive, 5 def (stepC, replayC, certPosC, certNegC, PanelEquiv), 12 theorem (inventory counts 13 because a docstring word "transports;" matched its scan) |
| Axiom reports in `artifacts/lean_axioms.txt` | 12 lines; axioms seen: none / propext, Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

Stage IV asks for the strongest in-kernel form of Rule 2, "no observer from nowhere". It extends the one-step support factorization of `Represented` to whole histories, to the successor family, to the obstruction certificate and to the quiescence verdict, and bundles the four as the "effectual-outside dichotomy": two worlds that agree on the represented support and receive the same history agree on every operational result, so whatever changes an operational result already differs in the support. It lifts the invariance ceiling to family-valued constructions. And it removes the one piece of the certification story that still sat outside replay: in `Represented` the evaluator panel was a free argument of `certPosB`; here the panel becomes a field of an extended state `CWorld`, admitted by an `admitEvaluator` event, so a certificate is a function of replayed state. What is removed from the external viewer is exactly that free argument. What survives is the ceiling: panel-induced non-separation is an equivalence relation, the negative certificate is exactly joint-quotient membership for a non-empty panel, and `cert_not_correspondence` carries over verbatim — a unanimous panel still certifies an equivalence that a column outside the panel refutes. The module says in its own words that no metaphysical claim about unrepresented existence is made; the paper names the absolute form ABSOLUTE_NO_OUTSIDE_UNFORMULABLE.

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| CWorld | 125 | structure | a kernel `World` plus a panel `List Evaluator` | ADMITTED (conservative extension) |
| CEvent | 130 | inductive | `base e` or `admitEvaluator E` | ADMITTED (extended event grammar) |
| stepC | 135 | def | base events act by `step` on the base; admission appends a fresh evaluator | ADMITTED |
| replayC | 141 | def | fold of stepC | ADMITTED |
| certPosC / certNegC | 160 / 163 | def | `certPosB` / `certNegB` of the replayed panel | ADMITTED |
| PanelEquiv | 174 | def | ∀ E ∈ panel, ∀ c ∈ E, (i ∈ c ↔ j ∈ c): joint non-separation | ADMITTED (the declared joint quotient) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| support_replay | 32 | supp w = supp w' ⇒ supp (replay h w) = supp (replay h w') for every history h | FROZEN | propext, Quot.sound | S |
| support_repairFamily | 43 | supp-equal worlds have equal repair families (rfl after subst) | FROZEN | propext, Quot.sound | A |
| support_quiescent | 56 | supp-equal worlds have equal quiescence verdicts | FROZEN | propext, Quot.sound | A |
| support_obstructed | 68 | supp-equal worlds have equal obstruction certificates | FROZEN | propext, Quot.sound | A |
| effectual_outside_dichotomy | 91 | supp-equal worlds, same history ⇒ equal replayed support, repair family, certificate, quiescence | FROZEN | propext, Quot.sound | S |
| equivariant_family_invariant | 108 | for any types S, R, actions, and F with F (actS s) = (F s).map actR: a fixed point s has (F s).map actR = F s | FROZEN (pure metatheory; two-line calc) | none | A |
| stepC_conservative | 146 | base events act as `step` on `.base` and leave the panel (rfl, rfl) | FROZEN (definitional) | propext, Quot.sound | S |
| admitEvaluator_base_inert | 153 | admission leaves `.base` unchanged | FROZEN | propext, Quot.sound | S |
| replayC_deterministic | 167 | cw = cw' ⇒ replayC h cw = replayC h cw' (rw) | FROZEN (trivially true conclusion) | propext, Quot.sound | A |
| panel_equiv | 177 | PanelEquiv panel is an Equivalence | FROZEN | none | S |
| certNeg_iff_panelEquiv | 190 | certNegB panel i j = true ↔ panel ≠ [] ∧ PanelEquiv panel i j | FROZEN | propext, Quot.sound | S |
| certC_ceiling | 266 | the concrete `cert_not_correspondence` restated through certNegC (proof term is the sealed theorem) | VERIFIED_FINITE / REFUTED (refutes certification = correspondence in the integrated kernel) | propext, Quot.sound | S |

Count check: 12 theorems, all in the artifact.

## 4. External and admitted assumptions

- Everything about `World`, `step`, `supp`, `repairFamily`, `obstructedB`, `quiescentB`, `certPosB`, `certNegB`, `sepB`, `verdictB` comes from Represented and is admitted constitution there.
- The "outside" in the dichotomy is literally the complement of `supp` in `World`, i.e. the `notes` field alone (the companion module `NoOutsideFidelity.lean` line 7 says so explicitly). The theorems quantify over worlds differing only there. They are correct and the prose is explicit that the scope is operational and constitution-relative.
- `equivariant_family_invariant` quantifies over arbitrary `{S R : Type}`, arbitrary functions `actS`, `actR`, `F`, and an equivariance hypothesis. It is a statement of Lean's metatheory, not of the system (finitude flag: the `Type` parameters and function spaces are not system objects). Its content is a two-step rewrite.
- Library lemmas: `List.any_eq_true`, `List.all_eq_true`, `decide` on membership; structural `cases`/`subst`.
- Unearned identity: none found. Unrestricted external universe: the `{S R : Type}` parameters of `equivariant_family_invariant` (metatheory, flagged above). Unbounded function treated as internally available: none (panels are lists). Silently assumed observer: none; the panel is now data, admitted by an event. Unspecified correspondence between presentations: none. Cost function: none. Admitted condition later described as forced: none. Finite computation presented as universal: `certC_ceiling` is one concrete instance and is presented as a ceiling (a countermodel), which is the correct use of an instance.

## 5. Derived consequences

`Initiality.lean` uses `CWorld`, `stepC`, `replayC` for `extension_retract`, `extension_retract_replay`, `retract_section` (the panel extension retracts onto the kernel). `NoOutsideFidelity.lean` (a later module) analyses what `supp` forgets. Map row "replay factors through support" PROVED cites `support_replay`; row "certification panel certifies up to Zero/ZeroRel" cites `panel_equiv`. Ledger CL-NC-RULE2.

## 6. Counterexamples and limitations

- `certC_ceiling` is the only countermodel: panel [[[0,1]],[[0,1]]] certifies 0 ~ 1 while column [0] separates.
- Not proved, and said not to be: anything about unrepresented differences ("absolute no outside"); anything about positive certification being an equivalence (only the negative certificate is characterised; `certPosB` is not shown to induce a relation with any closure property); anything about panels that are not lists of column lists; completeness of the evaluator-admission grammar.
- `certNeg_iff_panelEquiv` requires `panel ≠ []` on the right: the empty panel certifies nothing while `PanelEquiv []` is vacuously total. The ledger records the scope (2026-08-18).
- `replayC_deterministic` has a trivially true conclusion (as `Represented.replay_deterministic`).

## 7. Axiom dependencies

All 12 within {propext, Quot.sound}; `equivariant_family_invariant` and `panel_equiv` use none. Theorems exceeding the set: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 12 theorems in the artifact. Paper cites all but `replayC_deterministic` (ledger CL-NC-RULE2; `paper/native_derivation_completion.md` §8, §13, §18). No probe run; proofs read in full (`certNeg_iff_panelEquiv` case-splits on the two decide values and discharges each branch; checked).

## 9. Related Python implementations

None found that mirror `CWorld`/`stepC`/`PanelEquiv`. `code/derivation/completion.py` lists `NoOutside.panel_equiv` only as a dependency-graph evidence name; `code/derivation/represented.py::cert_pos/cert_neg/certification_report` implement the un-integrated panel.

## 10. Textbook placement proposal

- Prerequisites: the Represented kernel; `supp`; `certPosB`/`certNegB`; the notion of an equivalence relation; `cert_not_correspondence`.
- Substantive: `support_replay`, `effectual_outside_dichotomy` (with its stated scope), `CWorld`/`stepC` as the move that puts the panel on the books, `panel_equiv`, `certNeg_iff_panelEquiv`, `certC_ceiling`.
- Auxiliary: `support_repairFamily`, `support_quiescent`, `support_obstructed`, `stepC_conservative`, `admitEvaluator_base_inert`, `replayC_deterministic`, `equivariant_family_invariant`.
- Lesson title: "Putting the viewer on the books: certification as a replayed, panel-relative quotient." The one question: once the panel is part of the state, what does a certificate mean, and what does it still not mean?
- Omit: `replayC_deterministic` (no content); present `equivariant_family_invariant` as a one-line remark if at all.

## 11. Interpretation findings

1. Module header line 6: "'No observer from nowhere', settled for the fixed kernel constitution". Lean: factorization through `supp`, where `World \ supp` is the `notes` field. The theorem shows that the one deliberately inert field is inert along histories; it does not show that no input outside `World` could matter — that is excluded by the type of `step`, not by a theorem, and the header of Represented says so. The paper (§8) adds ABSOLUTE_NO_OUTSIDE_UNFORMULABLE. Classification: INTERPRETATION DEFECT (mild): the word "settled" in the header reads stronger than "the notes field is inert and the panel is now data"; the paper's own ceiling corrects it.
2. `equivariant_family_invariant` docstring: "the ceiling constrains tied menus exactly as it constrains single results". Lean: a two-line consequence of the equivariance hypothesis for arbitrary types. Correct, but the "ceiling" content lives in the hypothesis `hequiv`, which is assumed, not derived, and no kernel construction is shown to satisfy it in this module. Classification: INTERPRETATION DEFECT (mild): a general tautology is presented as a lift of a result; the textbook should state it as a remark.
3. `certNeg_iff_panelEquiv`: the right-hand side carries `panel ≠ []`; the docstring says "(for a non-empty panel)". Faithful.
4. Vacuity: none of the hypotheses are unsatisfiable; `stepC_conservative` and `replayC_deterministic` have definitional/trivial conclusions (noted).
