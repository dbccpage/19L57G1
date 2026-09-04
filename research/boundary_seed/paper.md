# The boundary derivation: Challenge 0 under declared prior exposure

`AuthorityEffect: None`.  A source-isolated derivation from the inscription
`<|>`, carried out inside this repository under the read-only seed
`research/boundary_seed/SEED.md`.  The instrument had already reviewed the
sealed derivation and declared that remembered structure influenced this
run.  It is therefore **not evidence of blind or independent discovery**.
This paper grows one challenge per session; sections not reached say so.

## 0. Experimental and provenance boundary

The seed is read-only, sha256
`ba30bcd600d8232f054f3b4d9a5d03caafaa7442dfd8095643f39cfcea1ad0be`.
The run writes only `research/boundary_seed/` and the append-only
registration of its checks in the research job of the workflow.  Until a
committed `FREEZE.md` marker exists, the declared procedure reads nothing of the repository
beyond the seed, five named contract sections, and its own tree; it imports
nothing from the sealed kernel and builds its own.  The source-isolation
scan checks working, index, and committed-history bytes for citations into
the named sealed paths, sealed claim and Lean identifiers, sealed-kernel
imports, and identifiable other research-tree names.  This mechanical
scan cannot establish what the instrument remembered or read elsewhere.

The instrument drafted the seed in the same session after reviewing the
sealed derivation and research trees.  `MANUAL.md` and the Challenge 0
status record its use of remembered kernel shape, a designation convention,
and the expected observation choice.  Commit history proves only that the
seed, plan/manual, and predictions were committed in that order before the
branch committed code or proofs; it cannot prove when untracked or off-tree
work was written.  The surviving provenance claim is therefore
`SOURCE_ISOLATED_WITH_DECLARED_PRIOR_EXPOSURE`, not “blind derivation.”

## 1. Metatheory and object language

Metatheory is everything used to carry out and check the derivation:
Python, Lean, tests, receipts, readings, presentation tokens, extensional
profiles, and this prose.  The object language has one supplied opaque
datum and a closed positive judgment grammar: `OnSide(mark, side)` and,
under O, `SideNamed(side, name)`.  Python `contents` and `side_profile`
enumerate those judgments externally for comparison; their collection
values are not object-language data.  Presentation identity, internal
identity, observational equivalence, behavioural separation (not yet
declared), and semantic interpretation are kept distinct.

Supply, mention, admission, current-state designation, retention,
observation, and equality are distinct events or relations in the
kernel: a `Supply` presents and changes no admitted state; certifying
`replay` refuses a new `AdmitMark` without a prior `Supply`; re-admission
of an existing token is designation rather than duplication (declared
convention); retention is the placement tuple; observation is the closed
judgment grammar above; regime equality is structural.  The canonical key
is a bounded-computation tool for quotienting in the reported census, not
an unbounded completeness theorem.

## 2. The admitted boundary: one declaration, two readings

The inscription `<|>` is the one supplied opaque datum at genesis.  The
one admitted primitive exception is its boundary with two sides.  The
boundary is not a second datum; it is the frame against which later marks
may be placed.  It is listed first in the ledger and is never called free.

Reading U leaves the two sides unnamed.  The exchange of the sides is
then a renaming the object language cannot see, and the isomorphism
relation includes it.  Reading O names the sides `near` and `far`.  The
exchange is then not a renaming, and the isomorphism relation excludes
it.  The two readings are carried as separate towers from genesis; a
result that holds under one and not the other is stated under its
reading in the same sentence.  Two-ness is not assumed of the sides
beyond the declaration itself (declared reading 2 of `MANUAL.md`).

## 3. Definitions, in dependency order

All are implemented in `code/boundary/model.py`.  The theorem-bearing subset
listed in section 7 is mirrored or abstracted in `lean/BoundarySeed/Basic.lean`;
presentation tokens, token uniqueness, certifying supply-before-placement
replay, and the canonical key are Python-only at Challenge 0.

1. **Initial datum.**  One opaque supplied whole with internal identity
   zero.  Its presentation spelling is not stored.
