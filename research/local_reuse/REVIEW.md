# Execution and repair record

AuthorityEffect: None.

The packet began from remote main
`93853697ed845284ecbb9a9b51a78c9bf5b070cb` in an isolated worktree. The
existing Genesis implementation and its five sealed trees remain unchanged.
The research question is supplied by the user and is not a blind derivation.

Independent source review located the actual replay and response relations,
the root/continuation distinction, generated-name assumptions, and the fast
candidate domain. The executable witnesses were run against those sources
before writing the summary conclusions.

Two defects in the new audit were found and repaired:

1. The initial restart comparison used a set of selected edge fields. Changing
   `orbits` to 99 was not detected. The comparison now uses complete exported
   node/edge multisets, including emitted events, labels, costs, orbit counts,
   merge data, histories and status. Only IDs and relative depths are
   normalized. Field changes and duplicate-edge mutations must fail.
2. The original export verifier reconstructs histories from creation edges;
   it does not validate every live `Node.history` field. Replacing one such
   history with an empty tuple was not detected by the first cut checker.
   The checker now independently replays each live node's stored history
   against its regime before checking the normalized export and every cut.

The source guard is tested against missing source objects, altered pins,
added or changed sealed sources, duplicate manifest entries, and foreign
module origins, all in temporary fixtures. Original sources are not mutated.

Lean provides 31 authored theorems. Independent environment enumeration also
finds eight compiler-generated theorem helpers. All 39 declarations receive
reports and are audited; the inventory does not hide the helpers to preserve
an initially expected count. The semantic proofs are separate from this
audit apparatus. The compiled statement scope remains the one in CLAIMS.md.

The final scope review included the repository's later passage and trace
definitions. Three additional composition lemmas make shared-prefix replay,
certified interior rewriting, and halted-state absorption explicit on that
model. They import existing definitions and preserve their full state.
