# Audit: PrimitiveContact

| field | value |
|---|---|
| Path | lean4/Derivation/PrimitiveContact.lean |
| Commit | 33100245bb687b8242262279758bcc101ff2b5af |
| Content hash (sha256, first 16 hex) | 448bd29d6e5db6b3 |
| Lines | 142 |
| Imported by root `Derivation.lean` | yes (line 31) |
| Imports | `Derivation.PrimitiveCore`, `Derivation.PrimitiveCats`, `Derivation.ContactBridge` (through which `DiffInterface` is reached) |
| Declarations | 6 defs (`contactStatus`, `NativeKernel`, `nativeKernelWitness`, `contactStatusHistory`, `contactStatusCurrent`, `contactVerdictPrimary`), 3 theorems. The inventory lists a fourth theorem name `corpus`; it does not exist — the inventory's regex matched the docstring phrase "theorem corpus of `ObsDescent`, …" at line 110. |
| Axiom reports in `artifacts/lean_axioms.txt` | 3 lines: `native_kernel_initial` (Quot.sound), `contact_status_count` (none), `native_interface_not_representable` (none) |
| Forbidden tokens (sorry/admit/axiom) | none found |

## 1. Mathematical purpose

A record-and-interface module for the contact-and-passage run (stages III–V). It fixes the interface a future or arriving development meets: the native kernel is the class of settings carrying a pointed witnessed irreflexive relation (`PrimitiveCore.A`), inhabited by the oriented two-element realization; the status the kernel brings is re-exported under contact-facing names — initiality of the two-element carrier in the pointed witnessed category (`PrimitiveCats.d2_initial`) and the signature-level refutation that no difference observer's apartness (the complement of its zero relation, hence symmetric) can equal the oriented witness `D2` (`ContactBridge.d2_not_obs_complement`). It also carries the protocol's status constants: the sealed pre-contact terminal `CONTACT_INPUT_ABSENT` (preserved, superseded), the current status `CONTACT_PROCESSED_LEAN_ONLY`, the primary verdict `CONTACT_INCOMPARABLE_WITH_COUNTERMODELS`, and a two-entry history whose length is checked by `rfl`. The collision's mathematics lives in `ObsDescent`, `ContactBridge`, `ContactKernel` (other batches).

## 2. Definitions and structures

| name | line | kind | what it is | mark |
|---|---|---|---|---|
| `contactStatus` | 80 | def | `"CONTACT_INPUT_ABSENT"` — the superseded pre-contact terminal, kept unchanged | ADMITTED (declared policy; historical) |
| `NativeKernel` | 84 | def (`Type 1`) | `{ S : PrimitiveCore.Setting // PrimitiveCore.A S }` — settings with `S.r S.a S.b ∧ Irrefl S.r` | ADMITTED (the declared interface) |
| `nativeKernelWitness` | 89 | def | the setting `⟨Bool, D2, false, true, empty ret/prot/Ops⟩` with `D2_witness`, `D2_irrefl` | ADMITTED (inhabitant) |
| `contactStatusHistory` | 116 | def | the two-string list of terminals | ADMITTED (DECLARED_POLICY) |
| `contactStatusCurrent` | 122 | def | `"CONTACT_PROCESSED_LEAN_ONLY"` | ADMITTED (DECLARED_POLICY; must match the Python constant) |
| `contactVerdictPrimary` | 126 | def | `"CONTACT_INCOMPARABLE_WITH_COUNTERMODELS"` | ADMITTED (DECLARED_POLICY) |

## 3. Theorems and lemmas

| name | line | informal statement | mark | axioms | S/A |
|---|---|---|---|---|---|
| `native_kernel_initial` | 99 | `PrimitiveCats.Initial PrimitiveCats.d2Obj` (`:= PrimitiveCats.d2_initial`, a re-export) | FROZEN (proved in `PrimitiveCats`; not re-audited here) | Quot.sound | S (as interface) |
| `contact_status_count` | 131 | `contactStatusHistory.length = 2` (`rfl`) | VERIFIED_FINITE (of a declared datum) | none | A |
| `native_interface_not_representable` | 137 | `¬ ∃ (R : Type) (O : DiffObs Bool R), ∀ x y, obsApart O x y ↔ D2 x y` (`:= ContactBridge.d2_not_obs_complement`, a re-export) | REFUTED (proved in `ContactBridge`; not re-audited here) | none | S (as interface) |

## 4. External and admitted assumptions

