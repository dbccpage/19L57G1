# The boundary derivation: Challenges 0 to 4 under declared prior exposure

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
Challenges 1 to 4 were each closed in a fresh session under the same
ceiling; each status records where a remembered shape was used.

One further channel is material and is disclosed here rather than only in
the statuses.  Each rung is read by an adversarial review outside the run,
whose findings arrive as advisories at the start of the next session; every
advisory is actioned or carried with its reason in that challenge's
`STATUS.md`.  Through Challenge 4 that channel has supplied more than thirty
actioned repairs and the design of two gates — the Lean audit-totality check
at Challenge 2 and the independent placement check at Challenge 3 — so a
reader should not treat the apparatus as the run's unaided work.  It does
not supply object-language content: no advisory has proposed a definition, a
candidate, or a result, and the run's results are its own.  That distinction
is the run's own account of the channel and is not itself checked by
anything.

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
certifying `replay` refuses an admission whose token was not presented
first, and low-level `step` treats a re-admission of an admitted token on
its own side as a no-op and raises the refusal of one naming the other
side, because it would move the mark — certifying `replay` calls `step`
and so surfaces both refusals, but the second is raised by `step`, which
is where definition 6 puts it, and an earlier version of this sentence
attributed it to `replay` (all three are Python-only declarations; the
Lean events carry no token); the word designation is reserved for
current-state designation, the current state being the replay of the
caller's history, and an earlier use of it for the re-admission no-op is
WITHDRAWN; retention is the placement tuple, and it is proved that every
later event of the Lean grammar preserves an admitted mark's judgment;
observation is the closed judgment grammar above; regime equality is
structural and is never conflated with the isomorphism relation.  The
canonical key is a bounded-computation tool for quotienting in the
reported census, not an unbounded completeness theorem.

**Two equalities, and where they differ.**  Python `Regime` equality
compares the presentation tokens as well as the reading and the placement;
the Lean `Regime` carries no token, so its equality cannot.  The Lean
regime is the Python regime with tokens forgotten, which is what
`serialize` computes, and Lean equality is `serialize` equality.  Through
Challenge 1 the two coincided on everything the run compared, because
every regime carried at most one token; at Challenge 2 they part, because
the caller's two wholes carry the same visible mark and a relabelling
changes the Python regime while changing no Lean one.  The run reports
both: the relabelled regime is unequal and isomorphic
(`readings.*.label`), so the visible mark is presentation and not an
internal fact.

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
and the run retains a tied branch from Challenge 3 on.  A candidate class
the run does not drop is *kept*: it stays a certified branch, and keeping
it admits nothing.  An earlier version called kept candidate classes
retained, a second undeclared sense of a word the seed lists among those
never to be conflated, and that use is WITHDRAWN.

Challenge 2 decided the caller's sense.  The caller's “retains” is read as
the admission of both wholes, so that the caller's history contains one
admission per whole and the placement tuple carries both marks: the
caller's sense and the placement sense coincide from that rung on, by the
decision recorded in definition 30 and priced in definition 31.  That is a
decision of the run, not a reading forced by the word, and the run could
instead have refused the challenge and recorded it OPEN.

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
in `code/boundary/presentation.py`; 20 to 26 in `model.py` and
`code/boundary/challenge1.py` as marked; 29 to 35 are Challenge 2's, in
`model.py` and `code/boundary/challenge2.py` as marked; 37 to 46 are
Challenge 3's, in `model.py` and `code/boundary/challenge3.py` as marked;
47 to 58 are Challenge 4's, in `presentation.py`, `model.py`, and
`code/boundary/challenge4.py` as marked.
Definitions 27, 28, and 36 are **Lean-only** and have no Python counterpart,
as their headings say.  Two earlier versions of this sentence were wrong:
the first placed 20 to 27 in the Python modules while 27 and 28 were marked
Lean, and the second placed 29 to 36 in the Python modules although 36 is
Lean-only as well; both are corrected here.  The theorem-bearing subset
listed in section 7 is mirrored or abstracted in `lean/BoundarySeed/`;
presentation tokens, certifying supply-before-admission replay, the
canonical key, the reader, the convention, the identity policies, and the
whole Challenge 3 candidate space are Python-only.

1. **Initial datum.**  One opaque supplied whole.  Its presentation
   spelling is not stored.  Its `internal_id` is `0`, a name in the
   identity space of supplied wholes, which is not the identity space of
   marks: the two share a numeral and nothing else.
2. **Boundary and reading.**  The admitted boundary has two sides.  U
   leaves them unnamed; O admits the names `near` and `far`.
3. **Regime.**  The fixed initial datum, a reading, one presentation
   label for each admitted mark, and one valid side for each mark.
   **A mark's internal identity is its position in the admission order**:
   the index into the placement tuple, assigned when the mark is admitted.
   That assignment is a modelling decision, classified as metatheory
   apparatus, and it is the one place where identity and order meet in the
   model.  Order is not thereby made observable: definition 13 permits the
   mark permutations under both readings, so the index is a metatheoretic
   name and not internally available, and Challenge 2 computes that the
   admission order of two retained wholes is carried away by a permitted
   renaming (definition 34, result table 5.5).  The presentation label
   beside a mark is not its identity.  Construction rejects unknown
   readings, invalid sides, and length mismatch.  Challenges 0 and 1
   additionally rejected a repeated label, which identified presentation
   identity with internal identity; that requirement is WITHDRAWN at
   Challenge 2 (definition 31), where the caller's two wholes carry the
   same visible mark.  An earlier version of this definition stated
   neither the index rule nor the two identity spaces.
4. **Genesis.**  The initial datum is present and no later mark is admitted.
5. **Events.**  `Supply(token)` is external presentation;
   `AdmitMark(token, side)` is a requested admission.
6. **Step, replay, certification.**  Low-level `step` applies an already
   validated event: a supply changes nothing; a token-keyed admission of a
   new token places it; one naming an admitted token on its own side is a
   no-op; one naming the other side would move the mark and is refused by
   name; and, from Challenge 2, one whose token labels more than one
   admitted mark is refused by name, because a token-keyed admission
   cannot say which mark it names there (definition 31).  Certifying
   `replay` tracks presentations and refuses an admission whose token was
   not presented first; `certify` rejects a refused history.  The no-op
   and all three refusals are Python-only: the Lean `place` carries no
   token.
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
29. **Internal fact.**  A property of a regime, or of a mark or side in
    it, is an *internal fact of the reading* when it is invariant under
    every permitted renaming of that reading (definition 23).  Anything
    not so invariant is a fact of the presentation or of the metatheoretic
    naming, not of the state.  **The invariance is over the token-forgetting
    quotient of definition 14**: a permitted renaming carries the
    presentation labels along with their marks, and the serialization the
    comparison uses forgets them, so a property that reads a label is not an
    internal fact by this definition.  That clause is what stops presentation
    identity being readmitted as an internal fact by the definition written
    to exclude it, and it is the test the label row of 5.5 actually applies.
    It also fixes the scope of definition 33's justifying sentence below.
    Challenge 3's third coordinate withdraws exactly this clause and prices
    the withdrawal (definition 40).  Challenge 1's table used this notion under
    the name “internal fact” with no numbered definition, which made the U
    answer follow at once from the candidates being related by a permitted
    renaming; that implication is exactly what the notion says, and what
    was computed at Challenge 1 was the antecedent — that the two
    candidates *are* so related — not the implication.  The definition is
    numbered here so that the two are not confused again.
30. **Retention by the caller (Challenge 2).**  The caller's “retains” is
    read as the admission of the retained whole: the caller's history
    contains, for each retained whole, a `Supply` and an admission, and
    the current state is the replay of that history (definition 25).  A
    decision of the run, not a reading forced by the seed's word.
31. **Identity policy, and the declared space (Challenge 2).**  An
    *identity policy* decides what an admission of an already-presented
    token admits.  The declared space has exactly two: SHARED, under which
    an admission names the mark its token already names — the Challenge 1
    event `AdmitMark` — and OCCURRENCE, under which an admission admits a
    fresh mark and the token is only a label — the Challenge 2 event
    `AdmitOccurrence`.  The space is exhaustive over the caller's two
    wholes because the second admission's target either is or is not a
    mark already admitted, and there is no third answer; nothing is
    claimed about policies that would change the event grammar further.
    The run declares OCCURRENCE.  Its price is one new admission event and
    the withdrawal of definition 3's repeated-label rule, and with them the
    withdrawal of the identification of presentation identity with
    internal identity; the price is paid by the run, is the same under
    both readings, and buys that the caller's two wholes are two marks at
    all.
32. **Permitted automorphism (Challenge 2).**  A permitted renaming
    carrying a regime onto itself with tokens forgotten.  `automorphisms`
    filters the unpruned `permitted_images` enumeration by serialization
    equality.
33. **Internal separability of two marks (Challenge 2).**  Two admitted
    marks are *internally separable under a reading* when no permitted
    automorphism of the regime carries one to the other.  If one does, every
    mark property **that forgets the presentation tokens** and is invariant
    under permitted renamings takes the same value at both, so by definition
    29 nothing internal tells them apart.  The token-forgetting clause is
    needed and was missing from an earlier version of this sentence: a
    permitted automorphism is a renaming of the regime with tokens forgotten
    (definition 32), so it can exchange two marks whose labels differ, and a
    property that reads a label would then separate marks the automorphism
    exchanges.  At the Challenge 2 retained regime the point does not bite —
    both labels are `a`, so the image is equal and not merely equal after
    forgetting — but the sentence was false as a general claim, and
    Challenge 3's third coordinate is exactly the augmentation that withdraws
    the forgetting and is then computed to separate nothing here, both
    retained marks carrying the same label.  The corresponding notion for the
    two sides is that no permitted automorphism includes the reflection.
34. **Mark form, and its invariance (Challenge 2).**  The two *mark
    forms* are the mark properties “this mark lies on side 0” and “this
    mark lies on side 1”.  A form is *permitted-renaming-invariant on a
    bounded domain* when, at every regime of the domain, every permitted
    image of it, and every mark, the form holds of the mark exactly when
    it holds of the mark's image.  The declared domain is every
    hypothetical placement of at most two marks under the reading.
35. **The different-sides property (Challenge 2).**  No two admitted marks
    lie on the same side.  It reads the placement tuple only and is not an
    object-language value; its invariance is computed over every
    hypothetical placement of at most three marks under both readings and
    every permitted image of each.
36. **Mark exchange (Lean, Challenge 2).**  `exchangeFirstTwo` exchanges
    the first two internal identities and fixes every later one;
    `swapFirstTwo` and `exchangeMarks` are its actions on a placement list
    and on a regime.  Both are involutions.
37. **Renamings taken coordinate by coordinate (Challenge 3).**  Definitions
    13 and 16 fix the permitted renamings by the reading: the mark
    permutations always, the side exchange under U.  Challenge 3 must ask
    what a declared augmentation that WITHDRAWS one of those would do, so the
    kernel offers the same unpruned enumeration with each generator as a
    flag: `permitted_images_under`, and with it `automorphisms_under`,
    `mark_automorphism_to_under`, `marks_separable_under`,
    `side_exchanging_automorphism_under`, `is_isomorphic_under`, and
    `canonical_under`.  A third flag chooses the serialization:
    `serialize_keeping_labels` is definition 14 without the token forgetting.
    At the flags the reading declares, each is the Challenge 2 function it
    generalizes, which is checked for the image, automorphism, and
    canonical-key functions over every placement of at most three marks under
    both readings, and for the four separation and isomorphism functions at
    the two-mark placements.  A flag is a declaration of the augmentation
    being examined and is never a discovery.
38. **The required separation (Challenge 3).**  The requirement the caller
    imposes, in the sense the run declares: the two retained marks meet it
    under a reading when no permitted automorphism of the regime carries one
    to the other — definition 33's sense, at the augmentation's renamings
    rather than the reading's.  A second reading is declared beside it: some
    property of a mark that forgets whatever the candidate's declared
    serialization forgets — definition 33's clause, which at the base is
    definition 14's token forgetting and at the label-keeping coordinate is
    nothing — and that is invariant under every permitted renaming, holds of
    one and not of the other.  The clause is part of the reading and not a
    gloss on it: without it a property that reads a label separates marks a
    permitted automorphism exchanges, which is the defect definition 33 was
    repaired to exclude, and `carries_label_a`, which reads a token, is
    reported invariant at the base and at every one-step point under both
    readings, where the property census is reported.  What the receipt
    computes at all 48 points under each reading is the first reading against
    the declared orbit witness of definition 39, not against the existential
    over every such property; the direction back from an arbitrary such
    property to the first reading is definition 33's justifying sentence,
    which is prose.
    The caller's demand is an externally imposed challenge; the sense is a
    derived definition of the run, and a different sense was available.
39. **The orbit of a mark, and the orbit witness (Challenge 3).**  The
    *orbit* of a `(regime, mark)` pair is the set of pairs a permitted
    renaming carries it to, each recorded as the image's key with the index
    the mark is carried to.  Membership in one mark's orbit is a property of
    a pair that is invariant under those renamings **by construction**, and
    it holds of the second retained mark exactly when a permitted
    automorphism carries the first to the second.  So it witnesses the second
    reading of definition 38 whenever the first holds, and that half of the
    agreement is by unfolding rather than by search.  The invariance rests on
    a premise stated here and checked by nothing: that a candidate's
    permitted renamings are closed under composition and inverse.  The
    declared enumerations of definition 37 are — each offers the identity,
    the side exchange where its flag permits it, the mark permutations where
    its flag permits them, and their composites — but that closure is neither
    computed nor proved in this run.
