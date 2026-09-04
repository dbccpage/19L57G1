# The boundary derivation: Challenges 0 and 1 under declared prior exposure

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
Challenge 1 was closed in a fresh session under the same ceiling; its
status records where a remembered shape was used.

## 1. Metatheory and object language

Metatheory is everything used to carry out and check the derivation:
Python, Lean, tests, receipts, readings, presentation tokens, extensional
profiles, the presentation reader and its convention, and this prose.  The
object language has one supplied opaque datum and a closed positive
judgment grammar: `OnSide(mark, side)` and, under O, `SideNamed(side,
name)`.  Python `contents`, `side_profile`, and `mark_profile` enumerate
those judgments externally for comparison; their collection values are not
object-language data.  Presentation identity, internal identity,
observational equivalence, behavioural separation (not yet declared), and
semantic interpretation are kept distinct.

Supply, mention, admission, current-state designation, retention,
observation, and equality are distinct events or relations in the
kernel: a `Supply` presents and changes no admitted state; a mention is
the metatheory naming a token in an event and is not itself an event;
certifying `replay` refuses a new `AdmitMark` without a prior `Supply`;
re-admission of an existing token is designation rather than duplication
(declared convention); retention is the placement tuple, and at Challenge
1 it is proved that every later event preserves an admitted mark's
judgment; observation is the closed judgment grammar above; regime
equality is structural and is never conflated with the isomorphism
relation.  The canonical key is a bounded-computation tool for quotienting
in the reported census, not an unbounded completeness theorem.

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

Definitions 1 to 16 are implemented in `code/boundary/model.py`; 17 to 19
in `code/boundary/presentation.py`; 20 to 27 in `model.py` and
`code/boundary/challenge1.py` as marked.  The theorem-bearing subset
listed in section 7 is mirrored or abstracted in `lean/BoundarySeed/`;
presentation tokens, token uniqueness, certifying supply-before-placement
replay, the canonical key, the reader, and the convention are Python-only.

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
7. **Event-follows relation.**  The declared object-language relation
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
    initial datum is omitted because every valid regime has it.
15. **Canonical key.**  The minimum serialization over every mark renaming
    and, under U only, reflection.  Invariance and class separation are
    claimed only for the finite census through four marks.
16. **Permitted reflection.**  Permitted under U and not under O, including
    at the raw fixed point of O genesis.  The state-level automorphism
    predicate additionally requires stabilization up to mark renaming;
    canonical orbit equality alone is insufficient.  Permission is a
    definition, not discovered content.
17. **Read whole.**  Metatheory apparatus.  A supplied whole is read as at
    most one mark and the side of the bar it was presented on (`left` or
    `right`); the initial `<|>` reads as no mark.  The reader refuses
    anything beyond that declared bound (a second mark, a mark on each
    side, a nested whole) by name.  This is the one admitted exception
    made operational: the boundary lets the object language see that the
    mark lies on a side, and nothing else about the whole is read.
18. **Presentation convention.**  Metatheory apparatus.  A presented side
    becomes an admitted side only under a declared convention.  Two exist;
    the declared one maps `left` to side 0, which O names `near`.  The
    inscription does not decide the convention.
19. **Supply and admission events of a whole.**  The supply event of a
    read whole presents its token; the admission event under a convention
    places its token on the mapped side.  Neither applies anything.
20. **Mention and supplied tokens.**  Metatheoretic readings of a history:
    the tokens any event names, and the tokens a `Supply` presents.
21. **One-step admission candidates.**  The declared finite candidate space
    after a history: each supplied, not yet admitted token on each side.
    Deterministic computation in `challenge1.py`; it enumerates and
    applies nothing.  It lives outside the kernel because the Challenge 0
    generator census fired on it there.
22. **Mark profile and new observations.**  The metatheoretic extension of
    the holding judgments naming one mark; the set difference of two
    extensions.
