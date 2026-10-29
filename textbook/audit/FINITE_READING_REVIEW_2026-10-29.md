# Grouping, finite bounds, renaming, and pruning: reading review

Date: 2026-10-29. AuthorityEffect: None.

## Scope

Selected semantic and readability review of Units 27–30 against read-only
`Quot.lean`, `Counting.lean`, `CountTransport.lean`, `Mention.lean`, their
Python owners, existing paper/ledger records, and book checks. This follows
the [relation review](RELATION_READING_REVIEW_2026-10-29.md).

Four first passes introduce grouping, states versus rounds, transported
questions, and target mention. Short opening claims precede optional
detailed statements and sources; exercise answers are folded. Links lead
to the existing Map and Search labs. Units 28 and 30 have scoped titles in
the current overview and coverage table; their file IDs are unchanged.

## Corrections

| Unit | Previous issue | Correction and evidence |
|---|---|---|
| 27 | Arbitrary `Quot rel` described as though its generating relation already formed equivalence classes; every quotient function said to be constructed only by `Quot.lift` | A raw relation can generate equal quotient values along a chain without directly relating the endpoints. The book proves this on 0, 1, 2. The barrier is about any fixed quotient function, regardless of its construction. Collapse is separately packaged as a book setoid. |
| 27 | Broad procedure language and a language-wide claim about Python; reading a canonical key treated as sufficient for equality of all computation | The theorem concerns a fixed function whose only input is the quotient value. The Python model uses complete profiles and canonical keys as different grouping representations. Equal profile sizes need not give equal profiles: the binary link has two unequal one-element profiles. The native formal quotient is over `Nat`, not just admitted indices. The theorem namespace reference is corrected. |
| 28 | Disabled external supply conflated with fixed datum count; generic finite growth bound sometimes described as a bound on every successful event | Strict growth and a fixed ceiling are explicit hypotheses. The response grammar includes fresh-data items even when an external policy is disabled. Two exported baselines retain their bounded computational evidence. Repeated accepted request events give `[0,1,1,1]`, violating strict growth. |
| 28 | `L` states and `R` intervening rounds conflated; separate parity proof described as compulsory | The book derives `R ≤ B` for `R+1` states and derives the divided pair count from the multiplicative theorem. The native short comment's loose use of “rounds” is qualified without editing the sealed source. |
| 29 | Count statement omitted mapping the candidate list; range bounds described as unnecessary; the inverse described in the wrong proof direction | Count transport compares a list with its mapped list and counts its entries. A three-datum computation changes the answer on a fixed literal pair while preserving the renamed question. `DRen` includes both inverse laws and both range conditions. A reversible swap of 1 and 2 breaks a filled-slot range check with only two admitted data. |
| 29 | Requirement well-formedness said not to transport although this action leaves both `reqs` and `data` unchanged | The requirement guard is definitionally unchanged, proved by `Iff.rfl`. This differs from renaming the demand endpoints, which is the larger action in Unit 31. The native comment near `rename_insts_wf` is read against the actual current record-update definition; no native source is amended. |
| 30 | Fresh contexts said always to be new and always to fail derivability twice; merely mentioning a target said to produce separation | Unary context spaces need not grow when data arrive. With an unchanged uniform rule, a fresh-slot context can be positive on both old targets. R1 preserves old comparisons under its instance-range condition; it does not rule out new classes. R2 has distinct instance-form and rule-form range conditions. Mention alone is not sufficient for separation. |
| 30 | A newcomer-only instance described as omitted by the cost-2 generator; source theorem said to require an admitted target pair | R3 changes only the instance list and quantifies over natural indices. For a collapsed old pair, R1 then R3 shows the newcomer-only candidate cannot separate it. Shape (b) actually generates it and the validity check rejects it. A raw stale form reference also demonstrates why R2's old-form condition cannot simply be dropped. |

The form-activation example starts from a deliberately malformed raw
record. It is a counterexample to dropping a hypothesis, not a native
admission history from genesis. The fresh-context example uses an actual
valid Python history and an unchanged uniform rule. The native R1 proof
preserves the rule clause even though its comment's shorter gloss only
describes failed membership.

## Added book reports

The four book drivers check 49 exact reports. Eleven are new:

| Script | Report | Exact library dependencies |
|---|---|---|
| u27 | `collapse_refl` | `propext` |
| u27 | `collapse_trans` | `propext` |
| u27 | `collapseSetoid` | `propext` |
| u27 | `raw_chain_quotient` | `propext, Quot.sound` |
| u28 | `accepted_round_bound` | `propext, Quot.sound` |
| u28 | `allPairs_divided` | `propext, Quot.sound` |
| u29 | `jump_invol` | none |
| u29 | `bounded_context_needed` | `propext, Quot.sound` |
| u29 | `requirement_guard_unchanged` | none |
| u30 | `fresh_rule_context_positive` | `propext, Quot.sound` |
| u30 | `raw_form_activation` | `propext, Quot.sound` |

Ten are theorems; `collapseSetoid` is a definition carrying an equivalence
proof. None changes the sealed declaration inventory or native receipt.
The fixed-list Python example is a bounded computation, not a new general
theorem about arbitrary lists. The original 24/6 renamings, 59/26/33
candidate counts, and two baseline trees keep their existing populations.

Four temporary false propositions and one temporary generator omission
exercise the checks. The [injection record](../../docs/injection_record.md)
records their exact failures and recovery. No native artifact or pin is
regenerated under a defect.

## Reproduction and limits

Run `python ci/run_gates.py --job textbook` in the pinned local environment;
the PR records the clean source head and receipt. This is the textbook job,
not the twelve-family local merge contract.

This review covers selected claims in four chapters. It does not certify
every paragraph, declaration placement, S/A classification, source anchor,
hosted layout, or reader outcome. Later formal and research teaching,
comprehension, transfer, and retention remain open. The grouping and
counting arguments supply no general empirical claim about reality.
