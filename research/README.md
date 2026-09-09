# Research trees: what runs where

AuthorityEffect: None.  This file states, once, which research trees the
hosted workflow enumerates and which are local receipts only, and which
verifier files are hand copies of one another.  It is a map, not a gate:
nothing reads it.  Regenerate it by hand when a tree is added or wired.

Hosted CI is dormant (the Actions billing lapsed), so at present every
receipt in every tree is local, including the wired ones; "workflow" below
means the tree is enumerated by `.github/workflows/verify.yml` and would run
under gate 11 if the workflow ran.  The 2026-08-21 incident recorded in
`CLAUDE.md` — five failing research tests under a green rollup — is why the
distinction is written down.

Every tree's Lean package is a manual receipt: no gate builds the research
Lake packages (`CLAUDE.md`, gate 11).  A tree marked "manual receipt" carries
`verify_lean.py` and an `evidence/lean.json` written by hand-run compilation.

| tree | gate 11 | check entry points | tests | Lean axioms |
|---|---|---|---|---|
| `admission_sign_shadow` | local receipt only | `verify_frozen_compatibility.py`, `verify_lean.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `admit_leftover` | local receipt only | none | test_*.py | none |
| `balance_carrier` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `blind_restart` | workflow (gate 11) | `verify_pins.py` | test_*.py | none |
| `boundary_seed` | workflow (gate 11) | `verify_freeze.py`, `verify_lean.py`, `verify_pins.py` | tests/ | manual receipt (`verify_lean.py`) |
| `coherent_process_limits` | local receipt only | `verify.py`, `verify_lean.py`, `verify_sources.py` | tests/ | manual receipt (`verify_lean.py`) |
| `closed_family` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `convention_price` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `described_replay` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `dynamics_step` | local receipt only | none | test_*.py | none |
| `family_embedding` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `fresh_characters` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `g1_local_class` | local receipt only | none | none | none |
| `genesis_continuation` | local receipt only | none | none | none |
| `grammar_fit` | local receipt only | none | test_*.py | none |
| `identification_dual` | local receipt only | `verify_pins.py` | test_*.py | none |
| `ignition` | local receipt only | `verify.py`, `verify_lean.py`, `verify_sources.py` | tests/ | manual receipt (`verify_lean.py`) |
| `limit_and_observer` | workflow (gate 11) | `verify_lean.py`, `verify_pins.py`, `verify_prose.py` | tests/ | manual receipt (`verify_lean.py`) |
| `local_reuse` | local receipt only | `verify_lean.py`, `verify_sources.py` | tests/ | manual receipt (`verify_lean.py`) |
| `magnification` | local receipt only | `verify.py`, `verify_lean.py`, `verify_sources.py` | tests/ | manual receipt (`verify_lean.py`) |
| `natural_sections` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `observer_visibility` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `partial_decide` | workflow (gate 11) | `verify_pins.py` | test_*.py | none |
| `record_reading` | local receipt only | `verify.py`, `verify_lean.py`, `verify_sources.py` | tests/ | manual receipt (`verify_lean.py`) |
| `path_dependent_cost` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `portable_interface` | workflow (gate 11) | `verify_pins.py` | test_*.py | none |
| `priced_admissions` | local receipt only | none | test_*.py | none |
| `primitive_difference_tower` | workflow (gate 11) | `verify_lean.py`, `verify_manifest.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `reach_additivity` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `reach_measure` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `reachable` | local receipt only | `verify.py`, `verify_lean.py`, `verify_sources.py` | tests/ | manual receipt (`verify_lean.py`) |
| `represented_execution` | local receipt only | `verify.py`, `verify_lean.py`, `verify_sources.py` | tests/ | manual receipt (`verify_lean.py`) |
| `s9_obligations` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `second` | workflow (gate 11) | none | none | none |
| `second_inheritance` | workflow (gate 11) | `verify_pins.py` | test_*.py | none |
| `second_nofirst` | workflow (gate 11) | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `second_stake` | workflow (gate 11) | `verify_pins.py` | test_*.py | none |
| `second_stream` | workflow (gate 11) | `verify_pins.py` | test_*.py | none |
| `setting_translation` | local receipt only | `verify.py`, `verify_lean.py`, `verify_sources.py` | tests/ | manual receipt (`verify_lean.py`) |
| `side_free` | workflow (gate 11) | `verify_lean.py`, `verify_pins.py` | tests/ | manual receipt (`verify_lean.py`) |
| `sign_slice` | local receipt only | `verify_pins.py` | test_*.py | none |
| `standing_commitment` | local receipt only | `verify_lean.py`, `verify_pins.py` | test_*.py | manual receipt (`verify_lean.py`) |
| `thinghood` | local receipt only | none | test_*.py | none |
| `two_sided_commitment` | local receipt only | `verify_pins.py` | test_*.py | none |
| `typed_translation` | workflow (gate 11) | `verify_lean.py`, `verify_pins.py`, `verify_prose.py` | tests/ | manual receipt (`verify_lean.py`) |

13 trees are wired; 32 are local receipts only.

## Hand copies

The custody, Lean and record verifiers were copied tree to tree with names
changed; there is no shared helper, and a defect fixed in one copy stays
live in the others until carried by hand (the primed-name report parser was
one such defect).  The copies to touch on a defect:

* `verify_sources.py`: `coherent_process_limits`, `ignition`, `local_reuse`, `magnification`, `reachable`, `record_reading`, `represented_execution`, `setting_translation`
* `verify_pins.py`: `balance_carrier`, `blind_restart`, `boundary_seed`, `closed_family`, `convention_price`, `described_replay`, `family_embedding`, `fresh_characters`, `identification_dual`, `limit_and_observer`, `natural_sections`, `observer_visibility`, `partial_decide`, `path_dependent_cost`, `portable_interface`, `reach_additivity`, `reach_measure`, `s9_obligations`, `second_inheritance`, `second_nofirst`, `second_stake`, `second_stream`, `side_free`, `sign_slice`, `standing_commitment`, `two_sided_commitment`, `typed_translation`
* `verify_lean.py`: `admission_sign_shadow`, `balance_carrier`, `boundary_seed`, `closed_family`, `coherent_process_limits`, `convention_price`, `described_replay`, `family_embedding`, `fresh_characters`, `ignition`, `limit_and_observer`, `local_reuse`, `magnification`, `natural_sections`, `observer_visibility`, `path_dependent_cost`, `primitive_difference_tower`, `reach_additivity`, `reach_measure`, `reachable`, `record_reading`, `represented_execution`, `s9_obligations`, `second_nofirst`, `setting_translation`, `side_free`, `standing_commitment`, `typed_translation`
* `run.py`: `coherent_process_limits`, `ignition`, `local_reuse`, `magnification`, `record_reading`, `represented_execution`, `setting_translation`
* `verify.py`: `coherent_process_limits`, `ignition`, `magnification`, `reachable`, `record_reading`, `represented_execution`, `setting_translation`

A shared module under `research/` importable by every tree is the repair;
until it exists, this list is the checklist.
