# 13. Labels do not certify steps

A record may name plausible endpoints and still misdescribe the event
between them. We now use the actual passage step rule, not the toy switch.

Start at the empty initial passage state. Two events have different effects:

| Event | Computed result |
|---|---|
| admit occurrence 0 | occurrence list becomes [0]; terminal flag stays false |
| halt | occurrence list stays empty; terminal flag becomes true |

Consider a row that says **empty initial state — admit occurrence 0 →
halted empty state**.

**Predict:** the endpoints really are connected by halt. Does that validate
the event label written on this row?

<details><summary>Check the recorded event</summary>

No. Decoding the written label gives an occurrence admission. Applying
that event gives a different target from the one recorded. A path between
the endpoints exists, but it uses a different event. The research's
read-back check rejects the row rather than silently replacing its label.

</details>

## A second, independent check: the rows must join

Suppose two rows each start from the empty initial state. One correctly
records occurrence admission; the other correctly records halt. Each row
passes by itself, but the first row ends in a state with one occurrence.
The second starts in an empty state. They cannot be consecutive rows of
one history as written.

The desk checks both adjacency and the actual event equation. An unknown
label also fails: a decoder must be supplied before the label has an event
meaning in this model.

**Try a change:** repeat the occurrence admission after it has already
occurred. The passage keeps the state, because the occurrence is already
present. That inert step is valid; deleting it would change the history.

Try [Path practice](PATH_PRACTICE.md), then open the
[answers](PATH_ANSWERS.md). Use the [step desk](results.html#native-path-panel)
to compare all seven recorded trace cases.

<details><summary>Source boundary for programmers</summary>

The native Lean `Trace` type already requires adjoining endpoints.
`native_bridge.bridge.realize` checks each row's label and target but
does not check adjacency in an arbitrary Python row list. Our book wrapper
adds that gate. A Python helper's success alone is therefore weaker than
constructing the indexed Lean trace. The research owner is unchanged.

</details>

AuthorityEffect: None. NB-12 and NB-13 own the native read-back result
and mislabelled-step counterexample. Labels, target-event recipes, and
the optional physical meaning of any event remain supplied choices.
