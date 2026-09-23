# evidence_graph

AuthorityEffect: None. An index of source statements and independently checked
evidence. This tree consumes existing sources read-only and does not repair
their claims, change the seal, or confer authority through an aggregate pass.

The source snapshot and population are frozen before evidence dispositions
are assigned. Exact inherited prose is represented by a resolving source span,
its snapshot, Git blob, file digest, and span digest. It is not copied here.
Import and reference edges do not establish a semantic bridge.

The frozen source is `ed028912e0b06f73dd4c5bfe1bb7c2d0e6f3034f`: 2,665 tracked
files, 103 indexed research trees, and 23,426 nonblank public text blocks in
375 files. The public population is all Markdown under `paper/` and
`research/`, plus the root README, excluding the scaffold and this consumer.
The two excluded research directories in the tree index still contribute
their public prose. The three parked trees retain their declared status.

`evidence/coverage.md` is the readable report. Inventory completion means
every source block and tree has a disposition. **It does not mean every
headline is supported.** Only an explicit source/type/binder scope review
can mark a headline matched. Other statements, including substantive titles,
have individual unresolved rows; only neutral navigation headings are context.
The conservative unresolved count includes apparatus and historical text and
must not be read as a count of false mathematical claims.

Fresh captures contain 3,953 public theorem records from 23 compiled package
reports. They include generated public theorems and exclude compiler-internal
names. Every record includes the elaborated type, all term binders, axioms,
exact module population and source/build references. The report environment
reach includes the observer's apparatus imports and is labeled accordingly;
it is distinct from a product root's default-target import closure.

Thirty-one independent commands were run across 24 source trees: thirty
passed and one failed. `endogenous_demand` passed its 90 tests but its own
complete verifier failed its coverage thresholds (57.34% statements, 61.84%
branches). Its separate Lean build/report passed. The failure remains visible
and does not become successful computation evidence. A specialized pin check
is likewise never described as a complete tree verification. Other trees'
unexecuted commands remain explicitly unexecuted.

The native notion/bridge table's 30 rows are preserved with their original
classifications, separately from reviewed transition maps. A source's PROVED
label is not promoted to a reviewed semantic bridge. The stage ledger covers
0 through 6, the frontier includes all requested continuation channels, and
the dependent-work handoff names actual graph IDs. Section-3 source spans and
scope gaps are in `evidence/section3_handoff.json`; this consumer makes no
correction in the owner trees or sealed prose.

The import census has 35 direct native-import files in 22 trees. Four more
files contain comment-only mentions. The supplied count 38 had no named file
population, so its precise counting error cannot be reconstructed. The saved
header and compiler populations are the reproducible count; the unverified
number is retained as a discrepancy, not silently endorsed.

Large tables use deterministic gzip of canonical JSON. `evidence/artifacts.json`
records stored and decoded digests; `evidence/summary.json` is a small summary.
These commands run from this directory:

```text
python verify.py --check
python inventory.py --check
python graph.py --check
python corrections.py --check
python query.py --id claim:scoped:legal_replay
python query.py --source paper/paper_claim_ledger.md --line 128
python refresh.py --head HEAD --output /outside/checkout/current-head.json
```

`graph.py` regenerates twice from identical source and evidence inputs and
compares bytes. It rejects missing, extra and stale artifacts. The independent
block census is not inferred from accepted claim links. Source changes trigger
only their affected records and dependency descendants in the incremental
current-head view, while the entire source/headline/tree census is refreshed.
The historical graph remains intact. `refresh.py --previous` also detects
recovery after a change is reversed. The new consumer is an explicit 104th
tree at the execution head, not part of its own 103-tree source snapshot.

The Section 3 correction version is pending the owner merge and its local
checks. The full local verifier will refuse the missing review input until
that integration is complete. Once recorded, `versions/section3.json` will
import the twelve correction subjects from a later
source snapshot after that snapshot lands on `main`. The deliberate input
`correction_reviews.json` binds the corrected source spans, their scope,
remaining obligations, and local-check receipts to the tested tree. The
reader rejects unmerged sources, missing subjects, stale spans, failed checks
and checks of a different tree. These are scope corrections and custody
records; their mathematical obligations stay OPEN. The original graph and
compiled reports retain their original source snapshot. Run `corrections.py
--write` to regenerate this separate version twice and compare its bytes.

To reproduce the captures, create a separate checkout at the full source
snapshot, then run `capture.py --workspace SNAPSHOT_CHECKOUT --run-dir RUN_DIR
--mode core` and the corresponding `--mode research`. The runner executes
each named tree's own verifier; it does not certify that verifier's logic.
Use a full Git history and the packages' pinned installed toolchains. Tracked
outputs written by a source verifier are observed and restored only inside
that disposable checkout. Raw logs, absolute paths, interpreter identity and
elapsed time stay under RUN_DIR. Scientific records carry source bindings and
receipt digests, with no timestamps or machine paths. `scope_reviews.json`
is a deliberate review input and is never regenerated by the graph command.

The six schema examples and required negative controls live in the tests.
They are explicitly synthetic input mutations, not scientific receipts or
claims that a source theorem was edited. The local Lean result says only
that a path with strictly decreasing natural ranks cannot return to itself.
It neither proves the Python checker correct nor certifies source coverage.

The independent entry point is `python verify.py --check`, run here. The
canonical verifier checks this tree's local inputs, tests, strict typing, and
its explicitly named local Lean reports. Checks of other trees continue to
belong to those trees. Regenerating pins is a separate deliberate operation.
The first three input files are additionally frozen against their earlier
reachable commit, before evidence statuses were assigned. The capture and
scope-review inputs were pinned after observation and review. No hosted
verification or author merge authority is introduced.
