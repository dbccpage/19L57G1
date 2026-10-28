# The Genesis Textbook, part 2: actors and institutions

AuthorityEffect: None. This part teaches two research trees that sit outside
the seal, and the sealed definitions they build on. Nothing here is an input
to `prompt/`, `paper/`, `code/`, `lean4/Derivation/` or `artifacts/`, and
nothing here changes them or the research trees. Where a unit and the Lean
disagree, the Lean wins.

Part 1 (`textbook/units/`) teaches the sealed derivation from the mark
forward. This part starts where the sealed `Compression` namespace hands a
*presentation* and a *family of presentations* to the research trees, and
teaches what those trees proved about actors, institutions, information,
knowledge, authorization and the cost of finding out what another actor
can tell apart. It assumes part 1's Units 00 to 02: the mark, the external
constructor, the three layers, and the rule that nothing enters the system
without being derived or admitted at a price.

## Sources

| Code | Where | Revision |
|---|---|---|
| sealed `Compression` | `lean4/Derivation/Compression.lean` | `main` at `b8b3ab431a8f82b110fc5b42d8a6698d733953e6` (2026-10-28) |
| `two_theorems` | `research/two_theorems/lean/ResearchTwoTheorems/` (merged #277) | the same |
| `actor_institution` | `research/actor_institution/` (pull request #284) | the branch of that pull request |

Each unit quotes Lean by file and line; the line numbers are those of the
revision above. Axiom reports are read from each tree's `AxiomReport.lean`
output as pinned in its `TREE_CONTRACT.json`; every theorem quoted in this
part depends on at most `propext` and `Quot.sound`, and a unit says so in
its Sources.

## Status marks

The marks are part 1's (`textbook/README.md`): **admitted**, **derived**,
**verified finite**, **conditional**, **open**. One addition for this part:
**refuted** marks a conjecture that the research tree disproved with a
witness proved in Lean. A refutation is a derived result about a
proposal, and the unit says what replaced the proposal.

**derived** is always relative to the admitted definitions. The
definitions of this part (a presentation is a function, a family is a
list, knowing is factoring through the family's representative) are
chosen, not proved. Each unit names, under **What you need first**, the
admitted definitions its claim depends on, and Unit 00 names the price of
the two that everything else uses.

## Kinds of code

| Label | What it is | Trust |
|---|---|---|
| Lean (Genesis) | Copied from `lean4/Derivation/Compression.lean`. | Checked by Lean's kernel when Genesis builds. The authority. |
| Lean (research) | Copied from a research tree's `lean/`. | Checked by Lean's kernel when that tree's `verify.py --check` runs (`lake build`, then the tree's `AxiomReport.lean` against its contract). Not part of Genesis's build or `artifacts/lean_axioms.txt`. |
| Python (research) | Copied from `research/actor_institution/model.py`. | Tested by that tree's `tests/`. Tied to the Lean by executable checks, never by proof. |
| Gloss | Pseudocode written for this book. | Unchecked. A translation aid only. |

This part writes no Lean of its own. Every theorem it teaches is in a tree
that a verifier builds; the book quotes, it does not prove. Each unit that
makes a computational point has a script in `checks/` that imports the
research tree's own Python. Run it from the repository root:

```
python textbook/institutions/checks/i00_signatures.py
```

A check script is a finite sample or an exhaustive check over a declared
bound, and its docstring says which. It never promotes a result: the mark
of a claim is the mark its Lean earns.

## Notation

A **presentation** is a function `p : Nat → Nat`. The book reads it only on
a **carrier** `D : List Nat`, a finite list of data numbers, and writes it
as the table of its values there: on the carrier `[0, 1, 2]`,
`p1 = (0, 1, 0)` means `p1 0 = 0`, `p1 1 = 1`, `p1 2 = 0`. Two data with
the same value are *merged* by `p`; two with different values are *told
apart* (the Lean says *separated*). A table is the finite object the
system can hold; the function is Lean's (Unit 00, Outside the system).

A **family** is a list of presentations, `Q : List (Nat → Nat)`. The
research trees call a family an *institution* and a presentation read as a
member of one an *actor*. This part uses the trees' words and says, in
Unit 00, exactly what the words are attached to.

The **signature** of a datum under a family is the list of the members'
values at it, in family order. Two data with the same signature are merged
by every member; the family cannot tell them apart.

## The dependency graph

Each unit depends on the units in its row and on nothing later.

| Unit | Needs |
|---|---|
| 00 | part 1 Units 00, 01 (the mark; admitted definitions) |
| 01 | 00 |
| 02 | 00, 01 |
| 03 | 00, 01, 02 |
| 04 | 00, 02, 03 |
| 05 | 02, 04 |
| 06 | 02, 03, 04 |
| 07 | 03 |
| 08 | 02, 03 |
| 09 | 02 |
| 10 | 09 |
| 11 | 02, 09, 10 |
| 12 | 00, 02 |
| 13 | 00, 12 |
| 14 | 12, 13 |
| 15 | 03, 12, 13, 14 |

## Unit template

Part 1's eight sections, in its order: **Claim**, **What you need first**,
**The theorem**, **The proof, step by step**, **The same fact in Python**,
**Outside the system**, **What it shows, and what it does not**,
**Sources**. The Sources table of this part has one extra row, **Ledger**,
naming the claim-ledger row the unit teaches (`TT-nn` in
`research/two_theorems/CLAIMS.md`, `AI-nn` in
`research/actor_institution/CLAIMS.md`).

## Contents

| Unit | Claim | Lean | Status | Written |
|---|---|---|---|---|
| 00 | A presentation, a family, a signature: what an actor and an institution are attached to | `Compression.sigList`, `Compression.SigEq`, `Institution.Institution` | admitted | yes |
| 01 | The family's representative merges exactly the data the family cannot tell apart | `Compression.pQ_exact` | derived | yes |
| 02 | Knowing a claim is factoring through the representative; equivalently, equal signatures force equal values | `Institution.knows_iff_determined` | derived | yes |
| 03 | Information counts signature classes; a known question adds none, an unknown question adds at least one | `Institution.knows_iff_information_eq` | derived | yes |
| 04 | A family knows what no member knows, exactly when every pair the claim tells apart is told apart by some member and every member merges one; three data and two members are the least | `Inst.exceeds_iff`, `Inst.exceeds_three_two_resolution` | derived | yes |
| 05 | Correspondence across members is an admission, and names are not | `Inst.correspondence_matters`, `Inst.knows_rename` | derived | |
| 06 | Degradation: known members are inert, a digest hides the exceeding, a lost member leaves a false consensus | `Inst.aggregate_hides_exceeding`, `Inst.consensus_after_loss` | derived | |
| 07 | A chain of families longer than the carrier has a step at which nothing new is known | `Chain.long_chain_stationary` | derived | |
| 08 | Information is not determination, and determination is not truth; truth costs admitting the target | `Chain.determination_not_truth`, `Chain.truth_from_admitted_target` | derived | |
| 09 | Assert or demur: a demurral carries a witness and names the question that would settle it | `Policy.demur_carries_witness`, `Policy.residual_answerable` | derived | |
| 10 | A rule that authorizes only known claims refuses every residual, and authorization is not correctness | `Policy.scoped_sound_refuses_residual`, `Policy.authorization_not_correctness` | conditional | |
| 11 | "Same" is never supported and "apart" is never refuted; identity is scoped to the family | `Policy.same_never_supported`, `Policy.scoped_identity_not_absolute` | derived | |
| 12 | Probing an actor: the transcript, and why two actors that answer alike are the same to the prober | `Acquisition.run_congr` | admitted, derived | |
| 13 | Below `n(n−1)/2` probes some pair is never asked, and an actor that merges it has the same transcript | `Acquisition.lower_bound`, `Acquisition.transcripts_identical_capabilities_differ` | derived | |
| 14 | The complete table is sharp for every actor, so the cost is exact | `Acquisition.acquisition_cost_exact` | derived | |
| 15 | An evaluator sharp for every consistent actor fixes one partition; the promised-count conjecture is refuted | `Acquisition.acquires_implies_fixes`, `Acquisition.exact_promise_zero_probes_two` | derived, refuted, open | |

The order follows the dependency graph. The units marked unwritten are
planned; their claims and Lean names are fixed by the research trees'
ledgers, so a later session continues from the first unwritten row.
