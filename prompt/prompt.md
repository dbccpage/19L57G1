# 19L57G1

## INPUT

```text
<>
```

The whole inscription is initially uninterpreted. Do not inherit ordinary meanings for either mark. Do not decompose it unless a later proof requires that move.

## TASK

Starting only from the input, construct the least finite formal system you can justify.

At every stage:

1. separate what was supplied, declared, derived, optional, refuted, or still open;
2. state what does not follow;
3. prove every claimed necessity and every claimed minimality;
4. retain all non-isomorphic tied continuations;
5. stop when no continuation is justified.

Do not target or name a known theory during the derivation. A static result, termination, branching, impossibility, or countermodel is valid. Known mathematics may be discussed only in a final, clearly separated comparison.

Use only this repository. Do not read outside it, use the network for research, load prior project instructions, or ask the user for direction. Keep this file byte-identical.

## WORK

First create `CLAUDE.md` containing only the execution plan, repository boundary, assumption discipline, proof gates, and stop conditions. Commit it before substantive work.

Create:

```text
code/
tests/
lean4/
paper/paper.md
paper/paper_change_log.md
paper/paper_claim_ledger.md
```

### Python

Implement every finite construction, enumeration, branch, witness, replay rule, and countermodel used by the paper. The implementation must be deterministic and typed. All tests must pass with at least 95% line coverage and 95% branch coverage over project Python code.

### Lean 4

Formalize the substantive mathematical claims and countermodels. `lake build` must pass. Do not use `sorry`, `admit`, custom `axiom`, `unsafe`, or `partial`. Include `#print axioms` for every exported theorem cited by the paper.

### Paper

`paper.md` must present definitions in dependency order, proofs, branches, countermodels, computational evidence, limitations, and the final post-hoc comparison.

`paper_change_log.md` must record every material change.

`paper_claim_ledger.md` must give every claim a stable ID, exact statement, status, dependencies, Python evidence, Lean evidence, axiom report, and falsifier or surviving boundary.

## DONE

Finish only when:

1. every introduced notion has a recorded source;
2. every theorem-level claim has a valid Lean proof;
3. every computational claim has deterministic Python evidence;
4. tied minimum branches are retained unless their elimination is proved;
5. Python coverage meets both 95% thresholds;
6. Lean builds without forbidden escapes;
7. the repository is clean and all intentional artifacts are committed;
8. the paper states the strongest defensible terminal result.