23. **Permitted images and the isomorphism relation.**  Every regime a
    permitted renaming reaches (mark permutations under both readings, the
    reflection under U); an isomorphism witness is found by unpruned
    search over them, and `is_isomorphic` is its truth value.  Agreement
    with canonical-key equality is checked over every pair of regimes with
    at most three marks.
24. **Challenge 1 histories and the admitted regime.**  The supplied-only
    history `[Supply(a)]`, and for each side `s` the candidate history
    `[Supply(a), AdmitMark(a, s)]`.  In Lean, `admitted rd s` is the replay
    of the latter from genesis.
25. **Current-state designation.**  The admitted regime under the declared
    convention is designated current, by convention and not by proof; a
    candidate in another isomorphism class is retained as a branch.
26. **Judgment and regime domains.**  Bounded metatheoretic domains for
    the separating-judgment computation: every judgment naming a mark
    below two, and every hypothetical placement of at most one mark.  A
    judgment is permitted-renaming-invariant on the domain when it holds
    equally at every regime and at every permitted image of it.
27. **One-mark relatedness (Lean).**  Equality, or the reflection when the
    reading permits it.  Sufficient for regimes with at most one mark,
    where every mark permutation is the identity; the general relation is
    definition 23.

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
| C0-X extrapolation | NOT FORCED | HIT, scored by Challenge 1 | see 5.2 |

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
  admission grammar; that is the unresolved content of C0-X, now scored in
  5.2.
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

### 5.1 Challenge 1: the supply of `<a|>`

Receipt: `receipts/challenge1.json`.  Predictions frozen at sha256
`7cf17e56fffb4e45d4100750010265582fa921fabeed7fb1b84aa798f6e56dc7` in
commit `152ed096`, before any Challenge 1 code or proof existed in the
working tree.  This does not establish when off-tree or untracked work was
written.

The seed asks whether the supply of `<a|>` is a new external
presentation, a new admitted state, a new internally observable
distinction, or some combination requiring explicit definitions.  The
answer is the combination, with the definitions of section 3: it is a new
external presentation by the `Supply` event and nothing else; it becomes a
new admitted state only through the separately declared admission event,
which the supply does not entail; and it becomes a new internally
observable distinction only after that admission, by exactly one new
holding judgment.  Under U that one judgment is what takes the two sides
from collapsed to distinct; under O the sides were already distinct by
name and the judgment adds the mark's side to the difference.

