# Claim ledger: two_sided_commitment

`AuthorityEffect: None`.  Each claim carries exactly one class from the
sealed discipline.  Evidence names a receipt key in
`receipts/two_sided_commitment.json`, a test in `test_two_sided.py`, or
both.  No claim here is a theorem: this tree has no Lean, and says so.

| id | statement | class | evidence | falsifier | what does not follow |
|---|---|---|---|---|---|
| TS-01 | A two-sided standing commitment is a rule on every pair of datum indices, present or future, giving apart, same, or free; it is declared once by one event, emits nothing, and reads no state. | DECLARED_METATHEORY | `two_sided.Commitment`, `Declare`; `CommitmentTests`, `test_declare_is_once` | none; a declaration | that any commitment is derived |
| TS-02 | The demands of a state are the committed pairs among the held data that the state does not honour; they are read off the profiles and nothing emits them. | DERIVED_DEFINITION | `two_sided.demands`; `DemandTests` | a demand not read off a profile | that a demand is an object-language transition |
| TS-03 | Growth is the sealed supply-and-admission of one fresh datum, the only external event after the declaration, taken exactly at demand-free states below the data bound. | DECLARED_METATHEORY | `build_ts_tree`; `test_growth_is_the_sealed_supply_and_admission` | none; a declaration | that growth is derived |
| TS-04 | A response is valid when the augmented state honours the answered pair and regresses no committed pair among the previously held data that the base honoured; pairs involving a fresh datum are new demands, not regress. | DERIVED_DEFINITION | `two_sided.response_valid`; `ValidityTests` | disagreement with the definition on any delta | that another validity would give the same trees |
| TS-05 | The state isomorphism is the sibling's key over the sealed serialization with the apart labels in the separation store and the same labels in the identification store, so automorphisms preserve the stake's labels on held data. | DERIVED_DEFINITION | `two_sided.key_of`; `test_key_respects_the_commitment_labels` | a label-preserving renaming that changes the key | that an index-based stake is renaming-invariant; it is not, and the key says so |
| TS-06 | Under parity and residue_three every run answers same demands and apart demands in one tree, and the grammar carries no event that flips a demand kind. | FINITE_COMPUTATION | `prediction_detail.Q1_runs_with_both_kinds`; `summary.flip_events_in_grammar` | a run answering one kind only | that the sibling's switch is derivable; it is unneeded, which is different |
| TS-07 | 94 accepted responses honour two or more open demands at once. | FINITE_COMPUTATION | `prediction_detail.Q2_edges_honouring_several`; `trees[].edges_honouring_several` | zero such responses | anything about how many a response can honour in general |
| TS-08 | No accepted minimum in any of the 20 trees admits a fresh datum. | FINITE_COMPUTATION | `prediction_detail.Q4_edges_with_fresh_datum` | an accepted minimum with a fresh datum | the same at three items, which was not run (TS-16) |
| TS-09 | Under total_apart, growth from a demand-free state produces at most one demand, and under all three generating stakes some growth step produces none; under total_same no state ever carries a demand and every tree is a chain of growth steps. | FINITE_COMPUTATION, COUNTERMODEL to the per-growth count of n | `trees[].growth`, `prediction_detail.Q3_*`, `Q7_counterexamples` | a growth step under total_apart producing two demands | the sibling's theorem, which is about the viewless state and stands |
| TS-10 | Before the first growth step the reading-L trees under total_apart are the sealed closed baselines node for node; the reading-F trees are not (13 nodes against 20 under mu1, 3 against 4 under mu2). | FINITE_COMPUTATION, COUNTERMODEL | `prediction_detail.Q6_rows`; `sealed_closed_baselines` | equal counts for reading F | that the sealed baseline is wrong; its store is asymmetric by design and this stake is not |
| TS-11 | 154 demands have no valid response within two items, all of them same demands, 152 under residue_three at four or five data and two under parity at three and four data. | FINITE_COMPUTATION | `trees[].refusals`; `prediction_detail.Q5_refusals_at_four_or_more_data` | an apart refusal, or a same refusal answerable within two items | that the refusals persist at three items (TS-16) |
| TS-12 | Under total_apart the mu1 and mu2 trees differ at both readings (230 against 8; 227 against 7); under total_same they agree. | FINITE_COMPUTATION | `prediction_detail.Q8_node_counts` | equal counts under total_apart | anything about the measures beyond these stakes |
| TS-13 | Every node of every tree replays from the sealed genesis through the declaration and the recorded events. | FINITE_COMPUTATION | `summary.all_certified`; `test_genesis_replays_and_certifies` | an uncertified node | that replay proves any mathematical payload |
| TS-14 | At a demand-free state under total_apart at most one held datum has the empty profile, so a fresh datum collapses with at most one held datum and growth generates at most one demand. | CONJECTURE | argument: total_apart honoured means all pairs separated, and two empty profiles would be an equal pair; a fresh datum has the empty profile | a demand-free total_apart state with two viewless data | the count for other stakes |
| TS-15 | Under a no-regress validity a fresh datum is never part of a minimum response within two items: the one instance it can carry mentions it and at most one held datum, and cannot change the relation between two held data except through the third-party effect on one of them, which a held-data instance achieves at one item. | CONJECTURE | finite support: TS-08 | an accepted minimum with a fresh datum at any bound | the same at three items |
| TS-16 | Whether a three-item bound admits a fresh datum into a minimum, or answers the 154 refusals. | OPEN | none; not run | none until run | that the bound is forced |
| TS-17 | Whether the stake can be declared over profiles rather than indices so that it reads what the state can see. | OPEN | none | none | that an index-based stake is illegitimate; it is the sibling pull request's own shape |

## Prediction record

`PREDICTIONS.md` was frozen at sha256
`b9dea8cea62749321422da6b1ba01f76dc1af16624d9e8d5ea44e6338f46e333`
before the first run.  Five of eight hit; Q3, Q6, and Q7 missed, and
each miss is recorded as a finding (TS-09, TS-10).  The scoring is
computed in `run_two_sided.py` and stored under `predictions_scored` and
`prediction_detail`; the prose here restates it and adds nothing.
