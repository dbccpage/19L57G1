# 09. Check the whole history

A **history** is an ordered list of events. **Replay** starts from a
declared state and applies the step rule to each event in order.
An empty history contains no events and ends at its starting state.

Using [the switch table](08_states_and_events.md), consider this record:

| Before | Event | Claimed after |
|---|---|---|
| 0 | flip | 1 |
| 1 | hold | 1 |
| 1 | flip | 0 |

**Predict:** can you check the record by looking only at its first and
last states? What must you check between them?

<details><summary>Two checks</summary>

Each event must actually take its row's before-state to its after-state.
Also, a row's after-state must be the next row's before-state. Both checks
pass here. A **path of actual steps** records this connected sequence.

</details>

## Equal endpoints do not give equal histories

Starting at 0, both the empty history and “flip, flip” end at 0. Their
event lists differ. Knowing only the endpoints cannot recover which list
was used.

The native theorem goes in a more careful direction: for a fixed start,
replaying a given event list fixes the end. Within its path definition,
paths with the same endpoints and the same events are equal. The phrase
“same events” is an essential hypothesis.

**Try a change:** change the middle row's claimed after-state to 0 while
leaving the event hold. Its before-state is still 1. That row now fails
the table, even though you could write other rows with the old endpoints.

## Joining histories

You can follow one checked history by another when the first end matches
the second start. The combined event list puts the second list after the
first. For example, from 0, “flip” followed from 1 by “hold, flip” gives
“flip, hold, flip.” No event has to be invented at the join.

Continue with [10. Translate each step](10_translate_each_step.md).
Try the changed examples in [practice](PATH_PRACTICE.md) before its
[separate answers](PATH_ANSWERS.md).

AuthorityEffect: None. `native_bridge` claims NB-1 and NB-2 prove the path
and composition statements for deterministic step functions. An inert
event is an actual step here; this alone does not certify that every event
meets the passage's separate acceptance guards.
