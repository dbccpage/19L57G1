# 06. Replay someone else's result

[Previous](05_why_the_search_stopped.md) · [Search lab](README.md) · [Next: the check's scope](07_match_the_check.md)

## Ask for the moves

A picture of a final ledger does not tell you how it was obtained. Ask for
the **history**: the ordered list of events that built it. **Replay** means
applying those events again from the declared starting state.

Our longer example uses reading L, mu1, at most two items per repair,
forms of at most two slots, five expansion rounds, a pre-expansion guard
of 400, and supply enabled. It records 128 nodes and 130 edges. Its 92
depth-limit nodes retain the implementation's status `completed`.

A **node** records a reached ledger. An **edge** records a move from a
parent node to a child. This is a finite explored graph under those settings.

## Why some arrows merge

Different histories can reach structures that agree up to the declared
relabeling. The graph stores one representative and a **merge edge**
carrying the explicit entry/form maps to it. This export has three merge edges.

The 127 creation edges construct each non-root node once. The other three
edges lead to already represented nodes. A merge keeps its incoming move
and mapping certificate; it does not pretend that two literal histories
were identical.

## What the replay verifier checks

1. Rebuild the root from its history and compare its recorded fingerprint.
2. Follow creation edges to reconstruct every other node.
3. Replay every creation edge and compare the claimed child's fingerprint.
4. Replay every merge edge and check that its explicit relabeling carries
   the result onto the stored child's structure.

A **fingerprint**, here SHA-256, is a computed identifier for serialized
data. It helps detect changed records. Reconstructing and comparing the
records is the substantive replay check; a fingerprint alone says nothing
about whether a mathematical claim was proved.

## Try the portable record

The [authoring guide](DEVELOPMENT.md) gives a command that reads
`reading_L_mu1_rounds5.json` and runs `verify_full_export` without calling
the search routine. A second command recomputes the search and compares
its results with the recorded packet.

**Predict:** what should happen if the root fingerprint is replaced by
zeros, or a merge loses its relabeling map? The verifier rejects each in
the lab's separate in-memory examples. The committed records remain intact.

AuthorityEffect: None. Replay uses a separate path from search, sharing the
declared admission kernel. It is not an independently implemented kernel proof.
