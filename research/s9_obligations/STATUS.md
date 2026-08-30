# STATUS -- S9 obligations run (PROMPT.md steps 29 and 31)

AuthorityEffect: None.  This run proposes; it amends nothing sealed.

| object | id |
|---|---|
| governing prompt, `research/s9_obligations/PROMPT.md` | Git blob `1642e3f6ac746002678e4997f738e0fabd1248c9` |
| snapshot commit | `db1d2b225b577d5212780ff02700efd693c8e446` |
| verification commit at synthesis | the same: `verify_pins.py` re-checked the prompt blob, the five sealed pins, and the sealed prefixes at HEAD |

S9.1, S9.2, S9.3 are the first three bullets of section S9 of
`paper/primitive_difference.md`, numbered by the prompt; the paper's S9 is
an unnumbered list.  Written once, last, by the synthesis pass after P1,
P2, P3, their repair rounds, and the three Lean stages; it reads all three
findings documents, all three receipts, the Lean sources, and
`verify_lean.py`'s inventory, and it verified the parts' reports against
those files rather than copying them.  Repaired twice against the
reviewers' defects on the synthesis pass ("Repair round 1" and "Repair
round 2", with nothing outside the four synthesis files and the named
findings lines changed) and once against full-run audit 1 ("Repair round
3", the last section, which owned every file of the tree and changed
code, tests, two receipts and two Lean modules, as it records).

## Outcome, one line per bullet

* **S9.1 -- narrowed, with the residual written.**  The soundness-transfer
  property is characterized on every type (`transfers_iff_has_falsum_clause`,
  `pure_transfer_above_point_iff_has_falsum_clause`, `transfers_above_point_iff`
  with the above-the-point W identification
  `transfers_above_point_of_entails_reflexive_point_forces_singleton` and,
  under decidable identity on the carrier,
  `transfers_above_point_imp_entails_reflexive_point_forces_singleton`, all
  in `S9Obligations.AxiomLattice`); the lattice of extents is finite
  computation bounded by N = 4 (75 / 37 / 147 extents), and the lattice over
  all carriers as an object is open.  Proposed bullet: `PROPOSED_S9.md`.
* **S9.2 -- discharged with scope.**  Within the declared five-condition
  menu and for candidates on `Bool` with the asserted pair, the classes
  leaving some two-element object initial are decided on every type
  (`admits_primary_exactly`, `admits_secondary_exactly` in
  `S9Obligations.MorphismClasses`); the residual (conditions outside the
  menu; the 576-cell table as an artifact, bounded by N = 4) is written into
  the proposed bullet.
* **S9.3 -- discharged with scope, as a boundary.**  With `TOKEN_DOMAIN` and
  `TOKEN_EQ` admitted, witness-level structure is observable below function
  spaces within the declared vocabularies (the pair `W1`, `W2`, Lean-carried
  in `S9Obligations.WitnessTypes`); what stays invisible is finite
  computation bounded by N = 3 and T = 3 with cell (3, 3) not enumerated;
  the residuals (the list transcription, the sharing-count vocabulary, the
  multiset store) are written into the proposed bullet.
* **F3** changed status under both definitions of transfer; the change is a
  separate, labelled diff in `PROPOSED_S9.md`.

## Terminals

