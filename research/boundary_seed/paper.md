# The boundary derivation

`AuthorityEffect: None`.  A blind derivation from the inscription `<|>`,
carried out inside this repository under the seed
`research/boundary_seed/SEED.md`.  This paper grows one challenge per
session; sections the run has not reached say so.

## 0. The experimental boundary

The seed is read-only, sha256
`ba30bcd600d8232f054f3b4d9a5d03caafaa7442dfd8095643f39cfcea1ad0be`.
The run writes only `research/boundary_seed/` and the append-only
registration of its checks in the research job of the workflow.  Until
`FREEZE.md` exists the run reads nothing of the repository beyond the
seed, the five named sections of the repository contract, and its own
tree; it imports nothing from the sealed kernel and builds its own; and
the scan in `tests/test_blind.py` fails any committed or staged file of
the write root that cites a sealed path, a sealed claim identifier, a
sealed Lean name, the sealed kernel as an import, or another research
tree.

The blindness is by rule and not by ignorance.  The instrument that
opened this run drafted the seed in the same session after reviewing the
sealed derivation and its research trees, and remembers their
vocabulary.  That is declared reading zero of `MANUAL.md`.  Every result
below is derived from the seed and the tree's own code and proofs, and
every place the run noticed itself reaching for a remembered result is
recorded in the challenge's `STATUS.md` next to the result.

## 1. Metatheory and object language

Metatheory is everything used to carry out and check the derivation:
Python, Lean, the tests, the receipts, the readings, presentation
tokens, and this prose.  The object language is what the admitted state
can observe of itself: the contents of a side, and under one reading the
name of a side.  Presentation identity (which token was supplied),
internal identity (which admitted mark, by index), observational
equivalence (equal side profiles), behavioural separation (not yet
declared; Challenge 3), and semantic interpretation (never) are kept
distinct throughout.

Supply, mention, admission, current-state designation, retention,
observation, and equality are distinct events or relations in the
kernel: a `Supply` presents and changes nothing; an `AdmitMark` admits a
presented token on a side; re-admission of an admitted token is a
designation and not a duplication (declared convention); retention is
the placement tuple; observation is the `contents` and `side_profile`
functions; equality of regimes is structural, and equality up to a
permitted renaming is the canonical key.

## 2. The admitted boundary: one declaration, two readings

The one admitted primitive is the boundary with its two sides.  It is
not a datum; it is the frame every datum is placed against.  It is
listed first in every ledger of this tree and is never called free.

Reading U leaves the two sides unnamed.  The exchange of the sides is
then a renaming the object language cannot see, and the isomorphism
relation includes it.  Reading O names the sides `near` and `far`.  The
exchange is then not a renaming, and the isomorphism relation excludes
it.  The two readings are carried as separate towers from genesis; a
result that holds under one and not the other is stated under its
reading in the same sentence.  Two-ness is not assumed of the sides
beyond the declaration itself (declared reading 2 of `MANUAL.md`).

## 3. Definitions, in dependency order

All in `code/boundary/model.py` and `lean/BoundarySeed/Basic.lean`.

1. **Reading.**  `U` or `O`.  Metatheory.
2. **Regime.**  A reading, the admitted marks in admission order
   (tokens, metatheoretic), and for each mark the side it lies on, `0`
   or `1`.  The boundary is implicit and unique.
3. **Genesis.**  The regime with no marks, one per reading.
4. **Events.**  `Supply(token)`, external presentation; `AdmitMark(token,
   side)`, admission of a presented token on a side.  No other event
   kind exists at Challenge 0.
5. **Step.**  `Supply` returns the regime unchanged.  `AdmitMark` appends
   the mark and its side, unless the token is already admitted, in which
   case it returns the regime unchanged.  A side other than `0` or `1`
   is refused.
6. **Replay and certification.**  A history replays from a base by
   folding `step`; a claimed regime is certified when it equals the
   replay of its history.
7. **Contents.**  The set of internal identities of the marks on a side.
8. **Side profile.**  Under U, the contents; under O, the name and the
   contents.  This is everything the object language can observe of a
   side.
