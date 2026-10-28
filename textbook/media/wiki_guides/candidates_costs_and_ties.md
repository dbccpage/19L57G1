# Candidates, costs, and tied minima

## Declared grammar

A **delta** is a proposed batch of additions. It may introduce a datum,
a form, an instance, or a uniform rule. For example, a new unary form
and one instance can provide a test that separates two previously
collapsed data.

The implementation stores the batch as a canonically sorted tuple of
`NewDatum`, `NewForm(arity)`, `NewInst(form, args)`, or `NewRuleAll(form)`
items. Forms and data introduced in the same delta are available at the
appropriate admission positions.

`delta_events` turns the proposal into an event sequence. Evaluating a
proposal does not execute that sequence or admit the proposed items.

`Bounds(max_items=2, max_arity=2)` declares the default candidate search space. A valid response must separate the requested target and satisfy every prior imposed requirement after replay. The search does not define correctness by an external score.

## Measures

First count the additions. If two successful proposals have the same
item count, `mu1` keeps the tie. `mu2` then compares the sum of the new
forms' arities: fewer total argument slots win among equal item counts.
This second preference is declared separately.

| Measure | Order | Consequence |
| --- | --- | --- |
| `mu1` | Number of admission items | Equally sized successful deltas tie |
| `mu2` | Item count, then sum of new-form arities | Refines the first successful item count by an additional declared criterion |

`min_responses(base, target, measure, bounds)` returns `MinResponses` or `None`. The result carries the measure, attained cost, all minimum deltas, and `complete_within` bounds. `None` means no valid delta was found within those bounds, not that no response can exist outside them.

## Challenge 3: the result and its scope

Both admission readings need two items for the first required separation. Under `mu1` at `Bounds(2, 2)`, the enumeration retains three non-isomorphic classes in L and five in F. Under `mu2`, the bounded computation finds one class in each. The source also supplies stronger, specifically scoped Lean results for some L statements, including an arity-indexed tie family; these do not automatically transfer to every F completeness statement.

The distinction is not cosmetic: [reading-F distinctness](research_f_class_distinctness) proves pairwise non-isomorphism of five representatives, while completeness as all minima remains a separate Lean obligation. A proof of distinctness is not a proof of exhaustive enumeration.

## Search pruning and independent controls

The source names rule-removal, datum-irrelevance, form-irrelevance, and mention lemmas for cost-two pruning. Tests compare pruned enumeration with an unpruned space. The fast observation path requires a rule-free base and refuses a base with rules; general callers must not assume this optimization accepts every regime.

## What a tie does not authorize

Retaining alternatives is different from choosing one. A list position or unique minimum supplies no authorization by itself. The Alpha harness keeps that boundary explicit through a separate host-built License and dispositions for every retained class.

Sources: [candidates.py](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/code/derivation/candidates.py), [challenge report](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/code/derivation/engine.py), [claim ledger](papers_and_claim_ledgers).
