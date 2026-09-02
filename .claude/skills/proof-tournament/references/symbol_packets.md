# Sparse symbol packets

Intermediate calls use stable identifiers and finite fields so that
assumptions, imports, and residuals remain visible.

## Packet vocabulary

| Field | Meaning |
|---|---|
| `id` | stable packet identifier |
| `goal` | target claim identifier |
| `source_revisions` | exact repository, revision, path, and blob identities |
| `write_boundary` | paths the run may change |
| `toolchains` | exact proof and computation toolchains |
| `allowed_axioms` | permitted proof-kernel dependencies |
| `owner` | role or proof cell responsible for this packet |
| `consumers` | downstream packet or theorem identifiers |
| `mutation_specs` | exact adversarial mutations assigned to the packet |
| `level` | dependency/tournament level, starting at zero |
| `parents` | packets consumed by this packet |
| `kind` | `hypothesis`, `construction`, `theorem`, `computation`, `countermodel`, `bridge`, or `terminal` |
| `claim` | exact symbolic statement or typed signature |
| `premises` | already available proved or declared inputs |
| `foundations` | permitted libraries or metatheoretic apparatus, not bridge claims |
| `imports` | unresolved semantic or bridge inputs not derived by the run |
| `new_primitives` | declarations introduced by this route |
| `obligations` | proof obligations still live |
| `falsifiers` | attempted or successful attacks |
| `evidence` | Lean names, Python tests, and receipts |
| `status` | `candidate`, `survives`, `proved`, `computed`, `conditional`, `refuted`, or `open` |
| `residual` | smallest remaining gap or refutation reason |
| `l1` | sparse cost defined below |

The packet's sparse cost is

```text
l1 = |imports| + |new_primitives| + |obligations|
```

This schedules simpler survivors. It never decides truth, authorization,
minimality, or uniqueness.

Each list entry must name one atomic typed declaration or one atomic proof
obligation. Bundling several premises into a prose sentence to lower `l1` is
invalid even when the validator cannot detect the semantic bundle.

The unique level-zero manifest packet records the source and execution
envelope. Foundational libraries belong in `foundations`; putting an
unresolved history-to-sign or representation bridge there is a false packet.

## Context envelope for an intermediate call

Send only:

1. exact source fragments and revision identities needed by the leaf;
2. the current packet and its direct parents;
3. counterexamples already found against its strategy family;
4. the required output packet shape;
5. a time/token bound and stop condition.

Do not send the intended winner or a narrative urging one conclusion.

## Status rules

- `proved` requires Lean evidence and no unresolved import.
- `computed` requires Python evidence and a receipt.
- `conditional` requires Lean evidence and at least one explicit import.
- `refuted` requires a falsifier and machine evidence.
- `open` requires a nonempty residual.
- A terminal packet cannot say `proved` while any ancestor import remains
  unconsumed.

The validator enforces the local packet rules. Integration still requires a
separate dependency and ancestry audit; validation is not a proof.