9. **Collapsed sides.**  Equal side profiles.
10. **Observation relation.**  The set of pairs (mark, side).  It is
    positive: it lists what is placed and has no negative or counting
    form.
11. **Reflection.**  The exchange of the two sides.
12. **Mark renaming.**  A permutation of internal identities; tokens
    travel with their marks.
13. **Serialization.**  The reading and the placement, tokens forgotten.
14. **Canonical key.**  The minimum serialization over every mark
    renaming and, under U only, the reflection.  Two regimes have equal
    keys exactly when they differ by a renaming their reading permits.
    "Canonical" here means this implemented minimum and nothing more.
15. **Permitted renaming.**  Under U, mark renamings and the reflection;
    under O, mark renamings only.  Definition, not theorem.

## 4. Challenge 0: the initial state `<|>`

Receipt: `receipts/challenge0.json`.  Predictions frozen at sha256
`a03ee8127e83603af75c56c4061bcbe9dc1689c3b56b90854148dfb9856cc395`
before any code or proof was written.

### 4.1 Results under each reading

| result | reading U | reading O | evidence |
|---|---|---|---|
| side profiles at genesis | `[[]]`, `[[]]` | `["near", []]`, `["far", []]` | receipt `readings.*.side_profiles` |
| the two sides collapsed | yes | no, and the difference is the name component only | `sides_collapsed`; Lean `sides_collapsed_at_genesis_U`, `side_names_distinct` |
| observation relation at genesis | empty | empty | `observations`; Lean `no_observation_at_genesis`, `contents_genesis` |
| a supply changes the state | never | never | `supply_leaves_state_unchanged`; Lean `supply_no_op`, `replay_supply_inert` |
| an event follows from the state | no function of the kernel returns an event | same | `state_event_generators = []`; Lean `step_changes_only_by_place` |
| the reflection is a permitted renaming | yes | no | definition 15 |
| the reflection fixes genesis | yes, as a regime and as a renaming | yes as a regime, but it is not a renaming the reading permits | Lean `reflect_genesis`; receipt |
| the reflection is an involution | yes | yes | Lean `reflect_reflect` |
| the reflection moves any placed mark | yes | yes | Lean `reflect_moves_a_mark` |

Under O, that the sides differ at genesis is DEFINITION-level: it is
the two admitted names and nothing else, and the Lean statement is the
inequality of two constructors, closed by `decide`.  Nothing at
Challenge 0 gives the O-distinction content beyond the declaration.

### 4.2 The predictions, scored

| id | label | status | note |
|---|---|---|---|
| C0-1 collapse under U | FORCED | HIT | by definition 8 and 9 once side observation is contents |
| C0-2 distinction under O is bought | FORCED, DEFINITION-level | HIT | the profiles differ in the name component only |
| C0-3 inertia | FORCED | HIT | supply inert under both readings; no state-to-event function in the kernel |
| C0-4 emptiness is not a fact | NOT FORCED, DEFINITION-level | HIT | no observation fires; the observation relation has no negative form; the run admitted no negative observation, which is the choice the prediction hung on |
| C0-5 the reflection | FORCED for genesis | HIT, general clause SHARPENED | see 4.3 |
| C0-X extrapolation | NOT FORCED | PENDING | scored by Challenge 1 |

Five FORCED or DEFINITION-level hits are evidence of the order of the
work, not of insight: the predictions were written before the
definitions, and the definitions were written to the seed, not to the
predictions.  The one prediction that could have gone otherwise is C0-4,
which depended on whether the run would admit a negative observation.
It did not, because the seed admits none.

### 4.3 The reflection census (computation)

Over every hypothetical placement of up to four marks, none of them
admitted:

| marks | placements | fixed by the reflection up to mark renaming | classes under U | classes under O |
|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 |
| 1 | 2 | 0 | 1 | 2 |
| 2 | 4 | 2 | 2 | 3 |
| 3 | 8 | 0 | 2 | 4 |
| 4 | 16 | 6 | 3 | 5 |

