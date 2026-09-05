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
certifying `replay` refuses a new `AdmitMark` without a prior `Supply`,
treats a re-admission of an admitted token on its own side as a no-op, and
refuses one naming the other side because it would move the mark (all
three Python-only declarations; the Lean events carry no token); the word
designation is reserved for current-state designation, the current state
being the replay of the caller's history, and an earlier use of it for the
re-admission no-op is WITHDRAWN; retention is the placement tuple, and at
Challenge 1 it is proved that every later event of the Lean grammar
preserves an admitted mark's judgment; observation is the closed judgment
grammar above; regime equality is structural and is never conflated with
the isomorphism relation.  The canonical key is a bounded-computation tool for quotienting
in the reported census, not an unbounded completeness theorem.

That reservation is on this run's own prose.  The frozen
`challenge1/PREDICTIONS.md` uses the bare word in two senses, neither of
them current-state designation, and each is read in its own context and
scored on the frozen words alone: at C1-2 it names a re-admission of an
already admitted token, scored by whether such an event is accepted and
leaves the mark's judgment unchanged; at C1-5, where the noun and its
participle run together through the prediction, it names the convention's
selection of a candidate, which admits nothing.  C1-5's HIT depends on
that declared reading of its own clause, and neither frozen use is read
as current-state designation, which no clause of the frozen file names.

The word *retained* is used in the placement sense only.  The seed uses
*retain* of two other subjects: the caller retains a whole at Challenge 2,
and the run retains a tied branch from Challenge 3 on.  Neither is the
placement tuple.  What the caller's “retains” admits, and who pays, is
Challenge 2's first decision, so that word is quoted and not defined here;
and a candidate class the run does not drop is *kept*: it stays a certified
branch, and keeping it admits nothing.  An earlier version called kept
candidate classes retained, a second undeclared sense of a word the seed
lists among those never to be conflated, and that use is WITHDRAWN.

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
   validated event: a supply changes nothing; an admission of a new token
   places it; one naming an admitted token on its own side is a no-op; one
   naming the other side would move the mark and is refused by name.
   Certifying `replay` tracks presentations and refuses a new mark without
   an earlier supply; `certify` rejects a refused history.  The no-op and
   both refusals are Python-only: the Lean `place` carries no token.
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
24. **Challenge 1 histories and the candidate regimes.**  The supplied-only
    history `[Supply(a)]`, and for each side `s` the candidate history
    `[Supply(a), AdmitMark(a, s)]`.  In Lean, `admitted rd s` is the replay
    of the latter from genesis.
25. **Current-state designation.**  The current state after a challenge is
    the replay of the caller's history and of no event the caller's
    history does not contain.  At Challenge 1 the caller supplies and does
    not retain, so that history is `[Supply(a)]`, no admission event is in
    the caller's history at this challenge, and the current regime under
    each reading is genesis.  That `a` is supplied is a fact of the history
    (definition 20), not of the state: a regime has no supplied component,
    and the supply changes none it has.  No admission candidate is
    current.  The declared convention selects which candidate admission
    the presented side licenses, if admission is later called for; it
    admits nothing.  Every isomorphism class of candidates is kept as a
    certified branch: one class under U, two under O.  An earlier version
    of this definition designated the convention's admitted candidate as
    current; that turned a candidate from the run's own enumerator into
    admitted state with no admission event from the caller, conflated
    supply with admission, and is WITHDRAWN.  A later version described
    the current state as “genesis with `a` presented”; that read the
    supply into a regime that carries no such component, the conflation
    of supply with state that the rest of the rung avoids, and is
    WITHDRAWN too.  A third version wrote the rule as “nothing the caller
    did not supply”, a second sense of supply that is not the `Supply`
    event of definition 5; reworded.
26. **Judgment and regime domains.**  Bounded metatheoretic domains for
    the separating-judgment computation: every judgment naming a mark
    below two, and every hypothetical placement of at most one mark.  A
    judgment is permitted-renaming-invariant on the domain when it holds
    equally at every regime and at every permitted image of it.  In Lean,
    `bounded_invariant_judgment_does_not_separate` takes this notion as its
    hypothesis under U: invariance under the reflection at every regime of
    the reading with at most one mark, the reflection being the only
    permitted renaming beyond the identity there.  That identification is
    by inspection of `permitted_images` at one mark, not a theorem.
