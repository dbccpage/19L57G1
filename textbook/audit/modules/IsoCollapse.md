# Audit: IsoCollapse

| field | value |
|---|---|
| Path | lean4/Derivation/IsoCollapse.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 0c4b5edca0f0f281 |
| Lines | 177 |
| Imported by root `Derivation.lean` | no (parked: imported by `lean4/ParkedAudit.lean` line 15, listed in `parkedModules`; default target `ParkedAudit`) |
| Imports | Derivation.Minimality |
| Declarations | 3 def (`Iso.symm`, `Iso.imap`, `Iso.cmap`), 8 theorem; namespace `Derivation.Iso` for most |
| Axiom reports in `artifacts/lean_axioms.txt` | 8 lines (ParkedAudit section): propext (`map_eq_self_of_mem`), propext+Quot.sound (the rest). Defs probed: `Iso.symm` propext, Quot.sound; `Iso.imap`, `Iso.cmap` propext |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
IsoCollapse transports observational collapse across the declared isomorphism relation `Iso` of Minimality — the one that mirrors `iso.py` and is stated by membership conditions and range-bounded bijections, not by an action equation. It builds the inverse isomorphism, the image of an instance and of a context under an isomorphism, shows plugging commutes with those images, that well-formed contexts and derivability transport (with range bounds carried at every inversion, since `Iso`'s maps invert only on the admitted ranges), and concludes that two data are collapsed in `r` exactly when their images are collapsed in `s`. Requirements never enter.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Iso.symm h` | 59 | def | the inverse isomorphism (fields swapped; `arity` recomputed) | ADMITTED |
| `Iso.imap h i` | 88 | def | `(h.fmap i.1, i.2.map h.dmap)` | ADMITTED |
| `Iso.cmap h c` | 91 | def | `⟨h.fmap c.form, c.slots.map (Option.map h.dmap)⟩` | ADMITTED |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `map_eq_self_of_mem` | 33 | a list is fixed by a map fixing each member | FROZEN | propext | A |
| `plug_args_lt` | 44 | in a well-formed context, plugging an admitted datum yields admitted arguments | CONDITIONAL: `wfCtx r c`, `d < r.data` | propext, Quot.sound | A |
| `Iso.symm_dmap` | 85 | `h.symm.dmap = h.dinv` (`rfl`) | FROZEN | propext, Quot.sound | A |
| `Iso.plug_cmap` | 95 | `plug (h.cmap c) (h.dmap d) = h.imap (plug c d)` | FROZEN | propext, Quot.sound | A |
| `Iso.wfCtx_cmap` | 107 | `wfCtx r c → wfCtx s (h.cmap c)` | FROZEN | propext, Quot.sound | S |
| `Iso.derivable_imap` | 125 | for `i.1 < r.forms.length` and admitted arguments, `derivable s (h.imap i) ↔ derivable r i` | CONDITIONAL: bounds on `i` | propext, Quot.sound | S |
| `Iso.collapsed_fwd` | 151 | for `d, d' < r.data`, `collapsed s (h.dmap d) (h.dmap d') → collapsed r d d'` | CONDITIONAL: `d, d' < r.data` | propext, Quot.sound | A |
| `Iso.collapsed_transport` | 164 | for `d, d' < r.data`, `collapsed s (h.dmap d) (h.dmap d') ↔ collapsed r d d'` | CONDITIONAL: `d, d' < r.data` | propext, Quot.sound | S |

## 4. External and admitted assumptions
- `Iso` (Minimality): Type-valued, maps total on `Nat` but constrained on `List.range`; `dinv_dmap` etc. hold only on the admitted range, which is why every inversion step carries a bound (docstring says so).
- Library lemmas: `List.mem_map`, `List.map_map`, `List.length_map`, `List.mem_range`, `congrArg`. Core only.
- Universe: none. `Nat → Nat` as data: the `Iso` fields — metatheory.
- Unearned identity / unrestricted universe / unbounded internal function / silent observer / presentation correspondence (the module says plainly the action and `Iso` are distinct and proves from `Iso`'s fields) / cost / admitted-as-forced / finite-as-universal: none found.

## 5. Derived consequences
IsoCanon uses `Iso.symm` (in `iso_of_relabel_eq`), `map_eq_self_of_mem` (in `relabel_iso.insts_bwd`). Paper register R6 (line 787), paper 11 (984), ledger CL-COUNT-INVARIANCE and CL-REGISTER-SCOPE cite `collapsed_transport` as the full two-bijection collapse transport.

## 6. Counterexamples and limitations
No countermodels. Not proved: transport of `separable` across `Iso` (follows from collapse transport only if the pair of images is admitted in `s`, which `dmap_lt` gives — but no theorem states it); transport of transitions or validity across `Iso`; count transport across `Iso`. The direction of `derivable_imap` needs the instance admitted — an instance with out-of-range data is not covered (irrelevant for `plug` of a well-formed context, by `plug_args_lt`).

## 7. Axiom dependencies
All within {propext, Quot.sound}. Defs probed (probe2.lean, exit 0): `Iso.symm` propext, Quot.sound; `Iso.imap`, `Iso.cmap` propext. None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All 8 theorems in the artifact's ParkedAudit section. Paper 11, register R6, ledger cite `collapsed_transport`. Probe: probe2.lean for the three defs.

## 9. Related Python implementations
`code/derivation/iso.py::isomorphic`, `::find_iso`, `::canonical`; `code/derivation/observe.py::collapsed_pairs`; tests `tests/test_iso.py::test_mark_variants_are_isomorphic`, `::test_tokens_are_forgotten`, `::test_canonical_invariant_under_rename`.

## 10. Textbook placement proposal
- Prerequisites: Minimality (`Iso`), Basic (`collapsed`, `wfCtx`, `derivable`), CountTransport (`collapsed_rename` as the one-bijection warm-up).
- Substantive: `Iso.symm`, `Iso.collapsed_transport`. Auxiliary: `imap`, `cmap`, `plug_cmap`, `wfCtx_cmap`, `derivable_imap`, `collapsed_fwd`, `plug_args_lt`, `map_eq_self_of_mem`.
- Lesson title: "Isomorphic regimes collapse the same pairs". Question: if two presentations are the same regime up to relabelling, is "indistinguishable" the same notion in both?
- Omit: nothing; the chain is short.

## 11. Interpretation findings
- Header lines 26–27: "Parked module (not imported by `Derivation.lean`); axioms within `{propext, Quot.sound}`, verified by hand, not by the root gate." At this commit the theorems are in `artifacts/lean_axioms.txt` via `ParkedAudit`. Stale in the safe direction. INTERPRETATION DEFECT (minor, stale provenance note).
- Paper register R6: "full-isomorphism collapse transport: `collapsed_transport`". Lean: across any `Iso r s`, for admitted `d, d'`. Match (admittedness is the only scope, and is natural). none found beyond the provenance note.
- Vacuity: `Iso` is inhabited (`isoRefl`, `isoU1U0`); bounds satisfiable. none found.
- Finitude: none found.
