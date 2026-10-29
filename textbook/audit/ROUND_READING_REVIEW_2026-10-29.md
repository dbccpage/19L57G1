# Transitions, recorded demands, and response existence: reading review

Date: 2026-10-29. AuthorityEffect: None.

## Scope

Selected semantic and readability review of Units 31–35 against read-only
`TransitionTransport.lean`, `MinimalityF.lean`, `RuleBridge.lean`,
`Rounds.lean`, `Progress.lean`, their Python owners, and book checks. This
follows the [finite and transport review](FINITE_READING_REVIEW_2026-10-29.md).

Five concrete first passes precede shorter claims, optional detailed
statements and sources, and folded exercise answers. Titles for Units
31, 33, 34, and 35 now expose the relevant scope. Their file IDs and the
recorded prerequisite graph remain unchanged. Units 04–35 now have 32
consecutive revised openings; that count does not certify complete teaching
coverage or reader mastery.

## Corrections

| Unit | Previous issue | Correction and evidence |
|---|---|---|
| 31 | Child padding limited to one new datum; theorem language broadened to arbitrary policies and general isomorphisms | `DRen.pad` works at every larger datum count. The relation theorem concerns bounded datum renamings with forms fixed; the least-index regression is one policy counterexample. Python class sets and minimum enumeration remain separate finite evidence. |
| 31 | Exercise attributed the requirement hypothesis only to validity and treated normalization collisions as enough to change separation truth | Exact response transport also reads insertion and literal lists. An identity renaming on raw demands `[(1,0)]` sorts before versus after insertion, producing one versus two copies of `(0,1)`. This is a malformed-record counterexample to omitting ordering, not a failure of symmetric separation merely from duplicate tests. Count transport compares the caller list with its mapped list. |
| 32 | Python compared results with empty demand stores while Lean used `R2F`; one result class described as a forced labelled choice | Both readings now record the target before applying responses and check that the demand store is retained. The two successful marks remain different labelled deltas. Each reading has one minimum class under `mu2`; their different datum counts prohibit a cross-reading isomorphism. The four-datum exercise is checked as a finite example, not silently promoted to `mu2_unique_F`. |
| 33 | Shortening described as exactly one item; new datum said separable from everything; claim generalized beyond uniform rules and declared costs | The drop removes all new uniform-rule items and is strictly shorter if any were present. In the existing mixed example, the binary form preserves both required pairs, while newcomer 3 remains collapsed with datum 1. Validity and minimality remain different. The free-parameter induction explains the displayed proof, not the impossibility of every alternative proof. |
| 34 | Closed-run count read as number of demands met; initial-store assumptions omitted; no inhabitant claimed despite explicit runs | `ClosedRun.cons` requires fresh imposition, no new datum, and successful replay, but neither collapse nor `validResponse`. An empty response on two bare data is a formal closed run with an unmet demand. The general bound requires an initially ordered, bounded, duplicate-free store; the empty-store corollary supplies those facts. Existence of every allowed length and an infinite supplied run are not proved. |
| 35 | Failure of one mark treated as absence of any response; every bound said necessary; freshness assigned to `respond` | The unmet-demand example has a checked four-item repair. A malformed stale-rule record defeats the fresh mark when `wf` is dropped. The published proof never uses `hi`; a book example plugs an unadmitted first target. The theorem retains its stated admitted-target scope. Freshness belongs to `ClosedRun.cons`, while `respond` absorbs repeats. |
| 35 | Library dependencies described incorrectly; existence conflated with implementation search success; a third-datum mark rejected even for an already-separated pair | The exact reports distinguish the self-pair refutations from concrete reductions. The proof supplies a delta, while Python must enumerate it. A third-datum mark fails to repair a collapsed pair but may be valid when the target was already separated. A finite tree reaching its cap is not an infinite-execution theorem. |

References to admission guards now lead to Unit 17; references to the two
genesis readings lead to Unit 05. Frozen source comments and theorem
statements are read against their actual definitions, without modifying
native files. The stale-rule and disordered-demand records are explicitly
malformed raw examples, not histories admitted from genesis.

## Added book reports

The five book drivers check 70 exact reports. Seven are new:

| Script | Report | Exact library dependencies |
|---|---|---|
| u31 | `respond_order_needed` | `propext` |
| u34 | `unanswered_closed` | `propext, Quot.sound` |
| u34 | `empty_response_invalid` | `propext` |
| u34 | `repeat_response_no_growth` | `propext` |
| u35 | `longer_repair_valid` | `propext, Quot.sound` |
| u35 | `stale_rule_breaks_mark` | `propext, Quot.sound` |
| u35 | `unadmitted_first_target` | `propext, Quot.sound` |

The other reports and the native axiom inventory retain their populations.
The four-datum marks and newcomer collapse are finite Python examples;
they are not new grammar-wide uniqueness or renaming theorems.

Temporary false propositions and temporary book-check substitutions
exercise the new boundaries. The [injection record](../../docs/injection_record.md)
records their rejection and recovery. No native source, artifact, receipt,
or watchlist population is changed under a defect.

## Reproduction and limits

Run `python ci/run_gates.py --job textbook` in the pinned local environment.
The PR records the clean source head and receipt. This is the textbook
job, not the twelve-family local merge contract; the PR remains draft for
the author.

The author reports that the reading is fine. That feedback is retained as
readability feedback, not a scored novice, transfer, or retention result.
This review covers selected claims in five chapters. Other formal and
research teaching, semantic classification, source placement, hosted
rendering, and reader outcomes remain open. None of these model examples
establishes an empirical law about reality.
