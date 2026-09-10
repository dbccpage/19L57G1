# Research Estate Honesty Audit Report

**Date:** 2026-09-10  
**Auditor:** Sub-team Alpha (Worker M1)  
**Target:** Target 10 (Estate Honesty Pass)  
**AuthorityEffect:** None.  

*Scope Note:* This audit covers the 48 research trees present at the time of analysis. Trees added by this PR (cost_cohomology, estate_honesty, multi_depth, multi_magnitude, reading_f_iso, redheffer, self_interpreter) are not included in the census count.
## 1. Executive Summary & Epistemic Boundaries

This audit reconciles the estate-wide governance, Gate 11 CI integration, test count drift,
axiom dependencies, and verification boundaries across all 48 research trees in `research/`.

- **Total Research Trees Audited:** 48
- **Trees Integrated in Gate 11 CI:** 13 (workflow enumerated)
- **Trees Retained as Local Receipts Only:** 35
- **Trees with Lean Axiom Verification in CI:** 2 (`second_nofirst`, `typed_translation`)
- **Trees with Local Manual Lean Receipts:** 28 (`verify_lean.py` exists, local operator attestation)
- **Trees with Zero Lean Formalization:** 17 (pure Python / analytical)
- **Root Test Suite Count Drift:** 481 in `README.md` vs. **523** collected by pytest (+42 tests)
- **Kernel Axiom Report Drift:** 1,314 in `verification_20260817.md` vs. **1530** in `artifacts/lean_axioms.txt` (+216 reports across 75 modules)
- **Kernel Axiom Integrity:** 1530 / 1530 reports strictly within `{propext, Quot.sound}` (0 disallowed axioms)

---

## 2. Gate 11 CI Integration vs. Local Receipts Census

In `.github/workflows/verify.yml`, Gate 11 evaluates research trees under the written contract.
As recorded in `research/README.md`, hosted CI is permanently disabled; 'workflow' denotes the
written gate specification executed locally.

