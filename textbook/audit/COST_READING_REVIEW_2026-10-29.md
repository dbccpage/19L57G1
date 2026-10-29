# Requests, responses, and cost: reading review

Date: 2026-10-29. AuthorityEffect: None.

## Scope

Selected semantic and readability review of Units 17–22 against the current
read-only `Basic.lean`, `Minimality.lean`, `MinimalityF.lean`, Python
model/candidate/observation/isomorphism code, and their existing paper,
ledger, artifact, and book checks. This follows the
[Units 04–16 review](EARLY_READING_REVIEW_2026-10-29.md).

Six first passes now explain requests, the two-item lower bound, link and
loop witnesses, tied minima, and lexicographic prices with small examples.
Each opening claim is shorter; its detailed statement is retained with
the folded source/classification record. Exercise answers are folded. Two
chapters link to the slower Search lab. The original unit IDs, source
classifications, sealed files, and historical audit inventory are retained.
The word counts and passing checks are not learning-outcome evidence.

## Corrections

| Unit | Previous wording or inference | Current explanation |
|---|---|---|
| 17 | Every pair in a replayed record is sorted, without the initial-state qualification in the pseudocode; an accepted request means one more pair | Successful replay preserves sorting when it holds initially. A raw reversed pair survives a later valid request. Repeating an already present valid request leaves the state unchanged. Admission records a task and does not satisfy it. |
| 18 | Removing the form-range guard makes an unknown-form instance apply; breaking the rejection branch suggests failure of the lower bound | The remaining arity guard still rejects the displayed two-argument instance. Even forcibly inserting it into a raw record provides no well-formed context while forms remain empty. The record is malformed; a failed proof step alone is not a mathematical counterexample. The larger finite Python slice now states its actual argument lengths and includes out-of-range indices. |
| 19 | Not proved whether the link is cheapest; ordering described as absent | The link attains the proved item-count floor and is one cheapest response. It loses to the unary mark under the second measure. Argument positions remain ordered under isomorphism; swapping datum labels is different from swapping positions. No physical direction or relationship follows from the representation. |
| 19–20 | Any sentence mentioning one target suffices for separation | The positive and negative pluggings must actually disagree. A uniform rule retains the original link/loop instance while making both targets answer every available question positively. The pair collapses. The admission event can succeed while the response-validity test fails. |
| 21 | Incorrect condition count for `Iso`; a finer measure chooses | The text names the preservation conditions without the wrong count. A measure can leave one minimum class without choosing a literal response or executing an admission. |
| 22 | A proof restricted by new-form arity used as a reason about another cost; only an arity-sensitive cost could break ties; no statement about three-item responses | The alternative instance-count cost is refuted as unique by the existing mark and link, with a separate lower-bound argument. No universal claim about all alternative costs remains. Lexicographic priority excludes every three-item response from beating `(2, 1)` without classifying its shape. Python isomorphism comparisons include the recorded demand in both readings. |

## Added book proofs

These are teaching apparatus outside the frozen derivation. The five
changed Lean scripts check 67 reports altogether, including the existing
native results. Eight new reports remain inside the current axiom boundary:

| Script | New theorem | Exact library dependencies |
|---|---|---|
| u17 | `repeated_demand_unchanged` | `propext` |
| u17 | `malformed_base_survives` | `propext` |
| u18 | `no_forms_no_separation` | `propext` |
| u18 | `unknown_form_not_separable` | `propext` |
| u18 | `unknown_form_not_wf` | `propext, Quot.sound` |
| u19 | `BL_uniform_collapsed` | `propext, Quot.sound` |
| u20 | `BD_uniform_collapsed` | `propext, Quot.sound` |
| u22 | `instance_count_tie` | `propext, Quot.sound` |

The general no-form theorem follows directly from the context's required
form-range condition. It makes no statement about a different context
definition. The instance-count theorem exhibits tied valid responses and
their non-isomorphism; the text separately explains why no lower cost is
valid. No new theorem is added to a sealed module or native receipt.

Four false propositions are rejected in separate temporary book drivers:
a repeated request changing `R2L`, a two-element argument list having the
unknown form's default arity zero, a negative answer surviving the uniform
rule, and the link having a smaller new-form arity sum than the unary mark.
Lean names each exact proposition as false. See the dated
[injection record](../../docs/injection_record.md).

## Remaining work

Reproduce the textbook checks with `python ci/run_gates.py --job textbook`
in the pinned local environment. The PR records the exact source head and
local receipt. This runs the textbook job, not all twelve gate families.

This is a selected-claim repair in six chapters. It does not certify every
paragraph, source anchor, substantive/auxiliary classification, or
declaration's teaching coverage. Later chapters and research lessons remain
under review. Reader transfer and retention, hosted rendering of this
edition, and the complete twelve-family local merge run are not established
by these focused checks.
