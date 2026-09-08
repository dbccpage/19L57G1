# Reachable states: what the derived process can build, and what it cannot

AuthorityEffect: None.  Outside the sealed derivation; consumes it read-only.

## The question

Every node of the six exported towers is a state reached from the Challenge 2
close by demand and minimum response under the declared bounds (items ≤ 2,
arity ≤ 2, fifteen rounds, readings L and F, measures `mu1` and `mu2`).  The
sealed record certifies every node's replay and every edge's response.  It
does not say what every reachable state *satisfies*, and it does not name a
state the process *cannot* build.  This tree does both.

## What is proved (`lean/Reachable.lean`, 48 theorems, axioms within `{propext, Quot.sound}`)

A state is **reachable** from a root when it is the root, or follows a
reachable state by one supply (`stepE s .admitDatum`), or by one round: the
sealed `TransStep` (a collapsed target, a valid response, the recorded
successor) whose response is shortest among the valid responses inside the
declared candidate space (`MinResponse`).  Both declared measures order first
by item count, so every response the engine accepts is a `MinResponse`; that
correspondence is checked edge by edge below, not proved.

| invariant | statement | theorem |
|---|---|---|
| (a) rule-free | a reachable state has exactly the root's rules, i.e. none | `reach_rules` |
| (b) well-formed | `Regime.wf` is kept by supplies and rounds | `reach_wf` |
| (c) answered | every standing requirement is separated; at a closure fixpoint every pair of data is separated | `reach_answered`, `reach_fixpoint_separates` |
| (d) forms used | every admitted form carries an instance | `reach_formsUsed` |

(a) rests on the sealed `rule_item_never_minimal`.  (d) rests on a lemma the
sealed tree did not have: appending a form that no instance and no rule names
changes no separability verdict (`separable_appendForm`), so a shortest
response inside the bounds never leaves a form without an instance.

Two well-formed, rule-free states inside the arity bound are then unreachable
from both roots:

| state | why unreachable | theorem |
|---|---|---|
| `⟨2, [1], [], [], [(0, 1)]⟩` — a form admitted without an instance | fails (d) | `formNoInst_unreachable` |
| `⟨2, [1], [(0, [0])], [0], [(0, 1)]⟩` — the unary mark with its form promoted to a rule | fails (a) | `ruledMark_unreachable` |

The first is the answer to "can anything be built": no.  A form is admitted
only as the instrument of a separation, never on its own, so the process
cannot reach a declared-but-unused judgment form, and a rule is never the
shortest way to separate anything.  What the process can build is confined
to rule-free, fully instantiated, fully answered states.

## What is checked (`census.py`, `reachable.json`)

For each of the six exports, in order: the sealed `verify_full_export`; every
node replayed from genesis and compared with its recorded hash; the four
invariants on every node; every supply edge admitting exactly one fresh
datum; every round edge naming a collapsed, fresh target and carrying a
response inside the bounds that the sealed `min_responses`, re-run on the
parent, returns among its minima at the recorded cost; the per-depth class
census from the sealed canonical keys, every node its own class.  The two
unreachable states are compared with every node and their nearest exported
node is recorded with its replay certificate.

Figures as written by `python census.py --write` at the pinned commit:

| total | value |
|---|---|
| nodes replayed and checked | 5240 |
| edges checked | 5498 (4546 rounds, 952 supplies) |
| rounds re-derived as minima at the recorded cost | 4546 of 4546 |
| invariant failures | 0 |
| distinct isomorphism classes over all exports | 3338 |
| closure fixpoints, all answered | 28 |
| unreachable states isomorphic to an exported node | 0 |

## Injection record

Every injection is a mutation in memory over the real exports
(`tree_L_mu2`); nothing under `artifacts/` is written.  A gate is proved by
failing on the defect it exists to catch, naming the injected object, and
recovering on reversal.

| defect injected | injected object | observed failure | reversed |
|---|---|---|---|
| a rule on one exported node | node 17 | `tree_L_mu2 node 17: invariant rule_free fails` (and `answered`, since the rule collapses the marked pair) | no failure |
| one exported response replaced by a non-minimum | edge 3->4 | `tree_L_mu2 edge 3->4: response is not a minimum at the recorded cost`; 911 of 911 rounds re-derived on reversal | no failure |
| a form without an instance on one exported node | node 17 | `tree_L_mu2 node 17: invariant forms_used fails` | no failure |
| one recorded regime hash flipped | node 17 | `tree_L_mu2 node 17: replayed regime hash differs from the record` | no failure |

The unit tests carry one negative test per invariant and per edge check, each
asserting the exact named failure (`tests/test_census.py`).

## Custody

`verify_sources.py --check` pins, at commit
`60c2cb05d91cdfa099017c9cd205b52564db884b`, the seven derivation modules the
census imports (by digest and runtime origin), the whole `lean4/Derivation`
tree the proofs import (by Git tree object), the Lean configuration, and the
six exports with their summaries (by raw digest); it refuses an untracked
`.py` on the import path or `.lean` in the elaborated tree.  `prompt/` and
`paper/` are not pinned: this tree reads neither.

## Running

```powershell
cd research/reachable
python verify.py          # sources, tests, mypy strict, lake build + report census, census --check
```

Regenerate the two records deliberately, never under a live injection:
`python census.py --write`, `python verify_lean.py --write`.

## Not claimed

* Engine refinement.  Orbit selection, the isomorphism quotient and the
  node guards are not formalized; the correspondence between the engine's
  responses and `MinResponse` is a computation over the six exports.
* Anything beyond two-item responses.
* That the four invariants characterize reachability.  They are necessary;
  two states they exclude are exhibited; sufficiency is open.
* Any new challenge kind, and anything about the endogenous generator.

## Files

| file | role |
|---|---|
| `lean/Reachable.lean` | the reachability relation, the four invariants, the two unreachable states |
| `census.py`, `reachable.json` | the census over the six exports and its committed record |
| `verify_sources.py`, `SOURCE_MANIFEST.json` | custody of the consumed sealed inputs |
| `verify_lean.py`, `evidence/lean.json` | the Lean build, report census and reliance record |
| `verify.py` | every check in order, exit non-zero on any failure |
| `tests/` | the census over the real exports, the negative tests, the parser and custody tests |
| `CLAIMS.md` | one `CL-RE-*` entry per claim |
