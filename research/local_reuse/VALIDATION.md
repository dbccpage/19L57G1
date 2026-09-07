# Local validation

AuthorityEffect: None.

Source baseline: `93853697ed845284ecbb9a9b51a78c9bf5b070cb`.
Platform: Windows, Python 3.14.2, Lean 4.33.0. These are observed local
results on 2026-09-07, not hosted CI results. The commands needed to reproduce
the new packet are in REPRODUCE.md.

| Check | Observed result |
|---|---|
| New packet tests, including counterexamples and verifier mutations | 49 passed, no failures or skips |
| New packet strict typing | passed, four source files |
| New packet computation record | regenerated and byte-identical |
| New packet source guard | passed before and after replay and compilation |
| New packet Lean build and independent theorem census | 31 authored theorems and eight generated helpers; all 39 reported, within `{propext, Quot.sound}` |
| Original prompt hash gate | both frozen hashes match |
| Original transport citations | 190 verified, zero unresolved |
| Original skill declarations | seven checked |
| Original paper cross-references | 62 references across 29 documents resolve |
| Original claim-ledger evidence | 1,152 tokens across 129 entries resolve |
| Original parked-module audit | 75 modules: 63 root-imported and 12 parked |
| Original prose watchlist | unchanged pinned census |
| Original artifact regeneration | all 27 runners succeed; 40 JSON files byte-identical and six full exports content-identical with pinned hashes; both output sets match |
| Original Lean build | 80 build jobs succeed |
| Original recursive module census and explicit elaboration | all 75 pinned modules elaborate |
| Original forbidden-token and reliance audit | 77 sources; all 1,530 enumerated reports within `{propext, Quot.sound}` |
| Original axiom inventory | all 1,530 names match; fresh rendering is byte-identical to the committed artifact |
| Original tests under coverage | passed; one skipped test |
| Original independent dual coverage gate | 99.10% lines and 96.71% branches, both above 95%; fresh report covers the exact 60-source census |
| Original strict typing | passed, all 60 source files |

The original verification workflow also contains separate research-package
jobs and extra research Lean packages. Those untouched packages were not all
rerun locally. The new workflow runs the packet independently; hosted status
must be read from the PR at its actual head.

At initial PR head `d2d9db646c091ea67d54abe73c02cac789543e17`, hosted runs
`34146328611` (the new packet) and `34146328658` (original verification)
failed before execution: all five jobs report `runner_id=0` and empty step
lists. This provides no hosted test or proof result. The local passes above
remain separate evidence; a later head's workflow status must be checked
independently.

All edits are confined to this new packet and its dedicated workflow. No
existing source, frozen input, original proof, or original evidence artifact
is edited. The source guard checks the five sealed trees against the pinned
baseline rather than accepting updated source digests automatically.
