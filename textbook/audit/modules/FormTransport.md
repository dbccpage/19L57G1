# Audit: FormTransport

| field | value |
|---|---|
| Path | lean4/Derivation/FormTransport.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 9085b267f98ed5d5 |
| Lines | 196 |
| Imported by root `Derivation.lean` | no (parked: imported by `lean4/ParkedAudit.lean` line 9, listed in `parkedModules`; default target `ParkedAudit`) |
| Imports | Derivation.FormRenaming |
| Declarations | 1 def (`mapCtxForm`), 11 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 11 lines (ParkedAudit section): none (`plug_mapCtxForm`), propext, propext+Quot.sound |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
FormTransport supplies the half of observational transport that CountTransport left out: observational collapse is invariant under a form renaming, because a context's slots name data, not forms, so only the form index of a context moves and the arity lookup survives by `permForms_getD`. It then composes the datum action and the form action into a combined transport of collapse, with the datum pair carried by the datum map alone. Its header is explicit that this is a transport under an explicit ACTION (an equality of renamed regimes), not across the membership-stated isomorphism `Iso` — that connection is proved in IsoCollapse and IsoCanon — and that the transition relation is NOT yet transported under the form action.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `mapCtxForm φ c` | 76 | def | `⟨φ c.form, c.slots⟩` | ADMITTED |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `renameForms_forms`, `renameForms_insts`, `renameForms_rules` | 62–68 | projections of `renameForms` (`rfl`) | FROZEN | propext | A |
| `plug_mapCtxForm` | 80 | `plug (mapCtxForm φ c) d = mapInstForm φ (plug c d)` (`rfl`) | FROZEN | none | A |
| `mapCtxForm_f_g` | 84 | `mapCtxForm σ.f (mapCtxForm σ.g c) = c` | FROZEN | propext | A |
| `mapInstForm_inj` | 91 | injective `φ` gives injective `mapInstForm φ` | CONDITIONAL: `φ` injective | propext | A |
| `derivable_renameForms` | 102 | for injective `φ`, `derivable (renameForms φ g r) (mapInstForm φ i) ↔ derivable r i` | CONDITIONAL: `φ` injective | propext, Quot.sound | S |
| `wfCtx_renameForms` | 118 | for `σ : DRen r.forms.length`, `wfCtx (renameForms σ.f σ.g r) (mapCtxForm σ.f c) ↔ wfCtx r c` | FROZEN (over any such `σ`) | propext, Quot.sound | S |
| `collapsed_renameForms` | 137 | `collapsed (renameForms σ.f σ.g r) d d' ↔ collapsed r d d'` | FROZEN (over any `σ : DRen r.forms.length`) | propext, Quot.sound | S |
| `collapsed_congr` | 165 | regimes agreeing on data, forms, insts, rules collapse the same pairs | FROZEN | propext | A |
| `collapsed_renameDataForm` | 189 | for `σ : DRen n`, `r.data = n`, `τ : DRen r.forms.length`: `collapsed (renameForms τ.f τ.g (renameRegime σ.f r)) (σ.f d) (σ.f d') ↔ collapsed r d d'` | CONDITIONAL: `r.data = n` | propext, Quot.sound | S |

## 4. External and admitted assumptions
- `DRen` for both bijections; `renameRegime` (CountTransport) for the datum half, which leaves `reqs` alone.
- The header's two scope claims — `Iso` does not imply the action (duplicate instances), and the action is not an `Iso` witnessed by its own maps (`reqs` untouched) — are stated as prose; the second has a concrete example in the docstring, neither is a Lean theorem here.
- Library lemmas: `List.mem_map`, `List.length_map`, `simp only [wfCtx, …]`. Core only.
- Universe: none. `Nat → Nat` as data: `φ`, `g`, `σ.f` — metatheory.
- Unearned identity / unrestricted universe / unbounded internal function / silent observer / presentation correspondence (header says the action "is **not** the canonical regime isomorphism") / cost / admitted-as-forced / finite-as-universal: none found.

## 5. Derived consequences
No Lean module uses these theorems (IsoCanon imports FormRenaming, not FormTransport; grep confirms). Paper register R6 note (line 764), paper 11 (line 985), ledger CL-COUNT-INVARIANCE Lean bullet and CL-REGISTER-SCOPE cite `collapsed_renameForms`, `collapsed_renameDataForm` as the form-action components of collapse transport.

## 6. Counterexamples and limitations
No countermodels. Not proved: `separable`, `respond`, `validResponse`, `TransStep` under the form or combined action (header says so and explains why it does not compose with `transStep_rename_fwd`: that uses `renameRegimeR`); any statement about `Iso`.

## 7. Axiom dependencies
All within {propext, Quot.sound}; `plug_mapCtxForm` none. None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 11 theorems in the artifact's ParkedAudit section. Paper 11/12 and ledger cite `collapsed_renameForms`, `collapsed_renameDataForm`. No extra probe.

## 9. Related Python implementations
`code/derivation/iso.py::rename` (both halves), `::canonical`; `code/derivation/observe.py::collapsed_pairs`; tests `tests/test_iso.py::test_canonical_invariant_under_rename`, `tests/test_engine.py::test_closure_policy_is_token_blind`.

## 10. Textbook placement proposal
- Prerequisites: CountTransport (`collapsed_rename`), FormRenaming.
- Substantive: `collapsed_renameForms`, `collapsed_renameDataForm`, and the scope note distinguishing action from `Iso`. Auxiliary: the rest.
- Lesson title: "Collapse does not see the labels of forms either". Question: why does a form permutation change no collapsed pair, and why is that still not "isomorphism invariance"?
- Omit: the three `rfl` projections.

## 11. Interpretation findings
- Header lines 54–56: "Parked module (not imported by `Derivation.lean`); its axioms are within `{propext, Quot.sound}`, verified by hand, not by the root axiom gate." At this commit its theorems are reported through `ParkedAudit` into `artifacts/lean_axioms.txt`, which the audit script reads. Stale in the safe direction. INTERPRETATION DEFECT (minor, stale provenance note).
- Paper register R6 ("full-isomorphism collapse transport: `collapsed_transport`, `collapsed_renameDataForm`"). `collapsed_renameDataForm` is transport under the combined ACTION, not under `Iso`; `collapsed_transport` (IsoCollapse) is the one across `Iso`. The row's phrase "full-isomorphism" groups both; the paper 11 sentence says "two-bijection collapse transport", which fits the action. INTERPRETATION DEFECT (minor: the register headline folds an action theorem under "full-isomorphism"; no mathematical gap since IsoCollapse covers `Iso`).
- Vacuity: none found (hypotheses satisfiable by identity `DRen`s).
- Finitude: none found.
