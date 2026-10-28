# Audit: IsoCanon

| field | value |
|---|---|
| Path | lean4/Derivation/IsoCanon.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | b1c85ba330b70ade |
| Lines | 232 |
| Imported by root `Derivation.lean` | no (parked: imported by `lean4/ParkedAudit.lean` line 13, listed in `parkedModules`; default target `ParkedAudit`) |
| Imports | Derivation.IsoCollapse, Derivation.TransitionTransport, Derivation.FormRenaming |
| Declarations | 4 def (`Iso.trans`, `relabel`, `relabel_iso`, `iso_of_relabel_eq` — the last two Type-valued `Iso` constructions), 10 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 10 lines (ParkedAudit section), all propext. The inventory's extra match `QuotientRetention.RelationRefinement.trans` is a name collision with another module's `trans`, not this file. Defs probed: `Iso.trans`, `relabel_iso`, `iso_of_relabel_eq` propext, Quot.sound; `relabel` propext |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
`iso.py` decides isomorphism by a canonical key: the minimum over colour-class-preserving bijection pairs of a serialisation of the relabelled regime. IsoCanon proves the action half of that machinery: relabelling a regime by a datum bijection and a form bijection yields a regime isomorphic to it in the sense of the declared `Iso`, with the pair as witnessing maps (`relabel_iso`). It makes `Iso` transitive (`Iso.trans`; with `Iso.symm` and the conditional `isoRefl`, an equivalence on regimes with ordered requirements) and derives the soundness kernel: two regimes whose relabellings coincide as regimes are isomorphic. The header scopes precisely what is not here — the list-reorder step from equal sorted serialisations to equal regimes (IsoBridge takes the membership step), and the converse "isomorphic ⇒ equal key", which needs a normalisation hypothesis because `Iso` identifies `[p]` with `[p, p]`.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `Iso.trans h k` | 90 | def | composite isomorphism (unconditional) | ADMITTED (construction) |
| `relabel r π φ` | 136 | def | `renameForms φ.f φ.g (renameRegimeR π.f r)` for `π : DRen r.data`, `φ : DRen r.forms.length` | ADMITTED (the combined action `serialize` reads off) |
| `relabel_iso r π φ hord` | 158 | def (Type) | `Iso r (relabel r π φ)` given `∀ q ∈ r.reqs, q.1 ≤ q.2` | ADMITTED (construction; the mathematical content is in its fields) |
| `iso_of_relabel_eq … hr hs heq` | 225 | def (Type) | `Iso r s` from `relabel r πr φr = relabel s πs φs` with both requirement lists ordered | ADMITTED (construction) |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `sortPair_eq_minmax` | 53 | `sortPair (x,y) = (min x y, max x y)` | FROZEN | propext | A |
| `sortPair_comm` | 60 | symmetric | FROZEN | propext | A |
| `mapReq_eq_sortPair` | 65 | `mapReq f q = sortPair (f q.1, f q.2)` — bridge between the transition action and `Iso`'s requirement fields | FROZEN | propext | S |
| `sortPair_map_sortPair` | 70 | sorting before mapping does not change the sorted image | FROZEN | propext | A |
| `sortPair_of_le` | 77 | an ordered pair is fixed by `sortPair` | CONDITIONAL: `x ≤ y` | propext | A |
| `relabel_data`, `_forms`, `_insts`, `_rules`, `_reqs` | 139–152 | projections of `relabel` (`rfl`) | FROZEN | propext | A |

The two `Iso`-valued constructions are definitions, so they do not appear in the theorem table; their status: `relabel_iso` — CONDITIONAL: `∀ q ∈ r.reqs, q.1 ≤ q.2` (needed only for `reqs_bwd`), otherwise unconditional in the bijection bounds; `iso_of_relabel_eq` — CONDITIONAL: both orderings and `heq`.