40. **Declared augmentation, and the candidate space (Challenge 3).**  An
    *augmentation* is a value for each of five declared coordinates:
    withdraw the side exchange from the permitted renamings; withdraw the
    mark permutations; admit the two side names into the judgment grammar of
    the reading; keep the presentation labels in the serialization, that is
    withdraw definition 14's token forgetting; and admit one further mark, on
    side 0 or on side 1.  The last takes three values and the others two, so
    the space has 48 points under each reading.  Each coordinate names one
    capability, listed in the receipt's `candidate_space.capability_of`.
    The space is exhaustive over those five coordinates and over nothing
    wider: it does not enumerate an augmentation that changes the event
    grammar again, that admits more than one further mark in one step, that
    supplies a datum the caller never presented, or that derives the
    permitted renamings from the judgment grammar instead of declaring them.
    Every minimality statement of this rung is scoped to it.
41. **The capability count, and the one-step rule (Challenge 3).**  The first
    declared cost measure, `mu1`, is the number of undeclared capabilities a
    candidate uses, one for each coordinate it moves off its inherited value.
    **The two identifiers `mu1` and `mu2` are inherited vocabulary, not this
    run's.**  They are the sealed derivation's own names for its two declared
    cost measures over a candidate space of one-step augmentations, and the
    repository contract file, which the harness loads whole, says so; this
    run introduced them for the same role without noticing.  What the two
    measures ARE here is this run's, declared at this definition and at 44
    and computed; the names are inheritance, and are recorded as such so that
    no later comparison reads the coincidence as convergence.  Found by
    review, not by the run, and disclosed here as well as in the status.
    A candidate is *one step* exactly when it moves one coordinate, which is
    exactly when its count is one; a candidate of count two or more **bundles
    capabilities and is refused as a one-step augmentation**, as the seed
    requires.  Adopting reading O under U — the names together with the
    withdrawal — is such a bundle.
42. **Effective structure, and the quotient of candidates (Challenge 3).**
    The *effective structure* of a candidate under a reading is what it
    actually declares once the reading is applied: whether the side exchange
    is permitted, whether the mark permutations are, whether the names are
    admitted, and whether the labels are kept.  Two points with the same
    effective structure and isomorphic regimes are the same candidate; under
    O, withdrawing an already absent side exchange and admitting already
    admitted names change nothing and collapse into the null point.  The
    implemented class key is the effective structure together with
    `canonical_under` at that structure's own renamings, and it is the only
    sanctioned quotient of candidates.
43. **Mark property, and its bounded invariance (Challenge 3).**  A *mark
    property* is a property of a `(regime, mark)` pair; definition 34's two
    mark forms are two of them.  Five are declared: lies on side 0, lies on
    side 1, has index 0, has index 1, and carries the label the caller
    supplied.  A property is *invariant on the bounded domain* when, at every
    regime of the domain, every image permitted by the candidate, and every
    mark, it holds of a mark exactly when it holds of that mark's image.  The
    declared domain is every regime of at most three marks over the two
    declared labels, 85 per reading — wider than definition 34's, because a
    candidate regime may carry three marks and because a label-reading
    property needs two labels to be tested at all.
44. **The collateral facts, and the second measure (Challenge 3).**  Five
    facts about the retained configuration are declared: the two sides are
    internally separable; the retention order of the two wholes is internally
    available; the shared presentation label is; the presentation convention
    is; and a side-name judgment holds.  Each is computed at the candidate's
    own renamings and serialization by the same witness searches Challenge 2
    used.  The second declared cost measure, `mu2`, is the number of them a
    candidate makes available **that the same reading's base did not**.  It
    was declared so as to read what a candidate costs beside what it was
    asked for, and it does not do that: the required separation is not one of
    the five, but the first of them is that separation said of the two SIDES,
    and the enumeration computes that it takes the requirement's value at
    every one of the 48 points under each reading
    (`sides_fact_agrees_with_the_requirement_at_every_point`).  So where the
    base fails the requirement — under U — a satisfying candidate's count
    always includes that one fact, and to that extent the measure re-counts
    the requirement rather than excluding it.  The declared list is reported
    as it stands and not repaired: changing it after the enumeration would be
    fitting the declaration to the answer.
45. **The process's own admission (Challenge 3).**  The further-mark
    coordinate extends the caller's history by one `AdmitOccurrence` of the
    token the caller already supplied.  It needs no supply of its own, which
    the receipt computes, and a token the caller never presented is refused
    by name, which it also computes.  The one capability it uses is therefore
    not a supply but the issuing of an event by the process rather than by
    the caller: definition 25 makes the current state the replay of the
    *caller's* history, and this coordinate is the first thing in the run
    that would step outside it.  No such event is in any history the receipt
    reports as current; every candidate is a candidate.
46. **The counterfactual square (Challenge 3).**  The requirement at the
    retained regime over the two coordinates (the names admitted or not) by
    (the side exchange permitted or not), four cells under each reading, with
    the cell that is the reading's real one marked.  It isolates which half
    of the O declaration does the work.  That the names cannot enter the
    computation is definition 16 — permission is declared, not derived from
    the judgment grammar — so the square exhibits that declaration's
    consequence and does not discover it.

47. **The widened reader (Challenge 4).**  Metatheory apparatus.
    `read_pair_whole` reads a whole with at most one mark on EACH side of the
    bar; two marks on one side, and a nested whole, are refused by name.  The
    Challenge 1 reader of definition 17 keeps its narrower bound and refuses
    both of the caller's Challenge 4 inscriptions by name, which the receipt
    computes, and it is left refusing so that what forced the widening stays
    visible.  The widening is a declared augmentation of the metatheory, paid
    by the run at this rung.  Nothing beyond a mark per side is read: the
    reader refuses `<<a|>|>`, and what a whole within a side is belongs to
    Challenge 5.
48. **The within-whole admission order (Challenge 4).**  Metatheory
    apparatus.  In which order the two marks of one whole are admitted is a
    declaration of the same kind as the convention (definition 18): two
    orders exist, the declared one admits the left mark first, and the
    inscription decides neither.  The other order is computed to give an
    isomorphic configuration under both readings at the base.
49. **The caller's Challenge 4 retention.**  Under definition 30's reading of
    "retains" and the Challenge 2 occurrence identity (definition 31), the
    caller's history is, for each retained whole, a `Supply` for each of its
    marks in presented order and then an `AdmitOccurrence` for each in the
    declared within-whole order: eight events.  The current state under each
    reading is its replay — four admitted marks, placement `(0, 1, 0, 1)`,
    labels `("a", "b", "b", "a")`.  Supply, admission, and retention stay
    three things: a whole is presented once and presents both its marks, and
    each mark is admitted by its own event.
50. **The whole grouping (Challenge 4).**  Metatheory apparatus.  For each
    admitted mark, the tag of the presented whole whose admission introduced
    it; the caller's two wholes are tags 0 and 1, and a further mark the
    process admits carries a tag of its own, belonging to no whole the caller
    presented.  **The regime carries no such component.**  The grouping is
    read off the caller's history, so the requirement below is a statement
    about the automorphisms of the state and about a structure the state does
    not carry — and so is its declared witness — at every candidate that does
    not admit the grouping.  That is recorded as a narrowing of what internal
    separability can mean for a whole, and it is why the grouping is one of
    the declared coordinates.
51. **Configuration and declared renamings (Challenge 4).**  A
    *configuration* is a regime together with a grouping; `Renamings` collects
    the five flags a declared augmentation sets: whether the side exchange is
    a permitted renaming, whether the mark permutations are, whether the
    exchange of the two caller tags is, whether the key keeps the presentation
    labels, and whether it keeps the group tags.  The tag exchange is a
    permitted renaming exactly when the grouping is admitted and the two
    wholes are not named — the tag-level counterpart of the side exchange
    under reading U, and a declaration of this rung, not a discovery.  At the
    flags a reading declares with no augmentation these reduce to definitions
    13, 14, and 16 with the grouping ignored, which is checked.
52. **Whole separability (the Challenge 4 requirement).**  The requirement the
    caller imposes, in the sense the run declares: the two retained wholes
    meet it under a reading when no permitted automorphism of the
    configuration carries the mark-set of one onto the mark-set of the other.
    It reduces to definition 38's sense at the Challenge 3 configuration,
    where each whole is a single mark, which the receipt computes under both
    readings rather than asserting — but the agreement there is
    **DEFINITION-level**, not a result: with each whole a single mark the
    set test of the whole sense unfolds to the mark test of the pointwise
    sense over the same list of automorphisms, so the two cannot disagree at
    that configuration and the frozen falsifier naming that disagreement
    cannot fire.  The caller's demand is an externally imposed challenge; the
    sense is a derived definition of the run, and a different sense was
    available.
53. **The pointwise sense (Challenge 4).**  Definition 33 taken over every
    pair: every pair of distinct admitted marks is separable.  It is declared
    beside the requirement and computed beside it; the receipt computes that
    it implies the requirement at every point of the declared space and that
    the converse fails somewhere in it.
54. **The orbit of a whole, and the orbit witness (Challenge 4).**  The
    *orbit* of a `(configuration, mark-set)` pair is the set of pairs a
    permitted renaming carries it to, each recorded as the image's key with
    the mark-set the renaming carries it onto.  Membership in the first
    whole's orbit is a property of such a pair invariant under those renamings
    **by construction**, and it holds of the second whole's mark-set exactly
    when a permitted automorphism carries the first onto the second.  So it
    witnesses the second reading of definition 52 whenever the first holds,
    and that half of the agreement is by unfolding rather than by search.  As
    at Challenge 3, the invariance rests on a premise stated here and checked
    by nothing: that a candidate's permitted renamings are closed under
    composition and inverse.
55. **The declared whole properties, and what makes one a witness
    (Challenge 4).**  A *whole property* is a property of a
    `(configuration, mark-set)` pair; definition 34's two mark forms are the
    first two of the five declared here, read of a set: the set has a mark on
    side 0; it has a mark on side 1; it contains the first admitted mark; it
    carries the first caller token on side 0; and it is the mark-set the first
    caller tag groups.  A property is *invariant on the bounded domain* when,
    at every configuration of the domain, every image the candidate permits,
    and each of the two declared tags, it holds of a whole exactly when it
    holds of that whole's image.  It is *determined by the candidate's key*
    when any two configurations of the domain with equal keys give it equal
    values at every two-element mark-set.  **Only a property that is both, and
    that separates the two retained wholes, witnesses the separation.**  The
    second conjunct is definition 29's token-forgetting clause generalized,
    and it is load-bearing here rather than latent: without it the property
    that reads the group tag is invariant under every permitted renaming at
    the base and separates the two wholes there, so a census of invariance
    alone reports a witness at the very point where the requirement fails.
    That was live in this rung's first census and is recorded, with the
    injection that reproduces it, in `MANUAL.md`.  The declared domain is
    every configuration of two two-mark wholes over the two declared labels
    and the three ways four marks fall into two wholes of two: 768 per
    reading.  The grouping varies because a property that reads the tag must
    be tested against configurations whose grouping differs while their key
    does not.
56. **The Challenge 4 candidate space, the capability count, and the one-step
    rule.**  An *augmentation* is a value for each of seven declared
    coordinates: the five of definition 40 together with admitting the whole
    grouping and naming the two wholes.  The further-mark coordinate takes
    three values and the others two, so the space has 192 points under each
    reading.  Each coordinate names one capability, listed in the receipt's
    `candidate_space.capability_of`; the first measure is the number of
    coordinates a candidate moves off its inherited value, a candidate is
    *one step* exactly when that count is one, and a candidate of count two or
    more **bundles capabilities and is refused as a one-step augmentation**.
    The space is exhaustive over those seven coordinates and over nothing
    wider: it does not enumerate an augmentation that changes the event
    grammar again, that admits more than one further mark in one step, that
    supplies a datum the caller never presented, that groups marks by anything
    but the presented whole, or that derives the permitted renamings from the
    judgment grammar.  Every minimality statement of this rung is scoped to
    it.
57. **The Challenge 4 effective structure and class key.**  The effective
    structure adds the two grouping flags to definition 42's four, so two
    points that declare the same renamings and the same key are the same
    candidate: under O the two O-carried coordinates still collapse, and under
    both readings naming the wholes without admitting the grouping changes
    nothing and collapses into the null point.  The implemented class key is
    the effective structure together with the least key of the candidate's
    configuration under its own renamings, and it is the only sanctioned
    quotient of candidates.
58. **The collateral facts and the second measure (Challenge 4).**  Eight
    facts about the retained configuration are declared: the two sides are
    internally separable; every pair of admitted marks is separable; the order
    in which the two wholes were retained is internally available; the order
    within a whole is; the presentation labels are; the matching of a visible
    mark across the boundary is — that is, the configuration in which the
    second whole's copy of the first token is a token the caller never
    presented is not reached by a permitted renaming; the presentation
    convention is; and a side-name judgment holds.  The second measure is the
    number of them a candidate makes available **that the same reading's base
    did not**.  Challenge 3 found its own first declared fact taking the
    requirement's value at every point, so that its second measure re-counted
    the requirement; here the two facts nearest the requirement — the first
    and the second of the eight — are each computed against it at every point
    of the space, and neither agrees with it everywhere.

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
| “which side” as an internal fact (definition 29) | no | yes | the two rows above.  Under U the “no” follows at once from the candidates being related by a permitted renaming, which is what definition 29 says; the computed and proved content is the antecedent, that they are so related, not the implication |
| the presentation convention | invisible up to the permitted reflection | visible; the other convention's candidate is the reflection of the convention's candidate | definition 18; `convention.*` |
| the convention's candidate | `a` on side 0, selected by convention, not admitted | same; the side-1 candidate is a second class, kept | `convention.candidate_event`, `selection_is_by`, `candidate_classes` |
| every continuation of one candidate reflects to one of the other | yes | yes; this carries the second O class without a second tower, and what it carries are the SIDE-EXCHANGED facts of the first class: under O the reflection is not a permitted renaming, so it moves placements and not names, and the second class's facts are the first class's with every side exchanged and the two names left where they are | Lean `reflect_step`, `reflect_replay`, `continuation_reflects`, `other_continuation_is_a_reflection`; `test_reflect_commutes_with_replay` |
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