27. **One-mark relatedness (Lean).**  Equality, or the reflection when the
    reading permits it.  Intended for regimes with at most one mark, where
    every mark permutation is the identity; but that adequacy is prose,
    not a Lean theorem, so a Lean statement about this relation is a
    statement about it alone and the general relation is definition 23,
    computed.  Under O the relation reduces to equality by unfolding
    `reflectionPermitted`.
28. **Side exchange of a history (Lean).**  `exchangeSide` sends a supply
    to itself and a placement to the other side; it is an involution on
    events and, mapped, on histories.

## 4. Challenge 0: the initial state `<|>`

Receipt: `receipts/challenge0.json`.  Predictions frozen at sha256
`a03ee8127e83603af75c56c4061bcbe9dc1689c3b56b90854148dfb9856cc395`
in a commit preceding the branch's first code-or-proof commit.  This does not
establish when off-tree or untracked work was written.

### 4.1 Results under each reading

| result | reading U | reading O | evidence |
|---|---|---|---|
| initial opaque datum | present | present | receipt `readings.*.initial_datum`; Lean `genesis_initial_datum` (DEFINITION-level, `rfl`) |
| side profiles at genesis | `[[]]`, `[[]]` | `["near", []]`, `["far", []]` | receipt `readings.*.side_profiles` |
| the two sides collapsed | yes | no, and the difference is the name component only | `sides_collapsed`; Lean `sides_collapsed_at_genesis_U`, `sides_distinct_at_genesis_O` |
| mark-on-side judgments at genesis | none | none | `mark_observations`; Lean `no_observation_at_genesis` |
| side-name judgments at genesis | none | `near` and `far` | `name_observations`; Lean `O_name_judgment_at_genesis`, `U_no_name_judgment_at_genesis` |
| a supply changes the state | never | never | `supply_leaves_state_unchanged`; Lean `supply_no_op` (DEFINITION-level, `rfl`), `replay_supply_inert` (a history of supplies, by induction) |
| an event follows from the state | none in the declared relation | same | `event_follows_relation_empty`; Lean `no_event_follows` (DEFINITION-level: the declared relation is empty by unfolding) |
| public module function has an event-containing resolved return annotation | none in the census | same | supplementary `state_event_generators = []`, not the semantic proof; event constructors are outside this population |
| the reflection is a permitted renaming | yes | no | definition 16 |
| the reflection fixes genesis as raw data | yes | yes | Lean `reflect_genesis` (DEFINITION-level, `rfl`); receipt |
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
commit `152ed096`, before the branch's first Challenge 1 code-or-proof
commit.  Git establishes that committed order only; it does not establish
when off-tree or untracked work was written.  An earlier version of this
sentence claimed the stronger working-tree fact and is withdrawn.

The seed asks whether the supply of `<a|>` is a new external
presentation, a new admitted state, a new internally observable
distinction, or some combination requiring explicit definitions.  The
answer is the combination, with the definitions of section 3: it is a new
external presentation by the `Supply` event and nothing else; it would
become a new admitted state only through the separately declared admission
event, which the supply does not entail and which is in no history of the
caller's at this challenge, the caller supplying and not retaining; and it
would become a new internally observable distinction only after such an
admission, by exactly one new holding judgment.  So after Challenge 1 the
current regime under each reading is genesis, the caller's history being
`[Supply(a)]`, in which `a` is supplied and nothing is admitted; and the
two admission candidates are certified histories that show what an
admission on either side would do, kept as branches and not current.  Under U the
one candidate judgment is what would take the two sides from collapsed to
distinct; under O the sides were already distinct by name and the judgment
would add the mark's side to the difference.