| result | reading U | reading O | evidence |
|---|---|---|---|
| the supply alone | regime equals genesis; every judgment holds after exactly as before | same | receipt `readings.*.supply`; Lean `supply_preserves_holds`, `supply_no_op` |
| admission needs the prior supply | the candidate history certifies; the admission alone is refused | same | `candidates[*].certified`, `unsupplied_admission_refused` (Python-only precondition) |
| the admitted mark is retained | its judgment holds after every later event of the grammar; probed by a supply, a re-designation on either side, and a hypothetical second admission | same | `retention.*`; Lean `step_preserves_onSide`, `replay_preserves_onSide` |
| new holding judgments after admission | exactly `OnSide(0, s)`; `OnSide(0, s')` does not hold; no name judgment | exactly `OnSide(0, s)`; both name judgments hold as at genesis | `new_observations`, `other_side_judgment_holds`, `name_observations_unchanged`; Lean `admitted_onSide_true_iff`, `place_new_judgment`, `place_other_side_false`, `admitted_U_no_sideNamed`, `admitted_O_sideNamed`, `step_preserves_sideNamed`, `replay_preserves_sideNamed` |
| holding judgments before / after supply / after admission | 0 / 0 / 1 | 2 / 2 / 3 | `holding_judgments_*` |
| the mark's profile | its side, nothing else | same | `mark_profile`; definition 22 |
| the two side profiles after one mark | differ | differ | `sides_collapsed = false`; Lean `admitted_sides_differ`, `admitted_contents_placed`, `admitted_contents_other` |
| the two candidate regimes | unequal; each the other's reflection | same | `convention.candidates_equal`, `other_is_reflection_of_designated`; Lean `admitted_candidates_unequal`, `reflect_admitted`, `reflect_step_place`, `reflect_step_supply` |
| related by a permitted renaming | yes, the reflection: one class | no: two classes | `candidate_space.classes_under_isomorphism`, `isomorphism_witness`; Lean `candidates_related_U`, `candidates_not_related_O` |
| a permitted-renaming-invariant judgment separating them | none on the bounded domain | `OnSide(0, 0)` and `OnSide(0, 1)`; every renaming is the identity at one mark | `permitted_renaming_invariant_separating_judgments`; Lean `invariant_judgment_does_not_separate`, `onSide_separates_candidates` |
| “which side” as an internal fact | no | yes | the two rows above |
| the presentation convention | invisible up to the permitted reflection | visible; the other convention's regime is the reflection of the designated one | definition 18; `convention.*` |
| designated current state | `a` on side 0, by convention | `a` on side 0, by convention; the side-1 candidate retained as a branch | `designated_current`, `retained_non_isomorphic_candidates` |
| an event follows from the admitted state | none | none | `event_follows_relation_empty`; Lean `no_event_follows_admitted` |
| initial datum and reading | unchanged by every event | same | `initial_datum_unchanged`, `reading_unchanged`; Lean `step_reading`, `step_initialDatum`, `replay_reading`, `replay_initialDatum` |
| new event kind or judgment form needed | none | none | `event_kinds`, `observation_vocabulary` |
| event-returning functions, by module | kernel: none; presentation: the two constructors; challenge module: the enumerator, the probes, and the two imported constructors | same | `event_returning_functions_by_module`; supplementary census, not the semantic proof |

Three things in this table are decisions and are labelled as such.  The
convention is metatheory: the inscription `<a|>` does not say which
admitted name the left of the bar carries, and under O the two
conventions yield two non-isomorphic regimes.  The run declares one,
designates its regime current, and retains the other as a branch; the
branch is carried without a second tower because every continuation of it
is the reflection of a continuation of the designated one (Lean
`reflect_step_place`, `reflect_step_supply`).  The one-boundary modelling
(the mark is placed on a side of the one admitted boundary; the whole is
not admitted as a second datum) follows the seed's phrase “the admitted
boundary” and is OPEN as to whether a whole on a side is a datum, which
Challenge 5 asks.  The designation of the admitted regime as current is by
convention, not proof, and is said so in the receipt.

#### 5.2 The predictions, scored

| id | label | status | note |
|---|---|---|---|
| C0-X (from Challenge 0) | NOT FORCED | HIT | U: genesis collapsed, the admitted regime not, by one supply and one admission with no new form; O: the sides distinct before and after, the only new holding judgment the mark's own side |
| C1-1 supply is presentation only | FORCED | HIT | |
| C1-2 admission is separate; the mark is retained | FORCED | HIT | |
| C1-3 exactly one new judgment | FORCED | HIT | |
| C1-4 the two sides under U | FORCED | HIT | |
| C1-5 the two sides under O, and the convention | NOT FORCED | HIT | the run declared a convention and retained the other candidate, as predicted |
| C1-6 no transition follows | FORCED | HIT | |
| C1-7 one boundary, no second datum | NOT FORCED | HIT on its mechanical part | the falsifier is a modelling claim only a later challenge can trigger |
| C1-X extrapolation | NOT FORCED | PENDING | scored by Challenge 2 |

Seven of seven hit, and C0-X hit in both halves.  Five of the seven were
labelled FORCED and follow from Challenge 0's definitions plus the
admission event Challenge 0 declared; the two NOT FORCED hits concern
decisions the run made, not facts it found.  The hit rate is evidence of
the order of the work, not of insight.

#### 5.3 What Challenge 1 does not establish

- Nothing about two marks.  The retention probe's second admission is
  hypothetical and its token was never supplied by the caller.