### 5.5 Challenge 2: the caller retains `<a|>` and `<|a>`

Receipt: `receipts/challenge2.json`.  Predictions frozen at sha256
`95f9371b030b8df64b4842a5df7be695d9e7f1b2311a300e78d915a701c16474` in
commit `22d9ea4b`, before the branch's first Challenge 2 code-or-proof
commit.  Git establishes that committed order only; it does not establish
when off-tree or untracked work was written.

The caller supplies and **retains** both wholes: the same visible mark,
the other side.  Two decisions come first, and both are recorded as
decisions.

**What “retains” licenses** (definition 30): the admission of both
wholes, so the caller's history is a supply and an admission for each,
and the current state under each reading is its replay — a regime with
two marks.  This is the first rung at which the caller's history contains
an admission; Challenge 1 admitted nothing and nothing was inherited.
The two supplies are the same event value twice, separated only by their
position, and they change nothing.

**What the shared visible mark costs** (definition 31): with the
Challenge 1 admission event the caller's history is **refused by name**,
under both readings and under both conventions, by the moving-admission
refusal — the token-keyed admission reads the second whole as naming the
first mark and asking for it on the other side.  The declared space of
identity policies has exactly two members, and exactly one of them lets
the caller retain both wholes.  The run declares that one; its price is
one new admission event, `AdmitOccurrence`, and the withdrawal of
definition 3's repeated-label rule.  **The run pays it, not the boundary
and not the caller**, and pays the same under both readings.  This is the
rung's one augmentation, and Challenge 1's C1-6 clause “Challenge 1
justifies no augmentation of the event or judgment grammar” is not
disturbed by it: the judgment grammar is unchanged, and the event grammar
grew at Challenge 2 and for Challenge 2's reason.

| result | reading U | reading O | evidence |
|---|---|---|---|
| the retained state | two marks, placement `(0, 1)` under the declared convention, labels `("a", "a")`; certified and replayed from genesis | same | `readings.*.retained`; Lean `retained_eq` (DEFINITION-level, `rfl`), `retained_placement_length` |
| the caller's history under the Challenge 1 admission event | refused by name, under both conventions: the moving-admission refusal | same | `identity_policies.rows`; DEFINITION-level, the Challenge 1 declaration replayed |
| policies of the declared space that retain both wholes | exactly one, the declared one | same | `identity_policies.declared_is_the_only_one_admitting_both`; the space is exhaustive over the caller's two wholes by definition 31, and the claim is scoped to it |
| what admission adds | exactly two holding judgments, `OnSide(0, 0)` and `OnSide(1, 1)`; 0 to 2 | the same two; 2 to 4, the two name judgments unchanged | `retained.new_observations`, `holding_judgments_*`; Lean `retained_onSide_true_iff`, `retained_onSide_zero`, `retained_onSide_one`, `retained_onSide_beyond`, `retained_sideNamed` |
| each mark's profile | its own side, nothing else | same | `separation.mark_profiles`; definition 22 |
| retention of both marks | both judgments hold after a further supply and a further admission | same | `retained.later_events`; Lean `retained_judgments_survive` |
| the Challenge 1 admission event on the retained regime | refused by name: the label names two marks | same | `retained.later_events.token_keyed_refusal`; the withdrawn identification made visible |
| permitted automorphisms of the retained regime | exactly two: the identity, and the reflection with the exchange of the two marks | exactly one: the identity | `automorphisms.count`, `entries`; COMPUTED over the unpruned `permitted_images` search; the concrete composite is Lean `exchangeMarks_reflect_retained` (DEFINITION-level, `rfl`) with `retained_composite_permitted_U` |
| the two retained marks, internally separable (definition 33) | **no**: the one non-identity automorphism carries mark 0 to mark 1 | **yes**: no permitted automorphism carries one to the other | `automorphisms.mark_exchange_witness`, `marks_internally_separable`; Lean `retained_exchange_transports` for what the composite carries, `retained_marks_separated_by_a_side` for the raw separation |
| mark forms invariant on the bounded domain (definition 34) | neither: the reflection is permitted and moves the side | both | `separation.invariant_mark_forms` |
| mark forms that separate the two marks | both, but neither is invariant, so none separates them internally | both, and both are invariant | `separation.separating_mark_forms`, `invariant_separating_mark_forms` |
| which named side each mark lies on | not formulable: U admits no name | mark 0 on `near`, mark 1 on `far` | `separation.mark_side_names` |
| the two sides, internally separable | **no**: a permitted automorphism exchanges them, the same one that exchanges the marks | **yes**: none does | `automorphisms.side_exchange_witness`, `sides_internally_separable` |
| `sides_collapsed`, the Challenge 0 profile comparison | false, and not the internal fact: it reads internal identities that a permitted renaming permutes | false, and the names alone would make it so | `retained.sides_collapsed`; definition 29 |
| the two marks on different sides (definition 35) | an internal fact: invariant under every permitted renaming in the census, and it holds | same | `different_sides_census`, `retained.marks_on_different_sides`; Lean `retained_marks_differ_in_side` |
| the admission order of the two wholes | not internally available: the other order gives an isomorphic regime | same | `readings.*.order`; Lean `retainedOtherOrder_is_exchange`, `retainedOtherOrder_ne_retained` |
| the shared visible mark | not internally available: a relabelled regime is unequal and isomorphic | same | `readings.*.label` |
| the presentation convention | invisible up to a permitted renaming, as at Challenge 1 | now also invisible up to a permitted renaming: one class, the other convention's regime reached by the mark exchange | `convention.isomorphic_under_reading`, `classes_under_isomorphism` |
| initial datum and reading | unchanged | same | `retained.initial_datum_unchanged`, `reading_unchanged`; Lean `retained_reading`, `retained_initialDatum` |
| an event follows from the retained regime | none | none | `retained.event_follows_relation_empty`; Lean `no_event_follows_retained` |
| new judgment form needed | none | none | `observation_vocabulary` |

Three results in that table are worth stating in prose because they are
not what the previous rung's table would suggest.

**The sides become interchangeable again under U.**  At genesis the two U
sides had equal profiles; one admitted mark made them unequal; two marks,
one on each side, make them unequal as raw data and yet interchangeable
under a permitted renaming.  The Challenge 0 profile comparison
`sides_collapsed` reads the internal identities of the marks on each side,
and those a permitted renaming permutes, so at two marks it is not the
internal fact and definition 29's notion is.  A symmetry that an
admission broke, a later admission restored.

**The one non-identity U automorphism does both exchanges at once.**  It
is the same witness in the mark search and in the side search.  Under U
the two marks and the two sides are un-separated together, not
independently; nothing in the rung separates one pair while leaving the
other joined.

**Under O the convention stops changing the class.**  At Challenge 1 the
two conventions gave two non-isomorphic O candidates, and the run kept
both classes.  At two retained marks the mark exchange, permitted under
both readings, carries one convention's regime to the other's, so there
is one class under O as well.  What the convention still fixes is the
correspondence between presented wholes and admitted marks — which whole
is on `near` — and not that the two marks are separated.

**The seed's question, answered.**  Are the two wholes internally
distinguishable by the admitted boundary alone?  Under U, no: a permitted
automorphism exchanges them, and no invariant mark form separates them;
what the boundary alone buys there is that they do not share a side, and
nothing more about them.  Under O, yes: no permitted automorphism
exchanges them and both invariant mark forms separate them, one whole
lying on `near` and the other on `far`.  What that cost, and who paid: the
admitted boundary, paid at the seed; the O reading of that one
declaration, paid at genesis; and, under both readings, the occurrence
identity, paid by the run at this rung, without which the two wholes are
not two marks at all.  The presentation convention, paid by the run at
Challenge 1, buys which whole is which and not the separation.

**What remains internally unavailable**, under both readings: the shared
visible mark; the order in which the two wholes were retained; and, under
U only, which mark is which, which side is which, and any name for either.

#### 5.6 The predictions, scored

| id | label | status | note |
|---|---|---|---|
| C1-X (from Challenge 1) | NOT FORCED | PARTIAL | U half HIT: the retained regime is fixed by the reflection up to mark renaming, a permitted automorphism exchanges the two marks, and no invariant mark form separates them.  O half PARTIAL: the names clause hits, the two marks being separated with one on `near` and one on `far`; the clause “the price is the O declaration paid at genesis, and nothing new is paid at Challenge 2” is false as written and its own falsifier, “under O a price beyond the names”, fired — the occurrence identity is a new declaration paid at this rung, under both readings (`scores.C1-X.O_nothing_new_paid_clause_status`).  The frozen condition, that Challenge 2 admits two internal identities for the two wholes despite the shared visible mark, was met (`condition_status`) |
| C2-1 what “retains” licenses | NOT FORCED | HIT, DEFINITION-level | the caller's history is a supply and an occurrence admission per whole, certified, replayed from genesis, two marks on opposite sides, the two supplies equal as values; every clause is fixed by the run's own reading of the word and by the declared convention and policy, so the hit is by construction and is not counted as content |
| C2-2 the shared visible mark refuses the Challenge 1 admission | FORCED | HIT, DEFINITION-level | all four shared-policy histories, two readings by two conventions, are refused by the moving-admission refusal by name; the refusal is the Challenge 1 declaration replayed on a declared history, so the hit is by construction, although that declaration was made before this question arose |
| C2-3 the identity policy is one declaration, and not free | NOT FORCED | HIT, DEFINITION-level | the declared space has two policies and exactly one retains both wholes; the price is one new admission event and the withdrawn repeated-label rule, paid by the run, equal under both readings; all of it declared by this rung, so the hit is by construction |
| C2-4 two judgments, and nothing else | FORCED | HIT | counted as content: the two new judgments and their evaluation rest on `retained_onSide_true_iff` with `retained_onSide_zero`, `retained_onSide_one`, and `retained_onSide_beyond`, none by unfolding, and retention on `retained_judgments_survive` |
| C2-5 under U the marks are exchanged by a permitted automorphism | FORCED | HIT | counted as content: the automorphism counts, two under U and one under O, and the exchanging witness are computed over the unpruned enumeration, and the invariance of each mark form is a census over the bounded domain |
| C2-6 under O the marks are separated, and by the names | FORCED | HIT, narrowed at Challenge 3 | counted as content: the single O automorphism, the absence of an exchanging one, both invariant separating forms, and the one-class convention computation are searches; the raw separation is `retained_marks_separated_by_a_side`.  **The clause "and by the names" did not survive**: Challenge 3's counterfactual square computes that the separation holds in exactly the cells where the side exchange is not permitted, whether or not the names are admitted, so what separates under O is the withdrawal the O reading carries and not the names it also carries.  The prediction's own falsifier, "a separation that survives removing the names", fired there.  The status is unmoved because the rung's computation is unmoved; what is narrowed is the attribution, and B2-MARKS-O carries the narrowing |
| C2-7 what the boundary alone buys | FORCED | HIT | counted as content: the different-sides property survives all 177 permitted images of the census, and holds of the retained regime; under U no invariant form separates the wholes, under O both do |
| C2-8 the sides become interchangeable again under U | NOT FORCED | HIT | counted as content: the side-exchanging automorphism, the order isomorphism, and the label isomorphism are witness searches; `sides_collapsed` is false at the retained regime and is not the internal fact |
| C2-X extrapolation | NOT FORCED | PENDING | scored by Challenge 3 |

Eight of eight scored predictions hit; five as content (C2-4 to C2-8) and
three by construction, DEFINITION-level and not counted (C2-1 to C2-3),
by the criterion Challenge 1 declared and this rung reuses unchanged
(`tally.criterion`).  The counts are the receipt's `tally`, computed from
the statuses and a declared list.  Four of the five FORCED predictions
are among the content hits; the fifth, C2-2, is DEFINITION-level.  **A
clean sweep of a rung's own predictions is weak evidence**: they were
written by an instrument that had read the whole tree and reasoned the
rung through before writing them, and the commit order shows only that
they were frozen before the code.  The informative number is the previous
rung's extrapolation, written before this rung existed, and it is
PARTIAL: one of its two O clauses is a recorded miss, and its own
falsifier named the miss.

Two of those scores carry a reading that was not recorded when they were
made, and Challenge 3's review of them records it here.  C2-5's frozen
clause “its permitted automorphism group has exactly two elements” is read
as the *set* of permitted automorphisms and is scored by the size of that
set, with the set's entries reported beside the count
(`automorphisms.entries`); no structure beyond the set is read into the
word, and none is computed.  C2-8's four conjuncts are not all searches: the
U side-exchanging witness, the order isomorphism, and the label isomorphism
are searches over the unpruned enumeration, and both values of each are
attainable, but the absence of a side-exchanging automorphism under O
follows at once from the declaration that the reflection is not a permitted
renaming there, so that conjunct is DEFINITION-level.  C2-8 keeps its
content hit on the U clauses; no status and no tally moves.  The
corresponding wording inside `receipts/challenge2.json` still says that none
of its evidence is fixed by a declaration; that repair would regenerate a
closed rung's receipt and is carried, with its reason, in
`challenge3/STATUS.md`.