| result | reading U | reading O | evidence |
|---|---|---|---|
| the supply alone | regime equals genesis; every judgment holds after exactly as before | same | receipt `readings.*.supply`; Lean `supply_no_op`, `supply_preserves_holds` (both DEFINITION-level, by unfolding `step`) and `replay_supply_inert` (a history of supplies, by induction) |
| the current state after the challenge | the current regime is genesis: the replay of the caller's history `[Supply(a)]`, in which `a` is supplied and nothing is admitted; no admission candidate is current | same | `current_state` (`admitted_candidate_is_current` is membership of the current regime in the candidate regimes); definition 25; Lean `replay_supply_inert` at n = 1, which is `rfl` (DEFINITION-level) |
| admission needs the prior supply | each candidate history certifies; the admission alone is refused | same | `candidates[*].certified`, `unsupplied_admission_refused` (Python-only precondition) |
| a candidate's admitted mark is retained | its judgment holds after every later event of the Lean grammar (a supply or a new placement), PROVED; a re-admission on its own side is a no-op and one naming the other side is refused by certifying replay, both Python-only DEFINITION; probed by a supply, a same-side re-admission, a moving admission, and a hypothetical second admission | same | `retention.*`; Lean `replay_preserves_onSide` (its step `step_preserves_onSide`) |
| new holding judgments after a candidate admission | exactly `OnSide(0, s)`; `OnSide(0, s')` does not hold; no name judgment | exactly `OnSide(0, s)`; both name judgments hold as at genesis | `new_observations`, `other_side_judgment_holds`, `name_observations_unchanged`; Lean `admitted_onSide_true_iff`, `place_new_judgment`, `place_other_side_false`, `admitted_U_no_sideNamed`, `admitted_O_sideNamed`, `replay_preserves_sideNamed` (its step `step_preserves_sideNamed` is by unfolding) |
| holding judgments before / after supply / after a candidate admission | 0 / 0 / 1 | 2 / 2 / 3 | `holding_judgments_*` |
| the mark's profile | its side, nothing else | same | `mark_profile`; definition 22 |
| the two side profiles after one mark | differ | differ | `sides_collapsed = false`; Lean `admitted_sides_differ`, `admitted_contents_placed`, `admitted_contents_other` |
| the two candidate regimes | unequal; each the other's reflection | same | `convention.candidates_equal`, `other_is_reflection_of_candidate`; Lean `admitted_candidates_unequal`, and `reflect_admitted` (DEFINITION-level, `rfl`) |
| related by a permitted renaming | yes, the reflection: one class (Lean `candidates_related_U`, DEFINITION-level, both halves by unfolding: `reflectionPermitted .U := True` and `reflect_admitted`, which is `rfl`) | no: two classes, COMPUTED over the unpruned search of every mark permutation; the Lean `candidates_not_related_O` closes only the one-mark relation, which under O is raw inequality | `candidate_space.classes_under_isomorphism`, `candidate_classes`, `isomorphism_witness`; Lean as stated |
| a permitted-renaming-invariant judgment separating them | none on the bounded domain: PROVED for every judgment invariant under the reflection over the one-mark regimes of the reading, which is definition 26's notion under U, and COMPUTED over the eight-judgment domain | `OnSide(0, 0)` and `OnSide(0, 1)`; every renaming is the identity at one mark | `permitted_renaming_invariant_separating_judgments`; Lean `bounded_invariant_judgment_does_not_separate` (the bounded hypothesis), `invariant_judgment_does_not_separate` (the global hypothesis, which closes less), `onSide_separates_candidates` |
| “which side” as an internal fact | no | yes | the two rows above |
| the presentation convention | invisible up to the permitted reflection | visible; the other convention's candidate is the reflection of the convention's candidate | definition 18; `convention.*` |
| the convention's candidate | `a` on side 0, selected by convention, not admitted | same; the side-1 candidate is a second class, kept | `convention.candidate_event`, `selection_is_by`, `candidate_classes` |
| every continuation of one candidate reflects to one of the other | yes | yes; this carries the second O class without a second tower | Lean `reflect_step`, `reflect_replay`, `continuation_reflects`, `other_continuation_is_a_reflection`; `test_reflect_commutes_with_replay` |
| an event follows from a candidate regime | none | none | `event_follows_relation_empty`; Lean `no_event_follows_admitted` (an instantiation of `no_event_follows`; the relation is empty by definition) |
| initial datum and reading | unchanged by every event and history | same | `initial_datum_unchanged`, `reading_unchanged`; Lean `replay_reading`, `replay_initialDatum` (their steps `step_reading`, `step_initialDatum` are by unfolding) |
| new event kind or judgment form needed | none | none | `event_kinds`, `observation_vocabulary` |
| event-returning functions, by module | kernel: none; presentation: the two constructors; challenge module: the enumerator, the probes, and the two imported constructors | same | `event_returning_functions_by_module`; supplementary census, not the semantic proof |