2. **Boundary and reading.**  The admitted boundary has two sides.  U
   leaves them unnamed; O admits the names `near` and `far`.
3. **Regime.**  The fixed initial datum, a reading, unique admitted mark
   tokens, and one valid side for each mark.  Construction rejects unknown
   readings, duplicate tokens, invalid sides, and length mismatch.
4. **Genesis.**  The initial datum is present and no later mark is admitted.
5. **Events.**  `Supply(token)` is external presentation;
   `AdmitMark(token, side)` is a requested admission.
6. **Step, replay, certification.**  Low-level `step` applies an already
   validated event.  Certifying `replay` tracks presentations and refuses
   a new mark without an earlier supply; `certify` rejects such a history.
7. **Event-follows relation.**  The Challenge 0 object-language relation
   from a regime to an event is the empty relation.  External events remain
   possible inputs to replay.
8. **Judgment grammar.**  The closed sum `OnSide | SideNamed`; it contains
   no empty-side or counting constructor.
9. **Judgment holding.**  `OnSide(i,s)` holds exactly for a placed mark.
   `SideNamed(s,n)` holds exactly under O for the admitted name of `s`.
10. **Contents and side profile.**  Metatheoretic extensional enumerations
    of the positive judgments.  Under U a profile contains marks only;
    under O it also contains the name.
11. **Collapsed sides.**  Equal extensional side profiles.
12. **Reflection.**  The exchange of the two sides.
13. **Mark renaming.**  A permutation of internal identities; tokens travel
    with their marks.
14. **Serialization.**  Reading and placement, tokens forgotten; the fixed
    initial datum is omitted because every valid Challenge 0 regime has it.
15. **Canonical key.**  The minimum serialization over every mark renaming
    and, under U only, reflection.  Invariance and class separation are
    claimed only for the finite census through four marks.
16. **Permitted reflection.**  Permitted under U and not under O, including
    at the raw fixed point of O genesis.  The state-level automorphism
    predicate additionally requires stabilization up to mark renaming;
    canonical orbit equality alone is insufficient.  Permission is a
    definition, not discovered content.

## 4. Challenge 0: the initial state `<|>`

Receipt: `receipts/challenge0.json`.  Predictions frozen at sha256
`a03ee8127e83603af75c56c4061bcbe9dc1689c3b56b90854148dfb9856cc395`
in a commit preceding the branch's first code-or-proof commit.  This does not
establish when off-tree or untracked work was written.

### 4.1 Results under each reading

| result | reading U | reading O | evidence |
|---|---|---|---|
| initial opaque datum | present | present | receipt `readings.*.initial_datum`; Lean `genesis_initial_datum` |
| side profiles at genesis | `[[]]`, `[[]]` | `["near", []]`, `["far", []]` | receipt `readings.*.side_profiles` |
| the two sides collapsed | yes | no, and the difference is the name component only | `sides_collapsed`; Lean `sides_collapsed_at_genesis_U`, `sides_distinct_at_genesis_O` |
| mark-on-side judgments at genesis | none | none | `mark_observations`; Lean `no_observation_at_genesis` |
| side-name judgments at genesis | none | `near` and `far` | `name_observations`; Lean `O_name_judgment_at_genesis`, `U_no_name_judgment_at_genesis` |
| a supply changes the state | never | never | `supply_leaves_state_unchanged`; Lean `supply_no_op`, `replay_supply_inert` |
| an event follows from the state | none in the declared relation | same | `event_follows_relation_empty`; Lean `no_event_follows` |
| public module function has an event-containing resolved return annotation | none in the census | same | supplementary `state_event_generators = []`, not the semantic proof; event constructors are outside this population |
| the reflection is a permitted renaming | yes | no | definition 16 |
| the reflection fixes genesis as raw data | yes | yes | Lean `reflect_genesis`; receipt |
| the reflection is a permitted automorphism of genesis | yes | no, even at the raw fixed point | receipt; Lean `reflection_permitted_U`, `reflection_not_permitted_O`; bounded non-genesis stabilizers are in 4.3 |
| the reflection is an involution | yes | yes | Lean `reflect_reflect` |
| the reflection moves any placed mark | yes | yes | Lean `reflect_moves_a_mark` |

