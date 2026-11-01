# Units 04–07: answers

Attempt the [practice](state_history_practice.md) first.

1. Both results keep [A]. The base and the history are separate inputs;
   an empty history returns whatever base it was given.
2. The first event adds P; the second leaves [P] unchanged. There is one
   admitted entry and a two-event history. A policy can select an existing
   admission kind. Its selection rule is separately supplied.
3. Positions (0,2) in F. L has no position naming the initial mark, so
   there is no corresponding pair in its admitted data. Copying position
   0 from F into L changes what it names; L's position 2 is absent too.
4. The resulting ledgers agree, but supply and admission are different
   constructors. The retained event history distinguishes them. A reader
   restricted to the final ledger has not been given that history.
5. The list stays [A, A]. Erasure uses list length, so its count is two.
   Deduplicating a new admission does not remove duplicates from an
   arbitrary starting state. Empty-start replay has a stronger invariant.
6. From empty, translate to bare admission. From [A], translate to supply
   A. A bare admission would incorrectly increase the erased count to two;
   the detailed store stays at one entry. Use the actual base before
   translating the first event.
7. After A there is one datum, so position 1 is absent and the imposed
   demand is refused. Both Lean replays return `none`. The translated
   history contains bare admission and the refused demand, then stops;
   it does not include admission of B. Python reports refusal by raising
   `AdmissionError`, rather than returning Lean's `none` value.
8. The list's declared equality and update rule establish one entry for
   that label. They do not establish one physical person. A physical
   identity claim needs a specified identification procedure and actual
   supporting observations. No such evidence is supplied in this example.

The seven computational questions have implementation checks or selected
Lean witnesses in the existing Unit drivers. Question 8 asks for reasoning
about evidence and is not automatically graded. Return to
[Unit 07](units/07_erasure.md), then [Unit 08](units/08_contexts_and_collapse.md).

AuthorityEffect: None. Model answers, not observed learner scores.