Three things in this table are decisions and are labelled as such.  The
convention is metatheory: the inscription `<a|>` does not say which
admitted name the left of the bar carries, and under O the two
conventions yield two non-isomorphic candidates.  The run declares one
convention, which selects a candidate and admits nothing; both candidate
classes are kept, and the second O class is carried without a second
tower because every continuation of it is the reflection of a
continuation of the first (Lean `reflect_replay`, `continuation_reflects`,
`other_continuation_is_a_reflection`; the step lemmas
`reflect_step_place`, `reflect_step_supply` alone did not cover histories,
and an earlier version cited only them).  The current state after the
challenge is the replay of the caller's history, the supply alone: the
caller supplied and did not retain, so no admission event is the caller's
and no candidate is current.  An earlier version designated the
convention's admitted candidate as the current state; that turned a
candidate from the run's own enumerator into admitted state without an
admission event from the caller, conflating supply with admission, and is
WITHDRAWN (definition 25).  The one-boundary modelling (the mark is placed
on a side of the one admitted boundary; the whole is not admitted as a
second datum) follows the seed's phrase “the admitted boundary” and is OPEN
as to whether a whole on a side is a datum, which Challenge 5 asks.

#### 5.2 The predictions, scored

| id | label | status | note |
|---|---|---|---|
| C0-X (from Challenge 0) | NOT FORCED | HIT | U: genesis collapsed, every certified candidate not, by one supply and one admission with no new form; O: the sides distinct before and after, the only new holding judgment the mark's own side; scored against the candidates, on which it is conditional |
| C1-1 supply is presentation only | FORCED | HIT, DEFINITION-level | every clause is true by unfolding `step`: `supply_no_op` and `supply_preserves_holds` are `rfl`, and the supply-only history replays to genesis as the n = 1 instance of `replay_supply_inert`, which is `rfl` (B1-SUPPLY-PRESENTATION); HIT by construction and not counted as content, by the rule applied to C1-7; an earlier version counted it (`scores.C1-1.result_basis`) |
| C1-2 admission is separate; the mark is retained | FORCED | PARTIAL | the facts hit: no mark after the supply alone, every candidate certified only with the prior supply, the mark's judgment retained after a supply, a same-side re-admission, and the growth probe, and no accepted event moves or duplicates it (`facts_status`); the frozen parenthetical “a re-admission of the same token on either side, which is designation and not duplication” predicts an accepted other-side re-admission, which the repaired kernel refuses by name, so that clause is false as written and MISSED (`either_side_readmission_clause_status`, from the clause's own fact `moving_admission_accepted_and_inert`); an earlier version labelled it SHARPENED from the overall score with no clause fact, WITHDRAWN; the frozen bare word designation is read here as a re-admission of an already admitted token, not as current-state designation, which the run reserves for its own prose (section 1) |
| C1-3 exactly one new judgment | FORCED | HIT | counted as content: the one new judgment and its evaluation at the candidates rest on `admitted_onSide_true_iff`, `place_new_judgment`, and `place_other_side_false`, none by unfolding (B1-ONE-JUDGMENT); its name clause, read per event as the frozen text has it (“hold after every event exactly as before”), is `step_preserves_sideNamed`, DEFINITION-level, exactly as C1-6's parallel clause was scored, the induction `replay_preserves_sideNamed` being the rung's addition and not the prediction's; its supply clause alone is DEFINITION-level (`scores.C1-3.result_basis`).  An earlier version attributed the name clause to the induction; corrected, no status changing |
| C1-4 the two sides under U | FORCED | PARTIAL | the clause “the admission is the only event in the history” is false as written: each candidate history is one supply and one admission, and a supply is an event by definition 5; the first scoring silently read it as “the only state-changing event”, on which reading it holds; every other clause hits; scored PARTIAL as C0-4 was, the receipt carrying both readings |
| C1-5 the two sides under O, and the convention | NOT FORCED | HIT | the declared convention is the frozen one, left is side 0, which O names `near`, pinned piece by piece (`convention_clause_status`); the candidates are unequal in two classes, the other candidate is the reflection of the convention's candidate, and both are carried (`facts_status`); and the designation is by convention and not by proof, scored on the frozen words: the convention designates, that is selects, a candidate, the selected candidate is the convention's image of the presented side, and the regime under the other convention is the reflection of the designated one (`designation_clause_status`, from `selection_is_by` and `other_is_reflection_of_candidate`); counted as content, the two classes and the absent permitted renaming being COMPUTED over the unpruned search and the inequality PROVED, `admitted_candidates_unequal`, while `reflect_admitted` is `rfl` and is DEFINITION-level (`scores.C1-5.result_basis`); the frozen bare word designation is read as the convention's selection, declared in section 1.  Earlier versions scored a clause “current-state designation of the admitted candidate” MISSED and reported PARTIAL; the frozen text does not contain those words, so that scoring is WITHDRAWN, while the withdrawal of the current-state designation itself stands (definition 25) |
| C1-6 no transition follows | FORCED | HIT, DEFINITION-level | the relation is empty by unfolding `EventFollows := False` (`no_event_follows_admitted` is a bare instantiation); one event keeps the reading and the initial datum by unfolding `step` (`step_reading`, `step_initialDatum`), which is the clause as written, the history-level inductions being the rung's addition and not the prediction's; and the unchanged grammars are a census of the run's own declarations, a modelling decision of the same kind as C1-7's (B1-INERTIA); HIT by construction and not counted as content; an earlier version counted it (`scores.C1-6.result_basis`) |
| C1-7 one boundary, no second datum | NOT FORCED | HIT by construction, DEFINITION-level | the regime type represents neither a second datum nor a second boundary, so the mechanical part cannot be reported false, and `marks == 1` is a proxy reading “the mark placed on a side” as exactly one placed mark, which the frozen text does not name; not counted as content; the modelling clause can only be falsified by a later challenge |
| C1-X extrapolation | NOT FORCED | PENDING | scored by Challenge 2 |