## 4. External and admitted assumptions
- `Iso` (Minimality), `DRen`, `renameRegimeR`/`mapReq` (TransitionTransport), `renameForms`/`permForms` (FormRenaming), `Iso.symm`, `map_eq_self_of_mem` (IsoCollapse).
- The correspondence "`serialize(r, π, φ)` reads off the combined action … then sorts" is a declared reading of `iso.py`; not proved (cannot be, in Lean).
- Ordered requirement pairs (as `Regime.wf` gives) on `relabel_iso`, `iso_of_relabel_eq` and on `isoRefl` — the header notes a regime with an unordered requirement pair is not `Iso` to itself.
- Library lemmas: `Nat.min/max_*`, `List.mem_map`, `List.map_map`, `simpa`. Core only.
- Universe: none. `Nat → Nat` as data: bijection fields — metatheory.
- Unearned identity: none found (the header refuses the converse without a normalisation hypothesis). Unrestricted universe: none. Unbounded internal function: none. Silent observer: none. Presentation correspondence: the Lean `relabel` vs Python `serialize` is declared, with the sort step named as the unproved remainder. Cost: none. Admitted-as-forced: none. Finite-as-universal: the header says the agreement of the two key computations is "finite test evidence, not a proved general agreement". none found.

## 5. Derived consequences
IsoBridge imports this module (uses `sortPair_of_le`). Paper 11 (line 985: "the partial canonical-key bridges of `IsoCanon.lean` and `IsoBridge.lean`") and ledger CL-ISO-SOUND's scope rest on `relabel_iso` / `iso_of_relabel_eq`. FormRenaming's header cites `relabel_iso`.

## 6. Counterexamples and limitations
No countermodels. Not proved: equal canonical key ⇒ `Iso` in full (the sort/list-reorder step, partially closed by IsoBridge's `of_components`, with the sorted-list-equality-to-membership lemma still absent); isomorphic ⇒ equal key (needs normalisation; `[p]` vs `[p,p]`); that `canonical` and `canonical_bruteforce` agree in general (finite tests); anything about the permutation budget.

## 7. Axiom dependencies
All 10 theorems propext. Defs probed (probe2.lean, exit 0): `Iso.trans`, `relabel_iso`, `iso_of_relabel_eq` propext, Quot.sound; `relabel` propext. None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). The 10 theorems are in the artifact's ParkedAudit section; the three `Iso`-valued defs are not (the census reports theorems only) and were probed. Paper 11 cites the module by name.

## 9. Related Python implementations
`code/derivation/iso.py::serialize` (L123), `::canonical` (L162), `::canonical_bruteforce` (L198), `::isomorphic` (L215), `::rename` (L219), `::find_iso` (L174); tests `tests/test_iso.py::test_agreement_with_bruteforce_on_pairs`, `::test_rule_sets_participate_in_canonical`, `::test_perm_budget_error`, `::test_canonical_invariant_under_rename`.

## 10. Textbook placement proposal
- Prerequisites: Minimality (`Iso`, `sortPair`), TransitionTransport (`renameRegimeR`), FormRenaming, IsoCollapse (`Iso.symm`).
- Substantive: `relabel`, `relabel_iso`, `Iso.trans`, `iso_of_relabel_eq`, `mapReq_eq_sortPair`, and the stated gaps. Auxiliary: the `sortPair_*` and `relabel_*` lemmas.
- Lesson title: "Why deduplicating by canonical key is safe — and what is still unproved". Question: if two regimes serialise to the same key, are they isomorphic, and which step of that argument lives in Lean?
- Omit: the projection lemmas.

## 11. Interpretation findings
- Header lines 45–46: "Parked module (not imported by `Derivation.lean`); axioms within `{propext, Quot.sound}`, verified by hand, not by the root gate." The theorems are reported via `ParkedAudit` at this commit; the three `Iso`-valued defs are indeed outside any gate (census reports theorems only) and were checked by hand here. INTERPRETATION DEFECT (minor, stale for the theorems; accurate for the defs).
- Paper 11: "the partial canonical-key bridges of `IsoCanon.lean` and `IsoBridge.lean`" — "partial" matches the header's own scoping. none found.
- Ledger CL-ISO-SOUND (not re-read in full here; its Python side is the claim) — the Lean kernel here does not discharge it and does not claim to. Not checked further.
- Vacuity: `relabel_iso` with identity bijections and ordered requirements is `isoRefl`-like; `iso_of_relabel_eq` satisfiable with `r = s`. none found.
- Finitude: none found.