#### 5.7 What Challenge 2 does not establish

- Nothing about two marks on the *same* side, or about more than two
  marks, beyond the bounded censuses.
- Nothing about a whole within a side, depth, or the outside of the
  boundary.
- No unbounded theorem: the automorphism searches, the mark-form
  invariance census, and the different-sides census are bounded
  computations, and the Lean theorems are about the concrete two-mark
  regime, not about every regime.
- Nothing about Challenge 3's declared sense of separability.  Definition
  33 is this rung's notion, used to answer this rung's question; whether
  Challenge 3 declares it, and what follows if it does, is C2-X.
- The exhaustiveness of the identity-policy space is over the caller's two
  wholes and the question “what does the second admission admit”.  It is
  not a claim that no other treatment of the shared visible mark exists.
- Nothing about whether the O separation earns its keep beyond separating
  these two wholes.

#### 5.8 Dependence on the admitted boundary

| result | dependence |
|---|---|
| the identity policy space, the refusal of the shared policy, and the price | independent of the boundary; they concern presentation tokens and internal identity |
| supply is presentation only; the current state is the replay of the caller's history | independent of the boundary |
| the initial datum and reading unchanged; the empty event-follows relation | independent of the boundary |
| the two new judgments, the sides the marks are retained on, the automorphisms, the separation, the different-sides fact | require the admitted boundary and are not formulated after removing it |

### 5.9 Challenge 3: the required separation of `<a|>` and `<|a>`

Receipt: `receipts/challenge3.json`.  Predictions frozen at sha256
`27057895c47e5bd718b0ea8e51689f3325cef78102c912c6feea8e913a7e7755` in
commit `a4f2a688`, before the branch's first Challenge 3 code-or-proof
commit.  Git establishes that committed order only; it does not establish
when off-tree or untracked work was written.

The caller requires the two retained wholes to be internally separable in a
precisely declared sense.  The rung declares the sense (definitions 38 and
39), answers the requirement under each reading, and — where it fails —
enumerates the declared candidate space of 48 points, prices each candidate
under two declared measures, refuses the bundles, and retains every tied
minimum.

**Under O the requirement is already met, and the names are not what meets
it.**  The four-cell counterfactual square (definition 46) is the same under
both readings and turns on one coordinate only: the requirement holds in the
two cells where the side exchange is not a permitted renaming and fails in
the two where it is, whether or not the two names are admitted.  So what
satisfies the requirement under O is the *withdrawal* the O reading carries,
not the *names* it also carries.  That sharpens Challenge 2, whose price
listed the names among the capabilities the O separation uses; the
capabilities it uses are the admitted boundary, the withdrawal, and the
Challenge 2 occurrence identity, and the receipt now records the names under
`capabilities_not_used`, a field it marks as a declaration of the run and
not as a measurement; what shows the names to be idle is the square.
Nothing is paid at this rung under O: the minimum capability count is zero,
attained by the null augmentation alone, and that minimum is unique.

That the names *cannot* enter the square is definition 16 and not a
discovery: permission is declared and is not derived from the judgment
grammar.  Under a model in which permission were derived — the permitted
renamings being exactly the maps that preserve every declared judgment —
admitting the names would withdraw the exchange, the two coordinates would
not be independent, and the enumeration below would be a different one.
That model is outside the declared space and is recorded in section 10 as
open.

**Under U the requirement fails, and three non-isomorphic minima meet it.**

| result | reading U | reading O | evidence |
|---|---|---|---|
| the current regime meets the requirement | **no**: the composite of the side exchange with the exchange of the two marks is a permitted automorphism carrying mark 0 to mark 1 | **yes**: the only permitted automorphism is the identity | `readings.*.base.satisfies`; Lean `retained_U_requirement_fails` (a pairing of the Challenge 0 permission with the Challenge 2 `rfl`) |
| the declared sense and its second reading | agree at all 48 points, the second reading taken at its declared witness | same | `requirement_readings_agree_at_every_point`; by unfolding, definition 39 |
| the declared sense against Challenge 2's notion | the same at the current regime | same | `requirement_matches_the_challenge_2_notion` |
| what satisfies it under O | not applicable | the withdrawal of the side exchange, paid at genesis by the declared reading; the names are not used | `counterfactual_square` |
| adding judgment forms, whatever the forms | cannot satisfy it while the composite is permitted | not applicable, the composite not being permitted | Lean `no_invariant_mark_property_separates_retained`, quantified over an arbitrary property; the concrete `admit_names` point fails, and `points_satisfying_with_grammar_change_only` is empty **under U**, which is the only reading it can be non-empty under, its own definition carrying `reading == U`.  That key also admits the label-keeping coordinate, which definition 40 keeps distinct from the judgment grammar, so it is wider than its name; both narrowings are review findings and the key itself is carried, a repair to it regenerating a closed rung's receipt |
| the two mark forms under the composite | neither is invariant, which is why both separate the marks as raw data and neither does so internally | not applicable | Lean `mark_form_is_not_invariant_under_the_composite`; `base.invariant_mark_properties` |
| the declared candidate space | 48 points; one step exactly when the capability count is one | same | `candidate_space.size`, `one_step_iff_capability_count_one` |
| one-step points | six: withdraw the side exchange, withdraw the mark permutations, admit the names, keep the labels, admit a further mark on either side | same | `one_step_points` |
| one-step points that satisfy it | four, in **three** classes | not applicable: the null point already satisfies at count zero | `satisfying_one_step_points`, `minima_by_mu1.classes` |
| the minimum capability count | **1** | **0** | `minima_by_mu1.minimum` |
| the minimum is unique | **no**, refuted by three retained classes | yes, the null augmentation alone | `minima_by_mu1.unique`, `class_count` |
| the second measure, the collateral count | 1 at each of the three minima; the same three classes are selected | 0 at the null point, and its minimum of zero is attained by five points in three classes, so the two measures do **not** select the same minima here | `minima_by_mu2`; `readings.U.measures_agree_on_minima`, which is false under O |
| the two measures are the same function | no: they differ at points of the space | same | `measures_differ_somewhere` |
| bundles refused | 41 of the 48 points | same | `bundles_refused_count` |
| adopting reading O under U | count 2: refused as bundling, although it satisfies | not applicable | `reading_O_bundle` |
| the further mark needs a new supply | no: the caller already supplied the token; a token never presented is refused by name | same | `process_admission` |
| the retained marks after the further mark | both judgments survive | same | Lean `retainedPlus_judgments_survive` |
| the initial datum, the reading, the event-follows relation | unchanged, and empty on every event of all three declared kinds, five probes in all | same | `initial_datum_unchanged`, `reading_unchanged`, `event_follows_relation_empty`, `event_kinds`; Lean `no_event_follows_retainedPlus` |
| new event kind or judgment form | none added by the rung itself | none | `new_event_kinds_at_challenge_3`, `observation_vocabulary` |

**The three retained minima, and how each separates.**

| minimum | what it declares | how it separates | basis |
|---|---|---|---|
| withdraw the side exchange | the two sides are distinguishable, which is the part of the O reading that U does not carry | both side properties become invariant and both separate the two marks | COMPUTED: the mark exchange alone does not fix the placement, and the invariance is a census over the bounded domain |
| withdraw the mark permutations | a mark's admission index is internally available and not merely a metatheoretic name | both index properties become invariant and both separate them; the two side properties stay non-invariant | **DEFINITION-level**: with the mark permutations withdrawn no permitted renaming moves an index at all, so the requirement is met by unfolding.  Reported as such and not counted as content |
| admit one further mark, on either side | the process, and not only the caller, issues an admission | none of the five declared mark properties is both invariant and separating; the witness is the orbit property alone.  The two sides then carry different numbers of marks, so no renaming undoes the side exchange | COMPUTED, and PROVED in the unbounded direction: Lean `retainedPlus_counts_differ` with `countOn_perm` and `reflect_not_undone_by_renaming` |

Four things in that table are worth stating in prose.

**The declared sense admits a cheap answer, and the run reports it rather
than excluding it.**  The second minimum meets the requirement by unfolding:
withdraw the renamings that move indices and the two marks are separated
because nothing is left that could confuse them.  It buys the separation by
declaring the admission index — a metatheoretic name, by definition 3 — to be
internally available, and it makes the admitted boundary do no work at all.
An earlier version of these lines called that an internal *designation*, a
second sense of a word section 1 reserves for current-state designation;
reworded wherever the run used it so, no result moving.  It is not excluded, because the requirement as declared does not
oblige the boundary to do the work and no declaration of this run rules the
candidate out.  It is labelled DEFINITION-level in the receipt, and it is
the rung's clearest evidence that a precisely declared requirement can be
met in a way that misses what the requirement was for.

**The minimum is strictly cheaper than adopting the other reading.**  The
candidate that adopts reading O under U costs two capabilities and is
refused as a bundle; its withdrawal half alone costs one and is a retained
minimum, and its name half alone satisfies nothing.  So under U the
separation does not cost what reading O paid at genesis: it costs less, and
the difference is exactly the two names, which the counterfactual square
shows to be idle here.

**The third minimum separates by a count, not by a property of either
mark.**  Once a third mark is placed, the two sides carry two marks and one,
and the side exchange exchanges those counts, so no renaming of the marks
returns the reflected placement to the original.  That is proved in Lean
over every permutation rather than computed over a bounded enumeration, and
it is half of the equal-count law the Challenge 0 census observed and left
as a computation.  **The other half is not proved**: that at equal counts some
renaming does undo the side exchange is not established here, and
`retained_counts_equal` is not it.  What that theorem records is narrower and
is all the rung needs: at the retained regime the two counts are equal, so the
counting argument says nothing there, and the requirement fails because the
composite really does carry the regime onto itself rather than for want of a
proof.

**The shared visible mark is still idle.**  The property "carries the label
the caller supplied" is invariant under every candidate's renamings and
separates nothing, both retained marks carrying the same label; and, **under U**, the
candidate that keeps the labels in the serialization — the one that makes
presentation identity internal — satisfies nothing for the same reason.
Under O it satisfies, because the base already does and the candidate takes
nothing away; what it adds there is the label as a collateral fact and not the
separation.  An earlier version of this sentence was written without a reading
and was false under O.  That is Challenge 2's result restated where it now
costs something to try.

**What the boundary is charged, and what it buys.**  Under both readings the
boundary buys that a mark lies on a side at all, without which three of the
five declared mark properties, four of the five collateral facts, and two of
the three minima are not formulable.  It does not buy the separation under
U: two of the three minima there make it internal, and the third — the index
withdrawal — bypasses it entirely.  Under O it buys the separation outright,
through the half of its own declaration that withdraws the side exchange.

#### 5.10 The predictions, scored

| id | label | status | note |
|---|---|---|---|
| C2-X (from Challenge 2) | NOT FORCED | **PARTIAL** | five clauses hit: the declared sense is the Challenge 2 notion; under O the requirement holds with no augmentation; under U it fails; no candidate that only changes the judgment grammar satisfies it, which this rung PROVED for an arbitrary property rather than argued; and the tied-minima clause hits, with three rather than the two it named.  An earlier version of this row counted four and then named the fifth in the next sentence, while the status and the receipt counted five; corrected.  The clause “every minimum one-step augmentation will either name a side, paying under U what reading O paid at genesis, or admit a further datum that the automorphism cannot carry” is **MISSED**, recorded next to its value: two retained minima pay neither, the withdrawal of the side exchange admitting no name and the withdrawal of the mark permutations being neither, and the clause's own falsifier — “a minimum that pays neither a side name nor a further datum” — fired.  A weaker reading that counts the withdrawal as paying what reading O paid still misses, on the second of those two (`scores.C2-X`) |
| C3-1 the declared sense, and a second reading of it | NOT FORCED | HIT, DEFINITION-level | the sense is the run's declaration and the agreement of its two readings is by unfolding, the orbit witness being invariant by construction; not counted as content |
| C3-2 the current regime, and what does the work under O | FORCED | HIT | counted as content on the side-exchange coordinate, whose cells are automorphism searches with both values attained; DEFINITION-level on the names coordinate, where definition 16 keeps the names out of the computation |
| C3-3 no addition of judgment forms can satisfy it under U | FORCED | HIT | counted as content: the Lean statement quantifies over an arbitrary property, and the countermodel shows the hypothesis is a real restriction |
| C3-4 the declared candidate space, and the refusal of bundles | NOT FORCED | HIT, DEFINITION-level | the coordinates, their values, and the capability named for each are declarations of this rung, so the point count and the identity of one-step with count one are by construction; not counted as content |
| C3-5 the minimum under U is one, and it is not unique | FORCED | HIT | counted as content: which one-step points satisfy is a search at each candidate's own renamings, and the class count is the implemented quotient |
| C3-6 the two measures agree on the minimum and are not the same measure | FORCED | HIT | counted as content: each collateral fact is a witness search, and the difference of the two measures is a census over the 48 points |
| C3-7 three mechanisms, one of them by unfolding | FORCED | HIT | counted as content on the first and third mechanisms; the second is DEFINITION-level and the receipt says so separately |
| C3-8 what the reading changes, and what the boundary is charged | NOT FORCED | HIT | counted as content on the two minimum counts and the two class counts; the boundary-dependence map beside them is the run's classification and is not computed |
| C3-X extrapolation | NOT FORCED | PENDING | scored by Challenge 4 |