A prediction counts as content only if at least one of its hitting
clauses, read literally, rests on a theorem outside the DEFINITION-level
lists of 7.1 and 7.2 or on a computation not fixed by a declaration alone
(a search, a census over hypothetical placements, an isomorphism
witness); a prediction whose every clause is true by unfolding a
declaration, or reports a modelling decision of the run, is HIT by
construction and not counted, which is the rule of `PLAN.md`.  The list
of such predictions is declared in the scorer and reported as the
receipt's `tally.definition_level_declared`, and the counts that follow
are the receipt's `tally`, computed from the statuses.  Two of seven hit
as content (C1-3, C1-5); three hit by construction and are
DEFINITION-level, not counted as content (C1-1, C1-6, C1-7); two are
PARTIAL (C1-2, C1-4); and C0-X hit in both halves, as content, its profile
clauses being PROVED (B0-X).  An earlier version of this section scored
seven of seven; a later one five of seven, with C1-2's parenthetical
labelled SHARPENED and C1-7 counted as a hit; a third three of seven as
content, with C1-1 and C1-6 counted while C1-7 was excluded on the same
rule; and a fourth one of seven as content, with C1-5 PARTIAL on a clause
scored as “current-state designation”, words the frozen text does not
contain.  All four are WITHDRAWN: C1-1's facts are exactly the ones
B1-SUPPLY-PRESENTATION labels DEFINITION, C1-6's clauses are the empty
relation by declaration, the step lemmas by unfolding, and a census of
the run's own grammars, and C1-5's designation clause, scored on its own
words, hits.  That last is the one status change across the re-counts,
PARTIAL to HIT, recorded next to its value in the receipt, the status,
and the ledger.  The two PARTIAL scores come from scoring the frozen text
literally rather than on a silently weakened reading: each PARTIAL
prediction's facts hit and one of its clauses is false as written, scored
by its own receipt fact; the same literal rule re-scored C1-5, in the
other direction.  Five of the seven were labelled FORCED; where they hit,
they follow from Challenge 0's definitions plus the admission event
Challenge 0 declared, and the two FORCED PARTIALs (C1-2, C1-4) each
overstated an event-level clause.  The NOT FORCED C1-5 concerned a
decision the run made, the declared convention, whose identity is now
pinned literally so that the other convention would miss it.  The hit
rate is evidence of the order of the work, not of insight.