Only terminals from the prompt's legal list are emitted, each with its
scope in the same line (`test_status_terminals_are_legal_and_scoped`).  Not
emitted by anyone: `S9_1_LATTICE_BOUNDED` -- PREFLIGHT.md (step 4) reserved
that terminal for a meet closure that hits the closure-size bound 65536 and
is reported truncated, and no closure did; the carrier bound N = 4, which is
the bound that limits the lattice as an object, is carried by the "bounded
by N = 4" clause of the `S9_1_LATTICE_COMPLETE` line and by the open item
under "What stayed open" -- `S9_1_TRANSFER_OPEN`, and `S9_2_INTERVAL_SHAPE`
(the shape came out the other way in both object classes).  The three Lean stages ran, so the
`LEAN_NOT_CARRIED` with the obstacle "no Lean stage ran" that P3's
`lean_stage_note` reserved for that case is NOT emitted; P1's receipt key
`terminals.lean` holds, since repair round 3, the `LEAN_CARRIED` /
`LEAN_NOT_CARRIED` pair that names the same theorems and residuals as the
per-cell terminals below and P1_FINDINGS.md section 13.5 (before it, the
Python part's superseded `LEAN_NOT_CARRIED` string).

### S9.1 (P1 and its Lean stage)

* `EQ_FRAGMENT_SEPARATED` -- clauses mentioning `x = y` are enumerated as `EQ_BEARING` under their own receipt key with their own lattice and transfer analysis; the only object mixing them with the pure fragment is labelled `MERGED_PURE_AND_EQ_BEARING` and carries the merge sentence in every terminal string of a merged cell.
* `S9_1_LATTICE_COMPLETE` -- the meet closure of the single-clause extents terminated below the closure bound 65536 in every fragment at N = 4 (75 pure, 37 `EQ_BEARING`, 147 merged extents), bounded by N = 4: complete only as the lattice of extents over carriers at most 4, an extent equality there not being an equality at larger carriers; the N = 4 closure restricts injectively onto the N = 3 closure; N = 5 refused by name; `S9_1_LATTICE_BOUNDED` is not emitted because PREFLIGHT.md reserved it for a closure that hits the closure-size bound, which none did, the carrier bound being carried by this line's "bounded by N = 4" clause.
* `S9_1_TRANSFER_CHARACTERIZED` -- six cells (three fragments, two definitions), each bounded by N = 4 for its counts: transfer is containment in the fixed extent W, closure under strengthening and meet is automatic, and the non-definitional content is which extent W is and whether the lattice realizes it (irreflexivity's in every fragment under `TRANSFER_ALL_CARRIERS` and in PURE above the point; the extent of `r x x -> x = y` in `EQ_BEARING` and the merged object above the point, where the transferring set is NOT generated by irreflexivity); the characterization is carried on every type by `transfers_iff_has_falsum_clause` (every fragment under `TRANSFER_ALL_CARRIERS`), by `pure_transfer_above_point_iff_has_falsum_clause` (PURE above the point) and, for the `EQ_BEARING` and merged cells above the point, by `transfers_above_point_iff`, which only unfolds the definition (every model with two distinct points is irreflexive) and says nothing about `r x x -> x = y`, together with the identification of W as that clause's extent, `transfers_above_point_of_entails_reflexive_point_forces_singleton` and `transfers_above_point_imp_entails_reflexive_point_forces_singleton`, the latter under decidable identity on the carrier (every finite carrier has it); the converse without decidable identity is open (S9-1-21 in the ledger).
* `F3_UNTESTED` -- under `TRANSFER_ALL_CARRIERS` (the paper's reading of "sound") in each of the three fragments: the set of axioms that transfer but do not entail irreflexivity is empty by definitional identity, so the conjecture could not fail and was not tested by the sweep (carriers 1..4); `transfers_iff_entails_irrefl` proves on every type that it can never fail under this definition, which is why the terminal stays `F3_UNTESTED`.
* `F3_SUPPORTED_BOUNDED` -- under `TRANSFER_ABOVE_POINT` in PURE: the set is empty by computation, bounded by N = 4, and could not have come out otherwise; on every type the set is empty for pure clause sets by `pure_transfers_above_point_iff_entails_irrefl`, within the pure fragment and this definition of transfer.
* `F3_REFUTED` -- under `TRANSFER_ABOVE_POINT` in `EQ_BEARING` (5 members) and `MERGED_PURE_AND_EQ_BEARING` (6 members, merge sentence): the set is nonempty by construction, listed bounded by N = 4, and `r x x -> x = y` is a countermodel on every type (`reflexive_point_forces_singleton_f3_countermodel_above_point`); every member uses A3's identity atom, so this refutes F3 extended to A3's bill under a soundness weaker than S7's, not F3 as written, and does not touch F3 under the default definition.
* `LEAN_CARRIED` -- S9.1: all seven proposed targets (T1, T2, T3, T4, T6 in two halves, T7) proved, none weakened, six under their proposed names and T2 under the name `non_falsum_clause_set_admits_selfdiff` in place of the proposed `non_falsum_axiom_admits_selfdiff` (same statement; the proposed name embedded the type name `Axiom` of P1_FINDINGS.md section 8, which the Lean stage renamed `ClauseSet` for the reason it recorded in the module docstring of `AxiomLattice.lean`, lines 21-24, and in P1_FINDINGS.md section 13.1 -- a wrapped doc line beginning with the lowercased type name would be the line-leading token the plain-text scan of `verify_lean.py` forbids -- and the theorem's name followed the type's; the docstring above the theorem cites the proved name since repair round 3), plus sixteen further theorems, 23 reports within {propext, Quot.sound}; they carry `S9_1_TRANSFER_CHARACTERIZED` on every type by `transfers_iff_has_falsum_clause`, `pure_transfer_above_point_iff_has_falsum_clause` and `transfers_above_point_iff` with the above-the-point W identification `transfers_above_point_of_entails_reflexive_point_forces_singleton` and `transfers_above_point_imp_entails_reflexive_point_forces_singleton` (the latter under decidable identity), and the three F3 terminals as scoped above.
* `LEAN_NOT_CARRIED` -- S9.1: the lattice of extents as an object (the sizes 75 / 37 / 147, `closure_restriction`, the classifier rows, every lattice membership fact) stays finite computation bounded by N = 4; a syntactic characterization of transfer above the point with the identity atom admitted was neither proposed nor attempted; the converse of the above-the-point W identification without decidable identity is not attempted (the case split on `x = y` is taken as `[DecidableEq alpha]`, which every finite carrier has).
* `REFUSED` -- S9.1: carrier N = 5 refused by name in code (`check_carrier_bound` raises) and prose; nothing at that size was computed, so every S9.1 count stays bounded by N = 4.

### S9.2 (P2 and its Lean stage)

* `S9_2_CLASSES_BOUNDED` -- both object classes: every cell of the 512-cell primary and 64-cell secondary table is finite computation, bounded by object carrier N = 4 (526625 and 24772 objects); initiality quantifies over all objects and the sweep reaches only N; the N = 3 sweep gives the identical table cell for cell.
* `S9_2_CLASSES_CLASSIFIED` -- both object classes: on every type, within the declared five-condition menu and for candidates on `Bool` with the asserted pair, the classes leaving some two-element object initial are exactly {P}, {P,E}, {P,NE} over all pointed structures with an asserted pair and exactly {P}, {P,E}, {P,NE}, {P,I}, {P,E,I}, {P,NE,I} over irreflexive ones (`admits_primary_exactly`, `admits_secondary_exactly`); the verdict of every one of the 576 cells is an instance of a per-class theorem (`initial_P_iff`, `initial_P_E_iff`, `initial_P_NE_iff` for a decidable candidate, `not_initial_P_E_NE`), of a per-cell theorem, or of an exhibited countermodel object, where for the 64 primary cells of {P}, {P,E}, {P,NE}, {P,E,NE} the per-class right-hand side evaluated at the 16 candidates equals the table's verdict by `test_per_class_right_hand_sides_match_the_table_at_the_candidates` (finite computation bounded by N = 4, since repair round 3; a finite inspection in P2_FINDINGS.md section 11 before it), not by a Lean statement; the table as an artifact stays finite computation bounded by N = 4.
* `S9_2_INCOMPARABLE_CLASSES` -- both object classes: the admitting set is not an interval under inclusion (incomparable maximal pairs {P,E}, {P,NE} and {P,E,I}, {P,NE,I}; gap {P,E,NE}; minimal element {P}), a set property computed at N = 4 and bounded by N = 4 as computed, while the admitting sets themselves hold on every type by `admits_primary_exactly` and `admits_secondary_exactly`; no Lean statement of "not an interval" was written.
* `TIES_RETAINED` -- both object classes: primary {P} retains all 8 candidates with a != b; secondary {P} and {P,I} each retain D2 and S2, not pointed-isomorphic (`D2_not_pointed_iso_S2`); the counts are Python quotient sizes under `pointed_isomorphic`, bounded by N = 4, and that every a != b candidate is initial for {P} on every type is `initial_P_iff`.
* `PYTHON_ONLY_SCOPE_DECLARED` -- S9.2: the sweep reproduces S9's fifth bullet for the S9.2 table; its exhaustiveness over every object with carrier at most 4 lives in Python only, bounded by N = 4, and no Lean theorem states that the scope was swept; this names the situation and changes nothing about the fifth bullet.
* `LEAN_CARRIED` -- S9.2: all 15 proposed targets proved under their proposed names, none weakened (target 1 stated for a general pointing so `O10_1010` and `O10_1110` are literal instances; target 10 strengthened to injectivity; target 15 with injective copy inclusions), plus 13 further theorems including the four per-class verdicts and the four class-level statements over all 32 classes; 28 reports within {propext, Quot.sound}.
* `LEAN_NOT_CARRIED` -- S9.2: the receipt's table as an object (576 rows, the first-witness columns, the enumeration order) is read by no Lean statement and stays finite computation bounded by N = 4; the assignment of theorems to the cells of {P}, {P,E}, {P,NE}, {P,E,NE} is checked by a test (the per-class right-hand sides at the 16 candidates against the table, bounded by N = 4) and read by no Lean statement; no per-class "which candidate" theorem over general irreflexive candidates was stated.
* `REFUSED` -- S9.2: object carrier N = 5 refused by name; `morphism_classes.compute(5)` raises, so every S9.2 cell stays bounded by N = 4.

### S9.3 (P3 and its Lean stage)

* `S9_3_ADMISSION_NAMED` -- the admission beyond A2 is `TOKEN_DOMAIN` plus `TOKEN_EQ` (a decidable equality on the token sort, admitted as a primitive), with `TOKEN_NAMES` a separately labelled further admission for `V2_NAMED` only; priced by inclusion of the listed items: outside A1's bill (it adds an identity relation, on the token sort) and not contained in A3's bill (function types, composition, a one-point carrier), which it does not contain either -- incomparable under inclusion, with no ranking claimed (the receipt's `price_vs_A3` and its `S9_3_ADMISSION_NAMED` scope say the same since repair round 3; before it they ranked the bills "strictly less", which no declared order supports); a declaration, not a theorem.
* `S9_3_WITNESS_OBSERVABLE` -- finite computation, bounded by N = 3 (reached at T = 2) and T = 3 (reached at N = 2), cells (2, 2), (2, 3), (3, 2) enumerated whole in both declared spaces and cell (3, 3) not enumerated (its declared space of 117440512 assignments exceeds the per-cell bound 2^20), N = 4 and T = 4 refused by name: in every enumerated space there are pairs identical under every V1 question and separated by some V2_ANON question (390, 6, 100140, 150, 4015170, 16806, in the order N2_T2, N2_T3, N3_T2, witnessed then irreflexive), the first on the two-element irreflexive object being `{t0},{t0}` against `{t0},{t1}`, separated by `share((0,1),(1,0))`, which uses `TOKEN_EQ` on top of `TOKEN_DOMAIN` and nothing else; the Lean half for that pair is `S9_3_sep_V1_indistinguishable`, `S9_3_sep_V2_ANON_separates`, `S9_3_sep_not_isomorphic`.
* `S9_3_WITNESS_INVISIBLE` -- finite computation, bounded by N = 3 (reached at T = 2) and T = 3 (reached at N = 2) with cell (3, 3) not enumerated: V1 with V2_ANON leaves invisible pairs unequal as raw data (108, 9, 22098, 252, 98688, 1584, in the order N2_T2, N2_T3, N3_T2, witnessed then irreflexive) -- token renamings, count magnitudes, and, at T = 3 (cell (2, 3), the only T = 3 cell enumerated; none in any enumerated T = 2 space), 7650 and 18 invisible pairs of non-isomorphic families with equal count vectors (the receipt's `non_isomorphic_count_equal_pair_count` in that cell, witnessed then irreflexive; the isomorphism-class counts there are 696 and 16), every one of which differs in how many tokens two pairs share; under `V2_NAMED` no pair is invisible in any enumerated space, at the cost of separating every token renaming; no equality is claimed; the Lean half for the first count-equal pair is `S9_3_inv_V1_V2_ANON_indistinguishable`, `S9_3_inv_not_isomorphic`.
* `PYTHON_ONLY_SCOPE_DECLARED` -- S9.3: the exhaustiveness of the enumeration (the first-pair rule, every pair count, the split by invariant, the isomorphism-class counts) lives in Python only, bounded by N = 3 and T = 3 with cell (3, 3) not enumerated; the Lean theorems concern the two computed pairs and the carrier-size-2 lists.
* `LEAN_CARRIED` -- S9.3: the eight proposed statements proved under their proposed names with no statement weakened (the general `card` with `cardTwo`, bijectivity spelled as injective and surjective, and a transport route in place of the proposed case split are the differences), plus 24 further theorems including `v1ListReadsCounts` (the "only when" half of step 25 for the carrier-size-2 list, with the token domain `Fin k` for variable `k`; no carrier-general claim) and, since repair round 3, `v1ListNodup` and `v2AnonListNodup`; 32 reports within {propext, Quot.sound}.
* `LEAN_NOT_CARRIED` -- S9.3: the enumeration and its counts are read by no Lean statement; that `v1List` and `v1V2AnonList` equal the Python vocabulary at (2, 2) is checked by no gate (the lengths 22 / 10 / 28 and the absence of repeats in each list are proved, `v1ListLength`, `v2AnonListLength`, `v1V2AnonListLength`, `v1ListNodup`, `v2AnonListNodup`, `v1V2AnonListNodup`; the residual is the transcription itself -- that the entries are the Python questions -- narrowed and not closed); not proposed and not attempted: the token-bijection invariance entries, `V2_NAMED` in any form, the (3, 2) cell, and the refinement order.
* `REFUSED` -- S9.3: N = 4 and T = 4 refused by name; cell (3, 3) refused under the per-cell assignment bound (its irreflexive sub-space of 229376 assignments not enumerated either); the constructions `family_isomorphism_as_question`, `witness_composition`, `presence_quotient_of_carrier`, `sharing_quotient_of_tokens` refused by name in code and prose; every S9.3 count stays bounded by N = 3 and T = 3.

### Run-wide (synthesis pass)

* `MANUAL_RECEIPT_DECLARED` -- this tree's 83 `#print axioms` reports (23 for S9.1, 28 for S9.2, 32 for S9.3) are a manual receipt read by no CI gate; `verify_lean.py` and `verify_pins.py` are run by hand, and a committed report implies no enforcement (see "Manual receipt" below, in the prompt's words).
* `PROPOSED_TEXT_WRITTEN` -- `PROPOSED_S9.md` holds a unified diff against the current text of each of S9.1, S9.2, S9.3, with the residual scope written into each proposed bullet, and a separate F3 diff labelled by the definition it depends on; it is a proposal the author applies or does not, and the sealed paper is not edited by this run.
* `OB1_UNCHANGED` -- OB-1 is out of scope for this run and untouched: no part, no Lean stage, and no synthesis document makes a claim about it.
* `S66_UNCHANGED` -- S6.6 is out of scope for this run and untouched: no part, no Lean stage, and no synthesis document makes a claim about it.
* `S9_LAST_UNCHANGED` -- the S9 last bullet (the inscription bridge) is out of scope for this run and untouched: no diff in `PROPOSED_S9.md` touches its text, and no document makes a claim about it.

## Resource bounds declared (PREFLIGHT.md step 4) and reached

| part | declared | reached | time-outs |
|---|---|---|---|
| P1 (S9.1) | carrier N = 3 required, N = 4 attempted, N = 5 refused by name; closure-size bound 65536 extents | N = 4 completed inside the bound (66066 relations, 431 pattern classes); largest closure 147 extents, no closure hit the bound; N = 5 refused | none (the whole receipt builds in under one second) |
| P2 (S9.2) | object carrier N = 3 required, N = 4 attempted, N = 5 refused by name; candidate carrier 2; at most 8 conditions and 256 classes | N = 4 completed for both object classes (526625 primary and 24772 secondary objects); 5 conditions, 32 classes; N = 5 refused | none |
| P3 (S9.3) | carrier N = 2 required, N = 3 attempted, N = 4 refused; token domain T = 2 required, T = 3 attempted, T = 4 refused; at most 2^20 assignments per (N, T) cell | N = 3 reached at T = 2 and T = 3 reached at N = 2; cells (2, 2), (2, 3), (3, 2) enumerated whole in both spaces; cell (3, 3) not enumerated (117440512 assignments in its declared space, over 2^20); N = 4 and T = 4 refused | none (about ten seconds per receipt build) |
| Lean stages | no carrier bound: theorems quantify over `alpha : Type` (P1, P2) or fix the carrier `Bool` with the token domain `Fin k` (P3) | 23 + 28 + 32 = 83 reports, every one within {propext, Quot.sound} | none |

No part raised a bound; P3 proposed, and did not make, a PREFLIGHT amendment
(a per-space rather than per-cell assignment bound) that would make the
(3, 3) irreflexive sub-space enumerable.

## What stayed open, and why, per part

* **S9.1.**  The lattice of extents over all carriers as an object: no Lean
  theorem describes it and none was proposed (the sweep's sizes are facts
  about carriers at most 4).  A syntactic characterization of transfer above
  the point once the identity atom is admitted (the analogue of T7 for
  `EQ_BEARING`; 10 of 37 and 12 of 147 extents, finite computation bounded
  by N = 4): not proposed, not attempted.  The decidability-free converse of the above-the-point W
  identification: not attempted, the obstacle being that the transfer
  hypothesis yields only "no y differs from x".  A third definition of
  transfer (non-vacuous transfer) was considered and not computed.
* **S9.2.**  Conditions outside the declared five-condition menu are not
  classified.  The table as an artifact and the sweep as a procedure are
  Python-only, bounded by N = 4.  The reading of the per-class iff right-hand
  sides at the sixteen listed candidates is a test since repair round 3
  (`test_per_class_right_hand_sides_match_the_table_at_the_candidates`),
  finite computation bounded by N = 4, and no Lean statement reads the
  table.  No per-class "which candidate" theorem over
  general irreflexive candidates was stated.
* **S9.3.**  Whether a vocabulary with sharing-count comparisons would see
  the count-equal residue, and whether it is below function spaces: no such
  vocabulary was declared.  The Lean lists at carrier 2 are a mechanical
  transcription of the Python vocabulary, compared by no gate.  Multiset
  stores were not computed.  Cell (3, 3), N = 4 and T = 4 are refused.
* **Run-wide.**  The research tree's axiom reports are a manual receipt
  (next section).  The tree is not registered in any CI job (the diff is
  below, as text).

## Manual receipt (step 29)

This tree's axiom reports are a manual receipt.  No CI gate reads them.
Nothing in `.github/workflows` runs `verify_lean.py` or `verify_pins.py`;
`test_no_workflow_step_names_this_tree` in `test_forbidden.py` asserts that
the workflow does not name this tree, so a green run says the reports are
unread and the test must change on the day the tree is registered.  A pass
of `verify_lean.py` is a receipt for the sources present when it ran, on
the machine it ran on, and implies no enforcement.  The same holds for the
sibling research trees' Lean packages (CLAUDE.md gate 11 notes).

## Registration diff (step 31; text only -- `.github/workflows/verify.yml` is not edited)

To add this tree to the `research` job, in the same shape as the existing
`research/blind_restart` and `research/partial_decide` steps, the unified
diff against `.github/workflows/verify.yml` at the snapshot commit (its
289 lines end with the Partial Decide strict-typing step; the five context
lines are lines 285-289 of that file, and
`test_status_registration_diff_is_anchored_to_the_workflow` checks them
against the file line by line):

```diff
--- a/.github/workflows/verify.yml
+++ b/.github/workflows/verify.yml
@@ -285,5 +285,23 @@
       - name: Partial Decide strict typing
         working-directory: research/partial_decide
         run: python -m mypy
         env:
           PYTHONPATH: ${{ github.workspace }}/code
+      # The S9-obligations tree pins the five sealed inputs it reads and the
+      # governing prompt's blob id, and refuses any worktree change under a
+      # sealed prefix. NOT run here, for the same reason as every sibling:
+      # verify_lean.py, which builds the research Lake package. That tree's
+      # 83 axiom reports therefore remain a manual receipt.
+      - name: S9 obligations pins, prompt blob, and sealed prefixes
+        run: python research/s9_obligations/verify_pins.py
+      - name: S9 obligations tests
+        working-directory: research/s9_obligations
+        run: python -m unittest discover -s . -p "test_*.py"
+        env:
+          PYTHONPATH: ${{ github.workspace }}/code
+          PYTHONUTF8: "1"
+      - name: S9 obligations strict typing
+        working-directory: research/s9_obligations
+        run: python -m mypy
+        env:
+          PYTHONPATH: ${{ github.workspace }}/code
```

An earlier version of this section gave the steps as a `yaml` block plus
the prose location "append after the Partial Decide steps"; that was not a
diff, and a reviewer said so.  Registering also means adding the two
commands to the gate-11 block of `CLAUDE.md` and expecting the job to go
red on the census pin that repair round 3 repaired, had it been
registered before that round.
`verify_pins.py` needs no `fetch-depth: 0` and no `PYTHONPATH`: it reads
blobs at HEAD only and imports nothing from `code/`.

## Replay (step 33)

Each runner was run twice by the synthesis pass into two fresh directories
inside the tree (`tmp_syn_replay_a`, `tmp_syn_replay_b`, deleted
afterwards), and the two outputs were compared byte for byte with each
other and with the committed receipt:

| receipt | a == b | a == committed | SHA-256 of the committed file | bytes |
|---|---|---|---|---|
| `receipts/axiom_lattice.json` | yes | yes | `23f4c1b8547139dd1414a18b94ceba2ab473f4d90714f5b51fdec14d4741a363` | 445282 |
| `receipts/morphism_classes.json` | yes | yes | `6f779d207bf3ff1a8815f3521ae4ebcf9dcccdc8a7748b0916c503d9c63471bf` | 538439 |
| `receipts/witness_types.json` | yes | yes | `25a31fb5fe1c82271c8e46ccfe6e93156581acc3ac7964a42c34eca3c2a0b880` | 345705 |

The receipts carry no timestamp, path, or environment datum, and no CR
byte; the parts' own tests re-check the same byte identity in-process.
Repeated by repair round 1 into `tmp_rep_a` / `tmp_rep_b` (deleted
afterwards): the same three hashes, a == b and a == committed for each.
Repeated again by repair round 2 into `tmp_rep2_a` / `tmp_rep2_b` (deleted
afterwards): the same three hashes and byte counts, a == b and a ==
committed for each.  Repeated by repair round 3 into `tmp_rep3_a` /
`tmp_rep3_b` (deleted afterwards) after that round regenerated
`axiom_lattice.json` and `witness_types.json`: the table above holds that
round's hashes and byte counts (before it, `be72bb530aa0ab4cf01bd3a2d1c2cd92cf2a2a4820a81c13119c0b5480316f91` / 443687 and
`71c77fb32cd83d3a8bf42d90c42977b0b1ee729f4351dadd9e7200fb8c476e67` / 342087), a == b and a == committed
for each, and `morphism_classes.json` is unchanged.

## Known defects

None open after repair round 3.  The seven defects full-run audit 1 found
-- the six items this section carried since the synthesis pass and its
repair rounds (the census pin, P1's superseded `terminals.lean` string,
P3's two superseded terminal strings, the `TOKEN_EQ` ranking, the missing
`Nodup` statements, the stale T2 docstring) and the mixed classification of
ledger row S9-2-18 -- are repaired at their roots, each with its
disposition under "Repair round 3" below.  What remains is residual by
declaration, not defect, and is named where it lives: the Lean vocabulary
lists at carrier 2 are a transcription compared with the Python vocabulary
by no gate (ledger row S9-3-15); the tree's axiom reports are a manual
receipt (step 29, "Manual receipt" above); the scanners of
`test_forbidden.py` and of the parts' tests are proxies for the prose rules
of steps 36, 37 and 40 (the injection records below); and the lattice of
extents over all carriers, the syntactic characterization above the point
with the identity atom, and the decidability-free converse, each of which
is open ("What stayed open" above).

## Records of the synthesis pass

* Naming divergence (from PREFLIGHT): PROMPT.md step 3 names
  `SOURCE_MANIFEST.json`; this tree's pin file is `SOURCE_PINS.json`, the
  name of the sibling shape the prompt asks it to follow
  (`research/blind_restart/SOURCE_PINS.json`) and the name the brief gave.
  The content is the manifest the prompt describes: the exact snapshot
  commit, the prompt's blob id, and the SHA-256 of every sealed blob read.
* Consistency edits to `P1_FINDINGS.md`, `P2_FINDINGS.md`,
  `P3_FINDINGS.md`: none in the synthesis pass; three in repair round 1,
  each listed under "Repair round 1" below (the T2 name in P1's section
  13.2 table, the primary-class `S9_2_CLASSES_CLASSIFIED` scope line of
  P2's Lean section, and the `TOKEN_EQ` price paragraph of P3); one in
  repair round 2 (the T2 row of P1's section 13.2 table, whose round-1 note
  wrongly said the rename was unrecorded).  The receipt strings
  that lagged the Lean stages or carried the withdrawn ranking were named
  under "Known defects" until repair round 3 regenerated them; that
  round's edits to the three findings documents are listed under "Repair
  round 3".
* `test_forbidden.py` decisions (its docstring carries them too): step 36's
  mention rule is applied per table row, per list item, and otherwise per
  paragraph, the accepted markers being the brief's three plus "protected
  open(s)" (step 36's own name for the three, so a unit describing the rule
  can name them), with a mention inside a double-quoted span exempt from
  the marker rule only, so that P3's recorded injection sentence can be
  quoted while a quoted claim still fails the claim-pattern rule; step 37's phrase list is the brief's
  three phrases plus their "every type" relatives, applied to rows
  classified finite computation, bounded theorem, or countermodel, and --
  since repair round 1 -- to every sentence of `STATUS.md`, of
  `PROPOSED_S9.md` (its diff fences read as their `+` lines), and, per
  list item, paragraph or table row, of `P2_FINDINGS.md`, each such
  sentence or unit having to name a Lean theorem (any theorem of this
  tree's package or of the sealed `PrimDiff.lean`, a declared proxy: the
  scanner does not check that the named theorem states the general case)
  or to carry one of the declared openness markers ("no Lean theorem",
  "not attempted", "not proposed", "is open", "stays open", "no
  carrier-general claim"; for P2_FINDINGS.md also "bounded", "target",
  "attempt", "propos", "Lean stage", "Lean theorem", "does not promote",
  the markers P1's own scanner uses); P1_FINDINGS.md and P3_FINDINGS.md
  are scanned by their parts' own step-37 tests and not by this one;
  the definition of done's "bounded in the same sentence" rule is
  applied, since repair round 1, to the `+` lines of every diff fence of
  `PROPOSED_S9.md` (`test_proposed_plus_lines_say_bounded_beside_each_computed_result`):
  a sentence that names a computed result -- the words "invisible",
  "hides nothing", "enumerated space", "separated by", "pair count(s)",
  "interval(s)" (added in repair round 2), or a number of two or more
  digits that is not a section, step, line or row cross-reference (the
  declared exemption of repair round 2) -- must contain "bounded" or name
  a Lean theorem, a proxy declared as one; since repair round 2 the same
  scanner runs over the "Outcome" and "What stayed open" sections of
  `STATUS.md`
  (`test_status_outcome_and_open_sections_say_bounded_beside_each_computed_result`)
  and not over its other sections, whose numbers are report counts,
  hashes, line numbers and test tallies rather than computed results;
  step 39
  walks every regular file under the tree except dot-directories (the
  gitignored Lake and mypy build products) and `__pycache__`, scanning all
  102 identifiers including the native subject name; step 40 matches its
  markers in `.md`, `.py`, `.lean` files with the one declared exemption
  for marker lists inside `test_*.py`, and its docstring says the prose
  rule is wider.
* Ledger evidence grammar: `test_<name>` (optionally `test_<module>.`
  prefixed), `<receipt>:<dotted.path>` with `[n]` indexes,
  `S9Obligations.<Module>.<theorem>` (must be in `AXIOM_REPORT_DECLARATIONS`
  and declared in the module), `PrimDiff.<theorem>` (must be a theorem of
  the sealed file).  Every token of every row resolves
  (`test_every_evidence_token_resolves`), and the resolver is shown to
  reject dead tokens.
* The `.mypy_cache/` directory under the tree still holds cache entries for
  reviewers' deleted scratch scripts; it is a gitignored build product,
  skipped by the step-39 walk, and was not touched.
* The words `complete`, `minimal`, `maximal`, `equivalent` appear in this
  document and the ledger only with a scope in the same sentence.

## Injection record of the synthesis pass

Each gate of `test_forbidden.py` was made to fail on the exact defect it
exists to catch, with the failure naming the injected object, and shown to
pass again after the injection was reversed; the injected files were
compared byte for byte with their pre-injection copies afterwards, no
receipt was regenerated while an injection was live, and the sealed
prefixes were clean throughout.  The scanners' in-process probes
(`test_scanners_bite_on_injected_claims_and_stay_quiet_on_denials`,
`test_resolver_rejects_dead_tokens`, `test_phrase_list_bites`,
`test_boundary_regex_matches_the_firewall`, `test_markers_bite_on_injected_text`)
run on every test run; the table below is the live round.

| gate | injection | observed |
|---|---|---|
| step 36, claim on a protected open | a one-sentence claim attaching the verb "narrows" to the protected open OB-1 (spelled here in two pieces so this record does not itself trip the scanner), appended to `STATUS.md` | `test_documents_carry_no_claim_on_a_protected_open` fails naming the sentence; OK after reversal |
| step 36, proposed text touching a protected open's bullet | the sixth S9 bullet's first line, read from the sealed paper, appended to `PROPOSED_S9.md` as a `-` line inside a diff fence | `test_proposed_text_touches_none_of_the_protected_bullets` fails ("unexpectedly found"); OK after reversal |
| step 37, promotion without a theorem | a ledger row classified finite computation asserting its result for the general carrier (the step-37 phrase, spelled here as every-carrier so this record does not trip the prose scanner added in repair round 1) with no Lean token | `test_bounded_rows_with_a_general_phrase_name_a_lean_theorem` fails naming S9-1-99 and the missing theorem; OK after reversal |
| step 30, dead evidence | a ledger row citing a test, a receipt key and a Lean name that do not exist | `test_every_evidence_token_resolves` fails naming all three ("no test def", "has no key 'N9'", "is not in AXIOM_REPORT_DECLARATIONS"); OK after reversal |
| step 39, denylist leak | a probe file `zzz_probe.md` holding one working-denylist identifier read from the JSON at runtime (the eighth, which is the native subject name -- so the scan is stricter than the sealed firewall, as declared) | `test_no_working_denylist_identifier_anywhere_in_the_tree` fails naming `zzz_probe.md` and the token; OK after deletion |
| step 40, external marker | the probe file rewritten to hold a URL scheme | `test_no_external_marker_in_md_py_or_lean_files` fails naming `zzz_probe.md:1` and the marker; OK after deletion |
| step 37 in prose (repair round 1) | a sentence saying that the admitting sets hold for the general carrier "by the two theorems above", with no theorem named (the step-37 phrase spelled every-carrier in this record), appended to `STATUS.md` | `test_prose_sentences_with_a_general_phrase_name_a_lean_theorem` fails naming the sentence; OK after reversal, `STATUS.md` byte-identical to its pre-injection copy (SHA-256 `431707d7c0dbc3588a9905fb6d770fea1fbd29ad576c5f6cf898be6e440f8c8d`, the intermediate copy before this record was added) |
| definition of done on the proposed text (repair round 1) | the `+` line "Naming tokens hides nothing but separates renamings." inserted as the last line of the S9.3 diff of `PROPOSED_S9.md` | `test_proposed_plus_lines_say_bounded_beside_each_computed_result` fails naming the sentence; OK after reversal, `PROPOSED_S9.md` byte-identical to its pre-injection copy (SHA-256 `4f3ec80d1a4f357caa4d1e965f97ab40e1eb635f8fa3eec28f377bb52148c4de`) |
| step 31, registration diff anchoring (repair round 1) | the context line `run: python -m mypy` of the registration diff in `STATUS.md` changed to `run: python -m mypy --strict` | `test_status_registration_diff_is_anchored_to_the_workflow` fails with a list diff naming the drifted line against the workflow's line 287; OK after reversal, byte-identical (the same intermediate SHA-256 as above) |
| definition of done on the STATUS prose (repair round 2) | the list item "* **Probe.**  The syntactic analogue covers 10 of 37 extents at N = 4." inserted as the first item under "What stayed open" in `STATUS.md`.  A first attempt appended the same line at the END of the file, inside the last section, and the test stayed green -- which is the declared scope (two named sections), not a bite, and is recorded so the scope is not mistaken for coverage | `test_status_outcome_and_open_sections_say_bounded_beside_each_computed_result` fails naming the sentence; OK after reversal, `STATUS.md` byte-identical to its pre-injection copy (SHA-256 `c8e96bedcc04758dd8e259684ff34604d97e9bb2e68878869139c113ac8bb475`, the intermediate copy before this record and the round-2 section were added) |
| definition of done on the proposed text, the interval word (repair round 2) | the `+` line "So the admitting sets are not intervals." inserted as the last line of the S9.2 diff of `PROPOSED_S9.md` | `test_proposed_plus_lines_say_bounded_beside_each_computed_result` fails naming the sentence; OK after reversal, `PROPOSED_S9.md` byte-identical to its pre-injection copy (SHA-256 `9f7f4a0e9b6d9eea0a277d1d4190341e9c7554ec961478345b35812b69d5cda7`, the intermediate copy before the S9.2 lines were re-wrapped) |

What injection does not prove: that the phrase lists are the right lists.
A green run says the listed phrasings and markers are absent; the prose
rules of steps 36, 37 and 40 stay a manual check.

## Definition of done (PROMPT.md), item by item

| item | met | pointer |
|---|---|---|
| the axiom space is declared before use, with counts | yes | `CLAIM_LEDGER.md` DEC-01, S9-1-01; `axiom_lattice:axiom_space` |
| the morphism menu is declared before use, with counts | yes | DEC-06, S9-2-01; `morphism_classes:menu_size`, `class_count` |
| the token domain is declared before use | yes | DEC-09, S9-3-18; `witness_types:step21_admission` |
| the three vocabularies are declared before use, with counts | yes | DEC-10, S9-3-01; `witness_types:step22_vocabularies.sizes_by_cell` |
| every claim carries evidence that resolves | yes | `test_every_evidence_token_resolves` (every token of every row) |
| S9.1 ends in exactly one of discharged / narrowed / open | yes: narrowed with the residual written | "Outcome" above; `PROPOSED_S9.md` |
| S9.2 ends in exactly one of discharged / narrowed / open | yes: discharged with scope | "Outcome" above; `PROPOSED_S9.md` |
| S9.3 ends in exactly one of discharged / narrowed / open | yes: discharged with scope, as a boundary | "Outcome" above; `PROPOSED_S9.md` |
| proposed replacement text exists for each bullet touched | yes | `PROPOSED_S9.md` (three diffs plus the labelled F3 diff); `PROPOSED_TEXT_WRITTEN` |
| bounded results say `bounded` in the same sentence as the result | yes | the parts' terminal tests; `test_bounded_rows_say_bounded` (ledger rows); `test_status_bounded_results_name_their_bound` (STATUS terminal lines); `test_proposed_plus_lines_say_bounded_beside_each_computed_result` (the `+` lines of `PROPOSED_S9.md`, added in repair round 1 after a reviewer found the S9.3 bullet's boundary sentence unbounded); `test_status_outcome_and_open_sections_say_bounded_beside_each_computed_result` (the "Outcome" and "What stayed open" sections of this file, added in repair round 2 after a reviewer found an open item naming a count with its bound but not the word) |
| the three protected opens are untouched | yes | `test_documents_carry_no_claim_on_a_protected_open`, `test_every_mention_of_a_protected_open_carries_a_marker`, `test_proposed_text_touches_none_of_the_protected_bullets` |
| the prompt hash is stable | yes | `verify_pins.py` exit 0 at synthesis (blob `1642e3f6ac746002678e4997f738e0fabd1248c9`) |
| the receipts replay byte-identically | yes | "Replay" above |
| tests with `unittest`, strict `mypy` clean (step 34) | yes, since repair round 3 | "Commands and receipts" below: `Ran 191 tests`, `OK`; `Success: no issues found in 14 source files` |
| Lean: no forbidden token, every report within {propext, Quot.sound} (step 28) | yes, as a manual receipt | `verify_lean.py` exit 0, 83 declarations; "Manual receipt" |
| the manual-receipt sentence is in `STATUS.md` in the prompt's words (step 29) | yes | "Manual receipt" above |
| the registration diff is included as text and the workflow is not edited (step 31) | yes | "Registration diff" above; `test_no_workflow_step_names_this_tree` |

## Commands and receipts of the synthesis pass

Run from the repository root unless a `cd` is shown; `PYTHONPATH=../../code
PYTHONUTF8=1` for the tree-local Python commands.

Re-run after repair round 3; the numbers are that run's.

| command | exit | key line |
|---|---|---|
| `cd research/s9_obligations && python -m unittest discover -s . -p "test_*.py"` | 0 | `Ran 191 tests`, `OK` (189 with one failure after repair round 2; the census pin repaired and two tests added in repair round 3) |
| `cd research/s9_obligations && python -m unittest test_forbidden` | 0 | `Ran 38 tests`, `OK` |
| `cd research/s9_obligations && python -m mypy` | 0 | `Success: no issues found in 14 source files` |
| `python research/s9_obligations/verify_pins.py` | 0 | `sealed prefixes clean: prompt paper code lean4/Derivation artifacts`; the exit status read directly, not through a pipe |
| `python research/s9_obligations/verify_lean.py` | 0 | `Lean #print axioms declarations: 83 within ['Quot.sound', 'propext']`; `Lean sources scanned for forbidden tokens: 6`; `lake build (exit 0)`; the log written inside the tree and deleted |
| replay of the three runners twice each (table above) | 0 | byte-identical both ways for all three receipts; temporary directories deleted |
| `git status --porcelain -- prompt paper code lean4/Derivation artifacts` | 0 | empty |
| `git add research/s9_obligations` then `python -m pytest tests/test_primitive_contact.py -q` from the root (step 39, the sealed firewall over the staged tree) | 0 | exit 0; the progress line reports 15 passed and 1 skipped (the skip is the sealed test's own `external contact file not present`, not this tree); the index held the tree's files and nothing else |

## Repair round 1 (reviewers' defects on the synthesis pass)

Ten defects were reported against the synthesis documents.  Each was
re-verified against the sources it named before anything was changed; all
ten are real and are fixed below, and one reviewer's explanation (the
reason for the T2 rename) is recorded as not adopted -- a non-adoption
withdrawn in repair round 2, where the explanation is found to be exactly
what the Lean source records.  Files changed in
this round: `CLAIM_LEDGER.md`, `STATUS.md`, `PROPOSED_S9.md`,
`test_forbidden.py`, and three consistency edits to the findings
documents, each named in its row.  No code, receipt, or Lean file was
changed; the receipts replayed byte-identically after the round.

| # | finding, re-verified | disposition |
|---|---|---|
| 1 | T2 was proposed as `non_falsum_axiom_admits_selfdiff` (P1_FINDINGS.md section 8) and proved as `non_falsum_clause_set_admits_selfdiff`; the `LEAN_CARRIED` line and row S9-1-35 said "proved under their proposed names" | fixed: both name the proved and the proposed name; P1's section 13.2 row for T2 notes the rename.  The reviewer's explanation -- that the proposed name would trip the forbidden-token scan -- is NOT adopted: `verify_lean.FORBIDDEN_TOKENS` matches `axiom` only at the start of a line and `admit` only as a whole word, so the proposed name would not trigger it, and no source records a reason, so none is stated.  WITHDRAWN in repair round 2 (its row 1): the explanation was about the TYPE name `Axiom`, not the theorem name, and the Lean source records it |
| 2 | only `v1V2AnonListNodup` is a theorem; "the absence of repeats are proved" (the S9.3 `LEAN_NOT_CARRIED` line, rows S9-3-01 and S9-3-15) overstated | fixed: narrowed to the 28-entry list, the sublist reading being called prose; NEEDS PART FIX under "Known defects" |
| 3, 4 | the proposed S9.3 bullet stated "hides nothing" and the invisibility boundary without "bounded" in the same sentence, the bound sitting in a later sentence about other subjects; no test read the `+` lines | fixed: the boundary sentence carries the bound, the `TOKEN_NAMES` clause says "in any enumerated space, under the same bound", and the counts sentence is bounded on its own; `test_proposed_plus_lines_say_bounded_beside_each_computed_result` added and shown to bite (injection record); the definition-of-done row names it |
| 5 | step 37 was tested on ledger rows only; `STATUS.md`, `PROPOSED_S9.md`, `P2_FINDINGS.md` had no scanner; `is_lean_token` accepts any Lean token | fixed as a declared proxy: `test_prose_sentences_with_a_general_phrase_name_a_lean_theorem` (sentence level for the synthesis documents, unit level for P2_FINDINGS.md, markers declared in the test's docstring and under "Records"); the `S9_2_INCOMPARABLE_CLASSES` line and the two Outcome paragraphs of `PROPOSED_S9.md` now name their theorems in the sentence; the scanner still does not check that a named theorem states the general case, and says so |
| 6 | row S9-2-18 and the `S9_2_CLASSES_CLASSIFIED` line said "every one of the 576 cells has a Lean theorem for its verdict" while row S9-2-16 and P2's section 11 record a finite inspection for the per-class right-hand sides; the proposed S9.2 bullet dropped `initial_P_NE_iff`'s decidability hypothesis | fixed: both say the verdicts are instances of per-class theorems or exhibited countermodels, with the 64 primary cells of {P}, {P,E}, {P,NE}, {P,E,NE} read by the inspection; the bullet says "no other decidable candidate"; P2's primary-class `S9_2_CLASSES_CLASSIFIED` line carries the same clause |
| 7 | "strictly less than A3's bill" ranks two bills with no declared order; under inclusion of their listed items they are incomparable | fixed: the `S9_3_ADMISSION_NAMED` line, row S9-3-18, the proposed S9.3 bullet, and P3's price paragraph say "not contained in A3's bill, which it does not contain either"; the receipt and code strings are NEEDS PART FIX |
| 8 | the registration section was a `yaml` block plus a prose location, not a diff | fixed: a unified diff with the workflow's lines 285-289 as context, checked line by line by `test_status_registration_diff_is_anchored_to_the_workflow` (injection record) |
| 9 | `S9_1_LATTICE_COMPLETE` is emitted and `S9_1_LATTICE_BOUNDED` is not, with the carrier bound only in the scope clause | fixed by stating the reservation: PREFLIGHT.md reserved `S9_1_LATTICE_BOUNDED` for a closure hitting the closure-size bound; the terminal line, the "Not emitted" sentence, and row S9-1-29 say so, and the carrier bound stays in the "bounded by N = 4" clause.  `S9_1_LATTICE_BOUNDED` is still not emitted, because emitting it for a bound PREFLIGHT did not assign to it would redefine a declared terminal after the computation |
| 10 | the F3 diff said "theorems on every carrier" with the names in the following sentences | fixed: `transfers_iff_entails_irrefl`, `transfers_iff_has_falsum_clause`, `pure_transfers_above_point_iff_entails_irrefl`, `reflexive_point_forces_singleton_f3_countermodel_above_point` are named in that parenthetical |

Not changed by this round: the tree-wide `unittest` run stayed red on the
one pre-existing census pin in `test_verify_pins.py`, which no round of
the synthesis pass owned (repaired in repair round 3).

## Repair round 2 (reviewers' defects on repair round 1)

Ten defects were reported against repair round 1.  Each was re-verified
against the sources it named before anything was changed; all ten are real
(the tenth being the reviewers' accurate re-report of the census pin that
no round of this pass owns), none is rejected, and the first withdraws a
statement round 1 made in five places.  Files changed in this round:
`CLAIM_LEDGER.md`, `STATUS.md`, `PROPOSED_S9.md`, `test_forbidden.py`, and
one consistency edit to `P1_FINDINGS.md` (the T2 row of its section 13.2
table), named in its row.  No code, receipt, or Lean file was changed; the
receipts replayed byte-identically after the round.

| # | finding, re-verified | disposition |
|---|---|---|
| 1 | round 1 said, in five places, that no source records a reason for the T2 rename, on that basis did not adopt the reviewer's explanation, and raised a NEEDS PART FIX item on that premise.  The Lean source records the reason: `AxiomLattice.lean` lines 21-24 (the module docstring) say the type of clause sets is named `ClauseSet`, not the name P1 suggested, so that no line of the file begins with the token the plain-text scan of `verify_lean.py` forbids; P1_FINDINGS.md section 13.1 records the same.  Section 8 proposed the type name `Axiom` (`Axiom.holds`), the proposed theorem name `non_falsum_axiom_admits_selfdiff` embedded it, and the proved name `non_falsum_clause_set_admits_selfdiff` followed the type rename.  Round 1 answered a claim about the THEOREM name when the explanation was about the TYPE name | fixed: row S9-1-35, the S9.1 `LEAN_CARRIED` line, the Known-defects bullet, and P1's section 13.2 row for T2 state the recorded reason; the NEEDS PART FIX item keeps only the stale docstring above the theorem; round 1's introduction and its row 1 carry a visible WITHDRAWN note rather than a silent edit; the "REJECTED (in part)" open issue of round 1 is withdrawn |
| 2, 7 | the proposed S9.2 bullet cited `not_initial_P_E_NE` for an iff whose Lean statement is `admits_primary_iff` and `admits_secondary_iff` (`not_initial_P_E_NE` carries only the E-with-NE part), and wrote "so the admitting sets are not intervals" as a theorem consequence, while rows S9-2-12 and S9-2-19 and the `S9_2_INCOMPARABLE_CLASSES` line classify "not an interval" as finite computation bounded by N = 4 with no Lean statement; `test_proposed_plus_lines_say_bounded_beside_each_computed_result` did not see the word "interval" | fixed on the ledger's side of the disagreement (the reviewers' option b, the conservative one: the non-interval shape is stated by no Lean theorem): the bullet cites `admits_primary_iff` and `admits_secondary_iff`, keeps `not_initial_P_E_NE` for the E-with-NE exclusion only, and says the non-interval shape is a set property read off the two exact lists, finite computation bounded by N = 4 as computed, which no Lean theorem states; "interval(s)" is a `RESULT_MARKER` word and the scanner is shown to bite on it (injection record) |
| 3, 8 | the `S9_3_WITNESS_INVISIBLE` line said "7650 and 18 non-isomorphic families with equal count vectors"; the receipt keys those numbers come from count invisible PAIRS (`summary.N2_T3/<space>.invisible_in_V1_V2_ANON_non_isomorphic_count_equal`, equal to `non_isomorphic_count_equal_pair_count` in the cell), the isomorphism-class counts in those spaces being 696 and 16, so "7650 families" named a number under no receipt key; the two six-tuples of the `S9_3_WITNESS_OBSERVABLE` and `S9_3_WITNESS_INVISIBLE` lines carried no order | fixed: "7650 and 18 invisible pairs of non-isomorphic families with equal count vectors", with the receipt key and the class counts named in the line, and "in the order N2_T2, N2_T3, N3_T2, witnessed then irreflexive" after each six-tuple |
| 4 | the Known-defects list recorded P3's superseded `PYTHON_ONLY_SCOPE_DECLARED` string but not the `S9_3_WITNESS_OBSERVABLE` scope string (`witness_types:terminals[1].scope`), which ends "Lean statements proposed, not proved" and is cited through `witness_types:terminals` by rows S9-3-19, S9-3-20 and PRE-09 to PRE-11 without the divergence being flagged | fixed: the bullet names both strings (and P3_FINDINGS.md's own Python-part terminal record, which carries the same clause); row S9-3-19 names the superseded clause and cites `witness_types:terminals[1].scope`, the way row S9-3-18 names `price_vs_A3` |
| 5 | row S9-2-05 used the step-37 phrase for the doubled object, whereas `two_copies_not_unique` and `two_irrefl_copies_not_unique` fix the object carrier `Bool x Bool` (`Doubled r0`) and quantify over the candidate `r0` on `Bool` with its pointing, general in the candidate and not in the type | fixed: the row says "for every candidate `r0` on `Bool` with its asserted pair, the doubled object on the fixed carrier `Bool x Bool` exhibits two distinct maps preserving edges and non-edges (injective ones when the candidate is irreflexive) -- general in the candidate, not in the object carrier" and names both theorems |
| 6 | the `S9_1_TRANSFER_CHARACTERIZED` line and row S9-1-30 attributed the identification of W (the extent of `r x x -> x = y` in `EQ_BEARING` and the merged object above the point) to `transfers_above_point_iff`, which only unfolds `TransfersAbovePoint` (every model with two distinct points is irreflexive), and omitted that `transfers_above_point_imp_entails_reflexive_point_forces_singleton` assumes decidable identity on the carrier | fixed: both name `transfers_above_point_of_entails_reflexive_point_forces_singleton` and `transfers_above_point_imp_entails_reflexive_point_forces_singleton` for those cells, say the latter assumes decidable identity (every finite carrier has it), and point to the open converse (S9-1-21); the two Outcome paragraphs, the S9.1 `LEAN_CARRIED` line and row S9-1-35 name the same two theorems; row S9-1-30's evidence gains both tokens |
| 9 | the S9.1 item under "What stayed open" stated a computed count with its bound but without the word "bounded" in that sentence, and no test read that section | fixed: "10 of 37 and 12 of 147 extents, finite computation bounded by N = 4"; `test_status_outcome_and_open_sections_say_bounded_beside_each_computed_result` added over the "Outcome" and "What stayed open" sections of this file, with section, step, line and row numbers blanked first as cross-references (`CROSS_REFERENCE`, a declared exemption, so that "section 11" is not read as a result), and shown to bite (injection record); "the 16 listed candidates" in the S9.2 item is written "sixteen" so the proxy does not read a candidate count as a result |
| 10 | the tree-wide `unittest` run exits 1 on the census pin at `test_verify_pins.py` line 225, accurately reported by round 1 and outside this pass's ownership | not changed: recorded under "Known defects" with the one-line repair; the definition-of-done row and the commands table say so; the run is now 189 tests with that one failure |

Not changed by this round: the tree-wide `unittest` run stayed red on that
one pre-existing census pin, which no round of the synthesis pass owned,
and `ok` was reported false for that reason alone (repaired in repair
round 3).

## Repair round 3 (full-run audit 1)

The first full-run audit of the tree (eleven checks; ten passed and check
4, the tree-wide `unittest` run, failed on the census pin) reported seven
defects.  Each was re-verified against the sources it named before
anything was changed; all seven are real, none is rejected, and each is
fixed at its root -- in code, tests, receipts, Lean, findings, ledger,
status and proposed text together -- rather than by weakening a test or
deleting an evidence check.  Files changed in this round:
`test_verify_pins.py`, `witness_types.py`, `test_witness_types.py`,
`axiom_lattice.py`, `test_axiom_lattice.py`, `test_morphism_classes.py`,
`verify_lean.py`, `lean/S9Obligations/AxiomLattice.lean`,
`lean/S9Obligations/WitnessTypes.lean`,
`lean/S9Obligations/AxiomReport.lean`, `receipts/axiom_lattice.json`,
`receipts/witness_types.json`, `P1_FINDINGS.md` (a new section 14),
`P2_FINDINGS.md`, `P3_FINDINGS.md` (a new last section),
`CLAIM_LEDGER.md`, `PROPOSED_S9.md`, and this file.  `morphism_classes.py`,
its runner and its receipt are unchanged; nothing sealed was written, and
no count, first pair, or Lean target of any part changed.

| # | finding, re-verified | disposition |
|---|---|---|
| 1 | `test_verify_pins.py` pinned the research Lean source census to the empty package's three names while the live census had six; the tree-wide `unittest` run was red on that one test | fixed: the pin is the six-name list (`AxiomLattice.lean`, `AxiomReport.lean`, `MorphismClasses.lean`, `S9Obligations.lean`, `WitnessTypes.lean`, `lakefile.lean`), kept as an explicit pin so that a seventh file goes red until it is registered (injection record below) |
| 2 | `witness_types:step21_admission.TOKEN_EQ.price_vs_A3` and the `S9_3_ADMISSION_NAMED` scope ranked two metatheory bills "strictly less" with no declared order | fixed: both say "not contained in A3's bill, which it does not contain either", incomparable under inclusion of the listed items, no ranking claimed; recorded in the receipt's `revision.round_3` with the wording withdrawn; the receipt regenerated twice and compared; row S9-3-18, the terminal line above, and P3's price paragraph no longer carry the withdrawn wording as live |
| 3 | `witness_types:terminals[1].scope` ended "Lean statements proposed, not proved" and the `PYTHON_ONLY_SCOPE_DECLARED` scope said "no Lean theorem of this part exists", both superseded by the Lean stage | fixed: the strings name the carried theorems (`S9_3_sep_V1_indistinguishable`, `S9_3_sep_V2_ANON_separates`, `S9_3_sep_not_isomorphic`; for the Python-only scope all five names of `LEAN_STAGE_CITED`) with the bound in the same sentence, and `lean_stage_note` records that the stage ran and what stays not carried; `test_terminal_strings_cite_only_audited_lean_theorems` requires every cited name to be an audited report declared with `theorem` (injection record below); rows S9-3-19 and S9-3-21 narrowed |
| 4 | `axiom_lattice:terminals.lean` still held the Python part's `LEAN_NOT_CARRIED` string while 23 theorems existed | fixed: the key is the pair `LEAN_CARRIED` / `LEAN_NOT_CARRIED`, the first naming the ten theorems of the declared tuple `LEAN_CARRIED_THEOREMS` (`test_terminals` requires each to be an audited report declared with `theorem`; injection record below), the second naming the lattice of extents as finite computation bounded by N = 4 and the two items not attempted; the receipt regenerated twice and compared, no count changed; rows S9-1-25 and S9-1-36 cite the pair |
| 5 | the docstring above `non_falsum_clause_set_admits_selfdiff` cited the proposed name `non_falsum_axiom_admits_selfdiff` | fixed: it cites the proved name and points to the module docstring for the rename; `verify_lean.py` re-run, the 23 reports of the module unchanged; the "stale docstring" residual dropped from the S9.1 `LEAN_CARRIED` line, row S9-1-35 and P1's section 13.2 |
| 6 | only `v1V2AnonListNodup` was proved; no statement said `v1List.Nodup` or `v2AnonList.Nodup` | fixed: `v1ListNodup` and `v2AnonListNodup` (both `by decide`, no axioms) added after `v1V2AnonListNodup` in file order, with their report lines and inventory entries at the same position; `verify_lean.py` exit 0, 83 reports within {propext, Quot.sound}; rows S9-3-01, S9-3-15, S9-3-23, PRE-04, PRE-07 and the S9.3 `LEAN_CARRIED`, `LEAN_NOT_CARRIED` and `MANUAL_RECEIPT_DECLARED` lines widened; the transcription residual stays open |
| 7 | row S9-2-18 (proved theorem) asserted that 64 cell verdicts rest on a finite inspection -- two classifications in one row | fixed both ways the audit offered: `test_per_class_right_hand_sides_match_the_table_at_the_candidates` evaluates the four per-class right-hand sides at the 16 primary candidates (and at every member of each class) against the sweep at N = 3 and the committed rows at N = 4, and requires the candidates meeting each right-hand side to be exactly the receipt's initial objects; row S9-2-18 keeps the theorem, and the cell-to-theorem assignment is the new row S9-2-25, finite computation bounded by N = 4, citing that test; row S9-2-16, the two S9.2 terminal lines, the S9.2 open item, P2's section 11 and terminal bullet, and the S9.2 outcome paragraph of `PROPOSED_S9.md` say the same |

Injection record of this round, on the checks it added, in the sealed
tree's sense (a gate is proved by failing on the exact defect it exists to
catch, then recovering; no receipt regenerated while an injection was
live; every injected file compared byte for byte with its pre-injection
copy afterwards):

| gate | injection | observed |
|---|---|---|
| repaired census pin (defect 1) | `lean/ZzzProbe.lean` added, imported by nothing | `test_forbidden_token_scan_names_the_token_and_passes_the_sources` fails with a list diff naming `ZzzProbe.lean`; OK after deletion, the file absent afterwards |
| P3 cited-name resolver (defect 3) | `S9Obligations.WitnessTypes.S9_3_sep_not_isomorphic` removed from `verify_lean.AXIOM_REPORT_DECLARATIONS` in-process | `test_terminal_strings_cite_only_audited_lean_theorems` fails: `'S9Obligations.WitnessTypes.S9_3_sep_not_isomorphic' not found in {...}`; OK after the inventory is restored |
| P1 terminal pair (defect 4) | `S9Obligations.AxiomLattice.transfers_iff_has_falsum_clause` removed from the same inventory in-process | `test_terminals` fails: `'S9Obligations.AxiomLattice.transfers_iff_has_falsum_clause' not found in (...)`; OK after the inventory is restored |
| per-class right-hand sides against the table (defect 7) | the committed row (primary, {P,E}, `O01_0100`) rewritten with `initial` false in `receipts/morphism_classes.json` | `test_per_class_right_hand_sides_match_the_table_at_the_candidates` fails `False != True : ('{P,E}', 'O01_0100')`; the receipt restored byte-identically (SHA-256 `6f779d207bf3ff1a8815f3521ae4ebcf9dcccdc8a7748b0916c503d9c63471bf` before and after) and OK after |

What this round's injections do not prove: that the four checks are the
right checks.  The per-class test evaluates the right-hand sides as this
round transcribed them from the Lean statements; that the transcription
is faithful is read by a person against `MorphismClasses.lean`, not by
a gate.