Eight of eight scored predictions hit; six as content (C3-2, C3-3, C3-5 to
C3-8) and two by construction, DEFINITION-level and not counted (C3-1,
C3-4), by the criterion Challenge 1 declared and this rung reuses unchanged
(`tally.criterion`).  The counts are the receipt's `tally`, computed from
the statuses and a declared list.  Five of the eight were labelled FORCED,
and all five are among the content hits.

**A second clean sweep is weaker evidence than the first, not stronger.**
The predictions were written by an instrument that had read the whole tree
and had reasoned the rung through before writing them; the commit order
shows only that they were frozen before the code, and two of the eight were
scored only after the scorer itself was corrected to read their frozen words
(see the repairs in `challenge3/STATUS.md`).  The informative number is the
previous rung's extrapolation, written before this rung existed: it is
PARTIAL, and its own falsifier named the miss.

#### 5.11 What Challenge 3 does not establish

- **The minimality is scoped to the declared space** (definition 40).  A
  candidate outside those five coordinates — one that changed the event
  grammar again, that admitted two further marks in one step, or that
  derived the permitted renamings from the judgment grammar — is not
  enumerated, and no claim is made about it.
- Nor is “one step” a discovered notion: it is the run's declaration that
  one moved coordinate is one step, and the identity of that with a
  capability count of one is by construction.
- The three minima are tied under both declared measures.  A third measure
  could separate them, and none is offered; the tie is a fact about these
  two measures and this space.
- Nothing about whether the requirement, as declared, is the right
  requirement.  The second minimum meets it in a way that makes the admitted
  boundary idle, which the rung reports rather than repairs.
- Lean does not close the automorphism counts, the class count, or the
  enumeration.  It closes the judgment-form family, the countermodel that
  makes that family's hypothesis a real restriction, and the unbounded
  half of the further-mark mechanism.
- Nothing about two marks in one whole, a whole within a side, depth, or the
  outside of the boundary.  Challenges 4 and 5 are not reached.
- The collateral facts are five declared ones, not a survey of everything a
  candidate makes available.

#### 5.12 Dependence on the admitted boundary

| result | dependence |
|---|---|
| the declared sense, its second reading, and their agreement | independent of the boundary; they are about renamings and orbits |
| the identity of the candidate space, the capability counts, the one-step rule, and the refusal of bundles | independent of the boundary |
| the two index mark properties and the withdrawal of the mark permutations | independent of the boundary: the admission index is carried by the placement tuple's length and not by the sides |
| the side exchange, its withdrawal, the two side mark properties, the counterfactual square, and every separation result of the rung **except the index withdrawal** | require the admitted boundary and are not formulated after removing it |
| the further-mark minimum | requires the admitted boundary: the further mark is admitted ON a side, and what separates the two retained marks there is that the two sides then carry different numbers of marks |

The exception in the fourth row is stated because an earlier version of it read
"every separation result of the rung" with no exception, which the row above it
contradicts: the withdrawal of the mark permutations is a separation result and
is classified as independent of the boundary.  The receipt's own
`boundary_dependence` field still carries the unqualified text; repairing it
would regenerate a closed rung's receipt, and it is carried with that reason in
`challenge4/STATUS.md`.

### 5.13 Challenge 4: the caller retains `<a|b>` and `<b|a>`

Receipt: `receipts/challenge4.json`.  Predictions frozen at sha256
`42371f458e23ce89885a76c542863c112482c0ca6b4f1d9ff6a058b3c21f2041` in
commit `f07a20c4`, before the branch's first Challenge 4 code-or-proof
commit.  Git establishes that committed order only; it does not establish
when off-tree or untracked work was written.

The caller supplies and retains two wholes, each with a mark on each side of
the boundary, and requires their internal separability.  Two declarations come
first, and both are recorded as declarations.

**The reader bound had to be widened** (definition 47).  The Challenge 1
reader admits at most one mark in a whole and refuses **both** inscriptions by
name, so the caller's challenge could not be read at all.  The run declares
the widened reader — at most one mark on each side of the bar — and leaves the
narrower one refusing, so that what forced the widening stays visible.  **The
run pays it, not the boundary and not the caller.**  In which order the two
marks of one whole are admitted is a second declaration of the same kind as
the convention (definition 48), and the other order is computed to give an
isomorphic configuration under both readings.

**The requirement is about a structure the state does not carry**
(definition 50).  A whole is a set of marks, and the regime has no component
that groups marks into wholes: the grouping is read off the caller's history.
So the requirement, and its declared witness, are statements about the
automorphisms of the state and about a metatheoretic grouping, at every
candidate that does not admit that grouping.  The run reports that rather than
repairing it, and makes the grouping one of the declared coordinates.

**The requirement fails under BOTH readings.**  This is the first rung at
which reading O does not already meet it.

| result | reading U | reading O | evidence |
|---|---|---|---|
| the retained state | four marks, placement `(0, 1, 0, 1)`, labels `("a", "b", "b", "a")`, groups `(0, 0, 1, 1)`; certified and replayed from genesis | same | `readings.*.base`; Lean `crossRetained_eq` (DEFINITION-level, `rfl`), `crossRetained_placement_length` |
| the Challenge 1 reader on the caller's inscriptions | refused by name, both of them | same | `reader.challenge_1_reader`; DEFINITION-level, the Challenge 1 bound replayed |
| the other within-whole order | isomorphic: the order is not internally available | same | `base.collateral_facts.within_whole_order_internally_available` |
| what admission adds | exactly four holding judgments, one per mark; 0 to 4 | the same four; 2 to 6, the two name judgments unchanged | `base.holding_mark_judgments`, `holding_judgments_with_names`; Lean `crossRetained_onSide_true_iff`, `crossRetained_onSide_zero` to `crossRetained_onSide_beyond`, `crossRetained_sideNamed` |
| each mark's profile | its own side, nothing else | same | `base.mark_profiles`; definition 22 |
| permitted automorphisms of the retained configuration | **eight**, over 48 permitted images | **four**, over 24 | `base.automorphism_count`, `permitted_renamings.images`; COMPUTED over the unpruned enumeration |
| the two retained wholes meet the requirement | **no** | **no** | `base.satisfies`; Lean `exchangeWholesRegime_crossRetained` for the map that carries the regime onto itself |
| what carries one whole onto the other | the exchange of the two wholes, permutation `[2, 3, 0, 1]`, **with no side exchange** | the same map, and it is the only kind there is | `base.whole_exchange_witness`; Lean `exchangeWholes_carries_the_first_whole`, `exchangeWholesRegime_crossRetained` |
| the side exchange | is a permitted automorphism of the configuration | is not | `base.side_exchange_witness`; Lean `reflect_crossRetained_ne` shows the side exchange alone does not fix it |
| pairs of distinct marks that are separable | **none of the six** | **four of the six**: exactly the pairs on different sides | `base.separable_mark_pairs`; Lean `crossRetained_marks_share_a_side` and `crossRetained_other_marks_share_a_side`, one per pair, for the two that are not |
| the two sides carry | two marks each | same | `base.marks_on_each_side`; Lean `crossRetained_counts_equal` |
| adding judgment forms, whatever the forms | cannot meet the requirement while the whole exchange is a permitted renaming | same | Lean `no_invariant_pair_property_separates_the_wholes`, quantified over an arbitrary property of a pair of marks; `no_invariant_mark_property_separates_the_paired_marks` for a single mark |
| any continuation whatever | never removes the obstruction: the whole exchange still carries the regime onto itself after every later history | same | Lean `whole_exchange_survives_every_continuation`, and `whole_exchange_survives_a_further_mark` for the Challenge 3 third minimum |
| the declared candidate space | 192 points; one step exactly when the capability count is one | same | `candidate_space.size`, `one_step_iff_capability_count_one` |
| one-step points | eight | same | `one_step_points` |
| one-step points that meet it | **one**: withdraw the mark permutations | **two**: withdraw the mark permutations, or keep the presentation labels | `satisfying_one_step_points` |
| the minimum capability count | **1** | **1** | `minima_by_mu1.minimum` |
| the minimum is unique | **yes**, one class inside the declared space | **no**, two tied classes, both retained | `minima_by_mu1.unique`, `class_count` |
| the second measure at the minima | 2 | 3 at each of the two | `minima_by_mu2`; `measures_agree_on_minima` is true under both readings |
| the two measures are the same function | no: they differ at points of the space | same | `measures_differ_somewhere` |
| bundles refused | 183 of the 192 points | same | `bundles_refused_count` |
| admitting the whole grouping alone | does not meet the requirement: the tag exchange is then a renaming the object language cannot see | same | `grouping_square`, `one_step_detail` |
| naming the wholes without the grouping | a no-op that collapses into the null point | same | `name_wholes_collapses_into_the_base` |
| the grouping WITH the names | meets it, at capability count 2, and is refused as a bundle | same | `grouping_bundle` |
| the matching of a visible mark across the boundary | not internally available | not internally available | `base.collateral_facts.cross_boundary_matching_internally_available` |
| the pointwise sense against the requirement | implies it at every point; the converse fails at 18 points | implies it at every point; the converse fails at 16 | `pointwise_implies_whole_at_every_point`, `points_where_the_two_senses_part` |
| the requirement at the Challenge 3 configuration | the whole sense is the Challenge 3 sense | same | `reduction_to_challenge_3` |
| the initial datum, the reading, the event-follows relation | unchanged, and empty on every event of all three declared kinds | same | `base.*`; Lean `crossRetained_reading`, `crossRetained_initialDatum`, `no_event_follows_crossRetained` |
| new event kind or judgment form | none added by the rung | none | `new_event_kinds_at_challenge_4`, `observation_vocabulary` |

**Five things in that table are worth stating in prose.**

**The obstruction is the exchange of the two wholes, and it needs no side
exchange.**  At Challenge 3 the composite that defeated the requirement under
U was the side exchange with a mark exchange, and reading O defeated the
composite by withdrawing the side exchange.  Here the map that carries one
whole onto the other is a permutation of the marks alone — the first whole's
two marks go to the second whole's two — and no reading withdraws the mark
permutations.  So the half of the O declaration that did the work at Challenge
3 does no work here, and **the requirement fails under O for the first time in
the run**.  That is exactly what the previous rung's extrapolation predicted
would not happen, and its own falsifier named it.

**What the boundary contributes here, and what it cannot.**  It contributes
what it contributed at Challenge 3 — the side each mark lies on, and each
mark's profile is its side and nothing else — but that now sorts four marks
into two classes of two and no finer.  Under O it still separates marks that
lie on different sides, four of the six pairs; it separates neither of the two
pairs that share a side, which the receipt computes and Lean proves for both
pairs, one theorem each (`crossRetained_marks_share_a_side`,
`crossRetained_other_marks_share_a_side`), and each whole has one mark in each
class, so it separates no whole from the other.  What it cannot contribute is
which mark within a side is which, the grouping of marks into wholes, and the
matching of a visible mark across the boundary: the configuration in which the
second whole's copy of `a` is a token the caller never presented is reached by
a permitted renaming under both readings.

**Under O a label with a side is a complete invariant, and under U it is not.**
Keeping the presentation labels meets the requirement under O and fails under
U.  The reason is the shape of the challenge: the two wholes are each other's
reflection, so under U, where the side exchange is a renaming the object
language cannot see, the labels are carried onto each other along with the
sides.  Under O the four pairs of a label with a side are distinct and the
property "carries `a` on side 0" is invariant, determined by the key, and
separating.  This is the one place in the run where a presentation label,
made internal, buys something — and it buys it under one reading only.

**The augmentation the caller's demand actually names is a bundle.**  Admitting
the whole grouping is what would make "these two marks are one whole" a fact of
the state.  Alone it does not meet the requirement: with the two tags admitted
but unnamed, their exchange is a renaming the object language cannot see, and
composed with the mark permutation that exchanges the two wholes it carries the
configuration onto itself.  Naming the two wholes without admitting the
grouping names tags no mark carries and collapses into the null point.  The two
together meet the requirement under both readings — and cost two capabilities,
so they are refused as one step, and **neither half is a minimum**.  The
four-cell grouping square exhibits it: met in one cell of four, under both
readings.

**Under U the minimum is unique, and it is the cheap answer.**  Exactly one
one-step point meets the requirement under U: withdrawing the mark
permutations, which meets it by unfolding — with no permitted renaming moving
an index, nothing is left that could confuse two marks — and which leaves the
admitted boundary idle, exactly as at Challenge 3.  It is the first rung at
which uniqueness is not refuted under U, and the unique minimum is the
candidate the previous rung called the clearest evidence that a precisely
declared requirement can be met in a way that misses what the requirement was
for.  The withdrawal of the side exchange, a minimum at Challenge 3, is not one
here; nor is a further mark on either side, and Lean closes that for every
continuation and not only for one further mark.

**The boundary's price and purchase at this rung.**

| capability | what it buys at Challenge 4 |
|---|---|
| the admitted boundary | that a mark lies on a side at all: three of the five declared whole properties — every one but the index one and the tag one — six of the eight collateral facts, and the further-mark coordinate are not formulable without it.  It does **not** buy the requirement under either reading |
| the O reading's side names | nothing the requirement uses directly |
| the O reading's withdrawal of the side exchange | not the requirement, which the whole exchange defeats without the side exchange; it buys that a property reading a label and a side is invariant, which is what the label-keeping minimum uses under O |
| the Challenge 2 occurrence identity | that the four presented marks are four admitted marks at all |
| the presentation convention, and the within-whole order | which presented side and which presented mark become which; not the separation |
| the widened reader bound | that the caller's inscriptions can be read at all |