#### 5.3 What Challenge 1 does not establish

- Nothing about two marks.  The retention probe's second admission is
  hypothetical and its token was never supplied by the caller.
- Whether `<a|>` re-supplied at Challenge 2 is the same presentation as
  this one, or whether `<|a>` with the same glyph is a second mark: the
  kernel's `Supply` carries the token only, and the Challenge 0
  token-uniqueness rule would turn a second whole with the same token
  into a same-side no-op or a refused moving admission of the first mark.
  Challenge 2 must decide this loudly.
- No unbounded theorem for the isomorphism relation; its agreement with
  the canonical key is checked to three marks.  Under O, “related by no
  permitted renaming” is a computation over the unpruned search, not a
  Lean theorem: the Lean one-mark relation reduces to raw inequality
  there, and its adequacy for one mark is prose.
- Nothing about what Challenge 2's “retains” admits, or who pays for it.
  Challenge 1 admits nothing; the candidates show what an admission would
  do.
- Nothing about depth, nesting, or the outside of the boundary.

#### 5.4 Dependence on the admitted boundary

| result | dependence |
|---|---|
| supply is presentation only | independent of the boundary |
| the current state is the replay of the caller's history | independent of the boundary |
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
in this repository.  Fifty-six theorems, every one with a `#print axioms`
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

DEFINITION-level, true by `rfl`, by unfolding a declaration, by
substitution, or by a case split onto `rfl`, and not counted as content:
`supply_no_op`, `step_changes_only_by_place`, `genesis_initial_datum`,
`genesis_placement_nil`, `side_names_distinct`, `reflect_genesis`,
`reflection_permitted_U`, `reflection_not_permitted_O`,
`replay_deterministic`, and `no_event_follows`.  The content is the
induction lemmas `map_not_not`, `reflect_reflect`, and
`replay_supply_inert`, the theorem `reflect_moves_a_mark`, and the
evaluations at genesis.  An earlier version of this section carried no
such sentence while 7.2 did, so the same `rfl` shape was DEFINITION-level
at Challenge 1 and PROVED at Challenge 0; one theorem carries one label,
and the ledger and the Challenge 0 status now agree with this list.

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
| `admitted_onSide_true_iff` | exactly one mark-on-side judgment holds in the candidate regime `admitted rd s` | propext, Quot.sound |
| `admitted_U_no_sideNamed` | under U no side-name judgment holds after admission | propext |
| `admitted_O_sideNamed` | under O the name judgments hold as at genesis | propext |
| `admitted_contents_placed` | the placed side's extension is the one mark | propext, Quot.sound |
| `admitted_contents_other` | the other side's extension is empty | propext, Quot.sound |
| `admitted_sides_differ` | the two profiles differ after one mark, either reading | propext, Quot.sound |
| `reflect_step_supply` | the reflection commutes with a supply | none |
| `reflect_step_place` | the reflection carries a placement to the other side | propext |
| `exchangeSide_exchangeSide` | the side exchange of an event is an involution | propext |
| `map_exchangeSide_map_exchangeSide` | the side exchange of a history is an involution | propext |
| `reflect_step` | one step commutes with the reflection up to the side exchange of the event | propext |
| `reflect_replay` | replay commutes with the reflection: the reflection of a replayed history is the replay of the side-exchanged history from the reflected base | propext |
| `reflect_admitted` | the two candidates are each other's reflection | none |
| `continuation_reflects` | the reflection of a continuation of one candidate is the side-exchanged continuation of the other | propext |
| `other_continuation_is_a_reflection` | every continuation of the other candidate is the reflection of a continuation of the first | propext |
| `admitted_candidates_unequal` | the two candidates are unequal as raw data | propext |
| `candidates_related_U` | under U the candidates are related by the one-mark relation; both halves are by unfolding, the permission and `reflect_admitted` | none |
| `candidates_not_related_O` | under O the one-mark relation does not relate them; under O that relation is raw inequality by unfolding, so this restates `admitted_candidates_unequal` | propext |
| `invariant_judgment_does_not_separate` | a reflection-invariant judgment holds equally at both candidates; its hypothesis is invariance at every regime, stronger than the bounded notion | propext |
| `bounded_invariant_judgment_does_not_separate` | a judgment invariant under the reflection at every regime of the reading with at most one mark holds equally at both candidates; under U that hypothesis is definition 26's bounded invariance | propext |
| `onSide_separates_candidates` | the placed mark's own judgment separates them as raw data | propext, Quot.sound |
| `no_event_follows_admitted` | no event follows from a candidate regime; an instantiation of `no_event_follows` | propext |