- Whether `<a|>` re-supplied at Challenge 2 is the same presentation as
  this one, or whether `<|a>` with the same glyph is a second mark: the
  kernel's `Supply` carries the token only, and the Challenge 0
  token-uniqueness rule would silently turn a second whole with the same
  token into a designation of the first mark.  Challenge 2 must decide
  this loudly.
- No unbounded theorem for the isomorphism relation; its agreement with
  the canonical key is checked to three marks.
- Nothing about depth, nesting, or the outside of the boundary.

#### 5.4 Dependence on the admitted boundary

| result | dependence |
|---|---|
| supply is presentation only | independent of the boundary |
| admission is a separate event; certifying replay's precondition | independent of the boundary for the event discipline; the side the mark is retained on requires it |
| the initial datum and reading are unchanged by every event | independent of the boundary |
| the event-follows relation stays empty | independent of the boundary |
| the one new judgment, the profiles, the candidates, the convention, the classes | require the admitted boundary and are not formulated after removing it |

### 5.5 Challenges 2 to 5

Not yet reached.  Each opens in a fresh session with its own frozen
`PREDICTIONS.md`.

## 6. The autonomous branch procedure

Not yet declared; it is declared after Challenge 3 by the seed's order.

## 7. Proofs and countermodels

Lean package `lean/`, core Lean only, no dependency on any other package
in this repository.  Forty-nine theorems, every one with a `#print axioms`
report in `lean/axioms.txt`, checked against a successful clean and fresh
build by `verify_lean.py`; every report lies within
`{propext, Quot.sound}`.  `verify_lean.py` also requires every module under
`lean/BoundarySeed/` to lie in the root's import closure, because a module
the root does not reach is text-scanned but never elaborated; that check was
added at Challenge 1 after the hole was observed live and is proved by
injection.

### 7.1 Challenge 0 (`Basic.lean`)

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
| `no_event_follows` | the declared event relation is empty | propext |

### 7.2 Challenge 1 (`Challenge1.lean`)

| theorem | statement | axioms |
|---|---|---|
| `admitted_eq` | the Challenge 1 history replays to one placed mark | none |
| `supply_preserves_holds` | a supply changes no judgment | propext |
| `step_reading` | every event keeps the reading | none |
| `step_initialDatum` | every event keeps the initial datum | none |
| `replay_reading` | every history keeps the reading | none |
| `replay_initialDatum` | every history keeps the initial datum | none |
| `step_preserves_sideNamed` | every event keeps every side-name judgment | propext |
| `replay_preserves_sideNamed` | every history keeps every side-name judgment | propext |
| `getD_append_left` | list lookup below the length ignores an appended tail | propext |
| `step_preserves_onSide` | every event keeps an admitted mark's judgment | propext |
| `replay_preserves_onSide` | every history keeps an admitted mark's judgment (retention) | propext |
| `getD_append_singleton` | lookup at the old length reads the appended element | propext |
| `place_new_judgment` | after a placement the placed mark's judgment holds | propext, Quot.sound |
| `place_other_side_false` | after a placement the other side's judgment for it does not hold | propext |
| `admitted_onSide_true_iff` | exactly one mark-on-side judgment holds in the admitted regime | propext, Quot.sound |
| `admitted_U_no_sideNamed` | under U no side-name judgment holds after admission | propext |
| `admitted_O_sideNamed` | under O the name judgments hold as at genesis | propext |
| `admitted_contents_placed` | the placed side's extension is the one mark | propext, Quot.sound |
| `admitted_contents_other` | the other side's extension is empty | propext, Quot.sound |
| `admitted_sides_differ` | the two profiles differ after one mark, either reading | propext, Quot.sound |
| `reflect_step_supply` | the reflection commutes with a supply | none |
| `reflect_step_place` | the reflection carries a placement to the other side | propext |
| `reflect_admitted` | the two candidates are each other's reflection | propext |
| `admitted_candidates_unequal` | the two candidates are unequal as raw data | propext |
| `candidates_related_U` | under U the candidates are related by a permitted renaming | propext |
| `candidates_not_related_O` | under O they are related by no permitted renaming | propext |
| `invariant_judgment_does_not_separate` | a reflection-invariant judgment holds equally at both candidates | propext |
| `onSide_separates_candidates` | the placed mark's own judgment separates them as raw data | propext, Quot.sound |
| `no_event_follows_admitted` | no event follows from the admitted regime | propext |

