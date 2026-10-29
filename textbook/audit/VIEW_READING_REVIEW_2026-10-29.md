# Membership, refusal records, and observation windows: reading review

Date: 2026-10-29. AuthorityEffect: None.

## Scope

Selected semantic and readability review of Units 36 and 38–41 against
read-only `Ext.lean`, `Refusal.lean`, `RefusalFrontier.lean`,
`Generator.lean`, `SeparationCapacity.lean`, their Python owners, native
artifacts, and book checks. This follows the
[transition and response review](ROUND_READING_REVIEW_2026-10-29.md).
Unit 37's earlier revision is preserved.

Five first passes use ledger tables, occurrence records, declared price
comparisons, and chain windows. Short claims precede optional detailed
statements and sources; answers are folded. All five titles now state
their scope. File IDs and the recorded prerequisite graph are unchanged.
Units 04–41 now have concrete openings throughout that consecutive range;
this is not certification of complete semantic teaching coverage.

## Corrections

| Unit | Previous issue | Correction and evidence |
|---|---|---|
| 36 | Lean lists described as necessarily duplicate-free; every decision generalized from named operations; Python datum deduplication attributed to token-erased `insertNew` | `RegimeExt` also permits raw duplicate lists. A repeated demand changes length while retaining membership. The named transport statements return related results, not literal equality. Python deduplicates token-aware data; Lean `newDatum` always increments its count. Two items are computed separately. Equal Python values need not be the same allocated object. |
| 38 | Tagged translation described as a proved minimum and a general correspondence; a repeat record likened to another person; all non-reifying modes said to leave the whole state unchanged | The tagged regime is hand-written, with one form and one instance; it proves neither a general translation nor a translation-cost lower bound. Reification creates an occurrence position in this model. Counting changes its counter while preserving its data list. The book supplies an arbitrary-history carrier-bound induction with the native initial-state, mode, and single-token conditions. |
| 38 | Tagged mode said never to enter a symmetric state; the three-position exercise treated a tag-only operation as full symmetry | The declared repeat supplies asymmetry when creating the second occurrence; it does not orient an already symmetric two-occurrence record. `swapState` leaves data fixed and moves tags only. Its fixed-point result on a three-position record does not classify that record's automorphisms. |
| 39 | Silent mode said to change nothing over any history; cheapest route broadened to every price; carrier cap omitted; distinct receipt payloads said literally interchangeable | The inertness theorem restricts admissions to already-present tokens. The search uses two price orders, 44 enabled protocols, six events, and carrier cap 4, including two-token controls. `receipt 1` and `receipt 2` are unequal literal values. Their star links can have the same coarser incoming/outgoing observation; the book checks those claims separately. |
| 40 | Three inhabited profile classes claimed at every stage; `n` confused with number of positions; source profile equality read as an executing generator; later proved correspondence still called OPEN | Stage `n` counts links/steps and has `n+1` positions. Inhabited profile counts at stages 0–3 are 1, 2, 3, 3. The theorem describes the declared family, not an infinite physical execution or object-language runner. Static finite-position marking is distinct from dynamic strategy behavior. The existing Unit 41 interior correspondence is linked as proved. |
| 41 | Title said looking farther does not help; a particular correspondence generalized to an undefined depth hierarchy; off-interior claims dismissed wholesale | On stage 5, pair `(2,3)` agrees at radius 1 and differs at radius 2. The theorem fixes a radius and then permits sufficiently long chains. The book proves the converse arithmetic threshold for two deep points, while retaining the separate earliest-collision question. Only the two defined profiles have the proved interior correspondence; individual boundary equalities may still hold. |

The stage parameter and number of positions are introduced before the
window formulas. Older printed “length” labels explicitly count links.
The payload-forgetting link observation is a book definition, not a new
native `MState` renaming or a proved cross-language bridge. None of these
examples identifies record count with physical object count or derives a
universal law about observation.

## Added book reports

The five book drivers check 99 exact reports. Eight are new:

| Script | Report | Exact library dependencies |
|---|---|---|
| u36 | `repeated_demand_ext` | `propext` |
| u36 | `repeated_demand_counts` | none |
| u36 | `two_new_data` | `propext` |
| u38 | `nonreify_history` | `propext, Quot.sound` |
| u39 | `receipt_payloads_retained` | none |
| u40 | `stage_zero` | `propext, Quot.sound` |
| u41 | `radius_can_help` | `propext, Quot.sound` |
| u41 | `two_deep_need_threshold` | `propext, Quot.sound` |

The history result closes one book teaching gap, not the native hierarchy
question or a translation problem. Native statements, declaration census,
axiom artifact, research results, and receipt populations are unchanged.

Five temporary false propositions and two process-local book substitutions
exercise the boundaries. The [injection record](../../docs/injection_record.md)
records rejection and recovery without changing a native owner or pin.

## Reproduction and limits

Run `python ci/run_gates.py --job textbook` in the pinned local environment.
The PR records the clean source head and receipt. This is the textbook
job, not the twelve-family merge contract; author merge authority remains
unchanged.

This selected review does not certify every paragraph, source anchor,
classification, later theorem, or research lesson. The bounded
protocol and strategy computations keep their original ceilings. Hosted
rendering and novice comprehension, transfer, and retention remain
unverified. The author's positive reading feedback is retained without
assigning a score or changing those evidence limits.