The reflection fixes a placement up to mark renaming exactly when the two
sides carry equally many marks, under both readings, for every placement
of up to four marks (`fixed_iff_equal_counts = true`).  Prediction C0-5's
general clause named "every state whose sides carry the same contents";
with contents as sets of internal identities that is only the empty
placement, so the prediction was true and too narrow.  The sharper fact
is recorded as a computation to four marks and is not claimed beyond
that bound.  The class counts show what the readings differ by: under O
the key sees `n + 1` classes for `n` marks (how many lie on `near`);
under U it sees `floor(n/2) + 1` (the unordered split).  Computation to
four marks; the closed forms are a description of the table, not a
theorem.

### 4.4 What Challenge 0 does not establish

- Nothing about a mark's own profile.  Marks have no observable of their
  own at Challenge 0 beyond the side they lie on.
- Nothing about separability of the sides after admission; that is
  C0-X, scored by Challenge 1.
- Nothing about a whole within a side, the outside of the outermost
  boundary, depth, or the boundary's cost.  Those are Challenge 5 and
  the required questions of the seed, not reached.
- The O-distinction is bought.  Whether anything later makes it earn its
  keep is open.

## 5. Challenges 1 to 5

Not yet reached.  Each opens in a fresh session with its own frozen
`PREDICTIONS.md`.

## 6. The autonomous branch procedure

Not yet declared; it is declared after Challenge 3 by the seed's order.

## 7. Proofs and countermodels

Lean package `lean/`, core Lean only, no dependency on any other package
in this repository.  Thirteen theorems, every one with a `#print axioms`
report in `lean/axioms.txt`, checked against a fresh build by
`verify_lean.py`; every report lies within `{propext, Quot.sound}`.

| theorem | statement | axioms |
|---|---|---|
| `supply_no_op` | a supply is a no-op | none |
| `step_changes_only_by_place` | a step that changes the state is a placement | none |
| `genesis_placement_nil` | genesis has no placement | none |
| `no_observation_at_genesis` | no (mark, side) observation fires at genesis | propext |
| `contents_genesis` | both sides have empty contents at genesis | propext, Quot.sound |
| `sides_collapsed_at_genesis_U` | under U the two sides' contents agree at genesis | propext, Quot.sound |
| `side_names_distinct` | under O the two names differ (DEFINITION-level) | none |
| `map_not_not` | double negation of a Boolean list is the identity | propext |
| `reflect_reflect` | the reflection is an involution | propext |
| `reflect_genesis` | the reflection fixes genesis | none |
| `reflect_moves_a_mark` | the reflection moves any placed mark | propext |
| `replay_deterministic` | equal histories replay equally | none |
| `replay_supply_inert` | a history of supplies replays to its base | none |

No countermodel is needed at Challenge 0: no target failed.

## 8. Receipts

- `receipts/challenge0.json`: deterministic (sorted keys, LF, no
  timestamp, no environment value); regenerated byte-identically by
  `run_challenge0.py` and checked by the tests and by the research job.
- Tests: 37, under strict typing; line 98.09%, branch 95.83% over the
  tree's code by `check_coverage.py`.
- `lean/axioms.txt`: 13 reports.
- Injection record: `MANUAL.md`.

## 9. The strongest defensible statement so far

At genesis, under reading U, the two sides of the admitted boundary are
observationally collapsed, the state is inert under supply, no event is
produced by the state, no observation fires, and the exchange of sides is
a renaming the object language cannot see.  Under reading O the same
holds except that the two sides are distinguished, and that distinction
is the two admitted names and nothing else.  Every clause is a Lean
theorem or a definition labelled as such; none is content beyond the
declaration.

## 10. Limitations and open obstructions

- The class-count closed forms and the equal-count law are computations
  to four marks, not theorems.
- The reflection census enumerates hypothetical placements that no
  history admits; it is metatheory about the kernel, and it admits
  nothing.
- The Lean package is a manual receipt: the research job runs the
  Python gates and the blindness scan but does not build Lean.
- Blindness is by rule.  The declared-reading-zero record is a
  discipline, and the scan enforces only the part of it a scan can see.

## 11. Comparison

Withheld until `FREEZE.md` exists, as the seed's section 10 requires.
