# Typed translation: gate injections

`AuthorityEffect: None.`

These injections were run after build commit `90f00bc9` in the isolated
typed-translation worktree.  In this table, `python` denotes the exact runtime
`C:\Users\a343o\AppData\Local\Python\pythoncore-3.14-64\python.exe`; Python
test commands were run with `PYTHONPATH=code`.  Every mutation was minimal and
reversed before the recovery command.  No pin, receipt, prose page, coverage
report, or axiom inventory was regenerated while its mutation was live.

| gate | injected defect | failing command and observed diagnostic | fail | reversal and recovered diagnostic | recovered |
|---|---|---|---:|---|---:|
| frozen bytes | Changed only the verifier's expected `REQUIREMENTS.md` digest from leading `4` to `5`; the frozen file itself was never touched. | `python verify_pins.py` — `FAIL: frozen REQUIREMENTS.md working bytes moved`; `FAIL: frozen REQUIREMENTS.md does not match its freeze-commit blob` | 1 | Restored the expected digest; `pins ok: 2 frozen files at 2f576e5803ae, 31 exact source blobs at 6129e859f8889aa197d186e6a330aed43ef672fc, 37 vendored rows, 6 isolated kernel modules` | 0 |
| exact source blobs | Changed the first manifest digest from leading `6` to `7`. | `python verify_pins.py` — `FAIL: code/derivation/model.py blob digest differs at pinned commit` | 1 | Restored the manifest digest; the full `pins ok` line above returned. | 0 |
| vendored source population | Appended one word to R00's vendored subject. | `python verify_pins.py` — `FAIL: vendored dependence bytes differ from the build pin`; `FAIL: vendored dependence population differs from pinned receipts` | 1 | Restored the exact R00 subject; the full `pins ok` line returned. | 0 |
| kernel isolation | Added the absolute import `import derivation` to the kernel package root. | `python verify_pins.py` — `FAIL: code\typed_translation\__init__.py imports undeclared external root derivation` | 1 | Removed the import; the full `pins ok` line returned. | 0 |
| candidate census | Removed `true` from the administrative-presentation axis. | `python -m unittest tests.test_enumeration.EnumerationTests.test_candidate_count_is_exact_and_unpruned` — `AssertionError: 64 != 128` | 1 | Restored the axis; `Ran 1 test in 0.250s`, `OK` | 0 |
| independent history census | Started the unpruned permutation census at length one, omitting the empty prefix. | `python -m unittest tests.test_enumeration.EnumerationTests.test_unpruned_history_census_agrees_in_order` — `First differing element 0` and `Second tuple contains 1 additional elements` | 1 | Restored length zero; `Ran 1 test in 0.276s`, `OK` | 0 |
| total projection | Made removal drop `history` as well as `boundary`. | `python -m unittest tests.test_removal.RemovalTests.test_projection_drops_exactly_boundary` — `AssertionError: R00 projection changed keys ['boundary', 'history']` | 1 | Restored the all-fields-except-one comprehension; `Ran 1 test in 0.001s`, `OK` | 0 |
| refusal shell | Made an unknown label decode silently to an empty accepted state. | `python -m unittest tests.test_translation.CodecTests.test_nearby_shell_is_nonempty_and_fully_named` — `First list contains 226 additional elements` in `silent_truncations` | 1 | Restored `UNKNOWN_LABEL`; `Ran 1 test in 0.049s`, `OK` | 0 |
| asserted test count | Changed only the workflow literal from 119 to 120. | `python -m unittest tests.test_gates.GateRegistrationTests.test_workflow_literal_equals_discovered_test_count` — `AssertionError: 120 != 119` | 1 | Restored 119; `Ran 1 test in 0.033s`, `OK` | 0 |
| dual coverage | Added one uncalled two-branch function to the measured kernel, then regenerated coverage with all tests. | `python -m coverage run -m unittest discover -s tests -p 'test_*.py'`, `python -m coverage json -q`, `python check_coverage.py` — `line 97.15% branch 94.86% over 6 files`; `FAIL: coverage under 95%` | 1 | Removed the function, then regenerated only after reversal; `Ran 119 tests in 50.228s`, `OK`; `line 97.51% branch 95.52% over 6 files` | 0 |
| deterministic receipt | Changed the committed receipt schema suffix from `v1` to `v0`. | `python run_translation.py --check` — `FAIL: drift in receipts\typed_translation.json` | 1 | Restored the byte without regeneration; `checked typed translation: 128 candidates, 2 valid, removal 22/37, 1362786 bytes, sha256 560fec2b663e90fa95730ae8dace8477f644dc9cc27f9278f567f7c88917cbe4` | 0 |
| prose binding | Added `drift` to the `STATUS.md` title. | `python verify_prose.py` — `FAIL: STATUS.md differs from the fresh receipt rendering` | 1 | Restored the title without regeneration; `prose ok: 3 rendered documents match the fresh computation` | 0 |
| strict typing | Added a `str` initializer annotated as `int` to `run_translation.py`. | `python -m mypy` — `run_translation.py:18: error: Incompatible types in assignment (expression has type "str", variable has type "int")`; `Found 1 error in 1 file (checked 10 source files)` | 1 | Removed the assignment; `Success: no issues found in 10 source files` | 0 |
| Lean declaration totality | Added an elaborable theorem without adding a root `#print axioms` request. | `python verify_lean.py` — `FAIL: theorem inventory differs`, naming `TypedTranslation.injected_unreported` only in the declared list | 1 | Removed the theorem; `lean ok: 1 modules, 3 theorem reports within ['Quot.sound', 'propext'], byte-identical inventory` | 0 |
| Lean receipt freshness | Changed one theorem name in `lean/axioms.txt`. | `python verify_lean.py` — `FAIL: fresh reports differ from lean/axioms.txt` | 1 | Restored the committed byte without regeneration; the full `lean ok` line above returned. | 0 |
| Lean forbidden-token scan | Put the forbidden proof-placeholder token in a Lean line comment. | `python verify_lean.py` — `FAIL: lean\TypedTranslation\Basic.lean:11: forbidden token sorry` | 1 | Removed the comment; the full `lean ok` line returned. | 0 |

The recovered values in this table are observations from the reversal runs,
not claims that a green gate proves the mathematical payload.  The exact
bounded results remain in `receipts/typed_translation.json` and their theorem
claims remain separately constrained by the Lean inventory.