No countermodel is needed at Challenges 0 or 1: no target failed.
DEFINITION-level, true by unfolding or by instantiating a Challenge 0
theorem, and not counted as content: `admitted_eq`,
`supply_preserves_holds`, `step_reading`, `step_initialDatum`,
`step_preserves_sideNamed`, `reflect_step_supply`, `reflect_admitted`,
`candidates_related_U` as a whole, the permission half of
`candidates_not_related_O`, and `no_event_follows_admitted`.  An earlier version of this sentence listed
five of these and counted `step_preserves_sideNamed` and
`no_event_follows_admitted` as content, although the first has the same
by-unfolding shape as the listed step lemmas and the second is a bare
instantiation; that inconsistency is repaired here.  A later version
listed `reflect_step` as a case split onto `rfl`; its place branch is
`reflect_step_place`, a Challenge 1 lemma proved by `simp` with the map of
a placement over an append and carrying `propext`, so `reflect_step` is
PROVED through it and is removed from this list, and `reflect_step_place`,
`exchangeSide_exchangeSide`, and `map_exchangeSide_map_exchangeSide` are
labelled PROVED in B1-REFLECT-COMMUTES.  A third version proved
`reflect_admitted` by `simp [reflect]`, called it the content of
`candidates_related_U`, and carried the `simp`'s `propext` in the axiom
log; the statement is true by unfolding, both sides reducing to the
one-element placement exactly as `reflect_genesis` reduces on the empty
one, so the proof is now `rfl`, both theorems are DEFINITION-level and
axiom-free, and C1-5's content rests on `admitted_candidates_unequal` and
the unpruned search.  The content the ledger relies on
is the induction lemmas (`replay_reading`, `replay_initialDatum`,
`replay_preserves_sideNamed`, `replay_preserves_onSide`, `reflect_replay`,
`replay_supply_inert`), the step lemma `reflect_step_place` with the two
involution lemmas, and the evaluations at the candidates.

## 8. Receipts

- `receipts/challenge0.json` and `receipts/challenge1.json`: deterministic
  (sorted keys, LF, no timestamp, no environment value); regenerated
  byte-identically by `run_challenge0.py` and `run_challenge1.py` and
  checked by the tests and by the research job.
- The Challenge 1 receipt was regenerated deliberately once more at the
  third review repair, when the DEFINITION-level bases of C1-1, C1-3, and
  C1-6 and the prediction tally became receipt keys, and once more at the
  fourth, when C1-5's clauses were scored on the frozen words and the
  convention pinned, and once more at the fifth, when C1-7's evidence was
  rescoped to the candidate regimes, C1-5's basis relabelled, and the two
  designation clause facts reworded, with no injection live any time.
