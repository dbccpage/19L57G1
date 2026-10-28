# Audit: Ext

| field | value |
|---|---|
| Path | lean4/Derivation/Ext.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 6c597b6410a07ec1 |
| Lines | 179 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Basic |
| Declarations | 3 def (`SetEq`, `RegimeExt`, `OptExt`), 12 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 7 lines (`derivable_ext`: none; `wfCtx_ext`, `collapsed_ext`, `separable_ext`, `applyItem_ext`, `applyDelta_ext`, `validResponse_ext`: propext). The five `SetEq.*`/`RegimeExt.*` helpers are not in the artifact |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Ext is the second half of the Python-to-Lean bridge. Python's admitted instance, rule and requirement collections are sets; the Lean model uses deduplicated lists. The module declares membership-extensional equality of lists (`SetEq`) and of regimes (`RegimeExt`: equal data count, equal form table, membership-equal instances, rules, requirements) and proves that every observable of the development transports along it: derivability, context well-formedness, collapse, separability, item and delta application (up to `OptExt`), and response validity. So two list representations of the same admitted sets agree on every claim stated in terms of these observables, and no such claim depends on list order or representation.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `SetEq` | 21 | def | `∀ x, x ∈ l1 ↔ x ∈ l2` | ADMITTED |
| `RegimeExt` | 37 | def | `data` equal, `forms` equal as lists, `insts`/`rules`/`reqs` `SetEq` | ADMITTED (the declared bridge relation) |
| `OptExt` | 86 | def | `RegimeExt` on `some/some`, true on `none/none`, false otherwise | ADMITTED |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `SetEq.rfl'` | 23 | `SetEq l l` | FROZEN | not in artifact | A |
| `SetEq.symm'` | 26 | `SetEq` is symmetric | FROZEN | not in artifact | A |
| `SetEq.insertNew'` | 29 | `SetEq l1 l2 → SetEq (insertNew l1 a) (insertNew l2 a)` | FROZEN | not in artifact | A |
| `RegimeExt.refl'` | 41 | reflexive | FROZEN | not in artifact | A |
| `RegimeExt.symm'` | 44 | symmetric | FROZEN | not in artifact | A |
| `derivable_ext` | 50 | `RegimeExt r s → (derivable r i ↔ derivable s i)` | FROZEN | none | S |
| `wfCtx_ext` | 56 | `RegimeExt r s → (wfCtx r c ↔ wfCtx s c)` | FROZEN | propext | S |
| `collapsed_ext` | 62 | `RegimeExt r s → (collapsed r d d' ↔ collapsed s d d')` | FROZEN | propext | S |
| `separable_ext` | 74 | same for `separable` | FROZEN | propext | S |
| `applyItem_ext` | 92 | `RegimeExt r s → OptExt (applyItem r it) (applyItem s it)` | FROZEN | propext | S |
| `applyDelta_ext` | 129 | same for `applyDelta` over any delta | FROZEN | propext | S |
| `validResponse_ext` | 152 | `RegimeExt r s → (validResponse r i j δ ↔ validResponse s i j δ)` | FROZEN | propext | S |

(`RegimeExt` is the relation the statements are about, not an extra condition restricting a wider claim, so these are marked FROZEN rather than CONDITIONAL.)

## 4. External and admitted assumptions
- `RegimeExt` is declared. It is shown reflexive and symmetric; transitivity is not stated (not needed by any proof).
- `forms` must be equal as lists, not as sets — correct, since arity is read by position.
- Library lemmas: `or_congr`, `List.foldlM` unfolding; `mem_insertNew` from Basic. Core only.
- Universe parameters: `SetEq` lemmas polymorphic in `α : Type`.
- `Nat → X` as data: none. Unearned identity / unrestricted universe / unbounded internal function / silent observer / presentation correspondence / cost / admitted-as-forced / finite-as-universal: none found.

## 5. Derived consequences
No other Lean module uses these theorems (grep). They are cited by paper 2 (line 114–124) and ledger CL-TOKEN-ERASURE as component (ii) of the bridge.

## 6. Counterexamples and limitations
No countermodels. Not proved, and the paper/ledger say so since 2026-08-18: that every exported claim factors through the listed observables; claims stated at representation level (concrete replay equalities such as `historyL_replays`) are covered only up to `RegimeExt`. Also not proved: `RegimeExt` transitivity; extensionality of `stepE`/`replayE` (only `applyItem`/`applyDelta` are covered; `stepE`'s `impose` clause has no `applyItem` counterpart).

## 7. Axiom dependencies
`derivable_ext` axiom-free; the other six propext. Helpers not in artifact (not probed; trivial). None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Seven theorems in the artifact (root lines 112–118). Paper 2 and ledger CL-TOKEN-ERASURE cite them. No extra probe.

## 9. Related Python implementations
`code/derivation/model.py` (`insts`, `rules`, `reqs` as `frozenset`; `EMPTY`). Tests: `tests/test_model.py` (set semantics), `tests/test_observe.py`.

## 10. Textbook placement proposal
- Prerequisites: Basic; Erasure (the other half of the bridge).
- Substantive: `RegimeExt`, `collapsed_ext`, `validResponse_ext` (state the family once). Auxiliary: everything else.
- Lesson title: "Lists that mean sets". Question: can the order in which instances were admitted ever change what a regime can separate?
- Omit: `SetEq.*`, `RegimeExt.refl'/symm'`, `applyItem_ext` (fold into one sentence).

## 11. Interpretation findings
- Paper 2: "no claim **stated in terms of them** depends on list order or representation … That every exported claim factors through these observables is not proved and is not asserted". Exact match to the Lean. none found.
- Ledger CL-TOKEN-ERASURE: "the extensionality family reports per-theorem in `artifacts/lean_axioms.txt`" — true (one is axiom-free, six propext).
- Vacuity: `RegimeExt` is satisfiable (reflexive); conclusions are iffs over genuinely different lists. None found.
- Finitude: none found.