- Both substantive theorems are aliases; their hypotheses and proofs belong to `PrimitiveCats` and `ContactBridge` (batches D/other). Here: `obsApart O x y := ¬ ZeroRel O x y` (`ContactBridge.lean` line 116), so the refuted statement asks a symmetric relation to coincide with the asymmetric `D2` — the refutation is at signature level, as the docstring says.
- `NativeKernel : Type 1` because `Setting` carries a `Type`; a universe parameter, metatheory.
- The status strings are declared data; `contact_status_count` checks a count, not a meaning. The docstring on `contactStatus` warns that a consumer reading it alone gets the superseded value.
- Unearned identity: none. Unrestricted external universe: `Type 1` only as the kernel's universe. Unbounded function: none. Silently assumed observer: none. Unspecified correspondence between presentations: the "same status in Python" is a declared requirement (`contactStatusCurrent` "must equal the Python generator's status constant"), checked by `tests/test_primitive_contact.py::test_contact_processed_state` (status string) — the Lean constant and the Python constant are compared by text in the receipt, not by a Lean theorem. Cost function: none. Admitted condition later described as forced: none found. Finite computation presented as universal: none.

## 5. Derived consequences

`ContactKernel.lean` references `PrimitiveContact.` (presumably `NativeKernel` via `ContactKernel.toNativeKernel`, per the header; not read). Ledger: `CL-PD2-CONTACT` (`native_kernel_initial`; the sealed pre-contact entry), `CL-PD2-CONTACT-VERDICT` (`contactStatusHistory`, `contact_status_count`, `native_interface_not_representable`), `CL-PD2-CONTACT-COUNTERMODELS` (`native_interface_not_representable`). Python: `code/run_primitive_contact.py` (`STATUS_*`, `VERDICT_PRIMARY`, `contact_report`, the enumerations `enum_bool_observers`, `enum_settings_kernels`, …), `code/run_primitive_receipt.py`; artifact `artifacts/primitive_contact.json`.

## 6. Counterexamples and limitations

`native_interface_not_representable` is the one countermodel (any `DiffObs` on `Bool`: its apartness is symmetric, `D2` is not). The module proves nothing new; it names. The "three terminals" of the verdict (`CL-PD2-CONTACT-VERDICT`) are declared on the strength of evidence bundles in other modules; this module checks only that the history has two entries.

## 7. Axiom dependencies

All three within `{propext, Quot.sound}` (`native_kernel_initial`: `Quot.sound`, inherited from `d2_initial`). None exceed: none.

## 8. Verification status

Built in this session: yes (lake build of the whole library succeeded on 2026-10-28, exit 0, Lean 4.33.0). All three theorems in the artifact; cited by the three `CL-PD2-CONTACT*` entries. No probe run.

## 9. Related Python implementations

`code/run_primitive_contact.py` (status/verdict constants mirroring the Lean strings; `contact_report`; observer and kernel enumerations), `code/run_primitive_receipt.py`; tests `tests/test_primitive_contact.py` (`test_contact_processed_state`, `test_verdict_block`), `tests/test_primitive_receipt.py`.

## 10. Textbook placement proposal

- Prerequisites: PrimitiveCore (`Setting`, candidate `A`), PrimitiveCats (`d2_initial`), DiffInterface (`DiffObs`, `ZeroRel`), ContactBridge (`obsApart`).
- Substantive: the interface definition `NativeKernel` with its witness, and the two re-exported facts as the "what the native side brings to a collision" summary. Auxiliary: the status strings and `contact_status_count`.
- Lesson title: "The fixed interface a collision meets." Question answered: what, exactly, is on the table when an outside development arrives — a pointed witnessed irreflexive relation, initial in its category, and not representable as any observer's apartness.
- Recommend omitting: `contactStatus`, `contactStatusHistory`, `contactStatusCurrent`, `contactVerdictPrimary`, `contact_status_count` (protocol bookkeeping, not mathematics; mention in a provenance footnote).

## 11. Interpretation findings

1. `native_kernel_initial` — docstring: "the strongest universal status the native side brings to any future collision (proved, not postured)". The theorem is `PrimitiveCats.d2_initial` renamed; "universal" is used with its proof reference, within the pointed witnessed category. The word "strongest" is not a theorem. Not a defect; a scope note (the category and its morphisms are PrimitiveCats' declarations).
2. Inventory artefact: the inventory's theorem list for this module includes `corpus`, which is a docstring word, not a declaration. Not a Lean finding; a note for whoever consumes `inventory.json`.
3. Vacuity: `contact_status_count` is `rfl` on a declared list — content-free as mathematics, meaningful only as a cross-check against the Python mirror. Acknowledged by its own `FINITE_COMPUTATION` label. None found otherwise.
