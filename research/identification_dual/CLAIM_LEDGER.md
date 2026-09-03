# Claim ledger: identification_dual

`AuthorityEffect: None`.  Each claim carries exactly one class from the
sealed discipline: DECLARED_METATHEORY, EXTERNALLY_IMPOSED_CHALLENGE,
DERIVED_DEFINITION, FINITE_COMPUTATION, COUNTERMODEL, CONJECTURE, OPEN.
Evidence names a receipt key in `receipts/identification_dual.json`, a
test in `test_dual.py`, or both.  No claim here is a theorem: this tree
has no Lean, and says so.

| id | statement | class | evidence | falsifier | what does not follow |
|---|---|---|---|---|---|
| ID-01 | RequireSame(i, j) is an externally imposed requirement: two data separable in the sealed declared sense must reach equal profiles; it is persistent and recorded as a declared event. | EXTERNALLY_IMPOSED_CHALLENGE | `dual.RequireSame`; `EventTests` | none; a declaration | that anything inside the object language asks for it |
| ID-02 | Retract and Switch are declared metatheory: one event each, replayable, deriving nothing. | DECLARED_METATHEORY | `dual.Retract`, `dual.Switch`; `test_switch_retracts_both_stores_and_flips` | none; a declaration | that retraction is an object-language transition |
| ID-03 | The genesis states are exactly the iso-distinct terminal nodes of the sealed closed baselines for both readings and both sealed measures: 19 states, 3 from reading L and 16 from reading F, every one replay-certified and all-pairs-separated. | FINITE_COMPUTATION | `genesis[]` (`replay_certified`, `sealed_measures`); `GenesisTests` | a genesis state that does not replay or carries a collapsed pair | that these are the only interesting starting states |
| ID-04 | A response is valid when the augmented regime collapses every identification requirement and separates every standing separation requirement; the check is full recomputation by replay. | DERIVED_DEFINITION | `dual.response_valid`; `test_validity_is_full_recomputation` | disagreement with the hand definition on any delta | that a fast path exists; none is used |
| ID-05 | The state isomorphism is the sealed serialization minimised over every datum bijection and every arity-and-rule-preserving form bijection, paired with the mapped identification store and the mode. | DERIVED_DEFINITION | `dual.state_key`; `IsomorphismTests` | a renaming that changes the key, or two stores with one key | that the restriction on form bijections loses an isomorphism (it cannot: any isomorphism preserves arity and rule membership) |
| ID-06 | In reading R the minimum identification response over every genesis state and every separated pair costs one item; the sealed cost floor of two does not dualise. | FINITE_COMPUTATION | `summary.reading_R.costs_attained`; probes `pairs[].min_cost`; `test_minimum_in_reading_r_is_one_item` | a genesis state whose every separated pair needs two items | the general claim (ID-13) |
| ID-07 | Of the 290 accepted minima in reading R, 220 contain a uniform rule; 164 are a rule alone; under both sealed measures the trees agree at every genesis state and no accepted minimum admits a form. | FINITE_COMPUTATION | `summary.reading_R.kinds_census`, `mu1_vs_mu2` | any accepted minimum with a fresh form; unequal counts | anything about a reach-weighted measure, which is not run |
| ID-08 | 208 of the 290 accepted minima change the profile of a datum outside the target pair. | FINITE_COMPUTATION, COUNTERMODEL to locality | `summary.reading_R.edges_with_third_party_change`; `edges[].info.third_party_changed` | zero such edges | that the effect is bounded in any way beyond these states |
| ID-09 | In reading R no demand lacks a response within bounds, no tree is cut, and every maximal branch reaches the all-collapsed fixpoint in at most n minus one identification rounds. | FINITE_COMPUTATION | `summary.reading_R.no_response_nodes`, `round_bound_or_guard_nodes`, `branches[]` | a cut branch or a branch of n rounds | the general bound (ID-14) |
| ID-10 | At every reading-R fixpoint, re-separating any collapsed-pair orbit costs exactly two items, every minimum admits a fresh form, and none instantiates a ruled form; 548 orbits priced. | FINITE_COMPUTATION | `summary.reversal` | a cost-one reversal or a minimum on a ruled form | that a saturated form is dead in general (ID-15) |
| ID-11 | In reading P every tree is terminal without a response at its root; every pair carrying a standing separation refuses identification; and some never-required pairs also refuse within two items. | FINITE_COMPUTATION | `summary.reading_P.by_status`; `prediction_detail.P6_clauses`; `test_required_separation_blocks_identification` | a reading-P tree reaching the fixpoint; a required pair with a valid identification | that every never-required pair refuses; most answer |
| ID-12 | In the alternating runs no fresh datum is admitted, the ruled-form count never falls along an edge, forms accumulate above the genesis count, and the ruled-form count does not rise across every identify-to-separate cycle; all 38 runs are guard-cut or round-cut. | FINITE_COMPUTATION | `summary.alternating[]`; `prediction_detail.P8_clauses`; `trees[].branches[]` | a fresh datum; a falling ruled count | anything past the cut |
| ID-13 | Whenever the profiles of i and j differ in exactly one context and no separation requirement stands, one instance identifies them; whenever they differ only on forms none of which carries a standing separation, one rule per such form identifies them. | CONJECTURE | argument: an instance adds exactly its plugged contexts; a rule adds every context of its form to every datum | a state where profiles differ in one context and no one-item response is valid | a bound on how many contexts may differ |
| ID-14 | Under the identify closure policy with no standing separations, the all-collapsed fixpoint is reached within n minus one accepted rounds for n admitted data. | CONJECTURE | argument: equal profiles is an equivalence relation, each accepted round merges at least two classes, and n classes cannot merge more than n minus one times | a run needing n rounds | a bound on cost per round |
| ID-15 | A form on which every context is derivable for every datum (by rule or by saturation) contributes no separation witness, so any re-separation at an all-collapsed state must admit a fresh form. | CONJECTURE | sealed `separable_of_subrules` covers the ruled case; the saturated case is the 548 orbits of ID-10 | a re-separation minimum without a fresh form | the general statement for the saturated case, which has no Lean |
| ID-16 | The reading of RequireSame as internal identity (same index) is not reachable by any sealed admission event; a merge event would be a new primitive. | OPEN | none; the sealed grammar has no merge event | a sealed event that merges two indices | that a merge event should be added |
| ID-17 | A reach-weighted measure that prices a rule by the contexts it grants would separate "adjust the two" from "abolish for everyone"; it is declared, not derived, and not run. | OPEN | none | none until run | that such a measure is forced |

## Prediction record

`PREDICTIONS.md` was frozen at sha256
`b5e066fca1cc262dfbef84db142a647c36d055bd887c0bf2f48084d180424e97`
before the first run.  Eight of ten hit; P6 and P8 missed, each on one
clause of three, and each miss is recorded as a finding (ID-11, ID-12).
The scoring is computed in `run_dual.py` and stored under
`predictions_scored` and `prediction_detail`; the prose here restates it
and adds nothing.
