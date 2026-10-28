# Audit: Erasure

| field | value |
|---|---|
| Path | lean4/Derivation/Erasure.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | a52cdd98aed2dfaf |
| Lines | 161 |
| Imported by root `Derivation.lean` | yes |
| Imports | Derivation.Basic |
| Declarations | 1 structure (`TRegime`), 1 inductive (`TEvent`), 5 def, 4 theorem |
| Axiom reports in `artifacts/lean_axioms.txt` | 2 lines (`erase_step`, `erase_replay`: propext, Quot.sound); `replayT_cons`, `replayE_cons` not in artifact |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose
Erasure makes the bridge between the two Lean models exact. The Python model keeps presentation tokens and dedups datum admission on token identity; the token-erased `Regime` counts data. The module declares a token-aware state `TRegime` (a list of opaque token numbers in admission order), the token-aware step `stepT` whose `admitDatum` is idempotent on a present token, the erasure map (forget tokens, keep the count), and an event erasure relative to the current token-aware state under which a duplicate admission becomes a bare supply. It proves one-step simulation (`erase_step`) and history-level simulation (`erase_replay`): replaying token-aware and then erasing equals replaying the erased history in the erased model. The paper reads this as: the Lean development is a sound abstraction of the token-aware admission semantics, not a literal mirror.

## 2. Definitions and structures
| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `TRegime` | 20 | structure | `tokens : List Nat`, plus `forms`, `insts`, `rules`, `reqs` as in `Regime` | ADMITTED (the token-aware specification) |
| `TEvent` | 29 | inductive | the six events; `admitDatum` carries its token | ADMITTED |
| `stepT` | 40 | def | token-aware step; re-admitting a present token returns the state unchanged; datum bounds read `tokens.length` | ADMITTED (declared Python dedup semantics) |
| `TRegime.erase` | 62 | def | `⟨tokens.length, forms, insts, rules, reqs⟩` | ADMITTED |
| `eraseEvent` | 68 | def | duplicate `admitDatum tok` ↦ `supply tok`; everything else structural | ADMITTED (state-relative) |
| `replayT` | 107 | def | `foldlM stepT` | ADMITTED |
| `eraseHistory` | 113 | def | erase a history threading the token-aware state; cut after an ill-formed step | ADMITTED (state-relative; the erased history depends on the token-aware run) |

## 3. Theorems and lemmas
| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `erase_step` | 79 | for every `t`, `e`: `(stepT t e).map erase = stepE t.erase (eraseEvent t e)` | FROZEN | propext, Quot.sound | S |
| `replayT_cons` | 121 | `replayT (e :: rest) base = (stepT base e).bind (replayT rest)` | FROZEN | not in artifact | A |
| `replayE_cons` | 127 | same for `replayE`/`stepE` | FROZEN | not in artifact | A |
| `erase_replay` | 138 | for every history `h` and base `t`: `(replayT h base).map erase = replayE (eraseHistory base h) base.erase` | FROZEN | propext, Quot.sound | S |

## 4. External and admitted assumptions
- Structures: `TRegime` with `tokens : List Nat` — tokens are "opaque numbers"; the Python tokens are strings. The ledger's boundary says the two are related "by the declared opaque-token reading", not by proof.
- The simulation is one-directional (token-aware → erased) and the erased history is computed from the token-aware run (`eraseHistory` threads the state). No converse (lifting an arbitrary `Event` history to a token-aware one) is stated.
- Library lemmas: `List.foldlM`, `Option.map`/`bind` simp lemmas, decidable `∈` on `List Nat`.
- Universe parameters: none. `Nat → X` as data: none.
- Unearned identity: token identity is by `Nat` equality — a declared, not derived, identity of presentations (the paper calls it presentation identity). Unrestricted universe / unbounded internal function / silent observer / cost / admitted-as-forced / finite-as-universal: none found. Unspecified correspondence between presentations: the Python-string/Lean-`Nat` token correspondence is declared, not proved (ledger says so).

## 5. Derived consequences
`TRegime`, `stepT`, `replayT` are reused by Bridge.lean (`AtMostTok`, `stepT_preserves_atMostTok`). `erase_step`/`erase_replay` are cited by paper 2 (line 109) and ledger CL-TOKEN-ERASURE (with Ext as the second component); no other Lean module uses them.

## 6. Counterexamples and limitations
No countermodels. Not proved: anything about the Python source (connection is by executable tests, stated); that every erased history arises from some token-aware history; preservation of `wf` across `stepT` (Bridge proves a token bound only). The simulation says nothing about contexts or collapse directly; those are transported by Ext under membership-equality, which is why the paper insists the bridge is "two theorems, never duplicate idempotence alone".

## 7. Axiom dependencies
`erase_step`, `erase_replay`: propext, Quot.sound. The two `_cons` lemmas are not in the artifact (not probed; `simp`-based, so at most propext, Quot.sound). None exceed.

## 8. Verification status
Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). Both main theorems in the artifact (root lines 108–109). Paper 2 and ledger CL-TOKEN-ERASURE cite them. No extra probe.

## 9. Related Python implementations
`code/derivation/model.py::step` (`AdmitDatum` dedup on token identity; `Regime.data` is a tuple of tokens, `n_data`), `replay`, `certify`. Tests: `tests/test_model.py::test_admit_datum_dedups_on_presentation_identity`, `tests/test_export_and_run.py` (replay/certify).

## 10. Textbook placement proposal
- Prerequisites: Basic (`stepE`, `replayE`), Inertia (`supply_no_op`).
- Substantive: `TRegime`/`stepT`, `eraseEvent`, `erase_step`, `erase_replay`. Auxiliary: `replayT_cons`, `replayE_cons`, `eraseHistory` (explain in a sentence).
- Lesson title: "Why counting data loses nothing". Question: if two presentations with the same token are admitted twice, why does the counted model still replay the same regime?
- Omit: the two `_cons` lemmas.

## 11. Interpretation findings
- Paper 2 (line 110–113): "replaying a token-aware history … then erasing tokens equals replaying the erased history in the token-erased model". Exact. The paper also says the Lean is "a sound abstraction" — the theorem proves simulation in the direction token-aware → erased with a run-dependent erased history; "sound abstraction" is the right word for that direction. None found.
- Ledger CL-TOKEN-ERASURE class "theorem" with the Python endpoint connected "by the executable checks …, not by any proof over the Python source (endpoints stated 2026-09-08)". Consistent with the Lean.
- Finitude: `tokens : List Nat` are metatheoretic labels; no prose reads an infinity of tokens into the system. None found.
- Vacuity: none (both theorems are unconditional equalities over all inputs).
