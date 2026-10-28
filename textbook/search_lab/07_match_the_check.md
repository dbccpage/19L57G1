# 07. Match the check to the claim

[Previous](06_replay_the_result.md) · [Search lab](README.md) · [Practice](PRACTICE.md)

## A deliberately misleading price

Take a separate in-memory copy of the export. Change the first edge's
recorded price to `(999, 999)` without changing any of its events.

**Predict:** must the replay verifier reject it?

It accepts that copy. Its job is to check reconstructed states and edge
maps. It does not recompute the price field. The changed price is false
under the lab's mu1 rule, even though its event replay still works.

## Ask what was checked

| Claim | Evidence used in this lab |
|---|---|
| These events reconstruct these states | `verify_full_export`, including every merge map |
| These plans are the cheapest inside these bounds | Unpruned enumeration, naive response checks, explicit price comparison, agreement with `min_responses` |
| These results agree up to the declared relabeling | Explicit `find_iso` maps, plus brute-force comparison of the small class partition |
| No zero/one-item plan can work over the stated grammar | The separate Lean cost-floor theorem, under its hypotheses |
| A novice understands and can reuse this reasoning | A new task with the reader's own explanation; still to be tested |
| A real device has these observation properties | A separately declared and tested measurement correspondence; not supplied here |

Each row asks for evidence fitted to that claim. One successful check
cannot take on all of the other rows' jobs.

## A real-world question to investigate

Suppose a recorder is used to distinguish packages that must be sent to
different destinations. Before changing its questions, list which
distinctions the task requires. Give candidate changes and their actual
costs. Measure whether the recorder preserves the required distinctions.

The lab suggests a way to organize that investigation. The packages,
device behavior, costs, and reliability would need their own evidence.
The formal two-entry result does not supply those measurements.

## Your turn

Explain to someone else why “the export replays” and “the export's cost
annotation is correct” are different claims. Name the check you would
perform for each. Then give one assumption that would need checking before
applying the lesson to a physical recorder.

AuthorityEffect: None. The changed-cost example tests the verifier's actual
scope; it is not a defect in its documented replay contract.
