# Grammar-fit claim ledger

This ledger belongs only to `research/grammar_fit/`.  It reports a local
metatheory reconstruction and finite computations; it does not amend the
sealed derivation or register authority for a new constructor.

| ID | Claim | Evidence class | Evidence pointer | Falsifier |
| --- | --- | --- | --- | --- |
| GF-BOUNDARY | The run writes only under `research/grammar_fit/` and records the sealed paths as read-only. | DECLARED_POLICY | `grammar_fit.py::WRITE_ROOT`, receipt `sealed_paths_touched` | A nonempty sealed-path mutation list or a write outside the root fails the scope check. |
| GF-PROMPT | The grammar-fit prompt and priced receipt are byte-pinned before construction. | FINITE_COMPUTATION | `grammar_fit.py::check_inputs`, receipt hashes | Any byte or line-ending drift raises before the receipt is built. |
| GF-SEATING | Collision, equal-profile, and directional-residual data are seated in local grammar states; asserted/maps, profile fields, and comparison fields remain explicitly outside those states. | FINITE_COMPUTATION | `grammar_fit.py::seat_objects`, receipt `objects` | Moving an outside field into state without a named constructor fails the seating test. |
| GF-EVENT | No object-derived state-changing constructor or guarded response is found. `Impose` is an external challenge and `Observe` labels are no-op columns; `refineCol` and `addCol` are not upgraded to passage constructors. | FINITE_COMPUTATION | `grammar_fit.py::fit_events`, receipt `event_fit`, `test_grammar_fit.py::test_event_columns_keep_external_and_noop_separate` | Counting an external `Impose`, a no-op label, or an unguarded column name as `next_event_found` fails the negative test. |
| GF-PROFILE | A non-empty unary instance distinguishes the two data, so the built profile case is not the empty-profile case. | FINITE_COMPUTATION | `grammar_fit.py::nontrivial_profile_case`, receipt `profile_case` | Removing the instance must restore equal empty profiles. |
| GF-COMPARISON | Directional comparison policy is excluded as `DECLARED_POLICY`; no constructor is charged for it and the residual remains open. | DECLARED_POLICY | `grammar_fit.py::comparison_policy`, receipt `comparison` | A comparison atom or policy constructor would require a new priced declaration. |
| GF-MEASURE | The packet retains one named cost measure, `mu_fit_oriented_s9`, and does not reuse a second historical measure. | FINITE_COMPUTATION | `grammar_fit.py::fit_measure`, receipt `measure` | A second measure or a different bill total fails the single-measure test. |
| GF-ORIENTATION | Orientation is an explicit priced atom and the ordered-pair key keeps forward and reverse keys distinct; minimum ties remain retained. | FINITE_COMPUTATION | `grammar_fit.py::orientation_disposition`, receipt `orientation` | Forgetting order or dropping a minimum class fails the orientation test. |
| GF-S9 | Replaying inscription plus `Supply("<>")` leaves all six S9 lines unpaid. | FINITE_COMPUTATION | `grammar_fit.py::s9_bridge`, receipt `s9_bridge` | Treating supply as admission makes the six-line replay test fail. |
| GF-OPEN | OB-1, S6.6, S9's last bullet, comparison policy, and the unlisted candidate space remain open. | OPEN | receipt `open_boundaries`, `STATUS.md` | Any closure terminal for a named open surface fails the test. |
| GF-REFUSAL | Genesis does not fire `two_rule`; a missing-flag table and the historical tick table are not used as computation or evidence. | REFUSED | `grammar_fit.py::refusals`, receipt `refusals`, `test_grammar_fit.py::test_table_and_clock_closures_are_not_reported` | A genesis rule event, table-as-computation claim, or tick-table citation fails the refusal checks. |

## Scope note

`next_event_found` has the narrow scope `object_derived_state_change_only`.
Every object has an external `Impose` candidate, but that candidate is marked
`SUPPLIED_INPUT` and never sets the field.  The equal-profile context and the
two residual presentations produce `Observe` labels only; replay proves each
label leaves the grammar state unchanged.  Therefore the legal terminal is
`STATE_CHANGE_NOT_FOUND` together with `LABEL_ONLY`, not a successor claim.