- The suite passes 114 tests.  Fresh coverage over the five declared code
  files is 100.00% line and 100.00% branch; `check_coverage.py` computes
  line coverage as covered lines divided by statements rather than
  Coverage.py's combined line-plus-branch percentage.
- `lean/axioms.txt`: 56 reports, regenerated once at Challenge 1 when the
  theorem set was final, once more at the Challenge 1 review repair, when
  six theorems were added, once more at the second review repair, when one
  was added, and once more at the fifth, when `reflect_admitted` became
  `rfl` and two reports lost their `propext`; no regeneration was under a
  live injection.
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
every judgment holds as before: the supply is presentation only, and the
current regime after the challenge is genesis, because the caller supplied
and did not retain and the current state is the replay of the caller's
history, `[Supply(a)]`, in which `a` is supplied and nothing is admitted.
The mark would enter the admitted state only through the separate
admission event, which no history of the caller's contains at this
challenge; the two candidate admissions are certified and kept as
branches, none current.  In a candidate, once admitted the mark's
judgment survives every later event of the Lean grammar, and the Python
kernel additionally treats a re-admission on the mark's own side as a
no-op and refuses one that would move it.  A candidate admission adds
exactly one holding judgment, the mark's side, and changes no name
judgment, the initial datum, or the reading.  Under U it would take the
two sides from collapsed to distinct; the two candidate one-mark regimes
are each other's reflection and related by the permitted reflection, so
no permitted-renaming-invariant judgment of the bounded domain says which
side the mark is on.  Under O the sides were already distinct by name; the
two candidates are unequal, related by no permitted renaming (a
computation over the unpruned search; the Lean one-mark relation, which
is raw inequality under O, does not relate them), and the mark's own
judgment separates them, so which named side it lies on would be internal
— at the price of the O declaration and of a metatheoretic presentation
convention the inscription does not fix, and only once an admission is
called for.  Every continuation of either candidate is the reflection of
a continuation of the other, by a replay-level theorem.  No event follows
from any of these states.  These are scoped Lean theorems, bounded
computations, or labelled definitions and conventions.  Because the
instrument declared prior exposure, they carry no blind-independence or
independent-discovery conclusion.

## 10. Limitations and open obstructions

- The class-count closed forms and the equal-count law are computations
  to four marks, not theorems.
- No unbounded completeness or injectivity theorem is claimed for
  `canonical`; its evidence is the finite census, focused invariance
  tests, and agreement with the witness search to three marks.
- The Lean one-mark relatedness is intended for one mark only, and that
  adequacy is prose; under O it reduces to raw inequality.  The general
  isomorphism relation, mark permutations included, is Python, so “related
  by no permitted renaming” under O is COMPUTED and not PROVED.  The
  identification of `bounded_invariant_judgment_does_not_separate`'s
  hypothesis with the Python bounded invariance under U is by the same
  kind of inspection: at one mark the permitted renamings are the identity
  and the reflection.
- The reflection census and the retention probes enumerate hypothetical
  placements and events that no history admits; they are metatheory about
  the kernel, and they admit nothing.
- The presentation convention is metatheory.  Under O the candidate it
  selects depends on it; the other convention's candidate is carried as
  the reflection of it, by the replay-level theorem `reflect_replay`, not
  by a second tower.  The convention admits nothing, and nothing at
  Challenge 1 is admitted: what Challenge 2's “retains” admits, and who
  pays, is Challenge 2's first decision.
- The re-admission no-op and the moving-admission refusal are Python-only
  declarations; the Lean events carry no token, so the Lean retention
  theorems cover supplies and new placements only.
- Whether a whole on a side is itself a datum is OPEN for Challenge 5; the
  one-boundary modelling at Challenge 1 is a decision.
- `Supply` carries the token only.  Challenge 2 must say whether the two
  wholes with the same glyph are one presentation or two, and must not let
  token uniqueness turn the second into a same-side no-op or a refused
  moving admission silently.
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