#### 5.14 The predictions, scored

| id | label | status | note |
|---|---|---|---|
| C3-X (from Challenge 3) | NOT FORCED | **PARTIAL** | six clauses hit: the reader bound had to be widened and the widening is paid by the run; the retained placement is `(0, 1, 0, 1)`; the two sides carry equally many marks and a side-exchanging automorphism exists under U; the requirement fails under U at a minimum capability count of one; the boundary contributes the side each mark lies on, neither side-reading whole property separating the two wholes and every mark profile being its own side; and the matching of a visible mark across the boundary stays internally unavailable under both readings.  The clause "and hold again under O with no new declaration" is **MISSED**, recorded next to its value: under O the requirement fails, the exchange of the two wholes needing no side exchange, and the clause's own falsifier — "the O requirement needing a new declaration" — fired.  With it the clause that the boundary contributes here **exactly** what it contributed at Challenge 3 is MISSED too, that contribution having met the requirement under O there and not here (`scores.C3-X`) |
| C4-1 the reader bound, and what the retention makes | FORCED | HIT, DEFINITION-level | the Challenge 1 refusal is that rung's declared bound replayed on the caller's text, and the retained configuration follows from the widened reader, the convention, the within-whole order, and the Challenge 2 policy; not counted as content.  Its one non-declared clause, that the other within-whole order gives an isomorphic configuration, is an isomorphism-witness search and is reported separately |
| C4-2 the requirement fails under both readings | FORCED | HIT | counted as content: whether an automorphism carries one whole's mark-set onto the other's is a search over the unpruned enumeration at each reading's own renamings, and the pair census is a search per pair |
| C4-3 what the boundary contributes, and what it cannot | NOT FORCED | **PARTIAL** | three clauses hit: neither side-reading whole property separates the two wholes under either reading; the cross-boundary matching is internally unavailable at the retained configuration under both; and keeping the labels meets the requirement under O and not under U.  The clause "both declared side-reading whole properties are invariant under both readings" is **MISSED**, recorded next to its value: under U they are not invariant, the side exchange being a permitted renaming that moves a mark's side, which is the same fact that made the Challenge 2 mark forms non-invariant under U.  The receipt reports the value per reading (`scores.C4-3.side_properties_invariant_by_reading`) |
| C4-4 the declared candidate space | NOT FORCED | HIT, DEFINITION-level | the coordinates, their values, the capability named for each, and therefore the point count and the identity of one-step with capability count one are declarations of this rung; not counted as content |
| C4-5 the minimum under U, and its uniqueness | FORCED | HIT | counted as content: which one-step points meet the requirement is a search at each candidate's own renamings, and the class count is the implemented quotient.  That the one minimum meets it by unfolding is DEFINITION-level and the receipt says so separately |
| C4-6 the minima under O | FORCED | HIT | counted as content: the same search and the same quotient under the other reading |
| C4-7 the grouping is a bundle | FORCED | HIT | counted as content: each cell of the grouping square is an automorphism search with both values attained, and the collapse of the name-wholes point is the implemented quotient |
| C4-8 the two senses part | FORCED | HIT | counted as content: the pointwise sense is a search per pair, the whole sense a search per whole, and their comparison a census over the 192 points with the parting points named.  The reduction at the Challenge 3 configuration is **DEFINITION-level**, true by unfolding where each whole is one mark, so it is computed and reported separately and is no part of the content |
| C4-X extrapolation | NOT FORCED | PENDING | scored by Challenge 5 |

Seven of eight scored predictions hit and one is PARTIAL; five hit as content
(C4-2, C4-5 to C4-8) and two by construction, DEFINITION-level and not counted
(C4-1, C4-4), by the criterion Challenge 1 declared and this rung reuses
unchanged (`tally.criterion`).  The counts are the receipt's `tally`, computed
from the statuses and a declared list.  Six of the eight were labelled FORCED;
five of those are among the content hits and the sixth, C4-1, is
DEFINITION-level.

**This rung's own sweep is not clean, and the two misses are the informative
part.**  C4-3's invariance clause is false under U for a reason the run had
already established two rungs earlier and did not carry forward when writing
the prediction; that is a miss of attention, not of computation, and it is
recorded next to its value rather than reworded.  The previous rung's
extrapolation, written before this rung existed, is PARTIAL on the clause that
mattered most: it predicted that reading O would meet the requirement again
with no new declaration, and reading O does not.  As at every earlier rung, the
predictions were written by an instrument that had read the whole tree and
reasoned the rung through, so the hits are evidence of the order of the work
and not of insight; the misses are the evidence that the order was kept.

#### 5.15 What Challenge 4 does not establish

- **The minimality is scoped to the declared space** (definition 56).  A
  candidate outside those seven coordinates — one that changed the event
  grammar again, that grouped marks by anything but the presented whole, that
  admitted two further marks in one step, or that derived the permitted
  renamings from the judgment grammar — is not enumerated, and no claim is
  made about it.  In particular the uniqueness of the U minimum is uniqueness
  *inside that space*, and it is the first uniqueness statement the run makes:
  it is a fact about seven declared coordinates and not about augmentations in
  general.
- Nor is "one step" a discovered notion, and nor is the counting of the
  grouping-with-names as two capabilities rather than one.  A run that declared
  the grouping and its naming a single coordinate would report a second
  minimum under both readings; that the two are separate coordinates is this
  rung's declaration, made because naming tags is exactly the U-versus-O
  distinction one level up, and it is recorded as a declaration.
- The requirement is a statement about a grouping the state does not carry at
  every candidate that does not admit it, and so is its witness.  What
  "internally separable" can mean for a whole is narrowed accordingly, and the
  narrowing is reported rather than repaired.
- The declared whole properties are five, not a survey of everything a
  candidate makes available; the collateral facts are eight, likewise.
- Lean does not close the enumeration, the automorphism counts, the class
  counts, the capability counts, or the two measures.  It closes the
  obstruction, the judgment-form family with its countermodel, the two marks
  that share a side, and the continuation theorem.
- The Lean model carries no token and no grouping, so the label-keeping
  coordinate and the two grouping coordinates have no Lean counterpart; what
  Lean states about the wholes is stated through the index map
  `exchangeWholes`, whose correspondence with the Python renaming of a
  configuration is prose.
- Nothing about a whole within a side, depth, or the outside of the boundary.
  Challenge 5 is not reached.

#### 5.16 Dependence on the admitted boundary

| result | dependence |
|---|---|
| the declared sense, its second reading, the pointwise sense, and their comparison | independent of the boundary; they are about renamings, orbits, and mark-sets |
| the identity of the candidate space, the capability counts, the one-step rule, and the refusal of bundles | independent of the boundary |
| the whole grouping, the tag property, the index property, and the withdrawal of the mark permutations | independent of the boundary: a group tag and an admission index are carried by the caller's history and by the placement tuple's length, not by the sides |
| the widened reader bound and the within-whole order | require the admitted boundary in the weak sense that a presented side is what they read; the widening itself is about how many marks a whole may carry, which the boundary does not decide |
| the side exchange, its withdrawal, the two side-reading whole properties, the label-and-side property, the grouping square's cells, and every separation result of the rung except the index withdrawal | require the admitted boundary and are not formulated after removing it |
| the further-mark coordinate | requires the admitted boundary: the further mark is admitted ON a side, and there is no other coordinate for it to move |

The one exception in the fifth row is stated because Challenge 3's
corresponding row said "every separation result of the rung" without one, and
the withdrawal of the mark permutations is a separation result that the row
above it classifies as independent of the boundary.  Both rows are corrected
here.  The Challenge 4 receipt's own field repeated the same defect and was
corrected with them, in the review repair recorded in `change_log.md`; the
Challenge 3 receipt's field is carried, with its reason, in
`challenge4/STATUS.md`.

### 5.17 Challenge 5

Not yet reached.  It opens in a fresh session with its own frozen
`PREDICTIONS.md`.  This rung's reader refuses `<<a|>|>` by name, which the
receipt records and does not act on.

## 6. The autonomous branch procedure

Not yet declared; it is declared after Challenge 3 by the seed's order.

## 7. Proofs and countermodels

Lean package `lean/`, core Lean only, no dependency on any other package
in this repository.  One hundred and thirty-nine theorems, every one with a
`#print axioms`
report in `lean/axioms.txt`, checked against a successful clean and fresh
build by `verify_lean.py`; every report lies within
`{propext, Quot.sound}`.  `verify_lean.py` also requires every module under
`lean/BoundarySeed/` to lie in the root's import closure, because a module
the root does not reach is text-scanned but never elaborated; that check was
added at Challenge 1 after the hole was observed live and is proved by
injection.

The word *every* in the first sentence is now checked.  Through Challenge 1
it was not: the log comparison compares the reports the build happens to
emit, so a theorem added with no `#print axioms` line would leave every gate
green and this sentence silently false.  `verify_lean.py` now enumerates the
theorems declared under `lean/BoundarySeed/` from the source text, with
block and line comments stripped first, and requires each to carry a report
line in the root module.  It fails by name on a theorem with no line, and
the counterfactual was observed on the same tree: with the check removed,
the same injected theorem left the build reporting `lean ok: 84 axiom
reports … matching lean/axioms.txt`.  What the check does not do is read the
compiled environment, so a theorem the source-text scan cannot see would
escape it; the scan's population and the root's citation list currently
agree exactly, 139 and 139, in both directions.

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

**Where that line runs, and what it is not.**  `side_names_distinct`
(DEFINITION-level, above) and `admitted_candidates_unequal` (content, 7.2)
are both constructor-distinctness facts once their definitions are
unfolded, and a reader is right to ask what separates them.  The run's line
is this: `side_names_distinct` is a closed statement with no free variable,
closed by `decide` on two constructors, while `admitted_candidates_unequal`
is parametrised over the reading and the side and needs `admitted_eq`
rewritten in and a case split on the side before the constructors disagree.
That is a line about the shape of the proof obligation, not about
mathematical depth, and it is a convention of this run's labelling rule
rather than a discovered distinction.  It is stated here because the paper
drew the line without saying where it ran.  Under a stricter reading of the
same rule `admitted_candidates_unequal` would be DEFINITION-level too; that
would not move C1-5, whose content also rests on the unpruned search, and
the alternative is recorded rather than silently declined.

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

### 7.3 Challenge 2 (`Challenge2.lean`)

The Lean events carry no token, so the shared visible mark is invisible in
this file: `place` always adds a fresh entry to the placement list, and a
mark's internal identity is its position there.  The identity question the
shared mark raises is therefore a question about the Python kernel's
label-keyed admission, decided there, and the theorems below record what
follows once two marks lie on opposite sides.  Every theorem about the
retained regime is stated for every reading, with one exception:
`retained_composite_permitted_U`, which pairs the Challenge 0 permission
with the composite and is therefore stated at `.U`.  The three involution
lemmas are about an arbitrary argument and name no reading.  Which theorem
is *meaningful* under which reading is prose, because whether the
reflection is permitted is a fact about the reading and not about the
placement.

| theorem | statement | axioms |
|---|---|---|
| `retained_eq` | the caller's Challenge 2 history replays to two marks on opposite sides | none |
| `retained_placement_length` | the retained regime has two marks | none |
| `retained_without_supplies` | dropping the two supplies leaves the same regime | none |
| `retainedOtherOrder_eq` | the other retention order replays to the exchanged placement | none |
| `retained_onSide_zero` | mark 0 lies on one side and not the other | propext |
| `retained_onSide_one` | mark 1 lies on the other side and not the first | propext |
| `retained_onSide_beyond` | no judgment naming a third mark holds | propext |
| `retained_onSide_true_iff` | exactly two mark-on-side judgments hold, one per mark | propext, Quot.sound |
| `retained_marks_differ_in_side` | the two retained marks do not lie on the same side | propext |
| `retained_sideNamed` | every side-name judgment holds as at genesis | propext |
| `retained_contents_false` | one side's extension is the first mark | propext, Quot.sound |
| `retained_contents_true` | the other side's extension is the second | propext, Quot.sound |
| `retained_sides_differ` | the two extensional side profiles differ as raw data | propext, Quot.sound |
| `exchangeFirstTwo_involutive` | the exchange of the first two internal identities is an involution | none |
| `swapFirstTwo_involutive` | its action on a placement list is an involution | propext |
| `exchangeMarks_involutive` | its action on a regime is an involution | propext |
| `exchangeMarks_reflect_retained` | the reflection followed by that exchange carries the retained regime to itself | propext |
| `reflect_retained_ne` | the reflection alone does not | propext |
| `exchangeMarks_retained_ne` | the mark exchange alone does not | propext |
| `retainedOtherOrder_is_exchange` | the other retention order is the mark exchange of the first | propext |
| `retainedOtherOrder_ne_retained` | the two orders give different raw regimes | propext |
| `retained_composite_permitted_U` | under U the composite uses a renaming the reading permits | propext |
| `retained_exchange_transports` | the composite carries every mark-on-side judgment of one retained mark to the corresponding judgment of the other, with the side exchanged | propext |
| `retained_marks_separated_by_a_side` | without the side exchange, one judgment form holds of one mark and not the other | propext |
| `retained_judgments_survive` | each retained mark's judgment survives every later history of the Lean grammar | propext |
| `retained_reading` | the retained regime keeps the reading | none |
| `retained_initialDatum` | it keeps the initial datum | none |
| `no_event_follows_retained` | no event follows from it | propext |

