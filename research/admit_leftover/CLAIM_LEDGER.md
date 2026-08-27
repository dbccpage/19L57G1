# Admit-leftover claim ledger

This ledger belongs only to `research/admit_leftover/`.  It records one
explicit local admission choice and the fields left outside state.  It does
not amend the sealed derivation or authorize a successor.

| ID | Claim | Evidence class | Evidence pointer | Falsifier |
| --- | --- | --- | --- | --- |
| AL-BOUNDARY | The run writes only under `research/admit_leftover/` and treats grammar-fit as read-only input. | DECLARED_POLICY | `admit_leftover.py::WRITE_ROOT`, receipt `sealed_paths_touched` | A nonempty sealed-path mutation list or a write outside the root fails the scope test. |
| AL-PROMPT | The new prompt and grammar-fit receipt are byte-pinned before construction. | FINITE_COMPUTATION | `admit_leftover.py::check_inputs`, receipt hashes | Prompt or input-receipt drift raises before the receipt is built. |
| AL-ASSERT | The collision asserted pair is admitted by `assertWit` and appears in the new state; the identifying map remains outside. | FINITE_COMPUTATION | `collision_admission`, receipt `admission_choice` | Removing the admission or placing the map in state fails the state comparison. |
| AL-PROFILE | Profile rows are recomputed from the admitted instance state, not supplied as rows. | FINITE_COMPUTATION | `profile_rows`, `profile_case_from_input`, receipt `profile_case` | Changing/removing the instance changes the computed rows and fails the replay check. |
| AL-EVENT | Post-admission search keeps state change, no-op labels, external challenge, and guarded response separate. | FINITE_COMPUTATION | `_search_columns`, receipt `search_after_each_choice` | Counting `Impose`, `Observe`, or a conditional response as `state_change_found` fails the test. |
| AL-GUARD | `admitWit` is only a conditional guarded response after `assertWit`; it is not fired or called endogenous. | CONDITIONAL | `collision_admission`, receipt `GUARDED_CONDITIONAL` | A fired response without its extra admission fails the guard test. |
| AL-BILL | The chosen assertion spends one atom; retained/protected stores are conditional and comparison/map fields are explicitly outside or policy-excluded. | FINITE_COMPUTATION | `admission_bill`, receipt `measure` | Any unpriced extra admission fails the no-free-store test. |
| AL-COMPARISON | The residual comparison policy remains `COMPARISON_EXCLUDED` and open. | DECLARED_POLICY | `comparison`, receipt `open_boundaries` | A comparison constructor or atom would require a new declaration. |
| AL-ORIENTATION | The inherited ordered-pair key distinguishes reversal and retains the two priced minimum classes. | FINITE_COMPUTATION | `orientation_from_input`, receipt `orientation` | Forgetting order or dropping a tie fails the orientation test. |
| AL-S9 | Inscription plus `Supply("<>")` leaves all six S9 lines unpaid; the extra assertion is not supply. | FINITE_COMPUTATION | `s9_bridge`, receipt `s9_bridge` | Treating supply as admission or mixing histories fails the bridge test. |
| AL-OPEN | OB-1, S6.6, S9's last bullet, the map, comparison, and guarded family remain open. | OPEN | `open_boundaries`, `STATUS.md` | Any closure terminal for a named open surface fails the negative test. |
| AL-REFUSAL | Genesis `two_rule`, table-as-computation, and sealed/sibling writes are refused. | REFUSED | `refusals`, direct tests | A genesis rule event, table claim, or sibling mutation fails the refusal checks. |

## Scope note

`LEFTOVER_ADMITTED` applies only to the asserted pair and its named
`assertWit` choice.  The identifying map is still `LEFTOVER_LEFT_OUTSIDE`.
The residual comparison is excluded as `DECLARED_POLICY`.  The guarded family
is conditional on a further explicit `admitWit` admission and is unfired.
No line above is a claim of a unique minimum or a complete candidate space.
