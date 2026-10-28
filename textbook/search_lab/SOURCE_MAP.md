# Sources, classifications, and boundaries

AuthorityEffect: None. The lab is outside the seal and consumes these
sources read-only. It adds no derivation event to the frozen experiment.

## Exact source owners

| Teaching operation | Source definitions/results | Classification and reach |
|---|---|---|
| Supply, admission, and a required pair | `code/derivation/model.py`: `Supply`, `AdmitDatum`, `AdmitForm`, `AdmitInst`, `AdmitRuleAll`, `Impose`, `step`, `replay` | Admitted grammar and metatheoretic state representation |
| Positive test answers and separation | `code/derivation/observe.py`: `contexts`, `plug`, `derivable`, `profile`, `separable`, `witness`, `satisfies` | Declared observation semantics; computations in the lab |
| Both seed readings | `code/derivation/engine.py`: `READING_L`, `READING_F`, `GENESIS_L`, `GENESIS_F` | Preserved alternatives; no silent choice between them |
| Candidate population and prices | `code/derivation/candidates.py`: `Bounds`, `iter_full_deltas`, `min_responses`, `mu1`, `mu2`, `response_valid_naive` | Supplied finite candidate space and cost rules; deterministic bounded search |
| Grouping by relabeling | `code/derivation/iso.py`: `canonical`, `canonical_bruteforce`, `find_iso`, `serialize` | Declared isomorphism; explicit mappings and finite cross-checks |
| Continued search and stopping | `code/derivation/engine.py`: `closure_challenge_orbits`, `build_tree` | Supplied pair-separation and external-supply policies; scoped finite graph |
| Export/replay | `code/derivation/export.py`: `tree_full_json`, `verify_full_export`, `regime_sha256`, `dumps_deterministic` | Computational reconstruction and edge certification; no optimality check in this verifier |
| Cost floor over the item grammar | `lean4/Derivation/Minimality.lean`: `cost1_insufficient_general`, `cost1_insufficient`, `cost1_insufficient_F` | Proved theorem under its exact hypotheses; broader than a finite search |
| Nonunique item-count minima | `lean4/Derivation/Minimality.lean`: `mu1_minimum_not_unique`, `U0_not_iso_BL`, `BL_not_iso_BD`, `markK_separable`, `markK_pairwise_noniso` | Proved scoped nonuniqueness and unbounded-arity family |
| Finer-price result | `lean4/Derivation/Minimality.lean`: `mu2_unique`; `lean4/Derivation/MinimalityF.lean`: `mu2_unique_F` | Proved uniqueness up to the source isomorphism under stated validity/arity-sum hypotheses |

The longer treatments remain Part 1 Units 03, 08–09, 17–22, and the source
reference guides for candidates, costs, ties, isomorphism, engine, and
replay. This route prepares their definitions; it does not replace the
formal statements or prove a general Python-to-Lean correspondence.

## Finite populations reproduced by the lab

The two-entry reading L has six minimum raw plans in three classes for
mu1 at item bound two and arity bound two. Mu2 keeps two raw plans in one
class. The default 14-plan table includes all well-formed two-item plans,
including eight failures; it is not merely the optimized search's pruned list.

| Reading | Maximum arity | Well-formed two-item plans | Valid two-item plans | Mu1 minimum classes |
|---|---:|---:|---:|---:|
| L | 1 | 6 | 2 | 1 |
| L | 2 | 14 | 6 | 3 |
| L | 3 | 27 | 14 | 7 |
| F | 1 | 7 | 2 | 1 |
| F | 2 | 20 | 10 | 5 |
| F | 3 | 52 | 36 | 18 |

The exact check recomputes all zero-, one-, and two-item layers in these
six cases. It compares naive validity and independently selected minima
with `min_responses` under both measures. It checks the class partition
against all entry/form bijections and re-verifies each returned map.
Four additional searches vary protection and the item bound on the
three-entry example. Those finite checks do not prove the optimized
algorithm correct for every possible base regime.

## Important distinctions

- An admitted entry's index and its presentation token are different
  parts of the Python representation. Isomorphism excludes token glyphs.
- Arity and ordered argument positions are admitted structure. The
  isomorphism maps entries and forms; it does not freely permute a form's slots.
- Contexts may have more than one hole; the source requires at least one.
  Plugging fills every hole with the same selected entry.
- A failed positive derivability check is absence of derivability under
  the declared rules. It is not independently proved physical negation.
- The admission kernel checks event well-formedness. Search response
  validity separately requires the new demand and all old imposed demands.
  A raw well-formed event can spoil an old requirement.
- Imposed pair protection here is not a license system, normative
  authorization, or the retention interface of another Genesis model.
- In the mu1 API, `(cost, -1)` uses a sentinel in the second position.
  The learner's mu1 price is the item count alone. The sentinel is not a
  negative resource charge. Mu2 uses both components as declared prices.
- `complete_within` records item and arity bounds; it is not a declaration
  that all arities or all future histories were searched.

## Replay and source custody

`reading_L_mu1_rounds5.json` has 128 nodes, 127 creation edges, and three
merge edges. The verifier reconstructs states using the same admission
kernel through a separate path from the search. It checks every edge and
its required map. It does not recompute prices, minimum classes, status
labels, or the whole candidate population. The packet records that changed
cost metadata still passes this replay contract. The lab's separate
source-backed recomputation checks its own full packet and graph.

The source manifest records SHA-256 of decoded UTF-8 source text after LF
newline normalization, with that mode named explicitly. It is not a claim
of byte identity across different checkout line-ending conventions. Every
consumed module's actual loaded path is checked to be inside this repo's
`code/` directory. Neither a hash nor successful replay proves an
unverified theorem, a learner outcome, or an empirical correspondence.