No countermodel is needed at Challenge 2: no target failed.
DEFINITION-level, true by unfolding or by instantiating an earlier theorem,
and not counted as content: `retained_eq`, `retained_placement_length`,
`retained_without_supplies`, `retainedOtherOrder_eq`,
`exchangeMarks_reflect_retained`, `retainedOtherOrder_is_exchange`,
`retained_composite_permitted_U` (a pairing of the Challenge 0 permission
with the `rfl` above), `retained_sideNamed`, `retained_judgments_survive`,
`retained_reading`, `retained_initialDatum`, and `no_event_follows_retained`
(the last five instantiations of Challenge 0 or Challenge 1 theorems).  The
content is the evaluations at the retained regime (`retained_onSide_zero`,
`retained_onSide_one`, `retained_onSide_beyond`,
`retained_onSide_true_iff`, `retained_marks_differ_in_side`,
`retained_contents_false`, `retained_contents_true`,
`retained_sides_differ`, `retained_marks_separated_by_a_side`), the
transport theorem `retained_exchange_transports`, the two non-fixing
theorems `reflect_retained_ne` and `exchangeMarks_retained_ne` with
`retainedOtherOrder_ne_retained`, and the involution lemmas
`exchangeFirstTwo_involutive`, `swapFirstTwo_involutive`, and
`exchangeMarks_involutive`.

What Lean does **not** close at this rung: that the permitted automorphisms
of the retained regime are exactly the two listed under U and the one under
O.  That is the Python computation over the unpruned `permitted_images`
search; the Lean file exhibits the composite and shows that neither half
fixes the regime alone, which is weaker.  Nor does Lean carry the identity
policies, the labels, or the conventions, all of which are Python-only.

### 7.4 Challenge 3 (`Challenge3.lean`)

Two families the Python enumeration cannot close on its own.  The first is
every candidate that only adds judgment forms:
`no_invariant_mark_property_separates_retained` quantifies over an ARBITRARY
property of a `(Regime, Nat)` pair, so it covers every form the closed
grammar might gain and not only the one the declared space enumerates.  Its
hypothesis is a real restriction and not a vacuous one, which
`mark_form_is_not_invariant_under_the_composite` exhibits.  The second is the
further-mark candidate: a renaming of the marks is a permutation of the
placement, a permutation preserves how many marks lie on each side, and the
side exchange exchanges those counts, so at a placement whose sides carry
different numbers no renaming undoes the exchange — for every permutation,
not for the ones a bounded search enumerates.  `retained_counts_equal`
records the converse at the retained regime itself.

Every theorem is stated for both readings; which is meaningful under which
is prose, because whether the side exchange is permitted is a fact about the
reading and not about the placement.  `retained_U_requirement_fails` is the
one exception and is stated at `.U`, pairing the Challenge 0 permission with
the Challenge 2 composite.

| theorem | statement | axioms |
|---|---|---|
| `composite_retained` | the side exchange followed by the mark exchange carries the retained regime onto itself | propext |
| `exchangeFirstTwo_zero` | that exchange sends the first internal identity to the second | none |
| `exchangeFirstTwo_one` | and the second to the first | none |
| `retained_U_requirement_fails` | under U the SIDE EXCHANGE is permitted, the composite fixes the retained regime, and the mark exchange carries mark 0 to mark 1 | propext |
| `no_invariant_mark_property_separates_retained` | every property of a mark that the composite leaves alone takes the same value at the two retained marks | propext |
| `mark_form_is_not_invariant_under_the_composite` | neither mark form is such a property: a countermodel at the retained regime | propext, Quot.sound |
| `countOn_nil` | the empty placement puts no mark on a side | none |
| `countOn_cons` | the count of a placement is its head's contribution plus the count of its tail | none |
| `countOn_map_not` | the side exchange exchanges the two counts | none |
| `countOn_perm` | a permutation of the placement preserves each count | none |
| `reflect_not_undone_by_renaming` | at a placement whose two sides carry different numbers of marks, no permutation of the reflected placement is the original | none |
| `retainedPlus_eq` | the further mark appends its side to the retained placement | none |
| `retainedPlus_reading` | the further mark keeps the reading | none |
| `retainedPlus_initialDatum` | it keeps the initial datum | none |
| `retainedPlus_placement` | its placement, with the reading projected away | none |
| `retained_placement` | the retained placement, likewise | none |
| `retainedPlus_counts_differ` | after the further mark the two sides carry different numbers of marks | none |
| `retainedPlus_reflection_is_not_an_automorphism` | so no permutation of the reflected placement returns it | none |
| `retained_counts_equal` | at the retained regime itself the two counts are equal, so the counting argument says nothing there | none |
| `retainedPlus_judgments_survive` | both retained marks keep their judgments after the further mark | propext |
| `no_event_follows_retainedPlus` | no event follows from the further-mark regime | propext |

No countermodel target failed at Challenge 3, and one countermodel was
sought and found on purpose: `mark_form_is_not_invariant_under_the_composite`
exists to show that the HYPOTHESIS of the theorem above it is a real
restriction and not a vacuous one.  An earlier version of this sentence said
the theorem was not vacuous, which is a different statement and is not the one
the countermodel supports; the sentence four lines above it in 7.4 had it
right.
DEFINITION-level, true by unfolding or by instantiating an earlier theorem,
and not counted as content: `composite_retained` (the Challenge 2 `rfl`
under a new name), `exchangeFirstTwo_zero`, `exchangeFirstTwo_one`,
`retained_U_requirement_fails` (a pairing of two earlier results),
`countOn_nil`, `countOn_cons`, `retainedPlus_eq`, `retainedPlus_reading`,
`retainedPlus_initialDatum`, `retainedPlus_placement`, `retained_placement`,
`retainedPlus_judgments_survive`, and `no_event_follows_retainedPlus` (the
last two instantiations of Challenge 1 and Challenge 0 theorems).  The
content is `no_invariant_mark_property_separates_retained`, its countermodel
`mark_form_is_not_invariant_under_the_composite`, the induction lemmas
`countOn_map_not` and `countOn_perm`, and the three theorems that use them:
`reflect_not_undone_by_renaming`, `retainedPlus_counts_differ`, and
`retainedPlus_reflection_is_not_an_automorphism`, with `retained_counts_equal`
recording where the argument stops.

Two of the placement lemmas exist for a mechanical reason and the paper says
so: a decision procedure was offered a goal carrying the reading as a free
variable and refused it, so the placement is projected out first.  That is
apparatus, not mathematics.

What Lean does **not** close at Challenge 3: the enumeration of the declared
candidate space, the capability counts, the class count, the collateral
facts, and the two measures.  All of those are the Python computation.  Nor
does the Lean model carry a presentation label, so the coordinate that keeps
the labels has no Lean counterpart at all.

### 7.5 Challenge 4 (`Challenge4.lean`)

Three things the Python enumeration cannot close on its own.  The first is the
obstruction: `exchangeWholesRegime_crossRetained` says that the exchange of the
two wholes carries the retained regime onto itself, and it uses **no side
exchange**, which is why the requirement fails under both readings where at
Challenge 3 the O reading already met it.  The second is the family of
candidates that only add judgment forms:
`no_invariant_pair_property_separates_the_wholes` quantifies over an ARBITRARY
property of a regime and an ordered pair of internal identities, and
`firstIsMarkZero_is_not_invariant_under_the_whole_exchange` exhibits a property
outside its hypothesis — the property that reads an admission index, which is
exactly what the Python enumeration's one minimum under U makes available.  The
third is stronger than anything the enumeration reaches:
`whole_exchange_survives_every_continuation` shows that the exchange still
carries the regime onto itself after ANY later history of the Lean grammar, so
no number of further marks removes the obstruction, where the enumeration
reaches one.

The Lean model carries no token and no grouping.  A whole is therefore named
here by the index map `exchangeWholes` and not by a state component, and the
correspondence between that map and the Python renaming of a configuration is
prose, as the correspondence between `List.Perm` and `rename_marks` was at
Challenge 3.  Every theorem is stated for both readings; which is meaningful
under which is prose, because whether the side exchange is permitted is a fact
about the reading and not about the placement — and at this rung the
obstruction is permitted under both.

| theorem | statement | axioms |
|---|---|---|
| `crossRetained_eq` | the caller's Challenge 4 history replays to four marks, one of each whole on each side | none |
| `crossRetained_placement` | its placement, with the reading projected away | none |
| `crossRetained_placement_length` | it has four marks | none |
| `crossRetained_onSide_zero` | the first mark lies on one side and not the other | propext |
| `crossRetained_onSide_one` | the second lies on the other | propext |
| `crossRetained_onSide_two` | the third lies where the first does | propext |
| `crossRetained_onSide_three` | the fourth lies where the second does | propext |
| `crossRetained_onSide_beyond` | no judgment naming a fifth mark holds | propext |
| `crossRetained_onSide_true_iff` | exactly four mark-on-side judgments hold, one per mark | propext, Quot.sound |
| `crossRetained_marks_share_a_side` | **the boundary does not separate two marks that share a side**: the first and third marks satisfy the same mark-on-side judgments | propext |
| `crossRetained_other_marks_share_a_side` | the same of the other such pair, the second and fourth marks, so that both pairs are proved and not one | propext |
| `crossRetained_sideNamed` | every side-name judgment holds as at genesis | propext |
| `exchangeWholes_involutive` | the exchange of the two wholes is an involution on internal identities | none |
| `exchangeWholes_zero` | it sends the first identity to the third | none |
| `exchangeWholes_one` | and the second to the fourth | none |
| `exchangeWholes_carries_the_first_whole` | so it carries the first whole's marks onto the second's | none |
| `swapWholes_involutive` | its action on a placement list is an involution | propext |
| `exchangeWholesRegime_involutive` | its action on a regime is an involution | propext |
| `exchangeWholesRegime_crossRetained` | **it carries the retained regime onto itself, with no side exchange** | propext |
| `reflect_crossRetained_ne` | the side exchange alone does not | propext |
| `exchangeMarks_crossRetained_ne` | nor does the Challenge 2 exchange of the first two identities | propext |
| `no_invariant_pair_property_separates_the_wholes` | every property of a pair of marks that the whole exchange leaves alone takes the same value at the two retained wholes | propext |
| `no_invariant_mark_property_separates_the_paired_marks` | the same for a property of a single mark, at the two marks that share a side | propext |
| `firstIsMarkZero_separates_the_wholes` | the property that reads whether the first mark of a pair is the first admitted mark does separate them | propext |
| `firstIsMarkZero_is_not_invariant_under_the_whole_exchange` | so it lies outside the hypothesis above: a countermodel | propext |
| `crossRetained_counts_equal` | the two sides carry equally many marks, so the Challenge 3 counting argument says nothing here | none |
| `replay_placement_append` | replaying any history appends to the placement | propext |
| `exchangeWholesRegime_of_prefix` | a regime whose placement begins with the retained one is carried onto itself by the exchange | propext |
| `whole_exchange_survives_every_continuation` | **so no continuation whatever removes the obstruction** | propext |
| `whole_exchange_survives_a_further_mark` | in particular one further mark on either side, the Challenge 3 third minimum, does not | propext |
| `crossRetained_judgments_survive` | each retained mark's judgment survives every later history | propext |
| `crossRetained_reading` | the retained regime keeps the reading | none |
| `crossRetained_initialDatum` | it keeps the initial datum | none |
| `no_event_follows_crossRetained` | no event follows from it | propext |

One countermodel was sought and found on purpose:
`firstIsMarkZero_is_not_invariant_under_the_whole_exchange` exists to show that
the HYPOTHESIS of the theorem above it is a real restriction and not a vacuous
one.  DEFINITION-level, true by unfolding or by instantiating an earlier
theorem, and not counted as content: `crossRetained_eq`,
`crossRetained_placement`, `crossRetained_placement_length`,
`exchangeWholes_involutive`, `exchangeWholes_zero`, `exchangeWholes_one`,
`exchangeWholes_carries_the_first_whole`, `exchangeWholesRegime_crossRetained`
(`rfl` on the four-entry placement), `crossRetained_marks_share_a_side` and
`crossRetained_other_marks_share_a_side` (the two evaluations of each pair
rewritten together), `crossRetained_sideNamed`,
`crossRetained_judgments_survive`, `crossRetained_reading`,
`crossRetained_initialDatum`, and `no_event_follows_crossRetained` (the last
four instantiations of Challenge 0 and Challenge 1 theorems).  The content is
the evaluations at the retained regime (`crossRetained_onSide_zero` to
`crossRetained_onSide_beyond`, `crossRetained_onSide_true_iff`), the two
non-fixing theorems `reflect_crossRetained_ne` and
`exchangeMarks_crossRetained_ne`, the involution lemmas `swapWholes_involutive`
and `exchangeWholesRegime_involutive`, the two general theorems with their
countermodel, `crossRetained_counts_equal`, and the induction
`replay_placement_append` with `exchangeWholesRegime_of_prefix` and the two
continuation theorems that use them.

That `exchangeWholesRegime_crossRetained` is `rfl` is worth saying plainly: the
obstruction of this rung is true by unfolding the placement, and it is not
therefore a small fact.  What is DEFINITION-level is that this particular map
fixes this particular regime; what is not is that no property of the declared
kind can separate what it exchanges, and that no continuation removes it.

What Lean does **not** close at Challenge 4: the enumeration of the declared
space, the capability counts, the class counts, the collateral facts, the two
measures, the whole-property census, and the key-determination clause that
census turns on.  All of those are the Python computation.  Nor does the Lean
model carry a presentation label or a grouping, so three of the seven
coordinates have no Lean counterpart at all.

## 8. Receipts

