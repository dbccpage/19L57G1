# Institution foundations: definitions after the first pass

Date: 2026-10-31. AuthorityEffect: None.

This second reading pass covers I00–I03 after their short openings.
It does not revalidate every proof in the institution research trees.

## Reading changes

The four Units keep I00's tables `[0,1,0]` and `[0,1,1]`. Cards A/B/C
explicitly name inputs 0/1/2. Readers follow the same groups through
signatures, representatives, recovery rules and class counts.

Definitions separate the original input, reported answer, representative
input used as a label, and one lookup receiving only that available label.
I02 constructs a successful lookup and names incompatible equations in
the failure case. Selecting a different lookup using original identity
would change the stated task.

I03 writes signatures, removes repetitions, then counts. Last-occurrence
deduplication is separate from I01's first-input representative. Empty
family, empty carrier and repeated entries have different worked outcomes.
Equal counts with different groups demonstrate the importance of keeping
the carrier fixed and appending a table when applying stationarity.

All quoted Lean/Python blocks are preserved. Lean sources and tactic
walkthroughs are folded; short reasoning explanations remain visible.
Six changed-example and transfer tasks extend the existing reading
practice with separate answers. No new lab or research model is added.

## Semantic and scope corrections

| Location | Earlier wording | Correction and source |
|---|---|---|
| I00 | Functions and lists were called the least structure supporting the results | These are supplied definitions; no minimality theorem selects them. |
| I00 | Every theorem in this part was said to require carrier membership | `sigEq_iff_sigList` has no carrier parameter; `pQ_exact` restricts both inputs to D. The earlier logical identity does not enlarge D. |
| I00 | Without shared alignment the family was said to know nothing of the later example | A changed correspondence can change combined groups. It does not generally erase recoverability: `Institution.knows_const` holds for any family and carrier. |
| I01 | The first convention was said to make computation possible rather than selection | It specifies this source's deterministic list search. Other explicit selection rules can also be computable. |
| I01 | A default could be identified with every outside input | Outside inputs can match existing signatures or produce failed searches. Neither case is covered by on-carrier exactness. The numeral 0 does not identify a fallback. |
| I01–I03 | Checks claimed every family of at most two partitions | Their loops enumerate empty, singleton and one ordering of each distinct partition pair, for `1 ≤ n ≤ 4`. They do not enumerate all ordered lists or repeated members. |
| I02 | Its representative criterion could be mistaken for a factoring test on arbitrary labels | g(r)=q(r) is a witness for the first-input representative. General p-output labels need not name representative inputs. |
| I03 | A known claim “adds nothing” | Appending lengthens the family and signatures. Class count and recoverability are invariant. |

Owners read include sealed `Compression.lean`, the early definitions and
knowledge/count statements of `ResearchTwoTheorems/Institution.lean`,
`actor_institution/model.py`, the claim ledger, and the selected
count-versus-determination exhibit in `ResearchActorInstitution/Chain.lean`.
Source files and frozen results and receipts are unchanged.

## Verification reach

The four existing scripts pass: I00 prints three signatures, I01 checks
2,098 pairs, I02 checks 1,905 family/claim cases (1,187 known), and I03
checks 1,905 family/question cases. Only the latter three docstrings
change; their executable bodies and populations remain unchanged.

The new practice uses separately checked, supplied four-input tables.
Checks cover reordered representatives, injective relabelling, lookup
conflict, signature order, repeated reports, equal counts with different
groups, empty inputs and repeated carrier entries. These are concrete
calculations, not new general theorems or a refinement proof.

Exact quote preservation, balanced disclosures and code fences are
checked separately. The PR records clean-head textbook, fixed vocabulary
and selective Wiki publication receipts. No new gate, pin population or
negative-injection mechanism is introduced. The twelve-family merge
contract remains separate.

## Remaining work

This is a four-Unit reading pass, not comprehensive semantic review of
I00–I17 or the 75 Part 1 Units. Further dense passages, research integration,
full layout/accessibility inspection and observed beginner comprehension,
transfer and retention remain open. The author's positive reading
feedback supplies no measured novice score. New table rows contain no
physical observations.
