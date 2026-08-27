# Priced admissions claim ledger

This ledger belongs only to `research/priced_admissions/`.  Its evidence
classes and falsifiers are part of the run's local receipt; it neither amends
nor registers a claim in the sealed derivation.

| ID | Claim | Evidence class | Evidence pointer | Falsifier |
| --- | --- | --- | --- | --- |
| PA-BOUNDARY | The run writes only under `research/priced_admissions/` and records the sealed paths as read-only. | DECLARED_POLICY | `priced.py::SEALED_PATHS`, receipt `sealed_paths_touched` | A nonempty sealed-path mutation list fails the scope test. |
| PA-PROMPT | The new prompt is byte-pinned before the run. | FINITE_COMPUTATION | `priced.py::prompt_hash`, receipt `prompt_sha256` | Any prompt byte or line-ending drift raises before receipt construction. |
| PA-COLLISION | A concrete two-point relation and identifying map produce a loop after identifying the asserted endpoints; the protected law is irreflexivity. | FINITE_COMPUTATION | `priced.py::build_collision` | Removing the edge or changing the map makes `law_after` no longer false. |
| PA-PROFILES | Two concrete data with one admitted unary form and no derivable instance have equal, empty profiles. | FINITE_COMPUTATION | `priced.py::build_equal_profiles` | Adding a distinguishing instance makes the profile equality test fail. |
| PA-RESIDUAL | Two concrete presentations of one directed edge have a left map that identifies the pair and a right map that separates it. | FINITE_COMPUTATION | `priced.py::build_directional_residual` | Replacing either map so both agree makes the directional residual test fail. |
| PA-EVENT | Existing admission, observation, and external-challenge constructors are searched from each concrete state; guarded response construction is absent because its actual stores are absent. | FINITE_COMPUTATION | `priced.py::event_search_report` | Supplying retained/protected/observation stores changes the guarded-response result. |
| PA-ORIENT | Orientation is an explicit one-atom admission and the canonical key preserves the ordered asserted pair. | FINITE_COMPUTATION | `priced.py::orientation_report`, receipt `orientation` | An unordered pair key causes the forward/reverse mutation test to fail. |
| PA-TIES | The named finite candidate space retains both minimum law-bearing classes instead of selecting one. | FINITE_COMPUTATION | `priced.py::_minimum`, receipt `minimum_with_orientation.representatives` | Dropping either representative or changing its class key fails the tie test. |
| PA-S9 | The six-line S9 bill is replayed from `Supply("<>")`; no line is paid by supply alone. | FINITE_COMPUTATION | `priced.py::s9_bill_report` | Treating `Supply` as an admission makes the replay negative test fail. |
| PA-LAWS | The finite law list is named and each listed law is checked for a collapse witness; laws outside it remain open. | FINITE_COMPUTATION | `priced.py::law_violation_report` | Extending the list without a row or witness disposition fails the law test. |
| PA-OPEN | OB-1, S6 item 6, and the S9 last bullet remain open. | OPEN | receipt `open_boundaries`, `STATUS.md` | Any closure terminal for one of these surfaces fails the negative test. |
| PA-REFUSAL | Genesis does not fire `two_rule`, and a requirement table is not used as a computation. | REFUSED | receipt `refusals`, `test_priced.py` | A genesis `two_rule` event or a table-only object report fails the refusal tests. |

## Scope note

`NEXT_EVENT_FOUND` is scoped to an externally imposed `Impose` event (and to
the reconstructed observation declarations where present).  `NEXT_EVENT_NOT_FOUND`
is scoped to the guarded response family: all three concrete objects lack at
least one required retained/protected/observation admission.  Neither terminal
is a claim of an internally generated successor.
