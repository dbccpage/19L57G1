# Units 11–16: answers

Attempt one group of [practice questions](admission_practice.md) first.

## Admissions and comparisons

1. Only A is stored. Supply changes no admitted field; repeated admission
   of A is deduplicated. Admitting B would add a second stored token.
2. No. The empty or single-token starting condition is missing. A bound
   on later admissions alone cannot remove the two existing tokens.
3. The old pair stays collapsed: marked gives Yes on both. The newcomer
   gives No, so the number of distinct profiles grows from one to two.
   Preservation of old comparisons is not preservation of that count.
4. No: index 2 is out of range when the data count is two. The guarded
   admission rejects it. After raw growth, `linked(2,_)` becomes a valid
   context: it answers Yes on 0 and No on 1. This raw record violates the
   instance-range assumption of the fresh-datum preservation theorem.

## Witnesses and relation models

5. Either the admission of A or of B differs from reference C and can
   witness the existential conclusion. The theorem statement promises
   neither a unique witness nor a particular ordinal position.
6. No: reading the same fixed cell gives the same value. If both outputs
   must be A, assign A to that cell. Changing the cell between reads would
   require a different procedure with its own update definition.
7. The carrier elements are unequal. The relation contains no arrows.
   The restriction against self-arrows adds none; an empty relation
   already satisfies it. Carrier inequality and relation membership differ.
8. No. Those are separate mathematical models. A Genesis state change
   needs an explicit permitted event and its successful replay. An intended
   correspondence between the models needs its own definition and evidence.

## Requests and evidence

9. Separation is False; there is no context. `satisfies` is True: the
   empty request collection contains no unmet request. It does not assert
   that every possible pair can be separated.
10. Neither adds a context. The first records the pair; the duplicate
    leaves Python's request set unchanged. `satisfies` is False because
    that recorded pair has no separating witness.
11. `marked(_)` answers No on 0 and Yes on 1. The request remains recorded
    and is now met. The permitted admissions change the context answers;
    recording the request did not itself make that repair.
12. Specify which cards the data represent, what marked means, the
    inspection procedure, and the observation records supporting those
    assignments. A successful replay establishes a model result; it does
    not supply observations of the cards.

Calculations and scope checks support the first eleven answers. The last
question asks for evidence that has not been collected here. These checks
are not evidence that a beginner has learned or retained the ideas.
Return to [Unit 16](units/16_demand_not_met.md), then continue to
[Unit 17](units/17_impose_guard.md).

AuthorityEffect: None. Model answers and an unperformed observation question.
