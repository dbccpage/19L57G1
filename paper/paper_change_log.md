# Change log

Material changes only, newest last.

## 1. 2026-08-11 — Repository scaffold and plan

`CLAUDE.md` (execution plan, boundary, discipline, gates, stop conditions)
committed before substantive work.  Prompt inputs carried byte-identically
(SHA-256 recorded in `paper.md` section 1).

## 2. 2026-08-11 — Canonicalization defect found and fixed pre-publication

The first canonical-form implementation permuted color-class members *in
place* instead of assigning them to color-ordered positions, so the
canonical key was not isomorphism-invariant: the two unary marks (and the
paired binary variants) failed to merge, reporting 6 Challenge 3 classes
in reading L instead of 3.  Caught by the first smoke run against the hand
analysis; fixed in `code/derivation/iso.py` (`_class_perms`); regression
locked by `test_mark_variants_are_isomorphic` and the brute-force
agreement test.  No published artifact ever contained the wrong counts.

## 3. 2026-08-11 — First full artifact generation

Challenges 0-3 computed for both admission readings; four external-policy
trees and two closed-system baselines exported; byte-determinism verified
by dual runs.

## 4. 2026-08-11 — Caller correction (10 points) applied

1. Blind protocol tightened: the post-hoc comparison with known
   mathematics, originally required as a final section, is withheld
   entirely; a blindness sweep confirms no external-theory terminology
   anywhere outside the read-only seed prompt.
2. Every minimality claim now states candidate bounds, cost measure, and
   whether uniqueness is absolute or bounds-relative (paper section 7;
   ledger entries CL-3-*).
3. `CL-UNBOUNDED-WITH-SUPPLY` renamed to
   `CL-REACHES-REQUESTED-DEPTH-WITH-SUPPLY`: reaching a finite requested
   depth does not prove unboundedness; the unboundedness statement is
   downgraded to a conjecture supported by the progress theorem.
4. Termination evidence corrected: `any terminal node` replaced by
   per-branch reports (terminal / open / budget-cutoff / round-cutoff
   branches, plus an every-maximal-branch-terminates flag) in
   `CL-BRANCH-REPORTS` and `CL-ENDOGENOUS-TERMINATION`.  A related
   engine defect was found and fixed: a closed-system node reaching the
   fixpoint exactly at the round limit had been labeled as round-cut
   (`completed`) rather than terminal; terminal-ness is now checked
   before the round cutoff (`test_closed_system_terminal_at_round_
   boundary`).
5. Fresh-data supply reclassified as an explicitly declared external
   continuation policy (engine docstring, paper sections 3.10, 8.1).
6. `supply=False` runs retained and labeled as the closed-system
   baseline.
7. -9. New research obligation answered (paper section 9): the endogenous
   generator exists (least collapsed pair; token-blind; no fresh data; no
   new goal kind), is implemented deterministically
   (`next_endogenous_challenge`), preserves requirement satisfaction, and
   provably terminates at the all-pairs-separated fixpoint within
   n(n-1)/2 rounds (new Lean lemma `allPairs_length`; closed-system
   baselines terminate in 1 / 3 rounds with every maximal branch
   terminal).  Beyond the fixpoint no endogenous continuation exists: the
   native tower stops; further continuation requires the external policy.
10. Statement classification switched to the eight-way vocabulary
   (declared metatheory / definition / finite computation / theorem /
   bounded theorem / conjecture / counterexample / unresolved) throughout
   the paper and ledger.

Also in this pass: `cost1_insufficient` generalized in Lean to any
form-less, instance-less regime (now absolute over the item grammar and
instantiated for both readings); reading-F existence witness
`deltaU0F_valid` added; exported theorem count 42.

## 5. 2026-08-11 — Second caller correction (10 points) applied

1. `wfCtx` strengthened: well-formed contexts now require the slot count
   to equal the form's arity (`c.slots.length = r.forms.getD c.form 0`).
   Affected Lean proofs repaired (separation witnesses, `mark_progress`
   including a new `getD_append_lt` lemma, `separable_of_subrules`); the
   Python context enumeration already produced only arity-length slot
   tuples by construction.
2. Lean is now labeled a token-erased abstraction, never a mirror, and
   the abstraction is proved: `Derivation/Erasure.lean` adds a
   token-aware state with deduplicating admission and the simulation
   theorems `erase_step` / `erase_replay` (a duplicate admission erases
   to a bare supply, a proved no-op).  A first draft of the history-level
   statement was vacuous (`lhs = lhs`); it was caught and replaced by
   the genuine state-threaded statement before any claim cited it.
3. Claim scopes separated explicitly in paper and ledger: reading-L
   minimality Lean-proved; reading-F grammar-wide mu2 uniqueness is
   finite computation; Python class counts carry max_items=2 /
   max_arity=2; the arity-indexed `markK` family is its own theorem.
4. Every unboundedness claim removed (including the former conjecture):
   `mark_progress` is response existence for a supplied demand only;
   behavior beyond the exported depths is unresolved.
5. Claim ID renamed to
   `CL-REACHES-REQUESTED-DEPTH-WITH-EXTERNAL-SUPPLY`.
6. Fresh supply remains the declared external continuation policy;
   no-supply runs remain the closed-system baseline.
7. Termination is reported over all maximal branches (branch reports);
   no claim rests on the existence of one terminal node.
8. The counting laws (`strict_bounded_length`, `no_supply_round_bound`)
   are labeled conditional; the connection of their hypotheses to the
   transition system is recorded as computational and a Lean connection
   theorem as unresolved.
9. `separable_of_subrules` docstring and ledger weakened to exactly what
   is proved (witness transfer under a shrunken final rule set); the
   delta-level pruning corollary is recorded as computationally
   certified.
10. Axiom status stated exactly: no sorry, admit, or custom
   conclusion-producing axioms; standard `propext` and `Quot.sound`
   dependencies remain (44 per-theorem reports).

## 6. 2026-08-11 — Paper suite frozen

`paper.md`, `paper_claim_ledger.md`, and this log written against the
frozen artifacts; final gate run recorded in `paper.md` section 12.
