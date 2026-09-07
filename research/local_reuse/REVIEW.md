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

Two defects in the new audit were found before review, and repaired:

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
added or changed consumed sources, duplicate manifest keys, and foreign
module origins, all in temporary fixtures. Original sources are not mutated.

Its scope was narrowed after review. Schema v1 pinned all five sealed trees by
tree object, diffed all five against the baseline, and refused every untracked
file under any of them. Two consequences were found. A change under `paper/`
or `artifacts/` -- trees this packet never reads -- made it permanently
unverifiable with no repair path. And one untracked scratch file anywhere in
those trees reported a source-integrity failure: the repository's own checkout
carried `prompt/prompt_pr14.md`, so the documented commands would have failed
there on a packet whose every pinned byte was identical.

Schema v2 pins what the packet consumes and says so: `code/derivation`, whose
seven modules `audit.py` imports, and `lean4/Derivation`, whose whole content
the proofs import, both by exact tree object plus a per-file census; the four
Lean configuration files and the seven modules by content hash; and untracked
files refused only where a build or an import would pick them up. That is not
a weaker claim about this packet's inputs. It is the same claim over the
inputs it has.

Both halves were injected against a clean control. A stray untracked file
under `prompt/` and `paper/`, and a change under all three unconsumed trees,
now pass. An untracked `.py` under `code/derivation`, an untracked `.lean`
under `lean4/Derivation`, a changed pinned module, a changed Lean config, and
a committed change to an unpinned module inside a consumed tree all still
fail by name.

Lean provides 31 authored theorems. Independent environment enumeration also
finds eight compiler-generated theorem helpers. All 39 **theorem**
declarations receive reports and are audited; the inventory does not hide the
helpers to preserve an initially expected count. The semantic proofs are
separate from this audit apparatus. The compiled statement scope remains the
one in CLAIMS.md.

Reach, stated exactly: `Inventory.lean` filters on `.thmInfo`, so the census
is theorem-complete over the `LocalReuse` namespace. It reports nothing for
the two inductives (`ResponsePath`, `ContextPath`), their constructors, their
primitive recursors, or the six definitions (`itemEvent`, `roundEvents`,
`pathEvents`, `markedLeft`, `markedRight`, `mapRound`). It DOES report
`ContextPath.brecOn` and `ResponsePath.brecOn`, because a generated recursion
principle over a `Prop` inductive is a theorem; an earlier draft of this
paragraph said recursors were unreported, which contradicted the packet's own
`#print axioms` list two files away. A definition carrying a disallowed axiom
that no theorem reaches would go unreported. That is the same residual the
root `CLAUDE.md` records for the sealed audit, and it is named here rather
than left to a reader: an earlier draft also said "all 39 declarations", which
is the wording that document withdrew as false.

A private theorem would escape the namespace filter entirely, since Lean
registers it as `_private.<module>.<n>.LocalReuse.<name>`. `Inventory.lean`
refuses one rather than trying to spell mangled names, so the census stays
total over the theorems that exist. Injected: `private theorem
zzz_probe_private` made the build fail with
`LOCAL_REUSE_PRIVATE_THEOREM_PRESENT:
[_private.LocalReuse.0.LocalReuse.zzz_probe_private]`, and it built again when
the injection was reversed.

The final scope review included the repository's later passage and trace
definitions. Three additional composition lemmas make shared-prefix replay,
certified interior rewriting, and halted-state absorption explicit on that
model. They import existing definitions and preserve their full state.
