# Audit: FormRenaming

| field | value |
|---|---|
| Path | lean4/Derivation/FormRenaming.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | f53fbbd356cb970f |
| Lines | 147 |
| Imported by root `Derivation.lean` | no (parked: imported by `lean4/ParkedAudit.lean` line 8 and listed in `parkedModules`; `ParkedAudit` is a default target in `lean4/lakefile.toml`) |
| Imports | Derivation.Basic, Derivation.CountTransport |
| Declarations | 3 def (`permForms`, `mapInstForm`, `renameForms`), 9 theorem (two `@[simp]` instances among them counted by the inventory as "instance 1") |
| Axiom reports in `artifacts/lean_axioms.txt` | 8 lines (ParkedAudit section): none (`mapInstForm_gf`), propext, propext+Quot.sound. Not in artifact: `Regime.ext'` (probed: propext) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
The datum renaming of CountTransport relabels data and leaves form indices alone; a full regime isomorphism also permutes form indices while preserving arities. This module builds the record level of that second half: a permutation of the arity list by an index map, the relabelling of instance and rule form indices, and the two facts that make it a candidate isomorphism component — arity is preserved at the image index, and the action is inverted within the fibre of regimes with the same number of forms. It transports nothing observational; that is FormTransport's job.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `permForms g forms` | 41 | def | `(range forms.length).map (fun j => forms.getD (g j) 0)` — position `j` holds the arity of old position `g j` | ADMITTED |
| `mapInstForm φ i` | 64 | def | `(φ i.1, i.2)` | ADMITTED |
| `renameForms φ g r` | 69 | def | forms permuted by `g`, instance and rule form indices by `φ`, data and reqs untouched | ADMITTED (the form action) |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `permForms_length` | 44 | length preserved | FROZEN | propext, Quot.sound | A |
| `permForms_getD` | 53 | for `j < forms.length`, `(permForms g forms).getD j 0 = forms.getD (g j) 0` | CONDITIONAL: `j < forms.length` (docstring explains why: out of range `g` may map back in) | propext | A |
| `renameForms_data`, `renameForms_reqs` | 75, 78 | data and reqs unchanged (`rfl`) | FROZEN | propext | A |
| `renameForms_forms_length` | 81 | number of forms unchanged | FROZEN | propext, Quot.sound | A |
| `renameForms_arity` | 90 | if `φ i < r.forms.length` and `g (φ i) = i` then the arity at `φ i` after equals the arity at `i` before | CONDITIONAL: bound and local inverse | propext | S |
| `Regime.ext'` | 99 | field-wise extensionality for `Regime` | FROZEN | not in artifact; probed propext | A |
| `mapInstForm_gf` | 106 | `g` inverting `φ` at the form index undoes `mapInstForm` | CONDITIONAL: `g (φ i.1) = i.1` | none | A |
| `renameForms_gf` | 120 | for `σ : DRen r.forms.length`, `renameForms σ.g σ.f (renameForms σ.f σ.g r) = r` | FROZEN (over any `DRen r.forms.length`) | propext, Quot.sound | S |

## 4. External and admitted assumptions
- `DRen m` reused as the bijection type for forms (metatheory: total maps on `Nat`, bounded on `< m`).
- `permForms` reads out of range as `0` via `getD`; the restriction `j < forms.length` is where that convention bites.
- Library lemmas: `List.getD_eq_getElem?_getD`, `List.getElem?_map`, `List.ext_getElem`, `List.map_map`, `List.map_id`, `simp_all` (in `Regime.ext'`). Core only.
- Universe: none. `Nat → Nat` as data: `φ`, `g` — metatheory.
- Unearned identity / unrestricted universe / unbounded internal function / silent observer / presentation correspondence (declared: "mirroring the data-side idioms"; `iso.py`'s `rename` with `phi` is the Python counterpart, not proved) / cost / admitted-as-forced / finite-as-universal: none found.

## 5. Derived consequences
FormTransport (`renameForms_*`, `permForms_getD`, `mapInstForm`, `renameForms_arity` in `wfCtx_renameForms`), IsoCanon (`relabel := renameForms φ.f φ.g (renameRegimeR π.f r)`, `renameForms_arity` in `relabel_iso.arity`). Paper and ledger cite none of these names directly (register R6 note cites FormTransport's and IsoCollapse's results).

## 6. Counterexamples and limitations
No countermodels. Not proved here: any transport of `wf`, contexts, derivability, collapse or transitions (FormTransport does collapse); that the action is an automorphism of unqualified `Regime` (it is a bijection only within a fixed-form-length fibre, as the docstring says).

## 7. Axiom dependencies
All within {propext, Quot.sound}; `Regime.ext'` probed propext. None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). 8 of 9 theorems appear in `artifacts/lean_axioms.txt` under the ParkedAudit section (the ParkedAudit census reports theorems, not defs, so `renameForms` itself has no line). Probe: probe2.lean (exit 0) for `Regime.ext'`. The paper does not cite this module by name.

## 9. Related Python implementations
`code/derivation/iso.py::rename(r, pi, phi)` (the `phi` half), `::serialize`; tests `tests/test_iso.py::test_arity_distinguishes_classes`, `::test_canonical_invariant_under_rename`.

## 10. Textbook placement proposal
- Prerequisites: Basic (`Regime`), CountTransport (`DRen`, datum renaming).
- Substantive: `renameForms`, `renameForms_arity`, `renameForms_gf`. Auxiliary: the projections, `permForms_getD`, `Regime.ext'`, `mapInstForm_gf`.
- Lesson title: "Renaming the judgment forms". Question: what must a relabelling of form indices preserve to be half of an isomorphism?
- Omit: nothing beyond folding the auxiliary lemmas inline.

## 11. Interpretation findings
- Docstring (lines 27–32): "parked module, elaborated by the per-module CI census … but not by the default `lake build` target, and outside the paper's cited axiom inventory. Its axioms are verified here by hand, not preserved by the root axiom gate." At this commit `ParkedAudit` is a second default target (`lakefile.toml`) that imports this module and emits its theorem reports into `artifacts/lean_axioms.txt`, which `ci/check_lean_audit.py` reads. The docstring is stale in the safe direction (it understates the checking). INTERPRETATION DEFECT (minor, stale provenance note; no mathematical overreach).
- Docstring line 16: "`IsoCanon.lean` has since proved the combined action a `Minimality.Iso` (`relabel_iso`)". Checked: `relabel_iso` exists and is a def of type `Iso r (relabel r π φ)` under ordered requirements. Match.
- Vacuity: `renameForms_arity`'s hypotheses are satisfiable by any `DRen r.forms.length` (`renameForms_gf` uses them). none found.
- Finitude: none found.