No countermodel is needed at Challenges 0 or 1: no target failed.
`admitted_eq`, `step_reading`, `step_initialDatum`, `reflect_step_supply`,
and `supply_preserves_holds` are DEFINITION-level (true by unfolding) and
are not counted as content.

## 8. Receipts

- `receipts/challenge0.json` and `receipts/challenge1.json`: deterministic
  (sorted keys, LF, no timestamp, no environment value); regenerated
  byte-identically by `run_challenge0.py` and `run_challenge1.py` and
  checked by the tests and by the research job.
- The suite passes 97 tests.  Fresh coverage over the five declared code
  files is 100.00% line and 100.00% branch; `check_coverage.py` computes
  line coverage as covered lines divided by statements rather than
  Coverage.py's combined line-plus-branch percentage.
- `lean/axioms.txt`: 49 reports, regenerated once at Challenge 1 when the
  theorem set was final.
- Injection record: `MANUAL.md`.

## 9. The strongest defensible statement so far

At genesis the supplied opaque datum is present.  Under U, the two sides of
its admitted boundary have equal extensional profiles; supply is inert; no
event follows in the declared relation; no positive mark-on-side
judgment holds; and reflection is permitted.  Under O, no mark-on-side
judgment holds but the two admitted name judgments do, so the profiles
differ only by that declaration and reflection is not permitted even though
it fixes the empty placement as raw data.

After the supply of `<a|>`, under both readings, the regime is genesis and
every judgment holds as before: the supply is presentation only.  The mark
enters the admitted state only through the separate admission event, and
once admitted its judgment survives every later event of the grammar.
That admission adds exactly one holding judgment, the mark's side, and
changes no name judgment, the initial datum, or the reading.  Under U it
takes the two sides from collapsed to distinct, the two candidate one-mark
regimes are each other's reflection and related by the permitted
reflection, so no permitted-renaming-invariant judgment of the bounded
domain says which side the mark is on.  Under O the sides were already
distinct by name; the two candidates are unequal and related by no
permitted renaming, and the mark's own judgment separates them, so which
named side it lies on is internal — at the price of the O declaration and
of a metatheoretic presentation convention the inscription does not fix.
No event follows from any of these states.  These are scoped Lean
theorems, bounded computations, or labelled definitions and conventions.
Because the instrument declared prior exposure, they carry no
blind-independence or independent-discovery conclusion.

## 10. Limitations and open obstructions

- The class-count closed forms and the equal-count law are computations
  to four marks, not theorems.
- No unbounded completeness or injectivity theorem is claimed for
  `canonical`; its evidence is the finite census, focused invariance
  tests, and agreement with the witness search to three marks.
- The Lean one-mark relatedness is sufficient at one mark only; the
  general isomorphism relation is Python.
- The reflection census and the retention probes enumerate hypothetical
  placements and events that no history admits; they are metatheory about
  the kernel, and they admit nothing.
- The presentation convention is metatheory.  Under O the run's designated
  current state depends on it; the other convention's tower is carried as
  the reflection of this one, by a theorem, not by a second tower.
- Whether a whole on a side is itself a datum is OPEN for Challenge 5; the
  one-boundary modelling at Challenge 1 is a decision.
- `Supply` carries the token only.  Challenge 2 must say whether the two
  wholes with the same glyph are one presentation or two, and must not let
  token uniqueness turn the second into a designation silently.
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