Under O, the profile difference is DEFINITION-level: it is the two admitted
names and nothing else.  `contents_genesis = []` is a metatheoretic theorem
about the extension of positive judgments; it does not expose an empty-list
datum inside the object language.  Nothing at Challenge 0 gives the
O-distinction content beyond the declaration.

### 4.2 The predictions, scored

| id | label | status | note |
|---|---|---|---|
| C0-1 collapse under U | FORCED | HIT | by the declared extensional profile |
| C0-2 distinction under O is bought | FORCED, DEFINITION-level | HIT | the profiles differ in the name component only |
| C0-3 inertia | FORCED | HIT | supply inert; the declared event-follows relation is empty under both readings |
| C0-4 emptiness is not a primitive judgment | NOT FORCED | PARTIAL, target basis DEFINITION-level | no `OnSide` judgment holds and the grammar has no empty/count form, but the frozen “no observation fires” rationale is false because O name judgments do hold |
| C0-5 the reflection | FORCED for genesis | HIT, general clause SHARPENED | see 4.3 |
| C0-X extrapolation | NOT FORCED | PENDING | scored by Challenge 1 |

Four of five scored predictions hit.  The four HIT clauses were labelled
FORCED in the frozen file.  C0-4 was explicitly `NOT FORCED` and is PARTIAL:
its emptiness target is definition-level under the chosen closed positive
judgment grammar, while its stated “no observation fires” rationale is false
under O.  Git history establishes that the prediction file was committed
before code and proofs on this branch.  It does not establish when any
untracked or off-tree work was written, and it is not evidence of insight or
independent discovery.

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

Within the explicit zero-through-four-mark bound, applying reflection and
then allowing a mark renaming returns a placement exactly when the two
sides carry equally many marks (`fixed_iff_equal_counts = true`).  This
combinatorial comparison can be made under either reading, but reflection
is a *permitted automorphism* only under U.  Prediction C0-5's general U
clause named “every state whose sides carry the same contents”; with
contents as sets of internal identities that is only the empty placement,
so the bounded computation sharpens it.  No unbounded theorem is claimed.
Within the same table, O has `n + 1` observed classes and U has
`floor(n/2) + 1`; these closed forms describe five rows, not all `n`.

### 4.4 What Challenge 0 does not establish

- Nothing about a mark's own profile.  Marks have no observable of their
  own at Challenge 0 beyond the side they lie on.
- The model test conditionally shows that one admitted mark yields unequal
  side profiles under both readings.  Challenge 0 does not settle whether
  Challenge 1's supplied whole is admitted under its still-undeclared
  admission grammar; that is the unresolved content of C0-X.
- Nothing about a whole within a side, the outside of the outermost
  boundary, depth, or the boundary's cost.  Those are Challenge 5 and
  the required questions of the seed, not reached.
- The O-distinction is bought.  Whether anything later makes it earn its
  keep is open.

### 4.5 Dependence on the admitted boundary

The seed requires this classification at every stage.  Removing the
boundary is a counterfactual dependency classification here, not a third
reading silently added to the model.

| result | dependence |
|---|---|
| the opaque initial datum exists | independent of the boundary; the whole was supplied first |
| supply leaves admitted state unchanged | independent of the boundary under the declared event semantics |
| the Challenge 0 event-follows relation is empty | independent of the boundary |
| sides, side names/profiles, placements, reflection, collapse, and class counts | require the admitted boundary and are not formulable after removing it |

## 5. Challenges 1 to 5

Not yet reached.  Each opens in a fresh session with its own frozen
`PREDICTIONS.md`.

## 6. The autonomous branch procedure

Not yet declared; it is declared after Challenge 3 by the seed's order.

## 7. Proofs and countermodels

Lean package `lean/`, core Lean only, no dependency on any other package
in this repository.  Twenty theorems, every one with a `#print axioms`
report in `lean/axioms.txt`, checked against a successful clean and fresh
build by `verify_lean.py`; every report lies within
`{propext, Quot.sound}`.