| Tree Name | Status in research/README.md | Gate 11 in verify.yml | Lean Axioms in CI | Test Harness | Category |
|---|---|---|---|---|---|
| `admission_sign_shadow` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `admit_leftover` | local receipt only | NO (local only) | None | `test_*.py` | `LOCAL_RECEIPT_PYTHON` |
| `balance_carrier` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `blind_restart` | workflow (gate 11) | YES (Gate 11) | None | `test_*.py` | `GATE11_PYTHON_CI` |
| `boundary_seed` | workflow (gate 11) | YES (Gate 11) | Manual (`verify_lean.py`) | `tests/` | `GATE11_PYTHON_CI` |
| `closed_family` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `coherent_process_limits` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `tests/` | `LOCAL_RECEIPT_LEAN` |
| `convention_price` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `described_replay` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `dynamics_step` | local receipt only | NO (local only) | None | `test_*.py` | `LOCAL_RECEIPT_PYTHON` |
| `endogenous_demand` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `tests/` | `LOCAL_RECEIPT_LEAN` |
| `exchange_coefficients` | local receipt only | NO (local only) | None | `test_*.py` | `LOCAL_RECEIPT_PYTHON` |
| `family_embedding` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `fresh_characters` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `g1_local_class` | local receipt only | NO (local only) | None | `none` | `LOCAL_RECEIPT_SPEC` |
| `genesis_continuation` | local receipt only | NO (local only) | None | `none` | `LOCAL_RECEIPT_SPEC` |
| `grammar_fit` | local receipt only | NO (local only) | None | `test_*.py` | `LOCAL_RECEIPT_PYTHON` |
| `identification_dual` | local receipt only | NO (local only) | None | `test_*.py` | `LOCAL_RECEIPT_PYTHON` |
| `ignition` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `tests/` | `LOCAL_RECEIPT_LEAN` |
| `iso_sound` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `tests/ and test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `limit_and_observer` | workflow (gate 11) | YES (Gate 11) | Manual (`verify_lean.py`) | `tests/` | `GATE11_PYTHON_CI` |
| `local_reuse` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `tests/` | `LOCAL_RECEIPT_LEAN` |
| `magnification` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `tests/` | `LOCAL_RECEIPT_LEAN` |
| `natural_sections` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `observer_visibility` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `partial_decide` | workflow (gate 11) | YES (Gate 11) | None | `test_*.py` | `GATE11_PYTHON_CI` |
| `path_dependent_cost` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `portable_interface` | workflow (gate 11) | YES (Gate 11) | None | `test_*.py` | `GATE11_PYTHON_CI` |
| `priced_admissions` | local receipt only | NO (local only) | None | `test_*.py` | `LOCAL_RECEIPT_PYTHON` |
| `primitive_difference_tower` | workflow (gate 11) | YES (Gate 11) | Manual (`verify_lean.py`) | `test_*.py` | `GATE11_PYTHON_CI` |
| `reach_additivity` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `reach_measure` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `reachable` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `tests/` | `LOCAL_RECEIPT_LEAN` |
| `record_reading` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `tests/` | `LOCAL_RECEIPT_LEAN` |
| `represented_execution` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `tests/` | `LOCAL_RECEIPT_LEAN` |
| `s9_obligations` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `second` | workflow (gate 11) | YES (Gate 11) | None | `none` | `GATE11_PYTHON_CI` |
| `second_inheritance` | workflow (gate 11) | YES (Gate 11) | None | `test_*.py` | `GATE11_PYTHON_CI` |
| `second_nofirst` | workflow (gate 11) | YES (Gate 11) | YES (Lean Job) | `test_*.py` | `GATE11_FULL_CI` |
| `second_stake` | workflow (gate 11) | YES (Gate 11) | None | `test_*.py` | `GATE11_PYTHON_CI` |
| `second_stream` | workflow (gate 11) | YES (Gate 11) | None | `test_*.py` | `GATE11_PYTHON_CI` |
| `setting_translation` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `tests/` | `LOCAL_RECEIPT_LEAN` |
| `side_free` | workflow (gate 11) | YES (Gate 11) | Manual (`verify_lean.py`) | `tests/` | `GATE11_PYTHON_CI` |
| `sign_slice` | local receipt only | NO (local only) | None | `test_*.py` | `LOCAL_RECEIPT_PYTHON` |
| `standing_commitment` | local receipt only | NO (local only) | Manual (`verify_lean.py`) | `test_*.py` | `LOCAL_RECEIPT_LEAN` |
| `thinghood` | local receipt only | NO (local only) | None | `test_*.py` | `LOCAL_RECEIPT_PYTHON` |
| `two_sided_commitment` | local receipt only | NO (local only) | None | `test_*.py` | `LOCAL_RECEIPT_PYTHON` |
| `typed_translation` | workflow (gate 11) | YES (Gate 11) | YES (Lean Job) | `tests/` | `GATE11_FULL_CI` |

---

## 3. Test Count Drift Reconciliation

### 3.1 Root Pytest Suite Reconciliation
- **Documented in root `README.md` (line 24):** `41 files, 481 collected: 480 passed / 1 skipped`
- **Discovered by current `python -m pytest --collect-only`:** `41 files, 523 collected`
- **Observed Drift:** +42 tests across 41 files.

#### Cause of Drift:
The root test suite expanded through ongoing test development, adding 42 new test cases
across existing test files without updating the historical line in `README.md`.
Because `README.md` is outside the research tree and under blind seal, this report
reconciles and pins the exact per-file counts.

| Test File | Collected Test Count |
|---|---|
| `tests/test_apartness.py` | 6 |
| `tests/test_attachment_ladder.py` | 11 |
| `tests/test_axiom_artifact_bytes.py` | 6 |
| `tests/test_boundary_cancellation.py` | 10 |
| `tests/test_bridge.py` | 10 |
| `tests/test_candidates.py` | 19 |
| `tests/test_claim_ledger_conformance.py` | 26 |
| `tests/test_completion.py` | 29 |
| `tests/test_compression.py` | 20 |
| `tests/test_controller_category.py` | 17 |
| `tests/test_diff_interface.py` | 12 |
| `tests/test_engine.py` | 19 |
| `tests/test_equivariance.py` | 5 |
| `tests/test_export_and_run.py` | 11 |
| `tests/test_g1_class_receipt.py` | 7 |
| `tests/test_gates_skill_matches_workflow.py` | 1 |
| `tests/test_generator.py` | 12 |
| `tests/test_graph_genesis.py` | 12 |
| `tests/test_higher_structure.py` | 6 |
| `tests/test_interpreter_boundary.py` | 25 |
| `tests/test_iso.py` | 11 |
| `tests/test_local_strategy.py` | 8 |
| `tests/test_model.py` | 9 |
| `tests/test_observe.py` | 8 |
| `tests/test_observer_inventory.py` | 12 |
| `tests/test_paper_reconciliation.py` | 6 |
| `tests/test_primdiff.py` | 18 |
| `tests/test_primitive_contact.py` | 16 |
| `tests/test_primitive_core.py` | 19 |
| `tests/test_primitive_passage.py` | 13 |
| `tests/test_primitive_receipt.py` | 5 |
| `tests/test_prose_watchlist.py` | 17 |
| `tests/test_refusal.py` | 13 |
| `tests/test_refusal_frontier.py` | 14 |
| `tests/test_renaming_structure.py` | 9 |
| `tests/test_represented.py` | 22 |
| `tests/test_stable_content.py` | 9 |
| `tests/test_trace_algebra.py` | 10 |
| `tests/test_transition_alphabet.py` | 16 |
| `tests/test_transport_citations.py` | 17 |
| `tests/test_weight_profile.py` | 7 |
| **TOTAL** | **523** |

### 3.2 Gate 11 Hardcoded Literal Pins in `.github/workflows/verify.yml`

The written contract in `verify.yml` pins exact test counts for research trees to prevent
silent empty-suite passes. These literal pins are:

| Tree | Pinned Literal / Regex in `verify.yml` | Purpose |
|---|---|---|
| `second_stream` | `^Ran 150 tests in ` | Rung 1 stream response test count pin |
| `boundary_seed` | `^Ran 566 tests in ` | Boundary derivation test suite pin |
| `second_nofirst` | `^Ran 180 tests in ` | Rung 2 track 1 no-first demand test pin |
| `side_free` | `^Ran 364 tests in ` | Side-free control test pin (paired with `test_registration.py`) |
| `typed_translation` | `^Ran 119 tests in ` | Joined grammar test pin (paired with `test_gates.py`) |
| `limit_and_observer` | `^Ran ([6-9][0-9]|[1-9][0-9]{2,}) tests in ` | Minimum 60 tests regex pin |

---

## 4. Axiom Count Drift & Parked Audit Integrity

### 4.1 Kernel Axiom Inventory Drift
- **Historical Snapshot (`verification_20260817.md`, line 27):** 1,314 axiom reports (56 sources, 55 modules).
- **Current Inventory (`artifacts/lean_axioms.txt` & `README.md`):** 1530 axiom reports across 75 elaborated modules.
- **Reconciliation:** The drift (+216 reports) reflects the legitimate elaboration of 20 additional Lean modules between PR #57 (2026-08-17) and current trunk.
- **Axiom Strictness:** Every one of the 1530 axiom reports is strictly contained in `['Quot.sound', 'propext']`. Zero non-constructive axioms (`Classical.choice`) are present in the theorem call graph.

### 4.2 Definition-Level `Classical.choice` Boundary (ParkedAudit Analysis)
- **The Vulnerability:** `ci/check_parked_audit.py` and `lean4/ParkedAudit.lean` evaluate `#print axioms` on theorems. In Lean 4, `#print axioms` inspects declarations transitively referenced by the target theorem. A `def` or `instance` that invokes `Classical.choice` but is never referenced by an audited theorem does not appear in the axiom report.
- **Estate Status:** All 12 parked modules and 63 import-closure modules have their theorem heads checked. In the unsealed research trees, 26 trees maintain local `verify_lean.py` scripts asserting `ALLOWED_AXIOMS = {'propext', 'Quot.sound'}`.

---

## 5. Summary of Tree Categories

- **GATE11_FULL_CI (2):** Trees with both test/pin checks in Gate 11 and Lean axiom verification in the Lean job.
- **GATE11_PYTHON_CI (11):** Trees whose Python tests and pin checks run in Gate 11, with Lean (if present) attested locally.
- **LOCAL_RECEIPT_LEAN (24):** Trees with local Lean formalizations and `verify_lean.py` manual receipts.
- **LOCAL_RECEIPT_PYTHON (9):** Trees with Python tests only, executed locally.
- **LOCAL_RECEIPT_SPEC (2):** Specification trees without active code test suites.