- `receipts/challenge0.json` through `receipts/challenge4.json`:
  deterministic (sorted keys, LF, no timestamp, no environment value);
  regenerated byte-identically by `run_challenge0.py` through
  `run_challenge4.py` and checked by the tests and by the research job.
- The Challenge 2 receipt is 35499 bytes, the Challenge 3 receipt 220518,
  and the Challenge 4 receipt 795960, all inside the megabyte at which the
  run would owe a summary and a gzip with a content hash, so all are
  committed whole; a test holds each of the last two to that bound.  The
  Challenge 4 receipt is large because the enumeration IS the evidence: 192
  points under each reading, each with its coordinates, its cost under both
  measures, the collateral facts that hold of it, and its class key.  Its
  point rows carry the facts that HOLD rather than eight booleans, and the
  full map is on the nine rows the rung reports in full; that is what keeps
  it inside the bound, and it is recorded because a later rung adding keys
  to a point row has less room than the number alone suggests.
- The Challenge 0 to Challenge 3 receipts were byte-unchanged across
  Challenge 4, which is the check that the kernel additions did not disturb
  the earlier rungs: the configuration enumerations are new functions and
  change no value any earlier receipt reports, and the one Challenge 3
  repair this rung made is a docstring, which no receipt carries.  The same
  held at Challenge 3 for the three receipts before it, and at Challenge 2
  for the two before that.
- The Challenge 1 receipt was regenerated deliberately once more at the
  third review repair, when the DEFINITION-level bases of C1-1, C1-3, and
  C1-6 and the prediction tally became receipt keys, and once more at the
  fourth, when C1-5's clauses were scored on the frozen words and the
  convention pinned, and once more at the fifth, when C1-7's evidence was
  rescoped to the candidate regimes, C1-5's basis relabelled, and the two
  designation clause facts reworded, with no injection live any time.
- The suite passes 303 tests.  Fresh coverage over the eight declared code
  files is 100.00% line and 100.00% branch; `check_coverage.py` computes
  line coverage as covered lines divided by statements rather than
  Coverage.py's combined line-plus-branch percentage.
- `lean/axioms.txt`: 139 reports.  It was regenerated once at Challenge 1
  when the theorem set was final, three more times during that rung's
  review repairs, once at Challenge 2 when its twenty-eight theorems were
  final, 56 to 84 reports, once at Challenge 3 when its twenty-one were
  final, 84 to 105, and once at Challenge 4 when its thirty-three were
  final, 105 to 138, and once at this rung's review repair when the
  companion theorem for the other pair sharing a side was added, 138 to 139;
  no regeneration was under a live injection.
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
called for.  Every continuation of either candidate, **in the Lean
grammar**, is the reflection of a continuation of the other, by a
replay-level theorem over histories of supplies and placements; the Python
kernel's version is tested to three events over two tokens and is not
claimed beyond that bound, and neither statement covers the Python-only
re-admission no-op or the refusals, whose events the Lean grammar does not
carry.  No event follows from any of these states.

At Challenge 2 the caller supplies and retains `<a|>` and `<|a>`, the same
visible mark on the other side.  The caller's history under the Challenge 1
admission event is refused by name, under both readings and both
conventions, because that event keys the admitted mark by its presentation
token; of the two identity policies in the declared space, exactly one
lets the caller retain both wholes, and the run declares it at the price of
one new admission event and the withdrawal of the rule that admitted labels
be distinct.  The run pays that price, not the boundary and not the caller,
and pays the same under both readings.  The retained state then holds two
marks, one on each side, and the two admissions add exactly two holding
judgments and change no name judgment, datum, or reading; both judgments
survive every later history of the Lean grammar.  Under U the retained
regime has exactly two permitted automorphisms, and the non-identity one
exchanges the two marks and the two sides at once: neither pair is
internally separable, neither mark form is invariant, and the profile
comparison of Challenge 0 is false there without being the internal fact.
Under O the only permitted automorphism is the identity, both mark forms
are invariant and both separate the marks, and one whole lies on `near` and
the other on `far`.  Under both readings the two marks do not share a side,
and that property is invariant under every permitted renaming of a census
over placements of at most three marks; the admission order of the two
wholes, the shared visible mark, and the presentation convention are all
carried away by a permitted renaming and are not internal facts.  So the
admitted boundary alone distinguishes the two wholes under O and not under
U, and what it buys under U is that they are not on the same side.

At Challenge 3 the caller requires those two wholes to be internally
separable, and the run declares the requirement to be the sense Challenge 2
computed, with a second reading — some mark property that forgets whatever the
candidate's declared serialization forgets, and that is invariant under every
permitted renaming, holds of one and not the other.  The declared orbit
witness gives one direction of the agreement by unfolding; the direction back,
from an arbitrary property of that kind to the first reading, is definition
33's justifying sentence and is prose, computed at no point.  Under O
the requirement is already met, and the four-cell counterfactual shows that
what meets it is the half of the O declaration that withdraws the side
exchange and not the half that admits the names: the minimum capability
count under O is zero, attained by the null augmentation alone, and nothing
is paid at this rung.  Under U the requirement fails, and no addition of
judgment forms can meet it while the composite of the side exchange with the
mark exchange remains a permitted renaming — proved in Lean for an arbitrary
property of a mark, with a countermodel putting both mark forms outside the
hypothesis, so that the hypothesis is a real restriction and not a vacuous
one.  Over the declared space of 48 points, the minimum capability count
under U is one, four one-step points attain it, and they fall into **three**
non-isomorphic classes, all retained: withdraw the
side exchange; withdraw the mark permutations; or admit one further mark on
either side.  **The minimum is therefore not unique**, and the candidate
that adopts reading O under U costs two capabilities and is refused as a
bundle, its withdrawal half alone being one of the three minima.  The second
of the three meets the requirement by unfolding, by declaring the
metatheoretic admission index internally available, and so meets it
while leaving the admitted boundary idle; the third meets it because the two
sides then carry different numbers of marks, which no renaming of the marks
can repair — proved in Lean over every permutation.  Under U the second
declared measure, the collateral count, selects the same three minima; under
O it does not — its minimum of zero is attained by five points in three
classes, while the capability count's minimum is the null augmentation alone.
Under both readings the two measures are not the same function on the space.

At Challenge 4 the caller supplies and retains `<a|b>` and `<b|a>`, two wholes
with a mark on each side of the boundary.  The Challenge 1 reader refuses both
by name, so the run declares a widened reader — at most one mark on each side —
and a within-whole admission order, and pays for both; the narrower reader is
left refusing.  The caller's history is then a supply and an occurrence
admission for each of four marks, and the retained state under each reading has
placement `(0, 1, 0, 1)` with labels `("a", "b", "b", "a")`.  A whole is a set
of marks, and **the regime carries no grouping of marks into wholes**: the
requirement, and its declared witness, are statements about the automorphisms
of the state and about a grouping read off the caller's history, at every
candidate that does not admit that grouping.  In the declared sense — no
permitted automorphism carries the mark-set of one whole onto the other's —
**the requirement fails under BOTH readings**, the first rung at which reading
O does not already meet it.  The obstruction is the exchange of the two wholes,
a permutation of the marks that carries the retained regime onto itself using
no side exchange, so the withdrawal the O reading carries does not touch it;
that is proved in Lean, as is the fact that no property of a pair of marks
which that exchange leaves alone separates the two wholes, with a countermodel
putting the property that reads an admission index outside the hypothesis, and
as is the stronger fact that **no continuation whatever removes the
obstruction**, however many further marks are placed.  What the boundary
contributes is the side each mark lies on, and each side now carries one mark
of each whole: under O it still separates the four pairs of marks that lie on
different sides and neither of the two that share one, which is proved, and so
it separates no whole from the other.  What it cannot contribute is which mark
within a side is which, the grouping into wholes, and the matching of a visible
mark across the boundary — the configuration in which the second whole's copy
of `a` is a token the caller never presented is reached by a permitted renaming
under both readings.  Over the declared space of 192 points the minimum
capability count is one under each reading, and the two readings differ in what
attains it: under U exactly one class does, the withdrawal of the mark
permutations, which meets the requirement by unfolding and leaves the boundary
idle, so **uniqueness is not refuted there** — the first rung at which it is
not, and inside the declared space only; under O two tied classes do, that
withdrawal and the keeping of the presentation labels, which meets it under O
alone because the two wholes are each other's reflection and reading U cannot
see the reflection.  The augmentation the caller's demand actually names, the
whole grouping with the two wholes named, meets the requirement under both
readings at a capability count of two and is **refused as a bundle**; neither
half alone is a minimum, the grouping alone leaving the tag exchange a renaming
the object language cannot see and the names alone naming tags no mark carries.
The Challenge 3 sense taken pointwise implies the declared sense at every point
of the space and the converse fails inside it, so the two are not the same
requirement; at the Challenge 3 configuration, where each whole is one mark,
they agree.

These are scoped Lean theorems, bounded computations, or labelled
definitions and conventions.  Because the instrument declared prior
exposure, they carry no blind-independence or independent-discovery
conclusion.

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
- `Supply` carries the token only.  Challenge 2 said, loudly, what the two
  wholes with the same visible mark are: the token-keyed admission refuses
  the caller's history by name, and the run declared an occurrence-keyed
  admission and withdrew the repeated-label rule to accept it.  The
  refusal, the space it was chosen from, and the price are in the receipt;
  nothing was absorbed silently.
- The two identity policies are exhaustive over the question “what does the
  second admission of the caller's two wholes admit”, and over nothing
  wider.  A treatment that changed the event grammar further — an event
  that admits a pair, say — is outside the declared space, and the
  uniqueness claim is scoped to the space accordingly.
- The Challenge 2 automorphism counts, the mark-form invariance, and the
  different-sides census are bounded computations; the Lean file exhibits
  the composite that fixes the retained regime and shows that neither half
  fixes it alone, which is weaker than the count.
- Definition 33's sense of internal separability is this rung's, declared
  to answer this rung's question.  Challenge 3 declared the same sense
  (definition 38) and added a second reading of it that agrees by
  unfolding; a different sense was available and is not explored.
- **The Challenge 3 minimality is scoped to the declared space** of five
  coordinates (definition 40) and to the run's declaration that one moved
  coordinate is one step.  Nothing is claimed about an augmentation the
  space cannot express.
- **The permitted renamings are declared and not derived.**  Definition 16
  makes permission a declaration, which is why admitting the side names
  under U changes no automorphism and why the counterfactual square turns on
  one coordinate only.  A model in which the permitted renamings were
  exactly the maps preserving every declared judgment is a different
  candidate space: there, admitting the names would withdraw the side
  exchange in one move, and the enumeration would have to be redone.  That
  model is OPEN and is not enumerated.
- The three Challenge 3 minima are tied under both declared measures.  A
  third measure could separate them; none is offered.
- One of the three meets the requirement by unfolding, by making the
  metatheoretic admission index internally available, and so meets the
  requirement as declared while leaving the admitted boundary idle.  The run
  reports that rather than excluding it: no declaration of the run rules the
  candidate out, and the requirement as declared does not oblige the
  boundary to do the work.  Whether the requirement should have been
  declared so as to exclude it is OPEN.
- The further-mark minimum uses the token the caller supplied, so it needs
  no supply of its own; what it needs is that the process, and not only the
  caller, issues an event, which definition 25 does not license.  The
  candidate is enumerated and priced; nothing is admitted by it.
- **The Challenge 4 minimality is scoped to the declared space** of seven
  coordinates (definition 56) and to the run's declaration that one moved
  coordinate is one step.  The uniqueness of the U minimum is the run's first
  uniqueness statement and is uniqueness *inside that space*: a run that
  declared the whole grouping and its naming a single coordinate would report a
  second minimum under both readings, and that they are two coordinates is this
  rung's declaration, made because naming tags is the U-versus-O distinction
  one level up.
- **The Challenge 4 requirement is about a structure the state does not carry.**
  The grouping of marks into wholes is metatheory read off the caller's
  history, so the requirement and its orbit witness are statements about the
  automorphisms of the state together with that grouping at every candidate
  that does not admit it.  What "internally separable" can mean for a whole is
  narrowed accordingly.  The run reports the narrowing rather than repairing it,
  and prices the repair: it is the grouping coordinate, and with the naming it
  costs two.
- The Challenge 4 whole-property census turns on two conjuncts, invariance and
  determination by the candidate's key.  The second was live: without it the
  property that reads the group tag is reported as a witness at the very base
  where the requirement fails.  It is Challenge 3's token-forgetting clause
  generalized, and the Challenge 3 census, which carried the first conjunct
  only, is left as it stands: its one anomalous property, the label reader, was
  reported there as invariant and separating nothing, so no result of that rung
  moves — but a reader comparing the two censuses should know they are not the
  same test.
- The five declared whole properties and the eight declared collateral facts
  are declared lists, not surveys.  Neither of the two facts nearest the
  requirement tracks it at every point, which is what Challenge 3's did; that
  is reported and is not a repair of the Challenge 3 measure, which stands as
  it was computed.
- The Lean model carries no token and no grouping, so three of the seven
  Challenge 4 coordinates have no Lean counterpart, and a whole is named there
  by an index map whose correspondence with the Python renaming of a
  configuration is prose.
- Whether a whole within a side is admissible is still OPEN.  This rung's
  widened reader refuses `<<a|>|>` by name, which the receipt records; what the
  inner whole is belongs to Challenge 5.

- The audit-totality check reads the Lean source text, not the compiled
  environment.  A theorem it cannot see in the text would escape it, and
  the two populations agree today by count and by name in both directions.
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