| theorem | statement | axioms |
|---|---|---|
| `supply_no_op` | a supply is a no-op | none |
| `step_changes_only_by_place` | a step that changes the state is a placement | none |
| `genesis_initial_datum` | genesis contains the supplied opaque datum | none |
| `genesis_placement_nil` | genesis has no placement | none |
| `no_observation_at_genesis` | no positive mark-on-side judgment holds at genesis | propext |
| `O_name_judgment_at_genesis` | each admitted O side-name judgment holds | propext |
| `U_no_name_judgment_at_genesis` | no side-name judgment holds under U | propext |
| `contents_genesis` | metatheoretic positive extensions are empty | propext, Quot.sound |
| `sides_collapsed_at_genesis_U` | U extensional side profiles agree at genesis | propext, Quot.sound |
| `sides_distinct_at_genesis_O` | O extensional side profiles differ at genesis | propext, Quot.sound |
| `side_names_distinct` | the two name constructors differ | none |
| `map_not_not` | double negation of a Boolean list is the identity | propext |
| `reflect_reflect` | the reflection is an involution | propext |
| `reflect_genesis` | the reflection fixes genesis | none |
| `reflection_permitted_U` | reflection is permitted under U | none |
| `reflection_not_permitted_O` | reflection is not permitted under O | propext |
| `reflect_moves_a_mark` | the reflection moves any placed mark | propext |
| `replay_deterministic` | equal histories replay equally | none |
| `replay_supply_inert` | a history of supplies replays to its base | none |
| `no_event_follows` | the declared Challenge 0 event relation is empty | propext |

No countermodel is needed at Challenge 0: no target failed.

## 8. Receipts

- `receipts/challenge0.json`: deterministic (sorted keys, LF, no
  timestamp, no environment value); regenerated byte-identically by
  `run_challenge0.py` and checked by the tests and by the research job.
- The repaired suite passes 53 tests.  Fresh coverage over the three declared
  code files is 100.00% line and 100.00% branch; `check_coverage.py` computes
  line coverage as covered lines divided by statements rather than
  Coverage.py's combined line-plus-branch percentage.
- `lean/axioms.txt`: 20 reports.
- Injection record: `MANUAL.md`.

## 9. The strongest defensible statement so far

At genesis the supplied opaque datum is present.  Under U, the two sides of
its admitted boundary have equal extensional profiles; supply is inert; no
event follows in the declared Challenge 0 relation; no positive mark-on-side
judgment holds; and reflection is permitted.  Under O, no mark-on-side
judgment holds but the two admitted name judgments do, so the profiles
differ only by that declaration and reflection is not permitted even though
it fixes the empty placement as raw data.  These are scoped Lean theorems or
labelled definitions.  Because the instrument declared prior exposure, they
carry no blind-independence or independent-discovery conclusion.

## 10. Limitations and open obstructions

- The class-count closed forms and the equal-count law are computations
  to four marks, not theorems.
- No unbounded completeness or injectivity theorem is claimed for
  `canonical`; its Challenge 0 evidence is the finite census and focused
  invariance tests.
- The reflection census enumerates hypothetical placements that no
  history admits; it is metatheory about the kernel, and it admits
  nothing.
- The Lean package is a manual receipt: the research job runs the
  Python gates and source-isolation scan but does not build Lean.
- Prior exposure is disclosed and material: the run is source-isolated, not
  blind.  The scan proves only the byte populations and patterns it checks.
- The seed's future freeze instruction asks a file to hash every file in its
  own write root, which is self-referential if it includes itself.  Until a
  parent-tree or explicit-exclusion protocol is defined and verified, a
  committed marker can retire the mechanical source scan but cannot establish
  a valid freeze manifest; comparison remains OPEN.

## 11. Comparison

Withheld.  A working or staged `FREEZE.md` does not retire the isolation gate.
A committed marker does retire that mechanical scan, but does not by itself
close or verify the unresolved manifest protocol above.
