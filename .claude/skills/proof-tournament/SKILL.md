---
name: proof-tournament
description: Run a sparse, adversarial multi-strategy workflow for difficult theorem programs with several live proof routes or independent obligations. Use for proof discovery and mechanization, not ordinary theorem edits or routine review.
---

# Adversarial proof tournament

AuthorityEffect: None

Use this workflow when a proof problem has at least three genuinely different
strategies or several independent bridge obligations. Do not invoke it merely
to make a small task look larger.

The workflow separates discovery, falsification, mechanization, integration,
and independent verification. Every role emits a sparse symbol packet; prose
is rendered only after the theorem and evidence status is fixed.

## Routing

1. Pin the exact sources, target statement, write boundary, allowed axioms,
   and terminal statuses in a level-zero manifest packet. Every candidate is
   descended from that packet.
2. Generate a diverse candidate set. Choose width from the mathematical
   branching factor; do not use a fixed large tournament by default.
3. Pair every candidate with an adversary. Elimination requires a typed
   counterexample, failed obligation, forbidden import, or stronger surviving
   domination result. Preserve tied non-isomorphic survivors.
4. Before implementation, lock Lean theorem signatures, dependency edges,
   Python mutation specifications, and every remaining hypothesis/import.
5. Assign one proof cell per leaf obligation. A cell is the complete
   constructor/adversary/referee triad, not one role in that triad. Add an
   intermediate manager only for a real dependency cluster.
6. Integrate only compiled or explicitly conditional results. A shared noun,
   source pin, test pass, or majority vote is not a bridge theorem.
7. Run an independent victory audit from clean state. The auditor receives the
   goal and artifacts, not the intended winning argument.

Read [references/workflow.md](references/workflow.md) when planning or running
a tournament. Read [references/symbol_packets.md](references/symbol_packets.md)
when constructing agent prompts or result packets.

Validate packet streams with:

```powershell
python .claude/skills/proof-tournament/scripts/validate_packets.py packets.jsonl
```

## Stopping rule

Stop with one of the following run terminals. Packet files spell the same
statuses in lowercase, as required by the validator:

- `PROVED`: the exact target compiles with no unresolved import packet;
- `CONDITIONAL`: a compiled theorem remains hypothesis-relative;
- `REFUTED`: a typed countermodel or contradiction defeats the target;
- `OPEN`: all surviving routes name their smallest unresolved obligation.

Never convert `CONDITIONAL` or `OPEN` to `PROVED` through prose.
