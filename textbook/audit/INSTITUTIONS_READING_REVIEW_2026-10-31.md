# Institutions I00–I17: reading and selected scope review

Date: 2026-10-31. AuthorityEffect: None.

## Scope

This reviews the material after Act X in the Wiki: eighteen institution
Units, their introductions and source classifications, selected formal
claims in the four existing research owners, and their eighteen Python
checkers. It is not a fresh proof audit of every theorem in those trees.

All eighteen Units now begin with a short claim and a worked first pass
of 127–168 words. Detailed statements, sources, and classifications are
optional disclosures. Prediction questions have folded answers. Examples
cover answer tables, recoverability, class counts, shared input alignment,
plateaus, target disagreement, residual pairs, scoped policy labels,
probe transcripts, promises, changing views, and aligned guard codes.
The I02 example is moved forward rather than duplicated. The Part 2
entry links the existing beginner routes; its dependency graph is described
as a recorded map rather than a certificate of complete preparation.

The review starts from main `45bb09864f9b52ed5ecf66e977ca81f0ed623de7`,
after author merges of #293 and #294. At this review's first publication,
the previous worktree's unfinished Part 1 checks remained separate.
The subsequent [Units 57–61 follow-up](REPLAY_READING_REVIEW_2026-10-31.md)
validates and includes those book additions; the original worktree is
preserved.

## Findings and corrections

| Unit | Issue | Correction and source |
|---|---|---|
| I04 | Minimum-size wording omitted the nonempty-family hypothesis, despite the later proof stating it | `Exceeds D [] q` holds for constant questions. Opening and conclusion now scope the three-distinct-data/two-member minimum to nonempty families. `Inst.exceeds_nil_iff`, `exceeds_two_members`, and `exceeds_three_data` state the exact cases. |
| I05 | The fiber condition was reversed; identity was called the only case requiring injectivity | `FiberConstant D f q` says `f x = f y` implies `q x = q y`, not the reverse. A constant observed answer can be sharp through a varying correspondence. Any injective observed presentation, including a nonidentity one, forces an observing correspondence to separate its inputs. The source explicitly proves the identity case. |
| I07 | The title suggested permanent stabilization | The finite theorem locates a stationary step. The counts `1,1,2,3` show a plateau followed by later growth on a fixed carrier. The title and first pass now say a stationary step. |
| I08 | Target admission was described as sufficient for an arbitrary claim and its agreement question; admission was also made necessary for knowing agreement | `truth_from_admitted_target` additionally assumes agreement; `agreement_known_of_admitted` additionally assumes the claim is known. Admission does not create agreement. Conversely, the empty family knows the constant agreement of identity with itself without knowing identity. Repeated partitions are distinguished from a statistical independence calculation. |
| I09 | Removing a selected residual was liable to be read as clearing the entire residual list | The added indicator clears 0/2 but leaves 1/3 and 3/1. The theorem and introduction name one chosen residual pair. |
| I10 | A counterexample was stated as every report failing alone; a summary table reversed the direction of the target theorem | Constant reports are known by every family. The same nonconstant report can be grounded under one family and not another. Agreement is not inferred from authorization, even with an admitted target. The table now gives the actual hypothesis/conclusion direction. |
| I12 | The type `D → D` was used although `D` is a list, not a Lean type | `pQ D [q]` has type `Nat → Nat`, read on the supplied carrier. Probe examples distinguish a partition from its arbitrary numeric labels. |
| I17 | Wrong sealed field names and incorrect descriptions of quiescence and obstruction; a divergent copied Python transition | Correct field names are `gateBudget`, `gateLicense`, and `certRefusal`. Refusal records do not meet an unseparated requirement; budget/licence gate execution rather than structural repair-menu exhaustion. The checker now calls the existing `derivation.represented` and `derivation.completion` owners. |

The I17 copy counted refusal as resolution, checked mark positions by
token membership, appended rather than prepended marks, suppressed
duplicate marks even when acceptance was disabled, and used a one-item
genesis instead of the empty sealed genesis. Its old samples did not
expose those differences. Added examples use arbitrary token values,
refused but unseparated requirements, relaxed duplicate marks, and the
empty genesis. The acceptance-code mismatch case is now executed, and
the finite deduplication sample is no longer described as all events.
The aligned case remains a defining equality, not an independent
empirical confirmation of an interpreter bridge.

I11's worked introduction separates the policy label unresolved from
literal equality. I13–I15 distinguish pair-query acquisition from Boolean
representation capacity, and exactly from at most in the promise.
I16 separates modifying an old view from extending a family of views.
No blanket theorem about minds, organizations, empirical truth, or
real-world authorization follows from these mathematical definitions.

## Checks and evidence limits

Six existing unit checkers gain focused finite scope cases. Their
existing exhaustive/sample bounds remain as documented in each script;
the added fixtures are examples, not general theorem replacements.
Eight process-local negative substitutions are rejected, with recovery
under original bindings: empty-family suppression, reversed fibers,
suppressed post-plateau growth, arbitrary knowledge from target admission,
clearing all residuals with one separator, refusal-as-resolution,
token-based position checking, and reversed mark order. See the
[injection record](../../docs/injection_record.md).

The PR records a local textbook-job receipt and separate prose/firewall
results at the committed source revision. That job is not the full
twelve-family merge contract. The PR remains draft for author review.
Sealed sources, research source/results/receipts, historical inventories,
and the fixed watchlist/identifier populations are unchanged.

These edits improve entry points and selected semantic boundaries.
Hosted layout, independent novice comprehension, transfer, retention,
and exhaustive semantic coverage remain unverified. The author's positive
reading feedback is retained without assigning a score.
